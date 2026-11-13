#!/usr/bin/env python3
"""Exact checks accompanying the 2026-11-13 Sun/PR30 audit.

Python >=3.10, standard library only. This verifies finite identities and
certificates, not the universal arithmetic premises of either construction.
Run: python3 computation/sun_pr30_audit/check.py --output data/audits/sun_pr30_20261113.json
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
import json
from math import gcd
from pathlib import Path

@dataclass(frozen=True)
class K:
    a: F = F(0)
    b: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))
    @staticmethod
    def coerce(x):
        return x if isinstance(x, K) else K(x)
    def __add__(self, x):
        x = K.coerce(x); return K(self.a+x.a, self.b+x.b)
    __radd__ = __add__
    def __neg__(self): return K(-self.a, -self.b)
    def __sub__(self, x): return self + (-K.coerce(x))
    def __rsub__(self, x): return K.coerce(x) + (-self)
    def __mul__(self, x):
        x = K.coerce(x)
        return K(self.a*x.a+2*self.b*x.b, self.a*x.b+self.b*x.a)
    __rmul__ = __mul__
    def norm(self): return self.a*self.a-2*self.b*self.b
    def inv(self):
        n = self.norm()
        if not n: raise ZeroDivisionError('zero in Q(sqrt(2))')
        return K(self.a/n, -self.b/n)
    def __truediv__(self, x): return self * K.coerce(x).inv()
    def __rtruediv__(self, x): return K.coerce(x) * self.inv()
    def __pow__(self, n):
        if n < 0: return self.inv() ** (-n)
        out, base = K(1), self
        while n:
            if n & 1: out = out*base
            base = base*base; n >>= 1
        return out
    def encoded(self): return [str(self.a), str(self.b)]

rho = K(0, 1)
d = 3-rho
D = d*d
A = -D
R0 = (1+rho, 2*rho)
P = (K(F(57,8), F(-7,2)), K(F(-165,8), F(417,32)))
Point = tuple[K, K] | None

def on_curve(Q: Point) -> bool:
    return Q is None or Q[1]**2 == Q[0]**3+A*Q[0]

def add(U: Point, V: Point) -> Point:
    if U is None: return V
    if V is None: return U
    x,y = U; u,v = V
    if x == u:
        if y == -v: return None
        slope = (3*x*x+A)/(2*y)
    else: slope = (v-y)/(u-x)
    w = slope*slope-x-u
    return w, slope*(x-w)-y

def mul(n: int, Q: Point = P) -> Point:
    if n < 0:
        return mul(-n, None if Q is None else (Q[0], -Q[1]))
    out = None
    while n:
        if n & 1: out = add(out, Q)
        Q = add(Q,Q); n >>= 1
    return out

def vp(n: int, p: int) -> int:
    if n == 0: raise ValueError('valuation of zero is not finite')
    n = abs(n); out = 0
    while n % p == 0: n //= p; out += 1
    return out

def sqrt_lift(p: int, r: int, precision: int) -> int:
    if (r*r-2) % p: raise ValueError('not a root modulo p')
    mod = p
    for _ in range(1, precision):
        t = (-((r*r-2)//mod)*pow(2*r,-1,p)) % p
        r += t*mod; mod *= p
    assert (r*r-2) % mod == 0
    return r

def split_val(z: K, p: int, root: int, precision: int = 12) -> int:
    den = z.a.denominator*z.b.denominator//gcd(z.a.denominator,z.b.denominator)
    aa,bb = int(z.a*den), int(z.b*den)
    value = aa+bb*sqrt_lift(p,root,precision)
    if not value or vp(value,p) >= precision:
        raise ArithmeticError('insufficient precision to certify valuation')
    return vp(value,p)-vp(den,p)

def prime(n: int) -> bool:
    if n < 2: return False
    k = 2
    while k*k <= n:
        if n % k == 0: return False
        k += 1
    return True

def prime_factors(n: int) -> list[int]:
    n = abs(n); out=[]; p=2
    while p*p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0: n //= p
        p += 1
    if n > 1: out.append(n)
    return out

def norm_tree_coefficients(node, c=F(1,2)):
    if isinstance(node, str): return {node:c}
    return norm_tree_coefficients(node[0],c/2) | norm_tree_coefficients(node[1],(c+1)/2)

def main() -> dict:
    stages=[]
    def checked(name, condition):
        if not condition: raise AssertionError(name)
        stages.append({'name':name,'status':'PASS'})
    checked('explicit field and elliptic point identities', D==K(11,-6) and on_curve(R0) and on_curve(P))
    checked('duplication of R0', add(R0,R0)==P)
    Q=mul(2)
    checked('independent abscissa duplication formula', Q[0]==(P[0]**2+D)**2/(4*P[1]**2))
    expected=K(F(8226963211,2285245536),F(-1063929023,1713934152))
    checked('exact x(2P)', Q[0]==expected)
    checked('norm of x(P)', P[0].norm()==F(41**2,2**6))
    checked('norm of x(2P)', Q[0].norm()==F(593**2*8273**2,2**10*3**4*7**2*17**2*41**2))
    checked('prime factor identities used in the example', all(prime(p) for p in (3,7,17,41,593,8273)))
    vals={str(r):[split_val(P[0],41,r),split_val(Q[0],41,r)] for r in (17,24)}
    checked('opposite valuations at (41,rho-24)', vals=={'17':[0,0],'24':[2,-2]})
    checked('height defect of P,2P at 41', min(max(vals['24'][0],0),max(-vals['24'][1],0))==2)
    checked('support of x(P) fixed by denominator and norm', P[0].a.denominator==8 and P[0].b.denominator==2 and P[0].norm().numerator==41**2)
    vx=min(2*vp(57,2),2*vp(28,2)+1)-2*vp(8,2)
    vy=min(2*vp(660,2),2*vp(417,2)+1)-2*vp(32,2)
    checked('valuation at the prime above 2', (vx,vy,vx-vy)==(-6,-9,3))
    reduce7=lambda z: (z.a.numerator*pow(z.a.denominator,-1,7)+3*z.b.numerator*pow(z.b.denominator,-1,7))%7
    checked('smooth reduction at (3-rho)', (reduce7(P[0]),reduce7(P[1]),reduce7(D))==(1,6,0))
    checked('2-adic logarithm tail margin, bounded supplemental check', all(3*(m-1)>2*vp(m,2) for m in range(2,2049)))
    @lru_cache(None)
    def psi(m: int) -> K:
        x,y=P
        if m==0:return K(0)
        if m==1:return K(1)
        if m==2:return 2*y
        if m==3:return 3*x**4+6*A*x*x-A*A
        if m==4:return 4*y*(x**6+5*A*x**4-5*A*A*x*x-A**3)
        if m&1:
            k=(m-1)//2
            return psi(k+2)*psi(k)**3-psi(k-1)*psi(k+1)**3
        k=m//2
        return psi(k)*(psi(k+2)*psi(k-1)**2-psi(k-2)*psi(k+1)**2)/(2*y)
    acc=None
    for m in range(1,13):
        acc=add(acc,P)
        xx=P[0]-psi(m+1)*psi(m-1)/psi(m)**2
        yy=psi(2*m)/(2*psi(m)**4)
        if (xx,yy)!=acc or not on_curve(acc):raise AssertionError(('division polynomial',m))
    checked('division-polynomial recurrences versus repeated addition, m=1..12', True)
    tree=((('1','G1'),('G2','G3')),('G4',('G5','G6')))
    leaves=norm_tree_coefficients(tree)
    wanted=[F(1,16),F(9,16),F(5,16),F(13,16),F(3,8),F(7,16),F(15,16)]
    checked('exact seven-leaf norm-tree coefficients', list(leaves.values())==wanted)
    checked('strict integer precision extraction', all(c<1 for c in leaves.values()))
    q=F(24); kd,ki,ks=49,13,25
    checked('new strict precision inequalities', kd>2*q and ki>q/2 and ks>q)
    checked('minimal integers for these three strict inequalities', not(kd-1>2*q) and not(ki-1>q/2) and not(ks-1>q))
    checked('negative control: old boundary values are rejected', not(48>2*q) and not(12>q/2) and not(24>q))
    alpha=F(2103,1024)
    refined={'contact_exponent':str(alpha),'two_block_exponent':str(alpha/2),
             'lucas_power_of_B':str(2*alpha/3),
             'input_height_coefficient':str(alpha/(4-alpha)),
             'lucas_threshold_power':str(1/(2-2*alpha/3))}
    checked('exact sharpened PR30 exponents', list(refined.values())==['2103/1024','2103/2048','701/512','2103/1993','512/323'])
    checked('strict improvement over weakened PR30 exponents', 2*alpha/3<F(14,9) and alpha/(4-alpha)<F(7,5))
    checked('generic factor residue separation', all(len({0,(-5*nu)%8,(-5*nu+2)%8,(-5*nu+4)%8,(-5*nu+6)%8,(-2*nu)%8,(-2*nu+4)%8,(-4*nu)%8})==8 for nu in (1,3,5,7)))
    checked('special factor residue separation', all(len({0,(-5*nu)%8,(-5*nu+4)%8,(-3*nu)%8,(-3*nu+4)%8,(-2*nu)%8,(-2*nu+4)%8,(-4*nu)%8})==8 for nu in (1,3,5,7)))
    contacts=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
    reflected=[2-t for t in contacts]
    all_contacts=contacts+reflected
    bad=set()
    for i,t in enumerate(all_contacts):
        bad.update(prime_factors(t.denominator))
        bad.update(prime_factors((t-1).numerator))
        for u in all_contacts[i+1:]:bad.update(prime_factors((t-u).numerator))
    checked('PR30 contact differences and distance from 1', len(set(all_contacts))==10 and all(p<=76176 or p==2029147 for p in bad))
    for x in range(-100,101):
        beta=51*x*x+2504; rr=beta*(beta-1)*(beta-2401)*(32*beta+343)
        den=1+149**2*rr
        if gcd(rr,den)!=1 or gcd(149,den)!=1 or gcd(9792,den)!=1:raise AssertionError(('scalar gcd',x))
    checked('PR30 scalar denominator conditions for -100<=x<=100 (finite evidence)', True)
    return {'schema':'sun-pr30-scoped-checks/v1','status':'PASS','stage_count':len(stages),
            'stages':stages,'x_P':P[0].encoded(),'x_2P':Q[0].encoded(),
            'split_prime_41_valuations':vals,'exact_height_defect':'log(41)',
            'norm_tree_coefficients':{k:str(v) for k,v in leaves.items()},
            'sun_precision_orders':{'lucas':kd,'input':ki,'scalar':ks},
            'sun_height_exponents':{'lucas':str(q/kd),'input':str(q/ki),
                                    'scalar':str(q/ks),'input_log_coefficient':str(q/(2*ki-q))},
            'pr30_refined_exponents':refined,'pr30_contact_exceptional_primes':sorted(bad),
            'scope':'Finite exact checks only. Universal height criteria have written proofs. Rank, contact-height suppliers, prime patterns, pole realization, complete PR30 coefficients and the repository-wide verification suite are not verified by this program.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args=parser.parse_args()
    result=main(); text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')
    print(text)
