#!/usr/bin/env python3
"""Remove sr2 using the retained quadratic definition of a."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSORS = {
    "general": "undecidability/pell_signed_q_v98/signed_q_general_quadrics.json",
    "specified": "undecidability/pell_halftrace_v96/halftrace_m179_quadrics.json",
    "abc": "undecidability/pell_signed_q_v98/signed_q_abc_quadrics.json",
}
REMOVED_COORDINATE = "sr2"
REMOVED_ROW = "jones1980.sr2.definition"
CHANGED_ROW = "jones1980.p.definition"
RETAINED_ROW = "jones1980.a.definition"


def build_data(old):
    names = old["variable_names"]
    occurrences = [
        row["name"] for row in old["residuals"]
        if any(names[index - 1] == REMOVED_COORDINATE
               for term in row["terms"] for index in term["monomial"])
    ]
    assert occurrences == [REMOVED_ROW, CHANGED_ROW]
    new_names = [name for name in names if name != REMOVED_COORDINATE]
    ids = {name: index + 1 for index, name in enumerate(new_names)}
    rows = []
    for row in old["residuals"]:
        if row["name"] == REMOVED_ROW:
            continue
        if row["name"] == CHANGED_ROW:
            terms = [
                {"coefficient": "1", "monomial": [ids["p"]]},
                {"coefficient": "-2", "monomial": sorted([ids["a"], ids["sr"]])},
                {"coefficient": "2", "monomial": [ids["sr"], ids["sr"]]},
            ]
            terms.sort(key=lambda term: term["monomial"])
        else:
            terms = [
                {"coefficient": term["coefficient"],
                 "monomial": [ids[names[index - 1]] for index in term["monomial"]]}
                for term in row["terms"]
            ]
        rows.append({"name": row["name"], "terms": terms})
    new = dict(old)
    new.update({
        "variables": len(new_names),
        "variable_names": new_names,
        "residuals": rows,
        "outer_coordinates": old["outer_coordinates"] - 1,
        "outer_residuals": old["outer_residuals"] - 1,
        "source_repair_reused_register": "sr=r*Y=r*s*n^2; no separate sr^2 register is needed",
        "pell_product_predecessor_register_metadata": {
            "source_repair_reused_register": old["source_repair_reused_register"],
        },
        "pell_product_proof": "undecidability/pell_product_v99/pell_product_elimination.tex",
        "pell_product_removed_coordinate": REMOVED_COORDINATE,
        "pell_product_removed_row": REMOVED_ROW,
        "pell_product_changed_row": CHANGED_ROW,
        "pell_product_retained_identity_row": RETAINED_ROW,
        "pell_product_private_occurrences": occurrences,
        "pell_product_new_equation": "p-2*a*sr+2*sr^2=0",
        "pell_product_recovery": "sr2=sr^2",
        "pell_product_identity": "new_p=old_p+2*U*old_square-2*sr*retained_a",
        "pell_product_equivalence_scope": "Exact polynomial equivalence after forgetting sr2; unique inverse lift sr2=sr^2, with no division or nonzero assumptions",
        "pell_product_savings": {"coordinates": 1, "quadratic_rows": 1},
        "pell_product_integer_interfaces_unchanged": True,
        "unconditional_undecidability_claim": False,
    })
    assert len(rows) == len(old["residuals"]) - 1
    assert len(new_names) == old["variables"] - 1
    assert {index for row in rows for term in row["terms"] for index in term["monomial"]} == set(ids.values())
    return new


def main():
    for interface, relative in PREDECESSORS.items():
        raw = (ROOT / relative).read_bytes()
        old = json.loads(raw)
        new = build_data(old)
        new["pell_product_predecessor"] = relative
        new["pell_product_predecessor_sha256"] = hashlib.sha256(raw).hexdigest()
        output = (json.dumps(new, sort_keys=True, separators=(",", ":")) + "\n").encode()
        path = HERE / f"product_{interface}_quadrics.json"
        path.write_bytes(output)
        certificate = {
            "interface": interface,
            "variables": new["variables"],
            "quadratic_rows": len(new["residuals"]),
            "degree": 4,
            "table_sha256": hashlib.sha256(output).hexdigest(),
            **{key: value for key, value in new.items() if key.startswith("pell_product_")},
            "M_recovery": new["M_recovery"],
            "a_recovery": new["a_recovery"],
            "ordinary_integer_inputs": new["ordinary_integer_inputs"],
            "reciprocal_integer_inputs": new["reciprocal_integer_inputs"],
            **({"instance_range": new["instance_range"]} if "instance_range" in new else {}),
            "source_coding_theorem": new["source_coding_theorem"],
            "source_coding_theorem_independently_reproved": False,
            "source_universality_hypothesis": None,
            "retained_arithmetic_interfaces": True,
            "unconditional_undecidability_claim": False,
        }
        (HERE / f"product_{interface}_certificate.json").write_text(
            json.dumps(certificate, sort_keys=True, indent=2) + "\n")
        print(json.dumps({key: certificate[key] for key in (
            "interface", "variables", "quadratic_rows", "table_sha256")}))


if __name__ == "__main__":
    main()
