#!/usr/bin/env python3
"""Exact finite checks for the v43 early-scalar square-complement variant.

The modified arithmetic source is created in memory from the native builder.
Public repository files are never changed. The proof of source soundness,
completeness, and finite-local realization is in papers/pole_parameters/square_complement_baseline_20261116_v43.tex.
"""
import ast
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import argparse
import json
import sys
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NATIVE = REPO/"computation/few_variables/unit_norm_v28/build_sources.py"
sys.dont_write_bytecode = True
sys.path.insert(0, str(NATIVE.parent))
from build_sources import make_source

ELL = 76249


def valuation(value, p):
    value = F(value)
    assert value
    n, d = abs(value.numerator), value.denominator
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def square_locally(value, p):
    v = valuation(value, p)
    if v % 2:
        return False
    u = F(value)/F(p)**v
    modulus = 8 if p == 2 else p
    residue = u.numerator*pow(u.denominator, -1, modulus) % modulus
    return residue == 1 if p == 2 else pow(residue, (p-1)//2, p) == 1


def values(x, L):
    x = F(x)
    beta = 216*x**4+450459
    r = beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1)
    oldden = 1+17*(ELL**((L+1)//2)+1)*r
    newden = 1+153*ELL**L*r
    num = 102**2*ELL**L*r
    old, new = num/oldden**2, num/newden**2
    root = 17*(1-153*ELL**L*r)/newden
    assert new/old == (oldden/newden)**2
    assert root*root == 17*(17-new)
    return beta, r, old, new, root


def modified_builder():
    tree = ast.parse(NATIVE.read_text(), filename=str(NATIVE))
    expected = ast.dump(ast.parse("1+17*(prime_power+1)*raw", mode="eval").body)
    replacement = ast.parse("1+153*contact_power*raw", mode="eval").body
    replacements = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == "scalar_denominator":
                assert ast.dump(node.value) == expected
                node.value = replacement
                replacements += 1
    assert replacements == 2
    ast.fix_missing_locations(tree)
    namespace = {"__file__": str(NATIVE), "__name__": "square_baseline_source_variant"}
    exec(compile(tree, str(NATIVE), "exec"), namespace)
    return namespace["make_source"]


def eval_rational(source, rational, x):
    nodes, variables, cache = source["coefficient_dag"], source["variables"], {}

    def evaluate(i):
        if i in cache:
            return cache[i]
        op, *args = nodes[i]
        if op == "int":
            v = F(args[0])
        elif op == "variable":
            assert variables[args[0]]["name"] == "input.X"
            v = F(x)
        elif op == "neg":
            v = -evaluate(args[0])
        elif op == "add":
            v = sum((evaluate(j) for j in args), F(0))
        elif op == "mul":
            v = F(1)
            for j in args:
                v *= evaluate(j)
        elif op == "pow":
            v = evaluate(args[0])**args[1]
        else:
            raise AssertionError(op)
        cache[i] = v
        return v
    return evaluate(rational["numerator"])/evaluate(rational["denominator"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE/"verification.json")
    args = parser.parse_args()
    z = sp.symbols("z")
    assert sp.factor(17*(17-68*z/(1+z)**2)-(17*(1-z)/(1+z))**2) == 0
    assert 102**2 == 68*153
    assert all(ELL % n for n in range(2, isqrt(ELL)+1))

    # Complete fixed-prime residue certificate, independent of the old
    # saved certificate: none of the five raw factors vanishes modulo ell.
    counts = [0]*5
    beta_values = set()
    for x in range(ELL):
        beta = (216*x**4+450459) % ELL
        beta_values.add(beta)
        factors = [beta, beta-1, beta-2401, 32*beta+343, 2*beta-1]
        for j, factor in enumerate(factors):
            counts[j] += factor % ELL == 0
    assert counts == [0]*5

    integer_rows = []
    for L in (3, 5, 21, 23):
        for x in (0, 1, 3, 6, 7, 19):
            beta, r, old, new, root = values(x, L)
            assert r.denominator == 1 and r.numerator % 4 == 0
            assert 0 < new < F(1, 17) and root != 0
            assert all(square_locally(new, p) for p in (2, 3, 17))
            assert [valuation(new, p) for p in (2, 3, 17)] == [valuation(old, p) for p in (2, 3, 17)]
            assert valuation(new, 2) >= 3 and valuation(new, 3) >= 1 and valuation(new, 17) >= 2
            assert isqrt(new.denominator)**2 == new.denominator
            den = 1+153*ELL**L*r.numerator
            num = 102**2*ELL**L*r.numerator
            assert gcd(num, den) == 1 and new.denominator == den*den
            integer_rows.append({"L": L, "X": x,
                                 "valuations_2_3_17": [valuation(new, p) for p in (2, 3, 17)],
                                 "square_complement_identity": True, "prepared_scalar": True})

    depth_rows = []
    for L in (3, 19, 21, 39, 41):
        for m in (1, 2, 3):
            x = F(1, ELL**m)
            beta, r, old, new, root = values(x, L)
            assert valuation(beta, ELL) == -4*m
            assert valuation(r, ELL) == -20*m
            mu = valuation(new, ELL)
            assert mu == abs(L-20*m) and mu > 0 and mu % 2 == 1
            assert L <= mu+20*m
            depth_rows.append({"L": L, "m": m, "mu": mu,
                               "old_mu": valuation(old, ELL),
                               "L_le_mu_plus_20m": True})
    assert next(row for row in depth_rows if row["L"] == 21 and row["m"] == 1)["mu"] == 1

    make_variant = modified_builder()
    circuit_rows = []
    for name in ("general25", "explicit27"):
        L = 3
        native, variant = make_source(name, L), make_variant(name, L)
        assert native["variables"] == variant["variables"]
        assert [(b["name"], b["kind"], b["degree"]) for b in native["finite_blocks"]] == [
            (b["name"], b["kind"], b["degree"]) for b in variant["finite_blocks"]]
        assert native["total_external_variables"] == variant["total_external_variables"]
        event = next(e for e in variant["events"] if e["operation"] == "combined_height_scales")
        for x in (0, 3, F(1, ELL)):
            assert eval_rational(variant, event["scalar_contact"], x) == values(x, L)[3]
        circuit_rows.append({"source": name, "total_coordinates": variant["total_external_variables"],
                             "same_variable_roles_and_finite_blocks": True,
                             "native_replacement_identity_checked": True})

    # Exact polynomial form of the elementary homogeneous height bound.
    # For B>=66, (B+1)^2 >=68B follows from B^2-66B+1>=1.
    B, t = sp.symbols("B t")
    assert sp.expand((B+1)**2-68*B) == B**2-66*B+1
    assert sp.expand((B**2-66*B+1).subs(B, 66+t)) == t**2+66*t+1

    bound_sources = [
        "computation/few_variables/unit_norm_v28/build_sources.py",
        "papers/few_variables25/few_variables25_merged_20261110_v19.tex",
        "papers/finite_algebra/unit_norm_20261114_v28.tex",
        "papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex",
        "negative_results/papers/pole_parameters/square_complement_normalization_20261116_v43.tex",
    ]
    report = {
        "status": "PASS", "ell": ELL,
        "fixed_prime_complete_residue_count": ELL,
        "distinct_beta_residues": len(beta_values),
        "five_raw_factor_zero_counts": counts,
        "integer_scalar_examples": integer_rows,
        "nonintegral_fixed_prime_depth_examples": depth_rows,
        "native_variants": circuit_rows,
        "source_sha256": {path: sha256((REPO/path).read_bytes()).hexdigest() for path in bound_sources},
        "scope": "Exact identities, complete fixed-prime residue enumeration, finite local scalar examples, loss-of-depth controls, and in-memory native source variants. No new variable bound or effective defining exponent is claimed; infinite source arguments are in the companion paper and retain the existing arithmetic premises.",
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(f"PASS: square identity; {ELL} residues; 24 prepared scalar examples; 15 depth controls; 2 native variants; certificate {args.output}")


if __name__ == "__main__":
    main()
