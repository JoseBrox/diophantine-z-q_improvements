#!/usr/bin/env python3
"""Reconstruct the 196-coordinate family and its fixed-parameter balancing.

No search is performed: all maps are explicitly recorded and independently
checked by check.py. The parent arithmetic premises are unchanged.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
import argparse, hashlib, json
import algebra
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def write(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def build(out=HERE/'family196'):
 cfg=json.loads((HERE/'config196.json').read_text());raw=(ROOT/cfg['source']).read_bytes()
 algebra.require(hashlib.sha256(raw).hexdigest()==cfg['source_sha256'],'parent hash')
 src=json.loads(raw);system,cert=algebra.convert(src,cfg);poly=algebra.sum_squares(system)
 out.mkdir(parents=True,exist_ok=True)
 for name,obj in [('quadratic.json',system),('certificate.json',cert),('polynomial.json',poly)]:write(out/name,obj)
 pweights=json.loads((ROOT/'sources/h10_quartic198/circuits/inverse198/balancing-weights.json').read_text())['weights']
 weights={c['id']:int(pweights[str(c['parent_id'])])-cfg['weights'].get(str(c['parent_id']),[0])[0] for c in system['coordinates']}
 adjustments={'amplified.det1.factor0.0':1,'amplified.det1.factor0.1':1,'amplified.det1.factor4.0':0}
 for c in system['coordinates']:
  if c['name'] in adjustments:weights[c['id']]=adjustments[c['name']]
 rows=[];record=[]
 for row in system['residuals']:
  transformed=defaultdict(Q)
  for (a,m),c in algebra.parse(row['terms']).items():transformed[2*a+sum(weights[i] for i in m),m]+=c*149**a
  low=min(k for k,m in transformed);tmp={(k-low,m):c for (k,m),c in transformed.items()};tmp,f=algebra.primitive(tmp)
  algebra.require(max(k for k,m in tmp)<=1,'parameter degree exceeds one: '+row['name'])
  rows.append(dict(id=row['id'],name=row['name'],terms=algebra.serial(tmp)))
  record.append(dict(id=row['id'],division_power=low,primitive_multiplier=str(f)))
 balanced=dict(system);balanced.update(residuals=rows,fixedParameter=dict(symbol='C',quantified=False,domain='C=149^N, N>=1',oldParameter='A=149*C^2'))
 bpoly=algebra.sum_squares(balanced)
 write(out/'balanced-quadratic.json',balanced);write(out/'balanced-polynomial.json',bpoly)
 write(out/'balancing.json',dict(convention='unbalanced x_i=C^weight_i*balanced x_i, A=149*C^2',weights=weights,rows=record))
 print('Built',len(system['coordinates']),'coordinates,',len(rows),'quadrics,',len(poly['terms']),'unbalanced coefficient terms.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'family196');a=ap.parse_args();build(a.output)
