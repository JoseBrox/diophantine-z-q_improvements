#!/usr/bin/env python3
"""Independent exact coefficient/support audit; imports no builder."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def named(row, names):
    result = {}
    for term in row["terms"]:
        monomial = tuple(sorted(names[index - 1] for index in term["monomial"]))
        result[monomial] = result.get(monomial, sp.Integer(0)) + sp.sympify(term["coefficient"])
    return {monomial: sp.expand(coefficient) for monomial, coefficient in result.items() if coefficient}


def verify(interface, predecessor, expected_variables, expected_rows):
    old_bytes = (ROOT / predecessor).read_bytes()
    old = json.loads(old_bytes)
    table_path = HERE / f"signed_q_{interface}_quadrics.json"
    data_bytes = table_path.read_bytes()
    data = json.loads(data_bytes)
    certificate = json.loads(table_path.with_name(f"signed_q_{interface}_certificate.json").read_text())
    removed = {f"power_positive_{kind}_{j}" for kind in ("q", "bound") for j in range(1, 4)}
    removed_rows = {f"jones1980.pell_power.positive.{kind}" for kind in ("q", "bound")}
    changed_row = "jones1980.positive.eta"
    if interface == "abc":
        removed.add("power_b4")
        removed_rows.add("jones1980.pell_power.b4.definition")
    assert data["variable_names"] == [name for name in old["variable_names"] if name not in removed]
    assert len(set(data["variable_names"])) == data["variables"] == expected_variables
    old_rows = {row["name"]: named(row, old["variable_names"]) for row in old["residuals"]}
    rows = {row["name"]: named(row, data["variable_names"]) for row in data["residuals"]}
    assert len(rows) == len(data["residuals"]) == expected_rows
    assert set(rows) == set(old_rows) - removed_rows
    for kind in ("q", "bound"):
        expected_removed = ({(): Fraction(-2), ("q",): Fraction(2), ("B5",): Fraction(-2)}
                            if kind == "q" else
                            {(): Fraction(-2), ("c", "c"): Fraction(2), ("power_C", "power_C"): Fraction(-2)})
        for j in range(1, 4):
            name = f"power_positive_{kind}_{j}"
            expected_removed[(name,)] = Fraction(-1)
            expected_removed[(name, name)] = Fraction(-1)
        assert old_rows[f"jones1980.pell_power.positive.{kind}"] == expected_removed
    for name in rows:
        expected = dict(old_rows[name])
        if name == changed_row:
            assert ("power_C", "power_C") not in expected
            expected[("power_C", "power_C")] = Fraction(-2)
        if interface == "abc":
            expected = {tuple(sorted("int_b_30" if variable == "power_b4" else variable
                                     for variable in monomial)): coefficient
                        for monomial, coefficient in expected.items()}
        assert rows[name] == expected, name
        assert not removed.intersection(variable for monomial in rows[name] for variable in monomial)
    for variable in removed:
        if variable == "power_b4":
            assert {name for name, polynomial in old_rows.items()
                    if any(variable in monomial for monomial in polynomial)} == {
                        "jones1980.B5.definition", "jones1980.pell_power.A.definition", "jones1980.pell_power.b4.definition"}
            continue
        assert [name for name, polynomial in old_rows.items()
                if any(variable in monomial for monomial in polynomial)] == [
                    f"jones1980.pell_power.positive.{'q' if '_q_' in variable else 'bound'}"]
    assert max(len(monomial) for polynomial in rows.values() for monomial in polynomial) == 2
    support = {variable for polynomial in rows.values() for monomial in polynomial for variable in monomial}
    assert support == set(data["variable_names"])
    for key in ("ordinary_integer_inputs", "reciprocal_integer_inputs", "integer_blocks", "parameters",
                "source_coding_theorem", "retained_arithmetic_interfaces", "instance_range"):
        assert data[key] == old[key], key
    assert data["pell_power_new_integer_inputs_certified"] is True
    assert data["pell_signed_q_integer_inputs_unchanged"] is True
    assert data["source_universality_hypothesis"] is None
    assert data["source_coding_theorem_independently_reproved"] is False
    assert data["unconditional_undecidability_claim"] is False
    assert data["pell_power_bounds"] == ["k^2-4*(c-k*Y)^2-C^2>0 (absorbed in the retained eta margin)"]
    assert data["pell_power_new_positivity_coordinates"] == []
    assert data["outer_coordinates"] == old["outer_coordinates"] - len(removed)
    assert data["outer_residuals"] == old["outer_residuals"] - len(removed_rows)
    if interface == "abc":
        assert rows["integer.b.height.betaSquare"] == {("b", "b"): 1, ("int_b_29",): -1}
        assert rows["integer.b.height.betaFourth"] == {("int_b_29", "int_b_29"): 1, ("int_b_30",): -1}
        assert old_rows["jones1980.pell_power.b4.definition"] == {
            ("int_b_29", "int_b_29"): -1, ("power_b4",): 1}
        assert data["pell_power_new_registers"] == [name for name in old["pell_power_new_registers"] if name != "power_b4"]
        assert data["pell_signed_q_abc_fourth_substitution"] == {"power_b4": "int_b_30"}
    assert data["pell_signed_q_predecessor"] == predecessor
    assert data["pell_signed_q_predecessor_sha256"] == hashlib.sha256(old_bytes).hexdigest()
    sha256 = hashlib.sha256(data_bytes).hexdigest()
    assert certificate["table_sha256"] == sha256
    assert certificate["variables"] == expected_variables
    assert certificate["quadratic_rows"] == expected_rows
    return {"status": "PASS", "interface": interface, "variables": expected_variables,
            "quadratic_rows": expected_rows, "unchanged_rows_checked": len(rows) - (3 if interface == "abc" else 1),
            "strengthened_margin_rows_checked": 1,
            "deleted_private_wrapper_coordinates_checked": 6,
            "reused_fourth_power_rows_checked": 2 if interface == "abc" else 0,
            "table_sha256": sha256,
            "scope": "Complete exact coefficient, support, metadata and hash audit; signed-q arithmetic is proved separately."}


def main():
    reports = [
        verify("general", "undecidability/pell_power_v97/power_general_m163_quadrics.json", 973, 827),
        verify("abc", "undecidability/pell_power_v97/pell_power_abc_quadrics.json", 697, 592),
    ]
    print(json.dumps(reports, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
