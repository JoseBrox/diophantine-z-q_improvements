"""Compile the c^5,c^7 error packing using a stored exact weight certificate."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from math import gcd,lcm
import json,types
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'H10-quartics'
m=types.ModuleType('physical')
source=(ROOT/'quartics/check_physical.py').read_text().replace('eq=plus(eq,times(pm(e=power),term))','eq=plus(eq,times(pm(e=power+(4 if j in hy and power in (1,3) else 0)),term))')
exec(compile(source,str(ROOT/'quartics/check_physical.py'),'exec'),m.__dict__)
def dump(path,data):path.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
def polynomial(q):
 p=defaultdict(int)
 for r in q['residuals']:
  for t in r['terms']:
   for u in r['terms']:
    p[t['parameterPower']+u['parameterPower'],tuple(sorted(t['monomial']+u['monomial']))]+=int(t['coefficient'])*int(u['coefficient'])
 return {'variables':q['variables'],'inputCoordinate':1,'terms':[{'parameterPower':k,'monomial':list(a),'coefficient':str(c)} for (k,a),c in sorted(p.items()) if c]}
for n,folder in [(165,'general-physical'),(180,'explicit-physical')]:
 cert=json.loads((HERE/f'weights_enhanced_precision_{n}.json').read_text());w={int(i):v for i,v in cert['weights'].items()};h=cert['rows'];assignment=json.loads((ROOT/'quartics'/folder/'assignment.json').read_text())
 eqs=m.expected(ROOT/'source/computation/quartic/seven_units193_v74/primitive/laurent-source.json',n,assignment)
 ids=sorted(set(w)|{400,401,402});index={i:j+1 for j,i in enumerate(ids)};assert len(ids)==n and ids[0]==1
 unit={-4:(402,402),-3:(401,402),-2:(402,),-1:(401,),0:(),1:(400,),2:(400,400)}
 rows=[]
 for name,p in eqs.items():
  out=defaultdict(Fraction)
  for (k,e,a),coef in p.items():
   v=e+sum(w[i] for i in a)-h[name];mon=tuple(sorted(a+unit[v]));assert len(mon)<=2
   out[k,mon]+=coef
  out={z:a for z,a in out.items() if a};den=lcm(*(x.denominator for x in out.values()));g=gcd(*(int(x*den) for x in out.values()))
  rows.append({'name':name,'terms':[{'parameterPower':k,'monomial':sorted(index[i] for i in a),'coefficient':str(int(coef*den)//g)} for (k,a),coef in sorted(out.items())]})
 rows.extend([{'name':'shared.c_unit','terms':[{'parameterPower':0,'monomial':[],'coefficient':'-1'},{'parameterPower':0,'monomial':sorted([index[400],index[401]]),'coefficient':'1'}]},{'name':'shared.c_inverse_square','terms':[{'parameterPower':0,'monomial':[index[401],index[401]],'coefficient':'-1'},{'parameterPower':0,'monomial':[index[402]],'coefficient':'1'}]}])
 q={'variables':n,'inputCoordinate':1,'coordinates':[{'id':j+1,'source_id':i} for j,i in enumerate(ids)],'residuals':rows}
 out=HERE/'enhanced'/str(n);out.mkdir(parents=True,exist_ok=True);dump(out/'quadrics.json',q);dump(out/'polynomial.json',polynomial(q));dump(out/'weights.json',cert);dump(out/'assignment.json',assignment)
 if n==165:
  original=json.loads((ROOT/'quartics/general-physical/quadrics.json').read_text());oldcw=json.loads((ROOT/'quartics/general/certificate.json').read_text())['coordinate_weights'];cw={z['source_id']:oldcw[z['id']-1] for z in original['coordinates']};newrows=[]
  for row in rows:
   t=[(z['parameterPower']+sum(cw[ids[i-1]] for i in z['monomial']),z['monomial'],int(z['coefficient'])) for z in row['terms']];low=min(k for k,a,b in t);assert max(k for k,a,b in t)-low<=1
   newrows.append({'name':row['name'],'terms':[{'parameterPower':k-low,'monomial':a,'coefficient':str(b)} for k,a,b in t]})
  balanced={**q,'residuals':newrows};out=out/'balanced';out.mkdir(exist_ok=True);dump(out/'quadrics.json',balanced);dump(out/'polynomial.json',polynomial(balanced));dump(out/'parameter_weights.json',[cw[i] for i in ids])
 print(n,'compiled',len(rows),'rows',flush=True)
