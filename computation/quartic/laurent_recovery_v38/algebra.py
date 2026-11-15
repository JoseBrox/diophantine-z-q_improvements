#!/usr/bin/env python3
"""Exact sparse-polynomial and Laurent arithmetic used only by the producer."""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import gcd,lcm

def require(ok,message):
    if not ok:raise ValueError(message)
def parse(terms):
    out=defaultdict(Q)
    for t in terms:out[int(t['parameterPower']),tuple(sorted(t['monomial']))]+=Q(t['coefficient'])
    return {k:c for k,c in out.items() if c}
def serial(poly):return [dict(parameterPower=a,monomial=list(m),coefficient=str(c)) for (a,m),c in sorted(poly.items()) if c]
def primitive(poly):
    p={k:Q(c) for k,c in poly.items() if c};require(bool(p),'zero row')
    den=lcm(*(c.denominator for c in p.values()));g=gcd(*(abs(int(den*c)) for c in p.values()))
    if p[min(p)]<0:g=-g
    factor=Q(den,g);return {k:c*factor for k,c in p.items()},factor

def expand(poly,powers,weights,constants):
    dim=len(next(iter(powers.values())));out=defaultdict(Q)
    for (a,m),value in poly.items():
        e=[0]*dim;plain=[]
        for i in m:
            value*=constants.get(i,Q(1))
            if i not in powers:plain.append(i)
            for j,k in enumerate(powers.get(i,weights.get(i,[0]*dim))):e[j]+=k
        out[a,tuple(sorted(plain)),tuple(e)]+=value
    return {k:c for k,c in out.items() if c}

def representatives(powers,deleted):
    ids=sorted(set(powers)-set(deleted));dim=len(next(iter(powers.values())));answer={}
    for cap in range(3):
        opts={}
        for degree in range(cap+1):
            for m in combinations_with_replacement(ids,degree):
                e=tuple(sum(powers[i][j] for i in m) for j in range(dim))
                if e not in opts or (len(m),m)<(len(opts[e]),opts[e]):opts[e]=m
        answer[cap]=opts
    return answer

def convert(source,config):
    powers={int(k):tuple(v) for k,v in config['powers'].items()};weights={int(k):tuple(v) for k,v in config['weights'].items()};constants={int(k):Q(v) for k,v in config['constants'].items()}
    deleted=set(config['deleted_coordinates']);deleted_rows=set(config['deleted_rows']);zero=(0,)*len(next(iter(powers.values())))
    active=[c for c in source['coordinates'] if c['id'] not in deleted];rename={c['id']:i+1 for i,c in enumerate(active)}
    options=representatives(powers,deleted);rows=[];cert=[]
    for row in source['residuals']:
        p=parse(row['terms'])
        if row['name'] in deleted_rows:
            require(not expand(p,powers,weights,constants),'deleted equation is not an identity: '+row['name']);continue
        changed=any(i in weights or i in constants or i in deleted for a,m in p for i in m)
        if changed:
            lp=expand(p,powers,weights,constants);shifts=None
            for (a,m,e),c in lp.items():
                require(len(m)<=2,'plain degree >2')
                valid={tuple(x-y for x,y in zip(e,s)) for s in options[2-len(m)]};shifts=valid if shifts is None else shifts&valid
            require(bool(shifts),'no quadratic representative: '+row['name'])
            shift=min(shifts,key=lambda s:(sum(abs(x) for x in s),s));new=defaultdict(Q)
            for (a,m,e),c in lp.items():
                rest=tuple(x-y for x,y in zip(e,shift));new[a,tuple(sorted(m+options[2-len(m)][rest]))]+=c
            new,factor=primitive(new)
        else:new,factor=primitive(p);shift=zero
        require(all(not set(m)&deleted and len(m)<=2 for a,m in new),'invalid target row')
        target={(a,tuple(sorted(rename[i] for i in m))):c for (a,m),c in new.items()}
        rows.append(dict(id=len(rows)+1,name=row['name'],terms=serial(target)))
        cert.append(dict(source_row=row['id'],target_row=len(rows),division_exponents=list(shift),primitive_multiplier=str(factor)))
    coords=[dict(id=rename[c['id']],name=c['name'],parent_id=c['id']) for c in active]
    system=dict(format='exact-laurent-reduction/v38',variables=len(coords),inputCoordinate=rename[source['inputCoordinate']],fixedParameter=source['fixedParameter'],coordinates=coords,residuals=rows)
    certificate=dict(config,old_to_new={str(i):j for i,j in rename.items()},rows=cert)
    return system,certificate

def sum_squares(system):
    full=defaultdict(Q)
    for row in system['residuals']:
        p=parse(row['terms'])
        for (a,m),c in p.items():
            for (b,n),d in p.items():full[a+b,tuple(sorted(m+n))]+=c*d
    full={k:c for k,c in full.items() if c}
    poly=dict(format='integer-quartic/v38',variables=system['variables'],degree=4,inputCoordinate=system['inputCoordinate'],fixedParameter=system['fixedParameter'],coordinates=system['coordinates'],terms=serial(full))
    return poly
