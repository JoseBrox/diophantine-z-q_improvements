#!/usr/bin/env python3
"""Specify the quartic family obtained from two aggregate-trace height scales.

The family is exact. A defining member is an existence conclusion with an
ineffective threshold for N, as stated in the accompanying theorem.
"""
from pathlib import Path
from collections import defaultdict
from math import gcd
import hashlib,json

HERE=Path(__file__).resolve().parent
PIN='f7fb5bdf6a3d47275f1d78ed5e275954e2cc1f21fec8204d6a395bfc2f8b5394'

def main():
    raw=(HERE/'final389/quadratic-system389.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==PIN
    old=json.loads(raw)
    removed=[];coordinates=[];mapping={}
    for x in old['coordinates']:
        name=x['name']
        delete=(name.startswith('detector2.') or name.startswith('hybrid.det2.') or
                (name.startswith('heightProduct.') and name!='heightProduct.scale0.quadratic'))
        if delete:removed.append(x);continue
        mapping[x['id']]=len(coordinates)+1
        name='aggregateTrace.quarterSquare' if name=='heightProduct.scale0.quadratic' else name
        coordinates.append(dict(x,id=mapping[x['id']],name=name))
    gone={x['id'] for x in removed}
    byname={x['name']:x['id'] for x in old['coordinates']}
    trace={byname['A.chart.x.0.quadratic']:1,byname['S.chart.x.0.quadratic']:1,
           byname['T.chart.x.0.quadratic']:2,byname['Z.chart.x.0.quadratic']:1}
    new_scale=defaultdict(int)
    for x,a in trace.items():
        for y,b in trace.items():new_scale[tuple(sorted((x,y)))]+=a*b
    new_scale[(byname['heightProduct.scale0.quadratic'],)]=-4
    rows=[];deleted_rows=[]
    for r in old['residuals']:
        if r['sourceId']==295:
            terms=[{'parameterPower':0,'monomial':[mapping[j] for j in m],'coefficient':str(c)}
                    for m,c in sorted(new_scale.items())]
            rows.append(dict(r,name='aggregateTrace.quarterSquare.definition',terms=terms))
            continue
        if r['name'].startswith(('detector2.','hybrid.det2.','heightProduct.')):
            deleted_rows.append(r['sourceId']);continue
        assert not any(j in gone for t in r['terms'] for j in t['monomial']),r['name']
        rows.append(dict(r,terms=[dict(t,monomial=[mapping[j] for j in t['monomial']]) for t in r['terms']]))
    coefficients=defaultdict(int)
    for r in rows:
        for a in r['terms']:
            for b in r['terms']:
                coefficients[a['parameterPower']+b['parameterPower'],tuple(sorted(a['monomial']+b['monomial']))]+=int(a['coefficient'])*int(b['coefficient'])
    coefficients={k:c for k,c in coefficients.items() if c}
    terms=[{'parameterPower':e,'monomial':list(m),'coefficient':str(c)} for (e,m),c in sorted(coefficients.items())]
    parameter={'name':'A','base':80989,'exponent':'2*N+1','coordinate':False,
               'N':'An integer at least an ineffective threshold from the aggregate-trace height theorem.'}
    ir={'format':'integer-quadratic-family-v1','variables':len(coordinates),'inputCoordinate':1,
        'fixedParameter':parameter,'source':{'sha256':PIN,'construction':'quartic389'},
        'coordinates':coordinates,'residuals':rows}
    poly={'format':'integer-quartic-family-v1','variables':len(coordinates),'degree':4,'inputCoordinate':1,
          'fixedParameter':parameter,'coordinates':coordinates,'terms':terms}
    ordinary=defaultdict(dict)
    for (e,m),c in coefficients.items():ordinary[m][e]=c
    height_factor=max(sum(abs(c) for c in p.values()) for p in ordinary.values())
    out=HERE/'family329';out.mkdir(exist_ok=True)
    (out/'quadratic-family329.json').write_text(json.dumps(ir,indent=2)+'\n')
    (out/'polynomial-family329.json').write_text(json.dumps(poly,indent=2)+'\n')
    report={'status':'Exact family; defining parameters exist above an ineffective threshold.',
        'variables':len(coordinates),'quadraticResiduals':len(rows),
        'degree':max(len(m) for e,m in coefficients),'symbolicTerms':len(terms),
        'ordinaryMonomialsForSufficientlyLargeN':len(ordinary),
        'contentOfSymbolicCoefficients':gcd(*coefficients.values()),
        'coefficientBound':{'formula':'H(P_N)<=C*A^2 for A>=1','C':str(height_factor)},
        'removedCoordinates':removed,'deletedSourceRows':deleted_rows,
        'newScaleEquation':'(A.chart.x.0+S.chart.x.0+2*T.chart.x.0+Z.chart.x.0)^2=4*aggregateTrace.quarterSquare',
        'semanticScales':['1','F^2'],
        'warning':'No numerical value of a sufficient N is claimed. This is not an explicit defining polynomial in the coefficient sense.'}
    (out/'construction-report329.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','variables','quadraticResiduals','degree','symbolicTerms','ordinaryMonomialsForSufficientlyLargeN','coefficientBound']},indent=2))

if __name__=='__main__':main()
