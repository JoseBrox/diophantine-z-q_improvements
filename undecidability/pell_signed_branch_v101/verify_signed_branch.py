#!/usr/bin/env python3
"""Independent complete coefficient, support and semantic-metadata audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def named(row, names):
    result = {}
    for term in row["terms"]:
        monomial = tuple(sorted(names[index - 1] for index in term["monomial"]))
        result[monomial] = result.get(monomial, 0) + sp.sympify(term["coefficient"])
    return {monomial: sp.expand(coefficient) for monomial, coefficient in result.items() if coefficient}


def verify(interface, predecessor, variables, row_count):
    old_raw = (ROOT / predecessor).read_bytes()
    old = json.loads(old_raw)
    raw = (HERE / f"signed_branch_{interface}_quadrics.json").read_bytes()
    data = json.loads(raw)
    cert = json.loads((HERE / f"signed_branch_{interface}_certificate.json").read_text())
    deleted_coordinate = "pell_d_positive_square"
    deleted_row = "jones1980.pell_positive_root"
    old_rows = {row["name"]: named(row, old["variable_names"]) for row in old["residuals"]}
    rows = {row["name"]: named(row, data["variable_names"]) for row in data["residuals"]}
    assert data["variable_names"] == [name for name in old["variable_names"] if name != deleted_coordinate]
    assert len(set(data["variable_names"])) == len(data["variable_names"]) == data["variables"] == variables
    assert len(rows) == len(data["residuals"]) == row_count
    assert set(rows) == set(old_rows) - {deleted_row}
    assert old_rows[deleted_row] == {
        (): -2, ("c",): 2, ("a", "d"): -2,
        ("a", "ac"): -2, (deleted_coordinate, deleted_coordinate): 1}
    occurrences = [
        name for name, polynomial in old_rows.items()
        if any(deleted_coordinate in monomial for monomial in polynomial)
    ]
    assert occurrences == [deleted_row]
    for name, polynomial in rows.items():
        assert polynomial == old_rows[name], name
    support = {name for polynomial in rows.values() for monomial in polynomial for name in monomial}
    assert support == set(data["variable_names"])
    assert deleted_coordinate not in support
    assert max(len(monomial) for polynomial in rows.values() for monomial in polynomial) == 2
    parameter_symbols = [sp.Symbol(name) for name in data["parameters"]]
    for polynomial in rows.values():
        for coefficient in polynomial.values():
            assert coefficient.free_symbols <= set(parameter_symbols)
            sp.Poly(coefficient, *parameter_symbols, domain=sp.ZZ)
    for key in ("M_recovery", "a_recovery", "ordinary_integer_inputs", "reciprocal_integer_inputs",
                "integer_blocks", "parameters", "instance_range", "source_coding_theorem",
                "pell_power_bounds", "pell_power_new_integer_inputs_certified",
                "source_universality_hypothesis", "source_coding_theorem_independently_reproved"):
        assert data.get(key) == old.get(key), key
    assert data["integer_blocks"] == 13
    assert data["instance_range"] == "positive integer x > 32*z"
    assert data["outer_coordinates"] == old["outer_coordinates"] - 1
    assert data["outer_residuals"] == old["outer_residuals"] - 1
    assert data["pell_signed_branch_same_auxiliary_lift_claim"] is False
    assert data["pell_signed_branch_integer_interfaces_unchanged"] is True
    assert data["source_universality_hypothesis"] is None
    assert data["source_coding_theorem_independently_reproved"] is False
    assert data["unconditional_undecidability_claim"] is False
    prefixes = ("pell_halftrace_", "signed_binomial_positivity_")
    history_keys = {
        "pell_core_positive_root", "phi_recovery", "pell_power_signed_branches",
        "pell_signed_q_final_recovery", "pell_core_equivalence_scope",
        "source_universality_verification_scope"}
    history = {key: value for key, value in old.items()
               if key.startswith(prefixes) or key in history_keys}
    assert data["pell_signed_branch_predecessor_guard_metadata"] == history
    assert not any(key.startswith(prefixes) for key in data)
    assert "pell_core_positive_root" not in data and "phi_recovery" not in data
    assert data["pell_signed_branch_signed_guarantees"] == {
        "nonzero": "s!=0 and w!=0", "sigma": "sign(w)",
        "power_of_two": "b*w=sigma*2^(2*r+1)",
        "first_coordinate": "c=sigma*Y_(2*r+1)(abs(a))",
        "first_trace": "d=sigma*X_(2*r+1)(a)",
        "s_sign": "sign(s)=sigma^(r+1)",
        "binomial": "n^2 divides binomial(2*r,r)",
        "fixed_power": "q=b^(5^60)",
        "auxiliary_power": "power_C=Y_(5^60)(power_A)>0 and power_D=X_(5^60)(power_A); abs(power_A)>=2"}
    assert "abs(modulus)" in data["pell_signed_q_final_recovery"]
    assert "either sign" in data["pell_power_signed_branches"]
    assert data["pell_signed_branch_predecessor"] == predecessor
    assert data["pell_signed_branch_predecessor_sha256"] == hashlib.sha256(old_raw).hexdigest()
    assert data["pell_signed_branch_private_occurrences"] == occurrences
    sha256 = hashlib.sha256(raw).hexdigest()
    assert cert["table_sha256"] == sha256
    assert (cert["variables"], cert["quadratic_rows"], cert["degree"]) == (variables, row_count, 4)
    assert cert["pell_signed_branch_same_auxiliary_lift_claim"] is False
    return {"interface": interface, "status": "PASS", "variables": variables,
            "quadratic_rows": row_count, "unchanged_rows_checked": row_count,
            "table_sha256": sha256,
            "scope": "Exact deletion, complete unchanged-row audit, support, coefficient integrality, degree, current versus historical sign metadata, and hashes; quantified projection theorem is proved separately."}


def main():
    reports = [
        verify("general", "undecidability/aggregate_spacing_v100/aggregate_spacing_general_quadrics.json", 970, 825),
        verify("abc", "undecidability/pell_product_v99/product_abc_quadrics.json", 695, 590),
    ]
    print(json.dumps(reports, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
