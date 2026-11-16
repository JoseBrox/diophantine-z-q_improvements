#!/usr/bin/env python3
"""Exact universal identities for the varying-difference chart and its helpers."""
from pathlib import Path
import sympy as s,json,argparse
A,C,L,S,T,V,D,B4,Z=s.symbols('a c delta s t v D b4 Z')
q=[A*L-D*B4,A-C*C-L,V*(V+T-S)+L,S*T+C*(T-S)+2*C*V+2*L]
G=s.groebner(q,A,L,B4,S,T,V,C,D,order='grevlex')
def red(z):return s.expand(G.reduce(s.expand(z))[1])
U=V-S-C;W=V+T-C;B=V+T-S
checks={}
def ck(name,z):
 assert red(z)==0,(name,red(z));checks[name]='PASS'
ck('unit product',U*W-A)
ck('inverse chord',V*B+L)
x=V*W;y=V*U
ck('abscissa sum',x+y-((V-C)**2-A))
ck('abscissa product',x*y-A*V*V)
ck('first point curve',(S*x)**2-x**3+D*B4*x)
ck('second point curve',(T*y)**2-y**3+D*B4*y)
ck('difference point curve',(A*C)**2-A**3+D*B4*A)
ck('first ordinate on line',S*x-((V-C)*x-A*V))
ck('second negative ordinate on line',-T*y-((V-C)*y-A*V))
for i,z in enumerate(s.Poly(Z**3-D*B4*Z-((V-C)*Z-A*V)**2-(Z-A)*(Z**2-((V-C)**2-A)*Z+A*V*V),Z).all_coeffs()):ck('line cubic coefficient '+str(i),z)
ck('first scaled reciprocal',x*(-U*B)-D*B4)
ck('second scaled reciprocal',y*(-W*B)-D*B4)
# Two-torsion difference: the remaining quadratic cannot have root a.
assert s.expand((Z**2-((V-C)**2-A)*Z+A*V**2).subs({Z:A,C:0}))==2*A*A
checks['c zero tangent exclusion']='PASS'
# Universal degenerate zero-input witness.
HH,JJ=s.symbols('SH TH');cc=-HH*JJ/(HH-JJ)
subs={A:cc*cc,C:cc,L:0,S:HH,T:JJ,V:HH-JJ,B4:0}
for i,z in enumerate(q):
 assert s.cancel(z.subs(subs))==0;checks['zero input pair '+str(i)]='PASS'
assert s.cancel((U*B).subs(subs))==s.cancel((W*B).subs(subs))==0
checks['zero input reciprocal helpers']='PASS'
# The fixed three-coordinate reference has nonzero unit constants.
rho=s.sqrt(2);aa=1+rho;cc0=4-2*rho;delta0=-23+17*rho;dd=11-6*rho
assert s.expand(aa-cc0*cc0)==delta0
assert s.expand(aa*delta0)==dd
assert s.expand(aa*cc0)==2*rho
checks['fixed reference unit constants']='PASS'
SH=-s.Rational(87,41)+s.Rational(129,164)*rho;TH=4-2*rho
norm=s.simplify((SH-TH)*(SH-TH).xreplace({rho:-rho}));assert norm!=0
record={'status':'PASS','checks':checks,'count':len(checks),'pairFieldCoordinates':6,'pairFieldQuadrics':4,'extraGuards':0,'cZeroIncluded':True,'zeroInputOrdinateDifferenceNorm':str(norm),'fullSourceProvedByThisChecker':False}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('pair-certificate.json'))
args=parser.parse_args()
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
