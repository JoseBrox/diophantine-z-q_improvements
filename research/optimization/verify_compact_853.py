#!/usr/bin/env python3
"""Exact emitted-DAG audit of polynomial-853, importing no circuit producer.

The reader verifies the two quadratic equations' combination, every cleared
residual's rational substitution by an inductive polynomial certificate,
the parent comparison, denominator-guard removal, and arithmetic-DAG bounds.
It reuses small exact-polynomial helpers from the independent 854 verifier
and reruns the separate pole-guard verifier.
"""
from collections import Counter
from functools import lru_cache
import argparse
import hashlib
import json
from math import prod
from pathlib import Path

from verify_compact_854 import PARENT_SHA, check, children, plus, times, power, sparse_expander
import verify_pole_guard_removal as pole_verifier


def intern(objects, mappings):
    table, results = {}, []

    def make(*key):
        if key not in table:
            table[key] = len(table)
        return table[key]

    for obj, mapping in zip(objects, mappings):
        ids = []
        for op, *a in obj["nodes"]:
            if op == "variable":
                value = make(op, mapping[a[0]])
            elif op in ("int", "parameter"):
                value = make(op, *a)
            elif op == "pow":
                value = make(op, ids[a[0]], a[1])
            else:
                value = make(op, *(ids[k] for k in a))
            ids.append(value)
        results.append(ids)
    return results, make


def node_data(obj, mapping):
    bounds, support = [], []
    for index, node in enumerate(obj["nodes"]):
        check(isinstance(node, list) and node, "Invalid node")
        op, *a = node
        kids = children(node)
        check(all(type(k) is int and 0 <= k < index for k in kids), "Non-topological DAG")
        if op == "variable":
            check(len(a) == 1 and type(a[0]) is int and 0 <= a[0] < len(mapping), "Invalid variable")
            bound, mask = (1, 0), 1 << mapping[a[0]]
        elif op == "int":
            check(len(a) == 1 and type(a[0]) is int, "Noninteger constant")
            bound, mask = (0, (abs(a[0])-1).bit_length() if a[0] else 0), 0
        elif op == "parameter":
            check(len(a) == 2 and a[0] in obj["finite_parameters"], "Invalid parameter")
            magnitude = max(map(abs, obj["finite_parameters"][a[0]]))
            check(type(a[1]) is int and a[1] >= magnitude, "Understated parameter bound")
            bound, mask = (0, (magnitude-1).bit_length()), 0
        else:
            mask = 0
            for child in kids:
                mask |= support[child]
            if op == "neg":
                check(len(a) == 1, "Invalid negation")
                bound = bounds[a[0]]
            elif op == "add":
                check(len(a) >= 2, "Invalid addition")
                bound = (max(bounds[k][0] for k in a),
                         max(bounds[k][1] for k in a)+(len(a)-1).bit_length())
            elif op == "mul":
                check(len(a) >= 2, "Invalid multiplication")
                bound = tuple(sum(bounds[k][j] for k in a) for j in (0, 1))
            elif op == "pow":
                check(len(a) == 2 and type(a[1]) is int and a[1] >= 0, "Invalid power")
                bound = tuple(k*a[1] for k in bounds[a[0]])
        bounds.append(bound); support.append(mask)
    return bounds, support


def audit(parent, obj, pole_receipt):
    nodes, old_nodes = obj["nodes"], parent["nodes"]
    cert = obj["quadratic_combination_certificate"]
    mapping = obj["parent_variable_indices"]
    tau = cert["removed_pell_variable_index_in_parent"]
    check(parent["variables"][tau]["name"] == "proxy.t", "Wrong removed Pell variable")
    check(mapping == [i for i in range(855) if i not in (tau, 854)], "Wrong variable deletion map")
    check(len(obj["variables"]) == 853, "Wrong variable count")
    u_index = cert["private_anchor_variable_indices"][0]
    old_private = [next(v["index"] for v in parent["variables"] if v["name"] == "anchor."+name)
                   for name in ("u", "v", "w")]
    check([mapping[k] for k in cert["private_anchor_variable_indices"]] == old_private,
          "Wrong private anchor indices")
    for new, old_index in zip(obj["variables"], mapping):
        expected = dict(parent["variables"][old_index], index=mapping.index(old_index))
        if old_index == old_private[0]:
            expected["name"] = "anchor.reciprocal_U"
        check(new == expected, "Changed variable identity")
    check(obj["source_commit"] == parent["source_commit"] and obj["semantics"] == parent["semantics"]
          and obj["finite_parameters"] == parent["finite_parameters"], "Changed source or parameter semantics")
    bounds, support = node_data(obj, mapping)
    _, old_support = node_data(parent, list(range(855)))
    (old_ids, ids), make = intern([parent, obj], [list(range(855)), mapping])

    check(pole_receipt["status"] == "PASS" and pole_receipt["parent_circuit_sha256"] == PARENT_SHA,
          "Pole guard audit did not pass on the pinned parent")
    removed = sorted(b["delta_numerator_node"] for b in pole_receipt["pole_blocks"])
    retained = pole_receipt["retained_guard_numerator_nodes"]
    check(obj["removed_guard_nodes_in_parent"] == removed and len(removed) == 42, "Wrong removed guards")
    check(Counter(ids[k] for k in obj["nonzero_numerators"]) == Counter(old_ids[k] for k in retained),
          "A retained guard changed")
    pole_blocks = {b["label"]: b for b in pole_receipt["pole_blocks"]}
    check(len(obj["pole_guard_certificate"]) == 42, "Wrong pole certificate inventory")
    for block in obj["pole_guard_certificate"]:
        reference = pole_blocks[block["label"]]
        check(block["removed_guard_in_parent"] == reference["delta_numerator_node"]
              and block["argument_denominator_in_parent"] == reference["delta_denominator_node"],
              "A recorded pole argument differs from the guard certificate")

    U, N, B, S, G = [cert[k] for k in ("reciprocal_variable_node", "anchor_A_numerator",
                                     "anchor_A_denominator", "anchor_denominator_square_root", "guard_product")]
    P, Q, Psi = [cert[k] for k in ("tau_numerator", "tau_denominator", "psi")]
    A, b0, Delta = [cert[k] for k in ("pell_linear_coefficient", "pell_constant_coefficient", "pell_discriminant")]
    check(nodes[U] == ["variable", u_index], "Wrong reciprocal witness")
    expected_G = make("mul", *(old_ids[k] for k in pole_receipt["retained_guard_factor_nodes"]))
    check(ids[G] == expected_G and G == obj["guard_product_node"], "Guard product differs")
    private_mask = sum(1 << k for k in old_private)
    check(not support[G] & (private_mask | (1 << tau)), "Guard depends on eliminated coordinates")
    check(not support[N] & ((1 << old_private[0]) | (1 << tau)), "Anchor coefficient depends on u or tau")

    old_rows = parent["rational_equations_before_clearing"]
    old_anchor = next(r for r in old_rows if r["label"] == "packed semilocal anchor")
    old_pell = next(r for r in old_rows if r["label"] == "Lucas relation")
    originals = [r for r in old_rows if r is not old_anchor and r is not old_pell]
    check(len(originals) == len(obj["transformed_equations"]) == 295, "Wrong residual count")
    for row in originals+[old_pell]:
        check(not (old_support[row["numerator"]] | old_support[row["denominator"]]) & private_mask,
              "An anchor witness is not private in the original system")
    check(ids[cert["original_anchor_numerator"]] == old_ids[old_anchor["numerator"]]
          and ids[B] == old_ids[old_anchor["denominator"]], "Anchor reference changed")
    check(cert["original_pell_numerator_in_parent"] == old_pell["numerator"], "Pell reference changed")

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
            return Counter({k: e*a[1] for k, e in multiplicities(a[0]).items()})
        check(op != "neg", "Unexpected denominator negation")
        return Counter({index: 1})

    check(multiplicities(B) == Counter({k: 2*e for k, e in multiplicities(S).items()}),
          "Anchor denominator is not a polynomial square")
    R, rd, C4 = [cert[k] for k in ("anchor_r_numerator", "anchor_r_denominator", "anchor_C_fourth_power")]
    check(multiplicities(B) == Counter({k: 2*e for k, e in multiplicities(rd).items()}),
          "Wrong anchor rational denominator")
    check(nodes[C4][0] == "pow" and nodes[C4][2] == 2**26
          and nodes[nodes[C4][1]] == ["int", 3], "Wrong anchor constant")
    variable_nodes = {node[1]: i for i, node in enumerate(nodes) if node[0] == "variable"}
    uvw = [variable_nodes[k] for k in cert["private_anchor_variable_indices"]]
    atoms = {k for k in set(multiplicities(B)) | set(multiplicities(R)) if nodes[k][0] != "int"}
    anchor_expand = sparse_expander(nodes, atoms | set(uvw) | {C4})
    u, v, w = [anchor_expand(k) for k in uvw]
    full_anchor = plus(times(anchor_expand(B), plus(power(u, 2), times({(): 6}, power(v, 2)),
                       times({(): -2}, power(w, 2)), times({(): 2}, anchor_expand(C4)))),
                       times({(): -3}, power(anchor_expand(R), 2)))
    check(anchor_expand(cert["original_anchor_numerator"]) == full_anchor, "Incorrect ternary anchor")
    check(full_anchor == plus(times(anchor_expand(B), power(u, 2)), anchor_expand(N)),
          "Incorrect rescaled anchor numerator")

    # Verify the Pell relation itself and its completed-square parameters.
    old_varnodes = {node[1]: i for i, node in enumerate(old_nodes) if node[0] == "variable"}
    old_by_name = {v["name"]: v["index"] for v in parent["variables"]}
    old_proxy_nodes = [old_varnodes[old_by_name["proxy."+k]] for k in ("s", "t", "z")]
    pell_old = sparse_expander(old_nodes, set(old_proxy_nodes))
    os, ot, oz = [pell_old(k) for k in old_proxy_nodes]
    oa = times(os, plus(os, {(): -2}), oz)
    ob = plus(times(power(plus(os, {(): -2}), 2), power(oz, 2)), {(): -1})
    check(pell_old(old_pell["numerator"]) == plus(power(ot, 2), times({(): -1}, oa, ot), ob)
          and old_nodes[old_pell["denominator"]] == ["int", 1], "Original Pell polynomial differs")
    new_s = variable_nodes[mapping.index(old_by_name["proxy.s"])]
    new_z = variable_nodes[mapping.index(old_by_name["proxy.z"])]
    pell = sparse_expander(nodes, {new_s, new_z})
    ss, zz = pell(new_s), pell(new_z)
    aa = times(ss, plus(ss, {(): -2}), zz)
    bb = plus(times(power(plus(ss, {(): -2}), 2), power(zz, 2)), {(): -1})
    dd = plus(power(aa, 2), times({(): -4}, bb))
    check(pell(A) == aa and pell(b0) == bb and pell(Delta) == dd, "Wrong completed-square parameters")

    # Exact identities in the small formal ring Z[N,Delta,A,G,U].
    outer = sparse_expander(nodes, {N, Delta, A, G, U})
    n, d, a, g, u = [outer(k) for k in (N, Delta, A, G, U)]
    y = times(g, u)
    one = {(): 1}
    expected_psi = plus(one, times({(): 2}, plus(n, times({(): -1}, d)), power(y, 2)),
                        times(power(plus(n, d), 2), power(y, 4)))
    expected_p = plus(one, times({(): 2}, a, y), times(plus(n, d), power(y, 2)))
    expected_q = times({(): 4}, y)
    check(outer(Psi) == expected_psi and outer(P) == expected_p and outer(Q) == expected_q,
          "Incorrect reciprocal or reconstruction polynomial")
    t_num = plus(one, times({(): -1}, plus(n, d), power(y, 2)))
    v_num = plus(one, times(plus(n, d), power(y, 2)))
    check(plus(power(t_num, 2), times({(): 4}, n, power(y, 2))) == expected_psi,
          "Anchor reconstruction identity failed")
    check(plus(power(v_num, 2), times({(): -4}, d, power(y, 2))) == expected_psi,
          "Pell reconstruction identity failed")

    # Exact inductive certificate: an old polynomial H is replaced by
    # Q^d H(P/Q). Identity is checked through canonical expression trees;
    # no evaluation or numerical identity heuristic is used.
    image_ids, degrees = [], []
    pid, qid = ids[P], ids[Q]
    for index, node in enumerate(old_nodes):
        op, *args = node
        if not old_support[index] >> tau & 1:
            image, degree = old_ids[index], 0
        elif op == "variable":
            check(args == [tau], "Invalid substituted variable")
            image, degree = pid, 1
        elif op == "neg":
            image, degree = make(op, image_ids[args[0]]), degrees[args[0]]
        elif op == "mul":
            image = make(op, *(image_ids[k] for k in args))
            degree = sum(degrees[k] for k in args)
        elif op == "pow":
            image, degree = make(op, image_ids[args[0]], args[1]), degrees[args[0]]*args[1]
        elif op == "add":
            degree = max(degrees[k] for k in args)
            terms = []
            for k in args:
                gap = degree-degrees[k]
                multiplier = qid if gap == 1 else make("pow", qid, gap) if gap else None
                terms.append(image_ids[k] if gap == 0 else make("mul", image_ids[k], multiplier))
            image = make(op, *terms)
        else:
            raise ValueError("Unexpected dependent source node")
        image_ids.append(image); degrees.append(degree)
    rows = obj["transformed_equations"]
    for new, old in zip(rows, originals):
        check(new["label"] == old["label"] and new["parent_numerator"] == old["numerator"]
              and new["parent_denominator"] == old["denominator"], "Changed source residual reference")
        check(ids[new["numerator"]] == image_ids[old["numerator"]]
              and new["homogenizing_exponent"] == degrees[old["numerator"]],
              "Homogenized residual substitution failed: "+new["label"])

    output = nodes[obj["template_output"]]
    check(output[0] == "add", "Output is not an addition")
    actual = Counter()
    for index in output[1:]:
        check(nodes[index][0] == "pow" and nodes[index][2] == 2, "An output summand is not a square")
        actual[nodes[index][1]] += 1
    expected = Counter(row["numerator"] for row in rows)
    expected[Psi] += 1
    check(actual == expected, "Final sum of squares differs")
    check(support[obj["template_output"]] == sum(1 << k for k in mapping), "Not all declared variables are reached")
    branches = prod(map(len, obj["finite_parameters"].values()))
    degree, bits = bounds[obj["template_output"]]
    report = obj["report"]
    check(report["degree_upper_bound"] == branches*degree
          and report["coefficient_log2_upper_bound"] == branches*bits
          and report["finite_branches"] == branches == 54272, "Incorrect degree, height, or branch bound")
    return {
        "status": "passed",
        "total_variables": 853,
        "existential_witnesses": 852,
        "exactly_checked_substituted_residuals": len(rows),
        "omitted_pole_guards": len(removed),
        "retained_guards": len(retained),
        "retained_guard_factors": len(pole_receipt["retained_guard_factor_nodes"]),
        "full_private_anchor_and_pell_identities_checked": True,
        "quartic_and_both_reconstruction_identities_checked": True,
        "homogenization_identity": "new_H = Q^d * old_H(P/Q)",
        "maximum_homogenizing_exponent": max(r["homogenizing_exponent"] for r in rows),
        "squares_per_branch": len(rows)+1,
        "finite_branches": branches,
        "dag_nodes": len(nodes),
        "all_declared_variables_reached": True,
        "degree_upper_bound": degree*branches,
        "coefficient_log2_upper_bound": bits*branches,
        "scope": "Exact emitted-DAG transformation and reconstruction identities; pole-guard deletion is checked separately and rerun. Arithmetic characterization inherits the source theorem and the separately audited 855 rational formulas.",
    }


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--circuit", type=Path, default=root/"polynomial-853/polynomial-circuit.json")
    parser.add_argument("--output", type=Path, default=root/"polynomial-853/verification.json")
    args = parser.parse_args()
    pole_verifier.main()
    pole_receipt = json.loads((root/"pole-guard-removal-verification.json").read_text())
    parent_raw = (root/"polynomial-855/polynomial-circuit.json").read_bytes()
    check(hashlib.sha256(parent_raw).hexdigest() == PARENT_SHA, "Parent revision differs")
    raw = args.circuit.read_bytes()
    report = audit(json.loads(parent_raw), json.loads(raw), pole_receipt) | {
        "parent_circuit_sha256": PARENT_SHA,
        "circuit_sha256": hashlib.sha256(raw).hexdigest(),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pole_guard_verifier_sha256": hashlib.sha256((root/"verify_pole_guard_removal.py").read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
