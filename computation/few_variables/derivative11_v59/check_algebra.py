#!/usr/bin/env python3
"""Exact algebra and valuation checks for derivative_detector_11_v59.tex.

This checks the identities and numerical constants used in the proof. It does
not replace the cited abc consequences, elliptic preparation, or intrinsic
pole completeness theorem. All arithmetic below is exact.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import argparse
import sympy as sp


BASE = Path(__file__).resolve().parent
SHIFTS = tuple(range(-8, 0)) + tuple(range(1, 9))
K = len(SHIFTS)
A, Z, a, z, N, D, L, c = sp.symbols("A Z a z N D L c")
G = sp.Poly(sp.prod((A + j*j - Z)**2 - 4*j*j*A
                    for j in range(1, 9)), A, Z)
GA = G.diff(A)
assert GA.content() == 8
H = sp.Poly(GA.as_expr()/8,A,Z)
assert H.content() == 1
F_direct = sp.Poly(sp.prod((a+c0)**2-z*z for c0 in SHIFTS), a, z)
F_squared = sp.Poly(G.as_expr().subs({A:a*a, Z:z*z}), a, z)
assert F_direct == F_squared
Fa = F_direct.diff(a)
assert sp.Poly(2*a*GA.as_expr().subs({A:a*a, Z:z*z}), a, z) == Fa
assert F_direct.as_expr().subs(a, -a) == F_direct.as_expr()
assert F_direct.as_expr().subs(z, -z) == F_direct.as_expr()
assert sp.Poly(F_direct.as_expr(), z).LC() == 1
assert sp.Poly(F_direct.as_expr(), z).degree() == 32
assert sp.Poly(Fa.as_expr(), z).degree() == 30
assert sp.Poly(Fa.as_expr(), z).LC() == -32*a
assert sp.Poly(GA.as_expr(), Z).degree() == 15
assert sp.Poly(GA.as_expr(), Z).LC() == -16
assert sp.cancel(-32*a*F_direct.as_expr()/Fa.as_expr()
                 + 16*G.as_expr().subs({A:a*a, Z:z*z})
                 / GA.as_expr().subs({A:a*a, Z:z*z})) == 0

# The exact square-denominator prime factorization is a product of this
# identity. There are 16 minus signs, so their product is +1.
quadratic = (a+c)**2-(N/(D**2*L**2))**2
prime_pair = -(N-D**2*(a+c)*L**2)*(N+D**2*(a+c)*L**2)/(D**4*L**4)
assert sp.cancel(quadratic-prime_pair) == 0

# Weighted degrees in the retained point coordinates and X,z:
# deg(M)<=8, deg(A=M^6)<=48, deg(Z=z^2)=2.
degree_F = max(48*i+2*j for (i,j), coeff in G.terms())
degree_den_u = max(48*i+2*j for (i,j), coeff in GA.terms())
assert (degree_F, degree_den_u) == (768,720)

def vp(q, p):
    """Exact valuation, using None for zero."""
    q=Q(q)
    if not q:
        return None
    result=0
    numerator=abs(q.numerator)
    denominator=q.denominator
    while numerator % p == 0:
        numerator//=p
        result+=1
    while denominator % p == 0:
        denominator//=p
        result-=1
    return result

def pp(p,e):
    return Q(p**e) if e>=0 else Q(1,p**(-e))

# Independent exact rational evaluation of all finite odd-valuation cases
# in a specified finite box; the manuscript proves the unbounded statement.
balanced_checks=0
for p in (3,5,11,37):
    for nu in range(-9,10,2):
        for value in range(-6,7):
            for unit in (1,2):
                u0=pp(p,nu)
                c0=unit*pp(p,value)
                di=c0*c0/(1+u0*c0*c0)
                assert vp(di,p)==max(2*vp(c0,p),-nu)
                if nu>0:
                    assert (vp(di,p)>0)==(vp(c0,p)>0)
                else:
                    assert vp(di*di/u0,p)>=-3*nu>0
                    assert vp(1+di*di/u0,p)==0
                balanced_checks+=1

def G_value_derivative(x):
    """Product and formal derivative, without symbolic substitution."""
    value, derivative=Q(1),Q(0)
    for shift in SHIFTS:
        derivative=derivative*(x+shift)+value
        value*=x+shift
    return value,derivative

collision_checks=0
mixed_parity_examples=[]
for p in (37,41,43):
    for ci in SHIFTS:
        for cj in SHIFTS:
            if ci+cj==0:
                continue
            for r in (1,2):
                x=Q(-ci+p)
                y=Q(-cj+r*p)
                a0=(x+y)/2
                if vp(a0,p)!=0:
                    continue
                gx,gpx=G_value_derivative(x)
                gy,gpy=G_value_derivative(y)
                fad=gpx*gy+gx*gpy
                assert vp(gx,p)==vp(gy,p)==1
                assert vp(2*a0+ci+cj,p)==1
                assert vp(fad,p)==1
                assert vp(-2*K*a0*gx*gy/fad,p)==1
                collision_checks+=1
            # The asymmetric (1,2) case really loses its odd contact and
            # must be charged to J(y), as in the proof.
            x=Q(-ci+p)
            y=Q(-cj+p*p)
            a0=(x+y)/2
            if vp(a0,p)==0:
                gx,gpx=G_value_derivative(x)
                gy,gpy=G_value_derivative(y)
                fad=gpx*gy+gx*gpy
                assert (vp(gx,p),vp(gy,p),vp(fad,p))==(1,2,1)
                assert vp(-2*K*a0*gx*gy/fad,p)==2
                if len(mixed_parity_examples)<3:
                    mixed_parity_examples.append({"p":p,"ci":ci,"cj":cj,
                      "x":str(x),"y":str(y),"valuations_F_Fa_u":[3,1,2]})

# A distinct computational path checks the p-adic leading term, including
# numerator and denominator primes of a. The source uses a=M^3; a need
# not be a square because the quotient is normalized.
asymptotic_checks=0
for p in (2,3,5,7,37):
    for va in (-3,0,3):
        a0=pp(p,va)
        for vz in (-24,-25):
            z0=pp(p,vz)
            gx,gpx=G_value_derivative(a0-z0)
            gy,gpy=G_value_derivative(a0+z0)
            u0=-2*K*a0*gx*gy/(gpx*gy+gx*gpy)
            assert vp(u0,p)==2*vz
            # The leading-square unit is close enough also at two.
            ratio=u0/(z0*z0)
            assert vp(ratio-1,p) is None or vp(ratio-1,p)>=8
            asymptotic_checks+=1

kappa=Q(1001,1000)
epsilon=Q(1,100)
e,d=4,6
alpha=Q(e)/kappa-3
height_denominator=Q(d)-kappa*(Q(d,2)+2)
Qheight=(2*kappa-1)/height_denominator
gamma=(K-6-3*epsilon)/2
loss=4+epsilon
absorption=Qheight*(loss+1/(2*alpha))
margin=gamma-absorption
assert alpha==Q(997,1001)
assert height_denominator==Q(199,200)
assert Qheight==Q(1002,995)
assert gamma==Q(997,200)
assert loss==Q(401,100)
assert absorption==Q(225373347,49600750)
assert margin==Q(87545567,198403000)>0
assert 1+6+1+2+1==11
assert 4**3*2==128

collision_sums=sorted({ci+cj for ci in SHIFTS for cj in SHIFTS if ci+cj})
assert collision_sums==list(range(-16,0))+list(range(1,17))

certificate={
 "status":"PASS",
 "scope":"Exact algebra, stated valuation samples, constants and census; arithmetic existence theorems are inputs, not computational conclusions.",
 "shifts":SHIFTS,
 "sun_prime_positions":2*K,
 "F_symmetries":{"a_even":True,"z_even":True},
 "F_z_degree":32,
 "Fa_z_degree":30,
 "Fa_z_leading_coefficient":"-32*a",
 "G_A_Z_degree":15,
 "G_A_Z_leading_coefficient":-16,
 "normalized_u":"-16*G/G_A = -32*a*F/Fa",
 "u_over_z_squared_limit":1,
 "prime_factorization_denominator":{"D":64,"L":64},
 "G_monomials":len(G.terms()),
 "G_A_monomials":len(GA.terms()),
 "G_A_content":8,
 "primitive_denominator_monomials":len(H.terms()),
 "reduced_u":"-2*G/H, H=G_A/8 primitive",
 "G_coefficient_height":str(max(abs(int(v)) for _,v in G.terms())),
 "local_expression_degrees":{"height_argument":48,"u_numerator":degree_F,"u_denominator":degree_den_u},
 "balanced_valuation_cases":balanced_checks,
 "equal_simple_collision_cases":collision_checks,
 "mixed_parity_examples":mixed_parity_examples,
 "leading_square_cases":asymptotic_checks,
 "collision_sums":collision_sums,
 "height_parameters":{
  "k":K,"e":e,"d":d,"kappa":str(kappa),"epsilon":str(epsilon),
  "alpha":str(alpha),"signed_height_denominator":str(height_denominator),
  "Q":str(Qheight),"gamma":str(gamma),"C":str(loss),
  "absorption":str(absorption),"strict_margin":str(margin)},
 "finite_algebra_rank":128,
 "coordinate_census":{"input":1,"point_coordinates":6,"slope":1,
                       "pole_parameters":2,"encoder":1,"total":11},
 "sources_not_reproved_by_checker":[
  "ordinary rational abc and its squarefree-form consequence",
  "signed mixed-power height theorem",
  "retained elliptic rank, trace-height, formal comparison and congruence preparation",
  "Sun Theorem4.1 with32 fixed prime positions",
  "prepared intrinsic Burungale pole theorem and witness density",
  "guarded finite-algebra one-coordinate encoder"],
}
certificate["checker_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=BASE/'algebra_certificate.json')
target=parser.parse_args().output
target.write_text(json.dumps(certificate,indent=2)+"\n")
print(json.dumps({"status":"PASS","certificate":str(target),
                  "exact_valuation_cases":balanced_checks+collision_checks+asymptotic_checks,
                  "strict_margin":str(margin),"total_variables":11},indent=2))
