from pathlib import Path
import json,numpy as np,importlib.util
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
P=Path(__file__).parent;spec=importlib.util.spec_from_file_location('affine',P/'build_affine200.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);c=a.c
d=json.loads((P/'affine200/quadratic.json').read_text());coords={co['source204Id'] if 'source204Id'in co else 205+co['id']-191:dict(co) for co in d['coordinates']};lift={co['id']:co['source204Id'] if 'source204Id'in co else 205+co['id']-191 for co in d['coordinates']}
def pair(i):return c.var(i),c.var(i+1)
removed=set([2,3]+list(range(155,169)));remrows=set(range(104,122))|set(range(140,145))
rows=[]
for r in d['residuals']:
 if r.get('source204RowId') in remrows:continue
 rows.append((r['name'],{(t['parameterPower'],tuple(sorted(lift[i] for i in t['monomial']))):int(t['coefficient']) for t in r['terms']}))
def kr(n,z):rows.extend([(n+'.0',z[0]),(n+'.1',z[1])])
D=c.kconst(11,-6);one=c.kconst(1);R=c.rational(c.var(118));u,v,w,m,r,p,r2=[pair(i) for i in range(215,229,2)]
for i in range(215,229):coords[i]={'name':['u','v','w','m','r','p','r2'][(i-215)//2]+'.'+str((i-215)%2)}
FU=(c.var(56),c.scale(c.var(57),2));FV=(c.var(25),c.scale(c.var(26),2));L=pair(35);LP=pair(37);Z=pair(107);S=pair(19);TH=pair(183)
kr('inverse_vieta.product',c.diff(p,c.times(u,v)));kr('inverse_vieta.r',c.diff(r,c.times(p,w)));kr('inverse_vieta.sum',c.plus(c.times(r,c.plus(u,v,w,c.ktimes(2,m))),D));kr('inverse_vieta.pair',c.diff(c.plus(p,c.times(w,c.plus(u,v))),c.power2(m)))
kr('inverse_vieta.r2',c.diff(r2,c.power2(r)))
kr('inverse_vieta.fusquare',c.diff(c.times(FU,r2),c.power2(u)));kr('inverse_vieta.fvsquare',c.diff(c.times(FV,r2),c.power2(v)))
kr('inverse_vieta.primary',c.diff(c.times(L,c.plus(m,u)),c.ktimes(2,c.times(R,S))))
kr('inverse_vieta.alternate',c.plus(c.times(LP,c.plus(m,v)),c.ktimes(2,c.times(R,TH))))
kr('inverse_vieta.scalar',c.plus(c.times(R,c.times(Z,c.plus(m,w))),c.ktimes(2,S)))
retained=[i for i in coords if i not in removed|{117,118}];wids={i:j for j,i in enumerate(retained)};cons=[];lo=[];hi=[]
for rid,(name,poly) in enumerate(rows):
 for (param,monomial),coef in poly.items():
  q={};e=0;n=0
  for i in monomial:
   if i==118:e+=1
   elif i==117:e+=2
   else:q[wids[i]]=q.get(wids[i],0)+1;n+=1
  if n>2:raise ValueError((name,n,monomial))
  q[len(retained)+rid]=-1;cons.append(q);lo.append(-e);hi.append(2*(2-n)-e)
mat=lil_matrix((len(cons),len(retained)+len(rows)))
for row,q in enumerate(cons):
 for col,x in q.items():mat[row,col]=x
lb=np.full(mat.shape[1],-100.);ub=np.full(mat.shape[1],100.);lb[wids[1]]=ub[wids[1]]=0
res=milp(np.zeros(mat.shape[1]),integrality=np.ones(mat.shape[1]),bounds=Bounds(lb,ub),constraints=LinearConstraint(mat.tocsr(),np.array(lo),np.array(hi)),options={'time_limit':50})
report=dict(status=res.message)
if res.x is not None:
 report['weights']={str(i):int(round(res.x[k])) for i,k in wids.items() if abs(res.x[k])>.1};report['row_powers']={name:int(round(res.x[len(retained)+ri])) for ri,(name,_) in enumerate(rows)}
 print(json.dumps(report,indent=2))
else:print(res.message)
(P/'inverse-vieta-rescaling-search.json').write_text(json.dumps(report,indent=2)+'\n')
