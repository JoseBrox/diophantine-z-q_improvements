#!/usr/bin/env python3
"""Independent full-table and source-prefix audit of the c-block replacement."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def expression(row, names):
    return s.expand(sum(s.sympify(t["coefficient"]) * s.prod(s.Symbol(names[i - 1]) for i in t["monomial"])
                        for t in row["terms"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    raw = (HERE / "c_integrality_abc_quadrics.json").read_bytes()
    new = json.loads(raw)
    cert = json.loads((HERE / "c_integrality_abc_certificate.json").read_bytes())
    oldraw = (ROOT / new["abc_c_integrality_predecessor"]).read_bytes()
    old = json.loads(oldraw)
    assert sha256(raw).hexdigest() == cert["table_sha256"]
    assert sha256(oldraw).hexdigest() == new["abc_c_integrality_predecessor_sha256"]
    assert old["variables"] == 645 and len(old["residuals"]) == 564
    assert old["integer_blocks"] == 13
    assert new["variables"] == cert["variables"] == len(new["variable_names"]) == 605
    assert len(new["residuals"]) == cert["quadratic_rows"] == 528
    assert new["integer_blocks"] == cert["integer_blocks"] == 12
    assert new["ordinary_integer_inputs"] == [n for n in old["ordinary_integer_inputs"] if n != "c"]
    assert len(set(new["variable_names"])) == 605
    old_names, names = old["variable_names"], new["variable_names"]
    oldrows = {r["name"]: expression(r, old_names) for r in old["residuals"]}
    newrows = {r["name"]: expression(r, names) for r in new["residuals"]}
    assert len(oldrows) == 564 and len(newrows) == 528
    z = s.Symbol
    rename = {z("int_c_29"): z("source_c_square")}
    deleted = {name for name in oldrows if name.startswith(("integer.c.", "abc.scaled_point.c."))
               and name != "integer.c.height.betaSquare"}
    assert len(deleted) == 37 and deleted == set(new["abc_c_integrality_deleted_rows"])
    half_name, square_name = "jones1980.c_integrality.halftrace", "jones1980.c_square.definition"
    assert set(newrows) == (set(oldrows) - deleted - {"integer.c.height.betaSquare"}) | {half_name, square_name}
    unchanged = set(oldrows) - deleted - {"integer.c.height.betaSquare"}
    assert len(unchanged) == 526
    for name in unchanged:
        assert newrows[name] == oldrows[name].xreplace(rename), name
    assert newrows[square_name] == oldrows["integer.c.height.betaSquare"].xreplace(rename)
    assert newrows[square_name] == z("c") ** 2 - z("source_c_square")
    assert newrows[half_name] == z("c_integrality_zeta") ** 2 - 2 * z("a") * z("d") - 2 * z("a") * z("ac") + 2 * z("c") - 2
    removed = set(old_names) - set(names) - {"int_c_29"}
    assert len(removed) == 41 and removed == set(new["abc_c_integrality_removed_coordinates"])
    assert set(names) == (set(old_names) - removed - {"int_c_29"}) | {"source_c_square", "c_integrality_zeta"}
    for variable in removed:
        actual = [name for name, poly in oldrows.items() if z(variable) in poly.free_symbols]
        assert actual == new["abc_c_integrality_removed_occurrences"][variable]
        assert set(actual) <= deleted
    c_square_old = [name for name, poly in oldrows.items() if z("int_c_29") in poly.free_symbols]
    assert c_square_old == new["abc_c_integrality_kept_c_square_occurrences"]
    c_square_new = {name for name, poly in newrows.items() if z("source_c_square") in poly.free_symbols}
    assert c_square_new == {square_name, "jones1980.d.norm", "jones1980.E.odd_quotient"}
    assert newrows["jones1980.ac.definition"] == z("ac") - z("a") * z("c")
    assert newrows["jones1980.d.norm"] == z("d") ** 2 - z("ac") ** 2 + z("source_c_square") - 1
    assert s.expand(newrows["jones1980.E.odd_quotient"] - z("E") + (2 * z("i_half") + 1) * z("source_c_square")) == 0
    assert s.expand(newrows["jones1980.d.definition"] - z("d") + (z("a") - 2) * z("c") + z("b") * z("w") + (4 * z("a") - 5) * z("gamma")) == 0

    # Full shared reference, numerator, point and contact equations are unchanged.
    common_names = {name for name in oldrows if name.startswith(("abc.point_common.", "abc.common_numerator.", "integer.b.reference."))}
    common_names |= {name for name in oldrows if "contact" in name and not name.startswith("integer.c.")}
    assert all(name in unchanged for name in common_names)
    shared = old["abc_scaled_point_shared_coordinates"]
    assert new["abc_c_integrality_shared_coordinates_retained"] == shared
    assert all(n in names for n in shared)
    roles = ["i" if r == "i_half" else r for r in new["ordinary_integer_inputs"]]
    for role in roles:
        old_private = {name for name in oldrows if name.startswith((f"integer.{role}.", f"abc.scaled_point.{role}."))}
        assert old_private and old_private <= unchanged
    assert not any(name.startswith(("integer.c.", "abc.scaled_point.c.")) for name in newrows)

    # Independently interpret the exact prefix needed for 3|a.
    prefix = {
        "q2.definition": z("q2") - z("q") ** 2,
        "q4.definition": z("q4") - z("q2") ** 2,
        "q8.definition": z("q8") - z("q4") ** 2,
        "n.definition": z("n") - z("q8") ** 2,
        "n2.definition": z("n2") - z("n") ** 2,
        "r.definition": z("r") - z("S") * (z("n2") - z("n")) - z("T") * (z("n2") - 1),
        "Y.definition": z("Y") - z("s") * z("n2"),
        "sr.definition": z("sr") - z("r") * z("Y"),
        "U.definition": z("U") - z("w") * z("n2"),
        "a.definition": z("a") - (z("U") + 1) * z("sr"),
    }
    for name, expected in prefix.items():
        assert s.expand(newrows["jones1980." + name] - expected) == 0
    # This is the complete residue space, not sampling a larger finite range.
    residue_cases = 0
    for q in range(3):
        n, M = pow(q, 16, 3), pow(q, 32, 3)
        for source_S in range(3):
            for source_T in range(3):
                r = (source_S * (M - n) + source_T * (M - 1)) % 3
                assert M * r % 3 == 0
                residue_cases += 1
    # The new half-trace is exactly the arithmetic theorem's square once
    # the retained source registers are substituted.
    aa, cc, dd, TT = s.symbols("check_a check_c check_d check_T")
    Delta, D, La = aa ** 2 - 1, 4 * aa - 5, 2 * aa ** 2 - 2 * aa - 1
    assert s.expand(8 * La + 3 - D * (4 * aa + 1)) == 0
    assert s.expand(2 * (aa * ((aa - 2) * cc + TT) + Delta * cc + 1) - (2 * La * cc + 2 * aa * TT + 2)) == 0
    assert s.expand((D * cc - (aa - 2) * TT) ** 2 - (Delta * TT ** 2 - D) - D * (D * cc ** 2 - 2 * (aa - 2) * TT * cc - (TT ** 2 - 1))) == 0
    # Canonical odd-index completions are independent exact recurrences.
    pell_fixtures = 0
    for a in (3, 6, 9, 12):
        seq = [(1, 0), (a, 1)]
        for k in range(2, 20):
            seq.append((2 * a * seq[-1][0] - seq[-2][0], 2 * a * seq[-1][1] - seq[-2][1]))
        for r in range(0, 8):
            d, c = seq[2 * r + 1]
            zeta = 2 * seq[r + 1][0]
            assert zeta * zeta == 2 * (a * d + (a * a - 1) * c + 1)
            pell_fixtures += 1

    parameters = [z(k) for k in new["parameters"]]
    used = set()
    for row in new["residuals"]:
        for term in row["terms"]:
            assert term["monomial"] == sorted(term["monomial"]) and len(term["monomial"]) <= 2
            used.update(term["monomial"])
            coefficient = s.sympify(term["coefficient"])
            assert coefficient.free_symbols <= set(parameters)
            assert s.Poly(coefficient, *parameters, domain=s.ZZ)
    assert used == set(range(1, 606))
    assert newrows["integer.b.height.betaSquare"] == z("b") ** 2 - z("int_b_29")
    assert new["source_coding_theorem"] == old["source_coding_theorem"]
    assert new["source_universality_hypothesis"] is None and new["unconditional_undecidability_claim"] is False
    for key, value in cert.items():
        if key.startswith("abc_c_integrality_"):
            assert new[key] == value
    theorem = ROOT / new["abc_c_integrality_arithmetic_theorem"]
    assert theorem.is_file()
    result = {
        "status": "PASS", "variables": 605, "quadratic_rows": 528, "degree": 4,
        "integer_blocks": 12, "integer_predicates_removed": 1,
        "coordinates_saved": 40, "quadratic_rows_saved": 36,
        "unchanged_rows_under_coordinate_rename": 526, "retained_renamed_square_rows": 1,
        "new_halftrace_rows": 1, "deleted_rows": 37,
        "removed_coordinate_occurrences_audited": 41,
        "shared_and_contact_rows_checked": len(common_names),
        "source_prefix_rows_interpreted": len(prefix),
        "complete_modulo_three_prefix_cases": residue_cases,
        "symbolic_denominator_identities": 3, "canonical_halftrace_fixtures": pell_fixtures,
        "source_sha256": sha256(oldraw).hexdigest(), "table_sha256": sha256(raw).hexdigest(),
        "arithmetic_theorem": str(theorem.relative_to(ROOT)),
        "verification_scope": "Full row deletion/renaming, all 526 untouched rows, retained c-square usage, new half-trace, every deleted-coordinate occurrence, shared point and contact interfaces, exact source-prefix rows, all residue cases modulo three, coefficient ring, support, counts and hashes. Quantified c-integrality is proved in the cited signed Pell theorem; the finite fixture checks do not replace that proof or certify the retained elliptic arithmetic premises.",
    }
    if args.write_certificate:
        (HERE / "independent_verification.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
