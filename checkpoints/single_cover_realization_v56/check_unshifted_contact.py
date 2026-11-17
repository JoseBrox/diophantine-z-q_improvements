#!/usr/bin/env python3
"""Exact fresh-contact leading-square certificate for the unshifted detector.

It certifies one split good prime and the universal leading-form identity.
It does not assert a global rational square or a complete realization.
"""
from math import gcd
from pathlib import Path
import json
import sympy as sp

p=77017
root=18810
orders=(2141,2405)
assert sp.isprime(p) and root*root%p==2 and gcd(*orders)==1
mod=p*p

def double(P,D,m):
    X,Y,Z=P
    if Z==0:return P
    S=4*X*Y*Y%m
    M=(3*X*X-D*pow(Z,4,m))%m
    xx=(M*M-2*S)%m
    yy=(M*(S-xx)-8*pow(Y,4,m))%m
    return xx,yy,2*Y*Z%m

def add(P,Q,D,m):
    X,Y,Z=P;U,V,T=Q
    if Z==0:return Q
    if T==0:return P
    A=X*T*T%m;B=U*Z*Z%m
    C=Y*pow(T,3,m)%m;E=V*pow(Z,3,m)%m
    H=(B-A)%m
    R=2*(E-C)%m
    if H==0 and R==0:return double(P,D,m)
    # In the short annihilating-order calculation no equal-reduction,
    # unequal-lift addition occurs. This assertion prevents using a
    # nonprimitive Jacobian triple as a local point.
    assert H%p or R%p
    I=4*H*H%m;J=H*I%m;V0=A*I%m
    xx=(R*R-J-2*V0)%m
    yy=(R*(V0-xx)-2*C*J)%m
    zz=2*Z*T*H%m
    return xx,yy,zz

def mult(n,P,D,m):
    ans=(1,1,0)
    for digit in bin(n)[2:]:
        ans=double(ans,D,m)
        if digit=='1':ans=add(ans,P,D,m)
    return ans

rows=[]
logs=[]
for r,order in zip((root,p-root),orders):
    correction=((r*r-2)//p)*pow(2*r,-1,p)%p
    lifted=(r-correction*p)%mod
    assert (lifted*lifted-2)%mod==0
    D=(11-6*lifted)%mod
    P=((57-28*lifted)*pow(8,-1,mod)%mod,
       (-660+417*lifted)*pow(32,-1,mod)%mod,1)
    point=mult(order,P,D,mod)
    X,Y,Z=point
    assert Z%p==0 and Y%p!=0
    zeta=(-X*Z*pow(Y,-1,mod))%mod
    assert zeta%p==0 and zeta!=0
    log_unit=(zeta//p)*pow(order,-1,p)%p
    logs.append(log_unit)
    rows.append({'sqrt2_mod_p2':lifted,'annihilating_order':order,
                 'formal_zeta_mod_p2':zeta,'log_P_over_p_mod_p':log_unit})

n,a,b=sp.symbols('n a b')
assert sp.expand(((1+n**4)*(a**4+b**4)).subs(a,n*b)
                 -(1+n**4)**2*b**4)==0

fixtures=[]
for n0 in [1,2,3,5,8,-2,-5]:
    assert n0%p and (1+n0**4)%p
    l1,l2=logs
    eps=1 if (l1-n0*l2)%p else -1
    den=(l1-eps*n0*l2)%p
    h=(-eps*n0*l2)*pow(den,-1,p)%p
    aa=h*l1%p;bb=(h-1)*l2%p
    assert aa and bb and aa==eps*n0*bb%p
    lead=(1+n0**4)*(aa**4+bb**4)%p
    root_lead=(1+n0**4)*bb*bb%p
    assert root_lead*root_lead%p==lead
    # The reduction orders, the fixed even progression, and the new
    # p-adic residue are pairwise compatible in this exact example.
    from sympy.ntheory.modular import solve_congruence
    crt=solve_congruence((0,orders[0]),(1,orders[1]),(0,64),(h,p))
    assert crt is not None
    hc,mc=map(int,crt)
    assert hc%orders[0]==0 and hc%orders[1]==1 and hc%64==0 and hc%p==h
    fixtures.append({'integer_input':n0,'sign':eps,'h_mod_p':h,
                     'formal_leading_units':[aa,bb],
                     'test_sum_unit':lead,'square_root_unit':root_lead,
                     'compatible_h':hc,'combined_modulus':mc})

result={'status':'PASS','prime':p,'slots':rows,'fixtures':fixtures,
        'universal_leading_identity':'(1+n^4)((n b)^4+b^4)=(1+n^4)^2 b^4',
        'scope':'Fresh-contact local squares only; no fixed-place or global rational realization is asserted.'}
Path(__file__).with_name('unshifted_contact_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
