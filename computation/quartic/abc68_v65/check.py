#!/usr/bin/env python3
"""Producer-free exact audit of the 68-coordinate quartic specification.

All literal equations are reconstructed below from the complete 68-coordinate
source and the three-coordinate unit reference. No producer, old residual table,
computer-algebra package, or lattice-reduction implementation is imported.
Only the proposed invertible reference matrix is read from the report.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from collections import defaultdict
from math import gcd, lcm
from hashlib import sha256
import argparse
import json


@dataclass(frozen=True)
class K:
    re: Q = Q(0)
    im: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, 're', Q(self.re))
        object.__setattr__(self, 'im', Q(self.im))

    @staticmethod
    def co(value):
        if isinstance(value, K):
            return value
        if isinstance(value, (int, Q)):
            return K(value)
        return None

    def __add__(self, other):
        other = K.co(other)
        if other is None:
            return NotImplemented
        return K(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.re, -self.im)

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = K.co(other)
        if other is None:
            return NotImplemented
        return K(self.re * other.re + 2 * self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def inverse(self):
        n = self.norm()
        assert n
        return K(self.re / n, -self.im / n)

    def __truediv__(self, other):
        return self * K.co(other).inverse()

    def __rtruediv__(self, other):
        return K.co(other) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        result = K(1)
        for _ in range(n):
            result *= self
        return result

    def conjugate(self):
        return K(self.re, -self.im)

    def norm(self):
        return self.re ** 2 - 2 * self.im ** 2


class P:
    """Sparse polynomials in indexed variables with exact K coefficients."""
    def __init__(self, value=0):
        if isinstance(value, P):
            self.d = value.d.copy()
        elif isinstance(value, dict):
            self.d = {m: K.co(c) for m, c in value.items() if K.co(c) != K(0)}
        else:
            c = K.co(value)
            assert c is not None
            self.d = {} if c == K(0) else {(): c}

    def __add__(self, other):
        result = self.d.copy()
        for m, c in P(other).d.items():
            result[m] = result.get(m, K(0)) + c
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.d.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        result = {}
        for m, c in self.d.items():
            for n, d in P(other).d.items():
                mn = tuple(sorted(m + n))
                result[mn] = result.get(mn, K(0)) + c * d
        return P(result)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert n >= 0
        result = P(1)
        for _ in range(n):
            result *= self
        return result

    def conjugate(self):
        return P({m: c.conjugate() for m, c in self.d.items()})

    def components(self):
        return [{m: getattr(c, part) for m, c in self.d.items()
                 if getattr(c, part)} for part in ('re', 'im')]


def variable(i):
    return P({(i,): 1})


def clean(d):
    return {m: c for m, c in d.items() if c}


def separate_parameter(d):
    return {(m.count(0), tuple(i for i in m if i)): c for m, c in d.items()}


def primitive(d):
    d = clean(d)
    assert d
    den = lcm(*(Q(c).denominator for c in d.values()))
    integers = {m: int(Q(c) * den) for m, c in d.items()}
    content = gcd(*integers.values())
    sign = 1 if integers[min(integers)] > 0 else -1
    return ({m: sign * c // content for m, c in integers.items()},
            Q(sign * content, den))


def combine(rows, scalars):
    result = defaultdict(Q)
    for row, c in zip(rows, scalars):
        for m, d in row.items():
            result[m] += c * d
    return clean(result)


def decode(row):
    result = {(int(t['parameterPower']), tuple(t['monomial'])):
              int(t['coefficient']) for t in row['terms']}
    assert len(result) == len(row['terms']) and all(result.values())
    return result


def inverse(matrix):
    n = len(matrix)
    a = [[Q(x) for x in row] + [Q(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    determinant = Q(1)
    for j in range(n):
        i = next(i for i in range(j, n) if a[i][j])
        if i != j:
            a[i], a[j] = a[j], a[i]
            determinant = -determinant
        pivot = a[j][j]
        determinant *= pivot
        a[j] = [x / pivot for x in a[j]]
        for i in range(n):
            if i != j:
                c = a[i][j]
                a[i] = [x - c * y for x, y in zip(a[i], a[j])]
    return determinant, [row[n:] for row in a]


HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tables', type=Path, default=HERE)
parser.add_argument('--output', type=Path, default=HERE / 'independent-verification.json')
args = parser.parse_args()
quad_bytes = (args.tables / 'quadratic-family.json').read_bytes()
poly_bytes = (args.tables / 'polynomial-family.json').read_bytes()
quad = json.loads(quad_bytes)
expanded = json.loads(poly_bytes)
report = json.loads((args.tables / 'construction-report.json').read_text())
basis = json.loads((args.tables / 'basis-transformation.json').read_text())
for key in ['referenceMatrix', 'constantPivot', 'constantOperations']:
    assert basis[key] == report[key]
assert quad['variables'] == expanded['variables'] == 68
assert quad['inputCoordinate'] == 1

# Coordinate census is reconstructed from the specified source, independently
# of the table's coordinate descriptions.
coordinate_names = ['input', 'slope']
for stem in ['reference.u', 'reference.w', 'reference.v']:
    coordinate_names += [stem + '.0', stem + '.1']
coordinate_names += ['pair.a.0']
for stem in ['pair.S', 'pair.T', 'numerator.f', 'numerator.g',
             'pair.h', 'pair.d', 'product.first', 'product.second',
             'comparison.firstSquare', 'comparison.secondSquare']:
    coordinate_names += [stem + '.0', stem + '.1']
coordinate_names += ['height.betaSquare', 'height.betaFourth', 'detector1.argument']
for j in range(2):
    prefix = f'detector{j}.'
    block = ['contactSquareShift', 'contactSumShift', 'inverseWeight',
             'factor1.0', 'factor1.1', 'factor2.0', 'factor2.1',
             'product.0', 'product.1', 'trace', 'poleInput', 'pole.e',
             'pole.u', 'pole.p', 'pole.v', 'pole.q', 'pole.pSquare', 'pole.qSquare']
    coordinate_names += [prefix + name for name in block]
assert len(coordinate_names) == 68
assert quad['coordinates'] == [{'id': i, 'name': name}
                               for i, name in enumerate(coordinate_names, 1)]
rho = K(0, 1)
D, a0, b0 = 11 - 6 * rho, 1 + rho, 2 * rho
AP, BP = a0 ** 2 + D, a0 ** 2 - D
c0 = 4 - 2 * rho
delta0 = a0 - c0 ** 2
assert delta0 == K(-23, 17) and a0 * delta0 == D
C = D ** 2 + 6 * a0 ** 2 * D - 3 * a0 ** 4
assert b0 ** 2 == a0 ** 3 - D * a0
assert C == K(196, -144) and C.norm() == -3056
assert a0.norm() * b0.norm() * D.norm() != 0


def field(i):
    return variable(i) + rho * variable(i + 1)


X, lam, B = variable(1), variable(2), variable(0)
uH, wH, vH = [field(i) for i in (3, 5, 7)]
S, TH = vH - c0 - a0 * uH, a0 * wH - vH + c0
a_real = variable(9)
s, t, F, G, h, d = [field(i) for i in (10, 12, 14, 16, 18, 20)]
J, KK, C2, I2 = [field(i) for i in (22, 24, 26, 28)]
b2, b4, t1 = [variable(i) for i in (30, 31, 32)]

# The complete three-coordinate unit reference. Its three coordinates are
# units: a0*uH*wH=1, and vH times the other displayed factor is delta0!=0.
reference_literal = [a0 * uH * wH - 1,
                     vH * (vH - a0 * (uH + wH) - 2 * c0) - delta0]
reference_raw = []
for expression in reference_literal:
    reference_raw += [primitive(separate_parameter(d))[0]
                      for d in expression.components()]
assert len(reference_raw) == 4
U = [[1, 1, 0, 0], [-1, -2, 0, 0], [3, 4, -1, 1], [-7, -9, 0, 1]]
assert U == report['referenceMatrix']
assert len(U) == 4 and all(len(row) == 4 for row in U)
determinant, Uinv = inverse(U)
assert determinant in (1, -1)
assert all(x.denominator == 1 for row in Uinv for x in row)
pre, names, reference_scales = [], [], []
for i, vector in enumerate(U, 1):
    row, scale = primitive(combine(reference_raw, vector))
    pre.append(row)
    reference_scales.append(scale)
    names.append(f'reference.primitive.{i}')
for i, row in enumerate(reference_raw):
    assert combine(pre, [Uinv[i][j] * reference_scales[j]
                         for j in range(4)]) == row


def add(name, expression, field_valued=False):
    components = expression.components()
    if field_valued:
        assert all(components)
        for j, component in enumerate(components):
            pre.append(primitive(separate_parameter(component))[0])
            names.append(name + '.' + str(j))
    else:
        assert not components[1]
        pre.append(primitive(separate_parameter(components[0]))[0])
        names.append(name)


# Four literal field quadrics and the one rational half-trace output.
# The entire difference abscissa a=h(h+s+t) is derived. Only Re(a) is stored.
p = h+s+t
a = h*p
add('pair.differenceReal', a_real-P(a.components()[0]))
pair_rows = [d-p*F, D*(F+G)-(s-t)*h+t**2,
             d-G*h, b4-d*(s-t)+D*F*G]
for name, expression in zip(['firstProduct', 'secant',
                             'secondProduct', 'scale'], pair_rows):
    add('pair.' + name, expression, True)
add('product.first', vH * J - uH * F, True)
add('product.second', vH * KK - wH * G, True)
add('comparison.first', C2 - (s - S) ** 2, True)
add('comparison.second', I2 - (t - TH) ** 2, True)
add('height.betaSquare', b2 - X ** 2)
add('height.betaFourth', b4 - b2 ** 2)
add('detector1.argument', t1 - lam - B - b4 ** 2 - 4 * variable(9) ** 2)
assert len(pre) == 24

# Both native eighteen-rational-coordinate blocks are reconstructed literally.
for j, argument in enumerate([lam, t1]):
    start = 33 + 18 * j
    R, Z, w = [variable(start + k) for k in range(3)]
    A1, A2, Omega = [field(start + k) for k in (3, 5, 7)]
    omega0, omega1 = variable(start + 7), variable(start + 8)
    eta, pole_b, pole_e, pole_u, pole_p, pole_v, pole_q, p2, q2 = [
        variable(start + k) for k in range(9, 18)]
    prefix = f'detector{j}.'
    add(prefix + 'contactSquare', R - argument ** 2 + 2 * argument)
    add(prefix + 'contactSum', R * Z + Z - R ** 2 + 35 * R)
    add(prefix + 'inverseContact', (R + 1) * w - Z ** 2 - 24 * Z)
    add(prefix + 'factor1', w * A1 - w ** 2 - w * C2 - J ** 2, True)
    add(prefix + 'factor2', w * A2 - w ** 2 - w * I2.conjugate()
        - KK.conjugate() ** 2, True)
    add(prefix + 'product', w * Omega - A1 * A2, True)
    add(prefix + 'trace', omega0 ** 2 - 2 * omega0 * eta - 2 * omega1 ** 2)
    add(prefix + 'poleInput', w * pole_b - eta ** 2)
    add(prefix + 'pole.pSquare', p2 - pole_p ** 2)
    add(prefix + 'pole.first', pole_e ** 2 + pole_b * p2 - 1)
    add(prefix + 'pole.factor', pole_u * pole_v - pole_e * (1 - pole_b))
    add(prefix + 'pole.qSquare', q2 - pole_q ** 2)
    add(prefix + 'pole.second', pole_u ** 2 - pole_v ** 2 - pole_b * q2)
assert len(pre) == 56
assert len(set(names)) == 56

# Independent ideal-membership identities for this exact row basis.
q1 = P(0)  # a is now the literal derived quadratic h*p
q2, q3, q4, q5 = pair_rows
RU = b4-D*F**2-s**2*F
RV = b4-D*G**2-t**2*G
assert not (RU-(q5+(s-t)*q2-F*q3)).d
assert not (RV-(q5+(s-t)*q4-G*q3)).d
assert not ((h+t)*(-D*F)+D*d-D*s*F-D*q2).d
assert not ((h+t)*(-D*G)+D*d+D*t*G-D*q4).d
ZZ = variable(100)
line = (h+t)*ZZ+D*d
factorization_residual = ZZ**3-D*b4*ZZ-line**2-(ZZ+D*F)*(ZZ+D*G)*(ZZ-a)
ideal_certificate = ((q1-q3)*ZZ**2
    +D*((F+G)*q1-h*q2-p*q4-q5)*ZZ
    +D**2*(F*G*q1-h*G*q2-d*q4))
assert not (factorization_residual-ideal_certificate).d
assert not ((s+t)*F*(s-t)-(G-F)*(D*(F+G)+t**2)-(RV-RU)).d

# Exact invertible elimination of all fixed constants except the pole pivot.
pivot = int(report['constantPivot']) - 1
assert pivot == 36 and names[pivot] == 'detector0.pole.first'
pivot_row = pre[pivot]
assert pivot_row[(0, ())] == 1
final, operations = [], []
for i, row in enumerate(pre):
    multiple = 0 if i == pivot else row.get((0, ()), 0)
    reduced = row.copy()
    if i != pivot:
        for m, fixed_coefficient in pivot_row.items():
            reduced[m] = reduced.get(m, 0) - multiple * fixed_coefficient
    normalized, scale = primitive(reduced)
    assert scale.denominator == 1
    operations.append({'row': i + 1, 'pivotMultiple': multiple,
                       'content': abs(scale.numerator),
                       'sign': 1 if scale > 0 else -1})
    final.append(normalized)
    reconstructed = {m: scale * fixed_coefficient for m, fixed_coefficient in normalized.items()}
    if i != pivot:
        for m, fixed_coefficient in pivot_row.items():
            reconstructed[m] = reconstructed.get(m, 0) + multiple * fixed_coefficient
    assert clean(reconstructed) == row
assert operations == report['constantOperations']
assert len(quad['residuals']) == 56
for i, (row, name, stored) in enumerate(zip(final, names, quad['residuals']), 1):
    assert stored['id'] == i and stored['name'] == name
    assert decode(stored) == row, name
    assert gcd(*row.values()) == 1
    assert all(0 <= power <= 1 and len(mon) <= 2
               and all(1 <= k <= 68 for k in mon) for power, mon in row)
assert sum(bool(row.get((0, ()), 0)) for row in final) == 1
assert set(k for row in final for power, mon in row for k in mon) == set(range(1, 69))

# Independent sum-of-squares expansion, using unordered pairs of terms.
polynomial = defaultdict(int)
for row in final:
    terms = sorted(row.items())
    for i, ((power, mon), coefficient) in enumerate(terms):
        for k in range(i, len(terms)):
            (power2, mon2), coefficient2 = terms[k]
            polynomial[(power + power2, tuple(sorted(mon + mon2)))] += (
                coefficient * coefficient2 * (1 if i == k else 2))
polynomial = clean(polynomial)
assert polynomial == decode(expanded)
assert expanded['degree'] == max(len(mon) for power, mon in polynomial) == 4
assert polynomial[(0, (1, 1, 1, 1))] == 1
assert gcd(*polynomial.values()) == 1
profiles = defaultdict(dict)
for (power, mon), coefficient in polynomial.items():
    profiles[mon][power] = coefficient
assert len(profiles) == 1078 and len(polynomial) == 1081
assert profiles[()] == {0: 1, 2: 1}
assert profiles[(1, 1, 1, 1)] == {0: 1}
assert set(k for power, mon in polynomial for k in mon) == set(range(1, 69))
fixed = [(mon, abs(values[0])) for mon, values in profiles.items() if set(values) == {0}]
fixed_maximum = max(height for mon, height in fixed)
assert fixed_maximum == 3554
fixed_at = [list(mon) for mon, height in fixed if height == fixed_maximum]
moving = []
for mon, profile in profiles.items():
    if 1 in profile:
        assert set(profile) <= {0, 1}
        assert abs(profile[1]) <= 8 and abs(profile.get(0, 0)) <= 158
        moving.append({'monomial': list(mon), 'coefficientOfB': profile[1],
                       'fixedCoefficient': profile.get(0, 0)})
# For every integer B >= 81, 8B+158 <= B^2+1.  All moving coefficient
# profiles are nonzero there; X^4 remains 1, certifying content 1.
assert 81 ** 2 + 1 >= 8 * 81 + 158
assert 81 ** 2 + 1 > fixed_maximum
for entry in moving:
    assert abs(entry['coefficientOfB']) * 81 > abs(entry['fixedCoefficient'])

# A fully rational zero-input algebraic fixture checks all 56 rows together.
# Its parameter B is not asserted to meet the arithmetic height threshold.
mu = (3 * a0 ** 2 - D) / (2 * b0)
hx = mu ** 2 - 2 * a0
hy = mu * (a0 - hx) - b0
assert hy ** 2 == hx ** 3 - D * hx
refS, refT = hy / hx, b0 / a0
assert refS != refT
cv = -refS * refT / (refS - refT)
av = cv ** 2
vH_value = (c0 ** 2 - 2 * a0) / (2 * c0)
assert vH_value ** 2 == hx
uH_value, wH_value = vH_value / hx, vH_value / a0
assert vH_value - c0 - a0 * uH_value == refS
assert a0 * wH_value - vH_value + c0 == refT
hv = refT**2/(refS-refT)
assert hv*(hv+refS+refT) == av
fixture = {0: Q(2) - (2 * av.re) ** 2, 1: Q(0), 2: Q(0), 9: av.re, 32: Q(2)}
for index, value in [(3, uH_value), (5, wH_value), (7, vH_value),
                     (10, refS), (12, refT), (14, K(0)),
                     (16, K(0)), (18, hv), (20, K(0))]:
    fixture[index], fixture[index + 1] = value.re, value.im
for start in (33, 51):
    fixture[start + 11] = Q(1)  # e
    fixture[start + 12] = Q(1)  # u
    fixture[start + 14] = Q(1)  # v


def evaluate(row, values):
    total = Q(0)
    for (power, mon), coefficient in row.items():
        term = Q(coefficient) * values.get(0, Q(0)) ** power
        for i in mon:
            term *= values.get(i, Q(0))
        total += term
    return total


assert all(evaluate(row, fixture) == 0 for row in pre)
assert all(evaluate(row, fixture) == 0 for row in final)
assert evaluate(polynomial, fixture) == 0

receipt = {
    'status': 'PASS',
    'scope': 'Exact source equations, invertible row transformations, coefficient table, census, and full expansion; arithmetic source hypotheses are audited separately.',
    'implementation': 'Independent standard-library rational-pair sparse arithmetic; no producer import, inherited residual import, or LLL rerun.',
    'quadraticSha256': sha256(quad_bytes).hexdigest(),
    'polynomialSha256': sha256(poly_bytes).hexdigest(),
    'variables': 68, 'quadraticRows': 56, 'commonRows': 24,
    'detectorBlocks': 2, 'rationalCoordinatesPerDetectorBlock': 18,
    'rowsPerDetectorBlock': 16,
    'coordinateCensus': {'rationalCommonIncludingHalfTrace': 6, 'referenceField': 3,
                         'pairIncludingReciprocalsField': 6, 'helperField': 2, 'errorSquareField': 2,
                         'rationalDetectorBlocks': 36},
    'referenceRows': 4,
    'referenceMatrixDeterminant': str(determinant),
    'referenceInverseIntegral': True,
    'referenceNormalizationScales': [str(x) for x in reference_scales],
    'referenceConstants': {'a0': ['1', '1'], 'c0': ['4', '-2'],
                           'delta0': ['-23', '17'], 'normDelta0': '-49'},
    'referenceAffineOutputs': 'S=vH-c0-a0*uH, T_H=a0*wH-vH+c0',
    'referenceReciprocals': 'f(H)=uH/vH, f(H-R0)=wH/vH; vH is automatically a unit',
    'completePairedChartIdentities': 6,
    'derivedDifferenceAbscissa': 'a=h*(h+s+t); only Re(a) is a retained rational coordinate',
    'deletedImaginaryComponent': 'Reconstructed uniquely as Im(h*(h+s+t)); no guard uses it',
    'twoTorsionDifferenceCheck': 'All finite two-torsion differences are allowed, including (0,0); U=V is impossible.',
    'literalInputEquation': 'b2-X^2=0',
    'literalHeightEquation': 't1-lambda-B-b4^2-4*a_real^2=0',
    'errorSquares': ['C2=(s-S)^2', 'I2=(t-T_H)^2'],
    'reciprocalHelpers': 'F=beta^2/x(U), G=beta^2/x(V) are chart coordinates; vH*J=uH*F, vH*K=wH*G',
    'constantPivotRow': 37, 'constantBasisRoundTrips': 56,
    'degree': 4, 'contentForEveryIntegerB': 1,
    'ordinaryMonomialsForEveryIntegerBAtLeast81': 1078,
    'parameterSeparatedTerms': 1081,
    'constantCoefficient': 'B^2+1',
    'largestFixedCoefficient': 3554,
    'largestFixedCoefficientMonomials': fixed_at,
    'parameterLinearCoefficients': moving,
    'exactHeightForEveryIntegerBAtLeast81': 'B^2+1',
    'zeroInputFixture': {'reference': 'H=2R0', 'parameterB': str(fixture[0]),
                         'all56LiteralAndTransformedRowsVanish': True,
                         'arithmeticHeightThresholdClaimed': False},
    'noArithmeticFoundationClaimFromFiniteCertificate': True,
}
for key in ['variables', 'quadraticRows', 'degree', 'largestFixedCoefficient',
            'constantCoefficient', 'parameterSeparatedTerms']:
    assert report[key] == receipt[key]
assert report['coordinateMonomials'] == 1078 and report['content'] == 1
assert report['exactHeight'] == receipt['exactHeightForEveryIntegerBAtLeast81']
args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': 'PASS', 'output': str(args.output),
                  'variables': 68, 'rows': 56, 'degree': 4,
                  'heightForBAtLeast81': receipt['exactHeightForEveryIntegerBAtLeast81']}))
