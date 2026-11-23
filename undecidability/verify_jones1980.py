#!/usr/bin/env python3
"""Reconstruct the emended-source quartic checkpoint and compare all sparse rows.

This verifies finite identities and specifications. The infinite arithmetic
interfaces are retained, and emended-source universality U_em is unresolved.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'undecidability'
sys.path.insert(0, str(BASE/'code'))
import jones1980_system as source
import build_jones1980_combined as combined
import sympy as sp


def verify():
    actual_source = source.audit()
    stored_source = json.loads((BASE/'certificates/jones1980_source.json').read_text())
    assert actual_source == stored_source
    assert actual_source['instance_restriction'] == 'x > 2*z (cofinite tail preserves undecidability)'
    result = {}
    for m, rows_per_block in ((163,137),(179,151),(56,46)):
        table, certificate = combined.build(m, ROOT, BASE/'code/jones1980_system.py')
        table_path = BASE/f'coefficients/jones1980/jones1980_m{m}_quadrics.json'
        raw = table_path.read_bytes()
        assert raw == (json.dumps(table,separators=(',',':'),sort_keys=True)+'\n').encode(), (m,'sparse table mismatch')
        certificate['table_sha256'] = hashlib.sha256(raw).hexdigest()
        assert json.loads(table_path.with_name(f'jones1980_m{m}_certificate.json').read_text()) == json.loads(json.dumps(certificate))
        assert table['variables'] == 12*m+239
        assert len(table['residuals']) == 219+12*rows_per_block
        # Independently inspect the stored sparse representation, rather than
        # relying solely on the generating symbolic objects.
        names = table['variable_names']
        assert len(names) == len(set(names)) == table['variables']
        parameters = sp.symbols(' '.join(table['parameters']))
        loc = dict(zip(table['parameters'],parameters))
        support = set()
        quadratic_seen = False
        for row in table['residuals']:
            assert row['terms']
            for term in row['terms']:
                mon = term['monomial']
                assert len(mon) <= 2 and all(1 <= j <= len(names) for j in mon)
                support.update(mon)
                coefficient = sp.sympify(term['coefficient'],locals=loc)
                assert coefficient != 0
                assert sp.Poly(coefficient,*parameters).domain.is_ZZ
                quadratic_seen |= len(mon)==2
        assert support == set(range(1,len(names)+1)) and quadratic_seen
        # A nonzero pure triangular square term survives every specialization;
        # sums of real squares therefore have degree exactly four.
        guard_rows = [r for r in table['residuals'] if r['name'].startswith('jones1980.positive.')]
        assert len(guard_rows)==11
        assert all(any(len(t['monomial'])==2 and t['monomial'][0]==t['monomial'][1]
                       and names[t['monomial'][0]-1].startswith('positive_')
                       and t['coefficient']=='-1' for t in r['terms']) for r in guard_rows)
        result[str(m)] = {'variables':len(names),'quadratic_residuals':len(table['residuals']),
                          'table_sha256':certificate['table_sha256']}
    # This is a local discrepancy example, deliberately not asserted to solve
    # every row of the historical source.
    A,E,F=2,4,7
    assert F*F-(A*A-1)*E*E==1
    G=A+F*F*(F*F-A)
    assert G==2305 and G-1==48**2
    return {'status':'PASS','formula':'12*m+239','row_formula':'219+12*q0',
            'routes':result,'source_reconstruction':'emended Jones1980/Matiyasevich1999 system',
            'universality_hypothesis':'U_em','universality_independently_verified':False,
            'historical_MT_universality':'unresolved',
            'scope':'Exact source circuit, Laurent identities, all sparse rows, degree and counts; all integer-predicate premises are retained; universality U_em of the emended source remains unverified.'}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True))
