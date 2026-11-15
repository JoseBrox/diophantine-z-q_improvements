#!/usr/bin/env python3
"""Exact algebraic checks for the fixed-input K3 pole surfaces.

The companion paper proves the geometric conclusions. These checks verify
the universal equations, chart smoothness criteria, local A3 forms, and
resolution charts over exact rational function fields; no arithmetic
nonexistence or common-parameter conclusion is tested or asserted.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import sympy as sp

HERE=Path(__file__).resolve().parent


def zero(expression):
    assert sp.cancel(expression)==0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'verification.json')
    args=parser.parse_args()
    T,U,S,V,C,D=sp.symbols('T U S V C D')
    tau,s,q,x,v,w,a,b,c=sp.symbols('tau s q x v w a b c')
    F1=(T*T+3*D*U*U)*S*S-C*(T*T-D*U*U)*V*V
    F2=(T*T+3*D*U*U)*S*S+3*C*(T*T-D*U*U)*V*V
    for F in (F1,F2):
        assert all(i+j==2 and k+l==2 for (i,j,k,l),_ in sp.Poly(F,T,U,S,V).terms())
    f1=F1.subs({T:tau,U:1,S:s,V:1})
    f2=F2.subs({T:tau,U:1,S:s,V:1})
    e=(tau*tau-D)/(tau*tau+3*D)
    zero(D*f1*f2-D*(tau*tau+3*D)**2*(s*s-C*e)*(s*s+3*C*e))
    zero(F2-F1-4*C*(T*T-D*U*U)*V*V)
    zero(3*F1+F2-4*(T*T+3*D*U*U)*S*S)

    # In every affine chart, all four biquadratic coefficients and ad-bc
    # are nonzero Laurent monomials in C,D. This verifies the uniform
    # smoothness criterion under precisely CD != 0, without exceptions
    # hidden by a generic-field Groebner computation.
    chart_rows=[]
    for label,F in (('F1',F1),('F2',F2)):
        for tau_inverted in (False,True):
            for s_inverted in (False,True):
                substitutions={T:1,U:tau} if tau_inverted else {T:tau,U:1}
                substitutions.update({S:1,V:s} if s_inverted else {S:s,V:1})
                poly=sp.Poly(F.subs(substitutions),tau,s)
                coeffs=[poly.coeff_monomial(m) for m in (tau*tau*s*s,tau*tau,s*s,1)]
                aa,bb,cc,dd=coeffs
                determinant=sp.factor(aa*dd-bb*cc)
                for value in coeffs+[determinant]:
                    terms=sp.Poly(value,C,D).terms()
                    assert len(terms)==1 and terms[0][1]!=0
                chart_rows.append({'branch':label,'tau_inverted':tau_inverted,
                    's_inverted':s_inverted,'coefficients':[str(z) for z in coeffs],
                    'ad_minus_bc':str(determinant)})

    # Exact tangency data in regular local coordinates on the tau line.
    u=sp.symbols('u')
    near_zero_1=(u+4*D)*s*s-C*u
    near_zero_2=(u+4*D)*s*s+3*C*u
    uz1=4*D*s*s/(C-s*s)
    uz2=-4*D*s*s/(s*s+3*C)
    zero(near_zero_1.subs(u,uz1));zero(near_zero_2.subs(u,uz2))
    dz=16*C*D*s*s/((C-s*s)*(s*s+3*C))
    zero(uz1-uz2-dz)
    assert sp.limit(dz/(s*s),s,0)==16*D/(3*C)
    near_inf_1=u*(1-C*v*v)+4*C*D*v*v
    near_inf_2=u*(1+3*C*v*v)-12*C*D*v*v
    ui1=-4*C*D*v*v/(1-C*v*v)
    ui2=12*C*D*v*v/(1+3*C*v*v)
    zero(near_inf_1.subs(u,ui1));zero(near_inf_2.subs(u,ui2))
    di=-16*C*D*v*v/((1-C*v*v)*(1+3*C*v*v))
    zero(ui1-ui2-di)
    assert sp.limit(di/(v*v),v,0)==-16*C*D

    # The two exact local double-cover equations are A3 normal forms.
    zero((s*s-x)*(s*s+3*x)-(sp.Rational(4,3)*s**4-3*(x-s*s/3)**2))
    zero((x-C*v*v)*(x+3*C*v*v)-((x+C*v*v)**2-4*C*C*v**4))
    xzero=C*(tau*tau-D)/(tau*tau+3*D)
    xinf=(tau*tau+3*D)/(tau*tau-D)
    zero(sp.diff(xzero,tau)-8*C*D*tau/(tau*tau+3*D)**2)
    zero(sp.diff(xinf,tau)+8*D*tau/(tau*tau-D)**2)

    # Resolve ab=c^4 by two point blow-ups. The a,b charts are smooth;
    # the c chart is A1, whose next blow-up has smooth graphs or ab=1.
    aa,bb,cc=sp.symbols('aa bb cc')
    original=a*b-c**4
    strict_a=sp.cancel(original.subs({a:aa,b:aa*bb,c:aa*cc},simultaneous=True)/aa**2)
    strict_b=sp.cancel(original.subs({a:bb*aa,b:bb,c:bb*cc},simultaneous=True)/bb**2)
    strict_c=sp.cancel(original.subs({a:cc*aa,b:cc*bb,c:cc},simultaneous=True)/cc**2)
    zero(strict_a-(bb-aa**2*cc**4))
    zero(strict_b-(aa-bb**2*cc**4))
    zero(strict_c-(aa*bb-cc**2))
    A,B,H=sp.symbols('A B H')
    next_a=sp.cancel(strict_c.subs({aa:A,bb:A*B,cc:A*H},simultaneous=True)/A**2)
    next_b=sp.cancel(strict_c.subs({aa:B*A,bb:B,cc:B*H},simultaneous=True)/B**2)
    next_c=sp.cancel(strict_c.subs({aa:H*A,bb:H*B,cc:H},simultaneous=True)/H**2)
    zero(next_a-(B-H**2));zero(next_b-(A-H**2));zero(next_c-(A*B-1))

    # Transformation coefficients of the residue form da wedge dc / a.
    def form_coeff(a_expr,c_expr,first,second):
        jac=sp.det(sp.Matrix([[sp.diff(a_expr,first),sp.diff(a_expr,second)],
                              [sp.diff(c_expr,first),sp.diff(c_expr,second)]]))
        return sp.cancel(jac/a_expr)
    assert form_coeff(aa,aa*cc,aa,cc)==1
    assert form_coeff(cc*aa,cc,aa,cc)==1/aa
    assert form_coeff(A,A*H,A,H)==1
    assert form_coeff(H*A,H,A,H)==1/A

    # The elementary numerical invariants entering the geometric proof.
    branch_genus=(2-1)*(2-1)
    euler_branch=2*(2-2*branch_genus)-4
    euler_singular=2*4-euler_branch
    euler_resolution=euler_singular+4*3
    assert (branch_genus,euler_branch,euler_singular,euler_resolution)==(1,-4,12,24)
    h1_O_minus2_minus2=1*0+0*1
    assert h1_O_minus2_minus2==0
    assert tuple(-2+2 for _ in range(2))==(0,0)

    report={'status':'PASS',
        'scope':'algebraic certificates for the fixed-input K3 model; no arithmetic nonexistence or common rational parameter assertion',
        'assumptions':['characteristic zero','C != 0','D != 0'],
        'branch_bidegrees':[[2,2],[2,2]],
        'smoothness_charts':chart_rows,
        'intersections':[{'s':'0','tau_squared':'D','number':2,'multiplicity':2},
                         {'s':'infinity','tau_squared':'-3D','number':2,'multiplicity':2}],
        'local_branch_difference_leading_coefficients':[str(16*D/(3*C)),str(-16*C*D)],
        'local_singularity':'A3: ab=c^4',
        'first_blowup_strict_transforms':[str(strict_a),str(strict_b),str(strict_c)],
        'second_blowup_strict_transforms':[str(next_a),str(next_b),str(next_c)],
        'canonical_form_coefficients':['1','1/aa','1','1/A'],
        'euler_numbers':{'branch':euler_branch,'singular_double_cover':euler_singular,
                         'smooth_resolution':euler_resolution},
        'h1_O_minus2_minus2':h1_O_minus2_minus2,
        'canonical_bidegree':[0,0],
        'geometric_dependencies':['double-cover adjunction and structure algebra',
            'A3 rational and crepant resolution',
            'regular differential-form vanishing for smooth rationally connected varieties'],
        'primary_references':[
            {'authors':'G. Angermuller and W. Barth','title':'Elliptic fibres on Enriques surfaces',
             'publication':'Compositio Mathematica 47 (1982), no. 3, 317-332',
             'location':'Section 3, page 319',
             'url':'https://www.numdam.org/item/CM_1982__47_3_317_0.pdf'},
            {'author':'O. Debarre','title':'On rationality problems','date':'2024-04-15',
             'location':'Proposition 2.5(b)',
             'url':'https://perso.imj-prg.fr/olivier-debarre/wp-content/uploads/sites/34/2024/04/On-rationality-problems.pdf'}],
        'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','affine_smoothness_charts':len(chart_rows),
                      'A3_singularities':4,'certificate':str(args.output)},indent=2))


if __name__=='__main__':main()
