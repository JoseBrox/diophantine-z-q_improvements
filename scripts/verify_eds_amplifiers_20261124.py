#!/usr/bin/env python3
"""Exact local algebra and finite fixtures for the 2026-11-24 EDS amplifiers.
These tests do not prove weak abc, (SD), rank, or prime-pattern inputs.
"""
from fractions import Fraction as Q
from math import comb, gcd, prod
from itertools import product

# Infinity is used only in valuation comparisons with zero.
INF = float('inf')
def vp(x, p):
    x = Q(x)
    if x == 0:
        return INF
    a, b = abs(x.numerator), x.denominator
    n = 0
    while a % p == 0:
        a //= p; n += 1
    while b % p == 0:
        b //= p; n -= 1
    return n

def k(a=0,b=0): return Q(a),Q(b)
def add(a,b): return a[0]+b[0],a[1]+b[1]
def neg(a): return -a[0],-a[1]
def sub(a,b): return add(a,neg(b))
def mul(a,b): return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def inv(a):
    norm=a[0]**2-2*a[1]**2
    if not norm: raise ZeroDivisionError
    return a[0]/norm,-a[1]/norm
def div(a,b): return mul(a,inv(b))
def power(a,n):
    if n<0: return power(inv(a),-n)
    ans=k(1)
    while n:
        if n&1: ans=mul(ans,a)
        a=mul(a,a); n//=2
    return ans

D=k(11,-6)
P=(k(Q(57,8),-Q(7,2)),k(-Q(165,8),Q(417,32)))
assert power(P[1],2)==sub(power(P[0],3),mul(D,P[0]))
def ecadd(A,B):
    if A is None:return B
    if B is None:return A
    x,y=A; X,Y=B
    if x==X:
        if add(y,Y)==k():return None
        m=div(sub(mul(k(3),power(x,2)),D),mul(k(2),y))
    else:m=div(sub(Y,y),sub(X,x))
    xx=sub(sub(power(m,2),x),X)
    return xx,sub(mul(m,sub(x,xx)),y)

def z(A):return neg(div(*A))
points={1:P}
for n in range(2,13):
    points[n]=ecadd(points[n-1],P)
    X,Y=points[n]
    assert power(Y,2)==sub(power(X,3),mul(D,X))

# At simple-denominator primes of the quadratic carrier the unequal powers
# have a strict negative odd minimum. The synthetic check includes all
# possible negative valuations of each component; positive ones are harmless.
for a,b in product(range(-3,13),repeat=2):
    if min(a,b)==-3:
        assert 5*a!=7*b
        assert min(5*a,7*b)==(-21 if b==-3 else -15)

# Exhaust the odd-valuation Boolean selector profiles, including zero F.
profiles=0
for nu in range(-41,42,2):
    for xx,r in product(range(-16,17),list(range(-30,31))+[INF]):
        vz=2*nu-24*xx
        assert vz%4==2
        chi_res=int(vz>0)
        assert 2*r!=-nu
        j_res=int(2*r < -nu)
        good=chi_res*(1-j_res)
        if nu<0 and good:
            assert xx<0 and 2*r>-nu
        profiles+=1
for p in (3,5,7,11,13):
    for a,b in product((0,1),repeat=2):
        assert ((2-a-b)%p==0)==(a==b==1)

# Actual number-field point fixtures: reject arbitrary small j at a prime
# of max formal depth one for Q=[c]P. The test computes the entire rational
# b, not merely a residue of one of its components.
fixtures=0
for c,A in points.items():
    ps=[p for p in (3,5,11,13,17,19,23,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)
        if min(vp(v,p) for v in A[0])==-2]
    for p in ps:
        assert min(vp(v,p) for v in A[1])==-3
    if not ps:continue
    for eps in (1,2):
        ell=A[1][0]**5+eps*A[1][1]**7
        assert ell!=0
        for p in ps: assert vp(ell,p) in (-15,-21)
        for j in (1,2,3,5,8):
            T=points[j]
            Z=div(k(ell**2),power(T[0],24))
            chi=inv(add(k(1),Z))
            F=div(z(T),z(A)); F2=power(F,2)
            J=div(F2,add(k(1/ell),F2))
            C=2-2*mul(chi,sub(k(1),J))[0]
            b=1+ell*C*C
            assert b!=0
            for p in ps:
                assert j%(p**8)!=0
                vb=vp(Q(112,841)*b,p)
                assert vb<0 and vb%2, (c,j,p,eps,vb)
                fixtures+=1
assert fixtures>0

# Normalized multiplicity surplus cost after removal of a rational prime
# with any high-exponent slot. Check several degrees and all small profiles.
for degree in range(1,7):
    for exps in product(range(5),repeat=degree):
        if max(exps)<2:continue
        assert sum(exps)<=(degree+1)*sum(max(0,a-1) for a in exps)

# Mobius identity: v_p is a sum of the positive-power indicators.
def mu(n):
    s=1;p=2
    while p*p<=n:
        if n%p==0:
            n//=p;s=-s
            if n%p==0:return 0
        p+=1
    return -s if n>1 else s
for n in range(1,151):
    ds=[b for b in range(1,n+1) if n%b==0]
    for p in (2,3,5,7):
        assert sum(mu(n//b)*vp(b,p) for b in ds)==int(n>1 and n==p**vp(n,p))

# Six-coordinate quotient margins, both ordinary and fixed weak abc.
assert Q(1,5)-Q(10,299)>Q(1,7)
assert Q(3,5)-Q(10,299)>Q(1,2)
assert Q(147,242)-Q(16,27)==Q(97,6534)>Q(1,100)
assert Q(147,242)-Q(3,5)==Q(9,1210)>Q(1,200)
assert Q(1,100)-Q(324,380000)>Q(1,120)
assert -2*401+8*99<0 and -2*40001+8*9999<0
assert Q(8,1)/Q(27,25)-6==Q(38,27)
assert Q(1,10000)/Q(38,27)==Q(27,380000)
assert 1-12*(1-1/Q(13,12))==Q(1,13)
for t in (1,31,37,41,46):
    zz=2+Q(60,t-61)
    assert zz=={1:1,31:0,37:-Q(1,2),41:-1,46:-2}[t]
for zz in map(Q,range(-20,21)):
    assert zz*(zz+2)**3-(2*zz+1)**3==(zz-1)**3*(zz+1)
for n in range(1,41):
    assert 3**(2*n)>4*n+1
assert 67**287>=120*2**342
assert 67**287-1>=2**1727
for k_scales in (2,3): assert 1+5*2+1+2*k_scales+2+1==15+2*k_scales
print(f'PASS: {profiles} valuation profiles, {fixtures} exact number-field rejection fixtures; all mass, Belyi, and count identities.')
