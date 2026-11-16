#!/usr/bin/env python3
"""Reproduce the tangent fixtures and characteristic-zero rank certificates.

The manuscript supplies the monic normal-form lift and the product-closure
proof for restriction of scalars. This program uses exact integer arithmetic.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from itertools import combinations_with_replacement
import json
import argparse
import random
from pathlib import Path

@dataclass(frozen=True)
class K:
    a: F = F(0)
    b: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))
    @staticmethod
    def co(x): return x if isinstance(x, K) else K(x)
    def __add__(self, x):
        x=K.co(x); return K(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self): return K(-self.a,-self.b)
    def __sub__(self,x): return self+-K.co(x)
    def __rsub__(self,x): return K.co(x)+-self
    def __mul__(self,x):
        x=K.co(x); return K(self.a*x.a+2*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def inv(self):
        n=self.a*self.a-2*self.b*self.b
        assert n
        return K(self.a/n,-self.b/n)
    def __truediv__(self,x): return self*K.co(x).inv()
    def __rtruediv__(self,x): return K.co(x)*self.inv()
    def __pow__(self,n):
        if n<0: return self.inv()**(-n)
        r=K(1); x=self
        while n:
            if n&1: r=r*x
            x=x*x; n//=2
        return r
    def data(self): return [str(self.a),str(self.b)]
    def mod(self,p,rho):
        def f(q): return q.numerator*pow(q.denominator,-1,p)%p
        return (f(self.a)+rho*f(self.b))%p

rho=K(0,1)
e=-1+F(7,4)*rho
a=F(57,8)-F(7,2)*rho
c=-F(87,41)+F(129,164)*rho
D=(3-rho)**2
assert e*e==a and D==a*(a-c*c)

def double_point(P):
    x,y=P
    assert y != K(0)
    slope=(3*x*x-D)/(2*y)
    xx=slope*slope-2*x
    return xx,slope*(x-xx)-y

R0=(1+rho,2*rho)
assert R0[1]**2==R0[0]**3-D*R0[0]
P=double_point(R0)
assert P==(a,a*c)

def rows(vals,ref):
    FF,XX,LL,II,GG,YY,NN,JJ,aa,bb=vals
    r,q,S,T,u,w,v=ref
    return [
        II-(LL-1)**2,
        FF*XX+D*FF**2-r**2,
        (II+2*LL-1)*XX-(1-D*r**2),
        JJ-(NN-1)**2,
        GG*YY+D*GG**2-q**2,
        (JJ+2*NN-1)*YY-(1-D*q**2),
        aa*(XX+D*FF)-bb*(YY+D*GG),
        e*(w*bb-u*aa)-S*NN-T*LL,
    ]

# Project fixture H=U=R0, V=-R0, beta=L=N=1.
r=rho-1; q=r
S=4-2*rho; T=-S
# Reference recovery v-c-a*u=S, with u=v*r.
v=(S+c)/(1-a*r); u=v*r; w=u
ref=(r,q,S,T,u,w,v)
assert a*u*w==K(1) and v*(v-a*(u+w)-2*c)==D/a
assert r*S*S==1-D*r*r and q*T*T==1-D*q*q
FF=3-2*rho; XX=40*rho-56
vals=(FF,XX,K(1),K(0),FF,XX,K(1),K(0),K(0),K(0))
assert all(z==K(0) for z in rows(vals,ref))
assert a.a*2==F(57,4)

# A fixed generic reference H=2P for the quadratic-span calculation.
vg=(c*c-2*a)/(2*c)
rg=1/vg**2; qg=1/a
ug=1/vg; wg=vg/a
Sg=vg-c-a/vg; Tg=c
refg=(rg,qg,Sg,Tg,ug,wg,vg)
assert a*ug*wg==K(1)
assert vg*(vg-a*(ug+wg)-2*c)==D/a
assert rg*Sg*Sg==1-D*rg*rg
assert qg*Tg*Tg==1-D*qg*qg
fakeg=(rg/a,rg*c*c,Sg/c,(Sg/c-1)**2,
       qg/a,qg*c*c,K(-1),K(4),K(0),K(0))
assert all(z==K(0) for z in rows(fakeg,refg))
assert vg!=K(0) and Sg!=K(0)
H=double_point(P)
assert H[0]==vg*vg and H[1]/H[0]==Sg
fakeg_nonzero=list(fakeg)
LN=fakeg[2]*fakeg[6]
fakeg_nonzero[8]=e*wg*LN*(2*vg)
fakeg_nonzero[9]=e*ug*LN*(2*vg)
assert all(z==K(0) for z in rows(fakeg_nonzero,refg))
assert fakeg_nonzero[8]!=K(0) and fakeg_nonzero[9]!=K(0)
assert fakeg_nonzero[8]*fakeg_nonzero[9]/(LN*LN)==4*vg*vg

names=['F','X','L','I','G','Y','N','J','a1','a2']
mons=[()]+[(i,) for i in range(10)]+list(combinations_with_replacement(range(10),2))
index={m:i for i,m in enumerate(mons)}
assert len(mons)==66
p=1009; rt=439
assert all(p%d for d in range(2,32))
assert rt*rt%p==2
dd=D.mod(p,rt); ee=e.mod(p,rt)
rr,qq,ss,tt,uu,ww,vv=[z.mod(p,rt) for z in refg]
assert all([dd,ee,rr,qq,ss,tt,uu,ww,vv])

def rank_mod(mat):
    basis={}
    for row in mat:
        row=[x%p for x in row]
        while True:
            lead=next((i for i,x in enumerate(row) if x),None)
            if lead is None: break
            if lead not in basis:
                iv=pow(row[lead],-1,p)
                basis[lead]=[x*iv%p for x in row]
                break
            k=row[lead]; old=basis[lead]
            row=[(x-k*y)%p for x,y in zip(row,old)]
    return len(basis)

def mv(vals):
    out=[]
    for m in mons:
        z=1
        for i in m: z=z*vals[i]%p
        out.append(z)
    return out

# The seven proposed nonlinear rows, plus the original reciprocal chord
# row, and the linear coupling with all ten coordinate multiples, are
# universal true identities of degree <=2 after fixing the reference.
def pol(terms):
    out=[0]*66
    for k,v in terms.items(): out[index[tuple(sorted(k))]]=(out[index[tuple(sorted(k))]]+v)%p
    return out
known=[
 pol({(3,):1,(2,2):-1,(2,):2,():-1}),
 pol({(0,1):1,(0,0):dd,():-rr*rr}),
 pol({(3,1):1,(2,1):2,(1,):-1,():-1+dd*rr*rr}),
 pol({(7,):1,(6,6):-1,(6,):2,():-1}),
 pol({(4,5):1,(4,4):dd,():-qq*qq}),
 pol({(7,5):1,(6,5):2,(5,):-1,():-1+dd*qq*qq}),
 pol({(8,1):1,(8,0):dd,(9,5):-1,(9,4):-dd}),
 pol({(8,4):1,(8,0):-qq*pow(rr,-1,p),
      (0,6):-ee*ww*qq*pow(rr,-1,p)*ss,
      (0,2):-ee*ww*qq*pow(rr,-1,p)*tt}),
]
lin={(9,):ee*ww,(8,):-ee*uu,(6,):-ss,(2,):-tt}
known.append(pol(lin))
for i in range(10): known.append(pol({tuple(sorted(k+(i,))):v for k,v in lin.items()}))
knownrank=rank_mod(known)

squares={}
for z in range(1,p): squares.setdefault(z*z%p,[]).append(z)
pts=[]
for f in range(1,p):
    for s in squares.get((pow(f,-1,p)-dd*f)%p,[]): pts.append((f,s))
random.Random(47196).shuffle(pts)
evals=[]; witness=[]
for f,s in pts[:26]:
    for g,t in pts[26:52]:
        if g==f: continue
        LL=ss*pow(s,-1,p)%p; NN=tt*pow(t,-1,p)%p
        common=LL*NN*(s+t)*pow(g-f,-1,p)%p
        valsmod=[rr*f%p,rr*s*s%p,LL,(LL-1)**2%p,
                 qq*g%p,qq*t*t%p,NN,(NN-1)**2%p,
                 ee*ww*f*common%p,ee*uu*g*common%p]
        ev=mv(valsmod)
        assert all(sum(x*y for x,y in zip(ev,k))%p==0 for k in known)
        evals.append(ev); witness.append([f,s,g,t])
evalrank=rank_mod(evals)
fake_ev=mv([z.mod(p,rt) for z in fakeg])
assert all(sum(x*y for x,y in zip(fake_ev,k))%p==0 for k in known)
assert rank_mod(evals+[fake_ev])==evalrank
assert knownrank+evalrank==66,(knownrank,evalrank)

def rank_witness(mat):
    basis={}; chosen=[]; pivots=[]
    for i,row in enumerate(mat):
        row=[x%p for x in row]
        while True:
            lead=next((j for j,x in enumerate(row) if x),None)
            if lead is None:
                break
            if lead not in basis:
                iv=pow(row[lead],-1,p)
                basis[lead]=[x*iv%p for x in row]
                chosen.append(i);pivots.append(lead)
                break
            z=row[lead]
            row=[x-z*y for x,y in zip(row,basis[lead])]
            row=[x%p for x in row]
    return chosen,pivots

def det_mod(mat):
    mat=[list(row) for row in mat];det=1
    for j in range(len(mat)):
        k=next(i for i in range(j,len(mat)) if mat[i][j]%p)
        if k!=j:
            mat[j],mat[k]=mat[k],mat[j];det=-det
        piv=mat[j][j]%p;det=det*piv%p
        iv=pow(piv,-1,p)
        for i in range(j+1,len(mat)):
            z=mat[i][j]*iv%p
            mat[i]=[(x-z*y)%p for x,y in zip(mat[i],mat[j])]
    return det%p

chosen,columns=rank_witness(evals)
krows,kcols=rank_witness(known)
assert len(chosen)==47 and len(krows)==19
minor=[[evals[i][j] for j in columns] for i in chosen]
kminor=[[known[i][j] for j in kcols] for i in krows]
minor_det=det_mod(minor);known_det=det_mod(kminor)
assert minor_det and known_det
linear_rank=rank_mod([row[:11] for row in evals])
assert linear_rank==10

receipt={
 'status':'PASS',
 'exact_field':'Q(rho), rho^2=2',
 'constants':{n:z.data() for n,z in [('e',e),('a',a),('c',c),('D',D)]},
 'project_tangent_fixture':{
  'reference_H':'R0','numerator_U':'R0','numerator_V':'-R0',
  'beta':1,'coordinates':{n:z.data() for n,z in zip(names,vals)},
  'all_eight_rows_zero':True,'fake_trace':'0','true_trace':'57/4'},
 'nonzero_tangent_guard_failure':{
  'reference':'H=2P','U':'P','V':'-P','both_coupling_coordinates_nonzero':True,
  'fake_height_over_true_height':4,
  'coordinates':{n:z.data() for n,z in zip(names,fakeg_nonzero)}},
 'quadratic_span':{
  'reference':'H=2P; beta=1','variables':names,
  'monomial_count':66,'prime':p,'rho_residue':rt,
  'true_evaluation_rank':evalrank,'known_relation_rank':knownrank,
  'linear_evaluation_rank':linear_rank,
  'tested_secant_pairs':len(evals),
  'minor_sample_pairs':[witness[i] for i in chosen],
  'minor_columns':columns,'minor_determinant_mod_p':minor_det,
  'known_minor_rows':krows,'known_minor_columns':kcols,
  'known_minor_determinant_mod_p':known_det,
  'characteristic_zero_dimension':19,
  'lift':'Monic normal forms over the localization at (1009,rho-439); see manuscript.'},
 'restriction_of_scalars':{
  'rational_coordinates':20,
  'conjugate_component_quadrics_covered':True,
  'proof':'Degree-bounded zero closures commute with products; restriction of scalars splits into conjugate factors.'},
 'scope':{
  'complete_geometric_paired_chart':True,
  'additional_height_or_helper_coordinates':False,
  'different_coordinate_embeddings':False,
  'restricted_arithmetic_witness_families':False,
  'global_variable_count_lower_bound':False}
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
blob=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
if args.output:
    args.output.write_text(blob)
    print(json.dumps({'status':'PASS','output':str(args.output),'evaluation_rank':evalrank,'identity_rank':knownrank,'minor_determinants':[minor_det,known_det]}))
else:
    print(blob,end='')
