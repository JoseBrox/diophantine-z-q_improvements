#!/usr/bin/env python3
"""Independent rational row-span, coordinate-change and height verification."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from math import gcd,lcm
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE='computation/quartic/paired_redundancy196_v40/balanced-quadratic.json'
SHA='36dc9ae7dcc7cadd81bdfcd2145e0366f7acd4a0a14b2e9d7173c05e228fe4ab'
ROWS=['testSquare.40.0.0.definition','testSquare.40.0.1.definition']+[f'sharedT.reference.relation{i}.{j}' for i in (1,2,3) for j in (0,1)]
K0=126616122944180358034867798936
K2=32561227748626372080
def require(ok,message):
 if not ok:raise ValueError(message)
def read_polynomial(terms):
 p=defaultdict(Q)
 for t in terms:p[int(t['parameterPower']),tuple(sorted(t['monomial']))]+=Q(t['coefficient'])
 return {m:c for m,c in p.items() if c}
def determinant_and_inverse(matrix):
 n=len(matrix);a=[[Q(c) for c in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(matrix)];det=Q(1)
 for k in range(n):
  piv=next((i for i in range(k,n) if a[i][k]),None);require(piv is not None,'invertible row transformation')
  if piv!=k:a[k],a[piv]=a[piv],a[k];det=-det
  value=a[k][k];det*=value;a[k]=[c/value for c in a[k]]
  for i in range(n):
   if i!=k:
    value=a[i][k];a[i]=[x-value*y for x,y in zip(a[i],a[k])]
 inverse=[r[n:] for r in a]
 for i in range(n):
  for j in range(n):require(sum(Q(matrix[i][k])*inverse[k][j] for k in range(n))==Q(i==j),'explicit rational inverse')
 return det,inverse
def check(directory,write=False):
 cfg=json.loads((HERE/'transform.json').read_text());require(cfg['source']==SOURCE and cfg['source_sha256']==SHA,'source declaration');raw=(ROOT/SOURCE).read_bytes();require(hashlib.sha256(raw).hexdigest()==SHA,'authenticated source');old=json.loads(raw)
 require(cfg['row_names']==ROWS,'specified eight reference rows');det,inverse=determinant_and_inverse(cfg['matrix']);require(len(cfg['matrix'])==8 and all(len(r)==8 for r in cfg['matrix']),'matrix dimensions')
 source={r['name']:read_polynomial(r['terms']) for r in old['residuals']};modified={}
 for i,name in enumerate(ROWS):
  coeff=defaultdict(Q)
  for j,oldname in enumerate(ROWS):
   for monomial,value in source[oldname].items():coeff[monomial]+=Q(cfg['matrix'][i][j])*value
  modified[name]={m:c for m,c in coeff.items() if c}
 scales={76:Q(1,3813373161796),90:Q(1,3813373161796)};require(cfg['coordinate_scaling']=={str(i):str(c) for i,c in scales.items()},'two nonzero coordinate changes')
 new=json.loads((directory/'quadratic.json').read_text());poly=json.loads((directory/'polynomial.json').read_text());normalizations=json.loads((directory/'normalizations.json').read_text())
 require(new['variables']==poly['variables']==196 and new['inputCoordinate']==poly['inputCoordinate']==1,'variables and input')
 require(new['coordinates']==poly['coordinates']==old['coordinates'],'unchanged coordinate labels')
 require(new['fixedParameter']==poly['fixedParameter']==old['fixedParameter'],'fixed parameter meaning')
 require(new['coordinate_scaling']==poly['coordinate_scaling']==cfg['coordinate_scaling'],'coordinate interpretation metadata')
 require(len(new['residuals'])==len(normalizations)==176,'176 rows')
 for i,(a,b) in enumerate(zip(old['residuals'],new['residuals'])):
  require(a['id']==b['id'] and a['name']==b['name'],'row labels')
  expected={}
  for (power,monomial),c in modified.get(a['name'],source[a['name']]).items():
   for variable in monomial:c*=scales.get(variable,1)
   expected[power,monomial]=c
  primitive=read_polynomial(b['terms']);factor=Q(normalizations[i]);require(factor!=0,'nonzero primitive-row factor')
  require(primitive=={m:c*factor for m,c in expected.items() if c},'exact transformed row identity')
  require(all(c.denominator==1 and len(m)<=2 for (power,m),c in primitive.items()),'integral quadratic row')
  require(gcd(*(abs(int(c)) for c in primitive.values()))==1,'primitive row')
  row_profiles=defaultdict(dict)
  for (power,monomial),c in primitive.items():
   require(power>=0,'nonnegative row parameter powers')
   row_profiles[monomial][power]=int(c)
  fixed_gcd=gcd(*(abs(p[0]) for p in row_profiles.values() if set(p)=={0}))
  if fixed_gcd!=1:
   require(all(len(p)==1 for p in row_profiles.values()),'pure parameter powers in remaining rows')
   require(gcd(fixed_gcd,149)==1,'primitive row after every specialization C=149^N')
 expansion=defaultdict(Q)
 for row in new['residuals']:
  ts=list(read_polynomial(row['terms']).items())
  for i,((a,m),c) in enumerate(ts):
   expansion[2*a,tuple(sorted(m+m))]+=c*c
   for (b,n),d in ts[:i]:expansion[a+b,tuple(sorted(m+n))]+=2*c*d
 expansion={k:c for k,c in expansion.items() if c};require(expansion==read_polynomial(poly['terms']),'independent expanded quartic')
 require(max(len(m) for a,m in expansion)==poly['degree']==4,'exact degree');require(expansion.get((0,(1,1,1,1)))==1,'unit content from input fourth power')
 profiles=defaultdict(dict)
 for (a,m),c in expansion.items():profiles[m][a]=c
 require(len(profiles)==2994,'2994 coordinate monomials')
 require(all(a in (0,1,2) for a,m in expansion),'parameter exponents zero through two')
 require(profiles[(1,1,1,1)]=={0:Q(1)},'complete input fourth-power profile')
 require({i for a,m in expansion for i in m}==set(range(1,197)),'all196 coordinates actually occur')
 for p in profiles.values():
  d=max(p);require(abs(p[d])*149**d>sum(abs(c)*149**a for a,c in p.items() if a<d),'support for every C>=149')
  require(sum(abs(c)*Q(149**3)**(a-2) for a,c in p.items())<=K2,'height upper bound for N>=3')
 require(K0>K2*149**4 and K0<K2*149**6,'coefficient crossover N=3')
 for n in (1,2):require(max(abs(sum(c*149**(n*a) for a,c in p.items())) for p in profiles.values())==K0,'exact small-parameter height')
 require(any(p=={2:Q(K2)} or p=={2:Q(-K2)} for p in profiles.values()),'attained leading height')
 require(profiles[(15,18,152,152)]=={2:Q(-K2)},'fixed maximum coefficient witness')
 report=dict(status='PASS',source_sha256=SHA,row_transformation_determinant=str(det),row_transformation_inverse=[[str(c) for c in r] for r in inverse],variables=196,primitive_quadratic_rows=176,degree=4,integer_content=1,coordinate_monomials=2994,parameter_terms=len(expansion),height_formula=f'max({K0}, {K2} * 149^(2N))',height_constant=str(K0),height_leading_coefficient=str(K2),coefficient_crossover_N=3,scope='Exact input-preserving rational isomorphism and coefficient certificate; unchanged inherited arithmetic premises and defining threshold.')
 if write:(directory/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='row_transformation_inverse'},indent=2))
 return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE);p.add_argument('--write-certificate',action='store_true');a=p.parse_args();check(a.directory,a.write_certificate)
