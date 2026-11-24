#!/usr/bin/env python3
"""Exact finite verification of the CM norm-conic examples."""
from fractions import Fraction as Q
from math import lcm
import sympy as s
from sympy import sqrt
x=s.symbols('x')
F=x**3-2*x
psi3=3*x**4-12*x**2-4
psi4_y=4*(x**6-10*x**4-20*x*x+8)
psi5=s.expand(8*F**2*psi4_y-psi3**3)
psi6_over_psi2=s.expand(psi3*(psi5-psi4_y**2/4))
f=s.expand(psi6_over_psi2/3)
g=(x*x-2+4*sqrt(3)/3)*(x*x+6+4*sqrt(3))*(x**4+(-28-16*sqrt(3))*x*x+4)
gbar=g.xreplace({sqrt(3):-sqrt(3)})
assert s.expand(g*gbar-f)==0
assert s.degree(f,x)==16 and s.Poly(f,x).LC()==1

def add(P,R,A):
    if P is None:return R
    if R is None:return P
    x,y=P;z,w=R
    if x==z and y==-w:return None
    u=(w-y)/(z-x) if x!=z else (3*x*x+A)/(2*y)
    t=u*u-x-z
    return t,u*(x-t)-y

def mul(P,m,A):
    R=None
    while m:
        if m%2:R=add(R,P,A)
        P=add(P,P,A);m//=2
    return R
P=(Q(9,4),Q(-21,8)); U=mul(P,3,-2)
R=s.cancel(g.subs(x,P[0])/psi3.subs(x,P[0])**2)
assert s.simplify(R*R.xreplace({sqrt(3):-sqrt(3)})-U[1]/(3*P[1]))==0
P=(Q(3),Q(6)); U=mul(P,5,0)
assert mul(P,2,0)[0]==Q(-15,16)
assert U==(Q(1441917363,11895601),Q(-54753470848434,41027927849))
for eps,aa,bb in [(-1,197,50),(1,137,10)]:
    R=(sqrt(5)*(aa+bb*sqrt(5))/(107+40*sqrt(5)))**3
    R=s.radsimp(s.expand(R))
    assert s.simplify(R*R.xreplace({sqrt(5):-sqrt(5)})-125*(U[1]-eps*3)/(P[1]+eps*3))==0
for ell in [3,7,11,19,23,31,43]:
    assert pow(ell-1,(ell-1)//2,ell)==ell-1
for ell in [5,11,17,23,29,41,47]:
    assert ell%3==2
    assert (pow(ell-1,(ell-1)//2,ell)==ell-1)==(ell%4==3)
fixtures=0
for ell in [3,11,19,23]:
    moduli=[p**e for p in [2,3,5,7,11,13,17,29] if p!=ell for e in [1,2,4]]
    order=lcm(*(int(s.n_order(ell,m)) for m in moduli))
    for r in range(1,12):
        k=2*order*(r+1)-r
        assert k>0 and (k+r)%2==0
        assert all(pow(ell,k+r,M)==1 for M in moduli)
        fixtures+=1
print('PASS: m=3 factorization and rational norm, m=5 two rational norms,',fixtures,'simultaneous prime-power exponent fixtures.')
