#!/usr/bin/env python3
"""Exact finite certificate for the specified sequential-unit factor design.

Python standard library only. No search producer, symbolic algebra package,
SMT solver, floating-point arithmetic, or previous enumeration is imported.
"""
from pathlib import Path
from itertools import product
from hashlib import sha256
import argparse
import json

HERE = Path(__file__).resolve().parent
ZERO = (0, 0)


def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])


def minus(a, b):
    return (a[0] - b[0], a[1] - b[1])


def scale(n, a):
    return (n * a[0], n * a[1])


def digest(value):
    data = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return sha256(data).hexdigest()


def extensions(exponents):
    """All distinct new a+b-c, with a deterministic quadratic definition."""
    witnesses = {}
    for a, b, c in product(sorted(exponents), repeat=3):
        if b < a:
            continue
        e = minus(plus(a, b), c)
        if e in exponents:
            continue
        witness = (a, b, c)
        key = (sum(t != ZERO for t in witness), witness)
        if e not in witnesses or key < witnesses[e]:
            witnesses[e] = key
    return {e: value[1] for e, value in witnesses.items()}


def comparison_states(exponents):
    """All integer-weight states allowed by one comparison and both constants."""
    sums = {plus(a, b) for a, b in product(exponents, repeat=2)}
    states = []
    for p0, p1 in product((9, 11), repeat=2):
        for e0 in sorted(sums):
            # r0=2w+(-6+p0,0), e0=-r0.
            numerator = minus(scale(-1, e0), (-6 + p0, 0))
            if any(t % 2 for t in numerator):
                continue
            w = tuple(t // 2 for t in numerator)
            r0 = plus(scale(2, w), (-6 + p0, 0))
            r1 = plus(scale(2, w), (-6 + p1, p1))
            e1 = scale(-1, r1)
            if e1 not in sums:
                continue
            assert scale(-1, r0) == e0
            assert minus(e1, e0) == (p0 - p1, -p1)
            states.append({
                "powers": [p0, p1],
                "constant_exponents": [e0, e1],
                "comparison_weight": w,
                "row_exponents": [r0, r1],
            })
    return states


def survivor_certificate(exponents, states):
    """Verify the contradiction for all assignments, not a chosen pairing."""
    weights = {tuple(state["comparison_weight"]) for state in states}
    assert len(weights) == 1
    w = next(iter(weights))
    assert w[1] == 0
    assert {state["powers"][1] for state in states} == {9}
    r1s = {tuple(state["row_exponents"][1]) for state in states}
    assert len(r1s) == 1
    r1 = next(iter(r1s))
    # All four comparisons occupy detector 1's four first slots. Its four
    # second slots are consequently the four raw tests, all with power 3.
    raw_numerator = minus(r1, (3, 3))
    assert all(t % 2 == 0 for t in raw_numerator)
    raw_weight = tuple(t // 2 for t in raw_numerator)
    assert raw_weight[1] == 3
    # In detector 0, putting two comparisons in one factor would force
    # equal row exponents whose difference is the nonzero vector (2,0).
    comp_first = plus(scale(2, w), (3, 0))
    comp_second = plus(scale(2, w), (5, 0))
    assert minus(comp_second, comp_first) == (2, 0)
    # Four comparisons in four factors therefore give exactly one in each.
    # For both possible slots the other test is raw and the row exponents
    # disagree in their second component. Check the full vectors too.
    mismatches = []
    for comparison_power, raw_power in ((9, 3), (11, 1)):
        rc = plus(scale(2, w), (-6 + comparison_power, 0))
        rr = plus(scale(2, raw_weight), (raw_power, 0))
        assert rc[1] == 0 and rr[1] == 6
        assert rc != rr
        mismatches.append({
            "comparison_power": comparison_power,
            "raw_power": raw_power,
            "comparison_row_exponent": rc,
            "raw_row_exponent": rr,
        })
    return {
        "comparison_weight_for_every_test": w,
        "detector1_comparison_power_for_every_test": 9,
        "detector1_factor_row_exponent": r1,
        "raw_weight_for_every_test_forced_by_detector1": raw_weight,
        "two_comparisons_in_detector0_row_exponent_difference": (2, 0),
        "detector0_mixed_factor_mismatches": mismatches,
        "contradiction": "The same raw-test v-weight must be 3 and 0.",
        "all_quadratic_test_assignments_excluded": True,
    }


def enumerate_and_check():
    model_bytes = (HERE / "factor_model.json").read_bytes()
    model = json.loads(model_bytes)
    assert model["initial_s"] == [-2, -1, 0, 1, 2]
    assert model["physical_directions"] == [[1, 0], [1, 1]]
    assert model["comparison_fourth_power_storage_exponent"] == [-6, 0]
    assert model["raw_square_storage_exponent"] == [0, 0]
    assert model["comparison_slot_powers"] == [9, 11]
    assert model["raw_slot_powers"] == [1, 3]
    assert len(model["comparison_tests"]) == len(model["raw_tests"]) == 4
    assert model["regular_factors_per_detector"] == 4
    assert model["sequential_extensions"] == model["target_degree"] == 2
    counts, survivors = [], []
    global_bases, central_bases = set(), set()
    expected_counts = {
        -2: (1140, 762, 0), -1: (868, 592, 0),
        0: (648, 458, 2), 1: (868, 592, 0), 2: (1140, 762, 0),
    }
    for s in model["initial_s"]:
        initial = {ZERO, (1, 0), (-1, 0), (0, 1), (s, -1)}
        assert len(initial) == 5
        seen = set()
        sequential = passed = 0
        for e1, d1 in sorted(extensions(initial).items()):
            mid = initial | {e1}
            for e2, d2 in sorted(extensions(mid).items()):
                sequential += 1
                final = mid | {e2}
                key = tuple(sorted(final))
                if key in seen:
                    continue
                seen.add(key)
                global_bases.add(key)
                if -1 <= s <= 1:
                    central_bases.add(key)
                states = comparison_states(final)
                if not states:
                    continue
                passed += 1
                for exponent, witness, available in ((e1, d1, initial), (e2, d2, mid)):
                    a, b, c = witness
                    assert {a, b, c} <= available
                    assert exponent == minus(plus(a, b), c)
                proof = survivor_certificate(final, states)
                survivors.append({
                    "id": len(survivors), "s": s,
                    "unit_basis": {"77": (1, 0), "78": (-1, 0),
                                   "90": (0, 1), "91": (s, -1),
                                   "92": e1, "241": e2},
                    "definitions": [
                        {"coordinate": 92, "exponent": e1,
                         "numerator": d1[:2], "denominator": d1[2]},
                        {"coordinate": 241, "exponent": e2,
                         "numerator": d2[:2], "denominator": d2[2]},
                    ],
                    "comparison_states": states, "factor_contradiction": proof,
                })
        assert (sequential, len(seen), passed) == expected_counts[s]
        counts.append({"s": s, "sequential_choices": sequential,
                       "distinct_bases_for_s": len(seen),
                       "single_comparison_survivors": passed,
                       "sorted_basis_set_sha256": digest(sorted(seen))})
    assert len(survivors) == 2
    assert len(global_bases) == 2834 and len(central_bases) == 1557
    assert [tuple(item["unit_basis"]["241"]) for item in survivors] == [(-1, -6), (1, -6)]
    assert all(tuple(item["unit_basis"]["92"]) == (0, -3) for item in survivors)
    return {
        "schema": "exact-sequential-unit-factor-certificate/v70",
        "status": "PASS",
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "factor_model_sha256": sha256(model_bytes).hexdigest(),
        "arithmetic": "Exact integer arithmetic; Python standard library only",
        "counts_by_s": counts,
        "totals_all_five_s": {
            "sequential_choices": sum(c["sequential_choices"] for c in counts),
            "distinct_s_basis_pairs": sum(c["distinct_bases_for_s"] for c in counts),
            "globally_distinct_final_bases": len(global_bases),
            "sorted_global_basis_set_sha256": digest(sorted(global_bases)),
        },
        "totals_s_minus1_0_1": {
            "sequential_choices": sum(c["sequential_choices"] for c in counts if -1 <= c["s"] <= 1),
            "distinct_s_basis_pairs": sum(c["distinct_bases_for_s"] for c in counts if -1 <= c["s"] <= 1),
            "globally_distinct_final_bases": len(central_bases),
        },
        "survivors": survivors,
        "single_comparison_filter_necessity": "For each comparison, -r_j lies in P+P, r0=2w+(-6+p0,0), and r1=2w+(-6+p1,p1), with integer w.",
        "full_square_component_forcing": "The two nonzero real square monomials force equal component weights; the nonzero imaginary product then forces equal component row exponents.",
        "outcome": "Every enumerated basis is excluded for the specified factor design.",
        "scope": model["scope"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    report = enumerate_and_check()
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"],
                      "totals": report["totals_all_five_s"],
                      "survivors": len(report["survivors"]),
                      "outcome": report["outcome"]}, indent=2))


if __name__ == "__main__":
    main()
