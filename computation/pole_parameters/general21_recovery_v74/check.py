#!/usr/bin/env python3
"""Exact coupled physical-weight lifting for the general 21-coordinate target.

The algebraic fixtures here are NOT prepared elliptic witnesses.  This checker
does not claim simultaneous rational realization of the two trace square tests.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
X = sp.Symbol("lambda")
S = sp.Symbol("s")
THETA = tuple(sp.Rational(b) + c for b in (2, 4)
              for c in (sp.Rational(0), -sp.Rational(1, 2), -sp.Rational(1),
                        sp.Rational(1, 2399), -sp.Rational(32, 407)))
P = sp.Poly(sp.prod(X - c for c in THETA), X, domain=sp.QQ)


def coefficients(p):
    return [str(c) for c in p.all_coeffs()]


def physical_weights(rho, a, slope):
    rho, a, slope = map(sp.Rational, (rho, a, slope))
    assert rho != 0 and a > 0
    assert slope != -1 and a * slope != -2
    return (sp.cancel(rho * P.eval(slope) / (slope + 1) ** 10),
            sp.cancel(rho * P.eval(a * slope - 4) / (a * slope + 2) ** 10))


def lift_pair(rho, a, u0, u1):
    """Return EVERY finite rational lift, with the two contact poles removed.

    Higher-degree gcds are factored over Q: they are not assumed linear.
    The slope guard lambda != 0 and all detector guards belong to the caller.
    """
    rho, a, u0, u1 = map(sp.Rational, (rho, a, u0, u1))
    assert rho != 0 and a > 0
    f0 = sp.Poly(rho * P.as_expr() - u0 * (X + 1) ** 10, X, domain=sp.QQ)
    f1 = sp.Poly(rho * P.as_expr().subs(X, a * X - 4)
                 - u1 * (a * X + 2) ** 10, X, domain=sp.QQ)
    g = sp.gcd(f0, f1).monic()
    roots = sorted((r for r in sp.polys.polytools.ground_roots(g)
                    if r != -1 and a * r != -2), key=lambda r: r)
    for r in roots:
        assert physical_weights(rho, a, r) == (u0, u1)
    q0, rem0 = sp.div(f0, g)
    q1, rem1 = sp.div(f1, g)
    assert rem0.is_zero and rem1.is_zero
    # Certify maximality of the computed gcd by a rational Bezout identity.
    e0, e1, unit = sp.gcdex(q0, q1)
    assert unit == sp.Poly(1, X, domain=sp.QQ)
    assert e0 * q0 + e1 * q1 == unit
    return {
        "gcd_degree": int(g.degree()),
        "gcd_descending_coefficients": coefficients(g),
        "rational_lifts": [str(r) for r in roots],
        "bezout_after_gcd": {"e0": coefficients(e0), "e1": coefficients(e1)},
        "all_other_source_guards_checked": False,
    }


def normalized_preimages(w):
    """All rational preimages under u -> u/(1+u)^2, with u != -1."""
    w = sp.Rational(w)
    assert w != 0
    poly = sp.Poly(w * X ** 2 + (2 * w - 1) * X + w, X, domain=sp.QQ)
    roots = sorted(sp.polys.polytools.ground_roots(poly), key=lambda r: r)
    assert all(r != -1 and sp.cancel(r / (1 + r) ** 2) == w for r in roots)
    return roots


def lift_normalized_pair(rho, a, w0, w1):
    """Exact direct lift of normalized weights; no square-root branch is assumed."""
    rho, a, w0, w1 = map(sp.Rational, (rho, a, w0, w1))
    assert rho != 0 and a > 0 and w0 != 0 and w1 != 0
    numerators = [rho * P.as_expr(), rho * P.as_expr().subs(X, a * X - 4)]
    denominators = [(X + 1) ** 10, (a * X + 2) ** 10]
    polys = [sp.Poly(w * (n + d) ** 2 - n * d, X, domain=sp.QQ)
             for w, n, d in zip((w0, w1), numerators, denominators)]
    g = sp.gcd(*polys).monic()
    roots = []
    for r in sorted(sp.polys.polytools.ground_roots(g), key=lambda q: q):
        if any(d.subs(X, r) == 0 or (n + d).subs(X, r) == 0
               for n, d in zip(numerators, denominators)):
            continue
        uu = physical_weights(rho, a, r)
        assert tuple(sp.cancel(u / (1 + u) ** 2) for u in uu) == (w0, w1)
        roots.append(r)
    q0, r0 = sp.div(polys[0], g)
    q1, r1 = sp.div(polys[1], g)
    assert r0.is_zero and r1.is_zero
    e0, e1, unit = sp.gcdex(q0, q1)
    assert unit == sp.Poly(1, X, domain=sp.QQ) and e0 * q0 + e1 * q1 == unit
    return {"gcd_degree": int(g.degree()),
            "gcd_descending_coefficients": coefficients(g),
            "rational_lifts": [str(r) for r in roots],
            "maximal_gcd_verified_by_exact_Bezout_identity": True,
            "all_other_source_guards_checked": False}


def check():
    assert len(set(THETA)) == 10 and all(c > 0 for c in THETA)
    # At a=2 the two physical functions have the same pole.  In s=1/(lambda+1)
    # they are these polynomial functions, after division by rho.
    q0 = sp.Poly(sp.prod(1 - (c + 1) * S for c in THETA), S, domain=sp.QQ)
    q1 = sp.Poly(sp.prod(1 - (c + 6) * S / 2 for c in THETA), S, domain=sp.QQ)
    assert sp.cancel(q0.as_expr().subs(S, 1 / (X + 1))
                     - P.as_expr() / (X + 1) ** 10) == 0
    assert sp.cancel(q1.as_expr().subs(S, 1 / (X + 1))
                     - P.as_expr().subs(X, 2 * X - 4) / (2 * X + 2) ** 10) == 0
    z0 = q0.clear_denoms()[1]
    z1 = q1.clear_denoms()[1]
    p = 101
    f = sp.Poly(z0, S, modulus=p).diff()
    h = sp.Poly(z1, S, modulus=p).diff()
    e, k, g = sp.gcdex(f, h)
    assert f.degree() == h.degree() == 9 and g == sp.Poly(1, S, modulus=p)
    assert e * f + k * h == g
    assert sp.gcd(q0.diff(), q1.diff()).degree() == 0
    # Independently check the only possible rational deck involution.
    a = sp.Symbol("a", positive=True)
    involution = -((a + 2) * X + 4) / (2 * a * X + a + 2)
    mobius = (X + 1) / (a * X + 2)
    assert sp.cancel(mobius.subs(X, involution) + mobius) == 0
    assert sp.cancel(involution.subs(X, involution) - X) == 0
    examples = []
    rho = sp.Rational(3, 7)
    for aa in (sp.Rational(3, 2), sp.Rational(2), sp.Rational(3)):
        pair = physical_weights(rho, aa, 7)
        result = lift_pair(rho, aa, *pair)
        assert result["gcd_degree"] == 1 and result["rational_lifts"] == ["7"]
        examples.append({"rho": str(rho), "scale": str(aa), "slope": "7",
                         "u": [str(v) for v in pair], "lift": result})
    mixed0 = physical_weights(rho, 3, 7)[0]
    mixed1 = physical_weights(rho, 3, 8)[1]
    rejection = lift_pair(rho, 3, mixed0, mixed1)
    assert rejection["gcd_degree"] == 0 and not rejection["rational_lifts"]
    normalized = []
    for u in (sp.Rational(2, 3), sp.Rational(1), sp.Rational(5)):
        w = u / (1 + u) ** 2
        roots = normalized_preimages(w)
        assert set(roots) == {u, 1 / u}
        normalized.append({"w": str(w), "u_preimages": [str(r) for r in roots]})
    pair = physical_weights(rho, 3, 7)
    wp = tuple(u / (1 + u) ** 2 for u in pair)
    direct_normalized = lift_normalized_pair(rho, 3, *wp)
    assert direct_normalized["gcd_degree"] == 1
    assert direct_normalized["rational_lifts"] == ["7"]
    bad_wp = (mixed0 / (1 + mixed0) ** 2, mixed1 / (1 + mixed1) ** 2)
    rejected_normalized = lift_normalized_pair(rho, 3, *bad_wp)
    assert rejected_normalized["gcd_degree"] == 0
    assert rejected_normalized["rational_lifts"] == []
    return {
        "status": "PASS",
        "scope": "Coupled physical-weight birationality and exact lifting only",
        "general21_realization_claimed": False,
        "fixtures_are_prepared_elliptic_witnesses": False,
        "theta0": [str(c) for c in THETA],
        "same_pole_scale_two_certificate": {
            "s_coordinate": "1/(lambda+1)", "prime": p,
            "q0_integer_descending": coefficients(z0),
            "q1_integer_descending": coefficients(z1),
            "derivative0_mod_p_descending": [int(c) % p for c in f.all_coeffs()],
            "derivative1_mod_p_descending": [int(c) % p for c in h.all_coeffs()],
            "bezout_e_descending": [int(c) % p for c in e.all_coeffs()],
            "bezout_k_descending": [int(c) % p for c in k.all_coeffs()],
            "bezout_value": 1,
        },
        "exact_positive_lift_examples": examples,
        "mismatched_pair_rejected": rejection,
        "normalized_weight_branches": normalized,
        "direct_normalized_pair_lift": direct_normalized,
        "direct_normalized_mismatched_pair_rejected": rejected_normalized,
        "remaining_requirements": [
            "Actual elliptic point tuple, source scale and rho",
            "Both actual trace-square equations",
            "Original point, difference, scalar, contact and denominator guards",
            "Whole-character conditions, selected contacts, fixed places and real preparation",
            "Cofinite integer-input completeness, not supplied by this theorem",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--lift", nargs=4, metavar=("RHO", "SCALE", "U0", "U1"))
    parser.add_argument("--lift-normalized", nargs=4,
                        metavar=("RHO", "SCALE", "W0", "W1"))
    args = parser.parse_args()
    assert not (args.lift and args.lift_normalized)
    result = (lift_pair(*args.lift) if args.lift else
              lift_normalized_pair(*args.lift_normalized) if args.lift_normalized else check())
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result.get("status", "computed"),
                      "output": str(args.output),
                      "general21_realization_claimed": False}))


if __name__ == "__main__":
    main()
