#!/usr/bin/env python3
"""Independent exact audit of the v80 one-helper quartic.

No producer or prior checker is imported.  The physical reconstruction of
the unchanged v78 chart follows the previously audited v79 checker, copied
here and explicitly preserved as a dependency rather than claimed anew.
SymPy expands the complete new polynomial independently of the producer's
sparse convolution.  The new normalizer and twist identities are derived
directly from their formulas.  The accompanying proof_review58.md separates
this finite certificate from
the conditional arithmetic argument and its retained premises.

Run normally to verify the checked-in certificate; use --write once when
intentionally regenerating the certificate after a reviewed data change.
"""
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from math import gcd
from pathlib import Path
import argparse
import hashlib
import json

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / 'quartic58'
PARENT = ROOT / 'computation/coauthor_audit_v78/work_abc/small_gate62/primitive/quadrics.json'
V79 = ROOT / 'computation/variable_reductions_v79/abc/quartic59/quadrics.json'
KEEP = [1, *range(3, 32), *range(36, 47), 59, 61, 62]
OLD = dict(zip(KEEP, range(1, 45), strict=True))
NEW_NAMES = ('M M2 x y x2 x4 Gx Gpx y2 y4 Gy Gpy Ha alpha').split()
NEW = dict(zip(NEW_NAMES, range(45, 59), strict=True))
SHIFTS = (-8, -7, -2, -1, 3, 4, 5, 6)
B = s.Symbol('B')
Z = (None, *s.symbols('z1:59'))


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expression(terms, coordinate):
    seen = set()
    result = s.Integer(0)
    for term in terms:
        key = (term['parameterPower'], tuple(term['monomial']))
        assert key not in seen and tuple(sorted(key[1])) == key[1]
        seen.add(key)
        a = int(term['coefficient'])
        assert a
        result += a * B ** key[0] * s.prod(coordinate(i) for i in key[1])
    return s.expand(result)


def equal(left, right):
    assert s.cancel(left - right) == 0, (left, right)


def scalar_multiple(left, right):
    ratio = s.cancel(left / right)
    assert ratio.is_Rational and ratio != 0, (left, right, ratio)
    return str(ratio)


def selected(name):
    return (name.startswith(('reference.', 'pair.', 'product.', 'height.', 'C', 'I'))
            or name in {'product0', 'product1', 'sharedD', 'shared.unit'}
            or name.startswith('detector0.pole.'))


def reconstruct_physical_parent(parent_rows):
    """Reconstruct 31 physical equations and the unit row, not a row copy.

    Source labels here are the physical labels of the supplied v78 chart.
    Both the source-label list and its Laurent weights are stated explicitly,
    rather than inferred from a successful comparison.
    """
    source_ids = [*range(1, 36), *range(40, 54), *range(60, 69), 71, 73, 100, 101]
    assert len(source_ids) == 62
    weights = {i: 0 for i in source_ids if i < 100}
    weights.update({i: -1 for i in (16, 17, 20, 21)})
    weights.update({i: 1 for i in
                    (2, 28, 29, 32, 33, 34, 35, 40, 41, 42, 43, 44,
                     45, 47, 49, 50, 51, 52, 53, 60, 61, 62, 63, 65,
                     67, 68, 71, 73)})
    v = {i: s.Symbol(f'v{i}') for i in source_ids if i < 100}
    c = s.Symbol('c', nonzero=True)

    def physical_stored(old):
        src = source_ids[old - 1]
        if src == 100:
            return c
        if src == 101:
            return 1 / c
        return v[src] / c ** weights[src]

    def field(i):
        return (v[i], v[i + 1])

    def plus(*args):
        return tuple(sum(a[j] for a in args) for j in (0, 1))

    def scale(a, q):
        return tuple(q * z for z in a)

    def minus(a, b):
        return plus(a, scale(b, -1))

    def times(a, b):
        return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def bar(a):
        return (a[0], -a[1])

    def norm(a):
        return a[0] ** 2 - 2 * a[1] ** 2

    out, divisors = {}, {}

    def field_rows(name, pair, divisor=0, first=0):
        for j, entry in enumerate(pair):
            out[f'{name}{j + first}'] = entry
            divisors[f'{name}{j + first}'] = divisor

    S, T, vf = field(3), field(5), field(7)
    kap, delta, delta0 = (4, -2), (11, -6), (-23, 17)
    uref = times((-1, 1), minus(minus(vf, kap), S))
    wref = times((-1, 1), minus(plus(vf, T), kap))
    field_rows('reference.primitive.', plus(times(vf, minus(plus(vf, T), S)), delta0), first=1)
    field_rows('reference.primitive.',
               plus(times(S, T), times(kap, minus(plus(T, scale(vf, 2)), S)), scale(delta0, 2)),
               first=3)

    ss, tt, ff, gg, hh, dd = [field(i) for i in (10, 12, 14, 16, 18, 20)]
    pi, diff = plus(hh, ss, tt), minus(ss, tt)
    out['pair.differenceReal'] = v[9] - times(hh, pi)[0]
    field_rows('pair.firstProduct.', minus(dd, times(pi, ff)))
    field_rows('pair.secondProduct.', minus(dd, times(hh, gg)), divisor=-1)
    field_rows('pair.secant.', plus(times(delta, plus(ff, gg)), scale(times(diff, hh), -1), times(tt, tt)))
    field_rows('pair.scale.', plus((v[31], 0), scale(times(dd, diff), -1), times(delta, times(ff, gg))), divisor=-1)

    pp, qq, uu, vv = [field(i) for i in (26, 28, 22, 24)]
    J, KK = scale(plus(uu, vv), s.Rational(1, 2)), bar(scale(minus(uu, vv), 1 / (2 * c)))
    field_rows('product.first.', minus(times(vf, J), times(uref, ff)))
    field_rows('product.second.', minus(times(vf, KK), times(wref, gg)), divisor=-1)
    field_rows('C', minus(scale(plus(pp, qq), s.Rational(1, 2)), times(minus(ss, S), minus(ss, S))))
    field_rows('I', minus(bar(scale(minus(pp, qq), 1 / (2 * c))), times(minus(tt, T), minus(tt, T))))
    W = field(40)
    field_rows('product', minus(W, plus((1, 0), scale(times(pp, qq), c), scale(times(uu, vv), c ** 2))), divisor=2)
    out['sharedD'] = 2 * W[0] * v[71] - norm(minus(W, (1, 0)))
    divisors['sharedD'] = 2
    out['height.betaSquare'] = v[30] - v[1] ** 2
    out['height.betaFourth'] = v[31] - v[30] ** 2
    b, e, pu, p, pv, q, p2, q2 = [v[i] for i in (43, 44, 45, 46, 47, 48, 49, 50)]
    out.update({
        'detector0.pole.pSquare': p2 - p ** 2,
        'detector0.pole.first': e ** 2 + b * p2 - 1,
        'detector0.pole.factor': pu * pv - e * (1 - b),
        'detector0.pole.qSquare': q2 - q ** 2,
        'detector0.pole.second': pu ** 2 - pv ** 2 - b * q2,
    })
    for name in ('first', 'factor', 'second'):
        divisors[f'detector0.pole.{name}'] = 2

    ratios = {}
    for row in parent_rows:
        name = row['name']
        if not selected(name):
            continue
        decoded = expression(row['terms'], physical_stored)
        if name == 'shared.unit':
            equal(decoded, 0)
        else:
            decoded *= c ** divisors.get(name, 0)
            ratios[name] = scalar_multiple(decoded, out.pop(name))
    assert not out and len(ratios) == 31
    return ratios


def contact_polynomials():
    t = s.Symbol('t')
    G = s.Poly(s.prod(t + r for r in SHIFTS), t)
    a6 = G.nth(6)
    P = s.Poly(t * G.diff().as_expr() - 8 * G.as_expr(), t)
    Q = s.Poly((4 * t ** 2 + a6) * G.diff().as_expr() - 32 * t * G.as_expr(), t)
    assert G.nth(7) == 0 and a6 == -102 and P.degree() <= 6 and Q.degree() <= 6
    equal((4 * t ** 2 + a6) - 4 * t * t, a6)
    assert s.gcd(s.Poly(t, t), s.Poly(4 * t ** 2 + a6, t)).degree() == 0
    assert len(set(SHIFTS)) == 8 and sum(SHIFTS) == 0 and all(SHIFTS)
    assert all(a + b != 0 for a in SHIFTS for b in SHIFTS)
    assert 2 * 3 ** 4 + 2 * min(SHIFTS) == 146 > 0
    return t, G, P, Q


def new_rows(G, P, Q):
    n = {name: Z[i] for name, i in NEW.items()}
    c, ci, d, tau, b = [Z[OLD[i]] for i in (61, 62, 59, 38, 39)]
    rows = {
        'single.alpha': n['alpha'] - ci - d ** 2,
        'single.gate': tau * (1 + n['alpha']) - n['alpha'],
        'single.poleInput': b - 7 * tau ** 2,
        'height.M': n['M'] - B - Z[OLD[31]] ** 2 - 4 * Z[OLD[9]] ** 2,
        'height.M2': n['M2'] - n['M'] ** 2,
        'contact.midpoint': c * (n['x'] + n['y']) - 2 * n['M2'] ** 2,
    }
    for side in ('x', 'y'):
        t, t2, t4 = [n[side + suffix] for suffix in ('', '2', '4')]
        value, deriv = n['G' + side], n['Gp' + side]
        powers = {0: ci ** 2, 1: t * ci, 2: t2 * ci, 3: t * t2,
                  4: t4 * ci, 5: t * t4, 6: t2 * t4, 8: t4 ** 2}

        def lift(poly):
            return sum(a * powers[i[0]] for i, a in poly.terms())

        rows[f'contact.{side}.square'] = t2 * ci - t ** 2
        rows[f'contact.{side}.fourth'] = t4 * ci - t2 ** 2
        rows[f'contact.{side}.value'] = value * ci - lift(G)
        rows[f'contact.{side}.derivative1'] = t * deriv - 8 * value * ci - lift(P)
        rows[f'contact.{side}.derivative2'] = (4 * t2 + G.nth(6) * ci) * deriv - 32 * t * value - lift(Q)
    rows['contact.derivativeSum'] = n['Ha'] - n['Gpx'] * n['Gy'] - n['Gx'] * n['Gpy']
    rows['contact.derivativeQuotient'] = n['Ha'] * ci + 16 * n['Gx'] * n['Gy']
    assert len(rows) == 18
    return {name: s.expand(value) for name, value in rows.items()}


def physical_and_asymptotic_identities(G, P, Q):
    c, u, D, tau, b, e, pu, pv, p, q = s.symbols('c u D tau b e pu pv p q', nonzero=True)
    alpha = s.Symbol('alpha')
    equal((tau * (alpha + 1) - alpha).subs(alpha, -1), 1)
    alpha_c = 1 / c + D ** 2 / c ** 2
    equal(alpha_c.subs(c, 1 / u), u + u ** 2 * D ** 2)
    tau_c = s.cancel(alpha_c / (1 + alpha_c))
    equal(tau_c, (c + D ** 2) / (c ** 2 + c + D ** 2))
    equal((7 * c * tau ** 2).subs(c, 1 / u), 7 * tau ** 2 / u)

    # Check the new contact rows directly in physical coordinates.  The
    # t^2 and t^4 substitutions express the two recovered power equations.
    new = new_rows(G, P, Q)
    physical = {Z[OLD[61]]: c, Z[OLD[62]]: 1 / c}
    normalizer_physical = physical | {
        Z[NEW['alpha']]: alpha, Z[OLD[59]]: D / c,
        Z[OLD[38]]: tau, Z[OLD[39]]: b / c}
    equal(new['single.alpha'].subs(normalizer_physical), alpha - alpha_c)
    equal(new['single.gate'].subs(normalizer_physical), tau * (alpha + 1) - alpha)
    equal((c * new['single.poleInput']).subs(normalizer_physical), b - 7 * c * tau ** 2)
    slot = {}
    for side in ('x', 'y'):
        tx, gx, hx = s.symbols(f'{side} G_{side} H_{side}')
        slot[side] = (tx, gx, hx)
        physical.update({Z[NEW[side]]: tx / c,
                         Z[NEW[side + '2']]: tx ** 2 / c,
                         Z[NEW[side + '4']]: tx ** 4 / c,
                         Z[NEW['G' + side]]: gx / c,
                         Z[NEW['Gp' + side]]: hx / c})
        equal((c ** 2 * new[f'contact.{side}.square']).subs(physical), 0)
        equal((c ** 2 * new[f'contact.{side}.fourth']).subs(physical), 0)
        equal((c ** 2 * new[f'contact.{side}.value']).subs(physical), gx - G.as_expr().subs(G.gen, tx))
        equal((c ** 2 * new[f'contact.{side}.derivative1']).subs(physical),
              tx * hx - 8 * gx - P.as_expr().subs(P.gen, tx))
        equal((c ** 2 * new[f'contact.{side}.derivative2']).subs(physical),
              (4 * tx ** 2 - 102) * hx - 32 * tx * gx - Q.as_expr().subs(Q.gen, tx))
    Fa0 = s.Symbol('F_a')
    physical[Z[NEW['Ha']]] = Fa0 / c ** 2
    xx, gx, hx = slot['x']
    yy, gy, hy = slot['y']
    equal((c ** 2 * new['contact.derivativeSum']).subs(physical), Fa0 - hx * gy - gx * hy)
    equal((c ** 3 * new['contact.derivativeQuotient']).subs(physical), Fa0 + 16 * c * gx * gy)
    mm = s.Symbol('M')
    physical[Z[NEW['M2']]] = mm ** 2
    equal(new['contact.midpoint'].subs(physical), xx + yy - 2 * mm ** 4)

    # The retained native rows have physical b=c*b_s, e=c*e_s,
    # pu=c*pu_s, pv=c*pv_s, p=p_s, q=q_s, p^2=c*P_s, q^2=c*Q_s.
    equal(c ** 2 * ((e / c) ** 2 + (b / c) * (p ** 2 / c) - 1 / c ** 2), e ** 2 + b * p ** 2 - 1)
    equal(c ** 2 * ((b / c) * (e / c) - (e / c) / c + (pu / c) * (pv / c)), pu * pv - e * (1 - b))
    equal(c ** 2 * ((b / c) * (q ** 2 / c) - (pu / c) ** 2 + (pv / c) ** 2), -(pu ** 2 - pv ** 2 - b * q ** 2))

    a, z = s.symbols('a z')
    tt = G.gen
    F = s.Poly(G.as_expr().subs(tt, a - z) * G.as_expr().subs(tt, a + z), z)
    Fa = s.Poly(s.diff(F.as_expr(), a), z)
    assert F.degree() == 16 and F.LC() == 1
    assert Fa.degree() == 14 and Fa.LC() == -16 * a
    equal(s.limit((-16 * F.as_expr() / Fa.as_expr()) * a / z ** 2, z, s.oo), 1)

    # W=1+c*A+O(c^2), with bounded field coefficients.  Compute the
    # leading term of Nm(W-1)/Tr(W), allowing leading coefficient zero.
    aa = s.symbols('A0:8')
    W0 = 1 + sum(aa[2 * j] * c ** (j + 1) for j in range(4))
    W1 = sum(aa[2 * j + 1] * c ** (j + 1) for j in range(4))
    det = ((W0 - 1) ** 2 - 2 * W1 ** 2) / (2 * W0)
    equal(s.limit(det / c ** 2, c, 0), (aa[0] ** 2 - 2 * aa[1] ** 2) / 2)
    E = s.Symbol('E')
    equal(tau_c.subs(D, c ** 2 * E), (1 + c ** 3 * E ** 2) / (1 + c + c ** 3 * E ** 2))
    equal(s.limit(tau_c.subs(D, c ** 2 * E), c, 0), 1)
    equal(tau_c.subs(D, 0), 1 / (1 + c))
    equal((7 * c * tau_c ** 2).subs(D, 0), 7 * c / (1 + c) ** 2)
    return {'degree_F_in_z': 16, 'leading_F': '1', 'degree_Fa_in_z': 14,
            'leading_Fa': '-16*a', 'u_at_slope_infinity': 'u*a/z^2 -> 1',
            'normalizer_at_c_zero': 'tau=(1+c^3*E^2)/(1+c+c^3*E^2), D=c^2*E',
            'zero_D_fiber': 'tau=1/(1+c), b=7*c/(1+c)^2'}


def native_twist_identities():
    """Check the exact map from the two curves used in Theorem B.

    This is an identity in a rational function field.  The arithmetic
    hypotheses and nonzero factors are verified in the manual review.
    """
    b, a1, a2, r, y1, y2 = s.symbols('b a1 a2 r y1 y2', nonzero=True)
    e = r / (b * a1 ** 2)
    p = y1 / (b ** 2 * a1 ** 3)
    pu = a2 / a1
    pv = e * (1 - b) / pu
    q = y2 / (b ** 2 * a1 ** 3 * pu ** 2)
    curve1 = y1 ** 2 - b ** 3 * a1 ** 6 + r ** 2 * b * a1 ** 2
    curve2 = y2 ** 2 - b ** 3 * a2 ** 6 + r ** 2 * (1 - b) ** 2 * b * a2 ** 2
    equal(e ** 2 + b * p ** 2 - 1, curve1 / (b ** 3 * a1 ** 6))
    equal(pu * pv - e * (1 - b), 0)
    equal(pu ** 2 - pv ** 2 - b * q ** 2, -curve2 / (b ** 3 * a1 ** 2 * a2 ** 4))
    eta, dd, xx, yy = s.symbols('eta d x y', nonzero=True)
    equal((dd ** 3 * yy) ** 2 - (dd ** 2 * xx) ** 3
          + (r * eta * dd ** 2) ** 2 * dd ** 2 * xx,
          dd ** 6 * (yy ** 2 - xx ** 3 + (r * eta) ** 2 * xx))
    # Exact prepared class-seven example; it is a native-pole test only,
    # not a claim that any particular contact fixture defines the integers.
    native_example = tuple(map(s.Rational, ('112/841', '3/4', '29/16',
                                          '27/29', '81/116', '27/16')))
    bb, ee, pp, uu, vv, qq = native_example
    equal(ee ** 2 + bb * pp ** 2, 1)
    equal(uu * vv, ee * (1 - bb))
    equal(uu ** 2 - vv ** 2, bb * qq ** 2)
    equal(bb, 7 * s.Rational(4, 29) ** 2)
    return {'first_conic': 'curve1/(b^3*a1^6)', 'middle': '0',
            'second_conic': '-curve2/(b^3*a1^2*a2^4)',
            'twist_scaling': '(x,y)->(d^2*x,d^3*y), 1-b=eta*d^2',
            'prepared_native_example': [str(v) for v in native_example],
            'theorem_B_required_classes': 'beta=7 mod8, eta=1 mod8; eta=1 allowed'}


def valuation_and_height_checks():
    # This finite grid is regression evidence only.  The universal proof is
    # the valuation case split in proof_review58.md, not this loop.
    cases = 0
    for mu in range(-49, 50, 2):
        for d in range(-150, 151):
            assert mu % 2 != (2 * mu + 2 * d) % 2
            va = min(mu, 2 * mu + 2 * d)
            for cancellation_depth in (range(21) if va == 0 else (0,)):
                vt = va if va > 0 else (0 if va < 0 else -cancellation_depth)
                vb = -mu + 2 * vt  # p != 7
                assert vb % 2
                if mu < 0:
                    assert va < 0 and vt == 0 and vb > 0
                elif vb > 0:
                    assert va > 0 and 2 * va > mu and 4 * d > -3 * mu
                cases += 1
        # D=0 has va=mu and vb=abs(mu), so it is retained at either sign.
        va = mu
        vt = mu if mu > 0 else 0
        assert -mu + 2 * vt == abs(mu)
    eps = Fraction(1, 100)
    kap = Fraction(1001, 1000)
    gamma = (8 - 6 - 3 * eps) * Fraction(4, 2) - (2 + eps)
    eta = (2 * kap - 1) / (8 - 6 * kap)
    margin = gamma - 2 * eta
    assert gamma == Fraction(193, 100)
    assert eta == Fraction(501, 997)
    assert margin == Fraction(92221, 99700) > 0
    return {'radical_height_rate': str(gamma), 'input_height_rate': str(eta),
            'strict_margin': str(margin),
            'finite_valuation_regression_cases': cases,
            'finite_valuation_regression_scope': 'Odd -49<=mu<=49, -150<=d<=150; not a universal proof'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    spec, maps, claim = [read(DATA / name) for name in ('quadrics.json', 'maps.json', 'certificate.json')]
    parent = read(PARENT)
    assert spec['variables'] == 58 and spec['input'] == 1 and spec['parameter'] == 'B'
    assert maps['parent'] == str(PARENT.relative_to(ROOT)) and maps['parent_sha256'] == digest(PARENT)
    assert maps['old_to_new'] == {str(k): v for k, v in OLD.items()}
    assert maps['new_coordinates'] == NEW
    assert maps['shifts'] == list(SHIFTS)
    assert maps['physical_scaling'] == {
        'physical_pole_input_multiplier': 7, 'unscaled_alpha': 58,
        'c': 43, 'c_inverse': 44, 'unscaled_tau': 33, 'M': 45, 'M2': 46,
        'contact_degree_one_weight': list(range(47, 57)),
        'contact_derivative_sum_weight': {'coordinate': 57, 'power': 2}}
    rows = {r['name']: expression(r['terms'], lambda i: Z[i]) for r in spec['residuals']}
    assert len(rows) == len(spec['residuals']) == 50
    prior = {r['name']: expression(r['terms'], lambda i: Z[i])
             for r in read(V79)['residuals'] if not r['name'].startswith('single.')}
    assert len(prior) == 47
    assert set(rows) - set(prior) == {'single.alpha', 'single.gate', 'single.poleInput'}
    for name, value in prior.items():
        equal(rows[name], value)
    retained = {r['name']: expression(r['terms'], lambda i: Z[OLD[i]])
                for r in parent['residuals'] if selected(r['name'])}
    assert len(retained) == 32
    ratios = reconstruct_physical_parent(parent['residuals'])
    t, G, P, Q = contact_polynomials()
    assert maps['G_coefficients'] == [int(G.nth(i)) for i in range(9)]
    expected = retained | new_rows(G, P, Q)
    assert set(rows) == set(expected)
    for name in rows:
        equal(rows[name], expected[name])
        assert s.Poly(rows[name], *Z[1:]).total_degree() <= 2

    # Full expansion in a separately implemented polynomial engine.
    total = s.Poly(sum(value ** 2 for value in rows.values()), B, *Z[1:])
    stored = s.Poly(expression(read(DATA / 'polynomial.json')['terms'], lambda i: Z[i]), B, *Z[1:])
    assert total == stored
    profiles = defaultdict(dict)
    for exponents, coefficient in total.terms():
        profiles[exponents[1:]][exponents[0]] = int(coefficient)
    assert len(profiles) == 867 and len(total.terms()) == 870
    assert max(sum(exponents) for exponents in profiles) == 4
    assert set(i + 1 for p in profiles for i, exponent in enumerate(p) if exponent) == set(range(1, 59))
    coefficients = [int(a) for a in total.coeffs()]
    assert reduce(gcd, coefficients) == 1
    x4 = (4,) + (0,) * 57
    assert profiles[x4] == {0: 1}
    fixed = [p[0] for p in profiles.values() if set(p) == {0}]
    fixed_max = max(map(abs, fixed))
    assert fixed_max == 22838305425411
    mixed = []
    for exponents, profile in sorted(profiles.items()):
        if len(profile) > 1:
            monomial = [i + 1 for i, power in enumerate(exponents) for _ in range(power)]
            mixed.append({'monomial': monomial, 'coefficients': {str(i): a for i, a in sorted(profile.items())}})
    assert sorted(mixed, key=lambda p: p['monomial']) == sorted(claim['mixed_profiles'], key=lambda p: p['monomial'])
    assert {tuple(sorted(p.items())) for p in profiles.values() if len(p) > 1} == {
        ((0, 4091), (2, 1)), ((0, 1), (1, 8)), ((0, 1), (1, 2))}
    pure_parameter_caps = {power: max((abs(p[power]) for p in profiles.values() if set(p) == {power}), default=0)
                           for power in (1, 2)}
    # All parameter terms are bounded by B^2+4091 for every positive B.
    assert pure_parameter_caps == {1: 2, 2: 0}
    equal(B ** 2 + 4091 - (8 * B + 1), (B - 4) ** 2 + 4074)
    equal(B ** 2 + 4091 - (2 * B + 1), (B - 1) ** 2 + 4089)
    equal(B ** 2 + 4091 - 2 * B, (B - 1) ** 2 + 4090)

    identities = physical_and_asymptotic_identities(G, P, Q)
    twist_identities = native_twist_identities()
    arithmetic_constants = valuation_and_height_checks()
    assert all(claim[k] == v for k, v in {
        'variables': 58, 'quadrics': 50, 'degree': 4, 'content': 1,
        'monomials': 867, 'parameter_separated_terms': 870,
        'maximum_fixed_coefficient': fixed_max}.items())
    for name in ('radical_height_rate', 'input_height_rate', 'strict_margin'):
        assert claim['height_parameters'][name] == arithmetic_constants[name]

    report = {
        'schema': 'ordinary-abc-quartic58-independent/v80', 'status': 'PASS',
        'method': 'Retained v78 physical reconstruction from the audited v79 checker; new identities and SymPy expansion independent of both producers; no producer or checker import',
        'variables': 58, 'quadrics': 50, 'retained_parent_rows': 32,
        'unchanged_v79_rows': 47,
        'new_or_rederived_v78_rows': 18, 'degree': 4, 'content': 1,
        'coordinate_monomials': 867, 'parameter_separated_terms': 870,
        'exact_height_for_positive_integer_B': 'max(22838305425411,B^2+4091)',
        'physical_parent_row_multipliers': ratios,
        'contact_G_ascending_coefficients': [int(G.nth(i)) for i in range(9)],
        'contact_P_ascending_coefficients': [int(P.nth(i)) for i in range(7)],
        'contact_Q_ascending_coefficients': [int(Q.nth(i)) for i in range(7)],
        'derivative_guard': '(4*t^2-102)-4*t*t=-102',
        'denominator_guard': 'tau*(alpha+1)-alpha becomes 1 at alpha=-1; no eventual guard is used',
        'native_physical_input': 'b=c*z34=7*c*z33^2=7*tau^2/u; alpha=u+u^2*D^2',
        'mixed_profiles': sorted(mixed, key=lambda p: p['monomial']),
        'asymptotic_identities': identities,
        'native_twist_identities': twist_identities,
        'height_and_regression': arithmetic_constants,
        'scope': {
            'exact_computation': 'All 50 equations, retained physical chart, complete sum-of-squares coefficients, maps, counts, height profiles, derivative and native twist identities, rational constants and stated asymptotic identities',
            'proof_review': 'Universal odd-valuation proof, automatic guards, exact Theorem B hypothesis matching and quantified completeness choices are reviewed in proof_review58.md; the finite grid is supplementary only',
            'not_certified_by_computation': 'Rational abc and retained elliptic group, formal comparison, trace-index, simultaneous prime-pattern and the cited Theorem B; no effective sufficient defining B'},
        'input_sha256': {str(path.relative_to(ROOT)): digest(path) for path in
                         [PARENT, V79, DATA / 'quadrics.json', DATA / 'polynomial.json', DATA / 'maps.json', DATA / 'certificate.json']},
    }
    target = HERE / 'independent58.json'
    if args.write:
        target.write_text(json.dumps(report, indent=2) + '\n')
    else:
        assert read(target) == report, 'Independent certificate differs; review before --write'
    print('PASS: 58 variables, 50 quadrics, full physical and coefficient audit; arithmetic scope is explicit.')


if __name__ == '__main__':
    main()
