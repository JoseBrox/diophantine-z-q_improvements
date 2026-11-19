"""Independent exact circuit and identity checks for the twelve-contact source."""
from pathlib import Path
from fractions import Fraction as F
from functools import cache
import importlib.util
import json
import math
import sys
import sympy as sp

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]/"diophantine"
ARCHIVE=HERE.parent/"H10-quartics"
SHIFTS=[-9,-8,-7,-5,-4,-3,-2,-1,6,10,11,12]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def main():
    sys.argv=["check_positive.py","--balanced","--repo",str(REPO),"--output",str(HERE/"twelve")]
    check=load("twelve_independent_positive",ARCHIVE/"fewvars/check_positive.py")
    directory=HERE/"twelve/abc11"
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
    radical=d*(d+v*v)**2*s**4-d*(d-v*v)**2*(1-eta)**2
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
    assert final["degree"]==1+128*(1+guard_degree+final["separator_degree"])
    assert final["log2_l1"]==ordinary["log2_l1"]-128*saved
    degree=final["degree"]-1
    assert final["support_power"]==(math.comb(degree+11,11)-math.comb(degree-128+10,11)).bit_length()
    assert final["height_double_power"]==final["log2_l1"].bit_length()

    a,t,V,S,D,X=sp.symbols("a t V S D X")
    native=lambda e,v: e*(e+v**2)**2*S**4-e*(e-v**2)**2*(1-e)**2
    reduced=a*(a+V**2)**2*S**4-a*(a-V**2)**2*(1-a*t*t)**2
    assert sp.expand(native(a*t*t,t*V)-t**6*reduced)==0
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
        "intrinsic_square_factor_identity":True,"duplication_identity":True,
        "v_pi_parameter_P":3,"height_margin":"18863/40040",
        "sufficient_shift_effective":False,"scope":"Exact algebra and constants; the all-n trace and completeness statements are proved in the paper."
    }
    (HERE/"twelve_independent_certificate.json").write_text(json.dumps(certificate,indent=2)+"\n")
    print(json.dumps(certificate,indent=2))


if __name__=="__main__":main()
