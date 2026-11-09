#!/usr/bin/env python3
"""Compile a small shared-point source into an explicit indexed polynomial.

Supports finite-anchor and semilocal sources with triangular monic roots.
Finite algebra generators are eliminated by the proved
determinant/trace recipe. Indexed elliptic anchor products have canonical
integer factors and explicit height bounds, rather than unspecified clearing.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from math import comb, prod
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from finite_algebra_core import DAG, children, prune


def clog(n):
    return (n-1).bit_length() if n > 0 else 0


def algebra_bounds(nodes, relations, guard_node, closed, indexed, parameter_count):
    weights, logs, cache = [], [], {}

    def bound(index):
        if index in cache: return cache[index]
        op, *a = nodes[index]
        if op == "int": out = (0, clog(abs(a[0])))
        elif op == "variable": out = (1, 0)
        elif op == "parameter": out = (0, clog(a[1]))
        elif op == "algebra_generator":
            assert a[0] < len(weights)
            out = weights[a[0]], logs[a[0]]
        elif op == "neg": out = bound(a[0])
        elif op == "pow": out = tuple(k*a[1] for k in bound(a[0]))
        elif op == "mul": out = tuple(sum(bound(k)[j] for k in a) for j in (0, 1))
        elif op == "add": out = max(bound(k)[0] for k in a), max(bound(k)[1] for k in a)+clog(len(a))
        cache[index] = out
        return out

    point_count = sum(r["kind"] == "point" for r in relations)
    quadratic_count = len(relations)-point_count
    for r in relations:
        degree = r["maximum_degree"]
        nonzero = [(k, node) for k, node in enumerate(r["coefficient_nodes_ascending"])
                   if nodes[node] != ["int", 0]]
        weights.append(max([1]+[(bound(node)[0]+degree-k-1)//(degree-k) for k, node in nonzero]))
        logs.append(max([0]+[(bound(node)[1]+degree-k-1)//(degree-k) for k, node in nonzero])+clog(max(1, len(nonzero))))
    m = len(relations)
    rank_exp = 2*point_count+quadratic_count
    n = 2**rank_exp
    W = sum((r["maximum_degree"]-1)*weights[r["generator"]] for r in relations)
    wg, bg = bound(guard_node)
    # Every pole root is already a source guard. Completeness constructs
    # non-torsion elliptic points, so the zero cases may be discarded.
    residual_nodes = [e["numerator"] for e in closed]
    we = max([0]+[bound(k)[0] for k in residual_nodes])
    be = max([0]+[bound(k)[1] for k in residual_nodes])
    rcount = len(residual_nodes)
    selector = m*n*(n+1)//2
    blambda = clog(m+1)+max((i+1)*clog(selector)+b for i, b in enumerate(logs))
    factor_count = parameter_count*n*(1+selector)
    macro_bounds = []
    for macro in indexed:
        wb = max(bound(macro[k])[0] for k in ("N0", "N1", "D"))
        bb = max(bound(macro[k])[1] for k in ("N0", "N1", "D"))
        E = macro["index_last"]["exponent"]
        assert E >= 6 and 30*64+(2*bb+14) <= 64**2
        macro_bounds.append({
            "name": macro["name"], "coordinate_weight_bound": wb,
            "coordinate_operator_log2_norm_bound": bb,
            "weight_bound_power_of_two_exponent": 1+E+clog(max(1, wb)),
            "operator_log2_norm_bound_power_of_two_exponent": 3*E+5,
            "fixed_multiple_height_bound": "h0(x(nP)) <= 30*n^2",
            "guard_operator_log2_norm_bound": "20*M^3+30*M^2+(2*b+14)*M <= 21*M^3",
        })
    common = {
        "generator_weights": weights, "generator_operator_log2_norm_bounds": logs,
        "maximum_rank_power_of_two_exponent": rank_exp, "maximum_rank": n,
        "maximum_basis_weight": W, "materialized_guard_weight": wg,
        "materialized_guard_operator_log2_norm_bound": bg,
        "closed_residual_maximum_weight": we, "closed_residual_maximum_operator_log2_norm_bound": be,
        "closed_residual_count": rcount, "maximum_selector": selector,
        "selector_operator_log2_norm_bound": blambda,
        "source_parameter_branches": parameter_count,
        "exact_number_of_final_factors": factor_count,
        "indexed_guard_bounds": macro_bounds,
        "coefficient_norm_method": "weighted_companion_column_norm",
    }
    if not indexed:
        alpha, beta = wg+max(weights)+W, bg+blambda
        AH, BH = n*alpha, n*(beta+1)
        AR, BR = (n-1)*alpha+we+W, rank_exp+be+(n-1)*(beta+1)
        AL, BL = (2*n+2)*AH, (2*n+2)*BH+(2*n-1)*rank_exp
        dbranch = 2*max(AH, n*(AL+1), AR+(n-1)*(AL+1))
        bbranch = 2*max(BH, n*BL+clog(n+1), BR+(n-1)*BL)+clog(n+rcount+1)
        degree, bits = factor_count*dbranch, factor_count*bbranch
        common.update({"bound_mode": "exact_integer_majorants", "operator_entry_degree": alpha,
                       "operator_log2_norm_bound": beta, "H_coefficient_degree": AH, "H_log2_norm_bound": BH,
                       "trace_coefficient_degree": AR, "trace_log2_norm_bound": BR,
                       "scale_degree": AL, "scale_log2_norm_bound": BL,
                       "branch_degree_bound": dbranch, "branch_log2_norm_bound": bbranch,
                       "degree_bound": degree, "coefficient_height_log2_bound": bits,
                       "degree_bound_power_of_two_exponent": clog(degree),
                       "coefficient_height_bound_double_power_of_two_exponent": clog(bits)})
    else:
        # Store powers of two directly; never materialize a number with tens
        # of millions of digits merely to print an upper bound.
        ewg = max([clog(wg)]+[b["weight_bound_power_of_two_exponent"] for b in macro_bounds])+clog(1+len(indexed))
        ebg = max([clog(bg)]+[b["operator_log2_norm_bound_power_of_two_exponent"] for b in macro_bounds])+clog(1+len(indexed))
        ea = max(ewg, clog(max(weights)+W))+1
        eb = max(ebg, clog(blambda))+1
        eAH, eBH = rank_exp+ea, rank_exp+eb+1
        eAR = max(rank_exp+ea, clog(we+W))+1
        eBR = max(clog(rank_exp+be), rank_exp+eb+1)+1
        eAL = rank_exp+2+eAH
        eBL = max(rank_exp+2+eBH, rank_exp+1+clog(rank_exp))+1
        epsid = rank_exp+eAL+1
        epsib = max(rank_exp+eBL, clog(rank_exp+1))+1
        erd = max(eAR, rank_exp+eAL+1)+1
        erb = max(eBR, rank_exp+eBL)+1
        edbranch = 1+max(eAH, epsid, erd)
        ebbranch = max(1+max(eBH, epsib, erb), clog(clog(n+rcount+1)))+1
        common.update({"bound_mode": "explicit_power_of_two_envelopes",
                       "power_envelopes": {"guard_weight": ewg, "guard_log2_norm": ebg,
                           "operator_entry_degree": ea, "operator_log2_norm": eb,
                           "H_coefficient_degree": eAH, "H_log2_norm": eBH,
                           "trace_coefficient_degree": eAR, "trace_log2_norm": eBR,
                           "scale_degree": eAL, "scale_log2_norm": eBL,
                           "reciprocal_degree": epsid, "reciprocal_log2_norm": epsib,
                           "reversed_trace_degree": erd, "reversed_trace_log2_norm": erb,
                           "branch_degree": edbranch, "branch_log2_norm": ebbranch},
                       "degree_bound_power_of_two_exponent": edbranch+clog(factor_count),
                       "coefficient_height_bound_double_power_of_two_exponent": ebbranch+clog(factor_count)})
    return common


def compile_source(source, source_hash):
    assert source["format"] == "shared-point-source-coefficient-dag/v1"
    old = source["coefficient_dag"]
    base_count = source["retained_base_count"]
    source_relations = source["finite_monic_relations"]
    assert source['all_quadratic_roots_nonzero'] is True
    assert all(r['generator_node'] in source['guard_numerators']
               for r in source_relations if r['kind'] != 'point')
    m = len(source_relations)
    point_count = sum(r["kind"] == "point" for r in source_relations)
    assert len(source["variables"]) == base_count+m
    assert [r["variable"] for r in source_relations] == list(range(base_count, base_count+m))
    out = DAG()
    two = out.integer(2)
    base = [out.node("variable", i) for i in range(base_count)]
    zs = [out.node("algebra_generator", i) for i in range(m)]
    replacements = {i: (base[i], 0) for i in range(base_count)}
    conversion = {}

    def convert(index):
        if index in conversion: return conversion[index]
        op, *a = old[index]
        if op == "variable":
            assert a[0] in replacements, "Coefficient not triangular"
            result = replacements[a[0]]
        elif op in ("int", "parameter"):
            result = out.node(op, *a), 0
        elif op == "neg":
            v, d = convert(a[0]); result = out.neg(v), d
        elif op == "pow":
            v, d = convert(a[0]); result = out.pow(v, a[1]), d*a[1]
        elif op == "mul":
            terms = [convert(k) for k in a]
            result = out.mul(*(v for v, _ in terms)), sum(d for _, d in terms)
        elif op == "add":
            terms = [convert(k) for k in a]; d = max(k for _, k in terms)
            result = out.add(*(out.mul(v, out.pow(two, d-k)) for v, k in terms)), d
        else: raise ValueError(op)
        conversion[index] = result
        return result

    relations, bit = [], 0
    for i, r in enumerate(source_relations):
        assert r["monic"]
        if r["kind"] == "point":
            assert i < point_count and r["degree"] == 4
            coefficients = [convert(k) for k in r["coefficient_nodes_ascending"]]
            assert all(d == 0 for _, d in coefficients)
            replacements[r["variable"]] = zs[i], 0
            derivative, de = convert(r["derivative_guard"])
            assert de == 0 and r["derivative_guard"] in source["guard_numerators"]
            relations.append({"generator": i, "name": r["name"], "kind": "point", "maximum_degree": 4,
                              "coefficient_nodes_ascending": [n for n, _ in coefficients],
                              "derivative_guard": derivative, "source_relation": r,
                              "replacement_numerator": zs[i], "replacement_denominator_power_of_two_exponent": 0})
        elif r["kind"] == "Lucas":
            assert i == point_count and r["degree"] == 2
            assert old[r["a"]["denominator"]] == old[r["b"]["denominator"]] == ["int", 1]
            a, ad = convert(r["a"]["numerator"])
            b, bd = convert(r["b"]["numerator"])
            assert ad == bd == 0
            Delta = out.add(out.pow(a, 2), out.mul(out.integer(-4), b))
            constant = out.neg(Delta)
            numerator = out.add(zs[i], a)
            replacements[r["variable"]] = numerator, 1
            relations.append({"generator": i, "name": r["name"]+".completed", "kind": "quadratic",
                              "maximum_degree": 2, "bit": bit, "coefficient_nodes_ascending": [constant, out.zero],
                              "source_relation": r, "completion_a": a, "completion_b": b, "discriminant": Delta,
                              "replacement_numerator": numerator, "replacement_denominator_power_of_two_exponent": 1})
            bit += 1
        else:
            assert r["degree"] == 2 and old[r["coefficient_nodes_ascending"][1]] == ["int", 0]
            image, exponent = convert(r["coefficient_nodes_ascending"][0])
            scale = (exponent+1)//2
            constant = out.mul(out.pow(two, 2*scale-exponent), image)
            replacements[r["variable"]] = zs[i], scale
            relations.append({"generator": i, "name": r["name"]+".integer_scaled", "kind": "quadratic",
                              "maximum_degree": 2, "bit": bit, "coefficient_nodes_ascending": [constant, out.zero],
                              "source_relation": r, "converted_constant_node": image,
                              "converted_constant_denominator_power_of_two_exponent": exponent,
                              "replacement_numerator": zs[i], "replacement_denominator_power_of_two_exponent": scale})
            bit += 1
    assert bit == m-point_count
    # Expand only multiplication/power structure to remove repeated guard
    # factors. No polynomial factorization or generic localization is used.
    ff, literal_zero = [], []
    for index, node in enumerate(old):
        op, *a = node
        if op == "int": fs, zero = frozenset(), a[0] == 0
        elif op == "neg": fs, zero = ff[a[0]], literal_zero[a[0]]
        elif op == "mul": fs, zero = frozenset().union(*(ff[k] for k in a)), any(literal_zero[k] for k in a)
        elif op == "pow": fs, zero = (ff[a[0]] if a[1] else frozenset()), literal_zero[a[0]] and a[1] != 0
        else: fs, zero = frozenset((index,)), False
        ff.append(fs); literal_zero.append(zero)
    assert not any(literal_zero[k] for k in source["guard_numerators"])
    guard_factors = sorted(frozenset().union(*(ff[k] for k in source["guard_numerators"])))
    automatic_factors = frozenset().union(*(
        ff[k] for r in source_relations if r["kind"] == "point"
        for k in r["automatic_nonzero_nodes"]))
    assert automatic_factors <= set(guard_factors)
    guard_records = []
    for index in guard_factors:
        image, exponent = convert(index)
        guard_records.append({"source_node": index, "numerator": image,
                              "numeric_denominator_exponent": exponent,
                              "automatic_at_rational_base": index in automatic_factors})
    guard = out.mul(*(r["numerator"] for r in guard_records
                      if not r["automatic_at_rational_base"]))
    closed = []
    for row in source["closed_equations"]:
        assert ff[row["denominator"]] <= set(guard_factors)
        image, exponent = convert(row["numerator"])
        closed.append({"label": row["label"], "numerator": image, "source_row": row,
                       "numeric_denominator_exponent": exponent})
    indexed = []
    for macro in source["indexed_guard_polynomials"]:
        args = macro["variable_field_argument"]
        pairs = []
        for arg in args:
            assert ff[arg["denominator"]] <= set(guard_factors)
            nn, nd = convert(arg["numerator"])
            dn, dd = convert(arg["denominator"])
            pairs.append((out.mul(nn, out.pow(two, dd)), out.mul(dn, out.pow(two, nd))))
        if pairs[0][1] == pairs[1][1]:
            N0, N1, D = pairs[0][0], pairs[1][0], pairs[0][1]
        else:
            N0, N1 = out.mul(pairs[0][0], pairs[1][1]), out.mul(pairs[1][0], pairs[0][1])
            D = out.mul(pairs[0][1], pairs[1][1])
        assert macro["index_last"]["base"] == 2
        indexed.append({"name": macro["name"], "N0": N0, "N1": N1, "D": D,
                        "index_first": 1, "index_last": macro["index_last"],
                        "fixed_point": macro["fixed_point"], "fixed_curve_D": macro["fixed_curve_D"],
                        "constant_algorithm": "Left-to-right binary elliptic multiplication; exact arithmetic in Q[sqrt(2)].",
                        "canonical_triple": "x(nP)=(a_n+b_n*sqrt(2))/c_n, c_n>0, gcd(|a_n|,|b_n|,c_n)=1.",
                        "factor": "(c_n*N0-a_n*D)^2-2*(c_n*N1-b_n*D)^2",
                        "identity_multiple_rule": "If nP is the identity, the factor is 1.",
                        "source_macro": macro})
    local_relation_keys = ("derivative_guard", "completion_a", "completion_b", "discriminant",
                           "converted_constant_node", "replacement_numerator")
    roots = [guard]
    roots += [r["numerator"] for r in guard_records]+[r["numerator"] for r in closed]
    roots += [node for r in relations for node in r["coefficient_nodes_ascending"]]
    roots += [r[key] for r in relations for key in local_relation_keys if key in r]
    roots += [macro[key] for macro in indexed for key in ("N0", "N1", "D")]
    nodes, remap = prune(out.nodes, roots)
    for r in relations:
        r["coefficient_nodes_ascending"] = [remap[k] for k in r["coefficient_nodes_ascending"]]
        for key in local_relation_keys:
            if key in r: r[key] = remap[r[key]]
    for row in guard_records+closed: row["numerator"] = remap[row["numerator"]]
    for macro in indexed:
        for key in ("N0", "N1", "D"): macro[key] = remap[macro[key]]
    guard = remap[guard]
    parameter_count = prod(len(v) for v in source["finite_parameters"].values())
    bounds = algebra_bounds(nodes, relations, guard, closed, indexed, parameter_count)
    external = [dict(v) for v in source["variables"][:base_count]]+[{
        "index": base_count, "name": "U", "category": "single finite-algebra witness"}]
    return {
        "format": "integer-polynomial-indexed-finite-algebra/v2",
        "source_json_sha256": source_hash, "source_commit": source["source_commit"],
        "source_arithmetic_input": source["additional_arithmetic_input"],
        "family_parameter": source["family_parameter"],
        "arithmetic_status": "A fixed coefficient-family member. Its coefficient conversion and bounds are exact, but this anchor exponent is not certified to exceed the ineffective sufficient threshold.",
        "anchor_kind": source["anchor_kind"], "shared_scalar_height_point": source["share_scalar_height_point"],
        "external_variables": external, "retained_base_variables": base_count,
        "total_external_variables": base_count+1, "existential_witnesses": base_count,
        "coefficient_dag": nodes, "monic_relations": relations,
        "materialized_guard_node": guard, "source_guard_factor_certificates": guard_records,
        "automatic_nonzero_factor_nodes": sorted(automatic_factors),
        "closed_equations": closed, "indexed_guard_polynomials": indexed,
        "source_finite_parameters": source["finite_parameters"],
        "finite_algebra_recipe": {
            "generator_count": m, "point_count": point_count, "quadratic_count": bit,
            "basis_order": "lexicographic exponent tuples in generator order, 0<=a_i<degree_i",
            "quadratic_mask": {"from": 2**bit-1, "to": 2**bit-1, "bits": bit},
            "zero_case": "Excluded by the source guards on every quadratic generator",
            "nonzero_case": "z_i^2+c_i=0; z_i!=0 is already a source guard",
            "guard": "materialized_guard * product(indexed_guard_polynomials)",
            "closed_residuals": "source closed_equations",
            "rank": f"4^{point_count}*2^popcount(quadratic_mask)",
            "selector_range": f"0..{m}*rank*(rank+1)/2", "degree_range": "1..rank",
        },
        "polynomial_recipe": {
            "theorem": "Theorem thm:explicit-guarded-finite-algebra in the accompanying paper",
            "lambda": f"1+sum_{{i=1}}^{m} selector^i*z_i",
            "H": "det(I-V*M_{G*lambda})=sum_{k=0}^{rank} a_k V^k",
            "R": "R_i(V)=Tr(M_{E_i} adj(I-V*M_{G*lambda}))",
            "H_d": "sum_{k=0}^d a_k V^k",
            "g": "a_d*Res_V(H_d,H_d')", "L": "a_d^2*g",
            "Psi": "1+sum_{j=1}^d a_{d-j}*a_d^(2*j-1)*g^j*U^j",
            "Rtilde": "sum_{k=0}^{rank-1} coefficient_V^k(R_i)*(L*U)^(rank-1-k)",
            "factor": "Psi^2+sum_{k=d+1}^{rank} a_k^2+sum_i Rtilde_i^2",
            "product": "factor over all source finite parameters, quadratic masks, selector range, and degree range",
            "only_external_variables": "external_variables; formal algebra generators and V are bound by finite matrix/coefficient operations",
        },
        "bounds": bounds,
        "representation_scope": "Complete determinant/coefficient/finite-product polynomial specification with a materialized integer coefficient DAG. No finite elliptic exclusion is used in the fixed-prime construction. Rank-sized matrices, finite products, and monomial expansion are specified exactly rather than expanded.",
        "arithmetic_scope": "The compiler proves equality with the supplied guarded finite source. Identifying its input projection with Z additionally uses the source arithmetic proof and its cited inputs.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = gzip.decompress(args.source.read_bytes()) if args.source.suffix == ".gz" else args.source.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    spec = compile_source(json.loads(raw), source_hash)
    encoded = (json.dumps(spec, separators=(",", ":"))+"\n").encode()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/"polynomial-specification.json").write_bytes(encoded)
    report = {
        "total_variables": spec["total_external_variables"], "existential_witnesses": spec["existential_witnesses"],
        "formal_algebra_generators_not_external_variables": spec["finite_algebra_recipe"]["generator_count"],
        "coefficient_dag_nodes": len(spec["coefficient_dag"]),
        "maximum_rank_power_of_two_exponent": spec["bounds"]["maximum_rank_power_of_two_exponent"],
        "degree_bound_power_of_two_exponent": spec["bounds"]["degree_bound_power_of_two_exponent"],
        "coefficient_height_bound_double_power_of_two_exponent": spec["bounds"]["coefficient_height_bound_double_power_of_two_exponent"],
        "indexed_elliptic_anchor": bool(spec["indexed_guard_polynomials"]),
        "specification_sha256": hashlib.sha256(encoded).hexdigest(), "specification_bytes": len(encoded),
        "source_json_sha256": source_hash, "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "verification_status": "Producer assertions passed; independent results are recorded separately in verification.json.",
        "family_parameter": spec["family_parameter"],
        "arithmetic_status": spec["arithmetic_status"],
        "representation": spec["representation_scope"],
    }
    (args.output/"construction-report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
