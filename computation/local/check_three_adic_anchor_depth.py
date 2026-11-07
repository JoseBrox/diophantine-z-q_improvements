#!/usr/bin/env python3
"""Exact local certificate for the three-adic physical-anchor depth.

Standard library only; no imports from a polynomial producer.  The
general valuation formula is proved in three_adic_anchor_depth.tex.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json

ZERO=(F(0),F(0))
ONE=(F(1),F(0))
D=(F(11),F(-6))
P=((F(57,8),F(-7,2)),(F(-165,8),F(417,32)))

def add(a,b): return a[0]+b[0],a[1]+b[1]
def neg(a): return -a[0],-a[1]
def sub(a,b): return add(a,neg(b))
def scale(a,c): return c*a[0],c*a[1]
def mul(a,b): return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def inv(a):
    n=a[0]*a[0]-2*a[1]*a[1]
    assert n
    return a[0]/n,-a[1]/n
def div(a,b): return mul(a,inv(b))
def vp_int(n,p=3):
    assert n
    n=abs(n);v=0
    while n%p==0: n//=p;v+=1
    return v
def vp(a):
    return None if not a else vp_int(a.numerator)-vp_int(a.denominator)
def valuation(a):
    vals=[vp(c) for c in a if c]
    assert vals
    return min(vals)
def on_curve(Q):
    if Q is None:return True
    x,y=Q
    return mul(y,y)==sub(mul(mul(x,x),x),mul(D,x))
def point_add(A,B):
    if A is None:return B
    if B is None:return A
    x,y=A;xx,yy=B
    if x==xx:
        if y==neg(yy):return None
        assert y==yy
        slope=div(sub(scale(mul(x,x),3),D),scale(y,2))
    else:slope=div(sub(yy,y),sub(xx,x))
    xxx=sub(sub(mul(slope,slope),x),xx)
    yyy=sub(mul(slope,sub(x,xxx)),y)
    Q=xxx,yyy
    assert on_curve(Q)
    return Q
def multiply(n,Q):
    if n<0:return multiply(-n,(Q[0],neg(Q[1])))
    R=None
    while n:
        if n&1:R=point_add(R,Q)
        n//=2
        if n:Q=point_add(Q,Q)
    return R
def residue(a):
    assert valuation(a)>=0
    return [(c.numerator*pow(c.denominator,-1,3))%3 for c in a]
def strings(a):return list(map(str,a))

def main():
    here=Path(__file__).resolve().parent
    assert all((t*t-2)%3 for t in range(3))
    assert on_curve(P)
    x,y=P
    assert residue(x)==[0,1] and residue(y)==[0,0]
    numerator=sub(scale(mul(x,x),3),D)
    slope=div(numerator,scale(y,2))
    Q=point_add(P,P)
    x2,y2=Q
    # Independent closed duplication formula for the abscissa.
    assert x2==div(mul(add(mul(x,x),D),add(mul(x,x),D)),scale(mul(y,y),4))
    z2=neg(div(x2,y2))
    f2=inv(x2)
    facts={'yP':valuation(y),'tangent_numerator':valuation(numerator),
           'slope':valuation(slope),'x2P':valuation(x2),'y2P':valuation(y2),
           'z2P':valuation(z2),'f2P':valuation(f2)}
    assert facts=={'yP':1,'tangent_numerator':0,'slope':-1,'x2P':-2,'y2P':-3,'z2P':1,'f2P':2}
    examples=[]
    for c in [-18,-6,-3,-2,-1,1,2,3,4,6,9,10,18]:
        Q=multiply(c,P)
        assert Q is not None and Q[0]!=ZERO
        f=inv(Q[0]);got=valuation(f)
        expected=0 if c%2 else 2+2*vp_int(c)
        assert got==expected,(c,got,expected)
        if c%2==0:
            assert valuation(neg(div(Q[0],Q[1])))==1+vp_int(c)
        examples.append({'index':c,'coefficient_valuations':[vp(v) for v in f],
                         'minimum':got})
    h=2093448;r=13208226;N=2*r+1
    comparisons=[(31867,1,50508,'>'),(15288,5**10,24207,'>'),
                 (15601,1,24727,'<'),(9779,5**10,15477,'<')]
    power_certificate=[]
    for exponent,multiplier,two_exponent,relation in comparisons:
        left=3**exponent;right=multiplier*2**two_exponent
        assert (left>right) if relation=='>' else (left<right)
        power_certificate.append({'three_exponent':exponent,'right_multiplier':multiplier,
                                  'two_exponent':two_exponent,'relation':relation,
                                  'left_bits':left.bit_length(),'right_bits':right.bit_length()})
    assert r==414*31867+15288
    assert 10*h+39==414*50508+24207
    assert r-1==846*15601+9779
    assert 10*h+39==846*24727+15477
    assert N==26416453 and 2*N==52832906 and 4*N==105665812
    proof=here/'three_adic_anchor_depth.tex'
    result={'status':'PASS','field':'Q(sqrt(2)), v3(3)=1',
            'local_values':facts,'point_reduction':{'x':[0,1],'y':[0,0]},
            'duplication_certificate':{'x2P':strings(x2),'y2P':strings(y2),
                                       'z2P':strings(z2),'f2P':strings(f2)},
            'examples':examples,
            'general_formula':'min(v3(a_c),v3(b_c))=0 for odd c; 2+2*v3(c) for nonzero even c',
            'minimal_exponent':'N=2*r+1 forces c even and v3(c)>=r; |c|>=2*3^r',
            'numerical_anchor':{'height_exponent_h':h,'smallest_r':r,'N':N,
                                'S_power_of_3':2*N,'64S_squared_power_of_3':4*N,
                                'power_comparisons':power_certificate,
                                'scope':'Minimal r for 2*3^r>(80*2^h)^10; not an optimization over every possible anchor construction.'},
            'proof_sha256':sha256(proof.read_bytes()).hexdigest(),
            'scope':'Exact local computations and displayed finite examples; the all-index statement follows from the written integral formal-group argument.'}
    (here/'three-adic-anchor-depth-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'local_values':facts,'examples':len(examples),
                      'proof_sha256':result['proof_sha256']},indent=2))

if __name__=='__main__':main()
