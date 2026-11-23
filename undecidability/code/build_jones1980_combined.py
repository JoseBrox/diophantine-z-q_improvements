#!/usr/bin/env python3
"""Combine the emended Jones-type source with actual integer blocks.

Three square registers are shared with input squares already present in the
integer blocks. The reciprocal integer input is homogenized at its nonzero
denominator. Arithmetic assumptions of the chosen integer block are retained.
Undecidability additionally requires the unverified universality premise U_em.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json
from pathlib import Path
import sympy as sp
from quadratic_utils import SOURCES, rechart179, sparse_rows, expr_from_row

def module(path):
 spec=importlib.util.spec_from_file_location('jones1980_source',path)
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def build(m,repo,source_path):
 source=module(source_path).build_system()
 vs=source['variables'];s=source['symbols'];ps=list(source['parameters'])
 original_rows=source['rows']
 core_hash=hashlib.sha256('\n'.join(k+':'+sp.srepr(v) for k,v in original_rows.items()).encode()).hexdigest()
 c=sp.Symbol('c')
 ordinary=[c if v==s['phi'] else v for v in source['ordinary_integrality_inputs']]
 reciprocal=list(source['reciprocal_integrality_inputs'])
 assert len(ordinary)==11 and reciprocal==[s['i_inverse']]
 labels=[str(v) for v in ordinary]+['i_reciprocal']
 block_path=repo/SOURCES[m];block_bytes=block_path.read_bytes();block=json.loads(block_bytes)
 rechart=None
 if m==179:block,rechart=rechart179(block)
 par=sp.Symbol('C_parameter') if m==163 else sp.Symbol('B_abc') if m==56 else sp.Integer(1)
 if par!=1:ps.append(par)
 arrays={name:{j:sp.Symbol(f'int_{name}_{j}') for j in range(2,m+1)} for name in labels}
 if m==163: sq_index,q_index,inv_index,inv2_index=37,159,160,161
 elif m==179:sq_index,q_index,inv_index,inv2_index=37,162,163,164
 else:sq_index,q_index,inv_index,inv2_index=29,None,None,None
 def at(name,index):return arrays[name][index] if index else sp.Integer(1)
 def q(name):return at(name,q_index)
 def inv(name):return at(name,inv_index)
 def inv2(name):return at(name,inv2_index)
 def sq(name):return at(name,sq_index)
 qb,ub=q('b'),sq('b');qg,ug=q('g'),sq('g');qc,uc=q('c'),sq('c')
 phi_sub={s['phi']:c-2*s['r']-1}
 rows=[]
 b2=s['b2'];g2=s['g2'];C2=s['C2'];el=s['el']
 uses={str(v):[name for name,row in original_rows.items() if v in row.free_symbols] for v in [b2,g2,C2,el,s['M']]}
 assert set(uses['g2'])=={'g2.definition','positive.alpha'}
 assert set(uses['el'])=={'el.definition','positive.alpha'}
 assert set(uses['C2'])=={'C2.definition','d.norm','E.reciprocal'}
 assert set(uses['M'])=={'M.definition','a.definition'}
 for name,original in original_rows.items():
  if name in ['b2.definition','g2.definition','C2.definition','M.definition']:continue
  expr=sp.expand(original.subs(phi_sub,simultaneous=True))
  if b2 in expr.free_symbols:
   poly=sp.Poly(expr,b2);degree=poly.degree()
   assert degree in [1,2]
   if degree==1:
    A=poly.coeff_monomial(1);B=poly.coeff_monomial(b2)
    expr=sp.expand(A*inv('b')+ub*B)
    # Equality modulo the existing inverse relation, checked as a Laurent identity.
    expected=sp.expand(original.subs(phi_sub,simultaneous=True).subs(b2,qb*ub)/qb)
   else:
    A=poly.coeff_monomial(1);B=poly.coeff_monomial(b2*b2)
    assert poly.coeff_monomial(b2)==0 and not B.free_symbols
    expr=sp.expand(A*inv2('b')+B*ub*ub)
    expected=sp.expand(original.subs(phi_sub,simultaneous=True).subs(b2,qb*ub)/qb**2)
   if m!=56:
    assert sp.cancel((expr-expected).subs({inv('b'):1/qb,inv2('b'):1/qb**2},simultaneous=True))==0
   else:assert sp.expand(expr-expected)==0
  if name=='el.definition':expr=el*inv('g')-s['e']*s['ell']
  elif name=='positive.alpha':
   expr=sp.expand(expr.subs({g2:qg*ug,el:el/qg},simultaneous=True))
  expr=sp.expand(expr.subs(C2,qc*uc))
  if name=='a.definition':
   expr=2*s['sr']*s['a']-(s['p']+2*s['sr2'])*s['n2']
   # Recover the old integer-polynomial value before dividing by nonzero sr.
   assert sp.expand(expr.subs({s['p']:2*s['U']*s['sr']**2,
                              s['sr2']:s['sr']**2,
                              s['a']:(s['U']+1)*s['sr']*s['n2']},simultaneous=True))==0
  rows.append((f'jones1980.{name}',expr))
 core=[c if v==s['phi'] else v for v in vs if v not in {b2,g2,C2,s['M']}]
 core_count=len(core);outer_count=len(rows)
 assert core_count==len(vs)-4 and outer_count==len(original_rows)-4
 input_map={str(v):v for v in ordinary};input_map['i_reciprocal']=sp.Integer(1)
 den=s['i_inverse']
 for name in labels:
  coords={1:input_map[name],**arrays[name]}
  for old in block['residuals']:
   result=0
   for term in old['terms']:
    val=sp.Integer(term['coefficient'])*par**term.get('parameterPower',0)
    val*=sp.prod(coords[j] for j in term['monomial'])
    if name=='i_reciprocal':val*=den**(2-len(term['monomial']))
    result+=val
   result=sp.expand(result)
   if name=='i_reciprocal':
    expected=den**2*expr_from_row(old,{j:v/den for j,v in coords.items()},par)
    assert sp.cancel(result-expected)==0
   rows.append((f'integer.{name}.{old["name"]}',result))
 variables=core+[arrays[name][j] for name in labels for j in range(2,m+1)]
 assert len(variables)==core_count+12*(m-1)
 assert len(rows)==outer_count+12*len(block['residuals'])
 sparse=sparse_rows(rows,variables,ps)
 status='exact algebraic checkpoint; undecidability conditional on U_em and all retained integer-predicate premises'
 data={
  'status':status,'source_universality':source['source'],
  'universality_hypothesis':'U_em','universality_independently_verified':False,
  'source_core_sha256':core_hash,'variables':len(variables),'variable_names':list(map(str,variables)),
  'parameters':list(map(str,ps)),'input_is_fixed_coefficient':'x',
  'degree_of_each_residual_at_most':2,'sum_of_squares_degree':4,
  'ordinary_integer_inputs':list(map(str,ordinary)),
  'reciprocal_integer_inputs':['1/i_inverse'],
  'reciprocal_nonzero_guard':'i_inverse*E=c^2 and c=2*r+1+phi>0',
  'integer_definition_source':SOURCES[m],'integer_definition_source_sha256':hashlib.sha256(block_bytes).hexdigest(),
  'integer_definition_total_variables':m,'integer_blocks':12,
  'outer_coordinates':core_count,'outer_residuals':outer_count,
  'square_sharing':{'b2':str(qb*ub),'g2':str(qg*ug),'C2':str(qc*uc)},
  'el_recovery':str(el*inv('g')),'phi_recovery':str(phi_sub[s['phi']]),
  'M_recovery':'sr*n2','a_recovery':'(U+1)*sr*n2',
  'source_occurrences':uses,'rechart179':rechart,
  'power_chain':source['power_chain'],'power_multiplications':len(source['power_chain']),
  'residuals':sparse,
 }
 cert={k:v for k,v in data.items() if k not in ['residuals','variable_names','power_chain']}
 cert['quadratic_residuals']=len(rows)
 cert['verified']=['all input-square sharing identities','el Laurent rescaling','affine replacement of phi by c','M elimination at sr>0',
    'every reciprocal input homogenization identity','each 179 Laurent rechart row' if m==179 else 'original integer block unchanged',
    'integer parameter-polynomial coefficients','degree at most two','all coordinates occur','complete sparse table materialized']
 cert['not_verified']=['universality U_em of the precise emended system','all retained arithmetic interfaces','global minimality']
 return data,cert

def main():
 ap=argparse.ArgumentParser();base=Path(__file__).resolve().parents[2]
 ap.add_argument('--repo',type=Path,default=base)
 ap.add_argument('--source',type=Path,default=Path(__file__).resolve().parent/'jones1980_system.py')
 ap.add_argument('--out',type=Path,default=base/'undecidability/coefficients/jones1980')
 ap.add_argument('--m',type=int,choices=list(SOURCES),nargs='+',default=[163,179,56]);args=ap.parse_args()
 args.out.mkdir(parents=True,exist_ok=True)
 for m in args.m:
  data,cert=build(m,args.repo.resolve(),args.source.resolve())
  path=args.out/f'jones1980_m{m}_quadrics.json';path.write_text(json.dumps(data,separators=(',',':'),sort_keys=True)+'\n')
  cert['table_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
  (args.out/f'jones1980_m{m}_certificate.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
  print(json.dumps({'m':m,'N':data['variables'],'quadrics':len(data['residuals']),'outer':data['outer_coordinates'],'sha256':cert['table_sha256']}))
if __name__=='__main__':main()
