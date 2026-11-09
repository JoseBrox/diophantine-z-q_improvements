#!/usr/bin/env python3
"""Independent semantic and coefficient audit of normalized quartic tables."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import json, math
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'bundle_v11/publication/computation/quartic'
NEW=ROOT/'work/quartic'

def plus(a,b):
 d=defaultdict(F,a)
 for k,v in b.items():d[k]+=v
 return {k:v for k,v in d.items() if v}
def scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def times(a,b):
 d=defaultdict(F)
 for i,x in a.items():
  for j,y in b.items():d[i+j]+=x*y
 return {k:v for k,v in d.items() if v}

def check(baseline,new):
 old=json.loads((BASE/f'family{baseline}/quadratic-family{baseline}.json').read_text())
 lk={c['id']:c['sourceId'] for c in old['coordinates']}
 defs={r['sourceId']:r for r in old['residuals']}
 expressions={248:{1:F(1)}}
 for row_id,variable in [(453,487),(454,488),(455,489)]:
  accum={};den=F(0)
  for t in defs[row_id]['terms']:
   assert t['parameterPower']==0
   mon=tuple(lk[i] for i in t['monomial']);c=F(t['coefficient'])
   if variable in mon:
    assert mon==(variable,);den+=c
   else:
    term={0:c}
    for v in mon:term=times(term,expressions[v])
    accum=plus(accum,term)
  assert den
  expressions[variable]=scale(accum,-1/den)
 r={0:F(-103171881284)}
 for sid,c in [(248,-2103220824),(487,-21050600),(488,-7629700),(489,-45771136)]:
  r=plus(r,scale(expressions[sid],F(c)))
 beta={0:F(2504),1:F(51)}
 target={0:F(1)}
 for factor in [beta,plus(beta,{0:F(-1)}),plus(beta,{0:F(-2401)}),plus(scale(beta,32),{0:F(343)}),plus(scale(beta,2),{0:F(-1)})]:target=times(target,factor)
 assert r==target,(baseline,r,target)
 p=json.loads((NEW/f'family{new}/polynomial-family{new}.json').read_text())
 nm={c['id']:c['sourceId'] for c in p['coordinates']}
 coeff=defaultdict(dict)
 for term in p['terms']:
  mon=tuple(sorted(nm[i] for i in term['monomial']));power=term['parameterPower']
  assert power not in coeff[mon]
  coeff[mon][power]=int(term['coefficient'])
 assert coeff[(489,489)]=={0:1,2:1}
 mixed=[(m,c) for m,c in coeff.items() if len(c)>1]
 assert mixed==[((489,489),{0:1,2:1})]
 const=max(abs(c[0]) for c in coeff.values() if set(c)=={0})
 linear=max(abs(c[1]) for c in coeff.values() if set(c)=={1})
 assert linear==2*80989**2
 assert all(set(c) in ({0},{1},{0,2}) for c in coeff.values())
 minN=None
 for N in range(1,27465):
  A=pow(80989,2*N+1)
  if A*A+1>max(const,linear*A):minN=N;break
 assert minN==23
 A=pow(80989,54929)
 assert A*A+1>max(const,linear*A)
 return {'baseline':baseline,'variables':new,'semantic_contact_product_identity':'PASS','old_z489_occurs_in_rows':[r0['sourceId'] for r0 in old['residuals'] if any(lk[i]==489 for t in r0['terms'] for i in t['monomial'])], 'support':len(coeff),'support_valid_for_every_positive_A':True,'only_mixed_parameter_coefficient':{'monomial_source_ids':[489,489],'formula':'A^2+1'},'maximum_constant_coefficient_bits':const.bit_length(),'maximum_linear_multiplier':linear,'exact_height_threshold_N':minN,'explicit_height_bits':(A*A+1).bit_length(),'affine_determinant':-45771136}

report={'status':'PASS','checks':[check(301,297),check(351,342)]}
out=Path(__file__).with_name('affine-scalar-independent-audit.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
