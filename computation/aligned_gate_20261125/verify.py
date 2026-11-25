"""Exact independent replay of the aligned-gate reductions."""
import hashlib
import json
import re
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def read(path):
    return json.loads(path.read_text())

def clean(p):
    return {k: v for k, v in p.items() if v}

def add(a, b):
    p = defaultdict(Q, a)
    for k, v in b.items():
        p[k] += v
    return clean(p)

def mul(a, b):
    p = defaultdict(Q)
    for (l, e, m), v in a.items():
        for (k, f, n), w in b.items():
            p[l+k, e+f, tuple(sorted(m+n))] += v*w
    return clean(p)

def mon(l, e, m, a=1):
    return clean({(l, e, tuple(m)): Q(a)})

def proportional(a, b):
    if not a or a.keys() != b.keys():
        return False
    k = next(iter(a))
    return all(a[j]*b[k] == b[j]*a[k] for j in a)

def check(n):
    z = read(HERE/f"certificate{n}.json")
    p = z["config"]
    parent = ROOT/"computation/depressed_scalar_20261125"/f"quartic{p['n']}.json"
    raw = parent.read_bytes()
    blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    assert blob == z["parent"], blob
    a, b = json.loads(raw), read(HERE/f"quartic{n}.json")
    assert b["variables"] == z["variables"] == n
    assert a["parameter"] == b["parameter"]
    keep = [j for j in range(1,p["n"]+1) if j not in p["drop"]]
    idx = {j:i for i,j in enumerate(keep,1)}

    def unit(j):
        if j == p["c"]: return mon(-1,0,[])
        if j == p["u"]: return mon(1,0,[])
        if j == p["v"]: return mon(2,0,[])
        return mon(0,0,[j])

    def sub(j):
        if str(j) not in z["substitutions"]:
            return unit(j)
        result = {}
        for e, m, num, den in z["substitutions"][str(j)]:
            assert e == 0 and len(m) <= 1
            result = add(result, mul(mon(0,0,[],Q(num)/Q(den)), unit(m[0]) if m else mon(0,0,[])))
        return result

    def embed(row, old):
        result = {}
        for t in row["terms"]:
            q = mon(-p["exps"].get(row["name"],0) if old else 0,
                    t["parameterPower"], [], int(t["coefficient"]))
            for i in t["monomial"]:
                j = i if old else keep[i-1]
                s = mul(mon(p["chg"].get(str(j),0),0,[]),sub(j)) if old else unit(j)
                q = mul(q,s)
            result = add(result,q)
        return result

    by = {row["name"]:row for row in b["residuals"]}
    assert len(by) == len(b["residuals"]) == z["rows"]
    guards = {"unit.c_inverse","unit.c_inverse_square"}
    removed = []
    for row in a["residuals"]:
        name = row["name"]
        if name in guards:
            assert by[name]["terms"] == [
                dict(t,monomial=[idx[j] for j in t["monomial"]]) for t in row["terms"]]
        elif name in by:
            assert proportional(embed(row,True),embed(by[name],False)), name
        else:
            removed.append(name)
            assert proportional(embed(row,True),embed(by["shared.gate0"],False)), name
    assert len(removed) == len(p["drop"])
    assert set(by) == {r["name"] for r in a["residuals"]} - set(removed)

    used, total = set(), {}
    for row in b["residuals"]:
        assert row["terms"]
        q = {}
        for t in row["terms"]:
            assert len(t["monomial"]) <= 2
            used.update(t["monomial"])
            q = add(q, mon(0,t["parameterPower"],t["monomial"],int(t["coefficient"])))
        total = add(total,mul(q,q))
    assert used == set(range(1,n+1))
    assert len(total) == z["symbolicTerms"]
    assert len({m for _,_,m in total}) == z["profiles"]
    fixed = defaultdict(Q)
    for (l,e,m),v in total.items():
        assert l == 0
        fixed[m] += v*(331**26)**e
    fixed = clean(fixed)
    assert len(fixed) == z["N26Monomials"]
    assert all(v.denominator == 1 for v in fixed.values())
    assert max(abs(int(v)).bit_length() for v in fixed.values()) == z["N26HeightBits"]
    assert fixed[(1,1,1,1)] == 1
    assert max(map(len,fixed)) == 4
    if n == 175:
        raw = (HERE/"expanded175.txt").read_bytes()
        assert len(raw) == z["expandedBytes"]
        s = raw.decode("ascii")
        assert "\n" not in s and " " not in s
        expanded = {}
        for token in re.findall(r"[+-]?[^+-]+", s):
            sign = -1 if token.startswith("-") else 1
            parts = token.lstrip("+-").split("*")
            coefficient = sign*(int(parts.pop(0)) if parts[0].isdigit() else 1)
            m = []
            for part in parts:
                match = re.fullmatch(r"x(\d+)(?:\^(\d+))?",part)
                assert match, part
                m.extend([int(match[1])]*int(match[2] or 1))
            key = tuple(sorted(m))
            assert key not in expanded
            expanded[key] = coefficient
        assert expanded == fixed
    print(f"{n}: {len(a['residuals'])} parent equations, {len(removed)} eliminated gates; "
          f"{len(by)} quadratics, {len(fixed)} specialized monomials, exact replay passed")

if __name__ == "__main__":
    for n in (161,175):
        check(n)
