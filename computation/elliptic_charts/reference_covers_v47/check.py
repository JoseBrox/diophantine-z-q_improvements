#!/usr/bin/env python3
"""Exact identities for quadratic reference covers and numerator charts.

Default verification prints JSON and does not change any artifact. Use
--output PATH only when explicitly generating a receipt.
"""
import argparse
import json
from pathlib import Path
import sympy as S


def build_receipt():
    checks = {}
    def zero(name, expression):
        checks[name] = S.cancel(S.expand(expression)) == 0
    def ideal_zero(name, basis, expression):
        checks[name] = S.expand(basis.reduce(S.expand(expression))[1]) == 0

    e,c=S.symbols('e c')
    a=e**2
    D=a*(a-c*c)
    delta=a-c*c
    domain=S.QQ.frac_field(e,c)
    r,rp,z=S.symbols('r rp z')
    R,Q,s,t=S.symbols('R Q s t')
    cover3=[z-r*rp, a*(r*r+rp*rp)+2*c*e*z+D*z*z-1]
    cover4=[s*s+D*R*R-1, t*t+D*Q*Q-1,
            c*e*s*t+a-D*(R+Q)-a*D*R*Q]
    G3=S.groebner(cover3,rp,r,z,domain=domain)
    G4=S.groebner(cover4,s,t,Q,R,domain=domain)
    forward={R:r*r,Q:rp*rp,
             s:e*rp+c*r+(D/e)*r*z,
             t:-e*r-c*rp-(D/e)*rp*z}
    inverse={r:-(t/e+e*R*t+c*Q*s)/2,
             rp:(s/e+c*R*t+e*Q*s)/2,
             z:(1-a*(R+Q)-D*R*Q)/(2*c*e)}
    for i,p in enumerate(cover4):
        ideal_zero(f'cover_forward_equation_{i}',G3,p.subs(forward,simultaneous=True))
    for i,p in enumerate(cover3):
        ideal_zero(f'cover_inverse_equation_{i}',G4,p.subs(inverse,simultaneous=True))
    for x in [r,rp,z]:
        ideal_zero(f'cover_composition_{x}',G3,
                   inverse[x].subs(forward,simultaneous=True)-x)
    for x in [R,Q,s,t]:
        ideal_zero(f'cover_composition_{x}',G4,
                   forward[x].subs(inverse,simultaneous=True)-x)

    ell=e*z
    J=ell**2
    alpha=1-a*r*r-c*ell
    gamma=alpha-delta*J-1
    ideal_zero('compact_reference_equation',G3,
               alpha*gamma+c*ell*(1-delta*J)+2*delta*J)
    ideal_zero('reference_reciprocal_H',G3,1-alpha-c*ell-a*r*r)
    ideal_zero('reference_reciprocal_translate',G3,alpha-delta*J-c*ell-a*rp*rp)
    ideal_zero('reference_scaled_ordinate_H',G3,alpha*r-ell*forward[s])
    ideal_zero('reference_scaled_ordinate_translate',G3,gamma*rp-ell*forward[t])
    for sign in [-1,1]:
        for label,point in [
            ('H_identity',{R:0,Q:1/a,s:sign,t:-sign*c/e}),
            ('H_equals_P',{R:1/a,Q:0,s:sign*c/e,t:-sign})]:
            for i,p in enumerate(cover4):
                zero(f'boundary_{label}_{sign}_{i}',p.subs(point))

    beta,b2,b4=S.symbols('beta b2 b4')
    Rh,Qh,Sh,Th=S.symbols('Rh Qh Sh Th')
    scaled=[Sh**2+D*Rh**2-b4,Th**2+D*Qh**2-b4,
            c*e*Sh*Th+a*b4-D*b2*(Rh+Qh)-a*D*Rh*Qh]
    subscale={Rh:beta**2*R,Qh:beta**2*Q,Sh:beta**2*s,
              Th:beta**2*t,b2:beta**2,b4:beta**4}
    for i,p in enumerate(scaled):
        zero(f'homogeneous_reference_scaling_{i}',
             p.subs(subscale,simultaneous=True)-beta**4*cover4[i])
    checks['all_reference_equations_are_quadratic'] = all(
        S.Poly(p,*[r,rp,z]).total_degree()<=2 for p in cover3) and all(
        S.Poly(p,R,Q,s,t).total_degree()<=2 for p in cover4) and all(
        S.Poly(p,Rh,Qh,Sh,Th,b2,b4).total_degree()<=2 for p in scaled)

    q,zu=S.symbols('q zu')
    RR=beta**2*r*r
    SS=beta**2*s
    kk=beta*r*q
    FF=RR*q*q
    ZZ=RR*zu
    ll=beta*q*s/(r*zu)
    zero('numerator_square',FF-kk*kk)
    zero('numerator_circle',ZZ*ZZ+D*FF*FF-RR*RR-RR*RR*(zu*zu+D*q**4-1))
    zero('numerator_scaled_ratio',ZZ*ll-kk*SS)
    zero('numerator_physical_product',FF-beta**2*r*r*q*q)
    zero('numerator_physical_ratio',ll/beta-(-q/zu)/(-r/s))

    u,v,su,sv,DD=S.symbols('u v su sv DD')
    Gj=S.groebner([su*su+DD*u**4-1,sv*sv+DD*v**4-1],
                  su,sv,u,v,domain=S.QQ.frac_field(DD))
    chord_numerator=(su*v**3+sv*u**3)**2-(u*u+v*v)*(v*v-u*u)**2
    chord_denominator=u*u*v*v*(v*v-u*u)**2
    ideal_zero('jacobi_difference_abscissa',Gj,
               chord_numerator*(u*sv-v*su)**2-
               chord_denominator*(1+DD*u*u*v*v)**2)
    fu,fv,zu,zv=S.symbols('fu fv zu zv')
    e1=zu*zu+DD*fu*fu-1
    e2=zv*zv+DD*fv*fv-1
    e3=1+DD*fu*fv
    zero('zero_height_sum_of_squares',
         zu*zu+DD*fu*fu*zv*zv-(e1+DD*fu*fu*e2-(DD*fu*fv-1)*e3))
    d=S.symbols('d',nonzero=True)
    for sign in [-1,1]:
        point={DD:d*d,fu:sign/d,fv:-sign/d,zu:0,zv:0}
        for i,p in enumerate([e1,e2,e3]):
            zero(f'zero_height_boundary_{sign}_{i}',p.subs(point,simultaneous=True))

    h0,h1,TT,PP,rho=S.symbols('h0 h1 TT PP rho')
    H=TT/2+2*rho*PP
    zero('trace_compression',S.rem(
         (h0+rho*h1)**2-H.subs({TT:2*(h0*h0+2*h1*h1),PP:h0*h1}),
         rho*rho-2,rho))
    rho2=S.sqrt(2)
    ee=-1+7*rho2/4
    aa=S.Rational(57,8)-S.Rational(7,2)*rho2
    cc=-S.Rational(87,41)+S.Rational(129,164)*rho2
    dd=3-rho2
    checks['project_e_square']=S.simplify(ee*ee-aa)==0
    checks['project_curve_constants']=S.simplify(aa*(aa-cc*cc)-dd*dd)==0
    checks['norm_generator_class']=S.expand((1+rho2)*(1-rho2))==-1
    checks['norm_torsion_class']=S.expand(dd*(3+rho2))==7
    checks['norm_inverse_torsion_class']=S.simplify(1/(dd*(3+rho2)))==S.Rational(1,7)
    assert all(checks.values()),[k for k,v in checks.items() if not v]
    return {
        'status':'PASS','checks':checks,'passed':len(checks),
        'counts':{
            'three_coordinate_reference':{'rational_coordinates':6,'rational_quadrics':4},
            'four_coordinate_reference':{'rational_coordinates':8,'rational_quadrics':6},
            'one_numerator_with_ratio':{'point_rational_coordinates':6,'ratio_rational_coordinates':2,
                                        'rational_quadrics':6},
            'jacobi_pair_with_original_trace':{'rational_coordinates_including_trace':16,
                                              'rational_quadrics':12}},
        'scope':('Exact chart, scaling, numerator and Jacobi identities. '
                 'No complete defining polynomial or improved variable count is asserted. '
                 'The Kummer-image and formal-reality arguments are proved in the manuscript.')}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    data=json.dumps(build_receipt(),indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(data)
    else:
        print(data,end='')


if __name__=='__main__':
    main()
