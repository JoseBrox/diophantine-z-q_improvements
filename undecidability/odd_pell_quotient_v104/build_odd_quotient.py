#!/usr/bin/env python3
"""Use an odd second-Pell quotient and remove the ordinary-abc reciprocal.

This is an equivalence on the source-instance projection. The i interface
now certifies i_half, while the source quotient is 2*i_half+1. It is not a
polynomial lift preserving the old i-interface's elliptic witnesses.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = "undecidability/abc_common_numerator_v103/common_numerator_abc_quadrics.json"
PREDECESSOR_SHA256 = "91098cd9c25b2336ce320391fd7f9f195bee838404996e24dd2e2067412b6877"
DELETED_ROW = "integer.i_reciprocal.unit"
REPLACED_ROW = "jones1980.E.reciprocal"
NEW_ROW = "jones1980.E.odd_quotient"


def terms_by_name(row, names):
    return sorted((str(term["coefficient"]), tuple(sorted(names[i-1] for i in term["monomial"])))
                  for term in row["terms"])


def build(old):
    oldnames = old["variable_names"]
    oldrows = {row["name"]: row for row in old["residuals"]}
    assert old["variables"] == 675 and len(oldrows) == 594
    assert old["integer_blocks"] == 13
    assert old["reciprocal_integer_inputs"] == []
    assert old["source_universality_hypothesis"] is None
    assert terms_by_name(oldrows[DELETED_ROW], oldnames) == [
        ("-1", ()), ("1", ("i", "i_inverse"))]
    assert terms_by_name(oldrows[REPLACED_ROW], oldnames) == [
        ("-1", ("int_c_29",)), ("1", ("E", "i_inverse"))]
    occurrences = {
        name: [row["name"] for row in old["residuals"]
               if any(name == oldnames[i-1] for term in row["terms"] for i in term["monomial"])]
        for name in ("i", "i_inverse")
    }
    assert set(occurrences["i_inverse"]) == {DELETED_ROW, REPLACED_ROW}
    assert set(occurrences["i"]) == {DELETED_ROW, "integer.i.height.betaSquare"}
    assert terms_by_name(oldrows["integer.c.height.betaSquare"], oldnames) == [
        ("-1", ("int_c_29",)), ("1", ("c", "c"))]
    assert terms_by_name(oldrows["integer.i.height.betaSquare"], oldnames) == [
        ("-1", ("int_i_reciprocal_29",)), ("1", ("i", "i"))]

    rename = {"i": "i_half"}
    names = [rename.get(name, name) for name in oldnames if name != "i_inverse"]
    ids = {name: i+1 for i, name in enumerate(names)}
    rows = []
    for row in old["residuals"]:
        if row["name"] == DELETED_ROW:
            continue
        if row["name"] == REPLACED_ROW:
            terms = [
                {"coefficient": "1", "monomial": [ids["E"]]},
                {"coefficient": "-2", "monomial": sorted([ids["i_half"], ids["int_c_29"]])},
                {"coefficient": "-1", "monomial": [ids["int_c_29"]]},
            ]
            rows.append({"name": NEW_ROW, "terms": sorted(terms, key=lambda term: term["monomial"])})
        else:
            rows.append({"name": row["name"], "terms": [
                {"coefficient": term["coefficient"],
                 "monomial": sorted(ids[rename.get(oldnames[i-1], oldnames[i-1])]
                                     for i in term["monomial"])}
                for term in row["terms"]]})

    new = dict(old)
    new["odd_pell_predecessor_scope_metadata"] = {
        key: new.pop(key) for key in (
            "reciprocal_nonzero_guard", "abc_common_numerator_zero_set_scope",
        )
    }
    new["ordinary_integer_inputs"] = [rename.get(name, name) for name in old["ordinary_integer_inputs"]]
    for key in ("fixed_offset_translations", "abc_common_numerator_private_coordinates"):
        new[key] = {rename.get(name, name): value for name, value in old[key].items()}
    new.update({
        "variables": len(names), "variable_names": names, "residuals": rows,
        "outer_coordinates": old["outer_coordinates"]-1,
        "outer_residuals": old["outer_residuals"]-1,
        "odd_pell_predecessor": PREDECESSOR,
        "odd_pell_predecessor_sha256": PREDECESSOR_SHA256,
        "odd_pell_proof": "undecidability/odd_pell_quotient_v104/odd_pell_quotient.tex",
        "odd_pell_removed_coordinate": "i_inverse",
        "odd_pell_removed_row": DELETED_ROW,
        "odd_pell_replaced_row": REPLACED_ROW,
        "odd_pell_new_row": NEW_ROW,
        "odd_pell_coordinate_renaming": rename,
        "odd_pell_old_occurrences": occurrences,
        "odd_pell_source_quotient": "i_source=2*i_half+1",
        "odd_pell_unchanged_interface_role": "integer.i.* and int_i_reciprocal_* are historical role names; the certified input is now i_half",
        "odd_pell_nonzero_proof": "i_half is integral, hence 2*i_half+1 is an odd nonzero integer",
        "odd_pell_positive_completeness": "For B=2*r+1 and c=Y_B(a), choose q=B*c; i_source=Y_q(a)/c^2 is odd and greater than one, so i_half=(i_source-1)/2 is positive integral",
        "odd_pell_projection_scope": "Same source-instance projection after reselecting positive Pell and simultaneous elliptic witnesses. No same-coordinate lift of the old integer.i interface is claimed.",
        "odd_pell_retained_arithmetic_premises": True,
        "odd_pell_savings": {"coordinates": 1, "quadratic_rows": 1},
        "odd_pell_integer_block_count_unchanged": True,
        "simultaneous_completeness_scope": "Nonzero integer tuples; the new i_half input is positive in canonical completeness, and all other inputs retain their previous positive choices",
        "unconditional_undecidability_claim": False,
    })
    assert len(names) == 674 and len(rows) == 593
    assert max(len(term["monomial"]) for row in rows for term in row["terms"]) == 2
    assert {i for row in rows for term in row["terms"] for i in term["monomial"]} == set(ids.values())
    return new


def main():
    raw = (ROOT/PREDECESSOR).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PREDECESSOR_SHA256
    data = build(json.loads(raw))
    output = (json.dumps(data, sort_keys=True, separators=(",", ":"))+"\n").encode()
    (HERE/"odd_quotient_abc_quadrics.json").write_bytes(output)
    certificate = {
        "interface": "ordinary rational abc",
        "variables": data["variables"], "quadratic_rows": len(data["residuals"]),
        "degree": 4, "table_sha256": hashlib.sha256(output).hexdigest(),
        "ordinary_integer_inputs": data["ordinary_integer_inputs"],
        "integer_blocks": data["integer_blocks"],
        "source_universality_hypothesis": data["source_universality_hypothesis"],
        "source_coding_theorem": data["source_coding_theorem"],
        "unconditional_undecidability_claim": False,
        **{key:value for key,value in data.items() if key.startswith("odd_pell_")},
    }
    (HERE/"odd_quotient_abc_certificate.json").write_text(json.dumps(certificate, sort_keys=True, indent=2)+"\n")
    print(json.dumps({key:certificate[key] for key in ("variables","quadratic_rows","degree","table_sha256")}))


if __name__ == "__main__":
    main()
