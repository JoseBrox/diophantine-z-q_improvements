#!/usr/bin/env python3
"""Genus-twelve even-valuation actual weight cover and degree-seven physical lifting.

The fixed tuple X=1, B=3, A=P, H=U=P/2 uses the full auxiliary
charts. This certificate proves identities and genera, not rational
realization or complete preparation for this fixed tuple.
"""
from __future__ import annotations
from fractions import Fraction as Q
from functools import reduce
from pathlib import Path
from math import gcd,lcm
import argparse,hashlib,importlib.util,json,sys
import sympy as s

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('halfpoint_field_v70',REPO/'computation/pole_parameters/actual_trace_arithmetic_v70/check.py')
field=importlib.util.module_from_spec(spec);sys.modules[spec.name]=field;spec.loader.exec_module(field)
K=lambda a=0,b=0:field.K(Q(a),Q(b))

def coeffs(poly):return [str(c) for c in reversed(poly.all_coeffs())]
def modpoly(poly,p):return s.Poly.from_list([int(c)%p for c in poly.all_coeffs()],poly.gens[0],modulus=p)
def ints(A,B):
    d=lcm(*(int(c.q) for f in (A,B) for c in f.all_coeffs()))
    A=s.Poly(d*A.as_expr(),*A.gens,domain=s.ZZ);B=s.Poly(d*B.as_expr(),*B.gens,domain=s.ZZ)
    c=reduce(gcd,(abs(int(x)) for f in (A,B) for x in f.all_coeffs()))
    return A.exquo_ground(c),B.exquo_ground(c)
def compose(poly,A,B,p):
    result=s.Poly(0,A.gens[0],modulus=p);n=poly.degree()
    for i,c in enumerate(reversed(poly.all_coeffs())):result+=(int(c)%p)*A**i*B**(n-i)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--contacts',type=int,choices=[7,9],default=7)
    args=ap.parse_args();contacts=args.contacts
    H=(K(1,1),K(0,2));P=field.P
    assert field.on_curve(H) and field.point_add(H,H)==P
    HminusP=field.point_add(H,(P[0],-P[1]))
    assert HminusP==(H[0],-H[1])
    assert H[0]!=P[0] and H[0]!=K() and H[1]!=K()
    c=1/H[0];assert c==K(-1,1)
    tests=(c,c,c.bar(),c.bar(),K(),K())
    u,t=s.symbols('u t')
    D=s.Poly(u**2*(1-2*u-u*u)**2,u)
    R=D+s.Poly(2*u**3+4*u*u+6*u+1,u)
    Pi=4*D**4*s.Poly((u+1)**2,u)+2*s.Poly(u,u)*R**2*(R**2-D**2)
    assert Pi.degree()==26 and Pi.LC()==4 and Pi.eval(0)==0 and Pi.diff().eval(0)==2
    assert s.gcd(R,D).degree()==0 and s.gcd(Pi,Pi.diff()).degree()==0
    # R is monic with constant term 1. Its only possible rational roots are +/-1.
    assert R.LC()==1 and R.TC()==1 and R.eval(1)!=0 and R.eval(-1)!=0
    assert s.discriminant(1-2*u-u*u,u)==8
    samples=[]
    for value in [Q(1),Q(2),Q(-2),Q(1,3)]:
        W=K(1)
        for index,C in enumerate(tests):
            Di=(C/(1+value*C) if index<4 else C*C/(1+value*C*C))
            W*=1+Di*Di/value
        normJ=Q(int(R.eval(s.Rational(value.numerator,value.denominator)).p),int(R.eval(s.Rational(value.numerator,value.denominator)).q))/Q(D.eval(s.Rational(value.numerator,value.denominator)))
        assert W.b==0 and W.a==normJ**2
        V=2/W.a
        assert V==2/normJ**2
        rad=V*V+value/(1+value)**2*(2-V)
        uu=s.Rational(value.numerator,value.denominator)
        predicted=Q(Pi.eval(uu))/((1+value)**2*Q(R.eval(uu))**4)
        assert rad==predicted
        samples.append(dict(u=str(value),J=str(normJ),V=str(V),radicand=str(rad)))
    shifts=((-7,-6,-4,1,3,5,8) if contacts==7 else (-10,-8,-5,1,2,3,4,6,7))
    scale=(Q(10621537,256))**(8 if contacts==7 else 4)
    factors=[s.Poly(s.Rational((scale+h)**2)-t,t) for h in shifts]
    F=reduce(lambda a,b:a*b,factors,s.Poly(1,t))
    Fa=s.Poly(0,t)
    for i,h in enumerate(shifts):
        term=s.Poly(2*s.Rational(scale+h),t)
        for j,f in enumerate(factors):
            if i!=j:term*=f
        Fa+=term
    A,B=ints(-2*contacts*F,Fa)
    assert A.degree()==contacts and B.degree()==contacts-1
    certificates=[]
    for p in s.primerange(53,400):
        pm=modpoly(Pi,p);am=modpoly(A,p);bm=modpoly(B,p)
        if am.degree()!=contacts or bm.degree()!=contacts-1 or s.gcd(am,bm).degree()!=0:continue
        if pm.degree()!=26 or s.gcd(pm,pm.diff()).degree()!=0:continue
        cp=compose(pm,am,bm,p)
        if cp.degree()!=26*contacts or cp.eval(0)==0 or s.gcd(cp,cp.diff()).degree()!=0:continue
        for name,f in [('weight',pm),('physical_squared_slope',cp)]:
            e,g,d=s.gcdex(f,f.diff());assert d==s.Poly(1,*f.gens,modulus=p)
            certificates.append(dict(name=name,prime=int(p),degree=f.degree(),
                coefficients=coeffs(f),bezout_polynomial=coeffs(e),bezout_derivative=coeffs(g)))
        break
    assert len(certificates)==2
    report=dict(status='PASS',scope=__doc__,fixed_input=1,fixed_shift=3,
        fixed_shift_is_defining_threshold=False,root_point='P',auxiliary_points='H=U=P/2',
        half_point=[q.data() for q in H],tests=[q.data() for q in tests],
        ascending_integer_coefficients=dict(D=coeffs(D),R=coeffs(R),Pi=coeffs(Pi),
            physical_A=coeffs(A),physical_B=coeffs(B)),scale=str(scale),shifts=list(shifts),
        sample_actual_field_evaluations=samples,finite_field_certificates=certificates,
        genera=dict(weight=12,squared_slope=13*contacts-1,twisted_squared_slope=13*contacts,slope=26*contacts-1),
        balancing='C/(1+u*C) for first four; C^2/(1+u*C^2) for comparisons',
        contact_count=contacts,physical_lift_degree=contacts,cover_guard_exclusions=['u=0','u=-1'],
        additional_physical_guards=['B(t)!=0','t is a rational square','a^2-t!=0',
            'original point/chart and whole-character guards','all fixed-place/selected-contact/real preparation'],
        rational_witness_proved=False,nine_coordinate_completeness_claimed=False)
    (HERE/('certificate.json' if contacts==7 else 'nine_contact_certificate.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','genera','physical_lift_degree','rational_witness_proved']},indent=2))

if __name__=='__main__':main()
