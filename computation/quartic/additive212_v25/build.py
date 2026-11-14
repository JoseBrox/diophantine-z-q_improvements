#!/usr/bin/env python3
"""A 212-coordinate family with additive comparison arguments.

Both contact blocks and the aggregate relation change. The arithmetic
proof of the changed arguments is separate from these exact coefficient
calculations. The fixed parameter threshold for defining Z is ineffective.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import gcd,lcm
from pathlib import Path
import argparse,json

HERE=Path(__file__).resolve().parent
SOURCE_SHA='49cf4066bf1e35e02e2156bf4bd24a21bb4c5e794f7374e056413d8306fb73c5'
OLD_SCALED={117,118}
K=31581660**28;J=5898050446009651968;A0=(J*K)**2

def clean(p):return {k:Q(c) for k,c in p.items() if c}
def add(*ps):
    p=defaultdict(Q)
    for x in ps:
        for k,c in x.items():p[k]+=c
    return clean(p)
def scale(p,a):return clean({k:c*a for k,c in p.items()})
def mul(p,q):
    r=defaultdict(Q)
    for (a,m),c in p.items():
        for (b,n),d in q.items():r[a+b,tuple(sorted(m+n))]+=c*d
    return clean(r)
def V(i):return {(0,(i,)):Q(1)}
ONE={(0,()):Q(1)}
def rd(row):return {(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient']) for t in row['terms']}
def prim(p):
    p=clean(p);D=lcm(*(c.denominator for c in p.values()));g=gcd(*(int(c*D) for c in p.values()))
    if p[min(p)]<0:g=-g
    return scale(p,Q(D,g))
def ser(p):return [dict(parameterPower=a,monomial=list(m),coefficient=str(c)) for (a,m),c in sorted(p.items())]
def expand(rows):
    p=defaultdict(Q)
    for r in rows:
        for k,c in mul(rd(r),rd(r)).items():p[k]+=c
    return clean(p)
def profiles(p):
    d=defaultdict(dict)
    for (a,m),c in p.items():d[m][a]=int(c)
    return d

def build(source:Path,out:Path):
    raw=(source/'quadratic214.json').read_bytes();assert sha256(raw).hexdigest()==SOURCE_SHA
    old=json.loads(raw);coords=json.loads((source/'coordinates214.json').read_text())
    assert len(coords)==214 and len(old['residuals'])==188
    roots=[Q(1),Q(9,4),Q(4),Q(2398,2399)**2,Q(439,407)**2]
    es=[Q(1)]+[sum((__import__('math').prod(c) for c in combinations(roots,k)),Q(0)) for k in range(1,6)]
    e1,e2,e3,e4,e5=es[1:]
    changes={}
    for j,(arg,ri,ui,vi,si,first) in enumerate([(4,76,77,78,80,22),(90,91,92,93,95,35)]):
        lam,r,u,v,s=map(V,[arg,ri,ui,vi,si]);one_s=add(ONE,s)
        changes.update({
          first:(f'additive.detector{j}.contactSquare',add(r,scale(mul(add(lam,scale(ONE,-1)),add(lam,scale(ONE,-1))),-1))),
          first+1:(f'additive.detector{j}.contactFourthPower',add(u,scale(mul(r,r),-1))),
          first+2:(f'additive.detector{j}.contactCombination',add(v,scale(mul(r,u),-1),scale(mul(one_s,u),e1),scale(mul(one_s,r),-e2))),
          first+3:(f'additive.detector{j}.contactRelation',add(mul(u,v),scale(mul(one_s,add(scale(u,e3),scale(r,-e4),scale(ONE,e5))),-1))) })
    aggregate=rd(next(row for row in old['residuals'] if row['id']==182))
    assert aggregate.pop((0,(4,90)))==8
    aggregate=add(aggregate,scale(mul(V(90),V(117)),8),scale(mul(V(4),V(117)),-8))
    changes[182]=('additive.aggregate.rootTrace',aggregate)
    removed={119,120};renames={4:'additive.lambda',76:'additive.detector0.contactSquare',77:'additive.detector0.contactFourthPower',78:'additive.detector0.contactCombination',90:'additive.detector1.argument',91:'additive.detector1.contactSquare',92:'additive.detector1.contactFourthPower',93:'additive.detector1.contactCombination'}
    kept=[c for c in coords if c['id'] not in removed];remap={c['id']:i+1 for i,c in enumerate(kept)}
    coordinates=[dict(c,id=remap[c['id']],parent214Id=c['id'],name=renames.get(c['id'],c['name'])) for c in kept]
    rows=[];balanced=[]
    for oldrow in old['residuals']:
        if oldrow['id'] in {64,65}:continue
        name,p=changes.get(oldrow['id'],(oldrow['name'],rd(oldrow)))
        assert not any(removed.intersection(m) for a,m in p)
        p=prim(p);assert max(len(m) for a,m in p)<=2
        mapped={(a,tuple(sorted(remap[i] for i in m))):c for (a,m),c in p.items()}
        rows.append(dict(id=len(rows)+1,parent214RowId=oldrow['id'],name=name,terms=ser(mapped)))
        minimum=min(2*a+sum(i in OLD_SCALED for i in m) for a,m in p)
        bp={(2*a+sum(i in OLD_SCALED for i in m)-minimum,tuple(sorted(remap[i] for i in m))):c*149**a for (a,m),c in p.items()}
        bp=prim(bp);assert max(a for a,m in bp)<=1
        balanced.append(dict(id=len(balanced)+1,parent214RowId=oldrow['id'],name=name,divided_C_power=minimum,terms=ser(bp)))
    assert len(coordinates)==212 and len(rows)==186
    results={}
    out.mkdir(parents=True,exist_ok=True)
    for variant,rr in [('unbalanced',rows),('balanced',balanced)]:
        poly=expand(rr);pp=profiles(poly)
        assert max(len(m) for a,m in poly)==4 and gcd(*(int(c) for c in poly.values()))==1
        assert {i for a,m in poly for i in m}==set(range(1,213))
        parameter={'name':('A' if variant=='unbalanced' else 'C'),'value':('149^(2N+1)' if variant=='unbalanced' else '149^N'),'quantified':False,'definingThreshold':'Fixed but ineffective, under the retained arithmetic inputs; may differ from the 214 source threshold.'}
        system=dict(format='additive212-quadratic-v25',variables=212,inputCoordinate=1,fixedParameter=parameter,coordinates=coordinates,residuals=rr)
        full=dict(format='additive212-quartic-v25',variables=212,degree=4,inputCoordinate=1,fixedParameter=parameter,terms=ser(poly))
        for suffix,obj in [('quadratic',system),('polynomial',full)]:
            (out/f'{variant}-{suffix}.json').write_text(json.dumps(obj,indent=2)+'\n')
        if variant=='balanced':
            assert max(abs(p.get(0,0)) for p in pp.values())==A0
            assert max(abs(p.get(2,0)) for p in pp.values())==K
            for p in pp.values():
                if set(p)=={1}:assert p[1]**2<=A0*K
                else:
                    assert set(p)<={0,2}
                    assert abs(p.get(0,0))*K+abs(p.get(2,0))*A0<=A0*K
            height='max((5898050446009651968*31581660^28)^2,31581660^28*C^2)'
        else:
            for p in pp.values():assert set(p) in ({0},{1},{0,2})
            assert [p for p in pp.values() if 2 in p]==[{0:1,2:1}]
            C0=max(abs(p[0]) for p in pp.values() if set(p)=={0})
            lin=max(abs(p[1]) for p in pp.values() if 1 in p)
            assert lin**2<C0 and 149**210+1<C0<149**214+1
            height=f'max({C0},A^2+1)'
        results[variant]=dict(variables=212,quadraticRows=186,degree=4,content=1,coordinateMonomials=len(pp),parameterSeparatedTerms=len(poly),coefficientHeight=height)
    report=dict(schema='additive212-construction/v25',sourceRowsSha256=SOURCE_SHA,changedParentRows=sorted(changes),removedParentRows=[64,65],removedParentCoordinates=[119,120],unchangedParentRows=177,comparisonArguments=['lambda','lambda+T'],contactSquaredDistances=[str(a) for a in roots],contactElementarySymmetric=[str(e) for e in es],fixedParameterEffectiveness='No numerical sufficient defining N; all N above one fixed ineffective threshold.',balancedScalingParentCoordinates=sorted(OLD_SCALED),results=results,arithmeticScope='Retains the rank, scalar, pole, prime-pattern, aggregate-sum-height and full-family contact-height inputs of the pinned 214 source. The additive realization and new contact equations have their own proof; no all-source audit acceptance is claimed.')
    (out/'construction-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=HERE.parent/'balanced214_v24/source');p.add_argument('--output',type=Path,default=HERE);a=p.parse_args();build(a.source,a.output)
