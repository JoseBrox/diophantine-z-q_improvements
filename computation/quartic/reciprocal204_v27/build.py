#!/usr/bin/env python3
"""Exact 204-coordinate quartic with two recovered elliptic differences.

Algebraic coefficients only. The arithmetic projection theorem, including
half-index completeness and weighted height, is a separate written proof.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd,lcm
import json,sys,argparse
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'abc81_v25'))
from build import con,var,add,scale,mul,sq,sub,prim,serial,plus,diff,times,power2,kconst,rational,ktimes
SOURCE=HERE.parent/'additive212_v25/unbalanced-quadratic.json'
# These are exact coordinate substitutions in the literal 212 system.
WEIGHTS={i:1 for i in list(range(39,47))+list(range(48,52))}
WEIGHTS.update({i:-1 for i in range(205,209)})
REMOVED=set(range(155,169))|set(range(183,197))
REMOVED_ROWS=set(range(104,122))|set(range(140,158))
K=31581660**28; J=5898050446009651968; H0=(J*K)**2

def read(row):return {(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient']) for t in row['terms']}
def expand(rows):
    out=defaultdict(Q)
    for r in rows:
        for key,c in sq(read(r)).items():out[key]+=c
    return {k:c for k,c in out.items() if c}
def rescale(p):
    """old v_i=R^WEIGHTS[i] new v_i, with R2=R^2, on R!=0."""
    data=[]
    for (a,m),c in p.items():
        e=sum(WEIGHTS.get(i,0) for i in m)+m.count(118)+2*m.count(117)
        mm=tuple(i for i in m if i not in (117,118));data.append((a,e,mm,c))
    e0=min(e for a,e,m,c in data);out=defaultdict(Q)
    for a,e,m,c in data:
        e-=e0
        if e not in (0,1,2):raise ValueError(('R degree',e))
        mm=tuple(sorted(m+(() if e==0 else ((118,) if e==1 else (117,)))))
        out[a,mm]+=c
    return {k:c for k,c in out.items() if c},e0

def build(out=HERE):
    raw=SOURCE.read_bytes();assert sha256(raw).hexdigest()=='b2f32d64ef1fb2591d37cfd41aadf8869ce691c39ed92e0e597ec10aaa53fc75';old=json.loads(raw)
    assert old['variables']==212 and len(old['residuals'])==186
    coords=[dict(c,parent212Id=c['id']) for c in old['coordinates'] if c['id'] not in REMOVED]
    for c in coords:
        if c['id'] in WEIGHTS:c['name']='v27.'+c['name']+'.rescaling_'+str(WEIGHTS[c['id']])
    nextid=213
    def field(n):
        nonlocal nextid
        z=[]
        for j in range(2):
            coords.append(dict(id=nextid,name=n+'.'+str(j),kind='reciprocal_pair'))
            z.append(var(nextid));nextid+=1
        return tuple(z)
    def pair(i,j,half=False):return (var(i),scale(var(j),2 if half else 1))
    S=pair(19,20);TH=pair(211,212);D=kconst(11,-6);one=kconst(1)
    newrows=[];rootcs=[]
    def row(n,p):
        p=prim(p);assert max(len(m) for a,m in p)<=2,n
        newrows.append(dict(name=n,terms=serial(p)))
    def krow(n,p):row(n+'.0',p[0]);row(n+'.1',p[1])
    for nr,fu,fv,L,LP,kappa in [(1,(54,55),(23,24),(31,32),(33,34),1),(3,(58,59),(27,28),(39,40),(41,42),2)]:
        f=field(f'pair{nr}.f');h=field(f'pair{nr}.h');g=field(f'pair{nr}.g');k=field(f'pair{nr}.k');s=field(f'pair{nr}.s')
        FU=pair(*fu,half=True);FV=pair(*fv,half=True);L=pair(*L);LP=pair(*LP)
        krow(f'pair{nr}.square.f',diff(FU,power2(f)))
        krow(f'pair{nr}.square.g',diff(FV,power2(g)))
        krow(f'pair{nr}.curve',plus(power2(h),ktimes(-1,f),times(D,times(f,FU))))
        krow(f'pair{nr}.secant',diff(times(s,diff(f,g)),plus(h,k)))
        krow(f'pair{nr}.tangent',plus(times(s,diff(h,k)),ktimes(-1,one),times(D,plus(FU,times(f,g),FV))))
        for suffix,h1,f1,F1,L1,S1 in [('primary',h,f,FU,L,S),('alternate',k,g,FV,LP,TH)]:
            krow(f'pair{nr}.ratio.{suffix}.raw',plus(times(h1,L1),ktimes(kappa,times(f1,S1))))
            krow(f'pair{nr}.ratio.{suffix}.regular',plus(times(diff(one,times(D,F1)),L1),ktimes(kappa,times(h1,S1))))
        rootcs.append(plus(power2(s),times(D,plus(f,g))))
    agg=scale(sub(var(4),var(90)),8)
    for C,E in [(173,175),(201,203)]:
        ce=diff(pair(C,C+1),pair(E,E+1));agg=add(agg,power2(ce)[0])
    agg=add(agg,*(scale(c[0],4) for c in rootcs))
    rows=[];transforms=[]
    for r in old['residuals']:
        if r['id'] in REMOVED_ROWS:continue
        p=read(r);name=r['name']
        if r['id']==180:p=agg;name='weighted.aggregate.trace'
        elif any(set(m)&set(WEIGHTS) for a,m in p):
            p,e=rescale(p);transforms.append(dict(row=r['id'],divided_R_power=e));name='v27.'+name
        assert not any(set(m)&REMOVED for a,m in p),name
        p=prim(p);assert max(len(m) for a,m in p)<=2,name
        rows.append(dict(name=name,parent212RowId=r['id'],terms=serial(p)))
    rows.extend(newrows)
    ids={c['id']:i+1 for i,c in enumerate(coords)}
    for c in coords:c['id']=ids[c['id']]
    results={}
    out.mkdir(parents=True,exist_ok=True)
    for variant in ('unbalanced','balanced'):
        rr=[]
        for r in rows:
            p=read(r);e=0
            if variant=='balanced':
                e=min(2*a+sum(i in (117,118) for i in m) for a,m in p)
                p={(2*a+sum(i in (117,118) for i in m)-e,m):c*149**a for (a,m),c in p.items()}
                p=prim(p)
                assert max(a for a,m in p)<=1,r['name']
            p={(a,tuple(sorted(ids[i] for i in m))):c for (a,m),c in p.items()}
            rr.append(dict(r,id=len(rr)+1,divided_C_power=e,terms=serial(p)))
        poly=expand(rr);profiles=defaultdict(dict)
        for (a,m),c in poly.items():profiles[m][a]=int(c)
        assert len(coords)==204 and len(rr)==186
        assert max(len(m) for a,m in poly)==4
        assert gcd(*(int(c) for c in poly.values()))==1
        assert {i for a,m in poly for i in m}==set(range(1,205))
        if variant=='balanced':
            assert max(abs(p.get(0,0)) for p in profiles.values())==H0
            assert max(abs(p.get(2,0)) for p in profiles.values())==K
            for p in profiles.values():
                if set(p)=={1}:assert p[1]**2<=H0*K
                else:assert set(p)<={0,2} and abs(p.get(0,0))*K+abs(p.get(2,0))*H0<=H0*K
            ht='max((5898050446009651968*31581660^28)^2,31581660^28*C^2)'
        else:
            assert all(set(p) in ({0},{1},{0,2}) for p in profiles.values())
            assert [p for p in profiles.values() if 2 in p]==[{0:1,2:1}]
            C0=max(abs(p.get(0,0)) for p in profiles.values())
            ht=f'max({C0},A^2+1)'
        parameter=dict(symbol='C' if variant=='balanced' else 'A',value='149^N' if variant=='balanced' else '149^(2N+1)',quantified=False,sufficientDefiningThreshold='Ineffective')
        system=dict(format='reciprocal204-v27',variables=204,inputCoordinate=1,fixedParameter=parameter,coordinates=coords,residuals=rr)
        full=dict(format='reciprocal204-quartic-v27',variables=204,degree=4,inputCoordinate=1,fixedParameter=parameter,terms=serial(poly))
        for suffix,dat in [('quadratic',system),('polynomial',full)]:
            (out/f'{variant}-{suffix}.json').write_text(json.dumps(dat,indent=2)+'\n')
        results[variant]=dict(variables=204,quadraticRows=186,degree=4,content=1,coordinateMonomials=len(profiles),parameterSeparatedTerms=len(poly),coefficientHeight=ht)
    report=dict(schema='reciprocal204-construction/v27',sourceSha256=sha256(raw).hexdigest(),removedSourceCoordinates=sorted(REMOVED),removedSourceRows=sorted(REMOVED_ROWS),rescalingWeights=WEIGHTS,rescaledRows=transforms,newFieldPointPairs=[1,3],comparisonRatioMultipliers={'1':1,'3':2},aggregate='T=Tr(x(Q1)+x(Q3)+R^2*(x(Q2)+x(Q4)))/4',indexConvention='Q1 index n in (1/2)Z; Q2 index a in Z nonzero; Q3 index t/2 with t integer; Q4 index b in Z nonzero.',results=results,scope='Exact polynomial construction. Arithmetic proof uses the inherited premises, the separately proved weighted-height theorem, and doubling of R0 at selected Gaussian primes. No numerical defining threshold or complete external-source audit is asserted.')
    (out/'construction-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(results,indent=2));return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE);a=p.parse_args();build(a.output)
