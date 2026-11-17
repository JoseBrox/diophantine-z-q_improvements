#!/usr/bin/env python3
"""Independent native-source evaluation on actual rational elliptic points.

All 64 ordinate-sign characters are checked for three actual index tuples
at two split primes. The reference implementation uses the ordinary chord
and tangent law, not the source's homogeneous differences or field circuit.
These are exact finite evaluations, not a test of the infinite existence
premises or a numerical certification of the stored B=3 defining shift.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt, prod
from pathlib import Path
import argparse
import hashlib
import json

class K:
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)
    def __add__(self, other):
        other = other if isinstance(other, K) else K(other)
        return K(self.a+other.a, self.b+other.b)
    __radd__ = __add__
    def __neg__(self): return K(-self.a, -self.b)
    def __sub__(self, other): return self+(-other if isinstance(other,K) else -K(other))
    def __rsub__(self, other): return K(other)-self
    def __mul__(self, other):
        other = other if isinstance(other,K) else K(other)
        return K(self.a*other.a+2*self.b*other.b,
                 self.a*other.b+self.b*other.a)
    __rmul__ = __mul__
    def inv(self):
        n = self.a*self.a-2*self.b*self.b
        return K(self.a/n, -self.b/n)
    def __truediv__(self, other):
        other = other if isinstance(other,K) else K(other)
        return self*other.inv()
    def __rtruediv__(self, other): return K(other)*self.inv()
    def __pow__(self, e):
        if e < 0: return self.inv()**(-e)
        out, base = K(1), self
        while e:
            if e & 1: out = out*base
            base, e = base*base, e//2
        return out
    def __eq__(self, other):
        other = other if isinstance(other,K) else K(other)
        return self.a == other.a and self.b == other.b
    def pair(self): return [str(self.a), str(self.b)]

D = K(11,-6)
P = (K(Q(57,8),Q(-7,2)),K(Q(-165,8),Q(417,32)))
assert P[1]**2 == P[0]**3-D*P[0]

def add(left, right):
    if left is None: return right
    if right is None: return left
    x,y = left; X,Y = right
    if x == X:
        if y == -Y: return None
        slope = (3*x*x-D)/(2*y)
    else:
        slope = (Y-y)/(X-x)
    xx = slope*slope-x-X
    return xx, slope*(x-xx)-y

def multiple(n):
    if n < 0:
        x,y = multiple(-n)
        return x,-y
    answer, base = None, P
    while n:
        if n & 1: answer = add(answer,base)
        base, n = add(base,base), n//2
    return answer

def qsqrt(value):
    if value < 0: return None
    n,d = isqrt(value.numerator), isqrt(value.denominator)
    return Q(n,d) if n*n == value.numerator and d*d == value.denominator else None

def ksqrt(value):
    norm = value.a*value.a-2*value.b*value.b
    rootnorm = qsqrt(norm)
    assert rootnorm is not None
    for nr in (rootnorm,-rootnorm):
        a = qsqrt((value.a+nr)/2)
        if a is not None and a:
            root = K(a,value.b/(2*a))
            if root*root == value: return root
    if value.b == 0:
        b = qsqrt(value.a/2)
        if b is not None: return K(0,b)
    raise AssertionError('actual point abscissa not a square')

def modq(value,p):
    value = Q(value)
    return value.numerator*pow(value.denominator,-1,p)%p

def sqrt_mod_prime(a,p):
    a %= p
    assert pow(a,(p-1)//2,p) == 1
    if p%4 == 3: return pow(a,(p+1)//4,p)
    q,s = p-1,0
    while q%2 == 0: q,s=q//2,s+1
    z=2
    while pow(z,(p-1)//2,p) != p-1: z+=1
    c,x,t,m=pow(z,q,p),pow(a,(q+1)//2,p),pow(a,q,p),s
    while t != 1:
        i,tt=1,t*t%p
        while tt != 1: i,tt=i+1,tt*tt%p
        b=pow(c,2**(m-i-1),p)
        x,t,c,m=x*b%p,t*b*b%p,b*b%p,i
    assert x*x%p == a
    return x

def embedding(value,root,p):
    return (modq(value.a,p)+root*modq(value.b,p))%p

def fp_difference(left,right,p):
    # Ordinary chord formula for left + (-right).
    x,y=left; X,Y=right
    slope=(y+Y)*pow(x-X,-1,p)%p
    xx=(slope*slope-x-X)%p
    yy=(slope*(x-xx)-y)%p
    return xx,yy

def fp_parameter(point,p): return -point[0]*pow(point[1],-1,p)%p

def evaluate_dag(nodes,variables,p):
    out=[]
    for op,*data in nodes:
        if op=='int': v=data[0]%p
        elif op=='parameter': v=data[1]%p
        elif op=='variable': v=variables[data[0]]%p
        elif op=='neg': v=-out[data[0]]%p
        elif op=='add': v=sum(out[i] for i in data)%p
        elif op=='mul': v=prod(out[i] for i in data)%p
        elif op=='pow': v=pow(out[data[0]],data[1],p)
        else: raise AssertionError(op)
        out.append(v)
    return out

def audit(source,p,n,h):
    root=sqrt_mod_prime(2,p)
    indices={'A':n,'H':h,'UA':n*h}
    points={name:multiple(index) for name,index in indices.items()}
    chart={name:(ksqrt(point[0]),point[1]/ksqrt(point[0])) for name,point in points.items()}
    for name,(hh,jj) in chart.items():
        assert hh**2 == points[name][0]
        assert jj**2 == hh**4-D
        assert hh*jj == points[name][1]
    variables=[1]*len(source['variables'])
    names={v['name']:v['index'] for v in source['variables']}
    B=source['fixed_parameters']['fixed_input_shift']
    T=2*points['A'][0].a
    M=(Q(n*n+B))**4+T**4
    a=M**4
    z=a+11
    variables[names['input.X']]=n%p
    variables[names['contact.z']]=modq(z,p)
    variables[names['pole.v']]=2
    variables[names['pole.s']]=3
    for name,(hh,jj) in chart.items():
        variables[names[name+'.a0']]=modq(hh.a,p)
        variables[names[name+'.a1']]=modq(hh.b,p)
    events={e['operation']:e for e in source['events'] if e['operation']!='point_block'}
    pole=next(block for block in source['finite_blocks'] if block['kind']=='pole')
    checked=0
    for signs in product((-1,1),repeat=6):
        slots={}
        for index,name in enumerate(('A','H','UA')):
            hh,jj=chart[name]
            jp=signs[2*index]*embedding(jj,root,p)%p
            jm=signs[2*index+1]*embedding(jj,-root,p)%p
            variables[names[name+'.U']]=(jp+jm)%p
            variables[names[name+'.V']]=(jp-jm)*pow(root,-1,p)%p
            variables[names[name+'.W']]=jp*jm%p
            point=points[name]
            slots[name]=[(embedding(point[0],root,p),signs[2*index]*embedding(point[1],root,p)%p),
                         (embedding(point[0],-root,p),signs[2*index+1]*embedding(point[1],-root,p)%p)]
        values=evaluate_dag(source['coefficient_dag'],variables,p)
        def rat(obj): return values[obj['numerator']]*pow(values[obj['denominator']],-1,p)%p
        def pair(obj):
            c0,c1=[rat(x) for x in obj]
            return [(c0+root*c1)%p,(c0-root*c1)%p]
        for event in (e for e in source['events'] if e['operation']=='point_block'):
            name=event['name']
            assert pair(event['x']) == [x for x,y in slots[name]]
            assert pair(event['y']) == [y for x,y in slots[name]]
        for block in (b for b in source['finite_blocks'] if b['kind']=='point_block'):
            U,V,W=[values[q] for q in block['variable_nodes']]
            AA,BB=rat(block['A']),rat(block['B'])
            assert (U*U-2*AA-2*W)%p == 0
            assert (V*V-AA+W)%p == 0
            assert (U*V-2*BB)%p == 0
            assert (U*W-AA*U+2*BB*V)%p == 0
            assert (V*W-BB*U+AA*V)%p == 0
            assert (W*W-AA*AA+2*BB*BB)%p == 0
        Pslots=[(embedding(P[0],r,p),embedding(P[1],r,p)) for r in (root,-root)]
        V0=[fp_difference(slots['H'][i],Pslots[i],p) for i in range(2)]
        V1=[fp_difference(slots['UA'][i],slots['A'][i],p) for i in range(2)]
        rr=[fp_parameter(slots['UA'][i],p)*pow(fp_parameter(slots['H'][i],p),-1,p)%p for i in range(2)]
        rp=[fp_parameter(V1[1-i],p)*pow(fp_parameter(V0[1-i],p),-1,p)%p for i in range(2)]
        tests=[[pow(slots['H'][i][0],-1,p) for i in range(2)],
               [pow(slots['UA'][i][0],-1,p) for i in range(2)],
               [pow(V0[1-i][0],-1,p) for i in range(2)],
               [pow(V1[1-i][0],-1,p) for i in range(2)],
               [(rr[i]-rp[i])%p for i in range(2)],
               [(rr[i]-n)%p for i in range(2)]]
        height=events['moving_contact_height']
        aa,zz=modq(a,p),modq(z,p)
        shifts=(-10,-8,-5,1,2,3,4,6,7)
        factors=[((aa+c)**2-zz*zz)%p for c in shifts]
        F=prod(factors)%p
        log_derivative=sum(2*(aa+c)*pow(f,-1,p) for c,f in zip(shifts,factors))%p
        u=-18*pow(log_derivative,-1,p)%p
        w=u*pow(1+u,-2,p)%p
        assert rat(height['M']) == modq(M,p)
        assert rat(height['trace']) == modq(T,p)
        assert rat(height['t']) == (aa*aa-zz*zz)%p
        assert rat(height['G']) == F
        assert rat(height['u']) == u and rat(height['w']) == w
        event=events['balanced_actual_detector']
        assert [pair(C) for C in event['original_tests']] == tests
        transformed=[[c*c*pow(1+u*c*c,-1,p)%p for c in C] for C in tests]
        assert [pair(C) for C in event['transformed_tests']] == transformed
        Ws=[prod((1+C[i]*C[i]*pow(u,-1,p))%p for C in transformed)%p for i in range(2)]
        V=(pow(Ws[0],-1,p)+pow(Ws[1],-1,p))%p
        b=4*w*pow(V,-2,p)%p
        eta=7*b%p
        assert pair(event['product_components']) == Ws
        assert rat(event['product_norm']) == Ws[0]*Ws[1]%p
        assert rat(event['trace']) == V
        assert rat(event['b']) == b and rat(event['eta']) == eta
        rawrad=(eta*(eta+4)**2*81-eta*(eta-4)**2*(1-eta)**2)%p
        assert rat(events['intrinsic_pole']['radicand']) == rawrad
        assert rat(pole['original_square_input']) == rawrad
        assert -values[pole['coefficient_nodes_ascending'][0]]%p == rawrad*values[pole['original_square_input']['denominator']]**2%p
        assert rawrad != 0
        for guard in source['guard_numerators']:
            if guard == pole['generator_node']:
                # The generator itself may lie in F_(p^2).  Every one of
                # its roots is nonzero precisely because the cleared
                # radicand is nonzero; no fake choice of Y is accepted.
                assert values[pole['coefficient_nodes_ascending'][0]] != 0
            else:
                assert values[guard] != 0, (p,n,h,signs,guard)
        checked+=1
    return {'prime':p,'input':n,'auxiliary_index':h,'actual_indices':indices,
            'characters_checked':checked,'point_coordinates':{name:hh.pair() for name,(hh,jj) in chart.items()},
            'all_original_and_added_guards_nonzero':True,
            'all_ordinate_signs':True,'pole_quadratic_checked_by_radicand':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('native_certificate.json'))
    args=parser.parse_args()
    path=args.repo/'computation/few_variables/derivative11_v63/specification/source.json'
    raw=path.read_bytes();source=json.loads(raw)
    assert source['retained_base_count']==10 and source['total_external_variables']==11
    assert [b['degree'] for b in source['finite_blocks']]==[4,4,4,2]
    records=[audit(source,p,n,h) for p in (1000000007,1000000009) for n,h in ((1,2),(-1,2),(2,3))]
    certificate={'status':'PASS','scope':'Exact finite reductions of actual rational point tuples and all 64 sign characters; no infinite existence or B=3 defining assertion.',
                 'source_sha256':hashlib.sha256(raw).hexdigest(),
                 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 'dag_nodes':len(source['coefficient_dag']),
                 'guard_count':len(source['guard_numerators']),
                 'actual_tuple_prime_pairs':len(records),'characters':sum(r['characters_checked'] for r in records),
                 'records':records,'variables':11,'finite_rank':128}
    args.output.write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({'status':'PASS','actual_tuple_prime_pairs':len(records),'characters':certificate['characters'],
                      'guards':certificate['guard_count'],'output':str(args.output)},indent=2))

if __name__=='__main__': main()
