#!/usr/bin/env python3
"""Independent exact checks for the complete three-coordinate reference chart."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def add(*polys):
    result = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(poly, coefficient):
    return {m: c * coefficient for m, c in poly.items() if c * coefficient}


def mul(left, right):
    result = {}
    for m, a in left.items():
        for n, b in right.items():
            exponent = tuple(x + y for x, y in zip(m, n))
            result[exponent] = result.get(exponent, 0) + a * b
    return {m: c for m, c in result.items() if c}


def square(poly):
    return mul(poly, poly)


def variable(i, width=6):
    monomial = [0] * width
    monomial[i] = 1
    return {tuple(monomial): 1}


class Quadratic:
    """Exact arithmetic in Q(sqrt(2)), independent of the polynomial checker."""
    __slots__ = ('a', 'b')

    def __init__(self, a=0, b=0):
        self.a, self.b = Fraction(a), Fraction(b)

    @staticmethod
    def convert(other):
        return other if isinstance(other, Quadratic) else Quadratic(other)

    def __add__(self, other):
        other = self.convert(other)
        return Quadratic(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.a, -self.b)

    def __sub__(self, other):
        return self + -self.convert(other)

    def __rsub__(self, other):
        return self.convert(other) + -self

    def __mul__(self, other):
        other = self.convert(other)
        return Quadratic(self.a * other.a + 2 * self.b * other.b,
                         self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a * self.a - 2 * self.b * self.b
        if not norm:
            raise ZeroDivisionError
        return Quadratic(self.a / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * self.convert(other).inverse()

    def __rtruediv__(self, other):
        return self.convert(other) * self.inverse()

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse() ** -exponent
        result, base = Quadratic(1), self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        return result

    def __eq__(self, other):
        other = self.convert(other)
        return self.a == other.a and self.b == other.b

    def serialize(self):
        return [str(self.a), str(self.b)]


def field_neg(point):
    return None if point is None else (point[0], -point[1])


def field_add(left, right, D):
    if left is None:
        return right
    if right is None:
        return left
    x, y = left
    X, Y = right
    if x == X:
        if y + Y == 0:
            return None
        slope = (3 * x * x - D) / (2 * y)
    else:
        slope = (Y - y) / (X - x)
    z = slope * slope - x - X
    return z, slope * (x - z) - y


def field_mul(point, multiplier, D):
    if multiplier < 0:
        return field_mul(field_neg(point), -multiplier, D)
    result = None
    while multiplier:
        if multiplier & 1:
            result = field_add(result, point, D)
        point = field_add(point, point, D)
        multiplier >>= 1
    return result


def finite_neg(point, p):
    return None if point is None else (point[0], -point[1] % p)


def finite_add(left, right, D, p):
    if left is None:
        return right
    if right is None:
        return left
    x, y = left
    X, Y = right
    if x == X:
        if (y + Y) % p == 0:
            return None
        slope = (3*x*x-D) * pow(2*y, -1, p) % p
    else:
        slope = (Y-y) * pow(X-x, -1, p) % p
    z = (slope*slope-x-X) % p
    return z, (slope*(x-z)-y) % p


def verify_polynomials():
    a, c, S, T, v, Z = [variable(i) for i in range(6)]
    delta = add(a, scale(square(c), -1))
    D = mul(a, delta)
    q1 = add(mul(v, add(v, T, scale(S, -1))), delta)
    q2 = add(mul(S, T), mul(c, add(T, scale(S, -1))),
             scale(mul(c, v), 2), scale(delta, 2))
    U = add(v, scale(S, -1), scale(c, -1))
    W = add(v, T, scale(c, -1))
    mu = add(v, scale(c, -1))
    Splusc = add(S, c)
    Tminusc = add(T, scale(c, -1))
    checks = {
        'unit_product': add(mul(U, W), scale(a, -1), scale(q1, -1), q2),
        'first_root': add(mul(a, v), scale(mul(add(square(mu), scale(a, -1)), U), -1),
                          mul(v, square(U)), mul(Splusc, q1), scale(mul(v, q2), -1)),
        'second_root': add(mul(a, v), scale(mul(add(square(mu), scale(a, -1)), W), -1),
                           mul(v, square(W)), scale(mul(Tminusc, q1), -1),
                           scale(mul(v, q2), -1)),
        'first_curve': add(mul(mul(U, v), square(S)), mul(delta, square(U)),
                           scale(mul(a, square(v)), -1), scale(mul(square(Splusc), q1), -1),
                           mul(mul(v, Splusc), q2)),
        'second_curve': add(mul(mul(W, v), square(T)), mul(delta, square(W)),
                            scale(mul(a, square(v)), -1), scale(mul(square(Tminusc), q1), -1),
                            scale(mul(mul(v, Tminusc), q2), -1)),
        'line_intersection_factorization': add(
            mul(Z, square(Z)), scale(mul(D, Z), -1),
            scale(square(add(mul(mu, Z), scale(mul(a, v), -1))), -1),
            scale(mul(add(Z, scale(a, -1)),
                      add(square(Z), scale(mul(add(square(mu), scale(a, -1)), Z), -1),
                          mul(a, square(v)))), -1)),
    }
    for name, remainder in checks.items():
        assert remainder == {}, (name, remainder)
    return sorted(checks)


def verify_quadratic_field():
    a = Quadratic(Fraction(57, 8), Fraction(-7, 2))
    b = Quadratic(Fraction(-165, 8), Fraction(417, 32))
    D = Quadratic(11, -6)
    c, delta = b/a, D/a
    assert a != 0 and b != 0 and D != 0
    assert b*b == a*a*a-D*a
    assert c == Quadratic(Fraction(-87, 41), Fraction(129, 164))
    assert delta == Quadratic(Fraction(2328, 1681), Fraction(-272, 1681))
    P = a, b
    T0 = Quadratic(0), Quadratic(0)
    R0 = Quadratic(1, 1), Quadratic(0, 2)
    assert field_add(R0, R0, D) == P
    d = Quadratic(3, -1)
    assert d*d == D
    samples = [('-P', field_neg(P)), ('2P', field_mul(P, 2, D)),
               ('3P', field_mul(P, 3, D)), ('half_P', R0),
               ('negative_half_P', field_neg(R0)),
               ('positive_two_torsion', (d, Quadratic(0))),
               ('negative_two_torsion', (-d, Quadratic(0))),
               ('translated_negative_P', field_add(field_neg(P), T0, D))]
    report = []
    for label, H in samples:
        Q = field_add(H, field_neg(P), D)
        assert H is not None and H[0] != 0
        assert Q is not None and Q[0] != 0
        x, y = H
        if x == a:
            assert H == field_neg(P)
            slope = (3*a*a-D)/(2*y)
        else:
            slope = (y+b)/(x-a)
        v = slope+c
        S, T = y/x, Q[1]/Q[0]
        assert v*(v+T-S)+delta == 0
        assert S*T+c*(T-S)+2*c*v+2*delta == 0
        u, w = (v-S-c)/a, (v+T-c)/a
        assert u*w == 1/a
        assert v != 0 and u != 0 and w != 0
        assert 1/v == -(v+T-S)/delta
        assert (v/u, S*v/u) == H
        assert (v/w, T*v/w) == Q
        assert u/v == 1/H[0] and w/v == 1/Q[0]
        report.append({'label': label, 'S': S.serialize(), 'T': T.serialize(),
                       'v': v.serialize(), 'same_abscissa': H[0] == Q[0],
                       'zero_ratio': S == 0 or T == 0})
    excluded = [None, T0, P, field_add(P, T0, D)]
    for H in excluded:
        Q = field_add(H, field_neg(P), D)
        assert H is None or H[0] == 0 or Q is None or Q[0] == 0
    return {'constants': {'a': a.serialize(), 'b': b.serialize(), 'D': D.serialize(),
                           'c': c.serialize(), 'delta': delta.serialize()},
            'allowed_samples': report, 'excluded_points_checked': 4}


def verify_finite_fields():
    reports = []
    totals = {'parameter_pairs': 0, 'chart_points': 0, 'tangent_at_fixed_point': 0,
              'other_repeated_intersections': 0, 'triple_intersections': 0,
              'zero_ratios': 0}
    for p in [3, 5, 7, 11, 13, 17, 19]:
        record = {'prime': p, 'parameter_pairs': 0, 'chart_points': 0}
        for D in range(1, p):
            points = [None] + [(x, y) for x in range(p) for y in range(p)
                               if (y*y-x*x*x+D*x) % p == 0]
            for P in points:
                if P is None or not P[0] or not P[1]:
                    continue
                a, b = P
                c, delta = b*pow(a, -1, p) % p, D*pow(a, -1, p) % p
                minusP = finite_neg(P, p)
                domain = set()
                for H in points:
                    Q = finite_add(H, minusP, D, p)
                    if H is not None and H[0] and Q is not None and Q[0]:
                        domain.add(H)
                assert len(domain) == len(points)-4
                image = set()
                tuples = set()
                # q1 forces v!=0 and then uniquely determines T.
                for v in range(1, p):
                    for S in range(p):
                        T = (S-v-delta*pow(v, -1, p)) % p
                        if (S*T+c*(T-S)+2*c*v+2*delta) % p:
                            continue
                        u = (v-S-c)*pow(a, -1, p) % p
                        w = (v+T-c)*pow(a, -1, p) % p
                        assert u and w and (a*u*w) % p == 1
                        x, xprime = v*pow(u, -1, p) % p, v*pow(w, -1, p) % p
                        H, Q = (x, S*x % p), (xprime, T*xprime % p)
                        assert H in domain
                        assert finite_add(H, minusP, D, p) == Q
                        assert H not in image
                        image.add(H)
                        tuples.add((S, T, v))
                        totals['tangent_at_fixed_point'] += int(x == a)
                        totals['other_repeated_intersections'] += int(x == xprime)
                        totals['triple_intersections'] += int(x == xprime == a)
                        totals['zero_ratios'] += int(S == 0 or T == 0)
                assert image == domain
                # Independent construction from every allowed elliptic point.
                for H in domain:
                    x, y = H
                    Q = finite_add(H, minusP, D, p)
                    if x == a:
                        assert H == minusP
                        slope = (3*a*a-D)*pow(2*y, -1, p) % p
                    else:
                        slope = (y+b)*pow(x-a, -1, p) % p
                    v = (slope+c) % p
                    S, T = y*pow(x, -1, p) % p, Q[1]*pow(Q[0], -1, p) % p
                    assert (S, T, v) in tuples
                record['parameter_pairs'] += 1
                record['chart_points'] += len(tuples)
        reports.append(record)
        totals['parameter_pairs'] += record['parameter_pairs']
        totals['chart_points'] += record['chart_points']
    assert totals['triple_intersections'] > 0
    assert totals['zero_ratios'] > 0
    return {'fields': reports, 'totals': totals,
            'scope': 'Exhaustive for every D!=0 and every fixed P with ab!=0 in the listed fields.'}


def run():
    return {
        'schema': 'three-coordinate-reference-chart-check/v40',
        'universal_polynomial_identities': verify_polynomials(),
        'quadratic_field_checks': verify_quadratic_field(),
        'finite_field_checks': verify_finite_fields(),
        'scope': 'Exact algebraic certificates and finite exhaustive checks. The all-field '
                 'isomorphism and exceptional-point analysis are proved in the companion paper. '
                 'No defining-polynomial variable reduction or arithmetic realization is asserted.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    report = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'passed',
                      'finite_field_totals': report['finite_field_checks']['totals'],
                      'certificate_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()},
                     sort_keys=True))
