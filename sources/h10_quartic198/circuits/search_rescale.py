from pathlib import Path
import json,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
P=Path(__file__).parent;d=json.loads((P.parent/'source/computation/quartic/reciprocal204_v27/unbalanced-quadratic.json').read_text());coords={c['id']:c for c in d['coordinates']}
results=[]
for powers,removed_rows,scale_name in [({118:1,117:2},{60},'R'),({79:-1,80:1,81:2,82:4},{26,27,58},'q0'),({94:-1,95:1,96:2,97:4},{39,40,59},'q1')]:
 for maxkeep in ([1] if scale_name=='R' else [1,2]):
  retained=[i for i in coords if i not in powers];wids={i:j for j,i in enumerate(retained)};rows=[r for r in d['residuals'] if r['id'] not in removed_rows]
  cons=[];lo=[];hi=[]
  for rid,r in enumerate(rows):
   for t in r['terms']:
    q={};e=0;n=0
    for i in t['monomial']:
     if i in powers:e+=powers[i]
     else:q[wids[i]]=q.get(wids[i],0)+1;n+=1
    q[len(retained)+rid]=-1;cons.append(q);lo.append(-e);hi.append(maxkeep*(2-n)-e)
  mat=lil_matrix((len(cons),len(retained)+len(rows)))
  for row,q in enumerate(cons):
   for col,x in q.items():mat[row,col]=x
  lb=np.full(mat.shape[1],-200.);ub=np.full(mat.shape[1],200.)
  lb[wids[1]]=ub[wids[1]]=0
  res=milp(np.zeros(mat.shape[1]),integrality=np.ones(mat.shape[1]),bounds=Bounds(lb,ub),constraints=LinearConstraint(mat.tocsr(),np.array(lo),np.array(hi)),options={'time_limit':50})
  report=dict(base=scale_name,keep_through=maxkeep,status=res.message)
  if res.x is not None:report['weights']={str(i):int(round(res.x[k])) for i,k in wids.items() if abs(res.x[k])>.1}
  results.append(report);print(json.dumps(report),flush=True)
(P/'rescaling-search.json').write_text(json.dumps(results,indent=2)+'\n')
