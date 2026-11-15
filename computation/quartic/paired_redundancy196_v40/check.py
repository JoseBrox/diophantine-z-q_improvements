#!/usr/bin/env python3
"""Independently verify the 176-row 196-variable coefficient specification."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import gcd
import argparse,hashlib,json,tempfile,subprocess,sys,copy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCES={
 'computation/quartic/laurent_recovery_v38/family196/quadratic.json':'3b6ab20da25bced159559c35e512e2bb2e56959b734b4265c8f80a7bd9cdb1c1',
 'computation/quartic/laurent_recovery_v38/family196/balanced-quadratic.json':'5b86e26d395e60360ecd1210dd87819b3f57b60e3585db7ad7deff0d677a593c'}
REMOVED={f'pair{i}.curve.{j}' for i in (1,3,4) for j in (0,1)}
HEIGHT=11903780636513165769654680680436132271178681610029854792
def require(ok,msg):
 if not ok:raise ValueError(msg)
def parse(ts):
 p=defaultdict(F)
 for t in ts:p[int(t['parameterPower']),tuple(sorted(t['monomial']))]+=F(t['coefficient'])
 return {k:c for k,c in p.items() if c}
def expand_rows(rows):
 p=defaultdict(F)
 for r in rows:
  terms=list(parse(r['terms']).items())
  for i,((a,m),c) in enumerate(terms):
   p[2*a,tuple(sorted(m+m))]+=c*c
   for (b,n),d in terms[:i]:p[a+b,tuple(sorted(m+n))]+=2*c*d
 return {k:c for k,c in p.items() if c}
def validate(prefix,directory):
 rel='computation/quartic/laurent_recovery_v38/family196/'+prefix+'quadratic.json';raw=(ROOT/rel).read_bytes()
 require(hashlib.sha256(raw).hexdigest()==SOURCES[rel],'parent source digest')
 old=json.loads(raw);new=json.loads((directory/(prefix+'quadratic.json')).read_text());poly=json.loads((directory/(prefix+'polynomial.json')).read_text())
 require(new['variables']==196 and new['inputCoordinate']==1,'coordinate count/input')
 require(new['coordinates']==old['coordinates'] and poly['coordinates']==old['coordinates'],'unchanged coordinate meanings')
 require(new['fixedParameter']==old['fixedParameter'] and poly['fixedParameter']==old['fixedParameter'],'unchanged fixed parameter')
 keep=[r for r in old['residuals'] if r['name'] not in REMOVED]
 require(len(keep)==len(new['residuals'])==176,'retained row count')
 require({r['name'] for r in old['residuals'] if r['name'] in REMOVED}==REMOVED,'exact removed row set')
 for i,(a,b) in enumerate(zip(keep,new['residuals'])):
  require(b['id']==i+1 and b['parent_id']==a['id'],'row source map')
  require(a['name']==b['name'] and parse(a['terms'])==parse(b['terms']),'unchanged retained row')
  require(all(len(m)<=2 and c.denominator==1 for (k,m),c in parse(b['terms']).items()),'integral quadrics')
  require(gcd(*(abs(int(c)) for c in parse(b['terms']).values()))==1,'primitive row')
 expected=expand_rows(keep);actual=parse(poly['terms']);require(actual==expected,'independent symmetric expansion')
 require(poly['variables']==196 and poly['degree']==4,'quartic metadata')
 require(max(len(m) for a,m in actual)==4,'exact degree')
 require(actual.get((0,(1,1,1,1)))==1,'input fourth-power coefficient and unit content')
 profiles=defaultdict(dict)
 for (a,m),c in actual.items():profiles[m][a]=c
 require(len(profiles)==2853,'ordinary support')
 require(profiles[(1,1,1,1)]=={0:F(1)},'complete input fourth-power profile')
 require(all(a in (0,1,2) for a,m in actual),'parameter exponents zero through two')
 if prefix:
  require(max(a for a,m in actual)==2,'balanced parameter degree')
  for m,p in profiles.items():
   k=max(p);require(abs(p[k])*149**k>sum(abs(c)*149**a for a,c in p.items() if a<k),'noncancellation for every C>=149')
   require(sum(abs(c)*F(149)**(a-2) for a,c in p.items())<=HEIGHT,'uniform coefficient majorant H/C²')
  witnesses=[list(m) for m,p in profiles.items() if p=={2:F(HEIGHT)} or p=={2:F(-HEIGHT)}]
  require(witnesses,'exact maximum coefficient attainment')
 else:witnesses=[]
 return dict(variables=196,quadrics=176,coordinate_monomials=len(profiles),parameter_terms=len(actual),degree=4,integer_content=1,maximum_witnesses=witnesses)
def poly_add(*ps):
 out=defaultdict(F)
 for p in ps:
  for m,c in p.items():out[m]+=c
 return {m:c for m,c in out.items() if c}
def poly_mul(p,q):
 out=defaultdict(F)
 for m,c in p.items():
  for n,d in q.items():out[tuple(sorted(m+n))]+=c*d
 return {m:c for m,c in out.items() if c}
def neg(p):return {m:-c for m,c in p.items()}
def universal_identities():
 one={():F(1)}
 f,g,h,k,s,D,L,S,K=[{(i,):F(1)} for i in range(9)]
 f2=poly_mul(f,f);g2=poly_mul(g,g)
 CU=poly_add(poly_mul(h,h),neg(f),poly_mul(D,poly_mul(f,f2)))
 CV=poly_add(poly_mul(k,k),neg(g),poly_mul(D,poly_mul(g,g2)))
 sec=poly_add(poly_mul(s,poly_add(f,neg(g))),neg(h),neg(k))
 tan=poly_add(poly_mul(s,poly_add(h,neg(k))),neg(one),poly_mul(D,poly_add(f2,poly_mul(f,g),g2)))
 require(not poly_add(CU,neg(CV),neg(poly_mul(poly_add(f,neg(g)),tan)),poly_mul(poly_add(h,neg(k)),sec)),'paired defect identity')
 r1=poly_add(poly_mul(h,L),poly_mul(K,poly_mul(f,S)))
 r2=poly_add(poly_mul(poly_add(one,neg(poly_mul(D,f2))),L),poly_mul(K,poly_mul(h,S)))
 require(not poly_add(poly_mul(K,poly_mul(S,CU)),neg(poly_mul(h,r2)),poly_mul(poly_add(one,neg(poly_mul(D,f2))),r1)),'ratio defect identity')
 return 2
def removed_physical_rows():
 src=json.loads((ROOT/'computation/quartic/laurent_recovery_v38/family196/quadratic.json').read_text());ids={c['name']:c['id'] for c in src['coordinates']};rs={r['name']:parse(r['terms']) for r in src['residuals']}
 for block,slot in [(1,0),(3,2),(4,3)]:
  f0,f1=[ids[f'pair{block}.f.{j}'] for j in (0,1)];h0,h1=[ids[f'pair{block}.h.{j}'] for j in (0,1)];F0,F1=[ids[f'testSquare.1.{slot}.{j}.quadratic'] for j in (0,1)]
  p0={(0,tuple(sorted(m))):F(c) for c,m in [(11,(F0,f0)),(-12,(F0,f1)),(-24,(F1,f0)),(44,(F1,f1)),(-1,(f0,)),(1,(h0,h0)),(2,(h1,h1))]}
  p1={(0,tuple(sorted(m))):F(c) for c,m in [(6,(F0,f0)),(-11,(F0,f1)),(-22,(F1,f0)),(24,(F1,f1)),(1,(f1,)),(-2,(h0,h1))]}
  require(rs[f'pair{block}.curve.0']==p0 and rs[f'pair{block}.curve.1']==p1,'literal deleted curve components')
 return 6
def main(directory,write):
 a=validate('',directory);b=validate('balanced-',directory)
 bindings=json.loads((directory/'source-bindings.json').read_text())
 require(bindings==dict(sources=SOURCES,removed_rows=sorted(REMOVED),variables=196,residuals=176),'source binding document')
 report=dict(status='PASS',sources=SOURCES,universal_polynomial_identities=universal_identities(),literal_deleted_components=removed_physical_rows(),unbalanced=a,balanced=b,height_coefficient=str(HEIGHT),height_formula='H=11903780636513165769654680680436132271178681610029854792 * 149^(2N), N>=1',arithmetic_scope='Exact rational-system equivalence; unchanged inherited arithmetic premises and ineffective defining threshold.')
 if write:(directory/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE);p.add_argument('--write-certificate',action='store_true');a=p.parse_args();main(a.directory,a.write_certificate)
