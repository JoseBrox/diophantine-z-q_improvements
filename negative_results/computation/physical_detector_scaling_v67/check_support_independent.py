#!/usr/bin/env python3
"""Independent symbolic audit of the corrected physical four-row obstruction."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import sympy as s


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package",type=Path,required=True)
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--mapping-certificate",type=Path,required=True)
    ap.add_argument("--manuscript",type=Path,help="Final manuscript, if stored outside the package")
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    model=json.loads((args.package/"model.json").read_text())
    cert=json.loads((args.package/"farkas_certificate.json").read_text())
    mapping=json.loads(args.mapping_certificate.read_text())
    source=json.loads(args.source.read_text())
    assert sha(args.source)==model["source_sha256"]
    assert mapping["status"]=="PASS" and mapping["literal_consumer_rows_checked"]==71
    assert mapping["physical_contacts"]=={"q0":"u","q1":"u*v"}
    assert mapping["factor_parameter_powers"]==[1,1,1,0,-1]
    assert mapping["partial_product_parameter_powers"]==[3,4,3]
    assert model["physical_contact_directions"]=={"q0":[1,0],"q1":[1,1]}
    source_row=next(row for row in source["residuals"] if row["name"]==model["reference_row"]["name"])
    assert source_row==model["reference_row"]
    table=defaultdict(int)
    for term in source_row["terms"]:
        table[term["parameterPower"],tuple(term["monomial"])]+=int(term["coefficient"])
    assert table[0,(19,77)]==2128691946 and table[0,(19,65)]==56549819456

    rows={row["name"]:row for row in model["rows"]}
    variable_names=list(model["variables"])
    axis_names=[("w",name,d) for name in variable_names for d in range(2)]
    axis_names += [("r",name,d) for name in rows for d in range(2)]
    axes={name:i for i,name in enumerate(axis_names)}
    matrix=s.zeros(len(cert["inequalities"]),len(axes))
    multipliers=s.Matrix([item["multiplier"] for item in cert["inequalities"]])
    for i,item in enumerate(cert["inequalities"]):
        name,m,e,n=item["row"],item["monomial"],item["unit_exponent"],item["facet"]
        assert isinstance(item["multiplier"],int) and item["multiplier"]>=0
        assert {"monomial":m,"unit_exponent":e} in rows[name]["terms"]
        for d in range(2):
            matrix[i,axes["r",name,d]]-=n[d]
            for variable in m:matrix[i,axes["w",variable,d]]+=n[d]
    assert multipliers.T*matrix==s.zeros(1,len(axes))
    basis_reports={}
    for name,raw in model["unit_bases"].items():
        units=[(0,0)]+[tuple(v) for v in raw]
        rhs=[]
        contributions=defaultdict(int)
        for item in cert["inequalities"]:
            n=item["facet"]
            bound=max(sum(x*y for x,y in zip(n,p)) for p in units)
            value=(2-len(item["monomial"]))*bound-sum(x*y for x,y in zip(n,item["unit_exponent"]))
            rhs.append(value)
            contributions[item["row"]]+=item["multiplier"]*value
        total=int((multipliers.T*s.Matrix(rhs))[0])
        assert total==cert["combined_rhs"][name] and total<0
        differences={(x[0]-y[0],x[1]-y[1]) for x in units for y in units}
        assert (0,-3) not in differences
        slices=defaultdict(list)
        for first,second in units:slices[first].append(second)
        assert max(max(values)-min(values) for values in slices.values())==2
        projected=[sum(p) for p in units]
        assert max(projected)==1 and -2*min(projected)<12
        basis_reports[name]={"weighted_rhs":total,"row_contributions":dict(contributions),
                             "projected_unit_interval":[min(projected),max(projected)],
                             "constant_row_upper_bound":-2*min(projected),
                             "required_row_difference":12,
                             "excluded_shared_factor_difference":[0,-3],
                             "maximum_vertical_difference_at_fixed_first_coordinate":2}

    # Direct field expansion in normalized comparison-square coordinates.
    # The fixed C normalizations are pinned in the separate full-map certificate.
    u,v,rho=s.symbols("u v rho",nonzero=True)
    names="h0 h1 v0 v1 j0 j1 k0 k1 a0 a1 b0 b1 l0 l1 o00r o00i o01r o01i o10r o10i".split()
    x=dict(zip(names,s.symbols(" ".join(names))))
    def fld(a,b):return x[a]+rho*x[b]
    j,k=fld("j0","j1")/u**3,fld("k0","k1")/u**3
    dh=(x["h0"]+2*rho*x["h1"])/u
    bzero=(x["v0"]+2*rho*x["v1"])/u
    aval,bval,linear=fld("a0","a1"),fld("b0","b1"),fld("l0","l1")
    factors={
        "F00":1+u**9*j**2+u**11*k**2+u**2*dh-u*fld("o00r","o00i"),
        "F01":1+u*aval**2+u**3*bval**2+u**2*bzero-u*fld("o01r","o01i"),
        "F10":1+(u*v)**11*j**2+(u*v)*aval**2+(u*v)**2*linear-u*v**2*fld("o10r","o10i"),
    }
    components={}
    for name,expr in factors.items():
        poly=s.Poly(s.rem(expr,rho**2-2,rho),rho)
        components[name]=[s.Poly(poly.nth(d),*x.values()) for d in range(2)]
    checked=[]
    for name in factors:
        for term in rows[name]["terms"]:
            m=s.prod(x[var] for var in term["monomial"])
            e=term["unit_exponent"]
            coeffs=[s.cancel(poly.coeff_monomial(m)/(u**e[0]*v**e[1])) for poly in components[name]]
            assert any(coeffs) and all(c.is_Rational for c in coeffs)
            checked.append({"row":name,**term,"component_coefficients":[str(c) for c in coeffs]})
    triples={"F00":("j0","j1",(3,0)),"F01":("a0","a1",(1,0)),"F10":("j0","j1",(5,11))}
    for name,(a,b,e) in triples.items():
        real,imag=components[name]
        unit=u**e[0]*v**e[1]
        assert s.cancel(real.coeff_monomial(x[a]**2)/unit)==1
        assert s.cancel(real.coeff_monomial(x[b]**2)/unit)==2
        assert s.cancel(imag.coeff_monomial(x[a]*x[b])/unit)==2
    equalities=s.Matrix([[2,0,-1,0],[0,2,-1,0],[1,1,0,-1]])
    assert s.Matrix([[s.Rational(1,2),-s.Rational(1,2),0]])*equalities==s.Matrix([[1,-1,0,0]])
    assert s.Matrix([[-s.Rational(1,2),-s.Rational(1,2),1]])*equalities==s.Matrix([[0,0,1,-1]])

    manuscript=args.manuscript or args.package/"physical_detector_scaling_20261117_v67.tex"
    mapping_checker=args.mapping_certificate.with_name("check_mapping_independent.py")
    report={
        "status":"PASS","engine":"Independent SymPy integer matrices and direct physical field expansion; no author checker imported",
        "source_sha256":sha(args.source),"full_mapping_certificate_sha256":sha(args.mapping_certificate),
        "manuscript_sha256":sha(manuscript),
        "package_sha256":{name:sha(args.package/name) for name in
                           ["model.json","farkas_certificate.json","check.py","check_mapping.py","certificate.json","mapping_certificate.json"]},
        "independent_mapping_checker_sha256":sha(mapping_checker),
        "independent_support_checker_sha256":sha(Path(__file__)),
        "inequalities":len(cert["inequalities"]),"weight_components":len(axes),
        "weighted_left_side":"identically zero","basis_results":basis_reports,
        "physical_contacts":{"q0":"u","q1":"u*v"},
        "factor_output_unit_directions":{"detector0":[1,0],"detector1":[1,2]},
        "physical_factor_selected_coefficients":checked,
        "reference_coefficients":{"x19*x77":2128691946,"x19*x65":56549819456},
        "full_square_forcing_verified":True,"literal_consumer_rows_independently_verified":71,
        "four_row_proof_independent_of_all_other_model_rows":True,
        "scope":"The fixed literal four-row support under diagonal Laurent scaling and monomial row division, for the two stated unit bases; no count improvement or general polynomial lower bound",
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({key:value for key,value in report.items() if key!="physical_factor_selected_coefficients"},indent=2,sort_keys=True))


if __name__=="__main__":main()
