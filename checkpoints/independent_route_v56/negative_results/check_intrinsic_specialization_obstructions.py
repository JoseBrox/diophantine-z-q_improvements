"""Exact auxiliary checks for intrinsic_specialization_obstructions.tex.
The uniform p-adic and rank-one arguments are proofs in the manuscript;
finite checks here certify only the explicitly stated identities/tables.
"""
from fractions import Fraction
from pathlib import Path
import json
import sympy as S

d,v,u=S.symbols('d v u')
P=lambda ss: d*(d+v*v)**2*ss**4-d*(d-v*v)**2*(1-d)**2
factor_check=S.expand(P(1)-d*d*(v*v+2-d)*((2-d)*v*v+d*d))==0
assert factor_check
p=13
squares=sorted({x*x%p for x in range(p)})
assert 5 not in squares and 8 not in squares
critical=S.Poly((u*u+226)*(226*u*u+12544)-5*(u*u+5)**2,u)
assert all(int(c)%13==0 for c in critical.all_coeffs())
critical_values=[((a*a+226)*(226*a*a+12544))%13 for a in range(1,13)]
assert all(a not in squares for a in critical_values)
d0=Fraction(112,169)
assert 0<d0<1 and d0==7*Fraction(4,13)**2
assert d0.numerator%16==0 and d0.numerator%32!=0

# Four positive descent classes and their Q_2 unit square classes.
classes={"1":1,"l":5,"beta":7,"l_beta":(5*7)%8}
assert len(set(classes.values()))==4 and classes['beta']==7
# The abstract independent-support images for n=beta*m and n*eta.
# Vector coordinates are beta,m,eta; -1 is separated by the real sign.
first={0,1,2,3}
second={0,1,6,7}
assert first&second=={0,1}
certificate={
 'status':'All exact checks passed; no global one-coordinate realization is claimed.',
 'factorization':str(S.factor(P(1))),
 'prepared_counterexample':str(d0),
 'prime':13,
 'squares_mod_13':squares,
 'critical_unit_values_mod_13':critical_values,
 'critical_identity_mod_13':'(u^2+226)(226u^2+12544)=5(u^2+5)^2',
 'positive_rank_one_classes_at_2':classes,
 'two_curve_positive_class_intersection':'{1,beta}, when eta>1 with disjoint prime support',
 'uniform_theorem_scope':'Any finite list of rational functions s=R_j(d); adaptive s(v,d) is not excluded.'
}
Path(__file__).with_name('intrinsic_specialization_obstructions_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate,indent=2))
