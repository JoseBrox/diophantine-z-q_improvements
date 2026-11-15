from pathlib import Path
import json,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
P=Path(__file__).parent;d=json.loads((P/'affine200/quadratic.json').read_text());coords={c['id']:c for c in d['coordinates']};oid={c['source204Id']:c['id'] for c in d['coordinates'] if 'source204Id' in c};R=oid[118];R2=oid[117]
removed={oid[x] for x in [2,3]+list(range(155,169))};removed_rows=set(range(104,122))|set(range(140,145))
retained=[i for i in coords if i not in removed|{R,R2}];wids={i:j for j,i in enumerate(retained)};rows=[r for r in d['residuals'] if r.get('source204RowId') not in removed_rows]
cons=[];lo=[];hi=[]
for rid,r in enumerate(rows):
 for t in r['terms']:
  q={};e=0;n=0
  for i in t['monomial']:
   if i==R:e+=1
   elif i==R2:e+=2
   else:q[wids[i]]=q.get(wids[i],0)+1;n+=1
  q[len(retained)+rid]=-1;cons.append(q);lo.append(-e);hi.append(2*(2-n)-e)
mat=lil_matrix((len(cons),len(retained)+len(rows)))
for row,q in enumerate(cons):
 for col,x in q.items():mat[row,col]=x
lb=np.full(mat.shape[1],-100.);ub=np.full(mat.shape[1],100.)
fixed={1:0,19:0,20:0,183:0,184:0,56:0,57:0,25:0,26:0,35:1,36:1,37:1,38:1,107:-1,108:-1}
for old,w in fixed.items():lb[wids[oid[old]]]=ub[wids[oid[old]]]=w
res=milp(np.zeros(mat.shape[1]),integrality=np.ones(mat.shape[1]),bounds=Bounds(lb,ub),constraints=LinearConstraint(mat.tocsr(),np.array(lo),np.array(hi)),options={'time_limit':50})
report=dict(status=res.message)
if res.x is not None:
 report['weights']={str(coords[i].get('source204Id',i+14)):int(round(res.x[k])) for i,k in wids.items() if abs(res.x[k])>.1}
 print(json.dumps(report,indent=2))
else:print(res.message)
(P/'scalar-vieta-rescaling-search.json').write_text(json.dumps(report,indent=2)+'\n')
