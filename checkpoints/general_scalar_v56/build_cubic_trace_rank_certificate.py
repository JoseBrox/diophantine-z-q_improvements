#!/usr/bin/env python3
"""Build exact factor and residue certificates for the cubic trace section.

The separate standard-library verifier checks every factor product and
projective no-root certificate without using this factorization engine.
"""
from pathlib import Path
from fractions import Fraction
import json
import sympy as s

w=s.symbols('w')
x,y=s.Integer(49),s.Integer(336)
a2,a4=-2-24*w,1+1176*w
b2,b4,b8=4*a2,2*a4,-a4*a4
psi={0:s.Integer(0),1:s.Integer(1),2:2*y,
     3:s.expand(3*x**4+b2*x**3+3*b4*x*x+b8),
     4:s.expand(2*y*(2*x**6+b2*x**5+5*b4*x**4+10*b8*x*x+b2*b8*x+b4*b8))}

def division_at_P(n):
    if n in psi:return psi[n]
    if n%2:
        m=n//2
        f=division_at_P(m+2)*division_at_P(m)**3-division_at_P(m-1)*division_at_P(m+1)**3
    else:
        m=n//2
        f=division_at_P(m)/(2*y)*(division_at_P(m+2)*division_at_P(m-1)**2-division_at_P(m-2)*division_at_P(m+1)**2)
    psi[n]=s.Poly(f,w).as_expr()
    return psi[n]

def evalmod(coeff,v,p):
    z=0
    for a in coeff:z=(z*v+a)%p
    return z

factors=[]
known={}
rows=[]
for n in [8,10,12]:
    scalar,fac=s.factor_list(division_at_P(n),w)
    index=[]
    for ff,multiplicity in fac:
        p=s.Poly(ff,w)
        coeff=tuple(int(a)for a in p.all_coeffs())
        if coeff not in known:
            lab='F'+str(len(factors)+1)
            row={'label':lab,'degree':int(p.degree()),'coefficients_descending':coeff}
            if p.degree()==1:
                row['rational_root']=str(Fraction(-coeff[1],coeff[0]))
            else:
                prime=next(int(ell)for ell in s.primerange(2,100)
                           if coeff[0]%ell and all(evalmod(coeff,a,ell)for a in range(ell)))
                row.update({'certificate_prime':prime,
                            'coefficients_mod_prime':[a%prime for a in coeff],
                            'affine_value_table':[evalmod(coeff,a,prime)for a in range(prime)],
                            'value_at_projective_infinity':coeff[0]%prime})
            known[coeff]=lab
            factors.append(row)
        index.append({'factor':known[coeff],'multiplicity':int(multiplicity)})
    rows.append({'n':n,'degree':int(s.degree(division_at_P(n),w)),'scalar':str(scalar),'factors':index})

whole_quotients=[]
by_label={f['label']:f for f in factors}
for row in rows:
    QQ=s.Integer(1)
    linear=[]
    for term in row['factors']:
        ff=by_label[term['factor']]
        if ff['degree']==1:
            linear.append(term['factor'])
        else:
            QQ*=s.Poly.from_list(ff['coefficients_descending'],w).as_expr()**term['multiplicity']
    coeff=[int(a)for a in s.Poly(QQ,w).all_coeffs()]
    pp=next(int(p)for p in s.primerange(2,1000) if coeff[0]%p
            and all(evalmod(coeff,a,p)for a in range(p)))
    whole_quotients.append({'n':row['n'],'degree':len(coeff)-1,
        'removed_linear_factors':linear,'coefficients_descending':coeff,
        'certificate_prime':pp,'value_at_projective_infinity':coeff[0]%pp,
        'affine_value_table':[evalmod(coeff,a,pp)for a in range(pp)]})

report={'status':'BUILT; run independent verifier',
        'curve':'y^2=x^3-(2+24w)x^2+(1+1176w)x',
        'P':[49,336],
        'discriminant':'9216w(w-8)(1+1176w)^2',
        'singular_weights':['0','8','-1/1176'],
        'rational_torsion_specializations':{'296/49':3,'-96/49':3,'100/49':4},
        'division_factorizations':rows,'factors':factors,
        'whole_quotient_certificates':whole_quotients,
        'theoretical_input':'Mazur torsion classification; division-polynomial vanishing criterion',
        'actual_detector_matching_proved':False}
out=Path(__file__).with_name('cubic_trace_rank_certificate.json')
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'certificate':str(out),'factors':len(factors),
                  'nonlinear_modular_certificates':sum(f['degree']>1 for f in factors)}))
