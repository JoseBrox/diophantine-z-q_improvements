"""Two fixed-weak-abc quartic specifications, built from the verified 62-coordinate chart."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
from math import gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[2]/"abc/shared/record62"

def term(a, *xs, b=0):
    return (b,tuple(sorted(xs))),a

def parse(items):
    return {(r["parameterPower"],tuple(r["monomial"])):int(r["coefficient"]) for r in items}

def serialize(p):
    return [{"parameterPower":b,"monomial":m,"coefficient":str(a)} for (b,m),a in sorted(p.items()) if a]

def contacts(t,e,f,w):
    invc=62
    return [dict((term(1,t,e),term(-1,invc,invc))),
            dict((term(1,f,invc),term(-1,e,e))),
            dict((term(70,w,invc),term(-70,t,t),term(-239,t,invc),term(-170,invc,invc),
                  term(150,e,invc),term(230,f,invc),term(89,e,f),term(10,f,f)))]

def build(source,flavor):
    base=json.loads(source.read_text())
    residuals={r["name"]:parse(r["terms"]) for r in base["residuals"]}
    for i,(t,e,f,w) in enumerate(((2,33,34,35),(32,47,48,49))):
        for name,p in zip(("contactSquare","contactSum","inverseContact"),contacts(t,e,f,w)):
            residuals[f"detector{i}."+name]=p
    residuals["height.betaEighth"]=dict((term(1,63),term(-1,31,31)))
    power=63
    if flavor=="weak":
        residuals["height.betaSixteenth"]=dict((term(1,64),term(-1,63,63)))
        power=64
    argument=residuals["detector1.argument"]
    assert argument.pop((0,(31,31)))==1
    argument[(0,(power,power))]=1
    expanded=Counter()
    for pol in residuals.values():
        for ((b,m),v),((c,n),w) in product(pol.items(),repeat=2):
            expanded[b+c,tuple(sorted(m+n))]+=v*w
    expanded={t:v for t,v in expanded.items() if v}
    common=gcd(*expanded.values())
    assert common==1
    support=defaultdict(dict)
    for (b,m),v in expanded.items():
        support[m][b]=v
    height_fixed=max(abs(v[0]) for v in support.values() if set(v)=={0})
    mixed={str(m):p for m,p in support.items() if max(p)>0}
    fixedgcd=gcd(*(p[0] for p in support.values() if set(p)=={0}))
    assert fixedgcd==1
    n=power
    assert set(x for m in support for x in m)==set(range(1,n+1))
    out=dict(variables=n,residuals=[dict(name=name,terms=serialize(p)) for name,p in residuals.items()])
    return (out,dict(variables=n,terms=serialize(expanded)),
            dict(variables=n,rows=len(residuals),degree=max(map(len,support)),monomials=len(support),
                 constantHeight=height_fixed,parameterProfiles=mixed,fixedCoefficientGcd=fixedgcd))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent",type=Path,default=BASE/"quadrics.json")
    parser.add_argument("--output",type=Path,default=HERE)
    args=parser.parse_args()
    for flavor in ("weak","strong"):
        folder=args.output/flavor
        folder.mkdir(exist_ok=True,parents=True)
        rows,quartic,summary=build(args.parent,flavor)
        for n,rec in (("quadrics",rows),("polynomial",quartic),("summary",summary)):
            (folder/(n+".json")).write_text(json.dumps(rec,separators=(",",":"))+"\n")
        print(flavor,summary)
