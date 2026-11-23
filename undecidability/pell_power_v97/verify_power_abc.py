#!/usr/bin/env python3
"""Independent audit of the complete 704-variable fixed-power abc quartic."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def named(row,names):
    return sorted((str(t["coefficient"]),tuple(sorted(names[i-1]for i in t["monomial"])))for t in row["terms"])


def expression(row,names):
    return sp.expand(sum(sp.sympify(t["coefficient"])*sp.prod(sp.Symbol(names[i-1])for i in t["monomial"])
                         for t in row["terms"]))


def main():
    predecessor=ROOT/"undecidability/pell_halftrace_v96/halftrace_m56_quadrics.json"
    template=ROOT/"undecidability/source_repair_v93/coefficients/signed_abc_fixed_offsets_quadrics.json"
    target=HERE/"pell_power_abc_quadrics.json"
    certpath=HERE/"pell_power_abc_certificate.json"
    old,source,new,cert=[json.loads(p.read_text())for p in (predecessor,template,target,certpath)]
    assert hashlib.sha256(target.read_bytes()).hexdigest()==cert["table_sha256"]
    assert hashlib.sha256(predecessor.read_bytes()).hexdigest()==cert["pell_power_predecessor_sha256"]
    assert hashlib.sha256(template.read_bytes()).hexdigest()==cert["pell_power_abc_template_sha256"]
    ns=new["variable_names"];oldns=old["variable_names"];srcns=source["variable_names"]
    assert len(ns)==len(set(ns))==new["variables"]==cert["variables"]==704
    before={r["name"]:r for r in old["residuals"]}
    after={r["name"]:r for r in new["residuals"]}
    assert len(after)==len(new["residuals"])==cert["quadratic_rows"]==595
    assert cert["degree"]==4 and cert["integer_inputs"]==13
    removed_names={"power_001"}|{n for n in oldns if n.startswith("ceiling_power_")}
    removed_rows={"jones1980.power_001.definition"}|{n for n in before if n.startswith("jones1980.ceiling_power.")}
    assert len(removed_names)==137 and len(removed_rows)==138
    assert set(oldns)-set(ns)==removed_names
    assert before.keys()-after.keys()==removed_rows
    core_names={"power_delta","power_alpha","power_b4","power_A","power_C","power_D","power_modulus","power_AC"}
    core_names|={f"power_positive_{tag}_{i}"for tag in ("q","bound")for i in (1,2,3)}
    template_private={n for n in srcns if n.startswith("int_o_")}
    assert len(template_private)==47
    added_private={n.replace("int_o_",f"int_{label}_",1)
                   for label in ("power_delta","power_alpha")for n in template_private}
    assert len(added_private)==94
    assert set(ns)-set(oldns)==core_names|added_private
    for coordinate in removed_names:
        occurrences={r["name"]for r in old["residuals"]
                     if any(coordinate==oldns[i-1]for t in r["terms"]for i in t["monomial"])}
        assert occurrences and occurrences<=removed_rows|{"jones1980.B5.definition"}
    unchanged=before.keys()-removed_rows-{"jones1980.B5.definition"}
    for name in unchanged:
        assert named(before[name],oldns)==named(after[name],ns)

    symbols={n:sp.Symbol(n)for n in ns}
    b,B5,q,c,s=(symbols[n]for n in ("b","B5","q","c","s"))
    b4,A,C,D,m,AC=(symbols[n]for n in ("power_b4","power_A","power_C","power_D","power_modulus","power_AC"))
    delta,alpha=(symbols[n]for n in ("power_delta","power_alpha"))
    expected={
        "jones1980.B5.definition":B5-b*b4,
        "b4.definition":b4-symbols["int_b_29"]**2,
        "A.definition":2*A-b4*B5-8*B5-b+8-10*(B5-1)*s,
        "C.definition":C-5**60-delta*(A-1),
        "AC.definition":AC-A*C,
        "D.norm":D*D-AC*AC+C*C-1,
        "modulus.definition":m-2*b*A+b*b+1,
        "q.congruence":q-D+AC-b*C+alpha*m,
    }
    for tag,value in [("q",q-B5),("bound",c*c-C*C)]:
        expected["positive."+tag]=2*(value-1)-sum(
            symbols[f"power_positive_{tag}_{i}"]**2+symbols[f"power_positive_{tag}_{i}"]for i in (1,2,3))
    for suffix,value in expected.items():
        name=suffix if suffix.startswith("jones1980.")else "jones1980.pell_power."+suffix
        assert sp.expand(expression(after[name],ns)-value)==0,name

    # Independent expansion from the unshifted o certificate, with simultaneous
    # affine substitution of both z and its shared square.  This is distinct
    # from the builder's sparse coefficient convolution.
    zr=sp.Symbol("int_b_48");zz=sp.Symbol("abc_common_contact_square")
    checked_copies=0
    for label,shift in [("power_delta",sp.Rational(0)),("power_alpha",sp.Rational(3,16))]:
        mapping={sp.Symbol("o"):symbols[label],
                 **{sp.Symbol(n):symbols[n.replace("int_o_",f"int_{label}_",1)]for n in template_private},
                 zr:zr+shift,zz:zz+2*shift*zr+shift**2}
        copied=[row for row in source["residuals"]if row["name"].startswith("integer.o.")]
        assert len(copied)==41
        for row in copied:
            name=row["name"].replace("integer.o.",f"integer.{label}.",1)
            translated=sp.expand(expression(row,srcns).subs(mapping,simultaneous=True))
            multiplier=sp.Rational(new["pell_power_abc_row_multipliers"][name])
            assert multiplier!=0
            assert sp.expand(expression(after[name],ns)-multiplier*translated)==0,name
            checked_copies+=1
    new_core_rows={name for name in after if name.startswith("jones1980.pell_power.")}
    new_cert_rows={name for name in after if name.startswith(("integer.power_delta.","integer.power_alpha."))}
    assert len(new_core_rows)==9 and len(new_cert_rows)==82
    assert after.keys()-before.keys()==new_core_rows|new_cert_rows
    assert max(len(t["monomial"])for r in new["residuals"]for t in r["terms"])==2
    assert {i for r in new["residuals"]for t in r["terms"]for i in t["monomial"]}==set(range(1,705))
    parameters=[sp.Symbol(n)for n in ("x","z","u","y","B_abc")]
    for row in new["residuals"]:
        for term in row["terms"]:
            sp.Poly(sp.sympify(term["coefficient"]),*parameters,domain=sp.ZZ)
    assert new["ordinary_integer_inputs"]==old["ordinary_integer_inputs"]+["power_delta","power_alpha"]
    assert len(new["ordinary_integer_inputs"])==new["integer_blocks"]==new["shared_reference_blocks"]==13
    assert new["reciprocal_integer_inputs"]==[]
    expected_offsets={**old["fixed_offset_translations"],"power_delta":"9/16","power_alpha":"3/4"}
    assert new["fixed_offset_translations"]==expected_offsets
    values=[Fraction(v)for v in expected_offsets.values()]
    assert len(values)==len(set(values))==13
    for i,x in enumerate(values):
        for y in values[:i]:
            assert (x-y).denominator in (2,4,8,16)
    assert new["pell_power_new_integer_inputs_certified"] is True
    assert new["instance_range"]=="positive integer x > 32*z"
    assert "power_chain"not in new and "power_multiplications"not in new
    assert not any(k.startswith("ceiling_power_")for k in new)
    assert new["pell_power_predecessor_power_metadata"]["power_multiplications"]==139
    assert new["source_universality_hypothesis"] is None
    assert new["source_coding_theorem_independently_reproved"] is False
    assert new["unconditional_undecidability_claim"] is False
    from build_power_abc import build
    assert (json.dumps(build(),sort_keys=True,separators=(",",":"))+"\n").encode()==target.read_bytes()
    print(json.dumps({"status":"pass","variables":704,"quadratic_rows":595,"degree":4,
                      "integer_inputs":13,"removed_power_coordinates":137,"added_source_coordinates":14,
                      "added_integer_auxiliary_coordinates":94,"unchanged_predecessor_rows":len(unchanged),
                      "independently_expanded_integer_rows":checked_copies,
                      "coefficient_domain":"Z[x,z,u,y,B_abc]",
                      "instance_range":"x > 32*z","table_sha256":cert["table_sha256"],
                      "source_coding_theorem_external":True,"unconditional_undecidability_claim":False},
                     sort_keys=True,indent=2))


if __name__=="__main__":main()
