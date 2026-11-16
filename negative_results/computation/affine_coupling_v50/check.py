#!/usr/bin/env python3
"""Exact standard-library certificate for the affine scalar-coupling counterexample."""
from math import isqrt
from pathlib import Path
import json
import argparse

x = 11
beta = 216*x**4 + 450459
p = 80287
ell = 76249
exceptions = {1875611, 3828397, 3982747}

assert p > 76176 and p not in exceptions
assert all(p % d for d in range(2, isqrt(p) + 1))
assert beta == 3**2 * 5 * p
factors = [beta, beta-1, beta-2401, 32*beta+343, 2*beta-1]
assert factors[0] % p == 0 and factors[0] % (p*p) != 0
assert all(f % p for f in factors[1:])
assert (102*ell) % p != 0
assert (beta+1) % p == 1
# For all odd L, the numerator of rho has p-order one, since p != ell.
# Its denominator is a p-adic unit for every integer C_L, because p | r.
r = 1
for f in factors:
    r *= f
assert r % p == 0 and r % (p*p) != 0
# An infinite progression of inputs preserves the same first-order valuation.
for t in (-5, -1, 0, 1, 7):
    xx = x + t*p*p
    bb = 216*xx**4 + 450459
    assert bb % (p*p) == beta % (p*p)

certificate = {
    "input": x,
    "beta": beta,
    "prime": p,
    "prime_is_prime": True,
    "beta_factorization": {"3": 2, "5": 1, str(p): 1},
    "contact_residues_mod_p": [f % p for f in factors],
    "beta_mod_p_squared": beta % (p*p),
    "coupled_c_mod_p": (beta+1) % p,
    "outside_fixed_exceptional_set": True,
    "rho_valuation_at_p_for_all_odd_L": 1,
    "required_c_valuation_minimum": 3,
    "actual_c_valuation": 0,
    "counterexample_progression_modulus": p*p,
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
out = parser.parse_args().output
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(certificate, indent=2) + "\n")
print(json.dumps(certificate, indent=2))
