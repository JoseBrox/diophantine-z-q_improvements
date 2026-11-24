#!/usr/bin/env python3
"""Compress the inverse-contact equations on the retained affine progression."""
from __future__ import annotations
import hashlib
import json
from math import gcd, lcm
from pathlib import Path
import sympy as sp
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSORS = {k: f'undecidability/contact_endpoint_v102/endpoint_{k}_quadrics.json' for k in ('general','specified')}
CONSTANTS = {
 'general': (3813373161796,122376041313918,-35893742479489,141822723674536,-192222345736537,-39896049934224),
 'specified': (7878870169,1229741066709366,-6786192246520,476802068222265625,-42042541279847500,-1738195040039062500),
}

def expr(row,names):
 return sp.expand(sum(sp.sympify(t['coefficient'])*sp.prod(sp.Symbol(names[i-1]) for i in t['monomial']) for t in row['terms']))

def encode(name,polynomial,names,parameters):
 ids={n:i+1 for i,n in enumerate(names)}; symbols={sp.Symbol(n) for n in names}
 used=sorted(polynomial.free_symbols & symbols,key=str)
 entries=sp.Poly(sp.expand(polynomial),*used).terms()
 ps=[sp.Symbol(p) for p in parameters]
 coefficients=[q for _,c in entries for q in sp.Poly(c,*ps).coeffs()]
 denominator=lcm(*(int(q.q) for q in coefficients));content=0
 for q in coefficients:content=gcd(content,abs(int(q*denominator)))
 multiplier=sp.Rational(denominator,content)
 terms=[]
 for powers,coefficient in entries:
  monomial=sorted(ids[str(s)] for s,e in zip(used,powers) for _ in range(e))
  assert len(monomial)<=2,(name,monomial)
  terms.append({'coefficient':str(sp.expand(multiplier*coefficient)),'monomial':monomial})
 return {'name':name,'terms':sorted(terms,key=lambda t:t['monomial'])},str(multiplier)

def build_data(old,interface):
 z=sp.Symbol; old_names=old['variable_names']; old_rows={r['name']:r for r in old['residuals']}
 A,B,C,D,E,F=CONSTANTS[interface]; scale=sp.Integer(1) if interface=='general' else z('int_b_162')
 u,f,u2,f2=(z('int_b_'+str(i)) for i in (60,61,69,70))
 w=z('contact_common_spacing_square'); a2,a3,a4=(z(f'contact_common_fourth_coefficient_{i}') for i in (2,3,4))
 v=(u2-u-256*w)/32; a1=(f2-f-256*a2-4096*a3-65536*a4)/16
 T=z('_progression_index'); U=u+2*T*v+T*T*w; FF=f+T*a1+T*T*a2+T**3*a3+T**4*a4
 P=sp.Poly(sp.expand(C*FF**2+B*U*FF+E*scale*FF+D*scale*U+F*scale**2),T)
 added=[f'contact_denominator_coefficient_{j}' for j in range(9)]
 contacts=[]
 for label,index in zip(old['affine_contact_blocks'],old['affine_contact_active_indices']):
  local='i_reciprocal' if label=='i' else label
  inv=f'int_{local}_'+('157' if interface=='general' else '159')
  contacts.append({'label':label,'index':index,'detector':0,'combination':f'int_{local}_62','inverse':inv})
 contacts.append({'label':'b','index':16,'detector':1,'combination':'int_b_71','inverse':'int_b_'+('158' if interface=='general' else '160')})
 removed=[c['combination'] for c in contacts]
 deleted=[]; substitutions={}; changed_expr={}; occurrences={}; reconstruct={}
 for c in contacts:
  index=c['index']; UI=sp.expand(U.subs(T,index)); FI=sp.expand(FF.subs(T,index)); WI=z(c['inverse'])
  old_W=(WI-A*C*UI-(C*C-A*B)*scale)/(C*C)
  substitutions[WI]=sp.expand(old_W)
  prefix=f"integer.{c['label']}.additive.detector{c['detector']}."
  comb_row=prefix+'contactCombination'; relation=prefix+'contactRelation'
  deleted.append(comb_row)
  CI=z(c['combination'])
  occurrences[c['combination']]=[r['name'] for r in old['residuals'] if any(old_names[i-1]==c['combination'] for t in r['terms'] for i in t['monomial'])]
  assert set(occurrences[c['combination']])=={comb_row,relation}
  occurrences[c['inverse']]=[r['name'] for r in old['residuals'] if any(old_names[i-1]==c['inverse'] for t in r['terms'] for i in t['monomial'])]
  Pvalue=sum(z(added[j])*index**j for j in range(9))
  R=(A*(B*B-C*E)*UI*FI+A*(B*E-C*D)*scale*FI+A*(B*D-C*F)*scale*UI+A*B*F*scale**2)
  changed_expr[relation]=sp.expand(Pvalue*WI+R)
  reconstruct[c['combination']]=str((A*UI*FI+(B*UI+C*FI)*(old_W+scale))/scale)
  c.update({'u':str(UI),'fourth':str(FI),'old_inverse':str(sp.expand(old_W)),'combination_row':comb_row,'relation_row':relation})
 names=[n for n in old_names if n not in removed]+added
 ids={n:i+1 for i,n in enumerate(names)}
 rows=[];changed=[];multipliers={}
 for r in old['residuals']:
  name=r['name']
  if name in deleted:continue
  touched=any(z(old_names[i-1]) in substitutions for t in r['terms'] for i in t['monomial'])
  if name in changed_expr or touched:
   p=changed_expr[name] if name in changed_expr else expr(r,old_names).xreplace(substitutions)
   encoded,mult=encode(name,sp.expand(p),names,old['parameters']);rows.append(encoded);changed.append(name);multipliers[name]=mult
  else:
   rows.append({'name':name,'terms':[{'coefficient':t['coefficient'],'monomial':sorted(ids[old_names[i-1]] for i in t['monomial'])} for t in r['terms']]})
 for j,n in enumerate(added):
  name=f'contact.denominator.coefficient.{j}'
  row,mult=encode(name,scale*z(n)-P.nth(j),names,old['parameters']);rows.append(row);multipliers[name]=mult
 new=dict(old)
 new.update({'variables':len(names),'variable_names':names,'residuals':rows,
 'contact_denominator_proof':'undecidability/quadratic_reduction_v103/contact_denominator_compression.tex',
 'contact_denominator_constants':{'A':A,'B':B,'C':C,'D':D,'E':E,'F':F},
 'contact_denominator_contacts':contacts,
 'contact_denominator_added_coordinates':added,
 'contact_denominator_removed_coordinates':removed,
 'contact_denominator_deleted_rows':deleted,
 'contact_denominator_changed_rows':changed,
 'contact_denominator_row_multipliers':multipliers,
 'contact_denominator_occurrences':occurrences,
 'contact_denominator_old_combination_recovery':reconstruct,
 'contact_denominator_savings':{'coordinates':len(contacts)-9,'quadratic_rows':len(contacts)-9},
 'contact_denominator_exact_equivalence':'Bijective rational reconstruction of the full predecessor zero set; only the retained nonzero common gauge and nonzero constant C are inverted',
 'contact_denominator_integer_interfaces_unchanged':True,
 'contact_denominator_inherited_metadata_scope':'Earlier chart names describe historical stages. Each listed inverse coordinate now stores C^2*(old_inverse+scale)+A*C*u-A*B*scale; listed combination coordinates are reconstructed by this step.',
 'unconditional_undecidability_claim':False})
 assert len(names)==old['variables']-len(contacts)+9
 assert len(rows)==len(old['residuals'])-len(contacts)+9
 assert {i for r in rows for t in r['terms'] for i in t['monomial']}==set(ids.values())
 return new

def main():
 for interface,relative in PREDECESSORS.items():
  raw=(ROOT/relative).read_bytes();old=json.loads(raw);new=build_data(old,interface)
  new['contact_denominator_predecessor']=relative
  new['contact_denominator_predecessor_sha256']=hashlib.sha256(raw).hexdigest()
  out=(json.dumps(new,sort_keys=True,separators=(',',':'))+'\n').encode()
  (HERE/f'denominator_{interface}_quadrics.json').write_bytes(out)
  cert={'interface':interface,'variables':new['variables'],'quadratic_rows':len(new['residuals']),'degree':4,'table_sha256':hashlib.sha256(out).hexdigest(),**{k:v for k,v in new.items() if k.startswith('contact_denominator_')},'source_coding_theorem':new['source_coding_theorem'],'source_coding_theorem_independently_reproved':False,'source_universality_hypothesis':None,'unconditional_undecidability_claim':False}
  (HERE/f'denominator_{interface}_certificate.json').write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n')
  print(json.dumps({k:cert[k] for k in ('interface','variables','quadratic_rows','table_sha256')}))
if __name__=='__main__':main()
