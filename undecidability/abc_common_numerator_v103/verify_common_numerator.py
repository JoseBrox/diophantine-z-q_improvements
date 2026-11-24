#!/usr/bin/env python3
"""Independent polynomial lift audit; deliberately does not import the compiler."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def polynomial(row, names):
    return s.expand(sum(s.sympify(t["coefficient"]) *
                        s.prod(s.Symbol(names[i - 1]) for i in t["monomial"])
                        for t in row["terms"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    path = HERE / "common_numerator_abc_quadrics.json"
    raw = path.read_bytes()
    new = json.loads(raw)
    cert = json.loads((HERE / "common_numerator_abc_certificate.json").read_bytes())
    predecessor = ROOT / new["abc_common_numerator_predecessor"]
    oldraw = predecessor.read_bytes()
    old = json.loads(oldraw)
    assert sha256(raw).hexdigest() == cert["table_sha256"]
    assert sha256(oldraw).hexdigest() == new["abc_common_numerator_predecessor_sha256"]
    labels = old["ordinary_integer_inputs"]
    assert labels == new["ordinary_integer_inputs"] == cert["ordinary_integer_inputs"]
    assert len(labels) == new["integer_blocks"] == old["integer_blocks"] == 13
    assert old["variables"] == 695 and len(old["residuals"]) == 590
    assert new["variables"] == cert["variables"] == len(new["variable_names"]) == 675
    assert len(new["residuals"]) == cert["quadratic_rows"] == 594
    ns, os = new["variable_names"], old["variable_names"]
    assert len(set(ns)) == len(ns)
    oldrows = {r["name"]: polynomial(r, os) for r in old["residuals"]}
    newrows = {r["name"]: polynomial(r, ns) for r in new["residuals"]}
    assert len(newrows) == len(new["residuals"])
    z = s.Symbol
    J0, J1, E0, E1, K0, K1 = map(z, [f"abc_numerator_{x}{i}" for x in ("J", "E", "K") for i in range(2)])
    v0, v1 = z("int_b_6"), z("int_b_7")
    e_def = [E0 - v0 * J0 - 2 * v1 * J1, E1 - v0 * J1 - v1 * J0]
    k_def = [K0 - J0 ** 2 - 2 * J1 ** 2, K1 - 2 * J0 * J1]
    for name, expected in zip(new["abc_common_numerator_added_rows"], e_def + k_def, strict=True):
        assert s.expand(newrows[name] - expected) == 0, name
    deleted, private, changed = [], [], set()
    substitution = {}
    for label in labels:
        prefix = "int_i_reciprocal" if label == "i" else f"int_{label}"
        uv = [z(f"{prefix}_{i}") for i in (21, 22, 23, 24)]
        L0, L1 = z(f"abc_numerator_{label}_L0"), z(f"abc_numerator_{label}_L1")
        X2, X4 = z(f"{prefix}_29"), z(f"{prefix}_30")
        lift = dict(zip(uv, (X2 * J0 + L0, X2 * J1 + L1,
                            X2 * J0 - L0, X2 * J1 - L1), strict=True))
        substitution.update(lift)
        deleted.extend(map(str, uv))
        private.extend((str(L0), str(L1)))
        # Every input square/fourth-power equation remains literally present.
        square_name = f"integer.{label}.height.betaFourth"
        assert s.expand(oldrows[square_name] - (X2 ** 2 - X4)) == 0
        assert newrows[square_name] == oldrows[square_name]
        for component in range(2):
            for side in ("first", "second"):
                name = f"integer.{label}.product.{side}.{component}"
                mul = s.Rational(new["abc_common_numerator_row_multipliers"][name])
                assert mul == s.Rational(1, 2)
                remainder = s.expand(oldrows[name].subs(lift, simultaneous=True) - newrows[name] / mul)
                expected = (2 if component == 0 else -2) * X2 * e_def[component] if side == "first" else 0
                assert s.expand(remainder - expected) == 0, name
                changed.add(name)
            name = f"integer.{label}.product{component}"
            assert new["abc_common_numerator_row_multipliers"][name] == "1"
            remainder = s.expand(oldrows[name].subs(lift, simultaneous=True) - newrows[name])
            expected = -X2 ** 2 * k_def[component] + (X2 ** 2 - X4) * (K0 if component == 0 else K1)
            assert s.expand(remainder - expected) == 0, name
            changed.add(name)
        allowed = {f"integer.{label}.product.{side}.{i}" for side in ("first", "second") for i in range(2)}
        allowed |= {f"integer.{label}.product{i}" for i in range(2)}
        actual_union = set()
        for variable in uv:
            occurrence = [name for name, row in oldrows.items() if variable in row.free_symbols]
            assert occurrence == new["abc_common_numerator_occurrences"][str(variable)]
            actual_union.update(occurrence)
        assert actual_union == allowed
    assert set(deleted) == set(new["abc_common_numerator_removed_coordinates"])
    assert set(changed) == set(new["abc_common_numerator_changed_rows"])
    assert len(changed) == 78
    for name, row in oldrows.items():
        if name not in changed:
            assert row == newrows[name], name
    assert len(oldrows) - len(changed) == 512
    assert set(oldrows) < set(newrows)
    assert set(ns) == set(os).difference(deleted) | set(private) | {str(v) for v in (J0, J1, E0, E1, K0, K1)}
    parameters = [z(name) for name in old["parameters"]]
    used_ids, maximum_degree = set(), 0
    for row in new["residuals"]:
        assert row["terms"]
        for t in row["terms"]:
            assert t["monomial"] == sorted(t["monomial"])
            assert len(t["monomial"]) <= 2
            used_ids.update(t["monomial"])
            maximum_degree = max(maximum_degree, len(t["monomial"]))
            coefficient = s.sympify(t["coefficient"])
            assert coefficient.free_symbols <= set(parameters)
            assert s.Poly(coefficient, *parameters, domain=s.ZZ)
    assert used_ids == set(range(1, 676)) and maximum_degree == 2
    # The input-square residual survives, so its square supplies a nonzero
    # degree-four homogeneous summand. Rational sums of squares cannot cancel it.
    assert newrows["integer.b.height.betaSquare"] == z("b") ** 2 - z("int_b_29")
    assert new["unconditional_undecidability_claim"] is False
    assert new["source_coding_theorem"] == old["source_coding_theorem"]
    assert new["source_universality_hypothesis"] is None
    for k, value in cert.items():
        if k.startswith("abc_common_numerator_"):
            assert new[k] == value
    result = {
        "status": "PASS", "variables": 675, "quadratic_rows": 594,
        "sum_of_squares_degree": 4, "coordinates_saved": 20,
        "changed_rows_independently_checked": 78, "unchanged_rows_checked": 512,
        "common_definition_rows_checked": 4, "complete_occurrence_audit": True,
        "all_rational_zeros_lift_to_predecessor": True,
        "integer_blocks_retained": 13,
        "source_sha256": sha256(oldraw).hexdigest(), "table_sha256": sha256(raw).hexdigest(),
        "verification_scope": "Exact polynomial lift identities, complete occurrences, coefficient domain, support, degree, counts and metadata. Common-numerator arithmetic completeness is proved in common_numerator.tex, not by this finite audit.",
    }
    if args.write_certificate:
        (HERE / "independent_verification.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
