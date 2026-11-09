#!/usr/bin/env python3
"""Independent integer bound and small-algebra checks; standard library only."""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import permutations
from math import isqrt
from pathlib import Path
import hashlib
import json


def trim(a):
    while len(a)>1 and a[-1]==0: a.pop()
    return a


def plus(a,b):
    c=[0]*max(len(a),len(b))
    for i,v in enumerate(a):c[i]+=v
    for i,v in enumerate(b):c[i]+=v
    return trim(c)


def times(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):c[i+j]+=u*v
    return trim(c)


def evaluate(a,x):
    out=0
    for c in reversed(a):out=out*x+c
    return out


def determinant_integer(A):
    n=len(A)
    if not n:return 1
    A=[list(r) for r in A]
    sign=1;previous=1
    for k in range(n-1):
        if not A[k][k]:
            j=next((j for j in range(k+1,n) if A[j][k]),None)
            if j is None:return 0
            A[k],A[j]=A[j],A[k];sign=-sign
        pivot=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=A[i][j]*pivot-A[i][k]*A[k][j]
                assert num%previous==0
                A[i][j]=num//previous
        previous=pivot
        for i in range(k+1,n):A[i][k]=0
    return sign*A[-1][-1]


def derivative_resultant(h,d):
    # Keep the prescribed degrees, even when the leading coefficient is zero.
    f=list(reversed(h+[0]*(d+1-len(h))))
    der=[i*(h[i] if i<len(h) else 0) for i in range(1,d+1)]
    g=list(reversed(der))
    size=2*d-1
    A=[]
    for shift in range(d-1):A.append([0]*shift+f+[0]*(size-shift-len(f)))
    for shift in range(d):A.append([0]*shift+g+[0]*(size-shift-len(g)))
    return determinant_integer(A)


def mm(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]


def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]


def matrix_polynomial(p,A):
    n=len(A);out=[[0]*n for _ in range(n)]
    for c in reversed(p):
        out=mm(out,A)
        for i in range(n):out[i][i]+=c
    return out


def companion(f):
    n=len(f)-1;assert f[-1]==1
    A=[[0]*n for _ in range(n)]
    for j in range(n-1):A[j+1][j]=1
    for i in range(n):A[i][-1]=-f[i]
    return A


def reciprocal_characteristic(M):
    n=len(M);out=[0]
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=[(-1)**inversions]
        for i in range(n):term=times(term,[int(i==p[i]),-M[i][p[i]]])
        out=plus(out,term)
    return trim(out)


def rational_roots_monic(f):
    f=trim(list(f));assert f[-1]==1
    roots=[]
    if f[0]==0:
        roots.append(0)
        while len(f)>1 and f[0]==0:f=f[1:]
    if len(f)==1:return roots
    c=abs(f[0]);candidates=set()
    for d in range(1,isqrt(c)+1):
        if c%d==0:candidates.update((d,-d,c//d,-c//d))
    return roots+sorted(x for x in candidates if evaluate(f,x)==0)


def kernel_vector(A):
    a=[[Fraction(x) for x in row] for row in A]
    n=len(a);pivots=[];r=0
    for c in range(n):
        p=next((i for i in range(r,n) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        t=a[r][c];a[r]=[x/t for x in a[r]]
        for i in range(n):
            if i!=r:
                t=a[i][c];a[i]=[x-t*y for x,y in zip(a[i],a[r])]
        pivots.append(c);r+=1
    free=[j for j in range(n) if j not in pivots]
    assert len(free)==1
    v=[Fraction(0)]*n;v[free[0]]=1
    for i,c in reversed(list(enumerate(pivots))):v[c]=-sum(a[i][j]*v[j] for j in free)
    return v


def toy_checks():
    examples=[
        ('irreducible_real_quadratic',[-2,0,1],[1]),
        ('irreducible_imaginary_quadratic',[1,0,1],[1]),
        ('split_with_zero_guard',[-2,-1,1],[1,1]),
        ('inactive_nonreduced_fiber',[0,0,-2,1],[0,1]),
        ('all_inactive_nonreduced',[0,0,1],[0,1]),
        ('split_with_selector_collisions',[-1,0,1],[1]),
        ('only_inactive_rational_point',[2,-2,-1,1],[-1,1]),
        ('rational_point_and_complex_factors',[-1,1,-1,1],[1]),
        ('complex_factors_only_after_guard',[-1,1,-1,1],[-1,1]),
    ]
    reports=[]
    for name,f,G in examples:
        n=len(f)-1;Z=companion(f);MG=matrix_polynomial(G,Z)
        expected=[x for x in rational_roots_monic(f) if evaluate(G,x)!=0]
        found=[];branches=0;collisions=0;drops=0
        for ell in range(n*(n+1)//2+1):
            L=[[int(i==j)+ell*Z[i][j] for j in range(n)] for i in range(n)]
            M=mm(MG,L);H=reciprocal_characteristic(M);H += [0]*(n+1-len(H))
            char=list(reversed(H));assert char[-1]==1
            eigenvalues=rational_roots_monic(char)
            for d in range(1,n+1):
                h=H[:d+1];g=derivative_resultant(h,d);branches+=1
                if not g:
                    # H_d(g*U) is identically one, including all degree drops.
                    assert h[0]==1
                    collisions+=1
                    continue
                assert h[d]!=0
                if any(H[d+1:]):continue
                if d<n:drops+=1
                for mu in eigenvalues:
                    if not mu:continue
                    V=Fraction(1,mu);U=V/g
                    assert evaluate(h,g*U)==0
                    A=[[Fraction(int(i==j))-V*M[i][j] for j in range(n)] for i in range(n)]
                    v=kernel_vector(A)
                    Zv=[sum(a*b for a,b in zip(row,v)) for row in Z]
                    j=next(j for j in range(n) if v[j])
                    z=Zv[j]/v[j]
                    assert all(a==z*b for a,b in zip(Zv,v))
                    assert evaluate(f,z)==0 and evaluate(G,z)!=0
                    found.append(z)
        assert bool(found)==bool(expected),(name,found,expected)
        reports.append({'name':name,'degree':n,'branches_checked':branches,
                        'zero_resultant_branches':collisions,'active_degree_drops':drops,
                        'rational_guarded_points':[str(x) for x in expected],
                        'recovered_points':sorted(set(map(str,found)))})
    return reports


def check_directory(directory):
    c=json.loads((directory/'construction-certificate.json').read_text())
    raw=(directory/'polynomial-specification.json').read_bytes()
    s=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()==c['output_specification_sha256']
    assert not s['closed_equations'] and not s['indexed_guard_polynomials']
    n=c['rank'];m=c['generator_count'];r=n.bit_length()-1
    assert n==2**r
    S=1+m*n*(n+1)//2
    # Independent, literal evaluation of the finite sum (no closed formula).
    C=2*sum(max(d*d*d+d,n) for d in range(1,n))+n*n*n+n
    degree=S*(c['multiplication_element_weight']*C+n*n)
    bits=S*((c['multiplication_operator_log2_norm_bound']+r)*C+(r+1)*(2*n**3+4*n-2))
    assert C==c['summed_case_weight']
    assert degree==c['degree_bound']
    assert bits==c['coefficient_l1_norm_log2_bound']
    assert degree<2**c['degree_bound_power_of_two_exponent']
    assert bits<2**c['coefficient_height_bound_double_power_of_two_exponent']
    assert s['bounds']['degree_bound']==degree
    assert s['bounds']['coefficient_l1_norm_log2_bound']==bits
    return {'directory':directory.name,'status':'PASS','degree_bound':degree,
            'coefficient_l1_norm_log2_bound':bits,'specification_sha256':hashlib.sha256(raw).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directories',type=Path,nargs='+')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result={'status':'PASS','bounds':[check_directory(d) for d in a.directories],
            'finite_algebra_examples':toy_checks(),
            'scope':'Literal integer bound sums and exact small-algebra reconstruction, including complex residue factors, zero guards, inactive nilpotents, collisions and degree drops. The general theorem is proved in the accompanying paper; global arithmetic inputs are not checked here.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
