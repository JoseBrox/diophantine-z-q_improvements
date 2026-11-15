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
D=c.kconst(11,-6);one=c.kconst(1);R=c.rational(c.var(118));u,v,w,m,k,p,ik=[pair(i) for i in range(215,229,2)]
for i in range(215,229):coords[i]={'name':['u','v','w','m','k','p','inversek'][(i-215)//2]+'.'+str((i-215)%2)}
FU=(c.var(56),c.scale(c.var(57),2));FV=(c.var(25),c.scale(c.var(26),2));L=pair(35);LP=pair(37);Z=pair(107);S=pair(19);TH=pair(183)
kr('vieta.product',c.diff(p,c.times(u,v)));kr('vieta.k2',c.diff(c.power2(k),c.times(p,w)));kr('vieta.sum',c.plus(u,v,w,c.ktimes(2,m),c.times(D,c.power2(k))));kr('vieta.pair',c.diff(c.plus(p,c.times(w,c.plus(u,v))),c.power2(m)))
kr('vieta.fusquare',c.diff(FU,c.power2(u)));kr('vieta.fvsquare',c.diff(FV,c.power2(v)))
kr('vieta.primary',c.diff(c.times(L,c.plus(m,u)),c.ktimes(2,c.times(R,c.times(k,S)))))
kr('vieta.alternate',c.plus(c.times(LP,c.plus(m,v)),c.ktimes(2,c.times(R,c.times(k,TH)))))
kr('vieta.scalar',c.plus(c.times(R,c.times(Z,c.plus(m,w))),c.ktimes(2,c.times(k,S))))
kr('vieta.guard',c.diff(c.times(k,ik),one))
agg=c.add(c.scale(c.sub(c.var(4),c.var(90)),8),c.con(40),c.scale(c.power2(w)[0],4))
for fs,gs,ss in [(185,189,193),(195,199,203),(205,209,213)]:agg=c.add(agg,c.scale(c.plus(c.power2(pair(ss)),c.times(D,c.plus(pair(fs),pair(gs))))[0],4))
rows.append(('mixed.aggregate',agg))
rows=[(n,{key:v for key,v in p.items() if not(n=='scalar.b.definition' and key==(0,(109,118)))}) for n,p in rows]
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
(P/'vieta-simple-b-rescaling-search.json').write_text(json.dumps(report,indent=2)+'\n')
