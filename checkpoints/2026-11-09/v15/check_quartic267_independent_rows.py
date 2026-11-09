#!/usr/bin/env python3
"""Read-only independent reconstruction of the scale-free row replacement."""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'repo/computation/quartic'

def read_table(path):
    raw = path.read_bytes()
    table = json.loads(raw)
    ids = {c['id']: c['sourceId'] for c in table['coordinates']}
    def decode(row):
        return {(t['parameterPower'], tuple(sorted(ids[i] for i in t['monomial']))):
                int(t['coefficient']) for t in row['terms']}
    return table, decode, sha256(raw).hexdigest()

source, ds, hs = read_table(FOLDER / 'family273/quadratic-family273.json')
target, dt, ht = read_table(FOLDER / 'family267/quadratic-family267.json')
poly, dp, hp = read_table(FOLDER / 'family267/polynomial-family267.json')
assert hs == 'c2e2ad2838e79aa38c93bd41aa079d612826b5991c19835b88e14ec12fecc18b'
removed_coordinates = {343, 395, 396, 397, 20100, 20101}
removed_rows = {295, 349, 350, 351, 20100, 20101}
expected = {r['sourceId']: ds(r) for r in source['residuals']
            if r['sourceId'] not in removed_rows}
expected[345] = {(0, (37, 82)): 1, (0, (37, 84)): 1,
                 (0, (37, 86)): 2, (0, (37, 88)): 1, (0, (391,)): -2}
expected[352] = {(0, (394, 398)): 1, (0, (20022, 20022)): -1}
actual = {r['sourceId']: dt(r) for r in target['residuals']}
assert expected == actual and len(actual) == 241
assert {c['sourceId'] for c in source['coordinates']} - removed_coordinates == {
    c['sourceId'] for c in target['coordinates']}
assert target['coordinates'] == poly['coordinates']
assert target['variables'] == poly['variables'] == 267
expanded = defaultdict(int)
for row in actual.values():
    for (a, m), (b, n) in combinations_with_replacement(row, 2):
        factor = 1 if (a, m) == (b, n) else 2
        expanded[a+b, tuple(sorted(m+n))] += factor*row[a, m]*row[b, n]
expanded = {k: v for k, v in expanded.items() if v}
assert expanded == dp(poly)
ordinary = defaultdict(dict)
for (a, m), c in expanded.items(): ordinary[m][a] = c
assert max(len(m) for a, m in expanded) == 4
assert gcd(*expanded.values()) == 1
assert ordinary[(489, 489)] == {0: 1, 2: 1}
assert all(set(c) in ({0}, {1}, {0, 2}) for c in ordinary.values())
C = max(abs(c[0]) for c in ordinary.values() if set(c) == {0})
L = max(abs(c[1]) for c in ordinary.values() if set(c) == {1})
assert C.bit_length() == 1520 and L == 2*80989**2 and C > L**2
assert 80989**90+1 < C < 80989**94+1
report = dict(status='PASS', variables=267, quadratic_residuals=241,
              ordinary_monomials=len(ordinary), symbolic_terms=len(expanded),
              degree=4, content=1, constant_coefficient_bits=C.bit_length(),
              exact_height_for_N_at_least_23='80989^(4N+2)+1',
              source_sha256=hs, system_sha256=ht, polynomial_sha256=hp,
              verified='Every retained row, both changed rows, removed coordinates, independent unordered-pair sum-of-squares expansion and height formula',
              limitation='No inherited arithmetic premise is proved by this finite coefficient check.')
output = ROOT / 'quartic267_independent_reconstruction.json'
output.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
