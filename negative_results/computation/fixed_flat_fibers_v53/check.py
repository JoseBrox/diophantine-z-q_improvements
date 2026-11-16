#!/usr/bin/env python3
"""Independently verify the fixed-fiber certificate using the standard library.

No polynomial factorization package is used. Explicit modular coefficient
vectors and Euclidean Bezout identities certify the two decisive gcd claims.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
parser.add_argument('--repo',type=Path)
args=parser.parse_args()
data=json.loads(args.certificate.read_text())

def trim(f,p):
    out=[int(c)%p for c in f]
    while len(out)>1 and out[-1]==0:out.pop()
    return out or[0]
def add(f,g,p):
    out=[0]*max(len(f),len(g))
    for i,c in enumerate(f):out[i]+=c
    for i,c in enumerate(g):out[i]+=c
    return trim(out,p)
def neg(f,p):return trim([-c for c in f],p)
def sub(f,g,p):return add(f,neg(g,p),p)
def scale(f,c,p):return trim([c*x for x in f],p)
def mul(f,g,p):
    out=[0]*(len(f)+len(g)-1)
    for i,c in enumerate(f):
        for j,d in enumerate(g):out[i+j]=(out[i+j]+c*d)%p
    return trim(out,p)
def power(f,n,p):
    out=[1]
    while n:
        if n&1:out=mul(out,f,p)
        f=mul(f,f,p);n//=2
    return out
def frac(x,p):
    x=Q(x)
    return x.numerator*pow(x.denominator,-1,p)%p
def reduce_pair(x,s,p):return(frac(x[0],p)+s*frac(x[1],p))%p
def ecadd(P,R,D,p):
    if P is None:return R
    if R is None:return P
    x,y=P;u,v=R
    if x==u and(y+v)%p==0:return None
    numerator,denominator=(3*x*x-D,2*y) if x==u else(v-y,u-x)
    slope=numerator*pow(denominator,-1,p)%p
    xx=(slope*slope-x-u)%p
    return xx,(slope*(x-xx)-y)%p
def ecmul(n,P,D,p):
    out=None
    while n:
        if n&1:out=ecadd(out,P,D,p)
        P=ecadd(P,P,D,p);n//=2
    return out

summaries=[]
for record in data['records']:
    p=record['prime'];s=record['sqrt2_mod_prime'];X=record['input']
    assert p>7 and all(p%d for d in range(2,isqrt(p)+1))
    assert s*s%p==2
    assert record['auxiliary_index']==3 and record['coefficient_shift']==3
    assert record['height_exponent']==4 and X in(1,2)
    local=[]
    for sigma in(1,-1):
        rr=sigma*s%p;Dcurve=(11-6*rr)%p
        P=((57-28*rr)*pow(8,-1,p)%p,(-660+417*rr)*pow(32,-1,p)%p)
        pts={name:ecmul(index,P,Dcurve,p) for name,index in{
             'P':1,'A':X,'H':3,'U':3*X,'H_minus_P':2,'U_minus_A':2*X}.items()}
        for name,Z in pts.items():
            assert Z is not None and Z[0] and Z[1]
            assert (Z[1]**2-Z[0]**3+Dcurve*Z[0])%p==0
            given=record['source_points'][name]
            assert tuple(reduce_pair(coord,rr,p) for coord in given)==Z
        A,H,U,Hm,Um=(pts[name] for name in('A','H','U','H_minus_P','U_minus_A'))
        assert H[0]!=P[0] and U[0]!=A[0]
        z=lambda Z:-Z[0]*pow(Z[1],-1,p)%p
        local.append({'fH':pow(H[0],-1,p),'fU':pow(U[0],-1,p),
                      'fHm':pow(Hm[0],-1,p),'fUm':pow(Um[0],-1,p),
                      'r':z(U)*pow(z(H),-1,p)%p,
                      's':z(Um)*pow(z(Hm),-1,p)%p,'xA':A[0]})
    rows=[]
    for i in(0,1):
        L=local[i];C=local[1-i]
        last=(L['r']+C['s']-2*X)%p if record['comparison']=='symmetric' else(L['r']-X)%p
        rows.append([L['fH'],L['fU'],C['fHm'],C['fUm'],(L['r']-C['s'])%p,last])
    assert rows==record['tests_mod_prime']
    for i,rr in enumerate((s,-s%p)):
        assert [reduce_pair(c,rr,p) for c in record['actual_tests_in_Qsqrt2']]==rows[i]
    a=(pow(X*X+3,4,p)+pow((local[0]['xA']+local[1]['xA'])%p,4,p))%p
    assert a==record['scale_mod_prime']==frac(record['actual_scale'],p)
    assert a not in(0,1)
    active=[i-1 for i in record['active_test_indices']]
    assert active==[i for i,c in enumerate(record['actual_tests_in_Qsqrt2']) if any(Q(z) for z in c)]
    assert len(active)==(4 if X==1 else 6)
    assert all(row[i] for row in rows for i in active)
    F=[1]
    for c in[Q(0),Q(1,2),Q(1,4),Q(2,5),Q(1),Q(1,3)]:F=mul(F,[frac(c,p),1],p)
    E=scale(power([-1,1],8,p),4,p);G=add(E,F,p)
    Den=power(F,len(active),p)
    PP=[]
    for row in rows:
        value=[1]
        for i in active:value=mul(value,add(F,[row[i]**2],p),p)
        PP.append(value)
    plus,minus=PP
    LP=sub(mul(G,plus,p),mul(E,Den,p),p)
    LM=sub(mul(G,minus,p),mul(E,Den,p),p)
    MM=sub(scale(mul(mul(G,plus,p),minus,p),2,p),mul(mul(E,Den,p),add(plus,minus,p),p),p)
    f=scale(mul(mul(mul(F,LP,p),LM,p),MM,p),2,p)
    fs=trim([c*pow(a,i,p) for i,c in enumerate(f)],p)
    expected={'F':F,'E':E,'G':G,'D':Den,'P_plus':plus,'P_minus':minus,
              'L_plus':LP,'L_minus':LM,'M':MM,'f':f,'f_scaled':fs}
    assert expected==record['polynomials_mod_prime']
    degree=24*len(active)+24
    assert len(f)-1==degree==record['degree'] and f[-1]==4
    derivative=trim([i*f[i] for i in range(1,len(f))],p)
    b=record['squarefree_bezout']
    assert add(mul(b['coefficient_of_f'],f,p),mul(b['coefficient_of_derivative'],derivative,p),p)==[1]
    assert f[0]==fs[0]==0 and f[1] and fs[1]
    b=record['scaled_gcd_bezout']
    assert add(mul(b['coefficient_of_f_div_t'],f[1:],p),
               mul(b['coefficient_of_scaled_div_t'],fs[1:],p),p)==[1]
    assert record['characteristic_zero_branch_gcd']=='t'
    assert record['one_cover_genus']==(degree-2)//2
    assert record['simultaneous_cover_genus']==2*degree-4
    assert record['rational_points_above_infinity']==4
    summaries.append({'X':X,'comparison':record['comparison'],'prime':p,
                      'branch_degree':degree,'fiber_genus':2*degree-4})

if args.repo:
    repo=args.repo
else:
    candidates=[]
    for ancestor in(HERE,*HERE.parents):candidates.extend((ancestor,ancestor/'research-repo'))
    first=next(iter(data['source_sha256']))
    repo=next(p for p in candidates if(p/first).is_file())
for name,digest in data['source_sha256'].items():assert sha256((repo/name).read_bytes()).hexdigest()==digest
print(json.dumps({'status':'PASS','records':summaries,
                  'scope':'Specified fixed fibers only; no rational-point nonexistence or 21/9 completeness claim.'},indent=2))
