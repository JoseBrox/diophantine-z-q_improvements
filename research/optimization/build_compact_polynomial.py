#!/usr/bin/env python3
"""An exact, finite arithmetic-circuit specification with 855 variables.

The output is a polynomial, not a circuit with existential gate variables.
Its two formal parameters range over fixed finite lists; their product is
part of the polynomial specification. All rational divisions are removed
by numerator extraction and one branch-local product-of-denominators guard.
The arithmetic characterization of Z is inherited from the pinned source.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


class Circuit:
    def __init__(self):
        self.nodes = []
        self.cache = {}
        self.bounds = []
        self.variables = []
        self.equations = []
        self.guards = set()
        self.guard_descriptions = []
        self.factor_cache = {}
        self.point_count = 0
        self.pole_count = 0
        self.zero = self.node('int', 0)
        self.one = self.node('int', 1)

    def node(self, op, *args):
        key = (op, *args)
        if key in self.cache:
            return self.cache[key]
        if op == 'int':
            degree, bits = 0, (abs(args[0])-1).bit_length() if args[0] else 0
        elif op == 'parameter':
            degree, bits = 0, (args[1]-1).bit_length()
        elif op == 'variable':
            degree, bits = 1, 0
        elif op == 'neg':
            degree, bits = self.bounds[args[0]]
        elif op == 'add':
            degree = max(self.bounds[a][0] for a in args)
            bits = max(self.bounds[a][1] for a in args) + (len(args)-1).bit_length()
        elif op == 'mul':
            degree = sum(self.bounds[a][0] for a in args)
            bits = sum(self.bounds[a][1] for a in args)
        elif op == 'pow':
            degree, bits = (a*args[1] for a in self.bounds[args[0]])
        else:
            raise ValueError(op)
        index = len(self.nodes)
        self.nodes.append(list(key))
        self.bounds.append((degree, bits))
        self.cache[key] = index
        return index

    def add(self, a, b):
        if a == self.zero: return b
        if b == self.zero: return a
        if self.nodes[a] == ['neg', b] or self.nodes[b] == ['neg', a]: return self.zero
        if a == b: return self.mul(self.node('int', 2), a)
        if self.nodes[a][0] == self.nodes[b][0] == 'int':
            return self.node('int', self.nodes[a][1]+self.nodes[b][1])
        fa,fb=self.factors(a),self.factors(b)
        common={k:min(e,fb.get(k,0)) for k,e in fa.items() if k in fb}
        if common:
            aa=self.from_factors({k:e-common.get(k,0) for k,e in fa.items()})
            bb=self.from_factors({k:e-common.get(k,0) for k,e in fb.items()})
            return self.mul(self.from_factors(common),self.node('add',*sorted((aa,bb))))
        return self.node('add', *sorted((a, b)))

    def factors(self,a):
        if a in self.factor_cache:return self.factor_cache[a]
        op,*args=self.nodes[a]
        if op=='int' and args[0]==1:result={}
        elif op=='mul':
            result={}
            for child in args:
                for k,e in self.factors(child).items():result[k]=result.get(k,0)+e
        elif op=='pow':result={k:e*args[1] for k,e in self.factors(args[0]).items()}
        elif op=='neg':
            result=dict(self.factors(args[0]));k=self.node('int',-1);result[k]=result.get(k,0)+1
        else:result={a:1}
        self.factor_cache[a]=result
        return result

    def from_factors(self,ff):
        terms=[]
        for k,e in sorted(ff.items()):
            if not e:continue
            if self.nodes[k]==['int',-1]:e%=2
            if e:terms.append(self.power(k,e))
        if not terms:return self.one
        if len(terms)==1:return terms[0]
        return self.node('mul',*sorted(terms))

    def neg(self, a):
        if a == self.zero: return a
        if self.nodes[a][0] == 'neg': return self.nodes[a][1]
        if self.nodes[a][0] == 'int': return self.node('int', -self.nodes[a][1])
        return self.node('neg', a)

    def mul(self, a, b):
        if a == self.zero or b == self.zero: return self.zero
        if a == self.one: return b
        if b == self.one: return a
        if a == b: return self.power(a, 2)
        if self.nodes[a][0] == self.nodes[b][0] == 'int':
            x = self.nodes[a][1]*self.nodes[b][1]
            if x.bit_length() <= 128: return self.node('int', x)
        return self.node('mul', *sorted((a, b)))

    def power(self, a, e):
        assert isinstance(e, int) and e >= 0
        if e == 0: return self.one
        if e == 1 or a in (self.zero, self.one): return a
        if self.nodes[a][0] == 'pow':
            return self.power(self.nodes[a][1], self.nodes[a][2]*e)
        return self.node('pow', a, e)

    def rational(self, value):
        if isinstance(value, Rational): return value
        value = Fraction(value)
        return Rational(self, self.node('int', value.numerator), self.node('int', value.denominator))

    def variable(self, name, category):
        i = len(self.variables)
        self.variables.append({'index':i, 'name':name, 'category':category})
        return Rational(self, self.node('variable', i), self.one)

    def parameter(self, name, bound):
        return Rational(self, self.node('parameter', name, bound), self.one)

    def nonzero(self, a, label='division'):
        a = self.rational(a)
        if a.n == self.zero: raise ValueError('Identically zero divisor: '+label)
        if self.nodes[a.n][0] == 'int': return
        self.guards.add(a.n)
        self.guard_descriptions.append([a.n, label])

    def equation(self, a, label):
        a = self.rational(a)
        self.equations.append({'numerator':a.n, 'denominator':a.d, 'label':label})


class Rational:
    def __init__(self, circuit, numerator, denominator):
        self.c = circuit
        if numerator == circuit.zero:
            numerator, denominator = circuit.zero, circuit.one
        if numerator == denominator:
            numerator, denominator = circuit.one, circuit.one
        if numerator != circuit.zero:
            fn,fd=circuit.factors(numerator),circuit.factors(denominator)
            common={k:min(e,fd.get(k,0)) for k,e in fn.items() if k in fd}
            numerator=circuit.from_factors({k:e-common.get(k,0) for k,e in fn.items()})
            denominator=circuit.from_factors({k:e-common.get(k,0) for k,e in fd.items()})
        self.n, self.d = numerator, denominator

    def __add__(self, other):
        other = self.c.rational(other)
        if self.d == other.d:
            return Rational(self.c, self.c.add(self.n,other.n),self.d)
        fa,fb=self.c.factors(self.d),self.c.factors(other.d)
        den={k:max(fa.get(k,0),fb.get(k,0)) for k in fa.keys()|fb.keys()}
        ma=self.c.from_factors({k:e-fa.get(k,0) for k,e in den.items()})
        mb=self.c.from_factors({k:e-fb.get(k,0) for k,e in den.items()})
        return Rational(self.c,self.c.add(self.c.mul(self.n,ma),self.c.mul(other.n,mb)),self.c.from_factors(den))
    __radd__ = __add__
    def __neg__(self): return Rational(self.c,self.c.neg(self.n),self.d)
    def __sub__(self, other): return self + -self.c.rational(other)
    def __rsub__(self, other): return self.c.rational(other) + -self
    def __mul__(self, other):
        other = self.c.rational(other)
        a,b,c,d = self.n,self.d,other.n,other.d
        if a == d: a=d=self.c.one
        if b == c: b=c=self.c.one
        return Rational(self.c,self.c.mul(a,c),self.c.mul(b,d))
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = self.c.rational(other)
        self.c.nonzero(other)
        return self * Rational(self.c,other.d,other.n)
    def __rtruediv__(self, other): return self.c.rational(other)/self
    def __pow__(self, e):
        return Rational(self.c,self.c.power(self.n,e),self.c.power(self.d,e))


class Builder:
    def __init__(self):
        self.c = Circuit()
        self.j = self.c.parameter('j',211)
        self.correction = self.c.parameter('correction',510510)
        self.D = self.field(11,-6)

    def field(self,a=0,b=0): return self.c.rational(a),self.c.rational(b)
    @staticmethod
    def add(a,b): return a[0]+b[0],a[1]+b[1]
    @staticmethod
    def sub(a,b): return a[0]-b[0],a[1]-b[1]
    @staticmethod
    def scale(a,r): return a[0]*r,a[1]*r
    @staticmethod
    def mul(a,b): return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
    @staticmethod
    def conj(a): return a[0],-a[1]
    def inv(self,a):
        norm=a[0]**2-2*a[1]**2
        return a[0]/norm,-a[1]/norm
    def div(self,a,b): return self.mul(a,self.inv(b))
    def square(self,a): return self.mul(a,a)
    def double(self,p):
        x,y=p['x'],p['y']
        slope=self.div(self.sub(self.scale(self.square(x),3),self.D),self.scale(y,2))
        xx=self.sub(self.square(slope),self.scale(x,2))
        yy=self.sub(self.mul(slope,self.sub(x,xx)),y)
        return {'x':xx,'y':yy}
    def reciprocal(self,p): return self.inv(p['x'])
    def parameter_at_identity(self,p): return self.scale(self.div(p['x'],p['y']),-1)

    def point(self,label):
        self.c.point_count += 1
        a=tuple(self.c.variable(label+'.a'+str(i),'point') for i in range(2))
        C=self.c.variable(label+'.C','point')
        A,B=self.sub(self.mul(self.square(a),a),self.mul(self.D,a))
        lam=self.j**2-2
        v=(C**2-A-self.j*B)/lam
        h=B/2+self.j*v
        self.c.equation(C**2*v-h**2,label+'.quartic half-point')
        b1=h/C
        b=(C-self.j*b1,b1)
        result=self.double({'x':a,'y':b})
        # The old charts exclude both zero abscissa and zero ordinate.
        self.inv(result['x']);self.inv(result['y'])
        return result

    def difference(self,a,b):
        slope=self.div(self.add(a['y'],b['y']),self.sub(a['x'],b['x']))
        nu=self.sub(self.mul(slope,a['x']),a['y'])
        x=self.sub(self.sub(self.square(slope),a['x']),b['x'])
        y=self.sub(nu,self.mul(slope,x))
        return {'x':x,'y':y}

    def logarithm(self,p,precision):
        f=self.reciprocal(p)
        w=self.mul(self.D,self.square(f))
        aa=[Fraction(1),Fraction(-2,5)]
        for k in range(2,precision//4): aa.append(aa[-1]*Fraction(4*k-5,4*k+1))
        out=self.field()
        for a in reversed(aa[:precision//4]): out=self.add(self.mul(out,w),self.field(a))
        return self.mul(self.parameter_at_identity(p),out)

    def parity(self,b,label):
        self.c.pole_count += 1
        t,e,p,q,s=[self.c.variable(label+'.'+k,'pole') for k in ('t','e','p','q','s')]
        U=b*(1-b*t*t)/(1+b*t*t)
        B=17*b;h=e*(B-U*U)
        self.c.equation(p*p-B*(1-e)*(1+3*e),label+'.first conic')
        self.c.equation(B*q*q-(s*s-B*h)*(s*s+3*B*h),label+'.second conic')

    def norm_batch(self,r,tests,orders,label,height=False):
        assert len(tests)==len(orders) and orders[0]==1
        nodes=[1+tests[0]**2/r]
        for e in sorted(set(orders[1:])):
            xs=[x for x,k in zip(tests[1:],orders[1:]) if k==e]
            power=r**e
            for k in range(0,len(xs),2):
                a=xs[k]/power
                nodes.append(a if k+1==len(xs) else a*a+r*(xs[k+1]/power)**2)
        while len(nodes)>1:
            nodes=[nodes[k] if k+1==len(nodes) else nodes[k]**2+r*nodes[k+1]**2 for k in range(0,len(nodes),2)]
        b=r*nodes[0]**2
        self.parity(self.correction*b if height else b,label+'.parity')

    def anchor(self,f):
        C=Rational(self.c,self.c.power(self.c.node('int',3),2**24),self.c.one)
        r=f[0]**2+f[0]*f[1]-f[1]**2
        u,v,w=[self.c.variable('anchor.'+k,'anchor') for k in ('u','v','w')]
        self.c.equation(u*u+6*v*v-2*w*w-3*r*r+2*C**4,'packed semilocal anchor')

    def comparison(self,proxies,targets,fJ,zJinv,theta,error,r,label):
        points=[self.point(label+'.'+s) for s in ('H','beta','s','t','z')]
        differences=[self.difference(p,q) for p,q in zip(points,targets)]
        expressions=[self.reciprocal(p) for p in points]+[fJ]+[self.conj(self.reciprocal(p)) for p in differences]
        denominator=self.logarithm(points[0],64)
        expressions += [self.sub(self.div(self.logarithm(p,16 if k==0 else 64),denominator),self.field(proxy)) for k,(p,proxy) in enumerate(zip(points[1:],proxies))]
        expressions += [self.mul(self.conj(self.parameter_at_identity(p)),zJinv) for p in differences]
        assert len(expressions)==20
        tests=[error]
        for A,B in expressions: tests.extend((error*B,A+theta*B))
        orders=[1]*23+[16]*2+[64]*8+[16]*2+[64]*6
        self.norm_batch(r,tests,orders,label+'.norm')

    def build(self):
        X=self.c.variable('input','input')
        beta=X*X+2
        points=[self.point(k) for k in ('A','S','T','Z')]
        self.anchor(self.reciprocal(points[1]))
        s,t,z=[self.c.variable('proxy.'+k,'proxy') for k in ('s','t','z')]
        self.c.equation(t*t-s*(s-2)*t*z+(s-2)**2*z*z-1,'Lucas relation')
        theta=self.c.variable('theta','root approximation');error=theta*theta-2
        J0=self.point('height.J')
        tests=list(self.reciprocal(J0)+self.reciprocal(points[1])+self.div(self.parameter_at_identity(points[1]),self.parameter_at_identity(J0)))
        r=self.c.rational(1)
        for f in (beta,beta-1,beta-2401,32*beta+343,2*beta-1):r=r*f
        self.norm_batch(r,tests,[1,1,1,1,48,48],'height',True)
        base={'x':self.field(Fraction(57,8),Fraction(-7,2)),'y':self.field(Fraction(-165,8),Fraction(417,32))}
        targets=[self.double(self.double(base))]+[self.double(self.double(p)) for p in points]
        J=self.point('comparison.J')
        fJ=self.conj(self.reciprocal(J));zJinv=self.inv(self.conj(self.parameter_at_identity(J)))
        e=self.c.variable('coordinate denominator','denominator');self.c.nonzero(e,'coordinate denominator')
        scalars=[e]+[e*x for p in points for x in p['x']]
        u,v=[self.c.variable('contact.'+k,'contact') for k in ('u','v')]
        contacts=[v/Fraction(32*25878772920),u,u-v,u-2401*v,u+Fraction(343,32)*v]
        for a in scalars:
            A=47027*a+3
            contacts.extend([u-A*v,u-A*v+v,u-A*v+2401*v,u-A*v-Fraction(343,32)*v])
        assert len(contacts)==41
        for k,r in enumerate(contacts):self.comparison((beta,s,t,z),targets,fJ,zJinv,theta,error,r,'contact'+str(k))
        inverse=self.c.variable('common denominator inverse','inverse')
        guard_factors=set()
        for g in sorted(self.c.guards):
            for f in self.c.factors(g):
                if self.c.nodes[f][0]!='int':guard_factors.add(f)
        denominator=self.c.from_factors({f:1 for f in guard_factors})
        final=self.c.zero
        for row in self.c.equations:final=self.c.add(final,self.c.power(row['numerator'],2))
        guard=self.c.add(self.c.mul(inverse.n,denominator),self.c.neg(self.c.one))
        final=self.c.add(final,self.c.power(guard,2))
        corrections=[]
        primes=(2,3,5,7,11,13,17)
        for mask in range(128):
            n=1
            for k,p in enumerate(primes):
                if mask>>k&1:n*=p
            corrections.extend((n,-n))
        assert self.c.point_count==211 and self.c.pole_count==42
        assert len(self.c.variables)==855
        bdeg,bbits=self.c.bounds[final]
        report={'total_variables':len(self.c.variables),'existential_witnesses':len(self.c.variables)-1,
                'categories':dict(Counter(v['category'] for v in self.c.variables)),
                'point_charts':self.c.point_count,'pole_blocks':self.c.pole_count,
                'residuals_per_branch':len(self.c.equations)+1,'distinct_nonzero_guards':len(self.c.guards),
                'distinct_guard_factors':len(guard_factors),
                'template_nodes':len(self.c.nodes),'finite_branches':212*256,
                'degree_upper_bound':bdeg*212*256,'coefficient_log2_upper_bound':bbits*212*256,
                'bounds_are_upper_bounds_not_exact_expansion_statistics':True,
                'scope':'Exact polynomial circuit specification. Arithmetic characterization inherits the source theorem; no global minimality claimed.'}
        obj={'format':'integer-polynomial-circuit-with-finite-constant-products-v1',
             'source_commit':'28e87b1b62af0effd954605af7f70b2699dd5672',
             'semantics':'Product over j=0,...,211 and correction in the specified 256 integers of the template polynomial. These are finite constants, not variables. Each circuit node denotes a polynomial expression and adds no quantified coordinate.',
             'variables':self.c.variables,'nodes':self.c.nodes,'template_output':final,
             'finite_parameters':{'j':list(range(212)),'correction':corrections},
             'rational_equations_before_clearing':self.c.equations,
             'nonzero_numerators':sorted(self.c.guards),'guard_product_node':denominator,
             'report':report}
        return obj


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    obj=Builder().build()
    raw=(json.dumps(obj,separators=(',',':'))+'\n').encode()
    (a.output/'polynomial-circuit.json').write_bytes(raw)
    report=obj['report']|{'circuit_sha256':hashlib.sha256(raw).hexdigest(),'circuit_bytes':len(raw)}
    (a.output/'construction-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
