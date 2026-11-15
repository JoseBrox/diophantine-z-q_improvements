#!/usr/bin/env python3
"""Remove six redundant reciprocal-curve rows from the current196 family."""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PARENT=ROOT/'computation/quartic/laurent_recovery_v38/family196'
REMOVED={f'pair{i}.curve.{j}' for i in (1,3,4) for j in (0,1)}
def dump(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def expand(rows):
 out=defaultdict(Fraction)
 for row in rows:
  for t in row['terms']:
   for u in row['terms']:
    out[int(t['parameterPower'])+int(u['parameterPower']),tuple(sorted(t['monomial']+u['monomial']))]+=Fraction(t['coefficient'])*Fraction(u['coefficient'])
 return [dict(parameterPower=a,monomial=list(m),coefficient=str(c)) for (a,m),c in sorted(out.items()) if c]
def build(out):
 out.mkdir(parents=True,exist_ok=True)
 inputs={}
 for prefix in ('','balanced-'):
  path=PARENT/(prefix+'quadratic.json');raw=path.read_bytes();inputs[str(path.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest();old=json.loads(raw)
  rows=[r for r in old['residuals'] if r['name'] not in REMOVED]
  assert len(rows)==176 and {r['name'] for r in old['residuals'] if r['name'] in REMOVED}==REMOVED
  new=dict(old);new['format']='paired-ratio-redundancy/v40';new['residuals']=[dict(r,parent_id=r['id'],id=i+1) for i,r in enumerate(rows)]
  poly=dict(format='integer-quartic/v40',variables=new['variables'],degree=4,inputCoordinate=new['inputCoordinate'],fixedParameter=new['fixedParameter'],coordinates=new['coordinates'],terms=expand(rows))
  dump(out/(prefix+'quadratic.json'),new);dump(out/(prefix+'polynomial.json'),poly)
 dump(out/'source-bindings.json',dict(sources=inputs,removed_rows=sorted(REMOVED),variables=196,residuals=176))
 print('Built 196 coordinates, 176 quadrics, 2853 monomials.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE);a=p.parse_args();build(a.output)
