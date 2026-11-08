#!/usr/bin/env python3
"""Exact quadratic-extension specialization of the supplied 392-variable quartic."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
import json

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'final392'
poly=json.loads((DATA/'polynomial392.json').read_text())
system=json.loads((DATA/'quadratic-system392.json').read_text())
coordinate=next(c['id'] for c in system['coordinates'] if c['sourceId']==527)
assert coordinate==293
# At input X=1/2, set all coordinates except this private square-output to zero.
def restrict(terms):
    out=defaultdict(Fraction)
    for t in terms:
        m=t['monomial']
        if any(i not in (1,coordinate) for i in m):continue
        out[t['parameterPower'],m.count(coordinate)]+=Fraction(t['coefficient'])*Fraction(1,2)**m.count(1)
    return {k:v for k,v in out.items() if v}
from_table=restrict(poly['terms'])
from_rows=defaultdict(Fraction)
for row in system['residuals']:
    p=restrict(row['terms'])
    for (e,i),a in p.items():
        for (f,j),b in p.items():from_rows[e+f,i+j]+=a*b
from_rows={k:v for k,v in from_rows.items() if v}
assert from_rows==from_table
assert from_table[(0,2)]==1
assert set(from_table)=={(0,2),(0,0),(2,0)}
assert from_table[(0,0)]>0 and from_table[(2,0)]>0
D={str(e):str(16*c) for (e,i),c in from_table.items() if i==0}
assert all(Fraction(c).denominator==1 for c in D.values())
receipt={'status':'passed','input':'1/2','freeCoordinate':coordinate,
 'sourceCoordinate':527,'coordinateName':'normalized_scalar.p2.quadratic',
 'specialization':'Y^2 + D/16',
 'DPolynomialInA':D,'fixedA':{'base':80989,'exponent':54929},
 'field':'Q(sqrt(-D))','witness':'Y=sqrt(-D)/4; every other witness is zero',
 'conclusion':'The unchanged quartic accepts 1/2 over this imaginary quadratic field. Since a rational algebraic integer is an integer, its input projection there is not the ring of integers.',
 'independentChecks':['Direct substitution into the complete coefficient table','Separate substitution into all quadratic residuals followed by exact squaring'],
 'polynomialSHA256':sha256((DATA/'polynomial392.json').read_bytes()).hexdigest()}
(DATA/'field-specialization392.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
