#!/usr/bin/env python3
"""Remove the independent inverse witness from the 855-variable circuit.

The cleared private anchor is B*u^2+N=0 with B a polynomial square. Its
three private witnesses can be adjusted so that u is nonzero. After
rescaling u, a reciprocal witness incorporates every branch-local guard.
This script does not modify the 855 producer or package.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from build_compact_polynomial import Builder


class RecordingBuilder(Builder):
    def anchor(self, f):
        self.anchor_arguments = f
        return super().anchor(f)


def children(node):
    op, *args = node
    if op in ("int", "variable", "parameter"):
        return []
    if op in ("neg", "pow"):
        return [args[0]]
    if op in ("add", "mul"):
        return args
    raise ValueError(op)


def dependence(nodes, variable):
    out = []
    for node in nodes:
        out.append(node == ["variable", variable]
                   or any(out[i] for i in children(node)))
    return out


def coefficients_in_private_variable(circuit, root, variable):
    """Exact coefficient extraction; other subexpressions remain circuits."""
    c = circuit
    dep = dependence(c.nodes, variable)
    cache = {}

    def plus(a, b):
        out = dict(a)
        for k, n in b.items():
            out[k] = c.add(out.get(k, c.zero), n)
            if out[k] == c.zero:
                del out[k]
        return out

    def times(a, b):
        out = {}
        for i, n in a.items():
            for j, m in b.items():
                out = plus(out, {i+j: c.mul(n, m)})
        return out

    def expand(i):
        if i in cache:
            return cache[i]
        if not dep[i]:
            result = {} if i == c.zero else {0: i}
        else:
            op, *args = c.nodes[i]
            if op == "variable":
                assert args == [variable]
                result = {1: c.one}
            elif op == "neg":
                result = {k: c.neg(n) for k, n in expand(args[0]).items()}
            elif op == "add":
                result = {}
                for a in args:
                    result = plus(result, expand(a))
            elif op == "mul":
                result = {0: c.one}
                for a in args:
                    result = times(result, expand(a))
            elif op == "pow":
                result = {0: c.one}
                for _ in range(args[1]):
                    result = times(result, expand(args[0]))
            else:
                raise ValueError(op)
        cache[i] = result
        return result

    return expand(root)


def prune(nodes, roots):
    keep = set()
    todo = list(roots)
    while todo:
        i = todo.pop()
        if i in keep:
            continue
        keep.add(i)
        todo.extend(children(nodes[i]))
    mapping = {old: new for new, old in enumerate(sorted(keep))}
    result = []
    for old in sorted(keep):
        op, *args = nodes[old]
        if op in ("int", "variable", "parameter"):
            result.append(nodes[old])
        elif op == "pow":
            result.append([op, mapping[args[0]], args[1]])
        else:
            result.append([op, *(mapping[a] for a in args)])
    return result, mapping


def build():
    producer = RecordingBuilder()
    parent = producer.build()
    c = producer.c
    parent_bytes = (json.dumps(parent, separators=(",", ":")) + "\n").encode()
    original_anchor = [row for row in c.equations
                       if row["label"] == "packed semilocal anchor"]
    assert len(original_anchor) == 1
    original_anchor = original_anchor[0]
    u_entry = [v for v in c.variables if v["name"] == "anchor.u"]
    assert len(u_entry) == 1
    u_index = u_entry[0]["index"]
    U = c.node("variable", u_index)
    assert c.variables[-1]["name"] == "common denominator inverse"
    inverse_index = c.variables[-1]["index"]
    other_rows = [row for row in c.equations if row is not original_anchor]

    private_indices = [next(v["index"] for v in c.variables if v["name"] == "anchor."+name)
                       for name in ("u", "v", "w")]
    assert private_indices[0] == u_index
    for private_index in private_indices:
        private_dep = dependence(c.nodes, private_index)
        assert not private_dep[original_anchor["denominator"]]
        assert not any(private_dep[row[key]] for row in other_rows
                       for key in ("numerator", "denominator"))
        assert not any(private_dep[g] for g in c.guards)

    dep = dependence(c.nodes, u_index)
    assert not dep[original_anchor["denominator"]]
    assert not any(dep[row[key]] for row in other_rows
                   for key in ("numerator", "denominator"))
    assert not any(dep[g] for g in c.guards)

    coeffs = coefficients_in_private_variable(
        c, original_anchor["numerator"], u_index)
    assert set(coeffs) <= {0, 2} and 2 in coeffs
    N = coeffs.get(0, c.zero)
    B = original_anchor["denominator"]
    # The coefficient of u^2 in the cleared equation is exactly its denominator.
    assert c.factors(coeffs[2]) == c.factors(B)
    dep = dependence(c.nodes, u_index)
    assert not dep[N] and not dep[B]

    G = parent["guard_product_node"]
    guard_factors = set(c.factors(G))
    denominator_factors = set(c.factors(B))
    assert all(c.nodes[a][0] == "int" or a in guard_factors
               for a in denominator_factors)
    for row in other_rows:
        assert all(c.nodes[a][0] == "int" or a in guard_factors
                   for a in c.factors(row["denominator"]))

    # B is a polynomial square. On the guarded locus, t=sqrt(B)*u gives
    # the equivalent private equation t^2+N=0. The three anchor witnesses
    # can be adjusted rationally so that u is nonzero; see the proof.
    bf = c.factors(B)
    assert all(e % 2 == 0 for e in bf.values())
    S = c.from_factors({a: e//2 for a, e in bf.items()})
    assert c.factors(c.power(S, 2)) == bf
    f0, f1 = producer.anchor_arguments
    r = f0*f0 + f0*f1 - f1*f1
    assert c.factors(c.power(r.d, 2)) == bf
    C4 = c.power(c.node("int", 3), 2**26)
    # Raw nodes keep the outer identity easy to audit independently.
    G2, U2 = c.node("pow", G, 2), c.node("pow", U, 2)
    psi = c.node("add", c.one, c.node("mul", N, G2, U2))
    final_terms = [c.node("pow", row["numerator"], 2) for row in other_rows]
    final_terms.append(c.node("pow", psi, 2))
    final = c.node("add", *final_terms)

    evidence = {
        "anchor_variable_index": u_index,
        "original_anchor_numerator": original_anchor["numerator"],
        "original_anchor_denominator": original_anchor["denominator"],
        "anchor_A_numerator": N,
        "anchor_A_denominator": B,
        "anchor_u_squared_coefficient": coeffs[2],
        "anchor_denominator_square_root": S,
        "anchor_r_numerator": r.n,
        "anchor_r_denominator": r.d,
        "anchor_C_fourth_power": C4,
        "guard_product": G,
        "reciprocal_variable_node": U,
        "psi": psi,
    }
    roots = [final, *c.guards]
    roots += [v for k, v in evidence.items() if k != "anchor_variable_index"]
    roots += [row[key] for row in other_rows for key in ("numerator", "denominator")]
    nodes, renumber = prune(c.nodes, roots)
    assert all(node != ["variable", inverse_index] for node in nodes)
    variables = [dict(v) for v in c.variables[:-1]]
    variables[u_index]["name"] = "anchor.reciprocal_U"
    assert len(variables) == 854
    final_dep = set()
    todo = [renumber[final]]
    while todo:
        i = todo.pop()
        if i in final_dep:
            continue
        final_dep.add(i)
        todo.extend(children(nodes[i]))
    used = {nodes[i][1] for i in final_dep if nodes[i][0] == "variable"}
    assert used == set(range(854))

    bdeg, bbits = c.bounds[final]
    branches = parent["report"]["finite_branches"]
    report = {
        "total_variables": 854,
        "existential_witnesses": 853,
        "categories": dict(Counter(v["category"] for v in variables)),
        "point_charts": c.point_count,
        "pole_blocks": c.pole_count,
        "residuals_per_branch": len(other_rows) + 1,
        "distinct_nonzero_guards": len(c.guards),
        "distinct_guard_factors": len(guard_factors),
        "template_nodes": len(nodes),
        "finite_branches": branches,
        "branch_degree_upper_bound": bdeg,
        "branch_coefficient_log2_upper_bound": bbits,
        "degree_upper_bound": bdeg * branches,
        "coefficient_log2_upper_bound": bbits * branches,
        "bounds_are_upper_bounds_not_exact_expansion_statistics": True,
        "all_variables_occur_in_template_output": True,
        "private_anchor_witness_and_denominator_coverage_checked": True,
        "parent_855_circuit_sha256": hashlib.sha256(parent_bytes).hexdigest(),
        "scope": "Exact integer-polynomial circuit specification obtained from the 855-variable construction by a proved nonzero-private-anchor, square-rescaling, and reciprocal transformation. Arithmetic characterization inherits the source theorem; no global minimality claimed.",
    }
    obj = {
        "format": parent["format"],
        "source_commit": parent["source_commit"],
        "semantics": parent["semantics"],
        "variables": variables,
        "nodes": nodes,
        "template_output": renumber[final],
        "finite_parameters": parent["finite_parameters"],
        "rational_equations_before_clearing": [
            {"numerator": renumber[row["numerator"]],
             "denominator": renumber[row["denominator"]], "label": row["label"]}
            for row in other_rows
        ],
        "nonzero_numerators": sorted(renumber[g] for g in c.guards),
        "guard_product_node": renumber[G],
        "anchor_reciprocal_certificate": {
            k: v if k == "anchor_variable_index" else renumber[v]
            for k, v in evidence.items()
        } | {"private_anchor_variable_indices": private_indices},
        "report": report,
    }
    return obj


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    obj = build()
    raw = (json.dumps(obj, separators=(",", ":")) + "\n").encode()
    (args.output / "polynomial-circuit.json").write_bytes(raw)
    report = obj["report"] | {
        "circuit_sha256": hashlib.sha256(raw).hexdigest(),
        "circuit_bytes": len(raw),
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parent_producer_sha256": hashlib.sha256(
            Path(__file__).with_name("build_compact_polynomial.py").read_bytes()).hexdigest(),
    }
    (args.output / "construction-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
