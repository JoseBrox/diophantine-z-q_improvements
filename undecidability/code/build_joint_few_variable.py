#!/usr/bin/env python3
"""Build the complete shared-point rational sources for the 99/117 transfer.

This is a coordinate and coefficient-DAG transformation of the published
v88 sources.  It does not prove their retained arithmetic premises.  Finite
chart variables are internal generators of a multiplication algebra, not
additional quantified rational coordinates.  The resulting algebra is
encoded by the general single-variable guarded-character construction.

Run with --repo PATH --output PATH [--copies 9].  No third-party packages.
"""

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


SHARED_POINTS = ("S", "T", "Z", "H", "US", "UT", "UZ")
ALL_POINTS = ("A", "S", "T", "Z", "H", "UA", "US", "UT", "UZ")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Dag:
    def __init__(self):
        self.nodes = []
        self.index = {}

    def node(self, op, *args):
        key = (op, *args)
        if key not in self.index:
            self.index[key] = len(self.nodes)
            self.nodes.append(list(key))
        return self.index[key]


def scoped_name(variable, copy):
    name = variable["name"]
    if variable["category"] == "retained.slope":
        return "shared.lambda"
    if name.split(".")[0] in SHARED_POINTS:
        return "shared." + name
    return f"block{copy}." + name


def build(repo, output, route, copies):
    folder = repo / "computation/bhargava_burungale_v88/bb_general" / route
    source_path = folder / "native.json"
    source = json.loads(source_path.read_text())
    reduced = json.loads((folder / "reduced.json").read_text())
    e = {"general25": 2, "explicit27": 3}[route]
    assert source["retained_base_count"] == 20 + 2 * e
    assert source["total_external_variables"] == 21 + 2 * e
    assert source["target"] == "X^2+1"
    assert source["unsquared_scales"] is True
    assert [b["name"] for b in source["finite_blocks"] if b["kind"] == "point_block"] == list(ALL_POINTS)
    assert len([b for b in source["finite_blocks"] if b["kind"] == "pole"]) == e

    # All retained base coordinates precede every finite algebra generator.
    variables, variable_indices = [], {}
    original_variable_maps = [{} for _ in range(copies)]
    for finite in (False, True):
        for i in range(copies):
            for variable in source["variables"]:
                if variable["category"].startswith("finite.") != finite:
                    continue
                name = scoped_name(variable, i)
                if name not in variable_indices:
                    variable_indices[name] = len(variables)
                    variables.append({"index": len(variables), "name": name,
                                      "category": variable["category"]})
                original_variable_maps[i][variable["index"]] = variable_indices[name]
        if not finite:
            retained_count = len(variables)

    assert retained_count == (5 + 2 * e) * copies + 15
    dag = Dag()
    source_node_maps = []
    guard_nodes = set()
    finite_blocks = {}
    terminal_guards = set(reduced["pole_ordinate_guards"])
    assert terminal_guards == {b["generator_node"] for b in source["finite_blocks"] if b["kind"] == "pole"}
    assert terminal_guards <= set(source["guard_numerators"])

    for i in range(copies):
        node_map = []
        vmap = original_variable_maps[i]
        for old in source["coefficient_dag"]:
            op = old[0]
            if op == "variable":
                new = dag.node("variable", vmap[old[1]])
                if source["variables"][old[1]]["category"] == "retained.slope" and i:
                    new = dag.node("add", new, dag.node("int", 100 * i))
            elif op in ("int", "parameter"):
                new = dag.node(op, *old[1:])
            elif op == "pow":
                new = dag.node(op, node_map[old[1]], old[2])
            elif op in ("add", "mul", "neg"):
                new = dag.node(op, *(node_map[j] for j in old[1:]))
            else:
                raise ValueError(f"Unknown coefficient operation {op}")
            node_map.append(new)
        source_node_maps.append(node_map)
        guard_nodes.update(node_map[j] for j in source["guard_numerators"] if j not in terminal_guards)

        def rational(value):
            return {key: node_map[value[key]] for key in ("numerator", "denominator")}

        for block in source["finite_blocks"]:
            name = ("shared." if block["name"] in SHARED_POINTS else f"block{i}.") + block["name"]
            if block["kind"] == "point_block":
                transformed = {
                    "name": name, "kind": "point_block", "degree": 4,
                    "A": rational(block["A"]), "B": rational(block["B"]),
                    "variable_nodes": [node_map[j] for j in block["variable_nodes"]],
                }
            else:
                transformed = {
                    "name": name, "kind": "pole", "degree": 2, "monic": True,
                    "coefficient_nodes_ascending": [node_map[j] for j in block["coefficient_nodes_ascending"]],
                    "generator_node": node_map[block["generator_node"]],
                    "variable": vmap[block["variable"]],
                    "original_root": rational(block["original_root"]),
                    "original_square_input": rational(block["original_square_input"]),
                    "zero_stratum_rule": "Zero terminal roots are allowed; no terminal generator is a guard.",
                }
            if name in finite_blocks:
                # The common blocks agree coefficient-for-coefficient after mapping.
                assert finite_blocks[name] == transformed, name
            else:
                finite_blocks[name] = transformed

    points = [b for b in finite_blocks.values() if b["kind"] == "point_block"]
    poles = [b for b in finite_blocks.values() if b["kind"] == "pole"]
    assert len(points) == 7 + 2 * copies
    assert len(poles) == e * copies
    assert len(variables) - retained_count == 3 * len(points) + len(poles)

    # Terminal roots are absent from every retained guard and every coefficient
    # defining another finite block, including through intermediate DAG nodes.
    terminal_variables = {b["variable"] for b in poles}
    dependence = []
    for node in dag.nodes:
        op = node[0]
        if op == "variable":
            deps = {node[1]} if node[1] in terminal_variables else set()
        elif op in ("int", "parameter"):
            deps = set()
        elif op == "pow":
            deps = dependence[node[1]]
        else:
            deps = set().union(*(dependence[j] for j in node[1:]))
        dependence.append(deps)
    assert all(not dependence[j] for j in guard_nodes)
    assert all(not dependence[j] for b in poles for j in b["coefficient_nodes_ascending"])

    theta = [Fraction(0), Fraction(-1, 2), Fraction(-1), Fraction(1, 2399), Fraction(-32, 407)]
    contacts = [[Fraction(4 * j + shift) + t for shift in (2, 4) for t in theta]
                for j in range(e)]
    assert all(0 < x < 13 for row in contacts for x in row)
    assert all(len(set(row)) == 10 for row in contacts)
    assert 13 < 100  # The fixed translated intervals are disjoint.
    assert Fraction(5, 4) * 100 + 1 + 23 < Fraction(3, 2) * 100
    assert 23**2 > 5 * 100  # Exact sufficient Hasse check at u=100.

    rank_exponent = 14 + (4 + e) * copies
    tuple_count = retained_count + 1
    summary = {
        "scope": "Exact coordinate/DAG transformation; arithmetic completeness is proved separately under retained source premises.",
        "source": str(source_path.relative_to(repo)), "source_sha256": digest(source_path),
        "source_policy_sha256": digest(folder / "reduced.json"),
        "source_family_parameter": source["family_parameter"],
        "source_pole_policy": source["final_pole_policy"],
        "copies": copies, "detectors_per_copy": e,
        "shared_point_roles": list(SHARED_POINTS),
        "private_point_roles": ["A", "UA"],
        "slope_substitution": "lambda_i=lambda+100*i, 0<=i<copies",
        "retained_coordinate_counts": {"inputs": copies, "common_point_coordinates": 14,
            "private_point_coordinates": 4 * copies, "common_slope": 1,
            "private_pole_parameters": 2 * e * copies, "single_joint_encoder": 1},
        "tuple_total_variables": tuple_count,
        "mixed_integer_transfer_variables": tuple_count + 2 if copies == 9 else None,
        "finite_point_blocks": len(points), "finite_quadratic_pole_blocks": len(poles),
        "finite_algebra_rank_exponent_base2": rank_exponent, "finite_algebra_rank": 1 << rank_exponent,
        "joint_coefficient_nodes": len(dag.nodes), "joint_retained_guard_nodes": len(guard_nodes),
        "contact_intervals": [f"({-100*i},{-100*i+13})" for i in range(copies)],
        "terminal_zero_roots_allowed": True, "terminal_dependence_checks": "passed",
        "degree_claim": "A computable finite bound follows from the general guarded-character encoder; no old single-input degree bound is inherited.",
    }
    document = {
        "schema": "shared-seven-points/v1", "summary": summary,
        "variables": variables, "retained_base_count": retained_count,
        "coefficient_dag": dag.nodes, "finite_blocks": points + poles,
        "guard_numerators": sorted(guard_nodes),
        "point_block_multiplication": {
            "basis": ["1", "U", "V", "W"], "U^2": "2*A+2*W", "V^2": "A-W",
            "U*V": "2*B", "U*W": "A*U-2*B*V", "V*W": "B*U-A*V", "W^2": "A^2-2*B^2"},
        "encoder": "Apply joint_finite_algebra_encoder.tex to the product guard and this complete multiplication algebra.",
        "original_variable_maps": original_variable_maps,
        "original_coefficient_node_maps": source_node_maps,
    }
    destination = output / route
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "joint_source.json").write_text(json.dumps(document, separators=(",", ":")) + "\n")
    summary["joint_source_sha256"] = digest(destination / "joint_source.json")
    (destination / "certificate.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--copies", type=int, default=9)
    args = parser.parse_args()
    assert args.copies > 0
    summaries = [build(args.repo, args.output, route, args.copies)
                 for route in ("general25", "explicit27")]
    (args.output / "coordinate_ledger.json").write_text(json.dumps(summaries, indent=2) + "\n")
    for s in summaries:
        print(json.dumps({k: s[k] for k in ("source", "copies", "tuple_total_variables",
              "mixed_integer_transfer_variables", "finite_algebra_rank_exponent_base2",
              "joint_coefficient_nodes", "joint_retained_guard_nodes")}))


if __name__ == "__main__":
    main()
