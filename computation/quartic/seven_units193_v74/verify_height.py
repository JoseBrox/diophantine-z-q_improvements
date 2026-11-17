#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
from hashlib import sha256
from math import comb
import json
HERE=Path(__file__).parent

def shifted(poly,c):
 out=defaultdict(int)
 for k,a in poly.items():
  for j in range(k+1):out[j]+=a*comb(k,j)*c**(k-j)
 return dict(out)
def finalize(folder,cross,H0):
 p=HERE/folder;t=json.loads((p/'polynomial-family.json').read_text())['terms'];cs=defaultdict(dict)
 for x in t:cs[tuple(x['monomial'])][x['parameterPower']]=int(x['coefficient'])
 mixed=[]
 for m,f in cs.items():
  signs={1 if a>0 else-1 for a in f.values()}
  if len(signs)>1:mixed.append((m,f));assert f=={0:-578,2:289}or f=={2:289,0:-578}
 assert len(mixed)==1
 assert any(f=={0:H0}or f=={0:-H0}for f in cs.values())
 assert any(f=={4:128}for f in cs.values())
 below=[]
 for N in range(1,cross):
  C=149**N;h=max(abs(sum(a*C**k for k,a in f.items()))for f in cs.values());assert h==H0
  below.append({'N':N,'height':str(h)})
 c=149**cross;assert 128*c**4>H0
 for f in cs.values():
  for sign in(-1,1):
   g={k:sign*a for k,a in f.items()};g[4]=g.get(4,0)+128
   assert all(a>=0 for a in shifted(g,c).values())
 report=json.loads((p/'construction-report.json').read_text())
 report['coordinate_monomials_for_all_N_ge_1']=len(cs)
 report['coefficient_height']={'formula':f'max({H0},128*C^4)','constant':str(H0),'leading_coefficient':128,'parameter_power':4,'coefficient_crossover_N':cross,'crossover_is_not_a_defining_threshold':True}
 report['nonvanishing_certificate']='All coefficient polynomials have coefficients of one sign except289*(C^2-2), nonzero forC=149^N>=149.'
 report['height_certificate']={'below_crossover':below,'tail':'All coefficients of128*(C0+z)^4 +/- f(C0+z) are nonnegative, C0=149^crossover,z>=0.','number_of_tail_inequalities':2*len(cs),'C0':str(c)}
 (p/'construction-report.json').write_text(json.dumps(report,indent=2)+'\n')
 return report
if __name__=='__main__':
 for args in [('fewer_monomials',7,484991541504995159662206970923766531374664106904986910720),('primitive',4,126616122944180358034867798936)]:
  d=finalize(*args);print(args[0],d['coordinate_monomials_for_all_N_ge_1'],d['coefficient_height']['formula'])
