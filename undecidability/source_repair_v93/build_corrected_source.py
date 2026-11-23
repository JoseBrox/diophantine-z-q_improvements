#!/usr/bin/env python3
"""Compile the independently proved n^6 binomial block into old tables.

This is a deliberate replacement of the historical source relation, not a
claim of equivalence with the erroneous n^2 block.  The corrected complete
source is equivalent to Jones (1980), Theorem 2, by the binomial certificate.
The coding theorem remains a cited external mathematical result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGED_ROWS = ("jones1980.sr.definition", "jones1980.a.definition")


def terms_by_name(row, names):
    return sorted(
        (str(t["coefficient"]), tuple(sorted(names[i - 1] for i in t["monomial"])))
        for t in row["terms"]
    )


def build_data(old):
    """Change exactly two residuals; reuse sr as r*s*n^2, not r*s."""
    names = old["variable_names"]
    ids = {name: i + 1 for i, name in enumerate(names)}
    rows = {row["name"]: row for row in old["residuals"]}
    required = {
        "jones1980.sr.definition": [("-1", ("r", "s")), ("1", ("sr",))],
        "jones1980.sr2.definition": [("-1", ("sr", "sr")), ("1", ("sr2",))],
        "jones1980.U.definition": [("-1", ("n2", "w")), ("1", ("U",))],
        "jones1980.p.definition": [("-2", ("U", "sr2")), ("1", ("p",))],
        "jones1980.Y.definition": [("-1", ("n2", "s")), ("1", ("Y",))],
        "jones1980.a.definition": [
            ("-2", ("n2", "sr2")), ("-1", ("n2", "p")), ("2", ("a", "sr"))
        ],
    }
    for name, expected in required.items():
        assert terms_by_name(rows[name], names) == sorted(expected), name
    occurrences = [
        row["name"] for row in old["residuals"]
        if any(ids["sr"] in t["monomial"] for t in row["terms"])
    ]
    assert set(occurrences) == {
        "jones1980.sr.definition", "jones1980.sr2.definition", "jones1980.a.definition"
    }

    def serialize(ts):
        return sorted(
            ({"coefficient": str(c), "monomial": sorted(ids[n] for n in mon)} for c, mon in ts),
            key=lambda t: t["monomial"],
        )

    changed = {
        "jones1980.sr.definition": serialize([(1, ("sr",)), (-1, ("r", "Y"))]),
        "jones1980.a.definition": serialize([(1, ("a",)), (-1, ("U", "sr")), (-1, ("sr",))]),
    }
    new = dict(old)
    new["residuals"] = [
        {"name": row["name"], "terms": changed[row["name"]]} if row["name"] in changed else row
        for row in old["residuals"]
    ]
    assert new["variables"] == old["variables"] == len(names)
    assert len(new["residuals"]) == len(old["residuals"])
    assert max(len(t["monomial"]) for row in new["residuals"] for t in row["terms"]) == 2
    assert {i for row in new["residuals"] for t in row["terms"] for i in t["monomial"]} == set(ids.values())
    # Keep predecessor provenance, but do not leave its U_em claims in fields
    # that describe the current, deliberately different polynomial source.
    historical_keys = (
        "status", "source_universality", "source_universality_hypothesis",
        "source_universality_verified", "universality_hypothesis",
        "universality_independently_verified", "source_reconciliation",
        "source_core_sha256", "source_occurrences",
        "pell_core_source_p_parameter", "pell_core_source_discrepancy",
        "M_recovery", "a_recovery", "detector_trace_status",
        "global_gauge_scope", "global_gauge_status", "scalar_norm_status",
        "scalar_rechart_status",
    )
    new["source_repair_historical_source_metadata"] = {
        key: old[key] for key in historical_keys if key in old
    }
    for key in historical_keys:
        new.pop(key, None)
    new.update({
        "status": "Conditional quartic transfer from the corrected source equivalent to Jones (1980), Theorem 2; every stated arithmetic premise of the retained integer-defining interface remains required.",
        "universality_hypothesis": None,
        "universality_independently_verified": False,
        "source_universality": "The corrected polynomial source is equivalent to the cited classical Jones (1980), Theorem 2, by the independently proved binomial and signed-Pell certificates. The historical U_em premise is not used.",
        "source_universality_hypothesis": None,
        "source_universality_verified": True,
        "source_universality_verification_scope": "Reduction to the cited classical Jones (1980) Theorem 2, using the independently proved binomial and signed-Pell certificates; not an independent reproof of the coding theorem.",
        "source_coding_theorem_independently_reproved": False,
        "source_coding_theorem": "J. P. Jones, Undecidable Diophantine equations, Bull. Amer. Math. Soc. (N.S.) 3 (1980), 859-862, Theorem 2, p. 860, doi:10.1090/S0273-0979-1980-14832-6",
        "source_replacement": "p=2*w*s^2*r^2*n^6; a=(w*n^2+1)*r*s*n^2; Latin a in the power-of-two congruence; correct norm equations.",
        "source_replacement_is_equivalence_with_old_system": False,
        "source_reconciliation": "New source derived directly from Jones (1980), Theorem 2; the old expanded-source claim is recorded only as historical predecessor provenance.",
        "source_repair_changed_rows": list(CHANGED_ROWS),
        "source_repair_reused_register": "sr=r*Y=r*s*n^2; sr2=sr^2",
        "source_repair_old_sr_occurrences": occurrences,
        "source_repair_proof": "undecidability/source_repair_v93/corrected_jones_source.tex",
        "source_repair_dependencies": [
            "undecidability/papers/binomial_pell_certificate.tex",
            "undecidability/papers/pell_index_optimization.tex",
        ],
        "source_repair_coordinate_saving": 0,
        "source_repair_row_saving": 0,
        "unconditional_undecidability_claim": False,
        "retained_arithmetic_interfaces": True,
        "pell_core_source_p_parameter": "2*w*s^2*r^2*n^6",
        "pell_core_source_discrepancy": "Replaced by the independently proved binomial block; historical n^2 tables remain unchanged.",
        "M_recovery": "sr",
        "a_recovery": "(U+1)*sr",
    })
    # Interface transformations are unchanged, but their old status strings
    # referred to the historical expanded source.  Their present scope is the
    # corrected source, whose coding theorem is cited rather than reproved.
    interface_status = {
        "detector_trace_status": "Exact rational equivalence; every retained arithmetic interface remains required.",
        "global_gauge_scope": "No abc assumption added; every retained arithmetic interface remains required.",
        "global_gauge_status": "Proved transfer under retained arithmetic interfaces, applied to the corrected source.",
        "scalar_norm_status": "Exact quadratic equivalence with automatic common trace guard, applied to the corrected source.",
        "scalar_rechart_status": "Exact equivalence under retained nonvanishing, applied to the corrected source.",
    }
    for key, value in interface_status.items():
        if key in old:
            new[key] = value
    return new


def build(path):
    raw = Path(path).read_bytes()
    new = build_data(json.loads(raw))
    new["source_repair_predecessor_sha256"] = hashlib.sha256(raw).hexdigest()
    return new


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--include-compositions", action="store_true")
    args = ap.parse_args()
    if args.source is not None:
        if args.out is None:
            ap.error("--source requires --out")
        pairs = [(args.source, args.out)]
    else:
        pairs = []
        for m in (163, 179, 56):
            prefix = "detector_pell" if m != 56 else "pell_core"
            source = ROOT / "undecidability/coefficients" / f"jones1980_{prefix}" / f"{prefix}_m{m}_quadrics.json"
            target = Path(__file__).parent / "coefficients" / f"corrected_m{m}_quadrics.json"
            pairs.append((source, target))
        if args.include_compositions:
            for m in (163, 179, 56):
                source = ROOT / f"undecidability/coefficients/jones1980_ceiling_power/ceiling_power_m{m}_quadrics.json"
                target = Path(__file__).parent / "coefficients" / f"corrected_ceiling_m{m}_quadrics.json"
                pairs.append((source, target))
            pairs.append((ROOT / "undecidability/joint_detector_v93/abc_fixed_offsets_quadrics.json",
                          Path(__file__).parent / "coefficients/corrected_abc_fixed_offsets_quadrics.json"))
    for source, target in pairs:
        source, target = source.resolve(), target.resolve()
        data = build(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
        target.write_bytes(raw)
        certificate = {
            "variables": data["variables"],
            "quadratic_rows": len(data["residuals"]),
            "degree": 4,
            "source_repair_coordinate_saving": 0,
            "source_repair_row_saving": 0,
            "table_sha256": hashlib.sha256(raw).hexdigest(),
            **{k: data[k] for k in data if k.startswith("source_repair_") or k.startswith("source_coding_")},
            "source_universality_hypothesis": None,
            "external_source_theorem_used": True,
            "retained_arithmetic_interfaces": True,
            "source_replacement_is_equivalence_with_old_system": False,
            "unconditional_undecidability_claim": False,
        }
        target.with_name(target.name.replace("_quadrics.json", "_certificate.json")).write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
        print(json.dumps({"path": str(target.relative_to(ROOT)), "variables": data["variables"], "rows": len(data["residuals"]), "sha256": certificate["table_sha256"]}))


if __name__ == "__main__":
    main()
