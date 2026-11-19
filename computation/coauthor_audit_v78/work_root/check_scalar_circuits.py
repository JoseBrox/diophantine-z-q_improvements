"""Independent replay of the new scalar, targets, scales and determinant bounds."""
from pathlib import Path
from functools import cache
from fractions import Fraction
import importlib.util
import inspect
import json
import math
import sys

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parent/"H10-quartics"
REPO = HERE.parents[1]/"diophantine"


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def run(route):
    sys.argv=["check_positive.py","--repo",str(REPO),"--output",str(HERE/"four_contact")]
    check=load("four_contact_independent_"+route,ARCHIVE/"fewvars/check_positive.py")
    directory=HERE/"four_contact"/route
    source=json.loads((directory/"native.json").read_text())
    parent=json.loads((directory/"parent.json").read_text())
    ordinary=json.loads((directory/"certificate.json").read_text())
    reduced=json.loads((directory/"reduced.json").read_text())
    c=check.Circuit()
    for i,node in enumerate(source["coefficient_dag"]):
        assert c.node(*node)==i
    def r(value):
        return check.Rational(c,value["numerator"],value["denominator"])
    def leaf(i):
        return check.Rational(c,i,c.one)
    def eq(a,b):
        assert (a.n,a.d)==(b.n,b.d), ((a.n,a.d),(b.n,b.d))
    x=leaf(c.node("variable",0))
    beta=1632*x*x+2477
    target=x*x+1
    L=source["family_parameter"]["value"]
    # The source graph is also checked for the two exact constant powers below.
    p=lambda e:leaf(c.power(c.node("int",67),e))
    A=beta*(beta-1)
    B=(beta-2401)*(32*beta+343)
    T=(1224*(p((L+1)//2)+1))**2
    raw=c.rational(1)
    for factor in (beta,beta-1,beta-2401,32*beta+343):
        raw*=factor
    denominator=B+T*A
    rho=102**2*p(L)*T*raw/denominator**2
    event=lambda name:next(e for e in source["events"] if e["operation"]==name)
    height=event("combined_height_scales")
    for val,key in [(beta,"beta"),(raw,"raw_scalar_contact"),(denominator,"scalar_denominator"),(rho,"scalar_contact")]:
        eq(val,r(height[key]))
    points=[e for e in source["events"] if e["operation"]=="point_block"]
    roots=[next(e for e in points if e["name"]==name) for name in ("A","S","T","Z")]
    aggregate=[sum((r(e["x"][k]) for e in roots),c.rational(0)) for k in (0,1)]
    if route=="general25":
        trace=2*aggregate[0]
        eq(trace,r(height["trace"]))
        scales=[c.rational(1),1+rho*trace**2]
    else:
        for a,b in zip(aggregate,height["aggregate_components"],strict=True):
            eq(a,r(b))
        scales=[c.rational(1),1+rho*aggregate[0]**2,1+rho*(aggregate[0]+aggregate[1])**2]
    for a,b in zip(scales,height["scales"],strict=True):
        eq(a,r(b))
    tests=event("comparison_and_scalar_tests")
    eq(r(tests["comparison"][14][0]),r(tests["L"][0][0])-target)
    assert tests["comparison_powers"]==[1]*10+[2]*6
    chart=load("four_contact_reference_chart_"+route,REPO/"computation/few_variables/even_valuation25_v75/build_source.py")
    upstream=__import__("build_sources")
    base=upstream.General25 if route=="general25" else upstream.Explicit27
    class Reference(base):
        point=chart.FullAuxiliary25.point
    reference=Reference(L).build()
    new_sign=check.signatures(source["coefficient_dag"])
    old_sign=check.signatures(reference["coefficient_dag"])
    def normalize(v,sign):
        if isinstance(v,list):
            return [normalize(z,sign) for z in v]
        if isinstance(v,dict):
            if set(v)=={"numerator","denominator"}:
                return [sign[v["numerator"]],sign[v["denominator"]]]
            return {k:normalize(z,sign) for k,z in v.items()}
        return v
    old_tests=next(e for e in reference["events"] if e["operation"]=="comparison_and_scalar_tests")
    for key in ("scalar","L","Lprime","comparison_orders","scalar_orders"):
        assert normalize(tests[key],new_sign)==normalize(old_tests[key],old_sign)
    for i in range(16):
        if i!=14:
            assert normalize(tests["comparison"][i],new_sign)==normalize(old_tests["comparison"][i],old_sign)
    assert normalize(tests["comparison"][14][1],new_sign)==normalize(old_tests["comparison"][14][1],old_sign)
    old_points=[e for e in reference["events"] if e["operation"]=="point_block"]
    assert normalize(points,new_sign)==normalize(old_points,old_sign)
    slope=leaf(c.node("variable",next(v["index"] for v in source["variables"] if "slope" in v["name"])))
    theta=[Fraction(0),Fraction(-1,2),Fraction(-1),Fraction(1,2399),Fraction(-32,407)]
    detectors=[e for e in source["events"] if e["operation"]=="combined_detector"]
    for j,(scale,e) in enumerate(zip(scales,detectors,strict=True)):
        argument=scale*slope
        delta=argument-(-j-1)
        contacts=[offset+t for offset in (4*j+2,4*j+4) for t in theta]
        assert e["contacts"]==list(map(str,contacts))
        F=c.rational(1)
        for contact in contacts:
            F*=argument-contact
        R=F/delta**10
        q=rho*R
        for val,key in [(scale,"scale"),(argument,"argument"),(delta,"delta"),(F,"F"),(R,"contact_function"),(q,"combined_coefficient")]:
            eq(val,r(e[key]))
        for order,weight in zip(tests["comparison_orders"],e["comparison_weights"],strict=True):
            eq(q/(delta**2*q**(2*order)),r(weight))
        for order,weight,test,value in zip(tests["scalar_orders"],e["scalar_weights"],tests["scalar"],e["normalized_scalar"],strict=True):
            eq(q/q**(2*order),r(weight))
            z=R*r(test)
            eq(R**order*z/(1+z),r(value[0]))
            eq(c.rational(0),r(value[1]))
    # Full upstream independent coefficient/guard replay, with the new semantics
    # established above. Its general25 path selects the correct four-root/five-full
    # chart table even for the three-pole route.
    check.ancestor=lambda _:source
    audit_body=inspect.getsource(check.audit)
    assert audit_body.count("directory=args.output/route")==1
    audit_body=audit_body.replace("directory=args.output/route",f"directory=args.output/{route!r}")
    exec(compile(audit_body,"four_contact_independent_majorants","exec"),check.__dict__)
    replay=check.audit("general25")

    nodes=source["coefficient_dag"]
    @cache
    def atoms(i):
        op,*ys=nodes[i]
        if op=="int":
            assert ys[0]
            return set()
        if op in ("neg","pow"):
            return atoms(ys[0]) if op=="neg" or ys[1] else set()
        if op=="mul":
            return set().union(*(atoms(j) for j in ys))
        return {i}
    automatic=set()
    for f in [height["scalar_contact"],height["scalar_denominator"],*height["scales"]]:
        automatic |= atoms(f["numerator"]) | atoms(f["denominator"])
    automatic &= set(ordinary["norm_guard_nodes"])
    # All these rational fractions depend on base coordinates only; no root or
    # denominator needing the guard being deleted is used in their positivity.
    finite={i for i,row in enumerate(nodes) if row[0]=="variable" and row[1]>=source["retained_base_count"]}
    @cache
    def dependencies(i):
        op,*ys=nodes[i]
        if op in ("int","parameter"):
            return set()
        if op=="variable":
            return {i} if i in finite else set()
        args=ys[:1] if op in ("pow","neg") else ys
        return set().union(*(dependencies(j) for j in args))
    assert all(not dependencies(i) for i in automatic)
    assert automatic==set(reduced["early_positive_atoms"])
    point_atoms=set()
    blocks={b["name"]:b for b in source["finite_blocks"] if b["kind"]=="point_block"}
    for point in points:
        h0,h1=map(r,point["h"])
        norm=h0*h0-2*h1*h1
        assert norm.d==c.one
        point_atoms |= atoms(norm.n)
        if point.get("chart")!="full_auxiliary":
            point_atoms.add(blocks[point["name"]]["variable_nodes"][2])
    assert len(point_atoms)==13 and point_atoms==set(reduced["automatic_point_atoms"])
    assert all(not dependencies(i) for i in point_atoms if i not in {b["variable_nodes"][2] for b in blocks.values()})
    removed=automatic|point_atoms
    kept=set(ordinary["norm_guard_nodes"])-removed
    assert kept==set(reduced["norm_guard_nodes"])
    factors={row["node"]:row for row in parent["subalgebra_norm_factors"]}
    g=sum(factors[i]["scalar_norm_degree_bound"] for i in kept)
    gl=sum(factors[i]["scalar_norm_log2_l1_bound"] for i in kept)
    saved=sum(factors[i]["scalar_norm_log2_l1_bound"] for i in removed)
    assert sum(factors[i]["scalar_norm_degree_bound"] for i in point_atoms)==50
    n=ordinary["rank"]
    assert reduced["guard_degree"]==g
    assert reduced["degree"]==n*(1+g+ordinary["separator_degree"])
    assert reduced["log2_l1"]==ordinary["log2_l1"]-n*saved
    if route=="general25":
        projective=json.loads((directory/"projective.json").read_text())
        assert set(projective["automatic_point_atoms"])==point_atoms
        point=[row for row in parent["quadratic_tower"] if row["kind"]!="pole"]
        a,b=[row for row in parent["quadratic_tower"] if row["kind"]=="pole"]
        dN=max(3*a["root_weight"]+max(b["root_weight"],b["envelope_degree"]),3*a["envelope_degree"]+b["root_weight"])
        dD=3*a["envelope_degree"]+max(b["root_weight"],b["envelope_degree"])
        lJ=1+max(b["root_operator_log2_norm"],b["envelope_log2_l1"]+1)
        lN=1+max(3*a["root_operator_log2_norm"]+lJ,3*(a["envelope_log2_l1"]+1)+b["root_operator_log2_norm"])
        lD=3+3*(a["envelope_log2_l1"]+1)+lJ
        for row in reversed(point):
            dN=row["root_weight"]+max(dN,dD)
            dD+=row["envelope_degree"]
            lN=row["root_operator_log2_norm"]+1+max(lN,lD)
            lD+=2+row["envelope_log2_l1"]
        assert (dN,dD)==(projective["numerator_degree"],projective["denominator_degree"])
        assert projective["degree"]==n*max(dD,1+g+dN)
        assert projective["log2_l1"]==n*(1+max(lD,gl+lN))
        final=projective
    else:
        final=reduced
    v=source["total_external_variables"]
    d=final["degree"]
    assert final["support_power"]==(math.comb(d+v,v)-math.comb(d-n+v-1,v)).bit_length()
    assert final["height_double_power"]==final["log2_l1"].bit_length()
    return {"route":route,"degree":d,"variables":v,"rank":n,"guard_degree":g,
            "early_positive_atoms":sorted(automatic),"independent_replay":list(replay),
            "automatic_point_atoms":sorted(point_atoms),
            "log2_l1":final["log2_l1"],"support_power":final["support_power"]}


if __name__=="__main__":
    answers=[run(route) for route in ("general25","explicit27")]
    certificate={"status":"PASS","new_producer_imported":False,"pinned_source_interfaces_imported":True,"routes":answers}
    (HERE/"scalar_circuit_independent.json").write_text(json.dumps(certificate,indent=2)+"\n")
    print(json.dumps(certificate,indent=2))
