#!/usr/bin/env python3
"""Exact coefficient-dependent ASCII budget, independent of the producer."""
from pathlib import Path
from collections import defaultdict, Counter
import json

source = Path(__file__).with_name("quartic161.json")
data = json.loads(source.read_text())
assert data["variables"] == 161 and len(data["residuals"]) == 135
profiles = defaultdict(Counter)
for row in data["residuals"]:
    for a in row["terms"]:
        for b in row["terms"]:
            m = tuple(sorted(a["monomial"] + b["monomial"]))
            profiles[m][a["parameterPower"] + b["parameterPower"]] += (
                int(a["coefficient"]) * int(b["coefficient"]))
profiles = {m: {k:v for k,v in c.items() if v} for m,c in profiles.items()}
profiles = {m:c for m,c in profiles.items() if c}
assert len(profiles) == 2858
dep = {m:c for m,c in profiles.items() if max(c)>0}
assert len(dep) == 17
# Every nonconstant profile has only a leading power and possibly
# a constant. Its absolute value is >1 and increasing for C>=331.
for m,c in dep.items():
    k=max(c)
    assert k in (2,4) and set(c) <= {0,k}
    assert abs(c[k])*331**k > abs(c.get(0,0))+1
assert profiles[()][max(profiles[()])] > 0

def size(N):
    C=331**N
    coeff={m:sum(a*C**k for k,a in p.items()) for m,p in profiles.items()}
    assert all(coeff.values())
    def term(m,c,first):
        v="*".join("x"+str(i)+("^"+str(m.count(i)) if m.count(i)>1 else "")
                   for i in sorted(set(m)))
        return ("-" if c<0 else "" if first else "+")+(
            "" if abs(c)==1 and v else str(abs(c))+("*" if v else ""))+v
    return len("".join(term(m,c,i==0) for i,(m,c) in enumerate(sorted(coeff.items()))).encode("ascii"))
for N,n in [(1,63078),(25,66222),(282,99902),(283,100033),(1000,193982)]:
    assert size(N)==n, (N,size(N))
    print(N,n)
# Verify the precise numerical budget for the conditional height target.
assert 9*(2*282+1)//4+1==1272
assert 331**1272>2**10176
# The declared exception set for the smaller-radical contact estimate.
from fractions import Fraction as Q
from math import prod
theta=[Q(0),Q(-1,2),Q(-1),Q(1,2399),Q(-32,407)]
roots=theta+[2-x for x in theta]
G=[2,3,5,7,11,13,17,37,41,47,67,109,179,257,439,2099,2399,2029147]
J=prod(G)
assert J==54852429049017820832107412529142530
assert J<2**116
def supported(n):
    n=abs(n)
    assert n
    for p in G:
        while n%p==0:n//=p
    return n==1
for i,t in enumerate(roots):
    assert supported(t.denominator) and supported((t-1).numerator)
    for v in roots[:i]:assert supported((t-v).numerator)
print("All exact budget and support checks passed.")
