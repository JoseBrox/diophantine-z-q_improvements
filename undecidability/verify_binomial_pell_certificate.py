#!/usr/bin/env python3
"""Exact checks for the independently proved n^6 binomial/Pell certificate.

The universal parameter statement is proved in the companion TeX document.
The finite examples below illustrate its formulas; they do not claim to
exhaust the possible existential witnesses or prove source universality.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import comb
from pathlib import Path

import sympy as sp

BASE = Path(__file__).resolve().parent


def pell(a: int, n: int) -> tuple[int, int]:
    """Exact binary powering in Z[sqrt(a^2-1)]."""
    d = a*a-1
    result = (1, 0)
    factor = (a, 1)
    while n:
        if n & 1:
            x, y = result
            u, v = factor
            result = (x*u+d*y*v, x*v+y*u)
        x, y = factor
        factor = (x*x+d*y*y, 2*x*y)
        n //= 2
    return result


def symbolic_checks() -> dict:
    r, s, w, n, M, Y, V = sp.symbols("r s w n M Y V")
    a = r*Y*(V+1)
    p = 2*r*r*Y*Y*V
    assert sp.expand(p.subs({Y:s*M, V:w*M})-2*w*s*s*r*r*M**3) == 0
    assert sp.expand(a.subs({Y:s*M, V:w*M})-(w*M+1)*r*s*M) == 0
    assert sp.expand(p.subs({Y:s*n*n, V:w*n*n})-2*w*s*s*r*r*n**6) == 0
    L = r*s*n*n
    U = w*n*n
    pnew = 2*U*L*L
    anew = (U+1)*L
    assert sp.expand(anew-U*L-L) == 0
    assert sp.expand(2*L*anew-pnew-2*L*L) == 0
    Lold = r*s
    pold = 2*U*Lold*Lold
    assert sp.expand(2*Lold*anew-(pold+2*Lold*Lold)*n*n) == 0
    assert sp.expand(pnew-pold*n**4) == 0
    return {
        "general_modulus_parameter": "2*w*s^2*r^2*M^3",
        "square_modulus_parameter": "2*w*s^2*r^2*n^6",
        "old_parameter_was_not_silently_modified": True,
        "old_and_new_quadratic_blocks": "six coordinates and six rows each; the new a=(U+1)L row is division-free",
        "identities": "PASS",
    }


def ratio_examples() -> dict:
    normalized = 0
    for a in range(2, 17):
        previous = Fraction(1)
        for t in range(2, 31):
            v = Fraction(pell(a, t)[1], (2*a)**(t-1))
            assert 1-Fraction(t-2, 4*a*a) <= v <= 1
            if t > 2:
                assert v < previous
            previous = v
            normalized += 1
    ratios = 0
    worst = Fraction(0)
    worst_parameters = None
    for r in range(1, 13):
        for Y in range(2, 10):
            for V in range(2, 10):
                a = r*Y*(V+1)
                p = 2*r*r*Y*Y*V
                c = pell(a, 2*r+1)[1]
                k = pell(p, r+1)[1]
                rho = Fraction((V+1)**(2*r), V**r)
                error = rho-Fraction(c, k)
                bound = rho/Fraction(Y*Y*V*V)
                assert 0 < error < bound
                ratio = error/bound
                if ratio > worst:
                    worst, worst_parameters = ratio, (r, Y, V)
                ratios += 1
    return {
        "scope": "finite exact illustrative examples, not the universal proof",
        "normalized_pell_examples": normalized,
        "ratio_examples": ratios,
        "largest_error_to_stated_bound_ratio": str(worst),
        "parameters_at_largest_ratio": worst_parameters,
    }


def binomial_examples() -> dict:
    cases = []
    max_bits = 0
    for r in range(1, 21):
        central = comb(2*r, r)
        for M in range(2, 33):
            if central % M:
                continue
            b = 2
            while b <= 2*M:
                assert 2**(2*r+1) % b == 0
                w = 2**(2*r+1)//b
                V = w*M
                Y = sum(comb(2*r, j)*V**(r-j) for j in range(r+1))
                assert Y % M == 0
                s = Y//M
                a, p = r*Y*(V+1), 2*r*r*Y*Y*V
                d, c = pell(a, 2*r+1)
                tau, k = pell(p, r+1)
                eta = k*k-4*(c-k*Y)**2
                assert eta > 0
                assert (k-r-1) % (p-1) == 0
                h = (k-r-1)//(p-1)
                assert h > 0
                numerator = d-(a-2)*c-b*w
                assert numerator % (4*a-5) == 0
                gamma = numerator//(4*a-5)
                assert gamma > 0 and c > 2*r+1
                assert d*d == (a*a-1)*c*c+1
                assert tau*tau == (p*p-1)*k*k+1
                rho = Fraction((V+1)**(2*r), V**r)
                theta = rho-Y
                error = rho-Fraction(c, k)
                assert 0 < theta < Fraction(b, 4*M) <= Fraction(1, 2)
                assert 0 < error < Fraction(5, 32)
                assert -Fraction(1, 2) < theta-error < Fraction(1, 2)
                max_bits = max(max_bits, c.bit_length(), k.bit_length(), eta.bit_length())
                if len(cases) < 8:
                    cases.append({"r":r, "M":M, "b":b, "w":w, "s":s,
                                  "a":a, "p":p, "c":c, "k":k,
                                  "eta":eta, "gamma":gamma})
                b *= 2
    # The smallest example also checks the enlarged range M < b <= 2M.
    case = next(c for c in cases if (c['r'],c['M'],c['b']) == (1,2,4))
    a, c = case['a'], case['c']
    B, d = 3, pell(a, 3)[0]
    q = B*c
    F, E = pell(a, q)
    assert E % (c*c) == 0
    i = E//(c*c)
    G = a+F*F*(c+1-a)
    I, H = pell(G, B)
    assert (H-B) % c == 0 and (I-d) % F == 0
    j, o = (H-B)//c, (I-d)//F
    assert all(v > 0 for v in (i,F,j,o))
    assert F*F == (a*a-1)*i*i*c**4+1
    assert (d+o*F)**2 == (G*G-1)*(B+j*c)**2+1
    return {
        "scope": "finite exact constructive examples; complete witnesses checked only for the stated small case",
        "parameter_range": "1<=r<=20, 2<=M<=32, M divides binomial(2r,r), b a power of two with b<=2M",
        "first_examples": cases,
        "largest_checked_local_integer_bit_length": max_bits,
        "expanded_three_pell_case": {"r":1,"M":2,"b":4,"a":a,"c":c,"q":q,
                                      "largest_witness_bit_length":max(v.bit_length() for v in (F,i,j,o,I,H))},
        "square_modulus_boundary": {"n":2,"r":1,"divisibility":False,
                                     "reason":"4 does not divide binomial(2,1)=2"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    certificate = {
        "theorem": "independently proved polynomial certificate for b=2^e and M|binomial(2r,r)",
        "hypotheses": "r>=1, M>=2, 2<=b<=2M; all listed witnesses positive integers",
        "source_universality_claim": False,
        "alleged_57_47_source_reproved": False,
        "proof": "undecidability/papers/binomial_pell_certificate.tex",
        "symbolic": symbolic_checks(),
        "ratio_examples": ratio_examples(),
        "binomial_examples": binomial_examples(),
        "status": "PASS",
    }
    if args.write:
        (BASE/'certificates'/'binomial_pell_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    else:
        # The diagnostic maximum records its arguments as a Python tuple;
        # JSON represents the same data as an array.
        assert json.loads(json.dumps(certificate)) == json.loads((BASE/'certificates'/'binomial_pell_certificate.json').read_text())
    print(json.dumps({"status":certificate['status'],
                      "normalized_examples":certificate['ratio_examples']['normalized_pell_examples'],
                      "ratio_examples":certificate['ratio_examples']['ratio_examples'],
                      "source_universality_claim":False},indent=2))


if __name__ == '__main__':
    main()
