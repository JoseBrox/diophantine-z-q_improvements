#!/usr/bin/env python3
"""Independent exact source-to-indexed-polynomial audit for the small sources.

Imports no producer. Reconstructs every affine source substitution, checks the
zero/nonzero finite algebra and source guard coverage, and verifies all numeric
and power-envelope bounds. Source arithmetic theorems are a separate layer.
"""
import argparse
import gzip
import hashlib
import json
from math import prod
from pathlib import Path

from finite_algebra_check_core import check, children, support_table, expander, plus, times, power, Interner


def clog(n): return (n-1).bit_length() if n > 0 else 0


def audit(source, spec):
    check(source["format"] == "shared-point-source-coefficient-dag/v1"
          and spec["format"] == "integer-polynomial-indexed-finite-algebra/v2", "Unknown source or output grammar")
    b = source["retained_base_count"]
    old, nodes = source["coefficient_dag"], spec["coefficient_dag"]
    sr, rel = source["finite_monic_relations"], spec["monic_relations"]
    m = len(sr); p = sum(r["kind"] == "point" for r in sr); q = m-p
    check(len(rel) == m and [r["generator"] for r in rel] == list(range(m)), "Wrong finite generators")
    check([r["variable"] for r in sr] == list(range(b, b+m)), "Noncanonical source variables")
    check(spec["retained_base_variables"] == b and spec["total_external_variables"] == b+1
          and spec["existential_witnesses"] == b, "Wrong external variable count")
    check(spec["external_variables"] == source["variables"][:b]+[{
        "index": b, "name": "U", "category": "single finite-algebra witness"}], "Changed retained variables")
    check(spec["source_commit"] == source["source_commit"]
          and spec["source_arithmetic_input"] == source["additional_arithmetic_input"]
          and spec["anchor_kind"] == source["anchor_kind"]
          and spec["shared_scalar_height_point"] == source["share_scalar_height_point"], "Changed arithmetic-source metadata")
    check(spec["source_finite_parameters"] == source["finite_parameters"], "Changed source finite cases")
    old_support = support_table(old)
    gen_support = support_table(nodes, "algebra_generator")
    base_support = support_table(nodes, "variable")
    for op, *a in nodes:
        if op == "int": check(len(a) == 1 and type(a[0]) is int, "Noninteger node")
        elif op == "variable": check(len(a) == 1 and 0 <= a[0] < b, "Hidden external variable")
        elif op == "algebra_generator": check(len(a) == 1 and 0 <= a[0] < m, "Unknown finite generator")
        elif op == "parameter": check(len(a) == 2 and a[0] in source["finite_parameters"]
            and a[1] >= max(map(abs, source["finite_parameters"][a[0]])), "Wrong finite coefficient parameter")
        elif op == "pow": check(len(a) == 2 and type(a[1]) is int and a[1] >= 0, "Invalid power")
        elif op == "neg": check(len(a) == 1, "Invalid negation")
        elif op in ("add", "mul"): check(len(a) >= 2, "Invalid arithmetic arity")

    # Canonical expression-tree identities prove the full affine conversion.
    it = Interner(); ids = it.read(nodes); two = it.raw("int", 2)
    replacements = {i: (it.raw("variable", i), 0) for i in range(b)}
    memo = {}

    def convert(index):
        if index in memo: return memo[index]
        op, *a = old[index]
        if op == "variable":
            check(a[0] in replacements, "Nontriangular source coefficient")
            out = replacements[a[0]]
        elif op in ("int", "parameter"): out = it.raw(op, *a), 0
        elif op == "neg":
            n, d = convert(a[0]); out = it.neg(n), d
        elif op == "pow":
            n, d = convert(a[0]); out = it.pow(n, a[1]), d*a[1]
        elif op == "mul":
            terms = [convert(k) for k in a]
            out = it.mul(*(n for n, _ in terms)), sum(d for _, d in terms)
        elif op == "add":
            terms = [convert(k) for k in a]; d = max(e for _, e in terms)
            out = it.add(*(it.mul(n, it.pow(two, d-e)) for n, e in terms)), d
        memo[index] = out
        return out

    bit = 0
    source_names = {v["name"]: v["index"] for v in source["variables"]}
    x, y, z = [{(i,): 1} for i in range(3)]
    A = plus(power(x, 3), times({(): 6}, x, power(y, 2)), times({(): -11}, x), times({(): 12}, y))
    B = plus(times({(): 3}, power(x, 2), y), times({(): 2}, power(y, 3)), times({(): -11}, y), times({(): 6}, x))
    for i, (original, new) in enumerate(zip(sr, rel)):
        check(new["source_relation"] == original and original["monic"] is True, "Changed monic source relation")
        zi = it.raw("algebra_generator", i)
        if original["kind"] == "point":
            check(i < p and new["kind"] == "point" and new["maximum_degree"] == original["degree"] == 4,
                  "Wrong point monic degree")
            for old_coefficient, new_coefficient in zip(original["coefficient_nodes_ascending"], new["coefficient_nodes_ascending"]):
                image, d = convert(old_coefficient)
                check(d == 0 and image == ids[new_coefficient], "Changed point coefficient")
            replacements[original["variable"]] = zi, 0
            image, d = convert(original["derivative_guard"])
            check(d == 0 and image == ids[new["derivative_guard"]]
                  and original["derivative_guard"] in source["guard_numerators"], "Missing point derivative guard")
            prefix = original["name"][:-2]
            ia, ib = source_names[prefix+".a0"], source_names[prefix+".a1"]
            expand = expander(nodes, variables={ia: 0, ib: 1}, generators={i: 2})
            expected = [times({(): 8}, power(B, 2)), {}, times({(): -4}, A), {}]
            check([expand(k) for k in new["coefficient_nodes_ascending"]] == expected
                  and expand(new["derivative_guard"]) == plus(times({(): 4}, power(z, 3)), times({(): -8}, A, z)),
                  "Point quartic or derivative does not match the curve")
            check(new["replacement_denominator_power_of_two_exponent"] == 0
                  and ids[new["replacement_numerator"]] == zi, "Changed point replacement")
        elif original["kind"] == "Lucas":
            check(i == p and new["kind"] == "quadratic" and new["bit"] == bit, "Wrong completed Lucas position")
            check(old[original["a"]["denominator"]] == old[original["b"]["denominator"]] == ["int", 1],
                  "Nonintegral Lucas coefficients")
            aa, da = convert(original["a"]["numerator"])
            bb, db = convert(original["b"]["numerator"])
            check(da == db == 0 and aa == ids[new["completion_a"]] and bb == ids[new["completion_b"]],
                  "Changed Lucas coefficients")
            delta = it.add(it.pow(aa, 2), it.mul(it.raw("int", -4), bb))
            numerator = it.add(zi, aa)
            check(ids[new["discriminant"]] == delta and ids[new["coefficient_nodes_ascending"][0]] == it.neg(delta)
                  and nodes[new["coefficient_nodes_ascending"][1]] == ["int", 0], "Incorrect completed Lucas square")
            check(ids[new["replacement_numerator"]] == numerator
                  and new["replacement_denominator_power_of_two_exponent"] == 1, "Incorrect Lucas reconstruction")
            expand_old = expander(old, variables={k: k for k in range(b)})
            check(expand_old(original["coefficient_nodes_ascending"][0]) == expand_old(original["b"]["numerator"])
                  and plus(expand_old(original["coefficient_nodes_ascending"][1]), expand_old(original["a"]["numerator"])) == {},
                  "Source Lucas polynomial differs from its completion metadata")
            replacements[original["variable"]] = numerator, 1
            bit += 1
        else:
            check(original["degree"] == new["maximum_degree"] == 2 and new["kind"] == "quadratic"
                  and new["bit"] == bit and old[original["coefficient_nodes_ascending"][1]] == ["int", 0],
                  "Unknown quadratic source form")
            image, exponent = convert(original["coefficient_nodes_ascending"][0])
            scale = (exponent+1)//2
            constant = it.mul(it.pow(two, 2*scale-exponent), image)
            check(ids[new["coefficient_nodes_ascending"][0]] == constant
                  and nodes[new["coefficient_nodes_ascending"][1]] == ["int", 0]
                  and ids[new["converted_constant_node"]] == image
                  and new["converted_constant_denominator_power_of_two_exponent"] == exponent,
                  "Quadratic coefficient rescaling failed")
            check(ids[new["replacement_numerator"]] == zi
                  and new["replacement_denominator_power_of_two_exponent"] == scale, "Wrong quadratic recovery scale")
            replacements[original["variable"]] = zi, scale
            bit += 1
        check(all(gen_support[k] < (1 << i) for k in new["coefficient_nodes_ascending"]), "Output monic coefficients are not triangular")
    check(bit == q, "Wrong number of zero/nonzero quadratic cases")

    ff, zero = [], []
    for index, node in enumerate(old):
        op, *a = node
        if op == "int": factors, zz = frozenset(), a[0] == 0
        elif op == "neg": factors, zz = ff[a[0]], zero[a[0]]
        elif op == "mul": factors, zz = frozenset().union(*(ff[k] for k in a)), any(zero[k] for k in a)
        elif op == "pow": factors, zz = (ff[a[0]] if a[1] else frozenset()), zero[a[0]] and a[1] != 0
        else: factors, zz = frozenset((index,)), False
        ff.append(factors); zero.append(zz)
    check(not any(zero[k] for k in source["guard_numerators"]), "Literal-zero source guard")
    guard_factors = sorted(frozenset().union(*(ff[k] for k in source["guard_numerators"])))
    # Independently certify the source's rational-square clearing:
    # q^2=N/D is represented by Z=D*q and Z^2-N*D=0.
    # This checks the denominator before the later power-of-two changes.
    signed_factors = []
    for index, (op, *args) in enumerate(old):
        if op == "int":
            value = args[0]
            sign = (value > 0)-(value < 0)
            factors = {} if abs(value) <= 1 else {("integer", abs(value)): 1}
        elif op == "neg":
            sign, factors = signed_factors[args[0]]
            sign = -sign
        elif op == "pow":
            previous_sign, previous_factors = signed_factors[args[0]]
            sign = previous_sign**args[1]
            factors = {key: exponent*args[1] for key, exponent in previous_factors.items() if args[1]}
        elif op == "mul":
            sign, factors = 1, {}
            for child in args:
                child_sign, child_factors = signed_factors[child]
                sign *= child_sign
                for key, exponent in child_factors.items():
                    factors[key] = factors.get(key, 0)+exponent
        else:
            sign, factors = 1, {("node", index): 1}
        signed_factors.append((sign, factors))
    cleared_squares = 0
    for original in sr:
        if original["kind"] in ("point", "Lucas"):
            continue
        radicand = original["original_square_input"]
        root = original["original_root"]
        nn, dd = radicand["numerator"], radicand["denominator"]
        check(not zero[dd] and ff[dd] <= set(guard_factors),
              "Source rational-square denominator is unguarded")
        ns, nf = signed_factors[nn]
        ds, df = signed_factors[dd]
        expected_factors = dict(nf)
        for key, exponent in df.items():
            expected_factors[key] = expected_factors.get(key, 0)+exponent
        check(signed_factors[original["coefficient_nodes_ascending"][0]] == (-ns*ds, expected_factors),
              "Source rational-square clearing is not Z^2=N*D")
        check(old[root["numerator"]] == ["variable", original["variable"]]
              and signed_factors[root["denominator"]] == signed_factors[dd],
              "Source rational-square root is not Z/D")
        cleared_squares += 1
    records = spec["source_guard_factor_certificates"]
    check([r["source_node"] for r in records] == guard_factors, "Changed source guard factors")
    for record in records:
        image, exponent = convert(record["source_node"])
        check(ids[record["numerator"]] == image and record["numeric_denominator_exponent"] == exponent,
              "Source guard conversion failed")
    check(ids[spec["materialized_guard_node"]] == it.mul(*(ids[r["numerator"]] for r in records)), "Wrong materialized guard product")
    check(len(spec["closed_equations"]) == len(source["closed_equations"]), "Changed closed conditions")
    for old_eq, new_eq in zip(source["closed_equations"], spec["closed_equations"]):
        check(new_eq["source_row"] == old_eq and ff[old_eq["denominator"]] <= set(guard_factors), "Closed denominator is unguarded")
        image, exponent = convert(old_eq["numerator"])
        check(ids[new_eq["numerator"]] == image and new_eq["numeric_denominator_exponent"] == exponent,
              "Closed residual conversion failed")
    check(len(spec["indexed_guard_polynomials"]) == len(source["indexed_guard_polynomials"]), "Changed indexed guards")
    for old_macro, new_macro in zip(source["indexed_guard_polynomials"], spec["indexed_guard_polynomials"]):
        check(new_macro["source_macro"] == old_macro, "Changed indexed source guard")
        pairs = []
        for arg in old_macro["variable_field_argument"]:
            check(ff[arg["denominator"]] <= set(guard_factors), "Indexed argument denominator is unguarded")
            nn, nd = convert(arg["numerator"]); dn, dd = convert(arg["denominator"])
            pairs.append((it.mul(nn, it.pow(two, dd)), it.mul(dn, it.pow(two, nd))))
        if pairs[0][1] == pairs[1][1]: nn0, nn1, den = pairs[0][0], pairs[1][0], pairs[0][1]
        else: nn0, nn1, den = it.mul(pairs[0][0], pairs[1][1]), it.mul(pairs[1][0], pairs[0][1]), it.mul(pairs[0][1], pairs[1][1])
        check([ids[new_macro[k]] for k in ("N0", "N1", "D")] == [nn0, nn1, den], "Indexed norm clearing differs")
        check(new_macro["index_first"] == 1 and new_macro["index_last"] == old_macro["index_last"]
              and new_macro["index_last"]["base"] == 2
              and new_macro["fixed_curve_D"] == [11, -6]
              and new_macro["fixed_point"] == {"x": ["57/8", "-7/2"], "y": ["-165/8", "417/32"]},
              "Unknown indexed elliptic constants")
        check(new_macro["factor"] == "(c_n*N0-a_n*D)^2-2*(c_n*N1-b_n*D)^2"
              and new_macro["canonical_triple"] == "x(nP)=(a_n+b_n*sqrt(2))/c_n, c_n>0, gcd(|a_n|,|b_n|,c_n)=1."
              and new_macro["constant_algorithm"] == "Left-to-right binary elliptic multiplication; exact arithmetic in Q[sqrt(2)]."
              and new_macro["identity_multiple_rule"] == "If nP is the identity, the factor is 1.", "Ambiguous indexed-factor convention")

    # Independently verify every supplied algebra majorant as an inequality.
    bd = spec["bounds"]; ws, bs = bd["generator_weights"], bd["generator_operator_log2_norm_bounds"]
    check(len(ws) == len(bs) == m and all(type(v) is int and v >= 1 for v in ws)
          and all(type(v) is int and v >= 0 for v in bs), "Invalid generator bounds")
    estimates = []
    for op, *a in nodes:
        if op == "int": out = 0, clog(abs(a[0]))
        elif op == "variable": out = 1, 0
        elif op == "parameter": out = 0, clog(a[1])
        elif op == "algebra_generator": out = ws[a[0]], bs[a[0]]
        elif op == "neg": out = estimates[a[0]]
        elif op == "pow": out = tuple(e*a[1] for e in estimates[a[0]])
        elif op == "mul": out = tuple(sum(estimates[k][j] for k in a) for j in (0, 1))
        elif op == "add": out = max(estimates[k][0] for k in a), max(estimates[k][1] for k in a)+clog(len(a))
        estimates.append(out)
    for i, r in enumerate(rel):
        degree = r["maximum_degree"]
        nonzero = [(k, node) for k, node in enumerate(r["coefficient_nodes_ascending"]) if nodes[node] != ["int", 0]]
        check(all(estimates[node][0]+k*ws[i] <= degree*ws[i] for k, node in nonzero), "Weighted reduction can increase degree")
        # This checks the sufficient weighted-column inequalities directly,
        # without importing or repeating the producer's ceiling formula.
        count_bits = clog(max(1, len(nonzero)))
        check(bs[i] >= count_bits and all(
              (degree-k)*(bs[i]-count_bits) >= estimates[node][1]
              for k, node in nonzero),
              "Weighted companion multiplication norm is understated")
    W = sum((r["maximum_degree"]-1)*ws[i] for i, r in enumerate(rel))
    wg, bg = estimates[spec["materialized_guard_node"]]
    wg += sum(ws[i] for i, r in enumerate(rel) if r["kind"] == "quadratic")
    bg += sum(bs[i] for i, r in enumerate(rel) if r["kind"] == "quadratic")
    residual_nodes = [e["numerator"] for e in spec["closed_equations"]]+[r["coefficient_nodes_ascending"][0] for r in rel if r["kind"] == "quadratic"]
    we, be = (max([0]+[estimates[k][j] for k in residual_nodes]) for j in (0, 1))
    rexp = 2*p+q; n = 2**rexp; selector = m*n*(n+1)//2
    blambda = clog(m+1)+max((i+1)*clog(selector)+bits for i, bits in enumerate(bs))
    params = prod(len(v) for v in source["finite_parameters"].values())
    n0 = 4**p
    count = params*(n0*3**q+m*(n0**3*9**q+n0**2*5**q)//2)
    expected = {"maximum_rank_power_of_two_exponent": rexp, "maximum_rank": n, "maximum_basis_weight": W,
                "materialized_guard_weight": wg, "materialized_guard_operator_log2_norm_bound": bg,
                "closed_residual_maximum_weight": we, "closed_residual_maximum_operator_log2_norm_bound": be,
                "closed_residual_count": len(residual_nodes), "maximum_selector": selector,
                "selector_operator_log2_norm_bound": blambda, "source_parameter_branches": params,
                "exact_number_of_final_factors": count,
                "coefficient_norm_method": "weighted_companion_column_norm"}
    for key, value in expected.items(): check(bd[key] == value, "Incorrect aggregate bound: "+key)
    indexed = spec["indexed_guard_polynomials"]
    check(len(bd["indexed_guard_bounds"]) == len(indexed), "Missing indexed coefficient bound")
    for macro, bound in zip(indexed, bd["indexed_guard_bounds"]):
        wa = max(estimates[macro[k]][0] for k in ("N0", "N1", "D"))
        ba = max(estimates[macro[k]][1] for k in ("N0", "N1", "D"))
        E = macro["index_last"]["exponent"]
        check(E >= 6 and 30*64+(2*ba+14) <= 64**2, "Cubic exclusion constant requires M>=64")
        check(bound["coordinate_weight_bound"] == wa and bound["coordinate_operator_log2_norm_bound"] == ba
              and bound["weight_bound_power_of_two_exponent"] == 1+E+clog(max(1, wa))
              and bound["operator_log2_norm_bound_power_of_two_exponent"] == 3*E+5,
              "Incorrect indexed-anchor bound")
        check(bound["fixed_multiple_height_bound"] == "h0(x(nP)) <= 30*n^2"
              and bound["guard_operator_log2_norm_bound"] == "20*M^3+30*M^2+(2*b+14)*M <= 21*M^3",
              "Wrong cubic exclusion proof annotation")
    if not indexed:
        alpha, beta = wg+max(ws)+W, bg+blambda
        AH, BH = n*alpha, n*(beta+1)
        AR, BR = (n-1)*alpha+we+W, rexp+be+(n-1)*(beta+1)
        AL, BL = (2*n+2)*AH, (2*n+2)*BH+(2*n-1)*rexp
        dbranch = 2*max(AH, n*(AL+1), AR+(n-1)*(AL+1))
        bbranch = 2*max(BH, n*BL+clog(n+1), BR+(n-1)*BL)+clog(n+len(residual_nodes)+1)
        check(bd["bound_mode"] == "exact_integer_majorants", "Wrong finite bound mode")
        expected.update({"operator_entry_degree": alpha, "operator_log2_norm_bound": beta,
                         "H_coefficient_degree": AH, "H_log2_norm_bound": BH,
                         "trace_coefficient_degree": AR, "trace_log2_norm_bound": BR,
                         "scale_degree": AL, "scale_log2_norm_bound": BL,
                         "branch_degree_bound": dbranch, "branch_log2_norm_bound": bbranch,
                         "degree_bound": count*dbranch, "coefficient_height_log2_bound": count*bbranch,
                         "degree_bound_power_of_two_exponent": clog(count*dbranch),
                         "coefficient_height_bound_double_power_of_two_exponent": clog(count*bbranch)})
        for key, value in expected.items(): check(bd[key] == value, "Incorrect determinant/product bound: "+key)
    else:
        # Each listed e means the corresponding nonnegative quantity <=2^e.
        eg = max([clog(wg)]+[r["weight_bound_power_of_two_exponent"] for r in bd["indexed_guard_bounds"]])+clog(1+len(indexed))
        ebg = max([clog(bg)]+[r["operator_log2_norm_bound_power_of_two_exponent"] for r in bd["indexed_guard_bounds"]])+clog(1+len(indexed))
        ea, eb = max(eg, clog(max(ws)+W))+1, max(ebg, clog(blambda))+1
        eAH, eBH = rexp+ea, rexp+eb+1
        eAR, eBR = max(rexp+ea, clog(we+W))+1, max(clog(rexp+be), rexp+eb+1)+1
        eAL = rexp+2+eAH
        eBL = max(rexp+2+eBH, rexp+1+clog(rexp))+1
        epd, epb = rexp+eAL+1, max(rexp+eBL, clog(rexp+1))+1
        erd, erb = max(eAR, rexp+eAL+1)+1, max(eBR, rexp+eBL)+1
        edbranch = 1+max(eAH, epd, erd)
        ebbranch = max(1+max(eBH, epb, erb), clog(clog(n+len(residual_nodes)+1)))+1
        powers = {"guard_weight": eg, "guard_log2_norm": ebg,
                  "operator_entry_degree": ea, "operator_log2_norm": eb,
                  "H_coefficient_degree": eAH, "H_log2_norm": eBH,
                  "trace_coefficient_degree": eAR, "trace_log2_norm": eBR,
                  "scale_degree": eAL, "scale_log2_norm": eBL,
                  "reciprocal_degree": epd, "reciprocal_log2_norm": epb,
                  "reversed_trace_degree": erd, "reversed_trace_log2_norm": erb,
                  "branch_degree": edbranch, "branch_log2_norm": ebbranch}
        check(bd["bound_mode"] == "explicit_power_of_two_envelopes" and bd["power_envelopes"] == powers
              and bd["degree_bound_power_of_two_exponent"] == edbranch+clog(count)
              and bd["coefficient_height_bound_double_power_of_two_exponent"] == ebbranch+clog(count),
              "Incorrect indexed-product power envelopes")
    algebra = spec["finite_algebra_recipe"]
    check(algebra["generator_count"] == m and algebra["point_count"] == p and algebra["quadratic_count"] == q
          and algebra["quadratic_mask"] == {"from": 0, "to": 2**q-1, "bits": q}
          and algebra["zero_case"] == "z_i=0 and add closed equation c_i=0"
          and algebra["nonzero_case"] == "z_i^2+c_i=0 and add guard z_i!=0"
          and algebra["guard"] == "materialized_guard * product(indexed_guard_polynomials) * product(nonzero_case_generators)"
          and algebra["closed_residuals"] == "source closed_equations plus (1-bit_i)*c_i for every quadratic"
          and algebra["rank"] == f"4^{p}*2^popcount(quadratic_mask)"
          and algebra["selector_range"] == f"0..{m}*rank*(rank+1)/2" and algebra["degree_range"] == "1..rank",
          "Unknown finite-algebra macro grammar")
    recipe = spec["polynomial_recipe"]
    check(recipe["lambda"] == f"1+sum_{{i=1}}^{m} selector^i*z_i"
          and recipe["H"] == "det(I-V*M_{G*lambda})=sum_{k=0}^{rank} a_k V^k"
          and recipe["R"] == "R_i(V)=Tr(M_{E_i} adj(I-V*M_{G*lambda}))"
          and recipe["H_d"] == "sum_{k=0}^d a_k V^k"
          and recipe["g"] == "a_d*Res_V(H_d,H_d')" and recipe["L"] == "a_d^2*g"
          and recipe["Psi"] == "1+sum_{j=1}^d a_{d-j}*a_d^(2*j-1)*g^j*U^j"
          and recipe["Rtilde"] == "sum_{k=0}^{rank-1} coefficient_V^k(R_i)*(L*U)^(rank-1-k)"
          and recipe["factor"] == "Psi^2+sum_{k=d+1}^{rank} a_k^2+sum_i Rtilde_i^2"
          and recipe["product"] == "factor over all source finite parameters, quadratic masks, selector range, and degree range",
          "Unknown determinant/coefficient/product recipe")
    used = base_support[spec["materialized_guard_node"]]
    for r in rel:
        for node in r["coefficient_nodes_ascending"]: used |= base_support[node]
    for row in spec["closed_equations"]: used |= base_support[row["numerator"]]
    check(used == (1 << b)-1, "Unused declared base coordinate")
    return {
        "status": "passed", "external_variables": b+1, "existential_witnesses": b,
        "formal_algebra_generators_not_external_variables": m,
        "coefficient_dag_nodes": len(nodes), "source_point_quartics_checked": p,
        "quadratic_zero_nonzero_bits": q, "source_closed_conditions": len(source["closed_equations"]),
        "source_guard_atomic_factors_checked": len(guard_factors),
        "affine_source_substitutions_checked_exactly": True,
        "all_repeated_quadratic_root_cases_included": True,
        "source_point_derivative_guards_present": True,
        "source_rational_square_clearings_checked": cleared_squares,
        "all_external_base_coordinates_occur": True,
        "indexed_elliptic_guard_canonical_clearing_checked": bool(indexed),
        "degree_and_coefficient_majorants_checked": True,
        "maximum_rank_power_of_two_exponent": rexp,
        "degree_bound_power_of_two_exponent": bd["degree_bound_power_of_two_exponent"],
        "coefficient_height_bound_double_power_of_two_exponent": bd["coefficient_height_bound_double_power_of_two_exponent"],
        "scope": "Exact coefficient conversion, guard coverage, finite-case grammar, and degree/coefficient bounds. The finite-algebra theorem justifies the determinant, trace, resultant and finite-product operations. The supplied source arithmetic proof uses its four cited inputs; this computation does not verify those deep theorems.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("specification", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_raw = gzip.decompress(args.source.read_bytes()) if args.source.suffix == ".gz" else args.source.read_bytes()
    raw = args.specification.read_bytes(); spec = json.loads(raw)
    check(hashlib.sha256(source_raw).hexdigest() == spec["source_json_sha256"], "Source hash differs")
    report = audit(json.loads(source_raw), spec) | {
        "source_json_sha256": hashlib.sha256(source_raw).hexdigest(),
        "specification_sha256": hashlib.sha256(raw).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = args.output or args.specification.with_name("verification.json")
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
