#!/usr/bin/env python3
"""Independent coefficient and algebra audit of Pell half-trace guard absorption."""
from __future__ import annotations

import hashlib
from math import isqrt
import json
from pathlib import Path

import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
EXPECTED={163:(982,854),179:(1147,997),56:(733,642)}


def named(row,names):
    return sorted((str(t["coefficient"]),tuple(sorted(names[i-1]for i in t["monomial"])))for t in row["terms"])


def expr(row,names):
    return sp.expand(sum(sp.sympify(t["coefficient"])*sp.prod(sp.Symbol(names[i-1])for i in t["monomial"])
                         for t in row["terms"]))


def pell(a,n):
    x,y=1,0
    for _ in range(n):x,y=a*x+(a*a-1)*y,x+a*y
    return x,y


def check_algebra():
    D,c=sp.symbols("D c")
    assert sp.expand((D+1)*(D*c*c+1)-(D*c+1)**2-D*(c-1)**2)==0
    a,d,ac,z=sp.symbols("a d ac z")
    quadratic=z*z-2*a*d-2*a*ac+2*c-2
    assert sp.expand(quadratic.subs(ac,a*c)-(z*z-2*(a*d+(a*a-1)*c+1)))==0
    tested=0
    for A in range(2,13):
        for a0 in (A,-A):
            for B in range(3,26,2):
                X,Y=pell(a0,B)
                # Both signed choices of c are legitimate at the branch stage.
                for signc in (-1,1):
                    c0=signc*Y
                    assert X*X-(a0*a0-1)*c0*c0==1
                    value=2*(a0*X+(a0*a0-1)*c0+1)
                    n=(B+signc)//2
                    assert value==4*pell(a0,n)[0]**2
                    assert value>=0 and isqrt(value)**2==value
                    wrong=2*(-a0*X+(a0*a0-1)*c0+1)
                    assert wrong<0
                    tested+=1
                r=(B-1)//2
                oldroot=(a0-1)*(pell(a0,r+1)[1]+pell(a0,r)[1])
                assert oldroot**2==(a0-1)*(X-1)
    # Exhaust the only integer k,c branches allowed when s=0: tau²+k²=1
    # and eta=k²-4c²>0.  Rational tau²>=0 gives |k|<=1.
    zero_branches=[]
    for k in (-1,0,1):
        for c0 in (-1,0,1):
            if k*k-4*c0*c0>0 and 1-k*k>=0:
                zero_branches.append((k,c0))
                for d0 in (-1,1):
                    assert 2*(0*d0+(0*0-1)*c0+1)==2
    assert zero_branches==[(-1,0),(1,0)]
    assert isqrt(2)**2!=2
    return {"exact_polynomial_identities":2,"signed_pell_branch_fixtures":tested,
            "zero_s_integer_branches":2,
            "rational_obstruction":"A rational square equal to the integer2 would be an integer square;2 is not one.",
            "quantified_proof":"halftrace_guard.tex"}


def check_table(m):
    stem=f"pell_crt_m{m}" if m!=56 else "crt_abc"
    predecessor=ROOT/"undecidability/pell_crt_v95"/f"{stem}_quadrics.json"
    target=HERE/f"halftrace_m{m}_quadrics.json"
    certpath=HERE/f"halftrace_m{m}_certificate.json"
    old,new,cert=[json.loads(p.read_text())for p in (predecessor,target,certpath)]
    assert hashlib.sha256(target.read_bytes()).hexdigest()==cert["table_sha256"]
    assert hashlib.sha256(predecessor.read_bytes()).hexdigest()==cert["pell_halftrace_predecessor_sha256"]
    ns=new["variable_names"]
    assert len(ns)==len(set(ns))==new["variables"]
    assert (new["variables"],len(new["residuals"]))==EXPECTED[m]
    assert (cert["variables"],cert["quadratic_rows"] )==EXPECTED[m] and cert["degree"]==4
    assert old["variables"]-new["variables"]==1 and len(old["residuals"])-len(new["residuals"])==1
    assert set(old["variable_names"])-set(ns)=={"s_inverse"}
    assert set(ns)-set(old["variable_names"])==set()
    before={r["name"]:r for r in old["residuals"]}
    after={r["name"]:r for r in new["residuals"]}
    changed="jones1980.pell_positive_root"
    deleted="jones1980.s.nonzero"
    assert before.keys()-after.keys()=={deleted} and after.keys()-before.keys()==set()
    for n in before.keys()-{changed,deleted}:
        assert named(before[n],old["variable_names"])==named(after[n],ns)
    for var,expected in [("s_inverse",deleted),("pell_d_positive_square",changed)]:
        occurrences=[r["name"]for r in old["residuals"]
                     if any(var==old["variable_names"][i-1]for t in r["terms"]for i in t["monomial"])]
        assert occurrences==[expected]
    a,d,ac,c,z=sp.symbols("a d ac c pell_d_positive_square")
    assert sp.expand(expr(after[changed],ns)-(z*z-2*a*d-2*a*ac+2*c-2))==0
    assert max(len(t["monomial"])for r in new["residuals"]for t in r["terms"])==2
    assert {i for r in new["residuals"]for t in r["terms"]for i in t["monomial"]}==set(range(1,len(ns)+1))
    assert new["ordinary_integer_inputs"]==old["ordinary_integer_inputs"]
    assert new["reciprocal_integer_inputs"]==old["reciprocal_integer_inputs"]
    assert len(new["ordinary_integer_inputs"])+len(new["reciprocal_integer_inputs"])==11
    assert new["outer_coordinates"]==old["outer_coordinates"]-1
    assert new["outer_residuals"]==old["outer_residuals"]-1
    assert new["source_universality_hypothesis"] is None
    assert new["source_coding_theorem_independently_reproved"] is False
    assert new["unconditional_undecidability_claim"] is False
    from build_halftrace import build
    assert (json.dumps(build(m),sort_keys=True,separators=(",",":"))+"\n").encode()==target.read_bytes()
    return {"interface":m,"variables":EXPECTED[m][0],"quadratic_rows":EXPECTED[m][1],
            "unchanged_rows":len(after)-1,"degree":4,"integer_inputs":11,"table_sha256":cert["table_sha256"]}


def main():
    report={"status":"pass","algebra":check_algebra(),"tables":[check_table(m)for m in (163,179,56)],
            "local_equivalence_unconditional":True,"unconditional_undecidability_claim":False}
    print(json.dumps(report,sort_keys=True,indent=2))


if __name__=="__main__":main()
