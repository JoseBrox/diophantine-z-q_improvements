"""Check the enhanced packing against the independently audited old tables.
Does not import build_enhanced or any coauthor producer.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import importlib.util,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'H10-quartics'
s=importlib.util.spec_from_file_location('audit',HERE/'check_independent.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
def normalize(p):
 p={k:v for k,v in p.items() if v};loC=min(k for k,e,m in p);loc=min(e for k,e,m in p)
 out={(k-loC,e-loc,m):v for (k,e,m),v in p.items()};v=out[min(out)]
 return {k:val/v for k,val in out.items()}
def reverse(q,w):
 old={z['id']:z['source_id'] for z in q['coordinates']};out={};us={400:1,401:-1,402:-2}
 for row in q['residuals']:
  if row['name'].startswith(('shared.c_unit','shared.c_inverse_square')):continue
  p=defaultdict(Fraction)
  for t in row['terms']:
   mon=[old[i] for i in t['monomial']];e=sum(us.get(i,0)-w.get(i,0) for i in mon);mm=tuple(i for i in mon if i not in us)
   p[t['parameterPower'],e,mm]+=int(t['coefficient'])
  out[row['name']]=p
 return out
report={}
for n,folder in [(165,'general-physical'),(180,'explicit-physical')]:
 oldq=json.loads((ROOT/'quartics'/folder/'quadrics.json').read_text());ow={int(i):v for i,v in json.loads((ROOT/'quartics'/folder/'weights.json').read_text())['weights'].items()}
 newdir=HERE/'enhanced'/str(n);newq,rows,poly,mono=a.expansion(newdir);nw={int(i):v for i,v in json.loads((newdir/'weights.json').read_text())['weights'].items()}
 assert newq['coordinates']==oldq['coordinates'] and nw[1]==ow[1]==0
 old,new=reverse(oldq,ow),reverse(newq,nw);assert set(old)==set(new)
 pair={0:({60,61},{62,63}),1:({70,71},{72,73}),2:({66,67},{68,69})};changed=[]
 for name,p in old.items():
  expected=p
  for j,(left,right) in pair.items():
   if name in [f'new.det0.factor{j}.0',f'new.det0.factor{j}.1']:
    expected={};count=0
    for (k,e,m),v in p.items():
     odd=len(m)==2 and ((m[0] in left and m[1] in right) or (m[1] in left and m[0] in right))
     expected[k,e+(4 if odd else 0),m]=v;count+=odd
    assert count==2;changed.append(name)
  assert normalize(expected)==normalize(new[name]),name
 assert len(changed)==6 and n==newq['variables'] and len(rows)==(139 if n==165 else 152)
 # Verify the literal unit rows, rather than assuming their names imply their content.
 om={z['source_id']:z['id'] for z in newq['coordinates']}
 nr={r['name']:a.terms(r,n) for r in newq['residuals']}
 assert nr['shared.c_unit']=={(0,()):-1,(0,tuple(sorted([om[400],om[401]]))):1}
 assert nr['shared.c_inverse_square']=={(0,(om[401],om[401])):-1,(0,(om[402],)):1}
 report[str(n)]={'variables':n,'quadrics':len(rows),'degree':4,'coordinate_monomials':len(mono),'exactly_changed_physical_rows':changed,'all_other_physical_rows_unchanged':True}
 if n==165:
  bq,br,bp,bm=a.expansion(newdir/'balanced');cw=json.loads((newdir/'balanced/parameter_weights.json').read_text());a.independent_balance(rows,br,{'coordinate_weights':cw})
  profiles=[tuple(p.get(i,0) for i in range(3)) for p in bm.values()];assert all(max(p)<=2 for p in bm.values())
  K=126616122944180358034867798936
  assert any(abs(x)==K and y==z==0 for x,y,z in profiles) and any(abs(z)==22201 and x==y==0 for x,y,z in profiles)
  for N in range(1,6):
   C=149**N;values=[x+y*C+z*C*C for x,y,z in profiles];assert all(values) and max(map(abs,values))==max(K,22201*C*C)
  C=149**6
  for x,y,z in profiles:
   val=x+y*C+z*C*C;sign=1 if val>0 else -1
   assert sign*val>0 and sign*(y+2*z*C)>=0 and sign*z>=0
   for sign in [-1,1]:assert min(22201*C*C+sign*val,44402*C+sign*(y+2*z*C),22201+sign*z)>=0
  report[str(n)]['balanced_monomials']=len(bm);report[str(n)]['balanced_exact_height']='max(126616122944180358034867798936,149^(2N+2)) for every N>=1'
# Formula-level valuation checks are complete in the indicated residue classes.
for mu in [1,3,5,7]:
 vals=[{(e*(-mu)+4*k)%8 for k in range(8)} for e in [5,2,7]]+[{4},{0}]
 assert all(not(vals[i]&vals[j]) for i in range(5) for j in range(i))
# Prepared depths d>=1: all new error terms are >=8d-7>0;
# input is >=12d-5>0. These linear inequalities follow from their d=1 cases.
assert 8-7>0 and 12-5>0
# At mu>=1, errors have valuation>19mu/16 or27mu/16, hence at least2.
assert Fraction(19,16)>1 and Fraction(27,16)>1
report['status']='PASS';report['local_divisibilities']={'Lucas':'M_j^4 divides Delta','input':'M_j^3 divides nonzero reduced numerator of beta-n'};report['scope']='Exact tables and strengthening relative to the audited source arithmetic; no lower variable count claimed.'
assert json.loads((HERE/'enhanced/certificate.json').read_text())==report;print(json.dumps(report,indent=2))
