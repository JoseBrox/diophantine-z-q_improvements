#!/usr/bin/env python3
"""Replace the c integer block by the signed shifted-trace Pell theorem."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = ROOT / "undecidability/abc_scaled_point_v106/scaled_point_abc_quadrics.json"
RENAME = {"int_c_29": "source_c_square"}
HALFTRACE = "jones1980.c_integrality.halftrace"
SQUARE = "jones1980.c_square.definition"


def build_data(old):
    old_names = old["variable_names"]
    assert old["variables"] == 645 and len(old["residuals"]) == 564
    assert old["integer_blocks"] == 13 and "c" in old["ordinary_integer_inputs"]
    deleted = [r["name"] for r in old["residuals"]
               if r["name"].startswith(("integer.c.", "abc.scaled_point.c."))
               and r["name"] != "integer.c.height.betaSquare"]
    kept = [r for r in old["residuals"] if r["name"] not in deleted]
    used = {old_names[i - 1] for r in kept for t in r["terms"] for i in t["monomial"]}
    removed = [n for n in old_names if n not in used]
    names = [RENAME.get(n, n) for n in old_names if n in used] + ["c_integrality_zeta"]
    ids = {n: i + 1 for i, n in enumerate(names)}
    rows = []
    for row in kept:
        name = SQUARE if row["name"] == "integer.c.height.betaSquare" else row["name"]
        rows.append({"name": name, "terms": [
            {"coefficient": t["coefficient"],
             "monomial": sorted(ids[RENAME.get(old_names[i - 1], old_names[i - 1])] for i in t["monomial"])}
            for t in row["terms"]]})
    half_terms = [(1, ["c_integrality_zeta", "c_integrality_zeta"]),
                  (-2, ["a", "d"]), (-2, ["a", "ac"]), (2, ["c"]), (-2, [])]
    rows.append({"name": HALFTRACE, "terms": sorted([
        {"coefficient": str(coef), "monomial": sorted(ids[n] for n in monomial)}
        for coef, monomial in half_terms], key=lambda t: t["monomial"])})
    occurrences = {n: [r["name"] for r in old["residuals"]
                       if any(old_names[i - 1] == n for t in r["terms"] for i in t["monomial"])]
                   for n in removed}
    assert all(set(v) <= set(deleted) for v in occurrences.values())
    c_square_occurrences = [r["name"] for r in old["residuals"]
                            if any(old_names[i - 1] == "int_c_29" for t in r["terms"] for i in t["monomial"])]
    shared = old["abc_scaled_point_shared_coordinates"]
    for coordinate in shared:
        assert coordinate in names
    inputs = [n for n in old["ordinary_integer_inputs"] if n != "c"]
    new = dict(old)
    new.update({
        "variables": len(names), "variable_names": names, "residuals": rows,
        "ordinary_integer_inputs": inputs, "integer_blocks": len(inputs),
        "abc_c_integrality_proof": "undecidability/abc_pell_integrality_v108/abc_c_integrality.tex",
        "abc_c_integrality_arithmetic_theorem": "undecidability/pell_integrality_replacement_v106/pell_integrality_replacement.tex",
        "abc_c_integrality_source_integer_input": "c",
        "abc_c_integrality_remaining_certified_inputs": inputs,
        "abc_c_integrality_recovered_integral_source_outputs": ["c", "d"],
        "abc_c_integrality_removed_coordinates": removed,
        "abc_c_integrality_deleted_rows": deleted,
        "abc_c_integrality_removed_occurrences": occurrences,
        "abc_c_integrality_coordinate_renaming": RENAME,
        "abc_c_integrality_kept_c_square_occurrences": c_square_occurrences,
        "abc_c_integrality_renamed_square_row": {"old": "integer.c.height.betaSquare", "new": SQUARE},
        "abc_c_integrality_new_coordinate": "c_integrality_zeta",
        "abc_c_integrality_added_row": HALFTRACE,
        "abc_c_integrality_halftrace_identity": "zeta^2=2*(a*d+(a^2-1)*c+1); ac=a*c is already retained, so the row is quadratic.",
        "abc_c_integrality_source_prefix": "M=q^32, n=q^16, r=S*(M-n)+T*(M-1), a=(w*M+1)*r*s*M imply 3 divides a for integral prefix inputs; the independent signed shifted-trace Pell theorem and half-trace square recover c,d in Z.",
        "abc_c_integrality_shared_coordinates_retained": shared,
        "abc_c_integrality_contact_grid": "Keep the twelve surviving original offsets in the same dyadic grid. The omitted c contact list is simply absent; no relabeling or arithmetic strengthening is required.",
        "abc_c_integrality_scope": "Equivalence on the source-instance projection. Soundness first obtains the twelve remaining certified integer inputs, then applies the source-prefix and shifted-trace Pell integrality theorem. No reconstruction of the old c-block auxiliaries preserving all other old witnesses is asserted.",
        "abc_c_integrality_completeness": "Use the canonical positive source with d+c*sqrt(a^2-1)=(a+sqrt(a^2-1))^(2r+1). Then zeta=2*X_(r+1)(a) is integral and the twelve remaining common-point certificates exist under the same arithmetic premises.",
        "abc_c_integrality_savings": {"coordinates": 40, "quadratic_rows": 36, "integer_predicates": 1},
        "abc_c_integrality_historical_metadata": "Inherited transformation records describe their historical predecessors. The current integer count and certificate scope are given by ordinary_integer_inputs, integer_blocks, and abc_c_integrality_*.",
        "source_universality_hypothesis": None,
        "unconditional_undecidability_claim": False,
    })
    assert len(removed) == 41 and len(deleted) == 37
    assert len(names) == 605 and len(rows) == 528
    assert len(set(names)) == len(names) and len({r["name"] for r in rows}) == len(rows)
    assert {i for r in rows for t in r["terms"] for i in t["monomial"]} == set(ids.values())
    return new


def main():
    oldraw = PREDECESSOR.read_bytes()
    new = build_data(json.loads(oldraw))
    new["abc_c_integrality_predecessor"] = str(PREDECESSOR.relative_to(ROOT))
    new["abc_c_integrality_predecessor_sha256"] = sha256(oldraw).hexdigest()
    raw = (json.dumps(new, sort_keys=True, separators=(",", ":")) + "\n").encode()
    (HERE / "c_integrality_abc_quadrics.json").write_bytes(raw)
    cert = {"variables": new["variables"], "quadratic_rows": len(new["residuals"]), "degree": 4,
            "integer_blocks": new["integer_blocks"], "table_sha256": sha256(raw).hexdigest(),
            "ordinary_integer_inputs": new["ordinary_integer_inputs"],
            "source_coding_theorem": new["source_coding_theorem"],
            "source_universality_hypothesis": None, "unconditional_undecidability_claim": False,
            **{k: v for k, v in new.items() if k.startswith("abc_c_integrality_")}}
    (HERE / "c_integrality_abc_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: cert[k] for k in ("variables", "quadratic_rows", "integer_blocks", "degree", "table_sha256")}))


if __name__ == "__main__":
    main()
