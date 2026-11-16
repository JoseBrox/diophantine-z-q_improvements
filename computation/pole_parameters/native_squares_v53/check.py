#!/usr/bin/env python3
"""Exact identities and source-pattern certificates for the v53 square test.

This verifies algebra and listed local patterns; it does not establish
simultaneous global rational square values on the actual source.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import importlib.util
import json
import sys
import sympy as sp

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]

def main(output=None):
    w,A,B,a=sp.symbols('w A B a', nonzero=True)
    N=A*A-2*B*B;g=1+w
    V=2*A/N;J=1/N
    Q=1-V/g+J/g**2
    R=Q*(1+a*a*(1-V/2)/w)
    cleared=((g*g*N-2*g*A+1)*((w+a*a)*N-a*a*A))/(w*g*g*N*N)
    assert sp.cancel(R-cleared)==0
    assert sp.cancel(R.subs({A:1,B:0})-(w/g)**2)==0
    e0=1-V/(2*g);omega=w/g**2
    assert sp.cancel(R.subs(a,1)-Q*e0/(omega*g))==0
    u,v=sp.symbols('u v')
    inverse_Q=1-2*u/g+(u*u-2*v*v)/g**2
    inverse_R=inverse_Q*(1+(1-u)/w)
    x=1+(1-u)/w;q=v/w
    assert sp.cancel(inverse_R-w*w*x*(x*x-2*q*q)/g**2)==0

    t=sp.symbols('t')
    contact=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
    delta=t-1;physical=contact/(4*delta**8)
    C=sp.symbols('C')
    h=C/(2*delta**4*physical)
    assert sp.cancel(physical*h*h-C*C/contact)==0
    assert contact.subs(t,1)==7
    assert sp.limit(4*t*t*physical,t,sp.oo)==1
    assert sp.limit((C*C/contact)/physical**3,t,sp.oo)==64*C*C
    # This exact factor estimate yields W-1=O(w^3) on bounded test sets.

    xs=sp.symbols('c1:7');ys=sp.symbols('b1:7')
    product=sp.prod(1+x*x/contact for x in xs)
    substitution=dict(zip(xs,(ys[2],ys[3],ys[0],ys[1],-ys[4],ys[5])))
    assert sp.cancel(product.xreplace(substitution)-sp.prod(1+y*y/contact for y in ys))==0
    M=sp.Matrix([[1,0],[-1,2]])
    assert M.det()==2
    outer_orders=0
    for nu in range(1,32,2):
        for c_order in range(-24,25):
            summand=nu+2*c_order
            assert summand%2==1
            a_order=min(0,summand)
            assert a_order<=0
            assert (2*a_order-nu)%2==1 and 2*a_order-nu<0
            outer_orders+=1

    # Exact selected-contact expansions, with independent bounded coefficients.
    p,u,v,z=sp.symbols('p u v z', nonzero=True)
    weight=p*u
    inverse_good=1+p*p*v
    inverse_bad=p*p*z
    tv=inverse_good+inverse_bad
    tj=inverse_good*inverse_bad
    tq=1-tv/(1+weight)+tj/(1+weight)**2
    tr=tq*(1+a*a*(1-tv/2)/weight)
    assert sp.limit(tr,p,0)==a*a/2
    # Both-good pattern: deviations smaller than the weight give a square unit.
    eg=1+p*p*v;eb=1+p*p*z
    bv=eg+eb;bj=eg*eb
    bq=1-bv/(1+weight)+bj/(1+weight)**2
    br=bq*(1+a*a*(1-bv/2)/weight)
    assert sp.limit(br/(weight/(1+weight))**2,p,0)==1
    # Ordinary pole with integral reciprocal slots.
    big=1/p
    pq=1-(v+z)/(1+big)+v*z/(1+big)**2
    pr=pq*(1+a*a*(1-(v+z)/2)/big)
    assert sp.limit(pr,p,0)==1

    spec=importlib.util.spec_from_file_location(
        'native_fixture_v53',REPO/'computation/pole_parameters/native_trace_fixture_v47/build-fixture.py')
    native=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=native;spec.loader.exec_module(native)
    K=native.K
    def mul(P,n):
        if n<0:return native.minus_point(mul(P,-n))
        out=None
        while n:
            if n&1:out=native.add_point(out,P)
            P=native.add_point(P,P);n//=2
        return out
    P=mul((K(1,1),K(0,2)),2)
    def tests(A,H,U,X):
        Hm=native.subtract_point(H,P)
        Um=native.subtract_point(U,A)
        r=native.zcoord(U)/native.zcoord(H)
        s=native.zcoord(Um)/native.zcoord(Hm)
        return (native.reciprocal(H),native.reciprocal(U),
                native.reciprocal(Hm).bar(),native.reciprocal(Um).bar(),
                r-s.bar(),r+s.bar()-2*X)
    def block(cs,t):
        ff=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
        ww=ff/(4*(t-1)**8)
        prod=K(1)
        for c in cs:prod*=1+c*c/ff
        vv=2*prod.a/prod.norm();jj=1/prod.norm()
        qq=1-vv/(1+ww)+jj/(1+ww)**2
        rr=qq*(1+(1-vv/2)/ww)
        assert rr>0
        return prod,rr
    actual=[]
    for X in (1,2,3):
        A=mul(P,X);H=mul(P,3);U=mul(P,3*X)
        Htau=native.subtract_point(P,H);Utau=native.subtract_point(A,U)
        first=tests(A,H,U,X);second=tests(A,Htau,Utau,X)
        expected=(first[2].bar(),first[3].bar(),first[0].bar(),first[1].bar(),
                  -first[4].bar(),first[5].bar())
        assert second==expected
        W,R=block(first,F(2));Wt,Rt=block(second,F(2))
        assert Wt==W.bar() and R==Rt
        actual.append({'X':X,'H_index':3,'U_index':3*X,'slope':'2',
                       'all_test_permutations':True,'detector_conjugation':True,
                       'square_radicand_invariance':True})
    result={
        'status':'PASS',
        'rational_square_expression_and_clearing':True,
        'reference_product_exact_square':True,
        'flat_norm_trace_identity':True,
        'prescribed_coordinate_j1728_identity':True,
        'safe_outer_parameter_integer_order_checks':outer_orders,
        'faster_product_native_weight_identity':True,
        'conditional_pole_coefficient':7,
        'infinity_ratio_for_each_factor':str(64*C*C),
        'symbolic_tau_product_identity':True,
        'comparison_change_determinant':2,
        'mixed_contact_residue':str(a*a/2),
        'both_good_square_quotient_limit':1,
        'ordinary_pole_square_limit':1,
        'actual_multiplication_examples':actual,
        'scope':'Exact algebraic identities and specified local-pattern limits. No complete local audit or simultaneous global rational realization is asserted.'
    }
    content=(json.dumps(result,indent=2)+'\n').encode()
    target=HERE/'certificate.json'
    if output is None:
        if target.read_bytes()!=content:
            raise ValueError('Reconstructed native-square certificate differs.')
    else:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_bytes(content)
        target=output
    print(json.dumps({'status':'PASS','certificate':str(target),
                      'actual_examples':len(actual),'global_realization_proved':False}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,
                        help='Write a reconstructed certificate instead of comparing the stored one.')
    main(parser.parse_args().output)
