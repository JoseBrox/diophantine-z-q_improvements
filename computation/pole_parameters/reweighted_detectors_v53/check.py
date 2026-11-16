#!/usr/bin/env python3
"""Exact algebra and local models for the reweighted v53 source.

These checks do not verify the inherited arithmetic premises and do not
assert simultaneous rational realization of the finite square criteria.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib,json
import sympy as sy


def val(q,p):
    q=Q(q)
    if not q: raise ValueError('zero has no finite valuation')
    a,b=abs(q.numerator),q.denominator; v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v


def ppow(p,n):return Q(p**n) if n>=0 else Q(1,p**(-n))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c):return (a[0]*c,a[1]*c)
def norm(a):return a[0]**2-2*a[1]**2

def inverse(a):
    n=norm(a)
    return (a[0]/n,-a[1]/n)


def native(w,hs):
    W=(Q(1),Q(0))
    for h in hs:W=mul(W,add((Q(1),Q(0)),scale(mul(h,h),w)))
    return W


def main(output=None):
    u,R,S,C,delta,F,w,a=sy.symbols('u R S C delta F w a', nonzero=True)
    r,s,X=sy.symbols('r s X')
    old5,old6,new6=r-s,r-X,r+s-2*X
    phi=u/(1+u)**2
    identities={
      'physical_square_class':sy.cancel(phi/u-1/(1+u)**2),
      'real_physical_bound':sy.expand((1+u)**2-4*u-(1-u)**2),
      'extra_scalar_R':sy.cancel(R**(a+1)*(R*S/(1+R*S))-R*(R**a*(R*S/(1+R*S)))),
      'conditional_native_factor':sy.cancel((1+w*(C/(2*delta**4*w))**2).subs(w,F/(4*delta**8))-(1+C*C/F)),
      'comparison_forward':sy.expand(new6-(2*old6-old5)),
      'comparison_inverse':sy.expand((new6+old5)/2-old6),
      'comparison_determinant':sy.det(sy.Matrix([[1,0],[-1,2]]))-2,
    }
    assert all(v==0 for v in identities.values())
    A,B,N,g,aa=sy.symbols('A B N g aa', nonzero=True)
    V=2*A/N; J=1/N
    Qq=1-V/g+J/g**2
    criterion=Qq*(1+aa**2*(1-V/2)/w)
    displayed=(g*g*N-2*g*A+1)*((w+aa**2)*N-aa**2*A)/(w*g*g*N*N)
    assert sy.cancel(criterion-displayed)==0
    assert sy.cancel(criterion.subs({A:1,N:1,g:1+w})-w*w/(1+w)**2)==0
    identities['rational_square_criterion']=0
    identities['square_reference_value']=0
    t=sy.symbols('t')
    Ft=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
    wt=Ft/(4*(t-1)**8)
    assert Ft.subs(t,1)==7
    assert sy.limit((1/Ft)/wt**3,t,sy.oo)==64
    assert sy.limit(t*t*wt,t,sy.oo)==sy.Rational(1,4)

    primes=(5,7,11,13,19,23,31,41,73)
    weight_checks=scalar_checks=0
    for p in primes:
      for n in (-7,-5,-3,-1,0,1,3,5,7):
        for k in (1,2,-1,-2):
          x=k*ppow(p,n)
          if x==-1:continue
          wp=x/(1+x)**2
          old,new=val(x,p),val(wp,p)
          assert new%2==old%2
          if old%2:assert new==abs(old)>0
          if x>0:assert 0<wp<=Q(1,4)
          weight_checks+=1
      for kappa in (1,3):
        for order in (-7,-4,-2,0,1,4,7):
          rr=Q(p); ss=ppow(p,order)
          phim=rr*ss/(1+rr*ss)
          gp=rr**(kappa+1)*phim
          assert val(gp,p)>=kappa+1
          # At a selected fresh contact, v(w)=1.
          assert 2*val(gp,p)-(2*kappa-1)>=3
          scalar_checks+=1
      for order in range(-5,6):
        rr=Q(2); ss=ppow(p,order)
        ph=rr*ss/(1+rr*ss)
        for kappa in (1,3):
          gg=rr**(kappa+1)*ph
          assert (val(gg,p)>0)==(order>0)
          if order>0: assert val(gg,p)==order
          scalar_checks+=1

    # Native product models independently check the odd-pole criterion.
    product_checks=bad_poles=0
    sample=[]
    for p in primes:
      for n in (-3,-1,1,3):
        raw=ppow(p,n); ww=raw/(1+raw)**2
        for pole in (1,2,3):
          z=ppow(p,-pole)
          for coeff in ((1,1),(2,-1),(1,0)):
            hs=[(z*coeff[0],z*coeff[1]),(Q(1,3),Q(1,5))]
            W=native(ww,hs); inv=inverse(W)
            vv=2*inv[0]; jj=norm(inv); bb=4*ww/vv**2
            gg=1+ww; qq=1-vv/gg+jj/gg**2
            assert 0<vv<=2 and qq>0
            for parameter in (1,3):
              rad=qq*(1+parameter**2*(1-vv/2)/ww)
              assert rad>0
              vb=val(bb,p)
              if vb<0 and vb%2:
                assert val(rad,p)==-val(ww,p)
                bad_poles+=1
              sample.append((p,n,pole,coeff,parameter,str(bb),str(rad)))
              product_checks+=1
    assert bad_poles>0

    # The absolute scalar valuation lower bound and mixed-contact orders.
    order_checks=0
    for mu in range(-61,62):
      if not mu%2:continue
      alpha=abs(mu)
      assert (9*alpha)//4+1>=2*alpha+1>=3
      for test_order in (1,3):
        assert ((4*test_order-3)*alpha)//4+1>=test_order
        order_checks+=1

    certificate={
      'schema':'zq.reweighted-source.v53',
      'status':'PASS_EXACT_ALGEBRA_AND_LOCAL_MODELS',
      'symbolic_identity_names':sorted(identities),
      'weight_valuation_checks':weight_checks,
      'scalar_numerator_valuation_checks':scalar_checks,
      'local_native_product_criterion_checks':product_checks,
      'negative_odd_pole_cases':bad_poles,
      'integer_order_checks':order_checks,
      'native_product_sample_sha256':hashlib.sha256(json.dumps(sample,sort_keys=True).encode()).hexdigest(),
      'conditional_F_at_one':7,
      'conditional_limit_inverse_F_over_w_cubed':64,
      'counts':{'general':25,'conditional':13,'include_input':True},
      'new_variable_record_proved':False,
      'actual_uniform_rational_realization_proved':False,
      'numerical_determinant_degree_bound_transferred':False,
      'scope':'Symbolic identities and exact generic native-product local models. Universal source transfer is proved in the manuscript under the retained arithmetic premises; these computations do not verify those premises or prove 21/9.',
    }
    target=Path(__file__).with_name('certificate.json')
    content=(json.dumps(certificate,indent=2,sort_keys=True)+'\n').encode()
    if output is None:
        if target.read_bytes()!=content:
            raise ValueError('Reconstructed source certificate differs.')
    else:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_bytes(content)
        target=output
    print(json.dumps({'status':'pass','certificate':str(target),'sha256':hashlib.sha256(content).hexdigest(),
                      'checks':product_checks,'bad_poles':bad_poles},sort_keys=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,
                        help='Write a reconstructed certificate instead of comparing the stored one.')
    main(parser.parse_args().output)
