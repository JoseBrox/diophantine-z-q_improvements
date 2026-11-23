#!/usr/bin/env python3
"""Independent full coefficient and guard audit, plus exact local fixtures."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def expression(row, names):
    return sp.expand(sum(sp.sympify(term["coefficient"]) *
                         sp.prod(sp.Symbol(names[i - 1]) for i in term["monomial"])
                         for term in row["terms"]))


def verify(interface, expected_variables, expected_rows):
    path = HERE / f"aggregate_spacing_{interface}_quadrics.json"
    raw = path.read_bytes()
    data = json.loads(raw)
    certificate = json.loads(path.with_name(f"aggregate_spacing_{interface}_certificate.json").read_text())
    predecessor = f"undecidability/pell_product_v99/product_{interface}_quadrics.json"
    old_raw = (ROOT / predecessor).read_bytes()
    old = json.loads(old_raw)
    spacing = "contact_common_spacing"
    names, old_names = data["variable_names"], old["variable_names"]
    assert names == [name for name in old_names if name != spacing]
    assert len(set(names)) == len(names) == data["variables"] == expected_variables
    rows = {row["name"]: row for row in data["residuals"]}
    old_rows = {row["name"]: row for row in old["residuals"]}
    assert set(rows) == set(old_rows)
    assert len(rows) == len(data["residuals"]) == expected_rows
    d = sp.Symbol(spacing)
    replacement = (sp.Symbol("int_b_68") - sp.Symbol("int_b_2")) / 16
    changed = []
    for name, old_row in old_rows.items():
        previous = expression(old_row, old_names)
        expected = sp.expand(previous.subs(d, replacement))
        multiplier = sp.sympify(data["aggregate_spacing_row_multipliers"].get(name, "1"))
        assert multiplier.is_Rational and multiplier > 0
        assert sp.expand(expression(rows[name], names) - multiplier * expected) == 0, name
        if d in previous.free_symbols:
            changed.append(name)
    assert changed == data["aggregate_spacing_changed_rows"]
    assert set(changed) == set(data["aggregate_spacing_row_multipliers"])
    assert spacing not in {str(symbol) for row in rows.values() for symbol in expression(row, names).free_symbols}
    support = {index for row in rows.values() for term in row["terms"] for index in term["monomial"]}
    assert support == set(range(1, len(names) + 1))
    assert max(len(term["monomial"]) for row in rows.values() for term in row["terms"]) == 2
    parameters = [sp.Symbol(name) for name in data["parameters"]]
    for row in rows.values():
        for term in row["terms"]:
            sp.Poly(sp.sympify(term["coefficient"]), *parameters, domain=sp.ZZ)
    for key in ("ordinary_integer_inputs", "reciprocal_integer_inputs", "integer_blocks", "parameters",
                "outer_coordinates", "outer_residuals", "instance_range", "source_coding_theorem",
                "source_universality_hypothesis", "source_coding_theorem_independently_reproved",
                "affine_contact_active_indices", "global_contact_weights"):
        assert data.get(key) == old.get(key), key
    assert set(data["aggregate_spacing_contact_indices"]) <= set(range(16))
    assert data["aggregate_spacing_interface_hypotheses_unchanged"] is True
    assert data["source_universality_hypothesis"] is None
    assert data["source_coding_theorem_independently_reproved"] is False
    assert data["unconditional_undecidability_claim"] is False
    aggregate = expression(rows["integer.b.new.aggregate"], names)
    t, tprime = sp.Symbol("int_b_2"), sp.Symbol("int_b_68")
    if interface == "general":
        rho = sp.Symbol("int_b_159")
        assert sp.diff(aggregate, t) == 2 * rho
        assert sp.diff(aggregate, tprime) == -2 * rho
    else:
        assert sp.diff(aggregate, t) == 2
        assert sp.diff(aggregate, tprime) == -2
    assert data["aggregate_spacing_predecessor"] == predecessor
    assert data["aggregate_spacing_predecessor_sha256"] == hashlib.sha256(old_raw).hexdigest()
    digest = hashlib.sha256(raw).hexdigest()
    assert certificate["table_sha256"] == digest
    assert certificate["variables"] == expected_variables
    assert certificate["quadratic_rows"] == expected_rows
    return {"interface": interface, "status": "PASS", "variables": expected_variables,
            "quadratic_rows": expected_rows, "changed_rows_checked": len(changed),
            "unchanged_rows_checked": len(rows) - len(changed), "table_sha256": digest}


def lucas_mod(index, parameter, modulus):
    matrix = (parameter % modulus, -1 % modulus, 1, 0)
    value = (1, 0, 0, 1)
    def multiply(x, y):
        return ((x[0]*y[0]+x[1]*y[2]) % modulus,
                (x[0]*y[1]+x[1]*y[3]) % modulus,
                (x[2]*y[0]+x[3]*y[2]) % modulus,
                (x[2]*y[1]+x[3]*y[3]) % modulus)
    while index:
        if index & 1:
            value = multiply(value, matrix)
        matrix = multiply(matrix, matrix)
        index >>= 1
    return value[2]


def local_fixtures():
    checked = 0
    for depth in range(2, 17):
        for odd in (1, 3, 5, 7, 11):
            a = 3 * (2**depth) * odd
            modulus = 2**(2*depth+4)
            t = lucas_mod(a, a+1, modulus)
            difference = (lucas_mod(a-1, a+1, modulus) - (a-1)) % modulus
            assert t % 2**(2*depth+2) == 2**(2*depth+1)
            assert difference % 2**(depth+1) == 2**depth
            checked += 1
    for i in range(16):
        for j in range(i):
            assert (i-j) % 16 != 0
    return {"lucas_exact_modular_fixtures": checked, "index_difference_fixtures": 120,
            "scope": "Finite exact local fixtures support, but do not replace, the quantified proof."}


def main():
    reports = [verify("general", 971, 826), verify("specified", 1145, 996)]
    print(json.dumps({"tables": reports, "local_fixtures": local_fixtures(),
                      "checker_scope": "Independent affine substitution, full coefficient/support/guard/metadata/hash audit; no builder imported."},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
