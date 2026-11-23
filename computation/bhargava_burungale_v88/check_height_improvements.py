#!/usr/bin/env python3
"""Exact finite identities supporting the BB-v2 audit.

This verifies algebraic identities and the three-square wrapper seed.  It
does not replace the cited height, prime progression, or density theorems.
Requires SymPy; writes the certificate next to this file.
"""
from fractions import Fraction
from pathlib import Path
import json
import sympy as sp

s = sp.sqrt(13)
d = (1 + s) / 2
dc = (1 - s) / 2
Q = ((3 + s) / 2, (5 + s) / 2)

def clean(x):
    return sp.simplify(sp.expand(x))

def curve_residual(P):
    x, y = P
    return clean(y**2 - x**3 + d**2 * x)

assert curve_residual(Q) == 0
lam = clean((3*Q[0]**2-d**2)/(2*Q[1]))
x2 = clean(lam**2-2*Q[0])
y2 = clean(lam*(Q[0]-x2)-Q[1])
P2 = (x2, y2)
assert lam == (13+7*s)/12
assert x2 == (187+19*s)/72
assert y2 == -(410+191*s)/216
assert curve_residual(P2) == 0
a = sp.Rational(-205, 108)
b = sp.Rational(-191, 216)
assert clean(a+b*s-y2) == 0

def v2_rat(x):
    x = Fraction(str(x))
    assert x != 0
    def v2_int(n):
        n = abs(n)
        return (n & -n).bit_length()-1
    return v2_int(x.numerator)-v2_int(x.denominator)

assert v2_rat(a) == -2 and v2_rat(b) == -3
q = sp.symbols('q', integer=True)
interval_num = sp.expand((108*q+205)*(-216*q-191))
assert sp.Poly(interval_num, q).all_coeffs() == [-23328, -64908, -39155]
assert all(int(c) % 2 == 0 for c in sp.Poly(interval_num, q).all_coeffs()[:-1])
assert int(sp.Poly(interval_num, q).all_coeffs()[-1]) % 2 == 1
assert v2_rat(sp.Rational(1,108*216)) == -5
assert sp.expand((q-a)*(b-q)-interval_num/(108*216)) == 0

Y = sp.symbols('Y')
t = 27*Y**2/(4*(Y**2-1)**3)
one_minus_t = (Y**2-4)*(2*Y**2+1)**2/(4*(Y**2-1)**3)
assert sp.factor(1-t-one_minus_t) == 0
assert sp.factor(sp.diff(t,Y)) == -27*Y*(2*Y**2+1)/(2*(Y-1)**4*(Y+1)**4)
x = sp.symbols('x')
G = (x*x-1)*(x*x-9)*(x*x-25)
assert sp.Poly(G,x).degree() == 6
assert sp.factor(G.subs(x,2*Y-1)) == 64*Y*(Y-3)*(Y-2)*(Y-1)*(Y+1)*(Y+2)
assert sp.resultant(sp.together(t).as_numer_denom()[0], sp.together(t).as_numer_denom()[1], Y) != 0

Z,D = sp.symbols('Z D')
f = sum((-1)**r*sp.binomial(2*r,r)*D**r*Z**(4*r+1)/sp.Integer(4*r+1) for r in range(6))
assert sp.series(sp.diff(f,Z)-(1+4*D*Z**4)**sp.Rational(-1,2),Z,0,24).removeO() == 0
assert clean(d*dc) == -3
assert clean(d*(-dc)) == 3
assert clean(d+dc) == 1
assert clean(d-dc) == s

primes = [p for p in list(sp.primerange(26,10000)) if p % 312 == 17]
assert primes
for p in primes:
    assert p % 8 == 1 and p % 3 == 2 and p % 13 == 4
    assert sp.legendre_symbol(13,p) == 1
    assert sp.legendre_symbol(-1,p) == 1
    assert sp.legendre_symbol(-3,p) == -1

local_counts = []
for s_count in range(1,9):
    formal = [('rho_U',j) for j in range(s_count+1)] + [('rho_V_sigma',j) for j in range(s_count+1)]
    comparison = [('B_minus_C',j) for j in range(1,s_count+1)]
    polynomial = [('F',)]
    factors = formal+comparison+polynomial
    assert len(set(factors)) == len(factors) == 3*(s_count+1)
    local_counts.append({'indices':s_count,'formal_factors':len(formal),
        'comparison_factors':len(comparison),'polynomial_factors':len(polynomial),
        'all_factors_per_tuple':len(factors),'U_points_for_two_tests':2*6*(s_count+1)})

# The multiplication coefficient 1/2 follows from these two sum-of-squares
# decompositions, valid over the reals and hence on all integral indices.
n1,n2,n3 = sp.symbols('n1 n2 n3')
S = 1+n1**2+n2**2+n3**2
Delta = n1*n2-n3
assert sp.expand(S-2*Delta - ((n1-n2)**2+(n3+1)**2)) == 0
assert sp.expand(S+2*Delta - ((n1+n2)**2+(n3-1)**2)) == 0

certificate = {
    'status':'passed',
    'scope':'Finite exact identities only; no numerical variable record or proof of external arithmetic theorems.',
    'base_curve': 'y^2=x^3-((1+sqrt(13))/2)^2*x',
    'seed_Q':[str(x) for x in Q],
    'double_seed':[str(x2),str(y2)],
    'interval_seed': {'a':str(a),'b':str(b),'v2_a':-2,'v2_b':-3,'v2_product_for_all_integer_q':-5},
    'interval_numerator':str(interval_num),
    'shimura_identity':'1-27Y^2/(4(Y^2-1)^3)=(Y^2-4)(2Y^2+1)^2/(4(Y^2-1)^3)',
    'formal_log_retained_degrees':[4*r+1 for r in range(6)],
    'prime_residue_examples_checked':primes,
    'wrapper_bound': 'r+18 rational auxiliary variables, for the same quadratic presentation of T',
    'squaring_test_reduction': {'C_blocks_before':5,'C_blocks_after':2,'Gaussian_triples_before':30,'Gaussian_triples_after':12,
        'power_variant':'Use shifts 0,T^k; k fixed sufficiently large; no elliptic amplification map.'},
    'multiplication_block_counts': {'original_three_squarings_U_points':3*5*6*3,
        'improved_three_squarings_U_points':3*2*6*3,'direct_multiplication_U_points':2*6*4,
        'scope':'Counts auxiliary Gaussian points only, not rational variables.'},
    'local_factor_inventory':local_counts,
    'multiplication_error_coefficient':'1/2, certified by S +/- 2Delta as sums of two squares',
}
out = Path(__file__).with_name('certificate.json')
out.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate,indent=2))
