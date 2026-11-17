#!/usr/bin/env python3
"""Exact finite checks supporting, not proving, the infinite formal argument."""
import json
import argparse
import hashlib
from math import comb, prod
from pathlib import Path
import sympy as s
z,A,B=s.symbols('z A B')
order=18
X=s.Integer(1)
coefficients={}
for k in range(2,order,2):
    c=s.symbols('c')
    trial=X+c*z**k
    equation=s.Poly(trial**3-trial**2+A*z**4*trial+B*z**6,z)
    ck=s.solve(equation.coeff_monomial(z**k),c)[0]
    assert ck.is_polynomial(A,B)
    assert all(q.q==1 for q in s.Poly(ck,A,B).coeffs())
    X+=ck*z**k
    coefficients[str(k-2)]=str(ck)
assert s.expand(s.series(X**3-X**2+A*z**4*X+B*z**6,z,0,order).removeO())==0
omega=s.series(1-z*s.diff(X,z)/(2*X),z,0,order).removeO()
assert all(q.q==1 for q in s.Poly(omega,z,A,B).coeffs())
assert s.Poly(omega,z).coeff_monomial(z**2)==0
ell=s.integrate(omega,z)
# Formula for the special j=1728 model in the retained proof.
D=s.symbols('D')
ellspecial=s.expand(ell.subs({A:-D,B:0}))
expected=sum((-1)**j*s.binomial(2*j,j)*D**j*z**(4*j+1)/s.Integer(4*j+1) for j in range((order-1)//4+1))
assert s.expand(ellspecial-expected)==0
# Positive subset constant evaluated without floating-point logarithms.
subset=[]
for r in range(1,11):
    direct=2*sum(comb(r-1,j-1)*(j-1) for j in range(1,r+1))
    assert direct==(r-1)*2**(r-1)
    subset.append({'r':r,'log_M_coefficient':direct,'exp_b_r':prod(j**comb(r-1,j-1) for j in range(1,r+1))})
assert subset[3]['exp_b_r']==864
ROOT=Path(__file__).resolve().parents[3]
PAPER=ROOT/'papers/effective_sums/elliptic_sum_heights_over_number_fields_20261117_v63.tex'
result={
 'status':'PASS',
 'source_sha256':hashlib.sha256(PAPER.read_bytes()).hexdigest(),
 'scope':'Exact finite series identities through z^17 and subset constants; infinite coefficient integrality, local convergence, and DHK specialization are proved in the manuscript.',
 'equation':'y^2=x^3+A*x+B',
 'X_identity':'X^3-X^2+A*z^4*X+B*z^6=0',
 'X_coefficient_recursion_order':order,
 'x_series_coefficients_after_z^-2':coefficients,
 'differential_series':str(omega),
 'logarithm_series':str(ell),
 'special_j1728_logarithm_verified':True,
 'subset_constants':subset,
 'sympy_version':s.__version__,
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('certificate.json'))
path=parser.parse_args().output
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(result,indent=2)+'\n')
print(path)
