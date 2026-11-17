#!/usr/bin/env python3
"""Exact actual-trace curves for X=1, A=P, H=U=5P, B=3.

Certifies the elliptic inputs, the rational u-curve, the degree-nine
physical-weight map, and good-reduction squarefreeness certificates.
No rational-point enumeration or completeness result is claimed.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import json

import sympy as sp


@dataclass(frozen=True)
class K:
    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def coerce(v):
        return v if isinstance(v, K) else K(F(v))

    def __add__(self, v):
        v = K.coerce(v)
        return K(self.a+v.a, self.b+v.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, v):
        return self+-K.coerce(v)

    def __rsub__(self, v):
        return K.coerce(v)+-self

    def __mul__(self, v):
        v = K.coerce(v)
        return K(self.a*v.a+2*self.b*v.b, self.a*v.b+self.b*v.a)

    __rmul__ = __mul__

    def bar(self):
        return K(self.a, -self.b)

    def inverse(self):
        norm = self.a*self.a-2*self.b*self.b
        assert norm
        return K(self.a/norm, -self.b/norm)

    def __truediv__(self, v):
        return self*K.coerce(v).inverse()

    def __rtruediv__(self, v):
        return K.coerce(v)*self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse()**(-n)
        ans, base = K(F(1)), self
        while n:
            if n & 1:
                ans *= base
            base *= base
            n >>= 1
        return ans

    def data(self):
        return [str(self.a), str(self.b)]


E_D = K(F(11), F(-6))
P = (K(F(57, 8), F(-7, 2)), K(F(-165, 8), F(417, 32)))
SHIFTS = (-10, -8, -5, 1, 2, 3, 4, 6, 7)


def on_curve(point):
    if point is None:
        return True
    x, y = point
    return y*y == x*x*x-E_D*x


def point_add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    X, Y = q
    if x == X:
        if y == -Y:
            return None
        slope = (3*x*x-E_D)/(2*y)
    else:
        slope = (Y-y)/(X-x)
    xx = slope*slope-x-X
    result = (xx, slope*(x-xx)-y)
    assert on_curve(result)
    return result


def point_mul(n, p):
    result = None
    while n:
        if n & 1:
            result = point_add(result, p)
        p = point_add(p, p)
        n >>= 1
    return result


def rat(v):
    return sp.Rational(v.numerator, v.denominator)


def coeff_data(poly):
    return [str(c) for c in reversed(poly.all_coeffs())]


def p_add(a, b):
    return (a[0]+b[0], a[1]+b[1])


def p_mul(a, b):
    return (a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def p_bar(a):
    return (a[0], -a[1])


def p_const(v, u):
    v = K.coerce(v)
    return (sp.Poly(rat(v.a), u), sp.Poly(rat(v.b), u))


def p_pow(p, n, u):
    result = p_const(1, u)
    for _ in range(n):
        result = p_mul(result, p)
    return result


def int_pair(p, q):
    multiplier = lcm(*(int(c.q) for poly in (p, q) for c in poly.all_coeffs()))
    pp, qq = sp.Poly(multiplier*p.as_expr(), p.gens[0], domain=sp.ZZ), sp.Poly(multiplier*q.as_expr(), q.gens[0], domain=sp.ZZ)
    content = reduce(gcd, (abs(int(c)) for poly in (pp, qq) for c in poly.all_coeffs()))
    return pp.exquo_ground(content), qq.exquo_ground(content)


def modpoly(poly, p):
    return sp.Poly.from_list([int(c) % p for c in poly.all_coeffs()], poly.gens[0], modulus=p)


def homogenized_mod(poly, A, B, p):
    # Horner homogeneous composition, without constructing huge Q coefficients.
    Ap, Bp = modpoly(A, p), modpoly(B, p)
    result = sp.Poly(int(poly.LC()) % p, A.gens[0], modulus=p)
    b_power = sp.Poly(1, A.gens[0], modulus=p)
    for coefficient in poly.all_coeffs()[1:]:
        b_power *= Bp
        result = result*Ap+(int(coefficient) % p)*b_power
    return result


def frac_mod(v, p):
    v = F(v)
    return v.numerator % p * pow(v.denominator % p, -1, p) % p


def k_mod(v, p, rho):
    return (frac_mod(v.a, p)+rho*frac_mod(v.b, p)) % p


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=here / "certificate.json")
    parser.add_argument("--manuscript", type=Path,
                        default=here / "actual_trace_arithmetic_20261117_v70.tex")
    args = parser.parse_args()
    u, t = sp.symbols("u t")
    assert on_curve(P)
    halfP = (K(F(1),F(1)), K(F(0),F(2)))
    assert on_curve(halfP) and point_mul(2,halfP) == P
    H, HmP = point_mul(5, P), point_mul(4, P)
    assert point_add(HmP, P) == H
    for point in (P, H, HmP):
        assert point is not None and point[0] != K() and point[1] != K()
    assert H[0] != P[0]
    c, d = 1/H[0], (1/HmP[0]).bar()
    alpha, beta = c*c, d*d
    U = p_const(1, u)
    up = (sp.Poly(u, u), sp.Poly(0, u))
    alpha_linear = p_add(U, p_mul(up, p_const(alpha, u)))
    beta_linear = p_add(U, p_mul(up, p_const(beta, u)))
    Lalpha = p_add(p_mul(up, p_pow(alpha_linear, 2, u)), p_const(alpha*alpha, u))
    Lbeta = p_add(p_mul(up, p_pow(beta_linear, 2, u)), p_const(beta*beta, u))
    Q = p_mul(Lalpha, Lbeta)
    S = p_mul(p_pow(up, 2, u), p_mul(p_pow(alpha_linear, 2, u), p_pow(beta_linear, 2, u)))
    SQbar = p_mul(S, p_bar(Q))
    Qnorm = p_mul(Q, p_bar(Q))
    assert Qnorm[1].is_zero
    Nraw = 2*(SQbar[0]**2+2*SQbar[1]**2)
    Draw = Qnorm[0]**2
    N, D = int_pair(Nraw, Draw)
    Pu = N**2*sp.Poly((u+1)**2, u)+sp.Poly(u, u)*D*(2*D-N)
    assert N.degree() == D.degree() == 24 and Pu.degree() == 50
    assert N.LC() == 2*D.LC()
    assert Pu.eval(0) == 0 and Pu.diff().eval(0) != 0
    for sample in (1, 2, 3):
        ss = F(sample)
        dc = c*c/(1+ss*c*c)
        dd = d*d/(1+ss*d*d)
        W = ((1+dc*dc/ss)*(1+dd*dd/ss))**2
        direct_V = 2*W.inverse().a
        rational_V = F(int(N.eval(sample)), int(D.eval(sample)))
        assert direct_V == rational_V
        direct_C = direct_V**2+ss/(1+ss)**2*(2-direct_V)
        assert direct_C == F(int(Pu.eval(sample)), (sample+1)**2*int(D.eval(sample))**2)
    traceA = 2*P[0].a
    scale = (F(4)**4+traceA**4)**4
    contact_factors = [sp.Poly(rat((scale+s)**2)-t, t) for s in SHIFTS]
    Fpoly = reduce(lambda a,b:a*b, contact_factors, sp.Poly(1,t))
    Faderivative = sp.Poly(0,t)
    for i,s in enumerate(SHIFTS):
        product = sp.Poly(2*rat(scale+s),t)
        for j,factor in enumerate(contact_factors):
            if i != j:
                product *= factor
        Faderivative += product
    A, B = int_pair(-18*Fpoly, Faderivative)
    assert A.degree() == 9 and B.degree() == 8
    assert scale > 10
    # A single good reduction certifies all needed Q-squarefreeness claims.
    good = None
    for prime in list(sp.primerange(101, 1000)):
        Pmod = modpoly(Pu, prime)
        if Pmod.degree() != 50 or sp.gcd(Pmod,Pmod.diff()).degree() != 0:
            continue
        if sp.gcd(modpoly(N,prime),modpoly(D,prime)).degree() != 0:
            continue
        if sp.gcd(modpoly(A,prime),modpoly(B,prime)).degree() != 0:
            continue
        Qmod = homogenized_mod(Pu,A,B,prime)
        if Qmod.degree() != 450 or Qmod.eval(0) == 0:
            continue
        if sp.gcd(Qmod,Qmod.diff()).degree() != 0:
            continue
        Eu,Fu,Gu = sp.gcdex(Pmod,Pmod.diff())
        Et,Ft,Gt = sp.gcdex(Qmod,Qmod.diff())
        assert Gu == sp.Poly(1,u,modulus=prime)
        assert Gt == sp.Poly(1,t,modulus=prime)
        assert Eu*Pmod+Fu*Pmod.diff() == Gu
        assert Et*Qmod+Ft*Qmod.diff() == Gt
        good = {'prime':int(prime), 'u_degree':50, 't_degree':450,
                't_constant_residue':int(Qmod.eval(0)) % prime,
                'u_bezout':[coeff_data(Eu),coeff_data(Fu)],
                't_bezout':[coeff_data(Et),coeff_data(Ft)]}
        break
    assert good is not None
    # A fully actual slope with one locally soluble split contact and a
    # different, unit-weight local obstruction. This is not full preparation.
    slope = scale+12
    physical_u = -18/sum((2*(scale+c)/((scale+c)**2-slope*slope)
                          for c in SHIFTS), F(0))
    assert physical_u > 0 and slope > scale+10
    def valuation(q, prime):
        numerator, denominator = q.numerator, q.denominator
        assert numerator
        result = 0
        while numerator % prime == 0:
            numerator //= prime
            result += 1
        while denominator % prime == 0:
            denominator //= prime
            result -= 1
        return result
    assert valuation(physical_u,17) == 1
    assert frac_mod(physical_u/17,17) == 1
    assert (244*244-2) % (17*17) == 0
    assert k_mod(c,289,244) == k_mod(d,289,244) == 0
    assert (k_mod(c,17,11),k_mod(d,17,11)) == (2,1)
    sample_prime = 31
    residue_u = frac_mod(physical_u,sample_prime)
    assert residue_u == 9
    sample_dc = c*c/(1+residue_u*c*c)
    sample_dd = d*d/(1+residue_u*d*d)
    sample_W = ((1+sample_dc*sample_dc/residue_u)*(1+sample_dd*sample_dd/residue_u))**2
    residue_V = frac_mod(2*sample_W.inverse().a,sample_prime)
    assert residue_V == 22
    residue_V_polynomial = int(N.eval(residue_u)) % sample_prime * pow(int(D.eval(residue_u)) % sample_prime,-1,sample_prime) % sample_prime
    assert residue_V_polynomial == residue_V
    residue_w = residue_u*pow((1+residue_u)**2,-1,sample_prime) % sample_prime
    residue_C = (residue_V**2+residue_w*(2-residue_V)) % sample_prime
    assert residue_w == 19 and residue_C == 11
    assert pow(residue_C,15,31) == 30
    for field_value in (c,d):
        frac_mod(field_value.a,sample_prime)
        frac_mod(field_value.b,sample_prime)
    for balanced in (1+residue_u*c*c,1+residue_u*d*d):
        assert frac_mod((balanced*balanced.bar()).a,sample_prime) != 0
    assert frac_mod((sample_W*sample_W.bar()).a,sample_prime) != 0
    result = {
        'status':'PASS', 'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'sympy_version':sp.__version__,
        'actual_inputs':{'X':1,'B':3,'A':'P','H':'5P','U':'5P','P':[v.data() for v in P],
                         'H_coordinates':[v.data() for v in H], 'H_minus_P_coordinates':[v.data() for v in HmP],
                         'scale_a':str(scale), 'c_fH':c.data(), 'd_bar_fHmP':d.data(),
                         'tests':['c','c','d','d','0','0']},
        'integer_polynomials_ascending':{'N':coeff_data(N),'D':coeff_data(D),
                                         'A_physical':coeff_data(A),'B_physical':coeff_data(B)},
        'u_curve':'Y0^2=P(u)=N(u)^2*(1+u)^2+u*D(u)*(2D(u)-N(u))',
        'actual_trace':'V=N/D; original ordinate is Y=Y0/((1+u)D(u))',
        'physical_map':'u=A(t)/B(t), t=z^2; A/B=-18F/F_a',
        't_polynomial':'Q(t)=B(t)^50*P(A(t)/B(t)), specified by homogeneous composition',
        'good_reduction_certificate':good,
        'genera':{'u_curve':24,'t_quotient':224,'t_twist':225,'z_curve':449},
        'actual_local_example':{
            'slope':'z=a+12','u':str(physical_u),
            'real_condition':'z>a+10, u>0, all balanced factors positive at both real embeddings',
            'contact_prime':17,'v17_u':1,'u_over_17_mod_17':1,
            'successful_slot_sqrt2_mod_289':244,'c_and_d_in_successful_slot_mod_289':[0,0],
            'other_slot_c_d_mod_17':[2,1],
            'contact_trace_residue':1,'contact_radicand_residue':1,
            'obstruction_prime':31,'u_mod_31':9,'V_mod_31':22,'w_mod_31':19,
            'C_mod_31':11,'Legendre_C_mod_31':-1,
            'scope':'One split contact and the real condition only; not full retained fixed-place, prime-pattern or whole-character preparation.'},
        'jacobian_decomposition':'Jac(Y1^2=Q(z^2)) is Q-isogenous to Jac(Y1^2=Q(t)) x Jac(Y2^2=tQ(t))',
        'lift_requirement':'For each rational u-curve point, solve u*B(t)-A(t)=0 over Q; retain rational-square t and every original guard. Quotient points do not automatically lift.',
        'scope':'One fully actual rational point tuple. No enumeration of rational points, prepared rational witness, uniform obstruction or new variable count is proved.'
    }
    if args.manuscript.exists():
        result['manuscript_sha256'] = sha256(args.manuscript.read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'good_prime':good['prime'],
                      'genera':result['genera'],'certificate_bytes':args.output.stat().st_size,
                      'N_coefficient_max_bits':max(abs(int(c)).bit_length() for c in N.all_coeffs()),
                      'physical_coefficient_max_bits':max(abs(int(c)).bit_length() for c in A.all_coeffs())},indent=2))


if __name__ == '__main__':
    main()
