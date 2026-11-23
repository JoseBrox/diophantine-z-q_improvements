#!/usr/bin/env python3
"""Build the common-point quadratic checkpoint with 1601/1837 coordinates.

Finite algebra only: the paper proves joint completeness under the retained
arithmetic interfaces, including the all-sign order supplier. Undecidability
still requires the unresolved source-universality hypothesis U_em.
"""
from pathlib import Path
from collections import defaultdict
import argparse,json,hashlib
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
H=[15,16,17,18,19,20,64,65,150,151]
COMMON={
 163:{'reference':H,'scalar_pair':[23,24,33,34,54,55,102,103,*range(182,188),194,195],
  'lucas_pair_3':[*range(213,217),221,222],'lucas_pair_4':[*range(225,229),*range(233,237)],
  'cross_errors':[39,40,43,44],'lucas_expressions':[41,42,*range(46,50)],'input_numerator':[201,202,205,206]},
 179:{'reference':H,'scalar_pair':[33,34,102,103,*range(182,188)],
  'lucas_pair_3':[*range(213,219),221,222],'lucas_pair_4':[*range(225,229),*range(231,235)],
  'cross_errors':[39,40,43,44],'lucas_expressions':[41,42,*range(46,50)],'input_numerator':[201,202,205,206]}}

def build(m,root=ROOT):
 base=root/f'undecidability/coefficients/jones1980_shared_reciprocal/reciprocal_reference_m{m}_quadrics.json'
 raw=base.read_bytes();d=json.loads(raw)
 assert d['source_universality_hypothesis']=='U_em'
 assert d['source_universality_verified'] is False
 assert d['unconditional_undecidability_claim'] is False
 maps=json.loads((root/f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
 labels=sorted(i for group in COMMON[m].values()for i in group)
 assert len(set(labels))==len(labels)==(54 if m==163 else 50)
 physical_c={j:(1 if j in H+[23,24,33,34,54,55,39,40,43,44,41,42,*range(46,50)] else 0) for j in labels}
 for j in labels:
  assert maps['c_weights'][str(j)]==physical_c[j],(j,'c')
  assert maps['R_weights'][str(j)]==0,(j,'R')
  assert maps['parameter_weights'][str(j)]==(-1 if j in [33,34,54,55] else 0),(j,'C')
 slots=[maps['source_labels'][str(j)]for j in labels]
 refs=d['shared_reference_ids'];freshslots=[j for j in slots if j not in refs]
 blocks=d['ordinary_integer_inputs']+['i_reciprocal']
 rename={f'int_{b}_{j}':f'int_b_{j}'for b in blocks if b!='b'for j in freshslots}
 names=d['variable_names'];assert set(rename)<=set(names)
 newnames=[n for n in names if n not in rename];newid={n:j+1 for j,n in enumerate(newnames)}
 newrefids={newid[f'int_b_{j}']for j in slots}
 rows=[];canonical={};duplicates=[]
 for row in d['residuals']:
  acc=defaultdict(lambda:sp.Integer(0))
  for t in row['terms']:
   mon=tuple(sorted(newid[rename.get(names[j-1],names[j-1])] for j in t['monomial']))
   acc[mon]+=sp.sympify(t['coefficient'])
  terms=[{'monomial':list(mon),'coefficient':str(c)}for mon,c in sorted(acc.items())if c]
  assert terms
  key=json.dumps(terms,sort_keys=True)
  if row['name'].startswith('integer.') and all(set(t['monomial'])<=newrefids for t in terms):
   if key in canonical:duplicates.append({'name':row['name'],'identical_to':canonical[key]});continue
   canonical[key]=row['name']
  rows.append({'name':row['name'],'terms':terms})
 assert len(newnames)==d['variables']-11*len(freshslots)
 assert {j for r in rows for t in r['terms']for j in t['monomial']}==set(range(1,len(newnames)+1))
 ans=dict(d)
 ans.update({'variables':len(newnames),'variable_names':newnames,'residuals':rows,
   'common_point_source_labels':COMMON[m], 'common_point_stored_slots':slots,
   'common_point_shared_coordinates':len(slots),'common_point_additional_saved':11*len(freshslots),
   'common_point_duplicate_rows_removed':duplicates,
   'common_point_baseline_sha256':hashlib.sha256(raw).hexdigest(),
   'common_point_completeness_status':'proved in common_points_quartic_checkpoint.tex under retained arithmetic interfaces; finite verification does not prove those interfaces',
   'common_input_numerator':True,
   'common_input_numerator_source_labels':[201,202,205,206],
   'common_point_paper':'undecidability/papers/common_points_quartic_checkpoint.tex',
   'common_point_all_sign_order_source':'undecidability/papers/common_numerator_transfers.tex, section The common-index Chinese remainder theorem',
   'common_point_weight_audit':{str(j):{'stored_slot':maps['source_labels'][str(j)],'contact_weight':maps['c_weights'][str(j)],'normalizer_weight':maps['R_weights'][str(j)],'parameter_weight':maps['parameter_weights'][str(j)]}for j in labels}})
 cert={k:v for k,v in ans.items()if k not in ['variable_names','residuals','power_chain']}
 cert['quadratic_residuals']=len(rows)
 cert['verified']=['complete predecessor table by hash','physical-to-stored contact, normalizer, and parameter weights for every identified coordinate','each omitted row literally equals its retained counterpart','complete materialized quadratic table and coordinate support','exact coordinate and row counts']
 cert['not_verified']=['U_em: universality of the exact emended source','external arithmetic premises','minimality of the variable count']
 return ans,cert

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--repo',type=Path,default=ROOT)
 ap.add_argument('--out',type=Path,default=ROOT/'undecidability/coefficients/jones1980_common_points')
 args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 for m in (163,179):
  d,cert=build(m,args.repo)
  p=args.out/f'common_points_m{m}_quadrics.json';p.write_text(json.dumps(d,separators=(',',':'),sort_keys=True)+'\n')
  cert['table_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
  (args.out/f'common_points_m{m}_certificate.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
  print(json.dumps({'m':m,'N':d['variables'],'rows':len(d['residuals']),'shared':d['common_point_shared_coordinates'],'new_duplicate_rows':len(d['common_point_duplicate_rows_removed']),'sha256':cert['table_sha256']}))
if __name__=='__main__':main()
