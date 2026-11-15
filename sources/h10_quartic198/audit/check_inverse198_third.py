"""Independent final198 audit against affine200, and physical scaled chart.
No producer or other checker is imported. Formal parameter A is fixed per member.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as Q
from math import gcd,lcm
import json,hashlib
import sympy as s
B=Path(__file__).resolve().parents[1];oldpath=B/'circuits/affine200/quadratic.json';newpath=B/'circuits/inverse198/quadratic.json'
old=json.loads(oldpath.read_text());new=json.loads(newpath.read_text())
oldids={c['id']:c['source204Id'] if 'source204Id' in c else 205+2*('f','h','g','k','s').index(c['name'].split('.')[1])+int(c['name'].split('.')[2]) for c in old['coordinates']}
ids={c['id']:c['formalId'] for c in new['coordinates']};w={c['formalId']:c['rescalingExponent'] for c in new['coordinates']}
assert w.get(1,0)==w.get(118,0)==w.get(117,0)==w.get(107,0)==w.get(108,0)==0
assert w[35]==w[36]==w[37]==w[38]==1 # source comparison output R times physical ratio

def sparse(row,mp=None):return {(t['parameterPower'],tuple(sorted(mp[i] if mp else i for i in t['monomial']))):Q(t['coefficient']) for t in row['terms']}
def laurent(p,scale=False):
 out=defaultdict(Q)
 for (a,m),c in p.items():
  e=m.count(118)+2*m.count(117)+(sum(w.get(i,0) for i in m) if scale else 0)
  mm=tuple(i for i in m if i not in (117,118));out[(a,e,mm)]+=c
 return {k:c for k,c in out.items() if c}
def norm(p):
 p={k:c for k,c in p.items() if c};first=p[min(p)];return {k:c/first for k,c in p.items()}
rows={r['name']:r for r in new['residuals']};removed=set(range(104,122))|set(range(140,145))
checked=[]
for r in old['residuals']:
 if r.get('source204RowId') in removed:continue
 rr=rows[r['name']]
 if r['name']=='scalar.r_power_2.definition':assert norm(sparse(rr,ids))==norm({(0,(117,)):Q(1),(0,(118,118)):Q(-1)})
 else:
  ex=laurent(sparse(r,oldids),True);got=laurent(sparse(rr,ids));shift=rr['dividedRPower'];got={(a,e+shift,m):c for (a,e,m),c in got.items()}
  assert norm(got)==norm(ex),r['name']
 checked.append(r['name'])
# Direct construction of physical final scaled coordinates, not a replay of the producer's unscaled chart.
rho=s.sqrt(2);A=s.Symbol('A');vv=s.symbols('x1:229');v={i:vv[i-1] for i in range(1,229)}
def kp(i,half=False):return v[i]+rho*(2 if half else 1)*v[i+1]
def extract(e):
 e=s.expand(e);return [e.coeff(rho,0),e.coeff(rho,1)]
def terms(e):
 syms=sorted(e.free_symbols,key=str);p=s.Poly(s.expand(e),*syms);out={}
 for powers,c in p.terms():
  a=0;mm=[]
  for x,k in zip(syms,powers):
   if x==A:a=k
   else:mm.extend([int(str(x)[1:])]*k)
  out[a,tuple(sorted(mm))]=Q(c)
 return out
U,V,W,M,r,P,r2=[kp(i) for i in range(215,229,2)];R=v[118];R2=v[117];D=11-6*rho;S=kp(19);TH=kp(183);L=kp(35);LP=kp(37);Z=kp(107)
physical={
 'inverse_vieta.product':U*V-R2*P,
 'inverse_vieta.r':P*W-r,
 'inverse_vieta.sum':r*(U+V+W+2*M)+D*R2,
 'inverse_vieta.pair':R2*P+W*(U+V)-M*M,
 'inverse_vieta.r2':r2-r*r,
 'inverse_vieta.fusquare':kp(56,True)*r2-U*U,
 'inverse_vieta.fvsquare':kp(25,True)*r2-V*V,
 'inverse_vieta.primary':L*(M+U)-2*R*S,
 'inverse_vieta.alternate':LP*(M+V)+2*R*TH,
 'inverse_vieta.scalar':Z*(M+W)+2*S}
for name,expr in physical.items():
 for j,component in enumerate(extract(expr)):
  key=name+'.'+str(j);assert norm(terms(component))==norm(sparse(rows[key],ids)),key;checked.append(key)
agg=8*(v[4]-v[90])+56+4*v[225]
for f,g,ss in [(185,189,193),(195,199,203),(205,209,213)]:agg+=4*extract(kp(ss)**2+D*(kp(f)+kp(g)))[0]
key='inverse_vieta.unweighted.aggregate';assert norm(terms(agg))==norm(sparse(rows[key],ids));checked.append(key)
assert set(checked)==set(rows) and len(rows)==184 and len(ids)==198
# R is nonzero in the final equations, before any Laurent inversion.
x=s.Symbol('x');beta=51*x*x+2504;slot105=(51*x*x+2501)**2/4
contact=-14315517724-291790992*x*x-15531948*x*x*slot105-767410608*slot105+512*slot105**2
assert s.expand(contact-beta*(beta-1)*(beta-2401)*(32*beta+343))==0
# Independent full quartic expansion.
expanded=defaultdict(Q)
for row in rows.values():
 ts=list(sparse(row).items())
 for (a,m),c in ts:
  for (b,n),d in ts:expanded[a+b,tuple(sorted(m+n))]+=c*d
expanded={k:c for k,c in expanded.items() if c}
assert expanded==sparse(json.loads((newpath.parent/'polynomial.json').read_text()))
profiles=defaultdict(dict)
for (a,m),c in expanded.items():profiles[m][a]=int(c)
assert len(profiles)==2945 and len(expanded)==2945 and max(len(m) for a,m in expanded)==4
assert gcd(*(int(c) for c in expanded.values()))==1 and {i for a,m in expanded for i in m}==set(range(1,199))
assert all(len(p)==1 for p in profiles.values())
C0=(5898050446009651968*31581660**28)**2
assert max(abs(p.get(0,0)) for p in profiles.values())==C0
assert max(abs(p.get(2,0)) for p in profiles.values())==1
assert max(abs(p.get(1,0)) for p in profiles.values())<=149**3
assert 149**210<C0<=149**214
report={'status':'PASS','variables':198,'quadratic_rows':184,'ordinary_monomials':2945,'all_source_rescalings_checked':True,'physical_scaled_chart_checked_directly':True,'R_nonzero_before_Laurent_inversion':True,'exact_expansion_checked':True,'degree':4,'content':1,'exact_height':'max((5898050446009651968*31581660^28)^2,149^(4N+2))','height_crossover_N':53,'candidate_sha256':hashlib.sha256(newpath.read_bytes()).hexdigest(),'scope':'Finite algebraic checks; arithmetic projection proof and inherited assumptions are separate.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
