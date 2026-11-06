#!/usr/bin/env python3
"""Independent structural and sampled-formula audit of polynomial-855.

No producer code is imported. DAG validity, integer coefficients, the finite
parameter sets, the sum of squares, denominator coverage, and degree/L1 bounds
are checked exactly. A separate evaluator compares all 297 rational residuals
with directly written formulas at six reproducible finite-field samples.
Those samples are consistency checks, not proofs of polynomial identities or
of the source arithmetic theorem. See compact-audit-855.md for the algebra.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import isqrt, prod
from pathlib import Path
import random

REPO = Path(__file__).resolve().parents[2]
CIRCUIT_SHA = "6a1174891dccdd55bfc4cb6e7486cca2a4fde99ee8a755adaac0174f370da55b"
SOURCE_PINS = {
    "modules/Z_definition.json": "3481dc07810493980b94071aab3e728ead885710213d1fef337199e8d2f73885",
    "modules/q_anchor.json": "961e0cdbaefef28d3fa718f4e5924b5b60e4c500fb4bf2ce33e0898a4650c270",
    "modules/q_batch41.json": "2f9e8adfdabb3a224ddb0599c99c8e39877d27ac28516feec1a3df831aae96e2",
    "modules/q_compare4.json": "0c529d02717b4300bb76525f3eb13524abfc99a6156a96c18b4ba5492cc31482",
    "modules/q_height_batch.json": "15fc8a127c95a27b6104c9dfab5890c9f2ad801ee24203431248860f52b1ac42",
    "modules/q_primeparity.json": "df89176d00ab6cc61e86416c5d1209554fcf87f45f30a866177c76683c2a306a",
    "shared.json": "e8da6dac27a0aab65ab8a377a9a9c78bd8baccd40f4dff229fce17759b03cc28",
    "compiler/archive_build.py": "c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912",
    "compiler/reciprocal_kernel.py": "c4e94463cd59a2418a6502ac7cdcfd713edf9bc1134fe0b4d4bd84700983b304",
}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def ceil_log2(n):
    return (n-1).bit_length() if n else 0


def source_inventory():
    root = REPO / "quartics/quartic-12504/source"
    for name, expected in SOURCE_PINS.items():
        check(digest((root/name).read_bytes()) == expected, "Source pin differs: "+name)
    modules = {p.stem: json.loads(p.read_text()) for p in (root/"modules").glob("*.json")}
    counts = Counter()
    def visit(name, stack=()):
        check(name not in stack, "Recursive source call graph")
        counts[name] += 1
        for call in modules[name]["calls"]:
            visit(call["module"], stack+(name,))
    visit("Z_definition")
    check(counts == {"Z_definition": 1, "q_anchor": 1, "q_height_batch": 1,
                     "q_primeparity": 42, "q_compare4": 41, "q_batch41": 41}, "Source call counts differ")
    def labels(name):
        return [op[2] for op in modules[name]["construction_log"] if op[0] == "variable"]
    root_points = [s for s in labels("Z_definition") if s.endswith(".u.0")]
    private_points = [s for s in labels("q_compare4") if s.endswith(".u.0")]
    check(len(root_points) == 6 and len(private_points) == 5, "Point inventory differs")
    check(modules["q_compare4"]["compressed_primary_charts"] is True, "Unexpected comparison source")
    check(modules["q_compare4"]["label_precision"] == 16 and modules["q_compare4"]["precision"] == 64,
          "Unexpected logarithm precisions")
    check(modules["q_batch41"]["orders"] == [1]*23+[16]*2+[64]*8+[16]*2+[64]*6, "Comparison orders differ")
    check(modules["q_height_batch"]["orders"] == [1,1,1,1,48,48], "Height orders differ")
    check(labels("q_primeparity") == ["prime parity."+s for s in ("t","U","e","p","q","s","h")],
          "Pole coordinates differ")
    shared = json.loads((root/"shared.json").read_text())
    check(shared["witnesses"] == 25 and shared["residuals"][0] == [[-3,[]],[1,[-1]]], "Anchor seed differs")
    for k, row in enumerate(shared["residuals"][1:], 2):
        check(row == [[1,[-k]],[-1,[-k+1,-k+1]]], "Anchor square chain differs")
    check(modules["q_anchor"]["anchor_constant_global_index"] == -25, "Wrong anchor constant index")
    root_meta = modules["Z_definition"]
    check((root_meta["contact_scale"], root_meta["contact_shift"], root_meta["contact_W"])
          == (47027,3,25878772920), "Contact constants differ")
    return modules, dict(counts)


def structure(obj):
    nodes, var = obj["nodes"], obj["variables"]
    check(len(var) == 855 and [v["index"] for v in var] == list(range(855)), "Wrong variable list")
    check(len({v["name"] for v in var}) == 855 and var[0]["name"] == "input", "Variable names or input differ")
    categories = dict(Counter(v["category"] for v in var))
    check(categories == {"input":1,"point":633,"anchor":3,"proxy":3,"root approximation":1,
                         "pole":210,"denominator":1,"contact":2,"inverse":1}, "Wrong coordinate counts")
    parameters = obj["finite_parameters"]
    check(parameters["j"] == list(range(212)), "Wrong common-chart choices")
    corrections = {sign*prod(p for k,p in enumerate((2,3,5,7,11,13,17)) if mask>>k&1)
                   for sign in (-1,1) for mask in range(128)}
    check(len(parameters["correction"]) == 256 and set(parameters["correction"]) == corrections,
          "Wrong signed squareclass choices")
    check(set(parameters) == {"j","correction"}, "Unexpected formal parameters")

    bounds, factors, zero, seen_variables, seen_parameters = [], [], [], set(), set()
    for i, node in enumerate(nodes):
        check(type(node) is list and node, "Invalid node")
        op, *args = node
        children = args if op in ("add","mul","neg") else args[:1] if op == "pow" else []
        check(all(type(k) is int and 0 <= k < i for k in children), "DAG is not topologically ordered")
        if op == "int":
            check(len(args) == 1 and type(args[0]) is int, "Invalid integer node")
            bound = (0, ceil_log2(abs(args[0]))); fs = frozenset(); z = args[0] == 0
        elif op == "variable":
            check(len(args) == 1 and type(args[0]) is int and 0 <= args[0] < 855, "Invalid variable node")
            seen_variables.add(args[0]); bound = (1,0); fs = frozenset((i,)); z = False
        elif op == "parameter":
            check(len(args) == 2 and args[0] in parameters, "Invalid parameter node")
            magnitude = max(map(abs, parameters[args[0]]))
            check(type(args[1]) is int and args[1] >= magnitude, "Parameter magnitude understated")
            seen_parameters.add(args[0]); bound = (0,ceil_log2(magnitude)); fs = frozenset((i,)); z = False
        elif op == "neg":
            check(len(args) == 1, "Invalid negation")
            bound, fs, z = bounds[args[0]], factors[args[0]], zero[args[0]]
        elif op == "add":
            check(len(args) >= 2, "Invalid addition")
            bound = (max(bounds[k][0] for k in args), max(bounds[k][1] for k in args)+ceil_log2(len(args)))
            fs, z = frozenset((i,)), False
        elif op == "mul":
            check(len(args) >= 2, "Invalid multiplication")
            bound = tuple(sum(bounds[k][j] for k in args) for j in (0,1))
            fs, z = frozenset().union(*(factors[k] for k in args)), any(zero[k] for k in args)
        elif op == "pow":
            check(len(args) == 2 and type(args[1]) is int and args[1] >= 0, "Invalid power")
            bound = tuple(b*args[1] for b in bounds[args[0]])
            fs = factors[args[0]] if args[1] else frozenset()
            z = zero[args[0]] and args[1] != 0
        else:
            raise ValueError("Unknown arithmetic node: "+str(op))
        bounds.append(bound); factors.append(fs); zero.append(z)
    check(seen_variables == set(range(855)) and seen_parameters == set(parameters), "Missing coordinates or parameters")

    equations = obj["rational_equations_before_clearing"]
    check(len(equations) == 297 and len({r["label"] for r in equations}) == 297, "Wrong residual inventory")
    guards = obj["nonzero_numerators"]
    check(len(guards) == len(set(guards)) == 1681, "Wrong guard inventory")
    required = frozenset().union(*(factors[g] for g in guards))
    check(not any(zero[g] for g in guards), "Literal zero guard")
    guard_product = obj["guard_product_node"]
    check(not zero[guard_product] and factors[guard_product] == required and len(required) == 1602,
          "Guard product has different zero factors")
    for row in equations:
        check(not zero[row["denominator"]] and factors[row["denominator"]] <= required,
              "An equation denominator has an unguarded factor: "+row["label"])

    # Exact syntactic proof of the sum of 298 squares, without expanding the
    # potentially enormous polynomials inside each square.
    lookup = {tuple(node):i for i,node in enumerate(nodes)}
    check(len(lookup) == len(nodes), "Repeated DAG nodes")
    def square(i):
        op,*a = nodes[i]
        if op == "int" and a[0] in (0,1): return i
        return lookup[("pow", a[0], 2*a[1])] if op == "pow" else lookup[("pow",i,2)]
    inverse = lookup[("variable",854)]
    check(var[854]["name"] == "common denominator inverse", "Wrong guard witness")
    product_node = lookup[("mul", *sorted((inverse,guard_product)))]
    guard_equation = lookup[("add", *sorted((product_node,lookup[("int",-1)])))]
    expected = Counter(square(row["numerator"]) for row in equations)
    expected[square(guard_equation)] += 1
    todo, actual = [obj["template_output"]], Counter()
    while todo:
        i = todo.pop()
        if nodes[i][0] == "add": todo.extend(nodes[i][1:])
        else: actual[i] += 1
    check(actual == expected, "Template output is not the specified sum of squares")
    branches = prod(len(values) for values in parameters.values())
    degree, bits = bounds[obj["template_output"]]
    report = obj["report"]
    check(report["degree_upper_bound"] == degree*branches, "Degree bound differs")
    check(report["coefficient_log2_upper_bound"] == bits*branches, "Coefficient L1 bound differs")
    check(report["finite_branches"] == branches == 54272, "Branch count differs")
    return {"variables":855,"witnesses":854,"rational_residuals":297,"squares_per_branch":298,
            "finite_branches":branches,"guard_numerators":len(guards),"guard_factors":len(required),
            "degree_upper_bound":degree*branches,"log2_coefficient_upper_bound":bits*branches,
            "branch_degree_bound":degree,"branch_l1_log2_bound":bits,"node_count":len(nodes),
            "bound_convention":"degree <= D and coefficient height <= L1 norm <= 2^B"}


def evaluate_dag(obj, values, parameter_values, p):
    answer = []
    for op, *a in obj["nodes"]:
        if op == "int": v = a[0]
        elif op == "variable": v = values[a[0]]
        elif op == "parameter": v = parameter_values[a[0]]
        elif op == "neg": v = -answer[a[0]]
        elif op == "add": v = sum(answer[k] for k in a)
        elif op == "mul":
            v = 1
            for k in a: v = v*answer[k] % p
        elif op == "pow": v = pow(answer[a[0]],a[1],p)
        answer.append(v % p)
    return answer


class DirectFormulas:
    """Direct arithmetic in F_p[s]/(s^2-2); no rational-expression DAG."""
    def __init__(self, values, parameters, modules, p):
        self.values, self.pars, self.modules, self.p = values, parameters, modules, p
        self.D = (11%p,-6%p); self.equations = {}
    def inv(self, a):
        a %= self.p
        if a == 0: raise ZeroDivisionError
        return pow(a,-1,self.p)
    def fraction(self, a):
        a = Fraction(a)
        return a.numerator*self.inv(a.denominator)%self.p
    def var(self, name): return self.values[name]
    def add(self,a,b): return tuple((x+y)%self.p for x,y in zip(a,b))
    def sub(self,a,b): return tuple((x-y)%self.p for x,y in zip(a,b))
    def scale(self,a,c): return tuple(x*c%self.p for x in a)
    def mul(self,a,b):
        return ((a[0]*b[0]+2*a[1]*b[1])%self.p,(a[0]*b[1]+a[1]*b[0])%self.p)
    def power(self,a,n):
        out = (1,0)
        while n:
            if n&1: out = self.mul(out,a)
            a = self.mul(a,a); n >>= 1
        return out
    def div(self,a,b):
        norm = b[0]*b[0]-2*b[1]*b[1]
        return self.scale(self.mul(a,(b[0],-b[1])),self.inv(norm))
    @staticmethod
    def conj(a): return a[0],-a[1]
    def double(self,point):
        x,y = point
        h = self.div(self.sub(self.scale(self.mul(x,x),3),self.D),self.scale(y,2))
        xx = self.sub(self.mul(h,h),self.scale(x,2))
        return xx,self.sub(self.mul(h,self.sub(x,xx)),y)
    def reciprocal(self,point): return self.div((1,0),point[0])
    def z(self,point): return self.scale(self.div(point[0],point[1]),-1)
    def eq(self,label,value):
        check(label not in self.equations, "Repeated reference residual")
        self.equations[label] = value%self.p
    def point(self,label):
        a = (self.var(label+".a0"),self.var(label+".a1")); C = self.var(label+".C")
        A,B = self.sub(self.power(a,3),self.mul(self.D,a)); j = self.pars["j"]
        lam = j*j-2
        gamma = 8*C**4-4*((j*j+2)*A+4*j*B)*C*C+(2*j*A+(j*j+2)*B)**2
        self.eq(label+".quartic half-point",gamma*self.inv(-4*lam*lam))
        # Closed reconstruction formulas, rather than the producer's V,h steps.
        b = ((-4*C*C+2*j*j*A+j*(j*j+2)*B),
             (2*j*C*C-2*j*A-(j*j+2)*B))
        b = self.scale(b,self.inv(2*lam*C))
        return self.double((a,b))
    def difference(self,a,b):
        h = self.div(self.add(a[1],b[1]),self.sub(a[0],b[0]))
        x = self.sub(self.sub(self.mul(h,h),a[0]),b[0])
        return x,self.sub(self.mul(h,self.sub(a[0],x)),a[1])
    def log(self,point,precision):
        f = self.reciprocal(point); w = self.mul(self.D,self.mul(f,f)); g = (1,0)
        for k in range(1,precision//4):
            coefficient = Fraction(-2*prod(4*s-5 for s in range(2,k+1)),
                                   5*prod(4*s+1 for s in range(2,k+1)))
            g = self.add(g,self.scale(self.power(w,k),self.fraction(coefficient)))
        return self.mul(self.z(point),g)
    def parity(self,b,label):
        t,e,q1,q2,s = (self.var(label+"."+k) for k in ("t","e","p","q","s"))
        U = b*(1-b*t*t)*self.inv(1+b*t*t)%self.p
        B = 17*b; h = e*(B-U*U)%self.p
        self.eq(label+".first conic",q1*q1-B*(1-e)*(1+3*e))
        self.eq(label+".second conic",B*q2*q2-s**4-2*B*h*s*s+3*B*B*h*h)
    def batch(self,r,tests,label,height=False):
        module = self.modules["q_height_batch" if height else "q_batch41"]
        leaves = []
        # Read the ordered pairing plan from the frozen source JSON.
        for step in module["norm_tree"]:
            if step["type"] == "constant_pair":
                value = 1+tests[step["test"]-1]**2*self.inv(r)
            elif step["type"] == "single":
                value = tests[step["test"]-1]*self.inv(pow(r,step["order"],self.p))
            else:
                a,b = [tests[k-1] for k in step["tests"]]
                value = (a*a+r*b*b)*self.inv(pow(r,2*step["order"],self.p))
            leaves.append(value%self.p)
        sizes = []
        while len(leaves)>1:
            sizes.append(len(leaves))
            leaves = [(leaves[k]**2+r*leaves[k+1]**2)%self.p if k+1<len(leaves) else leaves[k]
                      for k in range(0,len(leaves),2)]
        check(sizes == module["norm_level_sizes"], "Source norm-tree levels differ")
        argument = r*leaves[0]**2%self.p
        if height: argument = argument*self.pars["correction"]%self.p
        self.parity(argument,label+".parity")
    def build(self):
        X = self.var("input"); beta = (X*X+2)%self.p
        points = [self.point(k) for k in ("A","S","T","Z")]
        f0,f1 = self.reciprocal(points[1]); r = (f0*f0+f0*f1-f1*f1)%self.p
        u,v,w = (self.var("anchor."+k) for k in ("u","v","w"))
        self.eq("packed semilocal anchor",u*u+6*v*v-2*w*w-3*r*r+2*pow(3,2**26,self.p))
        s,t,z = (self.var("proxy."+k) for k in ("s","t","z"))
        self.eq("Lucas relation",t*t-s*(s-2)*t*z+(s-2)**2*z*z-1)
        theta = self.var("theta"); error = (theta*theta-2)%self.p
        J0 = self.point("height.J")
        tests = list(self.reciprocal(J0)+self.reciprocal(points[1])+self.div(self.z(points[1]),self.z(J0)))
        r = prod((beta,beta-1,beta-2401,32*beta+343,2*beta-1))%self.p
        self.batch(r,tests,"height",True)
        base = ((self.fraction(Fraction(57,8)),self.fraction(Fraction(-7,2))),
                (self.fraction(Fraction(-165,8)),self.fraction(Fraction(417,32))))
        targets = [self.double(self.double(base))]+[self.double(self.double(P)) for P in points]
        J = self.point("comparison.J"); fJ = self.conj(self.reciprocal(J))
        zJinv = self.div((1,0),self.conj(self.z(J)))
        e = self.var("coordinate denominator"); u = self.var("contact.u"); v = self.var("contact.v")
        scalars = [e]+[e*x%self.p for P in points for x in P[0]]
        contacts = [v*self.inv(32*25878772920)%self.p,u,u-v,u-2401*v,u+self.fraction(Fraction(343,32))*v]
        for a in scalars:
            A = (47027*a+3)%self.p
            contacts += [u-A*v,u-(A-1)*v,u-(A-2401)*v,u-(A+self.fraction(Fraction(343,32)))*v]
        check(len(contacts) == 41, "Wrong reference contact count")
        for k,r in enumerate(contacts):
            label = "contact"+str(k)
            private = [self.point(label+"."+name) for name in ("H","beta","s","t","z")]
            diffs = [self.difference(P,Q) for P,Q in zip(private,targets)]
            expressions = [self.reciprocal(P) for P in private]+[fJ]+[self.conj(self.reciprocal(P)) for P in diffs]
            denominator = self.log(private[0],64)
            expressions += [self.sub(self.div(self.log(P,16 if i==0 else 64),denominator),(proxy,0))
                            for i,(P,proxy) in enumerate(zip(private[1:],(beta,s,t,z)))]
            expressions += [self.mul(self.conj(self.z(P)),zJinv) for P in diffs]
            tests = [error]
            for a,b in expressions: tests += [error*b%self.p,(a+theta*b)%self.p]
            self.batch(r%self.p,tests,label+".norm")
        return self.equations


def sampled_formulas(obj,modules):
    rng = random.Random(20261106); results = []
    for p in (1000003,1000037):
        check(all(p%d for d in range(2,isqrt(p)+1)), "Sample modulus is not prime")
        check(pow(2,(p-1)//2,p) == p-1, "Quadratic sample algebra is not a field")
        for j, correction in ((0,1),(1,-510510),(211,510510)):
            for attempt in range(20):
                values = [rng.randrange(p) for _ in obj["variables"]]
                pars = {"j":j,"correction":correction}
                numerical = evaluate_dag(obj,values,pars,p)
                if any(numerical[k] == 0 for k in obj["nonzero_numerators"]): continue
                try:
                    named = {v["name"]:values[v["index"]] for v in obj["variables"]}
                    expected = DirectFormulas(named,pars,modules,p).build()
                    check(set(expected) == {r["label"] for r in obj["rational_equations_before_clearing"]},
                          "Reference and circuit residual inventories differ")
                    for row in obj["rational_equations_before_clearing"]:
                        value = numerical[row["numerator"]]*pow(numerical[row["denominator"]],-1,p)%p
                        check(value == expected[row["label"]], "Sampled residual differs: "+row["label"])
                except ZeroDivisionError:
                    continue
                results.append({"prime":p,"j":j,"correction":correction,"attempt":attempt,
                                "matching_rational_residuals":len(expected)})
                break
            else: raise ValueError("Could not obtain a nonsingular sample")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package",type=Path,default=REPO/"research/optimization/polynomial-855")
    parser.add_argument("--receipt",type=Path,default=REPO/"research/optimization/verification-855.json")
    args = parser.parse_args()
    data = (args.package/"polynomial-circuit.json").read_bytes()
    check(digest(data) == CIRCUIT_SHA,"Circuit digest differs from the audited artifact")
    obj = json.loads(data); modules, counts = source_inventory()
    exact = structure(obj); samples = sampled_formulas(obj,modules)
    cubic = (195,-78,-26,-14)
    residues = [sum(c*pow(a,k,19) for k,c in enumerate(cubic))%19 for a in range(19)]
    check(cubic[-1]%19 != 0 and all(residues), "Short logarithm irreducibility check failed")
    receipt = {
        "status":"PASS for the checks explicitly listed below",
        "exact_structural_checks":exact,"source_occurrences":counts,"source_sha256":SOURCE_PINS,
        "short_logarithm_cubic":{"coefficients_in_ascending_order":cubic,"modulus":19,
                                  "values_at_all_residue_classes":residues,
                                  "conclusion":"irreducible over Q, so no root in Q(sqrt(2))"},
        "sampled_formula_checks":samples,"sample_scope":"Finite-field evaluations do not prove general polynomial identities",
        "mathematical_review":"See compact-audit-855.md for source correspondence, chart coverage, and nonvanishing proofs",
        "not_checked":["The source arithmetic theorem defining Z","Expanded monomial table","Exact degree or coefficient height","Global optimality"],
        "circuit_sha256":digest(data),"checker_sha256":digest(Path(__file__).read_bytes()),
    }
    args.receipt.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"status":"PASS","variables":exact["variables"],"degree_upper_bound":exact["degree_upper_bound"],
                      "log2_coefficient_upper_bound":exact["log2_coefficient_upper_bound"],
                      "samples":len(samples),"residuals_per_sample":297,"receipt":str(args.receipt)}))


if __name__ == "__main__":
    main()
