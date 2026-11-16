#!/usr/bin/env python3
"""Generate exact fixed-fiber certificates; the checker needs no SymPy."""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
import argparse
import json
import sympy as S

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
parser.add_argument('--repo',type=Path)
args=parser.parse_args()
t=S.symbols('t')
ZERO=(Q(0),Q(0))
ONE=(Q(1),Q(0))
D=(Q(11),Q(-6))
P=((Q(57,8),Q(-7,2)),(Q(-165,8),Q(417,32)))

def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def mul(a,b):return(a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c):return(a[0]*c,a[1]*c)
def inv(a):
    n=a[0]**2-2*a[1]**2
    return(a[0]/n,-a[1]/n)
def div(a,b):return mul(a,inv(b))
def bar(a):return(a[0],-a[1])
def ecadd(A,B):
    if A is None:return B
    if B is None:return A
    x,y=A;u,v=B
    if x==u and add(y,v)==ZERO:return None
    m=div(sub(scale(mul(x,x),3),D),scale(y,2)) if x==u else div(sub(v,y),sub(u,x))
    z=sub(sub(mul(m,m),x),u)
    return(z,sub(mul(m,sub(x,z)),y))
def ecmul(n,A):
    R=None
    while n:
        if n&1:R=ecadd(R,A)
        A=ecadd(A,A);n//=2
    return R
def oncurve(A):
    x,y=A
    return mul(y,y)==sub(mul(mul(x,x),x),mul(D,x))
def fieldstr(a):return[str(c) for c in a]
def pointstr(A):return[fieldstr(a) for a in A]
def fp(q,p):return q.numerator*pow(q.denominator,-1,p)%p
def reduce(a,p,s):return(fp(a[0],p)+s*fp(a[1],p))%p
def vector(f,p):return[int(f.nth(i))%p for i in range(f.degree()+1)]
def poly(expr,p):return S.Poly(expr,t,modulus=p)

def source(X,symmetric):
    A=ecmul(X,P);H=ecmul(3,P);U=ecmul(3*X,P)
    Hm=ecmul(2,P);Um=ecmul(2*X,P)
    assert all(oncurve(Z) and Z[0]!=ZERO and Z[1]!=ZERO for Z in(P,A,H,U,Hm,Um))
    assert H[0]!=P[0] and U[0]!=A[0]
    f=lambda Z:inv(Z[0])
    z=lambda Z:neg(div(Z[0],Z[1]))
    r=div(z(U),z(H));s=div(z(Um),z(Hm))
    tests=[f(H),f(U),bar(f(Hm)),bar(f(Um)),sub(r,bar(s))]
    tests.append(sub(add(r,bar(s)),(Q(2*X),Q(0))) if symmetric else sub(r,(Q(X),Q(0))))
    a=Q((X*X+3)**4)+(2*A[0][0])**4
    return tests,a,{'P':pointstr(P),'A':pointstr(A),'H':pointstr(H),'U':pointstr(U),
                    'H_minus_P':pointstr(Hm),'U_minus_A':pointstr(Um)}

def certificate(X,symmetric,p):
    cs,a,points=source(X,symmetric)
    roots=S.sqrt_mod(2,p,all_roots=True)
    s=int(roots[0]);amod=fp(a,p)
    assert amod not in(0,1)
    rows=[[reduce(c,p,sigma*s%p) for c in cs] for sigma in(1,-1)]
    active=[i for i,c in enumerate(cs) if c!=ZERO]
    assert all(row[i] for row in rows for i in active)
    assert len(active)==(4 if X==1 else 6)
    F=poly(1,p)
    for c in[Q(0),Q(1,2),Q(1,4),Q(2,5),Q(1),Q(1,3)]:F*=poly(t+fp(c,p),p)
    E=poly(4*(t-1)**8,p);G=E+F
    Den=F**len(active)
    polynomials=[]
    for row in rows:
        PP=poly(1,p)
        for i in active:PP*=F+poly(row[i]**2,p)
        polynomials.append(PP)
    PP,PM=polynomials
    LP=G*PP-E*Den;LM=G*PM-E*Den
    MM=2*G*PP*PM-E*Den*(PP+PM)
    f=2*F*LP*LM*MM
    n=f.degree()
    assert n==24*len(active)+24 and int(f.LC())%p==4
    s0,t0,gcd0=S.gcdex(f,f.diff())
    assert gcd0==poly(1,p) and s0*f+t0*f.diff()==poly(1,p)
    scaled=poly(sum(int(c)*pow(amod,i,p)*t**i for(i,),c in f.terms()),p)
    lin=poly(t,p)
    fdiv=f.exquo(lin);sdiv=scaled.exquo(lin)
    s1,t1,gcd1=S.gcdex(fdiv,sdiv)
    assert gcd1==poly(1,p) and s1*fdiv+t1*sdiv==poly(1,p)
    assert S.gcd(f,scaled).monic()==lin
    return{
      'input':X,'auxiliary_index':3,'coefficient_shift':3,'height_exponent':4,
      'comparison':'symmetric' if symmetric else 'original',
      'prime':p,'sqrt2_mod_prime':s,'source_points':points,
      'actual_tests_in_Qsqrt2':[fieldstr(c) for c in cs],
      'actual_scale':str(a),'scale_mod_prime':amod,'tests_mod_prime':rows,
      'active_test_indices':[i+1 for i in active],
      'polynomials_mod_prime':{name:vector(value,p) for name,value in{
           'F':F,'E':E,'G':G,'D':Den,'P_plus':PP,'P_minus':PM,
           'L_plus':LP,'L_minus':LM,'M':MM,'f':f,'f_scaled':scaled}.items()},
      'squarefree_bezout':{'coefficient_of_f':vector(s0,p),'coefficient_of_derivative':vector(t0,p),
                          'identity':'s*f+t*f_prime=1'},
      'scaled_gcd_bezout':{'coefficient_of_f_div_t':vector(s1,p),'coefficient_of_scaled_div_t':vector(t1,p),
                          'identity':'s*(f/t)+t_coefficient*(f_scaled/t)=1'},
      'degree':n,'leading_coefficient':4,'characteristic_zero_branch_gcd':'t',
      'one_cover_genus':(n-2)//2,'simultaneous_cover_genus':2*n-4,
      'rational_points_above_infinity':4}

source_names=['papers/conditional_few_variables/direct_input13_20261110_v22.tex',
              'papers/finite_algebra/unit_norm_20261114_v28.tex']
candidates=[]
for ancestor in(HERE,*HERE.parents):candidates.extend((ancestor,ancestor/'research-repo'))
repo=args.repo or next(p for p in candidates if(p/source_names[0]).is_file())
data={'schema':'actual-fast-detector-fixed-fibers/v53','status':'PASS',
      'scope':'Exact characteristic-zero genera for four specified actual fixed fibers; no rational-point nonexistence or global realization assertion.',
      'source_sha256':{name:sha256((repo/name).read_bytes()).hexdigest() for name in source_names},
      'records':[certificate(1,False,97),certificate(1,True,97),certificate(2,False,97),certificate(2,True,241)]}
content=(json.dumps(data,indent=2)+'\n').encode()
if args.output is None:
    if (HERE/'certificate.json').read_bytes()!=content:
        raise ValueError('Reconstructed fixed-fiber certificate differs.')
else:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(content)
print(json.dumps({'status':'PASS','records':len(data['records']),
                  'degrees':[r['degree'] for r in data['records']],
                  'genera':[r['simultaneous_cover_genus'] for r in data['records']]}))
