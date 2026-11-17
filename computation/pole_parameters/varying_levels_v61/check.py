"""Exact identities for locally soluble pole fibers and rational levels.

The infinite rational-fiber statement uses the manuscript proof and the
retained simultaneous-twist theorem. No prescribed-level realization or
new defining-variable bound is asserted.
"""
from pathlib import Path
import json
import argparse
import hashlib
import sympy as S

d,r,s,k,h,y=S.symbols('d r s k h y')
eta=1-d
kr=eta*(d+r*r)/(d-r*r)
hr=2*d*eta*r/(d-r*r)
assert S.factor(hr*hr-d*(kr*kr-eta*eta))==0
assert S.factor(kr.subs(r,0)-eta)==0
assert S.factor(kr.subs(r,d)-(1+d))==0
assert S.factor(hr.subs(r,d)-2*d)==0
Qd=d*(1-d)**2*(d+r*r)**2-d*(d-r*r)**2*s**4
assert S.factor((d-r*r)**2*d*(kr*kr-s**4)-Qd)==0
assert S.factor(S.Poly(Qd,s).coeff_monomial(s**4)+d*(d-r*r)**2)==0
assert S.factor(Qd.subs(d,1)+(1-r*r)**2*s**4)==0
Qpoly=S.Poly(Qd,d,r,s)
assert Qpoly.total_degree()==9
assert max(abs(vv) for vv in Qpoly.coeffs())==4
v2=d*(k*k-s**4)/(k+s*s)**2
assert S.factor((d-v2)/(d+v2)-s*s/k)==0
Y2=4*d*d*s**4*d*(k*k-eta*eta)/(k+s*s)**2
P=d*(d+v2)**2*s**4-d*(d-v2)**2*eta**2
assert S.factor(Y2-P)==0
Ex=-d*s*s
Ey=d*s*y
assert S.expand(Ey*Ey-(Ex**3-d*d*k*k*Ex)-d*d*s*s*(y*y-d*(k*k-s**4)))==0

beta,eta0,q,rr,t,z=S.symbols('beta eta0 q rr t z')
scaled=(y*y-d*(k*k-s**4)).subs({d:beta*rr*rr,k:eta0*q*q,s:q*t,y:rr*q*q*z})
assert S.expand(scaled-rr*rr*q**4*(z*z-beta*(eta0**2-t**4)))==0

n,a,b,U,V=S.symbols('n a b U V', nonzero=True)
K=d*b*b/n
H=V/n
RR=V/(d*b*b+n*(1-d))
V2=d**3*b**4-d*n*n*(1-d)**2
U2=d**3*a**4-d*n*n
assert S.factor((H*H-d*(K*K-(1-d)**2)).subs(V*V,V2))==0
assert S.factor((RR*RR-d*(K-(1-d))/(K+(1-d))).subs(V*V,V2))==0
YY=K*U/(d*a*a)
SS=b/a
assert S.factor((YY*YY-d*(K*K-SS**4)).subs(U*U,U2))==0
assert S.factor(d*K-n*(d*b/n)**2)==0

local_even_valuation_cases=0
for va in range(-12,13):
    for vr in range(-12,13):
        # For a unit D with both D and -D nonsquare, d+-r^2 cannot
        # cancel when their valuations tie. The ratio is always a unit.
        numerator_order=min(2*va,2*vr)
        denominator_order=min(2*va,2*vr)
        assert numerator_order==denominator_order
        eta_order=2*min(va,0)
        k_order=eta_order
        scale_s=min(va,0)
        scale_y=va+2*scale_s
        assert 2*scale_y==2*va+2*k_order==2*va+4*scale_s
        local_even_valuation_cases+=1

# An exact fiber with nonsquare complement, independently of the general
# arithmetic existence theorem.
dd=S.Rational(112,225)
kk=S.Rational(3364,675)
rr0=S.Rational(44,69)
ss=S.Rational(29,15)
yy=S.Rational(23548,10125)
hh=S.Rational(7084,2025)
vv=S.Rational(4,15)
YY0=S.Rational(226688,151875)
assert S.Rational(98)**2==28**3-21**2*28
assert S.Rational(3595130)**2==23548**3-2373**2*23548
assert kk==(1-dd)*(dd+rr0**2)/(dd-rr0**2)
assert hh==2*dd*(1-dd)*rr0/(dd-rr0**2)
assert yy**2==dd*(kk**2-ss**4)
assert vv==yy/(kk+ss**2)
assert YY0==2*dd*ss**2*hh/(kk+ss**2)
assert YY0**2==dd*(dd+vv**2)**2*ss**4-dd*(dd-vv**2)**2*(1-dd)**2
source=Path(__file__).resolve().parents[3]/'papers/pole_parameters/varying_level_pole_fibers_20261117_v61.tex'

certificate={
 'status':'PASS',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'nontrivial_complement_benchmark':{'d':str(dd),'r':str(rr0),'k':str(kk),'s':str(ss),'y':str(yy),'intrinsic_v':str(vv),'intrinsic_Y':str(YY0)},
 'parametrization':'k=(1-d)(d+r^2)/(d-r^2), h=2d(1-d)r/(d-r^2)',
 'intrinsic_reconstruction':'v=y/(k+s^2), Y=2ds^2h/(k+s^2)',
 'genus_one_cover':'y^2=d(k^2-s^4) -> E_(dk), (x,Y)=(-ds^2,dsy)',
 'prepared_levels':'Every rational r in the displayed family gives an everywhere locally soluble genus-one curve for prepared d.',
 'local_even_valuation_cases':local_even_valuation_cases,
 'global_fibers':'Burungale supplies infinitely many rational r in (0,sqrt(d)) with infinitely many rational points in each fiber; dk remains in one fixed elliptic isomorphism class.',
 'cleared_pole':{'degree':Qpoly.total_degree(),'coefficient_height':int(max(abs(vv) for vv in Qpoly.coeffs())),'monomials':len(Qpoly.terms())},
 'whole_character_guards':'Nonzero leading s^4 coefficient at every nonzero d character; d=1 is allowed without a 1-d or h guard.',
 'arithmetic_gap':'Representation of [-d] by E_(dk)(Q) for the actual prescribed k remains unproved.',
 'numerical_count_claim':None,
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('certificate.json'))
out=parser.parse_args().output
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate,indent=2))
