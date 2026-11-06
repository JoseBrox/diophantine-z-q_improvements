"""Independent exact verifier for the packed semilocal anchor.

Only Python's standard library and the digest-pinned upstream checker are used.
No producer code is imported.  The semantic anchor rule is a mathematical
theorem proved in anchor-proof.tex, not an identity in polynomial ideals.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import time


if not __debug__:
    raise RuntimeError("Do not disable verification with python -O")

PINNED = {
    "candidate-rows.json.gz": "ff5412848dff46ac6ea0328244930b66c0a51c365e2b133bbafc7f2c86ca4b9e",
    "certificate.jsonl.gz": "9f7979c1e786bebad624b9ea4631b7eccd879f4bebb5b9ab69250b945973b268",
    "variable-map.json": "de0cc5ffa613b60a3b10af4f4aa9033e09516c6fe4403dc7f0b58675e8e30b97",
    "polynomial.expanded.txt": "7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca",
    "source-residuals.jsonl.gz": "ce9eeac7c4730aced8cfb70a1ab3b1b6a7fb2110c597afad1f56ddc92aeea73f",
    "verify_certificate.py": "d2079177a4960740c5b7d42fbd0756dfc4ce8953cc947cee91c8786ba26fa8ba",
    "construction-map.json": "edad166ce99d33fe50271e2afdc1628bbec0361d812762212240cadd30f93cfe",
}
# Never accept an arbitrary alternate baseline just because its producer
# supplied a matching digest in the new certificate.


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(row):
    result = {}
    for coeff, mon in row:
        assert type(coeff) is int and coeff != 0
        assert all(type(v) is int and v >= 0 for v in mon)
        key = tuple(mon)
        assert key == tuple(sorted(key)) and key not in result
        result[key] = coeff
    return result


def encoded(row):
    return [[coeff, list(mon)] for mon, coeff in row.items()]


def read_rows(path):
    return [decode(row) for row in json.loads(gzip.decompress(path.read_bytes()))]


def read_records(path):
    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]


def variables(row):
    return {v for mon in row for v in mon}


def combine(*terms):
    result = defaultdict(Fraction)
    for scale, row in terms:
        for mon, coeff in row.items():
            result[mon] += scale * coeff
    return {mon: coeff for mon, coeff in result.items() if coeff}


def multiply(a, b):
    result = defaultdict(Fraction)
    for mon, coeff in a.items():
        for other, value in b.items():
            result[tuple(sorted(mon + other))] += coeff * value
    return {mon: coeff for mon, coeff in result.items() if coeff}


def normalized(row):
    if not row:
        return ()
    denominator = math.lcm(*(Fraction(c).denominator for c in row.values()))
    ints = {mon: int(coeff * denominator) for mon, coeff in row.items()}
    divisor = math.gcd(*ints.values())
    if ints[min(ints)] < 0:
        divisor = -divisor
    return tuple(sorted((mon, coeff // divisor) for mon, coeff in ints.items()))


def substitute(row, variable, replacement):
    result = {}
    for mon, coeff in row.items():
        value = {(): Fraction(coeff)}
        for v in mon:
            value = multiply(value, replacement if v == variable else {(v,): 1})
        result = combine((1, result), (1, value))
    return result


def square_sum(rows):
    """Full ordered-pair expansion, independent of the producer's method."""
    result = defaultdict(int)
    for row in rows:
        for mon, coeff in row.items():
            for other, value in row.items():
                result[tuple(sorted(mon + other))] += coeff * value
    return {mon: coeff for mon, coeff in result.items() if coeff}


def statistics(rows, active):
    poly = square_sum(rows)
    return {
        "variables": len(active), "witnesses": len(active) - 1,
        "rows": sum(bool(row) for row in rows), "degree": max(map(len, poly)),
        "monomials": len(poly), "max_abs_coefficient": max(map(abs, poly.values())),
    }


def replay_parent(base, parent):
    """Replay the optional large-coefficient linear/elimination suffix."""
    base_records = read_records(base / "certificate.jsonl.gz")
    records = read_records(parent / "certificate.jsonl.gz")
    assert base_records[-2]["kind"] == records[-2]["kind"] == "weights"
    assert base_records[-1]["kind"] == records[-1]["kind"] == "final"
    prefix = base_records[:-2]
    assert records[:len(prefix)] == prefix, "Parent is not an extension of the pinned certificate"
    rows = read_rows(base / "candidate-rows.json.gz")
    allocated = base_records[-1]["allocated_variables"]
    counts = Counter()
    for event in records[len(prefix):-2]:
        kind, data = event["kind"], event["data"]
        assert kind in ("linear", "eliminate"), ("Unsupported suffix operation", kind)
        counts[kind] += 1
        patches = {i: decode(row) for i, row in event["patches"]}
        assert len(patches) == len(event["patches"])
        assert all(type(i) is int and 0 <= i < len(rows) for i in patches)
        if kind == "linear":
            target, other, a, b = (data[k] for k in ("target", "other", "a", "b"))
            assert type(target) is int and type(other) is int
            assert 0 <= target < len(rows) and 0 <= other < len(rows) and target != other
            assert type(a) is int and type(b) is int and a != 0
            expected = {target: combine((a, rows[target]), (b, rows[other]))}
        else:
            index, variable = data["row"], data["variable"]
            assert type(index) is int and 0 <= index < len(rows)
            assert type(variable) is int and 0 < variable < allocated
            denominator = data.get("denominator", 1)
            assert type(denominator) is int and denominator > 0
            numerator = decode(data["replacement"])
            assert variable not in variables(numerator)
            assert all(v < allocated for v in variables(numerator))
            replacement = {mon: Fraction(coeff, denominator) for mon, coeff in numerator.items()}
            defining = combine((1, {(variable,): 1}), (-1, replacement))
            assert normalized(rows[index]) == normalized(defining), "Incorrect elimination equation"
            affected = {i for i, row in enumerate(rows) if variable in variables(row)} - {index}
            assert len(data["affected"]) == len(set(data["affected"]))
            assert set(data["affected"]) == affected, "Incomplete elimination occurrences"
            expected = {i: substitute(rows[i], variable, replacement) for i in affected}
            expected[index] = {}
        assert patches.keys() == expected.keys()
        for i, row in patches.items():
            assert normalized(row) == normalized(expected[i]), ("Incorrect patch", kind, i)
            assert all(len(mon) <= 2 for mon in row)
            assert all(v < allocated for v in variables(row))
            rows[i] = row
    assert records[-2]["values"] == [1] * len(rows)
    assert records[-1]["allocated_variables"] == allocated
    assert hashlib.sha256(canonical([encoded(row) for row in rows])).hexdigest() == records[-1]["rows_sha256"]
    assert rows == read_rows(parent / "candidate-rows.json.gz")
    active = json.loads((parent / "variable-map.json").read_bytes())
    assert active[0] == 0 and len(active) == len(set(active))
    assert set(active) == set().union(*(variables(row) for row in rows))
    stats = statistics(rows, active)
    for key, value in stats.items():
        assert records[-1]["report"][key] == value, ("Parent statistics differ", key)
    return rows, active, allocated, dict(counts)


def prove_nonzero(rows, target, forbidden_rows):
    """Recognize a nonzero rational constant followed by squaring equations."""
    known = {}
    progress = True
    while progress and target not in known:
        progress = False
        for i, row in enumerate(rows):
            if i in forbidden_rows or len(row) != 2:
                continue
            linear = [mon[0] for mon in row if len(mon) == 1]
            if len(linear) != 1:
                continue
            v = linear[0]
            if v in known:
                continue
            other = next(mon for mon in row if mon != (v,))
            if not other:
                known[v] = {"row": i, "variable": v, "reason": "nonzero rational constant"}
            elif len(other) == 2 and other[0] == other[1] and other[0] in known:
                known[v] = {"row": i, "variable": v, "reason": "nonzero multiple of a square", "dependency": other[0]}
            else:
                continue
            progress = True
    assert target in known, "No certified nonzero constant chain for C"
    chain = []
    v = target
    while True:
        step = known[v]
        chain.append(step)
        if "dependency" not in step:
            break
        v = step["dependency"]
    return list(reversed(chain))


def verify(root, baseline):
    started = time.monotonic()
    certificate = json.loads((root / "certificate.json").read_bytes())
    assert certificate["schema"] == "anchor-pack-v1"
    assert certificate["baseline"] == PINNED
    for name, expected in PINNED.items():
        assert digest(baseline / name) == expected, ("Changed baseline", name)
    spec = importlib.util.spec_from_file_location("pinned_quartic_checker", baseline / "verify_certificate.py")
    assert spec and spec.loader
    upstream = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(upstream)
    upstream_receipt = upstream.verify(baseline, write_report=False)
    assert upstream_receipt["status"] == "PASS"
    for name, expected in certificate["parent"].items():
        assert name in ("candidate-rows.json.gz", "certificate.jsonl.gz", "variable-map.json")
        assert digest(root / "parent" / name) == expected
    assert set(certificate["parent"]) == {"candidate-rows.json.gz", "certificate.jsonl.gz", "variable-map.json"}
    rows, parent_active, allocated, tail_counts = replay_parent(baseline, root / "parent")
    index = list(range(310, 316))
    private = set(range(329, 345))
    assert certificate["old_row_indices"] == index
    assert certificate["old_private_variables"] == sorted(private)
    assert certificate["interface_variables"] == {"C": 25, "f0": 51, "f1": 52}
    instantiations = json.loads((baseline / "construction-map.json").read_bytes())["instantiations"]
    anchors = [item for item in instantiations if item["module"] == "q_anchor"]
    assert anchors == [{"arguments": [51, 52], "first_local": 329, "first_residual": 310,
                        "local_count": 16, "module": "q_anchor", "path": "Z_definition/0", "residual_count": 6}]
    expected_old = []
    # This independently reconstructs both literal seven-witness predicates.
    for f, a in ((51, 329), (52, 337)):
        expected_old.extend([
            {(25, a): 1, (f,): -1},
            {(): -1, (a+1, a+1): 1, (a+2, a+2): -2,
             (a+3, a+3): -3, (a+4, a+4): 6},
            {(): -4, (a, a): 1, (a, a+1): -4, (a+1, a+1): 4,
             (a+5, a+5): -8, (a+6, a+6): -12, (a+7, a+7): 24},
        ])
    assert [decode(row) for row in certificate["matched_old_rows"]] == expected_old
    assert [rows[i] for i in index] == expected_old
    incidence = {v: [i for i, row in enumerate(rows) if v in variables(row)] for v in private}
    assert all(indices and set(indices) <= set(index) for indices in incidence.values())
    nonzero_chain = prove_nonzero(rows, 25, set(index))
    names = ("r", "D", "u", "v", "w")
    fresh = list(range(allocated, allocated+5))
    assert certificate["new_variables"] == dict(zip(names, fresh))
    r, d, u, v, w = fresh
    replacement = [
        {(r,): 1, (51, 51): -1, (51, 52): -1, (52, 52): 1},
        {(d,): 1, (25, 25): -1},
        {(u, u): 1, (v, v): 6, (w, w): -2, (r, r): -3, (d, d): 2},
    ]
    assert [decode(row) for row in certificate["new_rows"]] == replacement
    for i in index:
        rows[i] = {}
    for i, row in zip(index, replacement):
        rows[i] = row
    assert rows == read_rows(root / "candidate-rows.json.gz")
    active = json.loads((root / "variable-map.json").read_bytes())
    assert active == [v for v in parent_active if v not in private] + fresh
    assert len(active) == len(parent_active) - 11 and active[0] == 0
    assert set(active) == set().union(*(variables(row) for row in rows))
    mapping = {v: i for i, v in enumerate(active)}
    compact = [
        {tuple(sorted(mapping[v] for v in mon)): coeff for mon, coeff in row.items()}
        for row in rows if row
    ]
    assert compact == read_rows(root / "residuals.json.gz")
    assert json.loads((root / "weights.json").read_bytes()) == [1] * len(compact)
    assert all(len(mon) <= 2 for row in compact for mon in row)
    polynomial = square_sum(compact)
    expanded = (root / "polynomial.expanded.txt").read_bytes()
    assert gzip.decompress((root / "polynomial.expanded.txt.gz").read_bytes()) == expanded
    supplied = {}
    for line in expanded.decode("ascii").splitlines():
        if line.startswith("#"):
            continue
        coeff, *mon = map(int, line.split())
        mon = tuple(mon)
        assert coeff != 0 and mon == tuple(sorted(mon)) and mon not in supplied
        supplied[mon] = coeff
    assert supplied == polynomial, "Full integer coefficient table differs"
    assert hashlib.sha256(expanded).hexdigest() == certificate["expanded_sha256"]
    assert {v for mon in polynomial for v in mon} == set(range(len(active)))
    stats = statistics(compact, active)
    assert stats["degree"] == 4
    for key, value in stats.items():
        assert certificate["statistics"][key] == value
    report = {
        "status": "PASS",
        "scope": "Pinned baseline certificate replay, optional exact elimination suffix, literal semilocal anchor replacement, private-variable incidence, nonzero anchor constant, and full integer expansion. The semantic replacement uses the proved quaternion lemma; the source arithmetic characterization of the integers is not proved by this program.",
        **stats,
        "max_coefficient_bits": max(abs(c).bit_length() for c in polynomial.values()),
        "variables_saved_by_anchor": 11,
        "parent_variables": len(parent_active),
        "baseline_expanded_sha256": upstream_receipt["expanded_sha256"],
        "parent_suffix_operations": tail_counts,
        "private_occurrences": {str(v): indices for v, indices in sorted(incidence.items())},
        "nonzero_C_chain": nonzero_chain,
        "expanded_sha256": hashlib.sha256(expanded).hexdigest(),
        "checker_sha256": digest(Path(__file__)),
        "seconds": round(time.monotonic() - started, 3),
    }
    (root / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--baseline", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.directory.resolve(), args.baseline.resolve())
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("private_occurrences", "nonzero_C_chain")}, indent=2))
