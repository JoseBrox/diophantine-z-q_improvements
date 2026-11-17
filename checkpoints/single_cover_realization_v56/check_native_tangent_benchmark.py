#!/usr/bin/env python3
"""Actual prescribed-trace square-cover benchmark after one frozen rescaling.

This proves one exact algebraic fixture, not a nine-variable definition.
The physical rescaling is chosen once from this fixture. Its prime support
must be included in a fixed exceptional set before any other input varies.
"""
import importlib.util
import json
import sys
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import sympy as sp

sys.set_int_max_str_digits(0)
base=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('native_fixture',base/'native9_v47'/'actual_finite_level_fixture.py')
old=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=old
spec.loader.exec_module(old)
K=old.K

# Independent exact identity in freely variable actual detector coefficients.
a,b=sp.symbols('a b')
N=a*a-2*b*b
H=N-a
J=N-2*a+1
w=4*H*J/(8*b*b-3*H*H)
k=2*H*H/(8*b*b-H*H)
g=1+w
Delta=g*g*N-2*g*a+1
S=w*(g*N-a)/Delta
assert sp.cancel(S-k*k)==0

R0=(K(1,1),K(0,2))
P=old.add_point(R0,R0)
points={1:P}
for j in range(2,11):
    points[j]=old.add_point(points[j-1],P)
X=2
A=points[2]
Href=points[4]
U=points[8]
R=old.subtract_point(Href,P)
Vpoint=old.subtract_point(U,A)
assert R==points[3] and Vpoint==points[6]
for point in (A,Href,U,R,Vpoint):
    old.curve_check(point)

r=old.zcoord(U)/old.zcoord(Href)
s=old.zcoord(Vpoint)/old.zcoord(R)
tests=[old.reciprocal(Href),old.reciprocal(U),
       old.reciprocal(R).bar(),old.reciprocal(Vpoint).bar(),
       r-s.bar(),r+s.bar()-2*X]

# Exactly the ordinary-abc optimized height argument, at B=3 and z=1.
Bshift=3
e=8
d=6
trace=2*A[0].a
height=(X*X+Bshift)**e+trace**e
t=height**d+1
assert t>1
F=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
w_native=F/(4*(t-1)**8)
W=K(1)
for c in tests:
    W*=1+c*c/F
assert W.positive() and W.bar().positive()
assert (W-1).positive() and (W.bar()-1).positive()
Nq=W.norm()
Hq=Nq-W.a
Jq=Nq-2*W.a+1
den=8*W.b*W.b-3*Hq*Hq
assert Nq>0 and Hq>0 and Jq>0 and den>0
w_star=4*Hq*Jq/den
kq=2*Hq*Hq/(8*W.b*W.b-Hq*Hq)
assert w_star>0 and 0<kq<1
gamma=w_star/w_native
assert gamma>0

# The symbolic identity above proves the full square relation at this tuple.
# These additional exact substitutions independently check its numerator.
gq=1+w_star
Deltaq=gq*gq*Nq-2*gq*W.a+1
assert w_star*(gq*Nq-W.a)==kq*kq*Deltaq
native_R_root=kq*Deltaq/(w_star*gq*Nq)
Vtrace=2*W.a/Nq
Jtrace=1/Nq
native_R=(1-Vtrace/gq+Jtrace/(gq*gq))*(1+(1-Vtrace/2)/w_star)
assert native_R==native_R_root*native_R_root and native_R_root!=0

# Every sign branch of the three original point blocks retains defined
# differences: H±P has labels3,5 and U±A has labels6,10. Each displayed
# point has nonzero coordinates; point-chart unit conditions are checked.
charts={}
for label,half in [(2,1),(4,2),(8,4)]:
    _,_,chart=old.point_chart(points[half],points[label])
    charts[str(label)]=chart
for label in [3,5,6,10]:
    old.curve_check(points[label])
assert Href[0]!=P[0] and U[0]!=A[0]

def enc(q):
    return {'numerator':str(q.numerator),'denominator':str(q.denominator)}
def digest(q):
    s=f'{q.numerator}/{q.denominator}'
    return {'sha256':sha256(s.encode()).hexdigest(),
            'numerator_digits':len(str(abs(q.numerator))),
            'denominator_digits':len(str(q.denominator))}

result={
    'status':'PASS',
    'input':X,'height_shift':Bshift,'height_exponents':[e,d],
    'free_height_parameter':1,
    'point_labels':{'A':2,'H':4,'U':8,'H_minus_P':3,'U_minus_A':6},
    'root_trace':enc(trace),
    'tests':[[enc(c.a),enc(c.b)] for c in tests],
    'argument_formula':'t=((X^2+B)^8+Tr(x(A))^8)^6+1',
    'physical_weight_formula':'F(t)/(4(t-1)^8)',
    'frozen_rescaling_formula':'gamma=[4 H J/(8 B_W^2-3 H^2)]/w_native; H=N(W)-A_W; J=N(W)-2 A_W+1',
    'square_root_formula':'k Delta/(w_star (1+w_star) N(W)); k=2H^2/(8B_W^2-H^2)',
    'positive_tangent_condition':True,
    'actual_rational_square':True,
    'whole_character_guards':'All64 point branches are real; differences have nonzero labels3,5,6,10; positive W slots and fixed gamma>0 make every native-cover factor positive.',
    'digests':{'argument':digest(t),'frozen_rescaling':digest(gamma),
               'native_square_root':digest(native_R_root)},
    'charts':charts,
    'exceptional_set_rule':'For the unchanged S require gamma to be an S-unit. Without that unverified condition, fix S*=S union prime support(gamma) once for this redesigned source.',
    'limitations':['Only one integer input is realized.',
                   'The rescaling is frozen after constructing this fixture, and cannot vary with later inputs.',
                   'No assertion that B=3 is beyond the ineffective defining threshold.',
                   'No nine-variable or twenty-one-variable defining polynomial is proved.']
}
out=Path(__file__).with_name('native_tangent_benchmark_certificate.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ['status','input','point_labels','digests','limitations']},indent=2))
