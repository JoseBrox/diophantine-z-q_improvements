"""Exact bounds for the optional rank-zero two-pole encoder."""
import argparse
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument("--source",type=Path,default=HERE/"positive_factors")
args=parser.parse_args()


def bounds(route):
    directory=args.source/route
    cert=json.loads((directory/"certificate.json").read_bytes())
    spec=json.loads((directory/"parent.json").read_bytes())
    gs=set(cert["norm_guard_nodes"])
    glog=sum(x["scalar_norm_log2_l1_bound"] for x in spec["subalgebra_norm_factors"] if x["node"] in gs)
    g=cert["guard_degree"];n=cert["rank"]
    points=[x for x in spec["quadratic_tower"] if x["kind"]!="pole"]
    a,b=[x for x in spec["quadratic_tower"] if x["kind"]=="pole"]
    w1,w2=a["root_weight"],b["root_weight"]
    e1,e2=a["envelope_degree"],b["envelope_degree"]
    l1,l2=a["root_operator_log2_norm"],b["root_operator_log2_norm"]
    h1,h2=a["envelope_log2_l1"]+1,b["envelope_log2_l1"]+1
    wplus=max(w2,e2);lplus=1+max(l2,h2)
    degN=max(3*w1+wplus,3*e1+w2);degD=3*e1+wplus
    logN=1+max(3*l1+lplus,3*h1+l2);logD=3+3*h1+lplus
    # Expanded formula furnishes an independent check on recursive degrees.
    w=[p["root_weight"] for p in points];e=[p["envelope_degree"] for p in points]
    expanded=max([sum(w)+degN]+[sum(w[:i+1])+degD+sum(e[i+1:]) for i in range(len(points))])
    for p in reversed(points):
        degN=p["root_weight"]+max(degN,degD);degD+=p["envelope_degree"]
        logN=p["root_operator_log2_norm"]+1+max(logN,logD)
        logD+=2+p["envelope_log2_l1"]
    assert degN==expanded
    before=n*max(degD,1+g+degN)
    logheight=n*(1+max(logD,glog+logN))
    v=len(spec["external_variables"])
    monomials=math.comb(before+v,v)-math.comb(before-n+v-1,v)
    return dict(route=route,rank=n,guard_degree=g,numerator_degree=degN,denominator_degree=degD,
                degree=before+int(spec["multiply_by_input"]),log2_l1=logheight,
                height_double_power=logheight.bit_length(),support_power=monomials.bit_length())


if __name__=="__main__":
    # Symbolically verify the elementary reduction to Fermat's exponent three.
    import sympy as sp
    X,Y=sp.symbols("X Y")
    P=(X**3+64)/X**2;Q=Y*(X**3-128)/X**3
    identity=sp.together(Q**2-P**3+432).as_numer_denom()[0]
    assert sp.rem(identity,Y**2-X**3-16,Y)==0
    assert all(i**3-12*i**2+64 for j in [1,2,4,8,16,32,64] for i in [-j,j])
    rows=[bounds(r) for r in ("general25","weak13","abc13")]
    (HERE/"projective_bounds.json").write_text(json.dumps(rows,indent=2)+"\n")
    print("route,degree,coefficient height double power,support power,numerator degree,denominator degree")
    for r in rows:print(*(r[k] for k in ("route","degree","height_double_power","support_power","numerator_degree","denominator_degree")),sep=",")
