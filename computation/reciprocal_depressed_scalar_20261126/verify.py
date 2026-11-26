#!/usr/bin/env python3
"""Independent exact reconstruction of the reciprocal cubic tables."""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
from math import gcd
from functools import reduce
import hashlib, json, re
here=Path(__file__).resolve().parent
cert=json.loads((here/"certificate.json").read_text())
def add(*ps):
    out=defaultdict(int)
    for p in ps:
        for m,c in p.items():out[m]+=c
    return {m:c for m,c in out.items() if c}
def scale(p,k):return {m:c*k for m,c in p.items() if c*k}
def mul(p,q):
    out=defaultdict(int)
    for (e,m),a in p.items():
        for (f,n),b in q.items():out[e+f,tuple(sorted(m+n))]+=a*b
    return {m:c for m,c in out.items() if c}
def atom(i):return {(0,(i,)):1}
def con(c,power=0):return {(power,()):c}
def row(r):return add(*[{(t["parameterPower"],tuple(t["monomial"])):int(t["coefficient"])} for t in r["terms"]])
W=add(scale(atom(37),36000*2**20),con(34981))
T=atom(76);R=atom(88);K=con(18536,2);V=add(R,scale(K,-1))
alpha=900000;gamma=Fraction(-1053721,480);e=Fraction(-1081567619,25920000)
assert gamma*36000**2/alpha==-3161163
assert e*36000**3/alpha==-2163135238
expect={
 "scalar.depressed.reciprocal":add(mul(W,T),con(-1)),
 "scalar.depressed.linearized":add(mul(add(W,scale(T,-3161163)),V),scale(mul(K,mul(T,T)),2163135238))
}
assert 9*(2*25+1)//4+1==115 and 331**115>2**960
for rec in cert["records"]:
    n=rec["n"]
    oldpath=here.parent/"aligned_gate_20261125"/f"quartic{n}.json"
    raw=oldpath.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==rec["parentBlob"]
    old=json.loads(raw);new=json.loads((here/f"quartic{n}.json").read_text())
    assert new["variables"]==old["variables"]==n
    oldr=[r for r in old["residuals"] if r["name"] not in ("scalar.depressed.first","scalar.depressed.second")]
    newr=[r for r in new["residuals"] if r["name"] not in expect]
    assert oldr==newr
    assert all(76 not in t["monomial"] for r in oldr for t in r["terms"])
    assert {r["name"]:row(r) for r in new["residuals"] if r["name"] in expect}==expect
    assert len(new["residuals"])==rec["rows"]
    assert all(len(t["monomial"])<=2 for r in new["residuals"] for t in r["terms"])
    assert set(i for r in new["residuals"] for t in r["terms"] for i in t["monomial"])==set(range(1,n+1))
    sym=add(*(mul(row(r),row(r)) for r in new["residuals"]))
    assert len(sym)==rec["symbolicTerms"]
    C=331**25
    p=defaultdict(int)
    for (k,m),a in sym.items():p[m]+=a*C**k
    p={m:c for m,c in p.items() if c}
    assert len(p)==rec["monomials"] and max(map(len,p))==4
    H=max(abs(a) for a in p.values())
    assert H.bit_length()==rec["coefficientBits"] and len(str(H))==rec["decimalDigits"]
    assert p[(1,1,1,1)]==1 and reduce(gcd,p.values())==1
    def term(m,c,first):
        v="*".join("x"+str(i)+("^"+str(m.count(i)) if m.count(i)>1 else "") for i in sorted(set(m)))
        return ("-" if c<0 else "" if first else "+")+("" if abs(c)==1 and v else str(abs(c))+("*" if v else ""))+v
    s="".join(term(m,c,i==0) for i,(m,c) in enumerate(sorted(p.items())))
    assert len(s.encode("ascii"))==rec["expandedBytes"]<100000
    if n==175:
        raw=(here/"expanded175.txt").read_bytes()
        assert raw==s.encode("ascii")
        out={}
        for tok in re.findall(r"[+-]?[^+-]+",raw.decode("ascii")):
            sig=-1 if tok[0]=="-" else 1
            parts=tok.lstrip("+-").split("*")
            a=int(parts.pop(0)) if parts[0].isdigit() else 1
            m=[]
            for v in parts:
                q=re.fullmatch(r"x(\d+)(?:\^(\d+))?",v)
                assert q
                m.extend([int(q[1])]*int(q[2] or 1))
            assert tuple(m) not in out
            out[tuple(m)]=sig*a
        assert p==out
    print(n, "PASS", rec)
