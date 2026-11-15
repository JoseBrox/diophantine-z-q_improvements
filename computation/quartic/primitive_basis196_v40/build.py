#!/usr/bin/env python3
"""Reconstruct the fixed small-coefficient196-variable quartic specification."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from math import gcd,lcm
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def serial(p):return [dict(parameterPower=a,monomial=list(m),coefficient=str(c)) for (a,m),c in sorted(p.items()) if c]
def parse(ts):
 out=defaultdict(Q)
 for t in ts:out[int(t['parameterPower']),tuple(sorted(t['monomial']))]+=Q(t['coefficient'])
 return {k:c for k,c in out.items() if c}
def primitive(p):
 p={k:c for k,c in p.items() if c};d=lcm(*(c.denominator for c in p.values()));g=gcd(*(abs(int(d*c)) for c in p.values()))
 if p[min(p)]<0:g=-g
 s=Q(d,g);return {k:c*s for k,c in p.items()},s
def dump(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def build(out):
 cfg=json.loads((HERE/'transform.json').read_text());raw=(ROOT/cfg['source']).read_bytes();assert hashlib.sha256(raw).hexdigest()==cfg['source_sha256'];src=json.loads(raw)
 byname={r['name']:parse(r['terms']) for r in src['residuals']};transformed={}
 for i,name in enumerate(cfg['row_names']):
  pp=defaultdict(Q)
  for scale,oldname in zip(cfg['matrix'][i],cfg['row_names']):
   for k,c in byname[oldname].items():pp[k]+=Q(scale)*c
  transformed[name]={k:c for k,c in pp.items() if c}
 factors={int(i):Q(c) for i,c in cfg['coordinate_scaling'].items()};rows=[];normalizations=[]
 for row in src['residuals']:
  p=transformed.get(row['name'],parse(row['terms']));q={}
  for (a,m),c in p.items():
   for i in m:c*=factors.get(i,1)
   q[a,m]=c
  q,scale=primitive(q);rows.append(dict(row,terms=serial(q)));normalizations.append(str(scale))
 result=dict(src,format='primitive-quadratic-basis/v40',residuals=rows,coordinate_scaling=cfg['coordinate_scaling'],coordinate_convention=cfg['coordinate_convention'])
 expansion=defaultdict(Q)
 for row in rows:
  p=parse(row['terms'])
  for (a,m),c in p.items():
   for (b,n),d in p.items():expansion[a+b,tuple(sorted(m+n))]+=c*d
 poly=dict(format='integer-quartic/v40',variables=result['variables'],degree=4,inputCoordinate=result['inputCoordinate'],fixedParameter=result['fixedParameter'],coordinates=result['coordinates'],coordinate_scaling=cfg['coordinate_scaling'],coordinate_convention=cfg['coordinate_convention'],terms=serial(expansion))
 out.mkdir(parents=True,exist_ok=True);dump(out/'quadratic.json',result);dump(out/'polynomial.json',poly);dump(out/'normalizations.json',normalizations)
 print('Built 196 variables, 176 primitive quadratic rows and 2994 monomials.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE);a=p.parse_args();build(a.output)
