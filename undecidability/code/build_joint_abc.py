#!/usr/bin/env python3
"""Build the shared-reference ordinary-abc source used in the 69-variable bound.

Each v88 input is replaced by X_i^2+1, each contact coordinate by
a_i*(z+100*i), and only the H point block is shared.  The old input
factor is omitted because its new argument is everywhere positive.
All native guards except terminal-root nonvanishing are retained.
This exact DAG transformation does not prove the arithmetic premises.
"""

import argparse
import json
from pathlib import Path
from functools import cache
from build_joint_few_variable import Dag, digest


def build(repo, output, copies):
    folder = repo / "computation/bhargava_burungale_v88/bb_twelve/abc11"
    source_path = folder / "native.json"
    source = json.loads(source_path.read_text())
    policy = json.loads((folder / "strengthened.json").read_text())
    assert source["retained_base_count"] == 10
    assert source["total_external_variables"] == 11
    assert source["multiply_by_input"] is True
    assert source["contact_count"] == 12
    assert source["scale_exponent"] == 1
    event, = [e for e in source["events"] if e["operation"] == "moving_contact_height"]
    midpoint_node = event["A"]["numerator"]
    assert source["coefficient_dag"][event["A"]["denominator"]] == ["int", 1]
    assert event["A"] == event["M"]
    assert event["shifts"] == [-9, -8, -7, -5, -4, -3, -2, -1, 6, 10, 11, 12]
    variables_by_index = {v["index"]: v for v in source["variables"]}
    old_input, = [v["index"] for v in source["variables"] if v["category"] == "retained.input"]
    old_contact, = [v["index"] for v in source["variables"] if v["category"] == "retained.slope"]

    @cache
    def source_dependencies(j):
        op, *args = source["coefficient_dag"][j]
        if op == "variable":
            return frozenset(args)
        if op in ("int", "parameter"):
            return frozenset()
        if op == "pow":
            return source_dependencies(args[0])
        return frozenset().union(*(source_dependencies(a) for a in args))

    assert source_dependencies(midpoint_node) == frozenset((0, 1, 2))
    assert all(variables_by_index[j]["name"].startswith(("input.", "A."))
               for j in source_dependencies(midpoint_node))
    variables, indices = [], {}
    variable_maps = [{} for _ in range(copies)]
    for finite in (False, True):
        for i in range(copies):
            for v in source["variables"]:
                if v["category"].startswith("finite.") != finite:
                    continue
                if v["category"] == "retained.slope":
                    name = "shared.z"
                elif v["name"].startswith("H."):
                    name = "shared." + v["name"]
                else:
                    name = f"block{i}." + v["name"]
                if name not in indices:
                    indices[name] = len(variables)
                    variables.append({"index": len(variables), "name": name, "category": v["category"]})
                variable_maps[i][v["index"]] = indices[name]
        if not finite:
            retained_count = len(variables)
    assert retained_count == 7 * copies + 3

    dag, blocks, guards, node_maps = Dag(), {}, set(), []
    terminal_guards = set(policy["pole_ordinate_guards"])
    assert terminal_guards == {b["generator_node"] for b in source["finite_blocks"] if b["kind"] == "pole"}
    for i in range(copies):
        vmap = variable_maps[i]

        @cache
        def clone(j):
            op, *args = source["coefficient_dag"][j]
            if op == "variable":
                old = args[0]
                new = dag.node("variable", vmap[old])
                if old == old_input:
                    return dag.node("add", dag.node("pow", new, 2), dag.node("int", 1))
                if old == old_contact:
                    shifted = dag.node("add", new, dag.node("int", 100 * i)) if i else new
                    return dag.node("mul", clone(midpoint_node), shifted)
                return new
            if op in ("int", "parameter"):
                return dag.node(op, *args)
            if op == "pow":
                return dag.node(op, clone(args[0]), args[1])
            assert op in ("add", "mul", "neg")
            return dag.node(op, *(clone(a) for a in args))

        node_map = [clone(j) for j in range(len(source["coefficient_dag"]))]
        node_maps.append(node_map)
        guards.update(node_map[j] for j in source["guard_numerators"] if j not in terminal_guards)

        def rat(value):
            return {key: node_map[value[key]] for key in ("numerator", "denominator")}

        for b in source["finite_blocks"]:
            name = ("shared." if b["name"] == "H" else f"block{i}.") + b["name"]
            if b["kind"] == "point_block":
                new = {"name": name, "kind": "point_block", "degree": 4,
                       "A": rat(b["A"]), "B": rat(b["B"]),
                       "variable_nodes": [node_map[j] for j in b["variable_nodes"]]}
            else:
                new = {"name": name, "kind": "pole", "degree": 2, "monic": True,
                       "coefficient_nodes_ascending": [node_map[j] for j in b["coefficient_nodes_ascending"]],
                       "generator_node": node_map[b["generator_node"]], "variable": vmap[b["variable"]],
                       "original_root": rat(b["original_root"]),
                       "original_square_input": rat(b["original_square_input"]),
                       "zero_stratum_rule": "Zero terminal roots are allowed."}
            if name in blocks:
                assert blocks[name] == new
            else:
                blocks[name] = new
    points = [b for b in blocks.values() if b["kind"] == "point_block"]
    poles = [b for b in blocks.values() if b["kind"] == "pole"]
    assert len(points) == 1 + 2 * copies and len(poles) == copies
    terminal_variables = {b["variable"] for b in poles}
    dep = []
    for op, *args in dag.nodes:
        if op == "variable":
            d = {args[0]} & terminal_variables
        elif op in ("int", "parameter"):
            d = set()
        elif op == "pow":
            d = dep[args[0]]
        else:
            d = set().union(*(dep[j] for j in args))
        dep.append(d)
    assert all(not dep[j] for j in guards)
    assert all(not dep[j] for b in poles for j in b["coefficient_nodes_ascending"])
    assert 81 > max(abs(c) for c in event["shifts"])
    assert 12 < 81 and 4 < 100

    summary = {
        "scope": "Exact source transformation under ordinary rational abc and the retained non-pole source premises.",
        "source": str(source_path.relative_to(repo)), "source_sha256": digest(source_path),
        "source_policy_sha256": digest(folder / "strengthened.json"),
        "source_family_parameter": source["family_parameter"],
        "source_pole_policy": source["final_pole_policy"],
        "copies": copies, "input_substitution": "old_X_i=X_i^2+1",
        "contact_substitution": "old_z_i=a_i*(z+100*i), where a_i=(((X_i^2+1)^2+B)^4+Tr(x(A_i))^4)",
        "shared_point_roles": ["H"], "private_point_roles": ["A", "UA"],
        "retained_coordinate_counts": {"inputs": copies, "common_reference_coordinates": 2,
            "private_point_coordinates": 4 * copies, "common_contact_parameter": 1,
            "private_pole_parameters": 2 * copies, "single_joint_encoder": 1},
        "tuple_total_variables": retained_count + 1,
        "mixed_integer_transfer_variables": retained_count + 3 if copies == 9 else None,
        "finite_point_blocks": len(points), "finite_quadratic_pole_blocks": len(poles),
        "finite_algebra_rank_exponent_base2": 2 + 5 * copies,
        "finite_algebra_rank": 1 << (2 + 5 * copies),
        "joint_coefficient_nodes": len(dag.nodes), "joint_retained_guard_nodes": len(guards),
        "midpoint_depends_only_on_private_input_and_A_coordinates": True,
        "terminal_zero_roots_allowed": True, "terminal_dependence_checks": "passed",
        "old_input_factor_omitted": True,
        "contact_intervals": [f"({-100*i-2},{-100*i+2})" for i in range(copies)],
        "degree_claim": "A computable finite bound follows from the general guarded-character encoder; the old single-input bound is not inherited.",
    }
    document = {
        "schema": "shared-abc-reference/v1", "summary": summary, "variables": variables,
        "retained_base_count": retained_count, "coefficient_dag": dag.nodes,
        "finite_blocks": points + poles, "guard_numerators": sorted(guards),
        "point_block_multiplication": {"basis": ["1", "U", "V", "W"],
            "U^2": "2*A+2*W", "V^2": "A-W", "U*V": "2*B",
            "U*W": "A*U-2*B*V", "V*W": "B*U-A*V", "W^2": "A^2-2*B^2"},
        "encoder": "Apply the general single-variable guarded finite-algebra encoder; do not multiply by the original input factor.",
        "original_variable_maps": variable_maps, "original_coefficient_node_maps": node_maps,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "joint_source.json").write_text(json.dumps(document, separators=(",", ":")) + "\n")
    summary["joint_source_sha256"] = digest(output / "joint_source.json")
    (output / "certificate.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("copies", "tuple_total_variables",
          "mixed_integer_transfer_variables", "finite_algebra_rank_exponent_base2",
          "joint_coefficient_nodes", "joint_retained_guard_nodes")}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--copies", type=int, default=9)
    args = parser.parse_args()
    assert args.copies > 0
    build(args.repo, args.output, args.copies)
