#!/usr/bin/env python3
"""Exact small-algebra checks for the separating-element elimination theorem."""
from __future__ import annotations
from itertools import permutations
from fractions import Fraction
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json
import sys
sys.set_int_max_str_digits(0)

def add(a,b):return [x+y for x,y in zip(a,b)]
def scale(c,a):return [c*x for x in a]
def bmul(a,c,k):return [a[0]*c[0]+k*a[1]*c[1],a[0]*c[1]+a[1]*c[0]]
def amul(a,b,k,rad):
    lo=add(bmul(a[:2],b[:2],k),bmul(bmul(a[2:],b[2:],k),rad,k))
    hi=add(bmul(a[:2],b[2:],k),bmul(a[2:],b[:2],k))
    return lo+hi
def mat(a,k,rad):
    columns=[amul(a,[int(i==j) for i in range(4)],k,rad) for j in range(4)]
    return [list(row) for row in zip(*columns)]
def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c
def padd(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return c
def detpoly(M):
    n=len(M);out=[0]*(n+1)
    for perm in permutations(range(n)):
        inv=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=[(-1)**inv]
        for i,j in enumerate(perm):term=pmul(term,[int(i==j),-M[i][j]])
        out=padd(out,term)
    return out
def charnewton(M):
    n=len(M);power=[[int(i==j) for j in range(n)] for i in range(n)]
    traces=[0];coeff=[1]
    for k in range(1,n+1):
        power=[[sum(power[i][h]*M[h][j] for h in range(n)) for j in range(n)] for i in range(n)]
        traces.append(sum(power[i][i] for i in range(n)))
        val=-sum(coeff[k-j]*traces[j] for j in range(1,k+1))
        assert val%k==0
        coeff.append(val//k)
    return coeff
def norm(a,k):return a[0]**2-k*a[1]**2
def square(q):return q>=0 and isqrt(q)**2==q
def phash(p):return hashlib.sha256(json.dumps(p,separators=(',',':')).encode()).hexdigest()

def squarefree(p):
    a=list(map(Fraction,p))
    while a and not a[-1]:a.pop()
    b=[j*a[j] for j in range(1,len(a))]
    while b:
        rem=list(a)
        while len(rem)>=len(b):
            scale=rem[-1]/b[-1];offset=len(rem)-len(b)
            for i,x in enumerate(b):rem[i+offset]-=scale*x
            while rem and not rem[-1]:rem.pop()
        a,b=b,rem
    return len(a)==1

def run_case(name,k,rad,g,expected):
    T=bmul(bmul(g,g,k),rad,k); aa=[1,-2*T[0],norm(T,k)]
    r0=max([j for j in (1,2) if aa[j]]+[0])
    generators=[[0,1,0,0],[0,0,1,0]]
    mg=[[g[0],k*g[1]],[g[1],g[0]]]
    R=4*(1+sum(v*v for gen in generators for row in mat(gen,k,rad) for v in row)+sum(v*v for row in mg for v in row))
    rows=[];correct=None
    for r in (1,2):
        c=aa[r];h=[1,0]
        for j in range(1,r+1):h=add(bmul(h,T,k),[aa[j],0])
        E=add([c,0],scale(-1,h))
        D=c*c*(4*k)**2
        K=(2*R)**(2*r+2)*(1+c*c)*(1+(4*k)**2)
        C=D+4*R*K
        unscaled=[C*C,D*C,D*D,0]
        beta=scale(D,amul(E+[0,0],unscaled,k,rad))
        M=mat(beta,k,rad);H=detpoly(M)
        assert H==charnewton(M)
        if not c or not D:assert H==[1,0,0,0,0]
        active_count=0; rational=False
        if r==r0:
            assert c and D and bmul(E,E,k)==scale(c,E)
            assert squarefree(H)
            if k==1:
                product=[1]
                for z in (-1,1):
                    ev=E[0]+z*E[1];tt=T[0]+z*T[1]
                    assert ev==(c if tt else 0)
                    u=beta[0]+z*beta[1];v=beta[2]+z*beta[3]
                    cr=rad[0]+z*rad[1]
                    if tt:
                        assert cr and v
                        active_count+=2
                        rational|=square(cr)
                        factor=[1,-2*u,u*u-cr*v*v]
                        assert factor[2]
                    else:
                        assert u==v==0
                        factor=[1]
                    product=pmul(product,factor)
                assert H==product+[0]*(5-len(product))
            else:
                assert k==2 and rad==[1,0] and g==[1,0]
                product=[1]
                for q in (-1,1):
                    u=beta[0]+q*beta[2];v=beta[1]+q*beta[3]
                    assert v # each factor is irreducible over Q
                    product=pmul(product,[1,-2*u,u*u-2*v*v])
                assert H==product
                active_count=4;rational=False
            assert rational==expected
            correct={'degree':active_count,'rational_character':rational}
        elif not aa[r]:
            assert H==[1,0,0,0,0]
        else:
            assert any(aa[j] for j in range(r+1,3))
        rows.append({'case':r,'c_nonzero':bool(c),'D_nonzero':bool(D),
            'H_sha256':phash(H),'largest_H_coefficient_bit_length':max(abs(x).bit_length() for x in H)})
    if not r0:
        assert not expected
        correct={'degree':0,'rational_character':False}
    return {'name':name,'point_relation_z2':k,'pole_radicand':rad,'guard_factor':g,
            'actual_degree_case':r0,'correct_case':correct,'cases':rows}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    examples=[
        ('split base, one rational and one irrational pole fiber',1,[2,1],[1,0],True),
        ('one excluded point branch',1,[2,1],[-1,1],True),
        ('inactive nonreduced fiber and irrational active fiber',1,[1,1],[1,0],False),
        ('repeated nonzero T eigenvalues',1,[1,0],[1,0],True),
        ('nonreal active quadratic fiber and inactive nilpotents',1,[-1,1],[-1,1],False),
        ('nonsplit point algebra',2,[1,0],[1,0],False),
        ('empty active part',1,[2,1],[0,0],False),
    ]
    records=[run_case(*x) for x in examples]
    certificate={'status':'PASS','examples':records,
        'exact_checks':['integer multiplication tables','determinant by permutations',
            'independent Newton-trace characteristic coefficients','idempotent identity on the nonzero guard part','exact polynomial gcd with the derivative',
            'factorization over split quadratic fibers','rational-root classification of quadratic factors',
            'wrong degree and vanishing-scale rejection'],
        'scope':'Specializations illustrating the proved general theorem; no sampling claim about the full arithmetic sources.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({'status':'PASS','examples':len(records),'output':str(args.output)}))

if __name__=='__main__':main()
