#!/usr/bin/env python3
"""Compile the one-quotient Pell bridge and remove its discarded abc input.

The local theorem is in one_quotient_pell.tex.  The tuple witness theorem
applies to the eleven remaining nonzero integer inputs, using the same
distinct fixed offsets.  The old j coordinate is the new CRT quotient J.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = ROOT / "undecidability/source_repair_v93/coefficients/signed_abc_fixed_offsets_quadrics.json"
NEW_NAME = "pell_crt_cF"
NEW_ROW = "jones1980.crt.cF.definition"


def named_terms(row, names):
    return sorted((str(t["coefficient"]), tuple(sorted(names[i-1] for i in t["monomial"])))
                  for t in row["terms"])


def build_data(old):
    assert old["pell_core_source_p_parameter"] == "2*w*s^2*r^2*n^6"
    assert old["signed_binomial_positivity_coordinate_saving"] == 5
    assert old["source_universality_hypothesis"] is None
    assert old["variables"] == 781 and len(old["residuals"]) == 684
    names = old["variable_names"]
    rows = {row["name"]: row for row in old["residuals"]}
    assert len(rows) == len(old["residuals"])
    assert named_terms(rows["jones1980.I.definition"], names) == [
        ("-1", ("F", "o")), ("-1", ("d",)), ("1", ("I",))]
    assert named_terms(rows["jones1980.H.definition"], names) == [
        ("-1", ()), ("-1", ("c", "j")), ("-2", ("r",)), ("1", ("H",))]
    removed_names = {"o"} | {name for name in names if name.startswith("int_o_")}
    removed_rows = {name for name in rows if name.startswith("integer.o.")}
    assert len(removed_names) == 48 and len(removed_rows) == 41
    removed_rows.add("jones1980.I.definition")
    occurrences = {}
    for name in sorted(removed_names):
        found = [row["name"] for row in old["residuals"]
                 if any(name == names[i-1] for t in row["terms"] for i in t["monomial"])]
        assert found and set(found) <= removed_rows, (name, found)
        occurrences[name] = found

    assert NEW_NAME not in names and NEW_ROW not in rows
    new_names = [name for name in names if name not in removed_names] + [NEW_NAME]
    ids = {name: i+1 for i,name in enumerate(new_names)}
    new_rows = []
    for row in old["residuals"]:
        if row["name"] in removed_rows:
            continue
        if row["name"] == "jones1980.H.definition":
            terms = [(1, ("H",)), (-1, ("c",)), (-2, ("F2", "r")),
                     (-1, ("F2",)), (1, ("F2", "c")), (-1, (NEW_NAME, "j"))]
            new_rows.append({"name": row["name"], "terms": sorted(
                ({"coefficient": str(coefficient), "monomial": sorted(ids[n] for n in monomial)}
                 for coefficient,monomial in terms), key=lambda t:t["monomial"])})
        else:
            new_rows.append({"name": row["name"], "terms": [
                {"coefficient": t["coefficient"],
                 "monomial": sorted(ids[names[i-1]] for i in t["monomial"])}
                for t in row["terms"]]})
    new_rows.append({"name": NEW_ROW, "terms": sorted([
        {"coefficient": "1", "monomial": [ids[NEW_NAME]]},
        {"coefficient": "-1", "monomial": sorted([ids["c"], ids["F"]])},
    ], key=lambda t:t["monomial"])})

    new = dict(old)
    new.update({
        "variables": len(new_names), "variable_names": new_names, "residuals": new_rows,
        "ordinary_integer_inputs": [name for name in old["ordinary_integer_inputs"] if name != "o"],
        "integer_blocks": 11, "shared_reference_blocks": 11,
        "fixed_offset_translations": {k:v for k,v in old["fixed_offset_translations"].items() if k != "o"},
        "pell_crt_proof": "undecidability/pell_crt_v95/one_quotient_pell.tex",
        "pell_crt_deleted_integer_input": "o",
        "pell_crt_remaining_integer_input_count": 11,
        "pell_crt_quotient_register": "j is the new CRT quotient J, not the old quotient",
        "pell_crt_new_register": NEW_NAME,
        "pell_crt_new_equations": ["pell_crt_cF=c*F", "H=c+F2*(2*r+1-c)+pell_crt_cF*j"],
        "pell_crt_removed_names": sorted(removed_names),
        "pell_crt_removed_rows": sorted(removed_rows),
        "pell_crt_private_occurrences": occurrences,
        "pell_crt_changed_row": "jones1980.H.definition",
        "pell_crt_new_row": NEW_ROW,
        "pell_crt_savings": {"coordinates": 47, "quadratic_rows": 41},
        "pell_crt_outer_savings": {"coordinates": 0, "quadratic_rows": 0},
        "pell_crt_projection_scope": "Same coding-prefix and instance projection under the retained abc arithmetic premises; the new j is an existential replacement, and the deleted integer predicate is not reconstructed at the same shared witness values.",
        "pell_crt_positive_completeness": "J can be positive: choose the third Pell index B+4*q*L for sufficiently large L, where F=X_q(a) and c divides q.",
        "pell_crt_fixed_offsets_scope": "Keep the eleven old offsets; omitting 9/16 preserves all distinct cosets modulo Z_2. The finite-family simultaneous completeness theorem is applied with eleven inputs.",
        "unconditional_undecidability_claim": False,
    })
    assert (new["variables"], len(new_rows)) == (734,643)
    assert len(new["ordinary_integer_inputs"]) == 11
    assert max(len(t["monomial"]) for row in new_rows for t in row["terms"]) == 2
    assert {i for row in new_rows for t in row["terms"] for i in t["monomial"]} == set(ids.values())
    return new


def build():
    raw = PREDECESSOR.read_bytes()
    new = build_data(json.loads(raw))
    new["pell_crt_predecessor"] = str(PREDECESSOR.relative_to(ROOT))
    new["pell_crt_predecessor_sha256"] = hashlib.sha256(raw).hexdigest()
    return new


def main():
    data = build()
    raw = (json.dumps(data, sort_keys=True, separators=(",", ":"))+"\n").encode()
    target = HERE / "crt_abc_quadrics.json"
    target.write_bytes(raw)
    certificate = {
        "variables": data["variables"], "quadratic_rows": len(data["residuals"]), "degree": 4,
        "table_sha256": hashlib.sha256(raw).hexdigest(),
        **{k:v for k,v in data.items() if k.startswith("pell_crt_")},
        "source_universality_hypothesis": None,
        "source_coding_theorem": data["source_coding_theorem"],
        "source_coding_theorem_independently_reproved": False,
        "retained_arithmetic_interfaces": True,
        "unconditional_undecidability_claim": False,
    }
    target.with_name("crt_abc_certificate.json").write_text(json.dumps(certificate, sort_keys=True, indent=2)+"\n")
    print(json.dumps({"variables":734,"quadratic_rows":643,"table_sha256":certificate["table_sha256"]}))


if __name__ == "__main__":
    main()
