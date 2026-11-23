#!/usr/bin/env python3
"""Build common-reference variants from the pinned complete Jones tables.

This is a separate compiler: the independent-block tables are never modified.
Mathematical completeness uses the simultaneous-reference proof, not merely
the fact that the identified coordinates have equal source labels.
"""
from __future__ import annotations
import argparse, hashlib, json
from collections import defaultdict
from pathlib import Path
import sympy as sp
from quadratic_utils import SOURCES,rechart179

def build(m,repo,baseline):
 base_bytes=baseline.read_bytes();data=json.loads(base_bytes)
 assert data['integer_blocks']==12
 src=json.loads((repo/SOURCES[m]).read_text())
 if m==179:src,_=rechart179(src)
 if m==56:
  prefixes=('reference.primitive.',)
 else:prefixes=('sharedT.reference.','testSquare.40.0.')
 refrows=[r for r in src['residuals'] if r['name'].startswith(prefixes)]
 refids=sorted({j for r in refrows for t in r['terms'] for j in t['monomial']})
 assert 1 not in refids
 assert len(refids)==(6 if m==56 else 10)
 assert len(refrows)==(4 if m==56 else 8)
 oldnames=data['variable_names'];oldid=dict(enumerate(oldnames,1))
 ordinary=data['ordinary_integer_inputs'];labels=ordinary+['i_reciprocal']
 assert len(labels)==12 and ordinary[0]=='b'
 identified={f'int_{label}_{j}':f'int_b_{j}' for label in labels if label!='b' for j in refids}
 assert set(identified)<=set(oldnames)
 newnames=[v for v in oldnames if v not in identified]+['i']
 ids={v:j+1 for j,v in enumerate(newnames)}
 def target_name(name):return identified.get(name,name)
 def remap_terms(terms,names):
  acc=defaultdict(lambda:sp.Integer(0))
  for t in terms:
   mon=tuple(sorted(ids[target_name(names[j])] for j in t['monomial']))
   acc[mon]+=sp.sympify(t['coefficient'])
  result=[{'monomial':list(mon),'coefficient':str(sp.expand(a))} for mon,a in sorted(acc.items()) if a!=0]
  assert result
  assert max(len(t['monomial']) for t in result)<=2
  return result
 refnames={r['name'] for r in refrows}
 canonical={}
 rows=[];dropped=[]
 for r in data['residuals']:
  if r['name'].startswith('integer.i_reciprocal.'):continue
  terms=remap_terms(r['terms'],oldid)
  if r['name'].startswith('integer.'):
   _,label,name=r['name'].split('.',2)
   if name in refnames:
    if label=='b':canonical[name]=terms
    else:
     assert canonical[name]==terms,(label,name)
     dropped.append(r['name']);continue
  rows.append({'name':r['name'],'terms':terms})
 # Restore an ordinary input i=1/v so the reciprocal block's reference
 # coordinates have the same physical scale as the eleven other blocks.
 par=sp.Symbol('C_parameter') if m==163 else sp.Symbol('B_abc') if m==56 else sp.Integer(1)
 coords={1:'i',**{j:f'int_i_reciprocal_{j}' for j in range(2,m+1)}}
 for r in src['residuals']:
  literal=[{'monomial':t['monomial'],'coefficient':str(sp.Integer(t['coefficient'])*par**t.get('parameterPower',0))} for t in r['terms']]
  terms=remap_terms(literal,coords)
  if r['name'] in refnames:
   assert canonical[r['name']]==terms
   dropped.append('integer.i.'+r['name']);continue
  rows.append({'name':'integer.i.'+r['name'],'terms':terms})
 rows.append({'name':'integer.i_reciprocal.unit','terms':[
   {'monomial':[],'coefficient':'-1'},
   {'monomial':sorted([ids['i'],ids['i_inverse']]),'coefficient':'1'}]})
 assert len(dropped)==11*len(refrows)
 assert len(newnames)==data['variables']+1-11*len(refids)
 assert len(rows)==len(data['residuals'])+1-11*len(refrows)
 support={j for r in rows for t in r['terms'] for j in t['monomial']}
 assert support==set(range(1,len(newnames)+1))
 maximum_degree=max(len(t['monomial']) for r in rows for t in r['terms'])
 assert maximum_degree==2
 result=dict(data)
 result.update({
  'status':'conditional checkpoint: undecidability requires U_em and every retained arithmetic premise of the integer-defining interface',
  'source_universality':'U_em: universality of the exact emended positive-integer source; not independently verified',
  'source_universality_hypothesis':'U_em',
  'source_universality_verified':False,
  'unconditional_undecidability_claim':False,
  'source_reconciliation':'The 1980 display uses Greek alpha in the d row; the emendation uses Latin a, supported by the 1999 survey, whose separate Pell-row typo is also corrected. See the source reconciliation section of undecidability/papers/jones1980_quartic_transfer.tex.',
  'variables':len(newnames),'variable_names':newnames,'residuals':rows,
  'ordinary_integer_inputs':ordinary+['i'],'reciprocal_integer_inputs':[],
  'reciprocal_nonzero_guard':'i*i_inverse=1; the source value i equals the reciprocal of i_inverse',
  'outer_coordinates':data['outer_coordinates']+1,'outer_residuals':data['outer_residuals']+1,
  'baseline_table_sha256':hashlib.sha256(base_bytes).hexdigest(),
  'shared_reference_ids':refids,'shared_reference_rows':sorted(refnames),
  'shared_reference_blocks':12,'shared_reference_coordinates_saved':11*len(refids),
  'shared_reference_duplicate_rows_removed':len(dropped),
  'simultaneous_completeness_scope':'nonzero integer tuples; sufficient because original Jones witnesses have positive integer inputs' if m==56 else 'all integer tuples',
 })
 cert={k:v for k,v in result.items() if k not in ['variable_names','residuals','power_chain']}
 cert['quadratic_residuals']=len(rows)
 cert['verified']=['complete baseline table read by hash','ordinary replacement of reciprocal i block with i*i_inverse=1',
  'all identified coordinates matched to literal source references','each removed reference row identical to its retained copy',
  'quadratic degree and complete coordinate support','all modified rows materialized']
 cert['not_verified']=['U_em: universality of the exact emended source','external arithmetic premises','minimality of the total variable count']
 return result,cert

def main():
 ap=argparse.ArgumentParser();base=Path(__file__).resolve().parents[2]
 ap.add_argument('--repo',type=Path,default=base)
 ap.add_argument('--baseline',type=Path,default=base/'undecidability/coefficients/jones1980')
 ap.add_argument('--out',type=Path,default=base/'undecidability/coefficients/jones1980_shared')
 ap.add_argument('--m',nargs='+',type=int,choices=[163,179,56],default=[163,179,56]);args=ap.parse_args()
 args.out.mkdir(parents=True,exist_ok=True)
 for m in args.m:
  data,cert=build(m,args.repo.resolve(),args.baseline/f'jones1980_m{m}_quadrics.json')
  p=args.out/f'shared_reference_m{m}_quadrics.json';p.write_text(json.dumps(data,separators=(',',':'),sort_keys=True)+'\n')
  cert['table_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
  (args.out/f'shared_reference_m{m}_certificate.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
  print(json.dumps({'m':m,'N':data['variables'],'quadrics':len(data['residuals']),'sha256':cert['table_sha256']}))
if __name__=='__main__':main()
