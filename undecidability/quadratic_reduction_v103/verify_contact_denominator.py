#!/usr/bin/env python3
"""Independent exact audit: no compiler imports and no numeric root tests."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def expression(row,names):
 return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(names[i-1]) for i in t['monomial']) for t in row['terms']))

def ratio(actual,expected):
 diff_symbols=sorted(actual.free_symbols|expected.free_symbols,key=str)
 a=s.Poly(actual,*diff_symbols);b=s.Poly(expected,*diff_symbols)
 assert a.monoms()==b.monoms()
 k=a.coeffs()[0]/b.coeffs()[0]
 assert k.is_Rational and k!=0
 assert s.expand(actual-k*expected)==0
 return k

def symbolic_lemma():
 u,f,W,k,t,A,B,C,D,E,F=s.symbols('u f W k t A B C D E F')
 comb=A*u*f+(B*u+C*f)*(W+k)-k*t
 rel=(D*u+E*f+F*k)*(W+k)+f*t
 P=C*f*f+B*u*f+E*k*f+D*k*u+F*k*k
 R=A*(B*B-C*E)*u*f+A*(B*E-C*D)*k*f+A*(B*D-C*F)*k*u+A*B*F*k*k
 V=C*C*(W+k)+A*C*u-A*B*k
 identity=P*V+k*R-C*C*(k*rel+f*comb)-A*C*(B*f+D*k)*(u*u-k*f)
 assert s.expand(identity)==0
 # The new inverse coordinate has a unique affine rational inverse.
 recovered=(V-A*C*u-(C*C-A*B)*k)/(C*C)
 assert s.cancel(recovered-W)==0
 return 'Ptilde*V+kappa*R-C^2*(kappa*Rel+f*Comb)=A*C*(B*f+D*kappa)*(u^2-kappa*f)'

def audit(interface):
 source=ROOT/f'undecidability/contact_endpoint_v102/endpoint_{interface}_quadrics.json'
 raw=source.read_bytes();old=json.loads(raw);on=old['variable_names'];orr={r['name']:r for r in old['residuals']}
 target=HERE/f'denominator_{interface}_quadrics.json';out=target.read_bytes();new=json.loads(out);nn=new['variable_names'];nrr={r['name']:r for r in new['residuals']}
 cert=json.loads((HERE/f'denominator_{interface}_certificate.json').read_bytes())
 assert new['contact_denominator_predecessor_sha256']==hashlib.sha256(raw).hexdigest()
 assert cert['table_sha256']==hashlib.sha256(out).hexdigest()
 if interface=='general':
  A,B,C,D,E,F=3813373161796,122376041313918,-35893742479489,141822723674536,-192222345736537,-39896049934224
  k=s.Integer(1);inverse_slot=157;expected=(963,818,14)
 else:
  A,B,C,D,E,F=7878870169,1229741066709366,-6786192246520,476802068222265625,-42042541279847500,-1738195040039062500
  k=s.Symbol('int_b_162');inverse_slot=159;expected=(1140,991,12)
 z=s.Symbol;u,f,us,fs=map(z,('int_b_60','int_b_61','int_b_69','int_b_70'))
 w=z('contact_common_spacing_square');a2,a3,a4=[z(f'contact_common_fourth_coefficient_{j}') for j in (2,3,4)]
 v=(us-u-256*w)/32;a1=(fs-f-256*a2-4096*a3-65536*a4)/16
 T=z('_j');U=u+2*T*v+T*T*w;FF=f+T*a1+T*T*a2+T**3*a3+T**4*a4
 # Pin the retained rows proving U(j)^2=kappa*F(j) for EVERY j.
 root_square=u*u-k*f
 assert ratio(expression(orr['integer.b.additive.detector0.contactFourthPower'],on),root_square)!=0
 r1=k*a1-4*u*v;r2=k*a2-2*u*w-4*v*v;r3=k*a3-4*v*w;r4=k*a4-w*w
 for j,p in enumerate((r1,r2,r3,r4),1):
  assert ratio(expression(orr[f'contact.progression.fourth_coefficient_{j}'],on),p)!=0
 assert s.expand(U*U-k*FF-root_square+T*r1+T*T*r2+T**3*r3+T**4*r4)==0
 if interface=='specified':
  guard=k*z('int_b_163')-1
  guards=[r['name'] for r in old['residuals'] if s.expand(expression(r,on)-guard)==0 or s.expand(expression(r,on)+guard)==0]
  assert guards,'missing gauge unit guard'
 # Independently selected block order and endpoint index.
 labels=['b','g','t','m','w','s','h','c','gamma','j','i']
 indices=[0,1,2,3,4,5,6,7,8,10,11]
 if interface=='general':labels+=['power_delta','power_alpha'];indices += [12,13]
 contacts=[(label,index,0) for label,index in zip(labels,indices)]+[('b',16,1)]
 removed=[];old_sub={};expected_rel={};delete=[];occurrences={}
 added=[f'contact_denominator_coefficient_{j}' for j in range(9)]
 for label,index,det in contacts:
  local='i_reciprocal' if label=='i' else label
  combination=f'int_{local}_'+('62' if det==0 else '71')
  inverse=f'int_{local}_{inverse_slot+det}'
  W=z(inverse);t=z(combination);uj=s.expand(U.subs(T,index));fj=s.expand(FF.subs(T,index))
  prefix=f'integer.{label}.additive.detector{det}.'
  q1=prefix+'contactCombination';q2=prefix+'contactRelation'
  template1=A*uj*fj+(B*uj+C*fj)*(W+k)-k*t
  template2=(D*uj+E*fj+F*k)*(W+k)+fj*t
  assert ratio(expression(orr[q1],on),s.expand(template1))!=0,(interface,q1)
  assert ratio(expression(orr[q2],on),s.expand(template2))!=0,(interface,q2)
  uses=[r['name'] for r in old['residuals'] if any(on[i-1]==combination for term in r['terms'] for i in term['monomial'])]
  assert set(uses)=={q1,q2};occurrences[combination]=uses
  removed.append(combination);delete.append(q1)
  old_sub[W]=(W-A*C*uj-(C*C-A*B)*k)/(C*C)
  residue=A*(B*B-C*E)*uj*fj+A*(B*E-C*D)*k*fj+A*(B*D-C*F)*k*uj+A*B*F*k*k
  expected_rel[q2]=s.expand(sum(z(added[j])*index**j for j in range(9))*W+residue)
 assert nn==[n for n in on if n not in removed]+added
 assert new['contact_denominator_removed_coordinates']==removed
 assert new['contact_denominator_deleted_rows']==delete
 assert new['contact_denominator_added_coordinates']==added
 assert (len(nn),len(nrr),len(contacts))==expected
 assert new['variables']==len(nn)==cert['variables']
 assert cert['quadratic_rows']==len(nrr)
 assert set(nrr)==set(orr)-set(delete)|{f'contact.denominator.coefficient.{j}' for j in range(9)}
 changed=[];unchanged=[]
 for name,row in orr.items():
  if name in delete:continue
  original=expression(row,on)
  if name in expected_rel:
   expected_row=expected_rel[name];changed.append(name)
  elif original.free_symbols & old_sub.keys():
   expected_row=s.expand(original.xreplace(old_sub));changed.append(name)
  else:
   expected_row=original;unchanged.append(name)
  actual=expression(nrr[name],nn)
  if name in changed:
   assert ratio(actual,expected_row)==s.Rational(new['contact_denominator_row_multipliers'][name]),name
  else:assert s.expand(actual-expected_row)==0,name
 poly=s.Poly(s.expand(C*FF*FF+B*U*FF+E*k*FF+D*k*U+F*k*k),T)
 assert poly.degree()==8
 for j,n in enumerate(added):
  name=f'contact.denominator.coefficient.{j}'
  expected_row=s.expand(k*z(n)-poly.nth(j))
  assert ratio(expression(nrr[name],nn),expected_row)==s.Rational(new['contact_denominator_row_multipliers'][name])
 assert changed==new['contact_denominator_changed_rows']
 # The entire integer interface and outer source inherit the same premises.
 for field in ('integer_blocks','ordinary_integer_inputs','reciprocal_integer_inputs','source_coding_theorem','source_coding_theorem_independently_reproved','source_universality_hypothesis','parameters'):
  assert new[field]==old[field],field
 assert new['unconditional_undecidability_claim'] is False
 used=set();parameters=[z(n) for n in new['parameters']]
 for row in new['residuals']:
  for term in row['terms']:
   assert len(term['monomial'])<=2
   assert term['monomial']==sorted(term['monomial'])
   used.update(term['monomial'])
   assert all(c.is_Integer for c in s.Poly(s.sympify(term['coefficient']),*parameters).coeffs())
 assert used==set(range(1,len(nn)+1))
 assert any(len(t['monomial'])==2 for r in new['residuals'] for t in r['terms'])
 return {'interface':interface,'variables':len(nn),'quadratic_rows':len(nrr),'removed_combination_coordinates':len(removed),'new_shared_coefficients':9,'changed_old_rows':len(changed),'unchanged_rows':len(unchanged),'new_definition_rows':9,'source_sha256':hashlib.sha256(raw).hexdigest(),'table_sha256':hashlib.sha256(out).hexdigest(),'degree':4,'status':'PASS'}

def main():
 identity=symbolic_lemma();results=[audit(k) for k in ('general','specified')]
 print(json.dumps({'identity':identity,'results':results,'scope':'Exact rational zero-set equivalence and complete coefficient audit; inherited arithmetic interfaces and externally cited coding theorem remain assumptions'},sort_keys=True))
if __name__=='__main__':main()
