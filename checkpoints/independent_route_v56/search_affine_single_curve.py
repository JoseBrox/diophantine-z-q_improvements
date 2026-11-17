#!/usr/bin/env python3
"""Bounded exact point search only; absence is not a proof of non-solubility."""
from math import gcd,isqrt
from fractions import Fraction
import json
from pathlib import Path

def first_point(u,H):
 for s in range(1,H+1):
  s3=s*s*s; s4=s3*s
  for r in range(-H,H+1):
   if gcd(r,s)!=1: continue
   n=4*u**3*r**4+u*r*s3+u*s4
   w=isqrt(n)
   if w*w==n and w:
    x=Fraction(r,s);z=Fraction(w,u*s*s);c=2*u
    assert c*z*z==2*(c*c*x**4+x+1)
    return {'x':str(x),'z':str(z)}
 return None

H=300
results=[]
for b in range(0,11):
 u=1+2*b
 point=first_point(u,H)
 row={'b':b,'c':2*u,'height_bound':H,'point':point}
 results.append(row)
 print(row,flush=True)
Path(__file__).with_name('affine_single_curve_search.json').write_text(json.dumps(results,indent=2)+'\n')
