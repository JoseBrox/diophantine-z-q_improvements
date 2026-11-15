#!/usr/bin/env python3
"""Frozen exact maps 260 -> 259 -> 258 and a balanced 258-variable family."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as Q
import argparse,hashlib,json
import algebra
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def build(out=HERE):
 parent=None
 for number in [259,258]:
  cfg=json.loads((HERE/f'config{number}.json').read_text())
  raw=(ROOT/cfg['source']).read_bytes() if parent is None else (json.dumps(parent,indent=2)+'\n').encode()
  algebra.require(hashlib.sha256(raw).hexdigest()==cfg['source_sha256'],'parent hash at '+str(number))
  src=json.loads(raw);system,cert=algebra.convert(src,cfg);poly=algebra.sum_squares(system);folder=out/f'family{number}';folder.mkdir(parents=True,exist_ok=True)
  for name,obj in [('quadratic.json',system),('certificate.json',cert),('polynomial.json',poly)]:save(folder/name,obj)
  parent=system
 system=parent;weights={int(k):v for k,v in json.loads((HERE/'balance258-weights.json').read_text()).items()};ids={c['name']:c['id'] for c in system['coordinates']}
 H=31581660**14;K=82479248*H
 cn={'scalar.W2.quadratic':Q(1,H),'scalar.b.quadratic':Q(-1,K),'normalized_scalar.scaled_e':-K,'normalized_scalar.s':K,'normalized_scalar.p':K,'normalized_scalar.factored.q':K,'normalized_scalar.p2.quadratic':K*K,'normalized_scalar.factored.q2':K*K,'normalized_scalar.factored.v':-1}
 constants={ids[n]:Q(v) for n,v in cn.items()};rows=[];record=[]
 for r in system['residuals']:
  transformed=defaultdict(Q)
  for (a,m),c in algebra.parse(r['terms']).items():
   for i in m:c*=constants.get(i,Q(1))
   transformed[2*a+sum(weights[i] for i in m),m]+=c*149**a
  low=min(a for a,m in transformed);tmp={(a-low,m):c for (a,m),c in transformed.items()};tmp,f=algebra.primitive(tmp)
  algebra.require(max(a for a,m in tmp)<=1,'parameter exponent')
  rows.append(dict(id=r['id'],name=r['name'],terms=algebra.serial(tmp)));record.append(dict(id=r['id'],division_power=low,primitive_multiplier=str(f)))
 balanced=dict(system);balanced.update(residuals=rows,fixedParameter=dict(symbol='C',quantified=False,domain='C=149^N, N>=1',oldParameter='A=149*C^2'))
 save(folder/'balanced-quadratic.json',balanced);save(folder/'balanced-polynomial.json',algebra.sum_squares(balanced));save(folder/'balancing.json',dict(weights=weights,constants={str(i):str(c) for i,c in constants.items()},constant_scale_H=str(H),constant_scale_K=str(K),rows=record,convention='x_unbalanced=c_i*C^weight_i*x_balanced, A=149*C^2'))
 print('Built 259 and 258 coordinate families and balanced the latter.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE);args=ap.parse_args();build(args.output)
