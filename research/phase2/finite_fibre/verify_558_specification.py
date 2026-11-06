#!/usr/bin/env python3
"""Independent exact audit of the 558-variable indexed-polynomial specification.

No producer is imported. Source quadratic extraction, affine substitutions,
point quartics, monicity, triangularity, coordinate counts, and all norm/degree
inequalities are checked using integer arithmetic. Enormous multiplication
matrices and the final indexed product are not expanded by this audit.
"""
from collections import Counter
from functools import lru_cache
import argparse
import hashlib
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PARENT_SHA = "6a1174891dccdd55bfc4cb6e7486cca2a4fde99ee8a755adaac0174f370da55b"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def children(node):
    op, *a = node
    if op in ("int", "variable", "parameter", "algebra_generator"):
        return []
    if op in ("pow", "neg"):
        return a[:1]
    if op in ("add", "mul"):
        return a
    raise ValueError("Unknown node operation")


def support_table(nodes, kind="variable"):
    answer = []
    for i, node in enumerate(nodes):
        kids = children(node)
        check(all(type(k) is int and 0 <= k < i for k in kids), "Non-topological DAG")
        mask = 1 << node[1] if node[0] == kind else 0
        for k in kids:
            mask |= answer[k]
        answer.append(mask)
    return answer


def plus(*polys):
    out = Counter()
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def times(*polys):
    out = {(): 1}
    for poly in polys:
        result = Counter()
        for m, c in out.items():
            for n, d in poly.items():
                result[tuple(sorted(m+n))] += c*d
        out = {m: c for m, c in result.items() if c}
    return out


def power(poly, exponent):
    out = {(): 1}
    while exponent:
        if exponent & 1:
            out = times(out, poly)
        exponent >>= 1
        if exponent:
            poly = times(poly, poly)
    return out


def expander(nodes, atoms=None, variables=None, parameters=None, generators=None):
    atoms, variables = atoms or {}, variables or {}
    parameters, generators = parameters or {}, generators or {}

    @lru_cache(None)
    def expand(index):
        if index in atoms:
            return {(atoms[index],): 1}
        op, *a = nodes[index]
        if op == "int":
            return {(): a[0]} if a[0] else {}
        if op == "variable":
            check(a[0] in variables, "Unexpected variable in a small formal identity")
            return {(variables[a[0]],): 1}
        if op == "parameter":
            check(a[0] in parameters, "Unexpected parameter in a small formal identity")
            return {(parameters[a[0]],): 1}
        if op == "algebra_generator":
            check(a[0] in generators, "Unexpected algebra generator in a small formal identity")
            return {(generators[a[0]],): 1}
        if op == "neg":
            return {m: -c for m, c in expand(a[0]).items()}
        if op == "add":
            return plus(*(expand(k) for k in a))
        if op == "mul":
            return times(*(expand(k) for k in a))
        if op == "pow":
            check(a[1] < 100, "Escaped the intended formal-identity frontier")
            return power(expand(a[0]), a[1])
        raise ValueError(op)
    return expand


class Interner:
    """Exact expression-tree equality, including only 0/1 normalizations."""
    def __init__(self):
        self.table, self.nodes = {}, []
        self.zero, self.one = self.raw("int", 0), self.raw("int", 1)

    def raw(self, op, *a):
        key = (op, *a)
        if key not in self.table:
            self.table[key] = len(self.nodes); self.nodes.append(key)
        return self.table[key]

    def add(self, *a):
        a = tuple(k for k in a if k != self.zero)
        return self.zero if not a else a[0] if len(a) == 1 else self.raw("add", *a)

    def mul(self, *a):
        if self.zero in a:
            return self.zero
        a = tuple(k for k in a if k != self.one)
        return self.one if not a else a[0] if len(a) == 1 else self.raw("mul", *a)

    def pow(self, a, n):
        return self.one if n == 0 else a if n == 1 else self.raw("pow", a, n)

    def neg(self, a):
        return self.zero if a == self.zero else self.raw("neg", a)

    def read(self, nodes):
        answer = []
        for op, *a in nodes:
            if op in ("int", "variable", "parameter", "algebra_generator"):
                value = self.raw(op, *a)
            elif op == "pow":
                value = self.raw(op, answer[a[0]], a[1])
            else:
                value = self.raw(op, *(answer[k] for k in a))
            answer.append(value)
        return answer


def audit(parent, spec):
    check(spec["format"] == "integer-polynomial-indexed-finite-algebra-v1", "Unknown specification grammar")
    check(spec["parent_855_circuit_sha256"] == PARENT_SHA and spec["source_commit"] == parent["source_commit"],
          "Source identity changed")
    old_nodes = parent["nodes"]
    nodes = spec["coefficient_dag"]
    full_source = old_nodes+spec["coefficient_extraction_extension"]
    old_support = support_table(full_source)
    generator_support = support_table(nodes, "algebra_generator")
    base_support = support_table(nodes, "variable")
    old_variables = parent["variables"]
    old_by_name = {v["name"]: v["index"] for v in old_variables}
    old_points = [v for v in old_variables if v["category"] == "point" and v["name"].endswith(".C")]
    point_map = {v["index"]: i for i, v in enumerate(old_points)}
    private = [old_by_name["anchor.u"]]+[v["index"] for v in old_variables
               if v["category"] == "pole" and v["name"].endswith((".p", ".q"))]
    tau = old_by_name["proxy.t"]
    deleted = set(point_map) | set(private) | {tau, 854}
    retained = [i for i in range(855) if i not in deleted]
    base_map = {old: new for new, old in enumerate(retained)}
    check(len(retained) == 557 and len(point_map) == 211 and len(private) == 85, "Wrong source inventory")
    external = spec["external_variables"]
    check(len(external) == 558 and [v["index"] for v in external] == list(range(558)), "Wrong external variables")
    for new, old in zip(external[:-1], retained):
        check(new == dict(old_variables[old], index=base_map[old], parent_index=old), "Changed retained coordinate")
    check(external[-1] == {"index": 557, "name": "U", "category": "single finite-algebra witness"},
          "Wrong additional witness")
    check(spec["total_external_variables"] == 558 and spec["existential_witnesses"] == 557
          and spec["retained_base_variables"] == 557, "Incorrect reported variable count")
    parameters = spec["finite_parameters"]
    check(parameters["j"] == parent["finite_parameters"]["j"]
          and parameters["correction"] == parent["finite_parameters"]["correction"], "Source finite choices changed")
    check(parameters["quadratic_mask"] == {"from": 0, "to": 2**86-1, "bits": 86}, "Wrong quadratic masks")
    check(parameters["rank"] == {"formula": "4^211 * 2^popcount(quadratic_mask)"}
          and parameters["selector"] == {"from": 0, "to_formula": "297*rank*(rank+1)/2"}
          and parameters["degree_case"] == {"from": 1, "to_formula": "rank"}, "Wrong indexed ranges")
    for node in nodes:
        op, *a = node
        if op == "int":
            check(len(a) == 1 and type(a[0]) is int, "Noninteger coefficient")
        elif op == "variable":
            check(len(a) == 1 and 0 <= a[0] < 557, "Hidden external coordinate")
        elif op == "algebra_generator":
            check(len(a) == 1 and 0 <= a[0] < 297, "Unknown formal algebra generator")
        elif op == "parameter":
            check(len(a) == 2 and a[0] in ("j", "correction")
                  and a[1] >= max(map(abs, parameters[a[0]])), "Understated finite coefficient parameter")
        elif op == "pow":
            check(len(a) == 2 and type(a[1]) is int and a[1] >= 0, "Invalid exponent")
        elif op == "neg":
            check(len(a) == 1, "Invalid negation")
        elif op in ("add", "mul"):
            check(len(a) >= 2, "Invalid arithmetic arity")

    # Every source point quartic and every emitted coefficient is checked
    # exactly in the small ring Z[a0,a1,C,j], independently of node layouts.
    points = spec["point_relations"]
    check([p["generator"] for p in points] == list(range(211)), "Wrong point generators")
    old_rows = {row["label"]: row for row in parent["rational_equations_before_clearing"]}
    x, y, c, j = [{(i,): 1} for i in range(4)]
    A = plus(power(x, 3), times({(): 6}, x, power(y, 2)), times({(): -11}, x), times({(): 12}, y))
    B = plus(times({(): 3}, power(x, 2), y), times({(): 2}, power(y, 3)), times({(): -11}, y), times({(): 6}, x))
    j2p2 = plus(power(j, 2), {(): 2})
    K = plus(times(j2p2, A), times({(): 4}, j, B))
    J = plus(times({(): 2}, j, A), times(j2p2, B))
    lam = plus(power(j, 2), {(): -2})
    gamma = plus(times({(): 8}, power(c, 4)), times({(): -4}, K, power(c, 2)), power(J, 2))
    check(plus(power(K, 2), times({(): -2}, power(J, 2)))
          == times(power(lam, 2), plus(power(A, 2), times({(): -2}, power(B, 2)))),
          "Point discriminant identity failed")
    for point, old_point in zip(points, old_points):
        prefix = old_point["name"][:-2]
        a0, a1 = old_by_name[prefix+".a0"], old_by_name[prefix+".a1"]
        old_row = old_rows[prefix+".quartic half-point"]
        check(point["degree"] == 4 and point["parent_C_variable"] == old_point["index"]
              and point["parent_row_numerator"] == old_row["numerator"]
              and point["parent_row_denominator"] == old_row["denominator"], "Wrong point source reference")
        old_expand = expander(old_nodes, variables={a0: 0, a1: 1, old_point["index"]: 2}, parameters={"j": 3})
        check(plus(times({(): 4}, power(lam, 2), old_expand(old_row["numerator"])),
                   times(gamma, old_expand(old_row["denominator"]))) == {}, "A source point residual differs")
        new_expand = expander(nodes, variables={base_map[a0]: 0, base_map[a1]: 1}, parameters={"j": 3},
                              generators={point["generator"]: 2})
        expected = {"A": A, "B": B, "K": K, "J": J,
                    "constant_coefficient": times({(): 2}, power(J, 2)), "quadratic_coefficient": times({(): -2}, K),
                    "derivative_guard": plus(times({(): 4}, power(c, 3)), times({(): -4}, K, c))}
        for key, value in expected.items():
            check(new_expand(point[key]) == value, "A scaled point quartic or derivative differs")
        check(not generator_support[point["constant_coefficient"]]
              and not generator_support[point["quadratic_coefficient"]], "Point coefficient is not in the base ring")

    # Exact Pell completion; its zero-discriminant case is explicitly present.
    pell = spec["pell_certificate"]
    old_pell = old_rows["Lucas relation"]
    check(pell["parent_row"] == old_pell and pell["parent_tau_variable"] == tau
          and pell["tau_substitution_denominator"] == 2, "Changed Pell source")
    si, zi = old_by_name["proxy.s"], old_by_name["proxy.z"]
    old_pell_expand = expander(old_nodes, variables={si: 0, zi: 1, tau: 2})
    ss, zz, tt = x, y, c
    aa = times(ss, plus(ss, {(): -2}), zz)
    bb = plus(times(power(plus(ss, {(): -2}), 2), power(zz, 2)), {(): -1})
    dd = plus(power(aa, 2), times({(): -4}, bb))
    check(old_pell_expand(old_pell["numerator"]) == plus(power(tt, 2), times({(): -1}, aa, tt), bb)
          and old_nodes[old_pell["denominator"]] == ["int", 1], "Source Pell relation differs")
    new_pell_expand = expander(nodes, variables={base_map[si]: 0, base_map[zi]: 1}, generators={211: 2})
    check(new_pell_expand(pell["a"]) == aa and new_pell_expand(pell["b0"]) == bb
          and new_pell_expand(pell["discriminant"]) == dd
          and new_pell_expand(pell["tau_substitution_numerator"]) == plus(tt, aa), "Incorrect Pell completion")

    quads = spec["quadratic_relations"]
    check([q["generator"] for q in quads] == list(range(211, 297))
          and [q["bit"] for q in quads] == list(range(86)), "Wrong quadratic generators or zero branches")
    check(quads[0]["kind"] == "completed_pell" and nodes[quads[0]["L"]] == ["int", 1]
          and new_pell_expand(quads[0]["M"]) == times({(): -1}, dd), "Pell quadratic branch differs")
    private_mask = sum(1 << k for k in private)
    allowed_mask = sum(1 << k for k in retained) | sum(1 << k for k in point_map) | (1 << tau)
    source_variable_nodes = {node[1]: i for i, node in enumerate(old_nodes) if node[0] == "variable"}
    for quad, idx in zip(quads[1:], private):
        check(quad["kind"] == "private_quadratic" and quad["parent_private_variable"] == idx,
              "Wrong private quadratic variable")
        row = old_rows[quad["label"]]
        check(quad["parent_numerator"] == row["numerator"] and quad["parent_denominator"] == row["denominator"],
              "Wrong private equation reference")
        check(old_support[row["numerator"]] & private_mask == 1 << idx
              and not old_support[row["denominator"]] & private_mask, "Private witness is not private")
        check(not old_support[quad["source_L"]] & ~allowed_mask
              and not old_support[quad["source_M"]] & ~allowed_mask, "Extracted coefficient contains a private witness")
        frontier, seen, todo = set(), set(), [row["numerator"]]
        while todo:
            index = todo.pop()
            if index in seen:
                continue
            seen.add(index)
            if not old_support[index] >> idx & 1:
                if full_source[index][0] != "int":
                    frontier.add(index)
            else:
                todo.extend(children(full_source[index]))
        ynode = source_variable_nodes[idx]
        atoms = {k: i for i, k in enumerate(sorted(frontier | {ynode}))}
        expand = expander(full_source, atoms=atoms)
        check(expand(row["numerator"]) == plus(times(expand(quad["source_L"]), power(expand(ynode), 2)),
                                               expand(quad["source_M"])), "Quadratic coefficient extraction failed")
    check(not old_support[parent["guard_product_node"]] & ~allowed_mask, "A guard uses an unretained private coordinate")
    check(len(points)+len(quads[1:])+1 == len(old_rows) == 297, "Source residual inventory is incomplete")

    # Independent expression-tree induction for every simultaneous affine
    # substitution. The invariant is image(H)=2^k H(C_i=Z_i/2,tau=(V+a)/2).
    interner = Interner()
    actual_ids = interner.read(nodes)
    two_id = interner.raw("int", 2)
    memo = {}

    def converted(index):
        if index in memo:
            return memo[index]
        op, *a = full_source[index]
        if op == "variable":
            if a[0] in base_map:
                result = interner.raw("variable", base_map[a[0]]), 0
            elif a[0] in point_map:
                result = interner.raw("algebra_generator", point_map[a[0]]), 1
            elif a[0] == tau:
                result = actual_ids[pell["tau_substitution_numerator"]], 1
            else:
                raise ValueError("Uneliminated coordinate in source conversion")
        elif op in ("int", "parameter"):
            result = interner.raw(op, *a), 0
        elif op == "neg":
            n, d = converted(a[0]); result = interner.neg(n), d
        elif op == "pow":
            n, d = converted(a[0]); result = interner.pow(n, a[1]), d*a[1]
        elif op == "mul":
            pairs = [converted(k) for k in a]
            result = interner.mul(*(n for n, _ in pairs)), sum(d for _, d in pairs)
        elif op == "add":
            pairs = [converted(k) for k in a]
            d = max(k for _, k in pairs)
            result = interner.add(*(interner.mul(n, interner.pow(two_id, d-k)) for n, k in pairs)), d
        memo[index] = result
        return result

    for quad in quads[1:]:
        ln, ld = converted(quad["source_L"])
        mn, md = converted(quad["source_M"])
        d = max(ld, md)
        check(actual_ids[quad["L"]] == interner.mul(ln, interner.pow(two_id, d-ld))
              and actual_ids[quad["M"]] == interner.mul(mn, interner.pow(two_id, d-md)), "Cleared affine substitution differs")
        check((quad["coefficient_L_substitution_exponent"], quad["coefficient_M_substitution_exponent"],
               quad["common_substitution_exponent"]) == (ld, md, d), "Wrong numeric denominator exponent")
    gn, gd = converted(parent["guard_product_node"])
    check(actual_ids[spec["original_guard_node"]] == gn and spec["source_guard_substitution_exponent"] == gd,
          "Source guard substitution differs")
    for quad in quads:
        zi = interner.raw("algebra_generator", quad["generator"])
        check(actual_ids[quad["monic_constant_nonzero_case"]] == interner.mul(actual_ids[quad["L"]], actual_ids[quad["M"]])
              and actual_ids[quad["guard_nonzero_case"]] == interner.mul(actual_ids[quad["L"]], zi),
              "Private-root rescaling or nonzero guard differs")
        check(generator_support[quad["L"]] < (1 << quad["generator"])
              and generator_support[quad["M"]] < (1 << quad["generator"]), "A monic relation is not triangular")
    check(generator_support[spec["original_guard_node"]] < (1 << 212), "Unexpected source guard dependence")

    # Verify proposed filtration weights and matrix-norm majorants as
    # inequalities, not as outputs of the producer's recursive routine.
    bb = spec["bounds"]
    weights, logs = bb["generator_weights"], bb["generator_operator_log2_norm_bounds"]
    check(len(weights) == len(logs) == 297 and all(type(k) is int and k >= 1 for k in weights)
          and all(type(k) is int and k >= 0 for k in logs), "Invalid generator majorants")
    majorants = []
    for op, *a in nodes:
        if op == "int": out = (0, (abs(a[0])-1).bit_length() if a[0] else 0)
        elif op == "variable": out = (1, 0)
        elif op == "parameter": out = (0, (a[1]-1).bit_length() if a[1] else 0)
        elif op == "algebra_generator": out = (weights[a[0]], logs[a[0]])
        elif op == "neg": out = majorants[a[0]]
        elif op == "pow": out = tuple(k*a[1] for k in majorants[a[0]])
        elif op == "add": out = (max(majorants[k][0] for k in a), max(majorants[k][1] for k in a)+(len(a)-1).bit_length())
        elif op == "mul": out = tuple(sum(majorants[k][i] for k in a) for i in (0, 1))
        majorants.append(out)
    for point in points:
        i = point["generator"]
        w0, b0 = majorants[point["constant_coefficient"]]
        w2, b2 = majorants[point["quadratic_coefficient"]]
        check(w0 <= 4*weights[i] and w2+2*weights[i] <= 4*weights[i]
              and logs[i] >= max(b0, b2)+1, "Point companion bounds fail")
    for quad in quads:
        i = quad["generator"]
        w, b = majorants[quad["monic_constant_nonzero_case"]]
        check(w <= 2*weights[i] and b <= logs[i], "Quadratic companion bounds fail")
    basis_weight = 3*sum(weights[:211])+sum(weights[211:])
    guards = [spec["original_guard_node"]]+[p["derivative_guard"] for p in points]+[q["guard_nonzero_case"] for q in quads]
    wg, bg = (sum(majorants[k][i] for k in guards) for i in (0, 1))
    we = max(majorants[q["M"]][0] for q in quads)
    be = max(majorants[q["M"]][1] for q in quads)
    check((basis_weight, wg, bg, we, be) == (bb["maximum_basis_weight"], bb["guard_weight"],
          bb["guard_operator_log2_norm_bound"], bb["closed_residual_maximum_weight"],
          bb["closed_residual_maximum_operator_log2_norm_bound"]), "Aggregate algebra bounds differ")
    n, m, r = 2**508, 297, 86
    selector = m*n*(n+1)//2
    blambda = (m).bit_length()+max((i+1)*(selector-1).bit_length()+b for i, b in enumerate(logs))
    alpha, beta = wg+max(weights)+basis_weight, bg+blambda
    AH, BH = n*alpha, n*(beta+1)
    AR, BR = (n-1)*alpha+we+basis_weight, 508+be+(n-1)*(beta+1)
    AL, BL = (2*n+2)*AH, (2*n+2)*BH+(2*n-1)*508
    psi_degree, psi_bits = n*(AL+1), n*BL+509
    reverse_degree, reverse_bits = AR+(n-1)*(AL+1), BR+(n-1)*BL
    branch_degree = 2*max(AH, psi_degree, reverse_degree)
    branch_bits = 2*max(BH, psi_bits, reverse_bits)+(n+r).bit_length()
    # Count the actual finite factors by an independent binomial sum.
    factors = 54272*sum(comb(86, k)*(2**(422+k))*(1+m*(2**(422+k))*(2**(422+k)+1)//2)
                        for k in range(87))
    expected_bounds = {
        "maximum_rank": n, "maximum_selector": selector,
        "selector_operator_log2_norm_bound": blambda,
        "multiplication_operator_entry_degree_bound": alpha, "multiplication_operator_log2_norm_bound": beta,
        "characteristic_coefficient_degree_bound": AH, "characteristic_polynomial_log2_norm_bound": BH,
        "trace_coefficient_degree_bound": AR, "trace_polynomial_log2_norm_bound": BR,
        "reciprocal_scale_degree_bound": AL, "reciprocal_scale_log2_norm_bound": BL,
        "branch_degree_bound": branch_degree, "branch_coefficient_log2_norm_bound": branch_bits,
        "exact_number_of_final_factors": factors, "degree_bound": factors*branch_degree,
        "coefficient_height_log2_bound": factors*branch_bits,
    }
    for key, value in expected_bounds.items():
        check(bb[key] == value, "Incorrect determinant or product bound: "+key)
    check(bb["degree_power_of_two_bound_exponent"] == (factors*branch_degree-1).bit_length()
          and bb["coefficient_height_double_power_of_two_bound_exponent"] == (factors*branch_bits-1).bit_length(),
          "Rounded bounds are understated")

    # The macro grammar is fixed: it has no free matrix entries, selectors,
    # coefficient slots, or algebra generators beyond the stated finite rules.
    algebra = spec["finite_algebra_recipe"]
    check(algebra["generator_count"] == 297
          and algebra["point_equations"] == "z_i^4 + quadratic_coefficient_i*z_i^2 + constant_coefficient_i"
          and algebra["quadratic_zero_case"] == "z_i=0; add closed equation M_i=0"
          and algebra["quadratic_nonzero_case"] == "z_i^2+L_i*M_i=0; add guard L_i*z_i!=0"
          and algebra["guard"] == "original_guard * product(point_derivative_guards) * product(nonzero_case_L_i*z_i)"
          and algebra["closed_equations"] == "(1-bit_i)*M_i, for i=0,...,85", "Unknown algebra recipe")
    recipe = spec["polynomial_recipe"]
    check(recipe["outer_product_order"] == ["j", "correction", "quadratic_mask", "selector", "degree_case"]
          and recipe["lambda"] == "1+sum_{i=1}^{297} selector^i*z_i"
          and recipe["H"] == "det(I-V*M_{G*lambda}) = sum_{k=0}^{rank} a_k V^k"
          and recipe["trace_residual"] == "R_i(V)=Tr(M_{(1-bit_i)*M_i} adj(I-V*M_{G*lambda}))"
          and recipe["truncation"] == "H_d(V)=sum_{k=0}^d a_k V^k"
          and recipe["guard_scale"] == "g=a_d*Res_V(H_d,H_d'); L=a_d^2*g"
          and recipe["reciprocal"] == "Psi=1+sum_{j=1}^d a_{d-j}*a_d^(2*j-1)*g^j*U^j"
          and recipe["trace_reversal"] == "Rtilde_i=sum_{k=0}^{rank-1} coefficient_V^k(R_i)*(L*U)^(rank-1-k)"
          and recipe["factor"] == "Psi^2+sum_{k=d+1}^{rank} a_k^2+sum_{i=0}^{85} Rtilde_i^2", "Unknown polynomial recipe")
    used_base = 0
    for i in [spec["original_guard_node"]]+[p[k] for p in points for k in ("constant_coefficient", "quadratic_coefficient")]+[q[k] for q in quads for k in ("L", "M")]:
        used_base |= base_support[i]
    check(used_base == (1 << 557)-1, "A declared base coordinate is absent from the source specification")
    return {
        "status": "passed",
        "external_variables": 558,
        "existential_witnesses": 557,
        "formal_algebra_generators_eliminated_by_determinants": 297,
        "source_point_quartics_checked_exactly": 211,
        "private_quadratic_extractions_checked_exactly": 85,
        "completed_pell_identity_and_zero_case_checked": True,
        "source_substitution_identity": "image(H)=2^k H(C_i=Z_i/2,tau=(V+a)/2)",
        "quadratic_zero_nonzero_bits": 86,
        "coefficient_dag_nodes": len(nodes),
        "all_557_base_coordinates_occur": True,
        "monicity_triangularity_and_simplicity_guard_structure_checked": True,
        "matrix_norm_and_degree_majorants_checked": True,
        "finite_product_factor_count_checked_by_binomial_sum": True,
        "degree_bound_power_of_two_exponent": bb["degree_power_of_two_bound_exponent"],
        "coefficient_height_bound_double_power_of_two_exponent": bb["coefficient_height_double_power_of_two_bound_exponent"],
        "scope": "Exact source conversion, finite index grammar, and degree/coefficient bound audit. The indexed determinant construction is justified by the accompanying theorem; enormous matrices and the final product were not expanded. Arithmetic correctness still inherits the source theorem.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--specification", type=Path, default=Path(__file__).with_name("polynomial-558")/"polynomial-specification.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("polynomial-558")/"verification.json")
    args = parser.parse_args()
    parent_raw = (ROOT/"optimization/polynomial-855/polynomial-circuit.json").read_bytes()
    check(hashlib.sha256(parent_raw).hexdigest() == PARENT_SHA, "Parent source circuit changed")
    raw = args.specification.read_bytes()
    report = audit(json.loads(parent_raw), json.loads(raw)) | {
        "specification_sha256": hashlib.sha256(raw).hexdigest(),
        "parent_circuit_sha256": PARENT_SHA,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
