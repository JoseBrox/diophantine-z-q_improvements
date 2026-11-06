#!/usr/bin/env python3
"""Exact polynomial checks for quadratic square-root coordinate elimination.

This uses a tiny integer polynomial implementation, with no dependencies.
It checks identities in Z[b0,b1,j,delta] and in Z[A,B,C,j,delta].
The proof that these identities yield a chart equivalence (C != 0 and
j^2 != delta) is supplied in square_root_compression.tex.
"""

import json
from collections import defaultdict


class Poly:
    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def constant(cls, n, c):
        return cls(n, {(0,) * n: c})

    @classmethod
    def var(cls, n, k):
        m = [0] * n
        m[k] = 1
        return cls(n, {tuple(m): 1})

    def coerce(self, x):
        return x if isinstance(x, Poly) else Poly.constant(self.n, x)

    def __add__(self, other):
        other = self.coerce(other)
        out = defaultdict(int, self.terms)
        for m, c in other.terms.items():
            out[m] += c
        return Poly(self.n, out)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        out = defaultdict(int)
        for m, c in self.terms.items():
            for n, d in other.terms.items():
                out[tuple(a + b for a, b in zip(m, n))] += c * d
        return Poly(self.n, out)

    __rmul__ = __mul__

    def __pow__(self, k):
        out = Poly.constant(self.n, 1)
        for _ in range(k):
            out = out * self
        return out


def assert_zero(p):
    assert not p.terms, p.terms


def gamma(A, B, C, j, delta):
    return (4 * delta * C**4
            - 4 * ((j**2 + delta) * A + 2 * j * delta * B) * C**2
            + (2 * j * A + (j**2 + delta) * B)**2)


def reduce_w_square(p):
    """Reduce in Z[v,w]/(w^2+v^2-2), for a two-variable polynomial."""
    assert p.n == 2
    v, w = [Poly.var(2, k) for k in range(2)]
    result = Poly.constant(2, 0)
    for (a, b), c in p.terms.items():
        result += c * v**a * w**(b % 2) * (2 - v**2)**(b // 2)
    return result


def main():
    # General coefficient identity, not a finite sample.
    A, B, C, j, delta = [Poly.var(5, k) for k in range(5)]
    lam = j**2 - delta
    U = C**2 - A - j * B
    G = gamma(A, B, C, j, delta)
    assert_zero(G + 4 * lam * C**2 * U - (lam * B + 2 * j * U)**2)

    # The advertised norm and inverse formulas are polynomial identities
    # modulo Gamma, so denominator guards are the only remaining domain issue.
    L = (j**2 + delta) * A + 2 * j * delta * B
    H = 2 * j * A + (j**2 + delta) * B
    assert_zero(L**2 - delta * H**2 - lam**2 * (A**2 - delta * B**2))
    assert_zero((L - 2 * delta * C**2)**2
                - lam**2 * (A**2 - delta * B**2) - delta * G)

    # Substitute an arbitrary true square and verify Gamma identically.
    b0, b1, j, delta = [Poly.var(4, k) for k in range(4)]
    A = b0**2 + delta * b1**2
    B = 2 * b0 * b1
    C = b0 + j * b1
    lam = j**2 - delta
    assert_zero(gamma(A, B, C, j, delta))
    assert_zero(C**2 - A - j * B - lam * b1**2)
    assert_zero(2 * C * b1 - B - 2 * j * b1**2)
    n0 = -2 * delta * C**2 + 2 * j**2 * A + j * (j**2 + delta) * B
    n1 = 2 * j * C**2 - 2 * j * A - (j**2 + delta) * B
    assert_zero(n0 - 2 * lam * C * b0)
    assert_zero(n1 - 2 * lam * C * b1)

    # Exact inverse maps between the full point chart and a halfpoint.
    v, w = [Poly.var(2, k) for k in range(2)]
    A = (1 + v) * (1 + w)
    S = v + w
    N = 1 - v**2
    assert_zero(reduce_w_square(A * (S**2 - A) + N**2))
    assert_zero(reduce_w_square(A**2 + N**2 - 2 * S * A))
    assert_zero(reduce_w_square(A**2 - 2 * N * A - N**2 - 2 * v * S * A))
    assert_zero(reduce_w_square(A**2 + 2 * N * A - N**2 - 2 * w * S * A))

    print(json.dumps({
        "result": "verified",
        "identities": 12,
        "method": "exact polynomial identities over Z; no numerical sampling",
        "generalization": "arbitrary nonsquare delta over a field of characteristic different from 2",
        "required_guards": ["C != 0", "j^2-delta != 0"],
        "scope": "Quadratic square-root elimination and inverse full-chart/halfpoint identities, not certification of the complete integer-definition polynomial"
    }, indent=2))


if __name__ == "__main__":
    main()
