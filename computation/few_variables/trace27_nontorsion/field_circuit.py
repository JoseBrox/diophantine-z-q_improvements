"""Exact guarded rational operations and arithmetic in Q(sqrt(2)).

Extracted without arithmetic changes from the inherited circuit helper.
Source identities and the extraction are recorded in provenance.json.
"""
from __future__ import annotations
from fractions import Fraction

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

