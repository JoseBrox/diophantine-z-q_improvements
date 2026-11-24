#!/usr/bin/env python3
"""Share the squared input-comparison polynomial in complete quadratic tables."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STAGES={
 'reconstructed':'undecidability/contact_endpoint_v102/endpoint_{interface}_quadrics.json',
 'preferred':'undecidability/quadratic_reduction_v104/bb_native_{interface}_quadrics.json',
}
FIELDS={role:[f'input_comparison_{role}_{part}' for part in ('real','imag')] for role in ('linear','quadratic')}

def components_mul(a,b):return (s.expand(a[0]*b[0]+2*a[1]*b[1]),s.expand(a[0]*b[1]+a[1]*b[0]))
def components_add(a,b):return tuple(s.expand(x+y) for x,y in zip(a,b))
def scaled(c,a):return tuple(c*x for x in a)
def expression(row,names):return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(names[j-1]) for j in t['monomial']) for t in row['terms']))
def row(name,expr,names):
 expr=s.expand(expr);indices={n:j+1 for j,n in enumerate(names)}
 symbols=[s.Symbol(n) for n in names if s.Symbol(n) in expr.free_symbols]
 poly=s.Poly(expr,*symbols)
 terms=[]
 for powers,coefficient in poly.terms():
  assert sum(powers)<=2
  if coefficient==0:continue
  terms.append({'coefficient':str(coefficient),'monomial':[indices[str(symbols[j])] for j,p in enumerate(powers) for _ in range(p)]})
 terms.sort(key=lambda t:(len(t['monomial']),t['monomial']))
 return {'name':name,'terms':terms}

def build(stage,interface):
 relative=STAGES[stage].format(interface=interface)
 raw=(ROOT/relative).read_bytes();old=json.loads(raw);oldnames=old['variable_names']
 labels=['b','g','t','m','w','s','h','c','gamma','j']
 if interface=='general':labels+=['power_delta','power_alpha'];eps_index,rho_index,s_index=160,159,117
 else:eps_index,rho_index,s_index=163,162,118
 eps=s.Symbol(f'int_b_{eps_index}');rho=s.Symbol(f'int_b_{rho_index}')
 S=tuple(s.Symbol(f'int_b_{j}') for j in (17,18));T=tuple(s.Symbol(f'int_b_{j}') for j in (s_index,s_index+1))
 common={role:tuple(map(s.Symbol,pair)) for role,pair in FIELDS.items()}
 ST=components_mul(S,T);TT=components_mul(T,T);SS=components_mul(S,S)
 constant=components_add(SS,components_add(scaled(-5008,ST),scaled(15015,TT)))
 removed=[];recovery={};changed={};deleted=[];occurrences={}
 oldrows={r['name']:r for r in old['residuals']}
 for label in labels:
  local='i_reciprocal' if label=='i' else label
  Y=s.Symbol(f'int_{local}_37');P=s.Symbol(f'int_{local}_77')
  I=tuple(s.Symbol(f'int_{local}_{j}') for j in (23,24))
  prefix=f'integer.{label}.input.cleared'
  for j in range(2):
   name=str(I[j]);removed.append(name)
   recovery[name]=str(S[j]-2504*T[j]-51*rho*T[j]*Y)
   ix=oldnames.index(name)+1
   occurrences[name]=[r['name'] for r in old['residuals'] if any(ix in t['monomial'] for t in r['terms'])]
   assert set(occurrences[name])=={f'{prefix}.{j}',f'{prefix}.square.0',f'{prefix}.square.1'}
   expected=eps*(I[j]+2504*T[j]-S[j])+51*T[j]*Y
   assert s.expand(expression(oldrows[f'{prefix}.{j}'],oldnames)-expected)==0,(interface,label,j,expression(oldrows[f'{prefix}.{j}'],oldnames),expected)
   deleted.append(f'{prefix}.{j}')
  Isquare=components_mul(I,I)
  substitution=components_add(components_add(constant,scaled(-102*Y,common['linear'])),scaled(4*P,common['quadratic']))
  for j in range(2):
   target=f'{prefix}.square.{j}'
   auxiliary=s.Symbol(f'int_{local}_{48+j}');auxiliary2=s.Symbol(f'int_{local}_{46+j}')
   assert s.expand(expression(oldrows[target],oldnames)-(eps*auxiliary+auxiliary2-2*Isquare[j]))==0
   changed[target]=eps*auxiliary+auxiliary2-2*substitution[j]
 names=[n for n in oldnames if n not in removed]+[n for pair in FIELDS.values() for n in pair]
 indexes={n:j+1 for j,n in enumerate(names)};old_to_new={j+1:indexes[n] for j,n in enumerate(oldnames) if n in indexes}
 rows=[]
 for r in old['residuals']:
  if r['name'] in deleted:continue
  if r['name'] in changed:rows.append(row(r['name'],changed[r['name']],names))
  else:rows.append({'name':r['name'],'terms':[{'coefficient':t['coefficient'],'monomial':[old_to_new[j] for j in t['monomial']]} for t in r['terms']]})
 expressions={
  'linear':components_add(scaled(eps,common['linear']),components_add(scaled(-1,ST),scaled(3,TT))),
  'quadratic':components_add(scaled(eps,common['quadratic']),scaled(-1,TT)),
 }
 added=[]
 for role in FIELDS:
  for j in range(2):
   n=f'common.input_comparison.{role}.{j}';rows.append(row(n,expressions[role][j],names));added.append(n)
 new=dict(old)
 new.update({'variable_names':names,'variables':len(names),'residuals':rows,
  'input_comparison_stage':stage,
  'input_comparison_predecessor':relative,
  'input_comparison_predecessor_sha256':hashlib.sha256(raw).hexdigest(),
  'input_comparison_proof':'undecidability/input_comparison_v105/input_comparison_sharing.tex',
  'input_comparison_removed_coordinates':removed,
  'input_comparison_reconstruction':recovery,
  'input_comparison_occurrences':occurrences,
  'input_comparison_added_fields':FIELDS,
  'input_comparison_added_rows':added,
  'input_comparison_deleted_rows':deleted,
  'input_comparison_changed_rows':list(changed),
  'input_comparison_identity':'I_i^2=A-102*B*Y_i+4*C*P_i; A=S^2-5008*S*s+15015*s^2 is substituted directly, epsilon*B=(S-3*s)*s, epsilon*C=s^2.',
  'input_comparison_retained_pair_identity':'2601*Y_i^2+255102*epsilon*Y_i+6255001*epsilon^2-4*epsilon*P_i=0',
  'input_comparison_guard':'epsilon*rho=1 (existing row); no private quantity is inverted',
  'input_comparison_reciprocal_scope':'The reciprocal integer block has i_inverse in its first input and rPair equations instead of the common epsilon; its two comparison coordinates and all of its rows remain unchanged.',
  'input_comparison_projection_scope':'Bijective rational coordinate reconstruction on the entire predecessor zero set, including all zero input-comparison, input-square, and rPair fibers.',
  'input_comparison_new_arithmetic_premise':False,
  'input_comparison_recovery_provenance':'Independent reconstruction of the previously reported 948/1127 census. Earlier original files or commits were not recovered; this is a new exact construction, not a claim that old source files were found.',
  'input_comparison_composition':'Preferred stage starts from BB-native v104, which includes contact-denominator v103. The input-comparison rewrite changes none of their contact or pole rows.',
  'unconditional_undecidability_claim':False})
 expected={('reconstructed','general'):(948,803),('reconstructed','specified'):(1127,978),('preferred','general'):(943,798),('preferred','specified'):(1124,975)}[(stage,interface)]
 assert (len(names),len(rows))==expected
 encoded=(json.dumps(new,sort_keys=True,separators=(',',':'))+'\n').encode()
 out=HERE/f'{stage}_{interface}_quadrics.json';out.write_bytes(encoded)
 cert={'stage':stage,'interface':interface,'variables':len(names),'quadratic_rows':len(rows),'degree':4,'table_sha256':hashlib.sha256(encoded).hexdigest(),
  'predecessor_variables':old['variables'],'predecessor_rows':len(old['residuals']),
  'variable_saving':old['variables']-len(names),'row_saving':len(old['residuals'])-len(rows),
  **{k:v for k,v in new.items() if k.startswith('input_comparison_')},
  'retained_bb_native':stage=='preferred','unconditional_undecidability_claim':False}
 (HERE/f'{stage}_{interface}_certificate.json').write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n')
 return {k:cert[k] for k in ('stage','interface','variables','quadratic_rows','variable_saving','table_sha256')}

def main():
 for stage in STAGES:
  for interface in ('general','specified'):print(json.dumps(build(stage,interface),sort_keys=True))
if __name__=='__main__':main()
