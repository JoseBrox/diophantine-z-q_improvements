#!/usr/bin/env python3
"""Check a quartic optimization relative to the frozen 12,504-variable artifact.

This checker imports no producer or polynomial-arithmetic code. It checks only
the additional operations, starting from SHA-256-pinned parent residuals. The
unchanged parent's full certificate can optionally be checked as well.

Every new operation must be either an invertible constant row operation or
elimination of a variable by an equation with a nonzero constant coefficient.
All occurrences are found by scanning the complete current system. Substitution
uses exact fractions, and row equality is checked up to an explicitly nonzero
rational scalar. No coefficient-size threshold is used as a proof premise.

The result establishes equality of rational input projections to the parent
artifact. It does not establish the source system's characterization of Z.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[2]
PARENT_RELATIVE = Path("quartics/quartic-12504")
PARENT_COMMIT = "28e87b1b62af0effd954605af7f70b2699dd5672"
PINNED_PARENT = {
    "candidate-rows.json.gz": "ff5412848dff46ac6ea0328244930b66c0a51c365e2b133bbafc7f2c86ca4b9e",
    "certificate.jsonl.gz": "9f7979c1e786bebad624b9ea4631b7eccd879f4bebb5b9ab69250b945973b268",
    "verify_certificate.py": "d2079177a4960740c5b7d42fbd0756dfc4ce8953cc947cee91c8786ba26fa8ba",
    "verification.json": "06424ae5fcd9de6d2e5674bf7927c665ed1096a85dde463d456feaadc352a400",
    "source-residuals.jsonl.gz": "ce9eeac7c4730aced8cfb70a1ab3b1b6a7fb2110c597afad1f56ddc92aeea73f",
    "variable-map.json": "de0cc5ffa613b60a3b10af4f4aa9033e09516c6fe4403dc7f0b58675e8e30b97",
    "residuals.json.gz": "dd72c6830df6bfc8452d89ebccbe6a51c350f722fd50a4ecf1f294f81b25196e",
    "weights.json": "ae4342eaf01218bcc041aeda1960aca923b3f9089dd29cdfa62162ae3c7ba1bd",
    "polynomial.expanded.txt": "7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca",
}


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_bytes(path):
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def read_json(path):
    return json.loads(read_bytes(path))


def read_records(path):
    return [json.loads(line) for line in read_bytes(path).splitlines()]


def decode(terms, allocated):
    require(type(terms) is list, "A polynomial must be a list of terms")
    answer = {}
    for term in terms:
        require(type(term) is list and len(term) == 2, "Invalid term")
        coefficient, indices = term
        require(type(coefficient) is int and coefficient != 0,
                "A coefficient must be a nonzero integer")
        require(type(indices) is list and all(
            type(v) is int and 0 <= v < allocated for v in indices),
            "Invalid variable index")
        monomial = tuple(indices)
        require(monomial == tuple(sorted(monomial)), "Unsorted monomial")
        require(monomial not in answer, "Repeated monomial")
        require(len(monomial) <= 2, "A residual exceeds degree two")
        answer[monomial] = coefficient
    return answer


def add(left, right, left_scale=1, right_scale=1):
    answer = {m: left_scale*c for m, c in left.items()}
    for m, c in right.items():
        answer[m] = answer.get(m, 0) + right_scale*c
    return {m: c for m, c in answer.items() if c}


def multiply(left, right):
    answer = {}
    for m, c in left.items():
        for n, d in right.items():
            term = tuple(sorted(m+n))
            answer[term] = answer.get(term, 0) + c*d
    return {m: c for m, c in answer.items() if c}


def substitute(polynomial, variable, numerator, denominator):
    """Literal symbolic substitution over Q; no producer normalization."""
    replacement = {m: Fraction(c, denominator) for m, c in numerator.items()}
    answer = {}
    for monomial, coefficient in polynomial.items():
        term = {(): Fraction(coefficient)}
        for v in monomial:
            term = multiply(term, replacement if v == variable else {(v,): 1})
        answer = add(answer, term)
    return answer


def proportional(actual, expected, context):
    """Return the nonzero scalar actual/expected, or reject."""
    if not expected:
        require(not actual, context + ": nonzero replacement for a zero row")
        return None
    require(actual.keys() == expected.keys(), context + ": monomial support differs")
    first = min(expected)
    scalar = Fraction(actual[first]) / expected[first]
    require(scalar != 0, context + ": zero row multiplier")
    require(all(Fraction(actual[m]) == scalar*c for m, c in expected.items()),
            context + ": coefficients are not proportional")
    return scalar


def variables(rows):
    return {v for row in rows for monomial in row for v in monomial}


def index(value, count, name):
    require(type(value) is int and 0 <= value < count, "Invalid " + name)
    return value


def apply_event(rows, event, allocated, event_index):
    context = "Event " + str(event_index)
    require(set(event) == {"kind", "data", "patches"}, context + ": unexpected keys")
    data = event["data"]
    require(type(data) is dict, context + ": invalid data")
    supplied = {}
    for patch in event["patches"]:
        require(type(patch) is list and len(patch) == 2, context + ": invalid patch")
        i = index(patch[0], len(rows), "patch row")
        require(i not in supplied, context + ": duplicate patch")
        supplied[i] = decode(patch[1], allocated)

    kind = event["kind"]
    if kind == "linear":
        require(set(data) == {"target", "other", "a", "b"},
                context + ": unexpected row-operation data")
        i = index(data["target"], len(rows), "target row")
        j = index(data["other"], len(rows), "other row")
        a, b = data["a"], data["b"]
        require(i != j, context + ": target and retained row coincide")
        require(type(a) is int and a != 0 and type(b) is int,
                context + ": row operation is not invertible over Q")
        expected = {i: add(rows[i], rows[j], a, b)}
        detail = {"kind": kind, "target": i, "other": j, "a": a, "b": b}
    elif kind == "eliminate":
        require(set(data) in (
            {"row", "variable", "replacement", "denominator", "affected"},
            {"row", "variable", "replacement", "denominator", "affected", "variable_search"}),
            context + ": unexpected elimination data")
        i = index(data["row"], len(rows), "pivot row")
        v = index(data["variable"], allocated, "eliminated variable")
        require(v != 0, context + ": input elimination is forbidden")
        denominator = data["denominator"]
        require(type(denominator) is int and denominator > 0,
                context + ": denominator is not a nonzero rational constant")
        numerator = decode(data["replacement"], allocated)
        require(v not in variables([numerator]), context + ": circular substitution")
        pivot_equation = add({(v,): denominator}, numerator, 1, -1)
        proportional(rows[i], pivot_equation, context + " pivot equation")

        # Deliberately recompute all occurrences, without trusting a maintained
        # incidence index or the certificate's affected-row list.
        affected = [j for j, row in enumerate(rows) if j != i
                    and any(v in monomial for monomial in row)]
        require(data["affected"] == affected,
                context + ": affected rows do not list every occurrence")
        expected = {j: substitute(rows[j], v, numerator, denominator) for j in affected}
        expected[i] = {}
        detail = {"kind": kind, "row": i, "variable": v,
                  "denominator": denominator, "affected_rows": len(affected),
                  "replacement_degree": max(map(len, numerator), default=0)}
    else:
        raise VerificationError(context + ": unsupported extra operation " + str(kind))

    require(supplied.keys() == expected.keys(), context + ": incomplete or extraneous patches")
    for i, polynomial in expected.items():
        proportional(supplied[i], polynomial, context + " row " + str(i))
    for i, polynomial in supplied.items():
        rows[i] = polynomial
    if kind == "eliminate":
        require(v not in variables(rows), context + ": eliminated variable remains")
    detail["certificate_record"] = event_index
    detail["checked_patches"] = len(supplied)
    return detail


def expanded_sum(rows, weights):
    """Ordered-pair multiplication, independent of the producer's square loop."""
    result = {}
    for row, weight in zip(rows, weights):
        for left, a in row.items():
            for right, b in row.items():
                monomial = tuple(sorted(left+right))
                result[monomial] = result.get(monomial, 0) + weight*a*b
    return {m: c for m, c in result.items() if c}


def verify(candidate, check_parent=False):
    parent = REPO / PARENT_RELATIVE
    for name, expected in PINNED_PARENT.items():
        require(sha((parent/name).read_bytes()) == expected, "Frozen parent changed: " + name)

    if check_parent:
        spec = importlib.util.spec_from_file_location("unchanged_parent_checker", parent/"verify_certificate.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.verify(parent, write_report=False)

    old_records = read_records(parent/"certificate.jsonl.gz")
    require(old_records[-2]["kind"] == "weights" and old_records[-1]["kind"] == "final",
            "Invalid frozen parent trailer")
    prefix = old_records[:-2]
    require(len(prefix) == 1468, "Unexpected frozen parent prefix length")
    allocated = old_records[-1]["allocated_variables"]
    old_raw = read_bytes(parent/"candidate-rows.json.gz")
    require(sha(old_raw) == old_records[-1]["rows_sha256"], "Parent row digest mismatch")
    rows = [decode(row, allocated) for row in json.loads(old_raw)]
    old_active = variables(rows)
    require(len(old_active) == 12504 and 0 in old_active, "Unexpected parent variable count")

    records = read_records(candidate/"certificate.jsonl.gz")
    require(len(records) >= len(prefix)+2 and records[:len(prefix)] == prefix,
            "Candidate does not extend the exact frozen parent certificate")
    require(records[-2]["kind"] == "weights" and records[-1]["kind"] == "final",
            "Invalid candidate trailer")
    require((candidate/"source-residuals.jsonl.gz").read_bytes()
            == (parent/"source-residuals.jsonl.gz").read_bytes(), "Source residuals changed")
    details = [apply_event(rows, record, allocated, i)
               for i, record in enumerate(records[len(prefix):-2], len(prefix))]

    final = records[-1]
    require(final["allocated_variables"] == allocated, "Unexpected variable allocation")
    candidate_raw = read_bytes(candidate/"candidate-rows.json.gz")
    require(sha(candidate_raw) == final["rows_sha256"], "Candidate row digest mismatch")
    saved_rows = [decode(row, allocated) for row in json.loads(candidate_raw)]
    require(rows == saved_rows, "Replayed residuals differ from saved candidate rows")
    full_weights = records[-2]["values"]
    require(len(full_weights) == len(rows) and all(type(w) is int and w > 0 for w in full_weights),
            "Weights must be positive integers, one per residual slot")

    active = variables(rows)
    permutation = read_json(candidate/"variable-map.json")
    require(type(permutation) is list and permutation and permutation[0] == 0,
            "Variable remapping does not preserve the distinguished input")
    require(all(type(v) is int for v in permutation) and len(permutation) == len(set(permutation)),
            "Invalid variable-remapping list")
    require(set(permutation) == active, "Variable remapping omits or adds coordinates")
    inverse = {old: new for new, old in enumerate(permutation)}
    compact = [{tuple(sorted(inverse[v] for v in m)): c for m, c in row.items()}
               for row in rows if row]
    weights = [w for row, w in zip(rows, full_weights) if row]
    require(read_json(candidate/"weights.json") == weights, "Compact weight list differs")
    require([decode(row, len(active)) for row in read_json(candidate/"residuals.json.gz")] == compact,
            "Stored compact residuals do not match the full variable remapping")

    polynomial = expanded_sum(compact, weights)
    expanded = (b"# coefficient followed by repeated variable indices; input is variable 0\n"
                + b"".join((" ".join(map(str, (c, *m)))+"\n").encode("ascii")
                            for m, c in sorted(polynomial.items())))
    require((candidate/"polynomial.expanded.txt").read_bytes() == expanded,
            "Expanded monomial table differs from the independently computed sum of squares")
    require(read_bytes(candidate/"polynomial.expanded.txt.gz") == expanded,
            "Compressed monomial table differs")
    require(variables([polynomial]) == set(range(len(active))),
            "Expanded polynomial has a different active-variable set")

    height = max(map(abs, polynomial.values()))
    stats = {"variables": len(active), "witnesses": len(active)-1,
             "rows": len(compact), "degree": max(map(len, polynomial)),
             "monomials": len(polynomial), "max_abs_coefficient": height}
    for name, value in stats.items():
        require(final["report"][name] == value, "Final report disagrees: " + name)
    producer_report = read_json(candidate/"producer-report.json")
    for name, value in stats.items():
        require(producer_report[name] == value, "Producer report disagrees: " + name)
    require(stats["degree"] == 4, "Final polynomial is not quartic")
    stats.update({"max_coefficient_bit_length": height.bit_length(),
                  "max_coefficient_decimal_digits": len(str(height)),
                  "coefficient_content": gcd(*polynomial.values()),
                  "maximum_residual_terms": max(map(len, compact)),
                  "all_weights_one": all(w == 1 for w in weights),
                  "variables_removed": len(old_active)-len(active)})
    files = ["certificate.jsonl.gz", "candidate-rows.json.gz", "residuals.json.gz",
             "source-residuals.jsonl.gz", "weights.json", "variable-map.json",
             "polynomial.expanded.txt", "polynomial.expanded.txt.gz", "producer-report.json"]
    return {
        "status": "PASS",
        "scope": "Exact rational input-projection equivalence to the frozen parent; complete integer expansion checked",
        "arithmetic_status": "The source system's characterization of the integers is not proved by this checker",
        "parent_git_commit": PARENT_COMMIT,
        "parent_directory": str(PARENT_RELATIVE),
        "parent_files_sha256": PINNED_PARENT,
        "parent_full_certificate_rechecked_this_run": check_parent,
        "parent_prefix_records": len(prefix),
        "parent_transformation_events": len(prefix)-1,
        "extra_operation_counts": dict(Counter(d["kind"] for d in details)),
        "extra_operation_total": len(details),
        "checked_patch_total": sum(d["checked_patches"] for d in details),
        "statistics": stats,
        "extra_operations": details,
        "candidate_files_sha256": {name: sha((candidate/name).read_bytes()) for name in files},
        "checker_sha256": sha(Path(__file__).read_bytes()),
        "python_version": sys.version.split()[0],
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, default=REPO/"build/optimize4096")
    parser.add_argument("--receipt", type=Path, default=Path(__file__).with_name("verification-12476.json"))
    parser.add_argument("--check-parent", action="store_true",
                        help="Also run the SHA-pinned, unchanged parent checker with write_report=False")
    args = parser.parse_args()
    try:
        receipt = verify(args.candidate, args.check_parent)
    except (VerificationError, KeyError, TypeError, ValueError, OSError) as error:
        parser.exit(1, "REJECTED: " + str(error) + "\n")
    args.receipt.write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    stats = receipt["statistics"]
    print(json.dumps({"status": "PASS", "variables": stats["variables"],
                      "degree": stats["degree"], "monomials": stats["monomials"],
                      "coefficient_bits": stats["max_coefficient_bit_length"],
                      "extra_operations": receipt["extra_operation_counts"],
                      "receipt": str(args.receipt)}))


if __name__ == "__main__":
    main()
