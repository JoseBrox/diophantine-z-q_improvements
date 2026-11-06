#!/usr/bin/env python3
"""Bind the completed independent check receipts to the delivered artifact bytes.

This is an integrity index, not a replacement for the mathematical checkers.
The index does not rerun the preceding phases or expand any determinant.
"""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def digest(path, compressed=False):
    raw = path.read_bytes()
    if compressed:
        raw = gzip.decompress(raw)
    return hashlib.sha256(raw).hexdigest()


def receipt(path):
    data = json.loads(path.read_text())
    assert data["status"].lower() in ("pass", "passed"), path
    return data


def coordinate_monomials(path):
    data = json.loads(gzip.decompress(path.read_bytes()))
    grouped = {}
    for monomial, k_power, coefficient in data["expanded_polynomial"]:
        terms = grouped.setdefault(tuple(monomial), {})
        assert k_power not in terms
        assert coefficient != 0
        terms[k_power] = coefficient
    overlaps = []
    for monomial, terms in grouped.items():
        if len(terms) == 1:
            continue  # Nonzero integer times a power of the positive fixed constant.
        if not monomial:
            assert set(terms) == {0, 2} and terms[0] > 0 and terms[2] == 1024
            overlaps.append("positive constant plus 1024*kappa^2")
        else:
            assert terms == {0: 1, 1: -192}
            overlaps.append("1-192*kappa, nonzero for the fixed positive integer kappa")
    if data["fixed_constants"]:
        assert len(overlaps) == 4
    else:
        assert not overlaps
    return {"file": str(path.relative_to(REPO)),
            "encoded_entries": len(data["expanded_polynomial"]),
            "coordinate_monomials": len(grouped), "no_specialization_cancellation": True,
            "overlapping_coefficients": overlaps}


def main():
    indexed = []
    pairs = [
        ("source-41-direct.json.gz", "polynomial-41"),
        ("source-43-direct-semilocal.json.gz", "polynomial-43-semilocal"),
        ("source-41-shift2402.json.gz", "polynomial-41-shift2402"),
        ("source-43-semilocal-shift2402.json.gz", "polynomial-43-semilocal-shift2402"),
    ]
    generic = REPO / "research/phase2/finite_fibre/verify_shared_specification.py"
    for source, package in pairs:
        source_path = HERE / "compression" / source
        package_path = HERE / "finite_fibre" / package
        check = receipt(package_path / "verification.json")
        assert digest(source_path, True) == check["source_json_sha256"]
        assert digest(package_path / "polynomial-specification.json") == check["specification_sha256"]
        assert digest(generic) == check["checker_sha256"]
        indexed.append({"package": package, "source": source,
                        "total_variables": check["external_variables"],
                        "degree_bound_exponent": check["degree_bound_power_of_two_exponent"],
                        "source_sha256": check["source_json_sha256"],
                        "specification_sha256": check["specification_sha256"]})
    quartics = []
    for package in ("quartic-direct", "quartic-direct-small-coefficients"):
        base = HERE / "quartic" / package
        check = receipt(base / "verification.json")
        assert digest(base / "polynomial.json.gz", True) == check["uncompressed_sha256"]
        quartics.append({"package": package, "total_variables": check["total_variables"],
                         "degree": check["degree"], "uncompressed_sha256": check["uncompressed_sha256"]})
    transformed_check = receipt(HERE / "quartic/final-transforms-independent-verification.json")
    assert digest(HERE / "quartic" / transformed_check["checker"]) == transformed_check["checker_sha256"]
    assert len(transformed_check["results"]) == 3
    for entry in transformed_check["results"]:
        path = HERE / "quartic" / entry["artifact"] / "polynomial.json.gz"
        assert digest(path, True) == entry["sha256"]
        quartics.append({"package": entry["artifact"], "total_variables": entry["total_variables"],
                         "degree": entry["exact_degree"], "uncompressed_sha256": entry["sha256"]})
    norm_path = HERE / "number_fields/division-norm-independent-verification_20261106_v1.json"
    norm_check = receipt(norm_path)
    assert digest(HERE / "number_fields" / norm_check["checker"]) == norm_check["checker_sha256"]
    norms = []
    for entry in norm_check["norm_repairs"]:
        assert digest(REPO / entry["file"], True) == entry["uncompressed_sha256"]
        norms.append({k: entry[k] for k in ("file", "total_variables", "exact_degree", "uncompressed_sha256")})
    norm_v2 = receipt(HERE / "number_fields/division-norm-independent-verification_20261106_v2.json")
    assert digest(HERE / "number_fields" / norm_v2["checker"]) == norm_v2["checker_sha256"]
    assert digest(HERE / "number_fields" / norm_v2["independent_helper"]) == norm_v2["helper_sha256"]
    assert len(norm_v2["results"]) == 3
    for entry in norm_v2["results"]:
        assert digest(HERE / "number_fields" / entry["file"], True) == entry["uncompressed_sha256"]
        assert digest(REPO / entry["source"], True) == entry["source_sha256"]
        norms.append({k: entry[k] for k in ("file", "total_variables", "exact_degree", "uncompressed_sha256")})
    collected_counts = [coordinate_monomials(REPO / p) for p in (
        "research/phase3/quartic/quartic-direct/polynomial.json.gz",
        "research/phase3/quartic/quartic-direct-small-coefficients/polynomial.json.gz",
        "research/phase2/quartic/quartic-best/polynomial.json.gz",
        "research/phase2/quartic/quartic-small-coefficients/polynomial.json.gz")]
    paths = [
        "compression/direct-source-check.json",
        "compression/fixed-coefficient-support-check.json",
        "quartic/final-transforms-independent-verification.json",
        "number_fields/contact-exclusions-verification_20261106_v1.json",
        "number_fields/quartic-base-change-verification_20261106_v1.json",
        "number_fields/real-anchor-verification_20261106_v1.json",
        "number_fields/division-norm-independent-verification_20261106_v1.json",
        "number_fields/division-norm-independent-verification_20261106_v2.json",
        "number_fields/quartic-base-change-verification_20261106_v2.json",
        "paper-verification.json",
    ]
    receipts = []
    for name in paths:
        data = receipt(HERE / name)
        receipts.append({"file": name, "status": data["status"], "sha256": digest(HERE / name)})
    point_checks = []
    for name in ("compression/check_elliptic_density_data.py", "systems/check_point_depth_independent.py"):
        run = subprocess.run([sys.executable, "-E", "-B", str(HERE/name)],
                             cwd=REPO, check=True, text=True, capture_output=True)
        data = json.loads(run.stdout)
        assert data["status"].lower() in ("pass", "passed")
        point_checks.append({"script": name, "sha256": digest(HERE/name), "result": data})
    paper = receipt(HERE / "paper-verification.json")
    assert digest(HERE / paper["paper"]) == paper["sha256"]
    assert digest(REPO / "research/optimization/diophantine_optimization.tex") == paper["preceding_paper_sha256"]
    original_sha = digest(REPO / "quartic_12504.tex")
    assert original_sha == "38d458ba4178083766c5ae56a894da595fe27170c1ef07f6b49750fc5edf7c37"
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    assert revision == "28e87b1b62af0effd954605af7f70b2699dd5672"
    result = {
        "status": "PASS", "scope": "Integrity index for completed checks; source and formula hashes validated, two independent fixed-point computations replayed; no external arithmetic theorem certified",
        "pinned_revision": revision, "pinned_manuscript_sha256": original_sha,
        "indexed_polynomials": indexed, "expanded_quartics": quartics,
        "division_norm_specifications": norms, "other_receipts": receipts,
        "collected_coordinate_monomials": collected_counts,
        "fixed_point_checks": point_checks,
        "proof_reviews": ["compression/proof-review.json", "systems/independent_compression_review.md",
                          "number_fields/division_norm_independent_proof_review_20261106_v1.tex"],
        "paper_sha256": paper["sha256"], "tex_rendered": False,
        "arithmetic_hypotheses": "The Z over Q interpretations remain conditional on the named source arithmetic lemmas and Sun Theorem 4.1; no general O_K definition is established.",
        "commits_created": False, "pushes_or_pull_requests": False,
    }
    (HERE / "verification-index.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "indexed_polynomials": len(indexed),
                      "quartics": len(quartics), "norm_specifications": len(norms),
                      "fixed_point_checks": len(point_checks), "paper_sha256": paper["sha256"]}, indent=2))


if __name__ == "__main__":
    main()
