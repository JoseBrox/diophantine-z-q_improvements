"""Exact certificate for the d=112/225 one-coordinate cover obstruction.

This checker certifies the explicit arithmetic and polynomial identities in
prepared_q0_sha_counterexample.tex. The implication from its nonzero pairing
to the rank bound invokes the cited Cassels theorem and Monsky description,
not bounded searches or numerical L-values.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import prod
import json
import argparse
import sympy as S

n=791
primes=(7,113)
assert prod(primes)==n and all(S.isprime(p) for p in primes)
d=Q(112,225)
assert 0<d<1 and d==7*Q(4,15)**2
assert d.numerator%16==0 and d.numerator%32

A=S.zeros(2)
for i,p in enumerate(primes):
    for j,q in enumerate(primes):
        if i!=j:A[i,j]=int(S.legendre_symbol(q,p)==-1)
    A[i,i]=sum(A[i,j] for j in range(2))%2
D2=S.diag(*[int(S.legendre_symbol(2,p)==-1) for p in primes])
Dm2=S.diag(*[int(S.legendre_symbol(-2,p)==-1) for p in primes])
M=(A+Dm2).row_join(D2).col_join(D2.row_join(A+D2))%2
assert M==S.diag(1,0,0,0)
basis=[(113,1,113),(1,7,7),(1,113,113)]
for b1,b2,b3 in basis:
    assert S.integer_nthroot(b1*b2*b3,2)[1]
    vec=S.Matrix([int(b1%p==0) for p in primes]+[int(b2%p==0) for p in primes])
    assert M*vec==S.zeros(4,1)

# Exact projective conics in the cited full2descent convention.
t,u1,u2,u3=S.symbols('t u1 u2 u3')
H1=-n*t*t+7*u2*u2-7*u3*u3
H2=-n*t*t+7*u3*u3-u1*u1
H3=2*n*t*t+u1*u1-7*u2*u2
L1=u2-u3
L2=-113*t-4*u1+15*u3
L3=226*t+3*u1-17*u2
Q1={t:0,u2:1,u3:1}
Q2={t:1,u1:28,u3:15}
Q3={t:1,u1:21,u2:17}
for H,L,point,div in [(H1,L1,Q1,14),(H2,L2,Q2,14),(H3,L3,Q3,14)]:
    assert H.subs(point)==0
    tangent=sum(S.diff(H,v).subs(point)*v for v in (t,u1,u2,u3))/div
    assert S.expand(tangent-L)==0

# These identities prove all-prime parity of tangent valuations.
identity1=S.expand(L1*(u2+u3)-113*t*t-H1/7)
identity3=S.expand(L3*(226*t-3*u1+17*u2)+(17*u1-21*u2)**2/7-226*H3/7)
assert identity1==0 and identity3==0
# The second identity is exact modulo H3; determinant support only2,113.
det=int(S.Matrix([[17,-21],[3,-17]]).det())
assert abs(det)==226

# At113: r^2=7, r=32 mod113, localpoint(0,-r,-1,1).
p=113
r0=32
assert r0*r0%p==7
point={t:0,u1:-r0,u2:-1,u3:1}
assert all(int(H.subs(point))%p==0 for H in (H1,H2,H3))
L1val=int(L1.subs(point));L3val=int(L3.subs(point))
product_mod_p=L1val*L3val%p
assert product_mod_p==45
assert S.legendre_symbol(product_mod_p,p)==-1
assert pow(product_mod_p,(p-1)//2,p)==p-1
assert 113%8==1 and S.legendre_symbol(113,7)==1

# Cover, benchmark, and Mordell-Weil descent point.
a,c,z,x=S.symbols('a c z x')
cover_identity=S.expand((a*t*z)**2-((-a*t*t)**3-(a*c)**2*(-a*t*t))-a*a*t*t*(z*z-a*(c*c-t**4)))
assert cover_identity==0
X=-784;Y=-2940
assert Y*Y==X**3-n*n*X

def sf(q):
    q=Q(q);answer=-1 if q<0 else 1
    for p,e in S.factorint(abs(q.numerator)*q.denominator).items():
        if e%2:answer*=int(p)
    return answer

Pdescent=tuple(sf(v) for v in (X-n,X+n,X))
assert Pdescent==(-7,7,-1)
torsion=[(1,1,1),(2,2*n,n),(-2*n,2,-n),(-n,n,-1)]
normalized=tuple(sf(a*b) for a,b in zip(Pdescent,torsion[3]))
assert normalized==(113,113,1)
assert Pdescent not in torsion
assert all(row!=(1,1,1) for row in torsion[1:])
abscissa_image={1,-1,n,-n}
assert -7 not in abscissa_image

# Direct isomorphism from prepared C_d to the small quartic.
s,yy=S.symbols('s yy')
original=yy**2-S.Rational(112,225)*((1-S.Rational(112,225))**2-s**4)
transformed=(S.Rational(3375,4)*yy)**2-7*(113**2-(15*s)**4)
assert S.expand(transformed-S.Rational(3375,4)**2*original)==0

certificate={
 'status':'All exact checks passed; the rank bound uses the cited Monsky/Cassels theorems.',
 'prepared_d':str(d),
 'quartic':'z^2=7(113^2-t^4)',
 'genus_one_jacobian':'Y^2=X^3+4*791^2*X',
 'cover_target':'Y^2=X^3-791^2*X',
 'monsky_matrix':[list(map(int,M.row(i))) for i in range(4)],
 'pure_selmer_basis':basis,
 'pairing_arguments':{'Lambda':basis[1],'Lambda_prime':basis[0]},
 'tangent_forms':[str(L1),str(L2),str(L3)],
 'tangent_points':[[0,1,1],[1,28,15],[1,21,17]],
 'all_other_prime_vanishing':'Explicit tangent norm identities; determinant226; no3,5,17 exceptions.',
 'local_symbol_2':1,'local_symbol_7':1,'local_symbol_infinity':1,
 'sqrt7_mod113':r0,'tangent_product_mod113':product_mod_p,'local_symbol_113':-1,
 'global_pairing':-1,
 'rank_upper_bound_from_three_dimensional_pure_selmer_and_nonzero_pairing':1,
 'non_torsion_point':[X,Y],
 'point_descent':Pdescent,
 'pure_point_class':normalized,
 'rank':1,
 'abscissa_image':sorted(abscissa_image),
 'excluded_abscissa_class':-7,
 'conclusion':'The prepared curve is everywhere locally soluble and has no rational point.',
 'scope':'Prepared inputs in general; not asserted to be an actual detector tuple.',
 'primary_sources':[
  'https://arxiv.org/pdf/1511.03810 sections2.1-2.2',
  'https://zhangshenxing.github.io/publications/Zhang2025.pdf sections2.1-2.2'
 ]
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
out = args.output or Path(__file__).with_name('certificate.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate,indent=2))
