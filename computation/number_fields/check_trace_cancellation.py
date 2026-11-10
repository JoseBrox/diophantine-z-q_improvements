#!/usr/bin/env python3
"""Exact identities for complex multiplication and trace cancellation.

The universal computations take place in
Q[D,x,x^-1,y,i]/(y^2-x^3+D*x, i^2+1).
The finite arithmetic certificate proves that the displayed project point
has infinite order using reductions at17 and23. Height growth and rank
statements are proved in the companion paper, not inferred from samples.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import json


def clean(p):
    return {m:c for m,c in p.items() if c}


def mono(d=0, x=0, y=0, i=0, c=1):
    return {(d,x,y,i): F(c)} if c else {}


def add(*ps):
    out = {}
    for p in ps:
        for m,c in p.items():
            out[m] = out.get(m,F(0))+c
    return clean(out)


def scale(c,p):
    return clean({m:F(c)*v for m,v in p.items()})


def mul(a,b):
    out = {}
    for (d1,x1,y1,i1),c1 in a.items():
        for (d2,x2,y2,i2),c2 in b.items():
            yp,yr = divmod(y1+y2,2)
            ip,ir = divmod(i1+i2,2)
            for j in range(yp+1):
                m=(d1+d2+j,x1+x2+3*yp-2*j,yr,ir)
                c=c1*c2*comb(yp,j)*(-1)**(ip+j)
                out[m]=out.get(m,F(0))+c
    return clean(out)


def power(a,n):
    out=mono()
    for _ in range(n):
        out=mul(out,a)
    return out


def conjugate(p):
    return {m:c*(-1)**m[3] for m,c in p.items()}


# Q(sqrt(2),i), in the order1,sqrt(2),i,i*sqrt(2).
ZERO=(F(0),)*4
ONE=(F(1),F(0),F(0),F(0))
II=(F(0),F(0),F(1),F(0))


def c4(a=0,b=0,c=0,d=0):
    return tuple(map(F,(a,b,c,d)))


def add4(*xs):
    return tuple(sum((x[j] for x in xs),F(0)) for j in range(4))


def neg4(a):
    return tuple(-x for x in a)


def mul4(a,b):
    out=[F(0)]*4
    for j,c in enumerate(a):
        for k,d in enumerate(b):
            sr=(j&1)+(k&1)
            ir=(j>>1)+(k>>1)
            index=(sr%2)+2*(ir%2)
            out[index]+=c*d*(2**(sr//2))*(-1)**(ir//2)
    return tuple(out)


def inv4(a):
    assert a!=ZERO
    columns=[mul4(a,tuple(F(int(j==k)) for j in range(4))) for k in range(4)]
    rows=[[columns[k][j] for k in range(4)]+[F(j==0)] for j in range(4)]
    for k in range(4):
        pivot=next(j for j in range(k,4) if rows[j][k])
        rows[k],rows[pivot]=rows[pivot],rows[k]
        q=rows[k][k]
        rows[k]=[z/q for z in rows[k]]
        for j in range(4):
            if j==k:continue
            q=rows[j][k]
            rows[j]=[u-q*v for u,v in zip(rows[j],rows[k])]
    result=tuple(row[4] for row in rows)
    assert mul4(a,result)==ONE
    return result


def div4(a,b):
    return mul4(a,inv4(b))


def pow4(a,n):
    if n<0:return pow4(inv4(a),-n)
    out=ONE
    for _ in range(n):out=mul4(out,a)
    return out


def sigma4(a):
    return a[:2]+tuple(-x for x in a[2:])


def evaluate(p,D,x,y):
    out=ZERO
    for (de,xe,ye,ie),coefficient in p.items():
        value=c4(coefficient)
        for base,e in ((D,de),(x,xe),(y,ye),(II,ie)):
            value=mul4(value,pow4(base,e))
        out=add4(out,value)
    return out


def curve4(P,D):
    if P is None:return True
    x,y=P
    return pow4(y,2)==add4(pow4(x,3),neg4(mul4(D,x)))


def add_point4(P,Q,D):
    if P is None:return Q
    if Q is None:return P
    x,y=P;xx,yy=Q
    if x==xx and y==neg4(yy):return None
    numerator=add4(mul4(c4(3),pow4(x,2)),neg4(D)) if P==Q else add4(yy,neg4(y))
    denominator=mul4(c4(2),y) if P==Q else add4(xx,neg4(x))
    slope=div4(numerator,denominator)
    X=add4(pow4(slope,2),neg4(x),neg4(xx))
    Y=add4(mul4(slope,add4(x,neg4(X))),neg4(y))
    out=X,Y
    assert curve4(out,D)
    return out


def times_point4(n,P,D):
    out=None
    for _ in range(n):out=add_point4(out,P,D)
    return out


def iota4(P):
    if P is None:return None
    return neg4(P[0]),mul4(II,P[1])


def ff_add(P,Q,p,D):
    if P is None:return Q
    if Q is None:return P
    x,y=P;xx,yy=Q
    if x==xx and (y+yy)%p==0:return None
    m=((3*x*x-D)*pow(2*y,-1,p) if P==Q else (yy-y)*pow(xx-x,-1,p))%p
    X=(m*m-x-xx)%p
    return X,(m*(x-X)-y)%p


def ff_order(P,p,D):
    Q=None
    for n in range(1,2*p+5):
        Q=ff_add(Q,P,p,D)
        if Q is None:return n
    raise AssertionError('Hasse-size order bound exceeded')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('trace-cancellation-certificate.json'))
    args=ap.parse_args()
    one=mono(); x=mono(x=1); y=mono(y=1); D=mono(d=1); i=mono(i=1)
    assert add(power(y,2),scale(-1,power(x,3)),mul(D,x))=={}
    ix=scale(-1,x); iy=mul(i,y)
    assert add(power(iy,2),scale(-1,power(ix,3)),mul(D,ix))=={}
    assert power(i,2)==scale(-1,one)
    # C=(1+iota)P, using the chord joining P and iota(P).
    cx=scale(F(-1,2),mul(mul(i,add(power(x,2),scale(-1,D))),mono(x=-1)))
    cy=scale(F(-1,4),mul(mul(mul(add(one,i),y),add(power(x,2),D)),mono(x=-2)))
    assert add(power(cy,2),scale(-1,power(cx,3)),mul(D,cx))=={}
    slope=scale(F(1,2),mul(mul(add(one,scale(-1,i)),y),mono(x=-1)))
    assert power(slope,2)==cx
    assert add(mul(slope,add(x,scale(-1,cx))),scale(-1,y))==cy
    assert conjugate(cx)==scale(-1,cx)
    assert conjugate(cy)==scale(-1,mul(i,cy))
    # Clear denominators to check (1-iota)(1+iota)P=[2]P.
    x2_numerator=power(add(power(x,2),D),2)
    xcomposition=add(scale(4,mul(mul(i,power(y,2)),add(power(cx,2),scale(-1,D)))),scale(-2,mul(cx,x2_numerator)))
    assert xcomposition=={}
    y2_numerator=add(mul(add(scale(3,power(x,2)),scale(-1,D)),add(scale(4,mul(x,power(y,2))),scale(-1,x2_numerator))),scale(-8,power(y,4)))
    ycomposition=add(scale(-8,mul(mul(mul(add(one,scale(-1,i)),cy),add(power(cx,2),D)),power(y,3))),scale(-4,mul(power(cx,2),y2_numerator)))
    assert ycomposition=={}
    # Formal group decomposition: A=Q+sigmaQ and B=-i(Q-sigmaQ).
    A=(one,one); B=(scale(-1,i),i)
    sigma=lambda pair:(conjugate(pair[1]),conjugate(pair[0]))
    assert sigma(A)==A and sigma(B)==B
    assert tuple(add(a,mul(i,b)) for a,b in zip(A,B))==(scale(2,one),{})

    actual_D=c4(11,-6)
    P=(c4(F(57,8),F(-28,8)),c4(F(-660,32),F(417,32)))
    R0=(c4(1,1),c4(0,2))
    assert curve4(P,actual_D) and curve4(R0,actual_D)
    assert add_point4(R0,R0,actual_D)==P
    C=add_point4(P,iota4(P),actual_D)
    assert C==(evaluate(cx,actual_D,*P),evaluate(cy,actual_D,*P))
    trace_samples=[]
    for n in range(1,5):
        Q=times_point4(n,C,actual_D)
        assert add4(Q[0],sigma4(Q[0]))==ZERO
        trace_samples.append(n)
    for n in (1,2):
        Q=times_point4(2*n,P,actual_D)
        R=times_point4(4*n,P,actual_D)
        points=(Q,iota4(Q),R,iota4(R))
        assert all(curve4(T,actual_D) for T in points)
        assert len(set(points))==4 and len({T[0] for T in points})==4
        assert add4(*(T[0] for T in points))==ZERO

    reductions=[]
    for p,sqrt2 in ((17,6),(23,5)):
        dd=(11-6*sqrt2)%p
        assert dd and p not in (2,7)
        pp=((57-28*sqrt2)*pow(8,-1,p)%p,(-660+417*sqrt2)*pow(32,-1,p)%p)
        assert (pp[1]**2-pp[0]**3+dd*pp[0])%p==0
        count1=1+sum(1 for xx in range(p) for yy in range(p) if (yy*yy-xx**3+dd*xx)%p==0)
        count2=1+sum(1 if (value:=(xx**3-dd*xx)%p)==0 else 2 if pow(value,(p-1)//2,p)==1 else 0 for xx in range(p))
        assert count1==count2
        order=ff_order(pp,p,dd)
        reductions.append({'prime':p,'sqrt2_residue':sqrt2,'D_residue':dd,'P_residue':list(pp),'curve_order':count1,'point_order':order})
    assert reductions[0]['curve_order']==20 and reductions[0]['point_order']==5
    assert reductions[1]['curve_order']==24 and reductions[1]['point_order']==3
    assert reductions[1]['curve_order']%5!=0
    report={
        'status':'PASS',
        'universal_ring':'Q[D,x,x^-1,y,i]/(y^2-x^3+D*x,i^2+1)',
        'universal_identities':[
            'iota preserves E_D and iota^2=[-1]',
            'chord formula for (1+iota)P',
            '(1+iota)P lies on E_D',
            'sigma((1+iota)P)=-iota((1+iota)P)',
            '(1-iota)(1+iota)P=[2]P, both coordinates after clearing',
            'rank decomposition 2Q=(Q+sigmaQ)+iota[-iota(Q-sigmaQ)]'],
        'project_point':{'D':list(map(str,actual_D)),'P':[list(map(str,t)) for t in P],
                         'C':[list(map(str,t)) for t in C],
                         'P_is_double_of_R0':True},
        'nontorsion_certificate':{'method':'Reduction order5 at17 forces a5-primary torsion component if P were torsion, contradicting good reduction injection at23 with group order24.','reductions':reductions,'conclusion':'P has infinite order, unconditionally.'},
        'supplementary_samples':{'trace_zero_multiples':trace_samples,'four_distinct_doubled_points_n':[1,2]},
        'general_theorems':'Rank doubling and height-growth/zero-trace conclusions are proved in the companion paper; finite samples do not replace those proofs.',
        'definability_scope':'Obstruction to unchanged elliptic height and rank inputs after base extension. No counterexample to Diophantine definability of a ring of integers is asserted.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'universal_identities':len(report['universal_identities']),'nontorsion_certificate':True,'reductions':reductions}))


if __name__=='__main__':main()
