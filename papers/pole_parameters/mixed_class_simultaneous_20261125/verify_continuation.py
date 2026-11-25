from fractions import Fraction as F
from math import gcd, isqrt, prod
from itertools import product

def height(x):
    return max(abs(x.numerator), x.denominator)

def val(x,p):
    assert x
    n,d=abs(x.numerator),x.denominator
    a=0
    while n%p==0: a+=1; n//=p
    while d%p==0: a-=1; d//=p
    return a

def leg(a,p):
    t=pow(a%p,(p-1)//2,p)
    return -1 if t==p-1 else t

def prime(p):
    return p>=2 and all(p%i for i in range(2,isqrt(p)+1))

vs=[F(a,b) for a in range(-80,81) for b in range(1,81) if gcd(a,b)==1]
count=0
for v in vs:
    w=v/(1+7*v*v)
    assert val(w,7)>=0 if w else True
    assert height(v)**2<=7*height(w)<=56*height(v)**2
    for rho in (F(343,11),F(343,5),F(3,7),F(1,3),F(11**3,2),F(67,19)):
        alpha=1+rho*w*w
        assert 98*height(alpha)*height(rho)>=height(v)**4
        for p in (3,5,7,11,67):
            if val(rho,p)%2:
                assert val(alpha,p)<0 or alpha==1 or val(alpha-1,p)>0
        if val(rho,7)>=3:
            assert alpha==1 or val(alpha-1,7)>=3
        count+=1
print('height rechart: %d rationals, %d scale cases'%(len(vs),count))

J,A,B,C=33,97,313,1153
assert all(prime(p) for p in (3,11,A,B,C,66509,1009,1013,409))
assert all(x%8==1 for x in (J,A,B,C))
for x in (A,B,C):
    for y in (3,11,A,B,C):
        if x!=y:
            assert leg(x,y)==leg(y,x)==1
j1,j2,j3=J*A,J*B,J*C
d1,d2,d3=F(16*j1,1009**2),F(16*j2,409**2),F(16*j3,1013**2)
for d in (d1,d2,d3):
    assert 0<d<1 and isqrt(d.denominator)**2==d.denominator
    assert val(d,2)==4 and (d.numerator//16)*pow(d.denominator,-1,8)%8==1
f2=1+d2
assert f2==F(5*66509,409**2) and gcd(f2.numerator,J*A*B*C)==1
assert leg(j2,66509)==leg(-1,66509)==1 and leg(j3,66509)==-1
for k in range(10):
    den=409+2*k*66509**2*J*A*B*C
    d=F(16*j2,den**2)
    assert val(1+d,66509)==1 and gcd((1+d).numerator,J*A*B*C)==1
print('three-pole fixture and 10 denominator lifts: passed')

psi=prod(3*j+1 for j in range(2,91))
kappa=27160+16032*psi
t=2**20*(16*kappa+2**186+1)*(2**186+3)
assert kappa>342+3*4000000 and t<2**826 and t>1024
assert 2**1024>588**3*1024**12 and 2*1024**12>1025**12
for H in (1024,1025,2048,10**6, t):
    L=3+171033184*(H+1)**2
    assert L%171033184==3 and L%2==1 and 6*(2*L+1)>H**2
print('BB record parameters and strict threshold inequalities: passed')

count=0
for r,k,ell,m,a in product(range(-3,4),range(-3,4),range(-3,4),range(-3,4),(-10,-4,4,10)):
    if not k: continue
    def g(b):
        u=-r*a-ell*b-m
        return u*u-k*a*(a-2)*u*b+k*k*(a-2)**2*b*b-k*k
    assert (g(1)+g(-1)-2*g(0))//2==ell**2+k*ell*a*(a-2)+k*k*(a-2)**2
    count+=1
print('fixed-word Lucas coefficient: %d cases'%count)
M=3**6*5**4*7**3
for h in (17,-23,2):
    for l in range(10):
        m=(M+1)//2+l*M
        j=h+m*h*(h-1)
        assert j%h==0 and (j-1)%(h-1)==0
        assert F(j-1,h-1)-F(j,h)==m and (2*m-1)%M==0
print('double-divisibility local comparison: 30 exact CRT fixtures')
