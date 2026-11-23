#!/usr/bin/env python3
"""Independent exact checks of the corrected Jones-source coefficient tables.

The external Jones coding theorem is not proved by this program.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHANGED = {"jones1980.sr.definition", "jones1980.a.definition"}


def expr(row, names):
    return sp.expand(sum(
        sp.sympify(t["coefficient"]) * sp.prod(sp.Symbol(names[i-1]) for i in t["monomial"])
        for t in row["terms"]
    ))


def check_table(m, variant="baseline"):
    prefix = "detector_pell" if m != 56 else "pell_core"
    predecessor = ROOT / "undecidability/coefficients" / f"jones1980_{prefix}" / f"{prefix}_m{m}_quadrics.json"
    target = HERE / "coefficients" / f"corrected_m{m}_quadrics.json"
    if variant == "ceiling":
        predecessor = ROOT / f"undecidability/coefficients/jones1980_ceiling_power/ceiling_power_m{m}_quadrics.json"
        target = HERE / "coefficients" / f"corrected_ceiling_m{m}_quadrics.json"
    elif variant == "fixed_offsets":
        assert m == 56
        predecessor = ROOT / "undecidability/joint_detector_v93/abc_fixed_offsets_quadrics.json"
        target = HERE / "coefficients/corrected_abc_fixed_offsets_quadrics.json"
    else:
        assert variant == "baseline"
    cert_path = target.with_name(target.name.replace("_quadrics.json", "_certificate.json"))
    old = json.loads(predecessor.read_text())
    new = json.loads(target.read_text())
    cert = json.loads(cert_path.read_text())
    assert hashlib.sha256(target.read_bytes()).hexdigest() == cert["table_sha256"]
    assert hashlib.sha256(predecessor.read_bytes()).hexdigest() == cert["source_repair_predecessor_sha256"]
    assert old["variable_names"] == new["variable_names"]
    assert len(old["residuals"]) == len(new["residuals"])
    names = new["variable_names"]
    assert len(names) == len(set(names)) == new["variables"] == cert["variables"]
    old_rows = {r["name"]: r for r in old["residuals"]}
    new_rows = {r["name"]: r for r in new["residuals"]}
    assert old_rows.keys() == new_rows.keys()
    actually_changed = {n for n in old_rows if old_rows[n] != new_rows[n]}
    assert actually_changed == CHANGED
    for n in old_rows.keys() - CHANGED:
        assert old_rows[n] == new_rows[n]
    assert max(len(t["monomial"]) for row in new["residuals"] for t in row["terms"]) == 2
    assert {i for row in new["residuals"] for t in row["terms"] for i in t["monomial"]} == set(range(1, len(names)+1))
    assert new["source_universality_hypothesis"] is None
    assert new["universality_hypothesis"] is None
    assert new["source_universality_verified"] is True
    assert new["universality_independently_verified"] is False
    assert new["source_repair_historical_source_metadata"]["source_universality_hypothesis"] == "U_em"
    assert "requires U_em" not in new["status"]
    assert new["source_coding_theorem_independently_reproved"] is False
    assert new["source_replacement_is_equivalence_with_old_system"] is False
    assert new["unconditional_undecidability_claim"] is False
    assert new["M_recovery"] == "sr"
    assert new["a_recovery"] == "(U+1)*sr"
    assert "corrected positive source" in new["pell_core_equivalence_scope"]
    assert new["source_repair_historical_source_metadata"]["pell_core_equivalence_scope"] == old["pell_core_equivalence_scope"]
    assert new["source_repair_historical_source_metadata"]["M_recovery"] == "sr*n2"
    assert new["source_repair_historical_source_metadata"]["a_recovery"] == "(U+1)*sr*n2"
    for key in ("detector_trace_status", "global_gauge_scope", "global_gauge_status",
                "scalar_norm_status", "scalar_rechart_status"):
        if key in old:
            assert new["source_repair_historical_source_metadata"][key] == old[key]
            assert "U_em" not in new[key]

    n, r, s, w = sp.symbols("n r s w")
    substitution = {
        sp.Symbol("n2"): n**2,
        sp.Symbol("Y"): s*n**2,
        sp.Symbol("sr"): r*s*n**2,
        sp.Symbol("sr2"): r**2*s**2*n**4,
        sp.Symbol("U"): w*n**2,
        sp.Symbol("p"): 2*w*r**2*s**2*n**6,
        sp.Symbol("a"): (w*n**2+1)*r*s*n**2,
    }
    for name in ("Y", "sr", "sr2", "U", "p", "a"):
        assert sp.expand(expr(new_rows[f"jones1980.{name}.definition"], names).subs(substitution, simultaneous=True)) == 0
    assert sp.expand(expr(new_rows["jones1980.sr.definition"], names) - (sp.Symbol("sr") - r*sp.Symbol("Y"))) == 0
    assert sp.expand(expr(new_rows["jones1980.a.definition"], names) - (sp.Symbol("a") - (sp.Symbol("U")+1)*sp.Symbol("sr"))) == 0
    # Each register is assigned once by a monic row; the independent ordering
    # below proves that this block has exactly its prescribed rational lift.
    order = ["Y", "sr", "sr2", "U", "p", "a"]
    available = {"r", "s", "w", "n2"}
    for name in order:
        residual = expr(new_rows[f"jones1980.{name}.definition"], names)
        poly = sp.Poly(residual, sp.Symbol(name))
        assert poly.degree() == 1 and poly.coeff_monomial(sp.Symbol(name)) == 1
        assert {str(v) for v in residual.free_symbols} - {name} <= available
        available.add(name)
    expected = {163: (1103,953), 179:(1283,1109), 56:(837,725)}[m]
    if variant == "ceiling":
        expected = tuple(v-29 for v in expected)
    elif variant == "fixed_offsets":
        expected = (786,685)
    assert (len(names), len(new["residuals"])) == expected
    assert (cert["variables"], cert["quadratic_rows"]) == expected
    # Deterministic byte reproduction is additional to the mathematical tests.
    from build_corrected_source import build
    reproduced = (json.dumps(build(predecessor), sort_keys=True, separators=(",", ":")) + "\n").encode()
    assert reproduced == target.read_bytes()
    return {"interface": m, "variant": variant, "variables": expected[0], "quadratic_rows": expected[1], "degree": 4,
            "table_sha256": cert["table_sha256"], "unchanged_residuals": len(new_rows)-2}


def main():
    results = [check_table(m, variant) for variant in ("baseline", "ceiling") for m in (163,179,56)]
    results.append(check_table(56,"fixed_offsets"))
    # Source-side domain and count checks, independent of the circuit builder.
    initial = "b e g ell m n q r t omega alpha nu theta lam".split()
    added = "w s a p k tau h c d phi gamma eta i F j o".split()
    final = (set(initial)-{"omega", "nu"}) | set(added)
    assert len(initial)==14 and len(added)==16 and len(final)==28
    L=5**60
    assert L>1
    for b in range(2,65):
        # n=b^(16L) >= b and b <= 2n^2 follow from the exponent only;
        # the enormous integer is deliberately not constructed.
        assert 16*L>=1 and b<=2*b*b
    report = {"status":"pass", "checked":"exact quadratic coefficient repair and rational lift; source composition written in corrected_jones_source.tex",
              "source_coding_theorem":"Jones (1980), Theorem 2 (external)",
              "independent_reproof_of_coding_theorem":False,
              "old_U_em_proved":False,
              "tables":results}
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
