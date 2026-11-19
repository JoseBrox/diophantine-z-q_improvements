#!/usr/bin/env python3
"""Independent exact audit of the paired-contact quartic in 56 variables.

No producer or checker is imported. The retained physical reconstruction,
native twist identities and valuation regression are explicitly inherited
from the v80 audit; the new contact map, two-adic duplication and complete
SymPy expansion are independently reconstructed here. Arithmetic proofs
and their retained assumptions are separated in proof_review56.md.
Default mode is read-only. --write intentionally creates the reviewed receipt.
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
DATA = HERE / 'quartic56'
PARENT = ROOT / 'computation/coauthor_audit_v78/work_abc/small_gate62/primitive/quadrics.json'
KEEP = [1, *range(3, 32), *range(36, 47), 59, 61, 62]
OLD = dict(zip(KEEP, range(1, 45), strict=True))
NEW_NAMES = 'M M2 a z T S P A1 A2 Fbar H alpha'.split()
NEW = dict(zip(NEW_NAMES, range(45, 57), strict=True))
SHIFTS = (8, 9, 12, 15, 17, 20, 23, 24)
RADII = (1, 4, 7, 8)
B = s.Symbol('B')
Z = (None, *s.symbols('z1:57'))

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
    # the valuation case split in proof_review56.md, not this loop.
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


def contact_formulas():
    T, S, P = s.symbols('T S P')
    factors = {r: P - 2 * r**2 * S + r**4 for r in RADII}
    A1, A2 = [s.expand(factors[r] * factors[t]) for r, t in ((1, 8), (4, 7))]
    H1, H2 = [s.expand(2*T*s.diff(A, P) + s.diff(A, S)) for A in (A1, A2)]
    equal(H2 - H1, 720*(-4*T + 8*S - 130))
    equal(A2 - A1, 720*(-2*P + 4*S**2 - 130*S + 848))
    assert 1**2 + 8**2 == 4**2 + 7**2 == 65
    a, z, t, M = s.symbols('a z t M')
    G = s.prod(t+r for r in SHIFTS)
    F = s.expand(G.subs(t, a-16-z) * G.subs(t, a-16+z))
    Phi = A1*A2
    substitution = {P: (a*a-z*z)**2, S: a*a+z*z, T: a*a-z*z}
    equal(F, Phi.subs(substitution))
    equal(s.diff(F, a), 2*a*(H1*A2+A1*H2).subs(substitution))
    assert len(set(SHIFTS)) == 8 and all(r > 0 for r in SHIFTS)
    assert all(r+t != 0 for r in SHIFTS for t in SHIFTS)
    assert SHIFTS == tuple(sorted([16+r for r in RADII]+[16-r for r in RADII]))
    # Translation of the midpoint leaves the original derivative exactly.
    equal(F.subs(a, M**4+16), G.subs(t, M**4-z)*G.subs(t, M**4+z))
    Fa = s.Poly(s.diff(F, a), z)
    assert s.Poly(F, z).degree() == 16 and s.Poly(F, z).LC() == 1
    assert Fa.degree() == 14 and Fa.LC() == -16*a
    equal(s.limit((-16*F/Fa.as_expr())*a/z**2, z, s.oo), 1)
    return (T, S, P), (A1, A2, H1), F


def new_rows(symbols, expressions):
    T, S, P = symbols
    n = {name: Z[i] for name, i in NEW.items()}
    A1, A2, H1 = [expr.subs({T:n['T'], S:n['S'], P:n['P']}) for expr in expressions]
    c, ci, d, tau, b = [Z[OLD[i]] for i in (61, 62, 59, 38, 39)]
    rows = {
        'single.alpha': n['alpha']-ci-d*d,
        'single.gate': tau*(1+n['alpha'])-n['alpha'],
        'single.poleInput': b-7*tau*tau,
        'height.M': n['M']-B-2*Z[OLD[31]]**2-8*Z[OLD[9]]**2,
        'height.M2': n['M2']-n['M']**2,
        'contact.center': n['a']-n['M2']**2-16,
        'contact.sum': n['S']+n['T']-2*n['a']**2,
        'contact.difference': n['S']-n['T']-2*n['z']**2,
        'contact.square': n['P']-n['T']**2,
        'contact.A1': n['A1']-A1,
        'contact.A2': n['A2']-A2,
        'contact.value': n['a']*n['Fbar']-n['A1']*n['A2'],
        'contact.partialCombined': n['H']-H1,
        'contact.derivativeQuotient': n['H']*(n['A1']+n['A2'])
             +720*(-4*n['T']+8*n['S']-130)*n['A1']+8*c*n['Fbar'],
    }
    assert len(rows) == 14
    return {k:s.expand(v) for k,v in rows.items()}


def physical_normalizer():
    c, u, D, tau, b, alpha = s.symbols('c u D tau b alpha', nonzero=True)
    Ds = D/c
    equal((1/c+Ds**2).subs(c, 1/u), u+u*u*D*D)
    equal((tau*(1+alpha)-alpha).subs(alpha, -1), 1)
    equal((7*c*tau**2).subs(c, 1/u), 7*tau**2/u)
    tau_c = s.cancel((c+D**2)/(c*c+c+D**2))
    E = s.Symbol('E')
    equal(tau_c.subs(D,c*c*E), (1+c**3*E**2)/(1+c+c**3*E**2))
    equal(tau_c.subs(D,0), 1/(1+c))
    return {'native_input':'b=7*c*tau^2=7*tau^2/u',
            'normalizer':'alpha=u+u^2*D^2; D=c*Ds; tau*(1+alpha)=alpha',
            'zero_D':'tau=1/(1+c), b=7*c/(1+c)^2',
            'fixed_place_asymptotic':'D=O(c^2), tau->1, b/(7*c)->1'}


def two_adic_exact_checks():
    # Exact arithmetic in Q(sqrt(2)); these identities supplement, rather
    # than replace, the formal logarithm and translation proof for all n.
    rho = s.sqrt(2)
    Delta = 11-6*rho
    x, y = 1+rho, 2*rho
    slope = s.simplify((3*x*x-Delta)/(2*y))
    x2 = s.simplify(slope*slope-2*x)
    y2 = s.simplify(slope*(x-x2)-y)
    equal(y*y, x**3-Delta*x)
    equal(slope, 3-rho/4)
    equal(x2, (57-28*rho)/8)
    equal(y2, (-660+417*rho)/32)
    equal(y2*y2, x2**3-Delta*x2)
    xi2 = s.simplify(-x2/y2)
    equal(xi2, (232+86*rho)/357)
    equal(4*(x2+x2.xreplace({rho:-rho})), 57)
    S0, T0 = (-348+129*rho)/164, 4-2*rho
    half_trace = s.simplify(T0*T0/(S0-T0))
    trace = s.simplify(half_trace+half_trace.xreplace({rho:-rho}))
    equal(trace, -s.Rational(37888,7199))
    equal(s.simplify((S0-T0)*(S0-T0).xreplace({rho:-rho})), s.Rational(7199,328))
    # Integral translation: the first visible coefficients involve no
    # inverse of 2*y(R0), even though R0 has singular special reduction.
    t = s.Symbol('t')
    xq = t**-2+Delta*t**2-Delta**2*t**6+2*Delta**3*t**10
    yq = -xq/t
    translated = s.series(((yq-y)/(xq-x))**2-xq-x,t,0,4).removeO()
    coefficients = [s.expand(translated).coeff(t,j).expand() for j in range(4)]
    equal(coefficients[0], x)
    for coefficient in coefficients:
        aa = s.simplify((coefficient+coefficient.xreplace({rho:-rho}))/2)
        bb = s.simplify((coefficient-coefficient.xreplace({rho:-rho}))/(2*rho))
        assert aa.is_Integer and bb.is_Integer
    assert all((m**4+16)%8==1 for m in (1,3,5,7))
    return {'double_R0':[str(x2),str(y2)], 'xi_double_R0':str(xi2),
            'four_times_trace_x_double_R0':'57',
            'zero_input_scaled_trace':'-37888/7199',
            'formal_translation_first_coefficients':[str(v) for v in coefficients],
            'uniform_statement_in_review':'n^2*Tr(x([n]R0)) in Z_2 for every nonzero integer n',
            'finite_checks_are_not_uniform_proof':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    spec, maps, claim = [read(DATA/name) for name in ('quadrics.json','maps.json','certificate.json')]
    assert spec['variables']==56 and spec['input']==1 and spec['parameter']=='B'
    assert maps['parent']==str(PARENT.relative_to(ROOT)) and maps['parent_sha256']==digest(PARENT)
    assert maps['old_to_new']=={str(k):v for k,v in OLD.items()}
    assert maps['new_coordinates']==NEW and maps['shifts']==list(SHIFTS)
    assert maps['center']==16 and maps['radii']==list(RADII) and maps['padding']==2
    assert maps['physical_scaling']=={
        'physical_pole_input_multiplier':7, 'unscaled_alpha':56,
        'c':43, 'c_inverse':44, 'unscaled_tau':33,
        'unscaled_height_coordinates':{k:NEW[k] for k in ('M','M2')},
        'unscaled_contact_coordinates':{k:NEW[k] for k in NEW_NAMES[2:-1]}}
    parent=read(PARENT)
    retained={r['name']:expression(r['terms'],lambda i:Z[OLD[i]])
              for r in parent['residuals'] if selected(r['name'])}
    assert len(retained)==32
    ratios=reconstruct_physical_parent(parent['residuals'])
    symbols, expressions, F=contact_formulas()
    expected=retained|new_rows(symbols,expressions)
    rows={r['name']:expression(r['terms'],lambda i:Z[i]) for r in spec['residuals']}
    assert len(rows)==len(spec['residuals'])==46 and set(rows)==set(expected)
    for name,value in rows.items():
        equal(value,expected[name])
        assert s.Poly(value,*Z[1:]).total_degree()<=2
    # A separate symbolic polynomial engine expands every coefficient.
    total=s.Poly(sum(v*v for v in rows.values()),B,*Z[1:])
    stored=s.Poly(expression(read(DATA/'polynomial.json')['terms'],lambda i:Z[i]),B,*Z[1:])
    assert total==stored
    profiles=defaultdict(dict)
    for exponents, coefficient in total.terms():
        profiles[exponents[1:]][exponents[0]]=int(coefficient)
    assert len(profiles)==809 and len(total.terms())==812
    assert max(map(sum,profiles))==4
    assert {i+1 for exponents in profiles for i,e in enumerate(exponents) if e}==set(range(1,57))
    assert reduce(gcd,map(int,total.coeffs()))==1
    assert profiles[(4,)+(0,)*55]=={0:1}
    fixedmax=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
    assert fixedmax==125368156160
    mixed=[]
    for exponents,profile in profiles.items():
        if len(profile)>1:
            mixed.append({'monomial':[i+1 for i,e in enumerate(exponents) for _ in range(e)],
                          'coefficients':{str(i):a for i,a in sorted(profile.items())}})
    mixed.sort(key=lambda p:p['monomial'])
    assert mixed==sorted(claim['mixed_profiles'],key=lambda p:p['monomial'])
    assert {tuple(sorted(p.items())) for p in profiles.values() if len(p)>1}=={
        ((0,377888002299),(2,1)),((0,1),(1,16)),((0,1),(1,4))}
    caps={e:max((abs(p[e]) for p in profiles.values() if set(p)=={e}),default=0) for e in (1,2)}
    assert caps=={1:2,2:0}
    # Complete the square to prove the height for every positive B.
    assert 377888002299>fixedmax
    for linear in (2,4,16):
        constant=1 if linear in (4,16) else 0
        equal(B*B+377888002299-(linear*B+constant),
              (B-s.Rational(linear,2))**2+377888002299-constant-s.Rational(linear*linear,4))
        assert 377888002299-constant-s.Rational(linear*linear,4)>0
    for k,v in {'variables':56,'quadrics':46,'degree':4,'content':1,'monomials':809,
                'parameter_separated_terms':812,'maximum_fixed_coefficient':fixedmax}.items():
        assert claim[k]==v
    arithmetic=valuation_and_height_checks()
    for key in ('radical_height_rate','input_height_rate','strict_margin'):
        assert claim['height_parameters'][key]==arithmetic[key]
    report={
        'schema':'ordinary-abc-quartic56-independent/v81','status':'PASS',
        'method':'Independent contact reconstruction and SymPy expansion; explicitly retained v80 physical/twist routines; no producer or checker import',
        'variables':56,'quadrics':46,'retained_parent_rows':32,'new_or_rederived_rows':14,
        'contact_coordinates':9,'degree':4,'content':1,'coordinate_monomials':809,
        'parameter_separated_terms':812,'exact_height_for_positive_integer_B':'B^2+377888002299',
        'physical_parent_row_multipliers':ratios,'mixed_profiles':mixed,
        'contact_identities':{'radii':list(RADII),'shifts':list(SHIFTS),
            'paired_derivative_difference':'H2-H1=720*(-4*T+8*S-130)',
            'derivative':'F_a=2*a*(H1*A2+A1*H2)',
            'quotient':'F_a+16*c*F=0','only_new_divisor':'a=M^4+16>0',
            'degree_F_in_z':16,'leading_F':'1','degree_Fa_in_z':14,'leading_Fa':'-16*a'},
        'normalizer':physical_normalizer(),'two_adic_exact_checks':two_adic_exact_checks(),
        'native_twist_identities':native_twist_identities(),'height_and_regression':arithmetic,
        'scope':{'exact_computation':'All 46 quadrics, complete expansion, coordinate map, paired contact identities, duplication and zero fiber, native twist identities and stated constants',
            'proof_review':'Universal valuation, two-adic trace, height and actual-input completeness proofs in proof_review56.md',
            'not_certified_by_computation':'Retained elliptic/formal/trace/prime-pattern inputs, rational abc, published Burungale theorem, and no effective sufficient B'},
        'input_sha256':{str(path.relative_to(ROOT)):digest(path) for path in
            [PARENT,*[DATA/name for name in ('quadrics.json','polynomial.json','maps.json','certificate.json')]]}}
    target=HERE/'independent56.json'
    if args.write:
        target.write_text(json.dumps(report,indent=2)+'\n')
    else:
        assert read(target)==report,'Independent certificate differs; review before --write'
    print('PASS: 56 variables, 46 quadrics, full physical/contact/coefficient audit; arithmetic scope explicit.')


if __name__=='__main__':
    main()


