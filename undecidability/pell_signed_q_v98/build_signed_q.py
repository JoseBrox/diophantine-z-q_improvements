#!/usr/bin/env python3
"""Remove both new Pell-power wrappers, absorbing the index bound into eta."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSORS = {
    "general": "undecidability/pell_power_v97/power_general_m163_quadrics.json",
    "abc": "undecidability/pell_power_v97/pell_power_abc_quadrics.json",
}
REMOVED_ROWS = [f"jones1980.pell_power.positive.{kind}" for kind in ("q", "bound")]
REMOVED_COORDINATES = [f"power_positive_{kind}_{i}" for kind in ("q", "bound") for i in (1, 2, 3)]
CHANGED_ROW = "jones1980.positive.eta"


def build_data(old, interface):
    old_names = old["variable_names"]
    assert old["pell_power_new_integer_inputs_certified"] is True
    assert old["source_universality_hypothesis"] is None
    assert old["pell_power_bounds"] == ["q > b^5", "C^2 < c^2"]
    occurrences = {
        name: [row["name"] for row in old["residuals"]
               if any(name == old_names[i - 1]
                      for term in row["terms"] for i in term["monomial"])]
        for name in REMOVED_COORDINATES
    }
    assert all(rows == [REMOVED_ROWS[0 if "_q_" in name else 1]]
               for name, rows in occurrences.items())
    removed_coordinates = list(REMOVED_COORDINATES)
    removed_rows = list(REMOVED_ROWS)
    aliases = {}
    if interface == "abc":
        removed_coordinates.append("power_b4")
        removed_rows.append("jones1980.pell_power.b4.definition")
        aliases["power_b4"] = "int_b_30"
        occurrences["power_b4"] = [row["name"] for row in old["residuals"]
                                  if any(old_names[i - 1] == "power_b4"
                                         for term in row["terms"] for i in term["monomial"])]
        assert set(occurrences["power_b4"]) == {
            "jones1980.B5.definition", "jones1980.pell_power.b4.definition", "jones1980.pell_power.A.definition"}
    new_names = [name for name in old_names if name not in removed_coordinates]
    ids = {name: i + 1 for i, name in enumerate(new_names)}
    rows = []
    for row in old["residuals"]:
        if row["name"] in removed_rows:
            continue
        terms = [
            {"coefficient": term["coefficient"],
             "monomial": sorted(ids[aliases.get(old_names[i - 1], old_names[i - 1])]
                                for i in term["monomial"])}
            for term in row["terms"]]
        if row["name"] == CHANGED_ROW:
            assert all(ids["power_C"] not in term["monomial"] for term in terms)
            terms.append({"coefficient": "-2", "monomial": [ids["power_C"], ids["power_C"]]})
            terms.sort(key=lambda term: term["monomial"])
        rows.append({"name": row["name"], "terms": terms})
    new = dict(old)
    new.update({
        "variables": len(new_names), "variable_names": new_names, "residuals": rows,
        "outer_coordinates": old["outer_coordinates"] - len(removed_coordinates),
        "outer_residuals": old["outer_residuals"] - len(removed_rows),
        "pell_power_predecessor_bounds": old["pell_power_bounds"],
        "pell_power_bounds": ["k^2-4*(c-k*Y)^2-C^2>0 (absorbed in the retained eta margin)"],
        "pell_power_new_positivity_coordinates": [
            name for name in old["pell_power_new_positivity_coordinates"]
            if name not in REMOVED_COORDINATES],
        "pell_signed_q_proof": "undecidability/pell_signed_q_v98/signed_q_and_absorbed_bound.tex",
        "pell_signed_q_removed_coordinates": removed_coordinates,
        "pell_signed_q_removed_rows": removed_rows,
        "pell_signed_q_changed_row": CHANGED_ROW,
        "pell_signed_q_private_occurrences": occurrences,
        "pell_signed_q_savings": {"coordinates": len(removed_coordinates), "quadratic_rows": len(removed_rows)},
        "pell_signed_q_preliminary_bound": "Q=abs(q)>=b^5-2; no preliminary sign of q is imposed",
        "pell_signed_q_prefix_bounds": "S>14*Q^7 and abs(T)<2*Q^7 imply r>=M; x>32*z is retained",
        "pell_signed_q_final_recovery": "Signed congruences and Q*b^L+1<modulus force q=b^L>0",
        "pell_signed_q_projection_scope": "Same coding-prefix and instance projection as the predecessor; q=b^L and C^2<c^2 follow from the new system, and canonical completeness has eta-C^2>0",
        "pell_signed_q_integer_inputs_unchanged": True,
        "pell_signed_q_absorbed_bound": "The retained eta margin is k^2-4*(c-k*Y)^2-power_C^2>0; it implies abs(power_C)<abs(k)<abs(c)",
        "pell_signed_q_absorbed_bound_completeness": "Canonical eta>=k and power_C^2<p^(L-1)<k, using p>4*A^2 and r>L",
        "pell_signed_q_retained_integer_interfaces": True,
        "unconditional_undecidability_claim": False,
    })
    if interface == "abc":
        new["pell_power_new_registers"] = [name for name in old["pell_power_new_registers"] if name != "power_b4"]
        new["pell_signed_q_abc_reused_fourth"] = "int_b_30=b^4, forced by retained integer.b.height.betaSquare and betaFourth rows"
        new["pell_signed_q_abc_fourth_substitution"] = aliases
        new["pell_signed_q_abc_fourth_changed_rows"] = ["jones1980.B5.definition", "jones1980.pell_power.A.definition"]
    assert len(rows) == len(old["residuals"]) - len(removed_rows)
    assert len(new_names) == old["variables"] - len(removed_coordinates)
    assert {i for row in rows for term in row["terms"] for i in term["monomial"]} == set(ids.values())
    return new


def main():
    for interface, relative in PREDECESSORS.items():
        source = ROOT / relative
        raw = source.read_bytes()
        old = json.loads(raw)
        new = build_data(old, interface)
        new["pell_signed_q_predecessor"] = relative
        new["pell_signed_q_predecessor_sha256"] = hashlib.sha256(raw).hexdigest()
        output = (json.dumps(new, sort_keys=True, separators=(",", ":")) + "\n").encode()
        path = HERE / f"signed_q_{interface}_quadrics.json"
        path.write_bytes(output)
        certificate = {
            "interface": interface,
            "variables": new["variables"], "quadratic_rows": len(new["residuals"]),
            "degree": 4, "table_sha256": hashlib.sha256(output).hexdigest(),
            **{key: value for key, value in new.items() if key.startswith("pell_signed_q_")},
            "ordinary_integer_inputs": new["ordinary_integer_inputs"],
            "reciprocal_integer_inputs": new["reciprocal_integer_inputs"],
            "source_universality_hypothesis": None,
            "source_coding_theorem": new["source_coding_theorem"],
            "source_coding_theorem_independently_reproved": False,
            "retained_arithmetic_interfaces": True,
            "unconditional_undecidability_claim": False,
        }
        path.with_name(f"signed_q_{interface}_certificate.json").write_text(
            json.dumps(certificate, sort_keys=True, indent=2) + "\n")
        print(json.dumps({key: certificate[key] for key in (
            "interface", "variables", "quadratic_rows", "table_sha256")}))


if __name__ == "__main__":
    main()
