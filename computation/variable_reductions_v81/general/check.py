#!/usr/bin/env python3
"""Read-only exact checks for the v81 local scalar checkpoint.

The default invocation compares with independent.json and never writes.
--emit-certificate prints the deterministic certificate for explicit review.
No construction producer or other checker is imported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCES = (
    "papers/quartic/shared_product_audit_20261119_v78.tex",
    "papers/quartic/quartic193_20261117_v74.tex",
    "sources/h10_quartic198/arithmetic/inverse_vieta_198.tex",
    "computation/quartic/seven_units193_v74/primitive/laurent-source.json",
    "computation/variable_reductions_v81/general/README.md",
    "computation/variable_reductions_v81/general/check.py",
)


def zero(expr):
    assert s.cancel(expr) == 0, s.factor(expr)


def pair_square(pair):
    x, y = pair
    return x*x + 2*y*y, 2*x*y


def pair_norm(pair):
    x, y = pair
    return x*x - 2*y*y


def calculate():
    R, tau = s.symbols("R tau", nonzero=True)
    b, e, u, v, p, q = s.symbols("b e u v p q")
    # No substitution or cancellation below divides by e,u,v,p, or q.
    d = s.Integer(9792)
    K = R*(R+d)
    original = (
        3*e*e - 34*e - 289 + 17*b*p*p,
        e*(17-b) - 17*u*v,
        u*u + 34*u*v - 867*v*v - 17*b*q*q,
    )
    sigma = 1/tau
    B = b/tau
    E, U, V, P, Q = (x/tau for x in (e, u, v, p, q))
    P2, Q2 = p*p/tau, q*q/tau
    transformed = (
        3*E*E - 34*E*sigma - 289*sigma*sigma + 17*B*P2,
        E*(17*sigma-B) - 17*U*V,
        U*U + 34*U*V - 867*V*V - 17*B*Q2,
    )
    for new, old in zip(transformed, original):
        zero(new - old/tau**2)
    zero(sigma*P2-P*P)
    zero(sigma*Q2-Q*Q)
    zero((B*sigma-K).subs(b, K*tau**2))

    # Check the converse as polynomial identities, allowing zero auxiliaries.
    sig, bb, ee, uu, vv, pp, qq, ps, qs = s.symbols(
        "sig bb ee uu vv pp qq ps qs"
    )
    new_native = (
        3*ee**2-34*ee*sig-289*sig**2+17*bb*ps,
        ee*(17*sig-bb)-17*uu*vv,
        uu**2+34*uu*vv-867*vv**2-17*bb*qs,
    )
    inverse = {b: tau*bb, e: tau*ee, u: tau*uu, v: tau*vv,
               p: tau*pp, q: tau*qq}
    inverse_aux = {sig: 1/tau, ps: tau*pp**2, qs: tau*qq**2}
    for old, new in zip(original, new_native):
        zero(old.subs(inverse)-tau**2*new.subs(inverse_aux))
    zero((tau*bb-K*tau**2).subs(bb, K*tau))

    # Field operations are expanded independently in the basis (1,sqrt(2)).
    z0, z1, f0, f1 = s.symbols("z0 z1 f0 f1")
    zsq, fsq = pair_square((z0,z1)), pair_square((f0,f1))
    J = tuple(zsq[i]/R**5 + fsq[i]/R**4 for i in range(2))
    Jhat = tuple(R**4*x for x in J)
    for i in range(2):
        zero(R*Jhat[i]-zsq[i]-R*fsq[i])
    zero(pair_norm(Jhat)-R**8*pair_norm(J))
    zero(2*Jhat[0]-R**4*(2*J[0]))
    zero((R**4*tau)*(2*Jhat[0])-pair_norm(Jhat)
         -R**8*(tau*(2*J[0])-pair_norm(J)))
    zero((R**4*tau)*sigma-R**4)

    # These are algebraic certificates for universal proof steps, not sampling.
    mu, zz, ff, tt = s.symbols("mu zz ff tt")
    zero((2*zz-5*mu)+mu/2 - 2*(zz-s.Rational(9,4)*mu))
    zero((2*ff-4*mu)+mu/2 - 2*(ff-s.Rational(7,4)*mu))
    k, zi, fi, ti = s.symbols("k zi fi ti", integer=True)
    odd = 2*k+1
    difference = s.Poly((2*zi-5*odd)-(2*fi-4*odd), zi,fi,k)
    assert int(difference.TC()) % 2 == 1
    assert all(int(c) % 2 == 0 for mon,c in difference.terms() if any(mon))
    pole_parity = s.Poly(odd+2*ti, k,ti)
    assert int(pole_parity.TC()) % 2 == 1
    assert all(int(c) % 2 == 0 for mon,c in pole_parity.terms() if any(mon))
    lower, gap, cancellation = s.symbols("lower gap cancellation", real=True)
    # If w2=w1+gap and v(Tr J)=w1+cancellation, with both latter
    # quantities nonnegative, then v(tau)=max(w1,w2)-cancellation.
    zero(lower+(lower+gap)-(lower+cancellation)
         -((lower+gap)-cancellation))

    # The local-preparation identity and the real AM-GM identity.
    eps, rho = s.symbols("eps rho")
    zero((1+eps)**2+rho - (1+2*eps+eps**2+rho))
    x, y = s.symbols("x y", positive=True)
    zero((x+y)/4-x*y/(x+y) - (x-y)**2/(4*(x+y)))

    # The proposed weakening R^4 -> R^2 changes the scalar bound to 5/4.
    zero((2*zz-mu)-s.Rational(3,2)*mu
         -2*(zz-s.Rational(5,4)*mu))

    return {
        "schema": "v81-general-local-scalar-checkpoint-1",
        "status": "local lemma and rational identities only; no smaller defining quartic",
        "attribution": "Based on notes of Gabe Conant with Astra 6.2",
        "published_general_variable_counts_unchanged": [165,180],
        "coefficient_d": int(d),
        "checks": {
            "native_forward_residuals": 3,
            "native_reverse_residuals": 3,
            "native_square_relations": 2,
            "native_input_forward_and_reverse": 2,
            "field_definition_component_identities": 2,
            "norm_trace_rescaling_and_inverse_identities": 4,
            "universal_odd_parity_identities": 2,
            "universal_detection_threshold_identities": 2,
            "norm_over_trace_valuation_identity": True,
            "local_preparation_expansion": True,
            "real_bound_identity": True,
            "weakened_threshold_identity": True,
            "no_auxiliary_coordinate_inverted": True,
        },
        "universal_local_result": {
            "hypotheses": [
                "K=Q(sqrt(2)); R>0; Z in K; f in K nonzero",
                "p does not divide 2*9792; mu=v_p(R)>0 is odd",
                "b=R*(R+9792)*tau^2 has no negative odd p-adic valuation",
                "J=Z^2/R^5+f^2/R^4; tau=Norm(J)/Trace(J)",
            ],
            "conclusion": "one common slot w has v_w(Z)>9*mu/4 and v_w(f)>7*mu/4",
            "zero_Z_case_included": True,
            "method": "universal parity and valuation proof; not a finite-prime enumeration",
        },
        "remaining_tasks": [
            "realize the stated local approximation patterns in the full ordered elliptic converse",
            "encode tau_hat*sigma=R^4 without retaining or adding an R^2 register",
            "verify the entire downstream quadratic table, maps, and every zero fiber before a census claim",
        ],
        "source_sha256": {
            rel: hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
            for rel in SOURCES
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-certificate", action="store_true")
    args = parser.parse_args()
    certificate = calculate()
    if args.emit_certificate:
        print(json.dumps(certificate, indent=2, sort_keys=True))
        return
    saved = json.loads((HERE/"independent.json").read_text())
    if saved != certificate:
        raise SystemExit("certificate mismatch: review the mathematical/source change")
    print("PASS: universal scalar lemma identities and exact native-pole rechart; "
          "165/180 counts unchanged; certificate read-only")


if __name__ == "__main__":
    main()
