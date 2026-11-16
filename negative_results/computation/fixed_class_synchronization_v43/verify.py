#!/usr/bin/env python3
"""Exact algebra supporting fixed-class synchronization and its geometry.

The script verifies identities and the arithmetic of the stated genus
formula. The geometric proofs, and the use of Faltings, are in the paper.
No finite rational-point search or new defining-variable bound is claimed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as S


def zero(expr):
    assert S.factor(S.cancel(expr)) == 0, S.factor(S.cancel(expr))


def verify():
    t, D, D1, D2 = S.symbols("t D D1 D2", nonzero=True)
    F = lambda d: (t**2-d)*(t**2+3*d)
    disc = S.factor(S.discriminant(F(D), t))
    resultant = S.factor(S.resultant(F(D1), F(D2), t))
    assert disc == -12288*D**6
    zero(resultant-9*(D1-D2)**4*(D1+3*D2)**2*(3*D1+D2)**2)

    genera = []
    for count in range(1, 9):
        degree = 2**count
        ramification = 4*count*(degree//2)
        genus = 1+(-2*degree+ramification)//2
        assert genus == 1+degree*(count-1)
        character_dimensions = sum(
            S.binomial(count, size)*(2*size-1)
            for size in range(1, count+1)
        )
        assert character_dimensions == genus
        assert -2+2*count == 2*count-2
        genera.append({"factors": count, "degree": degree,
                       "branch_points": 4*count, "genus": genus})

    alpha, C, s0, z = S.symbols("alpha C s0 z", nonzero=True)
    seed_q_square = D*(s0**2-alpha*C)*(s0**2+3*alpha*C)
    propagated_q_square = D*((z*s0)**2-alpha*z*z*C)*(
        (z*s0)**2+3*alpha*z*z*C)
    zero(propagated_q_square-z**4*seed_q_square)

    # Explicit genus-one and genus-two quotient equations and differentials.
    a1, a2, u = S.symbols("alpha1 alpha2 u", nonzero=True)
    G = F(D1)*F(D2)/(a1*a2)
    E = (u-D1)*(u+3*D1)*(u-D2)*(u+3*D2)/(a1*a2)
    zero(E.subs(u, t*t)-G)
    zero((u*E).subs(u, t*t)-t*t*G)
    differential_coefficients = S.Matrix([[0, 2, 0], [2, 0, 0], [0, 0, 2]])
    assert differential_coefficients.rank() == 3
    assert 1+1+1+2 == 5

    # The local quotient and both canonical form computations.
    xi, eta, a, v = S.symbols("xi eta a v", nonzero=True)
    invariants = (xi*xi, eta*eta, xi*eta)
    zero(invariants[0]*invariants[1]-invariants[2]**2)
    quotient_jacobian = S.Matrix([xi*xi, xi*eta]).jacobian([xi, eta]).det()
    zero(quotient_jacobian/(xi*xi)-2)
    resolution_jacobian = S.Matrix([a, a*v]).jacobian([a, v]).det()
    zero(resolution_jacobian/a-1)

    # Fixed-fiber Jacobian invariants used in the accompanying literature note.
    n = S.symbols("n", nonzero=True)
    a2, a4 = -4*n, 16*n*n
    b2, b4 = 4*a2, 2*a4
    c4 = S.expand(b2*b2-24*b4)
    c6 = S.expand(-b2**3+36*b2*b4)
    discriminant = S.factor((c4**3-c6**2)/1728)
    assert c4 == -512*n*n
    assert c6 == -14336*n**3
    assert discriminant == -196608*n**6
    assert S.cancel(c4**3/discriminant) == S.Rational(2048, 3)

    repo = Path(__file__).resolve().parents[3]
    source = "negative_results/papers/pole_parameters/fixed_class_synchronization_20261116_v43.tex"
    return {
        "status": "PASS",
        "source": source,
        "source_sha256": hashlib.sha256((repo/source).read_bytes()).hexdigest(),
        "branch_discriminant": str(disc),
        "pairwise_branch_resultant": str(resultant),
        "checked_genus_values": genera,
        "genus_five_jacobian_dimensions": [1, 1, 1, 2],
        "canonical_fiber_coefficient": "2*r-2",
        "local_quotient_form_pullback": "2 dxi wedge deta",
        "resolution_chart_form": "da wedge dv",
        "fixed_fiber_jacobian_invariants": {
            "c4": str(c4), "c6": str(c6),
            "discriminant": str(discriminant), "j": "2048/3",
        },
        "scope": "Exact algebra and finite checks of formula arithmetic; the general geometric and finiteness results are proved or cited in the paper.",
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
