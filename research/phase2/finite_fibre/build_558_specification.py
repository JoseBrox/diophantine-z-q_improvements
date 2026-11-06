#!/usr/bin/env python3
"""Emit an exact indexed determinant/coefficient/product polynomial in 558 variables.

This materializes its coefficient DAG and all finite index bounds, not the
enormous multiplication matrices or the final expanded monomial list.
Formal finite-algebra generators are eliminated by the stated determinant
recipe; they are not additional quantified variables.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT / "optimization/polynomial-855/polynomial-circuit.json"
PARENT_SHA = "6a1174891dccdd55bfc4cb6e7486cca2a4fde99ee8a755adaac0174f370da55b"


def children(node):
    op, *a = node
    if op in ("int", "variable", "parameter", "algebra_generator"):
        return []
    if op in ("neg", "pow"):
        return a[:1]
    if op in ("add", "mul"):
        return a
    raise ValueError(op)


class DAG:
    def __init__(self, nodes=()):
        self.nodes = [list(node) for node in nodes]
        self.cache = {tuple(node): i for i, node in enumerate(self.nodes)}
        self.zero, self.one = self.node("int", 0), self.node("int", 1)

    def node(self, op, *a):
        key = (op, *a)
        if key not in self.cache:
            self.cache[key] = len(self.nodes)
            self.nodes.append(list(key))
        return self.cache[key]

    def add(self, *terms):
        terms = [t for t in terms if t != self.zero]
        return self.zero if not terms else terms[0] if len(terms) == 1 else self.node("add", *terms)

    def mul(self, *terms):
        if self.zero in terms:
            return self.zero
        terms = [t for t in terms if t != self.one]
        return self.one if not terms else terms[0] if len(terms) == 1 else self.node("mul", *terms)

    def pow(self, a, exponent):
        return self.one if exponent == 0 else a if exponent == 1 else self.node("pow", a, exponent)

    def neg(self, a):
        return self.zero if a == self.zero else self.node("neg", a)

    def integer(self, n):
        return self.node("int", n)


def supports(nodes):
    masks = []
    for node in nodes:
        mask = 1 << node[1] if node[0] == "variable" else 0
        for child in children(node):
            mask |= masks[child]
        masks.append(mask)
    return masks


def extract_quadratic(dag, root, variable, source_support):
    cache = {}

    def plus(a, b):
        result = dict(a)
        for degree, coefficient in b.items():
            result[degree] = dag.add(result.get(degree, dag.zero), coefficient)
        return result

    def times(a, b):
        result = {}
        for i, aa in a.items():
            for j, bb in b.items():
                result = plus(result, {i+j: dag.mul(aa, bb)})
        return result

    def expand(index):
        if index in cache:
            return cache[index]
        if not (source_support[index] >> variable & 1):
            result = {0: index}
        else:
            op, *a = dag.nodes[index]
            if op == "variable":
                assert a == [variable]
                result = {1: dag.one}
            elif op == "add":
                result = {}
                for child in a:
                    result = plus(result, expand(child))
            elif op == "mul":
                result = {0: dag.one}
                for child in a:
                    result = times(result, expand(child))
            elif op == "neg":
                result = {k: dag.neg(v) for k, v in expand(a[0]).items()}
            elif op == "pow":
                result = {0: dag.one}
                for _ in range(a[1]):
                    result = times(result, expand(a[0]))
            else:
                raise ValueError(op)
        cache[index] = result
        return result

    coefficients = expand(root)
    assert set(coefficients) == {0, 2}
    return coefficients[2], coefficients[0]


def prune(nodes, roots):
    reached, todo = set(), list(roots)
    while todo:
        index = todo.pop()
        if index in reached:
            continue
        reached.add(index); todo.extend(children(nodes[index]))
    mapping = {old: new for new, old in enumerate(sorted(reached))}
    result = []
    for index in sorted(reached):
        op, *a = nodes[index]
        if op in ("int", "variable", "parameter", "algebra_generator"):
            result.append(nodes[index])
        elif op == "pow":
            result.append([op, mapping[a[0]], a[1]])
        else:
            result.append([op, *(mapping[k] for k in a)])
    return result, mapping


def uniform_bounds(nodes, points, quadratics, original_guard):
    """Weights and submultiplicative matrix-column norms; see bounds proof."""
    generator_weights, generator_bits, memo = [], [], {}

    def bounds(index):
        if index in memo:
            return memo[index]
        op, *a = nodes[index]
        if op == "int":
            out = (0, (abs(a[0])-1).bit_length() if a[0] else 0)
        elif op == "variable":
            out = (1, 0)
        elif op == "parameter":
            out = (0, (a[1]-1).bit_length())
        elif op == "algebra_generator":
            assert a[0] < len(generator_weights), "Nontriangular coefficient"
            out = (generator_weights[a[0]], generator_bits[a[0]])
        elif op == "neg":
            out = bounds(a[0])
        elif op == "add":
            bb = [bounds(k) for k in a]
            out = (max(v[0] for v in bb), max(v[1] for v in bb)+(len(a)-1).bit_length())
        elif op == "mul":
            bb = [bounds(k) for k in a]
            out = tuple(sum(v[j] for v in bb) for j in (0, 1))
        elif op == "pow":
            out = tuple(v*a[1] for v in bounds(a[0]))
        else:
            raise ValueError(op)
        memo[index] = out
        return out

    for point in points:
        w0, b0 = bounds(point["constant_coefficient"])
        w2, b2 = bounds(point["quadratic_coefficient"])
        generator_weights.append(max(1, (w0+3)//4, (w2+1)//2))
        generator_bits.append(max(0, max(b0, b2)+1))
    for quad in quadratics:
        w, b = bounds(quad["monic_constant_nonzero_case"])
        generator_weights.append(max(1, (w+1)//2))
        generator_bits.append(max(0, b))
    assert len(generator_weights) == 297
    basis_weight = 3*sum(generator_weights[:211])+sum(generator_weights[211:])
    guard_weight, guard_bits = bounds(original_guard)
    for point in points:
        w, b = bounds(point["derivative_guard"])
        guard_weight += w; guard_bits += b
    for quad in quadratics:
        w, b = bounds(quad["guard_nonzero_case"])
        guard_weight += w; guard_bits += b
    residual_weight = max(bounds(q["M"])[0] for q in quadratics)
    residual_bits = max(bounds(q["M"])[1] for q in quadratics)
    n = 2**508
    m = 297
    selector_max = m*n*(n+1)//2
    selector_coefficient_bits = (selector_max-1).bit_length()
    lambda_bits = m.bit_length()+max((i+1)*selector_coefficient_bits+b
                                     for i, b in enumerate(generator_bits))
    operator_entry_degree = guard_weight+max(generator_weights)+basis_weight
    operator_bits = guard_bits+lambda_bits
    residual_entry_degree = residual_weight+basis_weight
    H_degree = n*operator_entry_degree
    H_bits = n*(operator_bits+1)
    trace_degree = (n-1)*operator_entry_degree+residual_entry_degree
    trace_bits = 508+residual_bits+(n-1)*(operator_bits+1)
    g_degree = 2*n*H_degree
    g_bits = H_bits+(2*n-1)*(H_bits+508)
    L_degree = 2*H_degree+g_degree
    L_bits = 2*H_bits+g_bits
    psi_degree = n*(L_degree+1)
    psi_bits = n*L_bits+(n.bit_length())
    reversed_trace_degree = trace_degree+(n-1)*(L_degree+1)
    reversed_trace_bits = trace_bits+(n-1)*L_bits
    branch_degree = 2*max(H_degree, psi_degree, reversed_trace_degree)
    branch_bits = 2*max(H_bits, psi_bits, reversed_trace_bits)+(n+86).bit_length()
    n0 = 2**422
    branches = 54272*(n0*3**86+m*(n0**3*9**86+n0**2*5**86)//2)
    degree, height_bits = branch_degree*branches, branch_bits*branches
    return {
        "generator_weights": generator_weights,
        "generator_operator_log2_norm_bounds": generator_bits,
        "maximum_rank": n,
        "maximum_selector": selector_max,
        "maximum_basis_weight": basis_weight,
        "guard_weight": guard_weight,
        "guard_operator_log2_norm_bound": guard_bits,
        "closed_residual_maximum_weight": residual_weight,
        "closed_residual_maximum_operator_log2_norm_bound": residual_bits,
        "selector_operator_log2_norm_bound": lambda_bits,
        "multiplication_operator_entry_degree_bound": operator_entry_degree,
        "multiplication_operator_log2_norm_bound": operator_bits,
        "characteristic_coefficient_degree_bound": H_degree,
        "characteristic_polynomial_log2_norm_bound": H_bits,
        "trace_coefficient_degree_bound": trace_degree,
        "trace_polynomial_log2_norm_bound": trace_bits,
        "reciprocal_scale_degree_bound": L_degree,
        "reciprocal_scale_log2_norm_bound": L_bits,
        "branch_degree_bound": branch_degree,
        "branch_coefficient_log2_norm_bound": branch_bits,
        "exact_number_of_final_factors": branches,
        "degree_bound": degree,
        "coefficient_height_log2_bound": height_bits,
        "degree_power_of_two_bound_exponent": (degree-1).bit_length(),
        "coefficient_height_double_power_of_two_bound_exponent": (height_bits-1).bit_length(),
        "bound_interpretation": "degree <= degree_bound; coefficient height <= 2^coefficient_height_log2_bound. These are upper bounds, not expanded-polynomial statistics.",
    }


def build(parent):
    source = DAG(parent["nodes"])
    parent_count = len(parent["nodes"])
    source_support = supports(parent["nodes"])
    variables = parent["variables"]
    by_name = {v["name"]: v["index"] for v in variables}
    point_variables = [v for v in variables if v["category"] == "point" and v["name"].endswith(".C")]
    assert len(point_variables) == 211
    point_map = {v["index"]: i for i, v in enumerate(point_variables)}
    tau_index = by_name["proxy.t"]
    private = [by_name["anchor.u"]]+[v["index"] for v in variables
               if v["category"] == "pole" and v["name"].endswith((".p", ".q"))]
    assert len(private) == 85
    excluded = set(point_map) | set(private) | {tau_index, 854}
    retained = [v["index"] for v in variables if v["index"] not in excluded]
    assert len(retained) == 557
    base_map = {old: new for new, old in enumerate(retained)}
    external = [dict(variables[old], index=new, parent_index=old)
                for new, old in enumerate(retained)]
    allowed_mask = sum(1 << i for i in retained) | sum(1 << i for i in point_map) | (1 << tau_index)
    old_rows = {r["label"]: r for r in parent["rational_equations_before_clearing"]}
    private_rows = []
    for idx in private:
        name = variables[idx]["name"]
        label = "packed semilocal anchor" if name == "anchor.u" else name[:-2]+(
            ".first conic" if name.endswith(".p") else ".second conic")
        row = old_rows[label]
        assert source_support[row["numerator"]] & ~allowed_mask == 1 << idx
        L, M = extract_quadratic(source, row["numerator"], idx, source_support)
        private_rows.append({"label": label, "parent_private_variable": idx,
                             "parent_numerator": row["numerator"], "parent_denominator": row["denominator"],
                             "source_L": L, "source_M": M})
    assert source_support[parent["guard_product_node"]] & ~allowed_mask == 0

    out = DAG()
    two = out.integer(2)
    j = out.node("parameter", "j", 211)
    algebra_nodes = [out.node("algebra_generator", i) for i in range(297)]
    base_nodes = [out.node("variable", i) for i in range(557)]
    s, z = base_nodes[base_map[by_name["proxy.s"]]], base_nodes[base_map[by_name["proxy.z"]]]
    sm2 = out.add(s, out.integer(-2))
    pell_a = out.mul(s, sm2, z)
    pell_b = out.add(out.mul(out.pow(sm2, 2), out.pow(z, 2)), out.integer(-1))
    pell_delta = out.add(out.pow(pell_a, 2), out.mul(out.integer(-4), pell_b))
    tau_numerator = out.add(algebra_nodes[211], pell_a)
    converted = {}

    def convert(index):
        if index in converted:
            return converted[index]
        op, *a = source.nodes[index]
        if op == "variable":
            if a[0] in base_map:
                result = base_nodes[base_map[a[0]]], 0
            elif a[0] in point_map:
                result = algebra_nodes[point_map[a[0]]], 1
            elif a[0] == tau_index:
                result = tau_numerator, 1
            else:
                raise ValueError("Uneliminated private variable "+str(a[0]))
        elif op in ("int", "parameter"):
            result = out.node(op, *a), 0
        elif op == "neg":
            n, degree = convert(a[0]); result = out.neg(n), degree
        elif op == "pow":
            n, degree = convert(a[0]); result = out.pow(n, a[1]), degree*a[1]
        elif op == "mul":
            terms = [convert(k) for k in a]
            result = out.mul(*(n for n, _ in terms)), sum(d for _, d in terms)
        elif op == "add":
            terms = [convert(k) for k in a]
            degree = max(d for _, d in terms)
            result = out.add(*(out.mul(n, out.pow(two, degree-d)) for n, d in terms)), degree
        else:
            raise ValueError(op)
        converted[index] = result
        return result

    points = []
    for i, variable in enumerate(point_variables):
        prefix = variable["name"][:-2]
        a0, a1 = [base_nodes[base_map[by_name[prefix+suffix]]] for suffix in (".a0", ".a1")]
        A = out.add(out.pow(a0, 3), out.mul(out.integer(6), a0, out.pow(a1, 2)),
                    out.mul(out.integer(-11), a0), out.mul(out.integer(12), a1))
        B = out.add(out.mul(out.integer(3), out.pow(a0, 2), a1), out.mul(two, out.pow(a1, 3)),
                    out.mul(out.integer(-11), a1), out.mul(out.integer(6), a0))
        j2p2 = out.add(out.pow(j, 2), two)
        K = out.add(out.mul(j2p2, A), out.mul(out.integer(4), j, B))
        J = out.add(out.mul(two, j, A), out.mul(j2p2, B))
        c0, c2 = out.mul(two, out.pow(J, 2)), out.mul(out.integer(-2), K)
        derivative = out.add(out.mul(out.integer(4), out.pow(algebra_nodes[i], 3)),
                             out.mul(two, c2, algebra_nodes[i]))
        row = old_rows[prefix+".quartic half-point"]
        points.append({"generator": i, "name": prefix+".scaled_chart_root", "degree": 4,
                       "constant_coefficient": c0, "quadratic_coefficient": c2,
                       "derivative_guard": derivative, "A": A, "B": B, "K": K, "J": J,
                       "parent_C_variable": variable["index"], "parent_row_numerator": row["numerator"],
                       "parent_row_denominator": row["denominator"]})
    quadratics = [{"generator": 211, "name": "Pell.completed_root", "bit": 0,
                   "L": out.one, "M": out.neg(pell_delta), "kind": "completed_pell"}]
    for bit, row in enumerate(private_rows, 1):
        ln, ld = convert(row["source_L"])
        mn, md = convert(row["source_M"])
        degree = max(ld, md)
        L, M = out.mul(ln, out.pow(two, degree-ld)), out.mul(mn, out.pow(two, degree-md))
        quadratics.append({"generator": 211+bit, "name": variables[row["parent_private_variable"]]["name"]+".scaled_root",
                           "bit": bit, "L": L, "M": M, "kind": "private_quadratic", **row,
                           "coefficient_L_substitution_exponent": ld,
                           "coefficient_M_substitution_exponent": md,
                           "common_substitution_exponent": degree})
    for quad in quadratics:
        quad["monic_constant_nonzero_case"] = out.mul(quad["L"], quad["M"])
        quad["guard_nonzero_case"] = out.mul(quad["L"], algebra_nodes[quad["generator"]])
    original_guard, guard_degree = convert(parent["guard_product_node"])
    point_node_keys = ("constant_coefficient", "quadratic_coefficient", "derivative_guard", "A", "B", "K", "J")
    quad_node_keys = ("L", "M", "monic_constant_nonzero_case", "guard_nonzero_case")
    roots = [original_guard, pell_a, pell_b, pell_delta, tau_numerator]
    roots += [point[key] for point in points for key in point_node_keys]
    roots += [quad[key] for quad in quadratics for key in quad_node_keys]
    nodes, remap = prune(out.nodes, roots)
    points = [point | {key: remap[point[key]] for key in point_node_keys} for point in points]
    quadratics = [quad | {key: remap[quad[key]] for key in quad_node_keys} for quad in quadratics]
    original_guard = remap[original_guard]
    bounds = uniform_bounds(nodes, points, quadratics, original_guard)
    return {
        "format": "integer-polynomial-indexed-finite-algebra-v1",
        "source_commit": parent["source_commit"],
        "parent_855_circuit_sha256": PARENT_SHA,
        "external_variables": external+[{"index": 557, "name": "U", "category": "single finite-algebra witness"}],
        "retained_base_variables": 557,
        "total_external_variables": 558,
        "existential_witnesses": 557,
        "coefficient_dag": nodes,
        "point_relations": points,
        "quadratic_relations": quadratics,
        "original_guard_node": original_guard,
        "source_guard_substitution_exponent": guard_degree,
        "pell_certificate": {"a": remap[pell_a], "b0": remap[pell_b], "discriminant": remap[pell_delta],
                             "tau_substitution_numerator": remap[tau_numerator], "tau_substitution_denominator": 2,
                             "parent_tau_variable": tau_index,
                             "parent_row": old_rows["Lucas relation"]},
        "coefficient_extraction_extension": source.nodes[parent_count:],
        "finite_parameters": {
            "j": parent["finite_parameters"]["j"],
            "correction": parent["finite_parameters"]["correction"],
            "quadratic_mask": {"from": 0, "to": 2**86-1, "bits": 86},
            "rank": {"formula": "4^211 * 2^popcount(quadratic_mask)"},
            "selector": {"from": 0, "to_formula": "297*rank*(rank+1)/2"},
            "degree_case": {"from": 1, "to_formula": "rank"},
        },
        "finite_algebra_recipe": {
            "basis_order": "lexicographic exponent tuples in generator order, 0 <= exponent_i < degree_i",
            "generator_count": 297,
            "point_equations": "z_i^4 + quadratic_coefficient_i*z_i^2 + constant_coefficient_i",
            "quadratic_zero_case": "z_i=0; add closed equation M_i=0",
            "quadratic_nonzero_case": "z_i^2+L_i*M_i=0; add guard L_i*z_i!=0",
            "guard": "original_guard * product(point_derivative_guards) * product(nonzero_case_L_i*z_i)",
            "closed_equations": "(1-bit_i)*M_i, for i=0,...,85",
            "matrix_entries": "normal-form coefficients of multiplication in the monic triangular algebra",
        },
        "polynomial_recipe": {
            "definition": "finite_algebra_polynomial.tex, Theorem thm:explicit-guarded-finite-algebra",
            "outer_product_order": ["j", "correction", "quadratic_mask", "selector", "degree_case"],
            "lambda": "1+sum_{i=1}^{297} selector^i*z_i",
            "H": "det(I-V*M_{G*lambda}) = sum_{k=0}^{rank} a_k V^k",
            "trace_residual": "R_i(V)=Tr(M_{(1-bit_i)*M_i} adj(I-V*M_{G*lambda}))",
            "truncation": "H_d(V)=sum_{k=0}^d a_k V^k",
            "guard_scale": "g=a_d*Res_V(H_d,H_d'); L=a_d^2*g",
            "reciprocal": "Psi=1+sum_{j=1}^d a_{d-j}*a_d^(2*j-1)*g^j*U^j",
            "trace_reversal": "Rtilde_i=sum_{k=0}^{rank-1} coefficient_V^k(R_i)*(L*U)^(rank-1-k)",
            "factor": "Psi^2+sum_{k=d+1}^{rank} a_k^2+sum_{i=0}^{85} Rtilde_i^2",
            "result": "product of factor over the stated five finite index ranges",
            "bound_formal_symbols": ["z_1,...,z_297", "V"],
            "only_external_symbols": "external_variables[0],...,external_variables[557]",
        },
        "bounds": bounds,
        "representation_scope": "Complete indexed determinant/coefficient/product polynomial specification, with a materialized integer coefficient DAG. Rank-sized matrices, the final finite product, and the monomial expansion are not materialized.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("polynomial-558"))
    args = parser.parse_args()
    raw = PARENT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_SHA
    spec = build(json.loads(raw))
    encoded = (json.dumps(spec, separators=(",", ":"))+"\n").encode()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/"polynomial-specification.json").write_bytes(encoded)
    report = {
        "total_variables": 558, "existential_witnesses": 557, "formal_algebra_generators_not_external_variables": 297,
        "coefficient_dag_nodes": len(spec["coefficient_dag"]), "maximum_algebra_rank": 2**508,
        "maximum_algebra_rank_power_of_two_exponent": 508,
        "degree_bound_power_of_two_exponent": spec["bounds"]["degree_power_of_two_bound_exponent"],
        "coefficient_height_bound_double_power_of_two_exponent": spec["bounds"]["coefficient_height_double_power_of_two_bound_exponent"],
        "specification_sha256": hashlib.sha256(encoded).hexdigest(), "specification_bytes": len(encoded),
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parent_circuit_sha256": PARENT_SHA,
        "representation": spec["representation_scope"],
        "verification_status": "Producer assertions passed; independent checker must be run separately.",
    }
    (args.output/"construction-report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
