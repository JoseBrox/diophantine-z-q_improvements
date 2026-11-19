"""Independent symbolic checks of the two fixed-weak-abc quartics."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from collections import defaultdict
from math import gcd
import argparse, json
import sympy as s
HERE=Path(__file__).resolve().parent
def terms(row):
    return {(r["parameterPower"],tuple(r["monomial"])):int(r["coefficient"]) for r in row}
def read_rows(p):
    return {r["name"]:terms(r["terms"]) for r in json.loads(p.read_text())["residuals"]}
def sympoly(x,p,B):
    return sum(v*B**b*s.prod(x[i] for i in m) for (b,m),v in p.items())
def verify(base,folder,weak):
    rows=read_rows(folder/"quadrics.json")
    pp=terms(json.loads((folder/"polynomial.json").read_text())["terms"])
    n=64 if weak else 63
    x=[None]+list(s.symbols("x1:"+str(n+1)))
    B=s.Symbol("B"); T=s.Symbol("t"); R=s.Symbol("r")
    theta=[-2,-1,-F(5,7),-F(1,2),-F(1,5),1]
    positions={(-1,2),(-2,1),(0,1),(1,1),(-1,1),(1,0)}
    im=[(5*s.Rational(t)+1,2*s.Rational(t)+4) for t in theta]
    assert {(int((a/b).p),int((a/b).q)) if b else (1,0) for a,b in im}==positions
    G=s.prod(T-r for r in theta).expand()
    allowed={"detector1.argument"}|{f"detector{i}.{name}" for i in range(2) for name in ("contactSquare","contactSum","inverseContact")}
    assert all(rows[k]==r for k,r in base.items() if k not in allowed)
    assert set(rows)-set(base)==({"height.betaEighth","height.betaSixteenth"} if weak else {"height.betaEighth"})
    assert sympoly(x,rows["height.betaEighth"],B)==x[63]-x[31]**2
    if weak:assert sympoly(x,rows["height.betaSixteenth"],B)==x[64]-x[63]**2
    transformed_gap=B+4*x[9]**2+x[n]**2+(x[2]-x[32])*x[61]
    assert s.expand(sympoly(x,rows["detector1.argument"],B)-transformed_gap)==0
    for i,(j,e,f,w) in enumerate(((2,33,34,35),(32,47,48,49))):
        d=f"detector{i}."; C=s.Symbol("c",nonzero=True)
        U,E,H,W=s.symbols("u e h w")
        substitution={x[j]:U/C,x[e]:E/C,x[f]:H/C,x[w]:W/C,x[62]:1/C}
        one,two,three=(s.cancel(C**2*sympoly(x,rows[d+k],B).subs(substitution)) for k in ("contactSquare","contactSum","inverseContact"))
        assert one==U*E-1 and two==H-E**2
        assert s.cancel(three.subs({U:T,E:1/T,H:1/T**2})-70*(W-G/T**4))==0
    sos=defaultdict(int)
    for r in rows.values():
        for (b,m),co in r.items():
            assert len(m)<=2
            for (bb,mm),v in r.items():sos[b+bb,tuple(sorted(m+mm))]+=co*v
    assert {k:v for k,v in sos.items() if v}==pp
    profiles=defaultdict(dict)
    for (b,m),v in pp.items():profiles[m][b]=v
    assert len(rows)==n-12 and len(profiles)==(856 if weak else 853)
    assert max(map(len,profiles))==4 and set(i for m in profiles for i in m)==set(range(1,n+1))
    const=[p[0] for p in profiles.values() if set(p)=={0}]
    assert gcd(*const)==1 and max(map(abs,const))==109940
    assert sorted(tuple(p.get(i,0) for i in range(3)) for p in profiles.values() if max(p)>0)==sorted([(4091,0,1),(1,8,0),(1,2,0),(0,-2,0),(0,2,0)])
    k,d=(F(121,100),32) if weak else (F(16,15),16)
    strict=4*(2*k-1)/(d-k*(d//2+2))/(8/k-6)
    assert strict==(F(17182,18907) if weak else F(17,30)) and strict<1
    return {"variables":n,"quadrics":len(rows),"monomials":len(profiles),"strict":str(strict),"height":"max(109940,B²+4091)","content":1}
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parent",type=Path,default=HERE.parents[2]/"abc/shared/record62/quadrics.json")
    args=p.parse_args();base=read_rows(args.parent)
    print(json.dumps({f:verify(base,HERE/f,f=="weak") for f in ("weak","strong")},indent=2))
