"""Exact coordinate, finite-algebra-rank and separating-menu census."""
from math import comb
import json
from pathlib import Path
c=json.loads(Path(__file__).with_name("certificate.json").read_text())
for x in c["checks"]:
    k=x["k"]
    n=2**(4*k+2)
    assert int(x["rank"])==n
    assert k+(2*k+2)+4*k+1==x["new"]==7*k+3
    assert x["old"]==10*k
    assert x["old"]-x["new"]==3*(k-1)
    assert (4*k+1)*comb(n,2)+1>0
    print(k,x["new"],n)
print("PASS: census only; arithmetic and joint-density proof in README.md")
