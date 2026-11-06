#!/usr/bin/env python3
"""Compile the shared-point rational system into a materialized quartic.

All arithmetic gates ARE existential variables in this degree-four format.
The optional symbol K is 3**(2**26), or 3**(2**28) at precision 52;
it is a fixed integer, not a variable.
Arithmetic validity of the new system is a separate, stated dependency.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from math import gcd, lcm
from pathlib import Path


class Lin:
    """Canonical affine linear form; index -1 denotes its constant."""
    def __init__(self, terms=()):
        out={}
        for i,c in terms:
            out[i]=out.get(i,F(0))+F(c)
        self.terms=tuple(sorted((i,c) for i,c in out.items() if c))
    def __add__(self, other):
        other=linear(other)
        return Lin(self.terms+other.terms)
    __radd__=__add__
    def __neg__(self): return self.scale(-1)
    def __sub__(self, other): return self+-linear(other)
    def __rsub__(self, other): return linear(other)+-self
    def scale(self,c): return Lin((i,a*F(c)) for i,a in self.terms)
    def constant(self):
        return all(i==-1 for i,c in self.terms)
    def value(self):
        assert self.constant()
        return sum((c for i,c in self.terms),F(0))
    def key(self): return tuple((i,c.numerator,c.denominator) for i,c in self.terms)
    def dump(self): return [[i,c.numerator,c.denominator] for i,c in self.terms]


def linear(a):
    return a if isinstance(a,Lin) else Lin([(-1,F(a))])


def normalization_scale(a):
    c=a.terms[0][1]
    # Keep the scalar normalization from propagating large rational
    # constants through long powering chains.
    if max(abs(c.numerator).bit_length(),c.denominator.bit_length())<=16:
        return c
    return F(1 if c>0 else -1)


def poly_add(out, mono, coefficient):
    coefficient=F(coefficient)
    out[mono]=out.get(mono,F(0))+coefficient
    if not out[mono]: del out[mono]


def add_linear(out,a,coefficient=1):
    for i,c in linear(a).terms:
        poly_add(out,() if i==-1 else (i,),c*coefficient)


def add_product(out,a,b,coefficient=1):
    for i,c in linear(a).terms:
        for j,d in linear(b).terms:
            mono=tuple(sorted(k for k in (i,j) if k!=-1))
            poly_add(out,mono,c*d*coefficient)


def simplify_quadratics(initial, allowed):
    """Certified row operations and substitutions preserving degree <= 2."""
    rows={i:dict(r['terms']) for i,r in initial}
    symbols={i:r['K_constant'] for i,r in initial}
    operations=[]
    # Existing pure multiplication gates can linearize later constraints.
    pivots={}
    for i,r in initial:
        if r['kind']!='gate' or symbols[i]:continue
        high=[m for m in rows[i] if len(m)==2]
        low=[m for m in rows[i] if len(m)<2]
        if len(high)==len(low)==1 and len(low[0])==1:
            pivots[high[0]]=i
    protected=set(pivots.values())
    for i in rows:
        if i in protected:continue
        for m in list(rows[i]):
            if m not in pivots:continue
            j=pivots[m];factor=-rows[i][m]/rows[j][m]
            for n,c in rows[j].items():poly_add(rows[i],n,factor*c)
            operations.append({'kind':'row_add','target':i,'other':j,
                               'factor':[factor.numerator,factor.denominator]})
    while True:
        incidence={}
        for i,r in rows.items():
            for v in {v for m in r for v in m}:incidence.setdefault(v,set()).add(i)
        candidates=[]
        for i,r in rows.items():
            if symbols[i]:continue
            for m,c in r.items():
                if len(m)!=1 or m[0] not in allowed:continue
                v=m[0]
                if any(v in n for n in r if n!=m):continue
                replacement={n:-d/c for n,d in r.items() if n!=m}
                degree=max(map(len,replacement),default=0)
                other=incidence[v]-{i}
                if degree==2 and any(any(v in n and len(n)>1 for n in rows[j]) for j in other):continue
                # Prefer linear replacements, then sparse constraints.
                candidates.append(((degree,len(replacement),len(other),-v),i,v,replacement))
        if not candidates:break
        _,i,v,replacement=min(candidates)
        affected=sorted(incidence[v]-{i})
        for j in affected:
            out={}
            for m,c in rows[j].items():
                power=m.count(v)
                term={tuple(x for x in m if x!=v):c}
                for _ in range(power):
                    new={}
                    for ma,ca in term.items():
                        for mb,cb in replacement.items():poly_add(new,tuple(sorted(ma+mb)),ca*cb)
                    term=new
                for n,d in term.items():poly_add(out,n,d)
            assert all(len(n)<=2 for n in out)
            rows[j]=out
        operations.append({'kind':'eliminate','pivot':i,'variable':v,
                           'affected':affected,
                           'replacement':[[list(m),c.numerator,c.denominator] for m,c in sorted(replacement.items())]})
        del rows[i];del symbols[i]
    result=[(i,r|{'terms':rows[i]}) for i,r in initial if i in rows and (rows[i] or symbols[i])]
    return result,operations


class Builder:
    def __init__(self, literal_anchor=True, share_height=False, precision=64, scalar_order=48):
        self.vars=[]; self.rows=[]; self.gates=[]; self.cache={}
        self.literal_anchor=literal_anchor; self.share_height=share_height
        assert precision in (52,64)
        self.precision=precision
        self.anchor_exponent=28 if precision==52 else 26
        assert scalar_order in (32,48)
        assert scalar_order==48 or precision==52
        self.scalar_order=scalar_order
        self.point_names=[]; self.pole_names=[]
        self.D=self.field(11,-6)
    def var(self,name,category):
        i=len(self.vars)
        self.vars.append({'index':i,'name':name,'category':category})
        return Lin([(i,1)])
    def row(self,label,terms=None,lin=0,kind='source',symbolic_constant=0):
        p={}; add_linear(p,lin)
        for c,a,b in terms or []: add_product(p,a,b,c)
        self.rows.append({'label':label,'kind':kind,'terms':p,
                          'K_constant':F(symbolic_constant)})
        return len(self.rows)-1
    def mul(self,a,b,label='product',force=False):
        a,b=linear(a),linear(b)
        if not force:
            if a.constant():return b.scale(a.value())
            if b.constant():return a.scale(b.value())
        # Scalar multiples share a gate. This is exact over Q and prevents
        # separately computing, for example, y^2 and (2y)^2.
        scale=F(1)
        if not force:
            ac,bc=normalization_scale(a),normalization_scale(b)
            a,b=a.scale(1/ac),b.scale(1/bc)
            scale=ac*bc
        ak,bk=a.key(),b.key()
        if bk<ak:a,b,ak,bk=b,a,bk,ak
        key=('mul',ak,bk)
        if key in self.cache:return self.cache[key].scale(scale)
        z=self.var(label,'arithmetic')
        row=self.row(label,[(1,a,b)],-z,kind='gate')
        self.gates.append({'variable':z.terms[0][0],'operation':'mul',
                           'arguments':[a.dump(),b.dump()],'row':row})
        self.cache[key]=z
        return z.scale(scale)
    def sq(self,a):return self.mul(a,a,'square')
    def quad_value(self,terms,label='quadratic value'):
        p={}
        for c,a,b in terms:add_product(p,a,b,c)
        low=Lin([(-1 if not m else m[0],c) for m,c in p.items() if len(m)<2])
        high={m:c for m,c in p.items() if len(m)==2}
        if not high:return low
        first=next(c for m,c in sorted(high.items()))
        scale=first if max(abs(first.numerator).bit_length(),first.denominator.bit_length())<=16 else F(1 if first>0 else -1)
        high={m:c/scale for m,c in high.items()}
        key=('quadratic',tuple((m,c.numerator,c.denominator) for m,c in sorted(high.items())))
        if key in self.cache:return self.cache[key].scale(scale)+low
        z=self.var(label,'arithmetic');zi=z.terms[0][0]
        p=dict(high);poly_add(p,(zi,),-1)
        row=len(self.rows)
        self.rows.append({'label':label,'kind':'gate','terms':p,'K_constant':F(0)})
        self.gates.append({'variable':zi,'operation':'quadratic','polynomial':[[list(m),c.numerator,c.denominator] for m,c in sorted(high.items())],'arguments':[],'row':row})
        self.cache[key]=z
        return z.scale(scale)+low
    def inv(self,a,label='inverse'):
        a=linear(a)
        if a.constant():
            if not a.value():raise ZeroDivisionError(label)
            return linear(1/a.value())
        scale=normalization_scale(a)
        a=a.scale(1/scale)
        key=('inv',a.key())
        if key in self.cache:return self.cache[key].scale(1/scale)
        z=self.var(label,'arithmetic')
        row=self.row(label,[(1,a,z)],-1,kind='inverse')
        self.gates.append({'variable':z.terms[0][0],'operation':'inv',
                           'arguments':[a.dump()],'row':row})
        self.cache[key]=z
        return z.scale(1/scale)
    def div(self,a,b):return self.mul(a,self.inv(b))
    def power(self,a,n):
        assert n>=0
        if n==0:return linear(1)
        if n==1:return linear(a)
        if n%2==0:return self.sq(self.power(a,n//2))
        return self.mul(a,self.power(a,n-1))
    def bit(self,name):
        b=self.var(name,'finite choice')
        self.row(name+' Boolean',[(1,b,b)],-b)
        return b
    def field(self,a=0,b=0):return linear(a),linear(b)
    def fadd(self,a,b):return a[0]+b[0],a[1]+b[1]
    def fsub(self,a,b):return a[0]-b[0],a[1]-b[1]
    def fscale(self,a,c):return self.mul(a[0],c),self.mul(a[1],c)
    def fmul(self,a,b):
        return (self.quad_value([(1,a[0],b[0]),(2,a[1],b[1])],'field product 0'),
                self.quad_value([(1,a[0],b[1]),(1,a[1],b[0])],'field product 1'))
    def fsq(self,a):
        return (self.quad_value([(1,a[0],a[0]),(2,a[1],a[1])],'field square 0'),
                self.mul(a[0],a[1]).scale(2))
    def fnorm(self,a):return self.quad_value([(1,a[0],a[0]),(-2,a[1],a[1])],'field norm')
    def finv(self,a):
        if a[0].constant() and a[1].constant():
            x,y=a[0].value(),a[1].value();n=x*x-2*y*y
            if not n:raise ZeroDivisionError('zero field inverse')
            return self.field(x/n,-y/n)
        if not a[1].terms:return self.inv(a[0]),linear(0)
        if not a[0].terms:return linear(0),self.inv(a[1]).scale(F(1,2))
        scale=normalization_scale(a[0]);aa=(a[0].scale(1/scale),a[1].scale(1/scale))
        key=('field inverse',aa[0].key(),aa[1].key())
        if key in self.cache:
            ans=self.cache[key];return ans[0].scale(1/scale),ans[1].scale(1/scale)
        z0=self.var('field inverse 0','arithmetic');z1=self.var('field inverse 1','arithmetic')
        i0,i1=z0.terms[0][0],z1.terms[0][0]
        row0=self.row('field inverse 0',[(1,aa[0],z0),(2,aa[1],z1)],-1,kind='inverse')
        row1=self.row('field inverse 1',[(1,aa[0],z1),(1,aa[1],z0)],kind='inverse')
        args=[aa[0].dump(),aa[1].dump()]
        self.gates.extend([{'variable':i0,'operation':'field_inverse_0','arguments':args,'row':row0,'pair':i1},
                           {'variable':i1,'operation':'field_inverse_1','arguments':args,'row':row1,'pair':i0}])
        self.cache[key]=(z0,z1)
        return z0.scale(1/scale),z1.scale(1/scale)
    def fdiv(self,a,b):return self.fmul(a,self.finv(b))
    def fquot(self,a,b,reason):
        """Two-coordinate quotient where the cited domain lemma proves b!=0."""
        assert reason in ('doubling slope','local parameter','nonzero logarithm','nonzero local parameter')
        if all(v.constant() for v in a+b):return self.fdiv(a,b)
        key=('domain quotient',reason,a[0].key(),a[1].key(),b[0].key(),b[1].key())
        if key in self.cache:return self.cache[key]
        z0=self.var(reason+' quotient 0','arithmetic');z1=self.var(reason+' quotient 1','arithmetic')
        i0,i1=z0.terms[0][0],z1.terms[0][0]
        row0=self.row(reason+' quotient 0',[(1,b[0],z0),(2,b[1],z1)],-a[0],kind='paired quotient')
        row1=self.row(reason+' quotient 1',[(1,b[0],z1),(1,b[1],z0)],-a[1],kind='paired quotient')
        args=[a[0].dump(),a[1].dump(),b[0].dump(),b[1].dump()]
        self.gates.extend([{'variable':i0,'operation':'field_quotient_0','arguments':args,'row':row0,'pair':i1,'domain_reason':reason},
                           {'variable':i1,'operation':'field_quotient_1','arguments':args,'row':row1,'pair':i0,'domain_reason':reason}])
        self.cache[key]=(z0,z1)
        return z0,z1
    def conj(self,a):return a[0],-a[1]
    def double(self,p):
        x,y=p['x'],p['y']
        slope=self.fquot(self.fsub(self.fscale(self.fsq(x),3),self.D),self.fscale(y,2),'doubling slope')
        xx=self.fsub(self.fsq(slope),self.fscale(x,2))
        yy=self.fsub(self.fmul(slope,self.fsub(x,xx)),y)
        return {'x':xx,'y':yy}
    def point(self,label):
        self.point_names.append(label)
        x=tuple(self.var(label+'.half.x'+str(i),'point') for i in range(2))
        y=tuple(self.var(label+'.half.y'+str(i),'point') for i in range(2))
        rhs=self.fsub(self.fmul(self.fsq(x),x),self.fmul(self.D,x))
        self.row(label+' half-curve 0',[(1,y[0],y[0]),(2,y[1],y[1])],-rhs[0])
        self.row(label+' half-curve 1',[(2,y[0],y[1])],-rhs[1])
        p=self.double({'x':x,'y':y})
        # The direct doubling equations force the half-ordinate nonzero.
        # The no-2-torsion lemma for 2E(K) then makes both coordinates of
        # the doubled point nonzero; see field_quotient_domains.tex.
        return p
    def difference(self,a,b):
        slope=self.fdiv(self.fadd(a['y'],b['y']),self.fsub(a['x'],b['x']))
        nu=self.fsub(self.fmul(slope,a['x']),a['y'])
        xx=self.fsub(self.fsub(self.fsq(slope),a['x']),b['x'])
        yy=self.fsub(nu,self.fmul(slope,xx))
        return {'x':xx,'y':yy}
    def reciprocal(self,p):return self.finv(p['x'])
    def local_z(self,p):return self.fscale(self.fquot(p['x'],p['y'],'local parameter'),-1)
    def logarithm(self,p,precision):
        f=self.reciprocal(p); w=self.fmul(self.D,self.fsq(f))
        cs=[F(1),F(-2,5)]
        for j in range(2,precision//4):cs.append(cs[-1]*F(4*j-5,4*j+1))
        # Paterson--Stockmeyer blocking: scalar linear combinations are free
        # affine forms. Degree 15 needs six field products, not fourteen.
        block=3 if len(cs)==13 else 4
        powers=[self.field(1),w]
        for k in range(2,block+1):
            powers.append(self.fsq(powers[k//2]) if k%2==0 else self.fmul(powers[k-1],w))
        chunks=[]
        for start in range(0,len(cs),block):
            chunk=self.field()
            for k,c in enumerate(cs[start:start+block]):
                chunk=self.fadd(chunk,self.fscale(powers[k],c))
            chunks.append(chunk)
        out=chunks[-1]
        for chunk in reversed(chunks[:-1]):out=self.fadd(self.fmul(out,powers[block]),chunk)
        return self.fmul(self.local_z(p),out)
    def correction(self):
        out=linear(1)
        for p in (2,3,5,7,11,13,17):
            out=self.mul(out,1+self.bit('height correction '+str(p)).scale(p-1))
        return self.mul(out,1-self.bit('height correction sign').scale(2))
    def pole(self,b,label,preparation_zero=True):
        self.pole_names.append(label)
        if preparation_zero:t=linear(0)
        else:t=self.var(label+'.t','pole')
        e,p,q,s=[self.var(label+'.'+n,'pole') for n in ('e','p','q','s')]
        if preparation_zero:U=b
        else:
            bt2=self.mul(b,self.sq(t))
            U=self.mul(b,self.div(1-bt2,1+bt2))
        B=b.scale(17)
        h=self.mul(e,B-self.sq(U))
        rhs1=self.mul(B,1+e.scale(2)-self.sq(e).scale(3))
        self.row(label+' conic 1',[(1,p,p)],-rhs1)
        bh=self.mul(B,h);s2=self.sq(s)
        q2=self.sq(q)
        self.row(label+' conic 2',[(1,B,q2),(-1,s2-bh,s2+bh.scale(3))])
        if not preparation_zero:
            self.inv(b,label+' nonzero detector')
        # In each coordinate detector, r!=0 and W_0!=0 already imply
        # b=r*N(W)^2/(4*W_0^2)!=0 over Q(sqrt(2)).
    def norm_batch(self,r,tests,orders):
        nodes=[1+self.div(self.sq(tests[0]),r)]
        for e in sorted(set(orders[1:])):
            xs=[x for x,k in zip(tests[1:],orders[1:]) if k==e]
            ri=self.inv(self.power(r,e))
            for i in range(0,len(xs),2):
                a=self.mul(xs[i],ri)
                if i+1==len(xs):nodes.append(a)
                else:
                    b=self.mul(xs[i+1],ri)
                    nodes.append(self.sq(a)+self.mul(r,self.sq(b)))
        while len(nodes)>1:
            nodes=[nodes[i] if i+1==len(nodes) else
                   self.sq(nodes[i])+self.mul(r,self.sq(nodes[i+1]))
                   for i in range(0,len(nodes),2)]
        return self.mul(r,self.sq(nodes[0]))
    def anchor(self,S):
        f0,f1=self.reciprocal(S)
        r=self.sq(f0)+self.mul(f0,f1)-self.sq(f1)
        u,v,w=[self.var('anchor.'+n,'anchor') for n in ('u','v','w')]
        terms=[(1,u,u),(6,v,v),(-2,w,w),(-3,r,r)]
        if self.literal_anchor:
            self.row('semilocal size anchor',terms,symbolic_constant=2)
        else:
            # K=3^(2^anchor_exponent); start from 3^16.
            K=linear(3**16)
            for j in range(self.anchor_exponent-4):K=self.mul(K,K,'anchor constant square '+str(j),force=True)
            self.row('semilocal size anchor',terms,K.scale(2))
    def product_coefficients(self,values):
        coeff=[self.field(1)]
        for v in values:
            out=coeff+[self.field()]
            for k in range(1,len(out)):
                out[k]=self.fadd(out[k],self.fmul(coeff[k-1],v))
            coeff=out
        return coeff
    def evaluate_field_polynomial(self,coeff,x):
        out=coeff[-1]
        for c in reversed(coeff[:-1]):out=self.fadd(self.fscale(out,x),c)
        return out
    def build(self):
        X=self.var('input','input'); beta=self.sq(X)+2
        roots=[self.point(k) for k in ('A','S','T','Z')]
        self.anchor(roots[1])
        H=self.point('H')
        J0=H if self.share_height else self.point('J0')
        heighttests=list(self.reciprocal(J0)+self.reciprocal(roots[1])+
                         self.fquot(self.local_z(roots[1]),self.local_z(J0),'nonzero local parameter'))
        r=linear(1)
        for a in (beta,beta-1,beta-2401,beta.scale(32)+343,beta.scale(2)-1):r=self.mul(r,a)
        b=self.mul(self.correction(),self.norm_batch(r,heighttests,[1,1,1,1,self.scalar_order,self.scalar_order]))
        self.pole(b,'height',False)
        points=[H]+[self.point('U'+k) for k in ('A','S','T','Z')]
        base={'x':self.field(F(57,8),F(-7,2)),'y':self.field(F(-165,8),F(417,32))}
        targets=[self.double(self.double(base))]+[self.double(self.double(p)) for p in roots]
        V=[self.difference(p,q) for p,q in zip(points,targets)]
        k=self.precision
        lden=self.logarithm(H,k);rden=self.logarithm(V[0],k)
        tests=[self.reciprocal(p) for p in points]+[self.conj(self.reciprocal(p)) for p in V]
        L=[self.fquot(self.logarithm(p,m),lden,'nonzero logarithm') for p,m in zip(points[1:],(16,k,k,k))]
        R=[self.conj(self.fquot(self.logarithm(p,m),rden,'nonzero logarithm')) for p,m in zip(V[1:],(16,k,k,k))]
        tests += [self.fsub(a,b) for a,b in zip(L,R)]
        # Direct integral polynomial test. The two-anchor cross tests make
        # L[1:4] integral and congruent to the integer labels at order k.
        # F(L[1],L[2],L[3]) therefore replaces all Lucas proxies.
        xm2=self.fsub(L[1],self.field(2))
        ax=self.fmul(L[1],xm2)
        tz=self.fmul(L[2],L[3])
        zz=self.fmul(xm2,L[3])
        pell=self.fsub(self.fadd(self.fsq(L[2]),self.fsq(zz)),
                       self.fadd(self.fmul(ax,tz),self.field(1)))
        tests += [self.fsub(L[0],self.field(beta)),pell]
        orders=[1]*10+[16,k,k,k]+[16,k]
        grouped={m:self.product_coefficients([self.fsq(t) for t,order in zip(tests,orders) if order==m]) for m in (1,16,k)}
        slope=self.var('common slope','slope')
        components=[x for p in roots for x in p['x']]
        scales=[linear(1)]
        for i,x in enumerate(components):
            # A doubled abscissa is a nonzero square in the real quadratic
            # field, so its rational component is positive. The other
            # component may vanish; (1+x^2)^2 handles that case uniformly.
            scales.append(self.sq(x) if i%2==0 else self.sq(1+self.sq(x)))
        contacts=(F(0),F(-1,2),F(-1),F(1,2399),F(-32,407))
        for i,A in enumerate(scales):
            ainv=self.inv(A,'square scale inverse')
            t=self.mul(A,slope);ci=self.inv(t-1,'normalizing point inverse')
            # A^-5 F_5(A lambda) = product(lambda-theta/A).
            f=linear(1)
            for theta in contacts:f=self.mul(f,slope-ainv.scale(theta))
            r=self.mul(f,self.power(ci,6));ri=self.inv(r,'contact detector inverse')
            vi=self.mul(ci,ri);prefix=self.mul(r,self.sq(ci))
            factors=[]
            for m in (1,16,k):
                qm=self.mul(prefix,self.power(vi,2*m))
                factors.append(self.evaluate_field_polynomial(grouped[m],qm))
            W=self.fmul(self.fmul(factors[0],factors[1]),factors[2])
            # Tr(1/W)=2W_0/N(W); the inverse of W_0 enforces every needed guard.
            w0inv=self.inv(W[0],'nonzero reciprocal trace numerator')
            b=self.mul(r,self.sq(self.mul(self.fnorm(W),w0inv))).scale(F(1,4))
            self.pole(b,'coordinate'+str(i),True)
        return self.export()
    def export(self):
        gate_by_var={g['variable']:g for g in self.gates}
        needed={0}; stack=[]
        for r in self.rows:
            if r['kind']!='gate':
                for mon in r['terms']:stack.extend(mon)
        while stack:
            i=stack.pop()
            if i in needed:continue
            needed.add(i)
            if i in gate_by_var:
                for a in gate_by_var[i]['arguments']:
                    stack.extend(v for v,n,d in a if v>=0)
                for mon,n,den in gate_by_var[i].get('polynomial',[]):stack.extend(mon)
                if 'pair' in gate_by_var[i]:stack.append(gate_by_var[i]['pair'])
        kept_gates={g['row'] for i,g in gate_by_var.items() if i in needed}
        active_rows=[(i,r) for i,r in enumerate(self.rows) if r['kind']!='gate' or i in kept_gates]
        initial_active_indices=[i for i,r in active_rows]
        initial_needed=set(needed)
        # Retain the optional constant-computation chain in the small-height
        # variant; eliminating it would reconstruct the enormous literal K.
        allowed={v for v in gate_by_var if not self.vars[v]['name'].startswith('anchor constant square')}
        active_rows,operations=simplify_quadratics(active_rows,allowed)
        needed={0}|{v for i,r in active_rows for m in r['terms'] for v in m}
        mapping={old:new for new,old in enumerate(sorted(needed))}
        rows=[]
        for old,r in active_rows:
            den=lcm(*(c.denominator for c in list(r['terms'].values())+[r['K_constant']]))
            ns=[int(c*den) for c in r['terms'].values()]+[int(r['K_constant']*den)]
            content=0
            for c in ns:content=gcd(content,abs(c))
            content=max(1,content)
            coeff=[(tuple(mapping[v] for v in mon),0,int(c*den)//content) for mon,c in sorted(r['terms'].items())]
            if r['K_constant']:coeff.append(((),1,int(r['K_constant']*den)//content))
            rows.append({'label':r['label'],'kind':r['kind'],
                         'terms':[[list(mon),kp,c] for mon,kp,c in coeff],
                         'old_row':old,'clearing_multiplier':[den,content]})
        variables=[self.vars[i]|{'index':mapping[i],'original_index':i} for i in sorted(needed)]
        gates=[g for g in self.gates if g['variable'] in initial_needed]
        polynomial={}
        for row in rows:
            tt=row['terms']
            for a,(ma,ka,ca) in enumerate(tt):
                for b in range(a,len(tt)):
                    mb,kb,cb=tt[b]
                    key=(tuple(sorted(ma+mb)),ka+kb)
                    polynomial[key]=polynomial.get(key,0)+ca*cb*(1 if a==b else 2)
        polynomial={k:v for k,v in polynomial.items() if v}
        terms=[[list(m),k,c] for (m,k),c in sorted(polynomial.items())]
        categories=Counter(v['category'] for v in variables)
        max_numeric=max(abs(c) for c in polynomial.values())
        report={'direct_Lucas_polynomial_test':True,'total_variables':len(variables),'existential_witnesses':len(variables)-1,
                'total_degree':max(map(lambda t:len(t[0]),terms)),
                'quadratic_residuals':len(rows),'expanded_terms_in_Z_K':len(terms),
                'categories':dict(categories),'point_occurrences':len(self.point_names),
                'pole_blocks':len(self.pole_names),'fixed_anchor_symbol':self.literal_anchor,
                'max_integer_coefficient_bits_in_Z_K':max_numeric.bit_length(),
                'height_point_shared':self.share_height,
                'comparison_precision':self.precision,
                'scalar_height_order':self.scalar_order,
                'quadratic_preserving_eliminations':sum(o['kind']=='eliminate' for o in operations),
                'arithmetic_status':'Conditional on shared_source.tex, sharing_review.tex, the precision supplement when precision=52, and Sun 2026 Theorem 4.1.',
                'representation':'Complete sparse sum-of-squares quartic; K, when present, is a specified fixed integer, not an existential coordinate.'}
        return {'format':'shared-point-quartic-v1','variables':variables,'residuals':rows,
                'expanded_polynomial':terms,'fixed_constants':{'K':'3^(2^'+str(self.anchor_exponent)+')'} if self.literal_anchor else {},
                'derivation':{'gates':gates,'original_variables':self.vars,'active_map':mapping,
                              'initial_active_rows':initial_active_indices,'quadratic_operations':operations,
                              'source_rows':[{'label':r['label'],'kind':r['kind'],
                                              'terms':[[list(m),c.numerator,c.denominator] for m,c in sorted(r['terms'].items())],
                                              'K_constant':[r['K_constant'].numerator,r['K_constant'].denominator]}
                                             for r in self.rows]},'report':report}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--small-coefficients',action='store_true')
    p.add_argument('--share-height',action='store_true')
    p.add_argument('--precision',type=int,choices=(52,64),default=64)
    p.add_argument('--scalar-order',type=int,choices=(32,48),default=48)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    obj=Builder(not a.small_coefficients,a.share_height,a.precision,a.scalar_order).build()
    raw=(json.dumps(obj,separators=(',',':'))+'\n').encode()
    with gzip.open(a.output/'polynomial.json.gz','wb') as f:f.write(raw)
    report=obj['report']|{'uncompressed_json_bytes':len(raw),'uncompressed_sha256':hashlib.sha256(raw).hexdigest()}
    (a.output/'construction-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
