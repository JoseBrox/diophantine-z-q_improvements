#!/usr/bin/env python3
"""Check two exact contact-parity examples with independent Fraction arithmetic.

The universal theorem is proved in the accompanying paper. These examples
neither prove that theorem nor satisfy all equations of the defining source.
"""
from fractions import Fraction
from pathlib import Path
import json
from math import isqrt

ROOT = Path(__file__).resolve().parent
CERT = ROOT / "rational-contact-combination-examples-v20.json"


def valuation(q, p):
    q = Fraction(q)
    assert q
    n, d = abs(q.numerator), q.denominator
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def contact(t):
    t = Fraction(t)
    return (t * (t + 1) * (2*t + 1) * (3*t + 1)
            * (4*t + 1) * (5*t + 2) / (120 * (t - 1)**8))


def check():
    certificate = json.loads(CERT.read_text())
    assert certificate["status"] == "PASS"
    p = 76213
    assert p > 76176
    assert all(p % d for d in range(2, isqrt(p) + 1))
    # At t=-1, differentiate only the simple vanishing factor t+1.
    derivative = Fraction((-1)*(-1)*(-2)*(-3)*(-3), 120 * (-2)**8)
    assert derivative == Fraction(-3, 5120)
    xi = 5598
    beta0 = 2 * xi**2 + 3
    a0 = Fraction(beta0**8) + Fraction(57, 4)**8
    assert beta0 % p == 28125
    assert 32 * xi * beta0**7 % p == 22560
    assert (a0 - 1).numerator % p == 0
    fixtures = [
        ("product", 6603791433, 3821558707, 3, (1, 1)),
        ("harmonic", 24884609587871, 304951751852576, 3, (1, 2)),
    ]
    computed = []
    for name, odd_numerator, z, w, expected in fixtures:
        X = Fraction(odd_numerator, 2)
        B, n, T = 3, 1, Fraction(57, 4)
        beta = 2 * X**2 + B
        a = beta**8 + T**8
        slope = z*z + w*w
        assert X.denominator == beta.denominator == 2
        assert a > 1 and slope > 1
        first, second = contact(slope), contact(a * slope)
        assert first > 0 and second > 0
        depths = (valuation(first, p), valuation(second, p))
        assert depths == expected
        combined = first * second
        if name == "harmonic":
            combined /= first + second
        assert valuation(combined, p) == 2
        assert valuation(beta - n, p) == 0
        computed.append({
            "name": name, "p": str(p), "B": B, "n": n, "T": str(T),
            "X": str(X), "lambda": str(slope),
            "lambdaSquareRepresentation": [str(z), str(w)],
            "contactValuations": list(depths), "combinerValuation": 2,
            "inputResidualValuation": 0, "inputNotIntegral": True,
        })
    assert computed == certificate["examples"]
    assert certificate["primeVerifiedByCompleteTrialDivision"] is True
    print("PASS: two exact positive-slope examples, simple contact derivative, "
          "primality, nonintegral inputs, and unit residuals.")


if __name__ == "__main__":
    check()
