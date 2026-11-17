#!/usr/bin/env python3
"""Exact factor-assignment and valuation certificate for the 194 system.

The unbounded formal-group, prime-pattern and height proof is in
papers/quartic/quartic194_20261117_v73.tex. This finite certificate checks the specific
factor table against the saved SAT assignment, not the compiled rows.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sympy as s

BASE=Path(__file__).resolve().parent
model_path=BASE/'coordinate-model.json'
result_path=BASE/'laurent-certificate.json'
model=json.loads(model_path.read_text())
result=json.loads(result_path.read_text())
assert result['status']=='sat'
assert hashlib.sha256(model_path.read_bytes()).hexdigest()==result['model_sha256']
assert {k: model['base_units'][k] for k in ['901','902','903']}=={
    '901':[0,-3],'902':[1,-1],'903':[-1,-1]}
assert len(model['active'])+len(model['base_units'])==194

physical={'C1':('E1',4),'C2':('E2',4),'C3':('E3',4),
          'C4':('E4',4),'GL':('H',4),'DH':('DH',2)}
for label in ['B0','A1','B1','A2','B2','A3','B3','A4','B4']:
    physical[label]=(label,2)
expected=[
    [('B3',2),('DH',2),('E2',4)],
    [('A1',2),('B0',2),('B1',2)],
    [('A3',2),('B4',2),('E3',4)],
    [('H',4),('B2',2),('E4',4)],
    [('A4',2),('A2',2),('E1',4)],
    [('E2',4),('E1',4),('E4',4)],
    [('B3',2),('DH',2),('A3',2)],
    [('B1',2),('B4',2),('E3',4)],
    [('A1',2),('B2',2),('H',4)],
    [('B0',2),('A4',2),('A2',2)],
]
actual=[[None]*3 for _ in range(10)]
for det in (0,1):
    assignment=result['assignments'][str(det)]
    assert sorted(assignment['quadratic'].values())==list(range(8))
    assert sorted(assignment['linear'].values())==list(range(7))
    for label,k in assignment['quadratic'].items():
        assert model['quadratic_tests'][label][2]==1
        factor,power=k//2,1+2*(k%2)
        actual[5*det+factor][power-1]=physical[label]
    for label,k in assignment['linear'].items():
        factor,power=(k,2) if k<4 else (4,k-3)
        actual[5*det+factor][power-1]=physical[label]
assert actual==expected

rows=[]
for j,row in enumerate(actual):
    det,k=divmod(j,5)
    cells=[]
    for e,(label,m) in enumerate(row,1):
        # Raw reciprocal depth is >=2d; cleared comparison/H depth >=2d.
        slope=2*m
        cells.append({'q_power':e,'test':label,'test_power':m,
                      'selected_depth_slope':slope,
                      'selected_depth_intercept':-e,
                      'selected_depth_minimum':slope-e,
                      'strict_extraction_coefficient':str(Fraction(2*e-1,2*m))})
        assert slope-e>0
    rows.append({'detector':det,'factor':k,'terms':cells,
                 'input_term':{'q_power':4,'test':'N','test_power':8,
                               'selected_depth_slope':24,
                               'selected_depth_intercept':-4,
                               'selected_depth_minimum':20} if k==4 else None})
    if k==4:
        tests=[z['test'] for rr in rows[-5:] for z in rr['terms']]
        assert sorted(tests)==sorted([z[0] for z in physical.values()])

residues=[]
for mu in [1,3,5,7]:
    ordinary=[(-e*mu)%4 for e in range(4)]
    assert sorted(ordinary)==[0,1,2,3]
    special=[{0},{(-4*mu)%8}]+[
        {(-e*mu)%8,(-e*mu+4)%8} for e in [1,2,3]]
    assert sum(map(len,special))==8
    assert set.union(*special)==set(range(8))
    assert all(not special[i]&special[j] for i in range(5) for j in range(i))
    residues.append({'mu_mod_8':mu,'ordinary_mod_4':ordinary,
                     'special_mod_8':[sorted(v) for v in special]})

A,T,w,S=s.symbols('A T w S')
C=(A-1)*(w+4*S);P=T*w;Q=(A+1)*P
H=P**2+C**2-C*Q-w**2
L4=1+4*S/w
G=T**2-(A+1)*(A-1)*T*L4+(A-1)**2*L4**2-1
assert s.cancel(H-w*w*G)==0

F,G,ss,t,h,d,D=s.symbols('F G s t h d D')
p=h+ss+t
r1=d-p*F;r2=d-h*G;r3=D*(F+G)-(ss-t)*h+t*t
r4=d*(ss-t)-1-D*F*G
assert s.expand(F*ss**2+D*F**2-1-r4+(ss-t)*r1-F*r3)==0
assert s.expand(G*t**2+D*G**2-1-r4+(ss-t)*r2-G*r3)==0

certificate={
    'status':'PASS',
    'scope':'exact 194 factor assignment, full valuation residue periods, selected-depth inequalities and chart/Lucas identities',
    'model_sha256':hashlib.sha256(model_path.read_bytes()).hexdigest(),
    'assignment_sha256':hashlib.sha256(result_path.read_bytes()).hexdigest(),
    'factor_table':rows,
    'residue_periods':residues,
    'input_error_minimum_depth':2,
    'height_argument_uses_input_depth':1,
    'soundness_depths':'all positive odd contact depths',
    'completeness_contact_depth':1,
    'synchronized_formal_depth':'max(d0,e0), not arbitrarily large',
    'point_chart_identities':2,
    'homogeneous_lucas_identity':True,
    'arithmetic_proof':'papers/quartic/quartic194_20261117_v73.tex',
    'not_certified_here':['compiled quadratic coefficients and zero-set map',
                          'external source premises',
                          'numerical sufficient N'],
}
target=Path(__file__).with_name('arithmetic-certificate.json')
target.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps({k:v for k,v in certificate.items() if k not in ['factor_table','residue_periods']},indent=2))
