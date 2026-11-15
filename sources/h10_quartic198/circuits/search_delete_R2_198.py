from pathlib import Path
import json,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
P=Path(__file__).parent;d=json.loads((P/'inverse198/quadratic.json').read_text());coords={c['id']:c for c in d['coordinates']};ids={c['formalId']:c['id'] for c in d['coordinates']};R=ids[118];R2=ids[117];removed={R2};rows=[r for r in d['residuals'] if r['name'] not in('scalar.r_power_2.definition','inverse_vieta.unweighted.aggregate')]
retained=[i for i in coords if i not in(R,R2)];wids={i:j for j,i in enumerate(retained)};cons=[];lo=[];hi=[]
for rid,r in enumerate(rows):
 for t in r['terms']:
  q={};e=0;n=0
  for i in t['monomial']:
   if i==R:e+=1
   elif i==R2:e+=2
   else:q[wids[i]]=q.get(wids[i],0)+1;n+=1
  q[len(retained)+rid]=-1;cons.append(q);lo.append(-e);hi.append(2-n-e)
mat=lil_matrix((len(cons),len(retained)+len(rows)))
for row,q in enumerate(cons):
 for col,x in q.items():mat[row,col]=x
lb=np.full(mat.shape[1],-100.);ub=np.full(mat.shape[1],100.);lb[wids[1]]=ub[wids[1]]=0
res=milp(np.zeros(mat.shape[1]),integrality=np.ones(mat.shape[1]),bounds=Bounds(lb,ub),constraints=LinearConstraint(mat.tocsr(),np.array(lo),np.array(hi)),options={'time_limit':50})
report=dict(status=res.message)
if res.x is not None:report['weights']={str(coords[i]['formalId']):int(round(res.x[k])) for i,k in wids.items() if abs(res.x[k])>.1}
print(json.dumps(report,indent=2));(P/'delete-R2-198-search.json').write_text(json.dumps(report,indent=2)+'\n')
