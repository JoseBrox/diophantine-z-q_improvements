"""Exact identities for the single quartic chart in a quadratic extension.

Only the Python standard library is required. All identities are checked
in a sparse Laurent polynomial ring over Q; clearing a power of the fixed
nonzero parameter d turns the general identities into polynomial identities.
The nonvanishing conclusions are mathematical consequences of the stated
nonsquare and noncube hypotheses, not conclusions of numerical sampling.
"""

from fractions import Fraction
from pathlib import Path
import hashlib
import json


class Poly:
    names = ("u", "v", "U", "V", "d", "kappa", "Y")
    n = len(names)

    def __init__(self, terms):
        if isinstance(terms, (int, Fraction)):
            terms = {(0,) * self.n: Fraction(terms)}
        self.terms = {m: Fraction(c) for m, c in terms.items() if c}

    @classmethod
    def monomial(cls, name, exponent=1):
        powers = [0] * cls.n
        powers[cls.names.index(name)] = exponent
        return cls({tuple(powers): 1})

    @classmethod
    def coerce(cls, other):
        return other if isinstance(other, cls) else cls(other)

    def __add__(self, other):
        other = self.coerce(other)
        out = dict(self.terms)
        for powers, coefficient in other.terms.items():
            out[powers] = out.get(powers, 0) + coefficient
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        out = {}
        for m, c in self.terms.items():
            for n, e in other.terms.items():
                powers = tuple(a + b for a, b in zip(m, n))
                out[powers] = out.get(powers, 0) + c * e
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        out = Poly(1)
        for _ in range(exponent):
            out *= self
        return out

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def degree(self):
        assert all(all(e >= 0 for e in m) for m in self.terms)
        return max(map(sum, self.terms), default=-1)

    def integer_height(self):
        assert all(c.denominator == 1 for c in self.terms.values())
        return max((abs(c.numerator) for c in self.terms.values()), default=0)


u, v, U, V, d, k, Y = [Poly.monomial(n) for n in Poly.names]
dinv = Poly.monomial("d", -1)
q = Fraction

# General formulas: independently expand the two components after replacing
# U and V by the components of (u+v*rho)^2.
Us = u**2 + d * v**2
Vs = 2 * u * v
asub = Us + q(1, 2) * k * dinv * Vs
bsub = -k * dinv**2 * Us - q(1, 2) * Vs
assert asub * u + d * bsub * v == u**3 - k * v**3
assert asub * v + bsub * u == d * v**3 - k * dinv**2 * u**3

a = U + q(1, 2) * k * dinv * V
b = -k * dinv**2 * U - q(1, 2) * V
assert a**2 - d * b**2 == q(1, 4) * (d**3 - k**2) * dinv**3 * (4 * U**2 - d * V**2)
det = -q(1, 2) + q(1, 2) * k**2 * dinv**3
assert 2 * d**3 * det == k**2 - d**3

# Compare multiplication with independently stated expanded cubics.
A = (a**2 + d * b**2) * U + 2 * d * a * b * V
B = (a**2 + d * b**2) * V + 2 * a * b * U
Aexpanded = (1 + k**2 * dinv**3) * U**3 - q(3, 4) * (d + k**2 * dinv**2) * U * V**2 - q(1, 2) * k * V**3
Bexpanded = -2 * k * dinv**2 * U**3 + q(3, 2) * k * dinv * U * V**2 + q(1, 4) * (k**2 * dinv**2 + d) * V**3
assert A == Aexpanded
assert B == Bexpanded

# Clear the Y denominator in the reconstructed square identity.
J = Y**4 - 4 * A * Y**2 + 4 * d * B**2
assert Y**4 + 4 * d * B**2 - 4 * A * Y**2 == J
assert 4 * (2 * u)**3 - 8 * (u**2 + d * v**2) * (2 * u) == 8 * (2 * u) * (u**2 - d * v**2)

# Integer-scaled Q(sqrt(2)) presentation, checked without substituting the
# preceding general cubics or reusing their derived coefficients.
a2, b2 = 2 * U + V, -(U + V)
A2 = 6 * U**3 - 9 * U * V**2 - 4 * V**3
B2 = -4 * U**3 + 6 * U * V**2 + 3 * V**3
assert a2**2 - 2 * b2**2 == 2 * U**2 - V**2
assert (a2**2 + 2 * b2**2) * U + 4 * a2 * b2 * V == A2
assert (a2**2 + 2 * b2**2) * V + 2 * a2 * b2 * U == B2
U2, V2 = u**2 + 2 * v**2, 2 * u * v
assert (2 * U2 + V2) * u - 2 * (U2 + V2) * v == 2 * (u**3 - 2 * v**3)
assert (2 * U2 + V2) * v - (U2 + V2) * u == 4 * v**3 - u**3
J2 = Y**4 - 4 * A2 * Y**2 + 8 * B2**2
reciprocal = 1 - 4 * A2 * Y**2 + 8 * B2**2 * Y**4
zero_inclusive = (U**2 - 2 * V**2) * reciprocal
zero_inclusive_product = (2 - 2 * U * Y**2 + V**2 * Y**4) * (V**2 + (U - 2 * Y**2)**2)
assert J2.degree() == 6
assert reciprocal.degree() == 10
assert zero_inclusive.degree() == 12
assert zero_inclusive_product.degree() == 10
assert zero_inclusive_product.integer_height() == 8
assert len(zero_inclusive_product.terms) == 12

report = {
    "status": "PASS",
    "arithmetic": "exact sparse Laurent polynomial arithmetic over Q",
    "general_assumptions": "char(F)=0; d nonsquare; kappa noncube; (U,V) nonzero",
    "identities_checked": [
        "general transformed rational and irrational components",
        "general multiplier norm and determinant",
        "general expanded transformed-square cubics",
        "quartic reconstruction after clearing the root denominator",
        "derivative equals 8*Y*Norm(z_prime)",
        "independently expanded Q(sqrt(2)) formulas",
    ],
    "rational_specialization": {
        "d": 2,
        "kappa": 2,
        "a": "2*U+V",
        "b": "-U-V",
        "A": "6*U^3-9*U*V^2-4*V^3",
        "B": "-4*U^3+6*U*V^2+3*V^3",
        "quartic": {"degree_in_Y": 4, "total_degree": J2.degree(), "monomials": len(J2.terms), "coefficient_height": J2.integer_height()},
        "nonzero_square_test": {"total_degree": reciprocal.degree(), "monomials": len(reciprocal.terms), "coefficient_height": reciprocal.integer_height()},
        "zero_inclusive_square_test": {"total_degree": zero_inclusive.degree(), "monomials": len(zero_inclusive.terms), "coefficient_height": zero_inclusive.integer_height()},
        "zero_inclusive_low_height_product": {"total_degree": zero_inclusive_product.degree(), "degree_in_quantified_variable": 8, "monomials": len(zero_inclusive_product.terms), "coefficient_height": zero_inclusive_product.integer_height()},
    },
    "proof_boundary": "Nonvanishing uses the proved nonsquare/noncube argument; no finite search is substituted for it.",
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
target = Path(__file__).with_name("quadratic-square-chart-certificate.json")
target.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
