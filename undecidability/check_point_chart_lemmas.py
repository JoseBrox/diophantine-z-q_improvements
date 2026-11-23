#!/usr/bin/env python3
"""Exact algebraic checks accompanying point_chart_research.tex.

The check covers polynomial identities, literal source-coordinate occurrences
and weights, the quadratic-twist calculation, the displayed point, and the
explicit local integer calculation. It does not certify Mordell--Lang, the
endomorphism-ring argument, or an arithmetic integrality interface.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import json
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]


def v2(q):
    q = Fraction(q)
    if not q:
        return float("inf")
    def integer_order(a):
        a = abs(a)
        return (a & -a).bit_length() - 1
    return integer_order(q.numerator) - integer_order(q.denominator)


def check():
    D, s, t, F, G, eta, d = sp.symbols("D s t F G eta d")
    r1 = d-F*(eta+s+t)
    r3 = D*(F+G)-(s-t)*eta+t*t
    r4 = d*(s-t)-D*F*G-1
    curve = F*s*s+D*F*F-1
    assert sp.expand(curve-(r4-(s-t)*r1+F*r3)) == 0

    c, Fhat, Gtilde, x = sp.symbols("c Fhat Gtilde x")
    new1 = Fhat*(eta+s+t)-eta*Gtilde
    new2 = D*(F+c*Gtilde)-(s-t)*eta+t*t
    subst = {d:c*Fhat*(eta+s+t), G:c*Gtilde}
    assert sp.expand(r1.subs(subst)-(c*Fhat-F)*(eta+s+t)) == 0
    assert sp.expand((d-eta*G).subs(subst)-c*new1) == 0
    assert sp.expand(r3.subs(subst)-new2) == 0
    assert sp.expand(curve-((F*x-1)-F*(x-s*s-D*F))) == 0
    for row in [F-c*Fhat, F*x-1, x-s*s-D*F, new1, new2]:
        assert sp.Poly(row, c,Fhat,Gtilde,x,s,t,F,eta).total_degree() <= 2

    # Check the source occurrence obligation, independently of the new builder.
    sources = {}
    for m in (163,179):
        directory=ROOT/"computation/variable_reductions_v82/general"
        source=json.loads((directory/f"source{m}.json").read_text())
        maps=json.loads((directory/f"quartic{m}/maps.json").read_text())
        rows = []
        for row in source["rows"]:
            if any(set(term["monomial"]) & {211,212} for term in row["terms"]):
                assert row["name"].startswith(
                    ("new1.d_piF.", "new1.d_Gh.", "new1.unit."))
                rows.append(row["name"])
        assert len(rows) == 6
        for j in (201,202,203,204,205,206,209,210):
            assert maps["c_weights"][str(j)] == 0
            assert maps["R_weights"][str(j)] == 0
            assert maps["parameter_weights"][str(j)] == 0
        for j in (207,208,211,212):
            assert maps["c_weights"][str(j)] == 1
            assert maps["R_weights"][str(j)] == 0
            assert maps["parameter_weights"][str(j)] == 0
        sources[str(m)]={"deleted_source_coordinates":[211,212],
                         "only_affected_original_rows":rows,
                         "stored_weight_obligation":"PASS"}

    a=sp.sqrt(2)
    small=3-a
    big=3+a
    discriminant_coefficient=small**2
    conjugate_coefficient=big**2
    assert sp.simplify(small*big-7) == 0
    assert sp.simplify(conjugate_coefficient/(49*discriminant_coefficient)
                       -(big/7)**4) == 0
    scale=sp.sqrt(7)/small
    assert sp.simplify(scale**4*discriminant_coefficient
                       -conjugate_coefficient) == 0
    px=(57-28*a)/8
    py=(-660+417*a)/32
    assert sp.simplify(py**2-px**3+discriminant_coefficient*px) == 0
    # In Q_2(sqrt(2)), rational coefficients have even valuation; the
    # sqrt(2) coefficient has odd valuation, so the minimum is exact.
    vx=min(2*v2(Fraction(57,8)), 2*v2(Fraction(-28,8))+1)
    vy=min(2*v2(Fraction(-660,32)), 2*v2(Fraction(417,32))+1)
    assert (vx,vy,vx-vy)==(-6,-9,3)

    X,Y=sp.symbols("X Y",nonzero=True)
    tx,ty=-D/X,-D*Y/X**2
    assert sp.simplify(ty/tx-Y/X) == 0
    assert sp.simplify(ty**2-tx**3+D*tx
                      -D**2/X**4*(Y**2-X**3+D*X)) == 0

    p=113
    constant=1-7*25**4
    assert sp.isprime(p) and p%16==1
    assert constant%p==0 and constant%(p*p)!=0
    return {
        "status":"PASS",
        "polynomial_chart_identity":"Fs^2+DF^2-1=r4-(s-t)r1+F*r3",
        "common_gauge_replacement_maximum_degree":2,
        "common_gauge_saving_for_12_blocks":{"rational_coordinates":20,
                                          "quadratic_residuals":42},
        "source_occurrence_audits":sources,
        "twist_identity":"Dbar/(49D)=((3+sqrt(2))/7)^4",
        "point_on_curve":True,
        "two_adic_valuation_normalization":"v(sqrt(2))=1, v(2)=2",
        "point_valuations":{"x":vx,"y":vy,"z":vx-vy},
        "same_slope_involution":"Q -> (0,0)-Q",
        "noncancellation_counterexample":{"p":113,"parameter_unit":25,
                                         "constant":constant,"valuation":1},
        "scope":"Exact finite algebra and literal source-map obligations only; geometric and arithmetic theorems are proved or cited in the manuscript."
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,
                        default=ROOT/"undecidability/certificates/point_chart_lemmas.json")
    args=parser.parse_args()
    result=check()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
