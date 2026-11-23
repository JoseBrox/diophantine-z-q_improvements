#!/usr/bin/env python3
"""Independent exact coefficient audit of the 734-coordinate abc table.

The quantified Pell and arithmetic arguments are in one_quotient_pell.tex;
this checker does not replace them with finite computational evidence.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def normalized(row, names):
    return sorted((t["coefficient"], tuple(sorted(names[i-1] for i in t["monomial"])))
                  for t in row["terms"])


def expression(row, names):
    return sp.expand(sum(sp.sympify(t["coefficient"])*sp.prod(sp.Symbol(names[i-1]) for i in t["monomial"])
                         for t in row["terms"]))


def main():
    predecessor = ROOT / "undecidability/source_repair_v93/coefficients/signed_abc_fixed_offsets_quadrics.json"
    target = HERE / "crt_abc_quadrics.json"
    certificate_path = HERE / "crt_abc_certificate.json"
    old,new,cert = [json.loads(p.read_text()) for p in (predecessor,target,certificate_path)]
    assert hashlib.sha256(target.read_bytes()).hexdigest() == cert["table_sha256"]
    assert hashlib.sha256(predecessor.read_bytes()).hexdigest() == cert["pell_crt_predecessor_sha256"]
    names = new["variable_names"]
    assert len(names) == len(set(names)) == new["variables"] == 734
    assert len(new["residuals"]) == cert["quadratic_rows"] == 643
    assert cert["variables"] == 734 and cert["degree"] == 4
    assert max(len(t["monomial"]) for row in new["residuals"] for t in row["terms"]) == 2
    assert {i for row in new["residuals"] for t in row["terms"] for i in t["monomial"]} == set(range(1,735))
    removed_names = {"o"} | {n for n in old["variable_names"] if n.startswith("int_o_")}
    assert len(removed_names) == 48
    assert set(old["variable_names"])-set(names) == removed_names
    assert set(names)-set(old["variable_names"]) == {"pell_crt_cF"}
    old_rows = {row["name"]:row for row in old["residuals"]}
    new_rows = {row["name"]:row for row in new["residuals"]}
    removed_rows = {name for name in old_rows if name.startswith("integer.o.")}
    assert len(removed_rows) == 41
    removed_rows.add("jones1980.I.definition")
    assert old_rows.keys()-new_rows.keys() == removed_rows
    assert new_rows.keys()-old_rows.keys() == {"jones1980.crt.cF.definition"}
    unchanged = old_rows.keys()-removed_rows-{"jones1980.H.definition"}
    for name in unchanged:
        assert normalized(old_rows[name],old["variable_names"]) == normalized(new_rows[name],names)
    for coordinate in removed_names:
        occurrences = {row["name"] for row in old["residuals"]
                       if any(coordinate == old["variable_names"][i-1]
                              for term in row["terms"] for i in term["monomial"])}
        assert occurrences and occurrences <= removed_rows

    c,F,F2,H,r,J,CF = sp.symbols("c F F2 H r j pell_crt_cF")
    assert sp.expand(expression(new_rows["jones1980.H.definition"],names)
                     -(H-c-F2*(2*r+1-c)-CF*J)) == 0
    assert sp.expand(expression(new_rows["jones1980.crt.cF.definition"],names)-(CF-c*F)) == 0
    # The two CRT remainders are recorded as exact integer divisibilities.
    B,T = sp.symbols("B T")
    HH=c+F**2*(B-c)+c*F*J
    assert sp.expand((HH-B)-(B-c)*(F**2-1)-c*F*J) == 0
    assert sp.expand((HH-c)-F*(F*(B-c)+c*J)) == 0
    assert sp.expand((HH-B).subs(F**2,1+c*T)-c*((B-c)*T+F*J)) == 0

    expected_inputs = [n for n in old["ordinary_integer_inputs"] if n != "o"]
    assert new["ordinary_integer_inputs"] == expected_inputs and len(expected_inputs) == 11
    assert new["integer_blocks"] == new["shared_reference_blocks"] == 11
    assert new["reciprocal_integer_inputs"] == old["reciprocal_integer_inputs"] == []
    assert new["outer_coordinates"] == old["outer_coordinates"]
    assert new["outer_residuals"] == old["outer_residuals"]
    expected_offsets = {k:v for k,v in old["fixed_offset_translations"].items() if k != "o"}
    assert new["fixed_offset_translations"] == expected_offsets
    offsets = [Fraction(v) for v in expected_offsets.values()]
    assert len(offsets) == 11 and len(set(offsets)) == 11
    for i,x in enumerate(offsets):
        for y in offsets[:i]:
            difference=x-y
            assert difference.denominator in (2,4,8,16)
    # All guards unrelated to the discarded integer input remain unchanged.
    guard_names = {name for name in old_rows if any(word in name for word in ("nonzero", "unit", "guard", "inverse"))
                   and not name.startswith("integer.o.")}
    assert guard_names <= unchanged
    assert new["source_universality_hypothesis"] is None
    assert new["source_coding_theorem_independently_reproved"] is False
    assert new["unconditional_undecidability_claim"] is False
    from build_crt_abc import build
    raw = (json.dumps(build(),sort_keys=True,separators=(",",":"))+"\n").encode()
    assert raw == target.read_bytes()
    print(json.dumps({"status":"pass","variables":734,"quadratic_rows":643,"degree":4,
                      "integer_inputs":11,"removed_private_coordinates":48,"added_coordinates":1,
                      "unchanged_rows":len(unchanged),"retained_guard_rows":len(guard_names),
                      "exact_crt_divisibility_identities":3,"table_sha256":cert["table_sha256"],
                      "source_coding_theorem_external":True,"unconditional_undecidability_claim":False},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
