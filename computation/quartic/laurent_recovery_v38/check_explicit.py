#!/usr/bin/env python3
"""Independent replay of both coordinate deletions and the explicit height.

No producer module is imported. Retained inverse equations exclude all
zero-boundary components. The parent's arithmetic threshold is unchanged.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import argparse,copy,hashlib,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pol(terms):
 p=defaultdict(F)
 for t in terms:p[int(t['parameterPower']),tuple(sorted(t['monomial']))]+=F(t['coefficient'])
 return {k:v for k,v in p.items() if v}
def translate(terms,powers,weights,constant,rename=None):
 p=defaultdict(F)
 for t in terms:
  m=[];ex=0;c=F(t['coefficient'])
  for v in t['monomial']:
   i=rename[v] if rename else v;c*=constant.get(i,F(1));ex+=powers.get(i,weights.get(i,0))
   if i not in powers:m.append(i)
  p[t['parameterPower'],tuple(sorted(m)),ex]+=c
 return {k:v for k,v in p.items() if v}
def expand(rows):
 p=defaultdict(F)
 for row in rows:
  ts=list(pol(row['terms']).items())
  for i,((a,m),c) in enumerate(ts):
   for j in range(i,len(ts)):
    (b,n),d=ts[j];p[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
 return {k:v for k,v in p.items() if v}
def step(src,target,cert,quartic,number):
 need(src['variables']==number+1 and target['variables']==number,'coordinate counts')
 need(len(src['residuals'])-len(target['residuals'])==1,'row count')
 need(target['inputCoordinate']==src['inputCoordinate']==1,'input unchanged')
 power={int(k):v[0] for k,v in cert['powers'].items()};weight={int(k):v[0] for k,v in cert['weights'].items()};constant={int(k):F(v) for k,v in cert['constants'].items()}
 need(1 not in power and 1 not in weight and not constant,'input and constants')
 n={c['name']:c['id'] for c in src['coordinates']};sr={r['name']:r for r in src['residuals']};tr={r['name']:r for r in target['residuals']};j=259-number;pref=f'detector{j}.'
 q,w,w2,w4=[n[pref+s] for s in ['q1','inverseWeight','inverseWeightSquared','inverseWeightFourthPower']]
 need(power=={q:-1,w:1,w2:2,w4:4},'powers')
 need(cert['deleted_coordinates']==[w4] and cert['deleted_rows']==[pref+'inverseWeightFourthPower.definition'],'deletion')
 need(pol(sr[pref+'inverseWeight.definition']['terms'])=={(0,()):F(1),(0,tuple(sorted((q,w)))):F(-1)},'source unit guard')
 need(pol(sr[pref+'inverseWeightSquared.definition']['terms'])=={(0,(w,w)):F(1),(0,(w2,)):F(-1)},'source square guard')
 need(pol(sr[pref+'inverseWeightFourthPower.definition']['terms'])=={(0,(w2,w2)):F(1),(0,(w4,)):F(-1)},'unique deleted coordinate definition')
 ren={int(k):v for k,v in cert['old_to_new'].items()};inv={v:k for k,v in ren.items()}
 need(len(ren)==number and set(ren)==set(range(1,number+2))-{w4},'coordinate bijection')
 need([c['id'] for c in target['coordinates']]==list(range(1,number+1)),'target ordering')
 need(all(c['parent_id']==inv[c['id']] for c in target['coordinates']),'parent coordinates')
 for name in cert['guard_rows']:
  old={(a,tuple(sorted(ren[i] for i in m))):c for (a,m),c in pol(sr[name]['terms']).items()}
  need(old==pol(tr[name]['terms']),'retained literal guard')
 for name in cert['deleted_rows']:need(not translate(sr[name]['terms'],power,weight,constant),'deleted identity')
 need(set(sr)-set(tr)==set(cert['deleted_rows']),'coverage')
 need(len(cert['rows'])==len(tr) and len({r['source_row'] for r in cert['rows']})==len(tr),'certificate coverage')
 for r in cert['rows']:
  a=src['residuals'][r['source_row']-1];b=target['residuals'][r['target_row']-1];need(a['name']==b['name'],'row matching')
  mul=F(r['primitive_multiplier']);need(mul!=0,'nonzero multiplier')
  old={(a,m,e-r['division_exponents'][0]):c*mul for (a,m,e),c in translate(a['terms'],power,weight,constant).items()}
  need(old==translate(b['terms'],power,{}, {},inv),'exact Laurent identity '+b['name'])
  need(all(len(m)<=2 and c.denominator==1 for (a,m),c in pol(b['terms']).items()),'primitive integral quadrics')
 need(expand(target['residuals'])==pol(quartic['terms']),'all quartic coefficients')
 return dict(parent_variables=number+1,variables=number,rows=len(tr),identities=len(tr),nonzero_unit=f'w{j}',dropped_row=cert['deleted_rows'][0])
def balance(src,s,b,cert):
 w={int(k):v for k,v in cert['weights'].items()};constants={int(k):F(v) for k,v in cert['constants'].items()}
 need(w[1]==0 and all(constants.values()),'balanced invertible input-preserving map')
 need(len(s['residuals'])==len(src['residuals'])==len(cert['rows'])==230,'balanced row count')
 for old,new,r in zip(src['residuals'],s['residuals'],cert['rows']):
  p=defaultdict(F)
  for (a,m),c in pol(old['terms']).items():
   for i in m:c*=constants.get(i,F(1))
   e=2*a+sum(w[i] for i in m)-r['division_power'];need(e>=0,'parameter power');p[e,m]+=c*149**a*F(r['primitive_multiplier'])
  need(dict(p)==pol(new['terms']),'balance identity '+old['name'])
 full=expand(s['residuals']);need(full==pol(b['terms']),'balanced all coefficients')
 need(max(len(m) for a,m in full)==4 and {i for a,m in full for i in m}==set(range(1,259)),'degree and occurrence')
 need(all(c.denominator==1 for c in full.values()),'integral coefficients')
 ps=defaultdict(dict)
 for (a,m),c in full.items():ps[m][a]=int(c)
 need(ps[(1,1,1,1)]=={0:1},'content one')
 height=95883264;C=149**9682;constant_max=max(abs(c) for p in ps.values() for a,c in p.items() if a==0)
 need(any(p=={2:height} for p in ps.values()),'height attained')
 need(any(p=={0:constant_max} or p=={0:-constant_max} for p in ps.values()),'fixed height attained')
 need(height*149**22<constant_max<height*149**24,'coefficient crossover 12')
 for p in ps.values():
  top=max(p);need(abs(p[top])*149**top>sum(abs(c)*149**a for a,c in p.items() if a<top),'nonzero for every N>=1')
  need(sum(abs(c)*149**(11*a) for a,c in p.items())<=constant_max,'height below crossover')
  need(sum(abs(c)*149**(12*a) for a,c in p.items())<=height*149**24,'height above crossover')
 need((height*C*C).bit_length()==139819,'bit length')
 return dict(variables=258,rows=230,degree=4,content_for_every_N_ge_1=1,monomials_for_every_N_ge_1=len(ps),parameter_separated_terms=len(full),certified_defining_exponent=9682,exact_height='max(fixed_coefficient_max,95883264*149^(2N)) for N>=1',coefficient_crossover=12,exact_height_for_N_ge_9682='95883264*149^(2N)',largest_coefficient_binary_digits_at_9682=139819,fixed_coefficient_max=str(constant_max),old_largest_coefficient_binary_digits=279599)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args();reports=[];neg=[]
 for n in [259,258]:
  cfg=json.loads((HERE/f'config{n}.json').read_text());raw=(ROOT/cfg['source']).read_bytes();need(hashlib.sha256(raw).hexdigest()==cfg['source_sha256'],'parent hash')
  src=json.loads(raw);folder=HERE/f'family{n}';objects=[json.loads((folder/f).read_text()) for f in ['quadratic.json','certificate.json','polynomial.json']]
  need({k:objects[1][k] for k in cfg}==cfg,'pinned coordinate map');reports.append(step(src,*objects,n))
  for kind in ['row','shift','quartic','guard']:
   bad=copy.deepcopy(objects)
   if kind=='row':bad[0]['residuals'][10]['terms'][0]['coefficient']=str(F(bad[0]['residuals'][10]['terms'][0]['coefficient'])+1)
   elif kind=='shift':bad[1]['rows'][10]['division_exponents'][0]+=1
   elif kind=='quartic':bad[2]['terms'][0]['coefficient']=str(F(bad[2]['terms'][0]['coefficient'])+1)
   else:bad[0]['residuals']=[r for r in bad[0]['residuals'] if r['name']!=cfg['guard_rows'][0]]
   try:step(src,*bad,n)
   except (ValueError,KeyError,IndexError):neg.append(str(n)+':'+kind)
   else:raise ValueError('negative control accepted')
 final=objects[0];items=[json.loads((HERE/'family258'/f).read_text()) for f in ['balanced-quadratic.json','balanced-polynomial.json','balancing.json']];report=balance(final,*items)
 with tempfile.TemporaryDirectory() as tmp:
  subprocess.run([sys.executable,'-B',str(HERE/'build_explicit.py'),'--output',tmp],check=True,stdout=subprocess.DEVNULL)
  for n in [259,258]:
   for p in (HERE/f'family{n}').glob('*.json'):need(p.read_bytes()==(Path(tmp)/f'family{n}'/p.name).read_bytes(),'regeneration '+str(p))
 result=dict(schema='independent-explicit258/v38',status='PASS',**report,steps=reports,negative_controls_rejected=neg,scope='Exact all-parameter projection equivalence and coefficients, conditional defining theorem inherited unchanged from explicit260. No new arithmetic height estimate or 233-variable result.',independent_mathematical_review=False)
 if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
