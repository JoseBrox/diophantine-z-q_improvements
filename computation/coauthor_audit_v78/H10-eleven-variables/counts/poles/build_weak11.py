"""Single-pole definition under fixed weak abc, using the upstream free point chart."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=HERE.parents[1]/"source")
parser.add_argument("--output", type=Path)
parser.add_argument("--strong", action="store_true", help="use the 16/15 weak-abc exponent")
parser.add_argument("--eight",action="store_true",help="eight finite contact slots and fresh-valuation-one scalar")
parser.add_argument("--simple",action="store_true",help="fresh-valuation-one scalar and quadratic balancing")
parser.add_argument("--shift", type=int, default=3)
args = parser.parse_args()
if args.eight:args.simple=True
if args.output is None:
    args.output=HERE/(("simple_strong" if args.strong else "simple") if args.simple else ("strong" if args.strong else "specification"))
    if args.eight:args.output=HERE/("eight_strong" if args.strong else "eight")
BASE = args.repo.resolve()/"computation/few_variables"
sys.path.insert(0,str(BASE/"unit_norm_v28"))
from build_sources import Conditional13
from field_circuit import Circuit

THETA = [Fraction(0), Fraction(-1), Fraction(-1,2), Fraction(-1,3), Fraction(-1,4), Fraction(-2,5)]
if args.eight:THETA=list(map(Fraction,["0","-1/21","-1/17","-1/25","-1/16","-1/26","-1","-1/41"]))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Weak11(Conditional13):
    def __init__(self,shift):
        if shift<3 or shift%2!=1:raise ValueError("shift must be odd and at least three")
        self.shift=shift
        self.scale_power=6 if args.strong else 10
        self.band=6 if args.strong else 15
        if args.eight:
            self.scale_power=4 if args.strong else 6
            self.band=5 if args.strong else 6
        self.c=Circuit()
        self.D=self.field(11,-6)
        self.relations=[];self.closed_equations=[];self.events=[]
        self.fourfold_points={};self.parametrize_poles=True
        self.X=self.c.variable("input.X","retained.input")
        self.point_names=["A","H","UA"]
        self.abscissas={name:tuple(self.c.variable(name+".a"+str(i),"retained.point") for i in range(2)) for name in self.point_names}
        self.z=self.c.variable("contact.z","retained.slope")
        self.pole_pair=tuple(self.c.variable("pole."+name,"retained.pole") for name in ("tau","s"))
        self.base_count=len(self.c.variables)

    def contact(self,x):
        product=self.c.rational(1)
        for theta in THETA:
            product*=x-theta
        return product

    def build(self):
        A,H,U=[self.point(name) for name in self.point_names]
        beta=self.X**2+self.c.parameter("fixed_input_shift",self.shift)
        T=2*A["x"][0]
        M=beta**self.scale_power+T**self.scale_power
        a=M
        x,y=a-self.z,a+self.z
        p,q=self.contact(x),self.contact(y)
        K=self.band
        guard_factor=(x-1)*(y-1)
        denominator=(p**3+q**5)*(p+q**K)*(p**K+q)
        if args.simple:
            u=guard_factor**(len(THETA)*(K-1))*p*q*(p**2+q**3)**2/denominator
        else:
            u=guard_factor**(6*K)*(p*q)**3/denominator
        w=u/(1+u)**2
        self.c.nonzero(u,"nonzero weight")
        self.events.append(dict(operation="moving_contacts",theta=[str(t) for t in THETA],band=K,scale_power=self.scale_power,
                                **{name:self.rr(value) for name,value in dict(beta=beta,T=T,M=M,a=a,x=x,y=y,p=p,q=q,u=u,w=w).items()}))
        Hm=self.difference(H,self.fixed_point());Um=self.difference(U,A)
        L=self.div(self.parameter_at_identity(U),self.parameter_at_identity(H))
        Lp=self.conj(self.div(self.parameter_at_identity(Um),self.parameter_at_identity(Hm)))
        tests=[self.reciprocal(H),self.reciprocal(U),self.conj(self.reciprocal(Hm)),self.conj(self.reciprocal(Um)),self.sub(L,Lp),self.sub(L,self.field(self.X))]
        W=self.field(1)
        for i,test in enumerate(tests):
            c2=self.square(test)
            numerator=c2 if args.simple else self.square(c2)
            if args.simple and i<4:
                if i<2:
                    left=[H,U][i]["x"]
                    right=self.field(1)
                else:
                    point=[Hm,Um][i-2]
                    left=self.conj(point["X"])
                    right=self.conj(self.square(point["dx"]))
                den=self.add(left,self.scale(right,u))
                t=self.div(right,den)
            else:
                den=self.add(self.field(1),self.scale(numerator,u if args.simple else u**2))
                t=self.div(numerator,den)
            summand=self.scale(self.square(t),1/u**2)
            W=self.mul(W,self.add(self.field(1),summand))
            self.events.append(dict(operation="test",C=[self.rr(k) for k in test],den=[self.rr(k) for k in den],
                                    den_norm=self.rr(self.norm(den)),t=[self.rr(k) for k in t],summand=[self.rr(k) for k in summand]))
        nW=self.norm(W)
        self.c.nonzero(nW,"product norm")
        self.c.nonzero(W[0],"trace numerator")
        b=w*nW**2/W[0]**2
        self.events.append(dict(operation="detector",W=[self.rr(k) for k in W],norm=self.rr(nW),b=self.rr(b)))
        self.zero_pole(b,self.pole_pair,"detector0")
        source=self.finish("weak13")
        source.update(name=("strong11" if args.strong else "weak11")+"_single_pole"+("_simple" if args.simple else "")+("_eight" if args.eight else ""),proof="weak11.md",
                      arithmetic_status="Fixed weak rational abc at "+("16/15" if args.strong else "121/100")+", plus the same elliptic, prime-pattern, and native pole premises as upstream weak13; no intrinsic-pole or polynomial-abc premise.")
        assert self.base_count==10 and len(self.relations)==4
        return source


if __name__=="__main__":
    output=args.output
    output.mkdir(parents=True,exist_ok=True)
    source=Weak11(args.shift).build()
    compiler=load("upstream_small_polynomial",BASE/"subalgebra_norms_v30/build.py")
    spec=compiler.compile_specification(source)
    spec.update(native_source_generator="build_weak11.py",arithmetic_scope=source["arithmetic_status"])
    spec["recipe"]["final"]="Multiply the determinant by the input X."
    from finite_bounds import encode
    compact=encode(source,spec)
    files=[("native",source),("polynomial",spec),("compact",compact)]
    if args.simple:files.append(("conservative",encode(source,spec,keep_balance=True)))
    for name,obj in files:
        (output/(name+".json")).write_text(json.dumps(obj,sort_keys=True,separators=(",",":"))+"\n")
    print({k:compact[k] for k in ("variables","degree_bound","rank","support_power","coefficient_double_power")})
