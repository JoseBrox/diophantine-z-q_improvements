#!/usr/bin/env python3
"""Independent exact audit of the odd-Pell-quotient source projection.

Does not import the builder. Full source universality and the arithmetic
interface remain external premises; finite Pell fixtures are not full
universal-source witnesses.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def named(row, names, rename=None):
    rename = rename or {}
    return sorted((str(term["coefficient"]), tuple(sorted(rename.get(names[i-1],names[i-1])
                    for i in term["monomial"]))) for term in row["terms"])


def pell_by_power(a, n):
    """Binary multiplication in Z[sqrt(a^2-1)]."""
    Delta = a*a-1
    x, y, xx, yy = 1, 0, a, 1
    while n:
        if n&1:
            x,y = x*xx+Delta*y*yy, x*yy+y*xx
        xx,yy = xx*xx+Delta*yy*yy, 2*xx*yy
        n //= 2
    return x,y


def audit():
    oldpath = ROOT/"undecidability/abc_common_numerator_v103/common_numerator_abc_quadrics.json"
    newpath = HERE/"odd_quotient_abc_quadrics.json"
    oldraw,newraw = oldpath.read_bytes(),newpath.read_bytes()
    assert hashlib.sha256(oldraw).hexdigest() == "91098cd9c25b2336ce320391fd7f9f195bee838404996e24dd2e2067412b6877"
    old,new = json.loads(oldraw),json.loads(newraw)
    on,nn = old["variable_names"],new["variable_names"]
    ro = {row["name"]:row for row in old["residuals"]}
    rn = {row["name"]:row for row in new["residuals"]}
    assert nn == ["i_half" if name=="i" else name for name in on if name!="i_inverse"]
    deleted,changed = "integer.i_reciprocal.unit","jones1980.E.reciprocal"
    added = "jones1980.E.odd_quotient"
    assert set(rn) == (set(ro)-{deleted,changed})|{added}
    for name in set(ro)-{deleted,changed}:
        assert named(ro[name],on,{"i":"i_half"}) == named(rn[name],nn),name
    assert named(ro[deleted],on) == [("-1",()),("1",("i","i_inverse"))]
    assert named(ro[changed],on) == [("-1",("int_c_29",)),("1",("E","i_inverse"))]
    assert named(rn[added],nn) == [("-1",("int_c_29",)),("-2",("i_half","int_c_29")),("1",("E",))]
    assert named(rn["integer.c.height.betaSquare"],nn) == [("-1",("int_c_29",)),("1",("c","c"))]
    assert named(rn["integer.i.height.betaSquare"],nn) == [("-1",("int_i_reciprocal_29",)),("1",("i_half","i_half"))]
    for name,allowed in [("i",{deleted,"integer.i.height.betaSquare"}),
                         ("i_inverse",{deleted,changed})]:
        occurrences = {row["name"] for row in old["residuals"]
                       if any(on[i-1]==name for term in row["terms"] for i in term["monomial"])}
        assert occurrences == allowed
    assert new["variables"]==len(nn)==674 and len(rn)==593
    assert len(nn)==len(set(nn))
    assert {i for row in new["residuals"] for term in row["terms"] for i in term["monomial"]} == set(range(1,675))
    assert max(len(term["monomial"]) for row in new["residuals"] for term in row["terms"]) == 2
    parameters = sp.symbols(" ".join(new["parameters"]))
    for row in new["residuals"]:
        for term in row["terms"]:
            coefficient = sp.sympify(term["coefficient"])
            assert coefficient.free_symbols <= set(parameters)
            assert not sp.Poly(coefficient,*parameters,domain=sp.ZZ).is_zero
    assert new["ordinary_integer_inputs"] == ["i_half" if value=="i" else value for value in old["ordinary_integer_inputs"]]
    assert new["integer_blocks"] == old["integer_blocks"] == 13
    assert new["reciprocal_integer_inputs"] == []
    assert new["source_universality_hypothesis"] is None
    assert new["source_coding_theorem"] == old["source_coding_theorem"]
    assert new["unconditional_undecidability_claim"] is False
    assert new["fixed_offset_translations"]["i_half"] == old["fixed_offset_translations"]["i"]
    assert "reciprocal_nonzero_guard" not in new

    # A direct identity verifies restoration of the old two outer rows.
    half,c = sp.symbols("half c")
    actual_i=2*half+1
    E=actual_i*c*c
    assert sp.cancel(actual_i/actual_i-1)==0
    assert sp.cancel(E/actual_i-c*c)==0

    fixtures=[]
    for a,B in [(2,3),(3,3),(4,3),(5,3),(2,5),(2,7)]:
        d,c=pell_by_power(a,B)
        q=B*c
        F,Y=pell_by_power(a,q)
        # Independent repeated recurrence at parameter d tests the composition.
        previous,current=0,1
        for _ in range(1,c):
            previous,current=current,2*d*current-previous
        assert Y==c*current
        assert Y%(c*c)==0
        i=Y//(c*c)
        assert c%2==q%2==Y%2==i%2==1 and i>1
        i_half=(i-1)//2
        assert i_half>0 and 2*i_half+1==i
        assert d*d-(a*a-1)*c*c==1
        assert F*F-(a*a-1)*i*i*c**4==1
        fixtures.append({"a":a,"B":B,"c":c,"q":q,"i_bits":i.bit_length(),"i_half_positive":True,"i_odd":True})
    certificate=json.loads((HERE/"odd_quotient_abc_certificate.json").read_text())
    assert certificate["table_sha256"]==hashlib.sha256(newraw).hexdigest()
    return {
        "status":"PASS", "variables":674, "quadratic_rows":593, "degree":4,
        "table_sha256":hashlib.sha256(newraw).hexdigest(),
        "predecessor_sha256":hashlib.sha256(oldraw).hexdigest(),
        "unchanged_rows_under_coordinate_renaming":592,
        "replaced_rows":1,"deleted_rows":1,"deleted_coordinates":1,
        "integer_blocks":13,"retained_source_and_arithmetic_premises":True,
        "actual_source_quotient":"2*i_half+1", "finite_pell_fixtures":fixtures,
        "verification_scope":"Exact full-table audit, quotient identities and six finite Pell fixtures. Quantified completeness is the proof in odd_pell_quotient.tex; no arithmetic-interface or universal-coding premise is independently proved.",
        "same_coordinate_predecessor_lift_claim":False,
        "unconditional_rational_undecidability_claim":False,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--write-certificate",action="store_true")
    args=parser.parse_args()
    report=audit()
    text=json.dumps(report,indent=2,sort_keys=True)+"\n"
    path=HERE/"independent_verification.json"
    if args.write_certificate:
        path.write_text(text)
    else:
        assert path.read_text()==text,"independent receipt mismatch"
    print(text,end="")


if __name__=="__main__":
    main()
