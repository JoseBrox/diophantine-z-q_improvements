#!/usr/bin/env python3
"""Exact rank certificate after adjoining the physical rational trace.

The two conjugate point pairs vary independently in the split model.
No random or numerical inference is used: nonzero minors certify ranks.
"""
import argparse
from itertools import combinations_with_replacement
from pathlib import Path
import random,json
p=1009;rho=439
assert all(p%d for d in range(2,32))

def frac(n,d=1):return n*pow(d,-1,p)%p

def constants(rt):
 e=(-1+frac(7,4)*rt)%p;a=e*e%p;c=(-frac(87,41)+frac(129,164)*rt)%p;D=(3-rt)**2%p
 v=(c*c-2*a)*pow(2*c,-1,p)%p;r=pow(v*v,-1,p);q=pow(a,-1,p);u=pow(v,-1,p);w=v*q%p;S=(v-c-a*u)%p;T=c
 return e,a,c,D,v,r,q,u,w,S,T

cs=[constants(rho),constants(-rho%p)]

def points(c):
 D=c[3];sq={}
 for s in range(1,p):sq.setdefault(s*s%p,[]).append(s)
 return [(f,s) for f in range(1,p) for s in sq.get((pow(f,-1,p)-D*f)%p,[])]
ps=[points(c) for c in cs]

def chart(c,data):
 e,a,c0,D,v,r,q,u,w,S,T=c;f,s,g,t=data
 L=S*pow(s,-1,p)%p;N=T*pow(t,-1,p)%p
 C=L*N*(s+t)*pow(g-f,-1,p)%p
 z=[r*f%p,r*s*s%p,L,(L-1)**2%p,q*g%p,q*t*t%p,N,(N-1)**2%p,e*w*f*C%p,e*u*g*C%p]
 h=f*g*(s+t)**2*pow(g-f,-2,p)%p
 return z,h

mons=[()]+[(i,) for i in range(21)]+list(combinations_with_replacement(range(21),2));index={m:i for i,m in enumerate(mons)}

def vec(z):
 row=[]
 for m in mons:
  a=1
  for i in m:a=a*z[i]%p
  row.append(a)
 return row

def pol(terms):
 row=[0]*253
 for m,c in terms.items():row[index[tuple(sorted(m))]]=(row[index[tuple(sorted(m))]]+c)%p
 return row

def identities(c,off):
 e,a,c0,D,v,r,q,u,w,S,T=c
 F,X,L,I,G,Y,N,J,A,B=[i+off for i in range(10)]
 nonlin=[{(I,):1,(L,L):-1,(L,):2,():-1},
 {(F,X):1,(F,F):D,():-r*r},
 {(I,X):1,(L,X):2,(X,):-1,():-1+D*r*r},
 {(J,):1,(N,N):-1,(N,):2,():-1},
 {(G,Y):1,(G,G):D,():-q*q},
 {(J,Y):1,(N,Y):2,(Y,):-1,():-1+D*q*q},
 {(A,X):1,(A,F):D,(B,Y):-1,(B,G):-D},
 {(A,G):1,(A,F):-q*pow(r,-1,p),(F,N):-e*w*q*pow(r,-1,p)*S,(F,L):-e*w*q*pow(r,-1,p)*T}]
 lin={(B,):e*w,(A,):-e*u,(N,):-S,(L,):-T}
 rows=[pol(row) for row in nonlin]+[pol(lin)]
 rows +=[pol({tuple(sorted(m+(i,))):coef for m,coef in lin.items()}) for i in range(21)]
 return rows
known=identities(cs[0],0)+identities(cs[1],10)
class Basis:
 def __init__(self):self.b={};self.selected=[];self.columns=[]
 def add(self,row,label=None):
  row=list(row)
  while True:
   i=next((i for i,x in enumerate(row) if x%p),None)
   if i is None:return False
   if i not in self.b:
    iv=pow(row[i],-1,p);self.b[i]=[x*iv%p for x in row];self.selected.append(label);self.columns.append(i);return True
   z=row[i]%p;old=self.b[i];row=[(x-z*y)%p for x,y in zip(row,old)]
 def rank(self):return len(self.b)
k=Basis()
for i,row in enumerate(known):k.add(row,i)
assert k.rank()==59
b=Basis();rng=random.Random(480194);evaluations=[]
for it in range(1500):
 data=[];zs=[];hh=0
 for pp,c in zip(ps,cs):
  while True:
   f,s=rng.choice(pp);g,t=rng.choice(pp)
   if g!=f:break
  d=[f,s,g,t];z,h=chart(c,d);data+=d;zs+=z;hh+=h
 row=vec(zs+[hh%p])
 assert all(sum(a*b for a,b in zip(row,k))%p==0 for k in known)
 if b.add(row,data):evaluations.append(row)
 if b.rank()==253-k.rank():break

assert b.rank()==194

def det_mod(mat):
 mat=[list(row) for row in mat];det=1
 for j in range(len(mat)):
  z=next(i for i in range(j,len(mat)) if mat[i][j]%p)
  if z!=j:mat[j],mat[z]=mat[z],mat[j];det=-det
  val=mat[j][j]%p;det=det*val%p;iv=pow(val,-1,p)
  for i in range(j+1,len(mat)):
   c=mat[i][j]*iv%p
   mat[i]=[(x-c*y)%p for x,y in zip(mat[i],mat[j])]
 return det%p

minor=[[row[j] for j in b.columns] for row in evaluations]
kminor=[[known[i][j] for j in k.columns] for i in k.selected]
det=det_mod(minor);kdet=det_mod(kminor)
assert det and kdet
receipt={
 'status':'PASS','prime':p,'rho_residue':rho,
 'coordinates':'two split ten-coordinate point pairs and T=h_plus+h_minus',
 'height_function':'h=f*g*(s+t)^2/(g-f)^2',
 'rational_coordinate_count':21,'monomial_count':253,
 'secant_evaluation_rank':194,'known_identity_rank':59,
 'independent_parameter_rows':b.selected,'evaluation_minor_columns':b.columns,
 'evaluation_minor_determinant_mod_p':det,
 'identity_minor_rows':k.selected,'identity_minor_columns':k.columns,
 'identity_minor_determinant_mod_p':kdet,
 'identities':'Eight nonlinear generators and one linear generator in each split factor, together with all21 coordinate multiples of each linear generator; one dependence gives59.',
 'characteristic_zero_lift':'The Laurent algebra of four monic quadratic curve equations is free of rank16; see manuscript.',
 'false_family':'Opposite points U=P,V=-P in each conjugate factor, arbitrary coupling parameter and arbitrary rational T.',
 'scope':'The same coordinate embedding with the physical trace alone; different embeddings, genuinely new helpers, or restricted arithmetic witness families are excluded.'}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
blob=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
if args.output:
 args.output.write_text(blob)
 print(json.dumps({'status':'PASS','evaluation_rank':194,'identity_rank':59,'minors':[det,kdet],'output':str(args.output)}))
else:print(blob,end='')
