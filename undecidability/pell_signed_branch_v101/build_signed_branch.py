#!/usr/bin/env python3
"""Delete the first-Pell sign square, using the signed projection theorem."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSORS = {
    "general": "undecidability/aggregate_spacing_v100/aggregate_spacing_general_quadrics.json",
    "abc": "undecidability/pell_product_v99/product_abc_quadrics.json",
}
REMOVED_COORDINATE = "pell_d_positive_square"
REMOVED_ROW = "jones1980.pell_positive_root"
HISTORY_PREFIXES = ("pell_halftrace_", "signed_binomial_positivity_")
HISTORY_KEYS = {
    "pell_core_positive_root", "phi_recovery",
    "pell_power_signed_branches", "pell_signed_q_final_recovery",
    "pell_core_equivalence_scope", "source_universality_verification_scope",
}


def build_data(old):
    names = old["variable_names"]
    assert old["pell_power_new_integer_inputs_certified"] is True
    assert old["integer_blocks"] == 13
    assert old["pell_power_bounds"] == [
        "k^2-4*(c-k*Y)^2-C^2>0 (absorbed in the retained eta margin)"]
    occurrences = [
        row["name"] for row in old["residuals"]
        if any(names[index - 1] == REMOVED_COORDINATE
               for term in row["terms"] for index in term["monomial"])
    ]
    assert occurrences == [REMOVED_ROW]
    new_names = [name for name in names if name != REMOVED_COORDINATE]
    ids = {name: index + 1 for index, name in enumerate(new_names)}
    rows = [
        {"name": row["name"],
         "terms": [
             {"coefficient": term["coefficient"],
              "monomial": [ids[names[index - 1]] for index in term["monomial"]]}
             for term in row["terms"]]}
        for row in old["residuals"] if row["name"] != REMOVED_ROW
    ]
    history = {
        key: value for key, value in old.items()
        if key.startswith(HISTORY_PREFIXES) or key in HISTORY_KEYS
    }
    new = {key: value for key, value in old.items() if key not in history}
    new.update({
        "variables": len(new_names), "variable_names": new_names, "residuals": rows,
        "outer_coordinates": old["outer_coordinates"] - 1,
        "outer_residuals": old["outer_residuals"] - 1,
        "pell_signed_branch_predecessor_guard_metadata": history,
        "pell_signed_branch_proof": "undecidability/pell_signed_branch_v101/signed_branch_projection.tex",
        "pell_signed_branch_removed_coordinate": REMOVED_COORDINATE,
        "pell_signed_branch_removed_row": REMOVED_ROW,
        "pell_signed_branch_private_occurrences": occurrences,
        "pell_signed_branch_savings": {"coordinates": 1, "quadratic_rows": 1},
        "pell_signed_branch_projection_scope": "Same coding-prefix and instance projection; arbitrary retained signed auxiliary values need not extend to the predecessor. Positive binomial, CRT, power and integer-interface witnesses can be chosen anew.",
        "pell_signed_branch_same_auxiliary_lift_claim": False,
        "pell_signed_branch_signed_guarantees": {
            "nonzero": "s!=0 and w!=0",
            "sigma": "sign(w)",
            "power_of_two": "b*w=sigma*2^(2*r+1)",
            "first_coordinate": "c=sigma*Y_(2*r+1)(abs(a))",
            "first_trace": "d=sigma*X_(2*r+1)(a)",
            "s_sign": "sign(s)=sigma^(r+1)",
            "binomial": "n^2 divides binomial(2*r,r)",
            "fixed_power": "q=b^(5^60)",
            "auxiliary_power": "power_C=Y_(5^60)(power_A)>0 and power_D=X_(5^60)(power_A); abs(power_A)>=2",
        },
        "pell_signed_branch_zero_exclusion": "The strengthened margin makes s=0 imply c=power_C=0 and A0-1 divides5^60; the factor (b-1)*H0(b), H0(1)=25 and b>32 give a contradiction modulo125.",
        "pell_signed_branch_binomial_recovery": "Signed Pell estimates and M>=4*b give the exact alternating truncation abs(s)*M=sum_{j=0}^r binomial(2*r,j)*sigma^j*U^(r-j), U=abs(w)*M.",
        "pell_signed_branch_phi_recovery_scope": "Only after canonical positive witnesses are reselected does phi=c-(2*r+1)>0 recover the old positive coordinate.",
        "pell_signed_branch_integer_interfaces_unchanged": True,
        "pell_signed_branch_positive_completeness": "Every coding-prefix solution can be represented with all thirteen integer inputs positive, so the retained simultaneous integer-interface completeness theorems apply.",
        "pell_power_signed_branches": "The auxiliary parameter A may have either sign. C=0 and C=-Y_L(A) are excluded; C=Y_L(A)>0 and D=X_L(A), so the inverse branch D=-X_L(A) is excluded. Both first-binomial trace signs are retained.",
        "pell_signed_q_final_recovery": "Signed congruences and abs(q)*b^L+1<abs(modulus) force q=b^L>0 for either sign of A.",
        "pell_core_equivalence_scope": "Same coding-prefix and instance projection as the corrected positive source after reconstructing positive Pell and integer-interface witnesses; no identical-auxiliary lift is asserted.",
        "source_universality_verification_scope": "Reduction to the cited Jones (1980), Theorem 2, by the signed-branch binomial projection and signed auxiliary-power recovery; the coding theorem is not independently reproved.",
        "unconditional_undecidability_claim": False,
    })
    assert len(new_names) == old["variables"] - 1
    assert len(rows) == len(old["residuals"]) - 1
    assert {index for row in rows for term in row["terms"] for index in term["monomial"]} == set(ids.values())
    return new


def main():
    for interface, relative in PREDECESSORS.items():
        old_raw = (ROOT / relative).read_bytes()
        new = build_data(json.loads(old_raw))
        new["pell_signed_branch_predecessor"] = relative
        new["pell_signed_branch_predecessor_sha256"] = hashlib.sha256(old_raw).hexdigest()
        raw = (json.dumps(new, sort_keys=True, separators=(",", ":")) + "\n").encode()
        (HERE / f"signed_branch_{interface}_quadrics.json").write_bytes(raw)
        cert = {
            "interface": interface, "variables": new["variables"],
            "quadratic_rows": len(new["residuals"]), "degree": 4,
            "table_sha256": hashlib.sha256(raw).hexdigest(),
            **{key: value for key, value in new.items() if key.startswith("pell_signed_branch_")},
            "integer_blocks": new["integer_blocks"],
            "ordinary_integer_inputs": new["ordinary_integer_inputs"],
            "reciprocal_integer_inputs": new["reciprocal_integer_inputs"],
            "instance_range": new["instance_range"],
            "source_coding_theorem": new["source_coding_theorem"],
            "source_coding_theorem_independently_reproved": False,
            "source_universality_hypothesis": None,
            "retained_arithmetic_interfaces": True,
            "unconditional_undecidability_claim": False,
        }
        (HERE / f"signed_branch_{interface}_certificate.json").write_text(
            json.dumps(cert, sort_keys=True, indent=2) + "\n")
        print(json.dumps({key: cert[key] for key in (
            "interface", "variables", "quadratic_rows", "table_sha256")}))


if __name__ == "__main__":
    main()
