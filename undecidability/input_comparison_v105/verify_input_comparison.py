#!/usr/bin/env python3
"""Independent exact reconstruction of the input-comparison sharing stage."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def expr(row,names):
 return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(names[j-1]) for j in t['monomial']) for t in row['terms']))
def named_terms(row,names):
 return sorted((tuple(names[j-1] for j in t['monomial']),t['coefficient']) for t in row['terms'])
def field_pair(product,z):
 p=s.Poly(s.expand(product),z)
 return tuple(s.expand(sum(c*2**(n[0]//2) for n,c in p.terms() if n[0]%2==j)) for j in (0,1))

def universal_identity():
 eps,rho,Y,P,I,S,T,A,B,C=s.symbols('eps rho Y P I S T A B C')
 L=eps*I+eps*(2504*T-S)+51*T*Y
 R=2601*Y*Y+255102*eps*Y+6255001*eps*eps-4*eps*P
 a=S-2504*T
 ad=A-S*S+5008*S*T-15015*T*T
 bd=eps*B-(S-3*T)*T
 cd=eps*C-T*T
 delta=I*I-A+102*B*Y-4*C*P
 identity=eps*eps*delta-L*(eps*I+eps*a-51*T*Y)-T*T*R+eps*eps*ad-102*eps*Y*bd+4*eps*P*cd
 assert s.expand(identity)==0
 # Rational forward/reverse maps use only the already nonzero epsilon.
 recovered={I:S-2504*T-51*T*Y/eps,A:S*S-5008*S*T+15015*T*T,B:(S-3*T)*T/eps,C:T*T/eps}
 assert s.cancel(L.subs(recovered))==0
 assert s.cancel(delta.subs(recovered)-T*T*R/eps**2)==0
 # Allowed zero fibers: no division by any private point or input quantity.
 assert s.cancel(delta.subs(recovered).subs(P,(51*Y+2501*eps)**2/(4*eps)))==0
 return {'identity':'epsilon^2*(I^2-A+102*B*Y-4*C*P) is the recorded exact combination of the old input row, retained pair row, two common field definitions, and the explicit expression A=S^2-5008*S*s+15015*s^2.',
 'guard':'epsilon!=0 follows only from the retained epsilon*rho=1 row','status':'PASS'}

def audit(stage,interface):
 if stage=='reconstructed':relative=f'undecidability/contact_endpoint_v102/endpoint_{interface}_quadrics.json'
 else:relative=f'undecidability/quadratic_reduction_v104/bb_native_{interface}_quadrics.json'
 raw=(ROOT/relative).read_bytes();old=json.loads(raw)
 out=(HERE/f'{stage}_{interface}_quadrics.json').read_bytes();new=json.loads(out)
 cert=json.loads((HERE/f'{stage}_{interface}_certificate.json').read_text())
 assert new['input_comparison_predecessor']==relative
 assert new['input_comparison_predecessor_sha256']==hashlib.sha256(raw).hexdigest()
 assert cert['table_sha256']==hashlib.sha256(out).hexdigest()
 labels=['b','g','t','m','w','s','h','c','gamma','j']
 if interface=='general':labels+=['power_delta','power_alpha'];ei,ri,si=160,159,117
 else:ei,ri,si=163,162,118
 eps=s.Symbol(f'int_b_{ei}');eps2=s.Symbol(f'int_b_{ei+1}');rho=s.Symbol(f'int_b_{ri}')
 S0,S1=s.symbols('int_b_17 int_b_18');T0,T1=s.symbols(f'int_b_{si} int_b_{si+1}')
 root=s.Symbol('root2');S=S0+root*S1;T=T0+root*T1
 A=field_pair(S*S-5008*S*T+15015*T*T,root)
 B=s.symbols('input_comparison_linear_real input_comparison_linear_imag')
 C=s.symbols('input_comparison_quadratic_real input_comparison_quadratic_imag')
 fields=lambda pair:pair[0]+root*pair[1]
 common={
  'linear':field_pair(eps*fields(B)-(S-3*T)*T,root),
  'quadratic':field_pair(eps*fields(C)-T*T,root),
 }
 oldnames=old['variable_names'];names=new['variable_names'];oldrows={r['name']:r for r in old['residuals']};rows={r['name']:r for r in new['residuals']}
 short=[expr(r,oldnames) for r in old['residuals'] if len(r['terms'])==2]
 assert any(s.expand(e-(eps*rho-1))==0 or s.expand(e+(eps*rho-1))==0 for e in short)
 assert any(s.expand(e-(eps2-eps**2))==0 or s.expand(e+(eps2-eps**2))==0 for e in short)
 removed=[];deleted=[];changed=[];recoveries={}
 for label in labels:
  local='i_reciprocal' if label=='i' else label
  z=lambda j:s.Symbol(f'int_{local}_{j}')
  I0,I1,Y,P=z(23),z(24),z(37),z(77)
  pairrow=f'integer.{label}.scalar.rPair1.definition'
  assert s.expand(expr(oldrows[pairrow],oldnames)-(2601*Y**2+255102*eps*Y+6255001*eps2-4*eps*P))==0,(stage,interface,label,pairrow)
  assert named_terms(rows[pairrow],names)==named_terms(oldrows[pairrow],oldnames)
  prefix=f'integer.{label}.input.cleared'
  for j,(Ij,Sj,Tj) in enumerate(((I0,S0,T0),(I1,S1,T1))):
   removed.append(str(Ij));deleted.append(f'{prefix}.{j}')
   expected=eps*Ij+eps*(2504*Tj-Sj)+51*Tj*Y
   assert s.expand(expr(oldrows[f'{prefix}.{j}'],oldnames)-expected)==0
   assert f'{prefix}.{j}' not in rows
   expected_recovery=Sj-2504*Tj-51*rho*Tj*Y
   assert s.expand(s.sympify(new['input_comparison_reconstruction'][str(Ij)])-expected_recovery)==0
   recoveries[str(Ij)]=str(expected_recovery)
   index=oldnames.index(str(Ij))+1
   occurrences=[r['name'] for r in old['residuals'] if any(index in t['monomial'] for t in r['terms'])]
   assert set(occurrences)=={f'{prefix}.{j}',f'{prefix}.square.0',f'{prefix}.square.1'}
   assert occurrences==new['input_comparison_occurrences'][str(Ij)]
  for j,I2 in enumerate((I0**2+2*I1**2,2*I0*I1)):
   n=f'{prefix}.square.{j}';changed.append(n)
   assert s.expand(expr(oldrows[n],oldnames)-(eps*z(48+j)+z(46+j)-2*I2))==0
   assert s.expand(expr(rows[n],names)-(eps*z(48+j)+z(46+j)-2*A[j]+204*B[j]*Y-8*C[j]*P))==0
 added=[]
 for role in ('linear','quadratic'):
  for j in (0,1):
   n=f'common.input_comparison.{role}.{j}';added.append(n)
   assert s.expand(expr(rows[n],names)-common[role][j])==0
 for n,r in oldrows.items():
  if n not in deleted and n not in changed:assert named_terms(rows[n],names)==named_terms(r,oldnames),n
 assert list(rows)==[n for n in oldrows if n not in deleted]+added
 newfields=[str(x) for pair in (B,C) for x in pair]
 assert names==[n for n in oldnames if n not in removed]+newfields
 assert new['input_comparison_removed_coordinates']==removed
 assert new['input_comparison_deleted_rows']==deleted
 assert new['input_comparison_changed_rows']==changed
 assert new['input_comparison_added_rows']==added
 for k,v in old.items():
  if k not in ('variable_names','variables','residuals'):assert new[k]==v,k
 assert new['input_comparison_new_arithmetic_premise'] is False
 expected={('reconstructed','general'):(948,803),('reconstructed','specified'):(1127,978),('preferred','general'):(943,798),('preferred','specified'):(1124,975)}[(stage,interface)]
 assert (len(names),len(rows))==expected
 support=set();quadratic=False;parameters=list(map(s.Symbol,new['parameters']))
 for r in rows.values():
  for t in r['terms']:
   assert len(t['monomial'])<=2;quadratic |= len(t['monomial'])==2
   support.update(t['monomial']);assert all(c.is_Integer for c in s.Poly(s.sympify(t['coefficient']),*parameters).coeffs())
 assert support==set(range(1,len(names)+1)) and quadratic
 assert cert['variables']==len(names) and cert['quadratic_rows']==len(rows)
 assert cert['variable_saving']==2*len(labels)-4 and cert['row_saving']==2*len(labels)-4
 return {'stage':stage,'interface':interface,'variables':len(names),'quadratic_rows':len(rows),'removed_coordinates':len(removed),'added_coordinates':4,'changed_square_rows':len(changed),'deleted_definition_rows':len(deleted),'added_definition_rows':4,'unchanged_rows':len(oldrows)-len(deleted)-len(changed),'source_sha256':hashlib.sha256(raw).hexdigest(),'table_sha256':hashlib.sha256(out).hexdigest(),'status':'PASS'}

def main():
 print(json.dumps({'universal_identity':universal_identity(),'results':[audit(stage,interface) for stage in ('reconstructed','preferred') for interface in ('general','specified')],'scope':'Exact algebraic bijection with each pinned predecessor. No arithmetic theorem or recovery of unavailable historical files is claimed.'},sort_keys=True))
if __name__=='__main__':main()
