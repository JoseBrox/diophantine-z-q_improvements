#!/usr/bin/env python3
"""Independent identities and complete finite-field fibers for the seven-coordinate chart.

No source producer or coefficient table is imported.  The field calculations
use an independently implemented chord-and-tangent group law.
"""
from pathlib import Path
import argparse
import json

import sympy as sp


def identities():
    a, s, t, F, G, h, d, D, Q, z = sp.symbols("a s t F G h d D Q z")
    p = h + s + t
    rows = [a - h*p, d-p*F, D*(F+G)-(s-t)*h+t*t,
            d-G*h, Q-d*(s-t)+D*F*G]
    q1, q2, q3, q4, q5 = rows
    U = Q-D*F*F-s*s*F
    V = Q-D*G*G-t*t*G
    tests = {
        "first_curve": U-(q5+(s-t)*q2-F*q3),
        "second_curve": V-(q5+(s-t)*q4-G*q3),
        "line_at_first_translated_point":
            (h+t)*(-D*F)+D*d-D*s*F-D*q2,
        "line_at_negative_second_translated_point":
            (h+t)*(-D*G)+D*d+D*t*G-D*q4,
        "full_line_factorization":
            z**3-D*Q*z-((h+t)*z+D*d)**2
            -(z+D*F)*(z+D*G)*(z-a)
            -((q1-q3)*z*z
              +D*((F+G)*q1-h*q2-p*q4-q5)*z
              +D*D*(F*G*q1-h*G*q2-d*q4)),
        "regular_slope_overlap":
            (s+t)*F*(s-t)-(G-F)*(D*(F+G)+t*t)-(V-U),
    }
    for name, expr in tests.items():
        assert sp.expand(expr) == 0, name
    substitutions = {
        F: 0, G: 0, d: 0, Q: 0,
        h: t*t/(s-t), a: s*s*t*t/(s-t)**2,
    }
    for i, row in enumerate(rows):
        assert sp.cancel(row.subs(substitutions, simultaneous=True)) == 0, i
    assert all(sp.Poly(row, a, s, t, F, G, h, d, Q).total_degree() <= 2
               for row in rows)
    return {"identities": list(tests), "identity_count": len(tests),
            "zero_input_rows": 5, "all_rows_quadratic": True,
            "sympy_version": sp.__version__}


def inv(a, p):
    return pow(a % p, -1, p)


def add(P, Q, D, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    xx, yy = Q
    if x == xx and (y+yy) % p == 0:
        return None
    if x == xx:
        slope = (3*x*x-D)*inv(2*y, p) % p
    else:
        slope = (yy-y)*inv(xx-x, p) % p
    x3 = (slope*slope-x-xx) % p
    return x3, (slope*(x-x3)-y) % p


def finite_fields(primes):
    per_prime = []
    total = dict(coefficient_fibers=0, solutions=0, tangent_pairs=0,
                 zero_ordinate_pairs=0, zero_abscissa_torsion_differences=0,
                 nonzero_abscissa_torsion_differences=0)
    for prime in primes:
        p = prime
        local = dict.fromkeys(total, 0)
        for D in range(1, p):
            points = {(x, y) for x in range(1, p) for y in range(p)
                      if (y*y-x*x*x+D*x) % p == 0}
            expected = {(U, V) for U in points for V in points if U != V}
            seen = {}
            Di = inv(D, p)
            for F in range(p):
                for s in range(p):
                    for t in range(p):
                        for h in range(p):
                            G = (((s-t)*h-t*t)*Di-F) % p
                            if (h*G-(h+s+t)*F) % p:
                                continue
                            d = G*h % p
                            if (1-d*(s-t)+D*F*G) % p:
                                continue
                            a = h*(h+s+t) % p
                            assert F != 0 and G != 0
                            xU, xV = inv(F, p), inv(G, p)
                            U, V = (xU, s*xU % p), (xV, t*xV % p)
                            assert U in points and V in points and U != V
                            A = add(U, (V[0], -V[1] % p), D, p)
                            assert A is not None
                            assert A == (a, (-(h+t)*a-D*d) % p)
                            assert (U, V) not in seen
                            seen[U, V] = (a, s, t, F, G, h, d)
                            local['solutions'] += 1
                            local['tangent_pairs'] += F == G
                            local['zero_ordinate_pairs'] += (U[1] == 0 or V[1] == 0)
                            if A[1] == 0:
                                key = ('zero_abscissa_torsion_differences' if A[0] == 0
                                       else 'nonzero_abscissa_torsion_differences')
                                local[key] += 1
            assert set(seen) == expected, (p, D, expected-set(seen))
            local['coefficient_fibers'] += 1
        for key in total:
            total[key] += local[key]
        per_prime.append({'prime': p, **local})
    return {'primes': list(primes), 'totals': total, 'per_prime': per_prime,
            'scale': 'beta=1; nonzero beta follows by the proved weighted scaling'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--primes', type=int, nargs='+', default=[3, 5, 7, 11, 13, 17, 19])
    args = parser.parse_args()
    result = {'status': 'PASS',
              'scope': 'universal chart identities and all finite fibers at listed fields',
              'identities': identities(), 'finite_fields': finite_fields(args.primes),
              'full_arithmetic_source_certified_by_computation': False}
    serialized = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end='')
