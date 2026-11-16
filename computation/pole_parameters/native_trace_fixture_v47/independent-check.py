#!/usr/bin/env python3
"""Independent polynomial-quotient audit of the prescribed-trace fixture.

Rebuilds the literal source over QQ[t]/(t^2-2). Neither the producer nor
the prior QQ(sqrt2) checker is imported. The source and valuation arguments are stated in the accompanying manuscripts.
"""
from pathlib import Path
from itertools import product
from hashlib import sha256
from fractions import Fraction
import json
import argparse
import sympy as s

HERE = Path(__file__).resolve().parent
TARGET = HERE
t = s.Symbol("t")
MOD = s.Poly(t*t-2, t, domain=s.QQ)


class Q2:
    def __init__(self, a=0):
        self.p = a.p if isinstance(a, Q2) else s.Poly(a, t, domain=s.QQ).rem(MOD)

    def __add__(self, b):
        z = Q2(); z.p = self.p+Q2(b).p; return z
    __radd__ = __add__

    def __neg__(self):
        z = Q2(); z.p = -self.p; return z

    def __sub__(self, b): return self+-Q2(b)
    def __rsub__(self, b): return Q2(b)+-self

    def __mul__(self, b):
        z = Q2(); z.p = (self.p*Q2(b).p).rem(MOD); return z
    __rmul__ = __mul__

    def inv(self):
        assert self
        z = Q2(); z.p = s.invert(self.p, MOD); return z

    def __truediv__(self, b): return self*Q2(b).inv()
    def __rtruediv__(self, b): return Q2(b)*self.inv()

    def __pow__(self, k):
        if k < 0: return self.inv()**(-k)
        a, b = Q2(1), self
        while k:
            if k & 1: a = a*b
            b = b*b; k //= 2
        return a

    def __bool__(self): return not self.p.is_zero
    def __eq__(self, b): return self.p == Q2(b).p

    def bar(self): return Q2(self.p.as_expr().subs(t, -t))
    def coeff(self, k): return self.p.nth(k)
    def rat(self):
        assert not self.p.nth(1)
        return self.p.nth(0)


def qr(a): return s.Rational(a["numerator"], a["denominator"])
def q2(a): return Q2(qr(a[0])+qr(a[1])*t)


def add(P, Q, curve_D):
    x, y = P; u, v = Q
    assert x != u or y == v
    slope = (v-y)/(u-x) if x != u else (3*x*x-curve_D)/(2*y)
    xx = slope*slope-x-u
    return xx, slope*(x-xx)-y


def sub(P, Q, curve_D): return add(P, (Q[0], -Q[1]), curve_D)
def bar(P): return tuple(z.bar() for z in P)
def neg(P, sign): return P[0], sign*P[1]
def f(P): return 1/P[0]
def z(P): return -P[0]/P[1]


def factor_certificate(number, fac):
    value = 1
    for p, e in fac.items():
        p, e = int(p), int(e)
        assert s.isprime(p) and e > 0
        value *= p**e
    assert value == abs(int(number))


parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--fixture",type=Path)
parser.add_argument("--scaling",type=Path)
parser.add_argument("--output",type=Path)
args=parser.parse_args()
raw = (args.fixture or TARGET/"fixture.json").read_bytes()
scaled_raw = (args.scaling or TARGET/"scaling.json").read_bytes()
data, scaled = json.loads(raw), json.loads(scaled_raw)
assert scaled["fixtureSha256"] == sha256(raw).hexdigest()
assert (data["input"], data["fixedB"], data["power"]) == (1, 3, 4)
curve_D = Q2(11-6*t)
R0 = Q2(1+t), Q2(2*t)
P = add(R0, R0, curve_D)
H = add(P, P, curve_D)
assert P == (Q2(s.Rational(57,8)-s.Rational(7,2)*t),
             Q2(-s.Rational(165,8)+s.Rational(417,32)*t))
for half, point, chart in ((R0, P, data["rootChart"]),
                           (P, H, data["referenceAndNumeratorChart"])):
    hh = (half[0]**2+curve_D)/(2*half[1])
    jj = point[1]/hh
    assert hh == q2(chart["h"]) and jj == q2(chart["j"])
    assert hh**2 == point[0] and jj**2 == hh**4-curve_D
    aa = hh**4-curve_D
    a, b = aa.coeff(0), aa.coeff(1)
    mult = Q2(2*a+b+(-a-b)*t)
    assert mult
    normalized = mult*jj
    u, v = normalized.coeff(0), normalized.coeff(1)
    assert u and v
    scalar_roots = [q2(x) for x in chart["scalarRoots"]]
    signs = []
    for Y in scalar_roots:
        Jp = (Y/2+(2*u*v/Y)*Q2(t))/mult
        Jm = (Y/2-(2*u*v/Y)*Q2(t))/mult.bar()
        yp, ym = hh*Jp, hh.bar()*Jm
        assert yp in (point[1], -point[1])
        assert ym in (point[1].bar(), -point[1].bar())
        signs.append((1 if yp == point[1] else -1,
                      1 if ym == point[1].bar() else -1))
    assert set(signs) == set(product((1,-1), repeat=2))

lam = qr(data["slope"])
scale = 4**4+s.Rational(57,4)**4
assert scale == qr(data["secondScale"])
assert lam == s.Rational(32003072,10621537)
assert lam*scale == 125012

# Cache all actual signed differences before reading the saved guard values.
point_data = []
for signs in product((1,-1), repeat=6):
    ap, am, hp, hm, up, um = signs
    Aplus, Aminus = neg(P, ap), neg(bar(P), am)
    Hplus, Hminus = neg(H, hp), neg(bar(H), hm)
    Uplus, Uminus = neg(H, up), neg(bar(H), um)
    V0plus = sub(Hplus, P, curve_D)
    V0minus = sub(Hminus, bar(P), curve_D.bar())
    V1plus = sub(Uplus, Aplus, curve_D)
    V1minus = sub(Uminus, Aminus, curve_D.bar())
    for pp, dd in [(Aplus,curve_D),(Hplus,curve_D),(Uplus,curve_D),
                   (V0plus,curve_D),(V1plus,curve_D),
                   (Aminus,curve_D.bar()),(Hminus,curve_D.bar()),
                   (Uminus,curve_D.bar()),(V0minus,curve_D.bar()),(V1minus,curve_D.bar())]:
        assert pp[0] and pp[1] and pp[1]**2 == pp[0]**3-dd*pp[0]
    lp, lm = z(Uplus)/z(Hplus), z(Uminus)/z(Hminus)
    l0p, l0m = z(V1plus)/z(V0plus), z(V1minus)/z(V0minus)
    tests = ((f(Hplus), f(Uplus), f(V0minus), f(V1minus), lp-l0m, lp-1),
             (f(Hminus), f(Uminus), f(V0plus), f(V1plus), lm-l0p, lm-1))
    point_data.append((signs, tests))

theta = [s.Rational(x) for x in (0, -1)] + [s.Rational(-1,2),s.Rational(-1,4),s.Rational(-2,5),s.Rational(-1,3)]
guards = 0
for j, block in enumerate(data["blocks"]):
    arg = lam if j == 0 else lam*scale
    F = s.prod(arg-th for th in theta)
    delta = arg-1
    weight, alpha = F/(4*delta**8), delta**4/F
    assert qr(block["weight"]) == weight and qr(block["alpha"]) == alpha
    assert weight > 0 and alpha > 0
    factor_certificate(weight.p, block["weightNumeratorFactors"])
    factor_certificate(weight.q, block["weightDenominatorFactors"])
    factor_certificate(alpha.q, block["alphaDenominatorFactors"])
    assert all(int(p)<=76176 for p in block["weightDenominatorFactors"])
    assert all(int(p)<=76176 for p in block["alphaDenominatorFactors"])
    assert all(int(e)%2 == 0 for p,e in block["weightNumeratorFactors"].items() if int(p)>76176)
    W = ((1+alpha*f(H)**2)*(1+alpha*f(P).bar()**2))**2
    assert W == q2(block["actualW"])
    N = (W*W.bar()).rat()
    W0, W1 = W.coeff(0), W.coeff(1)
    b = weight*(N/W0)**2
    fixed = weight*N
    V = 2*W0/N
    witness = 2*weight*N*W1/W0
    assert 0 < b < fixed
    assert b == qr(block["actualInput"])
    assert fixed == qr(block["fixedLevel"])
    assert V == qr(block["actualTraceInverse"])
    assert witness**2 == 2*fixed*(fixed-b)
    old_guards = {tuple(row["signs"]): q2(row["guard"]) for row in block["wholeCharacterGuards"]}
    new = scaled["blocks"][j]
    m, kk, cc = int(new["fixedPositiveIntegerM"]), int(new["denominatorClearer"]), int(new["classRepresentative"])
    gamma = qr(new["fixedWeightCoefficient"])
    assert gamma == s.Rational(17*kk*kk, cc)
    factor_certificate(cc, new["classRepresentativePrimeFactors"])
    factor_certificate(kk, new["denominatorClearerPrimeFactors"])
    assert all(int(p)<=76176 for p in new["classRepresentativePrimeFactors"])
    assert all(int(p)<=76176 for p in new["denominatorClearerPrimeFactors"])
    assert gamma*fixed == 17*m*m
    Y = -2*m*W1/N
    assert Y == qr(new["normWitnessY"])
    assert (m*V)**2-2*Y**2 == 4*gamma*weight/17
    for signs, tests in point_data:
        values = []
        for slot in tests:
            value = Q2(1)
            for test in slot:
                factor = 1+alpha*test**2
                assert factor
                value *= factor
            values.append(value)
        p, q = values
        assert p and q and p+q
        bchar = weight*(2*p*q/(p+q))**2
        guard = fixed-bchar
        assert guard and guard == old_guards[signs]
        assert 17*m*m-gamma*bchar == gamma*guard
        guards += 1

assert guards == 128
receipt = {
    "status": "PASS_INDEPENDENT_SOURCE_RECONSTRUCTION",
    "method": "Independent QQ[t]/(t^2-2) arithmetic, literal point and six-test source reconstruction; no producer/prior-checker import",
    "fixture_sha256": sha256(raw).hexdigest(),
    "scaled_fixture_sha256": sha256(scaled_raw).hexdigest(),
    "actual_norm_incidences": 2,
    "geometric_characters": 64,
    "whole_algebra_complement_guards": guards,
    "fixed_coefficients_are_S_units": True,
    "scope": "Exact fixture at X=1,B=3; the paper proves the sign involution yielding X=-1 with the same constants. Local soundness under fixed scaling; no uniform realization or defining count.",
}
(args.output or HERE/"independent-verification.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps(receipt, indent=2))
