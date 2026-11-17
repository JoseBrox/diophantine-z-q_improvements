#!/usr/bin/env python3
"""Exact prepared native products obstructing two adaptive square families.

The fixtures are abstract positive native detector products. They are not
asserted to arise from the elliptic tests and physical contacts of general21
or derivative9. Universal local conclusions are proved in the companion paper.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
P = 100003


def valuation(value, p):
    value = F(value)
    if not value:
        return None
    answer = 0
    for n, direction in ((abs(value.numerator), 1), (value.denominator, -1)):
        while n % p == 0:
            answer += direction
            n //= p
    return answer


def residue(value, p):
    value = F(value)
    assert value.denominator % p
    return value.numerator * pow(value.denominator, -1, p) % p


def local_square(value, p):
    value = F(value)
    if value == 0:
        return True
    v = valuation(value, p)
    if v % 2:
        return False
    unit = value / F(p)**v
    if p == 2:
        return residue(unit, 8) == 1
    return pow(residue(unit, p), (p-1)//2, p) == 1


def crt(congruences):
    value, modulus = 0, 1
    for r, m in congruences:
        value += modulus * ((r-value)*pow(modulus, -1, m) % m)
        modulus *= m
    return value, modulus


def native_pair(u, h0, h1):
    """W=1+w*(h0+h1*sqrt(2))^2; return exact rational invariants."""
    u, h0, h1 = F(u), F(h0), F(h1)
    w = u/(1+u)**2
    A = 1+w*(h0*h0+2*h1*h1)
    B = 2*w*h0*h1
    N = A*A-2*B*B
    V = 2*A/N
    C = V*V+w*(2-V)
    b = 4*w/(V*V)
    assert N != 0 and A != 0 and w != 0
    assert b == u*(N/((1+u)*A))**2
    return {'u':u, 'w':w, 'h0':h0, 'h1':h1,
            'W_real_component':A, 'W_sqrt2_component':B,
            'W_norm':N, 'V':V, 'C':C, 'b':b}


def preparation(pair):
    w, V, C, b = (pair[k] for k in ('w','V','C','b'))
    assert 0 < w <= F(1,4)
    assert F(200,101) < V < 2
    assert 0 < b < F(1,7)
    assert isqrt(b.denominator)**2 == b.denominator
    assert local_square(b,2) and valuation(b,2) >= 4
    assert valuation(b,7) >= 0
    assert all(local_square(b,p) for p in (3,17))
    assert valuation(b,3) >= 1 and valuation(b,17) >= 2
    assert all(local_square(C,p) for p in (2,3,7,17))
    return {
        'positive_weight_at_most_one_quarter':True,
        '200_over_101_less_than_V_less_than_2':True,
        '0_less_than_b_less_than_one_seventh':True,
        'square_reduced_denominator':True,
        'intrinsic_pole_prepared':True,
        'older_2_3_17_preparation_also_satisfied':True,
        'C_locally_square_at_2_3_7_17':True,
        'b_valuations':{str(p):valuation(b,p) for p in (2,3,7,17)},
    }


def first_fixture():
    m = F(509796,28707122557)
    z = F(509796,32337379873)
    assert 0 < m < F(1,1000) and 0 < z < F(1,1000)
    u = m*m
    pair = native_pair(u,z*(1+u)/m,0)
    assert pair['W_real_component'] == 1+z*z
    assert pair['V'] == 2/(1+z*z)
    assert pair['b'] == (m*(1+z*z)/(1+m*m))**2
    assert residue(m,P) == 7121
    assert (7121**2-7121+1) % P == 0
    assert residue(z,P) == 1
    assert [residue(pair[k],P) for k in ('w','V','C')] == [1,1,2]
    assert valuation(pair['C'],P) == 0 and not local_square(pair['C'],P)
    assert all(local_square(pair['C']*(1+24*pair['V']),p)
               for p in (2,3,7,17))
    return {
        'name':'quartic_in_q_class',
        'parameters':{'m':str(m),'z':str(z)},
        'native_pair':{k:str(v) for k,v in pair.items()},
        'preparation':preparation(pair),
        'fresh_prime':P,
        'fresh_prime_residues':{'w':1,'V':1,'C':2},
        'C_times_delta_at_c_zero_locally_square_at_2_3_7_17':True,
        'all_q_exclusion':'At p=100003, delta(q,V) is a nonzero Q_p square for every q in Q_p, whereas C is a nonsquare unit.',
        'all_c_exclusion':True,
    }


def second_fixture():
    r, M = 44974, 714**2
    assert valuation(r*r+2,P) == 1
    h0, h1 = M*P**3*r, M*P**3
    H = M*P**3*(r+2)
    residues = [(P*P-1,P**3),(16,128),(9,27),(289,4913),(1,7)]
    base, modulus = crt(residues)
    bound = 100*H*H+100
    u = base+max(0,(bound-base+modulus-1)//modulus)*modulus
    assert u == 52581464203154325228257242401217852539664811276478096
    assert all(u % m == r0 for r0,m in residues)
    assert u >= bound
    pair = native_pair(u,h0,h1)
    # Both real h slots have absolute value < H, hence W slots <101/100.
    assert pair['w']*H*H < F(1,100)
    fresh = {k:valuation(v,P) for k,v in pair.items()
             if k in ('u','w','V','C','b')}
    fresh['2-V'] = valuation(2-pair['V'],P)
    assert fresh == {'u':0,'w':-4,'V':0,'C':-1,'b':-4,'2-V':3}
    assert not local_square(pair['C'],P)
    return {
        'name':'positive_quartic_class',
        'parameters':{'r':r,'M':M,'u':str(u),'h0':str(h0),'h1':str(h1)},
        'native_pair':{k:str(v) for k,v in pair.items()},
        'preparation':preparation(pair),
        'both_real_W_slots_between_one_and_101_over_100':True,
        'fresh_prime':P,
        'fresh_prime_valuations':fresh,
        'all_c_exclusion':'At p=100003, every 1+(w*V^2*c^2)^2 has even valuation, while C has valuation -1.',
    }


def symbolic_identities():
    q,V,w,c,b,z,B,X,Y,y,n = sp.symbols('q V w c b z B X Y y n')
    delta = (q*q-2*q-1)**2+4*q*(q*q-1)*V
    assert sp.expand(delta-((q*q+1)**2+4*(V-1)*q*(q*q-1))) == 0
    discriminant = sp.factor(sp.discriminant(delta,q))
    assert discriminant == 16384*V**2*(V-2)**2*(V-1)**2
    assert sp.expand(delta.subs(q,2)) == 1+24*V
    C = V*V+w*(2-V)
    assert sp.cancel((C/V**2).subs(w,b*V**2/4)-(1+b*(2-V)/4)) == 0
    assert sp.cancel((1+w*w*V**4*c**4).subs({w:b*V**2/4,c:2*z/V**2})-(1+b*b*z**4)) == 0
    xx, yy, nn = B*b*b*z*z, B*b*b*z*y, B*b
    assert sp.expand(yy**2-xx**3-nn**2*xx
                     -B**2*b**4*z**2*(y*y-B*(1+b*b*z**4))) == 0
    xp,yp = X+n*n/X, Y*(1-n*n/X**2)
    assert sp.cancel(yp*yp-xp**3+4*n*n*xp
                     -(1-n*n/X**2)**2*(Y*Y-X**3-n*n*X)) == 0
    return {
        'delta_q_discriminant':str(discriminant),
        'old_c_curve_genus_on_1_less_V_less_2':3,
        'new_c_curve_genus_on_prepared_domain':1,
        'rescaled_new_curve':'y^2=B*(1+b^2*z^4), B=1+b*(2-V)/4, z=V^2*c/2',
        'plus_curve_map':'X=B*b^2*z^2, Y=B*b^2*z*y; Y^2=X^3+(B*b)^2*X',
        'two_isogeny':'x=X+(B*b)^2/X, y=Y*(1-(B*b)^2/X^2); y^2=x^3-(2*B*b)^2*x',
        'global_realization_inferred':False,
    }


def main():
    assert all(P%d for d in range(2,isqrt(P)+1))
    assert P%24 == 19
    assert pow(2,(P-1)//2,P) == P-1
    report = {
        'schema':'adaptive-prepared-native-pair-obstructions/v76',
        'status':'PASS',
        'prime_certificate':{'prime':P,'trial_division_through':isqrt(P),
                             'residue_mod_24':19,'two_euler_value':P-1},
        'fixtures':[first_fixture(),second_fixture()],
        'symbolic_identities':symbolic_identities(),
        'scope':'Exact prepared abstract native products and local obstructions for every rational added scalar. No actual elliptic source tuple is claimed; neither general21 nor derivative9 completeness is disproved.',
    }
    (HERE/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: both prepared native pairs, universal local obstructions, and exact quartic transformations.')


if __name__=='__main__':
    main()
