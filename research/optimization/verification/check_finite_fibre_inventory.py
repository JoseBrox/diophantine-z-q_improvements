#!/usr/bin/env python3
"""Audit source occurrence counts used in the finite-fiber construction.

This checks the actual JSON call graph and construction logs. It does not
replace the mathematical proof of finite geometric fibers in the paper.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    paths = sorted((args.source_directory / "modules").glob("*.json"))
    modules = {p.stem: json.loads(p.read_text()) for p in paths}
    occurrences = Counter()

    def visit(name, stack=()):
        assert name not in stack, "Unexpected recursion in module calls"
        occurrences[name] += 1
        for call in modules[name]["calls"]:
            visit(call["module"], stack + (name,))

    visit("Z_definition")

    def variable_labels(name):
        return [op[2] for op in modules[name]["construction_log"] if op[0] == "variable"]

    root_points = [s[:-4] for s in variable_labels("Z_definition") if s.endswith(".u.0")]
    comparison_points = [s[:-4] for s in variable_labels("q_compare4") if s.endswith(".u.0")]
    assert root_points == ["A", "S", "T", "Z", "height J", "common comparison J"]
    assert comparison_points == ["H", "X0", "X1", "X2", "X3"]
    assert occurrences == {
        "Z_definition": 1, "q_anchor": 1, "q_height_batch": 1,
        "q_primeparity": 42, "q_compare4": 41, "q_batch41": 41,
    }
    assert variable_labels("q_primeparity") == [
        "prime parity." + name for name in ("t", "U", "e", "p", "q", "s", "h")
    ]
    root = modules["Z_definition"]
    assert root["pell_equation"] == "t^2-s*(s-2)*t*z+(s-2)^2*z^2-1=0"
    height_bits = [s for s in variable_labels("q_height_batch")
                   if s.startswith("height local class ") or s == "height sign correction"]
    assert len(height_bits) == 8
    old_anchor_norm_variables = sum(s == "anchor norm witness" for s in variable_labels("q_anchor"))
    assert old_anchor_norm_variables == 14
    point_occurrences = len(root_points) + occurrences["q_compare4"] * len(comparison_points)
    retained = {
        "point_abscissa_coordinates": 2 * point_occurrences,
        "three_per_pole_block": 3 * occurrences["q_primeparity"],
        "new_anchor_free_coordinates": 2,
        "root_parameters_including_input": 7,
    }
    assert point_occurrences == 211
    assert sum(retained.values()) == 557
    receipt = {
        "result": "verified",
        "source_modules_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        "module_occurrences": dict(occurrences),
        "root_point_labels": root_points,
        "comparison_point_labels": comparison_points,
        "point_occurrences": point_occurrences,
        "height_bits": 8,
        "retained_coordinates": retained,
        "retained_total": sum(retained.values()),
        "total_variables_after_one_variable_finite_fibre_theorem": 558,
        "rational_witness_variables": 557,
        "scope": "Actual source count plus the proved exact substitutions. Not an expanded 558-variable polynomial or a source arithmetic proof.",
    }
    text = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
