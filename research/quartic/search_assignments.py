import json
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from pathlib import Path
names=['H','C2','C3','C4','F','C1','I','U1','U2','U3','U4','V0','V1','V2','V3','V4']
orders=[40]*5+[10]*2+[1]*9
free=[0]*11+[2,1,2,2,2]
L=7
keys=[('x',i,j) for i in range(16) for j in range(L)]+[('q',o,j) for o in [1,10,40] for j in range(L)]
ix={k:i for i,k in enumerate(keys)}
rows=[]; lows=[]; highs=[]
def cons(items,lo=-np.inf,hi=np.inf):
 r=np.zeros(len(keys))
 for k,v in items:r[ix[k]]+=v
 rows.append(r);lows.append(lo);highs.append(hi)
for i in range(16):cons([(('x',i,j),1) for j in range(L)],1,1)
for j in range(1,L):cons([(('x',i,j-1),1) for i in range(16)]+[(('x',i,j),-1) for i in range(16)],0)
for i in range(16):
 for j in range(L):cons([(('q',orders[i],j),1),(('x',i,j),-1)],0)
for o in [1,10,40]:
 for j in range(1,L):cons([(('q',o,j-1),1),(('q',o,j),-1)],0)
for detectors in [2,3]:
 c=np.zeros(len(keys))
 for i in range(16):
  for j in range(L):c[ix['x',i,j]]=2*max(0,j-free[i])+(4*detectors if j==0 else 0)
 for o in [1,10,40]:
  for j in range(L):c[ix['q',o,j]]=detectors if j>{1:2,10:1,40:0}[o] else 0
 res=milp(c,integrality=np.ones(len(keys)),bounds=Bounds(0,1),constraints=LinearConstraint(np.array(rows),lows,highs),options={'time_limit':60,'mip_rel_gap':0})
 assert res.success, res.message
 levels=[[names[i] for i in range(16) if res.x[ix['x',i,j]]>.5] for j in range(L)]
 groups=[[lev[k] for lev in levels if k<len(lev)] for k in range(len(levels[0]))]
 powercost=sum(2*max(0,j-free[i]) for i in range(16) for j in range(L) if res.x[ix['x',i,j]]>.5)
 weightcost=sum(c[ix['q',o,j]] for o in [1,10,40] for j in range(L) if res.x[ix['q',o,j]]>.5)
 out={'detectors':detectors,'objective':round(res.fun),'groups':groups,'new_field_coordinates':powercost,'new_weight_coordinates':int(weightcost),'solver_status':res.message,'gap':res.mip_gap}
 print(json.dumps(out,indent=2))
 Path(f'work/quartic/assignment{detectors}.json').write_text(json.dumps(out,indent=2)+'\n')
