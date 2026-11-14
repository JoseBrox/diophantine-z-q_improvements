#!/usr/bin/env python3
"""Rescale six coordinates of the pinned 214-coordinate quartic family.

The parameter A=149^(2N+1) becomes A=149*C^2, C=149^N.  This is
an invertible rational coordinate change for every nonzero C, not a
change to the arithmetic premises or sufficient defining threshold.
Standard library only. Run check.py separately after reconstruction.
"""
from __future__ import annotations
from collections import defaultdict
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SCALED = frozenset({90, 91, 93, 117, 118, 120})
SOURCE_SHA = '49cf4066bf1e35e02e2156bf4bd24a21bb4c5e794f7374e056413d8306fb73c5'
K = 31581660**28
J = 5898050446009651968
A0 = (J*K)**2


def serialize(p: dict) -> list[dict]:
    return [dict(parameterPower=a, monomial=list(m), coefficient=str(c))
            for (a, m), c in sorted(p.items()) if c]


def main() -> None:
    raw = (HERE/'source/quadratic214.json').read_bytes()
    if sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError('The reconstructed source rows have changed.')
    src = json.loads(raw)
    rows, polynomial, changes = [], defaultdict(int), []
    for row in src['residuals']:
        source_terms = row['terms']
        powers = [2*t['parameterPower'] + sum(i in SCALED for i in t['monomial'])
                  for t in source_terms]
        m = min(powers)
        p = defaultdict(int)
        for t, a in zip(source_terms, powers):
            p[a-m, tuple(sorted(t['monomial']))] += int(t['coefficient'])*149**t['parameterPower']
        p = {k: v for k, v in p.items() if v}
        if max(a for a, _ in p) > 1 or max(len(x) for _, x in p) > 2:
            raise ValueError('The transformed row is not quadratic and linear in C.')
        common = gcd(*p.values())
        if common != 1:
            raise ValueError('Unexpected integer row content; update the proof first.')
        sign = 1 if p[min(p)] > 0 else -1
        p = {k: sign*v for k, v in p.items()}
        if m or any(powers):
            changes.append(row['id'])
        rows.append(dict(id=row['id'], name=row['name'], divided_C_power=m,
                         row_sign=sign, terms=serialize(p)))
        for (a, u), c in p.items():
            for (b, v), d in p.items():
                polynomial[a+b, tuple(sorted(u+v))] += c*d
    polynomial = {k: v for k, v in polynomial.items() if v}
    profiles = defaultdict(dict)
    for (a, m), c in polynomial.items():
        profiles[m][a] = c
    if len(rows) != 188 or len(profiles) != 2919 or len(polynomial) != 2924:
        raise ValueError('Unexpected row or support count.')
    if max(abs(p.get(0, 0)) for p in profiles.values()) != A0:
        raise ValueError('Incorrect largest constant coefficient.')
    if max(abs(p.get(2, 0)) for p in profiles.values()) != K:
        raise ValueError('Incorrect largest quadratic coefficient.')
    for p in profiles.values():
        if set(p) == {1}:
            assert p[1]**2 <= A0*K
        else:
            assert set(p) <= {0, 2}
            assert abs(p.get(0, 0))*K + abs(p.get(2, 0))*A0 <= A0*K
    coordinates = json.loads((HERE/'source/coordinates214.json').read_text())
    for c in coordinates:
        c['old_coordinate_equals'] = ('C*' if c['id'] in SCALED else '')+f"Y{c['id']}"
    parameter = dict(name='C', value='149^N', quantified=False,
                     defining_threshold='Same fixed ineffective threshold as the pinned 214 source.')
    system = dict(format='integer-quadratic-family-balanced214-v24', variables=214,
                  inputCoordinate=1, fixedParameter=parameter,
                  scaled_coordinates=sorted(SCALED), coordinates=coordinates, residuals=rows)
    expanded = dict(format='integer-quartic-family-balanced214-v24', variables=214,
                    degree=4, inputCoordinate=1, fixedParameter=parameter,
                    terms=serialize(polynomial))
    report = dict(schema='balanced214-construction/v24', variables=214, quadratic_rows=188,
                  degree=4, content=gcd(*polynomial.values()), symbolic_terms=len(polynomial),
                  coordinate_monomials=len(profiles), changed_rows=changes,
                  source_rows_sha256=SOURCE_SHA,
                  height_constants=dict(K=str(K), J=str(J), A0=str(A0)),
                  height_for_every_positive_C='max((5898050446009651968*31581660^28)^2,31581660^28*C^2)',
                  height_for_N_at_least_57='31581660^28*149^(2*N)',
                  strict_height_improvement_over_source_for_N_at_least=53,
                  constant_maximum_monomial=[112,112,112,112],
                  quadratic_maximum_monomial=[109,109,117,117],
                  algebraic_scope='Exact rational projection equivalence for every positive integer C.',
                  arithmetic_scope='No new arithmetic premise, threshold or acceptance. Integer-definability is inherited only to the extent established for the pinned source.')
    for name, obj in [('quadratic-family-balanced214-v24.json',system),
                      ('polynomial-family-balanced214-v24.json',expanded),
                      ('construction-report.json',report)]:
        (HERE/name).write_text(json.dumps(obj, indent=2)+'\n')
    print('214 coordinates; 188 quadratic rows; degree 4; 2919 monomials; exact height max(A0,K*C^2).')

if __name__ == '__main__':
    main()
