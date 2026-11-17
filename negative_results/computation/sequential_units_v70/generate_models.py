#!/usr/bin/env python3
"""Recreate the 30 recorded support models from pinned v69 prototypes.

The exact factor theorem is checked by check.py, without these prototypes.
This optional generator retains the complete computational search ledger
without storing thirty almost identical JSON files in this package.
"""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
import argparse
import copy
import json

HERE = Path(__file__).resolve().parent
PROTOTYPE_HASHES = {
    "A4_B4": "ed4d339f03993dd5b46768037a02150bb3ba2ae969ff6e97d47670789513f0a6",
    "A1_B3": "3c7cd180c37370cba4e45a66fe506fe0f2e0215e0d2b6562d42d5a12f4f02bc8",
    "A1_A3": "c6fc9f26626ea520a29e0592ca45187753a05e8d1774c5128b8fa0b37dc6018e",
}
RAW_IDS = {"A1": 205, "B1": 207, "A3": 217,
           "B3": 219, "A4": 229, "B4": 231}


def model_bytes(prototype, prototype_hash, basis, helpers):
    model = copy.deepcopy(prototype)
    # Keep insertion order, including metadata, to reproduce the recorded
    # files byte for byte. Changing an existing value preserves key order.
    model["prior_support_model_sha256"] = prototype_hash
    model["schema"] = "sequential-unit-support194/v70"
    model["unit_basis_case"] = basis["id"]
    model["base_units"] = {k: v for k, v in basis["unit_basis"].items() if k != "241"}
    model["extra_unit_candidates"] = [basis["unit_basis"]["241"]]
    model["new_unit_definitions"] = basis["definitions"]
    model["initial_unit_s"] = basis["s"]
    label = "_".join(helpers)
    if label not in PROTOTYPE_HASHES:
        model["helpers"] = list(helpers)
        for out, helper in zip((237, 239), helpers):
            raw = RAW_IDS[helper]
            row = next(r for r in model["rows"] if r["name"] == f"new.square.{out}")
            row["terms"] = [
                [[out], [0, 0]], [[out + 1], [0, 0]],
                [[raw, raw], [0, 0]], [[raw, raw + 1], [0, 0]],
                [[raw + 1, raw + 1], [0, 0]],
            ]
        model["quadratic_tests"] = {
            "C2": [66, [-6, 0], 9], "C3": [68, [-6, 0], 9],
            "C4": [70, [-6, 0], 9], "GL": [72, [-6, 0], 9],
        }
        model["quadratic_tests"].update({
            name: [raw, [0, 0], 1] for name, raw in RAW_IDS.items() if name not in helpers
        })
        model["linear_tests"] = {
            "DH": [64, [-1, 0]], "B0": [19, [-1, 0]],
            "A2": [54, [-1, 0]], "B2": [23, [-1, 0]],
            helpers[0]: [237, [0, 0]], helpers[1]: [239, [0, 0]],
            "C1": [114, [-1, 0]],
        }
    assert model["helpers"] == list(helpers)
    assert len(model["active"]) == 188 and len(model["rows"]) == 134
    assert len(model["quadratic_tests"]) == 8 and len(model["linear_tests"]) == 7
    assert model["physical_contact_weights"] == ["u", "u*v"]
    assert model["factor_output_unit_exponents"] == [[1, 0], [1, 2]]
    assert model["scalar_aggregate"] == "Matching real-part products only"
    return (json.dumps(model, indent=2) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-package", type=Path, required=True,
                        help="Path to computation/quartic/search194_v69")
    parser.add_argument("--output", type=Path,
                        help="Optional directory for generated model JSONs; omit to verify hashes only")
    args = parser.parse_args()
    prototypes = {}
    for name, expected_hash in PROTOTYPE_HASHES.items():
        raw = (args.source_package / "models" / (name + ".json")).read_bytes()
        assert sha256(raw).hexdigest() == expected_hash, ("prototype hash", name)
        prototypes[name] = json.loads(raw)
    certificate = json.loads((HERE / "certificate.json").read_text())
    bases = certificate["survivors"]
    assert len(bases) == 2
    ledger = json.loads((HERE / "runs.json").read_text())
    expected = {run["model"]: run for run in ledger["runs"]}
    assert len(expected) == 30
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
    checked = []
    for basis in bases:
        for helpers in combinations(RAW_IDS, 2):
            label = "_".join(helpers)
            prototype = label if label in prototypes else "A4_B4"
            raw = model_bytes(prototypes[prototype], PROTOTYPE_HASHES[prototype], basis, helpers)
            name = f"basis{basis['id']}_{label}.json"
            actual_hash = sha256(raw).hexdigest()
            assert name in expected
            assert actual_hash == expected[name]["model_sha256"], (name, actual_hash)
            assert prototype == expected[name]["prototype"]
            if args.output:
                (args.output / name).write_bytes(raw)
            checked.append(name)
    assert set(checked) == set(expected)
    print(json.dumps({"status": "PASS", "models_recreated": len(checked),
                      "byte_exact_model_hash_matches": len(checked),
                      "written": bool(args.output)}, indent=2))


if __name__ == "__main__":
    main()
