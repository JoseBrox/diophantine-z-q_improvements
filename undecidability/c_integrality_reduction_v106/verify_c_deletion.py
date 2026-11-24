#!/usr/bin/env python3
"""Independent coefficient, source-square and global-contact deletion audit."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def expr(row,names):
 return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(names[j-1]) for j in t['monomial']) for t in row['terms']))
def named(row,names):
 return sorted((tuple(names[j-1] for j in t['monomial']),t['coefficient']) for t in row['terms'])

def audit(interface):
 src=ROOT/f'undecidability/input_comparison_v105/preferred_{interface}_quadrics.json';raw=src.read_bytes();old=json.loads(raw)
 expected_hash={'general':'b1b54b38f3268442e6fa173032f83e70cf6e63cb8cef4a1306575e560e3044d4','specified':'d17a8d0d61a1e3d383293cf6e74f4ffd41e9b2218760c1a6e37d01d78818be53'}[interface]
 assert hashlib.sha256(raw).hexdigest()==expected_hash
 out=(HERE/f'c_deleted_{interface}_quadrics.json').read_bytes();new=json.loads(out)
 cert=json.loads((HERE/f'c_deleted_{interface}_certificate.json').read_text())
 assert new['c_integrality_predecessor_sha256']==expected_hash and cert['table_sha256']==hashlib.sha256(out).hexdigest()
 ns=old['variable_names'];names=new['variable_names'];oldrows={r['name']:r for r in old['residuals']};rows={r['name']:r for r in new['residuals']}
 if interface=='general':ri,ei,last=159,160,1;windices=[153];expected=(887,750,57,49,12,24,36)
 else:ri,ei,last=162,163,2;windices=[154,155];expected=(1052,913,72,62,10,30,40)
 rho,eps,eps2=s.symbols(f'int_b_{ri} int_b_{ei} int_b_{ei+1}');c,d,ac,E,v=s.symbols('c d ac E i_inverse');X=s.Symbol('int_c_37')
 zeta,a=s.symbols('pell_d_positive_square a')
 half=zeta*zeta-2*a*d-2*a*ac+2*c-2
 removed=[n for n in ns if n.startswith('int_c_')]
 deleted=[n for n in oldrows if n.startswith(('integer.c.','global.c.','scalar_norm.c.','detector_trace.c.'))]
 assert len(removed)==expected[2] and len(deleted)==expected[3]
 weights=[s.Symbol(f'int_c_{j}') for j in windices]+[s.Symbol('int_c_last_contact_weight')]
 three=[f'integer.i.balanced.detector{last}.poleInput.definition',f'integer.i.shared.inverse{last}',f'integer.i.shared.gate{last}']
 outer=['jones1980.d.norm','jones1980.E.reciprocal'];changed=outer+three
 assert new['c_integrality_removed_coordinates']==removed and new['c_integrality_deleted_rows']==deleted
 assert new['c_integrality_changed_rows']==changed
 assert set(rows)==(set(oldrows)-set(deleted))|{'jones1980.pell_positive_root'}
 # Both source identities retain c^2 exactly, including c=0.
 square=expr(oldrows['integer.c.inputSquare.definition'],ns)
 assert s.expand(square-(c*c-rho*X))==0
 assert s.expand(expr(oldrows[outer[0]],ns)-(d*d-ac*ac+rho*X-1))==0
 assert s.expand(expr(oldrows[outer[1]],ns)-(E*v-rho*X))==0
 assert s.expand(expr(rows[outer[0]],names)-(d*d-ac*ac+c*c-1))==0
 assert s.expand(expr(rows[outer[1]],names)-(E*v-c*c))==0
 assert s.expand(expr(rows[outer[0]],names)-expr(oldrows[outer[0]],ns)-square)==0
 assert s.expand(expr(rows[outer[1]],names)-expr(oldrows[outer[1]],ns)+square)==0
 assert s.expand(square.subs(X,eps*c*c)-c*c*(1-rho*eps))==0
 guard=[expr(r,ns) for r in old['residuals'] if len(r['terms'])==2]
 assert any(s.expand(p-(rho*eps-1))==0 or s.expand(p+(rho*eps-1))==0 for p in guard)
 assert any(s.expand(p-(eps2-eps*eps))==0 or s.expand(p+(eps2-eps*eps))==0 for p in guard)
 # The actual eliminated final contact weight is changed in every occurrence.
 oldlhs,oldrhs=old['global_contact_sum_elimination'].split(' = ',1)
 newlhs,newrhs=new['global_contact_sum_elimination'].split(' = ',1)
 assert oldlhs==newlhs
 assert s.expand(s.sympify(newrhs)-s.sympify(oldrhs)-sum(weights))==0
 assert all(s.Symbol(n) in s.sympify(oldrhs).free_symbols for n in map(str,weights))
 for n in three:
  assert s.expand(expr(rows[n],names)-expr(oldrows[n],ns).subs({w:0 for w in weights}))==0,n
 # Derive all three rows directly from the omitted last weight, rather than
 # relying only on the syntactic zero substitution used by the compiler.
 if interface=='general':bi,gi,vi,di=73,72,158,156
 else:bi,gi,vi,di=174,173,161,158
 PB,PG,PV,PD=[s.Symbol(f'int_i_reciprocal_{j}') for j in (bi,gi,vi,di)]
 def templates(omega):
  pole=167281*PB*(eps2+omega)-166464*PG*PG
  inverse=eps*eps2-omega*PV
  gate=(2*eps*eps2-eps*PV-eps2*eps2+2*eps2*PG-eps2*omega-PD*PD) if interface=='general' else (2*eps*PG+2*eps-eps2-rho*PV-omega-PD*PD)
  return (pole,inverse,gate)
 for rowset,coordinates,weight in ((oldrows,ns,s.sympify(oldrhs)),(rows,names,s.sympify(newrhs))):
  for n,p in zip(three,templates(weight)):assert s.expand(expr(rowset[n],coordinates)-p)==0,n
 # Pin the retained source premises used by the arithmetic theorem.
 assert s.expand(expr(rows['jones1980.ac.definition'],names)-(ac-a*c))==0
 b,w,gamma=s.symbols('b w gamma')
 assert s.expand(expr(rows['jones1980.d.definition'],names)-(d-(a-2)*c-b*w-(4*a-5)*gamma))==0
 assert s.expand(expr(rows['jones1980.pell_positive_root'],names)-half)==0
 if interface=='specified':assert named(rows['jones1980.pell_positive_root'],names)==named(oldrows['jones1980.pell_positive_root'],ns)
 assert new['c_integrality_halftrace_added']==(interface=='general')
 # No removed coordinate has an unaudited occurrence.
 for n in removed:
  index=ns.index(n)+1
  occurrences=[r['name'] for r in old['residuals'] if any(index in t['monomial'] for t in r['terms'])]
  assert occurrences==new['c_integrality_removed_coordinate_occurrences'][n]
  outside=set(occurrences)-set(deleted)
  expected_outside=set(outer) if n=='int_c_37' else set(three) if n in map(str,weights) else set()
  assert outside==expected_outside,(n,outside,expected_outside)
 for n,r in oldrows.items():
  if n not in deleted and n not in changed:assert named(rows[n],names)==named(r,ns),n
 assert names==[n for n in ns if n not in removed]+(['pell_d_positive_square'] if interface=='general' else [])
 assert not any(n.startswith('int_c_') for n in names)
 assert len(names)==expected[0] and len(rows)==expected[1]
 assert new['integer_blocks']==expected[4] and new['global_contact_weights']==expected[5] and new['bb_native_poles']==expected[6]
 assert new['ordinary_integer_inputs']==[n for n in old['ordinary_integer_inputs'] if n!='c']
 assert new['reciprocal_integer_inputs']==old['reciprocal_integer_inputs']
 assert new['affine_contact_blocks']==[n for n in old['affine_contact_blocks'] if n!='c']
 assert new['affine_contact_active_indices']==[j for n,j in zip(old['affine_contact_blocks'],old['affine_contact_active_indices']) if n!='c']
 assert new['aggregate_spacing_contact_indices']==new['affine_contact_active_indices']
 # All surviving native poles are retained exactly; no old non-CM premise returns.
 for n in new['bb_native_changed_rows']:assert n in rows and not n.startswith('integer.c.')
 assert len(new['bb_native_changed_rows'])==3*expected[6]
 assert new['bb_native_old_non_cm_pole_required'] is False and new['bb_native_route_k_required'] is False
 for field in ('parameters','source_coding_theorem','source_coding_theorem_independently_reproved','source_universality_hypothesis','unconditional_undecidability_claim'):
  assert new[field]==old[field]
 support=set();params=list(map(s.Symbol,new['parameters']));degree=False
 for r in rows.values():
  for t in r['terms']:
   assert len(t['monomial'])<=2;degree|=len(t['monomial'])==2;support.update(t['monomial'])
   assert all(c.is_Integer for c in s.Poly(s.sympify(t['coefficient']),*params).coeffs())
 assert support==set(range(1,len(names)+1)) and degree
 assert cert['variables']==len(names) and cert['quadratic_rows']==len(rows)
 return {'interface':interface,'variables':len(names),'quadratic_rows':len(rows),'removed_coordinates':len(removed),'deleted_rows':len(deleted),'changed_rows':len(changed),'added_halftrace':interface=='general','unchanged_rows':len(oldrows)-len(deleted)-len(changed),'integer_predicates':expected[4],'contact_weights':expected[5],'BB_native_poles':expected[6],'source_sha256':expected_hash,'table_sha256':hashlib.sha256(out).hexdigest(),'status':'PASS'}

def main():
 print(json.dumps({'results':[audit(x) for x in ('general','specified')],'scope':'Finite coefficient, occurrence, gauge, half-trace and source-square audit. Quantified c-integrality is the separate proved Pell theorem; source-instance completeness reselects interface witnesses.'},sort_keys=True))
if __name__=='__main__':main()
