#!/usr/bin/env python3
"""Independent exact audit of four cyclic-norm specifications and degree bounds.

This file imports no producer or earlier checker.  It checks the complete
copied residual tables against pinned source bytes, constructs the cyclic
matrix entries by iterating the shift operator, verifies Galois conjugacy,
and recomputes all reported height and field-compiler degree bounds.

The degree-72/74 determinants are not expanded.  Arithmetic assertions that
the original source projects to Z are outside this audit.  Division over
the stated fields follows from the proof reviewed in the companion TeX.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import comb, factorial, gcd, isqrt, prod
from pathlib import Path
import gzip
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PINNED = {
    1315: (1272, 36, 37, 2, "research/phase3/quartic/quartic-direct/polynomial.json.gz",
           "dbd50fdd3484df9aa27b0133406f644689f9bff776c34bf2fdad64494270a5ff"),
    1339: (1296, 36, 37, 2, "research/phase3/quartic/quartic-direct-small-coefficients/polynomial.json.gz",
           "9486590b47c79aa4e37bf185dc278e2010567c3d98023785b6eb7bd6eeaa72e0"),
    1367: (1322, 37, 149, 5, "research/phase2/quartic/quartic-best/polynomial.json.gz",
           "3fa1e4a2119820c49ccd1de03ba4363041d780d73872b98623de4aebc38a6cee"),
    1391: (1346, 37, 149, 5, "research/phase2/quartic/quartic-small-coefficients/polynomial.json.gz",
           "f7c339b089908fd9365f183fdb2a67fdcfa2cb0ad4bdcd9e2179054bfdabc6a1"),
}
FIELD_SOURCES = {
    "research/phase3/finite_fibre/polynomial-41": (41, 9566686),
    "research/phase3/finite_fibre/polynomial-43-semilocal": (43, 250),
    "research/phase2/finite_fibre/polynomial-43-conic": (43, 9566693),
    "research/phase2/finite_fibre/polynomial-45-conic-semilocal": (45, 257),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def clog(n):
    require(type(n) is int and n >= 0, "Invalid nonnegative integer bound")
    return (n - 1).bit_length() if n > 0 else 0


def prime(n):
    return n >= 2 and all(n % a for a in range(2, isqrt(n) + 1))


def load_gzip(path):
    raw = gzip.decompress(path.read_bytes())
    return raw, json.loads(raw)


def verify_norm(norm, d, q, p):
    require(prime(q) and prime(p) and (q - 1) % d == 0, "Invalid norm primes/degrees")
    require((norm["cyclic_degree"], norm["conductor_prime"], norm["cyclic_parameter_prime"])
            == (d, q, p), "Changed cyclic algebra")
    g = norm["primitive_root"]
    require({pow(g, j, q) for j in range(q - 1)} == set(range(1, q)), "Not a primitive root")
    periods = norm["period_exponents"]
    subgroup = {pow(g, d * j, q) for j in range((q - 1) // d)}
    expected = [sorted(pow(g, j, q) * h % q for h in subgroup) for j in range(d)]
    require(periods == expected, "Cyclotomic periods changed")
    require(sorted(a for row in periods for a in row) == list(range(1, q)), "Periods do not partition")
    frobenius_order = next(j for j in range(1, d + 1) if pow(p, j, q) in subgroup)
    require(frobenius_order == d, "Parameter prime is not inert")
    require(norm["cyclotomic_modulus_coefficients_ascending"] == [1] * q, "Wrong cyclotomic modulus")
    require(norm["coefficient_basis"] ==
            f"beta_0=1; beta_i=sum(zeta^a for a in period_exponents[i]), 1<=i<{d}",
            "Ambiguous coefficient basis")
    require(norm["matrix_entry_rule"] ==
            f"scale*(F[{d}*block]+sum_{{i=1}}^{{{d-1}}}(sum_{{a in period_exponents[(i+period_shift)%{d}]}}zeta^a)*F[{d}*block+i]); pad F by zero to length{d*d}",
            "Changed matrix interpretation")
    require(norm["polynomial"] ==
            f"coefficient_zeta^0 of determinant(matrix), reduced modulo 1+zeta+...+zeta^{q-1}",
            "Changed coefficient-extraction interpretation")

    # Construct each U^j column by j successive applications of U.
    entries = {}
    for col in range(d):
        row, scale = col, 1
        for j in range(d):
            entries[row, col] = {"row": row, "column": col, "scale": scale,
                                 "residual_block": j, "period_shift": row}
            if row == 0:
                row, scale = d - 1, scale * p
            else:
                row -= 1
        require(row == col and scale == p, "U^d differs from pI")
    given = norm["matrix_entries"]
    require(len(given) == d * d and len({(a["row"], a["column"]) for a in given}) == d * d,
            "Missing or duplicate matrix entries")
    require(all(a == entries[a["row"], a["column"]] for a in given), "Wrong shifted matrix entry")

    # sigma(A)=U A U^{-1}, checked as formal linear forms in all residuals.
    for row in range(d):
        for col in range(d):
            lhs = entries[row, col]
            rhs = entries[(row + 1) % d, (col + 1) % d]
            ratio = Fraction(p if row == d - 1 else 1, p if col == d - 1 else 1)
            require(lhs["residual_block"] == rhs["residual_block"], "Conjugacy changes block")
            require(lhs["scale"] == ratio * rhs["scale"], "Conjugacy scalar mismatch")
            for i in range(1, d):
                transformed = sorted(g * a % q for a in periods[(i + row) % d])
                require(transformed == periods[(i + rhs["period_shift"]) % d],
                        "Galois conjugacy coefficient mismatch")

    norm_bound = factorial(d) * ((q - 1) * p) ** d
    require(norm["norm_degree"] == d and norm["norm_coefficient_l1_bound"] == norm_bound,
            "Norm degree or coefficient bound differs")
    certificate = {"degree": d, "conductor": q, "parameter": p, "primitive_root": g,
                   "frobenius_coset_order": frobenius_order, "matrix_entries_checked": d * d,
                   "formal_conjugacy": "sigma(A)=U*A*U^-1, coefficient by coefficient",
                   "coefficient_l1_bound": norm_bound, "coefficient_l1_bound_log2_ceiling": clog(norm_bound)}
    if d == 36:
        # X^37=2X modulo X^36-2.  Frobenius orbits of every nonzero root
        # therefore have length ord_37(2)=36: this is an exact irreducibility certificate.
        order_two = next(j for j in range(1, 37) if pow(2, j, 37) == 1)
        require(order_two == 36 and 6 * 6 % 37 == 36, "Local Q(i) certificate failed")
        certificate["local_Qi_certificate"] = {
            "polynomial": "X^36-2 over F_37", "frobenius_identity": "X^37=2X",
            "multiplicative_order_of_2_mod_37": order_two,
            "irreducible": True, "sqrt_minus_one_mod_37": 6,
            "scope": "Inputs to the local valuation proof; no determinant expansion or sampling."}
    return certificate


def verify_spec(total, item):
    rows, d, q, p, source_name, pinned_hash = item
    path = HERE / f"norm_repair_{total}_degree{2*d}_20261106_v1.json.gz"
    raw, spec = load_gzip(path)
    source_raw, source = load_gzip(REPO / source_name)
    require(sha256(source_raw).hexdigest() == pinned_hash == spec["source_json_sha256"],
            "Pinned source hash mismatch")
    require(spec["source_file"] == source_name, "Wrong source path")
    for key, old in (("variables", "variables"), ("fixed_constants", "fixed_constants"),
                     ("quadratic_residuals", "residuals")):
        require(spec[key] == source[old], "Copied source table differs: " + key)
    require(len(spec["variables"]) == total and [v["index"] for v in spec["variables"]] == list(range(total)),
            "Variable list is not consecutive")
    require(spec["total_variables"] == total and spec["existential_witnesses"] == total - 1,
            "Incorrect coordinate count")
    residuals = spec["quadratic_residuals"]
    require(len(residuals) == rows <= d * d, "Incorrect residual count")
    input_terms = []
    for ri, row in enumerate(residuals):
        seen = set()
        for monomial, kp, coefficient in row["terms"]:
            require(len(monomial) <= 2 and monomial == sorted(monomial)
                    and all(type(v) is int and 0 <= v < total for v in monomial), "Invalid monomial")
            require(type(kp) is int and kp in (0, 1) and type(coefficient) is int and coefficient != 0,
                    "Invalid coefficient or fixed-constant exponent")
            key = (tuple(monomial), kp)
            require(key not in seen, "Duplicate residual monomial")
            seen.add(key)
            if 0 in monomial:
                input_terms.append((ri, monomial, kp, coefficient))
    require(input_terms == [(0, [0, 0], 0, 1)], "Input leading-term argument failed")
    require(spec["exact_degree"] == 2 * d and spec["leading_input_coefficient"] == 1,
            "Incorrect exact degree or input coefficient")
    M = max(sum(abs(c) for _, _, c in row["terms"]) for row in residuals)
    kdegree = max(k for row in residuals for _, k, _ in row["terms"])
    require(spec["fixed_constants"] == ({"K": "3^(2^28)"} if kdegree else {}), "Wrong fixed integer")
    # 3^5<2^8 gives log2(kappa)<(8/5)2^28.
    require(3 ** 5 < 2 ** 8, "Fixed-integer logarithm bound failed")
    kbits = ((8 * 2 ** 28 + 4) // 5) if kdegree else 0
    norm_certificate = verify_norm(spec["norm_construction"], d, q, p)
    height = norm_certificate["coefficient_l1_bound_log2_ceiling"] + d * (clog(M) + kbits)
    require((spec["residual_coefficient_l1_bound"], spec["residual_kappa_degree"],
             spec["kappa_log2_upper_bound"], spec["coefficient_height_bound_power_of_two_exponent"])
            == (M, kdegree, kbits, height), "Height arithmetic differs")
    return {"file": str(path.relative_to(REPO)), "uncompressed_sha256": sha256(raw).hexdigest(),
            "source_json_sha256": pinned_hash, "total_variables": total, "residuals_compared": rows,
            "source_terms_compared": sum(len(r["terms"]) for r in residuals),
            "exact_degree": 2 * d, "leading_input_coefficient": 1,
            "height_bound_power_of_two_exponent": height, "residual_l1_log2_ceiling": clog(M),
            "norm_certificate": norm_certificate}


def verify_field_bound(name, expected):
    raw = (REPO / name / "polynomial-specification.json").read_bytes()
    spec = json.loads(raw)
    bd = spec["bounds"]
    rel = spec["monic_relations"]
    ws, logs = bd["generator_weights"], bd["generator_operator_log2_norm_bounds"]
    require(len(rel) == len(ws) == len(logs), "Wrong generator-bound lengths")
    estimates, dependencies = [], []
    nodes = spec["coefficient_dag"]
    for idx, (op, *a) in enumerate(nodes):
        deps = set()
        if op == "int": value = (0, clog(abs(a[0])))
        elif op == "variable":
            require(0 <= a[0] < spec["retained_base_variables"], "Non-base variable in coefficient DAG")
            value = (1, 0)
        elif op == "parameter":
            require(all(type(x) is int and abs(x) <= a[1] for x in spec["source_finite_parameters"][a[0]]),
                    "Parameter bound understated")
            value = (0, clog(a[1]))
        elif op == "algebra_generator":
            value = (ws[a[0]], logs[a[0]]); deps = {a[0]}
        else:
            refs = a[:1] if op in ("pow", "neg") else a
            require(all(type(j) is int and 0 <= j < idx for j in refs), "Not a forward DAG")
            deps = set().union(*(dependencies[j] for j in refs))
            if op == "neg": value = estimates[a[0]]
            elif op == "pow":
                require(type(a[1]) is int and a[1] >= 0, "Nonpolynomial power in coefficient DAG")
                value = tuple(a[1] * x for x in estimates[a[0]])
            elif op == "mul": value = tuple(sum(estimates[j][k] for j in a) for k in (0, 1))
            elif op == "add": value = (max(estimates[j][0] for j in a), max(estimates[j][1] for j in a) + clog(len(a)))
            else: raise AssertionError("Unknown DAG operation " + op)
        estimates.append(value); dependencies.append(deps)
    for i, relation in enumerate(rel):
        degree = relation["maximum_degree"]
        require((relation["kind"], degree) in (("point", 4), ("quadratic", 2)), "Unknown relation")
        nz = [(k, node) for k, node in enumerate(relation["coefficient_nodes_ascending"]) if nodes[node] != ["int", 0]]
        require(all(all(j < i for j in dependencies[node]) for _, node in nz), "Nontriangular relation")
        require(all(estimates[node][0] + k * ws[i] <= degree * ws[i] for k, node in nz),
                "Weighted degree can increase on reduction")
        require(logs[i] >= max([0] + [estimates[node][1] for _, node in nz]) + clog(max(1, len(nz))),
                "Companion-operator norm bound understated")
    types = Counter(r["kind"] for r in rel)
    points, quadratics, m = types["point"], types["quadratic"], len(rel)
    n = prod(r["maximum_degree"] for r in rel)
    rank_exp = 2 * points + quadratics
    require(n == 2 ** rank_exp == bd["maximum_rank"], "Rank mismatch")
    weights = sum((r["maximum_degree"] - 1) * ws[i] for i, r in enumerate(rel))
    wg, bg = estimates[spec["materialized_guard_node"]]
    wg += sum(ws[i] for i, r in enumerate(rel) if r["kind"] == "quadratic")
    bg += sum(logs[i] for i, r in enumerate(rel) if r["kind"] == "quadratic")
    residual_nodes = [e["numerator"] for e in spec["closed_equations"]]
    residual_nodes += [r["coefficient_nodes_ascending"][0] for r in rel if r["kind"] == "quadratic"]
    we, be = (max([0] + [estimates[j][k] for j in residual_nodes]) for k in (0, 1))
    c = len(residual_nodes)
    params = prod(len(v) for v in spec["source_finite_parameters"].values())
    count = 0
    # Count every rank/selector/degree case directly, grouped only by mask weight.
    for k in range(quadratics + 1):
        rank = 4 ** points * 2 ** k
        count += params * comb(quadratics, k) * rank * (1 + m * rank * (rank + 1) // 2)
    selector = m * n * (n + 1) // 2
    blambda = clog(m + 1) + max((i + 1) * clog(selector) + bits for i, bits in enumerate(logs))
    aggregates = {"maximum_basis_weight": weights, "materialized_guard_weight": wg,
                  "materialized_guard_operator_log2_norm_bound": bg,
                  "closed_residual_maximum_weight": we, "closed_residual_maximum_operator_log2_norm_bound": be,
                  "closed_residual_count": c, "maximum_selector": selector,
                  "selector_operator_log2_norm_bound": blambda,
                  "source_parameter_branches": params, "exact_number_of_final_factors": count}
    require(all(bd[k] == v for k, v in aggregates.items()), "Aggregate compiler bound mismatch")
    residual_number = n + c
    d = isqrt(residual_number)
    if d * d < residual_number: d += 1
    require((d - 1) ** 2 < residual_number <= d ** 2, "Wrong ceiling square root")
    if not spec["indexed_guard_polynomials"]:
        alpha = wg + max(ws) + weights
        AH = n * alpha
        AR = (n - 1) * alpha + we + weights
        AL = (2 * n + 2) * AH
        residual_degree = max(AH, n * (AL + 1), AR + (n - 1) * (AL + 1))
        require(bd["operator_entry_degree"] == alpha and bd["H_coefficient_degree"] == AH
                and bd["trace_coefficient_degree"] == AR and bd["scale_degree"] == AL
                and bd["branch_degree_bound"] == 2 * residual_degree
                and bd["degree_bound"] == count * 2 * residual_degree, "Unrounded branch degree differs")
        majorant = count * d * residual_degree
        exponent = clog(majorant)
        detail = {"residual_degree_bound": residual_degree, "exact_degree_majorant": majorant,
                  "rounding_slack_numerator": 2 ** exponent - majorant,
                  "rounding_slack_denominator": 2 ** exponent}
    else:
        macro_e = []
        for macro, certificate in zip(spec["indexed_guard_polynomials"], bd["indexed_guard_bounds"]):
            require(macro["index_first"] == 1 and macro["index_last"]["base"] == 2,
                    "Unexpected indexed guard")
            w = max(estimates[macro[k]][0] for k in ("N0", "N1", "D"))
            e = 1 + macro["index_last"]["exponent"] + clog(max(1, w))
            require(certificate["coordinate_weight_bound"] == w
                    and certificate["weight_bound_power_of_two_exponent"] == e,
                    "Indexed degree bound mismatch")
            macro_e.append(e)
        eg = max([clog(wg)] + macro_e) + clog(1 + len(macro_e))
        ea = max(eg, clog(max(ws) + weights)) + 1
        eAH = rank_exp + ea
        eAR = max(rank_exp + ea, clog(we + weights)) + 1
        eAL = rank_exp + 2 + eAH
        ePsi = rank_exp + eAL + 1
        eTrace = max(eAR, rank_exp + eAL + 1) + 1
        eResidual = max(eAH, ePsi, eTrace)
        powers = bd["power_envelopes"]
        require(all(powers[key] == value for key, value in {
            "guard_weight": eg, "operator_entry_degree": ea, "H_coefficient_degree": eAH,
            "trace_coefficient_degree": eAR, "scale_degree": eAL,
            "reciprocal_degree": ePsi, "reversed_trace_degree": eTrace,
            "branch_degree": eResidual + 1}.items()), "Power-envelope degree mismatch")
        multiplier = d * count
        multiplier_bits = clog(multiplier)
        exponent = eResidual + multiplier_bits
        detail = {"residual_degree_bound_power_of_two_exponent": eResidual,
                  "exact_final_multiplier": multiplier, "multiplier_log2_ceiling": multiplier_bits,
                  "rounding_slack_numerator": 2 ** multiplier_bits - multiplier,
                  "rounding_slack_denominator": 2 ** multiplier_bits}
    require((spec["total_external_variables"], exponent) == expected, "Final field bound differs")
    return {"source": name, "source_specification_sha256": sha256(raw).hexdigest(),
            "total_variables": expected[0], "coefficient_dag_nodes_checked": len(nodes),
            "maximum_rank": n, "closed_residual_bound": c, "maximum_branch_residuals": residual_number,
            "combining_norm_degree": d, "exact_number_of_final_factors": count,
            "degree_bound_power_of_two_exponent_over_K": exponent, "unrounded_details": detail}


def main():
    repairs = [verify_spec(n, item) for n, item in PINNED.items()]
    fields = [verify_field_bound(name, item) for name, item in FIELD_SOURCES.items()]
    producer_report_path = HERE / "division-norm-construction_20261106_v1.json"
    producer_report = json.loads(producer_report_path.read_text())
    reported = {r["source"]: r for r in producer_report["field_adapted_finite_algebra_bounds"]}
    for row in fields:
        require(all(row[k] == v for k, v in reported[row["source"]].items()), "Producer summary differs")
    receipt = {"status": "PASS", "checker": Path(__file__).name,
               "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "imports_producer": False, "randomized_checks": False,
               "scope": "Exact residual correspondence, finite cyclic-norm data, formal matrix conjugacy, input degree, coefficient-height bounds, and finite-algebra degree bounds. No norm expansion and no arithmetic Z-definition proof.",
               "proof_review": "division_norm_independent_proof_review_20261106_v1.tex",
               "norm_repairs": repairs, "field_compiler_bounds": fields}
    target = HERE / "division-norm-independent-verification_20261106_v1.json"
    target.write_text(json.dumps(receipt, indent=2) + "\n")
    print("PASS: four exact norm specifications and four field-compiler degree bounds.")
    print("Receipt:", target.relative_to(REPO))
    for row in repairs:
        print(row["total_variables"], "variables; degree", row["exact_degree"],
              "; height <= 2^" + str(row["height_bound_power_of_two_exponent"]))
    for row in fields:
        print(row["source"], ": degree <= 2^" + str(row["degree_bound_power_of_two_exponent_over_K"]))


if __name__ == "__main__":
    main()
