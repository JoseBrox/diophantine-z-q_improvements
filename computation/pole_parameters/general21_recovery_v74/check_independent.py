#!/usr/bin/env python3
"""Verify the scale-two coprimality certificate using integer lists only."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def trim(f):
    while len(f) > 1 and f[-1] == 0:
        f.pop()
    return f


def add(f, g, p):
    h = [0] * max(len(f), len(g))
    for i, c in enumerate(f):
        h[i] = (h[i] + c) % p
    for i, c in enumerate(g):
        h[i] = (h[i] + c) % p
    return trim(h)


def mul(f, g, p):
    h = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            h[i + j] = (h[i + j] + a * b) % p
    return trim(h)


def derivative(f, p):
    return trim([i * c % p for i, c in enumerate(f)][1:])


cert = json.loads((HERE / "certificate.json").read_text())
c = cert["same_pole_scale_two_certificate"]
p = c["prime"]
f = list(reversed(c["derivative0_mod_p_descending"]))
g = list(reversed(c["derivative1_mod_p_descending"]))
e = list(reversed(c["bezout_e_descending"]))
k = list(reversed(c["bezout_k_descending"]))
q0 = [int(v) % p for v in reversed(c["q0_integer_descending"])]
q1 = [int(v) % p for v in reversed(c["q1_integer_descending"])]
assert len(q0) == len(q1) == 11 and q0[-1] and q1[-1]
assert derivative(q0, p) == f and derivative(q1, p) == g
assert len(f) == len(g) == 10 and f[-1] and g[-1]
assert add(mul(e, f, p), mul(k, g, p), p) == [1]
out = {
    "status": "PASS",
    "method": "Independent Python integer-list derivative and convolution arithmetic",
    "prime": p,
    "degree_preserved": 9,
    "derivative_bezout_value": [1],
    "scope": "Scale-two coprimality certificate; not rational realization",
}
(HERE / "independent_certificate.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out))
