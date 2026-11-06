"""Sparse integer polynomial operations used by the untrusted search only."""
import math

def poly_add(dst, src, scale=1):
    for m,c in src.items():
        value=dst.get(m,0)+scale*c
        if value: dst[m]=value
        else: dst.pop(m,None)

def product(a,b):
    result={}
    for m,c in a.items():
        for n,d in b.items():
            key=tuple(sorted(m+n))
            result[key]=result.get(key,0)+c*d
    return {m:c for m,c in result.items() if c}

def square(a):
    result={}; terms=list(a.items())
    for i,(m,c) in enumerate(terms):
        for j in range(i,len(terms)):
            n,d=terms[j]; key=tuple(sorted(m+n))
            result[key]=result.get(key,0)+(1 if i==j else 2)*c*d
    return {m:c for m,c in result.items() if c}

def primitive(row):
    divisor=math.gcd(*row.values())
    if row[min(row)]<0: divisor=-divisor
    return tuple(sorted((m,c//divisor) for m,c in row.items()))

def vars_in(row): return {v for m in row for v in m}
