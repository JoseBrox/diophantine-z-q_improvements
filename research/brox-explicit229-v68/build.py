#!/usr/bin/env python3
"""Reconstruct the literal 74,007-byte quartic from the fixed diagonal map."""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent


def dump(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def main():
    transform=json.loads((ROOT/'transformation.json').read_text())
    source_raw=(ROOT/transform['source']['local']).read_bytes()
    assert sha256(source_raw).hexdigest()==transform['source']['sha256']
    source=json.loads(source_raw)
    assert transform['fixed_N']==15 and transform['coordinate_powers'][0]==0
    assert len(transform['coordinate_powers'])==229
    assert len(transform['row_powers'])==207
    powers=transform['coordinate_powers']
    rows=[]
    for j,row in enumerate(source['residuals']):
        result=defaultdict(Fraction)
        for term in row['terms']:
            mon=tuple(term['monomial'])
            exponent=15*term['parameterPower']+sum(powers[i-1]for i in mon)+transform['row_powers'][j]
            result[mon]+=Fraction(int(term['coefficient']))*Fraction(149)**exponent
        assert all(c.denominator==1 for c in result.values())
        rows.append({m:int(c)for m,c in result.items()if c})
    quadratic=dict(schema='compact-explicit229-quadratic/v68',variables=229,inputCoordinate=1,residuals=[dict(id=j+1,name=source['residuals'][j]['name'],terms=[dict(monomial=list(m),coefficient=str(c))for m,c in sorted(row.items())])for j,row in enumerate(rows)])
    dump(ROOT/'quadratic.json',quadratic)
    polynomial=defaultdict(int)
    for row in rows:
        for m,c in row.items():
            for n,d in row.items():
                polynomial[tuple(sorted(m+n))]+=c*d
    polynomial={m:c for m,c in polynomial.items()if c}
    dump(ROOT/'polynomial.json',dict(schema='compact-explicit229-literal-polynomial/v68',variables=229,inputCoordinate=1,degree=4,terms=[dict(monomial=list(m),coefficient=str(c))for m,c in sorted(polynomial.items())]))
    pieces=[]
    for m,c in sorted(polynomial.items()):
        factors=[f'x{i}'+(f'^{a}'if a>1 else'')for i,a in sorted(Counter(m).items())]
        if abs(c)!=1 or not factors:factors.insert(0,str(abs(c)))
        pieces.append(('-'if c<0 else('+'if pieces else''))+'*'.join(factors))
    raw=''.join(pieces).encode('ascii')
    (ROOT/'quartic229-N15.txt').write_bytes(raw)
    print(json.dumps(dict(bytes=len(raw),sha256=sha256(raw).hexdigest(),rows=len(rows),monomials=len(polynomial)),indent=2))


if __name__=='__main__':main()
