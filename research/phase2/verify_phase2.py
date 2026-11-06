#!/usr/bin/env python3
"""Run the exact checks for the five preferred polynomial specifications.

This script records the scope of each checker. It neither executes the
astronomically large indexed products nor proves the external arithmetic
inputs. It performs no network operation or git mutation.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PREFIX = [sys.executable, "-E", "-B"]
CHECKS = [
    ("source-structure", ["research/phase2/new_polynomials/check_source_structure.py"]),
    ("scalar-normalization", ["research/phase2/new_polynomials/verify_scalar_preparation_zero.py"]),
    ("conic-and-scale-identities", ["research/phase2/new_polynomials/check_degree_refinements.py"]),
    ("precision-52", ["research/phase2/new_polynomials/check_precision52.py"]),
    ("finite-algebra-small-execution", ["research/phase2/finite_fibre/small_algebra_interpreter.py"]),
    ("fixed-elliptic-anchor", ["research/phase2/finite_fibre/check_fixed_anchor_height.py"]),
    ("polynomial-558", ["research/phase2/finite_fibre/verify_558_specification.py"]),
    ("polynomial-43", [
        "research/phase2/finite_fibre/verify_shared_specification.py",
        "research/phase2/new_polynomials/source-43-conic.json.gz",
        "research/phase2/finite_fibre/polynomial-43-conic/polynomial-specification.json"]),
    ("polynomial-45", [
        "research/phase2/finite_fibre/verify_shared_specification.py",
        "research/phase2/new_polynomials/source-45-conic-semilocal.json.gz",
        "research/phase2/finite_fibre/polynomial-45-conic-semilocal/polynomial-specification.json"]),
    ("quartic-1367", [
        "research/phase2/quartic/verify_shared_quartic.py",
        "research/phase2/quartic/quartic-best/polynomial.json.gz"]),
    ("quartic-1391", [
        "research/phase2/quartic/verify_shared_quartic.py",
        "research/phase2/quartic/quartic-small-coefficients/polynomial.json.gz"]),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = HERE / "verification"
    logs = output / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    results = []
    for name, arguments in CHECKS:
        completed = subprocess.run(PREFIX + arguments, cwd=REPO, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = logs / (name + ".txt")
        log.write_text(completed.stdout)
        status = "PASS" if completed.returncode == 0 else "FAIL"
        results.append({
            "name": name, "status": status,
            "command_arguments": PREFIX + arguments,
            "checker_sha256": digest(REPO / arguments[0]),
            "log": str(log.relative_to(REPO)), "log_sha256": digest(log),
            "exit_code": completed.returncode,
        })
        print(name + ": " + status, flush=True)
        if completed.returncode:
            break
    receipt = {
        "status": "PASS" if len(results) == len(CHECKS)
                  and all(x["status"] == "PASS" for x in results) else "FAIL",
        "baseline_revision": "28e87b1b62af0effd954605af7f70b2699dd5672",
        "scope": (
            "Exact source specification, rational-square clearing, finite-case, "
            "coefficient-table and numerical-bound checks, plus complete execution "
            "of the finite-algebra construction on eight small examples. "
            "External arithmetic theorems, the full large indexed matrices/products, "
            "and global minimality are not certified by these computations."
        ),
        "checks": results,
    }
    target = output / "all-checks.json"
    target.write_text(json.dumps(receipt, indent=2) + "\n")
    print(str(target.relative_to(REPO)) + ": " + receipt["status"])
    if receipt["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
