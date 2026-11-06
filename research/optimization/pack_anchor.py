"""Produce the five-witness anchor replacement of a pinned quartic.

The producer is deliberately separate from verify_anchor.py.  The arithmetic
equivalence is proved in anchor-proof.tex; the checker validates its literal
application and independently expands every coefficient of the final quartic.
No Git operation is performed.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import shutil


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = REPO / "quartics" / "quartic-12504"
ANCHOR_ROWS = tuple(range(310, 316))
ANCHOR_PRIVATE = tuple(range(329, 345))
C, F0, F1 = 25, 51, 52


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("ascii")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(row):
    return {tuple(mon): coeff for coeff, mon in row}


def encode(row):
    return [[coeff, list(mon)] for mon, coeff in sorted(row.items())]


def variables(rows):
    return {v for row in rows for mon in row for v in mon}


def expand(rows):
    """Triangular expansion; the verifier instead uses ordered pairs."""
    result = defaultdict(int)
    for row in rows:
        terms = sorted(row.items())
        for i, (mon, coeff) in enumerate(terms):
            for j in range(i, len(terms)):
                other, value = terms[j]
                result[tuple(sorted(mon + other))] += coeff * value * (1 if i == j else 2)
    return {mon: coeff for mon, coeff in result.items() if coeff}


def old_anchor():
    rows = []
    for f, a in ((F0, 329), (F1, 337)):
        u0, u1, u2, u3, v1, v2, v3 = range(a + 1, a + 8)
        rows.extend([
            {(C, a): 1, (f,): -1},
            {(): -1, (u0, u0): 1, (u1, u1): -2,
             (u2, u2): -3, (u3, u3): 6},
            {(): -4, (a, a): 1, (a, u0): -4, (u0, u0): 4,
             (v1, v1): -8, (v2, v2): -12, (v3, v3): 24},
        ])
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, default=BASE)
    parser.add_argument("--output", type=Path, default=HERE / "quartic-anchor-packed")
    args = parser.parse_args()
    parent = args.parent.resolve()
    out = args.output.resolve()
    rows = [decode(r) for r in json.loads(gzip.decompress((parent / "candidate-rows.json.gz").read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((parent / "certificate.jsonl.gz").read_bytes()).splitlines()]
    allocated = records[-1]["allocated_variables"]
    assert records[-1]["kind"] == "final"
    active = json.loads((parent / "variable-map.json").read_bytes())
    assert active[0] == 0 and len(active) == len(set(active))
    assert set(active) == variables(rows)
    assert all(rows[index] == expected for index, expected in zip(ANCHOR_ROWS, old_anchor()))
    for v in ANCHOR_PRIVATE:
        occurrences = {i for i, row in enumerate(rows) if any(v in mon for mon in row)}
        assert occurrences and occurrences <= set(ANCHOR_ROWS), (v, occurrences)

    fresh = list(range(allocated, allocated + 5))
    r, d, u, v, w = fresh
    replacement = [
        {(r,): 1, (F0, F0): -1, (F0, F1): -1, (F1, F1): 1},
        {(d,): 1, (C, C): -1},
        {(u, u): 1, (v, v): 6, (w, w): -2, (r, r): -3, (d, d): 2},
    ]
    for index in ANCHOR_ROWS:
        rows[index] = {}
    for index, row in zip(ANCHOR_ROWS, replacement):
        rows[index] = row
    new_active = [v for v in active if v not in ANCHOR_PRIVATE] + fresh
    assert set(new_active) == variables(rows)
    assert len(new_active) == len(active) - 11
    mapping = {v: i for i, v in enumerate(new_active)}
    compact = [
        {tuple(sorted(mapping[v] for v in mon)): coeff for mon, coeff in row.items()}
        for row in rows if row
    ]
    polynomial = expand(compact)
    assert max(map(len, polynomial)) == 4
    assert {v for mon in polynomial for v in mon} == set(range(len(new_active)))
    report = {
        "status": "CANDIDATE: run the independent verifier",
        "variables": len(new_active),
        "witnesses": len(new_active) - 1,
        "rows": len(compact),
        "degree": max(map(len, polynomial)),
        "monomials": len(polynomial),
        "max_abs_coefficient": max(map(abs, polynomial.values())),
        "max_coefficient_bits": max(abs(c).bit_length() for c in polynomial.values()),
        "parent_variables": len(active),
        "variables_removed": 16,
        "variables_added": 5,
        "net_variables_saved": 11,
        "allocated_variables": allocated + 5,
    }
    out.mkdir(parents=True, exist_ok=False)
    (out / "parent").mkdir()
    for name in ("candidate-rows.json.gz", "certificate.jsonl.gz", "variable-map.json"):
        shutil.copyfile(parent / name, out / "parent" / name)
    for name, obj in (
        ("candidate-rows.json.gz", [encode(row) for row in rows]),
        ("residuals.json.gz", [encode(row) for row in compact]),
    ):
        (out / name).write_bytes(gzip.compress(canonical(obj), compresslevel=9, mtime=0))
    (out / "variable-map.json").write_bytes(canonical(new_active) + b"\n")
    (out / "weights.json").write_bytes(canonical([1] * len(compact)) + b"\n")
    expanded = (
        b"# coefficient followed by repeated variable indices; input is variable 0\n"
        + b"".join((" ".join(map(str, (coeff, *mon))) + "\n").encode("ascii")
                   for mon, coeff in sorted(polynomial.items()))
    )
    (out / "polynomial.expanded.txt").write_bytes(expanded)
    (out / "polynomial.expanded.txt.gz").write_bytes(gzip.compress(expanded, compresslevel=9, mtime=0))
    certificate = {
        "schema": "anchor-pack-v1",
        "semantic_rule": "five-witness semilocal anchor, proved in anchor-proof.tex",
        "baseline": {name: sha(BASE / name) for name in (
            "candidate-rows.json.gz", "certificate.jsonl.gz", "variable-map.json",
            "polynomial.expanded.txt", "source-residuals.jsonl.gz", "verify_certificate.py",
            "construction-map.json",
        )},
        "parent": {name: sha(out / "parent" / name) for name in (
            "candidate-rows.json.gz", "certificate.jsonl.gz", "variable-map.json",
        )},
        "old_row_indices": list(ANCHOR_ROWS),
        "old_private_variables": list(ANCHOR_PRIVATE),
        "interface_variables": {"C": C, "f0": F0, "f1": F1},
        "new_variables": dict(zip(("r", "D", "u", "v", "w"), fresh)),
        "matched_old_rows": [encode(row) for row in old_anchor()],
        "new_rows": [encode(row) for row in replacement],
        "projection": "input variable 0 and every unchanged coordinate are preserved",
        "scope": "literal application of the proved semilocal replacement; full expansion is checked separately",
        "expanded_sha256": hashlib.sha256(expanded).hexdigest(),
        "statistics": report,
    }
    (out / "certificate.json").write_text(json.dumps(certificate, indent=2) + "\n")
    (out / "producer-report.json").write_text(json.dumps(report, indent=2) + "\n")
    for name in ("verify_anchor.py", "anchor-proof.tex"):
        shutil.copyfile(HERE / name, out / name)
    (out / "README.md").write_text(
        "# Quartic with a packed semilocal anchor\n\n"
        f"This polynomial has **{report['variables']:,} total variables**, including input 0, "
        f"**degree 4**, and **{report['monomials']:,} nonzero monomials**. "
        f"There are {report['rows']:,} quadratic residuals, each with weight one.\n\n"
        "The anchor replacement saves eleven variables. Its exact rational projection "
        "equivalence is proved in `anchor-proof.tex`. The characterization of the full "
        "source as the integers retains the arithmetic hypotheses and review status "
        "of the upstream manuscript. This package does not independently prove those "
        "deep arithmetic inputs.\n\n"
        "`polynomial.expanded.txt` is the complete coefficient table. Each line gives "
        "an integer coefficient followed by the variable indices of its monomial; "
        "repetition means exponentiation. `residuals.json.gz` gives the complete "
        "quadratic system, whose sum of squares is the polynomial.\n\n"
        "Run from the repository root:\n\n```sh\n"
        f"python3 -E -B {out.relative_to(REPO)}/verify_anchor.py "
        f"{out.relative_to(REPO)} --baseline quartics/quartic-12504\n```\n\n"
        "The verifier first replays the pinned released certificate without changing "
        "its receipt, checks any subsequent rational eliminations and row operations, "
        "matches all six old anchor rows, checks private-variable incidence and the "
        "nonzero constant chain, and independently expands every coefficient. "
        "It imports no producer code. The copied `parent` files make the local "
        "transformation reproducible even when the parent was an intermediate variant. "
        "The pinned upstream package is still needed to replay its earlier certificate.\n\n"
        "Nothing in this directory has been committed or submitted as a pull request.\n"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
