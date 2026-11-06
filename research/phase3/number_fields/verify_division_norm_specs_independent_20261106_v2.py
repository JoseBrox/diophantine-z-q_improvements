#!/usr/bin/env python3
"""Independent audit of norm specifications for the final quartic sources.

Reuses only the previously independent finite cyclic-matrix verifier.
No construction producer is imported.  Complete source residuals and
the improved fixed-S coefficient estimate are checked exactly.
"""
from hashlib import sha256
from pathlib import Path
import gzip
import json

from verify_division_norm_specs_independent_20261106_v1 import verify_norm, require, clog


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCES = [
    ("norm_repair_1315_translated_degree72_20261106_v2.json.gz",
     "c2f74e460c5439a1a4e7e551bbc10760e1b3bfc1090795dce3308eae5355296a",
     "research/phase3/quartic/quartic-direct-translated/polynomial.json.gz",
     "54175d125631269040f8a207b7863f7f8f9331db92bb9d9e95bbf12cc15c1a10", 1315, 1272),
    ("norm_repair_1338_degree72_20261106_v2.json.gz",
     "422474ef93ad4768ddb4fab023ea227d4710b85314377e07def0abe5f073b604",
     "research/phase3/quartic/quartic-direct-small-coefficients-1338/polynomial.json.gz",
     "69a280afdd6a98f6b13ac3b9455baf36b92cc3bd203d7664860269004baab0a8", 1338, 1295),
    ("norm_repair_1335_degree72_20261106_v2.json.gz",
     "e770ece4a695b492b79b1da90bc398f9c401c62f67e84ff20ebb4267d8fdfcd2",
     "research/phase3/quartic/quartic-direct-small-coefficients-1335/polynomial.json.gz",
     "047ebb380d58179785ebe2d2e12c34e02594c01dab07afe242a80aa7455fd2b4", 1335, 1292),
]


def audit(item):
    name, expected, source_path, source_hash, total, rows = item
    raw = gzip.decompress((HERE / name).read_bytes())
    require(sha256(raw).hexdigest() == expected, "Norm artifact changed")
    spec = json.loads(raw)
    parent_raw = gzip.decompress((REPO / source_path).read_bytes())
    require(sha256(parent_raw).hexdigest() == source_hash == spec["source_json_sha256"], "Source hash mismatch")
    source = json.loads(parent_raw)
    require(spec["source_file"] == source_path, "Source path mismatch")
    for new_key, old_key in (("variables", "variables"), ("fixed_constants", "fixed_constants"),
                              ("quadratic_residuals", "residuals")):
        require(spec[new_key] == source[old_key], "Full source copy mismatch: " + new_key)
    require(len(spec["variables"]) == total == spec["total_variables"]
            and spec["existential_witnesses"] == total - 1, "Wrong variable count")
    residuals = spec["quadratic_residuals"]
    require(len(residuals) == rows <= 1296, "Wrong residual count")
    require(all(len(m) <= 2 and type(k) is int and k >= 0 and type(c) is int
                for row in residuals for m, k, c in row["terms"]), "Not integral quadratic residuals")
    input_terms = [(r, m, k, c) for r, row in enumerate(residuals)
                   for m, k, c in row["terms"] if 0 in m]
    require(input_terms == [(0, [0, 0], 0, 1)], "Input-leading-coefficient argument failed")
    require(spec["exact_degree"] == 72 and spec["leading_input_coefficient"] == 1,
            "Wrong exact degree or primitive coefficient")
    norm = verify_norm(spec["norm_construction"], 36, 37, 2)
    A = norm["coefficient_l1_bound"]
    require(clog(A) == 361, "Wrong determinant norm exponent")
    constant_parts = [sum(abs(c) for m, k, c in row["terms"] if k == 0) for row in residuals]
    M = max(constant_parts)
    symbols = [[r, m, k, c] for r, row in enumerate(residuals) for m, k, c in row["terms"] if k != 0]
    cert = spec["coefficient_certificate"]
    if symbols:
        require(spec["fixed_constants"] == {"S": "3^(2^27)"}
                and symbols == [[46, [55], 1, 8]], "Wrong fixed-S dependence")
        require(M < 2 ** 511 and 2 ** 27 > 511, "Constant residual part need not be smaller than S")
        # Every row has coefficient norm < S+8S=9S=3^(2^27+2).
        numerator = 8 * (2 ** 27 + 2)
        require(3 ** 5 < 2 ** 8 and numerator % 5 == 0, "Improved logarithm estimate fails")
        residual_bits = numerator // 5
        require(residual_bits == 214748368, "Wrong residual exponent")
        require(cert["constant_part_maximum_l1_norm"] == M and cert["symbolic_terms"] == symbols
                and cert["residual_coefficient_log2_bound"] == residual_bits,
                "Symbolic coefficient certificate differs")
        require(cert["full_coefficient_norm_bound"] == {
            "integer_factor": A, "power_base": 3, "power_exponent": 36 * (2 ** 27 + 2)},
            "Wrong exact symbolic norm majorant")
    else:
        require(spec["fixed_constants"] == {}, "Unexpected fixed coefficient constant")
        residual_bits = clog(M)
        require(residual_bits == 511 and cert["residual_coefficient_l1_bound"] == M
                and cert["residual_coefficient_log2_bound"] == residual_bits
                and cert["determinant_coefficient_l1_bound"] == A, "Ordinary coefficient certificate differs")
    height_bits = 361 + 36 * residual_bits
    require(spec["coefficient_height_bound_power_of_two_exponent"] == height_bits, "Wrong final height exponent")
    return {"file": name, "uncompressed_sha256": expected, "source": source_path,
            "source_sha256": source_hash, "total_variables": total,
            "residuals_compared": rows, "source_terms_compared": sum(len(r["terms"]) for r in residuals),
            "exact_degree": 72, "leading_input_coefficient": 1,
            "residual_coefficient_log2_bound": residual_bits,
            "coefficient_height_bound_power_of_two_exponent": height_bits,
            "cyclic_matrix_certificate": norm}


def main():
    rows = [audit(item) for item in SOURCES]
    helper = HERE / "verify_division_norm_specs_independent_20261106_v1.py"
    receipt = {"status": "PASS", "checker": Path(__file__).name,
               "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "independent_helper": helper.name, "helper_sha256": sha256(helper.read_bytes()).hexdigest(),
               "imports_producer": False, "randomized_checks": False,
               "scope": "Complete residual correspondence, explicit cyclic matrix algebra, exact degree and primitive input coefficient, and improved coefficient-height bounds. The determinant is not expanded; source arithmetic is not independently established here.",
               "results": rows}
    out = HERE / "division-norm-independent-verification_20261106_v2.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print("PASS: final-source degree72 norm specifications.")
    for row in rows:
        print(row["total_variables"], "variables; coefficient height < 2^" + str(row["coefficient_height_bound_power_of_two_exponent"]))
    print("Receipt:", out.relative_to(REPO))


if __name__ == "__main__":
    main()
