#!/usr/bin/env python3
"""Independent symbolic identities and group-law audit of the trace cubic.

The author's integer-polynomial verifier checks the full division
recurrences and all projective no-root certificates.  This second
checker uses affine tangent/chord addition instead: its multiplication
denominators must agree with the certified division polynomials.
"""
from pathlib import Path
from hashlib import sha256
import json
import sympy as s

HERE = Path(__file__).resolve().parent
CERT = HERE.parent / 'general_scalar_v56' / 'cubic_trace_rank_certificate.json'
data = json.loads(CERT.read_text())
w, V, q, c = s.symbols('w V q c')
a = q*q - 2*q - 1
delta = a*a + 4*q*(q*q-1)*V
assert s.expand(delta.subs(V, 0) - a*a) == 0
assert s.expand(delta.subs(V, 1) - (q*q+1)**2) == 0
assert s.expand(delta.subs(V, 2) - (q*q+2*q-1)**2) == 0
assert s.expand(delta.subs(q, 2) - (1+24*V)) == 0

C = V*V+w*(2-V)
x0, y0 = s.Integer(49), s.Integer(336)
A, B = -2-24*w, 1+1176*w
assert s.expand(y0*y0 - (x0**3+A*x0*x0+B*x0)) == 0
x = 1+24*V
assert s.expand(576*C*(1+24*V) - (x**3+A*x*x+B*x)) == 0
disc = s.factor(16*B*B*(A*A-4*B))
assert s.expand(disc-9216*w*(w-8)*(1+1176*w)**2) == 0

points = {1: (x0,y0)}
def plus(P, Q):
    x1,y1=P; x2,y2=Q
    if P == Q:
        slope=s.cancel((3*x1*x1+2*A*x1+B)/(2*y1))
    else:
        slope=s.cancel((y2-y1)/(x2-x1))
    xx=s.cancel(slope*slope-A-x1-x2)
    yy=s.cancel(-y1+slope*(x1-xx))
    return xx,yy

def multiple(n):
    if n not in points:
        if n % 2 == 0:
            P=multiple(n//2)
            points[n]=plus(P,P)
        else:
            points[n]=plus(multiple(n-1),points[1])
    return points[n]

factor_map={r['label']:r for r in data['factors']}
rows=[]
for row in data['division_factorizations']:
    n=row['n']
    psi=s.Integer(row['scalar'])
    for term in row['factors']:
        r=factor_map[term['factor']]
        poly=s.Poly.from_list(r['coefficients_descending'],w).as_expr()
        psi*=poly**term['multiplicity']
    xx,yy=multiple(n)
    num,den=s.fraction(xx)
    ratio=s.cancel(den/psi**2)
    assert ratio.is_Rational and ratio != 0
    assert s.gcd(s.Poly(num,w),s.Poly(den,w)).degree()==0
    rows.append({'n':n,'x_denominator_degree':s.degree(den,w),
                 'psi_degree':s.degree(psi,w),
                 'denominator_over_psi_squared':str(ratio),
                 'direct_tangent_chord_match':True})

report={'status':'PASS',
        'adaptive_reference_square_identities':True,
        'cubic_change_of_variables':True,
        'curve_discriminant':str(disc),
        'group_law_checks':rows,
        'certificate_sha256':sha256(CERT.read_bytes()).hexdigest(),
        'actual_detector_trace_matching_proved':False}
(HERE/'adaptive_and_cubic_audit_certificate.json').write_text(
    json.dumps(report,indent=2,default=int)+'\n')
print(json.dumps({'status':'PASS','group_law_orders':[r['n'] for r in rows]}))
