#!/usr/bin/env python3
"""Independent audit of the 42 redundant pole-denominator guards.

This checks a generic exact polynomial identity, then the actual 855 DAG's
denominator factors and variable supports. It imports no circuit producer.
The source-to-rational-formula equivalence is the separate 855 audit.
"""

from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CIRCUIT_SHA = "6a1174891dccdd55bfc4cb6e7486cca2a4fde99ee8a755adaac0174f370da55b"


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Polynomial:
    """Small exact Laurent polynomial ring Z[b,t,e,p,q,s,c]."""
    def __init__(self, value=0):
        self.terms = dict(value.terms) if isinstance(value,Polynomial) else (
            {m:a for m,a in value.items() if a} if isinstance(value,dict)
            else {(0,)*7:value} if value else {})
    @classmethod
    def variable(cls,i):
        monomial = [0]*7;monomial[i] = 1
        return cls({tuple(monomial):1})
    def __add__(self,other):
        other = Polynomial(other);answer = Counter(self.terms)
        for m,a in other.terms.items():answer[m] += a
        return Polynomial(dict(answer))
    __radd__ = __add__
    def __neg__(self):return Polynomial({m:-a for m,a in self.terms.items()})
    def __sub__(self,other):return self+-Polynomial(other)
    def __rsub__(self,other):return Polynomial(other)+-self
    def __mul__(self,other):
        other = Polynomial(other);answer = Counter()
        for m,a in self.terms.items():
            for n,b in other.terms.items():
                answer[tuple(x+y for x,y in zip(m,n))] += a*b
        return Polynomial(dict(answer))
    __rmul__ = __mul__
    def __pow__(self,n):
        require(type(n) is int and n >= 0,"Invalid polynomial exponent")
        out,base = Polynomial(1),self
        while n:
            if n&1:out = out*base
            base = base*base;n >>= 1
        return out
    def __eq__(self,other):return self.terms == Polynomial(other).terms
    def delta_zero(self,e_zero=False):
        answer = Counter()
        for m,a in self.terms.items():
            if e_zero and m[2]:continue
            out = list(m);out[1] -= 2*out[0]
            a *= (-1)**out[0];out[0] = 0
            answer[tuple(out)] += a
        return Polynomial(dict(answer))


class Fraction:
    """Formal fractions used only for cross-multiplied identity checks."""
    def __init__(self,n=0,d=1):
        if isinstance(n,Fraction):self.n,self.d = n.n,n.d
        else:self.n,self.d = Polynomial(n),Polynomial(d)
    def __add__(self,other):
        other = Fraction(other)
        if self.d == other.d:return Fraction(self.n+other.n,self.d)
        return Fraction(self.n*other.d+other.n*self.d,self.d*other.d)
    __radd__ = __add__
    def __neg__(self):return Fraction(-self.n,self.d)
    def __sub__(self,other):return self+-Fraction(other)
    def __rsub__(self,other):return Fraction(other)+-self
    def __mul__(self,other):
        other = Fraction(other)
        return Fraction(self.n*other.n,self.d*other.d)
    __rmul__ = __mul__
    def __pow__(self,n):return Fraction(self.n**n,self.d**n)


def generic_identities():
    b,t,e,p,q,s,c = [Polynomial.variable(i) for i in range(7)]
    delta = 1+b*t**2
    B = c*b
    U = Fraction(b*(1-b*t**2),delta)
    h = Fraction(e)*(Fraction(B)-U**2)
    K = B*delta**2-b**2*(1-b*t**2)**2
    first = p**2-B*(1-e)*(1+3*e)
    second = Fraction(B*q**2)-(Fraction(s**2)-Fraction(B)*h)*(Fraction(s**2)+Fraction(3*B)*h)
    cleared = B*q**2*delta**4-(s**2*delta**2-B*e*K)*(s**2*delta**2+3*B*e*K)
    require(delta**4*second.n-cleared*second.d == 0, "Clearing identity failed")
    inverse_t12 = Polynomial({(0,-12,0,0,0,0,0):1})
    require(cleared.delta_zero() == 48*c**2*e**2*inverse_t12, "Exceptional-fiber identity failed")
    require(t**2*first.delta_zero(e_zero=True) == p**2*t**2+c,
            "First-conic exceptional identity failed")
    return {
        "identities_checked":3,
        "clearing_multiplier":"(1+b*t^2)^4",
        "cleared_second_at_b_minus_inverse_t_squared":"48*c^2*e^2/t^12",
        "first_after_e_zero_and_b_minus_inverse_t_squared":"(p*t)^2+c",
        "field_hypotheses":"Characteristic different from 2 and 3; -c is not a square",
        "rational_application":"c=17; -17 is not a rational square"
    }


def main():
    raw = (ROOT/"polynomial-855/polynomial-circuit.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CIRCUIT_SHA, "Parent circuit differs")
    obj = json.loads(raw)
    nodes, variables = obj["nodes"], obj["variables"]
    dependencies, factors, zero = [], [], []
    variable_nodes = {}
    for i,node in enumerate(nodes):
        op,*args = node
        children = args[:1] if op == "pow" else args if op in ("add","mul","neg") else []
        require(all(type(k) is int and 0 <= k < i for k in children), "Non-topological node")
        support = 1 << args[0] if op == "variable" else 0
        for k in children:
            support |= dependencies[k]
        dependencies.append(support)
        if op == "variable":
            variable_nodes[args[0]] = i
        if op == "int":
            ff, zz = {}, args[0] == 0
        elif op == "mul":
            ff = Counter()
            for k in args:
                ff.update(factors[k])
            ff,zz = dict(ff),any(zero[k] for k in args)
        elif op == "pow":
            ff = {k:e*args[1] for k,e in factors[args[0]].items()} if args[1] else {}
            zz = zero[args[0]] and args[1] != 0
        elif op == "neg":
            ff,zz = factors[args[0]],zero[args[0]]
        else:
            ff,zz = {i:1},False
        factors.append(ff);zero.append(zz)

    pole_mask = sum(1 << v["index"] for v in variables if v["category"] == "pole")
    removed = [g for g in obj["nonzero_numerators"] if dependencies[g] & pole_mask]
    retained = [g for g in obj["nonzero_numerators"] if not dependencies[g] & pole_mask]
    require(len(removed) == 42 and len(retained) == 1639, "Unexpected guard inventory")
    retained_factors = set().union(*(factors[g] for g in retained))
    require(len(retained_factors) == 1560, "Unexpected retained factor count")
    require(not set(removed) & retained_factors, "A removed guard remains as a factor")
    support = 0
    for g in retained:
        support |= dependencies[g]
    names = [v["name"] for v in variables if support >> v["index"] & 1]
    categories = dict(Counter(v["category"] for v in variables if support >> v["index"] & 1))
    require(categories == {"input":1,"point":633,"denominator":1,"contact":2},
            "Retained guard has unexpected dependencies")
    require(all(not(support >> v["index"] & 1) for v in variables
                if v["category"] in ("proxy","anchor","root approximation","pole","inverse")),
            "Retained guard depends on an excluded coordinate")

    by_label = {row["label"]:row for row in obj["rational_equations_before_clearing"]}
    blocks = []
    for g in removed:
        pole_vars = [v for v in variables if v["category"] == "pole" and dependencies[g] >> v["index"] & 1]
        require(len(pole_vars) == 1 and pole_vars[0]["name"].endswith(".t"), "Wrong pole dependency")
        tvar = pole_vars[0]
        prefix = tvar["name"][:-2]
        require(factors[g] == {g:1} and nodes[g][0] == "add" and len(nodes[g]) == 3,
                "Pole divisor is not one quadratic-sum atom")
        nonconstant = [k for k in nodes[g][1:] if dependencies[k] >> tvar["index"] & 1]
        constant = [k for k in nodes[g][1:] if not(dependencies[k] >> tvar["index"] & 1)]
        require(len(nonconstant) == len(constant) == 1, "Wrong delta numerator form")
        Q = constant[0]
        tnode = variable_nodes[tvar["index"]]
        require(factors[nonconstant[0]].get(tnode) == 2, "Delta is not quadratic in its t")
        require(all(k == tnode or not(dependencies[k] & pole_mask) for k in factors[nonconstant[0]]),
                "Unexpected pole dependence in delta coefficient")
        require(not zero[Q] and set(factors[Q]) <= retained_factors, "Delta denominator is unguarded")
        first, second = by_label[prefix+".first conic"],by_label[prefix+".second conic"]
        require(first["denominator"] == Q, "Delta denominator differs from first conic denominator")
        df = factors[second["denominator"]]
        require(df.get(g) == 4 and set(df)-retained_factors == {g},
                "Second-conic denominator does not have exactly delta^4 times retained factors")
        blocks.append({"label":prefix,"delta_numerator_node":g,"delta_denominator_node":Q,
                       "second_conic_delta_exponent":4})
    require(len({b["label"] for b in blocks}) == 42, "Repeated pole block")
    for row in by_label.values():
        if not row["label"].endswith(".second conic"):
            require(not zero[row["denominator"]] and set(factors[row["denominator"]]) <= retained_factors,
                    "A remaining equation has an unguarded denominator")

    receipt = {
        "status":"PASS",
        "generic_exact_polynomial_checks":generic_identities(),
        "parent_circuit_sha256":CIRCUIT_SHA,
        "removed_guards":len(removed),"retained_guards":len(retained),
        "retained_factors":len(retained_factors),
        "retained_guard_support_categories":categories,
        "guard_independent_of":["all three proxies","all three anchor coordinates","theta","all210 pole coordinates","old inverse"],
        "equations_with_only_retained_denominators":255,
        "pole_blocks":blocks,
        "retained_guard_numerator_nodes":retained,
        "retained_guard_factor_nodes":sorted(retained_factors),
        "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope":"Exact generic clearing identities and exact855 DAG support/factor checks. Uses the separately audited source-to-rational-pole formulas. Does not certify an853 polynomial artifact or the source arithmetic theorem."
    }
    target = ROOT/"pole-guard-removal-verification.json"
    target.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({k:receipt[k] for k in ("status","removed_guards","retained_guards","retained_factors","retained_guard_support_categories")}))


if __name__ == "__main__":
    main()
