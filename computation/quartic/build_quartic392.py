#!/usr/bin/env python3
"""Construct the forced-prime quartic from the pinned 394-coordinate source.

Only exact rational arithmetic is used. The fixed integer A=80989**54929
is retained symbolically; it is a coefficient, never a coordinate.
The finite checks establish the stated algebraic construction. The arithmetic
projection theorem additionally uses the hypotheses stated in quartic392.tex.
"""
from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'upstream'/'candidate394-ir.json'
PIN='7eb02f9913b55d60a790a287616f1bb80d9f93523e9f11e12481c9ab955746a5'
ELL=80989
N=27464
EXPONENT=2*N+1
PARAMETER_ID=702
NEW_ROW_ID=733
RAW={():-105275102108,(0,):-8412883296,(248,):-8412883296,
     (487,):-21050600,(488,):-7629700,(489,):-45771136}


def terms(poly):
    return [{'parameterPower':e,'monomial':list(m),'coefficient':str(c)}
            for (e,m),c in sorted(poly.items()) if c]


def term(c,mon=(),power=0):
    return {(power,tuple(sorted(mon))):Fraction(c)}


def plus(*polys):
    out=defaultdict(Fraction)
    for p in polys:
        for k,v in p.items():out[k]+=v
    return {k:v for k,v in out.items() if v}


def scale(p,c):return {k:v*c for k,v in p.items() if v*c}


def mul(p,q):
    out=defaultdict(Fraction)
    for (e,m),c in p.items():
        for (f,n),d in q.items():out[e+f,tuple(sorted(m+n))]+=c*d
    return {k:v for k,v in out.items() if v}


def source_poly(row):
    return {(t['sPower'],tuple(t['monomial'])):Fraction(t['coefficient'])
            for t in row['terms']}


def primitive(p):
    den=lcm(*(c.denominator for c in p.values()))
    common=gcd(*(int(c*den) for c in p.values()))
    return {k:int(c*den)//common for k,c in p.items()}


def main():
    raw=SOURCE.read_bytes()
    assert sha256(raw).hexdigest()==PIN
    src=json.loads(raw)
    assert len(src['coordinates'])==394 and len(src['residuals'])==364
    old={r['id']:r for r in src['residuals']}
    r=plus(*(term(c,m) for m,c in RAW.items()))
    A=term(1,power=1)
    R=term(1,(PARAMETER_ID,))
    assert source_poly(old[560])==plus(term(1,(600,)),scale(mul(r,r),-1))
    assert source_poly(old[566])==plus(term(1,(540,604)),term(-1,(508,508)),scale(mul(r,term(1,(539,))),-1))
    assert source_poly(old[512])==plus(term(1,(542,604)),term(-1,(540,540)),scale(mul(r,term(1,(541,))),-1))
    assert source_poly(old[492])==plus(term(1,(525,600)),scale(mul(r,term(1,(525,))),4896),term(82479248,(526,)))
    changes={
        560:plus(term(1,(600,)),scale(mul(R,R),-1)),
        566:plus(term(1,(540,604)),term(-1,(508,508)),term(-1,(539,PARAMETER_ID))),
        512:plus(term(1,(542,604)),term(-1,(540,540)),term(-1,(541,PARAMETER_ID))),
        492:plus(term(1,(525,600)),term(4896,(525,PARAMETER_ID)),term(82479248,(526,))),
        NEW_ROW_ID:plus(R,scale(mul(r,R),ELL*ELL),scale(mul(A,r),-1))}
    removed={55,56,57}
    assert [row['id'] for row in src['residuals'] if any(set(t['monomial'])&removed for t in row['terms'])]==[504]
    assert [row['id'] for row in src['residuals'] if any(t['sPower'] for t in row['terms'])]==[504]
    coords=[{'sourceId':c['id'],'name':c['name'],'kind':c['kind']} for c in src['coordinates'] if c['id'] not in removed]
    coords.append({'sourceId':PARAMETER_ID,'name':'scalar.forced_positive_parameter','kind':'gate'})
    coords.sort(key=lambda c:c['sourceId'])
    for i,c in enumerate(coords,1):c['id']=i
    ids={c['sourceId']:c['id'] for c in coords}
    rows=[]
    for row in src['residuals']:
        if row['id']==504:continue
        p=changes.get(row['id'],source_poly(row))
        rows.append({'sourceId':row['id'],'name':row['name'], 'terms':terms(primitive(p))})
    rows.append({'sourceId':NEW_ROW_ID,'name':'scalar.forced_prime.definition','terms':terms(primitive(changes[NEW_ROW_ID]))})
    # Both the construction and public polynomial use consecutive 1-based ids.
    for row in rows:
        for t in row['terms']:t['monomial']=[ids[v] for v in t['monomial']]
    residuals={r['sourceId']:{(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in r['terms']} for r in rows}
    full=plus(*(mul(p,p) for p in residuals.values()))
    common=gcd(*(int(c) for c in full.values()))
    assert common==1
    assert len(coords)==392 and len(rows)==364
    assert max(len(m) for _,m in full)==4
    used=set(v for _,m in full for v in m)
    assert used==set(range(1,393))
    parameter={'name':'A','base':ELL,'exponent':EXPONENT,'coordinate':False}
    ir={'format':'integer-quadratic-system-v1','variables':392,'inputCoordinate':1,
        'fixedParameter':parameter,'source':{'commit':'5bbd74f6a479776a332cbe036809d5dddae63720','sha256':PIN},
        'coordinates':coords,'residuals':rows}
    polynomial={'format':'integer-quartic-consecutive-coordinates-v3','variables':392,
        'degree':4,'inputCoordinate':1,'fixedParameter':parameter,'coordinates':coords,'terms':terms(full)}
    out=HERE/'final392';out.mkdir(exist_ok=True)
    (out/'quadratic-system392.json').write_text(json.dumps(ir,indent=2)+'\n')
    (out/'polynomial392.json').write_text(json.dumps(polynomial,indent=2)+'\n')
    ordinary=defaultdict(dict)
    for (e,m),c in full.items():ordinary[m][e]=int(c)
    # The huge value is evaluated for comparisons only; no decimal expansion is stored.
    av=pow(ELL,EXPONENT)
    values={m:sum(c*pow(av,e) for e,c in coeff.items()) for m,coeff in ordinary.items()}
    assert all(values.values())
    maximum=max(values,key=lambda m:abs(values[m]))
    height={'monomial':list(maximum),'sign':1 if values[maximum]>0 else -1,
            'coefficientPolynomial':{str(e):str(c) for e,c in sorted(ordinary[maximum].items())},
            'bitLength':abs(values[maximum]).bit_length()}
    report={'variables':392,'quadraticResiduals':364,'degree':4,'content':1,
        'symbolicTerms':len(full),'ordinaryMonomials':len(ordinary),'coefficientHeight':height,
        'fixedPrime':ELL,'normalizerExponent':EXPONENT,'minimumPrimeValuation':2*N-1,
        'minimumIndexDepth':187*(2*N-1)//8+1,
        'modifiedSourceRows':[492,512,560,566], 'removedSourceRows':[504],
        'removedSourceCoordinates':sorted(removed),'newSourceCoordinate':PARAMETER_ID,'newSourceRow':NEW_ROW_ID,
        'rawContactAffine':{','.join(map(str,m)):str(c) for m,c in RAW.items()},
        'checksScope':'Exact construction, coefficient table and finite numerical certificates; arithmetic hypotheses are stated separately in the paper.'}
    (out/'construction-report392.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
