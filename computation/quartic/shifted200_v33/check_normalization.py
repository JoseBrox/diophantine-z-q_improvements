#!/usr/bin/env python3
"""Check physical ratio normalization independently of the coefficient generator."""
import argparse,json
from fractions import Fraction
from pathlib import Path
import sympy as s

def need(ok,msg):
    if not ok:raise AssertionError(msg)
def compute():
    R,l,lp,t,b=s.symbols('R l lp t b',nonzero=True)
    # The root-product chart stores R*l. Its cross squares and Lucas products
    # are normalized by R^2 and R in the literal retained equations.
    new=2*R*l+2*R;newp=2*R*lp+2*R
    need(s.expand((new-2*R)/2-R*l)==0,'Forward root chart')
    need(s.cancel(new/R-(2*l+2))==0,'Physical shifted label')
    need(s.cancel((new-newp)**2/R**2-4*(l-lp)**2)==0,'Cross normalization')
    C=s.cancel(new*b/R);AT=s.cancel(new*t/R)
    residual=t*t+4*b*b-4*b*C+2*b*AT+C*C-C*AT-1
    A=2*l+2
    target=t*t-A*(A-2)*t*b+(A-2)**2*b*b-1
    need(s.cancel(residual-target)==0,'Literal normalized Lucas circuit')
    wrong=2*R*l+2
    need(s.cancel(wrong/R-A)!=0,'Reject the old constant shift')
    examples=[]
    for r in [Fraction(101),Fraction(149),Fraction(12345,7)]:
        for a in [-7,0,3,11]:
            stored=2*r*a+2*r
            need(stored/r==2*a+2,'Exact normalized value')
            need((2*r*a+2)/r!=2*a+2,'Old formula differs')
            examples.append({'R':str(r),'index':a,'stored':str(stored),'physical':2*a+2})
    return dict(status='PASS',symbolic_identities=4,exact_normalization_examples=examples,
                old_shift_rejected=True,scope='Physical scalar-ratio normalization and the exact Lucas circuit; not an audit of external arithmetic inputs.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();r=compute()
    text=json.dumps(r,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    else:print(text)
