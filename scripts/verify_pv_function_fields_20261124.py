#!/usr/bin/env python3
"""Exact checks of new identities and counts. Not a proof of arithmetic inputs."""
from fractions import Fraction as Q
from itertools import permutations, product
from math import prod
import sympy as s

x,A,B,z,r,b=s.symbols('x A B z r b')
F=x**3+A*x+B
psi=3*x**4+6*A*x**2+12*B*x-A**2
assert s.expand((3*x*x+A)**2-12*x*F+psi)==0
assert s.diff(psi,x)==12*F
# f=-psi/(3y^3)=psi*z^3/(3x^3); leading order at O is z.
assert s.expand(psi.subs(x,z**-2)*z**9/3).as_leading_term(z)==z
# conic projection from the rational base point (1,1).
delta=-2*(r+b-1)/(r*r+b-1)
mu=1+delta; nu=1+r*delta
assert s.cancel(nu**2+(b-1)*mu**2-b)==0
# PV quartic substitutions: use c=1-b; identity in the numerator.
U,V,L,c=s.symbols('U V L c', nonzero=True)
assert s.expand((b*U**4+c*L**2)+(b-1)*L**2-b*U**4).subs(c,1-b).expand()==0
assert s.expand((b*V**4+c**3*L**2)+(b-1)*c**2*L**2-b*V**4).subs(c,1-b).expand()==0
assert s.expand(c*L*c*L-c**2*L**2)==0
# No fourth-power cancellation at the fixed preparation primes.
for p in (3,5,7):
    assert all((a**4+d**4)%p for a in range(1,p) for d in range(1,p))
assert all((a**4+d**4)%16==2 for a in range(1,16,2) for d in range(1,16,2))
# Odd difference guarantees a unique largest absolute valuation, hence
# a unique minimal valuation in a^4+a^-4+b^4+b^-4.
for a,d in product(range(-20,21), repeat=2):
    if (a-d)%2:
        vals=[4*a,-4*a,4*d,-4*d]
        assert vals.count(min(vals))==1 and min(vals)==-4*max(abs(a),abs(d))
# Group-theoretic Chebotarev improvement: exhaustive S_n toy checks.
for n in range(2,7):
    moves=[];pairs=[]
    for p in permutations(range(n)):
        fixed=sum(j==p[j] for j in range(n))
        seen=set(); cc=[]
        for j in range(n):
            if j not in seen:
                i=j; l=0
                while i not in seen:
                    seen.add(i); l+=1; i=p[i]
                cc.append(l)
        m=n-fixed; q=sum(l*(l-1) for l in cc)
        assert q>=m
        moves.append(m);pairs.append(q)
    assert Q(sum(moves),len(moves))==n-1
    assert Q(sum(pairs),len(pairs))>=n-1
# Finite squareclass table examples over F_9: i^2=-1 and (1+i)^4=-4.
i=s.I
assert s.expand((1+i)**4)==-4
# Exact ambient height and radical margins.
kappa=Q(101,100); e=8
alpha=Q(e)/kappa-3
C=(1+1/kappa-Q(2,e))/alpha
assert C==Q(703,1988)<Q(1,2)
eps=Q(1,100)
assert 2*(3-3*eps)-(2+eps)==Q(393,100)
assert Q(393,100)-Q(1,2)==Q(343,100)>0
assert Q(1001,997)**5/2<Q(393,100)
# Census arithmetic, no additional coordinate for finite roots.
for k in range(1,101):
    n=3*k+5; t=2
    assert k+(2*k+1)+4*k+1==7*k+2
    assert (3*k+8)-1+2*(3*k+8)+1+4*(3*k+8)+1==21*k+57
    assert 7*n+t+8==21*k+45
    assert 7*n+t+2==21*k+39
    assert (3*k+7)+6*(2*k+5)+2==15*k+39
    assert (3*k+7)+6*(2*k+4)+2==15*k+33
    assert k+2*(k+2)+1+2+1==3*k+8
assert (7*20+4+8,7*20+6+8)==(152,154)
print('PASS: torsion/division polynomial, conic/quartic identities, valuations, permutation averages, exact height margins and coordinate ledgers')
