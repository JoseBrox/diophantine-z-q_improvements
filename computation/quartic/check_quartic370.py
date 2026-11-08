#!/usr/bin/env python3
"""Independent row, scale, coefficient and finite arithmetic certificates."""
from collections import defaultdict
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent


def plus(left, right):
    result = defaultdict(Fraction, left)
    for key, value in right.items():
        result[key] += value
    return {key: value for key, value in result.items() if value}


def times(left, right):
    result = defaultdict(Fraction)
    for (a, m), c in left.items():
        for (b, n), d in right.items():
            result[a + b, tuple(sorted(m + n))] += c * d
    return {key: value for key, value in result.items() if value}


def parse(terms):
    result = {}
    for term in terms:
        key = term['parameterPower'], tuple(term['monomial'])
        assert key not in result
        result[key] = Fraction(term['coefficient'])
    return result


def substitute(poly, images):
    result = {}
    for (a, m), c in poly.items():
        term = {(a, ()): c}
        for j in m:
            term = times(term, images[j])
        result = plus(result, term)
    return result


def atom(index, scalar=1):
    return {(0, (index,)): Fraction(scalar)}


def same_up_to_nonzero_scalar(left, right):
    assert set(left) == set(right)
    key = next(iter(right))
    factor = left[key] / right[key]
    assert factor and left == {key: value * factor for key, value in right.items()}
    return factor


def main():
    raw = gzip.decompress((HERE / 'baseline389/quadratic-system389.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest() == 'f7fb5bdf6a3d47275f1d78ed5e275954e2cc1f21fec8204d6a395bfc2f8b5394'
    old = json.loads(raw)
    ir = json.loads((HERE / 'family370/quadratic-family370.json').read_text())
    table = json.loads((HERE / 'family370/polynomial-family370.json').read_text())
    old_source = {coord['sourceId']: coord['id'] for coord in old['coordinates']}
    new_source = {coord['sourceId']: coord['id'] for coord in ir['coordinates']}
    deleted = set(range(337, 343)) | {345} | {66, 67, 68, 70, 71, 72, 74, 75, 76, 78, 79, 80}
    assert set(new_source) == set(old_source) - deleted
    assert len(new_source) == ir['variables'] == table['variables'] == 370
    assert [coord['id'] for coord in ir['coordinates']] == list(range(1, 371))
    assert ir['coordinates'] == table['coordinates']
    old_rows = {row['sourceId']: row for row in old['residuals']}
    new_rows = {row['sourceId']: row for row in ir['residuals']}
    assert set(new_rows) == set(old_rows) - set(range(289, 295)) - {297} - set(range(687, 699))
    assert len(new_rows) == 342
    old_deleted = {old_source[sid] for sid in deleted}
    using_deleted = {row['sourceId'] for row in old['residuals']
                     if any(j in old_deleted for term in row['terms'] for j in term['monomial'])}
    assert using_deleted == set(range(289, 298)) | {395, 399, 400, 401, 402} | set(range(687, 699))

    # Recover every unchanged equation by the inverse input transformation.
    inverse = {new_source[sid]: atom(old_source[sid]) for sid in new_source}
    ox = old_source[0]
    oy = old_source[248]
    inverse[new_source[0]] = plus(atom(ox, 2), {(0, ()): Fraction(1)})
    inverse[new_source[248]] = plus(plus(atom(oy, 4), atom(ox, 4)), {(0, ()): Fraction(1)})
    old_names = {coord['name']: coord['id'] for coord in old['coordinates']}
    old_rows_by_name = {row['name']: row for row in old['residuals']}
    reverse_third = dict(inverse)
    third_coordinates = set()
    for coord in ir['coordinates']:
        name = coord['name']
        if name.startswith('detector2.'):
            original = 'detector1.' + name[len('detector2.'):]
        elif name.startswith('hybrid.det2.'):
            original = 'hybrid.det1.' + name[len('hybrid.det2.'):]
        else:
            continue
        reverse_third[coord['id']] = atom(old_names[original])
        third_coordinates.add(coord['id'])
    assert len(third_coordinates) == 52
    reverse_third[new_source[344]] = atom(old_source[343])
    third_rows = {sid for sid, row in new_rows.items()
                  if row['name'].startswith(('detector2.', 'hybrid.det2.'))}
    assert len(third_rows) == 50
    assert {sid for sid, row in new_rows.items()
            if any(j in third_coordinates for term in row['terms'] for j in term['monomial'])} == third_rows
    multipliers = {}
    for sid, row in new_rows.items():
        if sid in {295, 296}:
            continue
        if sid in third_rows:
            template_name = row['name'].replace('detector2.', 'detector1.', 1).replace('hybrid.det2.', 'hybrid.det1.', 1)
            actual = substitute(parse(row['terms']), reverse_third)
            expected = parse(old_rows_by_name[template_name]['terms'])
        else:
            actual = substitute(parse(row['terms']), inverse)
            expected = parse(old_rows[sid]['terms'])
        if sid == 492:
            keys = [key for key, value in expected.items() if value == 4896]
            assert len(keys) == 1
            expected[keys[0]] = Fraction(9792)
        multipliers[sid] = str(same_up_to_nonzero_scalar(actual, expected))

    # Check the original root-chart normalizations directly, not from names.
    for block, real_sid, imag_sid, real_scale, h0_sid, h1_sid in [
            ('A', 82, 83, 1, 1, 2), ('S', 84, 85, 1, 5, 6),
            ('T', 86, 87, 2, 9, 10), ('Z', 88, 89, 1, 13, 14)]:
        real_row = next(row for row in old['residuals'] if row['name'] == block + '.chart.x.0.definition')
        imag_row = next(row for row in old['residuals'] if row['name'] == block + '.chart.x.1.definition')
        real_expected = plus(plus(times(atom(old_source[h0_sid]), atom(old_source[h0_sid])),
                                  times(atom(old_source[h1_sid], 2), atom(old_source[h1_sid]))),
                             atom(old_source[real_sid], -real_scale))
        imag_expected = plus(times(atom(old_source[h0_sid]), atom(old_source[h1_sid])),
                             atom(old_source[imag_sid], -1))
        same_up_to_nonzero_scalar(parse(real_row['terms']), real_expected)
        same_up_to_nonzero_scalar(parse(imag_row['terms']), imag_expected)
    s0 = {}
    s1 = {}
    for sid, factor in [(82, 1), (84, 1), (86, 2), (88, 1)]:
        s0 = plus(s0, atom(new_source[sid], factor))
    for sid in [83, 85, 87, 89]:
        s1 = plus(s1, atom(new_source[sid], 2))
    expected_real = plus(times(s0, s0), atom(new_source[343], -4))
    expected_imag = plus(times(plus(s0, s1), plus(s0, s1)), atom(new_source[344], -4))
    same_up_to_nonzero_scalar(parse(new_rows[295]['terms']), expected_real)
    same_up_to_nonzero_scalar(parse(new_rows[296]['terms']), expected_imag)
    # Every downstream row is recovered above. Hence the source-certified
    # scales become 1,S0^2,(S0+S1)^2 exactly.

    # Independently expand the full rational normalization of every detector.
    # The symbolic inputs below are free indeterminates, not sample points.
    def scale(poly, scalar):
        return {key: value*scalar for key, value in poly.items() if value*scalar}
    def power(poly, exponent):
        value = {(0, ()): Fraction(1)}
        for _ in range(exponent):
            value = times(value, poly)
        return value
    def define(sid, env):
        polynomial = parse(new_rows[sid]['terms'])
        unknown = {j for a, m in polynomial for j in m if j not in env}
        assert len(unknown) == 1, (sid, unknown)
        j = unknown.pop()
        coefficient = Fraction(0)
        rest = {}
        for (a, m), value in polynomial.items():
            if j in m:
                assert (a, m) == (0, (j,))
                coefficient += value
            else:
                rest = plus(rest, substitute({(a, m): value}, env))
        assert coefficient
        env[j] = scale(rest, -1/coefficient)
        assert substitute(polynomial, env) == {}
    lam, u, v, e, q, pole_b, norm_t = [atom(j) for j in range(1001, 1008)]
    one = {(0, ()): Fraction(1)}
    base = {new_source[37]: lam, new_source[343]: power(u, 2), new_source[344]: power(v, 2)}
    theta = [Fraction(0), Fraction(-1, 2), Fraction(-1), Fraction(1, 2399), Fraction(-32, 407)]
    normalized = []
    for detector, definitions in enumerate([range(298, 301), range(345, 352), range(395, 402)]):
        env = dict(base)
        for sid in definitions:
            define(sid, env)
        env[new_source[[350, 398, 446][detector]]] = e
        env[new_source[[352, 400, 448][detector]]] = q
        env[new_source[[385, 433, 481][detector]]] = pole_b
        env[new_source[[383, 431, 479][detector]]] = norm_t
        a = [one, scale(power(u, 2), 4), scale(power(v, 2), 4)][detector]
        actual_t = times(a, lam)
        delta = plus(actual_t, scale(one, -1))
        represented = (env[new_source[37]] if detector == 0 else
                       scale(env[new_source[[37, 391, 439][detector]]], 4))
        assert represented == actual_t
        contact = one
        for root in theta:
            contact = times(contact, plus(actual_t, scale(one, -root)))
        expected = plus(times(contact, e), scale(power(times(a, delta), 5), -1))
        multiplier = same_up_to_nonzero_scalar(
            substitute(parse(new_rows[302+50*detector]['terms']), env), expected)
        assert multiplier == [Fraction(1952786), Fraction(976393, 8), Fraction(976393, 8)][detector]
        same_up_to_nonzero_scalar(substitute(parse(new_rows[304+50*detector]['terms']), env),
                                 plus(times(power(delta, 3), q), scale(e, -1)))
        define(336+50*detector, env)
        same_up_to_nonzero_scalar(substitute(parse(new_rows[337+50*detector]['terms']), env),
                                 plus(times(times(e, delta), pole_b), scale(power(norm_t, 2), -1)))
        normalized.append({'detector': detector, 'weightRowMultiplier': str(multiplier),
                           'FeEqualsAdeltaPower5': True, 'deltaCubedQ1EqualsE': True,
                           'eDeltaBEqualsT2': True})

    # Compute the polynomial by triangular convolution, independently of the
    # producer's ordered-pair expansion, and check every integer coefficient.
    total = defaultdict(Fraction)
    for row in ir['residuals']:
        entries = list(parse(row['terms']).items())
        assert max(len(m) for (a, m), c in entries) <= 2
        for i, ((a, m), c) in enumerate(entries):
            for j in range(i, len(entries)):
                (b, n), d = entries[j]
                total[a + b, tuple(sorted(m + n))] += (1 if i == j else 2) * c * d
    total = {key: value for key, value in total.items() if value}
    assert total == parse(table['terms'])
    assert all(value.denominator == 1 for value in total.values())
    assert max(len(m) for a, m in total) == 4
    assert max(a for a, m in total) == 2
    assert {j for a, m in total for j in m} == set(range(1, 371))
    ordinary = defaultdict(dict)
    for (a, m), value in total.items():
        ordinary[m][a] = int(value)
    assert len(total) == 5852 and len(ordinary) == 5837
    unit = next(m for m, coeffs in ordinary.items() if coeffs == {0: 1})
    majorant = max(sum(abs(c) for c in coeffs.values()) for coeffs in ordinary.values())
    assert majorant.bit_length() == 1520
    # A simple coefficient root bound guarantees the support after A=80989^54929.
    explicit_parameter = 80989**54929
    assert explicit_parameter > majorant + 1
    parameter_powers = [1, explicit_parameter, explicit_parameter**2]
    evaluated = {m: sum(c*parameter_powers[a] for a, c in coefficients.items())
                 for m, coefficients in ordinary.items()}
    assert all(evaluated.values())
    assert max(abs(c).bit_length() for c in evaluated.values()) == 1791357
    assert gcd(*evaluated.values()) == 1

    # The affine input and scalar-shift finite checks are repeated literally.
    nx = new_source[0]
    ny = new_source[248]
    assert parse(new_rows[200]['terms']) == {(0, (nx, nx)): 1, (0, (ny,)): -1}
    def r(x):
        beta = 51*x*x + 2504
        return beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1)
    def valuation(n, p):
        result = 0
        while n % p == 0:
            n //= p
            result += 1
        return result
    for x in range(16):
        assert valuation(r(x), 2) == (3 if x % 4 == 0 else 2)
    for x in range(9):
        assert valuation(r(x), 3) == 1
    for x in range(17):
        assert r(x) % 17 == 15
    ell = 80989
    assert all(ell % p for p in range(2, isqrt(ell) + 1))
    for theta in [Fraction(0), Fraction(1), Fraction(2401), Fraction(-343, 32), Fraction(1, 2)]:
        q = (theta - 2504)/51
        residue = q.numerator * pow(q.denominator, -1, ell) % ell
        assert pow(residue, (ell-1)//2, ell) == ell-1
    assert 9792 == 2**6 * 3**2 * 17

    # Integer-only numerical inequalities used by the proposed height proof.
    n = 27464
    anchor = (187*(2*n-1))//8 + 1
    assert anchor == 1283919
    assert ell**4096 > 2**66787
    margin = 66787*anchor - 4096*20934550
    assert margin == 1181453 > 0
    assert 14**19 < 4**40
    result = {
        'status': 'passed', 'variables': 370, 'quadraticResiduals': 342, 'degree': 4,
        'symbolicTerms': 5852, 'ordinaryMonomialsForNAtLeast27464': 5837,
        'contentForEveryIntegerParameter': 1, 'unitCoefficientMonomial': list(unit),
        'heightBound': 'H(P_N)<2^1520*80989^(4*N+2)',
        'explicitMember': {'N': 27464, 'parameterExponent': 54929,
                           'ordinaryMonomials': len(evaluated),
                           'largestCoefficientBinaryDigits': 1791357},
        'unchangedRowsRecoveredByInverseAffineMap': True,
        'thirdDetectorRowsRecoveredAsIndependentFirstDetector': len(third_rows),
        'thirdDetectorCoordinatesAndSoleUsesChecked': len(third_coordinates),
        'fullDetectorNormalizations': normalized,
        'rootAbscissaNormalizationsChecked': True, 'threeSemanticScalesChecked': True,
        'deletedCoordinateSoleUsesChecked': True, 'smallPrimeArithmeticChecked': True,
        'scalarSeparationCertificate': {'N': n, 'L': anchor, 'binaryExponent': 20934550, 'margin': margin},
        'inverseRowMultipliers': multipliers,
        'systemSHA256': hashlib.sha256((HERE/'family370/quadratic-family370.json').read_bytes()).hexdigest(),
        'polynomialSHA256': hashlib.sha256((HERE/'family370/polynomial-family370.json').read_bytes()).hexdigest(),
        'scope': 'Exact algebraic identities and finite arithmetic. The defining property follows from the paper and its stated arithmetic premises; this checker does not prove those premises.',
    }
    (HERE/'family370/independent-verification370.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'inverseRowMultipliers'}, indent=2))


if __name__ == '__main__':
    main()
