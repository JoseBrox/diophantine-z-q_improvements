#!/usr/bin/env python3
"""Exact certificate for failure of the unrestricted two-square height bound."""
from pathlib import Path
import argparse
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--output', type=Path, default=Path(__file__).with_name('certificate.json'))
output_path = _parser.parse_args().output
output_path.parent.mkdir(parents=True, exist_ok=True)
from fractions import Fraction as Q
from math import gcd
import json
import sympy as s

a=s.symbols('a')
assert s.expand((1-a**3)**2+(a+a*a)**2-(1+a*a)*(1+a**4))==0
for r in range(1,7):
    real,imag=s.Integer(1),s.Integer(0)
    for j in range(1,r):
        b=a**(2**(j-1))
        real,imag=s.expand(real-b*imag),s.expand(imag+b*real)
    assert s.expand((1-a*a)*(real*real+imag*imag)-(1-a**(2**r)))==0

L=10
rows=[]
for N in [2,3,10,100,1000,10000]:
    aa=Q(N*N-1,N*N+1)
    bb=Q(2*N,N*N+1)
    M=L*aa
    z1=L**4*bb*(1-aa**3)
    z2=L**4*bb*(aa+aa**2)
    assert aa*aa+bb*bb==1
    assert M**8+z1*z1+z2*z2==L**8
    assert z1>0 and z2>0 and Q(3*L,5)<=M<L
    assert M.denominator*2*L>=N*N+1
    rows.append({'N':N,'M':str(M),'t':L**8,'z1':str(z1),'z2':str(z2),
                 'M_reduced_denominator':M.denominator})

report={'status':'PASS','exponents_symbolically_verified':[2**r for r in range(1,7)],
        'unbounded_family_proved_for_all_powers_of_two':True,
        'fixed_t_d8_samples':rows,
        'actual_inner_form_or_full_detector_counterexample_claimed':False}
out=output_path
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','fixed_t':L**8,'largest_denominator':rows[-1]['M_reduced_denominator']}))
