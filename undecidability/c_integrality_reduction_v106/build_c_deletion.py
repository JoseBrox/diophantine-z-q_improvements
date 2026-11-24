#!/usr/bin/env python3
"""Replace the c-integrality interface by its arithmetic half-trace certificate."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCES={
 'general':('undecidability/input_comparison_v105/preferred_general_quadrics.json','b1b54b38f3268442e6fa173032f83e70cf6e63cb8cef4a1306575e560e3044d4'),
 'specified':('undecidability/input_comparison_v105/preferred_specified_quadrics.json','d17a8d0d61a1e3d383293cf6e74f4ffd41e9b2218760c1a6e37d01d78818be53'),
}
PRIVATE_PREFIXES=('integer.c.','global.c.','scalar_norm.c.','detector_trace.c.')
HALFTRACE='jones1980.pell_positive_root'
HALFVARIABLE='pell_d_positive_square'

def row_from_expr(name,expr,names):
 expr=s.expand(expr);index={n:j+1 for j,n in enumerate(names)}
 symbols=[s.Symbol(n) for n in names if s.Symbol(n) in expr.free_symbols]
 terms=[]
 for powers,coefficient in s.Poly(expr,*symbols).terms():
  assert sum(powers)<=2
  if coefficient:
   terms.append({'coefficient':str(coefficient),'monomial':[index[str(symbols[j])] for j,p in enumerate(powers) for _ in range(p)]})
 terms.sort(key=lambda t:(len(t['monomial']),t['monomial']))
 return {'name':name,'terms':terms}

def build(interface):
 relative,pinned=SOURCES[interface];raw=(ROOT/relative).read_bytes();assert hashlib.sha256(raw).hexdigest()==pinned
 old=json.loads(raw);oldnames=old['variable_names'];oldrows={r['name']:r for r in old['residuals']}
 removed=[n for n in oldnames if n.startswith('int_c_')]
 deleted=[n for n in oldrows if n.startswith(PRIVATE_PREFIXES)]
 if interface=='general':weights=['int_c_153','int_c_last_contact_weight'];rho='int_b_159';eps='int_b_160';last=1;expected=(887,750,57,49)
 else:weights=['int_c_154','int_c_155','int_c_last_contact_weight'];rho='int_b_162';eps='int_b_163';last=2;expected=(1052,913,72,62)
 assert len(removed)==expected[2] and len(deleted)==expected[3]
 changed=[f'integer.i.balanced.detector{last}.poleInput.definition',f'integer.i.shared.inverse{last}',f'integer.i.shared.gate{last}']
 outer=['jones1980.d.norm','jones1980.E.reciprocal']
 names=[n for n in oldnames if n not in removed]
 add_half=HALFVARIABLE not in names
 assert add_half==(interface=='general')
 if add_half:names.append(HALFVARIABLE)
 index={n:j+1 for j,n in enumerate(names)}
 occurrences={n:[] for n in removed}
 rows=[]
 for r in old['residuals']:
  for n in removed:
   ix=oldnames.index(n)+1
   if any(ix in t['monomial'] for t in r['terms']):occurrences[n].append(r['name'])
  if r['name'] in deleted:continue
  terms=[]
  for t in r['terms']:
   mon=[oldnames[j-1] for j in t['monomial']]
   if r['name'] in changed and any(n in weights for n in mon):continue
   if r['name'] in outer and sorted(mon)==sorted([rho,'int_c_37']):mon=['c','c']
   assert not set(mon).intersection(removed),(r['name'],mon)
   terms.append({'coefficient':t['coefficient'],'monomial':sorted(index[n] for n in mon)})
  rows.append({'name':r['name'],'terms':terms})
 if add_half:
  zeta,a,d,ac,c=s.symbols('pell_d_positive_square a d ac c')
  rows.append(row_from_expr(HALFTRACE,zeta*zeta-2*a*d-2*a*ac+2*c-2,names))
 oldsum=old['global_contact_sum_elimination'];lhs,rhs=oldsum.split(' = ',1)
 newsum=lhs+' = '+str(s.expand(s.sympify(rhs).subs({s.Symbol(w):0 for w in weights})))
 activeblocks=[b for b in old['affine_contact_blocks'] if b!='c']
 activeindices=[j for b,j in zip(old['affine_contact_blocks'],old['affine_contact_active_indices']) if b!='c']
 new=dict(old)
 historical={k:old[k] for k in ('integer_blocks','ordinary_integer_inputs','global_contact_weights','global_contact_sum_elimination','affine_contact_blocks','affine_contact_active_indices','aggregate_spacing_contact_indices','bb_native_poles','bb_native_comparison_poles','bb_native_scalar_poles','bb_native_changed_rows','bb_native_pole_prefixes','shared_reference_blocks') if k in old}
 new.update({'variables':len(names),'variable_names':names,'residuals':rows,
  'integer_blocks':old['integer_blocks']-1,
  'ordinary_integer_inputs':[n for n in old['ordinary_integer_inputs'] if n!='c'],
  'shared_reference_blocks':old['integer_blocks']-1,
  'global_contact_weights':old['global_contact_weights']-len(weights),
  'global_contact_sum_elimination':newsum,
  'affine_contact_blocks':activeblocks,'affine_contact_active_indices':activeindices,
  'aggregate_spacing_contact_indices':activeindices,
  'bb_native_poles':old['bb_native_poles']-(len(weights)+1),
  'bb_native_comparison_poles':old['bb_native_comparison_poles']-len(weights),
  'bb_native_scalar_poles':old['bb_native_scalar_poles']-1,
  'bb_native_changed_rows':[n for n in old['bb_native_changed_rows'] if not n.startswith('integer.c.')],
  'bb_native_pole_prefixes':[n for n in old['bb_native_pole_prefixes'] if not n.startswith('integer.c.')],
  'c_integrality_predecessor':relative,'c_integrality_predecessor_sha256':pinned,
  'c_integrality_proof':'undecidability/c_integrality_reduction_v106/c_predicate_deletion.tex',
  'c_integrality_arithmetic_theorem':'undecidability/pell_integrality_replacement_v106/pell_integrality_replacement.tex',
  'c_integrality_retained_hypotheses':'a is a multiple of3 from the integral prefix; d-(a-2)c=b*w+(4*a-5)*gamma is integral; first Pell norm and rational half-trace square imply c,d integral, including a=0.',
  'c_integrality_removed_coordinates':removed,'c_integrality_deleted_rows':deleted,
  'c_integrality_changed_rows':outer+changed,
  'c_integrality_removed_coordinate_occurrences':occurrences,
  'c_integrality_halftrace_added':add_half,'c_integrality_halftrace_coordinate':HALFVARIABLE,'c_integrality_halftrace_row':HALFTRACE,
  'c_integrality_removed_contact_weights':weights,
  'c_integrality_old_last_weight':oldsum,'c_integrality_new_last_weight':newsum,
  'c_integrality_source_square_reconstruction':'int_c_37=epsilon*c^2; old square row c^2-rho*int_c_37=0. New d.norm=old d.norm+square row; new E.reciprocal=old E.reciprocal-square row.',
  'c_integrality_source_square_removed':True,
  'c_integrality_historical_metadata':historical,
  'c_integrality_historical_scope':'Earlier stage hashes, auxiliary maps and deleted-coordinate lists are historical provenance, not a direct zero-set lift from this predicate-deletion stage. Current predicate, contact and pole counts are explicitly updated.',
  'c_integrality_projection_scope':'Same coded-instance existence under the retained interfaces and source theorem, using the proved half-trace integrality replacement. Completeness reselects the reduced simultaneous integer tuple; no full old/new zero-set bijection is asserted.',
  'c_integrality_exact_zero_set_equivalence':False,
  'c_integrality_no_new_arithmetic_premise':True,
  'c_integrality_remaining_bb_scope':'All remaining pole rows retain the BB-native interpretation. The same finite simultaneous preparation applies with the reduced contact and scalar lists.',
  'unconditional_undecidability_claim':False})
 assert (len(names),len(rows))==expected[:2]
 encoded=(json.dumps(new,sort_keys=True,separators=(',',':'))+'\n').encode()
 (HERE/f'c_deleted_{interface}_quadrics.json').write_bytes(encoded)
 cert={'interface':interface,'variables':len(names),'quadratic_rows':len(rows),'degree':4,
  'table_sha256':hashlib.sha256(encoded).hexdigest(),'predecessor_variables':old['variables'],'predecessor_rows':len(old['residuals']),
  'variable_saving':old['variables']-len(names),'row_saving':len(old['residuals'])-len(rows),
  'integer_blocks':new['integer_blocks'],'ordinary_integer_inputs':new['ordinary_integer_inputs'],'global_contact_weights':new['global_contact_weights'],
  'bb_native_poles':new['bb_native_poles'],**{k:v for k,v in new.items() if k.startswith('c_integrality_')},'unconditional_undecidability_claim':False}
 (HERE/f'c_deleted_{interface}_certificate.json').write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n')
 return {k:cert[k] for k in ('interface','variables','quadratic_rows','variable_saving','row_saving','table_sha256')}

def main():
 for interface in ('general','specified'):print(json.dumps(build(interface),sort_keys=True))
if __name__=='__main__':main()
