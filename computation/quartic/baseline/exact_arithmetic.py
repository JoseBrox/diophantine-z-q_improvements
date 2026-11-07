"""Exact rational polynomial arithmetic for the independent certificates."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from itertools import combinations_with_replacement
from math import gcd, lcm
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_terms(terms):
    p = {}
    for t in terms:
        m = tuple(t["monomial"])
        assert m == tuple(sorted(m))
        key = (m, t.get("sPower", 0))
        assert key not in p, "Repeated monomial/parameter pair in emitted table"
        p[key] = Q(t["coefficient"])
        assert p[key]
    return p


def normalize(p):
    denominator = 1
    for a in p.values():
        denominator = lcm(denominator, a.denominator)
    content = 0
    for a in p.values():
        content = gcd(content, abs(a.numerator * (denominator // a.denominator)))
    factor = Q(denominator, content)
    return {k: a * factor for k, a in p.items()}, factor


def sos(polynomials):
    result = defaultdict(Q)
    for p in polynomials:
        terms = list(p.items())
        for i, j in combinations_with_replacement(range(len(terms)), 2):
            (m, s), a = terms[i]
            (n, t), b = terms[j]
            result[(tuple(sorted(m + n)), s + t)] += a * b * (1 if i == j else 2)
    return {k: a for k, a in result.items() if a}


def valuation(q, prime):
    q = Q(q)
    assert q
    a, b = abs(q.numerator), q.denominator
    v = 0
    while a % prime == 0:
        a //= prime
        v += 1
    while b % prime == 0:
        b //= prime
        v -= 1
    return v


def add(*parts):
    out = defaultdict(Q)
    for factor, p in parts:
        for key, a in p.items():
            out[key] += factor * a
    return {key: a for key, a in out.items() if a}


def product(a, b):
    out = defaultdict(Q)
    for (m, s), x in a.items():
        for (n, t), y in b.items():
            out[(tuple(sorted(m+n)), s+t)] += x*y
    return {key: a for key, a in out.items() if a}


def fm(a, b):
    return [add((1, product(a[0], b[0])), (2, product(a[1], b[1]))),
            add((1, product(a[0], b[1])), (1, product(a[1], b[0])))]

