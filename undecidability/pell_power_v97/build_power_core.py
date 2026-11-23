#!/usr/bin/env python3
"""Replace the fixed power circuit by the proved two-integer Pell certificate.

build_core(old) adds power_delta and power_alpha as integer inputs but does
NOT supply their integer-certificate rows. A complete-table builder must
append both certificates with the appropriate shared-family construction.
The proof is pell_power_replacement.tex. The instance range is x > 32*z.
"""
from __future__ import annotations

from pathlib import Path

L=5**60
NEW_INPUTS=["power_delta","power_alpha"]
NEW_REGISTERS=["power_b4","power_A","power_C","power_D","power_modulus","power_AC"]
POSITIVE_NAMES=[f"power_positive_{label}_{i}" for label in ("q","bound") for i in (1,2,3)]
DELETED_PREFIX="jones1980.ceiling_power."


def named_terms(row,names):
    return sorted((str(t["coefficient"]),tuple(sorted(names[i-1]for i in t["monomial"])))for t in row["terms"])


def build_core(old):
    assert old["source_universality_hypothesis"] is None
    assert old["pell_core_source_p_parameter"]=="2*w*s^2*r^2*n^6"
    assert old["pell_halftrace_savings"]=={"coordinates":1,"quadratic_rows":1}
    names=old["variable_names"]
    rows={r["name"]:r for r in old["residuals"]}
    assert len(rows)==len(old["residuals"])
    removed_names={"power_001"}|{n for n in names if n.startswith("ceiling_power_")}
    removed_rows={"jones1980.power_001.definition"}|{n for n in rows if n.startswith(DELETED_PREFIX)}
    assert len(removed_names)==137 and len(removed_rows)==138
    changed="jones1980.B5.definition"
    if named_terms(rows[changed],names)==[("-1",("int_b_29","power_001")),("1",("B5",))]:
        assert named_terms(rows[changed],names)==[("-1",("int_b_29","power_001")),("1",("B5",))]
        assert named_terms(rows["jones1980.power_001.definition"],names)==[
            ("-1",("b","int_b_29")),("1",("power_001",))]
        b4_terms=[(1,("power_b4",)),(-1,("int_b_29","int_b_29"))]
        square_chart="ordinary input square int_b_29=b^2"
    else:
        # General global chart: int_b_37=b^2/rho,
        # int_b_160=1/rho and int_b_161=1/rho^2.  The retained
        # global gauge guard already proves the latter is nonzero.
        assert named_terms(rows[changed],names)==[
            ("-1",("int_b_37","power_001")),("1",("B5","int_b_160"))]
        assert named_terms(rows["jones1980.power_001.definition"],names)==[
            ("-1",("b","int_b_37")),("1",("int_b_160","power_001"))]
        b4_terms=[(1,("int_b_161","power_b4")),(-1,("int_b_37","int_b_37"))]
        square_chart="int_b_37=b^2/rho and nonzero int_b_161=1/rho^2"
    occurrences={}
    for name in sorted(removed_names):
        found=[row["name"]for row in old["residuals"]
               if any(name==names[i-1]for t in row["terms"]for i in t["monomial"])]
        assert found and set(found)<=removed_rows|{changed},(name,found)
        occurrences[name]=found
    added=NEW_INPUTS+NEW_REGISTERS+POSITIVE_NAMES
    assert not set(added)&set(names)
    newnames=[n for n in names if n not in removed_names]+added
    ids={n:i+1 for i,n in enumerate(newnames)}

    def serialize(terms):
        return sorted([{"coefficient":str(coef),"monomial":sorted(ids[n]for n in mon)}
                       for coef,mon in terms],key=lambda t:t["monomial"])

    newrows=[]
    for row in old["residuals"]:
        if row["name"] in removed_rows:continue
        if row["name"]==changed:
            newrows.append({"name":changed,"terms":serialize([(1,("B5",)),(-1,("b","power_b4"))])})
        else:
            newrows.append({"name":row["name"],"terms":[
                {"coefficient":t["coefficient"],"monomial":sorted(ids[names[i-1]]for i in t["monomial"])}
                for t in row["terms"]]})

    def append(suffix,terms):
        newrows.append({"name":"jones1980.pell_power."+suffix,"terms":serialize(terms)})

    append("b4.definition",b4_terms)
    append("A.definition",[(2,("power_A",)),(-1,("power_b4","B5")),(-8,("B5",)),
                           (-1,("b",)),(8,()),(-10,("B5","s")),(10,("s",))])
    append("C.definition",[(1,("power_C",)),(-L,()),(-1,("power_delta","power_A")),(1,("power_delta",))])
    append("AC.definition",[(1,("power_AC",)),(-1,("power_A","power_C"))])
    append("D.norm",[(1,("power_D","power_D")),(-1,("power_AC","power_AC")),
                     (1,("power_C","power_C")),(-1,())])
    append("modulus.definition",[(1,("power_modulus",)),(-2,("b","power_A")),(1,("b","b")),(1,())])
    append("q.congruence",[(1,("q",)),(-1,("power_D",)),(1,("power_AC",)),
                           (-1,("b","power_C")),(1,("power_alpha","power_modulus"))])
    for label,base in [
        ("q",[(2,("q",)),(-2,("B5",)),(-2,())]),
        ("bound",[(2,("c","c")),(-2,("power_C","power_C")),(-2,())]),
    ]:
        terms=list(base)
        for i in (1,2,3):
            name=f"power_positive_{label}_{i}"
            terms.extend([(-1,(name,)),(-1,(name,name))])
        append("positive."+label,terms)
    new=dict(old)
    historical_keys=[key for key in old if key.startswith("ceiling_power_")
                     or key.startswith("power_chain") or key=="power_multiplications"]
    new["pell_power_predecessor_power_metadata"]={key:old[key]for key in historical_keys}
    for key in historical_keys:
        new.pop(key,None)
    new.update({
        "variables":len(newnames),"variable_names":newnames,"residuals":newrows,
        "outer_coordinates":old["outer_coordinates"]-123,
        "outer_residuals":old["outer_residuals"]-129,
        "ordinary_integer_inputs":old["ordinary_integer_inputs"]+NEW_INPUTS,
        "integer_blocks":13,
        "pell_power_proof":"undecidability/pell_power_v97/pell_power_replacement.tex",
        "pell_power_exponent":str(L),
        "pell_power_instance_range":"x > 32*z; only a fixed finite initial segment is removed",
        "instance_range":"positive integer x > 32*z",
        "pell_power_new_integer_inputs":NEW_INPUTS,
        "pell_power_new_registers":NEW_REGISTERS,
        "pell_power_input_square_chart":square_chart,
        "pell_power_new_positivity_coordinates":POSITIVE_NAMES,
        "pell_power_removed_coordinates":sorted(removed_names),
        "pell_power_removed_rows":sorted(removed_rows),
        "pell_power_changed_row":changed,
        "pell_power_removed_occurrences":occurrences,
        "pell_power_parameter":"2*A=b^9+8*b^5+b-8+10*(b^5-1)*s",
        "pell_power_geometric_integrality":"A=1 mod5 and (b^5-1) divides2*b*A-b^2-1 force q=+/-1 mod(b^5-1) before identifying the exponent",
        "pell_power_bounds":["q > b^5","C^2 < c^2"],
        "pell_power_new_integer_inputs_certified":False,
        "pell_power_core_coordinate_change":-123,
        "pell_power_core_row_change":-129,
        "pell_power_signed_branches":"Auxiliary C=0 and all negative/inverse Pell branches explicitly excluded in the proof",
        "unconditional_undecidability_claim":False,
    })
    assert len(newrows)==len(old["residuals"])-129
    assert len(newnames)==old["variables"]-123
    assert max(len(t["monomial"])for row in newrows for t in row["terms"])==2
    assert {i for row in newrows for t in row["terms"]for i in t["monomial"]}==set(ids.values())
    return new
