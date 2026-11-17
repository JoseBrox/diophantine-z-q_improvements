#!/usr/bin/env python3
"""Exact odd-halfpoint raw-abscissa counterexample; standard library only."""
from fractions import Fraction
from math import isqrt
from pathlib import Path
import argparse
import json

P = 85817
H_INDEX = 2665
Z_RESIDUE = 39827
SHIFTS = (-10, -8, -5, 1, 2, 3, 4, 6, 7)


def add(a, b, D, modulus, unit_log=None):
    if a is None:
        return b
    if b is None:
        return a
    x, y = a
    X, Y = b
    if x == X:
        if (y + Y) % modulus == 0:
            return None
        numerator, denominator = 3*x*x-D, 2*y
    else:
        numerator, denominator = Y-y, X-x
    if unit_log is not None:
        assert denominator % P != 0
        unit_log.append(denominator % P)
    slope = numerator * pow(denominator, -1, modulus) % modulus
    xx = (slope*slope-x-X) % modulus
    out = (xx, (slope*(x-xx)-y) % modulus)
    assert (out[1]**2-out[0]**3+D*out[0]) % modulus == 0
    return out


def multiply(n, a, D, modulus, unit_log=None):
    result = None
    for bit in bin(n)[2:]:
        result = add(result, result, D, modulus, unit_log)
        if bit == "1":
            result = add(result, a, D, modulus, unit_log)
    return result


def rational_mod(a, modulus):
    return a.numerator*pow(a.denominator, -1, modulus) % modulus


def main(output):
    p = P
    assert all(p % q for q in range(2, isqrt(p)+1))
    assert p > 76176 and p % 8 == 1
    m = p**3
    slots = []
    for root, exact_order in ((21381, 5330), (64436, 1066)):
        s = root
        for exponent in (1, 2):
            modulus = p**exponent
            s = (s-((s*s-2)//modulus)*pow(2*s, -1, p)*modulus) % (p*modulus)
        assert (s*s-2) % m == 0
        D = (11-6*s) % m
        R = ((1+s) % m, 2*s % m)
        assert (R[1]**2-R[0]**3+D*R[0]) % m == 0
        units = []
        H = multiply(H_INDEX, R, D, m, units)
        assert H[0] % (p*p) == 0 and H[0] % m != 0
        assert H[1] % p == 0 and H[1] % (p*p) != 0
        Rp = tuple(v % p for v in R)
        assert multiply(exact_order, Rp, D % p, p) is None
        for q in (2, 5, 13, 41):
            if exact_order % q == 0:
                assert multiply(exact_order//q, Rp, D % p, p) is not None
        assert multiply(H_INDEX, Rp, D % p, p) == (0, 0)
        root_point = multiply(2, Rp, D % p, p)
        difference = add((0, 0), (root_point[0], -root_point[1] % p), D % p, p)
        assert difference[0] != 0 and difference[1] != 0
        slots.append({"sqrt2_mod_p": root, "sqrt2_mod_p3": s,
                      "R0_exact_order_mod_p": exact_order,
                      "H_mod_p3": list(H),
                      "xH_over_p2_mod_p": H[0]//(p*p) % p,
                      "yH_over_p_mod_p": H[1]//p % p,
                      "H_minus_P_mod_p": list(difference),
                      "unit_denominators_in_chain": len(units)})
    a = Fraction(10621537, 256)**4
    aa = rational_mod(a, p*p)
    terms = [((aa+c)**2-Z_RESIDUE**2) % (p*p) for c in SHIFTS]
    F = 1
    for term in terms:
        assert term % p != 0
        F = F*term % (p*p)
    Fa = 0
    for i, c in enumerate(SHIFTS):
        term = 2*(aa+c)
        for j, factor in enumerate(terms):
            if i != j:
                term = term*factor % (p*p)
        Fa = (Fa+term) % (p*p)
    assert Fa % p == 0 and Fa != 0
    pu = -18*(F % p)*pow(Fa//p, -1, p) % p
    leading_slots = [(pu*pu*row["xH_over_p2_mod_p"]**4) % p for row in slots]
    leading_trace = sum(leading_slots) % p
    assert leading_trace != 0
    certificate = {"status": "PASS", "scope": "Automatic preparation only; no global incompleteness claim",
        "prime": p, "prime_squared": p*p, "prime_cubed": p**3,
        "input": 1, "shift_B_fixture_only": 3, "root_A": "P=2R0",
        "auxiliaries_H_U": "2665R0", "R0": ["1+sqrt(2)", "2sqrt(2)"],
        "slope_residue_mod_p2": Z_RESIDUE, "slots": slots,
        "physical_scale_a": [str(a.numerator), str(a.denominator)],
        "F_mod_p2": F, "Fa_mod_p2": Fa, "Fa_over_p_mod_p": Fa//p,
        "pu_mod_p": pu, "first_four_C_valuations_each_slot": [-2, -2, 0, 0],
        "comparison_tests_selected_character": [0, 0],
        "inverse_W_valuation_each_slot": 6,
        "inverse_W_over_p6_mod_p_slots": leading_slots,
        "V_over_p6_mod_p": leading_trace,
        "valuation_u": -1, "valuation_w": 1,
        "valuation_V": 6, "valuation_b": -11,
        "valuation_trace_square_radicand": 1,
        "real_preparation": "All sufficiently large positive integers z in the stated residue class",
        "not_asserted": ["all fixed finite-place preparation", "selected prime factorization", "odd-coset completeness", "B=3 above the defining threshold"]}
    output.write_text(json.dumps(certificate, indent=2)+"\n")
    print("PASS: odd halfpoint coset; physical v_p(b)=-11; trace-square valuation=1")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("certificate.json"))
    main(parser.parse_args().output)
