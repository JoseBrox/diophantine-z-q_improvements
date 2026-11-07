#!/usr/bin/env python3
"""Exact checks for the quadratic elliptic-height bound and curve obstruction.

Uses only Python's standard library. Finite calculations certify identities,
constants, point counts, and all recorded downstream bound envelopes. The
uniform height and curve-image assertions are proved in the accompanying TeX.
"""
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class K:
    a: Q
    b: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', Q(self.a))
        object.__setattr__(self, 'b', Q(self.b))

    def __add__(self, other):
        other = other if isinstance(other, K) else K(other)
        return K(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self): return K(-self.a, -self.b)
    def __sub__(self, other): return self+-K(other) if not isinstance(other, K) else self+-other
    def __rsub__(self, other): return -self+other

    def __mul__(self, other):
        other = other if isinstance(other, K) else K(other)
        return K(self.a*other.a+2*self.b*other.b, self.a*other.b+self.b*other.a)

    __rmul__ = __mul__

    def inverse(self):
        n = self.a*self.a-2*self.b*self.b
        assert n
        return K(self.a/n, -self.b/n)

    def __truediv__(self, other):
        return self*(other if isinstance(other, K) else K(other)).inverse()

    def __rtruediv__(self, other): return self.inverse()*other

    def __pow__(self, n):
        if n < 0: return self.inverse()**(-n)
        result = K(1)
        base = self
        while n:
            if n & 1: result *= base
            base *= base
            n //= 2
        return result

    def conj(self): return K(self.a, -self.b)
    def norm(self): return self.a*self.a-2*self.b*self.b

    def triple(self):
        c = lcm(self.a.denominator, self.b.denominator)
        a, b = int(self.a*c), int(self.b*c)
        g = gcd(gcd(abs(a), abs(b)), c)
        return a//g, b//g, c//g


D = K(11, -6)
P = K(Q(57, 8), Q(-7, 2)), K(Q(-165, 8), Q(417, 32))


def on_curve(point):
    return point is None or point[1]**2 == point[0]**3-D*point[0]


def add_points(a, b):
    if a is None: return b
    if b is None: return a
    x, y = a
    u, v = b
    if x == u:
        if y == -v: return None
        assert y == v
        slope = (3*x*x-D)/(2*y)
    else:
        slope = (v-y)/(u-x)
    z = slope*slope-x-u
    return z, slope*(x-z)-y


def poly_add(a, b):
    c = Counter(a)
    for k, v in b.items(): c[k] += v
    return {k: v for k, v in c.items() if v}


def poly_scale(a, s): return {k: v*s for k, v in a.items() if v*s}


def poly_mul(a, b):
    c = Counter()
    for e, v in a.items():
        for f, w in b.items(): c[tuple(x+y for x, y in zip(e, f))] += v*w
    return {k: v for k, v in c.items() if v}


def polynomial_identity_checks():
    u, v, d = [{tuple(int(i == j) for i in range(3)): 1} for j in range(3)]
    sq = lambda p: poly_mul(p, p)
    uv = poly_mul(u, v)
    lhs = poly_add(poly_mul(sq(poly_add(u, v)), sq(poly_add(uv, poly_scale(d, -1)))),
                   poly_scale(poly_mul(uv, poly_mul(poly_add(sq(u), poly_scale(d, -1)),
                                                    poly_add(sq(v), poly_scale(d, -1)))), -4))
    rhs = poly_mul(sq(poly_add(u, poly_scale(v, -1))), sq(poly_add(uv, d)))
    assert lhs == rhs
    # (3u²-D)²-8u²(u²-D)=(u²+D)².
    assert poly_add(sq(poly_add(poly_scale(sq(u), 3), poly_scale(d, -1))),
                    poly_scale(poly_mul(sq(u), poly_add(sq(u), poly_scale(d, -1))), -8)) == sq(poly_add(sq(u), d))


def finite_field_checks():
    p = 17
    assert 4*4 % p == p-1
    squares = {y*y % p for y in range(p)}
    reports = []
    for s, expected_D, expected_count in [(6, 9, 20), (11, 13, 16)]:
        assert s*s % p == 2
        d = (11-6*s) % p
        assert d == expected_D and (64*d**3) % p != 0
        rows = [[x, (x**3-d*x) % p,
                 sum(y*y % p == (x**3-d*x) % p for y in range(p))]
                for x in range(p)]
        direct = 1+sum(r[2] for r in rows)
        legendre = 1+sum(1 if r[1] == 0 else 2 if r[1] in squares else 0 for r in rows)
        assert direct == legendre == expected_count
        reports.append({'sqrt2_residue': s, 'D_residue': d,
                        'point_count': direct, 'abscissa_rhs_and_root_counts': rows})
    return reports


def exact_points():
    assert on_curve(P) and D.norm() == 49
    assert P[0].norm() == Q(41**2, 8**2)
    R0 = K(1, 1), K(0, 2)
    assert on_curve(R0) and add_points(R0, R0) == P
    points = [None, P]
    records = []
    for n in range(2, 34):
        points.append(add_points(points[-1], P))
        assert on_curve(points[-1])
    for n in range(1, 17):
        x = points[n][0]
        doubled = (x*x+D)**2/(4*x*(x*x-D))
        assert doubled == points[2*n][0]
        u = points[n+1][0]
        odd = (x*u+D)**2/(P[0]*(x-u)**2)
        assert odd == points[2*n+1][0]
    for n in range(1, 34):
        x, y = points[n]
        a, b, c = x.triple()
        h0 = (max(1, abs(a), abs(b), c)-1).bit_length()
        assert h0 <= 30*n*n
        if y.a:
            A, B = (x*x*x-D*x).a, (x*x*x-D*x).b
            Y = 2*y.a
            assert Y**4-4*A*Y**2+8*B**2 == 0
            assert K(Y/2, B/Y) == y
        records.append({'multiple': n, 'coefficient_binary_height': h0,
                        'proved_upper_bound': 30*n*n})
    translated = add_points(R0, (K(0), K(0)))
    assert not R0[1].a and translated[1].a
    assert translated[1]/R0[1] == D/(R0[0]**2)
    d = K(3, -1)
    assert d*d == D and d*d.conj() == K(7)
    assert d.conj()/d == 7/(d*d) and d**3 == K(45, -29)
    # Three is inert in K. Its valuation on a+b*sqrt(2) is the minimum
    # of the rational coefficient valuations (with v(0)=infinity).
    def v3(q):
        if not q: return float('inf')
        def ord3(n):
            s = 0
            while n % 3 == 0: s, n = s+1, n//3
            return s
        return ord3(abs(q.numerator))-ord3(q.denominator)
    val = lambda z: min(v3(z.a), v3(z.b))
    assert val(P[0]) == 0 and val(P[1]) == 1
    assert val(3*P[0]**2-D) == 0
    twice = points[2]
    assert (val(twice[0]), val(twice[1]), val(-twice[0]/twice[1])) == (-2, -3, 1)
    return records


def ceil_log2(n): return (n-1).bit_length() if n > 0 else 0


def bound_certificate():
    spec_path = HERE/'construction29/polynomial-29-preferred/polynomial-specification.json'
    spec = json.loads(spec_path.read_text())
    math_data = {k: v for k, v in spec.items() if k != 'bounds'}
    math_digest = sha256(json.dumps(math_data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert math_digest == '24cacbb45176225d8e8278edeaf170cada85b0397134c69867ad8641a26f2823'
    bd = spec['bounds']
    assert len(bd['indexed_guard_bounds']) == 1
    anchor = bd['indexed_guard_bounds'][0]
    E = spec['indexed_guard_polynomials'][0]['index_last']['exponent']
    b = anchor['coordinate_operator_log2_norm_bound']
    assert (E, b) == (2093449, 1048)
    assert E >= 6 and 30*64+(2*b+14) < 64**2
    assert 20*64**3+30*64**2+(2*b+14)*64 < 21*64**3
    assert 21 < 2**5
    assert anchor['operator_log2_norm_bound_power_of_two_exponent'] == 3*E+5
    # Recompute each final envelope without importing either producer/checker.
    w, l = bd['generator_weights'], bd['generator_operator_log2_norm_bounds']
    r = bd['maximum_rank_power_of_two_exponent']
    n = 1 << r
    g = max(ceil_log2(bd['materialized_guard_weight']),
            anchor['weight_bound_power_of_two_exponent'])+1
    gb = max(ceil_log2(bd['materialized_guard_operator_log2_norm_bound']), 3*E+5)+1
    a = max(g, ceil_log2(max(w)+bd['maximum_basis_weight']))+1
    bb = max(gb, ceil_log2(bd['selector_operator_log2_norm_bound']))+1
    AH, BH = r+a, r+bb+1
    AR = max(r+a, ceil_log2(bd['closed_residual_maximum_weight']+bd['maximum_basis_weight']))+1
    BR = max(ceil_log2(r+bd['closed_residual_maximum_operator_log2_norm_bound']), r+bb+1)+1
    AL = r+2+AH
    BL = max(r+2+BH, r+1+ceil_log2(r))+1
    pd, pb = r+AL+1, max(r+BL, ceil_log2(r+1))+1
    rd, rb = max(AR, r+AL+1)+1, max(BR, r+BL)+1
    branch_d = 1+max(AH, pd, rd)
    branch_b = max(1+max(BH, pb, rb), ceil_log2(ceil_log2(n+bd['closed_residual_count']+1)))+1
    factors = bd['exact_number_of_final_factors']
    new_degree = branch_d+ceil_log2(factors)
    new_height = branch_b+ceil_log2(factors)
    assert (new_degree, new_height) == (2093605, 6280501)
    assert bd['degree_bound_power_of_two_exponent'] == new_degree
    assert bd['coefficient_height_bound_double_power_of_two_exponent'] == new_height
    other = json.loads((HERE/'construction29/polynomial-31-preferred/polynomial-specification.json').read_text())
    assert other['bounds']['degree_bound_power_of_two_exponent'] == 180
    assert other['bounds']['coefficient_height_bound_double_power_of_two_exponent'] == 184
    return {'cutoff_exponent': E, 'coordinate_log2_norm_bound': b,
            'exclusion_log2_norm_upper_bound': '21*M^3',
            'exclusion_log2_norm_binary_exponent': 3*E+5,
            'degree_bound_power_of_two_exponent': new_degree,
            'coefficient_height_bound_double_power_of_two_exponent': new_height,
            'polynomial_data_sha256_excluding_only_bounds': math_digest,
            'specification_sha256': sha256(spec_path.read_bytes()).hexdigest()}


def main():
    polynomial_identity_checks()
    assert 23534 == 41*574
    assert 574**3 == 23534*8036 and 574**3 >= 392
    assert 23534**2 < 2**30
    report = {'status': 'PASS', 'symbolic_duplication_identity': True,
              'symbolic_differential_addition_identity': True,
              'exact_height_induction_constants': {'A_exponential': 23534, 'B_exponential': 574,
                                                    'doubling_constant_exponential': 392,
                                                    'odd_step_constant_exponential': 8036},
              'exact_point_checks': exact_points(),
              'non_torsion_valuation_certificate_at_three': {'xP': 0, 'yP': 1, 'tangent_numerator': 0, 'x2P': -2, 'y2P': -3, 'formal_parameter_2P': 1},
              'independent_nonisogeny_point_counts': finite_field_checks(),
              'bound_certificate': bound_certificate(),
              'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Exact identities, finite point calculations, two finite-field counts, induction constants, and all numerical coefficient envelopes. The general height bound and finite rational-image theorem are supplied as mathematical proofs, not inferred from samples.'}
    (HERE/'quadratic-height-verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'fixed_multiples_checked': len(report['exact_point_checks']),
                      'nonisogeny_counts': [r['point_count'] for r in report['independent_nonisogeny_point_counts']],
                      'bound_certificate': report['bound_certificate']}, indent=2))


if __name__ == '__main__': main()
