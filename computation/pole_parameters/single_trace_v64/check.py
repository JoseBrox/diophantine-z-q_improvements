#!/usr/bin/env python3
"""Exact identities for the single actual-trace criterion and sign symmetry.

This does not certify global trace-square witnesses, abc, or a defining count.
The valuation and finite-algebra implications are proved in the manuscript.
"""
from pathlib import Path
import argparse, hashlib, json
import sympy as s

HERE=Path(__file__).resolve().parent
A,B,w=s.symbols('A B w')
N=A*A-2*B*B
V=2*A/N
C=V*V+w*(2-V)
assert s.cancel(C-(4*A*A+2*w*N*(N-A))/(N*N))==0
assert s.cancel(C.subs({A:1,B:0})-4)==0

x1,x2,y1,y2,d=s.symbols('x1 x2 y1 y2 d')
dx=x1-x2
X=(x1+x2)*(x1*x2-d)+2*y1*y2
Y=(y1*x2+y2*x1)*dx*dx-(y1+y2)*X
negate={y1:-y1,y2:-y2}
assert s.expand(dx.subs(negate,simultaneous=True)-dx)==0
assert s.expand(X.subs(negate,simultaneous=True)-X)==0
assert s.expand(Y.subs(negate,simultaneous=True)+Y)==0
assert s.cancel((-X*dx/Y).subs(negate,simultaneous=True)+(-X*dx/Y))==0
assert s.cancel((dx*dx/X).subs(negate,simultaneous=True)-dx*dx/X)==0

U,V0,W,A0,B0=s.symbols('U V0 W A0 B0')
relations=[U*U-2*A0-2*W,V0*V0-A0+W,U*V0-2*B0,
           U*W-A0*U+2*B0*V0,V0*W-B0*U+A0*V0,
           W*W-A0*A0+2*B0*B0]
signs=[1,1,1,-1,-1,1]
for relation,sign in zip(relations,signs):
    assert s.expand(relation.subs({U:-U,V0:-V0},simultaneous=True)-sign*relation)==0
# The original ordinate j=(U+sqrt(2)V0)/2 negates; its norm W is fixed.
r,rp,inputX,u,test=s.symbols('r rp inputX u test')
for value in (r-rp,r-inputX):
    assert s.expand(value.subs({r:-r,rp:-rp,inputX:-inputX},simultaneous=True)+value)==0
Di=test*test/(1+u*test*test)
assert s.cancel(Di.subs(test,-test)-Di)==0
assert s.cancel((1+Di*Di/u).subs(test,-test)-(1+Di*Di/u))==0
assert (inputX*inputX).subs(inputX,-inputX)==inputX*inputX

report={
 'status':'PASS',
 'derivative_source_commit':'f70057ffce6b8318a79a7e3648779067fd98c2e3',
 'scope':'Exact added identities and the six rank-four relations; no global witness realization or defining count is inferred.',
 'cleared_trace_identity':True,
 'reference_trace_radicand':4,
 'homogeneous_difference_signs':{'dx':1,'X_numerator':1,'Y_numerator':-1,'reciprocal':1,'formal_parameter':-1},
 'point_algebra_relation_signs':signs,
 'comparison_test_signs':[1,1,1,1,-1,-1],
 'balanced_test_and_product_invariant':True,
 'cofinite_positive_target_sufficient':'proved in manuscript, not inferred from finite checks',
 'uniform_actual_trace_realization_proved':False,
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=HERE/'certificate.json')
args=parser.parse_args()
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','rank_four_relations_checked':len(relations),'global_realization_proved':False},indent=2))
