#!/usr/bin/env python3
"""Exact checks for the scalar translated-secant chart.

The modular rank calculation concerns only the specified chart interface,
not the complete 195-coordinate system or all possible extra helpers.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import random


def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def neg(x):
    return -x[0], -x[1]


def mul(x, y):
    return x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def inv(x):
    n=x[0]*x[0]-2*x[1]*x[1]
    assert n
    return x[0]/n, -x[1]/n


def scale(c, x):
    return c*x[0], c*x[1]


def interface_relations(v):
    def pair(i):return (v[2*i],v[2*i+1])
    F,G,s,t,h,d,S,Z,F2,G2=[pair(i) for i in range(10)]
    D=(11,-6);p=add(add(h,s),t)
    pairs=[add(d,neg(mul(p,F))),
           add(d,neg(mul(h,G))),
           add(add(mul(D,add(F,G)),neg(mul(add(s,neg(t)),h))),mul(t,t)),
           add(add((1,0),neg(mul(d,add(s,neg(t))))),mul(D,mul(F,G))),
           add(F2,neg(mul(F,F))),add(G2,neg(mul(G,G))),
           add(mul(F,d),neg(mul(p,F2))),
           add(mul(G,d),neg(mul(h,G2)))]
    return [a for pair in pairs for a in pair]+[v[20]-mul(Z,d)[0]]


def exact_torsion():
    one=(Q(1), Q(0)); zero=(Q(0), Q(0)); D=(Q(11), Q(-6))
    x=(Q(1), Q(1)); y=(Q(0), Q(2))
    assert mul(y,y)==add(mul(mul(x,x),x),neg(mul(D,x)))
    F=inv(x); G=neg(mul(x,inv(D)))
    s=mul(y,inv(x)); t=neg(s); h=d=Z=e=zero
    p=add(add(h,s),t)
    assert d==mul(p,F)==mul(h,G)
    assert mul(D,add(F,G))==add(mul(add(s,neg(t)),h),neg(mul(t,t)))
    assert one==add(mul(d,add(s,neg(t))),neg(mul(D,mul(F,G))))
    S=s
    assert add(add(mul(e,add(h,s)),neg(Z)),scale(Q(2),mul(S,d)))==zero
    assert e==mul(Z,d)
    # Q=U-V=(0,0), Z=0. Both numerator points remain non-torsion.
    return {k:[str(a) for a in v] for k,v in
            dict(D=D,F=F,G=G,s=s,t=t,h=h,d=d,Z=Z,e=e,S=S).items()}


def exact_nontorsion_false_point():
    D=(Q(11),Q(-6));zero=(Q(0),Q(0))
    U=((Q(1),Q(1)),(Q(0),Q(2)))
    V=((Q(57,8),Q(-7,2)),(Q(-165,8),Q(417,32)))
    for x,y in (U,V):
        assert mul(y,y)==add(mul(mul(x,x),x),neg(mul(D,x)))
    slope=mul(add(scale(Q(3),mul(U[0],U[0])),neg(D)),inv(scale(Q(2),U[1])))
    xd=add(mul(slope,slope),scale(Q(-2),U[0]))
    yd=add(mul(slope,add(U[0],neg(xd))),neg(U[1]))
    assert (xd,yd)==V
    F=inv(U[0]);G=inv(V[0]);s=mul(U[1],F);t=mul(V[1],G)
    h=mul(mul(F,add(s,t)),inv(add(G,neg(F))));d=mul(h,G)
    p=add(add(h,s),t);a=mul(h,p)
    q=add(add(h,s),neg(inv(d)))
    assert a==U[0] and q==s
    S=s;Z=(Q(1),Q(0));e=mul(Z,d)
    assert all(a!=zero for a in (F,G,add(F,neg(G)),s,t,d,q,S,Z))
    v=[a for pair in (F,G,s,t,h,d,S,Z,mul(F,F),mul(G,G)) for a in pair]+[e[0]]
    assert all(r==0 for r in interface_relations(v))
    residual=add(add(mul(e,add(h,s)),neg(Z)),scale(Q(2),mul(S,d)))
    assert residual!=zero
    true_Z=scale(Q(-2),mul(S,inv(q)))
    assert true_Z==(Q(-2),Q(0))
    return {'coordinates':[str(x) for x in v],
            'true_Z':[str(x) for x in true_Z],
            'false_Z':[str(x) for x in Z],
            'scalar_residual':[str(x) for x in residual],
            'difference_abscissa':[str(x) for x in a],
            'guards_checked':['F!=0','G!=0','F!=G','s!=0','t!=0','d!=0','q!=0','S!=0','Z!=0'],
            'point_relation':'V=2U, so U-V=-U is nontorsion under the retained fixed-curve group premise.'}


def field_points(p, D):
    squares={}
    for y in range(1,p):
        squares.setdefault(y*y % p,[]).append(y)
    return [(x,y) for x in range(1,p)
            for y in squares.get((x*x*x-D*x) % p,[])]


def rank_rows(rows, p):
    pivots={}
    selected=[]
    for row_number, row in enumerate(rows):
        row=[v % p for v in row]
        for i in range(len(row)):
            value=row[i]
            if not value:
                continue
            if i in pivots:
                old=pivots[i]
                row=[(a-value*b) % p for a,b in zip(row,old)]
            else:
                inverse=pow(value,-1,p)
                pivots[i]=[(inverse*v) % p for v in row]
                selected.append(row_number)
                break
    return len(pivots),selected,pivots


def contact_graph_rank():
    # Split field coordinates make the two geometric embeddings independent.
    prime=1009
    assert all(prime % n for n in range(2,32))
    rho=next(r for r in range(prime) if r*r % prime==2)
    ds=[(11-6*rho) % prime,(11+6*rho) % prime]
    point_lists=[field_points(prime,D) for D in ds]
    rng=random.Random(20261117)
    def slot(D, points):
        while True:
            (x,y),(xx,yy)=rng.choices(points,k=2)
            F=pow(x,-1,prime);G=pow(xx,-1,prime)
            if F==G:continue
            s=y*F % prime;t=yy*G % prime
            h=F*(s+t)*pow((G-F) % prime,-1,prime) % prime
            d=h*G % prime
            if not d:continue
            q=(h+s-pow(d,-1,prime)) % prime
            if not q:continue
            S=rng.randrange(1,prime)
            Z=-2*S*pow(q,-1,prime) % prime
            assert (d-(h+s+t)*F) % prime==0
            assert (D*(F+G)-(s-t)*h+t*t) % prime==0
            assert (d*(s-t)-D*F*G-1) % prime==0
            assert (Z*d*(h+s)-Z+2*S*d) % prime==0
            return [F,G,s,t,h,d,S,Z,F*F % prime,G*G % prime],Z*d % prime
    names=[n+'.'+str(i) for n in ('F','G','s','t','h','d','S','Z','F2','G2') for i in (0,1)]+['e0']
    monomials=[()]+[(i,) for i in range(21)]+[(i,j) for i in range(21) for j in range(i,21)]
    rows=[];values=[]
    half=pow(2,-1,prime);inv2rho=pow(2*rho,-1,prime)
    for _ in range(300):
        (plus,ep),(minus,em)=[slot(D,ps) for D,ps in zip(ds,point_lists)]
        v=[]
        for a,b in zip(plus,minus):
            v.extend([(a+b)*half % prime,(a-b)*inv2rho % prime])
        v.append((ep+em)*half % prime)
        values.append(v)
        rows.append([1 if not m else v[m[0]] if len(m)==1 else v[m[0]]*v[m[1]] % prime for m in monomials])
    rank,selected,pivots=rank_rows(rows,prime)
    assert len(monomials)==253 and rank==236
    # Seventeen known quadrics: eight chart rows, four square definitions,
    # four saturated chart identities and e0=(Z*d)_0.
    # Check their coefficient rank directly by polynomial interpolation
    # on the standard 0/e_i/e_i+e_j evaluations (degree at most two).
    def known(v):
        return [a % prime for a in interface_relations(v)]
    z=[0]*21;constant=known(z)
    coeffs=[[c] for c in constant]
    linear=[];diagonal=[]
    for i in range(21):
        v=z.copy();v[i]=1;plus=known(v);v[i]=-1;minus=known(v)
        linear.append([(a-b)*half % prime for a,b in zip(plus,minus)])
        diagonal.append([(a+b-2*c)*half % prime for a,b,c in zip(plus,minus,constant)])
    for col in linear:
        for row,x in zip(coeffs,col):row.append(x)
    for i in range(21):
        for j in range(i,21):
            if i==j:col=diagonal[i]
            else:
                v=z.copy();v[i]=v[j]=1;k=known(v)
                col=[(k[r]-constant[r]-linear[i][r]-linear[j][r]-diagonal[i][r]-diagonal[j][r]) % prime for r in range(17)]
            for row,x in zip(coeffs,col):row.append(x)
    known_rank,_,known_pivots=rank_rows(coeffs,prime)
    assert known_rank==17
    assert all(sum(a*b for a,b in zip(row,c)) % prime==0 for row in rows for c in coeffs)
    columns=sorted(pivots)
    minor=[[rows[i][j] for j in columns] for i in selected]
    determinant=1
    for j in range(len(minor)):
        pivot=next(i for i in range(j,len(minor)) if minor[i][j] % prime)
        if pivot!=j:
            minor[j],minor[pivot]=minor[pivot],minor[j];determinant=-determinant
        c=minor[j][j] % prime;determinant=determinant*c % prime
        inverse=pow(c,-1,prime)
        for i in range(j+1,len(minor)):
            f=minor[i][j]*inverse % prime
            if f:
                for k in range(j+1,len(minor)):
                    minor[i][k]=(minor[i][k]-f*minor[j][k]) % prime
    assert determinant
    return {'prime':prime,'rho':rho,'coordinate_names':names,
            'coordinates':21,'degree_two_monomials':253,'sample_rows':300,
            'evaluation_rank':rank,'known_relation_rank':known_rank,
            'quadratic_relation_dimension':len(monomials)-rank,'seed':20261117,
            'evaluation_sha256':sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),
            'selected_rows':selected,
            'selected_columns':columns,'nonzero_minor_determinant_mod_prime':determinant,
            'evaluation_points':[values[i] for i in selected],
            'scope':'These chart outputs, free reference S, reciprocal-square outputs and e0 only. Other coordinates or a different helper are outside this obstruction.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--manuscript',type=Path,default=Path(__file__).with_name('half_scalar_helper.tex'))
    args=parser.parse_args()
    result={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'manuscript_sha256':sha256(args.manuscript.read_bytes()).hexdigest(),
            'false_torsion_chart':exact_torsion(),'nontorsion_false_point':exact_nontorsion_false_point(),
            'one_component_quadratic_interface':contact_graph_rank(),
            'limitations':'No lower bound for the full195 source or arbitrary quartics; no new variable-count result.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='one_component_quadratic_interface'},indent=2))
    print(json.dumps({k:v for k,v in result['one_component_quadratic_interface'].items() if k not in ('selected_rows','selected_columns','coordinate_names','evaluation_points')},indent=2))


if __name__=='__main__':main()
