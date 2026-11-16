#!/usr/bin/env python3
"""Verify the rational norm map from doubled points over Q(sqrt(2))."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as S


def zero(expr):
    assert S.factor(S.cancel(expr)) == 0, S.factor(S.cancel(expr))


def verify():
    # Duplication and its three explicit square roots, over any field of
    # characteristic not two with the displayed denominators nonzero.
    z, d = S.symbols("z d", nonzero=True)
    w_square = z*(z**2-d**2)
    x_double = (z**2+d**2)**2/(4*w_square)
    zero((z**2+2*d*z-d**2)**2/(4*w_square) - x_double - d)
    zero((z**2-2*d*z-d**2)**2/(4*w_square) - x_double + d)

    # Norm identity, first as a polynomial identity with arbitrary x in Q(sqrt2).
    x0, x1, rho = S.symbols("x0 x1 rho")
    quadratic_reduce = lambda f: S.rem(S.Poly(S.expand(f), rho), S.Poly(rho**2-2, rho)).as_expr()
    conjugate = lambda f: f.subs(rho, -rho)
    norm = lambda f: quadratic_reduce(f*conjugate(f))
    x = x0+x1*rho
    d = 3-rho
    Nx = norm(x)
    r = 3*x0+2*x1
    assert norm(d) == 7
    zero(norm(x+d) - (Nx+7+2*r))
    zero(norm(x-d) - (Nx+7-2*r))
    zero(norm(x*x-d*d) - ((Nx+7)**2-4*r*r))
    r, L = S.symbols("r L", nonzero=True)
    b_square = L*(L-4*r)
    zero((r*L)**3 - r*r*b_square*(r*L) - (2*r*r*L)**2)

    # Concrete source fixture P=2(1+sqrt2,2sqrt2), evaluated exactly.
    rho = S.sqrt(2)
    d = 3-rho
    z, w = 1+rho, 2*rho
    h = S.simplify((z*z+d*d)/(2*w))
    k_plus = S.simplify((z*z+2*d*z-d*d)/(2*w))
    k_minus = S.simplify((z*z-2*d*z-d*d)/(2*w))
    j = S.expand(k_plus*k_minus)
    x = S.expand(h*h)
    slope = (3*z*z-d*d)/(2*w)
    y = S.simplify(-w+slope*(z-x))
    zero(x - (57-28*rho)/8)
    zero(y - (-660+417*rho)/32)
    conjugate = lambda f: S.expand(f).xreplace({rho: -rho})
    norm = lambda f: S.simplify(f*conjugate(f))
    a, b = norm(h), norm(j)
    r = S.simplify((x*conjugate(d)+conjugate(x)*d)/2)
    L = norm(x+d)
    m = r*b
    assert a == -S.Rational(41, 8)
    assert b == -S.Rational(1071, 64)
    assert r == S.Rational(115, 8)
    assert L == S.Rational(3969, 64)
    assert m == -S.Rational(123165, 512)
    assert norm(k_plus)**2 == L
    point_x, point_y = r*L, 2*r*r*L
    assert point_y**2 == point_x**3-m*m*point_x
    assert 1071**2+1840**2 == 2129**2

    repo = Path(__file__).resolve().parents[3]
    source = "papers/pole_parameters/doubled_source_congruent_twists_20261116_v43.tex"
    return {
        "status": "PASS",
        "source": source,
        "source_sha256": hashlib.sha256((repo/source).read_bytes()).hexdigest(),
        "identities": ["three duplication square roots", "quadratic-field norm identity", "congruent-twist point", "abscissa square factor"],
        "source_fixture": {key: str(value) for key, value in {
            "a": a, "b": b, "r": r, "L": L, "m": m,
            "point_x": point_x, "point_y": point_y,
        }.items()},
        "scope": "Exact symbolic identities and one exact source fixture; source nonzero and positivity conditions are proved in the paper.",
        "new_variable_bound": None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON certificate path")
    args = parser.parse_args()
    certificate = verify()
    rendered = json.dumps(certificate, indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")
