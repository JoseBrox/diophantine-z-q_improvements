"""Audit single-pole certificates from source nodes and upstream chart/test data."""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
import tempfile
from fractions import Fraction
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument("--repo",type=Path,default=HERE.parents[1]/"source")
parser.add_argument("directories",nargs="*",type=Path,default=[HERE/name for name in ("specification","strong","simple","simple_strong","eight","eight_strong")])
args=parser.parse_args()
BASE=args.repo.resolve()/"computation/few_variables"
sys.path.insert(0,str(BASE/"unit_norm_v28"))
from build_sources import make_source
from field_circuit import Circuit,Rational


def load(name,path):
    modspec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(modspec)
    modspec.loader.exec_module(mod)
    return mod


def canonical(x):
    return (json.dumps(x,sort_keys=True,separators=(",",":"))+"\n").encode()


def signature(source):
    values=[]
    for op,*a in source["coefficient_dag"]:
        if op in ("add","mul"):label=[op,*sorted(values[j] for j in a)]
        elif op in ("neg","pow"):label=[op,values[a[0]],*a[1:]]
        elif op=="variable":label=[op,source["variables"][a[0]]["name"]]
        else:label=[op,*a]
        values.append(hashlib.sha256(canonical(label)).digest().hex())
    return values


def replay(source,upstream):
    c=Circuit()
    for i,row in enumerate(source["coefficient_dag"]):assert c.node(*row)==i
    def rat(r):return Rational(c,r["numerator"],r["denominator"])
    def field(a):return tuple(map(rat,a))
    def one():return c.rational(1),c.rational(0)
    def kmul(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
    def scale(a,k):return a[0]*k,a[1]*k
    def kplus1(a):return 1+a[0],a[1]
    def norm(a):return a[0]**2-2*a[1]**2
    def same(a,b):assert (a.n,a.d)==(b.n,b.d),((a.n,a.d),(b.n,b.d))
    def fp(a,b):
        for t,u in zip(a,b,strict=True):same(t,u)
    def ev(source,label):return [e for e in source["events"] if e["operation"]==label]
    def sig(r,labels):return labels[r["numerator"]],labels[r["denominator"]]
    oldtests=ev(upstream,"conditional_direct_target_tests")[0]["tests"]
    tests=ev(source,"test")
    oldlabels=signature(upstream);newlabels=signature(source)
    for old,test in zip(oldtests,tests,strict=True):
        assert [sig(r,oldlabels) for r in old]==[sig(r,newlabels) for r in test["C"]]
    (m,)=ev(source,"moving_contacts")
    vars={source["variables"][j]["name"]:Rational(c,i,1) for i,(op,*a) in enumerate(source["coefficient_dag"]) if op=="variable" for j in [a[0]]}
    B=source["family_parameter"]["value"]
    beta=vars["input.X"]**2+c.parameter("fixed_input_shift",B)
    h0,h1=vars["A.a0"],vars["A.a1"]
    T=2*(h0*h0+2*h1*h1)
    a=beta**m["scale_power"]+T**m["scale_power"]
    same(rat(m["beta"]),beta);same(rat(m["T"]),T);same(rat(m["M"]),a);same(rat(m["a"]),a)
    x=a-vars["contact.z"];y=a+vars["contact.z"]
    same(rat(m["x"]),x);same(rat(m["y"]),y)
    theta=list(map(Fraction,["0","-1","-1/2","-1/3","-1/4","-2/5"]))
    if source["name"].endswith("_eight"):
        import sympy as sp
        Z=sp.Symbol("Z")
        B6=(Z+4)*(Z+20)**3*(Z-5)**2
        C6=(Z-4)*(Z-20)**3*(Z+5)**2
        assert sp.expand(B6-C6)==108*Z**5 and sp.gcd(B6,C6)==1
        cusps=[0,4,-4,5,-5,20,-20]
        theta=[Fraction(0),*(1/Fraction(k-21) for k in cusps)]
    assert set(map(Fraction,m["theta"]))==set(theta)
    theta=list(map(Fraction,m["theta"]))
    def form(t):return math.prod((t-k for k in theta),start=c.rational(1))
    p,q=form(x),form(y);same(p,rat(m["p"]));same(q,rat(m["q"]))
    k=m["band"]
    u=((x-1)*(y-1))**(6*k)*(p*q)**3/((p**3+q**5)*(p+q**k)*(p**k+q))
    simple="_simple" in source["name"]
    if simple:
        u=((x-1)*(y-1))**(len(theta)*(k-1))*p*q*(p**2+q**3)**2/((p**3+q**5)*(p+q**k)*(p**k+q))
    w=u/(1+u)**2
    same(rat(m["u"]),u);same(rat(m["w"]),w)
    W=one();nW=c.rational(1)
    def plus(a,b):return a[0]+b[0],a[1]+b[1]
    def minus(a,b):return a[0]-b[0],a[1]-b[1]
    def conj(a):return a[0],-a[1]
    coords={}
    for a0,a1 in zip(ev(source,"point_block"),ev(upstream,"point_block"),strict=True):
        for key in ["h","x","j","y"]:
            assert [sig(r,newlabels) for r in a0[key]]==[sig(r,oldlabels) for r in a1[key]]
        coords[a0["name"]]=field(a0["x"]),field(a0["y"])
    Kpoint=lambda *a:tuple(map(c.rational,map(Fraction,a)))
    coords["F"]=Kpoint("57/8","-7/2"),Kpoint("-165/8","417/32")
    def diff_parts(a,b):
        x,y=coords[a];xx,yy=coords[b];delta=minus(x,xx)
        X=plus(kmul(plus(x,xx),minus(kmul(x,xx),Kpoint(11,-6))),scale(kmul(y,yy),2))
        return conj(X),conj(kmul(delta,delta))
    for i,test in enumerate(tests):
        C=field(test["C"]);C2=kmul(C,C);C4=kmul(C2,C2)
        num=C4;den=kplus1(scale(C4,u**2))
        if simple:
            if i<4:
                if i<2:L,num=coords[("H","UA")[i]][0],one()
                else:L,num=diff_parts(*(("H","F"),("UA","A"))[i-2])
                den=plus(L,scale(num,u))
            else:num=C2;den=kplus1(scale(num,u))
        fp(den,field(test["den"]))
        dn=norm(den);same(dn,rat(test["den_norm"]))
        t=kmul(num,(den[0]/dn,-den[1]/dn));fp(t,field(test["t"]))
        s=scale(kmul(t,t),1/u**2);fp(s,field(test["summand"]))
        g=kplus1(s);W=kmul(W,g);nW*=norm(g)
    (d,)=ev(source,"detector");(pole,)=ev(source,"rescaled_zero_pole")
    fp(W,field(d["W"]));same(nW,rat(d["norm"]))
    b=w*nW**2/W[0]**2;same(b,rat(d["b"]));same(b,rat(pole["input"]))
    d0=rat(pole["square_class"]);tau=vars["pole.tau"];s=vars["pole.s"]
    e=(tau*tau-17*d0)/(tau*tau+51*d0);same(e,rat(pole["e"]))
    v=17*e*(17-b)
    rad=17*d0*(s*s-v)*(s*s+3*v)
    same(rad,rat(pole["radicand"]));same(rad,rat(source["finite_blocks"][-1]["original_square_input"]))
    return m,tests,d


def local(k,e,kappa,d,simple):
    assert k>=2 and d in (6,8) and e%2==0
    for m,n in product(range(k),repeat=2):
        if 1 not in (m,n):continue
        groups=[(3*m,5*n),(m,k*n),(k*m,n)]
        assert all(a!=b for a,b in groups)
        base=3*(m+n)-sum(min(pair) for pair in groups)
        if simple:
            assert 2*m!=3*n
            base=m+n+2*min(2*m,3*n)-sum(min(pair) for pair in groups)
            assert base==1
        assert base>0 and base%2
    # In a mixed case write s=-j, j>=1. Distinct affine valuations for all j.
    for f,expected in [(lambda s:(1,6*s),lambda s:3-18*s),(lambda s:(6*s,1),lambda s:3-6*s)]:
        for s in [-1,-2,-10003]:
            m,n=f(s);pairs=[(3*m,5*n),(m,k*n),(k*m,n)]
            assert all(a!=b for a,b in pairs)
            assert 6*k*s+3*(m+n)-sum(min(pair) for pair in pairs)==expected(s)
    if simple:
        for s in [-1,-2,-451]:
            for m,n in [(1,d*s),(d*s,1)]:
                val=d*(k-1)*s+m+n+2*min(2*m,3*n)-sum([min(3*m,5*n),min(m,k*n),min(k*m,n)])
                assert val==1
        assert 2*d*(k-1)+2*d+6*d-(5*d+2*d*k)==d
    else:assert 12*k+36-(30+12*k)==6 and d==6
    gamma=2*(d-2)/kappa-d;alpha=e/kappa-3;rate=(gamma-Fraction(d,k))*alpha/2
    assert rate>Fraction(1,2)
    return rate


def audit(directory,compact_name):
    def read(name):return json.loads((directory/(name+".json")).read_text())
    source=read("native");parent=read("polynomial");out=read(compact_name)
    assert out["native_source_sha256"]==parent["native_source_sha256"]==hashlib.sha256(canonical(source)).hexdigest()
    check=load("independent_v30",BASE/"subalgebra_norms_v30/check.py")
    v28=load("extra_v28",BASE/"unit_norm_v28/build.py")
    with tempfile.TemporaryDirectory() as tmp:
        check.OLD=Path(tmp)
        ref=check.OLD/"specifications"/(source["name"]+".json")
        ref.parent.mkdir()
        ref.write_bytes(canonical(v28.compile_specification(source)))
        summary=check.verify_spec(source,parent)
    m,tests,d=replay(source,make_source("weak13",source["family_parameter"]["value"]))
    kappa=Fraction(16,15) if source["name"].startswith("strong") else Fraction(121,100)
    rate=local(m["band"],m["scale_power"],kappa,len(m["theta"]),"_simple" in source["name"])
    assert source["total_external_variables"]==out["variables"]==11
    assert len(source["variables"][:source["retained_base_count"]])==10
    assert [b["degree"] for b in source["finite_blocks"]]==[4,4,4,2]
    ds,logs,_,fac,_=check.arrays(source)
    nodes=source["coefficient_dag"]
    def ff(i):return {v for v in fac[i] if v>=0 and nodes[v][0]!="int"}
    root=source["finite_blocks"][-1]["generator_node"]
    assert root==out["suppressed_pole_node"]
    native=set().union(*(ff(r["node"]) for r in parent["guard_factorizations"] if r["node"]!=root))
    assert root not in native
    early=ff(m["u"]["numerator"])|ff(m["u"]["denominator"])
    intermediate=set();pos1=set()
    for t in tests:
        early.update(*(ff(v["denominator"]) for v in [*t["C"],*t["den"],t["den_norm"]]))
        pos1.update(ff(t["den_norm"]["numerator"]))
        intermediate.update(*(ff(v["denominator"]) for v in [*t["t"],*t["summand"]]))
    intermediate.update(*(ff(v["denominator"]) for v in [*d["W"],d["norm"]]))
    pos2=ff(d["W"][0]["numerator"])|ff(d["norm"]["numerator"])
    r1=set(out["positive_balancing_atoms"]);r2=set(out["positive_product_atoms"]);kept=set(out["retained_norm_atoms"])
    assert r1==(set() if compact_name=="conservative" else (pos1&native)-early) and r2==(pos2&native)-early-intermediate-r1
    assert kept==native-r1-r2 and early<=kept and intermediate<=kept|r1
    def denominators(obj):
        if isinstance(obj,list):
            for value in obj:yield from denominators(value)
        if isinstance(obj,dict):
            if set(("numerator","denominator"))<=set(obj):yield obj["denominator"]
            for value in obj.values():yield from denominators(value)
    for denominator in denominators([source["events"],source["finite_blocks"]]):
        assert ff(denominator)<=kept|r1|r2
    # All chart guards from before the first new weight are retained; the full
    # DAG replay above already fixes their original point coordinates and tests.
    for event in source["events"]:
        if event["operation"]=="test":break
        for denominator in denominators(event):
            assert ff(denominator)<=kept
    rows=[r for r in parent["subalgebra_norm_factors"] if r["node"] in kept]
    g=sum(r["subalgebra_rank"]*ds[r["node"]] for r in rows)
    gl=sum(r["subalgebra_rank"]*logs[r["node"]] for r in rows)
    tower=parent["quadratic_tower"]
    weights=[r["root_weight"] for r in tower];env=[r["envelope_degree"] for r in tower]
    wd=max(sum(weights),max(sum(weights[:i+1])+sum(env[i+1:]) for i in range(len(tower)-1)))
    assert (g,wd)==(out["guard_degree"],out["separator_degree"])
    h=tower[-1]["root_operator_log2_norm"]
    for i in reversed(range(len(tower)-1)):
        tail=sum(2+r["envelope_log2_l1"] for r in tower[i+1:])
        h=tower[i]["root_operator_log2_norm"]+1+max(h,tail)
    N=math.prod(p["degree"] for p in source["finite_blocks"]);assert N==out["rank"]
    D=N*(1+g+wd);nr=math.comb(D+11,11)-math.comb(D-N+10,11)
    assert D+1==out["degree_bound"] and nr.bit_length()==out["support_power"]
    l1=N*(1+gl+h);assert l1==out["coefficient_log2_l1"] and l1.bit_length()==out["coefficient_double_power"]
    print(f"{source['name']} {compact_name}: degree {D+1}, {len(tests)} original tests, rate {rate}, "
          f"{summary['rational_denominators']} denominators, {len(kept)} retained atoms, support <2^{nr.bit_length()}")

for path in args.directories:
    audit(path.resolve(),"compact")
    if (path/"conservative.json").exists():audit(path.resolve(),"conservative")
