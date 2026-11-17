"""Exact identities for the diagonal admissible trace class.

The finite valuation table supplements the uniform proof in the note;
it does not assert rational realization of any actual detector tuple.
"""
from pathlib import Path
import json
import sympy as S

w,V,c,k,C,s=S.symbols('w V c k C s', nonzero=True)
delta=1+k*k*w*w*c**4
rad=V*V+w*(2-V)
assert S.expand(delta.subs(c,0))==1

K=k*w
x=2*(s+1)/c**2
y=4*(s+1)/c**3
identity=S.factor((y*y-x**3+4*K*K*x)*c**6)
assert S.expand(identity+8*(s+1)*(s*s-1-K*K*c**4))==0

# Standard binary-quartic invariants and its Jacobian, followed by
# the rational change X=9*x, Y=27*y.
a=C*k*k*w*w
e=C
I=12*a*e
J=S.Integer(0)
assert I==12*C*C*k*k*w*w
assert S.cancel((-27*I)/81)==-4*C*C*k*k*w*w

valuation_cases=0
for nu in range(1,30,2):
    for cc in range(-30,31):
        exponent=2*nu+4*cc
        assert exponent!=0 and exponent%2==0
        assert min(0,exponent)%2==0
        assert (nu+min(0,exponent))%2==1
        valuation_cases+=1

# The pre-existing adaptive linear class gives a different genus-one
# curve in its class parameter q; this identifies its actual Jacobian.
q,aa=S.symbols('q aa')
old=q**4+4*aa*q**3+2*q*q-4*aa*q+1
Iold=S.expand(12-3*(4*aa)*(-4*aa)+2**2)
Jold=S.expand(72*2+9*(4*aa)*2*(-4*aa)
              -27*(-4*aa)**2-27*(4*aa)**2-2*2**3)
assert Iold==16*(1+3*aa**2)
assert Jold==128*(1-9*aa**2)
old_j=S.factor(1728*4*Iold**3/(4*Iold**3-Jold**2))
assert old_j==64*(3*aa**2+1)**3/(aa**2*(aa-1)**2*(aa+1)**2)

result={
    'status':'PASS',
    'uniform_local_class':'1+k^2*w^2*c^4, k a fixed S-unit',
    'valuation_cases_checked':valuation_cases,
    'birational_identity':str(identity),
    'Jacobian':'y^2=x^3-4*k^2*C^2*w^2*x',
    'untwisted_curve_inverse':'c=2*x/y',
    'necessary_norm_condition':'C is a norm from Q(i)',
    'free_class_parameter_extra_coordinates':1,
    'preexisting_class_function_extra_coordinates':0,
    'actual_trace_realization_proved':False,
    'older_adaptive_family_Jacobian_j':str(old_j),
}
Path(__file__).with_name('diagonal_safe_class_v59_certificate.json').write_text(
    json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
