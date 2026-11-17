#!/usr/bin/env python3
"""Exact algebra and valuation checks for the nine-contact derivative source.

This checks identities and exact constants used in the proof. It does not
replace the cited abc consequences, elliptic preparation, simultaneous prime
existence, or intrinsic pole completeness. All arithmetic below is exact.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import argparse
import sympy as sp

BASE = Path(__file__).resolve().parent
SHIFTS = (-10, -8, -5, 1, 2, 3, 4, 6, 7)
K = len(SHIFTS)
assert len(set(SHIFTS)) == K and sum(SHIFTS) == 0
assert all(ci+cj != 0 for ci in SHIFTS for cj in SHIFTS)
# Nine nonzero shifts with no opposite pair require max absolute value >=10:
# at bound nine they use exactly absolute values 1,...,9, whose sum is odd.
assert sum(range(1, K+1)) % 2 == 1 and max(map(abs, SHIFTS)) == K+1
A, Z, a, z, N, D, L, c = sp.symbols('A Z a z N D L c')
G = sp.Poly(sp.prod((A+ci)**2-Z for ci in SHIFTS), A, Z)
GA = G.diff(A)
assert GA.content() == 2
H = sp.Poly(GA.as_expr()/2, A, Z)
assert H.content() == 1
F_direct = sp.Poly(sp.prod((a+ci)**2-z*z for ci in SHIFTS), a, z)
F_substituted = sp.Poly(G.as_expr().subs({A:a, Z:z*z}), a, z)
assert F_direct == F_substituted
Fa = F_direct.diff(a)
assert sp.Poly(GA.as_expr().subs({A:a, Z:z*z}), a, z) == Fa
assert F_direct.as_expr().subs(a, -a) != F_direct.as_expr()
assert F_direct.as_expr().subs(z, -z) == F_direct.as_expr()
assert sp.Poly(F_direct.as_expr(), z).LC() == -1
assert sp.Poly(F_direct.as_expr(), z).degree() == 18
assert sp.Poly(Fa.as_expr(), z).degree() == 16
assert sp.Poly(Fa.as_expr(), z).LC() == 18*a
assert sp.Poly(H.as_expr(), Z).degree() == 8
assert sp.Poly(H.as_expr(), Z).LC() == 9*A
assert sp.cancel(-18*F_direct.as_expr()/Fa.as_expr()
                 + 9*G.as_expr().subs({A:a, Z:z*z})
                 / H.as_expr().subs({A:a, Z:z*z})) == 0

# Multiplying this identity gives nine minus signs and denominator D^36 L^36.
quadratic = (a+c)**2-(N/(D**2*L**2))**2
prime_pair = -(N-D**2*(a+c)*L**2)*(N+D**2*(a+c)*L**2)/(D**4*L**4)
assert sp.cancel(quadratic-prime_pair) == 0

# deg(M)<=8, deg(A=M^4)<=32, deg(Z=z^2)=2 in the retained coordinates.
degree_F = max(32*i+2*j for (i,j), coeff in G.terms())
degree_den_u = max(32*i+2*j for (i,j), coeff in H.terms())
assert (degree_F, degree_den_u) == (576,544)

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

# Directly test the new essential cases: no simple contact at a numerator
# or denominator prime of M is discarded. No power of a multiplies F/Fa.
scale_contact_checks=0
scale_contact_rows=[]
for p in (43,47,53):
    for vm in (-3,-1,1,2):
        a0=pp(p,4*vm)
        for ci in SHIFTS:
            for unit in (1,2):
                x=Q(-ci+unit*p)
                y=2*a0-x
                gx,gpx=G_value_derivative(x)
                gy,gpy=G_value_derivative(y)
                fad=gpx*gy+gx*gpy
                assert vp(gx,p)==1 and vp(gpx,p)==0
                if vm<0:
                    assert vp(gy,p)==4*K*vm
                    assert vp(fad,p)==4*K*vm
                else:
                    assert vp(gy,p)==vp(fad,p)==0
                assert vp(-2*K*gx*gy/fad,p)==1
                scale_contact_checks+=1
        scale_contact_rows.append({'p':p,'v_M':vm,'shifts_checked':K,'units_checked':2})

collision_checks=0
mixed_parity_examples=[]
for p in (37,41,43):
    for ci in SHIFTS:
        for cj in SHIFTS:
            for r in (1,2):
                x=Q(-ci+p)
                y=Q(-cj+r*p)
                a0=(x+y)/2
                assert vp(a0,p)==0
                gx,gpx=G_value_derivative(x)
                gy,gpy=G_value_derivative(y)
                fad=gpx*gy+gx*gpy
                assert vp(gx,p)==vp(gy,p)==1
                assert vp(2*a0+ci+cj,p)==1
                assert vp(fad,p)==1
                assert vp(-2*K*gx*gy/fad,p)==1
                collision_checks+=1
            # An asymmetric (1,2) contact loses oddness and is charged to J(y).
            x=Q(-ci+p)
            y=Q(-cj+p*p)
            gx,gpx=G_value_derivative(x)
            gy,gpy=G_value_derivative(y)
            fad=gpx*gy+gx*gpy
            assert (vp(gx,p),vp(gy,p),vp(fad,p))==(1,2,1)
            assert vp(-2*K*gx*gy/fad,p)==2
            if len(mixed_parity_examples)<3:
                mixed_parity_examples.append({'p':p,'ci':ci,'cj':cj,
                  'x':str(x),'y':str(y),'valuations_F_Fa_u':[3,1,2]})

# Check u/(z^2/a) ->1 at fixed places, also when M is not a local unit.
# Since a=M^4, the leading expression is a rational square.
asymptotic_checks=0
for p in (2,3,5,7,37):
    for vm in (-3,0,3):
        a0=pp(p,4*vm)
        for vz in (-24,-25):
            z0=pp(p,vz)
            gx,gpx=G_value_derivative(a0-z0)
            gy,gpy=G_value_derivative(a0+z0)
            u0=-2*K*gx*gy/(gpx*gy+gx*gpy)
            assert vp(u0,p)==2*vz-4*vm
            ratio=u0/(z0*z0/a0)
            assert vp(ratio-1,p) is None or vp(ratio-1,p)>=8
            asymptotic_checks+=1

kappa=Q(1001,1000)
epsilon=Q(1,100)
e,d=4,8
alpha=Q(e)/kappa-3
height_denominator=Q(d)-kappa*(Q(d,2)+2)
Qheight=(2*kappa-1)/height_denominator
gamma=(K-6-3*epsilon)/2
loss=2+epsilon
absorption=Qheight*(loss+1/(2*alpha))
margin=gamma-absorption
assert alpha==Q(997,1001)
assert height_denominator==Q(997,500)
assert Qheight==Q(501,997)
assert gamma==Q(297,200)
assert loss==Q(201,100)
assert absorption==Q(125473947,99400900)
assert margin==Q(44272779,198801800)>0
assert 1+6+1+2+1==11
assert 4**3*2==128
collision_sums=sorted({ci+cj for ci in SHIFTS for cj in SHIFTS})
assert 0 not in collision_sums

certificate={
 'status':'PASS',
 'scope':'Exact algebra, stated valuation samples, constants and census; arithmetic existence theorems are inputs, not computational conclusions.',
 'shifts':SHIFTS,
 'shifts_sum':sum(SHIFTS),
 'opposite_pairs':False,
 'minimal_possible_maximum_absolute_shift':10,
 'sun_prime_positions':2*K,
 'F_symmetries':{'a_even':False,'z_even':True},
 'F_z_degree':18,
 'Fa_z_degree':16,
 'Fa_z_leading_coefficient':'18*a',
 'H_Z_degree':8,
 'H_Z_leading_coefficient':'9*A',
 'normalized_u':'-9*G/H = -18*F/Fa; H=G_A/2',
 'u_over_z_squared_div_a_limit':1,
 'prime_factorization_denominator':{'D':36,'L':36},
 'G_monomials':len(G.terms()),
 'G_A_monomials':len(GA.terms()),
 'G_A_content':2,
 'primitive_denominator_monomials':len(H.terms()),
 'primitive_denominator_content':1,
 'G_coefficient_height':str(max(abs(int(v)) for _,v in G.terms())),
 'local_expression_degrees':{'height_argument':64,'u_numerator':degree_F,'u_denominator':degree_den_u},
 'balanced_valuation_cases':balanced_checks,
 'numerator_denominator_scale_contact_cases':scale_contact_checks,
 'scale_contact_rows':scale_contact_rows,
 'equal_simple_collision_cases':collision_checks,
 'mixed_parity_examples':mixed_parity_examples,
 'leading_square_cases':asymptotic_checks,
 'collision_sums':collision_sums,
 'height_parameters':{
  'k':K,'e':e,'d':d,'kappa':str(kappa),'epsilon':str(epsilon),
  'alpha':str(alpha),'signed_height_denominator':str(height_denominator),
  'Q':str(Qheight),'gamma':str(gamma),'C':str(loss),
  'absorption':str(absorption),'strict_margin':str(margin)},
 'finite_algebra_rank':128,
 'coordinate_census':{'input':1,'point_coordinates':6,'slope':1,
                       'pole_parameters':2,'encoder':1,'total':11},
 'sources_not_reproved_by_checker':[
  'ordinary rational abc and its squarefree-form consequence',
  'signed mixed-power height theorem',
  'retained elliptic rank, trace-height, formal comparison and congruence preparation',
  'Sun Theorem4.1 with18 fixed prime positions',
  'prepared intrinsic Burungale pole theorem and witness density',
  'guarded finite-algebra one-coordinate encoder'],
}
certificate['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=BASE/'algebra_certificate.json')
target=parser.parse_args().output
target.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps({'status':'PASS','certificate':str(target),
                  'exact_valuation_cases':balanced_checks+scale_contact_checks+collision_checks+asymptotic_checks,
                  'strict_margin':str(margin),'total_variables':11},indent=2))
