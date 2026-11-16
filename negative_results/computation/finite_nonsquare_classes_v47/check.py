#!/usr/bin/env python3
"""Exact certificate for the v47 native two-detector class obstruction.

Python standard library only. This checks explicit arithmetic certificates,
source-file hashes, three quartic fields, and contact reductions. The general
Chebotarev/CRT proof is in the manuscript, not inferred from finite sampling.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
import json
from math import gcd, isqrt, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def prime(n):
    if n < 2:
        return False
    return all(n % a for a in range(2, isqrt(n) + 1))


def legendre(d, p):
    z = pow(d % p, (p - 1) // 2, p)
    assert z in (0, 1, p - 1)
    return -1 if z == p - 1 else z


def residue(x, p):
    return x.numerator * pow(x.denominator, -1, p) % p


def crt(rows):
    x, modulus = 0, 1
    for a, m in rows:
        assert gcd(modulus, m) == 1
        x += modulus * (((a - x) * pow(modulus, -1, m)) % m)
        modulus *= m
        x %= modulus
    return x, modulus


theta = list(map(Fraction, [0, -1])) + [Fraction(-1, 2), Fraction(1, 2399), Fraction(-32, 407)]
contacts = [[Fraction(4*j+k)+q for k in (2, 4) for q in theta] for j in (0, 1)]
poles = [Fraction(-1), Fraction(-2)]
assert set(contacts[1]) == {x + 4 for x in contacts[0]}
assert min(contacts[0]) > 0
assert 1 + 4/min(contacts[0]) != 1 + 4/max(contacts[0])
assert prime(50051)
assert 50051 % 24 != 0
assert Fraction(300306, 144) == Fraction(50051, 24)
assert not (isqrt(50051)**2 == 50051 and isqrt(24)**2 == 24)

# Three distinct imaginary quadratic subfields suffice for every signed pair.
field_certificates=[]
radicand_factors={300306:[2,3,50051],675687:[3,79,2851],672087:[3,13,19,907]}
for theta,eisenstein,squarefree in ((0,50051,300306),(1,79,675687),(2401,13,672087)):
    constant=450459-theta
    q=Fraction(constant,216)
    assert prime(eisenstein) and 216%eisenstein
    factors=radicand_factors[squarefree]
    assert len(set(factors))==len(factors) and all(prime(p) for p in factors)
    assert prod(factors)==squarefree
    assert constant%eisenstein==0 and constant%(eisenstein*eisenstein)!=0
    ratio=q/Fraction(squarefree)
    assert isqrt(ratio.numerator)**2==ratio.numerator
    assert isqrt(ratio.denominator)**2==ratio.denominator
    assert not (isqrt(q.numerator)**2==q.numerator and isqrt(q.denominator)**2==q.denominator)
    field_certificates.append({"contact":theta,"quartic_coefficients":[216,0,0,0,constant],
                               "Eisenstein_prime":eisenstein,
                               "norm_alpha_squared":str(q),
                               "negative_radicand_prime_factors":factors,
                               "unique_quadratic_subfield":f"Q(sqrt(-{squarefree}))"})
assert len({row["unique_quadratic_subfield"] for row in field_certificates})==3

classes = [409, 433, 409*433]
data = [(76511, 31907), (76607, 16455), (76403, 46968)]
rows = []
for p, x in data:
    assert prime(p) and p > 76176
    assert p not in (76249, 1875611, 3828397, 3982747)
    assert all(d % p for d in classes)
    g = 24*x**4 + 50051
    assert g % p == 0 and g % (p*p) != 0
    assert 96*x**3 % p != 0
    beta = 216*x**4 + 450459
    assert beta == 9*g
    factors = [beta, beta-1, beta-2401, 32*beta+343, 2*beta-1]
    assert factors[0] % p == 0 and all(f % p for f in factors[1:])
    r = 1
    for f in factors:
        r = r*f % (p*p)
    assert r % p == 0 and r != 0
    assert 102*76249 % p != 0
    # Thus the numerator of rho has valuation one, and its denominator
    # is 1 modulo p for every L, without evaluating an enormous power.
    reductions = [{residue(t, p) for t in contacts[j]+[poles[j]]} for j in (0, 1)]
    assert all(len(s) == 11 and 0 not in s for s in reductions)
    assert reductions[0].isdisjoint(reductions[1])
    chars = {str(d): legendre(d, p) for d in classes}
    rows.append({
        "prime": p, "input_residue_mod_prime_squared": x,
        "modulus": p*p, "g_over_p_mod_p": g//p % p,
        "g_derivative_mod_p": 96*x**3 % p,
        "r_over_p_mod_p": r//p, "class_characters": chars,
        "contacts_nonzero_distinct_and_disjoint": True,
        "rho_valuation_for_every_odd_L": 1,
    })

coverage = []
for a, b in combinations_with_replacement(classes, 2):
    witnesses = [row["prime"] for row in rows
                 if row["class_characters"][str(a)] == -1
                 and row["class_characters"][str(b)] == -1]
    assert witnesses
    coverage.append({"classes": [a, b], "primes": witnesses})

x0, mod = crt([(x, p*p) for p, x in data])
assert all(x0 % (p*p) == x for p, x in data)
source_names = [
    "papers/finite_algebra/unit_norm_20261114_v28.tex",
    "papers/few_variables25/few_variables25_merged_20261110_v19.tex",
    "papers/pole_parameters/finite_complement_classes_20261116_v46.tex",
]
source_hashes = {name: sha256((REPO/name).read_bytes()).hexdigest() for name in source_names}
source_text = (REPO/source_names[0]).read_text()
assert "a_1=1+\\rho T^2" in source_text
assert "b_j&=w_j" in source_text

certificate = {
    "schema": "finite-nonsquare-native-class-obstruction/v47",
    "status": "PASS",
    "scope": "Arbitrary guarded rational source tuples; current unsquared general25 source only",
    "uniform_in": ["all odd L >= 3", "all rational slopes and auxiliary indices", "all nonzero rational m in levels17m^2"],
    "excluded_claims": ["no obstruction to using class 1", "no new variable count", "no claim about conditional13 weights"],
    "classes": classes,
    "prime_certificates": rows,
    "pair_coverage": coverage,
    "integer_input_progression": {"residue": x0, "modulus": mod},
    "two_class_example": {"classes": [409, 433], "prime": 76511,
                          "input": 31907, "progression_modulus": 76511**2},
    "field_certificates": field_certificates,
    "theorem_class_scope": "Every finite set of nontrivial rational squareclasses, including negative classes",
    "source_sha256": source_hashes,
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output",type=Path)
args=parser.parse_args()
encoded=json.dumps(certificate,indent=2)+"\n"
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(encoded)
else:
    assert (HERE/"certificate.json").read_text()==encoded, "Committed certificate differs"
print(json.dumps({"status":"PASS","classes_in_exact_example":classes,
                  "input_progression":certificate["integer_input_progression"],
                  "quartic_fields":len(field_certificates),"pair_count":len(coverage)},indent=2))
