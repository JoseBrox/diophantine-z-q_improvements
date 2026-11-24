#!/usr/bin/env python3
"""Independent guarded Laurent rechart and full endpoint-elimination audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def polynomial(row, names):
    return sp.expand(sum(sp.sympify(term["coefficient"]) *
                         sp.prod(sp.Symbol(names[i - 1]) for i in term["monomial"])
                         for term in row["terms"]))


def verify(interface, predecessor, variables, count):
    old_raw = (ROOT / predecessor).read_bytes()
    old = json.loads(old_raw)
    path = HERE / f"endpoint_{interface}_quadrics.json"
    raw = path.read_bytes()
    data = json.loads(raw)
    cert = json.loads(path.with_name(f"endpoint_{interface}_certificate.json").read_text())
    old_names, names = old["variable_names"], data["variable_names"]
    z = sp.Symbol
    v, a1 = z("contact_common_mixed_square"), z("contact_common_fourth_coefficient_1")
    removed = [str(v), str(a1)]
    assert names == [name for name in old_names if name not in removed]
    assert len(set(names)) == len(names) == data["variables"] == variables
    old_rows = {row["name"]: polynomial(row, old_names) for row in old["residuals"]}
    rows = {row["name"]: polynomial(row, names) for row in data["residuals"]}
    deleted = {"integer.b.additive.detector1.contactSquare", "integer.b.additive.detector1.contactFourthPower"}
    assert set(rows) == set(old_rows) - deleted
    assert len(rows) == len(data["residuals"]) == count
    if interface == "general":
        k = 1
        rho, eps, eps2 = (z(f"int_b_{i}") for i in (159, 160, 161))
        inverse = z("int_b_158")
        square_multiplier, mixed_multiplier, space_multiplier = 1, 2, 1
    else:
        k = 2
        rho, eps, eps2 = (z(f"int_b_{i}") for i in (162, 163, 164))
        inverse = z("int_b_160")
        square_multiplier, mixed_multiplier, space_multiplier = rho, 4, 4
    assert rows["integer.b.unit.c_inverse"] == rho * eps - 1
    assert rows["integer.b.unit.c_inverse_square"] == eps2 - eps**2
    t, t2 = z("int_b_2"), z("int_b_68")
    u, f, u2, f2 = (z(f"int_b_{i}") for i in (60, 61, 69, 70))
    w = z("contact_common_spacing_square")
    a2, a3, a4 = (z(f"contact_common_fourth_coefficient_{j}") for j in (2, 3, 4))
    substitutions = {v: (u2-u-256*w)/32,
                     a1: (f2-f-256*a2-4096*a3-65536*a4)/16}
    recharted = [u2, f2, z("int_b_71"), inverse]
    rechart_row_names = deleted | {
        "integer.b.additive.detector1.contactCombination", "integer.b.additive.detector1.contactRelation",
        "integer.b.shared.inverse1", "integer.b.shared.gate1"}
    occurrences = {str(coordinate): [name for name, p in old_rows.items() if coordinate in p.free_symbols]
                   for coordinate in recharted}
    assert occurrences == data["contact_endpoint_rechart_occurrences"]
    assert all(set(items) <= rechart_row_names for items in occurrences.values())
    # This derives every rechart directly. The builder instead copies the
    # first-contact templates and edits the inverse/gate coefficients.
    R = z("_audit_nonzero_rho")
    gauge = {rho: R, eps: 1/R, eps2: 1/R**2}
    old_reconstruction = {coordinate: coordinate / R**k for coordinate in recharted}
    old_reconstruction.update(gauge)
    factors = {
        "integer.b.additive.detector1.contactFourthPower": 2*k,
        "integer.b.additive.detector1.contactCombination": 2*k,
        "integer.b.additive.detector1.contactRelation": 2*k,
        "integer.b.shared.inverse1": k,
    }
    changed = []
    for name, current in rows.items():
        expected = old_rows[name].xreplace(old_reconstruction).xreplace(substitutions)
        expected = sp.expand(R**factors.get(name, 0) * expected)
        multiplier = sp.sympify(data["contact_endpoint_row_multipliers"].get(name, "1"))
        assert multiplier.is_Rational and multiplier > 0
        assert sp.cancel(current.xreplace(gauge) - multiplier * expected) == 0, name
        if name in rechart_row_names or old_rows[name].free_symbols.intersection({v, a1}):
            changed.append(name)
    assert changed == data["contact_endpoint_changed_rows"]
    assert set(changed) == set(data["contact_endpoint_row_multipliers"])
    # Reconstruct the two deleted equations by exact polynomial identities,
    # before using the retained nonzero gauge to undo the rechart.
    Q0 = old_rows["integer.b.additive.detector0.contactSquare"]
    Rv = old_rows["contact.progression.mixed_square"]
    Rw = old_rows["contact.progression.spacing_square"]
    Q2 = (t2**2 - 2*eps*t2 + eps2 - eps2*u2 if interface == "general"
          else (22*t2-3)**2 - eps*u2)
    assert sp.expand((Q2-Q0+mixed_multiplier*Rv+space_multiplier*Rw).xreplace(substitutions)) == 0
    P0 = old_rows["integer.b.additive.detector0.contactFourthPower"]
    P2 = u2**2 - square_multiplier*f2
    identity = P2-P0+sum(16**j * old_rows[f"contact.progression.fourth_coefficient_{j}"] for j in range(1, 5))
    assert sp.expand(identity.xreplace(substitutions)) == 0
    for name, target in (("integer.b.additive.detector1.contactSquare", Q2),
                         ("integer.b.additive.detector1.contactFourthPower", P2)):
        reconstructed = R**factors.get(name, 0) * old_rows[name].xreplace(old_reconstruction)
        assert sp.cancel(reconstructed-target.xreplace(gauge)) == 0
    support = {index for row in data["residuals"] for term in row["terms"] for index in term["monomial"]}
    assert support == set(range(1, len(names)+1))
    assert max(len(term["monomial"]) for row in data["residuals"] for term in row["terms"]) == 2
    parameters = [z(name) for name in data["parameters"]]
    for row in data["residuals"]:
        for term in row["terms"]:
            sp.Poly(sp.sympify(term["coefficient"]), *parameters, domain=sp.ZZ)
    for key in ("ordinary_integer_inputs", "reciprocal_integer_inputs", "integer_blocks", "parameters",
                "outer_coordinates", "outer_residuals", "instance_range", "global_contact_weights",
                "source_coding_theorem", "source_universality_hypothesis", "source_coding_theorem_independently_reproved"):
        assert data.get(key) == old.get(key), key
    assert data["contact_endpoint_arithmetic_interfaces_unchanged"] is True
    assert data["source_universality_hypothesis"] is None
    assert data["source_coding_theorem_independently_reproved"] is False
    assert data["unconditional_undecidability_claim"] is False
    assert data["contact_endpoint_predecessor"] == predecessor
    assert data["contact_endpoint_predecessor_sha256"] == hashlib.sha256(old_raw).hexdigest()
    digest = hashlib.sha256(raw).hexdigest()
    assert cert["table_sha256"] == digest
    assert (cert["variables"], cert["quadratic_rows"], cert["degree"]) == (variables, count, 4)
    return {"interface": interface, "status": "PASS", "variables": variables, "quadratic_rows": count,
            "changed_rows_checked": len(changed), "unchanged_rows_checked": len(rows)-len(changed),
            "recharted_coordinates": 4, "deleted_row_identities": 2, "gauge_guards_checked": 2,
            "table_sha256": digest}


def main():
    reports = [
        verify("general", "undecidability/pell_signed_branch_v101/signed_branch_general_quadrics.json", 968, 823),
        verify("specified", "undecidability/aggregate_spacing_v100/aggregate_spacing_specified_quadrics.json", 1143, 994),
    ]
    print(json.dumps({"tables": reports,
                      "scope": "No builder imported. Every rechart is derived by guarded Laurent substitution; both omitted rows have exact reconstruction identities."},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
