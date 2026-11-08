#!/usr/bin/env python3
"""Construct the389-variable quartic by removing three locally redundant guards."""
from pathlib import Path
from collections import defaultdict
from math import gcd
import gzip
import hashlib
import json

HERE=Path(__file__).resolve().parent
BASE=HERE/'baseline392'
IR_PIN='b66609c16f649481ea8edb14785af2fb6f9da151f76d75dfa203f9db189e93a0'
P_PIN='65f978c8b6418395535816a485093213631623766024555c69ef5db6c185450d'
REMOVED_SOURCE_COORDINATES={382,430,478}
REMOVED_SOURCE_ROWS={334,384,434}

def read(name,pin):
    raw=gzip.decompress((BASE/(name+'.gz')).read_bytes())
    assert hashlib.sha256(raw).hexdigest()==pin
    return json.loads(raw)

def main():
    source=read('quadratic-system392.json',IR_PIN)
    read('polynomial392.json',P_PIN)
    old_removed={c['id'] for c in source['coordinates'] if c['sourceId'] in REMOVED_SOURCE_COORDINATES}
    assert old_removed=={221,250,279}
    for row in source['residuals']:
        used={v for term in row['terms'] for v in term['monomial']}
        if used&old_removed:
            assert row['sourceId'] in REMOVED_SOURCE_ROWS
    coordinates=[]
    renumber={}
    for c in source['coordinates']:
        if c['id'] in old_removed:continue
        renumber[c['id']]=len(coordinates)+1
        coordinates.append(dict(c,id=renumber[c['id']]))
    residuals=[]
    for row in source['residuals']:
        if row['sourceId'] in REMOVED_SOURCE_ROWS:continue
        terms=[dict(term,monomial=[renumber[x] for x in term['monomial']]) for term in row['terms']]
        residuals.append(dict(row,terms=terms))
    coefficients=defaultdict(int)
    for row in residuals:
        for a in row['terms']:
            for b in row['terms']:
                exponent=a['parameterPower']+b['parameterPower']
                monomial=tuple(sorted(a['monomial']+b['monomial']))
                coefficients[exponent,monomial]+=int(a['coefficient'])*int(b['coefficient'])
    coefficients={key:value for key,value in coefficients.items() if value}
    terms=[{'parameterPower':e,'monomial':list(m),'coefficient':str(c)}
           for (e,m),c in sorted(coefficients.items())]
    ir={'format':'integer-quadratic-system-v1','variables':len(coordinates),
        'inputCoordinate':1,'fixedParameter':source['fixedParameter'],
        'source':{'repository':'JoseBrox/diophantine-z-q_improvements',
                  'commit':'de7aa60dd1794d7ea62a8a83cdc4bfd22380c74f',
                  'sha256':IR_PIN},'coordinates':coordinates,'residuals':residuals}
    polynomial={'format':'integer-quartic-consecutive-coordinates-v3',
        'variables':len(coordinates),'degree':4,'inputCoordinate':1,
        'fixedParameter':source['fixedParameter'],'coordinates':coordinates,'terms':terms}
    out=HERE/'final389';out.mkdir(exist_ok=True)
    (out/'quadratic-system389.json').write_text(json.dumps(ir,indent=2)+'\n')
    (out/'polynomial389.json').write_text(json.dumps(polynomial,indent=2)+'\n')
    ordinary=defaultdict(dict)
    for (e,m),c in coefficients.items():ordinary[m][e]=c
    a=80989**54929
    values={m:sum(c*a**e for e,c in v.items()) for m,v in ordinary.items()}
    assert all(values.values())
    maximum=max(values,key=lambda m:abs(values[m]))
    report={'variables':len(coordinates),'quadraticResiduals':len(residuals),
        'degree':max(len(m) for e,m in coefficients),'content':gcd(*coefficients.values()),
        'ordinaryMonomials':len(ordinary),'symbolicTerms':len(terms),
        'removedSourceCoordinates':sorted(REMOVED_SOURCE_COORDINATES),
        'removedSourceRows':sorted(REMOVED_SOURCE_ROWS),
        'coefficientHeight':{'monomial':list(maximum),
            'coefficientPolynomial':{str(e):str(c) for e,c in sorted(ordinary[maximum].items())},
            'bitLength':abs(values[maximum]).bit_length()},
        'guardProjection':'Each deleted guard has a unique rational lift whenever the corresponding contact radical is nontrivial; otherwise its divisibility conclusion is vacuous.',
        'scope':'Exact polynomial construction. The integer projection is proved in the accompanying paper relative to the retained arithmetic premises.'}
    (out/'construction-report389.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['variables','quadraticResiduals','degree','content','ordinaryMonomials','symbolicTerms']},indent=2))

if __name__=='__main__':main()
