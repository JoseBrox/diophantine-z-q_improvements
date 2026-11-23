"""Exact quadratic-table conversion and the reversible 179-coordinate rechart."""
import sympy as sp

SOURCES={
 163:'computation/variable_reductions_v82/general/quartic163/quadrics.json',
 179:'computation/variable_reductions_v82/general/quartic179/quadrics.json',
 56:'computation/variable_reductions_v81/abc/quartic56/quadrics.json',
}

def expr_from_row(row,coords,parameter):
 return sp.expand(sum(sp.Integer(t['coefficient'])*parameter**t.get('parameterPower',0)
                      *sp.prod(coords[i] for i in t['monomial']) for t in row['terms']))

def rechart179(data):
 """Change only three registers; the existing unit guards remain literal."""
 assert data['variables']==179
 yy={i:sp.Symbol(f'v{i}') for i in range(1,180)}
 q=yy[162]; inv=yy[163]; inv2=yy[164]
 weights={37:2,77:2,78:4}
 powers={'inputSquare.definition':0,
         'scalar.rPair1.definition':4,
         'scalar.four_contact_product.definition':4,
         'scalar.forced_prime.definition':4,
         'input.cleared.0':2,'input.cleared.1':2}
 helper={162:1,163:-1,164:-2}
 def hpower(e,degree):
  if e==0:return sp.Integer(1)
  if degree==1:
   return {1:q,-1:inv,-2:inv2}[e]
  assert degree==0
  return {1:q,2:q*q,-1:inv,-2:inv2,-3:inv*inv2,-4:inv2*inv2}[e]
 result=[]
 for row in data['residuals']:
  if row['name'] not in powers:
   assert all(i not in weights for t in row['terms'] for i in t['monomial'])
   result.append(row); continue
  out=0; r=powers[row['name']]
  for t in row['terms']:
   mon=[i for i in t['monomial'] if i not in helper]
   exponent=sum(helper.get(i,weights.get(i,0)) for i in t['monomial'])-r
   out+=sp.Integer(t['coefficient'])*sp.prod(yy[i] for i in mon)*hpower(exponent,len(mon))
  out=sp.expand(out)
  original=expr_from_row(row,yy,sp.Integer(1))
  want=original.subs({yy[i]:q**w*yy[i] for i,w in weights.items()},simultaneous=True)/q**r
  unit_sub={inv:1/q,inv2:1/q**2}
  assert sp.cancel((want-out).subs(unit_sub,simultaneous=True))==0
  terms=[]
  active=sorted(out.free_symbols,key=lambda v:int(str(v)[1:]))
  for mon,coeff in sp.Poly(out,*active).terms():
   inds=sorted([int(str(v)[1:]) for v,e in zip(active,mon) for _ in range(e)])
   assert len(inds)<=2 and coeff.is_Integer
   terms.append({'parameterPower':0,'monomial':inds,'coefficient':str(coeff)})
  result.append({'name':row['name'],'terms':terms})
 assert {r['name'] for r in result}=={r['name'] for r in data['residuals']}
 out=dict(data);out['residuals']=result
 # Verify the unchanged literal guards, rather than assuming them away.
 original_by_name={r['name']:r for r in data['residuals']}
 new_by_name={r['name']:r for r in result}
 for name in ['unit.c_inverse','unit.c_inverse_square']:
  assert new_by_name[name]==original_by_name[name]
 assert expr_from_row(new_by_name['inputSquare.definition'],yy,sp.Integer(1))==yy[1]**2-yy[37]*q
 return out,{'coordinate_weights':weights,'row_weights':powers,'unit':162,'inverse':163,'inverse_square':164,
             'proof':'old(v37,v77,v78)=(q^2*v37,q^2*v77,q^4*v78); all literal unit guards retained'}

def sparse_rows(rows,variables,parameters):
 ids={v:i+1 for i,v in enumerate(variables)}; unknown=set(variables)
 support=set(); maximum_degree=0; result=[]
 for name,expression in rows:
  expression=sp.expand(expression)
  assert expression!=0,name
  active=sorted(expression.free_symbols&unknown,key=ids.get)
  terms=[]
  poly=sp.Poly(expression,*active)
  for mon,coeff in poly.terms():
   indices=[ids[v] for v,e in zip(active,mon) for _ in range(e)]
   degree=len(indices); maximum_degree=max(maximum_degree,degree)
   assert degree<=2,(name,expression)
   assert coeff.free_symbols<=set(parameters),(name,coeff)
   assert sp.Poly(coeff,*parameters).domain.is_ZZ,(name,coeff)
   support.update(indices)
   terms.append({'monomial':indices,'coefficient':str(sp.expand(coeff))})
  result.append({'name':name,'terms':terms})
 assert support==set(range(1,len(variables)+1)),(len(support),len(variables))
 assert maximum_degree==2
 return result
