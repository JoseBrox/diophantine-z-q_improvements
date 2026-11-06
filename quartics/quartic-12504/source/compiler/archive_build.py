#!/usr/bin/env python3
"""Explicit degree-eight integer polynomial with a simultaneous Lucas certificate.

All witnesses range over Q. The theorem uses the arithmetic inputs stated
in the companion proof. This file computes every coefficient exactly.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd, lcm, comb
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT
MODULES = {}
PELL_PRECISION = 64
ANCHOR_SQUARINGS = 24


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.d = dict(value.d)
        elif isinstance(value, dict):
            self.d = {tuple(m): F(c) for m, c in value.items() if c}
        else:
            self.d = {(): F(value)} if value else {}

    @staticmethod
    def v(i):
        return P({(i,): F(1)})

    def __add__(self, other):
        other = P(other)
        d = dict(self.d)
        for m, c in other.d.items():
            d[m] = d.get(m, 0) + c
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.d.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        d = {}
        for m, c in self.d.items():
            for n, a in P(other).d.items():
                k = tuple(sorted(m + n))
                d[k] = d.get(k, 0) + c * a
        return P(d)

    __rmul__ = __mul__

    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=P(1);a=self
        while n:
            if n&1:out=out*a
            n//=2
            if n:a=a*a
        return out

    def key(self):
        return tuple(sorted(self.d.items()))

    def row(self):
        assert all(len(m) <= 4 for m in self.d), self.d
        if not self.d:
            return []
        den = lcm(*(c.denominator for c in self.d.values()))
        d = {m: int(c * den) for m, c in self.d.items()}
        common = gcd(*d.values())
        return [[c // common, list(m)] for m, c in sorted(d.items())]


class M:
    def __init__(self, name, free):
        self.name, self.free, self.count = name, free, free
        self.rows, self.calls, self.operations = [], [], []
        self.cache = {}

    def var(self, label='witness'):
        i = self.count
        self.count += 1
        self.operations.append(['variable', i, label])
        return i

    def force(self, expression, label='equation'):
        row = P(expression).row()
        if row:
            self.rows.append(row)
            self.operations.append(['equation', len(self.rows) - 1, label])

    def bind(self, expression, label='arithmetic'):
        p = P(expression)
        if len(p.d) == 1:
            (mon, c), = p.d.items()
            if len(mon) == 1 and c == 1 and mon[0] >= 0:
                return mon[0]
        if p.key() not in self.cache:
            i = self.var(label)
            self.force(P.v(i) - p, label)
            self.cache[p.key()] = i
        return self.cache[p.key()]

    def value(self, expression, label='arithmetic'):
        return P.v(self.bind(expression, label))

    def inv(self, expression, label='inverse'):
        i = self.var(label)
        self.force(P(expression) * P.v(i) - 1, label)
        return P.v(i)

    def bit(self, label='selector'):
        i = self.var(label)
        self.force(P.v(i) * P.v(i) - P.v(i), label)
        return P.v(i)

    def call(self, name, args, label=None):
        call = {'module': name, 'args': list(args)}
        if label:
            call['label'] = label
        self.calls.append(call)

    def save(self, **metadata):
        d = {'name': self.name, 'free': self.free,
             'locals': self.count - self.free,
             'residuals': self.rows, 'calls': self.calls,
             'construction_log': self.operations, **metadata}
        MODULES[self.name] = d
        write('modules/' + self.name + '.json', d)


def fa(a, b):
    return tuple(x + y for x, y in zip(a, b))


def fs(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, c):
    return tuple(c * x for x in a)


def raw_fmul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


class Field:
    def __init__(self, m):
        self.m = m
        self.D = tuple(P(a) for a in CURVE_D2)

    def mul(self, a, b):
        return tuple(self.m.value(x) for x in raw_fmul(a, b))

    def inv(self, a):
        b = tuple(P.v(self.m.var('field inverse')) for _ in range(2))
        product = raw_fmul(a, b)
        self.m.force(product[0] - 1, 'field inverse real')
        self.m.force(product[1], 'field inverse sqrt2')
        return b

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    @staticmethod
    def conj(a):
        return a[0], -a[1]

    def double(self, point):
        x, y = point['x'], point['y']
        slope = self.div(fs(scale(self.mul(x, x), 3), self.D), scale(y, 2))
        xx = fs(self.mul(slope, slope), scale(x, 2))
        yy = fs(self.mul(slope, fs(x, xx)), y)
        return {'x': xx, 'y': yy}

    def f(self, point):
        if 'f' not in point:
            point['f'] = self.inv(point['x'])
        return point['f']

    def z(self, point):
        if 'z' not in point:
            point['z'] = scale(self.div(point['x'], point['y']), -1)
        return point['z']

    def logarithm(self, point, precision=24):
        key = 'log' + str(precision)
        if key in point:
            return point[key]
        assert precision >= 4 and precision % 4 == 0
        z = self.z(point)
        z2 = self.mul(z, z)
        # Multiplication by the fixed element d^2 is linear in the two
        # rational coordinates, so it requires no auxiliary variables.
        w = raw_fmul(self.D, self.mul(z2, z2))
        coefficients = [F((-1)**j * comb(2*j, j), 4*j + 1)
                        for j in range(precision // 4)]
        n = len(coefficients)
        block = min(range(1, n + 1),
                    key=lambda m: (m + (n + m - 1)//m - 2, m))
        if LOG_BLOCK:block=LOG_BLOCK
        powers = [(P(1), P()), w]
        for k in range(2, block + 1):
            if k % 2 == 0:
                powers.append(self.mul(powers[k//2], powers[k//2]))
            else:
                powers.append(self.mul(powers[k-1], w))
        blocks = []
        for start in range(0, n, block):
            value = (P(), P())
            for k, coefficient in enumerate(coefficients[start:start + block]):
                value = fa(value, scale(powers[k], coefficient))
            blocks.append(value)
        acc = blocks[-1]
        for value in reversed(blocks[:-1]):
            acc = fa(self.mul(acc, powers[block]), value)
        point[key] = self.mul(z, acc)
        return point[key]



# Literal common parameters; no coefficient search remains.
CONTACT_SCALE=47027
CONTACT_SHIFT=3
CONTACT_W=25878772920
CHART=10
PARITY=7
BASE_GATES=False
UNIT_SCALE=False
LOG_BLOCK=0
CURVE_DROOT=(75,-53)
CURVE_D2=(11243,-7950)
BASE_POINT=((F(1641,8),F(-145)),(F(-15465,4),F(87483,32)))


def fvar(m,label):
    return tuple(P.v(m.var(label+'.'+str(i))) for i in range(2))

def feq(m,p,label):
    for i,c in enumerate(p):m.force(c,label+'.'+str(i))

def norm(p):return p[0]*p[0]-2*p[1]*p[1]


def gpoint(self,label):
    """Sparse 2E chart; xf=1 supplies its necessary nonzero guard."""
    m=self.m
    u,v,w,z=[fvar(m,label+'.'+part) for part in ('u','v','w','z')]
    f=fvar(m,label+'.f')
    feq(m,fs(f,raw_fmul(u,u)),label+'.f=u^2')
    d=tuple(P(a) for a in CURVE_DROOT)
    feq(m,fs(fa(raw_fmul(v,v),raw_fmul(d,f)),(P(1),P())),label+'.v2+df=1')
    feq(m,fs(fa(raw_fmul(w,w),raw_fmul(v,v)),(P(2),P())),label+'.w2+v2=2')
    if CHART==10:
        h=fvar(m,label+'.h');feq(m,fs(h,raw_fmul(v,w)),label+'.h=vw')
    else:h=raw_fmul(v,w)
    feq(m,fa(raw_fmul(z,h),u),label+'.zh+u=0')
    x=fvar(m,label+'.x');y=fvar(m,label+'.y')
    feq(m,fs(raw_fmul(x,f),(P(1),P())),label+'.xf=1')
    feq(m,fa(raw_fmul(y,z),x),label+'.yz+x=0')
    return {'x':x,'y':y,'f':f,'z':z}
Field.gpoint=gpoint


def difference(self,a,b):
    """Sparse affine subtraction with a shared line intercept."""
    m=self.m;x,y=a['x'],a['y'];r,s=b['x'],b['y']
    lam,nu,xo,yo,Fo,Zo=[fvar(m,'difference.'+k) for k in ('lambda','nu','x','y','f','z')]
    feq(m,fs(fs(raw_fmul(lam,x),y),nu),'difference line at first point')
    feq(m,fs(fa(raw_fmul(lam,r),s),nu),'difference line at negated second point')
    feq(m,fa(fs(xo,raw_fmul(lam,lam)),fa(x,r)),'difference abscissa')
    feq(m,fs(fa(raw_fmul(lam,xo),yo),nu),'difference line at output')
    feq(m,fs(raw_fmul(Fo,xo),(P(1),P())),'difference reciprocal abscissa')
    feq(m,fa(raw_fmul(Zo,yo),xo),'difference formal parameter')
    m.inv(norm(fs(x,r)),'distinct abscissae guard')
    return {'x':xo,'y':yo,'f':Fo,'z':Zo}
Field.difference=difference


def make_parity():
    m=M('q_primeparity',1);b=P.v(0)
    t,U,e,p,q,s,h=[P.v(m.var('prime parity.'+v)) for v in ('t','U','e','p','q','s','h')]
    B=17*b
    m.force(U*(1+b*t*t)-b*(1-b*t*t),'prime parity rational parametrization')
    m.force(p*p-B*(1-e)*(1+3*e),'prime parity first conic')
    m.force(h-e*(B-U*U),'prime parity shared expression')
    if PARITY==8:
        w=P.v(m.var('prime parity.w'));m.force(w-B*h,'prime parity w=Bh')
    else:w=B*h
    m.force(B*q*q-(s*s-w)*(s*s+3*w),'prime parity second conic')
    m.save(semantics='Parity predicate from the supplied six-variable certificate, with exact reversible rescaling',witness_variant=PARITY)


def make_anchor():
    m=M('q_anchor',2)
    for i in range(2):
        a=P.v(m.var('anchor scaled reciprocal coordinate'))
        m.force(P.v(-(ANCHOR_SQUARINGS+1))*a-P.v(i),'anchor f/C')
        u0,u1,u2,u3,v1,v2,v3=[P.v(m.var('anchor norm witness')) for _ in range(7)]
        m.force(u0*u0-2*u1*u1-3*u2*u2+6*u3*u3-1,'anchor first norm')
        m.force((a-2*u0)**2-8*v1*v1-12*v2*v2+24*v3*v3-4,'anchor second norm')
    m.save(anchor_squarings=ANCHOR_SQUARINGS,anchor_constant_global_index=-(ANCHOR_SQUARINGS+1),inputs='two coordinates of f(S)=1/x(S)')


def make_batch(name,orders,parity):
    """Binary norm tree with fused cross-multiplied normalized bottom pairs."""
    m=M(name,1+len(orders));r=P.v(0);m.inv(r,'nonzero contact factor')
    power_cache={0:P(1),1:r}
    def rp(n):
        if n not in power_cache:
            h=rp(n//2);power_cache[n]=m.value(h*h,'shared contact power')
            if n%2:power_cache[n]=m.value(power_cache[n]*r,'shared contact power')
        return power_cache[n]
    assert orders[0]==1
    first=P.v(m.var('constant leaf norm'))
    m.force(r*first-r-P.v(1)*P.v(1),'fused constant leaf norm')
    nodes=[first];plan=[{'type':'constant_pair','test':1}];groups={}
    for i,L in enumerate(orders[1:],2):groups.setdefault(L,[]).append(i)
    for L,inds in sorted(groups.items()):
        for start in range(0,len(inds),2):
            pair=inds[start:start+2];v=P.v(m.var('normalized bottom norm'))
            if len(pair)==1:
                m.force(v*rp(L)-P.v(pair[0]),'single normalized leaf')
                plan.append({'type':'single','test':pair[0],'order':L})
            else:
                a,b=map(P.v,pair);m.force(v*rp(2*L)-a*a-r*b*b,'fused normalized pair')
                plan.append({'type':'pair','tests':pair,'order':L})
            nodes.append(v)
    levels=[]
    while len(nodes)>1:
        levels.append(len(nodes))
        nodes=[m.value(nodes[i]*nodes[i]+r*nodes[i+1]*nodes[i+1],'cubic norm node') if i+1<len(nodes) else nodes[i] for i in range(0,len(nodes),2)]
    W=nodes[0];W2=m.value(W*W,'batched square')
    if name=='q_height_batch':
        bits={p:m.bit('height local class '+str(p)) for p in (2,3,5,7,11,13,17)}
        sign=m.bit('height sign correction')
        A=m.value((1+bits[2])*(1+2*bits[3])*(1+12*bits[13])*(1+16*bits[17]),'height correction product A')
        B=m.value((1+4*bits[5])*(1+6*bits[7])*(1+10*bits[11])*(1-2*sign),'height correction product B')
        arg=m.bind(A*B*r*W2,'corrected parity argument')
    else:arg=m.bind(r*W2,'parity argument')
    m.call(parity,[arg])
    m.save(orders=orders,norm_tree=plan,norm_level_sizes=levels,parity_module=parity,
           squareclass_correction=(name=='q_height_batch'),
           semantics='Psi(c*r*N_r(1,X_i/r^L_i)^2); constant leaf retained on left branch; c=1 except signed small-prime squareclass correction in height batch')


def field_tests(m,root,error,expressions):
    result=[m.bind(error)]
    for A,B in expressions:result.extend([m.bind(error*B),m.bind(A+B*root)])
    return result


def flat_point(p):return p['x']+p['y']


def make_multi_comparison():
    n=4;precision=PELL_PRECISION;free=n+4+4*n+4+3
    m=M('q_compare4',free);f=Field(m);at=n;proxies=tuple(P.v(i) for i in range(n))
    def read_point():
        nonlocal at
        p={'x':(P.v(at),P.v(at+1)),'y':(P.v(at+2),P.v(at+3))};at+=4;return p
    P4=read_point();Q4=[read_point() for _ in range(n)]
    fJ=(P.v(at),P.v(at+1));at+=2;zJinv=(P.v(at),P.v(at+1));at+=2
    root,error,r=P.v(at),P.v(at+1),at+2;assert r==free-1
    points=[f.gpoint('H')]+[f.gpoint('X'+str(i)) for i in range(n)]
    differences=[f.difference(p,q) for p,q in zip(points,[P4]+Q4)]
    formal=[f.f(p) for p in points]+[fJ]+[f.conj(f.f(p)) for p in differences]
    invlogH=f.inv(f.logarithm(points[0],precision))
    primary=[fs(f.mul(f.logarithm(p,precision),invlogH),(a,P())) for p,a in zip(points[1:],proxies)]
    alternate=[f.mul(f.conj(f.z(p)),zJinv) for p in differences]
    tests=field_tests(m,root,error,formal+primary+alternate);assert len(tests)==41
    m.call('q_batch41',[r]+tests)
    m.save(precision=precision,modeled_points=4,field_inequality_orders=[1]*11+[precision]*9,
           input_layout='beta,s,t,z;4P;4A;4S;4T;4Z;conj_fJ;inv_conj_zJ;root;root_error;r')


def base4():
    # Exact fixed-point arithmetic, no new witnesses or opaque constants.
    D=tuple(F(a) for a in CURVE_D2)
    def mul(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
    def add(a,b):return a[0]+b[0],a[1]+b[1]
    def sc(a,c):return a[0]*c,a[1]*c
    def inv(a):n=a[0]*a[0]-2*a[1]*a[1];return a[0]/n,-a[1]/n
    def double(p):
        x,y=p;lam=mul(add(sc(mul(x,x),3),sc(D,-1)),inv(sc(y,2)))
        xx=add(mul(lam,lam),sc(x,-2));yy=add(mul(lam,add(x,sc(xx,-1))),sc(y,-1));return xx,yy
    p=double(double(BASE_POINT))
    return {'x':tuple(P(a) for a in p[0]),'y':tuple(P(a) for a in p[1])}


def contacts(m,scalars):
    u,v=(P.v(m.var('contact common '+x)) for x in ('u','v'))
    raw=[F(1,32*CONTACT_W)*v,u,u-v,u-2401*v,u+F(343,32)*v]
    for a in scalars:
        A=m.value(CONTACT_SCALE*a+CONTACT_SHIFT,'affine transformed scalar')
        av=m.value(A*v,'affine numerator product')
        raw.extend([u-av,u-av+v,u-av+2401*v,u-av-F(343,32)*v])
    return [m.bind(a,'ordinary contact') for a in raw]


def make_root():
    m=M('Z_definition',1);f=Field(m)
    beta=P.v(m.bind(P.v(0)*P.v(0)+2,'beta=X^2+2'))
    points=[f.gpoint(k) for k in ('A','S','T','Z')];A,S,T,Z=points
    m.call('q_anchor',[m.bind(t) for t in S['f']])
    s,t,z=[P.v(m.var('index proxy '+k)) for k in ('s','t','z')]
    m.force(t*t-s*(s-2)*t*z+(s-2)**2*z*z-1,'Lucas norm proxy certificate')
    root=P.v(m.var('common sqrt2 approximation'));error=m.value(root*root-2,'root error')
    J0=f.gpoint('height J');first=f.f(J0)+f.f(S)+f.div(f.z(S),f.z(J0))
    r=P(1)
    for c in (beta,beta-1,beta-2401,32*beta+343,2*beta-1):r=m.value(r*c,'scalar height contact product')
    m.call('q_height_batch',[m.bind(r)]+[m.bind(a) for a in first])
    if BASE_GATES:
        base={'x':tuple(P(a) for a in BASE_POINT[0]),'y':tuple(P(a) for a in BASE_POINT[1])}
        P4=f.double(f.double(base))
    else:P4=base4()
    Q4=[f.double(f.double(q)) for q in points]
    J=f.gpoint('common comparison J');fJ=f.conj(f.f(J));zJinv=f.inv(f.conj(f.z(J)))
    prefix=[m.bind(a) for a in (beta,s,t,z)+flat_point(P4)+sum((flat_point(q) for q in Q4),())+fJ+zJinv+(root,error)]
    assert len(prefix)==30
    e=P.v(m.var('common coordinate denominator'));m.inv(e,'nonzero coordinate denominator')
    scalars=[e]+[m.value(e*x,'integer scaled coordinate') for q in points for x in q['x']]
    for r in contacts(m,scalars):m.call('q_compare4',prefix+[r],'simultaneous four-index comparison')
    m.save(precision=PELL_PRECISION,anchor_squarings=ANCHOR_SQUARINGS,chart=CHART,prime_parity_witnesses=PARITY,
           proxy_indices=[m.bind(a) for a in (beta,s,t,z)],point_coordinates={k:[m.bind(x) for x in flat_point(q)] for k,q in zip(('A','S','T','Z'),points)},
           coordinate_scalar_count=9,ordinary_contact_count=41,contact_scale=CONTACT_SCALE,contact_shift=CONTACT_SHIFT,contact_W=CONTACT_W,
           scalar_height_orders=[1,1,1,1,48,48],scalar_rule='beta=X^2+2',pell_equation='t^2-s*(s-2)*t*z+(s-2)^2*z^2-1=0')


def write(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,separators=(',',':'))+'\n')


def flatten():
    shared=[[[-3,[]],[1,[-1]]]]+[[[1,[-i-1]],[-1,[-i,-i]]] for i in range(1,ANCHOR_SQUARINGS+1)]
    g=ANCHOR_SQUARINGS+1;rows=[];nxt=g+1;memo={}
    def count(name):
        if name in memo:return memo[name]
        d=MODULES[name];w=d['locals'];r=len(d['residuals'])
        for c in d['calls']:
            cw,cr=count(c['module']);w+=cw;r+=cr
        memo[name]=[w,r];return w,r
    def emit(row,tr):rows.append([[c,sorted(tr(v) for v in mon)] for c,mon in row])
    for row in shared:emit(row,lambda v:-v)
    def visit(name,args):
        nonlocal nxt
        d=MODULES[name];start=nxt;nxt+=d['locals']
        def tr(v):return -v if v<0 else args[v] if v<d['free'] else start+v-d['free']
        for row in d['residuals']:emit(row,tr)
        for call in d['calls']:visit(call['module'],[tr(v) for v in call['args']])
    visit('Z_definition',[0]);w,r=count('Z_definition');assert nxt==w+g+1 and len(rows)==r+g
    counts={'witnesses':nxt-1,'residuals':len(rows),'degree':2*max(len(mon) for row in rows for c,mon in row),
            'modules':memo,'stored_residuals':sum(len(d['residuals']) for d in MODULES.values())+g,
            'stored_calls':sum(len(d['calls']) for d in MODULES.values()),'anchor_squarings':ANCHOR_SQUARINGS,'chart':CHART,'prime_parity_witnesses':PARITY,'unit_scale':UNIT_SCALE,'base_gates':BASE_GATES,'curve_droot':CURVE_DROOT,'curve_d2':CURVE_D2,'log_block':LOG_BLOCK}
    write('shared.json',{'witnesses':g,'residuals':shared})
    write('polynomial.json',{'semantics':'Sum the square of every instantiated residual. Variable 0 is free X; all remaining variables range over Q.',
                           'root':'Z_definition','modules':{n:'modules/'+n+'.json' for n in MODULES},'shared':'shared.json','counts':counts})
    write('counts.json',counts)
    with (OUT/'residuals.jsonl').open('w') as out:
        out.write(json.dumps(counts,separators=(',',':'))+'\n')
        for row in rows:out.write(json.dumps(row,separators=(',',':'))+'\n')
    return counts


def main():
    import argparse
    global OUT,CHART,PARITY,BASE_GATES,UNIT_SCALE,CURVE_DROOT,CURVE_D2,BASE_POINT,LOG_BLOCK
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'candidate');parser.add_argument('--chart',type=int,choices=(8,10),default=10);parser.add_argument('--parity',type=int,choices=(7,8),default=7)
    parser.add_argument('--base-gates',action=argparse.BooleanOptionalAction,default=True)
    parser.add_argument('--unit-scale',action=argparse.BooleanOptionalAction,default=True)
    parser.add_argument('--log-block',type=int,choices=range(1,17),default=2)
    args=parser.parse_args();OUT=args.out.resolve();CHART=args.chart;PARITY=args.parity;BASE_GATES=args.base_gates;UNIT_SCALE=args.unit_scale;LOG_BLOCK=args.log_block
    if UNIT_SCALE:
        CURVE_DROOT=(3,-1);CURVE_D2=(11,-6)
        BASE_POINT=((F(57,8),F(-7,2)),(F(-165,8),F(417,32)))
    make_parity();make_anchor();make_batch('q_batch41',[1]*23+[PELL_PRECISION]*18,'q_primeparity');make_batch('q_height_batch',[1]*4+[48]*2,'q_primeparity');make_multi_comparison();make_root()
    print(json.dumps(flatten(),indent=2))
if __name__=='__main__':main()
