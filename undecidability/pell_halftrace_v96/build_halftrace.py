#!/usr/bin/env python3
"""Absorb s!=0 into the Pell half-trace square; save one coordinate/row."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE_DIR=ROOT/"undecidability/pell_crt_v95"
SOURCE_STEMS={163:"pell_crt_m163",179:"pell_crt_m179",56:"crt_abc"}
CHANGED="jones1980.pell_positive_root"
REMOVED="jones1980.s.nonzero"
SQUARE="pell_d_positive_square"


def named_terms(row,names):
    return sorted((str(t["coefficient"]),tuple(sorted(names[i-1] for i in t["monomial"])))for t in row["terms"])


def build_data(old):
    assert old["source_universality_hypothesis"] is None
    assert len(old["ordinary_integer_inputs"])+len(old["reciprocal_integer_inputs"])==11
    assert old["pell_core_source_p_parameter"]=="2*w*s^2*r^2*n^6"
    names=old["variable_names"]
    rows={row["name"]:row for row in old["residuals"]}
    assert named_terms(rows[CHANGED],names)==[
        ("-1",()),("-1",("a","d")),("1",("a",)),("1",("d",)),("1",(SQUARE,SQUARE))]
    assert named_terms(rows[REMOVED],names)==[("-1",()),("1",("s","s_inverse"))]
    occurrences={}
    for name,expected in [("s_inverse",REMOVED),(SQUARE,CHANGED)]:
        found=[row["name"] for row in old["residuals"]
               if any(name==names[i-1]for t in row["terms"]for i in t["monomial"])]
        assert found==[expected]
        occurrences[name]=found
    new_names=[n for n in names if n!="s_inverse"]
    ids={n:i+1 for i,n in enumerate(new_names)}
    new_rows=[]
    for row in old["residuals"]:
        if row["name"]==REMOVED:continue
        if row["name"]==CHANGED:
            ts=[(1,(SQUARE,SQUARE)),(-2,("a","d")),(-2,("a","ac")),(2,("c",)),(-2,())]
            new_rows.append({"name":CHANGED,"terms":sorted([
                {"coefficient":str(coef),"monomial":sorted(ids[n]for n in mon)}for coef,mon in ts],key=lambda t:t["monomial"])})
        else:
            new_rows.append({"name":row["name"],"terms":[
                {"coefficient":t["coefficient"],"monomial":sorted(ids[names[i-1]]for i in t["monomial"])}for t in row["terms"]]})
    new=dict(old)
    new.update({
        "variables":len(new_names),"variable_names":new_names,"residuals":new_rows,
        "outer_coordinates":old["outer_coordinates"]-1,"outer_residuals":old["outer_residuals"]-1,
        "pell_halftrace_proof":"undecidability/pell_halftrace_v96/halftrace_guard.tex",
        "pell_halftrace_changed_row":CHANGED,"pell_halftrace_removed_row":REMOVED,
        "pell_halftrace_removed_coordinate":"s_inverse",
        "pell_halftrace_new_equation":"pell_d_positive_square^2=2*a*d+2*a*ac-2*c+2, with ac=a*c",
        "pell_halftrace_private_occurrences":occurrences,
        "pell_halftrace_savings":{"coordinates":1,"quadratic_rows":1},
        "pell_halftrace_nonzero_scope":"s=0 forces p=a=c=0, k=+/-1, d=+/-1; the new square would equal2, impossible over Q.",
        "pell_halftrace_sign_scope":"For |a|>=2 and |c|>1, the norm and new square force a*d>0.",
        "pell_halftrace_completeness":"For c=Y_B(a), d=X_B(a), B odd, choose the square coordinate 2*X_((B+1)/2)(a).",
        "pell_halftrace_integer_inputs_unchanged":True,
        "pell_halftrace_previous_positive_root":old["pell_core_positive_root"],
        "pell_core_positive_root":"pell_d_positive_square^2=2*(a*d+(a^2-1)*c+1), implemented using ac=a*c",
        "unconditional_undecidability_claim":False,
    })
    assert len(new_rows)==len(old["residuals"])-1
    assert new["variables"]==old["variables"]-1
    assert max(len(t["monomial"])for row in new_rows for t in row["terms"])==2
    assert {i for row in new_rows for t in row["terms"]for i in t["monomial"]}==set(ids.values())
    return new


def build(m):
    predecessor=SOURCE_DIR/f"{SOURCE_STEMS[m]}_quadrics.json"
    raw=predecessor.read_bytes()
    new=build_data(json.loads(raw))
    new["pell_halftrace_predecessor"]=str(predecessor.relative_to(ROOT))
    new["pell_halftrace_predecessor_sha256"]=hashlib.sha256(raw).hexdigest()
    return new


def main():
    for m in (163,179,56):
        data=build(m)
        raw=(json.dumps(data,sort_keys=True,separators=(",",":"))+"\n").encode()
        path=HERE/f"halftrace_m{m}_quadrics.json"
        path.write_bytes(raw)
        cert={"variables":data["variables"],"quadratic_rows":len(data["residuals"]),"degree":4,
              "table_sha256":hashlib.sha256(raw).hexdigest(),
              **{k:v for k,v in data.items()if k.startswith("pell_halftrace_")},
              "source_universality_hypothesis":None,
              "source_coding_theorem":data["source_coding_theorem"],
              "source_coding_theorem_independently_reproved":False,
              "retained_arithmetic_interfaces":True,
              "unconditional_undecidability_claim":False}
        path.with_name(f"halftrace_m{m}_certificate.json").write_text(json.dumps(cert,sort_keys=True,indent=2)+"\n")
        print(json.dumps({"interface":m,"variables":data["variables"],"quadratic_rows":len(data["residuals"]),"table_sha256":cert["table_sha256"]}))


if __name__=="__main__":main()
