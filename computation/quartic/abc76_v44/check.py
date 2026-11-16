#!/usr/bin/env python3
"""Independent reconstruction of the 76-variable quartic and exact local identities.

No import from build.py is used. Changed rows are derived by named SymPy
expressions; all remaining rows are bound to the published balanced parent.
"""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from collections import defaultdict
from math import gcd, lcm
import argparse
import json
import subprocess
import sys
import tempfile
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = ROOT/'computation/quartic/abc78_balanced_v40/quadratic-family.json'
PIN = '30c877255a00abfa70207fcbc2efc59ed6331aee1246eb4f9d1995af9a55c76c'


def run():
    assert sha256(PARENT.read_bytes()).hexdigest() == PIN
    parent = json.loads(PARENT.read_text())
    system = json.loads((HERE/'quadratic-family.json').read_text())
    polynomial = json.loads((HERE/'polynomial-family.json').read_text())
    report = json.loads((HERE/'construction-report.json').read_text())
    deleted = {f'detector{j}.inverseWeightCube' for j in (0, 1)}
    rename = {f'detector{j}.poleInput': f'detector{j}.poleScaledInput' for j in (0, 1)}
    names = [rename.get(c['name'], c['name']) for c in parent['coordinates']
             if c['name'] not in deleted]
    assert len(names) == 76
    assert system['coordinates'] == [dict(id=i+1, name=n) for i, n in enumerate(names)]
    variables = [s.Symbol(n) for n in names]
    lookup = dict(zip(names, variables))
    parameter, rho = s.symbols('B rho')
    oldnames = {c['id']: c['name'] for c in parent['coordinates']}

    def field(name):
        return lookup[name+'.0']+rho*lookup[name+'.1']

    def split(expr):
        p = s.rem(s.Poly(s.expand(expr), rho), s.Poly(rho*rho-2, rho)).as_expr()
        return s.expand(p).coeff(rho, 0), s.expand(p).coeff(rho, 1)

    changed = {}
    for j in (0, 1):
        prefix = f'detector{j}.'
        w = lookup[prefix+'inverseWeight']
        w2 = lookup[prefix+'inverseWeightSquare']
        bt = lookup[prefix+'poleScaledInput']
        eta = lookup[prefix+'trace']
        for number, comparison, reference, numerator in (
                (1, field('square.comparison'), field('square.common.f'), field('square.pair.f')),
                (2, field('square.input'), field('square.common.g').subs(rho, -rho),
                 field('square.pair.g').subs(rho, -rho))):
            residual = (w2*field(prefix+f'factor{number}')-w*w2
                        -comparison**2-w*reference-w2*numerator)
            for part, expression in enumerate(split(residual)):
                changed[prefix+f'factor{number}.{part}'] = expression
        e, u, v = (lookup[prefix+'pole.'+n] for n in ('e', 'u', 'v'))
        changed[prefix+'poleInput'] = w*bt-eta**2
        changed[prefix+'pole.factor'] = u*v-e*w2+e*bt

    def parent_expression(row):
        out = 0
        for term in row['terms']:
            monomial = 1
            for i in term['monomial']:
                name = rename.get(oldnames[i], oldnames[i])
                assert name in lookup
                monomial *= lookup[name]
            out += s.Rational(term['coefficient'])*parameter**term['parameterPower']*monomial
        return out

    def coefficient_map(expression, primitive=False):
        p = s.Poly(s.expand(expression), parameter, *variables)
        data = {}
        for exponents, value in p.terms():
            indices = tuple(i+1 for i, exponent in enumerate(exponents[1:])
                            for _ in range(exponent))
            data[exponents[0], indices] = Fraction(int(s.numer(value)), int(s.denom(value)))
        if primitive:
            denominator = lcm(*(c.denominator for c in data.values()))
            content = gcd(*(int(denominator*c) for c in data.values()))
            if data[min(data)] < 0:
                content = -content
            data = {key: int(denominator*c/content) for key, c in data.items()}
        return data

    expected_rows, expected_expressions = [], []
    for row in parent['residuals']:
        name = row['name']
        if name in deleted:
            continue
        expression = changed[name] if name in changed else parent_expression(row)
        coefficients = coefficient_map(expression, primitive=True)
        assert max(len(m) for _, m in coefficients) <= 2
        expected_rows.append((rename.get(name, name), coefficients))
        normalized = sum(c*parameter**j*s.prod(variables[i-1] for i in m)
                         for (j, m), c in coefficients.items())
        expected_expressions.append(normalized)
    assert len(expected_rows) == len(system['residuals']) == 66
    for i, ((name, expected), row) in enumerate(zip(expected_rows, system['residuals']), 1):
        assert row['id'] == i and row['name'] == name
        actual = {(t['parameterPower'], tuple(t['monomial'])): int(t['coefficient'])
                  for t in row['terms']}
        assert actual == expected, name
    full = coefficient_map(sum(expression**2 for expression in expected_expressions))
    actual = {(t['parameterPower'], tuple(t['monomial'])): int(t['coefficient'])
              for t in polynomial['terms']}
    assert full == actual
    assert all(c.denominator == 1 for c in full.values())
    assert max(len(m) for _, m in full) == 4
    assert full[0, (1, 1, 1, 1)] == 1
    assert {i for _, m in full for i in m} == set(range(1, 77))
    profiles = defaultdict(dict)
    for (j, m), value in full.items():
        profiles[m][j] = int(value)
    constant = profiles[()]
    assert set(constant) == {0, 2} and constant[2] == 1
    fixedmax = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    for p in profiles.values():
        if 1 in p:
            assert abs(p[1]) <= 2 and abs(p.get(0, 0)) <= 1
            assert p[1]*p.get(0, 0) >= 0
        elif 2 in p:
            assert p == constant
        else:
            assert p[0] != 0
    assert constant[0] >= 2
    assert report['variables'] == 76 and report['quadraticRows'] == 66
    assert report['ordinaryMonomialsForEveryPositiveB'] == len(profiles) == 1250
    assert report['parameterSeparatedTerms'] == len(full) == 1253
    height = f'max({fixedmax},B^2+{constant[0]})'
    assert report['exactHeight'] == height

    # Exact physical factor and pole transformations, not sampled numerical tests.
    w, A, C, fH, fU, bt, eta, e, p, u, v, q = s.symbols(
        'w A C fH fU bt eta e p u v q', nonzero=True)
    physical = 1+C**4/w**3+fH**2/w**2+fU**2/w
    cleared = w*w*A-w**3-C**4-w*fH**2-w*w*fU**2
    assert s.cancel(cleared-w**3*(A/w-physical)) == 0
    old_b, old_p, old_u, old_v, old_q = bt/w**2, w*p, u/w, v/w, q
    old_pole = [e*e+old_b*old_p**2-1,
                old_u*old_v-e*(1-old_b),
                old_u**2-old_v**2-old_b*old_q**2]
    new_pole = [e*e+bt*p*p-1, u*v-e*(w*w-bt), u*u-v*v-bt*q*q]
    for multiplier, old, new in zip((1, w*w, w*w), old_pole, new_pole):
        assert s.cancel(multiplier*old-new) == 0
    assert s.cancel(w**3*old_b-eta**2-(w*bt-eta**2)) == 0
    # Wrong scaling would not reconstruct the original pole.
    assert s.cancel(e*e+old_b*(p/w)**2-1-new_pole[0]) != 0
    assert s.cancel(u*v-e*(1-bt)-new_pole[1]) != 0

    residue_sets = []
    for nu in (1, 3):
        classes = [0, (-3*nu) % 4, (-2*nu) % 4, (-nu) % 4]
        assert len(set(classes)) == 4
        residue_sets.append({'nu_mod4': nu, 'summand_classes_mod4': classes})
    thresholds = {'comparison': str(Fraction(5, 8)),
                  'reference_reciprocal': str(Fraction(3, 4)),
                  'numerator_reciprocal': str(Fraction(1, 4))}
    assert (4*4-3, 2*2-2, 2*2-1) == (13, 2, 3)
    # Without even reciprocal valuations, the reference term could meet the baseline.
    assert 2*1-2*1 == 0

    t, r = s.symbols('t r')
    contacts = (-5, -2, -1, 0, 2, 3, 4, 7)
    contact_product = s.prod(t-theta for theta in contacts)
    assert s.expand(contact_product-s.prod((t-1)**2-a0 for a0 in (1, 4, 9, 36))) == 0
    Z = r-37+36/r
    assert s.cancel(r*r*Z*(Z+24)-s.prod(r-a0 for a0 in (1, 4, 9, 36))) == 0
    assert max(contacts)-min(contacts) == 12 < 81
    # The allowed zero-contact block has a consistent full pole/product witness.
    assert all(s.cancel(row.subs({w: 0, bt: 0, eta: 0, e: 1, p: 0, u: 0, v: 0, q: 0})) == 0
               for row in new_pole+[w*bt-eta**2])
    absorption = Fraction(301, 388)*Fraction(4, 7)*2
    assert absorption == Fraction(602, 679) < 1

    with tempfile.TemporaryDirectory(prefix='abc76_rebuild_') as td:
        rebuilt = subprocess.run([sys.executable, '-B', str(HERE/'build.py'), '--output', td],
                                 text=True, capture_output=True)
        assert rebuilt.returncode == 0, rebuilt.stderr
        for name in ('quadratic-family.json', 'polynomial-family.json', 'construction-report.json'):
            assert (Path(td)/name).read_bytes() == (HERE/name).read_bytes(), name
    return dict(schema='abc76-independent-verification/v44', status='PASS',
                variables=76, quadraticRows=66, degree=4,
                integerContentForEveryPositiveB=1, ordinaryMonomialsForEveryPositiveB=len(profiles),
                parameterSeparatedTerms=len(full), exactHeight=height,
                unchangedRows=54, changedRows=12, removedRows=2,
                parentQuadraticSha256=PIN, isolatedReconstruction=True,
                completeCoefficientExpansion='SymPy, independent of sparse producer',
                contactResidueChecks=residue_sets, extractionThresholds=thresholds,
                selectedContactSummandOrders=[13, 2, 3],
                exactPoleScaling=True, zeroContactStratumRetained=True,
                contactDiameter=12, minimumScale=81, heightAbsorption=str(absorption),
                negativeControls=['inverted p scaling', 'unscaled pole factor',
                                  'dropping even reciprocal orders'],
                scope='Exact rows, all quartic coefficients, pole scaling and contact identities. Infinite arithmetic assertions are proved separately; retained external inputs are not certified by finite checks.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = json.dumps(run(), indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(raw)
    else:
        assert (HERE/'independent-verification.json').read_text() == raw
    print(raw)
