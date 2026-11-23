#!/usr/bin/env python3
"""Use one sixteenth of the retained b-block aggregate as contact spacing."""
from __future__ import annotations

import hashlib
import json
from math import gcd, lcm
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPACING = "contact_common_spacing"
PREDECESSORS = {
    "general": "undecidability/pell_product_v99/product_general_quadrics.json",
    "specified": "undecidability/pell_product_v99/product_specified_quadrics.json",
}


def normalized_row(row, old_names, names, parameters):
    ids = {name: index + 1 for index, name in enumerate(names)}
    symbols = {name: sp.Symbol(name) for name in old_names}
    polynomial = sp.expand(sum(sp.sympify(term["coefficient"]) *
                              sp.prod(symbols[old_names[i - 1]] for i in term["monomial"])
                              for term in row["terms"]))
    polynomial = sp.expand(polynomial.subs(symbols[SPACING],
                                          (symbols["int_b_68"] - symbols["int_b_2"]) / 16))
    used = sorted(polynomial.free_symbols.intersection(symbols.values()), key=str)
    entries = sp.Poly(polynomial, *used).terms()
    parameter_symbols = [sp.Symbol(name) for name in parameters]
    coefficients = [coefficient for _, coefficient in entries]
    numeric_coefficients = [q for coefficient in coefficients
                            for q in sp.Poly(coefficient, *parameter_symbols).coeffs()]
    denominator = lcm(*(int(q.q) for q in numeric_coefficients))
    content = 0
    for q in numeric_coefficients:
        content = gcd(content, abs(int(denominator * q)))
    multiplier = sp.Rational(denominator, content)
    terms = []
    for powers, coefficient in entries:
        monomial = sorted(ids[str(symbol)] for symbol, power in zip(used, powers) for _ in range(power))
        terms.append({"coefficient": str(sp.expand(coefficient * multiplier)), "monomial": monomial})
    terms.sort(key=lambda term: term["monomial"])
    return {"name": row["name"], "terms": terms}, str(multiplier)


def build_data(old):
    old_names = old["variable_names"]
    assert SPACING in old_names
    assert max(old["affine_contact_active_indices"]) <= 15
    names = [name for name in old_names if name != SPACING]
    ids = {name: i + 1 for i, name in enumerate(names)}
    rows, changed, multipliers = [], [], {}
    for row in old["residuals"]:
        if any(old_names[i - 1] == SPACING for term in row["terms"] for i in term["monomial"]):
            new_row, multiplier = normalized_row(row, old_names, names, old["parameters"])
            rows.append(new_row)
            changed.append(row["name"])
            multipliers[row["name"]] = multiplier
        else:
            rows.append({"name": row["name"], "terms": [
                {"coefficient": term["coefficient"],
                 "monomial": sorted(ids[old_names[i - 1]] for i in term["monomial"])}
                for term in row["terms"]]})
    new = dict(old)
    new.update({
        "variables": len(names), "variable_names": names, "residuals": rows,
        "affine_contact_new_coordinates": [name for name in old["affine_contact_new_coordinates"] if name != SPACING],
        "aggregate_spacing_proof": "undecidability/aggregate_spacing_v100/aggregate_spacing.tex",
        "aggregate_spacing_removed_coordinate": SPACING,
        "aggregate_spacing_substitution": "contact_common_spacing=(int_b_68-int_b_2)/16",
        "aggregate_spacing_physical_definition": "D=T_b/16, with T_b the b-block's first retained aggregate shift",
        "aggregate_spacing_root_depth": "K=v_2(a_scalar)>=2; common Lucas Q3 gives v_2(T_i)=-4*K-4",
        "aggregate_spacing_order_scope": "T_b depends only on fixed difference points and remains fixed when the reference index h is retuned after contact-prime selection",
        "aggregate_spacing_contact_indices": old["affine_contact_active_indices"],
        "aggregate_spacing_changed_rows": changed,
        "aggregate_spacing_row_multipliers": multipliers,
        "aggregate_spacing_savings": {"coordinates": 1, "quadratic_rows": 0},
        "aggregate_spacing_interface_hypotheses_unchanged": True,
        "aggregate_spacing_inherited_metadata_scope": "Earlier affine-contact formulae are historical stages; the symbol d is now the displayed affine expression",
        "unconditional_undecidability_claim": False,
    })
    assert len(rows) == len(old["residuals"])
    assert len(names) == old["variables"] - 1
    assert max(len(term["monomial"]) for row in rows for term in row["terms"]) == 2
    assert {i for row in rows for term in row["terms"] for i in term["monomial"]} == set(ids.values())
    return new


def main():
    for interface, predecessor in PREDECESSORS.items():
        source_bytes = (ROOT / predecessor).read_bytes()
        data = build_data(json.loads(source_bytes))
        data["aggregate_spacing_predecessor"] = predecessor
        data["aggregate_spacing_predecessor_sha256"] = hashlib.sha256(source_bytes).hexdigest()
        output = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
        path = HERE / f"aggregate_spacing_{interface}_quadrics.json"
        path.write_bytes(output)
        certificate = {
            "interface": interface, "variables": data["variables"],
            "quadratic_rows": len(data["residuals"]), "degree": 4,
            "table_sha256": hashlib.sha256(output).hexdigest(),
            **{key: value for key, value in data.items() if key.startswith("aggregate_spacing_")},
            "source_universality_hypothesis": None,
            "source_coding_theorem": data["source_coding_theorem"],
            "source_coding_theorem_independently_reproved": False,
            "unconditional_undecidability_claim": False,
        }
        path.with_name(f"aggregate_spacing_{interface}_certificate.json").write_text(
            json.dumps(certificate, sort_keys=True, indent=2) + "\n")
        print(json.dumps({key: certificate[key] for key in ("interface", "variables", "quadratic_rows", "table_sha256")}))


if __name__ == "__main__":
    main()
