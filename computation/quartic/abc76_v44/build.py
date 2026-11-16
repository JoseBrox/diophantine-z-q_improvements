#!/usr/bin/env python3
"""Exact 76-coordinate detector source from the balanced abc78 source.

This producer uses sparse rational coefficient dictionaries only. Its separate
checker reconstructs every changed named row and expands the squares in SymPy.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd, lcm
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = ROOT/'computation/quartic/abc78_balanced_v40/quadratic-family.json'
PIN = '30c877255a00abfa70207fcbc2efc59ed6331aee1246eb4f9d1995af9a55c76c'


def clean(p):
    return {m: Q(c) for m, c in p.items() if c}


def add(*polys):
    result = defaultdict(Q)
    for p in polys:
        for m, c in p.items():
            result[m] += c
    return clean(result)


def scale(p, c):
    return clean({m: c*v for m, v in p.items()})


def multiply(p, q):
    result = defaultdict(Q)
    for (j, m), c in p.items():
        for (k, n), d in q.items():
            result[j+k, tuple(sorted(m+n))] += c*d
    return clean(result)


def square(p):
    return multiply(p, p)


def variable(name):
    return {(0, (name,)): Q(1)}


def kplus(*values):
    return tuple(add(*(v[j] for v in values)) for j in range(2))


def ktimes(x, y):
    return (add(multiply(x[0], y[0]), scale(multiply(x[1], y[1]), 2)),
            add(multiply(x[0], y[1]), multiply(x[1], y[0])))


def ksquare(x):
    return ktimes(x, x)


def kminus(x, y):
    return (add(x[0], scale(y[0], -1)), add(x[1], scale(y[1], -1)))


def rational(p):
    return (p, {})


def field(name):
    return (variable(name+'.0'), variable(name+'.1'))


def conjugate(x):
    return (x[0], scale(x[1], -1))


def serialize(p):
    return [dict(parameterPower=j, monomial=list(m), coefficient=str(c))
            for (j, m), c in sorted(p.items())]


def build(output=HERE):
    source_bytes = PARENT.read_bytes()
    source_hash = sha256(source_bytes).hexdigest()
    assert source_hash == PIN
    parent = json.loads(source_bytes)
    deleted = {f'detector{j}.inverseWeightCube' for j in range(2)}
    rename = {f'detector{j}.poleInput': f'detector{j}.poleScaledInput' for j in range(2)}
    names = [rename.get(c['name'], c['name']) for c in parent['coordinates']
             if c['name'] not in deleted]
    ids = {name: j+1 for j, name in enumerate(names)}
    oldnames = {c['id']: c['name'] for c in parent['coordinates']}
    changes = {}
    C2, I2 = field('square.comparison'), field('square.input')
    FH, GH = field('square.common.f'), field('square.common.g')
    FU, FV = field('square.pair.f'), field('square.pair.g')
    for j in range(2):
        prefix = f'detector{j}.'
        w = variable(prefix+'inverseWeight')
        w2 = variable(prefix+'inverseWeightSquare')
        eta = variable(prefix+'trace')
        bt = variable(prefix+'poleScaledInput')
        e, u, v = (variable(prefix+'pole.'+n) for n in ('e', 'u', 'v'))
        for number, comp, ref, point in ((1, C2, FH, FU),
                                         (2, I2, conjugate(GH), conjugate(FV))):
            A = field(prefix+f'factor{number}')
            rhs = kplus(rational(multiply(w, w2)), ksquare(comp),
                        ktimes(rational(w), ref), ktimes(rational(w2), point))
            residual = kminus(ktimes(rational(w2), A), rhs)
            for part in range(2):
                changes[prefix+f'factor{number}.{part}'] = residual[part]
        changes[prefix+'poleInput'] = add(multiply(w, bt), scale(square(eta), -1))
        changes[prefix+'pole.factor'] = add(multiply(u, v),
                                           scale(multiply(e, w2), -1), multiply(e, bt))

    def primitive_named(p):
        numeric = {(j, tuple(sorted(ids[name] for name in m))): c
                   for (j, m), c in p.items()}
        denominator = lcm(*(c.denominator for c in numeric.values()))
        content = gcd(*(int(denominator*c) for c in numeric.values()))
        if numeric[min(numeric)] < 0:
            content = -content
        return {m: int(denominator*c/content) for m, c in numeric.items()}

    rows = []
    for row in parent['residuals']:
        name = row['name']
        if name in deleted:
            continue
        if name in changes:
            p = changes[name]
        else:
            p = {}
            for term in row['terms']:
                monomial = tuple(sorted(rename.get(oldnames[i], oldnames[i])
                                        for i in term['monomial']))
                assert not any(n in deleted for n in monomial)
                p[term['parameterPower'], monomial] = Q(term['coefficient'])
        p = primitive_named(p)
        assert max(len(m) for _, m in p) <= 2
        rows.append(dict(id=len(rows)+1, name=rename.get(name, name), terms=serialize(p)))
    assert len(names) == 76 and len(rows) == 66
    expanded = defaultdict(int)
    for row in rows:
        p = {(t['parameterPower'], tuple(t['monomial'])): int(t['coefficient'])
             for t in row['terms']}
        for key, value in square(p).items():
            assert value.denominator == 1
            expanded[key] += int(value)
    expanded = {m: c for m, c in expanded.items() if c}
    assert max(len(m) for _, m in expanded) == 4
    assert expanded[0, (1, 1, 1, 1)] == 1
    assert {i for _, m in expanded for i in m} == set(range(1, 77))
    profiles = defaultdict(dict)
    for (j, m), value in expanded.items():
        profiles[m][j] = value
    constant = profiles[()]
    assert set(constant) == {0, 2} and constant[2] == 1
    fixedmax = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    for p in profiles.values():
        if 1 in p:
            assert abs(p[1]) <= 2 and abs(p.get(0, 0)) <= 1
        elif 2 in p:
            assert p == constant
        else:
            assert p[0] != 0
    assert constant[0] >= 2
    coordinates = [dict(id=j+1, name=name) for j, name in enumerate(names)]
    system = dict(format='integer-quadratic-family-abc76-v44', variables=76,
                  inputCoordinate=1, fixedParameter=parent['fixedParameter'],
                  coordinates=coordinates, residuals=rows,
                  parentQuadraticSha256=source_hash,
                  deletedCoordinates=sorted(deleted))
    polynomial = dict(format='integer-quartic-family-abc76-v44', variables=76,
                      degree=4, inputCoordinate=1, fixedParameter=parent['fixedParameter'],
                      coordinates=coordinates, terms=serialize(expanded))
    report = dict(schema='abc76-exact-construction/v44', variables=76,
                  quadraticRows=66, degree=4, integerContentForEveryPositiveB=1,
                  ordinaryMonomialsForEveryPositiveB=len(profiles),
                  parameterSeparatedTerms=len(expanded),
                  constantCoefficient=str(constant[0]),
                  largestFixedCoefficient=str(fixedmax),
                  exactHeight=f'max({fixedmax},B^2+{constant[0]})',
                  sourceQuadraticSha256=source_hash,
                  changedRows=sorted(changes), removedRows=sorted(deleted),
                  inputMap='beta=X^2+3', comparisonArguments=['lambda', 'lambda+B+X^8+T^2'],
                  poleMap='b_old=b_scaled/w^2; p_old=w*p; u_old=u/w; v_old=v/w; q_old=q',
                  contactZeroScope='Contact arguments are permitted bounded-height strata; no division by w there.',
                  definingThreshold='Ineffective sufficiently large fixed odd B; B=81 is only an algebraic fixture.',
                  arithmeticScope='Ordinary rational abc and the retained elliptic group, fixed-data prime patterns, all-point trace theorem and prepared simultaneous congruent-twist realization.',
                  scope='Exact finite coefficient specification. The infinite arithmetic proof and its inputs are not certified by these tables alone.')
    output.mkdir(parents=True, exist_ok=True)
    for name, data in [('quadratic-family.json', system), ('polynomial-family.json', polynomial),
                       ('construction-report.json', report)]:
        (output/name).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE)
    build(parser.parse_args().output)
