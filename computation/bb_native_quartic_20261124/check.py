#!/usr/bin/env python3
"""Independent audit of BB-native 163/179 quartic tables.

Does not import build.py; re-derives every changed quadratic from the original
physical Laurent-weighted source, reconstructs the full quartic by an ordered
double convolution, tests the arithmetic model, and checks coefficient bounds.
Not an independent proof of the external Bhargava--Burungale/TYZ theorems.
"""
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OLD = ROOT / "computation/variable_reductions_v82/general"

TABLES = {
    "first": {3: 289, -34: 0, -289: -289, 17: 7},
    "middle": {17: 289, -1: -7, -17: -289},
    "second": {1: 289, 34: 0, -867: -289, -17: -7},
}


def kind(name):
    if name.endswith(".firstConic") or name == "v82.scalar.first":
        return "first"
    if name.endswith(".Bh.definition") or name == "v82.scalar.middle":
        return "middle"
    if name.endswith(".secondConic") or name == "v82.scalar.second":
        return "second"
    return None


def unit_products(n):
    # Independent transcription of the Laurent unit quotient library.
    units = [(0, 0, ()), (1, 0, (400,)), (-1, 0, (401,)),
             (-2, 0, (402,)), (0, 1, (113,)), (0, 2, (112,))]
    if n == 179:
        units.append((0, -1, (114,)))
    atoms = units[1:].copy()
    for a, b in product(atoms, repeat=2):
        z = (a[0] + b[0], a[1] + b[1], tuple(sorted(a[2] + b[2])))
        if z not in units:
            units.append(z)
    lookup = {}
    for c, r, mon in sorted(units, key=lambda x: (len(x[2]), x[2])):
        lookup.setdefault((c, r), mon)
    return lookup


def recompile_one(row, maps, n, mapping):
    """Rebuild a row from the uncompiled source terms, not from old quadrics."""
    index = {int(i): v for i, v in maps["source_labels"].items()}
    cw = {int(i): v for i, v in maps["c_weights"].items()}
    rw = {int(i): v for i, v in maps["R_weights"].items()}
    kw = {int(i): v for i, v in maps["parameter_weights"].items()}
    hc, hr = maps["row_c_R_weights"][row["name"]]
    rk = maps["row_parameter_weights"][row["name"]]
    units = unit_products(n)
    raw = defaultdict(int)
    for term in row["terms"]:
        coeff = int(term["coefficient"])
        if mapping is not None:
            assert coeff in mapping
            coeff = mapping[coeff]
        if not coeff:
            continue
        source_mon = term["monomial"]
        n2 = source_mon.count(112)
        rest = [i for i in source_mon if i != 112]
        cexp = term["c_power"] + sum(cw[i] for i in rest) - hc
        rexp = term["R_power"] + 2 * n2 + sum(rw[i] for i in rest) - hr
        kexp = term["parameter_power"] + sum(kw[i] for i in rest) - rk if n == 163 else 0
        assert (cexp, rexp) in units
        mon = tuple(sorted(index[i] for i in rest + list(units[cexp, rexp])))
        assert len(mon) <= 2 and kexp >= 0, (row["name"], mon, kexp)
        raw[kexp, mon] += coeff
    raw = {k: x for k, x in raw.items() if x}
    divisor = reduce(gcd, (abs(x) for x in raw.values()))
    return {k: x // divisor for k, x in raw.items()}


def dict_of(row):
    return {(int(t["parameterPower"]), tuple(t["monomial"])): int(t["coefficient"])
            for t in row["terms"]}


def arithmetic_fixture():
    d = Fraction(112, 841)
    b = Fraction(4624, 841)
    e, p, u, v, q = (Fraction(3, 4), Fraction(29, 16), Fraction(27, 29),
                       Fraction(81, 116), Fraction(27, 16))
    assert d == Fraction(7, 289) * b and 0 < b < 17
    assert e*e + d*p*p == 1
    assert u*v == e*(1-d)
    assert u*u-v*v == d*q*q
    sig = Fraction(3, 5)
    E, B, U, V = (sig*e, sig*b, sig*u, sig*v)
    P2, Q2 = sig*p*p, sig*q*q
    assert 289*E*E - 289*sig*sig + 7*B*P2 == 0
    assert 289*U*V - 289*E*sig + 7*E*B == 0
    assert 289*U*U - 289*V*V - 7*B*Q2 == 0
    # The original equations are not tautologically equivalent to these.
    assert 3*e*e-34*e-289+17*b*p*p != 0
    return str(b)


def check(n):
    source = json.loads((OLD / f"source{n}.json").read_text())
    maps = json.loads((OLD / f"quartic{n}/maps.json").read_text())
    old = json.loads((OLD / f"quartic{n}/quadrics.json").read_text())
    new = json.loads((HERE / f"quartic{n}/quadrics.json").read_text())
    polynomial = json.loads((HERE / f"quartic{n}/polynomial.json").read_text())
    assert old["variables"] == new["variables"] == polynomial["variables"] == n
    assert old["parameter"] == new["parameter"] == polynomial["parameter"]
    assert old["input"] == new["input"] == polynomial["input"] == 1
    assert len(old["residuals"]) == len(new["residuals"]) == {163:137,179:151}[n]
    oldby = {r["name"]: r for r in old["residuals"]}
    newby = {r["name"]: r for r in new["residuals"]}
    assert len(oldby) == len(newby)
    changed = []
    for sr in source["rows"]:
        k = kind(sr["name"])
        if k is None:
            continue
        assert sr["name"].startswith("detector") or sr["name"].startswith("v82.scalar.")
        old_row = oldby[sr["name"]]
        new_row = newby["bbnative."+sr["name"]]
        assert recompile_one(sr, maps, n, None) == dict_of(old_row), sr["name"]
        assert recompile_one(sr, maps, n, TABLES[k]) == dict_of(new_row), sr["name"]
        changed.append(sr["name"])
    assert len(changed) == {163:9,179:12}[n]
    for o, r in zip(old["residuals"], new["residuals"]):
        if o["name"] in changed:
            assert r["name"] == "bbnative."+o["name"]
        else:
            assert o == r, o["name"]

    # Independently expand ordered pairs, not the producer's triangular sum.
    coeffs = defaultdict(int)
    for r in new["residuals"]:
        for a in r["terms"]:
            for b in r["terms"]:
                term = (a["parameterPower"]+b["parameterPower"],
                        tuple(sorted(a["monomial"]+b["monomial"])))
                coeffs[term] += int(a["coefficient"]) * int(b["coefficient"])
    coeffs = {k: v for k, v in coeffs.items() if v}
    stored = {(int(t["parameterPower"]), tuple(t["monomial"])): int(t["coefficient"])
              for t in polynomial["terms"]}
    assert coeffs == stored
    assert len(stored) == {163:2771,179:3012}[n]
    assert len({mon for _, mon in stored}) == len(stored)
    assert max(len(mon) for _, mon in stored) == 4
    assert reduce(gcd, (abs(c) for c in stored.values())) == 1
    maximum = max(abs(c) for c in stored.values())
    if n == 163:
        assert maximum == 126616122944180358034867798936
        assert {(k,m): c for (k,m), c in stored.items() if k} == {
            (2, (78,78,90)): -6615898, (2, (78,90)): -298,
            (4, (78,78)): 22201}
        # For C=149^N and N>=1, the last term dominates the other C terms:
        assert 6615898 < 22201*(149**2)
        assert 298 < 22201*(149**2)
    else:
        base=645904574641049503754777843805872291231896003979
        boost=14904184670611231
        assert maximum == (base*boost**4)**2 and maximum.bit_length() == 748
    return n, len(new["residuals"]), len(stored), len(changed), maximum.bit_length()


if __name__ == "__main__":
    print("arithmetic fixture b =", arithmetic_fixture())
    for n in (163, 179):
        print("PASS: N, rows, monomials, changed rows, max bits =", check(n))
