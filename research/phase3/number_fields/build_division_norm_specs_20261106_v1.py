#!/usr/bin/env python3
"""Specify exact degree-72 and degree-74 cyclic-norm repairs of quartics.

The 37 by 37 determinant is explicit; its full monomial expansion is not
materialized.  Cyclotomic coefficient extraction eliminates the coefficient
symbol and introduces no quantified coordinate.  Only the standard library
is used.  No phase-two file is changed.
"""
import gzip
import hashlib
import json
from math import factorial, isqrt
from pathlib import Path


def is_prime(n):
    return n >= 2 and all(n % p for p in range(2, isqrt(n)+1))


def clog(n):
    return (n-1).bit_length() if n else 0


def prime_factors(n):
    return [p for p in range(2, n+1) if n % p == 0 and is_prime(p)]


def norm_data(d, q, p):
    assert is_prime(q) and is_prime(p) and (q-1) % d == 0
    g = next(a for a in range(2, q) if all(pow(a, (q-1)//r, q) != 1 for r in prime_factors(q-1)))
    H = sorted(pow(g, d*j, q) for j in range((q-1)//d))
    periods = [sorted(pow(g, i, q)*h % q for h in H) for i in range(d)]
    assert sorted(x for period in periods for x in period) == list(range(1, q))
    assert all(pow(p, (q-1)//r, q) != 1 for r in prime_factors(d))
    return {
        "cyclic_degree": d, "conductor_prime": q, "cyclic_parameter_prime": p,
        "primitive_root": g, "cyclotomic_modulus_coefficients_ascending": [1]*q,
        "period_exponents": periods,
        "coefficient_basis": f"beta_0=1; beta_i=sum(zeta^a for a in period_exponents[i]), 1<=i<{d}",
        "matrix_entries": [{"row": r, "column": c, "scale": p if r > c else 1,
                            "residual_block": (c-r) % d, "period_shift": r}
                           for r in range(d) for c in range(d)],
        "matrix_entry_rule": f"scale*(F[{d}*block]+sum_{{i=1}}^{{{d-1}}}(sum_{{a in period_exponents[(i+period_shift)%{d}]}}zeta^a)*F[{d}*block+i]); pad F by zero to length{d*d}",
        "polynomial": f"coefficient_zeta^0 of determinant(matrix), reduced modulo 1+zeta+...+zeta^{q-1}",
        "rationality_certificate": f"Applying zeta->zeta^g conjugates the matrix by U, where Ue_j=e_{{j-1}} and Ue_0={p}e_{d-1}; therefore the determinant has rational integer coefficients.",
        "norm_degree": d, "norm_coefficient_l1_bound": factorial(d)*((q-1)*p)**d,
        "field_scope": (f"Anisotropic over every number field K with gcd({d},[K:Q])=1, and over Q(i). Arbitrary K uses field-dependent primes as proved in division_norm_compiler_20261106_v1.tex."),
    }


def compile_one(path, output, norm):
    raw = gzip.decompress(path.read_bytes())
    source = json.loads(raw)
    residuals = source["residuals"]
    d = norm["cyclic_degree"]
    assert len(residuals) <= d*d
    assert all(len(m) <= 2 for row in residuals for m, _, _ in row["terms"])
    assert [(ri, m, k, c) for ri, row in enumerate(residuals) for m, k, c in row["terms"] if 0 in m] == [(0, [0, 0], 0, 1)]
    M = max(sum(abs(c) for _, _, c in row["terms"]) for row in residuals)
    kdegree = max(k for row in residuals for _, k, _ in row["terms"])
    assert kdegree in (0, 1)
    kbits = (8*2**28+4)//5 if kdegree else 0
    height_bits = clog(norm["norm_coefficient_l1_bound"])+d*(clog(M)+kdegree*kbits)
    spec = {
        "format": "integer-polynomial-cyclic-norm/v1", "source_json_sha256": hashlib.sha256(raw).hexdigest(),
        "source_file": str(path.relative_to(Path(__file__).resolve().parents[3])), "variables": source["variables"], "fixed_constants": source["fixed_constants"],
        "quadratic_residuals": residuals, "norm_construction": norm,
        "total_variables": len(source["variables"]), "existential_witnesses": len(source["variables"])-1,
        "exact_degree": 2*d, "leading_input_coefficient": 1,
        "coefficient_height_bound_power_of_two_exponent": height_bits,
        "residual_coefficient_l1_bound": M, "residual_kappa_degree": kdegree,
        "kappa_log2_upper_bound": kbits,
        "equivalence": "Over fields where the specified cyclic algebra remains division, the polynomial vanishes exactly when every recorded quadratic residual vanishes.",
        "arithmetic_scope": "No assertion that the base-changed quadratic system defines the ring of integers of K is made.",
        "representation": f"Complete{d}x{d} indexed determinant and cyclotomic coefficient-extraction polynomial specification, with the complete residual coefficient tables. The expanded degree{2*d} coefficient table is not materialized. No cyclotomic symbol is quantified.",
    }
    encoded = (json.dumps(spec, separators=(",", ":"))+"\n").encode()
    output.write_bytes(gzip.compress(encoded, mtime=0))
    return {"file": str(output), "uncompressed_sha256": hashlib.sha256(encoded).hexdigest(),
            "source_json_sha256": spec["source_json_sha256"], "total_variables": spec["total_variables"],
            "residual_count": len(residuals), "exact_degree": 2*d, "leading_input_coefficient": 1,
            "coefficient_height_bound_power_of_two_exponent": height_bits,
            "residual_coefficient_l1_bound_power_of_two_exponent": clog(M)}


def field_degree_bounds(repo):
    paths = ["research/phase3/finite_fibre/polynomial-41", "research/phase3/finite_fibre/polynomial-43-semilocal",
             "research/phase2/finite_fibre/polynomial-43-conic", "research/phase2/finite_fibre/polynomial-45-conic-semilocal"]
    rows = []
    for name in paths:
        path = repo/name/"polynomial-specification.json"
        raw = path.read_bytes(); source = json.loads(raw); bd = source["bounds"]
        rank, closed = bd["maximum_rank"], bd["closed_residual_count"]
        r = rank+closed; d = isqrt(r)+(isqrt(r)**2 < r)
        if "degree_bound" in bd:
            assert bd["degree_bound"] % 2 == 0
            exponent = clog(d*(bd["degree_bound"]//2))
        else:
            exponent = bd["power_envelopes"]["branch_degree"]-1+clog(d*bd["exact_number_of_final_factors"])
        rows.append({"source": name, "source_specification_sha256": hashlib.sha256(raw).hexdigest(),
                     "total_variables": source["total_external_variables"], "maximum_rank": rank,
                     "closed_residual_bound": closed, "maximum_branch_residuals": r,
                     "combining_norm_degree": d, "degree_bound_power_of_two_exponent_over_K": exponent})
    return rows


def main():
    here = Path(__file__).resolve().parent; repo = here.parents[2]
    norm = norm_data(37, 149, 5)
    norm36 = norm_data(36, 37, 2)
    rows = [compile_one(repo/"research/phase2/quartic/quartic-best/polynomial.json.gz",
                        here/"norm_repair_1367_degree74_20261106_v1.json.gz", norm),
            compile_one(repo/"research/phase2/quartic/quartic-small-coefficients/polynomial.json.gz",
                        here/"norm_repair_1391_degree74_20261106_v1.json.gz", norm),
            compile_one(repo/"research/phase3/quartic/quartic-direct/polynomial.json.gz",
                        here/"norm_repair_1315_degree72_20261106_v1.json.gz", norm36),
            compile_one(repo/"research/phase3/quartic/quartic-direct-small-coefficients/polynomial.json.gz",
                        here/"norm_repair_1339_degree72_20261106_v1.json.gz", norm36)]
    report = {"producer_assertions": "passed", "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "norm_forms": [{"cyclic_degree": n["cyclic_degree"], "conductor_prime": n["conductor_prime"],
                               "cyclic_parameter_prime": n["cyclic_parameter_prime"],
                               "norm_coefficient_l1_bound_power_of_two_exponent": clog(n["norm_coefficient_l1_bound"])}
                              for n in [norm36, norm]],
              "quartic_system_repairs": rows, "field_adapted_finite_algebra_bounds": field_degree_bounds(repo)}
    target = here/"division-norm-construction_20261106_v1.json"
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
