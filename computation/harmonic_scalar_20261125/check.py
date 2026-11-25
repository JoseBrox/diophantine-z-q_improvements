"""Independent exact replay; no evaluation of the giant fixed parameter."""
from pathlib import Path
from collections import defaultdict
from hashlib import sha1
from itertools import combinations_with_replacement
import json

root = Path(__file__).resolve().parents[2]
here = Path(__file__).resolve().parent
k = 2**20
K = 3*2**15*211
for n, parent_path, pin, param, count, support, terms in [
    (162, "computation/bb_native_quartic_20261124/quartic163/quadrics.json",
     "0f85885f659374bef4b8af37a1835d00d70d7196", "C=211^N", 136, 2761, 2762),
    (177, "computation/weighted_explicit178_20261124/quadrics.json",
     "5f5dc81b80d46f93cd2018c93849c87e1ee83bc1", "C=211^(2^1600)", 149, 3004, 3005),
]:
    b = (root / parent_path).read_bytes()
    assert sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest() == pin
    parent = json.loads(b)
    new = json.loads((here / f"quartic{n}.json").read_text())
    assert new["variables"] == n and new["input"] == 1
    assert new["parameter"] == param
    assert len(new["residuals"]) == count
    def collect(row, renumber=False):
        d = defaultdict(int)
        for t in row["terms"]:
            m = t["monomial"]
            if renumber:
                assert 77 not in m
                m = [i-(i>77) for i in m]
            d[t["parameterPower"], tuple(sorted(m))] += int(t["coefficient"])
        return {p:c for p,c in d.items() if c}
    old = {row["name"]:row for row in parent["residuals"]}
    got = {row["name"]:collect(row) for row in new["residuals"]}
    assert len(got) == count
    changed = {"inputSquare.definition", "scalar.rPair1.definition",
        "scalar.four_contact_product.definition", "scalar.forced_prime.definition",
        "input.cleared.0", "input.cleared.1"}
    assert changed <= old.keys()
    # No overlooked use of either the eliminated or re-gauged coordinate.
    assert {r["name"] for r in parent["residuals"] if
            any(37 in t["monomial"] or 77 in t["monomial"]
                for t in r["terms"])} <= changed
    expected = {name:collect(row,True) for name,row in old.items()
                if name not in changed}
    expected["inputSquare.definition"] = {(0,(1,1)):1,(0,(37,)):-1}
    expected["scalar.harmonicA"] = {
        (0,(77,)):1, (0,()):-2401*343,
        (0,(37,)):-k*(2401*375+2400*343),
        (0,(37,37)):-k*k*2400*375}
    expected["scalar.harmonicR"] = {
        (0,(77,89)):1,(0,(89,)):1,(0,(37,89)):k,
        (2,(77,)):-K,(2,(37,77)):-K*k}
    for i in range(2):
        expected[f"input.cleared.{i}"] = {
            (0,(17+i,)):-1,(0,(23+i,)):1,
            (0,(37,116+i)):51,(0,(116+i,)):2504}
    assert got == expected
    all_vars = set()
    F = defaultdict(int)
    for row in got.values():
        for (e,m),c in row.items():
            assert e in (0,2) and len(m)<=2
            assert all(1<=v<=n for v in m)
            all_vars.update(m)
        for a,b in combinations_with_replacement(row.items(),2):
            (e,m),c=a; (f,j),d=b
            F[e+f,tuple(sorted(m+j))] += c*d*(1 if a==b else 2)
    F={p:c for p,c in F.items() if c}
    assert all_vars==set(range(1,n+1))
    assert len(F)==terms and len({m for e,m in F})==support
    assert max(len(m) for e,m in F)==4
    assert {(e,c) for (e,m),c in F.items() if m==(1,1,1,1)}=={(0,1)}
    print(n, count, support, terms, "OK")
assert k==1048576 and K==20742144
assert 2401*375-2400*343==3**2*5**2*7**3
assert 2401-2400==1 and 343-375==-32
for x in range(211):
    s=k*x*x %211
    A=(2401+2400*s)*(343+375*s)%211
    B=(1+s)%211
    assert A*B*(A+B)%211 != 0
assert (2401*343+1)%64==56
assert 2401*343%8==7 and 3*211%8==1
assert 9792==64*153 and 153%8==1
assert 4801*718*2<2**23
assert 211**2<2**16 and 7**2*4<2**8
assert 262*6+8000<1600*6
assert 6*(262+4)<1600
print("scalar arithmetic OK")
