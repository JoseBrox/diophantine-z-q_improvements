#!/usr/bin/env python3
"""Independently reconstruct the 273-coordinate quartic from its pinned source.

This standard-library checker imports no producer.  Contact coefficients are
recovered by finite differences; the simultaneous evaluation circuit is
recovered by descending coefficient equations rather than Euclidean division.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb, factorial, gcd, lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE
PIN = '9bf3b6e40af70d2a9313f3c211f07941fd6ef93068106d7332bafa73f0dd9069'


def linear(*pairs):
    result = defaultdict(F)
    for poly, factor in pairs:
        for monomial, value in poly.items():
            result[monomial] += value * factor
    return {m: c for m, c in result.items() if c}


def product(a, b):
    result = defaultdict(F)
    for m, c in a.items():
        for n, d in b.items():
            result[tuple(sorted(m + n))] += c * d
    return {m: c for m, c in result.items() if c}


def variable(i):
    return {(i,): F(1)}


ONE = {(): F(1)}


def field_product(a, b):
    return (linear((product(a[0], b[0]), 1), (product(a[1], b[1]), 2)),
            linear((product(a[0], b[1]), 1), (product(a[1], b[0]), 1)))


def normalize(p):
    denominator = lcm(*(F(c).denominator for c in p.values()))
    integers = {m: int(c * denominator) for m, c in p.items()}
    divisor = gcd(*integers.values())
    # Producer orders first by parameter power, then by coordinate monomial.
    first = min(integers, key=lambda m: (m.count(-1), tuple(i for i in m if i != -1)))
    if integers[first] < 0:
        divisor = -divisor
    return {m: c // divisor for m, c in integers.items()}


def decode(row, ids):
    return {tuple(sorted((-1,) * t['parameterPower'] + tuple(ids[i] for i in t['monomial']))):
            int(t['coefficient']) for t in row['terms']}


def univariate_add(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, c in enumerate(a): out[i] += c
    for i, c in enumerate(b): out[i] += c
    return out


def univariate_product(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, c in enumerate(a):
        for j, d in enumerate(b): out[i + j] += c * d
    return out


def verify(source_root=DEFAULT_SOURCE, output_root=HERE):
    raw = (source_root / 'family279/quadratic-family279.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    source_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    folder = output_root / 'family273'
    system_path = folder / 'quadratic-family273.json'
    poly_path = folder / 'polynomial-family273.json'
    system = json.loads(system_path.read_text())
    polynomial = json.loads(poly_path.read_text())
    report = json.loads((folder / 'construction-report273.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    roots = [theta + 3*j for j in range(4)
             for theta in [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]]
    differences = []
    for x in range(21):
        y = F(1)
        for root in roots: y *= x - root
        differences.append(y)
    contact = [F(0)]
    falling_factorial = [F(1)]
    for degree in range(21):
        contact = univariate_add(contact, [differences[0]*c/factorial(degree)
                                           for c in falling_factorial])
        differences = [differences[i+1]-differences[i]
                       for i in range(len(differences)-1)]
        falling_factorial = univariate_product(falling_factorial, [-degree, F(1)])
    assert contact[-1] == 1 and len(set(roots)) == 20
    assert all(sum(c*r**i for i, c in enumerate(contact)) == 0 for r in roots)
    V = [F(comb(10, i)*(-1)**(10-i)) for i in range(11)]
    # Solve F - V^2 = V*B + R, deg B<=9, deg R<=9, by the top ten coefficients.
    remaining = univariate_add(contact, [-c for c in univariate_product(V, V)])
    B = [F(0)]*10
    for k in range(9, -1, -1):
        B[k] = remaining[10+k]
        for j, c in enumerate(V): remaining[k+j] -= B[k]*c
    assert all(c == 0 for c in remaining[10:])
    R = remaining[:10]
    a = B[9]
    assert a != 0
    U = [c/a for c in B]
    low = univariate_add(V, [F(0)] + [-c for c in U])[:10]
    assert U[-1] == 1
    assert univariate_add(univariate_product(V, V),
                          univariate_add(univariate_product(B, V), R)) == contact
    assert univariate_add([F(0)] + U, low) == V
    saved = report['contactCircuit']
    for name, values in [('contactCoefficients', contact), ('U9Coefficients', U),
                         ('V10Coefficients', V), ('R9Coefficients', R),
                         ('VMinus_tUCoefficients', low)]:
        assert saved[name] == [str(x) for x in values]
    assert saved['leadingQuotientCoefficient'] == str(a)

    deleted = {850, 851, 21006, 21007, 20003, 20023}
    changes = {}
    for detector in range(2):
        t, t2, t3, ff = (37, 346, 347, 348) if detector == 0 else (391, 392, 393, 394)
        t6, uu, vv = [20000 + 20*detector + j for j in range(3)]
        basis = {0: ONE, 1: variable(t), 2: variable(t2), 3: variable(t3), 6: variable(t6)}

        def represent(coefficients):
            result = {}
            for k, coefficient in enumerate(coefficients):
                if not coefficient: continue
                if k in basis: value = basis[k]
                else:
                    left, right = min((i, j) for i in basis for j in basis if i <= j and i+j == k)
                    value = product(basis[left], basis[right])
                result = linear((result, 1), (value, coefficient))
            return result

        pref = f'detector{detector}.'
        apref = f'amplified.det{detector}.'
        cpref = f'compressed.det{detector}.'
        changes[pref+'Fmiddle.definition'] = (cpref+'tPower3.definition', linear((product(variable(t), variable(t2)), 1), (variable(t3), -1)))
        changes[apref+'tPower5.definition'] = (cpref+'tPower6.definition', linear((product(variable(t3), variable(t3)), 1), (variable(t6), -1)))
        changes[apref+'tPower8.definition'] = (cpref+'quotient9.definition', linear((represent(U), 1), (variable(uu), -1)))
        changes[apref+'tPower9.definition'] = (cpref+'deltaPower10.definition', linear((product(variable(t), variable(uu)), 1), (represent(low), 1), (variable(vv), -1)))
        changes[pref+'F.definition'] = (cpref+'contactPolynomial.definition', linear((product(variable(vv), variable(vv)), 1), (product(variable(uu), variable(vv)), a), (represent(R), 1), (variable(ff), -1)))
        if detector == 0:
            changes[pref+'eWeight.definition'] = (pref+'eWeight.definition', linear((product(variable(ff), variable(350)), 1), (product(variable(vv), variable(vv)), -1)))

    squares = {}
    for i, sid in enumerate([255, 257, 259, 261], 1):
        squares['U'+str(i)] = (variable(sid), linear((variable(sid+1), 2)))
    for name, sid in [('H', 311), ('C1', 305), ('C2', 313), ('C3', 315), ('C4', 317)]:
        squares[name] = (variable(sid), linear((variable(sid+1), 2)))
    squares['I'] = (linear((variable(307), 1), (variable(232), -6), (variable(248), 306), (ONE, 15015)), linear((variable(308), 2), (variable(233), -6)))
    squares['F'] = (linear((variable(319), 1), (variable(253), -2), (ONE, 1)), linear((variable(320), 4), (variable(254), -4)))
    squares['V1'] = (variable(190), linear((variable(191), -2)))
    powers = {(name, 2): value for name, value in squares.items()}
    powers['C1', 4] = (variable(21000), variable(21001))
    for name, oldname, sid in [('I', 'U3', 21002), ('V1', 'U4', 21004)]:
        value = field_product(squares[name], squares[name])
        for component in range(2):
            changes[f'amplified.{oldname}.power4.{component}.definition'] = (f'residue.{name}.power4.{component}.definition', linear((value[component], 1), (variable(sid+component), -1)))
        powers[name, 4] = (variable(sid), variable(sid+1))
    # Conjugate w^2/D^2, reconstructed by division in Q(sqrt(2)).
    D2 = (F(193), F(-132))
    norm = D2[0]**2 - 2*D2[1]**2
    assert norm == 2401
    for name, sid in [('V0', 180), ('V2', 198), ('V3', 210), ('V4', 222)]:
        w_squared = (linear((variable(sid), 193)), linear((variable(sid+1), -132)))
        value = field_product(w_squared, ({(): D2[0]/norm}, {(): -D2[1]/norm}))
        powers[name, 4] = (value[0], linear((value[1], -1)))
    groups = [[('C2', 2, 23), ('H', 2, 10), ('V1', 4, 4)],
              [('F', 2, 23), ('U3', 2, 2), ('V0', 4, 4)],
              [('I', 4, 23), ('U2', 2, 1), ('U4', 2, 2), ('V3', 4, 4)],
              [('C3', 2, 23), ('C1', 4, 10), ('V4', 4, 4)],
              [('C4', 2, 23), ('U1', 2, 2), ('V2', 4, 4)]]
    for detector in range(2):
        off = 48*detector
        weights = {1: 352+off, 2: 361+off, 4: 362+off, 10: 369+off, 23: 360+off}
        start = 22000 + 30*detector
        for g, group in enumerate(groups):
            for component in range(2):
                value = ONE if component == 0 else {}
                for name, power, exponent in group:
                    value = linear((value, 1), (product(variable(weights[exponent]), powers[name, power][component]), 1))
                value = linear((value, 1), (variable(start+2*g+component), -1))
                changes[f'amplified.det{detector}.factor{g}.{component}.definition'] = (f'residue.det{detector}.factor{g}.{component}.definition', value)
    expected = {}
    for row in source['residuals']:
        if row['sourceId'] in deleted: continue
        name, value = changes.pop(row['name']) if row['name'] in changes else (row['name'], decode(row, source_ids))
        assert not any(i in deleted for m in value for i in m)
        expected[row['sourceId']] = (name, normalize(value))
    assert not changes
    actual = {row['sourceId']: (row['name'], decode(row, ids)) for row in system['residuals']}
    assert actual == expected and len(actual) == 247
    assert set(source_ids.values()) - set(ids.values()) == deleted
    assert not (set(ids.values()) - set(source_ids.values()))
    assert system['coordinates'] == polynomial['coordinates']
    assert system['variables'] == polynomial['variables'] == len(ids) == 273
    assert sorted(ids) == list(range(1, 274)) and ids[1] == 0
    assert {i for name, p in actual.values() for m in p for i in m if i != -1} == set(ids.values())
    assert all(max(sum(i != -1 for i in m) for m in p) <= 2 for name, p in actual.values())
    expanded = defaultdict(int)
    for name, p in actual.values():
        for m, n in combinations_with_replacement(p, 2):
            expanded[tuple(sorted(m+n))] += p[m]*p[n]*(1 if m == n else 2)
    expanded = {m: c for m, c in expanded.items() if c}
    assert expanded == decode({'terms': polynomial['terms']}, ids)
    assert gcd(*expanded.values()) == 1 and max(sum(i != -1 for i in m) for m in expanded) == 4
    ordinary = defaultdict(dict)
    for m, c in expanded.items(): ordinary[tuple(i for i in m if i != -1)][m.count(-1)] = c
    assert ordinary[(489, 489)] == {0: 1, 2: 1}
    assert all(set(c) in ({0}, {1}) for m, c in ordinary.items() if m != (489, 489))
    constant = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    multiplier = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert constant.bit_length() == 1520 and multiplier == 13118436242
    assert constant > multiplier**2 and 80989**90+1 < constant < 80989**94+1

    # These complete residue classes prove no valuation cancellation for all
    # integer valuations, not merely for a bounded sample of them.
    residue_certificate = []
    orders = {'H': 6, 'C1': 3, 'I': 6, 'C2': 12, 'C3': 12, 'C4': 12, 'F': 12}
    complete_depths = {'H': 6, 'C1': 4, 'I': 12, 'C2': 12, 'C3': 12, 'C4': 12, 'F': 12}
    for nu in [1, 3, 5, 7]:
        for g, group in enumerate(groups):
            seen = {0}
            classes = []
            for name, power, exponent in group:
                even = name == 'H' or name[0] in 'UV'
                residues = {(power*v-exponent*nu) % 8 for v in range(0, 8, 2 if even else 1)}
                assert not seen.intersection(residues)
                seen.update(residues)
                classes.append(sorted(residues))
                lower_bound = F(2*exponent-1, 2*power)
                assert lower_bound > 0
                minimum = lower_bound.numerator // lower_bound.denominator + 1
                if even: minimum += minimum % 2
                assert minimum >= orders.get(name, 1)
                assert power*complete_depths.get(name, 2)-exponent > 0
            residue_certificate.append({'nuMod8': nu, 'factor': g+1, 'nonconstantValuationClassesMod8': classes})
    result = {
        'status': 'PASS', 'variables': 273, 'quadraticResiduals': 247,
        'degree': 4, 'content': 1, 'ordinaryMonomialsForEveryPositiveParameter': len(ordinary),
        'symbolicTerms': len(expanded), 'allRowsIndependentlyReconstructed': True,
        'completeUnorderedPairExpansion': True, 'allCoordinatesUsed': True,
        'sourceQuadraticTableSha256': PIN,
        'contactReconstruction': 'Forward differences of 21 exact evaluations, verified at all 20 distinct roots',
        'contactCircuitReconstruction': 'Descending coefficient equations for F-V^2=V*B+R; exact polynomial identity and six-coordinate quadratic evaluation',
        'contactLeadingQuotientCoefficient': str(a),
        'localOrders': orders, 'inputComparisonAfterCrossTest': 3,
        'completeValuationResidues': residue_certificate,
        'completenessDepths': complete_depths,
        'constantCoefficientMaximum': str(constant), 'constantCoefficientMaximumBits': constant.bit_length(),
        'linearCoefficientMultiplierMaximum': multiplier,
        'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
        'exactHeightThresholdN': 23, 'exactHeightForNAtLeast23': '80989^(4*N+2)+1',
        'noSupportCancellationForPositiveParameter': True,
        'quadraticTableSha256': sha256(system_path.read_bytes()).hexdigest(),
        'polynomialTableSha256': sha256(poly_path.read_bytes()).hexdigest(),
        'arithmeticScope': 'Finite coefficient algebra and complete valuation residue certificates only. No integer-projection theorem is asserted for this coefficient source; the independently normalized defining construction is family267.'}
    (folder / 'independent-verification273.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in ['status', 'variables', 'quadraticResiduals',
                     'ordinaryMonomialsForEveryPositiveParameter', 'symbolicTerms',
                     'quadraticTableSha256', 'polynomialTableSha256']}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
