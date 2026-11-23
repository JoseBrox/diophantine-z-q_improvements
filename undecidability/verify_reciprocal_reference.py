#!/usr/bin/env python3
"""Verify complete reciprocal-reference tables, including exact chart identities.

This checks finite algebra and metadata. It does not prove U_em, any retained
arithmetic interface, or a minimality statement.
"""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'undecidability/code'))
from build_reciprocal_reference import build

def expression(row,names):
    return sum(sp.sympify(t['coefficient'])*sp.prod(sp.Symbol(names[j-1]) for j in t['monomial']) for t in row['terms'])

for m,n,nrows in [(163,2085,1775),(179,2277,1943)]:
    base=ROOT/f'undecidability/coefficients/jones1980_shared/shared_reference_m{m}_quadrics.json'
    folder=ROOT/'undecidability/coefficients/jones1980_shared_reciprocal'
    table=folder/f'reciprocal_reference_m{m}_quadrics.json'
    certpath=folder/f'reciprocal_reference_m{m}_certificate.json'
    raw=table.read_bytes();actual=json.loads(raw);cert=json.loads(certpath.read_bytes())
    expected,expected_cert=build(m,ROOT,base)
    assert raw==(json.dumps(expected,separators=(',',':'),sort_keys=True)+'\n').encode()
    expected_cert['table_sha256']=hashlib.sha256(raw).hexdigest()
    assert cert==expected_cert
    assert actual['variables']==n and len(actual['residuals'])==nrows
    assert len(actual['variable_names'])==len(set(actual['variable_names']))==n
    assert len({r['name']for r in actual['residuals']})==nrows
    assert {i for r in actual['residuals']for t in r['terms']for i in t['monomial']}==set(range(1,n+1))
    assert max(len(t['monomial'])for r in actual['residuals']for t in r['terms'])==2
    assert 'i' not in actual['variable_names']
    for doc in [actual,cert]:
        assert doc['source_universality_hypothesis']=='U_em'
        assert doc['source_universality_verified']is False
        assert doc['unconditional_undecidability_claim']is False
    # Independently verify the six actual complete-table rows, without using
    # the producer's local six-row formulas or its audit_chart routine.
    old=json.loads(base.read_bytes());oldrows={r['name']:r for r in old['residuals']}
    newrows={r['name']:r for r in actual['residuals']}
    v=sp.Symbol('i_inverse');i=sp.Symbol('i')
    def z(j):return sp.Symbol(f'int_i_reciprocal_{j}')
    q0,q1,q2=(159,160,161)if m==163 else(162,163,164)
    q=z(q0);t=z(37);h=z(77);r=z(78)
    sub={i:1/v,t:t/(v*q),h:h/(v*q),r:r/v if m==163 else r/(v*v*q*q),z(q1):1/q,z(q2):1/q**2}
    factors={'inputSquare.definition':v*v,'scalar.rPair1.definition':v*v*q*q,
        'scalar.four_contact_product.definition':v*v*q*q,
        'scalar.forced_prime.definition':v if m==163 else v*v*q*q,
        'input.cleared.0':v*q,'input.cleared.1':v*q}
    for name,factor in factors.items():
        key='integer.i.'+name
        lhs=expression(oldrows[key],old['variable_names']).subs(sub,simultaneous=True)*factor
        rhs=expression(newrows[key],actual['variable_names'])
        assert sp.cancel(lhs-rhs)==0,key
    assert expression(newrows['integer.i.inputSquare.definition'],actual['variable_names'])==1-v*t
    assert 'integer.i_reciprocal.unit' not in newrows
    changed={'integer.i.'+name for name in factors}
    for name,row in oldrows.items():
        if name in changed or name=='integer.i_reciprocal.unit':continue
        assert expression(row,old['variable_names'])==expression(newrows[name],actual['variable_names']),name
    for row in actual['residuals']:
        for term in row['terms']:
            coef=sp.sympify(term['coefficient']);assert coef.free_symbols<=set(map(sp.Symbol,actual['parameters']))
            if coef.free_symbols:assert sp.Poly(coef,*sorted(coef.free_symbols,key=str)).domain==sp.ZZ
            else:assert coef.is_Integer
    print(f'm={m}: PASS, {n} coordinates, {nrows} quadratic rows; exact chart and complete table verified; U_em remains unverified')
