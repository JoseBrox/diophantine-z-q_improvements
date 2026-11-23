#!/usr/bin/env python3
"""Replace the corrected-source w,s positivity wrappers by s != 0.

The quantified equivalence is proved in signed_binomial_positivity.tex.
This transformer checks the exact private supports before removing them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DELETED_ROWS = {"jones1980.positive.w", "jones1980.positive.s"}
DELETED_NAMES = {f"positive_{name}_{i}" for name in ("w", "s") for i in (1, 2, 3)}
GUARD_NAME = "jones1980.s.nonzero"


def named_terms(row, names):
    return sorted((str(t["coefficient"]), tuple(sorted(names[i-1] for i in t["monomial"])))
                  for t in row["terms"])


def build_data(old):
    assert old["pell_core_source_p_parameter"] == "2*w*s^2*r^2*n^6"
    assert old["source_universality_hypothesis"] is None
    names = old["variable_names"]
    assert DELETED_NAMES <= set(names) and "s_inverse" not in names
    rows = {row["name"]: row for row in old["residuals"]}
    assert DELETED_ROWS <= rows.keys() and GUARD_NAME not in rows
    for name in ("w", "s"):
        expected = [("-2", ()), ("2", (name,))]
        for i in (1, 2, 3):
            coordinate = f"positive_{name}_{i}"
            expected.extend([("-1", (coordinate,)), ("-1", (coordinate, coordinate))])
        assert named_terms(rows[f"jones1980.positive.{name}"], names) == sorted(expected)
    occurrences = {
        name: [row["name"] for row in old["residuals"]
               if any(name == names[i-1] for term in row["terms"] for i in term["monomial"])]
        for name in sorted(DELETED_NAMES)
    }
    for name, found in occurrences.items():
        assert found == [f"jones1980.positive.{name.split('_')[1]}"]

    new_names = [name for name in names if name not in DELETED_NAMES] + ["s_inverse"]
    ids = {name: i+1 for i, name in enumerate(new_names)}
    new_rows = []
    for row in old["residuals"]:
        if row["name"] in DELETED_ROWS:
            continue
        new_rows.append({"name": row["name"], "terms": [
            {"coefficient": term["coefficient"],
             "monomial": sorted(ids[names[i-1]] for i in term["monomial"])}
            for term in row["terms"]
        ]})
    new_rows.append({"name": GUARD_NAME, "terms": [
        {"coefficient": "-1", "monomial": []},
        {"coefficient": "1", "monomial": sorted([ids["s"], ids["s_inverse"]])},
    ]})
    new = dict(old)
    new.update({
        "variables": len(new_names),
        "outer_coordinates": old["outer_coordinates"]-5,
        "outer_residuals": old["outer_residuals"]-1,
        "variable_names": new_names,
        "residuals": new_rows,
        "signed_binomial_positivity_proof": "undecidability/source_repair_v93/signed_binomial_positivity.tex",
        "signed_binomial_positivity_modulus_hypothesis": "M=n^2 >= 16, automatic from the retained q=b^(5^60), n=q^16 and b>=2",
        "signed_binomial_positivity_removed_rows": sorted(DELETED_ROWS),
        "signed_binomial_positivity_removed_coordinates": sorted(DELETED_NAMES),
        "signed_binomial_positivity_private_occurrences": occurrences,
        "signed_binomial_positivity_added_row": GUARD_NAME,
        "signed_binomial_positivity_added_coordinate": "s_inverse",
        "signed_binomial_positivity_new_equation": "s*s_inverse=1",
        "signed_binomial_positivity_coordinate_saving": 5,
        "signed_binomial_positivity_row_saving": 1,
        "signed_binomial_positivity_old_positive_inputs_recovered": ["w", "s"],
        "signed_binomial_positivity_integer_predicates_unchanged": True,
        "signed_binomial_positivity_zero_s_exclusion_required": True,
    })
    assert new["variables"] == old["variables"]-5
    assert len(new_rows) == len(old["residuals"])-1
    assert max(len(t["monomial"]) for row in new_rows for t in row["terms"]) == 2
    assert {i for row in new_rows for t in row["terms"] for i in t["monomial"]} == set(ids.values())
    return new


def build(path):
    raw = Path(path).read_bytes()
    new = build_data(json.loads(raw))
    new["signed_binomial_positivity_predecessor_sha256"] = hashlib.sha256(raw).hexdigest()
    return new


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    if args.source is not None:
        if args.out is None:
            ap.error("--source requires --out")
        pairs = [(args.source, args.out)]
    else:
        pairs = [(HERE / "coefficients" / f"corrected_ceiling_m{m}_quadrics.json",
                  HERE / "coefficients" / f"signed_ceiling_m{m}_quadrics.json") for m in (163,179)]
        pairs.append((HERE / "coefficients/corrected_abc_fixed_offsets_quadrics.json",
                      HERE / "coefficients/signed_abc_fixed_offsets_quadrics.json"))
    for source, target in pairs:
        source, target = source.resolve(), target.resolve()
        data = build(source)
        raw = (json.dumps(data, sort_keys=True, separators=(",", ":"))+"\n").encode()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        certificate = {
            "variables": data["variables"],
            "quadratic_rows": len(data["residuals"]),
            "degree": 4,
            "table_sha256": hashlib.sha256(raw).hexdigest(),
            **{k: v for k,v in data.items() if k.startswith("signed_binomial_positivity_")},
            "source_universality_hypothesis": data["source_universality_hypothesis"],
            "source_coding_theorem": data["source_coding_theorem"],
            "source_coding_theorem_independently_reproved": False,
            "retained_arithmetic_interfaces": True,
            "unconditional_undecidability_claim": False,
        }
        target.with_name(target.name.replace("_quadrics.json", "_certificate.json")).write_text(
            json.dumps(certificate, indent=2, sort_keys=True)+"\n")
        print(json.dumps({"path":str(target.relative_to(ROOT)), "variables":data["variables"],
                          "rows":len(data["residuals"]), "sha256":certificate["table_sha256"]}))


if __name__ == "__main__":
    main()
