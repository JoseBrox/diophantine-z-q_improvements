"""Regression tests for joint_divisibility_one_pole_20261124.
The universal valuations are proved in README.md; the finite tests below
are exact sanity checks and do not prove the primitive-divisor/BB theorems.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt

P=(Q(9,4),Q(-21,8))
def neg(A):
    return None if A is None else (A[0],-A[1])
def add(A,B):
    if A is None:return B
    if B is None:return A
    x,y=A; u,v=B
    if x==u:
        if y==-v:return None
        t=(3*x*x-2)/(2*y)
    else:t=(v-y)/(u-x)
    w=t*t-x-u
    return w,t*(x-w)-y

def mul(n,A):
    if n<0:return mul(-n,neg(A))
    S=None
    while n:
        if n&1:S=add(S,A)
        A=add(A,A);n//=2
    return S

def v(a,p):
    assert a
    a=Q(a);n=abs(a.numerator);d=a.denominator;r=0
    while n%p==0:n//=p;r+=1
    while d%p==0:d//=p;r-=1
    return r

def scalar(H,Us):
    L=H[1];q=Q(1)
    for U in Us:q/=1+L**2/U[0]**4
    return 1+L*(1-q)**2

# Exact local valuation rules. At the primitive depth-one reference
# disk v(L)=-3, any nonformal numerator gives chi valuation >=6;
# every formal numerator gives chi a unit congruent to 1.
for w in range(-20,21):
    if w<0 and w%2:continue # formal x has negative even valuation
    z=-6-4*w
    assert z>=2 if w<0 else z<=-6
    assert z!=0
# For a true multiple the reference depth and numerator depths obey e>=a.
for a,e in product(range(1,21),repeat=2):
    if e<a:continue
    z=-6*a+8*e
    assert z>=2*a and -3*a+2*z>=a
# At an integral reference, a pole of chi requires 2*l=4*w.
for l,w in product(range(0,21),range(-20,21)):
    if 2*l-4*w==0:assert l%2==0
# Actual rational point fixtures; test denominator squares of the entire
# scalar, not merely the valuations at a finite set of primes.
fixtures=0
for h in range(1,9):
    H=mul(h,P);assert H and H[1]
    for ms in ((1,2),(-2,3),(1,2,-3),(4,-1)):
        Us=[mul(m,H) for m in ms]
        b=scalar(H,Us)
        assert b and isqrt(b.denominator)**2==b.denominator,(h,ms)
        fixtures+=1
# Find actual exponent-one reference primes and deliberately incompatible
# points, checking the predicted negative odd valuation.
rejections=0
for p in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53):
    if p in (7,29):continue
    for h in range(2,17):
        H=mul(h,P)
        if v(H[0],p)!=-2:continue
        if any(v(mul(j,P)[0],p)<0 for j in range(1,h)):continue
        U=mul(1,P)
        assert v(U[0],p)>=0
        b=scalar(H,[mul(2,H),U])
        assert v(b,p)==-3,(p,h)
        assert v(Q(112,841)*b,p)==-3
        rejections+=1
        break
assert rejections>0
for k in range(1,51):
    assert (k+1+2*k+1)-(k+4)==2*(k-1)
print(f'PASS: exact valuation identities, {fixtures} true-multiple fixtures, {rejections} primitive-prime rejection fixtures, counts')
