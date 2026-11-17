#!/usr/bin/env python3
"""Rebuild all contact equations for reflection center 3/11."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
from math import lcm, gcd
import json
from build_base import build_base

R=Path(__file__).resolve().parent


def dump(name,obj):
    (R/name).write_text(json.dumps(obj,indent=2)+'\n')


def add(*polys):
    result=defaultdict(F)
    for p in polys:
        for m,c in p.items():result[m]+=c
    return {m:c for m,c in result.items() if c}


def times(a,b):
    result=defaultdict(F)
    for (u,m),c in a.items():
        for (v,n),d in b.items():result[(u+v,tuple(sorted(m+n)))]+=c*d
    return {m:c for m,c in result.items() if c}


def scale(p,c):return {m:c*v for m,v in p.items() if c*v}
def var(i,power=0):return {(power,(i,)):F(1)}
def parse(row):return {(t['parameterPower'],tuple(t['monomial'])):F(t['coefficient']) for t in row['terms']}
def serial(p):return [dict(parameterPower=u,monomial=list(m),coefficient=str(c)) for (u,m),c in sorted(p.items()) if c]


def main():
    source,graft=build_base()
    raw=(R/'source/quadratic195.json').read_bytes()
    theta=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
    center=F(3,11); midpoint=center/2
    a,b=midpoint.numerator,midpoint.denominator
    roots=[(b*t-a)**2 for t in theta]
    elementary=[F(1)]+[F(0)]*5
    for root in roots:
        for j in range(5,0,-1):elementary[j]+=root*elementary[j-1]
    L=lcm(*(e.denominator for e in elementary))
    e=[int(L*v) for v in elementary]
    table=source
    table['format']='three-detector-quartic229-reflection3over11/v62'
    rows={r['name']:r for r in table['residuals']}
    q=var(77)
    changes=[]
    for j,(ti,ri,si,vi,wi) in enumerate([(2,74,75,76,None),(86,87,88,89,91),(200,201,202,203,205)]):
        t,r,s,v=var(ti),var(ri),var(si),var(vi,1 if j==0 else 0)
        w={(0,()):F(1)} if wi is None else var(wi)
        qw=add(q,w)
        h=add(scale(t,b),scale(q,-a))
        square=add(times(h,h),scale(times(q,r),-1))
        combination=add(scale(times(r,s),L),scale(times(s,qw),-e[1]),
                        scale(times(r,qw),e[2]),scale(times(q,v),-1))
        relation=add(times(s,v),scale(times(s,qw),-e[3]),
                     scale(times(r,qw),e[4]),scale(times(q,qw),-e[5]))
        if j:relation=scale(relation,-1)
        for suffix,p in [('contactSquare',square),('contactCombination',combination),('contactRelation',relation)]:
            row=rows[f'additive.detector{j}.{suffix}']
            row['terms']=serial(p);changes.append(row['id'])
    assert len(changes)==9
    expanded=defaultdict(F)
    for row in table['residuals']:
        p=parse(row)
        assert all(len(m)<=2 and c.denominator==1 for (u,m),c in p.items())
        for key,c in times(p,p).items():expanded[key]+=c
    expanded={m:c for m,c in expanded.items() if c}
    profiles=defaultdict(dict)
    for (a,m),c in expanded.items():profiles[m][a]=int(c)
    assert gcd(*(int(c) for c in expanded.values()))==1
    assert max(len(m) for a,m in expanded)==4
    assert {i for a,m in expanded for i in m}==set(range(1,230))
    K=max(abs(p.get(0,0)) for p in profiles.values())
    assert {0:K} in profiles.values() or {0:-K} in profiles.values()
    crossover=next(n for n in range(1,100) if 22201*149**(2*n)>K)
    report=dict(schema='reflection-center-change/v62',source_sha256=sha256(raw).hexdigest(),
                center=str(center),midpoint=str(midpoint),contact_numerator=f'({b}t-{midpoint.numerator})^10',
                theta=list(map(str,theta)),paired_constants=list(map(str,roots)),
                common_denominator=L,scaled_elementary_coefficients=e,
                changed_rows=sorted(changes),variables=229,quadratic_rows=207,
                degree=4,content=1,coordinate_monomials=len(profiles),parameter_terms=len(expanded),
                expected_coefficient_height=f'max({K},149^(2*N+2))',expected_crossover=crossover,
                arithmetic_status='The center-3/11 arithmetic theorem proves the sufficient threshold N>=15 under retained premises.')
    dump('quadratic.json',table)
    dump('polynomial.json',dict(format='sum-of-207-quadratic-squares-reflection3over11/v62',variables=229,
        degree=4,inputCoordinate=1,fixedParameter=table['fixedParameter'],terms=serial(expanded)))
    dump('contact-change.json',report)
    dump('graft.json',graft)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
