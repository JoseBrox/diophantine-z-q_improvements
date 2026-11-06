if not __debug__:
    raise RuntimeError('Run without -O; assertions are part of validation.')

"""Small exact checks for the original seven-witness predicate; stdlib only."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import argparse
import json

HERE=Path(__file__).resolve().parent
PACKAGE=HERE.parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
PRIMES=[2,3,5,7,11,13,17]

def local_signature(n):
    out=[]
    for p in [2,3,17]:
        u=n;v=0
        while u%p==0:u//=p;v+=1
        out.append(v%2)
        if p==2:out.extend({1:(0,0),3:(1,1),5:(0,1),7:(1,0)}[u%8])
        else:out.append(int(pow(u%p,(p-1)//2,p)==p-1))
    return tuple(out)

columns=[local_signature(p) for p in PRIMES]
matrix=[list(row) for row in zip(*columns)]
expected=[[1,0,0,0,0,0,0],[0,1,0,1,1,0,0],[0,1,1,0,1,1,0],
          [0,1,0,0,0,0,0],[1,0,1,0,1,0,1],[0,0,0,0,0,0,1],
          [0,1,1,1,1,0,0]]
assert matrix==expected
signatures={}
products=[]
for bits in product([0,1],repeat=7):
    mu=1
    for p,b in zip(PRIMES,bits):mu*=p**b
    sig=local_signature(mu)
    assert sig==tuple(sum(b*c[i] for b,c in zip(bits,columns))%2 for i in range(7))
    assert sig not in signatures
    signatures[sig]=mu
    e=dict(zip(PRIMES,bits))
    for sign in [0,1]:
        A=(1+e[2])*(1+2*e[3])*(1+12*e[13])*(1+16*e[17])
        B=(1+4*e[5])*(1+6*e[7])*(1+10*e[11])*(1-2*sign)
        assert A*B==(-1)**sign*mu!=0
        products.append(A*B)
assert len(signatures)==128 and len(set(products))==256
# Check every possible local signature, with each prescribed real sign.
for sig,representative in signatures.items():
    for sign in [1,-1]:
        r=sign*representative;delta=sign
        mu=signatures[local_signature(delta*r)]
        assert delta*mu*r>0 and local_signature(delta*mu*r)==(0,)*7

def add(*polys):
    d=Counter()
    for p in polys:
        for m,c in p.items():d[m]+=c
    return {m:c for m,c in d.items() if c}
def scale(c,p):return {m:c*v for m,v in p.items() if c*v}
def mul(*polys):
    ans={():1}
    for p in polys:
        out=Counter()
        for m,a in ans.items():
            for n,b in p.items():out[tuple(sorted(m+n))]+=a*b
        ans={m:c for m,c in out.items() if c}
    return ans
def sub(a,b):return add(a,scale(-1,b))
def sq(a):return mul(a,a)
one={():1}
b,t,U,e,p,q,s,h=[{(i,):1} for i in range(8)]
B=scale(17,b)
r1=sub(mul(U,add(one,mul(b,sq(t)))),mul(b,sub(one,mul(b,sq(t)))))
r2=sub(sq(p),mul(B,sub(one,e),add(one,scale(3,e))))
r3=sub(h,mul(e,sub(B,sq(U))))
r4=sub(mul(B,sq(q)),mul(sub(sq(s),mul(B,h)),add(sq(s),scale(3,mul(B,h)))))
sos=add(*[sq(row) for row in [r1,r2,r3,r4]])
assert len(sos)==30 and max(map(len,sos))==8
# Verify the exact source rescaling, after eliminating h by its own equation.
eold=mul(B,e);pold=mul(B,p);qold=mul(B,q)
old2=sub(sq(pold),mul(B,sub(B,eold),add(B,scale(3,eold))))
assert old2==mul(sq(B),r2)
H=mul(e,sub(B,sq(U)))
new4=sub(mul(B,sq(q)),mul(sub(sq(s),mul(B,H)),add(sq(s),scale(3,mul(B,H)))))
old3=sub(sq(qold),mul(B,sub(sq(s),mul(eold,sub(B,sq(U)))),add(sq(s),scale(3,mul(eold,sub(B,sq(U)))))))
assert old3==mul(B,new4)

module=json.loads((PACKAGE/'modules/q_primeparity.json').read_bytes())
assert module['free']==1 and module['locals']==7 and not module['calls']
assert [{tuple(m):c for c,m in row} for row in module['residuals']]==[r1,r2,r3,r4]
paths=[PACKAGE/'modules/q_primeparity.json',PACKAGE/'source/archive_build.py',
       PACKAGE/'source/article/short-scalar-parity.tex',HERE/'parity-justification.tex']
report={'status':'pass','literal_four_residuals_checked':True,'squareclass_matrix':matrix,'local_signatures':len(signatures),
        'signed_boolean_products':len(set(products)),
        'all_local_classes_correctable_with_each_real_sign':True,
        'psi_sum_of_squares_monomials':len(sos),'psi_total_degree':max(map(len,sos)),
        'exact_source_rescaling':'old R2 = B^2 new R2; old R3 = B new R4 after h=e(B-U^2)',
        'source_sha256':{p.relative_to(PACKAGE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
