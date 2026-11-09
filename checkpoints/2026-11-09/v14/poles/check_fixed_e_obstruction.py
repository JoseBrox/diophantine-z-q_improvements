#!/usr/bin/env python3
"""Exact pole-specialization obstruction, using PARI's unconditional ellrank.

All non-rank calculations use the Python standard library.  PARI performs
2-descent and the 2-part of the Cassels pairing; analytic ranks and BSD
are not used.  The --rank-log mode retains the exact descent diagnostics.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import json
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "v13/number_fields/python"))
from cypari2 import Pari

pari = Pari()
pari.allocatemem(128000000, silent=True)
pari.setrand(1)

if "--rank-log" in sys.argv:
    pari("default(debug,3)")
    for n in (-29427, 9809):
        print("CURVE", n, flush=True)
        E = pari.ellinit([0, 2*n, 0, -3*n*n, 0])
        print("RANK_RESULT", pari.ellrank(E), flush=True)
    raise SystemExit(0)


def vp_int(n, p):
    assert n
    n, v = abs(n), 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def local_square_data(x, p):
    x = F(x)
    assert x
    a, b = x.numerator, x.denominator
    va, vb = vp_int(a, p), vp_int(b, p)
    v = va-vb
    a //= p**va
    b //= p**vb
    modulus = 8 if p == 2 else p
    unit = a * pow(b, -1, modulus) % modulus
    square = v % 2 == 0 and (unit == 1 if p == 2 else pow(unit, (p-1)//2, p) == 1)
    return {"valuation": v, "unit_modulus": modulus, "unit": unit, "is_square": square}


def prepared(b):
    assert 0 < b < 17 and isqrt(b.denominator)**2 == b.denominator
    local = {str(p): local_square_data(b, p) for p in (2, 3, 17)}
    assert all(row["is_square"] for row in local.values())
    assert [local[str(p)]["valuation"] for p in (2, 3, 17)] == [4, 2, 2]
    return {"b": str(b), "square_denominator_root": isqrt(b.denominator), "local": local}


def curve_count(n, p):
    assert (6*n) % p != 0
    freq = [0]*p
    for y in range(p):
        freq[y*y % p] += 1
    return 1 + sum(freq[x*(x-n)*(x+3*n) % p] for x in range(p))


def rank_f2(matrix):
    rows = [sum((x % 2) << i for i, x in enumerate(row)) for row in matrix]
    rank = 0
    for bit in range(len(matrix[0])):
        pivot = next((j for j in range(rank, len(rows)) if rows[j] >> bit & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for j in range(len(rows)):
            if j != rank and rows[j] >> bit & 1:
                rows[j] ^= rows[rank]
        rank += 1
    return rank


def squareclass(n):
    result = -1 if n < 0 else 1
    n = abs(n)
    p = 2
    while p*p <= n:
        parity = 0
        while n % p == 0:
            n //= p
            parity ^= 1
        if parity:
            result *= p
        p += 1
    return result*n


M, t, d = 55, F(204, 55), 577
b0, b1 = t*t, F(409*204**2, 1001**2)
prep = [prepared(b) for b in (b0, b1)]
assert d == M*M-2448 and 204**2 == 17*2448
assert all(409 % p for p in range(2, isqrt(409)+1))
assert squareclass(409) == 409
assert b1 / b0 == F(409*55**2, 1001**2)

# Direct polynomial-coefficient verification of the two substitutions.
B = 17*b0
V = B*(B-b0*b0)
maps = []
for e, scale in ((F(1), 1), (F(-1, 3), 3)):
    scoef = 17*t*t/(scale*M)
    qcoef = 17*t**3/(scale*scale*M*M)
    lhs = B*qcoef*qcoef
    normalized = [(-3*e*e*V*V)/lhs, (2*e*V*scoef*scoef)/lhs, scoef**4/lhs]
    expected = ([-51*d*d, 34*d, 17] if e == 1 else [-459*d*d, -102*d, 17])
    assert normalized == expected
    n = 17*d if e == 1 else -51*d
    # x=17u², y=17uv sends v²=17(u²-n/17)(u²+3n/17) to E_n.
    assert F(n, 17) == (d if e == 1 else -3*d)
    maps.append({"e": str(e), "s_coefficient": str(scoef), "q_coefficient": str(qcoef),
                 "quartic_coefficients_ascending_in_u_squared": list(map(int, expected)), "elliptic_parameter": n})

# Exact ranks and independent finite-field torsion bounds.
curves = []
for n, expected in ((-29427, (0, 0, 2)), (9809, (1, 1, 2))):
    E = pari.ellinit([0, 2*n, 0, -3*n*n, 0])
    result = pari.ellrank(E)
    assert tuple(int(result[i]) for i in range(3)) == expected
    counts = {str(p): curve_count(n, p) for p in (5, 7, 11, 13)}
    bound = 0
    for cardinality in counts.values():
        bound = gcd(bound, cardinality)
    assert bound == 4
    torsion = [[0, 0], [n, 0], [-3*n, 0]]
    assert all(y*y == x*(x-n)*(x+3*n) for x, y in torsion)
    curves.append({"parameter": n, "coefficients": [0, 2*n, 0, -3*n*n, 0],
                   "ellrank": str(result), "rank_lower": expected[0], "rank_upper": expected[1],
                   "sha_pairing_rank": expected[2], "good_prime_counts": counts,
                   "torsion_order_upper_bound": bound, "nonidentity_two_torsion": torsion})

P = (-20449, 2356926)
assert P[1]**2 == P[0]*(P[0]-9809)*(P[0]+3*9809)
assert -P[0] == 143**2 and P[1] != 0
classes = sorted({squareclass((-1)**a * (-3)**b * 9809**c) for a, b, c in product(range(2), repeat=3)})
assert len(classes) == 8 and 17 not in classes
assert squareclass(88281) == 9809 and 9809 != 17

# Both obstructed quartics are soluble at every completion.  Good reduction
# outside 2,3,17,577 and Hasse's bound handle the other finite places.
local_witnesses = {}
for e, witnesses in (("1", {2:23, 3:1, 17:4, 577:1}), ("-1/3", {2:21, 3:12, 17:22, 577:1})):
    rows = {}
    for p, u in witnesses.items():
        rhs = 17*(u*u-d)*(u*u+3*d) if e == "1" else 17*(u*u+3*d)*(u*u-9*d)
        data = local_square_data(rhs, p)
        assert data["is_square"]
        rows[str(p)] = {"u": u, "right_hand_side": rhs, **data}
    real_rhs = 17*(10000-d)*(10000+3*d) if e == "1" else 17*(10000+3*d)*(10000-9*d)
    assert real_rhs > 0
    rows["real"] = {"u": 100, "right_hand_side_positive": True}
    local_witnesses[e] = rows

# Save and parse exact descent diagnostics, including Cassels matrices.
run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--rank-log"], capture_output=True, text=True, check=True)
log = run.stdout + run.stderr
(HERE / "fixed-e-pari-descent.log").write_text(log)
selmer = list(map(int, re.findall(r"Selmer rank: (\d+)", log)))
matrices = []
for raw in re.findall(r"Cassels Pairing: \[([^\]]+)\]", log):
    matrices.append([[int(x.strip()) for x in row.split(",")] for row in raw.split(";")])
assert selmer == [4, 5] and len(matrices) == 2
for i, matrix in enumerate(matrices):
    assert rank_f2(matrix) == 2
    assert all(matrix[j][j] == 0 for j in range(len(matrix)))
    assert all(matrix[j][k] == matrix[k][j] for j in range(len(matrix)) for k in range(len(matrix)))
    assert selmer[i] - 2 - rank_f2(matrix) == curves[i]["rank_upper"]
    curves[i]["two_selmer_rank"] = selmer[i]
    curves[i]["cassels_pairing_matrix"] = matrix
    curves[i]["pairing_rank_independently_checked_over_F2"] = 2

certificate = {
    "status": "PASS", "pari_version": str(pari("version()")),
    "scope": "No constant rational e gives a complete zero-preparation pole specialization. The rank bounds use unconditional PARI 2-descent and Cassels pairings; no analytic rank or BSD assumption is used.",
    "prepared_inputs": prep, "maps": maps, "elliptic_curves": curves,
    "known_infinite_order_point_on_E9809": list(P),
    "complete_x_squareclass_image_on_E9809": classes,
    "required_squareclass_absent": 17,
    "everywhere_local_witnesses": local_witnesses,
    "good_reduction_outside": [2, 3, 17, 577],
    "rank_documentation": "https://pari.math.u-bordeaux.fr/dochtml/html/Elliptic_curves.html#ellrank",
}
output = HERE / "fixed-e-obstruction-certificate.json"
output.write_text(json.dumps(certificate, indent=2) + "\n")
print(json.dumps({"status": "PASS", "certificate": str(output), "rank_bounds": [[r['rank_lower'],r['rank_upper']] for r in curves], "all_fixed_e_obstructed": True}, indent=2))
