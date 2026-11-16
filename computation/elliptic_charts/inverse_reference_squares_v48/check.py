#!/usr/bin/env python3
"""Universal identities for the inverse reference-square presentation."""
from pathlib import Path
import sympy as s,json,argparse
u,w,h,A,B,a,c=s.symbols('u w h A B a c');delta=a-c*c
v=a*(u+w)+2*c+delta*h
q=[a*u*w-1,delta*h*h+a*h*(u+w)+2*c*h-1,
   a*A*(v+delta*w)+2*c*h*u+h-u,
   a*B*(v+delta*u)+2*c*h*w+h-w,
   a*a*(delta*delta*A*B-(1+4*c*w)*A-(1+4*c*u)*B)+1-2*(2*a+c*c)*h*h]
curve=h*h+(a*u+2*c+1/u)*h/delta-1/delta
for f in q:
    z=f.subs({w:1/(a*u),A:u*u*h*h,B:h*h/(a*a*u*u)},simultaneous=True)
    assert s.cancel(s.rem(z,curve,h))==0
# At an exceptional A graph coefficient, the recovered B is1/delta².
coefficient_A=s.diff(q[4],A).subs(B,1/delta**2)
assert s.expand(coefficient_A+4*a*a*c*w)==0
coefficient_B=s.diff(q[4],B).subs(A,1/delta**2)
assert s.expand(coefficient_B+4*a*a*c*u)==0
# Simultaneous graph coefficient failure forces Delta0.
Delta=(a+delta)**2-4*a*c*c
rho=s.sqrt(2);ea=-1+s.Rational(7,4)*rho
av=s.expand(ea**2);cv=-s.Rational(87,41)+s.Rational(129,164)*rho
def pair(z):
    z=s.radsimp(s.expand(z)); z=s.collect(s.expand(z),rho)
    return [str(s.expand(z).coeff(rho,0)),str(s.expand(z).coeff(rho,1))]
checks={'a_nonzero':av,'c_nonzero':cv,'delta_nonzero':av-cv**2,'Delta_nonzero':Delta.subs({a:av,c:cv})}
vals={}
for name,z in checks.items():
    z=s.simplify(z);assert z!=0
    norm=s.simplify(z*z.xreplace({rho:-rho}));assert norm!=0
    vals[name]={'value':pair(z),'norm':str(norm)}
# Polynomial inverse old reference (r,S,T,A,B) -> h and new (u,w,h).
SS=v-c-a*u;TT=a*w-v+c
old_h=(SS*TT+c*(SS-TT)+2*delta)/(2*c*delta)
assert s.cancel(s.rem((old_h-h).subs(w,1/(a*u)),curve,h))==0
record={'status':'PASS','generic_assumptions':'a*c*(a-c²)*((2a-c²)²-4ac²)!=0; characteristic0','quadrics':[str(s.expand(z)) for z in q],'generic_identities':5,'exceptional_A_coefficient':'-4*a²*c*w !=0','exceptional_B_coefficient':'-4*a²*c*u !=0','constant_checks':vals,'reference_coordinates':5,'extra_guards':0,'full_quartic_record_claim':False}
alt_a=1+rho;alt_c=4-2*rho;alt_delta=s.expand(alt_a-alt_c**2)
alt_Delta=s.expand((alt_a+alt_delta)**2-4*alt_a*alt_c**2)
assert s.expand(alt_a*alt_delta-(11-6*rho))==0
assert s.expand(alt_Delta-(1164-824*rho))==0
record['translator_R0']={}
for name,z in [('a',alt_a),('c',alt_c),('delta',alt_delta),('Delta',alt_Delta)]:
    norm=s.simplify(z*z.xreplace({rho:-rho}));assert norm!=0
    record['translator_R0'][name]={'value':pair(z),'norm':str(norm)}
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('certificate.json'))
args=parser.parse_args()
args.output.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':record['status'],'generic_identities':5,'extra_guards':0,'output':str(args.output)}))
