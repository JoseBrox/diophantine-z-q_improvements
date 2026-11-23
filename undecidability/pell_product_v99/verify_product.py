#!/usr/bin/env python3
"""Independent polynomial identity, full coefficient, support and metadata audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def named(row, names):
    polynomial = {}
    for term in row["terms"]:
        monomial = tuple(sorted(names[index - 1] for index in term["monomial"]))
        polynomial[monomial] = polynomial.get(monomial, 0) + sp.sympify(term["coefficient"])
    return {monomial: sp.expand(coefficient) for monomial, coefficient in polynomial.items() if coefficient}


def verify(interface, predecessor, variables, residuals):
    old_raw = (ROOT / predecessor).read_bytes()
    old = json.loads(old_raw)
    raw = (HERE / f"product_{interface}_quadrics.json").read_bytes()
    new = json.loads(raw)
    cert = json.loads((HERE / f"product_{interface}_certificate.json").read_text())
    removed_row = "jones1980.sr2.definition"
    changed_row = "jones1980.p.definition"
    retained_row = "jones1980.a.definition"
    old_rows = {row["name"]: named(row, old["variable_names"]) for row in old["residuals"]}
    rows = {row["name"]: named(row, new["variable_names"]) for row in new["residuals"]}
    assert new["variable_names"] == [name for name in old["variable_names"] if name != "sr2"]
    assert len(set(new["variable_names"])) == len(new["variable_names"]) == new["variables"] == variables
    assert len(rows) == len(new["residuals"]) == residuals
    assert set(rows) == set(old_rows) - {removed_row}
    assert old_rows[removed_row] == {("sr2",): 1, ("sr", "sr"): -1}
    assert old_rows[changed_row] == {("p",): 1, ("U", "sr2"): -2}
    assert old_rows[retained_row] == {("a",): 1, ("sr",): -1, ("U", "sr"): -1}
    assert rows[changed_row] == {("p",): 1, ("a", "sr"): -2, ("sr", "sr"): 2}
    occurrences = [
        name for name, polynomial in old_rows.items()
        if any("sr2" in monomial for monomial in polynomial)
    ]
    assert occurrences == [removed_row, changed_row]
    for name, polynomial in rows.items():
        if name != changed_row:
            assert polynomial == old_rows[name], name
    support = {name for polynomial in rows.values() for monomial in polynomial for name in monomial}
    assert support == set(new["variable_names"])
    assert "sr2" not in support
    assert max(len(monomial) for polynomial in rows.values() for monomial in polynomial) == 2
    for polynomial in rows.values():
        for coefficient in polynomial.values():
            assert coefficient.free_symbols <= {sp.Symbol(name) for name in new["parameters"]}
            sp.Poly(coefficient, *[sp.Symbol(name) for name in new["parameters"]], domain=sp.ZZ)
    for key in ("M_recovery", "a_recovery", "ordinary_integer_inputs", "reciprocal_integer_inputs",
                "integer_blocks", "parameters", "instance_range", "source_coding_theorem",
                "source_universality_hypothesis", "source_coding_theorem_independently_reproved"):
        assert new.get(key) == old.get(key), key
    assert new["M_recovery"] == "sr"
    assert new["a_recovery"] == "(U+1)*sr"
    assert new["outer_coordinates"] == old["outer_coordinates"] - 1
    assert new["outer_residuals"] == old["outer_residuals"] - 1
    assert new["pell_product_integer_interfaces_unchanged"] is True
    assert new["source_universality_hypothesis"] is None
    assert new["source_coding_theorem_independently_reproved"] is False
    assert new["unconditional_undecidability_claim"] is False
    assert new["pell_product_private_occurrences"] == occurrences
    assert new["pell_product_predecessor_register_metadata"]["source_repair_reused_register"] == old["source_repair_reused_register"]
    assert "sr2" not in new["source_repair_reused_register"]
    assert new["pell_product_predecessor"] == predecessor
    assert new["pell_product_predecessor_sha256"] == hashlib.sha256(old_raw).hexdigest()
    sha256 = hashlib.sha256(raw).hexdigest()
    assert cert["table_sha256"] == sha256
    assert (cert["variables"], cert["quadratic_rows"], cert["degree"]) == (variables, residuals, 4)
    return {"interface": interface, "status": "PASS", "variables": variables,
            "quadratic_rows": residuals, "unchanged_rows_checked": residuals - 1,
            "table_sha256": sha256}


def main():
    p, U, a, sr, sr2 = sp.symbols("p U a sr sr2")
    old_p = p - 2 * U * sr2
    old_square = sr2 - sr**2
    retained_a = a - (U + 1) * sr
    new_p = p - 2 * a * sr + 2 * sr**2
    assert sp.expand(new_p - old_p - 2 * U * old_square + 2 * sr * retained_a) == 0
    assert sp.expand(old_p.subs(sr2, sr**2) - new_p - 2 * sr * retained_a) == 0
    reports = [
        verify("general", "undecidability/pell_signed_q_v98/signed_q_general_quadrics.json", 972, 826),
        verify("specified", "undecidability/pell_halftrace_v96/halftrace_m179_quadrics.json", 1146, 996),
        verify("abc", "undecidability/pell_signed_q_v98/signed_q_abc_quadrics.json", 696, 591),
    ]
    print(json.dumps({"polynomial_identities": 2, "tables": reports,
                      "scope": "No builder imported; exact algebraic equivalence and complete coefficient/support/metadata/hash audit."},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
