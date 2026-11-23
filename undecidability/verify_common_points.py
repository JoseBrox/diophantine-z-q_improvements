#!/usr/bin/env python3
"""Read-only exact audit of the two common-point quadratic checkpoints.

Counts, maps, substitutions, duplicate rows and complete output bytes are
checked here. Arithmetic completeness is proved in the companion paper
under retained source interfaces; U_em remains explicitly unverified.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import hashlib,json,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'undecidability/code'))
from build_common_points import build

# Independent physical-pair census, written as first indices of field pairs.
REF=[15,17,19,64,150]
PAIRS={163:REF+[23,33,54,102,182,184,186,194,213,215,221,225,227,233,235,39,43,41,46,48,201,205],
       179:REF+[33,102,182,184,186,213,215,217,221,225,227,231,233,39,43,41,46,48,201,205]}
CONTACT_ONE=set(j for first in [15,17,19,64,150,23,33,54,39,43,41,46,48]for j in [first,first+1])
for m,n,q,s,removed in [(163,1601,1599,54,176),(179,1837,1811,50,132)]:
 folder=ROOT/'undecidability/coefficients/jones1980_common_points'
 path=folder/f'common_points_m{m}_quadrics.json'
 raw=path.read_bytes();new=json.loads(raw)
 certificate=json.loads((folder/f'common_points_m{m}_certificate.json').read_bytes())
 rebuilt,rebuilt_cert=build(m,ROOT)
 assert raw==(json.dumps(rebuilt,separators=(',',':'),sort_keys=True)+'\n').encode()
 rebuilt_cert['table_sha256']=hashlib.sha256(raw).hexdigest()
 assert certificate==rebuilt_cert
 assert new['variables']==n and len(new['residuals'])==q
 assert len(new['variable_names'])==len(set(new['variable_names']))==n
 assert len(set(r['name']for r in new['residuals']))==q
 assert new['common_point_shared_coordinates']==s
 assert len(new['common_point_duplicate_rows_removed'])==removed
 for doc in [new,certificate]:
  assert doc['source_universality_hypothesis']=='U_em'
  assert doc['source_universality_verified']is False
  assert doc['unconditional_undecidability_claim']is False
  assert doc['common_input_numerator']is True
 source_labels=sorted(j for first in PAIRS[m]for j in [first,first+1])
 assert len(source_labels)==len(set(source_labels))==s
 assert source_labels==sorted(j for group in new['common_point_source_labels'].values()for j in group)
 maps=json.loads((ROOT/f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
 for j in source_labels:
  assert maps['c_weights'][str(j)]==(1 if j in CONTACT_ONE else 0),(m,j)
  assert maps['R_weights'][str(j)]==0,(m,j)
  assert maps['parameter_weights'][str(j)]==(-1 if j in [33,34,54,55]else 0),(m,j)
 slots=[maps['source_labels'][str(j)]for j in source_labels]
 old_path=ROOT/f'undecidability/coefficients/jones1980_shared_reciprocal/reciprocal_reference_m{m}_quadrics.json'
 old_bytes=old_path.read_bytes();old=json.loads(old_bytes)
 assert new['common_point_baseline_sha256']==hashlib.sha256(old_bytes).hexdigest()
 old_names=old['variable_names'];new_names=new['variable_names'];new_id={name:j+1 for j,name in enumerate(new_names)}
 blocks=old['ordinary_integer_inputs']+['i_reciprocal']
 renaming={f'int_{b}_{j}':f'int_b_{j}'for b in blocks if b!='b'for j in slots}
 def transformed(row):
  acc=defaultdict(lambda:sp.Integer(0))
  for term in row['terms']:
   names=[renaming.get(old_names[j-1],old_names[j-1])for j in term['monomial']]
   mon=tuple(sorted(new_id[name]for name in names))
   acc[mon]+=sp.sympify(term['coefficient'])
  return [{'monomial':list(mon),'coefficient':str(value)}for mon,value in sorted(acc.items())if value]
 new_rows={r['name']:r for r in new['residuals']}
 deleted={r['name']:r['identical_to']for r in new['common_point_duplicate_rows_removed']}
 assert len(deleted)==removed
 assert set(new_rows)|set(deleted)=={r['name']for r in old['residuals']}
 assert not set(new_rows)&set(deleted)
 for row in old['residuals']:
  name=row['name'];expected=transformed(row)
  retained=deleted.get(name,name)
  assert expected==new_rows[retained]['terms'],(m,name,retained)
 # Every rational coordinate occurs and every coefficient is an integer
 # polynomial in the declared coefficient parameters.
 assert {j for r in new['residuals']for t in r['terms']for j in t['monomial']}==set(range(1,n+1))
 assert max(len(t['monomial'])for r in new['residuals']for t in r['terms'])==2
 params=set(map(sp.Symbol,new['parameters']))
 for row in new['residuals']:
  for term in row['terms']:
   a=sp.sympify(term['coefficient']);assert a.free_symbols<=params
   if a.free_symbols:assert sp.Poly(a,*sorted(a.free_symbols,key=str)).domain==sp.ZZ
   else:assert a.is_Integer
 # Count independently from the 251-coordinate/219-row optimized outer core.
 assert n==251+12*(m-1)-s*11
 assert q==219+12*({163:137,179:151}[m])-({163:24,179:20}[m])*11
 print(f'm={m}: PASS, {n} coordinates, {q} quadratic rows, {s} common coordinates; U_em remains unverified')
