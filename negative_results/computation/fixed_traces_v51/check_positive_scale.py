#!/usr/bin/env python3
"""Exact certificates for the actual-test positive-slope obstruction."""
from pathlib import Path
import json
import sympy as s

r=s.sqrt(2)
embeddings=[]
for sign in (1,-1):
    rr=sign*r
    p=(57-28*rr)/8
    q=(-660+417*rr)/32
    D=(3-rr)**2
    assert s.simplify(q*q-p**3+D*p)==0
    embeddings.append((p,q,D))
p,q,D=embeddings[0]
assert bool(p>0) and bool(p<s.Rational(11,5))
assert bool(abs(q)<s.Rational(9,4))
assert bool(p*p-D<s.Rational(9,4))
assert bool(s.sqrt(D)<2)
first=s.Rational(1600,841)*(s.Rational(11,5)+s.Rational(9,32)+s.Rational(45,28))
assert first==s.Rational(45790,5887) and first<8
assert s.Rational(14,5)**2<8
p,q,D=embeddings[1]
assert bool(p>0) and bool(p<s.Rational(49,4))
assert bool(abs(q)<s.Rational(157,4))
assert bool(p*p-D<127)
assert bool(s.sqrt(D)<5)
second=s.Rational(192,143)**2*(s.Rational(49,4)+s.Rational(127,48)+s.Rational(785,69))
assert second==s.Rational(22275840,470327) and second<48
assert s.Rational(69,10)**2<48

t=s.symbols('t')
F=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
w=F/(4*(t-1)**8)
alpha=(t-1)**4/F
assert s.cancel(w*alpha-1/(4*(t-1)**4))==0
small=s.factor((w/t).subs(t,s.Rational(1,16)))
assert small==s.Rational(12237824,854296875) and small<s.Rational(1,64)
assert s.factor(w.subs(t,4))==s.Rational(2431,8748)
assert s.factor(alpha.subs(t,4))==s.Rational(27,2431)
upper=s.Rational(11179,8748)*s.Rational(2539,2431)**6
assert upper<2
assert 16*64*2304==9*2**18
assert 4*(9*2**12)==147456
assert 20**4>147456

out={
 'status':'PASS_EXACT_POSITIVE_SLOPE_OBSTRUCTION_CERTIFICATES',
 'first_embedding_translation_bound':str(first),
 'second_embedding_translation_bound':str(second),
 'w_over_t_at_one_sixteenth':str(small),
 'normalized_product_bound_at_four':str(upper),
 'minimum_inner_positive_argument':'1/36864',
 'strict_scale_upper_bound':147456,
 'scope':'Actual guarded conditional reference-point tests, all positive slopes, simultaneous normalized unit trace only. No obstruction to negative slopes or unrestricted norm witnesses is asserted.',
}
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
certificate_path=parser.parse_args().output or Path(__file__).with_name('positive_scale_certificate.json')
certificate_path.parent.mkdir(parents=True,exist_ok=True)
certificate_path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
