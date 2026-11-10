#!/usr/bin/env python3
"""Independent exact identities for the four-coordinate fixed-translation chart.

Only the Python standard library is used.  All calculations take place in
Z[a,b,D,S,T]/(b^2-a^3+aD), before any numerical parameter is substituted.
The accompanying proof deals with both exceptional denominator strata.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from math import comb
from pathlib import Path
import json


ZERO = (0, 0, 0, 0, 0)


class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {m: int(c) for m, c in value.items() if c}
        else:
            self.terms = {ZERO: int(value)} if value else {}

    def __add__(self, other):
        out = self.terms.copy()
        for m, c in Poly(other).terms.items():
            out[m] = out.get(m, 0) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) - self

    def __mul__(self, other):
        out = {}
        for m, c in self.terms.items():
            for n, d in Poly(other).terms.items():
                e = tuple(x+y for x, y in zip(m, n))
                out[e] = out.get(e, 0) + c*d
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result = Poly(1)
        for _ in range(exponent):
            result *= self
        return result

    def reduce(self):
        out = {}
        for (ea, eb, ed, es, et), c in self.terms.items():
            k, eb0 = divmod(eb, 2)
            # b^(2k) = (a^3-aD)^k.
            for j in range(k+1):
                m = (ea+3*k-2*j, eb0, ed+j, es, et)
                out[m] = out.get(m, 0) + c*comb(k, j)*(-1)**j
        return Poly(out)

    def canonical(self):
        return [[list(m), c] for m, c in sorted(self.terms.items())]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name(
        "fixed-difference-chart-certificate.json"))
    args = parser.parse_args()
    a, b, D, S, T = [Poly({tuple(int(i == j) for i in range(5)): 1})
                      for j in range(5)]
    A, B = a*a+D, a*a-D
    C = D*D+6*a*a*D-3*a**4
    Phi = a*S*S*T*T-B*(S*S+T*T)+2*A*S*T+4*a*D
    Lf, Lg = 2*b*D*(a*T-b), 2*b*D*(a*S+b)
    Qf = a*A*S*T+b*A*S-b*B*T+4*a*a*D
    Qg = -(a*A*S*T+b*B*S-b*A*T+4*a*a*D)
    Nf = -A*S+B*T-b*S*S-a*S*S*T
    Ng = A*T-B*S-b*T*T+a*S*T*T
    N = a**4-6*D*a*a+D*D
    residuals = {
        "elimination_without_division":
            D*D*Qf*Qg+a*D*(Qf*Lg+Qg*Lf)
            +(a*S*T+b*(S-T)+D)*Lf*Lg+a*D*D*C*Phi,
        "first_polynomial_reconstruction": (a*T-b)*Nf-Qf+a*Phi,
        "second_polynomial_reconstruction": (a*S+b)*Ng-Qg-a*Phi,
        "third_quadratic_on_old_chart":
            Nf*Ng+2*a*b*(Nf+Ng)+4*b*b*(a*S*T+b*(S-T)+D)
            -(B-a*S*T-b*(S-T))*Phi,
        "first_curve_equation":
            a*D*Nf*Nf+2*a*b*D*S*S*Nf-4*a*b*b*D*D
            -D*(a*a*S*S-b*b)*Phi,
        "second_curve_equation":
            a*D*Ng*Ng+2*a*b*D*T*T*Ng-4*a*b*b*D*D
            -D*(a*a*T*T-b*b)*Phi,
        "translation_abscissa":
            Nf*Ng*(a*S+b)**2-a*(2*b*D-a*Nf)**2
            +(a*S+b)**2*(a*S*T+b*(S-T)+D)*Phi,
        "translation_ordinate":
            (a*T-b)*Nf+(a*S+b)*Ng-2*b*D*(S+T),
        "exceptional_Rf_Rg": N-B*B+4*a*a*D,
        "exceptional_nonvanishing": a*N+2*b*b*A+a*C,
        "exceptional_R3": 4*B*D+N+(2*D-B)*A,
        "simultaneous_exception_excluded":
            b**4-2*a*B*b*b-2*a*A*b*b+4*a**4*D-a*a*C,
    }
    checks = {}
    for name, residual in residuals.items():
        reduced = residual.reduce()
        assert not reduced.terms, (name, reduced.canonical())
        checks[name] = {
            "status": "PASS",
            "terms_before_reducing_b_squared": len(residual.terms),
            "terms_after_reducing_b_squared": 0,
        }
    # Independent specialization at P=(2,2) on y^2=x^3-2x.
    # Check the two exceptional points and an ordinary point 3P.
    a0, b0, d0 = Fraction(2), Fraction(2), Fraction(2)
    def add(p, q):
        if p is None:
            return q
        if q is None:
            return p
        x, y = p
        u, v = q
        if x == u and y == -v:
            return None
        m = (3*x*x-d0)/(2*y) if p == q else (v-y)/(u-x)
        r = m*m-x-u
        return r, -y+m*(x-r)
    p = (a0, b0)
    p2 = add(p, p)
    p3 = add(p2, p)
    point_checks = []
    for name, h in [("minus_P", (a0, -b0)), ("twice_P", p2), ("three_P", p3)]:
        hp = add(h, (a0, -b0))
        assert hp is not None and h[0] and hp[0]
        s, t, f, g = h[1]/h[0], hp[1]/hp[0], 1/h[0], 1/hp[0]
        aa, bb = a0*a0+d0, a0*a0-d0
        rf = 2*b0*d0*(a0*t-b0)*f-(a0*aa*s*t+b0*aa*s-b0*bb*t+4*a0*a0*d0)
        rg = 2*b0*d0*(a0*s+b0)*g+(a0*aa*s*t+b0*bb*s-b0*aa*t+4*a0*a0*d0)
        r3 = d0*d0*f*g+a0*d0*(f+g)+a0*s*t+b0*(s-t)+d0
        assert rf == rg == r3 == 0
        point_checks.append({"case": name, "S_T_f_g": [str(v) for v in (s,t,f,g)],
                             "status": "PASS"})
    payload = json.dumps({"Lf": Lf.canonical(), "Lg": Lg.canonical(),
                          "Qf": Qf.canonical(), "Qg": Qg.canonical()}, sort_keys=True)
    certificate = {
        "status": "PASS",
        "scope": "Exact general polynomial identities and exceptional-stratum calculations; projection proof is supplied in the manuscript.",
        "ring": "Z[a,b,D,S,T]/(b^2-a^3+aD)",
        "assumptions": "a*b*D*(a^2+D)*(D^2+6*a^2*D-3*a^4) != 0; characteristic zero",
        "chart_quadrics": ["Lf*f-Qf", "Lg*g-Qg",
                            "D^2*f*g+a*D*(f+g)+a*S*T+b*(S-T)+D"],
        "coefficient_definition_sha256": sha256(payload.encode()).hexdigest(),
        "identities": checks,
        "rational_point_checks": point_checks,
        "zero_loci": {
            "T=b/a": "H=2P, g=1/a, f=4*b^2/(a^2+D)^2",
            "S=-b/a": "H=-P, f=1/a, g=4*b^2/(a^2+D)^2",
            "both": "Phi=C/a != 0, so impossible",
            "f_or_g_zero": "Impossible from D*f^2+S^2*f=1 and D*g^2+T^2*g=1",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "polynomial_identities": len(checks),
                      "rational_point_checks": len(point_checks)}, sort_keys=True))


if __name__ == "__main__":
    main()
