#!/usr/bin/env python3
"""Exact Gaussian-field counterexamples for both frozen phase-two quartics.

The sparse coefficient table and the sum of squared residuals are checked
independently.  The fixed integer kappa remains a formal symbol, so no
enormous integer is expanded.  Only the Python standard library is used.
"""
from fractions import Fraction
from hashlib import sha256
import gzip
import json
from pathlib import Path


def add(a, b):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, (Fraction(0), Fraction(0)))
        out[m] = (out[m][0]+c[0], out[m][1]+c[1])
        if out[m] == (0, 0):
            del out[m]
    return out


def scale(a, c):
    return {m: (r*c, i*c) for m, (r, i) in a.items() if c}


def multiply(a, b):
    out = {}
    for ma, (ar, ai) in a.items():
        for mb, (br, bi) in b.items():
            m = tuple(x+y for x, y in zip(ma, mb))
            c = (ar*br-ai*bi, ar*bi+ai*br)
            out = add(out, {m: c})
    return out


def power(a, e):
    out = {(0, 0): (Fraction(1), Fraction(0))}
    for _ in range(e):
        out = multiply(out, a)
    return out


def specialize_to_three(terms, u, v):
    """Return the exact polynomial in T,u,v,kappa after other witnesses=0."""
    out = {}
    for monomial, kappa, coefficient in terms:
        if not set(monomial) <= {0, u, v}:
            continue
        key = (monomial.count(0), monomial.count(u), monomial.count(v), kappa)
        out[key] = out.get(key, 0)+coefficient
        if out[key] == 0:
            del out[key]
    return out


def square_three(poly):
    out = {}
    for a, c in poly.items():
        for b, d in poly.items():
            m = tuple(x+y for x, y in zip(a, b))
            out[m] = out.get(m, 0)+c*d
    return {m: c for m, c in out.items() if c}


def substitute(poly, upoly, vpoly):
    out = {}
    for (t, u, v, k), c in poly.items():
        term = {(t, k): (Fraction(c), Fraction(0))}
        term = multiply(term, power(upoly, u))
        term = multiply(term, power(vpoly, v))
        out = add(out, term)
    return out


def check_one(path, u, v):
    raw = gzip.decompress(path.read_bytes())
    source = json.loads(raw)
    expanded = specialize_to_three(source["expanded_polynomial"], u, v)
    residual_sum = {}
    specialized_residuals = []
    for row in source["residuals"]:
        residual = specialize_to_three(row["terms"], u, v)
        specialized_residuals.append(residual)
        for monomial, coefficient in square_three(residual).items():
            residual_sum[monomial] = residual_sum.get(monomial, 0)+coefficient
    residual_sum = {m: c for m, c in residual_sum.items() if c}
    assert expanded == residual_sum
    assert expanded[(0, 2, 0, 0)] == expanded[(0, 0, 2, 0)] == 1
    remainder = {m: c for m, c in expanded.items() if m not in [(0, 2, 0, 0), (0, 0, 2, 0)]}
    assert all(a == b == 0 for _, a, b, _ in remainder)
    R = {(t, k): (Fraction(c), Fraction(0)) for (t, _, _, k), c in remainder.items()}
    one = {(0, 0): (Fraction(1), Fraction(0))}
    upoly = scale(add(one, scale(R, -1)), Fraction(1, 2))
    real_v = scale(add(one, R), Fraction(1, 2))
    vpoly = {m: (-b, a) for m, (a, b) in real_v.items()}
    assert substitute(expanded, upoly, vpoly) == {}
    independently_substituted_sum = {}
    for residual in specialized_residuals:
        term = substitute(residual, upoly, vpoly)
        independently_substituted_sum = add(independently_substituted_sum, multiply(term, term))
    assert independently_substituted_sum == {}
    return {
        "file": str(path), "source_json_sha256": sha256(raw).hexdigest(),
        "total_variables": len(source["variables"]), "residuals": len(source["residuals"]),
        "u_index": u, "v_index": v, "u_variable": source["variables"][u],
        "v_variable": source["variables"][v],
        "restriction_terms_T_u_v_kappa": [[list(m), c] for m, c in sorted(expanded.items())],
        "generic_witnesses": "u=(1-R)/2; v=i*(1+R)/2; all other witnesses zero",
        "nonintegral_rational_input": "T=1/2",
        "scope": "Exact polynomial identity over Q(i)[T,kappa], checked independently from expanded terms and squared residuals. For the 1367 polynomial substitute its fixed integer kappa afterwards.",
        "conclusion": "The existential projection is the whole field over every characteristic-zero field containing i.",
    }


def find_pair(path):
    source = json.loads(gzip.decompress(path.read_bytes()))
    singles, pairs = {}, set()
    for monomial, kappa, coefficient in source["expanded_polynomial"]:
        support = set(monomial)-{0}
        if len(support) == 1:
            v = next(iter(support))
            singles.setdefault(v, []).append((monomial, kappa, coefficient))
        elif len(support) == 2:
            pairs.add(tuple(sorted(support)))
    candidates = sorted(v for v, terms in singles.items() if terms == [([v, v], 0, 1)])
    return next((u, v) for i, u in enumerate(candidates) for v in candidates[i+1:] if (u, v) not in pairs)


def main():
    here = Path(__file__).resolve().parent
    repo = here.parents[2]
    root = repo/"research/phase2/quartic"
    cases = [check_one(root/"quartic-best/polynomial.json.gz", 62, 78),
             check_one(root/"quartic-small-coefficients/polynomial.json.gz", 86, 102)]
    for name in ["quartic-direct", "quartic-direct-small-coefficients"]:
        path = repo/"research/phase3/quartic"/name/"polynomial.json.gz"
        cases.append(check_one(path, *find_pair(path)))
    receipt = {"status": "passed", "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(), "cases": cases}
    target = here/"quartic-base-change-verification_20261106_v1.json"
    target.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({"status": "passed", "total_variable_counts": [c["total_variables"] for c in cases], "receipt": str(target)}))


if __name__ == "__main__":
    main()
