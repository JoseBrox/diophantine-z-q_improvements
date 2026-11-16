#!/usr/bin/env python3
"""Exact v43 checks: actual general-source return neighborhoods can miss C=square.

This does not prove nonexistence of other actual source witnesses. The infinite
arithmetic and guard assertions are those stated in negative_results/papers/pole_parameters/actual_square_complement_neighborhoods_20261116_v43.tex; this
checker certifies the uniform mod23 table, its native source binding, and the
detector reduction b=rho when R=W_+=W_-=1 mod23.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(REPO / "computation/few_variables/unit_norm_v28"))
from build_sources import make_source

P = 23
XS = [3, 6, 6, 3, 7, 3, 3, 6, 7, 3, 3]
EXPECTED = [
    [20, 1, 12, 8, 15], [7, 19, 6, 22, 7], [7, 19, 18, 11, 10],
    [20, 1, 2, 1, 19], [16, 9, 15, 9, 21], [20, 1, 15, 16, 17],
    [20, 1, 6, 13, 22], [7, 19, 10, 5, 20], [16, 9, 13, 4, 14],
    [20, 1, 9, 9, 21], [20, 1, 5, 13, 22],
]


def residue(q):
    q = F(q)
    assert q.denominator % P
    return q.numerator * pow(q.denominator, -1, P) % P


def literal_scalar(x, L):
    beta = 216*x**4 + 450459
    r = beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1)
    denominator = 1 + 17*(76249**((L+1)//2)+1)*r
    rho = F(102**2 * 76249**L * r, denominator**2)
    return beta, r, denominator, rho


def native_scalar(name, L, x):
    source = make_source(name, L)
    nodes, variables = source["coefficient_dag"], source["variables"]
    event = next(e for e in source["events"] if e["operation"] == "combined_height_scales")
    cache = {}
    seen_variables = set()

    def evaluate(i):
        if i in cache:
            return cache[i]
        op, *args = nodes[i]
        if op == "int":
            value = args[0] % P
        elif op == "variable":
            name = variables[args[0]]["name"]
            seen_variables.add(name)
            assert name == "input.X"
            value = x % P
        elif op == "neg":
            value = -evaluate(args[0]) % P
        elif op == "add":
            value = sum(evaluate(j) for j in args) % P
        elif op == "mul":
            value = 1
            for j in args:
                value = value*evaluate(j) % P
        elif op == "pow":
            value = pow(evaluate(args[0]), args[1], P)
        else:
            raise AssertionError((op, args))
        cache[i] = value
        return value

    def rational_value(r):
        n, d = evaluate(r["numerator"]), evaluate(r["denominator"])
        assert d
        return n*pow(d, -1, P) % P

    values = [rational_value(event[key]) for key in
              ("beta", "raw_scalar_contact", "scalar_denominator", "scalar_contact")]
    assert seen_variables == {"input.X"}
    assert len([e for e in source["events"] if e["operation"] == "combined_detector"]) == (
        2 if name == "general25" else 3)
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE/"verification.json")
    args = parser.parse_args()
    assert 76249 % P == 4
    assert pow(4, 11, P) == 1
    assert all(pow(4, j, P) != 1 for j in range(1, 11))
    squares = {a*a % P for a in range(1, P)}
    assert len(squares) == 11
    rows = []
    for k, x in enumerate(XS):
        L = 2*k-1
        while L < 3:
            L += 22
        beta, r, denominator, rho = literal_scalar(x, L)
        C = 17*(17-rho)
        row = [residue(v) for v in (beta, r, denominator, rho, C)]
        assert row == EXPECTED[k]
        assert all(row[j] != 0 for j in (1, 2, 3, 4))
        assert row[4] not in squares and pow(row[4], 11, P) == P-1
        assert native_scalar("general25", L, x) == row[:4]
        rows.append({"k_mod_11": k, "representative_L": L, "input_X": x,
                     "beta": row[0], "r": row[1], "denominator": row[2],
                     "rho": row[3], "complement": row[4],
                     "Euler_criterion": P-1, "native_general25_match": True})

    # An independent periodic check uses modular exponentiation directly,
    # rather than the large integer/Fraction formula above.
    for k in range(2, 90):
        x = XS[k % 11]
        beta = (9*x**4+4) % P
        r = beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1) % P
        den = (1+17*(pow(4, k, P)+1)*r) % P
        rho = 8*pow(4, 2*k-1, P)*r*pow(den, -2, P) % P
        assert rho == EXPECTED[k % 11][3]
        assert 17*(17-rho) % P not in squares | {0}

    # Native explicit source at the already certified exponent. This
    # evaluation never expands 76249**20483 as an integer.
    explicit = native_scalar("explicit27", 20483, 6)
    assert explicit == [7, 19, 6, 22]
    assert ((20483+1)//2) % 11 == 1

    # Verify the complete finite-field detector reduction, with split
    # embeddings W_+=W_-=1. Half-trace=W0 and norm=W_+*W_-.
    half_trace = (1+1)*pow(2, -1, P) % P
    norm = 1
    assert half_trace == 1
    for rho in range(1, P):
        b = rho*1*norm*norm*pow(half_trace, -2, P) % P
        assert b == rho

    bound_sources = [
        "computation/few_variables/unit_norm_v28/build_sources.py",
        "papers/few_variables25/few_variables25_merged_20261110_v19.tex",
        "papers/few_variables27/explicit27_20261110_v19.tex",
        "papers/finite_algebra/unit_norm_20261114_v28.tex",
        "papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex",
        "papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex",
    ]
    report = {
        "status": "PASS",
        "prime": P,
        "multiplicative_order_of_76249_mod23": 11,
        "inputs_suffice": [3, 6, 7],
        "rows": rows,
        "explicit27_at_L20483_X6": {"native_scalar_data": explicit, "complement_mod23": 7},
        "all_nonzero_rho_detector_reductions_checked": P-1,
        "source_sha256": {path: sha256((REPO/path).read_bytes()).hexdigest() for path in bound_sources},
        "scope": "Uniform finite-field and native-source identities only; existence of guarded prepared actual return families uses the explicitly retained completeness premises. Other actual tuples and common rational tau fibers are not excluded.",
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(f"PASS: 11 residue classes; 11 native general source bindings; native explicit L=20483; certificate {args.output}")


if __name__ == "__main__":
    main()
