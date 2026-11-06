#!/usr/bin/env python3
"""Exact counterexample to extending the released quartic to Q(i).

Usage:
    python3 check_base_change.py path/to/quartics/quartic-12504

No third-party packages are used.  The program independently reads the expanded
polynomial and the quadratic residuals, then performs the substitution over
Q(i)[t] using pairs of fractions for Gaussian rational coefficients.
It does NOT disprove the existence of some other polynomial defining Z[i].
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

TABLE_SHA256 = "7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca"
C = 5937913971887799417367
KEEP = {0, 2242, 2243}
ZERO = (F(0), F(0))
ONE = (F(1), F(0))
I = (F(0), F(1))


def gadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def gmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def padd(a, b):
    out = dict(a)
    for e, c in b.items():
        out[e] = gadd(out.get(e, ZERO), c)
        if out[e] == ZERO:
            del out[e]
    return out


def pmul(a, b):
    out = {}
    for e, c in a.items():
        for f, d in b.items():
            k = e + f
            out[k] = gadd(out.get(k, ZERO), gmul(c, d))
            if out[k] == ZERO:
                del out[k]
    return out


def pscale(a, c):
    return {e: d for e, v in a.items() if (d := gmul(v, c)) != ZERO}


def substitute_term(c, ids, values):
    out = {0: (F(c), F(0))}
    for idx in ids:
        if idx not in values:
            return {}
        out = pmul(out, values[idx])
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quartic_directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    table = args.quartic_directory / "polynomial.expanded.txt"
    digest = hashlib.sha256(table.read_bytes()).hexdigest()
    if digest != TABLE_SHA256:
        raise ValueError(f"Unexpected source table SHA-256: {digest}")

    # R=C+4t^2+t^4, u=(1-R)/2, v=i(1+R)/2.
    r = {0: (F(C), F(0)), 2: (F(4), F(0)), 4: ONE}
    u = pscale(padd({0: ONE}, pscale(r, (F(-1), F(0)))), (F(1, 2), F(0)))
    v = pscale(padd({0: ONE}, r), (F(0), F(1, 2)))
    values = {0: {1: ONE}, 2242: u, 2243: v}

    restriction_table = defaultdict(int)
    substitution_table = {}
    table_terms = 0
    for line in table.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        c, *ids = map(int, line.split())
        table_terms += 1
        if set(ids) <= KEEP:
            restriction_table[tuple(ids)] += c
        substitution_table = padd(substitution_table, substitute_term(c, ids, values))

    residual_file = args.quartic_directory / "residuals.json.gz"
    with gzip.open(residual_file, "rt") as stream:
        residuals = json.load(stream)
    restriction_residuals = defaultdict(int)
    substitution_residuals = {}
    for row in residuals:
        restricted = defaultdict(int)
        substituted = {}
        for c, ids in row:
            if set(ids) <= KEEP:
                restricted[tuple(ids)] += c
            substituted = padd(substituted, substitute_term(c, ids, values))
        for m, c in restricted.items():
            for n, d in restricted.items():
                restriction_residuals[tuple(sorted(m + n))] += c * d
        substitution_residuals = padd(substitution_residuals, pmul(substituted, substituted))

    restriction_residuals = {m: c for m, c in restriction_residuals.items() if c}
    expected = {(): C, (0, 0): 4, (0, 0, 0, 0): 1, (2242, 2242): 1, (2243, 2243): 1}
    assert dict(restriction_table) == expected
    assert restriction_residuals == expected
    assert substitution_table == {}, substitution_table
    assert substitution_residuals == {}, substitution_residuals

    t_example = F(1, 2)
    r_example = F(C) + 4 * t_example**2 + t_example**4
    u_example = (1 - r_example) / 2
    v_imaginary = (1 + r_example) / 2
    assert r_example + u_example**2 - v_imaginary**2 == 0

    receipt = {
        "result": "verified",
        "source_table_sha256": digest,
        "expanded_table_monomials": table_terms,
        "quadratic_residuals": len(residuals),
        "specialized_variable_indices": sorted(KEEP),
        "restriction": "C + 4*t^2 + t^4 + X2242^2 + X2243^2",
        "C": C,
        "generic_field": "Any field containing Q(i)",
        "generic_substitution": {
            "R": "C+4*t^2+t^4",
            "X2242": "(1-R)/2",
            "X2243": "i*(1+R)/2",
            "other_witnesses": "0",
        },
        "generic_substitution_verified_in_Qi_t": {
            "expanded_table": True,
            "sum_of_squared_residuals": True,
        },
        "nonintegral_example": {
            "t": str(t_example),
            "X2242": str(u_example),
            "X2243": str(v_imaginary) + "*i",
            "other_witnesses": "0",
            "value": "0",
        },
        "scope": "The released polynomial projects onto all of Q(i). This does not rule out another Diophantine definition of Z[i] in Q(i).",
    }
    encoded = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
