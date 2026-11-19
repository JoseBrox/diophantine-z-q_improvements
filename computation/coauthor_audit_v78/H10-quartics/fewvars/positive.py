"""Generate positive reciprocal-square-trace native sources and degree bounds."""
import argparse
import ast
from functools import cache
import hashlib
import importlib.util
import inspect
import json
import math
from pathlib import Path
import subprocess
import sys
import textwrap

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=HERE.parent/"source")
parser.add_argument("--termwise",action="store_true")
parser.add_argument("--balanced",action="store_true",help="eleven-variable positive balancing denominators")
parser.add_argument("--parameter",type=int,help="fixed L or B, default is the upstream stored member")
parser.add_argument("--route", choices=["general25","explicit27","weak13","abc13","abc11","abc11seven"])
parser.add_argument("--output", type=Path)
args = parser.parse_args()
if args.balanced:args.termwise=True
if args.output is None:args.output=HERE/("balanced" if args.balanced else "positive_factors" if args.termwise else "positive")
BASE = args.repo.resolve()/"computation/few_variables"
sys.path.insert(0,str(BASE/"unit_norm_v28"))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def transform(source,namespace):
    if args.termwise:
        # Only the second argument in each W <- W * (1+a) update changes.
        class PositiveFactor(ast.NodeTransformer):
            count=0
            def visit_Assign(self,node):
                self.generic_visit(node)
                call=node.value
                if len(node.targets)!=1 or not isinstance(node.targets[0],ast.Name) or node.targets[0].id!="W" or not isinstance(call,ast.Call) or len(call.args)!=2:
                    return node
                assert ast.unparse(call.func)=="self.mul" and ast.unparse(call.args[0])=="W"
                factor=call.args[1]
                assert ast.unparse(factor.func)=="self.add" and ast.unparse(factor.args[0])=="self.field(1)"
                call.args[1]=ast.Call(func=ast.Name(id="positive_factor",ctx=ast.Load()),args=[ast.Name(id="self",ctx=ast.Load()),factor.args[1]],keywords=[])
                self.count+=1
                return node
        rewrite=PositiveFactor()
        tree=rewrite.visit(ast.parse(source));assert rewrite.count in (1,2)
        new=ast.unparse(tree)
    else:
        new=source
    marker=next(line for line in new.splitlines() if line.strip().replace(" ","")=="norm=self.norm(W)")
    assert new.count(marker)==1
    lead=marker[:len(marker)-len(marker.lstrip())]
    if args.termwise:
        newlines=[marker,lead+"self.events.append(dict(operation='positive_detector_product',",
                  lead+"    W=[self.rr(x) for x in W], norm=self.rr(norm)))"]
    else:
        newlines=[lead+"original_product = W",lead+"W = self.square(W)",marker,
                  lead+"self.events.append(dict(operation='reciprocal_square_trace',",
                  lead+"    original=[self.rr(x) for x in original_product],",
                  lead+"    squared=[self.rr(x) for x in W],norm=self.rr(norm)))"]
    new=new.replace(marker,"\n".join(newlines))
    scope=dict(namespace)
    def positive_factor(self,raw):
        self.events.append(dict(operation="positive_factor_argument",raw=[self.rr(x) for x in raw]))
        return self.add(self.field(1),self.square(raw))
    scope["positive_factor"]=positive_factor
    exec(compile(new,"squared-reciprocal-trace","exec"),scope)
    return scope["build"]


def native(route):
    import build_sources as old
    if route=="general25":
        mod=load("newtrace_parent25",BASE/"even_valuation25_v75/build_source.py")
        mod.patch()
        text=textwrap.dedent(inspect.getsource(old.General25.build))
        before="for C,order in zip(tests,comparison_orders):"
        after="for test_index,(C,order) in enumerate(zip(tests,comparison_orders)):"
        assert text.count(before)==text.count("self.scale(self.square(C),weight)")==1
        text=text.replace(before,after).replace("self.scale(self.square(C),weight)","self.scale(C if test_index<10 else self.square(C),weight)")
        mod._native_build=transform(text,old.General25.build.__globals__)
        return mod.FullAuxiliary25(3 if args.parameter is None else args.parameter).build(),mod.helper.old._subalgebra.compile_specification
    if route.startswith("abc11"):
        mod=load("newtrace_parent11",BASE/"even_valuation11_v75/build_source.py")
        mod.patch_compiler()
        path=BASE/"derivative11_v63/build_source.py"
        body=path.read_text()
        cls=next(n for n in ast.parse(body).body if isinstance(n,ast.ClassDef) and n.name=="Derivative11")
        method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="build")
        text=ast.get_source_segment(body,method)
        # get_source_segment excludes preceding indentation on the first line.
        text=textwrap.dedent("    "+text)
        for before,after in mod.CHANGES.items():
            assert text.count(before)==1
            text=text.replace(before,after)
        if args.balanced:
            start=text.index("        if i < 2:")
            end=text.index("        transformed.append(Di)",start)
            text=text[:start]+"""        if i<2:
            L=[H['x'],U['x']][i]
            R=self.field(1)
        elif i<4:
            point=[HminusP,UminusA][i-2]
            L=point['X']
            R=self.square(point['dx'])
        else:
            L=self.field(1)
            R=self.square(C)
        n=self.square(R)
        den=self.add(self.square(L),self.scale(n,u**2))
        bn=self.norm(den)
        self.c.nonzero(bn,'balanced%d.denominator norm'%i)
        self.events.append(dict(operation='sum_square_balance',index=i,
            L=[self.rr(x) for x in L],R=[self.rr(x) for x in R],
            denominator_components=[self.rr(x) for x in den],norm=self.rr(bn),
            numerator_components=[self.rr(x) for x in n],
            u=self.rr(u),nonzero=self.rr(self.norm(L))))
        Di=self.div(n,den)
        if i in (2,3):Di=self.conj(Di)
"""+text[end:]
            assert text.count("self.scale(self.square(Di), 1/u)")==1
            text=text.replace("self.scale(self.square(Di), 1/u)","self.scale(Di, 1/u)")
        mod.old.Derivative11.build=transform(text,mod.old.__dict__)
        return mod.make_source(3 if args.parameter is None else args.parameter,7 if route.endswith("seven") else 9),mod.old.parent_specification
    cls=old.Explicit27 if route=="explicit27" else old.Conditional13
    cls.build=transform(textwrap.dedent(inspect.getsource(cls.build)),cls.build.__globals__)
    compiler=load("newtrace_parentcompiler",BASE/"subalgebra_norms_v30/build.py")
    return old.make_source(route,args.parameter),compiler.compile_specification


def calculate(source,spec):
    nodes=source["coefficient_dag"]
    @cache
    def atoms(i):
        op,*ys=nodes[i]
        if op=="int":
            assert ys[0];return set()
        if op in ("neg","pow"):return atoms(ys[0]) if op=="neg" or ys[1] else set()
        if op=="mul":return set.union(*(atoms(j) for j in ys))
        return {i}
    roots={f["generator_node"] for f in source["finite_blocks"] if f["kind"]=="pole"}
    retained=set.union(*(atoms(i) for i in source["guard_numerators"] if i not in roots))
    events=[e for e in source["events"] if e["operation"]=="reciprocal_square_trace"]
    safe=set()
    for e in events:
        # Only atoms first appearing after the original components are candidates.
        # Rewrite of a_i/b_i ensures all numerator factors of the rational
        # representation of (W_0)^2+2(W_1)^2 are nonzero at a rational
        # character when its component denominators and the norm are nonzero.
        original_cutoff=max(c[k] for c in e["original"] for k in ("numerator","denominator"))
        support=atoms(e["squared"][0]["numerator"])
        automatic={i for i in support if i>original_cutoff}
        assert len(automatic)==1
        assert all(nodes[i][0]=="add" for i in automatic)
        assert automatic.isdisjoint(set.union(*(atoms(c["denominator"]) for c in e["original"])))
        assert automatic.isdisjoint(atoms(e["norm"]["numerator"]))
        safe.update(automatic)
    if args.termwise:
        masks=[e for e in source["events"] if e["operation"]=="positive_factor_argument"]
        products=[e for e in source["events"] if e["operation"]=="positive_detector_product"]
        assert len(products)==len(roots) and len(masks)>=len(products)
        denominators={c["denominator"] for e in masks for c in e["raw"]}
        denominators.update(c["denominator"] for e in products for c in [*e["W"],e["norm"]])
        protected=set().union(*(atoms(i) for i in denominators))
        safe=set().union(*(atoms(c["numerator"]) for e in products for c in [e["W"][0],e["norm"]]))-protected
        safe &= retained
    balanced_safe=set()
    if args.balanced:
        balance=[e for e in source["events"] if e["operation"]=="sum_square_balance"]
        assert len(balance)==6
        bsafe=set().union(*(atoms(e["norm"]["numerator"]) for e in balance))
        base_protected=set()
        for e in balance:
            for c in [*e["L"],*e["R"],*e["denominator_components"],e["norm"],e["u"],e["nonzero"]]:
                base_protected|=atoms(c["denominator"])
            base_protected|=atoms(e["u"]["numerator"])|atoms(e["nonzero"]["numerator"])
        assert base_protected<=retained-safe
        balanced_safe=(bsafe&retained)-base_protected-safe
    kept=retained-safe-balanced_safe
    factors={r["node"]:r for r in spec["subalgebra_norm_factors"]}
    g=sum(factors[i]["scalar_norm_degree_bound"] for i in kept)
    glog=sum(factors[i]["scalar_norm_log2_l1_bound"] for i in kept)
    points=[r for r in spec["quadratic_tower"] if r["kind"]!="pole"]
    poles=[r for r in spec["quadratic_tower"] if r["kind"]=="pole"]
    m=len(points);s=len(poles);k=1 if s==1 else 3
    w=k*max(r["root_weight"] for r in poles);b=k*max(r["envelope_degree"] for r in poles)
    numlog=(s-1).bit_length()+max(i+k*r["root_operator_log2_norm"] for i,r in enumerate(poles))
    denlog=2+s.bit_length()+max(i+k*r["envelope_log2_l1"] for i,r in enumerate(poles))
    for r in reversed(points):
        w=r["root_weight"]+max(w,b)
        b+=r["envelope_degree"]
        numlog=r["root_operator_log2_norm"]+1+max(numlog,denlog)
        denlog+=2+r["envelope_log2_l1"]
    n=2**(m+s);before=n*(g+w+1);v=source["total_external_variables"];flag=int(source["multiply_by_input"])
    support=math.comb(before+v,v)-math.comb(before-n+v-1,v)
    logheight=n*(1+numlog+glog)
    return dict(route=args.route,source_sha256=spec["native_source_sha256"],degree=before+flag,
                pole_ordinate_guards=sorted(roots),positive_trace_atoms=sorted(safe),positive_balancing_atoms=sorted(balanced_safe),norm_guard_nodes=sorted(kept),
                guard_degree=g,separator_degree=w,rank=n,log2_l1=logheight,height_double_power=logheight.bit_length(),
                support_power=support.bit_length(),extra_witness_degree=2*max(1+g,n*(1+w))+flag)


if __name__=="__main__":
    if args.route:
        source,compiler=native(args.route)
        source.update(proof="POSITIVE.md",squared_reciprocal_traces=not args.termwise,positive_detector_factors=args.termwise,positive_balancing=args.balanced)
        source["arithmetic_status"]="Inherits the pinned arithmetic premises and parameter threshold, with positive detector factors or a squared product as specified."
        spec=compiler(source)
        result=calculate(source,spec)
        subdir=args.output/args.route
        subdir.mkdir(parents=True,exist_ok=True)
        for file,obj in [("native",source),("parent",spec),("certificate",result)]:
            (subdir/(file+".json")).write_text(json.dumps(obj,sort_keys=True,separators=(",",":"))+"\n")
        print(*(result[x] for x in ["route","degree","guard_degree","separator_degree","height_double_power","support_power","positive_trace_atoms","extra_witness_degree"]))
    else:
        for route in (["abc11","abc11seven"] if args.balanced else ["general25","explicit27","weak13","abc13","abc11","abc11seven"]):
            subprocess.run([sys.executable,"-B",str(Path(__file__).resolve()),"--repo",str(args.repo),"--output",str(args.output),"--route",route]+(["--termwise"] if args.termwise else [])+(["--balanced"] if args.balanced else [])+(["--parameter",str(args.parameter)] if args.parameter is not None else []),check=True)
