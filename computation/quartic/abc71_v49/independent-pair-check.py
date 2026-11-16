#!/usr/bin/env python3
"""Independent exhaustive check of the six-coordinate pair's finite fibers.

For nonzero beta, scaling reduces to beta=1. The field coefficient D
is allowed to vary. This checker enumerates all a,c with a(a-c*c)!=0
and all possible s,v, solves the first chart equation for t, and
compares the complete solution set with an independent elliptic group
implementation. It includes c=0. These finite checks supplement the
characteristic-zero proof; they do not prove the arithmetic source.
"""
from pathlib import Path
import argparse
import json


def inv(x, p):
    return pow(x % p, -1, p)


def add(P, Q, D, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    u, z = Q
    if x == u and (y + z) % p == 0:
        return None
    slope = ((z-y) * inv(u-x, p) if x != u
             else (3*x*x-D) * inv(2*y, p)) % p
    xx = (slope*slope-x-u) % p
    return xx, (slope*(x-xx)-y) % p


def neg(P, p):
    return None if P is None else (P[0], -P[1] % p)


def run(primes=(3, 5, 7, 11, 13, 17, 19)):
    totals = dict(coefficient_fibers=0, chart_solutions=0,
                  c_zero_fibers=0, c_zero_solutions=0,
                  tangent_numerators=0, two_torsion_numerators=0)
    per_prime = []
    for p in primes:
        points = {
            D: {(x, y) for x in range(p) for y in range(p)
                if (y*y-x*x*x+D*x) % p == 0}
            for D in range(1, p)
        }
        local = dict.fromkeys(totals, 0)
        for a in range(1, p):
            for c in range(p):
                delta = (a-c*c) % p
                if delta == 0:
                    continue
                D = a*delta % p
                A = (a, a*c % p)
                excluded = {(0, 0), A, add(A, (0, 0), D, p)}
                expected = points[D] - excluded
                seen = {}
                for s in range(p):
                    for v in range(1, p):
                        t = (s-v-delta*inv(v, p)) % p
                        if (s*t+c*(t-s)+2*c*v+2*delta) % p:
                            continue
                        Ulin = (v-s-c) % p
                        Wlin = (v+t-c) % p
                        chord = (v+t-s) % p
                        assert Ulin*Wlin % p == a
                        assert v*chord % p == -delta % p
                        assert Ulin and Wlin and chord
                        xu, xv = v*Wlin % p, v*Ulin % p
                        U, V = (xu, s*xu % p), (xv, t*xv % p)
                        assert U in points[D] and V in points[D]
                        assert xu and xv
                        assert add(U, neg(V, p), D, p) == A
                        assert U in expected
                        assert U not in seen
                        F = -Ulin*chord*inv(D, p) % p
                        G = -Wlin*chord*inv(D, p) % p
                        assert F*xu % p == G*xv % p == 1
                        if c == 0:
                            assert xu != a and xv != a
                            local['c_zero_solutions'] += 1
                        if U == neg(V, p):
                            local['tangent_numerators'] += 1
                        if U[1] == 0 or V[1] == 0:
                            local['two_torsion_numerators'] += 1
                        seen[U] = (s, t, v)
                assert set(seen) == expected, (p, a, c, expected-set(seen))
                local['coefficient_fibers'] += 1
                local['chart_solutions'] += len(seen)
                local['c_zero_fibers'] += (c == 0)
        for key in totals:
            totals[key] += local[key]
        per_prime.append({'prime': p, **local})
    return {
        'status': 'PASS',
        'scope': 'Complete finite pair fibers, including c=0; beta!=0 by scaling',
        'characteristic_zero_argument':
            'papers/quartic_existence/quartic_abc71_20261116_v49.tex, varying-difference chart proposition',
        'full_source_or_variable_record_proved_by_this_check': False,
        'primes': list(primes), 'totals': totals, 'per_prime': per_prime,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        help='write the deterministic certificate to this path')
    args = parser.parse_args()
    result = run()
    serialized = json.dumps(result, indent=2)+'\n'
    if args.output is not None:
        args.output.write_text(serialized)
    print(serialized, end='')
