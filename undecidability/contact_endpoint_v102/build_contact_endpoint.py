#!/usr/bin/env python3
"""Rechart the root second contact and reuse its two endpoint powers."""
from __future__ import annotations

import hashlib
import json
from math import gcd, lcm
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSORS = {
    "general": "undecidability/pell_signed_branch_v101/signed_branch_general_quadrics.json",
    "specified": "undecidability/aggregate_spacing_v100/aggregate_spacing_specified_quadrics.json",
}
REMOVED = ["contact_common_mixed_square", "contact_common_fourth_coefficient_1"]
DELETED_ROWS = ["integer.b.additive.detector1.contactSquare", "integer.b.additive.detector1.contactFourthPower"]


def expr(row, names):
    return sp.expand(sum(sp.sympify(term["coefficient"]) *
                         sp.prod(sp.Symbol(names[i - 1]) for i in term["monomial"])
                         for term in row["terms"]))


def encode(name, polynomial, names, parameters):
    ids = {name: i + 1 for i, name in enumerate(names)}
    coordinate_symbols = {sp.Symbol(name) for name in names}
    used = sorted(polynomial.free_symbols.intersection(coordinate_symbols), key=str)
    entries = sp.Poly(sp.expand(polynomial), *used).terms()
    parameter_symbols = [sp.Symbol(name) for name in parameters]
    coefficients = [q for _, c in entries for q in sp.Poly(c, *parameter_symbols).coeffs()]
    denominator = lcm(*(int(q.q) for q in coefficients))
    content = 0
    for q in coefficients:
        content = gcd(content, abs(int(denominator * q)))
    multiplier = sp.Rational(denominator, content)
    terms = []
    for powers, coefficient in entries:
        monomial = sorted(ids[str(symbol)] for symbol, power in zip(used, powers) for _ in range(power))
        assert len(monomial) <= 2
        terms.append({"coefficient": str(sp.expand(multiplier * coefficient)), "monomial": monomial})
    return {"name": name, "terms": sorted(terms, key=lambda term: term["monomial"])}, str(multiplier)


def build_data(old, interface):
    old_names = old["variable_names"]
    old_rows = {row["name"]: row for row in old["residuals"]}
    z = sp.Symbol
    if interface == "general":
        inverse_old, inverse_new, gauge_power = "int_b_157", "int_b_158", 1
        rho, epsilon, epsilon2, weight = "int_b_159", "int_b_160", "int_b_161", "int_b_last_contact_weight"
    else:
        inverse_old, inverse_new, gauge_power = "int_b_159", "int_b_160", 2
        rho, epsilon, epsilon2, weight = "int_b_162", "int_b_163", "int_b_164", "int_b_155"
    recharted = ["int_b_69", "int_b_70", "int_b_71", inverse_new]
    rechart_rows = DELETED_ROWS + ["integer.b.additive.detector1.contactCombination",
                                  "integer.b.additive.detector1.contactRelation",
                                  "integer.b.shared.inverse1", "integer.b.shared.gate1"]
    occurrences = {}
    for coordinate in recharted:
        occurrences[coordinate] = [row["name"] for row in old["residuals"]
                                   if any(old_names[i - 1] == coordinate
                                          for term in row["terms"] for i in term["monomial"])]
        assert set(occurrences[coordinate]) <= set(rechart_rows)
    root_to_second = {z("int_b_2"): z("int_b_68"), z("int_b_60"): z("int_b_69"),
                      z("int_b_61"): z("int_b_70"), z("int_b_62"): z("int_b_71"),
                      z(inverse_old): z(inverse_new)}
    changed_expressions = {}
    for suffix in ("contactCombination", "contactRelation"):
        source = "integer.b.additive.detector0." + suffix
        target = "integer.b.additive.detector1." + suffix
        changed_expressions[target] = expr(old_rows[source], old_names).xreplace(root_to_second)
    inverse_term = z(epsilon2 if interface == "general" else epsilon)
    changed_expressions["integer.b.shared.inverse1"] = inverse_term - z(weight) * z(inverse_new)
    old_gate = expr(old_rows["integer.b.shared.gate1"], old_names)
    previous_factor = z(epsilon if interface == "general" else rho)
    target_factor = z(epsilon2 if interface == "general" else epsilon)
    changed_expressions["integer.b.shared.gate1"] = sp.expand(
        old_gate + z(inverse_new) * previous_factor - z(inverse_new) * target_factor)
    u, f = z("int_b_60"), z("int_b_61")
    u2, f2 = z("int_b_69"), z("int_b_70")
    w = z("contact_common_spacing_square")
    a2, a3, a4 = (z(f"contact_common_fourth_coefficient_{j}") for j in (2, 3, 4))
    replacements = {z(REMOVED[0]): (u2-u-256*w)/32,
                    z(REMOVED[1]): (f2-f-256*a2-4096*a3-65536*a4)/16}
    names = [name for name in old_names if name not in REMOVED]
    ids = {name: i + 1 for i, name in enumerate(names)}
    rows, changed, multipliers = [], [], {}
    for row in old["residuals"]:
        name = row["name"]
        if name in DELETED_ROWS:
            continue
        has_removed = any(old_names[i - 1] in REMOVED for term in row["terms"] for i in term["monomial"])
        if name in changed_expressions or has_removed:
            polynomial = changed_expressions.get(name, expr(row, old_names))
            polynomial = sp.expand(polynomial.xreplace(replacements))
            encoded, multiplier = encode(name, polynomial, names, old["parameters"])
            rows.append(encoded)
            changed.append(name)
            multipliers[name] = multiplier
        else:
            rows.append({"name": name, "terms": [
                {"coefficient": term["coefficient"],
                 "monomial": sorted(ids[old_names[i - 1]] for i in term["monomial"])}
                for term in row["terms"]]})
    new = dict(old)
    new.update({
        "variables": len(names), "variable_names": names, "residuals": rows,
        "affine_contact_new_coordinates": [name for name in old["affine_contact_new_coordinates"] if name not in REMOVED],
        "contact_endpoint_proof": "undecidability/contact_endpoint_v102/contact_endpoint_reuse.tex",
        "contact_endpoint_removed_coordinates": REMOVED,
        "contact_endpoint_removed_rows": DELETED_ROWS,
        "contact_endpoint_recharted_coordinates": recharted,
        "contact_endpoint_rechart_occurrences": occurrences,
        "contact_endpoint_rechart": f"For each listed register, old_value=epsilon^{gauge_power}*new_value; epsilon=1/rho is already guarded",
        "contact_endpoint_gauge_power": gauge_power,
        "contact_endpoint_gauge_coordinates": {"rho": rho, "epsilon": epsilon, "epsilon2": epsilon2},
        "contact_endpoint_substitution": {str(symbol): str(sp.expand(value)) for symbol, value in replacements.items()},
        "contact_endpoint_changed_rows": changed,
        "contact_endpoint_row_multipliers": multipliers,
        "contact_endpoint_savings": {"coordinates": 2, "quadratic_rows": 2},
        "contact_endpoint_exact_equivalence": "Guarded rational rechart and affine coordinate elimination give a bijective reconstruction of the predecessor zero set",
        "contact_endpoint_arithmetic_interfaces_unchanged": True,
        "contact_endpoint_inherited_metadata_scope": "Earlier chart formulae describe historical stages; the four recharted registers and two removed helpers have the reconstruction stated here",
        "unconditional_undecidability_claim": False,
    })
    assert len(names) == old["variables"] - 2
    assert len(rows) == len(old["residuals"]) - 2
    assert {i for row in rows for term in row["terms"] for i in term["monomial"]} == set(ids.values())
    return new


def main():
    for interface, predecessor in PREDECESSORS.items():
        source_bytes = (ROOT / predecessor).read_bytes()
        data = build_data(json.loads(source_bytes), interface)
        data["contact_endpoint_predecessor"] = predecessor
        data["contact_endpoint_predecessor_sha256"] = hashlib.sha256(source_bytes).hexdigest()
        output = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
        path = HERE / f"endpoint_{interface}_quadrics.json"
        path.write_bytes(output)
        certificate = {
            "interface": interface, "variables": data["variables"],
            "quadratic_rows": len(data["residuals"]), "degree": 4,
            "table_sha256": hashlib.sha256(output).hexdigest(),
            **{key: value for key, value in data.items() if key.startswith("contact_endpoint_")},
            "source_universality_hypothesis": None,
            "source_coding_theorem": data["source_coding_theorem"],
            "source_coding_theorem_independently_reproved": False,
            "unconditional_undecidability_claim": False,
        }
        path.with_name(f"endpoint_{interface}_certificate.json").write_text(
            json.dumps(certificate, sort_keys=True, indent=2) + "\n")
        print(json.dumps({key: certificate[key] for key in ("interface", "variables", "quadratic_rows", "table_sha256")}))


if __name__ == "__main__":
    main()
