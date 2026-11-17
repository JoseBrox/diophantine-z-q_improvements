#!/usr/bin/env python3
"""Exact arithmetic checks supporting the Sun-v2 audit and power-shift theorem.

The finite computations verify the fixed algebraic identities, a reproducible
split-prime/CRT avoidance instance in Q(sqrt(2)), and four-contact examples.
They do not prove the prime-pattern, pole-realization, or height suppliers.
No producer or precomputed polynomial table is imported.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path

import sympy as sp


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def pair_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def pair_neg(x):
    return -x[0], -x[1]


def pair_mul(x, y):
    return x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def pair_scale(c, x):
    return c * x[0], c * x[1]


def pair_div(x, y):
    den = y[0] ** 2 - 2 * y[1] ** 2
    require(den != 0, "nonzero quadratic denominator")
    return pair_scale(1 / den, pair_mul(x, (y[0], -y[1])))


def fixed_curve():
    zero = (F(0), F(0))
    d = (F(3), F(-1))
    D = pair_mul(d, d)
    P = ((F(57, 8), F(-7, 2)), (F(-165, 8), F(417, 32)))
    R = ((F(1), F(1)), (F(0), F(2)))
    for label, point in (("P", P), ("R0", R)):
        x, y = point
        residual = pair_add(pair_mul(y, y), pair_neg(pair_add(pair_mul(pair_mul(x, x), x), pair_neg(pair_mul(D, x)))))
        require(residual == zero, "curve point " + label)
    x, y = R
    lam = pair_div(pair_add(pair_scale(F(3), pair_mul(x, x)), pair_neg(D)), pair_scale(F(2), y))
    xd = pair_add(pair_mul(lam, lam), pair_scale(F(-2), x))
    yd = pair_add(pair_mul(lam, pair_add(x, pair_neg(xd))), pair_neg(y))
    require((xd, yd) == P, "2R0=P")
    return {"D": [str(c) for c in D], "points_checked": ["P", "R0"], "doubling": "2R0=P"}


def symbolic_checks():
    u, v, a, f0, f1, y1, D, z = sp.symbols("u v a f0 f1 y1 D z")
    rho = sp.Symbol("rho")
    expression = sp.rem((u + v * rho) ** 3 - (11 - 6 * rho) * (u + v * rho), rho ** 2 - 2, rho)
    require(sp.expand(expression.coeff(rho, 0) - (u**3 + 6*u*v*v - 11*u + 12*v)) == 0, "ordinate F0")
    require(sp.expand(expression.coeff(rho, 1) - (3*u*u*v + 2*v**3 - 11*v + 6*u)) == 0, "ordinate F1")
    result = sp.resultant(a*a + 2*y1*y1 - f0, 2*a*y1 - f1, y1)
    quartic = a**4 - f0*a*a + f1*f1/2
    require(sp.expand(result - 4*quartic) == 0, "ordinate resultant")
    disc = sp.factor(sp.discriminant(quartic, a))
    require(sp.expand(disc - 8*f1*f1*(f0*f0-2*f1*f1)**2) == 0, "ordinate quartic discriminant")
    # In z=-x/y, x=(1+sqrt(1+4Dz^4))/(2z^2), y=-x/z.
    x = (1 + sp.sqrt(1 + 4*D*z**4))/(2*z**2)
    omega = sp.diff(x, z)/(-2*x/z)
    require(sp.simplify(omega - 1/sp.sqrt(1+4*D*z**4)) == 0, "invariant differential")
    formal = sum((-1)**j * sp.binomial(2*j, j) * D**j * z**(4*j+1)/sp.Integer(4*j+1) for j in range(16))
    require(sp.expand(sp.diff(formal, z) - sp.series(1/sp.sqrt(1+4*D*z**4), z, 0, 64).removeO()) == 0, "formal logarithm through degree 63")
    return {"ordinate_quartic_discriminant": str(disc), "formal_log_terms": 16, "formal_log_degree": 61, "derivative_precision": 64}


def contacts():
    # Homogeneous evaluation includes the contact at infinity.
    points = [(0, 1), (13, 1), (525, 1), (637, 1), (650, 1)]
    images = []
    for x, y in points:
        num, den = 49*x - 31213*y, x - 13*y
        images.append("infinity" if den == 0 else str(F(num, den)))
    require(images == ["2401", "infinity", "-343/32", "0", "1"], "Burungale-to-Sun contact map")
    finite = [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]
    pulled = ["infinity" if t == 0 else str(2 + 1/t) for t in finite]
    require(pulled == ["infinity", "0", "1", "2401", "-343/32"], "finite contact pullback")
    require(F(3) not in finite, "normalizer is not a contact")
    return {"first_map_images": images, "finite_contacts": [str(x) for x in finite], "second_map_images": pulled}


def crt_pair(a, mod, b, prime):
    require(gcd(mod, prime) == 1, "coprime CRT moduli")
    return (a + mod * ((b-a) * pow(mod, -1, prime) % prime)) % (mod*prime), mod*prime


def residue(x, prime):
    return (x.numerator * pow(x.denominator, -1, prime)) % prime


def avoidance_example(exponent):
    # Algebraic values a+b sqrt(2); primes split in Q(sqrt(2),mu_m).
    values = [(F(-3, 2), F(0)), (F(0), F(1)), (F(1), F(1)), (F(5, 7), F(-2, 7))]
    modulus, shift, used = 12, 5, set()
    local = []
    for ca, cb in values:
        prime = 2
        while True:
            if (sp.isprime(prime) and prime not in used and gcd(prime, 12*exponent*ca.denominator*cb.denominator) == 1 and (prime-1) % exponent == 0):
                roots = [r for r in range(prime) if r*r % prime == 2 % prime]
                if roots:
                    break
            prime += 1
        used.add(prime)
        r = roots[0]
        powers = {pow(x, exponent, prime) for x in range(prime)}
        nonpower = next(x for x in range(1, prime) if x not in powers)
        alpha = (residue(ca, prime) + r*residue(cb, prime)) % prime
        target = (alpha-nonpower) % prime
        shift, modulus = crt_pair(shift, modulus, target, prime)
        local.append({"alpha": [str(ca), str(cb)], "prime": prime, "sqrt2_residue": r, "alpha_residue": alpha, "shift_residue": target, "nonpower_unit": nonpower})
    require(shift % 12 == 5, "original shift progression preserved")
    for record in local:
        prime = record["prime"]
        require(shift % prime == record["shift_residue"], "CRT local condition")
        require(all((pow(x, exponent, prime)+shift-record["alpha_residue"]) % prime for x in range(prime)), "no local power-shift root")
    return {"exponent": exponent, "initial_progression": [5, 12], "refined_progression": [shift, modulus], "local_certificates": local}


def rational_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    u, v = Q
    if x == u and y == -v:
        return None
    lam = (3*x*x-25)/(2*y) if P == Q else (v-y)/(u-x)
    r = lam*lam-x-u
    return r, lam*(x-r)-y


def four_contact_examples():
    P = (F(25, 4), F(75, 8))
    require(P[1]**2 == P[0]**3-25*P[0], "congruent-number point")
    Q, out = None, []
    for n in range(1, 7):
        Q = rational_add(Q, P)
        require(Q is not None, "nonidentity sampled multiple")
        x, y = Q
        a = x/5
        u, v = a.numerator, a.denominator
        G = u*v*(u-v)*(u+v)
        require(G > 0 and G % 5 == 0, "positive integral contact product")
        r = isqrt(G//5)
        require(G == 5*r*r, "four-contact square class 5")
        require(F(G) == 5*(v*v*y/25)**2, "homogeneous four-contact identity")
        out.append({"n": n, "a": str(a), "square_root_of_G_over_5": str(r), "height_max_num_den": str(max(abs(u), v))})
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manuscript", type=Path, default=None,
                        help="Optional path to the companion TeX after repository integration.")
    args = parser.parse_args()
    certificate = {
        "status": "PASS",
        "scope": "Exact fixed identities, finite local avoidance examples, and four-contact arithmetic examples; no proof of imported global arithmetic premises.",
        "curve": fixed_curve(),
        "algebra": symbolic_checks(),
        "contacts": contacts(),
        "power_shift_examples": [avoidance_example(m) for m in (2, 3, 5)],
        "four_contact_boundary_examples": four_contact_examples(),
    }
    base = Path(__file__).resolve().parent
    manuscript = args.manuscript or base/"power_shifts_and_finite_exceptions_20261117_v69.tex"
    certificate["source_sha256"] = {
        "check.py": sha256(Path(__file__).read_bytes()).hexdigest(),
        manuscript.name: sha256(manuscript.read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status": "PASS", "output": str(args.output), "avoidance_instances": 3, "four_contact_multiples": 6}, sort_keys=True))


if __name__ == "__main__":
    main()
