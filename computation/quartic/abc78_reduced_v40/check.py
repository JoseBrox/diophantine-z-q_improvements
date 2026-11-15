#!/usr/bin/env python3
"""Independent algebraic and coefficient verification of abc78_reduced_v40.

The checker does not import the producer. SymPy verifies exact identities and
expands each rational row. No floating point or sampled rational witnesses are
used to establish the polynomial assertions.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'abc78_v34'
HASH = 'ceffdf6e0a38ac1c8c42812f5e7bef599231dc5bc4b5f7c4527303b81dfc11bb'
POLYNOMIAL_HASH = '697f23d5c788fa7d4b9e543444b8dbd22d9e9261b1dad9156d4f51293816eefc'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def check_identities():
    f, h, g, k, s, D, F, G, L, M, S, T = sp.symbols('f h g k s D F G L M S T')
    first = h * L + f * S
    second = (1 - D * F) * L + h * S
    other_first = k * M + g * T
    other_second = (1 - D * G) * M + k * T
    cu = h**2 - f + D * f**3
    cv = k**2 - g + D * g**3
    secant = s * (f - g) - h - k
    tangent = s * (h - k) - 1 + D * (F + f * g + G)
    identities = [
        h * second - (1 - D * F) * first - S * cu - D * f * S * (F - f**2),
        k * other_second - (1 - D * G) * other_first - T * cv - D * g * T * (G - g**2),
        cv - cu + (f - g) * tangent - (h - k) * secant
            - D * (f - g) * (F - f**2 + G - g**2),
    ]
    require(all(sp.expand(p) == 0 for p in identities), 'Universal implication identities')
    v = sp.Symbol('v', nonzero=True)
    old_rows = [F - f**2, G - g**2,
                s * (f - g) - h - k,
                s * (h - k) - 1 + D * (F + f * g + G),
                first, second, other_first, other_second,
                h**2 - f + D * f * F]
    new_rows = [v * F - f**2, v * G - g**2,
                s * (f - g) - v * (h + k),
                s * (h - k) - v**2 + D * (v * F + f * g + v * G),
                h * L + f * S, (v - D * F) * L + h * S,
                k * M + g * T, (v - D * G) * M + k * T,
                h**2 - v * f + D * f * F]
    substitution = {x: x / v for x in (f, h, g, k, s, F, G)}
    clearing = [2, 2, 2, 2, 1, 1, 1, 1, 2]
    for old, new, exponent in zip(old_rows, new_rows, clearing):
        require(sp.expand(v**exponent * old.subs(substitution, simultaneous=True) - new) == 0,
                'Uniform rescaling identity')
    # The regular ratio row cannot be dropped at an identity numerator point:
    # the raw row alone leaves L unrestricted there.
    bad = {f: 0, h: 0, F: 0, L: 1, S: 1, D: 1}
    require(first.subs(bad) == 0 and second.subs(bad) != 0,
            'Identity-point corruption control')
    # At the fixed reference P=(a,b), b is nonzero without a rank premise.
    bnorm = Fraction(-165, 8)**2 - 2 * Fraction(417, 32)**2
    require(bnorm != 0, 'Fixed translation is not two-torsion')
    return str(bnorm)


def parse(terms):
    result = {}
    for t in terms:
        key = t['parameterPower'], tuple(t['monomial'])
        require(key not in result, 'No duplicate terms')
        result[key] = int(t['coefficient'])
    return result


def main(output):
    source = PARENT / 'quadratic-family.json'
    require(sha256(source.read_bytes()).hexdigest() == HASH, 'Pinned source')
    old = json.loads(source.read_text())
    new = json.loads((HERE / 'quadratic-family.json').read_text())
    final = json.loads((HERE / 'polynomial-family.json').read_text())
    report = json.loads((HERE / 'construction-report.json').read_text())
    removed = {'pair.cubic.0', 'pair.cubic.1'}
    expected = [r for r in old['residuals'] if r['name'] not in removed]
    require(len(expected) == len(new['residuals']) == 68, 'Exactly two rows deleted')
    require(old['coordinates'] == new['coordinates'] == final['coordinates'], 'Unchanged coordinates')
    require(old['fixedParameter'] == new['fixedParameter'] == final['fixedParameter'], 'Unchanged parameter')
    for i, (a, b) in enumerate(zip(expected, new['residuals']), 1):
        require(a['name'] == b['name'] and a['terms'] == b['terms'] and
                a['id'] == b['sourceId'] and b['id'] == i, 'Every retained row is literal')
        coeffs = [int(t['coefficient']) for t in b['terms']]
        require(sp.igcd(*coeffs) == 1, 'Primitive source row')
    bnorm = check_identities()
    B = sp.Symbol('B')
    variables = sp.symbols('x1:79')
    result = defaultdict(int)
    for row in new['residuals']:
        used_ids = sorted({i for t in row['terms'] for i in t['monomial']})
        used = [variables[i - 1] for i in used_ids]
        expression = sum(sp.Integer(t['coefficient']) * B**t['parameterPower'] *
                         sp.prod(variables[i - 1] for i in t['monomial']) for t in row['terms'])
        require(max(len(t['monomial']) for t in row['terms']) <= 2, 'Quadratic rows')
        poly = sp.Poly(expression**2, B, *used, domain=sp.ZZ)
        for powers, coefficient in poly.terms():
            monomial = tuple(i for i, exponent in zip(used_ids, powers[1:]) for _ in range(exponent))
            result[powers[0], monomial] += int(coefficient)
    result = {k: c for k, c in result.items() if c}
    require(result == parse(final['terms']), 'Independent expansion matches full quartic')
    require(max(len(m) for _, m in result) == 4 and result[0, (1, 1, 1, 1)] == 1,
            'Exact degree and primitive content for all B')
    require({i for _, m in result for i in m} == set(range(1, 79)), 'All 78 coordinates occur')
    parent_polynomial = PARENT / 'polynomial-family.json'
    require(sha256(parent_polynomial.read_bytes()).hexdigest() == POLYNOMIAL_HASH,
            'Pinned parent coefficient table')
    oldpoly = parse(json.loads(parent_polynomial.read_text())['terms'])
    profiles, oldprofiles = defaultdict(dict), defaultdict(dict)
    for (j, m), c in result.items():
        profiles[m][j] = c
    for (j, m), c in oldpoly.items():
        oldprofiles[m][j] = c
    require(len(profiles) == 1113 and len(oldprofiles) == 1143, 'Exact monomial counts')
    dynamic = {m for m, p in oldprofiles.items() if any(j for j in p)}
    require(all(profiles[m] == oldprofiles[m] for m in dynamic), 'All parameter profiles unchanged')
    require(all(set(p) == {0} or m in dynamic for m, p in profiles.items()), 'No new parameter profiles')
    for m in dynamic:
        p = profiles[m]
        require(all(c >= 0 for c in p.values()) or all(c <= 0 for c in p.values()),
                'Dynamic coefficient never vanishes at positive B')
    fixedmax = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    C0 = profiles[()][0]
    require(profiles[()] == {0: C0, 2: 1}, 'Positive constant coefficient')
    require(fixedmax == int(report['largestFixedCoefficient']) and
            C0 == int(report['constantCoefficient']), 'Published constants')
    require(fixedmax == max(abs(p[0]) for p in oldprofiles.values() if set(p) == {0}),
            'Largest fixed coefficient unchanged')
    # Certify the height bound for every B>=1, without a finite numerical sweep:
    # each nonconstant, nonconstant-monomial profile has |c0+c1 B| <= C0+B²,
    # or <= fixedmax while that upper envelope is smaller.
    switch = int(sp.integer_nthroot(max(0, fixedmax - C0), 2)[0]) + 1
    for m in dynamic - {()}:
        p = profiles[m]
        require(set(p) <= {0, 1}, 'Only the constant monomial has B²')
        a, c = abs(p.get(1, 0)), abs(p.get(0, 0))
        require(a * (switch - 1) + c <= fixedmax, 'Linear profiles below height switch')
        require(switch**2 + C0 >= a * switch + c and 2 * switch >= a,
                'Linear profiles above height switch')
    receipt = dict(schema='abc78-reduced-independent-verification/v40', passed=True,
                   sourceQuadraticSha256=HASH, variables=78, quadraticRows=68,
                   degree=4, integerContentForEveryPositiveB=1,
                   ordinaryMonomialsForEveryPositiveB=1113,
                   universalPolynomialIdentities=3, uniformRescalingIdentities=9,
                   fixedTranslationOrdinateNorm=bnorm,
                   exactHeight=report['exactHeight'],
                   scope='Universal curve-row implication identities, exact source preservation, independent expansion and coefficient bounds. The reference-chart theorem and all arithmetic premises retain their stated scopes.')
    output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'independent-verification.json')
    main(parser.parse_args().output)
