#!/usr/bin/env python3
"""Exact expansion and finite residue certificates for the height-seven test.

The proof that this is optimal in the full integral linear-multiplier
family is in the companion TeX. The finite 16-case check here is applied
only after that proof reduces any hypothetical height <=6 example to it.
"""
from itertools import product
from functools import reduce
from math import gcd
from pathlib import Path
import hashlib
import json


def construct(a, b, c, e):
    A = [a*a+2*c*c, 2*a*b+4*c*e+4*a*c,
         b*b+2*e*e+4*a*e+4*b*c, 4*b*e]
    B = [2*a*c, a*a+2*c*c+2*a*e+2*b*c,
         2*a*b+4*c*e+2*b*e, b*b+2*e*e]
    terms = {(0, 0, 4): 2}
    for j, coefficient in enumerate(A):
        terms[(3-j, j, 2)] = -2*coefficient
    for j, x in enumerate(B):
        for k, y in enumerate(B):
            key = (6-j-k, j+k, 0)
            terms[key] = terms.get(key, 0)+x*y
    terms = {key: val for key, val in terms.items() if val}
    content = reduce(gcd, (abs(val) for val in terms.values()))
    assert content in (1, 2)
    assert (content == 2) == (a % 2 == b % 2 == 0)
    primitive = {key: val//content for key, val in terms.items()}
    return A, B, content, primitive


def main():
    A, B, content, G = construct(1, 1, -1, 0)
    assert A == [3, -2, -3, 0]
    assert B == [-2, 1, 2, 1]
    expected = {
        (0, 0, 4): 2, (3, 0, 2): -6, (2, 1, 2): 4,
        (1, 2, 2): 6, (6, 0, 0): 4, (5, 1, 0): -4,
        (4, 2, 0): -7, (2, 4, 0): 6, (1, 5, 0): 4,
        (0, 6, 0): 1,
    }
    assert G == expected
    assert content == 1 and max(map(abs, G.values())) == 7
    assert max(map(sum, G)) == 6 and len(G) == 10
    residues = [sum(B[j]*t**(3-j) for j in range(4)) % 3
                for t in range(3)]
    residues.append(B[0] % 3)
    assert residues == [1, 2, 2, 1]

    # Exhaust the mathematically proved finite reduction, not a bounded
    # empirical search over arbitrary multiplier coefficients.
    reduced_cases = []
    for a, c in product((-1, 1), repeat=2):
        for b, e in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            _, bc, cont, poly = construct(a, b, c, e)
            height = max(map(abs, poly.values()))
            assert cont == 1 and height >= 7
            reduced_cases.append({"a_b_c_e": [a, b, c, e],
                                  "B": bc, "height": height})
    assert len(reduced_cases) == 16
    assert min(case["height"] for case in reduced_cases) == 7

    path = Path(__file__).resolve()
    certificate = {
        "status": "PASS",
        "checker_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "variable_order": ["U", "V", "T"],
        "multiplier": {"a": 1, "b": 1, "c": -1, "e": 0},
        "A_coefficients_descending_U": A,
        "B_coefficients_descending_U": B,
        "G_terms": [{"exponents": key, "coefficient": G[key]} for key in sorted(G)],
        "degree": 6,
        "monomials": 10,
        "height": 7,
        "content": 1,
        "anisotropy_mod_3": {"projective_inputs": ["(0:1)", "(1:1)", "(2:1)", "(1:0)"], "nonzero_values": residues},
        "optimality_scope": "Integral linear multipliers m=(aU+bV)+(cU+eV)sqrt(2), primitive normalization of 2T^4-2AT^2+B^2.",
        "content_two_branch": "The primitive U^6 coefficient is 2*a^2*c^2 >=8, because a is nonzero even and c is nonzero.",
        "finite_reduction": reduced_cases,
        "scope_note": "The unconditional reduction of every hypothetical height<=6 member to these cases is proved in the companion TeX; this is not a claim of global coefficient optimality among all square predicates.",
    }
    dest = path.with_name("height7-linear-multiplier-certificate.json")
    dest.write_text(json.dumps(certificate, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "height": 7, "terms": 10,
                      "certificate": str(dest)}, indent=2))


if __name__ == "__main__":
    main()
