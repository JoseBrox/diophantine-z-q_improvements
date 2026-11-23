"""Independent exact verifier of the three BB v2 degree improvements.

The new producers are never imported.  This checker reuses only the pinned
circuit interfaces and the archived independent operator-norm verifier, and
reconstructs the modified scalar and every product-pole equation itself.

Usage: python check_degrees.py --work-root PATH --report PATH
PATH contains diophantine/, audit_20261119/, bb_twelve/, and bb_general/.
"""
from pathlib import Path
from fractions import Fraction
from fractions import Fraction as F
from functools import cache
import argparse
import hashlib
import importlib.util
import inspect
import json
import math
import sys
import sympy as sp

SHIFTS=[-9,-8,-7,-5,-4,-3,-2,-1,6,10,11,12]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def run_abc():
    sys.argv=["check_positive.py","--balanced","--repo",str(REPO),"--output",str(WORK/"bb_twelve")]
    check=load("twelve_independent_positive",ARCHIVE/"fewvars/check_positive.py")
    directory=WORK/"bb_twelve/abc11"
    source=json.loads((directory/"native.json").read_text())
    parent=json.loads((directory/"parent.json").read_text())
    ordinary=json.loads((directory/"certificate.json").read_text())
    final=json.loads((directory/"strengthened.json").read_text())
    assert source["contact_count"]==12 and source["scale_exponent"]==1
    assert source["square_class_exponents"]==[0,0]
    assert len(SHIFTS)==len(set(SHIFTS))==12 and sum(SHIFTS)==0
    assert all(a+b for a in SHIFTS for b in SHIFTS)
    c=check.Circuit()
    nodes=source["coefficient_dag"]
    for i,row in enumerate(nodes):
        assert c.node(*row)==i
    def rat(x):return check.Rational(c,x["numerator"],x["denominator"])
    def leaf(i):return check.Rational(c,i,c.one)
    def equal(a,b):assert (a.n,a.d)==(b.n,b.d),((a.n,a.d),(b.n,b.d))
    event=lambda name:next(e for e in source["events"] if e["operation"]==name)
    height=event("moving_contact_height")
    x=leaf(c.node("variable",0))
    shift=leaf(c.node("parameter","fixed_input_shift",source["fixed_parameters"]["fixed_input_shift"]))
    beta=x*x+shift
    points=[e for e in source["events"] if e["operation"]=="point_block"]
    root=next(e for e in points if e["name"]=="A")
    trace=2*rat(root["x"][0])
    M=beta**4+trace**4
    z=leaf(c.node("variable",7))
    aa=M
    zz=z*z
    G,H=c.rational(1),c.rational(0)
    for constant in SHIFTS:
        factor=(aa+constant)**2-zz
        H,G=H*factor+G*(aa+constant),G*factor
    u=-12*G/H
    w=u/(1+u)**2
    for value,key in [(beta,"beta"),(trace,"trace"),(M,"M"),(M,"A"),(zz,"Z"),(aa**2-zz,"t"),(G,"G"),(H,"H"),(2*H,"G_A"),(u,"u"),(w,"w")]:
        equal(value,rat(height[key]))
    assert height["shifts"]==SHIFTS
    assert rat(height["t"]).n in source["deleted_signed_argument_guard"]
    assert rat(height["t"]).n not in source["guard_numerators"]
    original=check.ancestor("abc11")
    old_sig=check.signatures(original["coefficient_dag"])
    new_sig=check.signatures(nodes)
    def normalize(v,sig):
        if isinstance(v,list):return [normalize(t,sig) for t in v]
        if isinstance(v,dict):
            if set(v)=={"numerator","denominator"}:return [sig[v["numerator"]],sig[v["denominator"]]]
            return {k:normalize(t,sig) for k,t in v.items()}
        return v
    assert normalize(points,new_sig)==normalize([e for e in original["events"] if e["operation"]=="point_block"],old_sig)
    old_detector=next(e for e in original["events"] if e["operation"]=="balanced_actual_detector")
    detector=event("balanced_actual_detector")
    assert normalize(detector["original_tests"],new_sig)==normalize(old_detector["original_tests"],old_sig)
    eta=rat(detector["eta"])
    v=leaf(c.node("variable",8))
    s=leaf(c.node("variable",9))
    d=7*u
    radical=(1-eta)*(v**4-d**2)*(s**4-d**2)
    equal(eta,rat(event("intrinsic_pole")["input"]))
    # Check the square-class identity without calling the new producer.
    multiplier=rat(detector["product_norm"])/((1+u)*rat(detector["product_components"][0]))
    equal(eta,d*multiplier**2)
    equal(radical,rat(event("intrinsic_pole")["radicand"]))
    pole=[b for b in source["finite_blocks"] if b["kind"]=="pole"]
    assert len(pole)==1
    equal(radical,rat(pole[0]["original_square_input"]))
    # Existing independent replay checks every positive/balanced field factor,
    # all denominators, all square extraction, and all operator majorants.
    check.ancestor=lambda _:source
    replay=check.audit("abc11")

    @cache
    def atoms(i):
        op,*a=nodes[i]
        if op=="int":
            assert a[0]
            return set()
        if op in ("neg","pow"):return atoms(a[0]) if op=="neg" or a[1] else set()
        if op=="mul":return set().union(*(atoms(j) for j in a))
        return {i}
    automatic=(atoms(M.n)|atoms((1+u).n))&set(ordinary["norm_guard_nodes"])
    assert automatic==set(final["automatic_height_atoms"])
    point_atoms=set()
    blocks={b["name"]:b for b in source["finite_blocks"] if b["kind"]=="point_block"}
    for point in points:
        h0,h1=map(rat,point["h"])
        norm=h0*h0-2*h1*h1
        assert norm.d==c.one
        point_atoms |= atoms(norm.n)
        if point.get("chart")!="full_auxiliary":
            point_atoms.add(blocks[point["name"]]["variable_nodes"][2])
    assert len(point_atoms)==4 and point_atoms==set(final["automatic_point_atoms"])
    removed=automatic|point_atoms
    kept=set(ordinary["norm_guard_nodes"])-removed
    assert kept==set(final["norm_guard_nodes"])
    factors={r["node"]:r for r in parent["subalgebra_norm_factors"]}
    guard_degree=sum(factors[i]["scalar_norm_degree_bound"] for i in kept)
    saved=sum(factors[i]["scalar_norm_log2_l1_bound"] for i in removed)
    assert sum(factors[i]["scalar_norm_degree_bound"] for i in point_atoms)==14
    assert final["guard_degree"]==guard_degree
    assert final["separator_degree"]==ordinary["separator_degree"]
    assert source["total_external_variables"]==11 and source["retained_base_count"]==10
    assert final["rank"]==ordinary["rank"]==128
    assert final["extra_witness_degree"]==2*max(1+guard_degree,128*(1+final["separator_degree"]))+1
    assert final["degree"]==1+128*(1+guard_degree+final["separator_degree"])
    assert final["log2_l1"]==ordinary["log2_l1"]-128*saved
    degree=final["degree"]-1
    assert final["support_power"]==(math.comb(degree+11,11)-math.comb(degree-128+10,11)).bit_length()
    assert final["height_double_power"]==final["log2_l1"].bit_length()

    a,t,V,S,D,X=sp.symbols("a t V S D X")
    native=(1-a*t*t)*((t*V)**4-(a*t*t)**2)*((t*S)**4-(a*t*t)**2)
    reduced=(1-a*t*t)*(V**4-a**2)*(S**4-a**2)
    assert sp.expand(native-t**8*reduced)==0
    doubling=(X*X+D)**2/(4*X*(X*X-D))
    assert sp.cancel(4*doubling-X-D*(3*X*X+D)/(X*(X*X-D)))==0
    # Norm calculations at the fixed point prove v_pi(t(P))=3.
    norm_x=F(57**2-2*28**2,8**2)
    norm_y=F(660**2-2*417**2,32**2)
    def val2(q):
        def v(n):
            r=0
            while n%2==0:r+=1;n//=2
            return r
        return v(q.numerator)-v(q.denominator)
    assert val2(norm_x)==-6 and val2(norm_y)==-9
    assert val2(norm_x/norm_y)==3
    assert 2*F(57,8)==F(57,4)
    alpha=F(997,1001)
    lam=F(39,40)
    assert lam*alpha-F(1,2)==F(18863,40040)>0
    certificate={
        "status":"PASS","new_producer_imported":False,"pinned_source_interfaces_imported":True,"variables":11,"rank":128,
        "degree":final["degree"],"guard_degree":guard_degree,
        "separator_degree":final["separator_degree"],"support_power":final["support_power"],
        "log2_l1_fixture_B3":final["log2_l1"],"shifts":SHIFTS,
        "automatic_point_atoms":sorted(point_atoms),
        "independent_circuit_replay":list(replay),
        "bb_product_square_factor_identity":True,"terminal_zero_roots_allowed":True,"duplication_identity":True,
        "v_pi_parameter_P":3,"height_margin":"18863/40040",
        "sufficient_shift_effective":False,"scope":"Exact algebra and constants; the all-n trace and completeness statements are proved in the paper."
    }
    certificate["source_sha256"]=ordinary["source_sha256"]
    return certificate


def run_general(route):
    sys.argv=["check_positive.py","--repo",str(REPO),"--output",str(WORK/"bb_general")]
    check=load("four_contact_independent_"+route,ARCHIVE/"fewvars/check_positive.py")
    directory=WORK/"bb_general"/route
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
    denominator=B+7*T*A
    rho=7*102**2*p(L)*T*raw/denominator**2
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
    # Independently reconstruct each BB product pole and its square-class map.
    poles=[e for e in source["events"] if e["operation"]=="bb_product_pole"]
    blocks=[b for b in source["finite_blocks"] if b["kind"]=="pole"]
    assert len(poles)==len(detectors)==(2 if route=="general25" else 3)
    structural=[v for v in source["variables"] if v["category"]=="retained.pole"]
    for j,(pole,block,detector) in enumerate(zip(poles,blocks,detectors,strict=True)):
        e=r(detector["pole_input"])
        eq(e,r(pole["input"]))
        d,t=r(pole["square_class"]),r(pole["square_multiplier"])
        eq(d*t**2,e)
        v=leaf(c.node("variable",structural[2*j]["index"]))
        s=leaf(c.node("variable",structural[2*j+1]["index"]))
        eq(v,r(pole["first_parameter"]))
        eq(s,r(pole["second_parameter"]))
        radical=(1-e)*(v**4-d**2)*(s**4-d**2)
        eq(radical,r(pole["radicand"]))
        eq(radical,r(block["original_square_input"]))
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
    assert reduced["separator_degree"]==ordinary["separator_degree"]
    assert reduced["rank"]==n
    assert source["total_external_variables"]==(25 if route=="general25" else 27)
    assert source["retained_base_count"]==source["total_external_variables"]-1
    assert n==(1048576 if route=="general25" else 2097152)
    assert reduced["extra_witness_degree"]==2*max(1+g,n*(1+reduced["separator_degree"]))
    assert reduced["degree"]==n*(1+g+ordinary["separator_degree"])
    assert reduced["log2_l1"]==ordinary["log2_l1"]-n*saved
    if route=="general25":
        projective=json.loads((directory/"projective.json").read_text())
        assert set(projective["automatic_point_atoms"])==point_atoms
        assert projective["guard_degree"]==g and projective["rank"]==n
        assert set(projective["early_positive_atoms"])==automatic
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
    return {"route":route,"degree":d,"source_sha256":ordinary["source_sha256"],"pole_count":len(poles),"terminal_zero_roots_allowed":True,"variables":v,"rank":n,"guard_degree":g,
            "early_positive_atoms":sorted(automatic),"independent_replay":list(replay),
            "automatic_point_atoms":sorted(point_atoms),
            "log2_l1":final["log2_l1"],"support_power":final["support_power"]}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root",type=Path,required=True)
    parser.add_argument("--report",type=Path,required=True)
    args=parser.parse_args()
    WORK=args.work_root.resolve()
    REPO=WORK/"diophantine"
    ARCHIVE=WORK/"audit_20261119/H10-quartics"
    report=args.report.resolve()
    abc=run_abc()
    general=[run_general(route) for route in ("general25","explicit27")]
    assert [abc["degree"],*(r["degree"] for r in general)]==[3261569,48318382080,183368679424]
    result={"status":"PASS","new_producer_imported":False,
        "pinned_source_interfaces_imported":True,
        "checks":["all modified rational circuits", "unchanged point charts and tests",
                  "every BB product pole", "each input square-class identity",
                  "every independent operator and norm majorant",
                  "denominator coverage and terminal zero-root relaxation",
                  "positive guard removal", "final determinants, degree, support, and height bounds"],
        "routes":[abc,*general]}
    report.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
