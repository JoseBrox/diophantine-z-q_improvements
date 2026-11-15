#!/usr/bin/env python3
"""Exact 81-coordinate quartic under abc and the stated arithmetic inputs.

The coefficient parameter B has degree zero. All rational coefficients are
cleared row by row to primitive integers. The complete polynomial is the
sum of the resulting quadratic squares. Python standard library only.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent
# A key is (power of fixed B, sorted tuple of coordinate indices).
def clean(p): return {k:Q(c) for k,c in p.items() if c}
def con(c): return {(0,()):Q(c)} if c else {}
def var(i): return {(0,(i,)):Q(1)}
def add(*ps):
    out=defaultdict(Q)
    for p in ps:
        for k,c in p.items():out[k]+=c
    return clean(out)
def scale(p,c):return clean({k:c*v for k,v in p.items()})
def mul(p,q):
    out=defaultdict(Q)
    for (i,m),a in p.items():
        for (j,n),b in q.items():out[i+j,tuple(sorted(m+n))]+=a*b
    return clean(out)
def sq(p):return mul(p,p)
def sub(p,q):return add(p,scale(q,-1))
def prim(p):
    p=clean(p)
    if not p:raise ValueError('Zero residual')
    d=lcm(*(c.denominator for c in p.values()))
    g=gcd(*(int(d*c) for c in p.values()))
    if p[min(p)]<0:g=-g
    return scale(p,Q(d,g))
def serial(p):
    return [dict(parameterPower=a,monomial=list(m),coefficient=str(c))
            for (a,m),c in sorted(p.items())]
def plus(*xs):return (add(*(x[0] for x in xs)),add(*(x[1] for x in xs)))
def neg(x):return (scale(x[0],-1),scale(x[1],-1))
def diff(x,y):return plus(x,neg(y))
def times(x,y):return (add(mul(x[0],y[0]),scale(mul(x[1],y[1]),2)),add(mul(x[0],y[1]),mul(x[1],y[0])))
def power2(x):return times(x,x)
def kconst(a,b=0):return (con(a),con(b))
def rational(p):return (p,{})
def ktimes(c,x):return times(kconst(c),x)
def conjugate(x):return (x[0],scale(x[1],-1))


def build(out:Path=HERE):
    coordinates=[];rows=[]
    def scalar(name):
        i=len(coordinates)+1;coordinates.append(dict(id=i,name=name));return var(i)
    def field(name):return (scalar(name+'.0'),scalar(name+'.1'))
    def row(name,p):
        p=prim(p)
        if max(len(m) for _,m in p)>2:raise ValueError('Not quadratic: '+name)
        rows.append(dict(id=len(rows)+1,name=name,terms=serial(p)))
    def krow(name,p):row(name+'.0',p[0]);row(name+'.1',p[1])
    one=con(1);oneK=kconst(1);zeroK=kconst(0)
    B={(1,()):Q(1)}
    X=scalar('input');I0=scalar('inputComparison.real');lam=scalar('slope')
    S=field('common.S');TH=field('common.T');fH=field('common.f');F0=field('common.g')
    f=field('pair.f');h=field('pair.h');F=field('pair.g');k=field('pair.k');s=field('pair.slope')
    L=field('ratio.primary');L0=field('ratio.alternate')
    FH=field('square.common.f');FG=field('square.common.g')
    FU=field('square.pair.f');FV=field('square.pair.g')
    C2=field('square.comparison');I2=field('square.input')
    T=scalar('height.trace')
    sh=scalar('height.sumSquares');ph=scalar('height.product')
    D=kconst(11,-6); a=kconst(Q(57,8),Q(-7,2)); b=kconst(Q(-165,8),Q(417,32))
    AP=plus(power2(a),D);BP=diff(power2(a),D)
    Lf=ktimes(2,times(times(b,D),diff(times(a,TH),b)))
    Lg=ktimes(2,times(times(b,D),plus(times(a,S),b)))
    Qf=plus(times(times(a,AP),times(S,TH)),times(times(b,AP),S),neg(times(times(b,BP),TH)),ktimes(4,times(power2(a),D)))
    Qg=plus(neg(times(times(a,AP),times(S,TH))),neg(times(times(b,BP),S)),times(times(b,AP),TH),neg(ktimes(4,times(power2(a),D))))
    krow('common.first',diff(times(Lf,fH),Qf))
    krow('common.second',diff(times(Lg,F0),Qg))
    krow('common.third',plus(times(power2(D),times(fH,F0)),times(times(a,D),plus(fH,F0)),times(a,times(S,TH)),times(b,diff(S,TH)),D))
    # The reciprocal pair includes O=(f,h)=(0,0). Its difference is finite.
    krow('pair.cubic',plus(power2(h),neg(f),times(D,times(f,FU))))
    krow('pair.secant',diff(times(s,diff(f,F)),plus(h,k)))
    krow('pair.tangent',plus(times(s,diff(h,k)),neg(oneK),times(D,plus(FU,times(f,F),FV))))
    for name,x,y in [('common.f',fH,FH),('common.g',F0,FG),('pair.f',f,FU),('pair.g',F,FV)]:
        krow('square.'+name,diff(y,power2(x)))
    # Both equations on each branch retain the identity case and avoid division.
    krow('ratio.primary.raw',plus(times(h,L),times(f,S)))
    krow('ratio.primary.regular',plus(times(diff(oneK,times(D,FU)),L),times(h,S)))
    krow('ratio.alternate.raw',plus(times(k,L0),times(F,TH)))
    krow('ratio.alternate.regular',plus(times(diff(oneK,times(D,FV)),L0),times(k,TH)))
    C=diff(L,conjugate(L0)); I=(I0,L[1]); beta=sub(L[0],I0)
    row('inputComparison',add(I0,scale(L[0],-1),sq(X),B))
    krow('square.comparison',diff(C2,power2(C)))
    krow('square.input',diff(I2,power2(I)))
    root_c=plus(power2(s),times(D,plus(f,F)))
    row('height.trace',sub(T,scale(root_c[0],2)))
    row('height.sumSquares',sub(sh,add(sq(beta),sq(T))))
    row('height.product',sub(ph,mul(beta,T)))
    for j in range(2):
        pfx=f'detector{j}.'
        if j==0:t=lam
        else:
            t=scalar(pfx+'argument');row(pfx+'argument',add(t,scale(lam,-1),scale(sq(sh),-1),scale(sq(ph),2)))
        R=scalar(pfx+'contactSquareShift');Z=scalar(pfx+'contactSumShift')
        w=scalar(pfx+'inverseWeight');w2=scalar(pfx+'inverseWeightSquare');w3=scalar(pfx+'inverseWeightCube')
        A1=field(pfx+'factor1');A2=field(pfx+'factor2');Omega=field(pfx+'product')
        eta=scalar(pfx+'trace');bpole=scalar(pfx+'poleInput')
        e=scalar(pfx+'pole.e');u=scalar(pfx+'pole.u');p=scalar(pfx+'pole.p');v=scalar(pfx+'pole.v');q=scalar(pfx+'pole.q');p2=scalar(pfx+'pole.pSquare');q2=scalar(pfx+'pole.qSquare')
        row(pfx+'contactSquare',add(R,scale(sq(t),-1),scale(t,2)))
        row(pfx+'contactSum',add(mul(R,Z),Z,scale(sq(R),-1),scale(R,35)))
        row(pfx+'inverseContact',add(mul(add(R,one),w),scale(sq(Z),-1),scale(Z,-24)))
        row(pfx+'inverseWeightSquare',sub(w2,sq(w)))
        row(pfx+'inverseWeightCube',sub(w3,mul(w,w2)))
        for nr,A,comp,low,high in [(1,A1,C2,FH,FU),(2,A2,I2,conjugate(FG),conjugate(FV))]:
            rhs=plus(rational(sq(w2)),times(rational(w3),comp),times(rational(w2),low),power2(high))
            krow(pfx+f'factor{nr}',diff(times(rational(w3),A),rhs))
        krow(pfx+'product',diff(times(rational(add(R,one)),Omega),times(A1,A2)))
        row(pfx+'trace',add(sq(Omega[0]),scale(mul(Omega[0],eta),-2),scale(sq(Omega[1]),-2)))
        row(pfx+'poleInput',sub(mul(w3,bpole),sq(eta)))
        row(pfx+'pole.pSquare',sub(p2,sq(p)))
        row(pfx+'pole.first',add(con(289),scale(e,34),scale(sq(e),-3),scale(mul(bpole,p2),-17)))
        row(pfx+'pole.factor',add(scale(e,17),scale(mul(e,bpole),-1),scale(mul(u,v),-17)))
        row(pfx+'pole.qSquare',sub(q2,sq(q)))
        row(pfx+'pole.second',add(sq(u),scale(mul(u,v),34),scale(mul(bpole,q2),-17),scale(sq(v),-867)))
    # An invertible rational change of the six common-chart component rows.
    # The exact matrix and determinant are checked independently; it does not
    # change any coordinate, input, parameter, or common zero set.
    reduction=json.loads((HERE/'common-row-reduction.json').read_text())
    base=[{(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient'])
           for t in r['terms']} for r in rows[:6]]
    for i,coeffs in enumerate(reduction['matrix']):
        rows[i]['terms']=serial(prim(add(*(scale(p,Q(c)) for p,c in zip(base,coeffs)))))
    assert len(coordinates)==81,(len(coordinates),len(rows))
    assert len(rows)==73,len(rows)
    full=defaultdict(Q)
    for r in rows:
        p={(x['parameterPower'],tuple(x['monomial'])):Q(x['coefficient']) for x in r['terms']}
        for key,c in sq(p).items():full[key]+=c
    full=clean(full); profiles=defaultdict(dict)
    for (j,m),c in full.items():profiles[m][j]=int(c)
    assert {i for _,m in full for i in m}==set(range(1,82))
    assert max(len(m) for _,m in full)==4
    assert all(c.denominator==1 for c in full.values())
    const=profiles[()][0]; assert profiles[()][2]==1
    fixedmax=max(abs(v[0]) for v in profiles.values() if set(v)=={0})
    linear=[(m,p) for m,p in profiles.items() if 1 in p]
    # Certify max(fixedmax,B^2+const) against each |a B+c| for all B>=3.
    # Below the switch, a linear function is bounded at the two endpoints;
    # above it, B^2+const-|a|B-|c| is increasing once B>=|a|/2.
    switch=max(3,isqrt(max(0,fixedmax-const))+1)
    for m,p in linear:
        aa=abs(p[1]);cc=abs(p.get(0,0))
        assert aa*3+cc<=max(fixedmax,9+const)
        if switch>3:assert aa*(switch-1)+cc<=fixedmax
        assert switch*switch+const>=aa*switch+cc and 2*switch>=aa
    # Constant profiles are nonzero and the only variable profiles have no positive root.
    assert all(set(p) in ({0},{1},{0,2}) for p in profiles.values())
    assert all(p[0]>0 and p[2]>0 for p in profiles.values() if set(p)=={0,2})
    report=dict(schema='abc81-exact-construction/v1',variables=81,quadraticRows=73,degree=4,
                integerContent=gcd(*(abs(int(c)) for c in full.values())),
                ordinaryMonomialsForEveryPositiveB=len(profiles),parameterSeparatedTerms=len(full),
                constantCoefficient=str(const),largestFixedCoefficient=str(fixedmax),
                exactHeight=f'max({fixedmax},B^2+{const})',heightSwitchInteger=switch,
                inputMap='beta=X^2+B',comparisonArguments=['lambda','lambda+beta^4+T^4'],ellipticIndexDomain='(1/2) Z, including torsion index zero',
                definingThreshold='Ineffective; sufficiently large fixed odd B; B=3 is not certified',
                arithmeticScope='Ordinary rational abc, the retained elliptic group, pole obstruction and prepared nonzero realization, simultaneous prime-pattern inputs. The all-point trace-height lemma is proved separately from von Buhren (2017), Theorem 1.1.',
                squareRootsNotAssumed='The reciprocal auxiliary points need not have square abscissas.',
                checksScope='Exact finite polynomial specification and coefficients only; arithmetic proof is separate.')
    parameter=dict(symbol='B',quantified=False,domain='fixed odd integer B>=3',sufficientThresholdEffective=False)
    system=dict(format='integer-quadratic-family-abc81-v25',variables=81,inputCoordinate=1,fixedParameter=parameter,coordinates=coordinates,residuals=rows)
    polynomial=dict(format='integer-quartic-family-abc81-v25',variables=81,degree=4,inputCoordinate=1,fixedParameter=parameter,coordinates=coordinates,terms=serial(full))
    out.mkdir(parents=True,exist_ok=True)
    for filename,obj in [('quadratic-family.json',system),('polynomial-family.json',polynomial),('construction-report.json',report)]:
        (out/filename).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return system,polynomial,report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE);a=ap.parse_args();build(a.output)
