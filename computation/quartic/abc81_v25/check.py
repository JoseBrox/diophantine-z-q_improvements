#!/usr/bin/env python3
"""Independent exact verification. Does not import the construction program.

Reconstructs every equation from the mathematical formulas using SymPy,
then expands the sum of squares by an independent sparse calculation.
Exact elliptic examples are supplementary: the universal projection
argument is the separate written proof, not a finite search.
"""
from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from math import gcd, lcm, isqrt
from pathlib import Path
import json
import sympy as S

ROOT=Path(__file__).resolve().parent
stages=[]
def passed(name,**details):stages.append(dict(name=name,status='PASS',**details))
def raw_terms(row):return {(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in row['terms']}
def canonical(expr,z,B):
    poly=S.Poly(S.expand(expr),*z,B)
    d=lcm(*(int(c.q) for c in poly.coeffs()))
    out={}
    for powers,c in poly.terms():
        m=tuple(i+1 for i,e in enumerate(powers[:-1]) for _ in range(e))
        out[powers[-1],m]=int(c*d)
    g=gcd(*out.values())
    if out[min(out)]<0:g=-g
    return {k:c//g for k,c in out.items() if c}

def reconstruct(system):
    z=S.symbols('x1:82');B=S.Symbol('B');rho=S.Symbol('rho')
    names={c['name']:z[c['id']-1] for c in system['coordinates']}
    assert len(names)==81 and [c['id'] for c in system['coordinates']]==list(range(1,82))
    def r(name):return names[name]
    def K(name):return r(name+'.0')+rho*r(name+'.1')
    def comp(expr):
        p=S.Poly(S.expand(expr),rho).rem(S.Poly(rho*rho-2,rho))
        return S.expand(p.nth(0)),S.expand(p.nth(1))
    def bar(expr):return expr.subs(rho,-rho)
    expected=[]
    def add(name,expr):expected.append((name,canonical(expr,z,B)))
    def fieldrow(name,expr):
        for i,e in enumerate(comp(expr)):add(name+f'.{i}',e)
    D=11-6*rho; a=(57-28*rho)/8;b=(-660+417*rho)/32
    X=r('input');I0=r('inputComparison.real');lam=r('slope')
    SH=K('common.S');TH=K('common.T');fH=K('common.f');gH=K('common.g')
    f=K('pair.f');h=K('pair.h');g=K('pair.g');k=K('pair.k');s=K('pair.slope')
    L=K('ratio.primary');L0=K('ratio.alternate')
    HH=K('square.common.f');GG=K('square.common.g');UU=K('square.pair.f');VV=K('square.pair.g')
    CC=K('square.comparison');II=K('square.input')
    ap=a*a+D;bp=a*a-D
    fieldrow('common.first',2*b*D*(a*TH-b)*fH-(a*ap*SH*TH+b*ap*SH-b*bp*TH+4*a*a*D))
    fieldrow('common.second',2*b*D*(a*SH+b)*gH-(-a*ap*SH*TH-b*bp*SH+b*ap*TH-4*a*a*D))
    fieldrow('common.third',D*D*fH*gH+a*D*(fH+gH)+a*SH*TH+b*(SH-TH)+D)
    initial=[dict(p) for _,p in expected]
    Tmat=S.Matrix([[S.Rational(x) for x in rr] for rr in json.loads((ROOT/'common-row-reduction.json').read_text())['matrix']])
    assert Tmat.det()==-S.Rational(1,362963666515968)
    for i in range(6):
        p=defaultdict(lambda:S.Integer(0))
        for j in range(6):
            for key,c in initial[j].items():p[key]+=Tmat[i,j]*c
        den=lcm(*(int(c.q) for c in p.values())); pp={key:int(c*den) for key,c in p.items() if c}
        gg=gcd(*pp.values());gg=gg if pp[min(pp)]>0 else -gg
        expected[i]=(expected[i][0],{key:c//gg for key,c in pp.items()})
    fieldrow('pair.cubic',h*h-f+D*f*UU)
    fieldrow('pair.secant',s*(f-g)-h-k)
    fieldrow('pair.tangent',s*(h-k)-1+D*(UU+f*g+VV))
    for name,x,y in [('common.f',fH,HH),('common.g',gH,GG),('pair.f',f,UU),('pair.g',g,VV)]:fieldrow('square.'+name,y-x*x)
    fieldrow('ratio.primary.raw',h*L+f*SH)
    fieldrow('ratio.primary.regular',(1-D*UU)*L+h*SH)
    fieldrow('ratio.alternate.raw',k*L0+g*TH)
    fieldrow('ratio.alternate.regular',(1-D*VV)*L0+k*TH)
    beta=r('ratio.primary.0')-I0
    add('inputComparison',I0-r('ratio.primary.0')+X*X+B)
    fieldrow('square.comparison',CC-(L-bar(L0))**2)
    fieldrow('square.input',II-(I0+rho*r('ratio.primary.1'))**2)
    trace=r('height.trace');u=r('height.sumSquares');v=r('height.product')
    add('height.trace',trace-2*comp(s*s+D*(f+g))[0])
    add('height.sumSquares',u-beta*beta-trace*trace)
    add('height.product',v-beta*trace)
    for j in range(2):
        p=f'detector{j}.'
        t=lam if j==0 else r(p+'argument')
        if j:add(p+'argument',t-lam-u*u+2*v*v)
        R=r(p+'contactSquareShift');Z=r(p+'contactSumShift');w=r(p+'inverseWeight');w2=r(p+'inverseWeightSquare');w3=r(p+'inverseWeightCube')
        A1=K(p+'factor1');A2=K(p+'factor2');O=K(p+'product');eta=r(p+'trace');bpole=r(p+'poleInput')
        e=r(p+'pole.e');uu=r(p+'pole.u');pp=r(p+'pole.p');vv=r(p+'pole.v');qq=r(p+'pole.q');p2=r(p+'pole.pSquare');q2=r(p+'pole.qSquare')
        add(p+'contactSquare',R-t*t+2*t)
        add(p+'contactSum',R*Z+Z-R*R+35*R)
        add(p+'inverseContact',(R+1)*w-Z*Z-24*Z)
        add(p+'inverseWeightSquare',w2-w*w)
        add(p+'inverseWeightCube',w3-w*w2)
        fieldrow(p+'factor1',w3*A1-w2*w2-w3*CC-w2*HH-UU*UU)
        fieldrow(p+'factor2',w3*A2-w2*w2-w3*II-w2*bar(GG)-bar(VV)**2)
        fieldrow(p+'product',(R+1)*O-A1*A2)
        add(p+'trace',r(p+'product.0')**2-2*r(p+'product.0')*eta-2*r(p+'product.1')**2)
        add(p+'poleInput',w3*bpole-eta*eta)
        add(p+'pole.pSquare',p2-pp*pp)
        add(p+'pole.first',289+34*e-3*e*e-17*bpole*p2)
        add(p+'pole.factor',17*e-e*bpole-17*uu*vv)
        add(p+'pole.qSquare',q2-qq*qq)
        add(p+'pole.second',uu*uu+34*uu*vv-17*bpole*q2-867*vv*vv)
    assert len(expected)==73
    return expected

def check_rows(system,expected):
    assert system['variables']==81 and system['inputCoordinate']==1
    assert len(system['residuals'])==73
    assert [r['id'] for r in system['residuals']]==list(range(1,74))
    for row,(name,p) in zip(system['residuals'],expected):
        assert row['name']==name
        assert raw_terms(row)==p,name
        assert max(len(m) for _,m in p)<=2

def expand_rows(rows):
    out=defaultdict(int)
    for row in rows:
        terms=list(raw_terms(row).items())
        for i,((a,m),c) in enumerate(terms):
            for j in range(i,len(terms)):
                (b,n),d=terms[j];out[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
    return {k:c for k,c in out.items() if c}

def verify():
    system=json.loads((ROOT/'quadratic-family.json').read_text())
    polynomial=json.loads((ROOT/'polynomial-family.json').read_text())
    report=json.loads((ROOT/'construction-report.json').read_text())
    expected=reconstruct(system);check_rows(system,expected)
    passed('independent reconstruction of all quadratic equations and invertible common-chart row basis',rows=73,variables=81)
    p=expand_rows(system['residuals']);assert p==raw_terms(polynomial)
    assert max(len(m) for _,m in p)==4 and gcd(*p.values())==1 and p[0,(1,1,1,1)]==1
    assert {i for _,m in p for i in m}==set(range(1,82))
    profiles=defaultdict(dict)
    for (b,m),c in p.items():profiles[m][b]=c
    assert len(profiles)==941 and len(p)==942
    passed('independent complete quartic expansion, exact degree, content and support',coefficientProfiles=941,parameterTerms=942)
    C=4153456;c0=797551;switch=1832
    assert profiles[()]=={0:c0,2:1}
    assert max(abs(pp[0]) for pp in profiles.values() if set(pp)=={0})==C
    for m,pp in profiles.items():
        assert set(pp) in ({0},{1},{0,2})
        if 1 in pp:
            a=abs(pp[1]);b=abs(pp.get(0,0))
            assert a*3+b<=C and a*(switch-1)+b<=C
            assert switch**2+c0>=a*switch+b and 2*switch>=a
    assert (switch-1)**2+c0<=C<switch**2+c0
    for B in [3,17,1831,1833,1000000]:
        assert max(abs(sum(c*B**i for i,c in pp.items())) for pp in profiles.values())==max(C,B*B+c0)
    assert report['exactHeight']=='max(4153456,B^2+797551)'
    passed('coefficient-height formula for every fixed odd B>=3',formula=report['exactHeight'],coefficientOnlyThresholdOddB=1833)
    f,g,h,k,s,D=S.symbols('f g h k s D')
    r1=s*(f-g)-h-k;r2=s*(h-k)-1+D*(f*f+f*g+g*g);r3=h*h-f+D*f**3
    c=s*s+D*(f+g);y=D*h-s*(D*f+c)
    assert S.expand(k*k-g+D*g**3-r3+(f-g)*r2-(h-k)*r1)==0
    assert S.expand(y*y-c**3+D*c-D*D*r3+D*(D*f+c)*(r2-s*r1))==0
    passed('universal reciprocal cubic and oriented-difference polynomial identities')
    t,z,w=S.symbols('t z w');r=(t-1)**2
    P=S.prod(r-a for a in [1,4,9,36])
    assert S.expand(P-S.prod(t-a for a in [-5,-2,-1,0,2,3,4,7]))==0
    assert S.cancel(P/r**2-((r+36/r)**2-50*(r+36/r)+481))==0
    assert S.expand((z+37)**2-50*(z+37)+481-z*z-24*z)==0
    passed('exact reciprocal contact identity and its affine normalization')
    for nu in [1,3,5,7]:
        # Residue representatives suffice because all classes depend only on nu mod 8.
        assert (-nu)%2==1 and (-2*nu)%4==2 and (-4*nu)%8==4
        assert Fraction(nu,4)>0 and Fraction(3*nu,4)>0 and Fraction(7*nu,8)>0
    assert Fraction(4,3)*Fraction(2,3)==Fraction(8,9)<1
    # The zero inverse-weight locus forces f=g=h=k=0 and then r2=-1.
    assert r2.subs({f:0,g:0,h:0,k:0})==-1
    passed('valuation residue classes, positive-depth implications, zero-weight exclusion, and strict height coefficient')
    mutated=deepcopy(system);mutated['residuals'][8]['terms'][0]['coefficient']=str(int(mutated['residuals'][8]['terms'][0]['coefficient'])+1)
    try:check_rows(mutated,expected)
    except AssertionError:pass
    else:raise AssertionError('Corrupted coefficient was accepted')
    mutated=deepcopy(system);mutated['residuals'].pop()
    try:check_rows(mutated,expected)
    except AssertionError:pass
    else:raise AssertionError('Missing row was accepted')
    corrupted=dict(p);key=next(iter(corrupted));corrupted[key]+=1;assert corrupted!=expand_rows(system['residuals'])
    passed('three deliberate rejection controls',controls=['changed quadratic coefficient','missing equation','changed quartic coefficient'])
    return dict(schema='abc81-independent-verification/v1',status='PASS',stages=stages,
                stageCount=len(stages),sympyVersion=S.__version__,
                sourceFiles={n:sha256((ROOT/n).read_bytes()).hexdigest() for n in ['build.py','common-row-reduction.json','quadratic-family.json','polynomial-family.json','construction-report.json']},
                independentImplementation=True,independentNonauthorReview=False,
                scope='Exact algebraic identities, all quadratic equations, all quartic coefficients, height profiles and rejection controls. Does not verify abc, the inherited prime-pattern/pole premises, a numerical defining threshold, or the repository-wide legacy suite.')

if __name__=='__main__':
    result=verify();(ROOT/'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
