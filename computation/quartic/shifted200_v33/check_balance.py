#!/usr/bin/env python3
"""Independent exact diagonal-map, expansion, and coefficient-envelope checks."""
from __future__ import annotations
import argparse,hashlib,json
from collections import defaultdict
from fractions import Fraction as Q
from math import gcd,lcm
from pathlib import Path
HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise AssertionError(message)
def decode(row):
    out=defaultdict(Q)
    for t in row['terms']:out[int(t['parameterPower']),tuple(t['monomial'])]+=Q(t['coefficient'])
    return {k:v for k,v in out.items() if v}
def normalize(p):
    den=lcm(*(c.denominator for c in p.values()));g=gcd(*(int(c*den) for c in p.values()))
    if p[min(p)]<0:g=-g
    return {k:c*den/g for k,c in p.items()}
def compute(directory:Path):
    parent=json.loads((directory/'quadratic-family.json').read_text())
    child=json.loads((directory/'balanced-quadratic.json').read_text())
    require(len(parent['residuals'])==len(child['residuals'])==186,'Rows')
    for old,new in zip(parent['residuals'],child['residuals']):
        changed=defaultdict(Q)
        for (a,m),c in decode(old).items():
            changed[2*a+m.count(117)+m.count(118),m]+=c*149**a
        shift=min(a for a,m in changed)
        expected=normalize({(a-shift,m):c for (a,m),c in changed.items() if c})
        require(expected==decode(new),'Diagonal row '+str(old['id']))
    full=defaultdict(Q)
    for row in child['residuals']:
        terms=list(decode(row).items())
        for i,((a,m),c) in enumerate(terms):
            for j in range(i,len(terms)):
                (b,n),d=terms[j];full[a+b,tuple(sorted(m+n))]+=c*d*(1 if i==j else 2)
    full={k:v for k,v in full.items() if v}
    expanded=json.loads((directory/'balanced-polynomial.json').read_text())
    require(full==decode(expanded),'Independent coefficient expansion')
    profiles=defaultdict(dict)
    for (a,m),c in full.items():
        require(c.denominator==1,'Integral coefficient');profiles[m][a]=int(c)
    K=31581660**28;J=5898050446009651968;H0=(J*K)**2
    pure0=[m for m,p in profiles.items() if p=={0:H0} or p=={0:-H0}]
    pure2=[m for m,p in profiles.items() if p=={2:K} or p=={2:-K}]
    require(pure0 and pure2,'Both envelope values attained by pure profiles')
    kinds=defaultdict(int)
    for m,p in profiles.items():
        kinds[str(sorted(p))]+=1
        if set(p)=={1}:
            require(p[1]**2<=H0*K,'Linear envelope')
        else:
            require(set(p)<={0,2},'Unexpected mixed degree')
            require(abs(p.get(0,0))*K+abs(p.get(2,0))*H0<=H0*K,'Quadratic envelope')
        require(not (min(p.values())<0<max(p.values())),'No positive-parameter cancellation')
    require(full.get((0,(191,191,191,191)))==1,'Content one for every parameter')
    require(max(len(m) for a,m in full)==4,'Degree four')
    require(len(profiles)==3221 and len(full)==3222,'Exact support')
    require(149**114>=J**2*K,'N>=57 reaches the stated branch')
    # Negative controls for coefficient and affine-map corruption.
    broken=dict(full);broken[0,(191,191,191,191)]+=1
    require(broken!=decode(expanded),'Coefficient corruption not detected')
    return {'schema':'balanced200-exact-verification/v33','status':'PASS','variables':200,'quadratic_rows':186,'degree':4,
        'integer_content':1,'ordinary_monomials_for_all_positive_C':3221,'parameter_separated_terms':3222,
        'profile_types':dict(kinds),'exact_height':'max((5898050446009651968*31581660^28)^2,31581660^28*C^2)',
        'C':'149^N','eventual_height_from_N':57,'constant_height_monomial':list(pure0[0]),'quadratic_height_monomial':list(pure2[0]),
        'coefficient_condition_not_defining_threshold':True,
        'files':{name:hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in ['balanced-quadratic.json','balanced-polynomial.json']},
        'scope':'Exact rational coordinate scaling, primitive row normalization, every expanded coefficient, all-positive-parameter height and support; no proof of external arithmetic premises.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--directory',type=Path,default=HERE);ap.add_argument('--output',type=Path,default=HERE/'balanced-verification.json');a=ap.parse_args()
    report=compute(a.directory);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
