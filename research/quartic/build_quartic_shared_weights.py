#!/usr/bin/env python3
"""Construct 297/342-coordinate quartics with one shared local weight."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=Path(__file__).resolve().parents[2]/'bundle_v11/publication/computation/quartic'
PINS={301:'9917be941135778816ce25ecb0cbc872b4ed7c9f3691d79355e5e8352667a4fe',351:'452d063b6d7da598471aa1ec0302b9e37611a44168610592931ec56aac241966'}

def run(baseline,source_root=DEFAULT_SOURCE,output_root=HERE):
 source=source_root/f'family{baseline}'/f'quadratic-family{baseline}.json'
 raw=source.read_bytes(); assert sha256(raw).hexdigest()==PINS[baseline],(baseline,sha256(raw).hexdigest())
 old=json.loads(raw); lookup={c['id']:c['sourceId'] for c in old['coordinates']}
 count=2 if baseline==301 else 3; number=297 if baseline==301 else 342
 deleted={sid+48*d for d in range(count) for sid in (353,354,356)}
 names={};edits={};remove=set();newrows=[];newcoords=[]
 for d in range(count):
  off=48*d;q,q4,c,q19,q38,q79=[x+off for x in [352,362,355,359,369,360]];q8=850+d
  for sid,name in [(c,'inverseCube'),(q19,'qPower19'),(q38,'qPower38'),(q79,'qPower79')]:names[sid]=f'detector{d}.{name}'
  edits[f'detector{d}.toric.c.definition']={(0,tuple(sorted((c,q4)))):1,(0,(q,)):-1}
  edits[f'detector{d}.toric.q10.definition']={(0,tuple(sorted((c,q19)))):1,(0,(q8,q8)):-1}
  edits[f'detector{d}.toric.q40.definition']={(0,tuple(sorted((c,q79)))):1,(0,(q38,q38)):-1}
  remove.update(f'detector{d}.toric.{label}.definition' for label in ('a','b','d'))
  if baseline==301:
   newcoords.append({'sourceId':q8,'name':f'mixed.det{d}.q1Power8','kind':'gate'})
   newrows.append(({'sourceId':q8,'name':f'mixed.det{d}.q1Power8.definition'},{(0,(q4,q4)):1,(0,(q8,)):-1}))
 coords=[dict(c,id=i+1,name=names.get(c['sourceId'],c['name'])) for i,c in enumerate(c for c in old['coordinates'] if c['sourceId'] not in deleted)]
 for c in newcoords:coords.append(dict(c,id=len(coords)+1))
 mapping={c['sourceId']:c['id'] for c in coords};rows=[];coefs=defaultdict(int);changed=[];removed=[];assembled=[]
 for row in old['residuals']:
  if row['name'] in remove:removed.append(row['sourceId']);continue
  poly={(t['parameterPower'],tuple(sorted(lookup[i] for i in t['monomial']))):int(t['coefficient']) for t in row['terms']}
  name=row['name']
  if name in edits:
   poly=edits.pop(name);changed.append(row['sourceId'])
   label='inverseCube' if '.toric.c.' in name else ('qPower19' if '.toric.q10.' in name else 'qPower79')
   name=name.split('.')[0]+'.'+label+'.definition'
  elif 'E10.power2.definition' in name:name=name.split('.')[0]+'.qPower38.definition'
  assembled.append((dict(row,name=name),poly))
 assert not edits
 assembled.extend(newrows)
 for metadata,poly in assembled:
  if poly[min(poly)]<0:poly={m:-c for m,c in poly.items()}
  assert all(i not in deleted for (a,m) in poly for i in m)
  transported={(a,tuple(sorted(mapping[i] for i in m))):c for (a,m),c in poly.items()}
  rows.append(dict(metadata,terms=[{'parameterPower':a,'monomial':list(m),'coefficient':str(c)} for (a,m),c in sorted(transported.items())]))
  for (a,m),c in transported.items():
   for (b,n),d in transported.items():coefs[a+b,tuple(sorted(m+n))]+=c*d
 coefs={m:c for m,c in coefs.items() if c};assert len(coords)==number
 assert len(rows)==len(old['residuals'])-(baseline-number)
 ordinary=defaultdict(dict)
 for (a,m),c in coefs.items():ordinary[m][a]=c
 maxsum=max(sum(abs(c) for c in p.values()) for p in ordinary.values())
 system=dict(old,format='integer-quadratic-family-v5',variables=number,source={'construction':f'quartic-family{baseline}','sha256':PINS[baseline]},coordinates=coords,residuals=rows)
 polynomial={'format':'integer-quartic-family-v5','variables':number,'degree':4,'inputCoordinate':1,'fixedParameter':old['fixedParameter'],'coordinates':coords,'terms':[{'parameterPower':a,'monomial':list(m),'coefficient':str(c)} for (a,m),c in sorted(coefs.items())]}
 report={'status':'Exact coefficient specification; projection theorem has stated arithmetic dependencies.','baselineVariables':baseline,'variables':number,'quadraticResiduals':len(rows),'degree':4,'symbolicTerms':len(coefs),'ordinaryMonomialsForNAtLeast27464':len(ordinary),'sourceSha256':PINS[baseline],'removedSourceCoordinates':sorted(deleted),'newSourceCoordinates':[c['sourceId'] for c in newcoords],'removedSourceRows':removed,'modifiedSourceRows':changed,'replacementWeights':{'q1':'1/(R*delta^4)','inverseCube':'q1^(-3)','q10':'q1^19','q40':'q1^79'},'quadraticWeightRelations':['q2=q1^2','q4=q2^2','c*q4=q1','q8=q4^2','c*q19=q8^2','q38=q19^2','c*q79=q38^2'],'heightBound':{'coefficientSumBitLength':maxsum.bit_length(),'formula':f'H(P_N)<2^{maxsum.bit_length()}*80989^(4*N+2)'},'effectiveness':'Ineffective eventual parameter' if baseline==301 else 'Every N>=27464; specified member A=80989^54929'}
 out=output_root/f'family{number}';out.mkdir(exist_ok=True,parents=True)
 for file,data in [(f'quadratic-family{number}.json',system),(f'polynomial-family{number}.json',polynomial),(f'construction-report{number}.json',report)]:
  (out/file).write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=DEFAULT_SOURCE);p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args()
 for n in (301,351):run(n,a.source_root,a.output_root)
