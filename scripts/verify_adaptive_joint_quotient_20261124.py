#!/usr/bin/env python3
"""Exact arithmetic checks for the adaptive joint quotient transfer.
The elliptic mass, abc and BB inputs are theorems/retained premises,
not verified by these finite fixtures.
"""
from fractions import Fraction as Q
from itertools import product
from math import gcd

def f(t):
    a=Q(1)
    for l in range(1,11): a*=t-l
    return a

def phi(t):
    return t/(1+t)**2

def val(n,p):
    if not n: return None
    n=Q(n); a=abs(n.numerator); b=n.denominator; v=0
    while a%p==0: a//=p; v+=1
    while b%p==0: b//=p; v-=1
    return v

def primes(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,int(p**0.5)+1))]

F0=f(100)
assert Q(361,360)**10<2
ps=[p for p in primes(197) if p not in (2,7,29) and F0.numerator%p]
# Compare complete rational recursion with the abstract persistence rule,
# including previously odd negative valuations of the seed.
xs=[Q(0),Q(1),Q(-3),Q(2,3),Q(-1,5),Q(5,11),Q(17,7),Q(23,13),Q(31,17)]
seeds=[Q(1),Q(101),Q(1,101),Q(103,107),Q(109**2)]
checks=0; captures=0; persistent=0
for s0,x in product(seeds,xs):
    t=100+phi(s0*x*x); s1=s0*f(t)/F0
    assert Q(100)<=t<=Q(401,4)
    assert 1<=s1/s0<2
    den=t.denominator
    from math import isqrt
    assert isqrt(den)**2==den
    for p in ps:
        a=val(s0,p); b=val(f(t),p); c=val(s1,p)
        if a%2:
            assert b==0 and c==a
            persistent+=1
        if b>0 and b%2:
            assert a%2==0 and c%2==1
            assert val(phi(s1),p)>0 and val(phi(s1),p)%2==1
            captures+=1
        checks+=1
for xx in [(Q(1,5),Q(2,3)),(Q(7,5),Q(-3,11)),(Q(0),Q(1,13),Q(2))]:
    s=Q(1); seen=set()
    for x in xx:
        t=100+phi(s*x*x)
        seen.update(p for p in ps if val(f(t),p)>0 and val(f(t),p)%2)
        s*=f(t)/F0
    u=phi(s)
    assert 4<=1/u<=2**len(xx)+3
    for p in seen: assert val(u,p)>0 and val(u,p)%2
# Abstract local inequalities; explicit constants in the proof.
profiles=0
for k in range(1,501):
    K=1000*(k+1)**2; gamma=Q(299,50)
    assert (40*k+Q(k,4)+Q(5,2)*k*(k-1))/(gamma*K)<=Q(1,100)
for K in (10,100,4000):
    for a in range(K):
        for mu in (1,3,7,13):
            nu=-(4*K+1)*mu
            assert -3*a>nu and 2*nu+8*a<0
            profiles+=1
for a in range(1,51):
    for c in range(-100,101):
        if a%2:
            # Failure fraction T: valuation of F^2/(p^(3a)+F^2)
            vT=2*c-min(3*a,2*c)
            assert vT>=0 and (vT>0)==(2*c>3*a)
        if c>=4*a:
            assert 2*c-3*a>=5*a
        assert -3*a+4*a==a
        profiles+=1
for b in range(1,101):
    assert 3**(2*b)>4*b+1
    for p in (3,5,7,11,29,149):
        assert 4*b-val(4*b+1,p)>=2*b
# Exact non-growing rational Lucas witnesses and simultaneous congruence
# fixtures. The integer labels need not solve the residual exactly.
def delta(a,t,m):
    v=(a-1)*(2*m+1)
    return t*t-(a+1)*t*v+v*v-1
crt_count=0
for L in range(1,9):
    a=6*7*29*149**L
    m=Q(1,a-1)
    assert delta(a,1,m)==0 and val(2*m+1,2)==0
    target=(Q(1,5),Q(a),Q(1),m)
    local=[p for p in (2,3,7,11,13,17,29,149) if all(x.denominator%p for x in target)]
    assert {2,7,29,149}.issubset(local)
    mods=[p**(L+6) for p in local]
    P=1
    for d in mods:P*=d
    reps=[sum((x.numerator*pow(x.denominator,-1,d)%d)*(P//d)*pow(P//d,-1,d) for d in mods)%P for x in target]
    reps=[x+P for x in reps]
    for p,d in zip(local,mods):
        for x,y in zip(target,reps):
            assert (y*x.denominator-x.numerator)%d==0
        assert delta(*reps[1:])%d==0
        crt_count+=1
    # Changing one coordinate by the entire modulus preserves all tests.
    assert any(delta(reps[1],reps[2]+i*P,reps[3])!=0 for i in (1,2,3))
    for i in (1,100,10000):
        assert delta(reps[1],reps[2]+i*P,reps[3])%P==0
print('PASS:',checks,'exact recursion prime checks,',captures,'new odd contacts,',persistent,'persistent odd valuations;',profiles,'local inequality profiles;',crt_count,'Lucas CRT fixtures; 500 height constants.')

# Independent charge checks using actual rational elliptic points.
def add(P,Qp):
    if P is None: return Qp
    if Qp is None: return P
    x,y=P; z,w=Qp
    if x==z and y==-w: return None
    slope=(w-y)/(z-x) if x!=z else (3*x*x-2)/(2*y)
    u=slope*slope-x-z
    return u,slope*(x-u)-y
R=(Q(2),Q(2)); P=add(R,R); Rn=None; Pn=None
assert P==(Q(9,4),Q(-21,8))
gs=[]
for n in range(1,9):
    Rn=add(Rn,R); Pn=add(Pn,P)
    x,y=Rn; g=(x*x+2)/(2*y)
    assert Pn[0]==g*g and Pn[1]**2==Pn[0]**3-2*Pn[0]
    gs.append(g)
charge_profiles=0
for r in range(1,7):
    for vv in product(range(-1,4),repeat=r):
        if -1 not in vv: continue
        tagged=[(2*i+1)*v for i,v in enumerate(vv)]
        top=max(i for i,v in enumerate(vv) if v==-1)
        assert min(tagged)==-(2*top+1) and tagged.count(min(tagged))==1
        assert ((-min(tagged))+1)//2==top+1
        charge_profiles+=1
charge_fixtures=0; charge_conics=0
for ii in product(range(8),repeat=3):
    gg=[gs[i] for i in ii]
    L=sum(g**(2*i+1) for i,g in enumerate(gg))
    if L==0: continue
    t=Q(1 if L!=1 else 2)
    s=2*t/(1-L*t*t); u=(1+L*t*t)/(1-L*t*t)
    assert s and u*u==1+L*s*s
    charge_conics+=1
    for p in primes(197):
        vv=[val(g,p) for g in gg]
        if -1 not in vv or min(vv)<-1: continue
        top=max(i for i,v in enumerate(vv) if v==-1)
        assert val(L,p)==-(2*top+1) and val(s,p)>=top+1
        charge_fixtures+=1
print('PASS:',charge_profiles,'shared-charge valuation profiles;',charge_conics,'exact rational conics;',charge_fixtures,'elliptic prime fixtures.')
