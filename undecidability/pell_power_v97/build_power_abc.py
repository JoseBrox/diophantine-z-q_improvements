#!/usr/bin/env python3
"""Complete the new fixed-power source with thirteen shared abc certificates."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from math import gcd,lcm
from pathlib import Path

import sympy as sp

from build_power_core import build_core

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PREDECESSOR=ROOT/"undecidability/pell_halftrace_v96/halftrace_m56_quadrics.json"
TEMPLATE=ROOT/"undecidability/source_repair_v93/coefficients/signed_abc_fixed_offsets_quadrics.json"
TRANSLATIONS={"power_delta":Fraction(9,16),"power_alpha":Fraction(12,16)}


def build():
    oldraw=PREDECESSOR.read_bytes()
    templateraw=TEMPLATE.read_bytes()
    old=json.loads(oldraw)
    source=json.loads(templateraw)
    data=build_core(old)
    names=list(data["variable_names"])
    template_names=source["variable_names"]
    template_private=[n for n in template_names if n.startswith("int_o_")]
    template_rows=[r for r in source["residuals"]if r["name"].startswith("integer.o.")]
    assert len(template_private)==47 and len(template_rows)==41
    z=source["fixed_offset_common_coordinate"]
    zz=source["fixed_offset_common_square"]
    assert z==data["fixed_offset_common_coordinate"]=="int_b_48"
    assert zz==data["fixed_offset_common_square"]=="abc_common_contact_square"
    for label in TRANSLATIONS:
        names.extend(n.replace("int_o_",f"int_{label}_",1)for n in template_private)
    assert len(names)==len(set(names))==704
    ids={n:i+1 for i,n in enumerate(names)}
    rows=list(data["residuals"])
    multipliers={}
    added_rows={}
    for label,delta in TRANSLATIONS.items():
        shift=delta-Fraction(9,16)
        rename={"o":label,**{n:n.replace("int_o_",f"int_{label}_",1)for n in template_private}}
        substitution={z:{z:Fraction(1),None:shift},
                      zz:{zz:Fraction(1),z:2*shift,None:shift*shift}}
        added_rows[label]=[]
        for row in template_rows:
            accumulated=defaultdict(lambda:sp.Integer(0))
            for term in row["terms"]:
                products={():sp.sympify(term["coefficient"])}
                for index in term["monomial"]:
                    oldname=template_names[index-1]
                    target=rename.get(oldname,oldname)
                    factors=substitution.get(target,{target:Fraction(1)})
                    nxt=defaultdict(lambda:sp.Integer(0))
                    for monomial,coefficient in products.items():
                        for name,scale in factors.items():
                            newmon=monomial if name is None else tuple(sorted((*monomial,ids[name])))
                            nxt[newmon]+=coefficient*sp.Rational(scale.numerator,scale.denominator)
                    products={mon:coef for mon,coef in nxt.items()if coef}
                for monomial,coefficient in products.items():
                    accumulated[monomial]+=coefficient
            accumulated={mon:sp.expand(coef)for mon,coef in accumulated.items()if coef}
            parameter=sp.Symbol("B_abc")
            rational_coefficients=[co for value in accumulated.values()for co in sp.Poly(value,parameter,domain=sp.QQ).all_coeffs()]
            denominator=lcm(*(int(co.q)for co in rational_coefficients))
            integer={mon:sp.expand(coef*denominator)for mon,coef in accumulated.items()}
            content=gcd(*(int(co)for value in integer.values()for co in sp.Poly(value,parameter,domain=sp.ZZ).all_coeffs()))
            name=row["name"].replace("integer.o.",f"integer.{label}.",1)
            multipliers[name]=str(Fraction(denominator,content))
            rows.append({"name":name,"terms":[
                {"coefficient":str(sp.expand(coef/content)),"monomial":list(mon)}
                for mon,coef in sorted(integer.items())]})
            added_rows[label].append(name)
    data.update({
        "variables":len(names),"variable_names":names,"residuals":rows,
        "shared_reference_blocks":13,
        "fixed_offset_translations":{**old["fixed_offset_translations"],**{k:str(v)for k,v in TRANSLATIONS.items()}},
        "pell_power_new_integer_inputs_certified":True,
        "pell_power_predecessor":str(PREDECESSOR.relative_to(ROOT)),
        "pell_power_predecessor_sha256":hashlib.sha256(oldraw).hexdigest(),
        "pell_power_abc_template":str(TEMPLATE.relative_to(ROOT)),
        "pell_power_abc_template_sha256":hashlib.sha256(templateraw).hexdigest(),
        "pell_power_abc_template_label":"o",
        "pell_power_abc_template_translation":"9/16",
        "pell_power_abc_added_translations":{k:str(v)for k,v in TRANSLATIONS.items()},
        "pell_power_abc_added_integer_rows":added_rows,
        "pell_power_abc_row_multipliers":multipliers,
        "pell_power_abc_added_auxiliary_coordinates":94,
        "pell_power_abc_added_integer_rows_count":82,
        "pell_power_abc_family_scope":"Thirteen distinct offsets modulo Z_2 with denominator16; all integer inputs nonzero in positive source completeness; the existing finite-family theorem applies to this larger fixed family.",
        "pell_power_savings":{"coordinates":29,"quadratic_rows":47},
    })
    assert (len(names),len(rows))==(704,595)
    assert len(data["ordinary_integer_inputs"])==13 and data["reciprocal_integer_inputs"]==[]
    assert len({r["name"]for r in rows})==len(rows)
    assert max(len(t["monomial"])for r in rows for t in r["terms"])==2
    assert {i for r in rows for t in r["terms"]for i in t["monomial"]}==set(ids.values())
    return data


def main():
    data=build()
    raw=(json.dumps(data,sort_keys=True,separators=(",",":"))+"\n").encode()
    target=HERE/"pell_power_abc_quadrics.json"
    target.write_bytes(raw)
    cert={
        "variables":704,"quadratic_rows":595,"degree":4,"integer_inputs":13,
        "table_sha256":hashlib.sha256(raw).hexdigest(),
        **{k:v for k,v in data.items()if k.startswith("pell_power_") and k!="pell_power_predecessor_power_metadata"},
        "source_universality_hypothesis":None,
        "source_coding_theorem":data["source_coding_theorem"],
        "source_coding_theorem_independently_reproved":False,
        "retained_arithmetic_interfaces":True,
        "unconditional_undecidability_claim":False,
    }
    target.with_name("pell_power_abc_certificate.json").write_text(json.dumps(cert,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"variables":704,"quadratic_rows":595,"integer_inputs":13,"table_sha256":cert["table_sha256"]}))


if __name__=="__main__":main()
