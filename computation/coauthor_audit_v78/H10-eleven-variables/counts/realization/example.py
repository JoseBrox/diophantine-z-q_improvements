from fractions import Fraction as F
from math import isqrt
import sys
sys.set_int_max_str_digits(0)
P=(F(8),F(24))
def add(p,q):
 if p is None:return q
 if q is None:return p
 x,y=p;z,w=q
 if x==z and y==-w:return None
 m=(3*x*x+8)/(2*y) if p==q else (y-w)/(x-z)
 xx=m*m-x-z
 return xx,m*(x-xx)-y
pm=None
for n in range(1,120):
 pm=add(pm,P)
 if not n%2:continue
 x,y=pm;u=x/8
 v=F(isqrt(u.numerator),isqrt(u.denominator));assert v*v==u
 for z in (y/(8*v),-y/(8*v)):
  d=(1+2*v*v-z)/2
  if not(0<d<1):continue
  val=lambda z:(abs(z)&-abs(z)).bit_length()-1
  vd=val(d.numerator)-val(d.denominator)
  if vd<4 or vd%2:continue
  un=d/2**vd
  if un.numerator*pow(un.denominator,-1,8)%8!=7:continue
  assert isqrt(d.denominator)**2==d.denominator
  assert (d+v*v)**2*v**4==(d-v*v)**2*(1-d)**2
  print(n,vd,len(str(d)),len(str(v)),'d',str(d)[:110],'v',str(v)[:115],flush=True)
  exit()
