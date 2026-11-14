#!/usr/bin/env python3
"""Independent exact audit of the 212-coordinate additive construction.

No producer is imported. SymPy reconstructs the nine changed equations;
all 177 retained equations and every coefficient are compared exactly.
"""
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import gcd,lcm
from pathlib import Path
import argparse,json
import sympy as S
HERE=Path(__file__).resolve().parent
PIN='49cf4066bf1e35e02e2156bf4bd24a21bb4c5e794f7374e056413d8306fb73c5'

def rd(row):return {(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in row['terms']}
def primitive(p):
    p={k:S.Rational(c) for k,c in p.items() if c};den=lcm(*(int(c.q) for c in p.values()))
    p={k:int(c*den) for k,c in p.items()};g=gcd(*p.values())
    if p[min(p)]<0:g=-g
    return {k:c//g for k,c in p.items()}
def exprpoly(e,x):
    P=S.Poly(S.expand(e),*x)
    return primitive({(0,tuple(i+1 for i,d in enumerate(exps) for _ in range(d))):c for exps,c in P.terms()})
def expand(rows):
    p=defaultdict(int)
    for row in rows:
        terms=list(rd(row).items())
        for i,((a,m),c) in enumerate(terms):
            for j in range(i,len(terms)):
                (b,n),d=terms[j];p[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
    return {k:c for k,c in p.items() if c}
def run(source):
    stages=[]
    def ok(n,**kw):stages.append(dict(name=n,status='PASS',**kw))
    raw=(source/'quadratic214.json').read_bytes();assert sha256(raw).hexdigest()==PIN
    old=json.loads(raw);coords=json.loads((source/'coordinates214.json').read_text())
    assert len(coords)==214 and len(old['residuals'])==188
    original=expand(old['residuals'])
    assert original==rd(json.loads((source/'polynomial214.json').read_text()))
    ok('source reconstruction against every original quartic coefficient',quadraticRows=188)
    x=S.symbols('x1:215');V=lambda i:x[i-1]
    theta=[S.Rational(0),-S.Rational(1,2),-S.Rational(1),S.Rational(1,2399),-S.Rational(32,407)]
    alpha=[(1-t)**2 for t in theta]
    e=[S.Integer(1)]+[sum(S.prod(a) for a in combinations(alpha,k)) for k in range(1,6)]
    changes={}
    for arg,r,u,v,s,first in [(4,76,77,78,80,22),(90,91,92,93,95,35)]:
        t,r,u,v,s=map(V,[arg,r,u,v,s])
        for i,E in enumerate([r-(t-1)**2,u-r*r,v-r*u+e[1]*(1+s)*u-e[2]*(1+s)*r,u*v-(1+s)*(e[3]*u-e[4]*r+e[5])]):changes[first+i]=exprpoly(E,x)
    agg=rd(old['residuals'][181]);assert agg.pop((0,(4,90)))==8
    agg[0,(90,117)]=8;agg[0,(4,117)]=-8;changes[182]=primitive(agg)
    kept=[c['id'] for c in coords if c['id'] not in {119,120}];remap={v:i+1 for i,v in enumerate(kept)}
    expected=[]
    for row in old['residuals']:
        if row['id'] in {64,65}:continue
        p=changes.get(row['id'],rd(row));assert not any({119,120}.intersection(m) for a,m in p)
        expected.append((row['id'],{(a,tuple(sorted(remap[i] for i in m))):c for (a,m),c in p.items()}))
    systems={k:json.loads((HERE/f'{k}-quadratic.json').read_text()) for k in ['unbalanced','balanced']}
    def check_unbalanced(system):
        assert system['variables']==212 and len(system['residuals'])==186
        assert [c['parent214Id'] for c in system['coordinates']]==kept
        assert [c['id'] for c in system['coordinates']]==list(range(1,213))
        for row,(parent,p) in zip(system['residuals'],expected):
            assert row['parent214RowId']==parent and rd(row)==p,parent
    check_unbalanced(systems['unbalanced'])
    ok('nine changed and 177 retained quadratic equations; complete coordinate-use check',changed=9,retained=177,removedRows=[64,65],removedCoordinates=[119,120])
    r,s,q,t,w=S.symbols('r s q t w');P=S.prod(r-a for a in alpha);U=r*r
    Vnew=r*U-e[1]*(1+s)*U+e[2]*(1+s)*r
    relation=S.expand(U*Vnew-(1+s)*(e[3]*U-e[4]*r+e[5]))
    assert S.expand(relation-((1+s)*P-s*r**5))==0
    assert S.expand(q*((1+s)*P-s*r**5)-( (1+q)*P-r**5 )).subs(s,1/q).expand()==0
    contacts=theta+[2-c for c in theta]
    assert len(set(contacts))==10 and max(contacts)-min(contacts)==4
    assert S.expand(P.subs(r,(t-1)**2)-S.prod(t-c for c in contacts))==0
    assert P.subs(r,0)!=0
    assert S.expand(relation.subs({r:0,s:-1}))==0
    ok('universal contact identity, all ten roots, and the t=1 boundary')
    # Recover the actual old contact rows, not just the formal degree-five identity.
    rr=(t-1)**2;PP=P.subs(r,rr);qq=rr**5/PP-1
    maps=[({4:1/t,76:1/t**2,77:1/t**4,78:PP/t**10,79:qq,119:1/t**5},[22,23,24,25,64]),
          ({90:w*t,91:w*rr,92:w*rr**2,93:w*w*PP,94:qq,117:w,120:w*rr**3},[35,36,37,38,65])]
    for subs,indices in maps:
        for idx in indices:
            E=sum(c*S.prod(subs[i] for i in m) for (a,m),c in rd(old['residuals'][idx-1]).items())
            assert S.cancel(E)==0,idx
    ok('both physical contact normalizations independently matched to the pinned source')
    Bidx={remap[117],remap[118]};balanced=systems['balanced'];assert len(balanced['residuals'])==186
    for rb,ru in zip(balanced['residuals'],systems['unbalanced']['residuals']):
        p=rd(ru);mn=min(2*a+sum(i in Bidx for i in m) for a,m in p)
        target=primitive({(2*a+sum(i in Bidx for i in m)-mn,m):c*149**a for (a,m),c in p.items()})
        assert rd(rb)==target and rb['divided_C_power']==mn
    ok('all-row verification of the two-coordinate coefficient rescaling')
    K=31581660**28;A0=(5898050446009651968*K)**2
    for name,system in systems.items():
        p=expand(system['residuals']);assert p==rd(json.loads((HERE/f'{name}-polynomial.json').read_text()))
        assert max(len(m) for a,m in p)==4 and gcd(*p.values())==1
        assert {i for a,m in p for i in m}==set(range(1,213))
        profiles=defaultdict(dict)
        for (a,m),c in p.items():profiles[m][a]=c
        assert len(profiles)==2908 and len(p)==(2909 if name=='unbalanced' else 2910)
        assert all(set(v) in ({0},{1},{2},{0,2}) for v in profiles.values())
        assert all(v[0]*v[2]>0 for v in profiles.values() if set(v)=={0,2})
        if name=='balanced':
            assert max(abs(v.get(0,0)) for v in profiles.values())==A0
            assert max(abs(v.get(2,0)) for v in profiles.values())==K
            assert any(v=={0:A0} for v in profiles.values()) and any(v=={2:K} for v in profiles.values())
            for v in profiles.values():
                if set(v)=={1}:assert v[1]**2<=A0*K
                else:assert abs(v.get(0,0))*K+abs(v.get(2,0))*A0<=A0*K
            assert K*149**112<A0<=K*149**114
        else:
            C0=max(abs(v[0]) for v in profiles.values() if set(v)=={0})
            assert [v for v in profiles.values() if 2 in v]==[{0:1,2:1}]
            lin=max(abs(v[1]) for v in profiles.values() if 1 in v)
            assert lin**2<C0 and 149**210+1<C0<149**214+1
        ok(name+' complete quartic coefficients, all positive-parameter support and exact height',variables=212,quadraticRows=186,monomials=2908)
    broken=deepcopy(systems['unbalanced']);broken['residuals'][21]['terms'][0]['coefficient']=str(int(broken['residuals'][21]['terms'][0]['coefficient'])+1)
    try:check_unbalanced(broken)
    except AssertionError:pass
    else:raise AssertionError('A changed contact coefficient was accepted')
    broken=deepcopy(systems['unbalanced']);broken['residuals'].pop()
    try:check_unbalanced(broken)
    except AssertionError:pass
    else:raise AssertionError('A missing row was accepted')
    ok('deliberate coefficient and missing-row rejection controls')
    result=dict(schema='additive212-independent-check/v1',status='PASS',stages=stages,stageCount=len(stages),independentImplementation=True,independentNonauthorReview=False,sourceRowsSha256=PIN,files={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.json')) if p.name!='independent-verification.json'},scope='Finite exact algebra, all rows, full coefficients, contact-domain identities and coefficient thresholds. The arithmetic proof, its inherited premises, and a numerical defining threshold are not verified by this program.')
    (HERE/'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=HERE.parent/'balanced214_v24/source');a=p.parse_args();run(a.source)
