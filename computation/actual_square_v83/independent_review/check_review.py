#!/usr/bin/env python3
"""Independent group-operation and fixture reconstruction for the eta241 note.

This uses PARI group operations, independently of the author's Fraction-based
chord-and-tangent implementation. Rank bounds use the same PARI descent.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json,sys
from sage.libs.pari import pari
from sympy import factorint

base=Path('/workspace/scratch/7ac4dd889cf6/v83_search25')
pins={
'deep_new_scalar_counterfamily.md':'ede15cd01c7e20bf6466cbb6da0a2b5d0d05647441440a92f83162dfced7c71c',
'check_deep_new_scalar_counterfamily.py':'74b957e37c0cd490f15e7c4d5b69443f256a7c761576fa931764dbed808e3ecd',
'deep_new_scalar_counterfamily.json':'136c867986936add4bfb0020fcd40109364297dbcc14a2fb500f7cadf8df1fc2'}
for name,h in pins.items():assert sha256((base/name).read_bytes()).hexdigest()==h
source=json.loads((base/'deep_new_scalar_counterfamily.json').read_text())
def rational(z):return F(str(z))
def sc(z):
 q=rational(z);assert q
 n=q.numerator*q.denominator;a=-1 if n<0 else 1
 for p,e in factorint(abs(n)).items():
  if e%2:a*=int(p)
 return a
N=3615
E=pari.ellinit([0,0,0,-N*N,0]);D=pari.ellinit([0,0,0,4*N*N,0])
ranks=[list(map(int,curve.ellrank()[:2])) for curve in [E,D]]
assert ranks==[[1,1],[1,1]]
assert int(E.elltors()[0])==4
R=pari([-441,75348]);tors=[[0],[0,0],[N,0],[-N,0]]
pts=[pari(v) for v in tors]+[E.elladd(R,v) for v in tors]
classes=[]
for Q in pts:
 if len(Q)==1:classes.append([1,1]);continue
 x=Q[0]
 classes.append([sc(x) if x else -1,sc(x-N) if x!=N else 2])
assert classes==source['kummer_classes'] and len(set(map(tuple,classes)))==8
assert sorted(set(a for a,b in classes))==[-N,-1,1,N]

S=pari.ellinit([0,-1890,0,848925,0]);P=pari(['5145/4','77175/8'])
reductions=[]
for p in [13,17]:
 Sp=pari.ellinit([0,-1890,0,848925,0],p)
 Pp=[int(pari.Mod(a,p)) for a in P]
 reductions.append({'prime':p,'curve_order':int(Sp.ellcard()),'point_order':int(Sp.ellorder(Pp))})
assert reductions==source['scalar_point_reductions']
Q=S.ellmul(P,18);x,y=map(rational,Q)
t=x/105;L=t*t-14*t+77;r=2*y/(1575*L)
d=28*t*(t-7)*(t-11)/(L*L)
q,c=F(-52729,6548),F(3769,6548)
V=q*r;e=4*d/(V*V);H=V*V+d
assert q*q+15==241*c*c
assert t>11 and 0<d<1 and 0<V<2 and 0<e<1
assert d==15*r*r and d*H==N*(r*r*c)**2
assert 1+d==((t*t-77)/L)**2
assert 49-28*d==(7*(t*t-22*t+77)/L)**2
fixture={name:str(v) for name,v in [('x',x),('y',y),('t',t),('r',r),('d',d),('q',q),('c',c),('V',V),('e',e),('H',H)]}
blob=(json.dumps(fixture,sort_keys=True,separators=(',',':'))+'\n').encode()
assert sha256(blob).hexdigest()==source['prepared_fixture']['full_exact_fixture_sha256']
assert len(blob)==source['prepared_fixture']['full_exact_fixture_canonical_json_bytes']
result={'status':'PASS','source_pins':pins,'independent_group_engine':'PARI elladd/ellmul; author used rational Fraction additions',
 'rank_bounds':ranks,'scalar_reductions':reductions,'kummer_classes':classes,
 'independent_Q18_fixture_sha256':sha256(blob).hexdigest(),
 'limitations':['Rank upper bounds use the same PARI algebraic descent implementation as the author.',
 'Universal local-depth and real-approximation arguments are reviewed separately in proof_review.md.',
 'No actual detector realization, external source-premise re-proof, or new variable bound is claimed.']}
out=Path(__file__).with_name('independent_reconstruction.json')
if '--write' in sys.argv:out.write_text(json.dumps(result,indent=2)+'\n')
else:assert json.loads(out.read_text())==result
print('PASS: independent Kummer additions, finite reductions and complete Q18 fixture')
