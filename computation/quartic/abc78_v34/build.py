#!/usr/bin/env python3
"""Exact 78-coordinate quartic under ordinary abc and the stated arithmetic inputs.

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
from reference import equations as reference_equations
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
    X=scalar('input');lam=scalar('slope')
    S=field('common.S');TH=field('common.T');fH=field('common.f')
    f=field('pair.f');h=field('pair.h');F=field('pair.g');k=field('pair.k');s=field('pair.slope')
    L=field('ratio.primary');L0=field('ratio.alternate')
    FH=field('square.common.f');FG=field('square.common.g')
    FU=field('square.pair.f');FV=field('square.pair.g')
    C2=field('square.comparison');I2=field('square.input')
    T=scalar('height.trace')
    sh=scalar('height.inputSquare');ph=scalar('height.inputFourth')
    D=kconst(11,-6); a=kconst(Q(57,8),Q(-7,2)); b=kconst(Q(-165,8),Q(417,32))
    krow('common.fSquare',diff(FH,power2(fH)))
    r1,r2,r3,_,_=reference_equations(fH,S,FH,FG,TH)
    krow('common.first',r1);krow('common.second',r2);krow('common.third',r3)
    # The reciprocal pair includes O=(f,h)=(0,0). Its difference is finite.
    krow('pair.cubic',plus(power2(h),neg(f),times(D,times(f,FU))))
    krow('pair.secant',diff(times(s,diff(f,F)),plus(h,k)))
    krow('pair.tangent',plus(times(s,diff(h,k)),neg(oneK),times(D,plus(FU,times(f,F),FV))))
    for name,x,y in [('pair.f',f,FU),('pair.g',F,FV)]:
        krow('square.'+name,diff(y,power2(x)))
    # Both equations on each branch retain the identity case and avoid division.
    krow('ratio.primary.raw',plus(times(h,L),times(f,S)))
    krow('ratio.primary.regular',plus(times(diff(oneK,times(D,FU)),L),times(h,S)))
    krow('ratio.alternate.raw',plus(times(k,L0),times(F,TH)))
    krow('ratio.alternate.regular',plus(times(diff(oneK,times(D,FV)),L0),times(k,TH)))
    C=diff(L,conjugate(L0)); beta=add(sh,con(3)); I=diff(L,rational(beta))
    krow('square.comparison',diff(C2,power2(C)))
    krow('square.input',diff(I2,power2(I)))
    root_c=plus(power2(s),times(D,plus(f,F)))
    row('height.trace',sub(T,scale(root_c[0],2)))
    row('height.inputSquare',sub(sh,sq(X)))
    row('height.inputFourth',sub(ph,sq(sh)))
    for j in range(2):
        pfx=f'detector{j}.'
        if j==0:t=lam
        else:
            t=scalar(pfx+'argument');row(pfx+'argument',add(t,scale(lam,-1),scale(B,-1),scale(sq(ph),-1),scale(sq(T),-1)))
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
        row(pfx+'pole.first',add(sq(e),mul(bpole,p2),con(-1)))
        row(pfx+'pole.factor',add(mul(u,v),scale(e,-1),mul(e,bpole)))
        row(pfx+'pole.qSquare',sub(q2,sq(q)))
        row(pfx+'pole.second',add(sq(u),scale(sq(v),-1),scale(mul(bpole,q2),-1)))

    def require(ok,message):
        if not ok: raise AssertionError(message)
    require(len(coordinates)==78,'Coordinate count')
    require(len(rows)==70,'Quadratic row count')
    full=defaultdict(Q)
    for rr in rows:
        pp={(x['parameterPower'],tuple(x['monomial'])):Q(x['coefficient']) for x in rr['terms']}
        for key,c in sq(pp).items():full[key]+=c
    full=clean(full)
    require(max(len(m) for _,m in full)==4,'Exact quartic degree')
    require(all(c.denominator==1 for c in full.values()),'Integral coefficients')
    require({i for _,m in full for i in m}==set(range(1,79)),'Every coordinate occurs')
    require(full.get((0,(1,1,1,1)))==1,'Unit coefficient of the fourth power of the input')
    require(not any(j and m==(1,1,1,1) for j,m in full),'Parameter-independent unit coefficient')
    profiles=defaultdict(dict)
    for (j,m),c in full.items():profiles[m][j]=int(c)
    # No nonzero profile can vanish at a positive fixed integer parameter.
    for m,p in profiles.items():
        require(set(p).issubset({0,1,2}),'Unexpected parameter degree')
        if set(p)=={0}:require(p[0]!=0,'Zero constant profile')
        elif 2 not in p:
            a=p.get(1,0);c=p.get(0,0)
            require(a!=0 and (a*c>=0 or -Q(c,a)<=0),'Possible positive parameter root')
        else:
            require(p[2]>0 and p.get(1,0)>=0 and p.get(0,0)>=0,'Uncertified quadratic profile')
    const=profiles[()][0]
    require(profiles[()].get(2)==1 and 1 not in profiles[()],'Constant coefficient form')
    fixedmax=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
    switch=max(1,isqrt(max(0,fixedmax-const))+1)
    for m,p in profiles.items():
        if 1 not in p:continue
        aa=abs(p[1]);cc=abs(p.get(0,0))
        require(aa+cc<=max(fixedmax,1+const),'Height at parameter one')
        if switch>1:require(aa*(switch-1)+cc<=fixedmax,'Height below switch')
        require(switch*switch+const>=aa*switch+cc and 2*switch>=aa,'Height above switch')
    parameter=dict(symbol='B',quantified=False,domain='fixed odd integer B>=81',sufficientThresholdEffective=False)
    report=dict(schema='abc78-exact-construction/v34',variables=78,quadraticRows=70,degree=4,
       integerContentForEveryPositiveB=1,ordinaryMonomialsForEveryPositiveB=len(profiles),
       parameterSeparatedTerms=len(full),constantCoefficient=str(const),largestFixedCoefficient=str(fixedmax),
       exactHeight=f'max({fixedmax},B^2+{const})',heightSwitchInteger=switch,
       unitCoefficientMonomial=[1,1,1,1],inputMap='beta=X^2+3',
       comparisonArguments=['lambda','lambda+B+X^8+T^2'],
       ellipticIndexDomain='(1/2) Z, including torsion index zero',
       definingThreshold='Ineffective; sufficiently large fixed odd B; B=81 is not certified',
       arithmeticScope='Ordinary rational abc, the retained elliptic group, fixed-data simultaneous prime patterns, and the prepared congruent-number pole realization. The new height estimates are proved separately.',
       checksScope='Exact finite polynomial specification and coefficient facts. Infinite arithmetic inputs and independent mathematical acceptance are not certified.')
    system=dict(format='integer-quadratic-family-abc78-v34',variables=78,inputCoordinate=1,fixedParameter=parameter,coordinates=coordinates,residuals=rows)
    polynomial=dict(format='integer-quartic-family-abc78-v34',variables=78,degree=4,inputCoordinate=1,fixedParameter=parameter,coordinates=coordinates,terms=serial(full))
    out.mkdir(parents=True,exist_ok=True)
    for filename,obj in [('quadratic-family.json',system),('polynomial-family.json',polynomial),('construction-report.json',report)]:
        (out/filename).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return system,polynomial,report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE);args=ap.parse_args();build(args.output)
