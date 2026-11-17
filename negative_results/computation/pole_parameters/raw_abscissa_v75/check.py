#!/usr/bin/env python3
"""Actual physical failure of automatic preparation after raw abscissa replacement.

The two specified raw variants retain balanced comparison factors. This
is a finite actual-tuple obstruction, not a global completeness result.
"""
from pathlib import Path
import importlib.util,sys,json,hashlib
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3]
p=76777;mod=p*p
assert all(p%d for d in range(2,int(p**0.5)+1))

def jdouble(P,A,m):
 X,Y,Z=P
 if Z%m==0 or Y%m==0:return(1,1,0)
 YY=Y*Y%m;YYYY=YY*YY%m;ZZ=Z*Z%m
 S=4*X*YY%m;M=(3*X*X+A*ZZ*ZZ)%m
 return((M*M-2*S)%m,(M*(S-(M*M-2*S))-8*YYYY)%m,2*Y*Z%m)
def jadd(P,Q,A,m):
 if P[2]%m==0:return Q
 if Q[2]%m==0:return P
 X,Y,Z=P;x,y,z=Q
 Z2=Z*Z%m;z2=z*z%m
 U=X*z2%m;u=x*Z2%m;S=Y*z*z2%m;s=y*Z*Z2%m
 H=(u-U)%m;R=(s-S)%m
 assert not (H%p==0 and R%p==0) or (H==0 and R==0), (P,Q,H,R)
 if H==0 and R==0:return jdouble(P,A,m)
 HH=H*H%m;HHH=H*HH%m;V=U*HH%m
 xx=(R*R-HHH-2*V)%m;yy=(R*(V-xx)-S*HHH)%m;zz=H*Z*z%m
 return xx,yy,zz

def jvalid(P,A,m):
 X,Y,Z=P
 assert (Y*Y-X*X*X-A*X*pow(Z,4,m))%m==0
 assert any(c%p for c in P), P

def jmul(n,P,A,m):
 Q=(1,1,0)
 jvalid(P,A,m)
 while n:
  if n&1:
   Q=jadd(Q,P,A,m);jvalid(Q,A,m)
  n//=2;P=jdouble(P,A,m);jvalid(P,A,m)
 return Q

def affine(P,m):
 X,Y,Z=P;iz=pow(Z,-1,m);return X*iz*iz%m,Y*iz*iz*iz%m

r=13251
r2=(r+p*((-(r*r-2)//p)*pow(2*r,-1,p)%p))%mod
assert r2*r2%mod==2
local=[]
for rr in [r2,(-r2)%mod]:
 D=(11-6*rr)%mod
 P=((57-28*rr)*pow(8,-1,mod)%mod,(-660+417*rr)*pow(32,-1,mod)%mod,1)
 Hm=affine(jmul(10335,P,-D,mod),mod)
 assert Hm[0]%mod==0 and Hm[1]%p==0 and Hm[1]%mod!=0
 local.append({'sqrt2_mod_p2':rr,'HminusP_affine_mod_p2':Hm,'v_y':1,'v_x':2,'v_inverse_x':-2})
path=REPO/'computation/pole_parameters/actual_trace_arithmetic_v70/check.py'
sp=importlib.util.spec_from_file_location('raw_fixture_field',path);ff=importlib.util.module_from_spec(sp);sys.modules[sp.name]=ff;sp.loader.exec_module(ff)
A=ff.point_mul(2,ff.P);T=2*A[0].a;M=F(7)**4+T**4;a=M**4
am=a.numerator%mod*pow(a.denominator%mod,-1,mod)%mod
shifts=(-10,-8,-5,1,2,3,4,6,7)
def evals(z,m):
 G,H=1,0
 for c in shifts:
  fac=((am+c)**2-z*z)%m
  H=(H*fac+G*(am+c))%m;G=G*fac%m
 return G,2*H%m
chosen=None
for z0 in [21480,21480+p]:
 G,Fa=evals(z0,mod)
 if G%p and Fa%p==0 and Fa%mod:
  chosen=z0;break
assert chosen is not None
z=chosen+mod*(int((a+11-F(chosen))/mod)+1)
assert F(z)>a+100
assert F(101,100)**4*(1+F(1,1000000))**2<F(11,10)
G,Fa=evals(z,mod)
assert G%p and Fa%p==0 and Fa%mod
report={'p':p,'n':2,'B':3,'A':'2P','H':'10336P','U':'20672P','sqrt2_mod_p':r,
 'root_trace_T':str(T),'scale_M':str(M),'scale_a':str(a),'slope_z':str(z),'slope_residue_mod_p':z%p,'F_mod_p':G%p,'Fa_mod_p2':Fa,
 'v_physical_u':-1,'point_valuations':local,
 'raw_unsquared_abscissa_factor_valuation':-1,'reciprocal_product_slot_valuation_lower_bound':1,
 'negative_odd_b_valuation_for_any_nonzero_trace':True,
 'scope':'Exact actual multiplication tuple with real slope z>a+100. No selected-prime factorization or full preparation assertion. Shows that raw first-four factors do not automatically prepare all actual derivative denominator primes.'}
uunit=-18*(G%p)*pow((Fa//p)%p,-1,p)%p
xunits=[]
for item in local:
    rho=item['sqrt2_mod_p2']%p;DD=(11-6*rho)%p
    yy=item['HminusP_affine_mod_p2'][1]//p
    xunit=-yy*yy*pow(DD,-1,p)%p
    item['x_over_p2_mod_p']=xunit;xunits.append(xunit)
    # H=P+T0 and U=2H=A in both residue slots, while U-A=O.
    PP=((57-28*rho)*pow(8,-1,p)%p,(-660+417*rho)*pow(32,-1,p)%p,1)
    HH=affine(jmul(10336,PP,-DD,p),p)
    UU=affine(jmul(20672,PP,-DD,p),p)
    AA=affine(jmul(2,PP,-DD,p),p)
    assert HH[0] and UU[0] and UU==AA
    item['H_abscissa_mod_p']=HH[0];item['U_abscissa_mod_p']=UU[0]
raw=[]
for e in [1,2]:
    leading=uunit*sum(pow(x,e,p) for x in xunits)%p
    assert leading
    raw.append(dict(first_four_factor='1+C^%d/u'%e,
        comparison_factor='1+(C^2/(1+u*C^2))^2/u',
        raw_pole_factor_valuation=1-2*e,
        reciprocal_product_slot_valuation=2*e-1,
        trace_leading_coefficient_mod_p=leading,
        trace_valuation=2*e-1,b_valuation=3-4*e,
        actual_trace_radicand_valuation=1))
report.update(status='PASS',p_squared=mod,physical_u_times_p_mod_p=uunit,
    candidate_raw_factors=raw,real_bounds={'u_lower_bound':100,'slot_product_upper_bound':'11/10','trace_lower_bound':'20/11','eta_upper_bound':'847/10000'},producer_field_dependency_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    guards_established=['all pre-pole point, difference and quotient guards at every point character',
        'M,t,F,Fa,u,1+u nonzero','balanced comparison denominator norms nonzero',
        'raw product and trace norms nonzero','positive real u and all raw factors in both embeddings'],
    preparation_not_established=['selected contact-prime factorization','fixed finite-place pole preparation',
        'a sufficient defining shift','global raw-source completeness or failure'])
(HERE/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
