"""Independent verifier of the termwise-positive determinant sources and bounds.

Load the pinned circuit arithmetic only, with no calls to positive.py or its
arithmetic builder. Replay every detector using exact integer circuit nodes.
"""
import argparse
from collections import Counter
import importlib.util
import inspect
from functools import cache
import hashlib
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument("--repo",type=Path,default=HERE.parent/"source")
parser.add_argument("--output",type=Path)
parser.add_argument("--balanced",action="store_true")
args=parser.parse_args()
if args.output is None:args.output=HERE/("balanced" if args.balanced else "positive_factors")
BASE=args.repo/"computation/few_variables"
sys.path.insert(0,str(BASE/"trace27_nontorsion"))
sys.path.insert(0,str(BASE/"unit_norm_v28"))
from field_circuit import Circuit,Rational
from build_sources import make_source


def ancestor(route):
    folder={"general25":"even_valuation25_v75/specification","abc11":"even_valuation11_v75/specification","abc11seven":"even_valuation11_v75/seven_contact"}.get(route)
    return json.loads((BASE/folder/"source.json").read_bytes()) if folder else make_source(route)


def canon(obj):
    return (json.dumps(obj,sort_keys=True,separators=(",",":"))+"\n").encode()


def signatures(nodes):
    # Circuit node numbering changes across the two graphs after the first
    # detector. Reconcile labels recursively, sorting commutative arguments.
    result=[]
    for op,*ys in nodes:
        if op in ("mul","add"):data=[op,*sorted(result[i] for i in ys)]
        elif op in ("neg","pow"):data=[op,result[ys[0]],*ys[1:]]
        else:data=[op,*ys]
        result.append(hashlib.sha256(canon(data)).hexdigest())
    return result


def witness_events(source):
    return [e for e in source["events"] if e["operation"] in ("detector","combined_detector","balanced_actual_detector")]


def replay(route,source,old):
    nodes=source["coefficient_dag"]
    c=Circuit()
    for i,row in enumerate(nodes):
        assert c.node(*row)==i
    def rat(r):return Rational(c,r["numerator"],r["denominator"])
    def field(pair):return tuple(map(rat,pair))
    def sig(x):return (x.n,x.d)
    def same(x,y):assert sig(x)==sig(y),(sig(x),sig(y))
    def kmul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def scale(a,w):return (a[0]*w,a[1]*w)
    def compare(a,b):
        for x,y in zip(a,b):same(x,y)
    event=lambda name:next(e for e in source["events"] if e["operation"]==name)
    assert source["variables"]==old["variables"]
    # Equality of every test, weight and normalizer with the baseline native graph.
    new_signatures=signatures(nodes)
    old_signatures=signatures(old["coefficient_dag"])
    def normalize(obj,sigs):
        if isinstance(obj,list):return [normalize(y,sigs) for y in obj]
        if isinstance(obj,dict):
            if set(obj)=={"numerator","denominator"}:return [sigs[obj["numerator"]],sigs[obj["denominator"]]]
            return {k:normalize(v,sigs) for k,v in obj.items()}
        return obj
    for before,after in zip(witness_events(old),witness_events(source)):
        skip={"product_components","pole_input","product_norm","trace","b","eta"}
        if args.balanced:skip.add("transformed_tests")
        for key in (set(before)&set(after))-skip:
            assert normalize(before[key],old_signatures)==normalize(after[key],new_signatures),(route,key)
    for nm in ("comparison_and_scalar_tests","conditional_direct_target_tests","moving_contact_height"):
        bef=[e for e in old["events"] if e["operation"]==nm];aft=[e for e in source["events"] if e["operation"]==nm]
        assert normalize(bef,old_signatures)==normalize(aft,new_signatures)
    raw=[];results=[]
    for e in source["events"]:
        if e["operation"]=="positive_factor_argument":raw.append(field(e["raw"]))
        if e["operation"]!="positive_detector_product":continue
        w=(c.rational(1),c.rational(0));expected_norm=c.rational(1)
        for a in raw:
            u,v=kmul(a,a);factor=(1+u,v)
            w=kmul(w,factor)
            expected_norm*=factor[0]**2-2*factor[1]**2
        compare(w,field(e["W"]));same(expected_norm,rat(e["norm"]))
        results.append((raw,w,expected_norm));raw=[]
    assert not raw
    for e,(supplied,w,norm) in zip(witness_events(source),results,strict=True):
        if e["operation"]=="combined_detector":
            tests=event("comparison_and_scalar_tests")["comparison"]
            raw=[]
            for i,(v,wt) in enumerate(zip(tests,e["comparison_weights"],strict=True)):
                z=field(v)
                if route!="general25" or i>=10:z=kmul(z,z)
                raw.append(scale(z,rat(wt)))
            for v,wt in zip(e["normalized_scalar"],e["scalar_weights"],strict=True):
                z=field(v);raw.append(scale(kmul(z,z),rat(wt)))
            same(rat(e["pole_input"]),rat(e["combined_coefficient"])*norm**2/w[0]**2)
        elif e["operation"]=="detector":
            wt=rat(e["weights"]["1"])
            raw=[scale(kmul(z,z),wt) for z in map(field,event("conditional_direct_target_tests")["tests"])]
            same(rat(e["pole_input"]),rat(e["F"])*norm*norm/(4*rat(e["delta"])**8*w[0]*w[0]))
        else:
            wt=1/rat(event("moving_contact_height")["u"])
            transformed=list(map(field,e["transformed_tests"]))
            if args.balanced:
                par=[ev for ev in source["events"] if ev["operation"]=="sum_square_balance"]
                assert len(par)==len(transformed)==6
                def kdiv(a,b):
                    n=b[0]**2-2*b[1]**2
                    return kmul(a,(b[0]/n,-b[1]/n))
                for i,(ev,z,original) in enumerate(zip(par,transformed,e["original_tests"],strict=True)):
                    L,R=field(ev["L"]),field(ev["R"]);C=field(original);u=rat(ev["u"])
                    same(rat(ev["nonzero"]),L[0]**2-2*L[1]**2)
                    kk=kdiv(R,L)
                    if i in (2,3):kk=kk[0],-kk[1]
                    compare(kk,C if i<4 else kmul(C,C))
                    num=kmul(R,R);a=kmul(L,L);b=scale(num,u**2)
                    den=a[0]+b[0],a[1]+b[1]
                    compare(den,field(ev["denominator_components"]));compare(num,field(ev["numerator_components"]))
                    same(rat(ev["norm"]),den[0]**2-2*den[1]**2)
                    x=kdiv(num,den)
                    if i in (2,3):x=x[0],-x[1]
                    compare(x,z)
                raw=[scale(z,wt) for z in transformed]
            else:
                raw=[scale(kmul(z,z),wt) for z in transformed]
            same(rat(e["b"]),rat(event("moving_contact_height")["w"])*norm**2/w[0]**2)
            same(rat(e["eta"]),7*rat(e["b"]))
        for x,y in zip(raw,supplied,strict=True):compare(x,y)
        compare(w,field(e["product_components"]))
    return sum(len(raw) for raw,_,_ in results)


def denominator_nodes(value):
    if isinstance(value,list):
        for child in value:yield from denominator_nodes(child)
    elif isinstance(value,dict):
        if "numerator" in value and "denominator" in value:yield value["denominator"]
        for child in value.values():yield from denominator_nodes(child)


def upstream_majorants(route,source,spec):
    """Audit elementary operator bounds with the upstream independent DAG verifier.

    The v75 charts use the separate v71/v72 integral-point weight table.
    """
    path=BASE/"subalgebra_norms_v30/check.py"
    loader=importlib.util.spec_from_file_location("independent_arithmetic_majorants",path)
    module=importlib.util.module_from_spec(loader);loader.loader.exec_module(module)
    full=route in ("general25","abc11","abc11seven")
    oldroots=("A","S","T","Z") if route=="general25" else ("A",)
    if full:
        text=inspect.getsource(module.arrays)
        needle="(2,2,4), (4,4,6), (x,x,x^y)"
        assert text.count(needle)==1
        repl=f"(2,2,4 if block['name'] in {oldroots!r} else 3), (4,4,7), (x,x,x^y)"
        exec(compile(text.replace(needle,repl),"upstream-v75-independent-bound-table","exec"),module.__dict__)
    ds,logs,aff,fact,points=module.arrays(source)
    for f in spec["guard_factorizations"]:
        assert module.normalized(f["sign"],f["factors"])==fact[f["node"]]
    for p in spec["subalgebra_norm_factors"]:
        i=p["node"];offset,directions=aff[i];basis=module.low_basis([offset,*directions])
        assert module.same_span(basis,p["subspace_basis"]) and len(basis)==p["subspace_dimension"]
        sw=lambda b:sum((((b>>(2*j))&1)<<(2*j+1))+(((b>>(2*j+1))&1)<<(2*j)) for j in range(len(points)))
        assert module.same_span(basis,[sw(b) for b in basis])
        assert p["subalgebra_rank"]==2**len(basis)
        assert (p["element_degree_bound"],p["element_operator_log2_norm_bound"])==(ds[i],logs[i])
        assert p["scalar_norm_degree_bound"]==ds[i]*2**len(basis) and p["scalar_norm_log2_l1_bound"]==logs[i]*2**len(basis)
    tower=[]
    for point in points:
        if not full:tower.extend([(8,11,4,6),(12,20,6,12)])
        elif point["name"] in oldroots:tower.extend([(8,11,4,7),(12,20,6,12)])
        else:tower.extend([(6,11,3,7),(9,20,5,12)])
    pole_blocks=[x for x in source["finite_blocks"] if x["kind"]=="pole"]
    for block,r in zip(pole_blocks,spec["quadratic_reductions"],strict=True):
        native=fact[block["coefficient_nodes_ascending"][0]].copy()
        native[-1]+=1;native=module.normalized(1,native.items())
        rec=Counter(r["odd_factor_nodes"])
        for i,e in r["square_multiplier_factors"]:rec[i]+=2*e
        assert module.normalized(r["sign"],rec.items())==native
        orig=block["original_square_input"]
        assert module.normalized(1,(fact[orig["numerator"]]+fact[orig["denominator"]]).items())==native
        d=sum(ds[i] for i in r["odd_factor_nodes"]);lg=sum(logs[i] for i in r["odd_factor_nodes"])
        tower.append((d,lg,(d+1)//2,(lg+1)//2+1))
    for record,(d,lg,w,h) in zip(spec["quadratic_tower"],tower,strict=True):
        assert (record["degree"],record["operator_log2_norm"],record["root_weight"],record["root_operator_log2_norm"])==(d,lg,w,h)
        k=(d+3)//4;g=(lg+1)//2
        assert (record["envelope_degree"],record["envelope_power"],record["envelope_constant_exponent"],record["envelope_log2_l1"])==(2*k,k,g,g+k*source["retained_base_count"].bit_length())


def audit(route):
    directory=args.output/route
    source=json.loads((directory/"native.json").read_bytes())
    spec=json.loads((directory/"parent.json").read_bytes())
    cert=json.loads((directory/"certificate.json").read_bytes())
    assert cert["source_sha256"]==spec["native_source_sha256"]==hashlib.sha256(canon(source)).hexdigest()
    upstream_majorants(route,source,spec)
    calls=replay(route,source,ancestor(route))
    nodes=source["coefficient_dag"];atom=[];deps=[]
    poles=[b for b in source["finite_blocks"] if b["kind"]=="pole"]
    roots={p["generator_node"] for p in poles}
    for i,(op,*ys) in enumerate(nodes):
        if op=="int":a=set() if ys[0] else {i}
        elif op=="neg":a=atom[ys[0]]
        elif op=="pow":a=atom[ys[0]] if ys[1] else set()
        elif op=="mul":a=set.union(*(atom[y] for y in ys))
        else:a={i}
        atom.append(a)
        if op in {"variable","parameter","int"}:deps.append({i} if i in roots else set())
        elif op in {"neg","pow"}:deps.append(deps[ys[0]])
        else:deps.append(set.union(*(deps[y] for y in ys)))
    remain=set(source["guard_numerators"])-roots
    assert all(not deps[i] for i in remain)
    base_atoms=set.union(*(atom[i] for i in remain))
    early=[];guaranteed=[]
    for e in source["events"]:
        if e["operation"]=="positive_factor_argument":
            early+=list(denominator_nodes(e["raw"]))
        if e["operation"]=="positive_detector_product":
            early+=list(denominator_nodes([e["W"],e["norm"]]))
            guaranteed += [e["W"][0]["numerator"],e["norm"]["numerator"]]
    witnesses=set.union(*(atom[i] for i in guaranteed))
    positive=set(cert["positive_trace_atoms"]);kept=set(cert["norm_guard_nodes"])
    assert positive==((witnesses&base_atoms)-set.union(*(atom[i] for i in early)))
    balance_atoms=set(cert.get("positive_balancing_atoms",[]))
    if args.balanced:
        records=[e for e in source["events"] if e["operation"]=="sum_square_balance"]
        protected=set()
        for e in records:
            protected.update(set.union(*(atom[i] for i in denominator_nodes([e["L"],e["R"],e["denominator_components"],e["norm"],e["u"],e["nonzero"]]))))
            protected.update(atom[e["u"]["numerator"]]|atom[e["nonzero"]["numerator"]])
        possible=set.union(*(atom[e["norm"]["numerator"]] for e in records))
        assert balance_atoms==(possible&base_atoms)-protected-positive
        assert protected<=kept
    assert kept==base_atoms-positive-balance_atoms and roots==set(cert["pole_ordinate_guards"])
    # Soundness after extraction requires a rational character. No automatic
    # factor needs a nonvanishing assertion on any other character.
    assert all(atom[i]<=kept|balance_atoms for i in early)
    denoms=list(denominator_nodes([source["events"],source["finite_blocks"]]))
    assert all(atom[i]<=kept|balance_atoms|positive for i in denoms)
    for red in spec["quadratic_reductions"]:
        assert all(not deps[i] for i in [red["native_constant_node"],*red["odd_factor_nodes"],*(i for i,_ in red["square_multiplier_factors"])])
    factors=[r for r in spec["subalgebra_norm_factors"] if r["node"] in kept]
    assert len(factors)==len(kept)
    g=sum(x["element_degree_bound"]*2**x["subspace_dimension"] for x in factors)
    gl=sum(x["element_operator_log2_norm_bound"]*2**x["subspace_dimension"] for x in factors)
    assert g==cert["guard_degree"]
    points=[x for x in spec["quadratic_tower"] if x["kind"]!="pole"]
    q=[x for x in spec["quadratic_tower"] if x["kind"]=="pole"]
    k=1 if len(q)==1 else 3;s=len(q)
    b=k*max(x["envelope_degree"] for x in q)
    tail=k*max(x["root_weight"] for x in q)
    weight=[x["root_weight"] for x in points];envelopes=[x["envelope_degree"] for x in points]
    w=max([sum(weight)+tail]+[sum(weight[:j+1])+b+sum(envelopes[j+1:]) for j in range(len(points))])
    n=2**(len(points)+len(q));v=len(spec["external_variables"]);d=n*(1+w+g);flag=int(source["multiply_by_input"])
    assert cert["rank"]==n and cert["separator_degree"]==w and cert["degree"]==d+flag
    monomials=math.comb(d+v,v)-math.comb(d-n+v-1,v)
    assert cert["support_power"]==monomials.bit_length()
    log_num=(s-1).bit_length()+max(j+k*x["root_operator_log2_norm"] for j,x in enumerate(q))
    log_den=2+s.bit_length()+max(j+k*x["envelope_log2_l1"] for j,x in enumerate(q))
    for x in reversed(points):
        log_num=x["root_operator_log2_norm"]+1+max(log_den,log_num)
        log_den+=2+x["envelope_log2_l1"]
    lc=n*(1+log_num+gl)
    assert lc==cert["log2_l1"] and lc.bit_length()==cert["height_double_power"]
    return route,calls,len(denoms),len(positive)+len(balance_atoms),len(kept),cert["degree"]


if __name__=="__main__":
    print("route,detector factors exactly replayed,denominator checks,positive atoms,retained norm atoms,degree")
    for route in (("abc11","abc11seven") if args.balanced else ("general25","explicit27","weak13","abc13","abc11","abc11seven")):
        print(*audit(route),sep=",")
