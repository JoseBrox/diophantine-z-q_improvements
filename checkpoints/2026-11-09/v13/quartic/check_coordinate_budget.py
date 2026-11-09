#!/usr/bin/env python3
"""Exact disjoint coordinate budget for the current279-variable family."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
p=HERE/'family279/quadratic-family279.json';raw=p.read_bytes();data=json.loads(raw)
budget=defaultdict(list)
root=set(range(1,17))|set(range(82,90))
aux=set(range(21,37))|set(range(110,116))|set(range(118,124))|set(range(126,132))|set(range(134,140))|{90,91,140,141,142,143,160,161,164,165,168,169,172,173,176,177,700,701}
for c in data['coordinates']:
 sid=c['sourceId'];name=c['name']
 if sid in {0,37,248}:key='Input, input square, common slope'
 elif sid in root:key='Four root point charts'
 elif sid in aux:key='Auxiliary and difference point charts, including z values'
 elif name.startswith('logV'):key='Formal logarithm data'
 elif name.startswith(('L1.','L2.','L3.','L4.','LP1.','LP2.','LP3.','LP4.','Lucas.')):key='Comparison ratios and Lucas residual'
 elif name.startswith('testSquare.') or name.startswith(('amplified.C1.','amplified.U3.','amplified.U4.')):key='Squared tests and shared higher powers'
 elif name.startswith('aggregateTrace.'):key='Aggregate trace square scale'
 elif name.startswith(('scalar.','normalized_scalar.','reduced_scalar.')):key='Scalar height and fixed-prime block'
 elif name.startswith(('detector0.','detector1.','amplified.det','mixed.det')):
  if ('.factor' in name and '.factored.' not in name) or '.product' in name:key='Local factor values and intermediate products'
  elif any(s in name for s in ['normalized.','factored.']):key='Comparison pole witnesses'
  elif any(s in name for s in ['actualW.','normOver2w0','.B']):key='Comparison trace and pole inputs'
  elif sid in {355,403,359,407,369,417,360,408,361,409,362,410,850,851}:key='Comparison weight power gates'
  else:key='Comparison contacts, scales, numerator and delta clearing'
 else:raise AssertionError((sid,name))
 budget[key].append({'sourceId':sid,'name':name})
expected={'Input, input square, common slope':3,'Four root point charts':24,'Auxiliary and difference point charts, including z values':58,'Formal logarithm data':20,'Comparison ratios and Lucas residual':22,'Squared tests and shared higher powers':30,'Aggregate trace square scale':1,'Scalar height and fixed-prime block':27,'Local factor values and intermediate products':32,'Comparison pole witnesses':14,'Comparison trace and pole inputs':8,'Comparison weight power gates':14,'Comparison contacts, scales, numerator and delta clearing':26}
actual={k:len(v) for k,v in budget.items()};assert actual==expected,(actual,expected)
assert sum(actual.values())==279
result={'status':'PASS','variables':279,'sourceSha256':sha256(raw).hexdigest(),'counts':actual,'coordinates':dict(budget),'fixedBlockCountExcludingAlternateZ':{'rootCharts':24,'auxiliaryChartsExcludingEightZValues':50,'scalarBlock':27,'input':1,'total':102},'scope':'The102 count is only an accounting obstruction when these literal disjoint blocks are retained, not a lower bound for all quartics or all encodings.'}
(HERE/'coordinate-budget279.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['counts'],indent=2))
