"""Restricted MILP screening with full residue classes and actual gate DAG.

No global optimality claim. Exact candidate compilation is a separate step.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
HERE=Path(__file__).resolve().parent
NAMES=['H','C2','C3','C4','F','C1','I','U1','U2','U3','U4','V0','V1','V2','V3','V4']

def screen(base,detectors,groupcounts=(3,4,5)):
 high,low,hreq=(12,3,6) if base==279 else (40,10,20)
 free_weights={1,2,4,8,2*low-1,4*low-2,2*high-1}
 # All new gate definitions are homogeneous binomial quadratic relations.
 dag={}
 def gate(e,a,b,op='+'):
  if e in free_weights or e in dag:return
  assert a in free_weights or a in dag,(e,a)
  assert b in free_weights or b in dag,(e,b)
  assert e==(a+b if op=='+' else a-b)
  dag[e]=(a,b,op)
 for e,a,b,op in [(3,2,1,'+'),(6,4,2,'+'),(7,8,1,'-'),(9,8,1,'+'),(12,8,4,'+'),(16,8,8,'+')]:gate(e,a,b,op)
 for center in [2*low-1,4*low-2,2*high-1]:
  gate(center-1,center,1,'-');gate(center+1,center,1,'+')
  prev=center
  for j in (1,2,3):
   current=2*prev;gate(current,prev,prev)
   for a in [1,2,3]:
    if current-a>0:gate(current-a,current,a,'-')
    gate(current+a,current,a,'+')
   prev=current
 allweights=sorted(free_weights|set(dag));M=32
 iseven={n:(n=='H' or n[0] in 'UV') for n in NAMES}
 target={n:(hreq if n=='H' else 2 if n[0] in 'UV' else low if n in ['C1','I'] else high) for n in NAMES}
 complete={n:(40 if n=='H' or n[0]=='U' else 2 if n[0]=='V' else (4 if base==279 else 12) if n=='C1' else 80 if n in ['I','F'] else high) for n in NAMES}
 # Maximum existing test-power exponent is2^freeb. V0 also has f itself.
 freeb={n:(1 if n not in ['V0','V1','V2','V3','V4'] else (2 if base==279 else 3) if n!='V1' else (1 if base==279 else 2)) for n in NAMES}
 for groups in groupcounts:
  choices=[]
  for i,n in enumerate(NAMES):
   for b in range(0 if n in ['H','V0'] else 1,5):
    L=2**b;mod=L*(2 if iseven[n] else 1)
    if mod>M:continue
    minimum=L*(target[n]-(2 if iseven[n] else 1))+1
    maximum=L*complete[n]-1
    for a in allweights:
     if minimum<=a<=maximum and a%mod:
      for g in range(groups):choices.append((i,g,b,a,mod))
  xcount=len(choices);zindex={a:xcount+j for j,a in enumerate(sorted(dag))};size=xcount+len(dag)
  rr=[];cc=[];vv=[];lo=[];hi=[]
  def row(items,lower=-np.inf,upper=np.inf):
   r=len(lo)
   for c,v in items:rr.append(r);cc.append(c);vv.append(v)
   lo.append(lower);hi.append(upper)
  bytest={i:[] for i in range(16)};byweight={a:[] for a in dag};bycell={(g,s):[] for g in range(groups) for s in range(M)}
  costs=np.zeros(size)
  for j,(i,g,b,a,mod) in enumerate(choices):
   n=NAMES[i];bytest[i].append(j)
   if a in dag:byweight[a].append(j)
   for s in range(a%mod,M,mod):bycell[g,s].append(j)
   costs[j]=2*max(0,b-freeb[n])-(2 if n=='H' and b==0 else 0)
  for i,js in bytest.items():row([(j,1) for j in js],1,1)
  for (g,s),js in bycell.items():
   if js:row([(j,1) for j in js],0,1)
  # Cost counts actual auxiliary weight gates in the fixed acyclic DAG.
  for a,js in byweight.items():
   for j in js:row([(j,1),(zindex[a],-1)],upper=0)
   for p in dag[a][:2]:
    if p in dag:row([(zindex[a],1),(zindex[p],-1)],upper=0)
   costs[zindex[a]]=detectors
  # Break factor permutation symmetry by requiring C2 in the first factor.
  row([(j,1) for j,c in enumerate(choices) if NAMES[c[0]]=='C2' and c[1]!=0],0,0)
  matrix=coo_matrix((vv,(rr,cc)),shape=(len(lo),size)).tocsr()
  res=milp(costs,integrality=np.ones(size),bounds=Bounds(0,1),constraints=LinearConstraint(matrix,lo,hi),options={'time_limit':70,'mip_rel_gap':0})
  if res.x is None:
   print(json.dumps({'base':base,'detectors':detectors,'groups':groups,'status':res.message}),flush=True);continue
  selected=[c for j,c in enumerate(choices) if res.x[j]>.5];activated=[a for a,j in zindex.items() if res.x[j]>.5]
  lists=[[{'test':NAMES[i],'power':2**b,'qPower':a,'modulus':mod,'residue':a%mod} for i,g,b,a,mod in selected if g==grp] for grp in range(groups)]
  variable=base+round(res.fun)+4*detectors*groups-(48 if base==279 else 58)
  output={'base':base,'detectors':detectors,'groups':groups,'candidateVariables':variable,'extraPowerAndWeightCost':round(res.fun),'factors':lists,'newWeights':{str(a):dag[a] for a in activated},'solverStatus':res.message,'mipGap':float(res.mip_gap),'claim':'Candidate circuit cost only; needs exact reconstruction and domain/valuation proof. No global optimality claim.'}
  (HERE/f'packing-{base}-{groups}groups.json').write_text(json.dumps(output,indent=2)+'\n')
  print(json.dumps(output),flush=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--base',type=int,choices=[279,322],required=True);p.add_argument('--groups',type=int,nargs='+',default=[3,4,5]);a=p.parse_args()
 screen(a.base,2 if a.base==279 else 3,a.groups)
