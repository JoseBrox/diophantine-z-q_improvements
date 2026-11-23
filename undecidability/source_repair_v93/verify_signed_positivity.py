#!/usr/bin/env python3
"""Independent exact audits for the five-coordinate signed-source reduction.

Finite Pell examples illustrate identities, not the quantified theorem.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
REMOVED_ROWS = {"jones1980.positive.w", "jones1980.positive.s"}
REMOVED_NAMES = {f"positive_{n}_{i}" for n in ("w","s") for i in (1,2,3)}


def normalized(row, names):
    return sorted((t["coefficient"], tuple(sorted(names[i-1] for i in t["monomial"])))
                  for t in row["terms"])


def check_table(stem, expected):
    predecessor = HERE / "coefficients" / f"corrected_{stem}_quadrics.json"
    target = HERE / "coefficients" / f"signed_{stem}_quadrics.json"
    cert_path = target.with_name(target.name.replace("_quadrics.json", "_certificate.json"))
    old, new, cert = [json.loads(p.read_text()) for p in (predecessor,target,cert_path)]
    assert hashlib.sha256(target.read_bytes()).hexdigest() == cert["table_sha256"]
    assert hashlib.sha256(predecessor.read_bytes()).hexdigest() == cert["signed_binomial_positivity_predecessor_sha256"]
    assert old["variables"]-new["variables"] == 5
    assert len(old["residuals"])-len(new["residuals"]) == 1
    assert set(old["variable_names"])-set(new["variable_names"]) == REMOVED_NAMES
    assert set(new["variable_names"])-set(old["variable_names"]) == {"s_inverse"}
    assert len(new["variable_names"]) == len(set(new["variable_names"])) == new["variables"]
    old_rows = {row["name"]:row for row in old["residuals"]}
    new_rows = {row["name"]:row for row in new["residuals"]}
    assert old_rows.keys()-new_rows.keys() == REMOVED_ROWS
    assert new_rows.keys()-old_rows.keys() == {"jones1980.s.nonzero"}
    for name in old_rows.keys()-REMOVED_ROWS:
        assert normalized(old_rows[name],old["variable_names"]) == normalized(new_rows[name],new["variable_names"])
    for coordinate in REMOVED_NAMES:
        occurrences = [row["name"] for row in old["residuals"]
                       if any(coordinate==old["variable_names"][i-1]
                              for term in row["terms"] for i in term["monomial"])]
        assert occurrences == [f"jones1980.positive.{coordinate.split('_')[1]}"]
    assert normalized(new_rows["jones1980.s.nonzero"],new["variable_names"]) == [("-1",()),("1",("s","s_inverse"))]
    assert max(len(t["monomial"]) for row in new["residuals"] for t in row["terms"]) == 2
    assert {i for row in new["residuals"] for t in row["terms"] for i in t["monomial"]} == set(range(1,new["variables"]+1))
    assert (new["variables"],len(new_rows)) == expected
    assert (cert["variables"],cert["quadratic_rows"]) == expected
    assert new["source_universality_hypothesis"] is None
    assert new["source_coding_theorem_independently_reproved"] is False
    assert new["unconditional_undecidability_claim"] is False
    from build_signed_positivity import build
    reproduced = (json.dumps(build(predecessor),sort_keys=True,separators=(",",":"))+"\n").encode()
    assert reproduced == target.read_bytes()
    return {"variant":stem,"variables":expected[0],"quadratic_rows":expected[1],
            "unchanged_rows":len(new_rows)-1,"table_sha256":cert["table_sha256"]}


def pell(a,n):
    x,y=1,0
    for _ in range(n):
        x,y=a*x+(a*a-1)*y,x+a*y
    return x,y


def check_algebra_and_examples():
    a,x,y=sp.symbols("a x y")
    norm=x*x-(a*a-1)*y*y-1
    assert sp.expand((x-(a-2)*y)*(x+(a-2)*y)-(1+(4*a-5)*y*y)-norm) == 0
    xn,yn=a*x+(a*a-1)*y,x+a*y
    assert sp.expand(xn-(a-2)*yn-2*(x-(a-2)*y)-(4*a-5)*y) == 0
    r,Y=sp.symbols("r Y")
    forced_square=(r*Y**2)**2-Y**2+1
    assert sp.expand(forced_square-(r*Y**2-1)**2-(2*r-1)*Y**2) == 0
    assert sp.expand((r*Y**2)**2-forced_square-(Y**2-1)) == 0
    assert Fraction(7,8)*Fraction(15,16)*Fraction(14,4) == Fraction(735,256) > 2

    tested=0
    for A in (2,3,16,31):
        for j in range(1,13):
            Xp,Yp=pell(A,j)
            Xn,Yn=pell(-A,j)
            assert Xn==(-1)**j*Xp and Yn==(-1)**(j-1)*Yp
            for parameter in (A,-A):
                Xj,Yj=pell(parameter,j)
                assert Xj*Xj-(parameter*parameter-1)*Yj*Yj == 1
                modulus=4*parameter-5
                minus=Xj-(parameter-2)*Yj
                plus=Xj+(parameter-2)*Yj
                assert (minus-pow(2,j))%modulus == 0
                assert (plus*pow(2,j)-1)%modulus == 0
                tested+=1
    # Exact false-positive fixture if the s != 0 guard is omitted.
    r,M,b,w,s=1,256,16,1,0
    Y=s*M; B=2*r+1; a=(w*M+1)*r*Y; p=2*w*r*r*Y*Y*M
    c=0; k=h=i=F=d=1; tau=zeta=j=o=0; gamma=3
    G=a+F*F*(c+1-a)
    assert k==r+1+h*(p-1)
    assert tau*tau==(p*p-1)*k*k+1
    assert k*k-4*(c-k*Y)**2==1
    assert d==b*w+(a-2)*c+(4*a-5)*gamma
    assert d*d==(a*a-1)*c*c+1
    assert F*F==(a*a-1)*i*i*c**4+1
    assert (d+o*F)**2==(G*G-1)*(B+j*c)**2+1
    assert zeta*zeta==(a-1)*(d-1)
    assert sp.binomial(2*r,r)%M != 0
    assert s*0 != 1
    return {"exact_polynomial_identities":4,"signed_pell_examples":tested,
            "zero_s_counterexample_checked":True,
            "quantified_positivity_theorem_proved_by":"signed_binomial_positivity.tex"}


def main():
    algebra=check_algebra_and_examples()
    tables=[check_table("ceiling_m163",(1069,923)),
            check_table("ceiling_m179",(1249,1079)),
            check_table("abc_fixed_offsets",(781,684))]
    print(json.dumps({"status":"pass","coordinate_saving":5,"row_saving":1,
                      "retained_integer_predicates":12,"source_coding_theorem_external":True,
                      "unconditional_undecidability_claim":False,"algebra":algebra,"tables":tables},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
