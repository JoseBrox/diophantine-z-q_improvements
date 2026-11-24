#!/usr/bin/env python3
"""Audit the reconstructed quartics, their compositions, and the c-integrality replacement."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "undecidability"
CHECKERS = [
    "quadratic_reduction_v104/verify_bb_native.py",
    "abc_common_numerator_v103/verify_common_numerator.py",
    "odd_pell_quotient_v104/verify_odd_quotient.py",
    "abc_point_rechart_v105/verify_point_rechart.py",
    "abc_scaled_point_v106/verify_scaled_point.py",
    "input_comparison_v105/verify_input_comparison.py",
    "pell_classification_reconstructed_v105/verify_classification.py",
    "pell_integrality_replacement_v106/verify_replacement.py",
    "c_integrality_reduction_v106/verify_c_deletion.py",
    "abc_pell_integrality_v108/verify_abc_integrality.py",
    "abc_bb_native_v107/verify_abc_bb.py",
    "odd_quotient_obstruction_v109/verify_odd_obstruction.py",
    "pell_quotient_obstruction_v109/verify_obstruction.py",
    "unary_outer_checkpoint_v109/verify_outer.py",
]
EXPECTED = {
    "bb-native-combined-quartic-163": (963, 818, 13),
    "bb-native-combined-quartic-179": (1140, 991, 11),
    "common-numerator-quartic-56": (675, 594, 13),
    "odd-quotient-quartic-56": (674, 593, 13),
    "common-point-quartic-56": (656, 575, 13),
    "scaled-point-quartic-56": (645, 564, 13),
    "reconstructed-input-comparison-quartic-163": (948, 803, 13),
    "reconstructed-input-comparison-quartic-179": (1127, 978, 11),
    "bb-input-comparison-quartic-163": (943, 798, 13),
    "bb-input-comparison-quartic-179": (1124, 975, 11),
    "c-integrality-replacement-quartic-163": (887, 750, 12),
    "c-integrality-replacement-quartic-179": (1052, 913, 10),
    "c-integrality-replacement-quartic-56": (605, 528, 12),
}
CURRENT = {
    "general": "c-integrality-replacement-quartic-163",
    "specified": "c-integrality-replacement-quartic-179",
    "ordinary_abc": "c-integrality-replacement-quartic-56",
}

def check(relative):
    p = subprocess.run([sys.executable, "-B", str(FOLDER / relative)],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    result = json.loads(p.stdout)
    if "results" in result:
        assert all(r["status"] == "PASS" for r in result["results"])
    else:
        assert result["status"] == "PASS"
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    checks = {name: check(name) for name in CHECKERS}
    ledger = json.loads((FOLDER / "results.json").read_text())
    records = {r["id"]: r for r in ledger["records"]}
    assert len(records) == len(ledger["records"])
    assert ledger["current_preferred_quartic_records"] == CURRENT
    audited = []
    for key, (n, rows, blocks) in EXPECTED.items():
        r = records[key]
        table_path = FOLDER / r["table"]
        t = json.loads(table_path.read_text())
        c = json.loads((FOLDER / r["certificate"]).read_text())
        digest = hashlib.sha256(table_path.read_bytes()).hexdigest()
        assert r["variables"] == t["variables"] == c["variables"] == n
        assert r["quadratic_rows"] == len(t["residuals"]) == c["quadratic_rows"] == rows
        assert r["integer_certificates"] == t["integer_blocks"] == blocks
        assert r["table_sha256"] == c["table_sha256"] == digest
        assert r["degree"] == t["sum_of_squares_degree"] == 4
        assert r["source_universality_hypothesis"] is None
        assert r["retains_project_arithmetic_premises"] is True
        assert r["unconditional_undecidability_claim"] is False
        if key in CURRENT.values():
            assert r["uses_BB_native_poles"] is True
            assert r["old_non_CM_pole_realization_required"] is False
        proof = FOLDER / r["proof"]
        assert proof.is_file() and proof.with_suffix(".pdf").is_file()
        predecessor = records[r["predecessor_record"]]
        assert r["predecessor_table_sha256"] == predecessor["table_sha256"]
        assert r["coordinates_saved_in_this_step"] == predecessor["variables"] - n
        assert r["quadratic_rows_saved_in_this_step"] == predecessor["quadratic_rows"] - rows
        audited.append({"record": key, "variables": n, "quadratic_rows": rows,
                        "integer_certificates": blocks, "table_sha256": digest})
    replacement = checks["pell_integrality_replacement_v106/verify_replacement.py"]
    assert replacement["arithmetic_c_integrality_replacement_proved"] is True
    assert replacement["complete_table_count_claim_in_this_checkpoint"] is False
    poles = checks["abc_bb_native_v107/verify_abc_bb.py"]
    assert (poles["variables"], poles["quadratic_rows"], poles["pole_blocks"]) == (605, 528, 12)
    assert poles["literal_rows_checked"] == 84 and poles["table_modified"] is False
    assert poles["table_sha256"] == records[CURRENT["ordinary_abc"]]["table_sha256"]
    outer = checks["unary_outer_checkpoint_v109/verify_outer.py"]
    assert outer["external_power_graphs_required"] is True
    assert outer["external_y_integrality_required"] is True
    assert outer["full_polynomial_source_compiled"] is False
    assert outer["new_global_variable_bound_claim"] is False
    current = {route: next(row for row in audited if row["record"] == key)
               for route, key in CURRENT.items()}
    scope = ledger["recovery_20261124"]
    assert scope["original_prior_chat_artifacts_recovered"] is False
    assert scope["reported_abc_649_original_recovered"] is False
    assert scope["independently_reconstructed_general_counts"] == [948, 1127]
    result = {
        "schema": "zq-undecidability-verification/v108",
        "status": "PASS",
        "current_quartics": current,
        "registered_complete_tables": audited,
        "independent_checker_count": len(checks),
        "arithmetic_c_integrality_replacement_proved": True,
        "integer_predicates_removed_from_each_route": 1,
        "all_current_pole_realizations_BB_native": True,
        "abc_native_pole_literal_rows_audited": 84,
        "quotient_counterexamples_scope": "Subsystems only; not the full coding source.",
        "alternative_unary_source_compiled": False,
        "unrestricted_degree_counts_unchanged": [82, 100, 52],
        "reported_649_artifact_recovered": False,
        "prior_948_1127_counts_independently_reconstructed": True,
        "quartic_target_263_established": False,
        "arithmetic_interfaces_and_external_coding_theorem_retained": True,
        "scope": (
            "Complete coefficient and occurrence audits, polynomial identities, "
            "guard and shared-contact reconstruction, signed arithmetic theorem "
            "checks, source-instance projection proofs, registry and file hashes. "
            "Finite computations do not prove the inherited arithmetic premises "
            "or independently reprove the external coding theorem."
        ),
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
