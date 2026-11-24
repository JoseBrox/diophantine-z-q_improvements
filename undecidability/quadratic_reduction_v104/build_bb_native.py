#!/usr/bin/env python3
"""Replace every old non-CM private pole in the combined quartic systems."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PREDECESSORS={k:f'undecidability/quadratic_reduction_v103/denominator_{k}_quadrics.json' for k in ('general','specified')}
CHANGES={
 'first':{'3':'9','-34':None,'-289':'-9','17':'7'},
 'middle':{'17':'9','-1':'-7','-17':'-9'},
 'second':{'1':'9','34':None,'-867':'-9','-17':'-7'},
}

def part(name):
 if not name.startswith('integer.'):return None
 if '.detector' in name:
  return {'firstConic':'first','Bh.definition':'middle','secondConic':'second'}.get(name.split('.detector',1)[1].split('.',1)[1])
 if '.v82.scalar.' in name:
  return {'first':'first','middle':'middle','second':'second'}.get(name.rsplit('.',1)[1])
 return None

def build_data(old,interface):
 changed=[];rows=[];scopes=[]
 for row in old['residuals']:
  kind=part(row['name'])
  if kind is None:rows.append(row);continue
  coefficients={t['coefficient'] for t in row['terms']}
  assert coefficients==set(CHANGES[kind]),(row['name'],coefficients)
  terms=[{'coefficient':CHANGES[kind][t['coefficient']],'monomial':t['monomial']} for t in row['terms'] if CHANGES[kind][t['coefficient']] is not None]
  rows.append({'name':row['name'],'terms':terms});changed.append(row['name'])
  if kind=='first':scopes.append(row['name'].removesuffix('firstConic').removesuffix('first'))
 blocks=old['integer_blocks'];comparisons=2 if interface=='general' else 3
 assert len(changed)==3*blocks*(comparisons+1)
 new=dict(old)
 new['bb_native_historical_pole_metadata']={k:old[k] for k in ('integer_definition_source','integer_definition_source_sha256','retained_arithmetic_interfaces','simultaneous_completeness_scope') if k in old}
 new.update({'residuals':rows,
 'bb_native_proof':'undecidability/quadratic_reduction_v104/bb_native_combined.tex',
 'bb_native_reference':{'authors':'Manjul Bhargava and Ashay Burungale','title':'A Diophantine definition of Z in Q','version':'arXiv:2611.16130v2','result':'Theorem 2.3; prepared consequence related to Lemma 2.2','url':'https://arxiv.org/html/2611.16130v2'},
 'bb_native_physical_input':'d=7*b/9',
 'bb_native_physical_equations':['9*e^2-9+7*b*p^2=0','9*e-7*e*b-9*u*v=0','9*u^2-9*v^2-7*b*q^2=0'],
 'bb_native_changed_rows':changed,
 'bb_native_poles':blocks*(comparisons+1),
 'bb_native_comparison_poles':blocks*comparisons,
 'bb_native_scalar_poles':blocks,
 'bb_native_pole_prefixes':scopes,
 'bb_native_extra_preparation_prime':7,
 'bb_native_simultaneous_scalar_depth':'For fixed R_i, r_i=v_7(R_i), k_i=v_7(R_i*(R_i+9792)), choose one t>=max_i ceil((10*r_i-k_i)/4); choose common reference formal depths so r_i+4*d_w-2*t>=q and 4*d_w-O_7(1)>=q for every i,w. Then v_7(b_scalar_i)=k_i+4*t-10*r_i>=0.',
 'bb_native_simultaneous_comparison_limit':'After fixing all roots and shifts, all q_ij tend to0, the shared rho=sum(q_ij) tends to0, W_i tends to1, D_i tends to0, g_ij tends to1, and b_ij tends to(204/409)^2, a7-adic unit. The finite-family supplier preserves these common neighborhoods.',
 'bb_native_soundness_scope':'Every negative odd valuation of a pole input b is excluded at primes other than7; the prime7 already belongs to the retained height exceptional set.',
 'bb_native_projection_scope':'New pole predicate, same integer input projection under the retained non-pole arithmetic interfaces and the cited BB result; no bijection of old and new complete rational zero sets is asserted.',
 'bb_native_old_non_cm_pole_required':False,
 'bb_native_route_k_required':False,
 'bb_native_original_theorem_5_3_required':False,
 'bb_native_cr3_required':False,
 'bb_native_proposition_n_required':False,
 'bb_native_retained_non_pole_arithmetic_interfaces':True,
 'retained_arithmetic_interfaces':'All predecessor elliptic-carrier, height, comparison, finite-family prime and common-index preparation interfaces except the old non-CM pole realization; the latter is replaced by Bhargava-Burungale Theorem2.3 with the simultaneous preparation proved in bb_native_combined.tex.',
 'simultaneous_completeness_scope':'All earlier shared point/CRT/contact constructions with common finite preparation enlarged by7. Private BB-native pole witnesses are filled only after every shared physical datum is fixed.',
 'bb_native_inherited_metadata_scope':'Earlier table hashes, reconstruction maps, and frozen paper references retain their historical meaning. Only the explicitly enumerated private pole rows and their realization premise are replaced here.',
 'unconditional_undecidability_claim':False})
 assert new['variable_names']==old['variable_names']
 assert len(rows)==len(old['residuals'])
 return new

def main():
 for interface,relative in PREDECESSORS.items():
  raw=(ROOT/relative).read_bytes();old=json.loads(raw);new=build_data(old,interface)
  new['bb_native_predecessor']=relative;new['bb_native_predecessor_sha256']=hashlib.sha256(raw).hexdigest()
  encoded=(json.dumps(new,sort_keys=True,separators=(',',':'))+'\n').encode()
  (HERE/f'bb_native_{interface}_quadrics.json').write_bytes(encoded)
  cert={'interface':interface,'variables':new['variables'],'quadratic_rows':len(new['residuals']),'degree':4,'table_sha256':hashlib.sha256(encoded).hexdigest(),**{k:v for k,v in new.items() if k.startswith('bb_native_')},'integer_blocks':new['integer_blocks'],'source_coding_theorem':new['source_coding_theorem'],'source_coding_theorem_independently_reproved':False,'source_universality_hypothesis':None,'unconditional_undecidability_claim':False}
  (HERE/f'bb_native_{interface}_certificate.json').write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n')
  print(json.dumps({k:cert[k] for k in ('interface','variables','quadratic_rows','table_sha256','bb_native_poles')}))
if __name__=='__main__':main()
