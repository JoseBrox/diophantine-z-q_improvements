#!/usr/bin/env python3
"""Independent exact replay of the 198 -> 196 map and all coefficients.

Does not import the producer. All checks use explicit exceptions. The finite
identities below establish the rational isomorphism; the arithmetic theorem
for the parent remains a separately stated premise.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import gcd
import argparse, copy, hashlib, json, tempfile, subprocess, sys
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sparse(terms):
 out=defaultdict(F)
 for t in terms:out[(int(t['parameterPower']),tuple(sorted(t['monomial'])))]+=F(t['coefficient'])
 return {k:v for k,v in out.items() if v}
def laurent(terms,powers,weights,constants,rename=None):
 out=defaultdict(F)
 for t in terms:
  value=F(t['coefficient']);m=[];e=[0,0,0]
  for ind in t['monomial']:
   i=rename[ind] if rename else ind
   value*=constants.get(i,F(1))
   if i not in powers:m.append(i)
   vec=powers.get(i,weights.get(i,(0,0,0)))
   for k in range(3):e[k]+=vec[k]
  out[(int(t['parameterPower']),tuple(sorted(m)),tuple(e))]+=value
 return {k:v for k,v in out.items() if v}
def coefficients(rows):
 out=defaultdict(F)
 for row in rows:
  terms=list(sparse(row['terms']).items())
  for i,((a,m),c) in enumerate(terms):
   for j in range(i,len(terms)):
    (b,n),d=terms[j];out[(a+b,tuple(sorted(m+n)))]+=(1 if i==j else 2)*c*d
 return {k:v for k,v in out.items() if v}
def literal(row,expected):
 need(sparse(row['terms'])=={k:F(v) for k,v in expected.items()},'literal guard mismatch: '+row['name'])
def audit(src,sysm,cert,poly,balanced,bpoly,bal):
 cfg=json.loads((HERE/'config196.json').read_text())
 need({k:cert[k] for k in cfg}==cfg,'config/certificate mismatch')
 names={c['name']:c['id'] for c in src['coordinates']};sr={r['name']:r for r in src['residuals']};tr={r['name']:r for r in sysm['residuals']}
 need(len(names)==198 and len(sr)==184,'parent dimensions')
 need(sysm['variables']==196 and len(sysm['coordinates'])==196 and len(tr)==182,'target dimensions')
 need([c['id'] for c in sysm['coordinates']]==list(range(1,197)),'coordinate ordering')
 need(sysm['inputCoordinate']==1 and names['input']==1,'input coordinate')
 ren={int(k):v for k,v in cert['old_to_new'].items()};inv={v:k for k,v in ren.items()}
 need(len(ren)==196 and len(inv)==196,'bijection')
 need(all(c['parent_id']==inv[c['id']] and c['name']==src['coordinates'][inv[c['id']]-1]['name'] for c in sysm['coordinates']),'coordinate names')
 powers={int(k):tuple(v) for k,v in cert['powers'].items()};weights={int(k):tuple(v) for k,v in cert['weights'].items()};constants={int(k):F(v) for k,v in cert['constants'].items()}
 need(all(constants.values()) and 1 not in powers and 1 not in weights and 1 not in constants,'nonzero diagonal / input fixed')
 R=names['scalar.forced_positive_parameter'];R2=names['scalar.r_power_2'];J=names['scalar.contactProduct'];u=names['inputSquare.quadratic'];v=names['scalar.rPair1.quadratic'];sort=lambda *i:tuple(sorted(i))
 literal(sr['inputSquare.definition'],{(0,(1,1)):1,(0,(u,)):-1})
 literal(sr['scalar.rPair1.definition'],{(0,()):6255001,(0,(u,)):255102,(0,(u,u)):2601,(0,(v,)):-4})
 literal(sr['scalar.four_contact_product.definition'],{(0,()):14315517724,(0,(u,)):291790992,(0,sort(u,v)):15531948,(0,(v,)):767410608,(0,(v,v)):-512,(0,sort(J,R)):1})
 literal(sr['scalar.forced_prime.definition'],{(0,()):1,(0,sort(J,R)):22201,(1,(J,)):-1})
 literal(sr['scalar.r_power_2.definition'],{(0,(R2,)):1,(0,(R,R)):-1})
 need(powers[R]==(1,0,0) and powers[R2]==(2,0,0),'scalar powers')
 X=sp.Symbol('X');uu=X**2;vv=(6255001+255102*uu+2601*uu**2)/4
 product=-14315517724-291790992*uu-15531948*uu*vv-767410608*vv+512*vv**2
 fact=(51*X**2+103)*(51*X**2+2503)*(51*X**2+2504)*(1632*X**2+80471)
 need(sp.expand(product-fact)==0,'positive scalar contact product')
 for j in range(2):
  q,w,w2,w4=[names[f'detector{j}.'+s] for s in ['q1','inverseWeight','inverseWeightSquared','inverseWeightFourthPower']]
  literal(sr[f'detector{j}.inverseWeight.definition'],{(0,()):1,(0,sort(q,w)):-1})
  literal(sr[f'detector{j}.inverseWeightSquared.definition'],{(0,(w,w)):1,(0,(w2,)):-1})
  literal(sr[f'detector{j}.inverseWeightFourthPower.definition'],{(0,(w2,w2)):1,(0,sort(R,w4) if j else (w4,)):-1})
  for i,a in [(q,-1),(w,1),(w2,2),(w4,4)]:
   e=[-j if i==w4 else 0,0,0];e[j+1]=a;need(powers[i]==tuple(e),'detector powers')
  need(w4 in cert['deleted_coordinates'],'deleted fourth power')
 # These nine relations survive literally, not just up to an unverified division.
 for name in cfg['guard_rows']:
  need(name in tr,'missing nonzero guard '+name)
  expected={(a,tuple(sorted(ren[i] for i in m))):c for (a,m),c in sparse(sr[name]['terms']).items()}
  need(sparse(tr[name]['terms'])==expected,'changed nonzero guard '+name)
 deleted=set(cert['deleted_rows']);need(set(sr)-set(tr)==deleted,'exact row coverage')
 need(len(cert['rows'])==182 and len({r['source_row'] for r in cert['rows']})==182,'certificate coverage')
 for name in deleted:need(not laurent(sr[name]['terms'],powers,weights,constants),'deleted row not identity')
 for entry in cert['rows']:
  old=src['residuals'][entry['source_row']-1];new=sysm['residuals'][entry['target_row']-1]
  need(old['name']==new['name'],'row names')
  lp=laurent(old['terms'],powers,weights,constants);shift=entry['division_exponents'];mul=F(entry['primitive_multiplier'])
  need(mul!=0,'zero row multiplier')
  lp={(a,m,tuple(e[i]-shift[i] for i in range(3))):c*mul for (a,m,e),c in lp.items()}
  need(lp==laurent(new['terms'],powers,{}, {},inv),'row replay '+old['name'])
  need(all(len(t['monomial'])<=2 and F(t['coefficient']).denominator==1 for t in new['terms']),'integer quadrics')
 raw=coefficients(sysm['residuals']);need(raw==sparse(poly['terms']),'unbalanced expansion')
 # Fixed coefficient balancing is checked directly, without using producer functions.
 ww={int(k):v for k,v in bal['weights'].items()};need(ww[1]==0 and set(ww)==set(range(1,197)),'balancing weights')
 need(len(bal['rows'])==182 and len(balanced['residuals'])==182,'balancing rows')
 for old,new,entry in zip(sysm['residuals'],balanced['residuals'],bal['rows']):
  out=defaultdict(F)
  for (a,m),c in sparse(old['terms']).items():out[(2*a+sum(ww[i] for i in m)-entry['division_power'],m)]+=c*149**a*F(entry['primitive_multiplier'])
  need(dict(out)==sparse(new['terms']),'balancing replay '+old['name'])
  need(all(k>=0 for k,m in out),'negative coefficient parameter exponent')
 full=coefficients(balanced['residuals']);need(full==sparse(bpoly['terms']),'balanced expansion')
 need(max(len(m) for a,m in full)==4 and {i for a,m in full for i in m}==set(range(1,197)),'exact degree and occurrence')
 need(all(c.denominator==1 for c in full.values()),'integral quartic')
 profiles=defaultdict(dict)
 for (a,m),c in full.items():profiles[m][a]=int(c)
 need(profiles[(1,1,1,1)]=={0:1},'content-one witness')
 need(max(a for a,m in full)==2,'coefficient parameter degree')
 height=max(abs(c) for (a,m),c in full.items() if a==2)
 need(any(p=={2:height} or p=={2:-height} for p in profiles.values()),'attained height')
 # Each coefficient is at most height*C^2 for every C>=149.
 for m,p in profiles.items():
  need(sum(abs(c)*149**a for a,c in p.items())<=height*149**2,'height upper envelope')
  a=max(p)
  need(abs(p[a])*149**a>sum(abs(c)*149**b for b,c in p.items() if b<a),'nonvanishing coefficient profile')
 return dict(variables=196,quadratic_rows=182,degree=4,content_for_every_parameter=1,monomials_for_every_N_ge_1=len(profiles),parameter_separated_terms=len(full),height_constant=str(height),exact_height='height_constant*149^(2N) for every N>=1',unchanged_guard_rows=len(cfg['guard_rows']),exact_laurent_identities=182,deleted_identity_rows=2,balancing_identities=182,projection_equivalence='Every fixed N>=1; entire rational input projection, with explicit inverse maps.',sufficient_defining_threshold='Identical to parent 198 family; ineffective, not N=1.')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
 cfg=json.loads((HERE/'config196.json').read_text());raw=(ROOT/cfg['source']).read_bytes();need(hashlib.sha256(raw).hexdigest()==cfg['source_sha256'],'parent source SHA')
 src=json.loads(raw);folder=HERE/'family196';names=['quadratic.json','certificate.json','polynomial.json','balanced-quadratic.json','balanced-polynomial.json','balancing.json'];objects=[json.loads((folder/n).read_text()) for n in names]
 result=audit(src,*objects);negative=[]
 for name in ['row coefficient','division exponent','quartic coefficient','deleted weight','guard row']:
  bad=copy.deepcopy(objects)
  if name=='row coefficient':bad[0]['residuals'][10]['terms'][0]['coefficient']=str(F(bad[0]['residuals'][10]['terms'][0]['coefficient'])+1)
  elif name=='division exponent':bad[1]['rows'][10]['division_exponents'][1]+=1
  elif name=='quartic coefficient':bad[4]['terms'][0]['coefficient']=str(F(bad[4]['terms'][0]['coefficient'])+1)
  elif name=='deleted weight':bad[1]['powers'][str(cfg['deleted_coordinates'][0])][1]-=1
  else:bad[0]['residuals']=[r for r in bad[0]['residuals'] if r['name']!='detector0.inverseWeight.definition']
  try:audit(src,*bad)
  except (ValueError,KeyError,IndexError):negative.append(name)
  else:raise ValueError('negative control accepted: '+name)
 with tempfile.TemporaryDirectory() as tmp:
  subprocess.run([sys.executable,'-B',str(HERE/'build.py'),'--output',tmp],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
  for n in names:need(Path(tmp,n).read_bytes()==(folder/n).read_bytes(),'non-reproducible '+n)
 report=dict(schema='independent-laurent196/v38',status='PASS',**result,negative_controls_rejected=negative,source_sha256=cfg['source_sha256'],scope='Exact algebraic equivalence, nonzero-guard identities and all coefficients; not an independent proof of the parent infinite arithmetic premises.',independent_mathematical_review=False)
 if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
