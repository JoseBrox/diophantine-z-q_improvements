#!/usr/bin/env python3
"""Exact identities and finite certificates for the six-factor product paper.

Only the Python standard library is used. The real-density argument is proved
in the paper; the finite checks certify its elliptic curve and non-torsion input.
"""
from fractions import Fraction as Q
from itertools import permutations
from math import gcd, lcm
from pathlib import Path
import argparse
import json

CONTACTS = (Q(0), Q(-1, 2), Q(-1, 4), Q(-2, 5), Q(-1), Q(-1, 3))


def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def add(p, q):
    z = [Q(0)] * max(len(p), len(q))
    for i, a in enumerate(p):
        z[i] += a
    for i, a in enumerate(q):
        z[i] += a
    return trim(z)


def scale(p, a):
    return trim([a*x for x in p])


def mul(p, q):
    z = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            z[i+j] += a*b
    return trim(z)


def power(p, n):
    z = [Q(1)]
    for _ in range(n):
        z = mul(z, p)
    return z


def product(polys):
    z = [Q(1)]
    for p in polys:
        z = mul(z, p)
    return z


def evaluate(p, t):
    z = Q(0)
    for c in reversed(p):
        z = z*t+c
    return z


def fh(n, d):
    return product(add(n, scale(d, -theta)) for theta in CONTACTS)


F = fh([0, 1], [1])


def f(t):
    return evaluate(F, t)


def r(t):
    return f(t)/(t-1)**8


def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def canonical(v):
    den = lcm(*(a.denominator for a in v))
    v = [int(a*den) for a in v]
    common = gcd(*v)
    v = [a//common for a in v]
    if next(a for a in v if a) < 0:
        v = [-a for a in v]
    return tuple(v)


def map_triple(src, dst):
    rows = [[x, Q(1), -y*x, -y] for x, y in zip(src, dst)]
    v = [(-1)**j * det3([[row[k] for k in range(4) if k != j]
                         for row in rows]) for j in range(4)]
    return canonical(v)


def mobius(m, t):
    a, b, c, d = m
    return (a*t+b)/(c*t+d) if c*t+d else None


def curve_value(x):
    return (x-105)*(x+70)*(x+84)


def curve_add_mod(p, q, prime):
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    u, v = q
    if x == u and (y+v) % prime == 0:
        return None
    if p == q:
        slope = (3*x*x+98*x-10290)*pow(2*y, -1, prime) % prime
    else:
        slope = (v-y)*pow(u-x, -1, prime) % prime
    xx = (slope*slope-49-x-u) % prime
    return (xx, (slope*(x-xx)-y) % prime)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('product-height-obstructions-v19-certificate.json'))
    args = parser.parse_args()
    # Complete formal identities for the two contact involutions.
    assert fh([0, -1], [1, 5]) == scale(F, -1)
    assert fh([1, 1], [-1, 2]) == scale(F, 27)
    # The explicit rational square root in the scale parameter a.
    n, d = [-1, -1], [0, 5]
    qnum = mul(mul(fh(n, d), add(scale(n, 5), d)), d)
    qden = mul(power(add(n, scale(d, -1)), 4),
               power(add(scale(n, 6), d), 4))
    stated_num = scale(product(([0, 1], [-4, 1], [-1, 1], [1, 1],
                                 [-3, 2], [-2, 3], [-1, 4])), 25)
    stated_den = scale(mul(power([6, 1], 4), power([1, 6], 4)), 24)
    assert mul(qnum, stated_den) == mul(stated_num, qden)
    # Exhaust the 120 possible images of three fixed branch points.
    automorphisms = []
    seen = set()
    for dst in permutations(CONTACTS, 3):
        m = map_triple(CONTACTS[:3], dst)
        if {mobius(m, t) for t in CONTACTS} != set(CONTACTS):
            continue
        assert m not in seen
        seen.add(m)
        a, b, c, d = m
        ff = fh([b, a], [d, c])
        index = next(i for i, coefficient in enumerate(F) if coefficient)
        multiplier = ff[index]/F[index]
        assert ff == scale(F, multiplier)
        positive = 'all t>0' if m == (1, 0, 0, 1) else 't>1/2' if m == (1, 1, 2, -1) else 'none'
        if positive == 'none':
            assert a > 0 and b >= 0 and c < 0 and d < 0
        automorphisms.append({'matrix': list(m), 'multiplier': str(multiplier),
                              'contact_permutation': [CONTACTS.index(mobius(m, t)) for t in CONTACTS],
                              'positive_domain': positive})
    assert len(automorphisms) == 12
    automorphisms.sort(key=lambda item: item['matrix'])
    # Positive norm-family specializations check the complete R identity.
    for m in range(2, 102):
        lam, mu = Q(m*m+1, 2*m*m), Q(3*m*m+1, 2)
        assert mu/lam > 4 and lam > 0 and mu > 0
        assert lam == Q(m+1, 2*m)**2+Q(m-1, 2*m)**2
        q = 3*f(lam)*(2*lam-1)/((lam-1)**4*(lam-2)**4)
        assert r(lam)*r(mu) == 3*q*q
    # Elliptic residual identity: clear the sixth-power denominator first.
    h = product(([-1, 2], [1, 3], [2, 5]))
    j = product(([0, 1], [1, 1], [1, 2], [1, 4]))
    assert scale(mul(F, fh([1], [-2, 2])), 3600) == mul(power(j, 2), h)
    e_at_210t = product(([-105, 210], [70, 210], [84, 210]))
    assert e_at_210t == scale(h, 308700)
    assert Q(1470)**2 == 7*308700
    x, y = Q(210), Q(2940)
    assert y*y == curve_value(x)
    slope = (3*x*x+98*x-10290)/(2*y)
    x2 = slope*slope-49-2*x
    assert slope == Q(97, 4) and x2 == Q(1905, 16)
    assert 9*x2+147 == Q(19497, 16)
    finite_data = []
    for prime in (11, 13):
        assert len({105 % prime, -70 % prime, -84 % prime}) == 3
        points = [(u, v) for u in range(prime) for v in range(prime)
                  if (v*v-curve_value(u)) % prime == 0]
        pp = (210 % prime, 2940 % prime)
        q = None
        sequence = []
        for k in range(1, len(points)+2):
            q = curve_add_mod(q, pp, prime)
            sequence.append(list(q) if q is not None else None)
            if q is None:
                break
        finite_data.append({'prime': prime, 'point_count': len(points)+1,
                            'point_order': k, 'multiples': sequence})
    assert [(d['point_count'], d['point_order']) for d in finite_data] == [(8, 4), (20, 10)]
    # A torsion P would have order divisible by5 after reduction at13;
    # rational5-torsion injects at the good prime11, whose group has order8.
    report = {
        'status': 'PASS',
        'scope': 'Exact polynomial identities, complete rational contact-automorphism enumeration, and finite elliptic non-torsion certificate. Density and domain conclusions are proved in the paper.',
        'contacts': list(map(str, CONTACTS)),
        'universal_scale_domain': 'every rational a>4',
        'universal_slope': '-(a+1)/(5a)',
        'universal_product_squareclass': '-1',
        'automorphism_candidates': 120,
        'automorphisms': automorphisms,
        'positive_norm_family_checks': 100,
        'positive_norm_product_squareclass': '3',
        'elliptic_residual_identity': '3600 F(t) F_h(1,2t-2) = [t(t+1)(2t+1)(4t+1)]^2 (2t-1)(3t+1)(5t+2)',
        'elliptic_curve': 'Y^2=(X-105)(X+70)(X+84)',
        'elliptic_point': [210, 2940],
        'double_x': str(x2),
        'short_model_double_x': str(9*x2+147),
        'finite_reductions': finite_data,
        'elliptic_product_squareclass': '7',
        'limitations': 'No full Diophantine-source false witness is asserted. The positive families are not asserted to have the prescribed eighth-power scale; the elliptic family is not asserted to have lambda-1 a Gaussian norm.'
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('status', 'automorphism_candidates',
          'positive_norm_family_checks', 'elliptic_curve', 'finite_reductions')}))


if __name__ == '__main__':
    main()
