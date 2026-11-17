#!/usr/bin/env python3
"""Independent arithmetic audit of the varying-squareclass height criterion."""
from fractions import Fraction as F
from pathlib import Path
import json
from math import gcd

def coefficients(kappa, e, d):
    alpha = F(e)/kappa-3
    gamma = F(8)/kappa-6
    epsilon = F(d)-kappa*(F(d,2)+2)
    assert min(alpha,gamma,epsilon)>0
    # Use the epsilon form rather than the source checker's closed quotient.
    C = kappa*(F(3*d,2)+1)/epsilon+2
    return alpha,gamma,C,C/(alpha*gamma)

original_single = [(F(25,24),16,10,F(33125,84357)),
                   (F(16,15),24,8,F(128,351)),
                   (F(121,100),64,12,F(40453083,103643216))]
for k,e,d,expected in original_single:
    *_,q=coefficients(k,e,d)
    assert q == expected
    assert F(5,2)*q < 1

two=[]
for k,e in [(F(36,35),6),(F(16,15),8),(F(121,100),14)]:
    alpha,gamma=F(e)/k-3,F(8)/k-6
    value=F(5)/(alpha*gamma)
    assert 0<value<1
    two.append({'kappa':str(k),'e':e,'alpha_gamma':str(alpha*gamma),
                'absorption':str(value)})

single=[]
for k,e,d in [(F(251,250),14,8),(F(301,300),14,8),
              (F(16,15),24,8),(F(121,100),64,12)]:
    a,g,C,q=coefficients(k,e,d)
    value=F(5,2)*q
    assert 0<value<1
    single.append({'kappa':str(k),'e':e,'d':d,'q':str(q),
                   'absorption':str(value),'height_argument_degree':2*e*d})

limit_pairs=[]
for e in range(4,112//6+1,2):
    for d in range(6,112//e+1,2):
        if e*d >= 112:
            continue
        a,g,C,q=coefficients(F(1),e,d)
        value=F(5,2)*q
        assert value>=1
        limit_pairs.append({'e':e,'d':d,'product':e*d,
                            'limiting_absorption':str(value)})
assert F(5,2)*coefficients(F(1),14,8)[-1] == F(85,88)
assert F(5,2)*coefficients(F(1),18,6)[-1] == 1

input_class_cases=0
for aa in range(-25,26):
    for qq in range(1,11):
        if gcd(aa,qq)!=1:
            continue
        delta_num=aa**4+qq**4
        assert gcd(delta_num,qq**4)==1
        for BB in (1,3,81,1001):
            beta_num=aa**2+BB*qq**2
            assert gcd(beta_num,qq**2)==1
            assert beta_num>=max(abs(aa),qq)**2
            assert delta_num<=2*beta_num**2
            assert 2*beta_num**2-delta_num == (
                aa**4+4*BB*aa**2*qq**2+(2*BB**2-1)*qq**4)
            input_class_cases+=1

report={'status':'PASS','two_cover_rows':two,'single_cover_rows':single,
        'all_smaller_even_pairs_at_kappa_one':limit_pairs,
        'ordinary_abc_two_cover_minimum_even_e_within_criterion':6,
        'ordinary_abc_single_cover_minimum_even_power_degree_within_criterion':224,
        'additional_input_squareclass':{
            'delta':'1+X^4','budget_k':2,
            'uniform_in_B':'B>=1',
            'exact_reduced_fraction_and_height_cases':input_class_cases,
            'universal_identity':'2(a^2+Bq^2)^2-(a^4+q^4)=a^4+4Ba^2q^2+(2B^2-1)q^4',
            'support_bound':'log rad_odd(delta)<=4h(X)+log2<=2E_h+log2',
            'extra_coordinate_or_guard':False},
        'coordinate_count_per_criterion':9,
        'actual_realization_proved':False,'new_defining_bound_proved':False}
Path(__file__).with_name('variable_classes_independent_certificate.json').write_text(
    json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
