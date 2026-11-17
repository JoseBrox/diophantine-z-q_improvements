#!/usr/bin/env python3
"""Independent affine mod-p^2 audit of the actual raw-abscissa fixture.

No producer module or projective arithmetic is imported. Every affine
inverse used over Z/p^2 Z is checked to be a unit first.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd,isqrt
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent

def point_add(P,R,A,m,p):
    if P is None:return R
    if R is None:return P
    x,y=P;z,t=R
    if x==z:
        if (y+t)%m==0:return None
        den=2*y%m;num=(3*x*x+A)%m
    else:den=(z-x)%m;num=(t-y)%m
    assert gcd(den,p)==1,(P,R,den)
    slope=num*pow(den,-1,m)%m
    xx=(slope*slope-x-z)%m;yy=(slope*(x-xx)-y)%m
    assert (yy*yy-xx**3-A*xx)%m==0
    return xx,yy

def point_mul(n,P,A,m,p):
    result=None
    while n:
        if n&1:result=point_add(result,P,A,m,p)
        n//=2;P=point_add(P,P,A,m,p)
    return result

def main():
    data=json.loads((HERE/'certificate.json').read_text());p=data['p'];m=p*p
    assert p==76777 and all(p%d for d in range(2,isqrt(p)+1))
    r=s.symbols('r');modulus=s.Poly(r*r-2,r,domain=s.QQ)
    def fld(expr):
        num,den=s.fraction(s.cancel(expr))
        n=s.rem(s.Poly(num,r,domain=s.QQ),modulus)
        d=s.rem(s.Poly(den,r,domain=s.QQ),modulus)
        return s.rem(n*s.invert(d,modulus),modulus).as_expr()
    x=s.Rational(57,8)-s.Rational(7,2)*r
    y=-s.Rational(165,8)+s.Rational(417,32)*r
    D=11-6*r
    assert fld(y*y-x*x*x+D*x)==0
    slope=fld((3*x*x-D)/(2*y));x2=fld(slope*slope-2*x)
    T=s.expand(x2+x2.subs(r,-r));assert T==s.Rational(data['root_trace_T'])
    M=s.Rational(7)**4+T**4;a=M**4
    assert a==s.Rational(data['scale_a']) and M==s.Rational(data['scale_M'])
    z=int(data['slope_z']);assert z>a+100
    assert Q(101,100)**4*(1+Q(1,1000000))**2<Q(11,10)
    assert z%p==21480
    am=int(a.p)%m*pow(int(a.q)%m,-1,m)%m
    shifts=(-10,-8,-5,1,2,3,4,6,7)
    factors=[((am+c)**2-z*z)%m for c in shifts]
    F=1
    for value in factors:F=F*value%m
    Fa=0
    for i,c in enumerate(shifts):
        term=2*(am+c)%m
        for j,value in enumerate(factors):
            if i!=j:term=term*value%m
        Fa=(Fa+term)%m
    assert F%p==data['F_mod_p']==44843
    assert Fa==data['Fa_mod_p2']==169753947
    assert Fa%p==0 and Fa%m!=0
    e=-18*(F%p)*pow((Fa//p)%p,-1,p)%p
    assert e==data['physical_u_times_p_mod_p']==66932
    roots=[];xunits=[]
    for entry in data['point_valuations']:
        rho=entry['sqrt2_mod_p2'];assert rho*rho%m==2
        dd=(11-6*rho)%m
        P=((57-28*rho)*pow(8,-1,m)%m,(-660+417*rho)*pow(32,-1,m)%m)
        assert (P[1]*P[1]-P[0]**3+dd*P[0])%m==0
        HminusP=point_mul(10335,P,-dd,m,p)
        assert list(HminusP)==entry['HminusP_affine_mod_p2']
        assert HminusP[0]==0 and HminusP[1]%p==0 and HminusP[1]%m!=0
        xi=-(HminusP[1]//p)**2*pow(dd%p,-1,p)%p
        assert xi==entry['x_over_p2_mod_p'];xunits.append(xi)
        Pp=(P[0]%p,P[1]%p);aa=-dd%p
        H=point_mul(10336,Pp,aa,p,p)
        U=point_mul(20672,Pp,aa,p,p)
        A=point_mul(2,Pp,aa,p,p)
        assert H[0]==entry['H_abscissa_mod_p'] and U[0]==entry['U_abscissa_mod_p']
        assert H[0] and U[0] and U==A
        assert point_mul(20670,Pp,aa,p,p) is None
        roots.append(rho)
    assert sum(roots)%m==0
    cases=[]
    for power,expected in zip([1,2],data['candidate_raw_factors']):
        lead=e*sum(pow(xi,power,p) for xi in xunits)%p
        assert lead==expected['trace_leading_coefficient_mod_p'] and lead!=0
        assert expected['trace_valuation']==2*power-1
        assert expected['b_valuation']==3-4*power
        assert expected['actual_trace_radicand_valuation']==1
        cases.append(dict(power=power,trace_leading_coefficient_mod_p=lead,
            trace_valuation=2*power-1,b_valuation=3-4*power,radicand_valuation=1))
    result=dict(status='PASS',scope=__doc__,certificate_sha256=sha256((HERE/'certificate.json').read_bytes()).hexdigest(),
        exact_root_trace=str(T),independent_affine_multiplications=2,
        all_mod_p2_affine_denominators_units=True,independent_contact_derivative=True,
        raw_cases=cases,full_preparation_claimed=False,global_completeness_failure_claimed=False)
    (HERE/'independent_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
