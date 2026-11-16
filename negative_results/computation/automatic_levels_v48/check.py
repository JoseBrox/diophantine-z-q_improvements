#!/usr/bin/env python3
"""Exact certificates for automatic-level local obstruction and its fixtures.

The all-prime argument and Faltings finiteness are proved in the accompanying
paper; the finite valuation screen is supplementary, not a substitute for them.
This checker imports no earlier detector producer.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import sympy as sp


@dataclass(frozen=True)
class K:
    a: Q = Q(0)
    b: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, "a", Q(self.a))
        object.__setattr__(self, "b", Q(self.b))

    @staticmethod
    def co(z):
        return z if isinstance(z, K) else K(z)

    def __add__(self, z):
        z = K.co(z)
        return K(self.a + z.a, self.b + z.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, z):
        return self + -K.co(z)

    def __rsub__(self, z):
        return K.co(z) + -self

    def __mul__(self, z):
        z = K.co(z)
        return K(self.a*z.a + 2*self.b*z.b, self.a*z.b + self.b*z.a)

    __rmul__ = __mul__

    def norm(self):
        return self.a*self.a - 2*self.b*self.b

    def bar(self):
        return K(self.a, -self.b)

    def inverse(self):
        n = self.norm()
        assert n
        return K(self.a/n, -self.b/n)

    def __truediv__(self, z):
        return self*K.co(z).inverse()

    def __rtruediv__(self, z):
        return K.co(z)*self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse()**(-n)
        z, b = K(1), self
        while n:
            if n & 1:
                z *= b
            b *= b
            n //= 2
        return z


D = K(11, -6)
R0 = K(1, 1), K(0, 2)
THETA = [Q(0), Q(-1, 2), Q(-1, 4), Q(-2, 5), Q(-1), Q(-1, 3)]


def add(P, QP):
    if P is None:
        return QP
    if QP is None:
        return P
    x, y = P
    u, v = QP
    if x == u:
        if y == -v:
            return None
        assert y == v and y != K()
        m = (3*x*x-D)/(2*y)
    else:
        m = (v-y)/(u-x)
    xx = m*m-x-u
    return xx, m*(x-xx)-y


def neg(P):
    return None if P is None else (P[0], -P[1])


def mul(n, P):
    if n < 0:
        return mul(-n, neg(P))
    R = None
    while n:
        if n & 1:
            R = add(R, P)
        P = add(P, P)
        n //= 2
    return R


def f(P):
    assert P is not None and P[0] != K()
    return 1/P[0]


def z(P):
    assert P is not None and P[1] != K()
    return -P[0]/P[1]


def val(q, p):
    q = Q(q)
    assert q
    n, d, v = abs(q.numerator), q.denominator, 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def weight(t):
    Ft = Q(1)
    for theta in THETA:
        Ft *= t-theta
    return Ft/(4*(t-1)**8), (t-1)**4/Ft


def support(q):
    q = Q(q)
    return set(sp.factorint(abs(q.numerator))) | set(sp.factorint(q.denominator))


def main():
    P = add(R0, R0)
    assert P == (K(Q(57,8), Q(-7,2)), K(Q(-165,8), Q(417,32)))
    assert P[1]**2 == P[0]**3-D*P[0]
    assert P[0].norm() == Q(41**2, 64)
    assert D.norm() == 49
    local_bad = {2, 7, 41}
    for theta in THETA:
        local_bad |= support(theta-1)
        for theta0 in THETA:
            if theta != theta0:
                local_bad |= support(theta-theta0)
    assert local_bad == {2,3,5,7,41}

    t = sp.Symbol("t")
    Ft = sp.prod(t-sp.Rational(q.numerator,q.denominator) for q in THETA)
    assert sp.degree(Ft,t) == 6 and sp.gcd(Ft,sp.diff(Ft,t)) == 1
    disc = sp.discriminant(Ft,t)
    assert disc != 0

    screen = 0
    for nu in range(1,20,2):
        for a in range(-10,11):
            for b in range(-10,11):
                if min(a,b) > 0:
                    continue
                assert min(0,2*a-nu)+min(0,2*b-nu) <= -nu
                screen += 1

    cases = []
    for X, ah, au in [(1,2,2),(2,2,3)]:
        A, H, U = mul(X,P), mul(ah,P), mul(au,P)
        HP, UA = add(H,neg(P)), add(U,neg(A))
        L, L0 = z(U)/z(H), z(UA)/z(HP)
        tests = [f(H),f(U),f(HP).bar(),f(UA).bar(),L-L0.bar(),L-X]
        for p in [100003,100049]:
            assert sp.isprime(p) and p > 76176
            split = int(sp.legendre_symbol(2,p))
            assert val(D.norm(),p) == val(P[0].norm(),p) == 0
            for nu in [1,3]:
                tt = Q(p**nu)
                w, alpha = weight(tt)
                assert val(w,p) == nu and val(alpha,p) == -nu
                W = K(1)
                for test in tests:
                    W *= 1+alpha*test**2
                N = W.norm()
                assert N and W.a and W.b
                automatic = w*N
                native_b = w*(N/W.a)**2
                witness = 2*w*N*W.b/W.a
                assert witness**2 == 2*automatic*(automatic-native_b)
                vn, va = val(N,p), val(automatic,p)
                assert vn <= -2*nu and va <= -nu
                cases.append({"input":X,"reference_index":ah,"numerator_index":au,
                              "prime":p,"splitting":"split" if split==1 else "inert",
                              "contact_order":nu,"norm_valuation":vn,
                              "automatic_level_valuation":va,
                              "actual_trace_identity":True})

    # The existing positive benchmark has no odd weight valuation outside S.
    slope = Q(32003072,10621537)
    scale = Q(10621537,256)
    benchmark = []
    for tt in [slope,scale*slope]:
        w, _ = weight(tt)
        facn = sp.factorint(abs(w.numerator)); facd = sp.factorint(w.denominator)
        bad = sorted(int(p) for p,e in facn.items() if p>76176 and e%2)
        bad += sorted(int(p) for p,e in facd.items() if p>76176 and e%2)
        assert not bad
        benchmark.append({"argument":str(tt),"odd_weight_primes_outside_original_S":bad})

    # All conic levels at a fixed native input: independent symbolic identity.
    b, u = sp.symbols("b u")
    level = b/(1-2*u*u)
    ordinate = 2*b*u/(1-2*u*u)
    assert sp.factor(ordinate**2-2*level*(level-b)) == 0

    receipt = {
        "status":"PASS",
        "field":"Q(sqrt(2))",
        "local_exceptional_primes":sorted(local_bad),
        "reference_abscissa_norm":str(P[0].norm()),
        "curve_D_norm":str(D.norm()),
        "contact_degree":6,
        "contact_discriminant":str(disc),
        "hyperelliptic_genus":2,
        "supplementary_valuation_cases":screen,
        "exact_actual_detector_examples":cases,
        "positive_benchmark_consistency":benchmark,
        "all_level_conic_parametrization_identity":True,
        "scope":"The paper proves the universal local norm bound and Faltings finiteness. Finite screens do not replace either proof; no claim about arbitrary nonautomatic levels or variable-count minima is made."
    }
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    data=json.dumps(receipt,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(data)
    else:
        print(data,end="")


if __name__ == "__main__":
    main()
