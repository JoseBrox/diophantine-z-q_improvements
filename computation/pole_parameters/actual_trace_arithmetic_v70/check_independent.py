#!/usr/bin/env python3
"""Independent exact audit of the actual-trace arithmetic fixture.

Standard library only. Does not import the author's producer, SymPy,
or a symbolic-algebra implementation. Reconstructs all recorded integer
polynomials and verifies both supplied finite-field Bezout identities.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
from math import gcd, lcm
import argparse
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "actual_trace_arithmetic_v71"
Z = (F(0), F(0))
O = (F(1), F(0))


def k(a, b=0):
    return (F(a), F(b))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[0], -a[1])


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    return (a[0]*b[0] + 2*a[1]*b[1], a[0]*b[1] + a[1]*b[0])


def inv(a):
    n = a[0]*a[0] - 2*a[1]*a[1]
    assert n
    return (a[0]/n, -a[1]/n)


def div(a, b):
    return mul(a, inv(b))


def bar(a):
    return (a[0], -a[1])


def trim(p):
    while len(p) > 1 and p[-1] == Z:
        p.pop()
    return p


def padd(a, b):
    out = [Z] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = add(a[i] if i < len(a) else Z, b[i] if i < len(b) else Z)
    return trim(out)


def pmul(a, b):
    out = [Z] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = add(out[i+j], mul(x, y))
    return trim(out)


def pscale(c, a):
    return trim([mul(c, x) for x in a])


def pbar(a):
    return [bar(c) for c in a]


def primitive_pair(a, b):
    assert all(c[1] == 0 for c in a + b)
    aa, bb = [c[0] for c in a], [c[0] for c in b]
    den = lcm(*(c.denominator for c in aa + bb))
    ia, ib = [int(den*c) for c in aa], [int(den*c) for c in bb]
    content = reduce(gcd, (abs(c) for c in ia + ib))
    return [c//content for c in ia], [c//content for c in ib]


CURVE_D = k(11, -6)
P = (k(F(57, 8), F(-7, 2)), k(F(-165, 8), F(417, 32)))


def on_curve(point):
    if point is None:
        return True
    x, y = point
    return mul(y, y) == sub(mul(mul(x, x), x), mul(CURVE_D, x))


def elliptic_add(first, second):
    if first is None:
        return second
    if second is None:
        return first
    x, y = first
    X, Y = second
    if x == X:
        if add(y, Y) == Z:
            return None
        slope = div(sub(mul(k(3), mul(x, x)), CURVE_D), mul(k(2), y))
    else:
        slope = div(sub(Y, y), sub(X, x))
    xx = sub(sub(mul(slope, slope), x), X)
    yy = sub(mul(slope, sub(x, xx)), y)
    result = (xx, yy)
    assert on_curve(result)
    return result


def read_point(value):
    return tuple(tuple(F(c) for c in coordinate) for coordinate in value)


def modtrim(a, prime):
    a = [c % prime for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def modadd(a, b, prime):
    out = [0] * max(len(a), len(b))
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return modtrim(out, prime)


def modmul(a, b, prime):
    out = [0] * (len(a) + len(b) - 1)
    for i, c in enumerate(a):
        for j, d in enumerate(b):
            out[i+j] = (out[i+j] + c*d) % prime
    return modtrim(out, prime)


def modderivative(a, prime):
    return modtrim([i*a[i] for i in range(1, len(a))] or [0], prime)


def modremainder(a, b, prime):
    a, b = modtrim(a[:], prime), modtrim(b[:], prime)
    assert b != [0]
    invlead = pow(b[-1], -1, prime)
    while len(a) >= len(b) and a != [0]:
        coefficient = a[-1]*invlead % prime
        shift = len(a) - len(b)
        for i, c in enumerate(b):
            a[i+shift] = (a[i+shift] - coefficient*c) % prime
        a = modtrim(a, prime)
    return a


def modgcd(a, b, prime):
    a, b = modtrim(a, prime), modtrim(b, prime)
    while b != [0]:
        a, b = b, modremainder(a, b, prime)
    inverse = pow(a[-1], -1, prime)
    return modtrim([c*inverse for c in a], prime)


def homogeneous_composition(poly, a, b, prime):
    # Independent direct power-sum evaluation; no Horner composition.
    n = len(poly) - 1
    ap, bp = [[1]], [[1]]
    for _ in range(n):
        ap.append(modmul(ap[-1], a, prime))
        bp.append(modmul(bp[-1], b, prime))
    result = [0]
    for i, coefficient in enumerate(poly):
        summand = modmul(ap[i], bp[n-i], prime)
        result = modadd(result, [coefficient*c for c in summand], prime)
    return result


def evaluate_integer_poly(poly, value):
    result = F(0)
    for coefficient in reversed(poly):
        result = result*value + coefficient
    return result


def fraction_residue(value, modulus):
    value = F(value)
    return value.numerator % modulus * pow(value.denominator % modulus, -1, modulus) % modulus


def valuation(value, prime):
    value = F(value)
    numerator, denominator = value.numerator, value.denominator
    assert numerator
    result = 0
    while numerator % prime == 0:
        numerator //= prime
        result += 1
    while denominator % prime == 0:
        denominator //= prime
        result -= 1
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=HERE / "independent_certificate.json")
    args = parser.parse_args()
    source_bytes = (args.source / "certificate.json").read_bytes()
    data = json.loads(source_bytes)
    records = data["actual_inputs"]
    assert records["X"] == 1 and records["B"] == 3
    assert P == read_point(records["P"]) and on_curve(P)
    half_P = (k(1, 1), k(0, 2))
    assert on_curve(half_P) and elliptic_add(half_P, half_P) == P
    # Compute by consecutive additions rather than binary scalar multiplication.
    multiples = [None]
    for _ in range(5):
        multiples.append(elliptic_add(multiples[-1], P))
    H, HminusP = multiples[5], multiples[4]
    assert H == read_point(records["H_coordinates"])
    assert HminusP == read_point(records["H_minus_P_coordinates"])
    assert elliptic_add(H, (P[0], neg(P[1]))) == HminusP
    assert all(point is not None and point[0] != Z and point[1] != Z
               for point in (P, H, HminusP))
    assert H[0] != P[0]
    c, d = inv(H[0]), bar(inv(HminusP[0]))
    assert c == tuple(F(x) for x in records["c_fH"])
    assert d == tuple(F(x) for x in records["d_bar_fHmP"])
    # Actual U=H and A=P give r=r'=1, hence exactly (c,c,d,d,0,0).
    tests = (c, c, d, d, Z, Z)
    assert records["tests"] == ["c", "c", "d", "d", "0", "0"]
    u = [Z, O]
    numerator, denominator = [O], [O]
    for test in tests:
        if test == Z:
            continue
        square = mul(test, test)
        balance = [O, square]
        factor_denominator = pmul(u, pmul(balance, balance))
        factor_numerator = padd(factor_denominator, [mul(square, square)])
        numerator = pmul(numerator, factor_numerator)
        denominator = pmul(denominator, factor_denominator)
    # W=numerator/denominator; take the trace of its reciprocal directly.
    trace_numerator = padd(pmul(denominator, pbar(numerator)),
                          pmul(pbar(denominator), numerator))
    trace_denominator = pmul(numerator, pbar(numerator))
    N, D = primitive_pair(trace_numerator, trace_denominator)
    stored = {name: [int(c) for c in coefficients]
              for name, coefficients in data["integer_polynomials_ascending"].items()}
    assert N == stored["N"] and D == stored["D"]
    assert len(N) == len(D) == 25 and N[-1] == 2*D[-1]
    assert N[:4] == [0]*4 and N[4] != 0 and D[0] != 0
    traceA = 2*P[0][0]
    a = (F(4)**4 + traceA**4)**4
    assert a == F(records["scale_a"]) and a > 10
    shifts = (-10, -8, -5, 1, 2, 3, 4, 6, 7)
    assert sum(shifts) == 0
    Fpoly, derivative = [O], [Z]
    for shift in shifts:
        factor = [k((a+shift)**2), k(-1)]
        derivative = padd(pmul(derivative, factor), pscale(k(2*(a+shift)), Fpoly))
        Fpoly = pmul(Fpoly, factor)
    A, B = primitive_pair(pscale(k(-18), Fpoly), derivative)
    assert A == stored["A_physical"] and B == stored["B_physical"]
    assert len(A) == 10 and len(B) == 9
    # The nine positive, distinct a+shift give simple contact roots and
    # nonzero F_a at every root. Thus A/B is also coprime in Q[t].
    roots = [(a+shift)**2 for shift in shifts]
    assert len(set(roots)) == 9
    assert all(a+shift > 0 for shift in shifts)
    prime = data["good_reduction_certificate"]["prime"]
    assert prime == 101
    n, dd = modtrim(N, prime), modtrim(D, prime)
    aa, bb = modtrim(A, prime), modtrim(B, prime)
    assert len(n) == len(dd) == 25 and len(aa) == 10 and len(bb) == 9
    assert modgcd(n, dd, prime) == [1]
    assert modgcd(aa, bb, prime) == [1]
    p = modadd(modmul(modmul(n, n, prime), [1, 2, 1], prime),
               modmul([0, 1], modmul(dd, modadd([2*c for c in dd], [-c for c in n], prime), prime), prime),
               prime)
    assert len(p) == 51 and p[0] == 0 and p[1] != 0
    q = homogeneous_composition(p, aa, bb, prime)
    assert len(q) == 451 and q[0] == 42
    good = data["good_reduction_certificate"]
    bezout_results = {}
    for name, polynomial in (("u", p), ("t", q)):
        left, right = ([int(c) % prime for c in row] for row in good[name+"_bezout"])
        derivative_mod = modderivative(polynomial, prime)
        result = modadd(modmul(left, polynomial, prime),
                        modmul(right, derivative_mod, prime), prime)
        assert result == [1]
        assert modgcd(polynomial, derivative_mod, prime) == [1]
        bezout_results[name] = "exact identity 1 and independent gcd=1"
    # Squarefreeness transfers to Q because the integer polynomial degrees
    # survive reduction. Q(0)!=0 makes Q(z^2) and tQ(t) squarefree too.
    genera = {"u_curve": (50-2)//2, "t_quotient": (450-2)//2,
              "t_twist": (451-1)//2, "z_curve": (900-2)//2}
    assert genera == data["genera"]
    assert genera["t_quotient"] + genera["t_twist"] == genera["z_curve"]
    local = data["actual_local_example"]
    slope = a + 12
    physical_u = evaluate_integer_poly(A, slope*slope)/evaluate_integer_poly(B, slope*slope)
    assert physical_u == F(local["u"]) and physical_u > 0 and slope > a+10
    contact_valuations = {str(shift): valuation((a+shift)**2-slope*slope, 17) for shift in shifts}
    assert contact_valuations["-5"] == 1
    assert all(value == 0 for shift, value in contact_valuations.items() if shift != "-5")
    assert valuation(physical_u, 17) == 1
    assert fraction_residue(physical_u/17, 17) == 1
    assert (244*244-2) % 289 == 0
    successful = [(fraction_residue(value[0],289) + 244*fraction_residue(value[1],289)) % 289 for value in (c,d)]
    opposite = [(fraction_residue(value[0],17) + 11*fraction_residue(value[1],17)) % 17 for value in (c,d)]
    assert successful == [0,0] and opposite == [2,1]
    # At p=17 the successful slot has four factor corrections of valuation
    # >=7; the opposite slot has four factors of valuation -1. Thus the
    # reciprocal trace is 1 mod 17, and the radicand is also 1 mod 17.
    assert local["contact_trace_residue"] == local["contact_radicand_residue"] == 1
    # Independent finite-field evaluation at both roots of 2 modulo 31.
    assert fraction_residue(physical_u,31) == 9
    inverse_slots = []
    for rho in (8,23):
        assert rho*rho % 31 == 2
        product = 1
        for value in tests:
            ci = (fraction_residue(value[0],31)+rho*fraction_residue(value[1],31)) % 31
            denominator_mod = (1+9*ci*ci) % 31
            assert denominator_mod
            di = ci*ci*pow(denominator_mod,-1,31) % 31
            factor = (1+di*di*pow(9,-1,31)) % 31
            assert factor
            product = product*factor % 31
        inverse_slots.append(pow(product,-1,31))
    residue_V = sum(inverse_slots) % 31
    assert residue_V == 22
    assert fraction_residue(evaluate_integer_poly(N,F(9))/evaluate_integer_poly(D,F(9)),31) == residue_V
    residue_w = 9*pow(100,-1,31) % 31
    residue_C = (residue_V*residue_V+residue_w*(2-residue_V)) % 31
    assert (residue_w,residue_C,pow(residue_C,15,31)) == (19,11,30)
    assert [local[key] for key in ("u_mod_31","V_mod_31","w_mod_31","C_mod_31")] == [9,22,19,11]
    manuscript = args.source / "actual_trace_arithmetic_20261117_v70.tex"
    result = {
        "status": "PASS",
        "scope": "Exact selected actual point tuple and its algebraic covers; no prepared witness or completeness assertion.",
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "author_checker_sha256": sha256((args.source / "check.py").read_bytes()).hexdigest(),
        "author_certificate_sha256": sha256(source_bytes).hexdigest(),
        "manuscript_sha256_if_present": sha256(manuscript.read_bytes()).hexdigest() if manuscript.exists() else None,
        "independent_method": "Python standard library; exact Fraction arithmetic in Q(sqrt(2)); consecutive elliptic additions; direct six-factor reciprocal trace; direct finite-field power-sum composition; both Bezout identities plus Euclidean gcds.",
        "integer_polynomials_reconstructed": ["N", "D", "A_physical", "B_physical"],
        "degrees": {"N": 24, "D": 24, "A_physical": 9, "B_physical": 8, "u_polynomial": 50, "t_polynomial": 450, "z_polynomial": 900},
        "prime": prime,
        "bezout_checks": bezout_results,
        "genera": genera,
        "jacobian_dimension_check": "224+225=449",
        "local_example": {
            "slope": "z=a+12", "contact_factor_valuations_at_17": contact_valuations,
            "v17_u": 1, "u_over_17_mod_17": 1,
            "successful_slot_c_d_mod_289": successful,
            "opposite_slot_c_d_mod_17": opposite,
            "inverse_detector_slots_mod_31": inverse_slots,
            "u_V_w_C_mod_31": [9,22,19,11], "Legendre_C_mod_31": -1,
            "scope": "These small primes lie in the retained exceptional set; this is not full preparation or a realization counterexample."
        },
        "full_rational_lift_guard_check": "See independent_review.md; rational-point lifting was not attempted.",
    }
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "genera": genera,
                      "polynomials_reconstructed": len(result["integer_polynomials_reconstructed"]),
                      "prime": prime}, indent=2))


if __name__ == "__main__":
    main()
