#!/usr/bin/env python3
"""Exact checks for the shifted-Lucas construction and reflection obstruction.

This checks finite identities and a complete quadratic/quartic reconstruction.
It does not certify any inherited infinite arithmetic premise.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def lucas(a, j):
    u, v = 0, 1
    for _ in range(j):
        u, v = v, a*v-u
    return u

def lucas_checks():
    inputs=[(r,a) for r in (2,3,4,6) for a in range(2,25)]+[(2,25)]
    witnesses=[]
    for r,a in inputs:
        A=r*a+2
        w=lucas(A,a)
        require(w % a == 0, 'Lucas divisibility')
        require((w//a-1) % r == 0, 'Lucas congruence')
        m=(w//a-1)//r
        t=lucas(A,a+1)
        require(w==a*(r*m+1), 'Shifted label')
        require(t*t-A*t*w+w*w==1, 'Lucas norm equation')
        if a>=4:
            require(abs(t)>=(r*a-3)**(a-2), 'Lucas growth')
        witnesses.append(dict(r=r,a=a,A=A,m=str(m),t=str(t)))
    negative=[]
    for c in range(4,21):
        a=-c; A=2*a+2; w=lucas(A,c); t=lucas(A,c+1)
        require(w%a==0 and (w//a-1)%2==0, 'Negative-index congruence')
        m=(w//a-1)//2
        require(w==a*(2*m+1) and w!=0, 'Negative shifted label')
        require(t*t-A*t*w+w*w==1, 'Negative norm equation')
        require(abs(t)>=(2*c-3)**(c-2), 'Negative growth')
        negative.append(dict(a=a,m=str(m),t=str(t)))
    A,t,w=sp.symbols('A t w')
    require(sp.expand(t*t-A*t*w+w*w-1).subs({A:6,t:35,w:6})==0,
            'Independent small Lucas fixture')
    return dict(completeness_examples=len(witnesses),negative_examples=len(negative),
                witnesses=witnesses,negative_witnesses=negative)

def elliptic_identity_checks():
    D,f,g,h,k,s=sp.symbols('D f g h k s')
    r1=s*(f-g)-h-k
    r2=s*(h-k)-1+D*(f*f+f*g+g*g)
    r3=h*h-f+D*f**3
    x=s*s+D*(f+g)
    y=D*h-s*(D*f+x)
    require(sp.expand(k*k-g+D*g**3-r3+(f-g)*r2-(h-k)*r1)==0,
            'Second reciprocal curve identity')
    require(sp.expand(y*y-x**3+D*x-D*D*r3+D*(D*f+x)*(r2-s*r1))==0,
            'Difference curve identity')
    a,m,t=sp.symbols('a m t')
    A=2*a+2; b=m+sp.Rational(1,2)
    delta=t*t-A*(A-2)*t*b+(A-2)**2*b*b-1
    explicit=t*t-(2*a+2)*a*(2*m+1)*t+a*a*(2*m+1)**2-1
    require(sp.expand(delta-explicit)==0, 'Integral shifted Lucas residual')
    return dict(symbolic_identities=3)

# A separate exact finite-field implementation; no elliptic software dependency.
class K19:
    __slots__=('a','b')
    def __init__(self,a=0,b=0): self.a=int(a)%19;self.b=int(b)%19
    @staticmethod
    def cast(x): return x if isinstance(x,K19) else K19(x)
    def __add__(self,x):
        x=self.cast(x);return K19(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self): return K19(-self.a,-self.b)
    def __sub__(self,x): return self+-self.cast(x)
    def __rsub__(self,x): return self.cast(x)+-self
    def __mul__(self,x):
        x=self.cast(x);return K19(self.a*x.a+2*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.cast(x);n=(x.a*x.a-2*x.b*x.b)%19
        require(n!=0,'Division by zero in finite field')
        return self*K19(x.a,-x.b)*pow(n,-1,19)
    def __pow__(self,n):
        require(n>=0,'Only nonnegative powers used')
        z=K19(1);x=self
        while n:
            if n&1:z=z*x
            x=x*x;n//=2
        return z
    def __eq__(self,x):
        x=self.cast(x);return self.a==x.a and self.b==x.b
    def serial(self): return [self.a,self.b]

def finite_field_checks():
    rr=K19(0,1);d=3-rr;D=d*d
    P=((57-28*rr)/8,(-660+417*rr)/32)
    def on(Qp): return Qp is None or Qp[1]**2==Qp[0]**3-D*Qp[0]
    def add(Qp,Rp):
        if Qp is None:return Rp
        if Rp is None:return Qp
        x,y=Qp;u,v=Rp
        if x==u:
            if y+v==0:return None
            ss=(3*x*x-D)/(2*y)
        else:ss=(v-y)/(u-x)
        xx=ss*ss-x-u;out=(xx,ss*(x-xx)-y)
        require(on(out),'Finite-field group output is on curve')
        return out
    def mul(n,Qp):
        out=None
        for _ in range(n):out=add(out,Qp)
        return out
    require(pow(2,9,19)==18,'19 is inert in Q(sqrt(2))')
    require(on(P),'P is on the finite-field curve')
    expected={1:(6*rr,15-3*rr),2:(8+rr,8-rr),4:(11-rr,13+5*rr),5:(16+rr,K19(0))}
    for n,Qp in expected.items():require(mul(n,P)==Qp,'Finite-field multiple '+str(n))
    require(mul(10,P) is None,'P has order dividing ten')
    require(mul(2,P) is not None and mul(5,P) is not None,'P has exact order ten')
    torsion=[None,(K19(0),K19(0)),(d,K19(0)),(-d,K19(0))]
    traces=[];points=[]
    for tau in torsion:
        Qp=add(P,tau)
        require(Qp is not None,'All translated points are affine')
        traces.append(2*Qp[0].a%19)
        points.append([z.serial() for z in Qp])
    require(traces==[0,2,2,3],'All four torsion trace residues')
    require([(7**4+t**4)%19 for t in traces]==[7,4,4,12], 'Contact residues')
    contacts=[(1+r)%19 for r in (-6,-3,-2,-1,1,2,3,6)]
    require(len(set(contacts))==8,'Distinct eight contacts at 19')
    require(4*121**3*190%361==38,'First-order coefficient')
    # The pigeonhole statement is exhaustive over arbitrary unknown lifts d_i.
    # Each d_i+2t has exactly one zero modulo 19, so any four zero positions
    # leave at least one of the five trial positions unused.
    from itertools import product
    trials=set(range(5));count=0
    for forbidden in product(range(19),repeat=4):
        require(bool(trials-set(forbidden)), 'Five-trial pigeonhole')
        count+=1
    return dict(prime=19,order_of_P=10,translated_points=points,trace_residues=traces,
                candidate_shift_residues=[117,307,497,687,877],shift_modulus=3610,
                first_order_slope_mod_19=2,exhaustive_pigeonhole_cases=count,
                selected_progression='Existence proved by pigeonhole; no chosen lift residue asserted')

# Polynomial representation independent of the construction producer.
def decode(row):
    ans=defaultdict(Q)
    for t in row['terms']:
        ans[(int(t['parameterPower']),tuple(t['monomial']))]+=Q(t['coefficient'])
    return {k:v for k,v in ans.items() if v}

def plus(*ps):
    d=defaultdict(Q)
    for p in ps:
        for k,v in p.items():d[k]+=v
    return {k:v for k,v in d.items() if v}

def scale(p,a):return {k:Q(a)*v for k,v in p.items() if Q(a)*v}
def prod(p,q):
    d=defaultdict(Q)
    for (j,m),a in p.items():
        for (k,n),b in q.items():d[j+k,tuple(sorted(m+n))]+=a*b
    return {k:v for k,v in d.items() if v}
def c(a):return {(0,()):Q(a)} if a else {}
def v(i):return {(0,(i,)):Q(1)}
def primitive(p):
    p={k:Q(x) for k,x in p.items() if x};require(bool(p),'Nonzero row')
    den=lcm(*(x.denominator for x in p.values()))
    gg=gcd(*(int(x*den) for x in p.values()))
    if p[min(p)]<0:gg=-gg
    return scale(p,Q(den,gg))
def sig(p):return tuple(sorted(primitive(p).items()))
def subst(p,repl):
    out={}
    for (j,m),a in p.items():
        term={(j,()):a}
        for i in m:term=prod(term,repl.get(i,v(i)))
        out=plus(out,term)
    return out

def quadratic_reconstruction(source, generated):
    parent=json.loads(source.read_text()); child=json.loads(generated.read_text())
    require(parent['variables']==204 and len(parent['residuals'])==186,'Pinned parent shape')
    require(child['variables']==200 and len(child['residuals'])==186,'New shape')
    remove=set(range(169,183));oldids=list(range(1,215))
    keep=[i for i in oldids if i not in remove];rename={old:i+1 for i,old in enumerate(keep)}
    def compact(p):
        out={}
        for (j,m),a in p.items():
            require(not remove.intersection(m),'A deleted coordinate survives')
            out[j,tuple(rename[i] for i in m)]=a
        return out
    aff={35:plus(scale(v(35),Q(1,2)),scale(v(118),-1)),36:scale(v(36),Q(1,2)),
         37:plus(scale(v(37),Q(1,2)),scale(v(118),-1)),38:scale(v(38),Q(1,2))}
    oldroot=plus(prod(plus(v(173),scale(v(175),-1)),plus(v(173),scale(v(175),-1))),
                 scale(prod(plus(v(174),scale(v(176),-1)),plus(v(174),scale(v(176),-1))),2))
    # Four times the real component of s^2+(11-6rho)(f+g).
    newroot=scale(plus(prod(v(213),v(213)),scale(prod(v(214),v(214)),2),
              scale(plus(v(205),v(209)),11),scale(plus(v(206),v(210)),-12)),4)
    retained=[];touching=[]
    for row in parent['residuals']:
        rid=int(row['id']);p=decode(row)
        if any(remove.intersection(m) for _,m in p):touching.append(rid)
        if 122<=rid<=139:continue
        if 104<=rid<=121:p=subst(p,aff)
        if rid==144:
            factor=p.get((0,(173,173)))
            require(factor is not None and factor!=0,'Aggregate coefficient found')
            removedpart={key:a for key,a in p.items() if remove.intersection(key[1])}
            require(removedpart==scale(oldroot,factor),'Literal old aggregate term')
            p=plus(p,scale(oldroot,-factor),scale(newroot,factor))
        retained.append(sig(compact(p)))
    require(touching==list(range(122,140))+[144], 'Exactly the specified removed incidence rows')
    require([sig(decode(r)) for r in child['residuals'][:168]]==retained,
            'Every retained or modified row reconstructed independently')
    # SymPy, used only for the eighteen new rows, supplies a separate algebra engine.
    xx={i:sp.Symbol('x'+str(i)) for i in [19,20,29,30,43,44,45,46,60,61,169,170,*range(191,201)]}
    def kadd(*args):return (sum(x[0] for x in args),sum(x[1] for x in args))
    def kmul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def ks(c,a):return (c*a[0],c*a[1])
    def ksub(a,b):return kadd(a,ks(-1,b))
    one=(sp.Integer(1),sp.Integer(0));DD=(sp.Integer(11),sp.Integer(-6))
    ff=(xx[191],xx[192]);hh=(xx[193],xx[194]);gg=(xx[195],xx[196]);kk=(xx[197],xx[198]);ss=(xx[199],xx[200])
    FF=(xx[60],2*xx[61]);GG=(xx[29],2*xx[30]);S=(xx[19],xx[20]);TH=(xx[169],xx[170])
    M=(xx[43]-sp.Rational(1,2),xx[44]);M0=(xx[45]-sp.Rational(1,2),xx[46])
    eqs=[ksub(FF,kmul(ff,ff)),ksub(GG,kmul(gg,gg)),
          kadd(kmul(hh,hh),ks(-1,ff),kmul(DD,kmul(ff,FF))),
          ksub(kmul(ss,ksub(ff,gg)),kadd(hh,kk)),
          kadd(kmul(ss,ksub(hh,kk)),ks(-1,one),kmul(DD,kadd(FF,kmul(ff,gg),GG))),
          kadd(kmul(hh,M),ks(2,kmul(ff,S))),
          kadd(kmul(ksub(one,kmul(DD,FF)),M),ks(2,kmul(hh,S))),
          kadd(kmul(kk,M0),ks(2,kmul(gg,TH))),
          kadd(kmul(ksub(one,kmul(DD,GG)),M0),ks(2,kmul(kk,TH)))]
    rev={symbol:i for i,symbol in xx.items()}
    def sparse(expr):
        out={}
        for term,coefficient in sp.expand(expr).as_coefficients_dict().items():
            ids=[]
            for sym,power in term.as_powers_dict().items():
                if sym==1:continue
                require(sym in rev,'Only known quadratic coordinates')
                ids.extend([rev[sym]]*int(power))
            out[0,tuple(sorted(ids))]=Q(int(coefficient.p),int(coefficient.q))
        return out
    expected=Counter(sig(sparse(e)) for pair in eqs for e in pair)
    actual=Counter(sig(decode(r)) for r in child['residuals'][168:])
    require(expected==actual,'All eighteen new rational equations match the mathematical formulas')
    full=defaultdict(Q)
    for row in child['residuals']:
        items=list(decode(row).items())
        require(all(len(key[1])<=2 for key,_ in items),'Every row is quadratic')
        for i,((j,m),a) in enumerate(items):
            for l in range(i,len(items)):
                (k,n),b=items[l]
                full[j+k,tuple(sorted(m+n))]+=a*b*(1 if i==l else 2)
    full={key:a for key,a in full.items() if a}
    polynomial=json.loads((generated.parent/'polynomial-family.json').read_text())
    require(full==decode(polynomial),'Every expanded quartic coefficient independently reconstructed')
    require(full.get((0,(191,191,191,191)))==1,'Parameter-independent unit coefficient')
    require(max(len(m) for _,m in full)==4,'Exact degree four')
    require({i for _,m in full for i in m}==set(range(1,201)),'All 200 coordinates used')
    require(all(a.denominator==1 for a in full.values()),'Integral coefficients')
    altered=dict(full);altered[0,(191,191,191,191)]+=1
    require(altered!=decode(polynomial),'Coefficient corruption is detected')
    bad=actual.copy();some=next(iter(bad));bad[some]+=1
    require(bad!=expected,'Equation corruption is detected')
    return dict(variables=200,quadratic_rows=186,degree=4,integer_content=1,
                parameter_separated_terms=len(full),coordinate_monomials=len({m for _,m in full}),
                exact_monomial_count_after_specialization_claimed=False,
                independently_compared_retained_rows=168,independently_compared_new_rows=18,
                negative_controls=2,source_sha256=sha256(source.read_bytes()).hexdigest(),
                quadratic_sha256=sha256(generated.read_bytes()).hexdigest(),
                quartic_sha256=sha256((generated.parent/'polynomial-family.json').read_bytes()).hexdigest())

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=ROOT/'computation/quartic/reciprocal204_v27/unbalanced-quadratic.json')
    ap.add_argument('--quadratic',type=Path,default=HERE/'quadratic-family.json')
    ap.add_argument('--output',type=Path,default=HERE/'verification.json')
    ap.add_argument('--arithmetic-only',action='store_true')
    args=ap.parse_args()
    report={'schema':'shifted-lucas-reflection-exact-checks/v33',
            'lucas':lucas_checks(),'identities':elliptic_identity_checks(),
            'reflection':finite_field_checks()}
    if not args.arithmetic_only:
        report['quartic']=quadratic_reconstruction(args.source,args.quadratic)
    report.update(status='PASS',complete_coefficient_check=not args.arithmetic_only,
                  inherited_arithmetic_verified=False,independent_mathematical_review=False,
                  scope='Exact identities, finite-field arithmetic, finite Lucas examples, and, unless arithmetic-only, complete quadratic and quartic reconstruction. Universal proofs are separate.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('lucas','reflection')},indent=2))
if __name__=='__main__':main()
