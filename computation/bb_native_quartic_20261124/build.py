#!/usr/bin/env python3
"""Rebuild the BB-native quartics from the immutable v82 physical quadrics.

Use only Python's standard library.  This is a producer, not the independent
source reconstruction; run check.py separately after building.
"""
from collections import defaultdict
from itertools import combinations_with_replacement
from pathlib import Path
from math import gcd
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

REPLACE = {
    "first": {"3": "289", "-34": "0", "-289": "-289", "17": "7"},
    "middle": {"17": "289", "-1": "-7", "-17": "-289"},
    "second": {"1": "289", "34": "0", "-867": "-289", "-17": "-7"},
}


def row_kind(name):
    if name.endswith(".firstConic") or name == "v82.scalar.first":
        return "first"
    if name.endswith(".Bh.definition") or name == "v82.scalar.middle":
        return "middle"
    if name.endswith(".secondConic") or name == "v82.scalar.second":
        return "second"
    return None


def produce(n):
    old = ROOT / f"computation/variable_reductions_v82/general/quartic{n}/quadrics.json"
    q = json.loads(old.read_text())
    modified = []
    for row in q["residuals"]:
        kind = row_kind(row["name"])
        if not kind:
            continue
        # Other rows are not modified, including BOTH private square registers.
        assert row["name"].startswith("detector") or row["name"].startswith("v82.scalar.")
        table = REPLACE[kind]
        for t in row["terms"]:
            assert t["coefficient"] in table, (row["name"], t)
            t["coefficient"] = table[t["coefficient"]]
        row["terms"] = [t for t in row["terms"] if t["coefficient"] != "0"]
        modified.append(row["name"])
        row["name"] = "bbnative." + row["name"]
    assert len(modified) == (9 if n == 163 else 12), modified

    expanded = defaultdict(int)
    for row in q["residuals"]:
        for i, a in enumerate(row["terms"]):
            for b in row["terms"][i:]:
                k = a["parameterPower"] + b["parameterPower"]
                mon = tuple(sorted(a["monomial"] + b["monomial"]))
                expanded[(k, mon)] += int(a["coefficient"]) * int(b["coefficient"]) * (1 if a is b else 2)
    expanded = {k: v for k, v in expanded.items() if v}
    p = {
        "variables": n,
        "parameter": q["parameter"],
        "input": 1,
        "terms": [
            {"parameterPower": k, "monomial": list(mon), "coefficient": str(coeff)}
            for (k, mon), coeff in sorted(expanded.items())
        ],
    }
    assert q["variables"] == p["variables"] == n
    assert gcd(*expanded.values()) == 1
    assert max(len(m) for _, m in expanded) == 4
    return q, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="compare against committed tables")
    ap.add_argument("--output", type=Path, help="write a separate reproduction directory")
    args = ap.parse_args()
    assert args.verify or args.output
    for n in (163, 179):
        q, p = produce(n)
        if args.verify:
            for name, obj in (("quadrics", q), ("polynomial", p)):
                path = HERE / f"quartic{n}/{name}.json"
                assert json.loads(path.read_text()) == obj, path
        if args.output:
            out = args.output / f"quartic{n}"
            out.mkdir(parents=True, exist_ok=True)
            (out / "quadrics.json").write_text(json.dumps(q) + "\n")
            (out / "polynomial.json").write_text(json.dumps(p) + "\n")
        print(f"PASS {n}: {len(q['residuals'])} quadrics, {len(p['terms'])} terms")


if __name__ == "__main__":
    main()
