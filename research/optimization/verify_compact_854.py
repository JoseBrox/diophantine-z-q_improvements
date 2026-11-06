#!/usr/bin/env python3
"""Exact audit of the private-anchor transformation from 855 to 854 variables.

This verifier imports neither producer. It reads both emitted DAGs, compares
unchanged expressions by exact structural interning, and verifies the anchor
identities by sparse polynomial arithmetic with opaque common subexpressions.
The arithmetic characterization of the original system is a separate theorem;
see the parent audit in compact-audit-855.md.
"""
from collections import Counter
from functools import lru_cache
import argparse
import hashlib
import json
from math import prod
from pathlib import Path


PARENT_SHA = "6a1174891dccdd55bfc4cb6e7486cca2a4fde99ee8a755adaac0174f370da55b"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def children(node):
    op, *args = node
    if op in ("int", "variable", "parameter"):
        return []
    if op in ("neg", "pow"):
        return args[:1]
    if op in ("add", "mul"):
        return args
    raise ValueError("Unknown operation: " + str(op))


def plus(*polynomials):
    out = Counter()
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def times(*polynomials):
    out = {(): 1}
    for polynomial in polynomials:
        result = Counter()
        for m, c in out.items():
            for n, d in polynomial.items():
                result[tuple(sorted(m+n))] += c*d
        out = {m: c for m, c in result.items() if c}
    return out


def power(polynomial, exponent):
    out = {(): 1}
    while exponent:
        if exponent & 1:
            out = times(out, polynomial)
        polynomial = times(polynomial, polynomial)
        exponent >>= 1
    return out


def sparse_expander(nodes, atoms):
    """Expand only the small outer circuit, treating each atom as independent."""
    @lru_cache(None)
    def expand(index):
        if index in atoms:
            return {(index,): 1}
        op, *a = nodes[index]
        if op == "int":
            return {(): a[0]} if a[0] else {}
        if op == "neg":
            return {m: -c for m, c in expand(a[0]).items()}
        if op == "add":
            return plus(*(expand(k) for k in a))
        if op == "mul":
            return times(*(expand(k) for k in a))
        if op == "pow":
            check(a[1] < 100, "Unexpected expansion outside the certified frontier")
            return power(expand(a[0]), a[1])
        raise ValueError("Unrecognized leaf outside the certified frontier")
    return expand


def structurally_intern(objects):
    """Collision-free equality of expression trees across node renumberings."""
    table, outputs = {}, []
    for obj in objects:
        ids = []
        for node in obj["nodes"]:
            op, *args = node
            if op in ("int", "variable", "parameter"):
                key = tuple(node)
            elif op == "pow":
                key = (op, ids[args[0]], args[1])
            else:
                key = (op, *(ids[a] for a in args))
            if key not in table:
                table[key] = len(table)
            ids.append(table[key])
        outputs.append(ids)
    return outputs


def audit(parent, obj):
    nodes = obj["nodes"]
    variables = obj["variables"]
    certificate = obj["anchor_reciprocal_certificate"]
    u_index = certificate["anchor_variable_index"]
    U = certificate["reciprocal_variable_node"]
    N = certificate["anchor_A_numerator"]
    B = certificate["anchor_A_denominator"]
    S = certificate["anchor_denominator_square_root"]
    G = certificate["guard_product"]
    one = {(): 1}
    check(len(variables) == 854, "Wrong variable count")
    check([v["index"] for v in variables] == list(range(854)), "Variable indices differ")
    check(parent["variables"][-1]["name"] == "common denominator inverse", "Wrong deleted coordinate")
    for new, old in zip(variables, parent["variables"][:-1]):
        expected = old | ({"name": "anchor.reciprocal_U"} if old["index"] == u_index else {})
        check(new == expected, "Unexpected changed variable")
    check(parent["variables"][u_index]["name"] == "anchor.u", "Wrong private anchor coordinate")
    check(nodes[U] == ["variable", u_index], "Wrong reciprocal coordinate node")
    private_indices = certificate["private_anchor_variable_indices"]
    check(private_indices == [next(v["index"] for v in parent["variables"] if v["name"] == "anchor."+name)
                              for name in ("u", "v", "w")], "Wrong private anchor variables")
    check(obj["source_commit"] == parent["source_commit"], "Source revision changed")
    check(obj["finite_parameters"] == parent["finite_parameters"], "Parameter branches changed")
    check(obj["semantics"] == parent["semantics"], "Finite-product semantics changed")

    dep, factors, literal_zero, bounds = [], [], [], []
    for index, node in enumerate(nodes):
        check(isinstance(node, list) and node, "Invalid DAG node")
        op, *a = node
        kids = children(node)
        check(all(type(k) is int and 0 <= k < index for k in kids), "Non-topological DAG")
        dep.append(node == ["variable", u_index] or any(dep[k] for k in kids))
        if op == "int":
            check(len(a) == 1 and type(a[0]) is int, "Noninteger constant")
            fs = frozenset(); zero = a[0] == 0
            bound = (0, (abs(a[0])-1).bit_length() if a[0] else 0)
        elif op == "variable":
            check(len(a) == 1 and type(a[0]) is int and 0 <= a[0] < 854, "Invalid coordinate")
            fs = frozenset((index,)); zero = False; bound = (1, 0)
        elif op == "parameter":
            check(len(a) == 2 and a[0] in obj["finite_parameters"], "Invalid parameter")
            magnitude = max(map(abs, obj["finite_parameters"][a[0]]))
            check(type(a[1]) is int and a[1] >= magnitude, "Parameter bound understated")
            fs = frozenset((index,)); zero = False; bound = (0, (magnitude-1).bit_length())
        elif op == "neg":
            check(len(a) == 1, "Invalid negation")
            fs, zero, bound = factors[a[0]], literal_zero[a[0]], bounds[a[0]]
        elif op == "add":
            check(len(a) >= 2, "Invalid addition")
            fs = frozenset((index,)); zero = False
            bound = (max(bounds[k][0] for k in a),
                     max(bounds[k][1] for k in a)+(len(a)-1).bit_length())
        elif op == "mul":
            check(len(a) >= 2, "Invalid multiplication")
            fs = frozenset().union(*(factors[k] for k in a))
            zero = any(literal_zero[k] for k in a)
            bound = tuple(sum(bounds[k][j] for k in a) for j in (0, 1))
        elif op == "pow":
            check(len(a) == 2 and type(a[1]) is int and a[1] >= 0, "Invalid power")
            fs = factors[a[0]] if a[1] else frozenset()
            zero = literal_zero[a[0]] and a[1] != 0
            bound = tuple(k*a[1] for k in bounds[a[0]])
        factors.append(fs); literal_zero.append(zero); bounds.append(bound)

    parent_ids, ids = structurally_intern([parent, obj])
    old_rows = parent["rational_equations_before_clearing"]
    old_anchor = [r for r in old_rows if r["label"] == "packed semilocal anchor"]
    check(len(old_anchor) == 1, "Parent does not have one anchor")
    old_anchor = old_anchor[0]
    expected_rows = [(r["label"], parent_ids[r["numerator"]], parent_ids[r["denominator"]])
                     for r in old_rows if r is not old_anchor]
    rows = obj["rational_equations_before_clearing"]
    actual_rows = [(r["label"], ids[r["numerator"]], ids[r["denominator"]]) for r in rows]
    check(actual_rows == expected_rows and len(rows) == 296, "An untouched residual changed")
    check(ids[certificate["original_anchor_numerator"]] == parent_ids[old_anchor["numerator"]],
          "Anchor numerator reference changed")
    check(ids[B] == parent_ids[old_anchor["denominator"]]
          and B == certificate["original_anchor_denominator"], "Anchor denominator changed")
    guards = obj["nonzero_numerators"]
    check(Counter(ids[g] for g in guards) == Counter(parent_ids[g] for g in parent["nonzero_numerators"]),
          "Guard list changed")
    check(ids[G] == parent_ids[parent["guard_product_node"]]
          and G == obj["guard_product_node"], "Guard product changed")
    check(not any(dep[r[key]] for r in rows for key in ("numerator", "denominator"))
          and not any(dep[g] for g in guards) and not dep[N] and not dep[B]
          and not dep[S] and not dep[G],
          "Anchor witness is not private")
    for private_index in private_indices[1:]:
        private_dep = []
        for node in nodes:
            private_dep.append(node == ["variable", private_index]
                               or any(private_dep[k] for k in children(node)))
        check(not any(private_dep[r[key]] for r in rows for key in ("numerator", "denominator"))
              and not any(private_dep[g] for g in guards) and not private_dep[B],
              "One of the other two anchor witnesses is not private")
    required = frozenset().union(*(factors[g] for g in guards))
    check(not any(literal_zero[g] for g in guards), "Literal-zero guard")
    check(factors[G] == required and not literal_zero[G], "Guard product misses a divisor")
    for denominator in [B, *(r["denominator"] for r in rows)]:
        check(not literal_zero[denominator] and factors[denominator] <= required,
              "An expression denominator has an unguarded factor")

    # Expose only the old anchor's small dependence on u; every independent
    # child becomes an opaque symbol. This is a formal polynomial identity,
    # stronger than an equality tested at arithmetic samples.
    frontier, visited, todo = set(), set(), [certificate["original_anchor_numerator"]]
    while todo:
        index = todo.pop()
        if index in visited:
            continue
        visited.add(index)
        if not dep[index]:
            frontier.add(index)
        else:
            todo.extend(children(nodes[index]))
    expand = sparse_expander(nodes, frontier | {U})
    old_n = expand(certificate["original_anchor_numerator"])
    check(old_n == plus(times(expand(B), power(expand(U), 2)), expand(N)),
          "The cleared anchor is not B*u^2+N")
    check(expand(certificate["anchor_u_squared_coefficient"]) == expand(B),
          "Incorrect quadratic coefficient certificate")

    # Independently verify the polynomial square B=S^2 by expanding its
    # multiplicative structure only. Opaque factors remain formal atoms.
    @lru_cache(None)
    def multiplicities(index):
        op, *a = nodes[index]
        if op == "int" and a[0] == 1:
            return Counter()
        if op == "mul":
            out = Counter()
            for child in a:
                out.update(multiplicities(child))
            return out
        if op == "pow":
            return Counter({k: v*a[1] for k, v in multiplicities(a[0]).items()})
        check(op != "neg", "Unexpected negation in the denominator square")
        return Counter({index: 1})
    check(multiplicities(B) == Counter({k: 2*v for k, v in multiplicities(S).items()}),
          "The anchor denominator is not the certified square")

    # Certify the complete ternary anchor, including its nonzero right-hand
    # side. This justifies choosing u!=0 after changing the two other
    # private anchor witnesses, with every outside coordinate held fixed.
    R = certificate["anchor_r_numerator"]
    rden = certificate["anchor_r_denominator"]
    C4 = certificate["anchor_C_fourth_power"]
    check(multiplicities(B) == Counter({k: 2*v for k, v in multiplicities(rden).items()}),
          "Wrong denominator for the anchor parameter r")
    check(nodes[C4][0] == "pow" and nodes[C4][2] == 2**26
          and nodes[nodes[C4][1]] == ["int", 3], "Wrong fixed nonzero anchor constant")
    coordinate_nodes = {node[1]: i for i, node in enumerate(nodes) if node[0] == "variable"}
    uvw = [coordinate_nodes[k] for k in private_indices]
    atoms = {k for k in set(multiplicities(B)) | set(multiplicities(R)) if nodes[k][0] != "int"}
    full = sparse_expander(nodes, atoms | set(uvw) | {C4})
    u0, v0, w0 = [full(k) for k in uvw]
    target_anchor = plus(
        times(full(B), plus(power(u0, 2), times({(): 6}, power(v0, 2)),
                            times({(): -2}, power(w0, 2)), times({(): 2}, full(C4)))),
        times({(): -3}, power(full(R), 2)))
    check(full(certificate["original_anchor_numerator"]) == target_anchor,
          "The ternary anchor is not B*(u^2+6v^2-2w^2+2*C^4)-3*R^2")

    # Check the actual single reciprocal expression over Z[G,N,U].
    outer = sparse_expander(nodes, {G, N, U})
    g, n, u = (outer(k) for k in (G, N, U))
    psi = plus(one, times(n, power(g, 2), power(u, 2)))
    check(outer(certificate["psi"]) == psi, "Reciprocal-guard polynomial differs")
    output = nodes[obj["template_output"]]
    check(output[0] == "add", "Output is not a sum of squares")
    expected_squared = Counter(r["numerator"] for r in rows)
    expected_squared[certificate["psi"]] += 1
    actual_squared = Counter()
    for index in output[1:]:
        check(nodes[index][0] == "pow" and nodes[index][2] == 2, "A summand is not a square")
        actual_squared[nodes[index][1]] += 1
    check(actual_squared == expected_squared, "Incorrect final sum of squares")

    reached, todo = set(), [obj["template_output"]]
    while todo:
        index = todo.pop()
        if index in reached:
            continue
        reached.add(index); todo.extend(children(nodes[index]))
    used = {nodes[k][1] for k in reached if nodes[k][0] == "variable"}
    check(used == set(range(854)), "A declared variable is absent from the output DAG")
    branch_degree, branch_bits = bounds[obj["template_output"]]
    branches = prod(map(len, obj["finite_parameters"].values()))
    report = obj["report"]
    check(report["degree_upper_bound"] == branch_degree*branches
          and report["coefficient_log2_upper_bound"] == branch_bits*branches,
          "Incorrect global degree or coefficient bound")
    check(report["total_variables"] == 854 and report["existential_witnesses"] == 853
          and report["finite_branches"] == branches == 54272, "Incorrect report inventory")
    return {
        "status": "passed",
        "total_variables": 854,
        "existential_witnesses": 853,
        "unchanged_rational_residuals_checked_exactly": len(rows),
        "unchanged_guards_checked_exactly": len(guards),
        "guard_factors": len(required),
        "cleared_anchor_polynomial_identity": "B*u^2+N",
        "anchor_denominator_polynomial_square_checked": True,
        "complete_ternary_anchor_and_three_private_witnesses_checked": True,
        "opaque_anchor_subexpressions": len(frontier),
        "reciprocal_polynomial_identity_checked_exactly": "1+N*G^2*U^2",
        "squares_per_branch": len(output)-1,
        "finite_branches": branches,
        "dag_nodes": len(nodes),
        "output_reachable_nodes": len(reached),
        "all_declared_coordinates_reached": True,
        "degree_upper_bound": branch_degree*branches,
        "coefficient_log2_upper_bound": branch_bits*branches,
        "scope": "Exact emitted-circuit transformation and bounds, without importing either producer. Arithmetic correctness of the inherited source definition is outside this transformation audit.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, default=Path(__file__).with_name("polynomial-855") / "polynomial-circuit.json")
    parser.add_argument("--circuit", type=Path, default=Path(__file__).with_name("polynomial-854") / "polynomial-circuit.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("polynomial-854") / "verification.json")
    args = parser.parse_args()
    parent_raw, raw = args.parent.read_bytes(), args.circuit.read_bytes()
    check(hashlib.sha256(parent_raw).hexdigest() == PARENT_SHA, "Unaudited parent circuit revision")
    report = audit(json.loads(parent_raw), json.loads(raw)) | {
        "parent_circuit_sha256": PARENT_SHA,
        "circuit_sha256": hashlib.sha256(raw).hexdigest(),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
