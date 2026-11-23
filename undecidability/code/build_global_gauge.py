#!/usr/bin/env python3
"""Compile the complete quadratic systems with one global contact gauge.

The algebraic maps and finite counts are exact. Their arithmetic interpretation
retains the stated integrality interfaces and the unresolved universality
assertion U_em. No unconditional undecidability claim is made.
"""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from itertools import product
from fractions import Fraction
from math import gcd,lcm
import json,sys,hashlib
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'undecidability/code'))
from quadratic_utils import SOURCES,rechart179

def pairmul(a,b):return (sp.expand(a[0]*b[0]+2*a[1]*b[1]),sp.expand(a[0]*b[1]+a[1]*b[0]))
def padd(a,b):return tuple(sp.expand(x+y)for x,y in zip(a,b))
def psub(a,b):return tuple(sp.expand(x-y)for x,y in zip(a,b))
def pscale(a,c):return tuple(sp.expand(c*x)for x in a)

# Functions of common H, roles2/3/4, and the common input numerator.
# Nonzero R-weights are filtered below; physical R-dependent Pstar/Jhat are
# not members of this list. Product registers128:131 are redefined below.
PHYSICAL_COMMON=[15,16,17,18,19,20,23,24,33,34,35,36,39,40,41,42,43,44,
 *range(46,52),54,55,64,65,*range(66,74),102,103,150,151,
 *range(182,188),190,191,194,195,201,202,205,206,
 *range(213,237),120,121,122,123,124,125,610,611]

def last_gate_rows(m,maps):
 last=1 if m==163 else 2
 b,nr,inv=(96,95,311)if m==163 else(582,581,312)
 # The former last weight c-q0[-q1] is now an independent physical X620.
 def term(a,cp=0,mon=()):return {'coefficient':str(a),'parameter_power':0,'c_power':cp,'R_power':0,'monomial':list(mon)}
 return [
 {'name':f'balanced.detector{last}.poleInput.definition','terms':[term(167281,1,(b,)),term(167281,1,(b,620)),term(-166464,2,(nr,nr))]},
 {'name':f'shared.inverse{last}','terms':[term(1,1),term(-1,0,(620,inv))]},
 {'name':f'shared.gate{last}','terms':[term(2,1,(nr,)),term(-1),term(-1,0,(305,305)),term(-1,1,(inv,)),term(2,1),term(-1,0,(620,))]}]

def compile_physical_rows(m,maps,rows):
 cw={int(k):v for k,v in maps['c_weights'].items()};cw[620]=2
 rw={int(k):v for k,v in maps['R_weights'].items()};rw[620]=0
 kw={int(k):v for k,v in maps['parameter_weights'].items()};kw[620]=0
 rc=maps['row_c_R_weights'];rk=maps['row_parameter_weights']
 units=[(0,0,()),(1,0,(400,)),(-1,0,(401,)),(-2,0,(402,)),(0,1,(113,)),(0,2,(112,))]
 if m==179:units.append((0,-1,(114,)))
 for x,y in product(units[1:].copy(),repeat=2):
  z=(x[0]+y[0],x[1]+y[1],tuple(sorted(x[2]+y[2])))
  if z not in units:units.append(z)
 choose={}
 for a,b,mon in sorted(units,key=lambda z:(len(z[2]),z[2])):choose.setdefault((a,b),mon)
 ans=[]
 for row in rows:
  hc,hr=rc[row['name']];out=defaultdict(Fraction)
  for t in row['terms']:
   mon=t['monomial'];rest=tuple(j for j in mon if j!=112)
   e=t['c_power']+sum(cw[j]for j in rest)-hc
   r=t['R_power']+2*mon.count(112)+sum(rw[j]for j in rest)-hr
   p=t['parameter_power']+sum(kw[j]for j in rest)-rk[row['name']]if m==163 else 0
   helper=choose[e,r];newmon=tuple(sorted(rest+helper))
   assert len(newmon)<=2 and p>=0,(m,row['name'],e,r,newmon,p)
   out[p,newmon]+=Fraction(t['coefficient'])
  den=lcm(*(x.denominator for x in out.values()));val={key:int(x*den)for key,x in out.items()if x}
  common=gcd(*val.values());val={key:x//common for key,x in val.items()}
  ans.append({'name':row['name'],'terms':[{'monomial':list(mon),'coefficient':str(a),'parameterPower':p}for(p,mon),a in sorted(val.items())]})
 return ans

def build(m,root=ROOT):
 path=root/f'undecidability/coefficients/jones1980_common_points/common_points_m{m}_quadrics.json'
 oldbytes=path.read_bytes();old=json.loads(oldbytes)
 maps=json.loads((root/f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
 src=json.loads((root/SOURCES[m]).read_text())
 if m==179:src,_=rechart179(src)
 labels={int(k):v for k,v in maps['source_labels'].items()}
 assert len(PHYSICAL_COMMON)==len(set(PHYSICAL_COMMON))
 common=[j for j in PHYSICAL_COMMON if maps['R_weights'][str(j)]==0]
 common+=list(range(128,132))+[400,401,402]
 assert len(common)==(91 if m==163 else 93),(m,len(common))
 blocks=old['ordinary_integer_inputs']+['i_reciprocal'];assert len(blocks)==12
 def sym(name):return sp.Symbol(name)
 def oldslot(b,j):return f'int_{b}_{labels[j]}'
 # Only live private copies need identification; old common fields already
 # have canonical b-block names.
 rename={oldslot(b,j):oldslot('b',j)for b in blocks if b!='b'for j in common}
 rename={a:b for a,b in rename.items()if a in old['variable_names']}
 def name(b,j):
  if j==620:return f'int_{b}_last_contact_weight'
  original=oldslot(b,j)
  if original not in old['variable_names']:original=oldslot('b',j)
  return rename.get(original,original)
 def Z(b,j):return sym(name(b,j))
 C=sp.Symbol('C_parameter')if m==163 else sp.Integer(1)
 c=Z('b',400);ci=Z('b',401);ci2=Z('b',402)
 changed=compile_physical_rows(m,maps,last_gate_rows(m,maps))
 changed_by={r['name']:r for r in changed}
 # Independent local identity: the three new physical rows specialize to
 # their old physical rows under X620=c-X300[-X301].
 physical=json.loads((root/f'computation/variable_reductions_v82/general/source{m}.json').read_text())
 oldphysical={r['name']:r for r in physical['rows']}
 pc=sp.Symbol('physical_c');px={j:sp.Symbol('X'+str(j))for j in labels};px[620]=sp.Symbol('X620')
 def phys(r):return sum(sp.Integer(t['coefficient'])*pc**t['c_power']*sp.prod(px[j]for j in t['monomial'])for t in r['terms'])
 for row in last_gate_rows(m,maps):
  qlast=pc-px[300]-(px[301]if m==179 else 0)
  assert sp.expand(phys(row).subs(px[620],qlast)-phys(oldphysical[row['name']]))==0,row['name']
 oldnames=old['variable_names'];rows=[];replaced=[]
 pair_names={'new1.d_piF.0','new1.d_piF.1','new1.sum.0','new1.sum.1','new1.d_Gh.0','new1.d_Gh.1','new1.unit.0','new1.unit.1'}
 prodnames={f'amplified.det0.product{k}.{j}.definition'for k in [1,2,3]for j in [0,1]}
 def local_rows_to_expr(row,b):return sum(sp.Integer(t['coefficient'])*C**t.get('parameterPower',0)*sp.prod(Z(b,j)for j in t['monomial'])for t in row['terms'])
 for row in old['residuals']:
  n=row['name']
  if n.startswith('integer.'):
   _,label,local=n.split('.',2);b='i_reciprocal'if label=='i'else label
   if local in pair_names or local in prodnames:continue
   if local in changed_by:
    expr=local_rows_to_expr(changed_by[local],b);replaced.append(n)
   else:
    expr=sum(sp.sympify(t['coefficient'])*sp.prod(sym(rename.get(oldnames[j-1],oldnames[j-1]))for j in t['monomial'])for t in row['terms'])
  else:
   expr=sum(sp.sympify(t['coefficient'])*sp.prod(sym(rename.get(oldnames[j-1],oldnames[j-1]))for j in t['monomial'])for t in row['terms'])
  rows.append((n,sp.expand(expr)))
 assert len(replaced)==36
 Fhat=(sym('common_input_F_over_c_real'),sym('common_input_F_over_c_imag'))
 xU=(sym('common_input_x_real'),sym('common_input_x_imag'))
 def field(b,j):return (Z(b,j),Z(b,j+1))
 F=field('b',205);s=field('b',201);D=(sp.Integer(11),sp.Integer(-6))
 common_curve=[('global.common_input.scale',psub(F,pscale(Fhat,c))),
  ('global.common_input.unit',psub(pairmul(F,xU),(sp.Integer(1),sp.Integer(0)))),
  ('global.common_input.curve',psub(xU,padd(pairmul(s,s),pairmul(D,F))))]
 for b in blocks:
  t=field(b,203);G=field(b,207);eta=field(b,209)
  eq1=psub(pairmul(Fhat,padd(eta,padd(s,t))),pairmul(eta,G))
  eq2=padd(psub(pairmul(D,padd(F,pscale(G,c))),pairmul(psub(s,t),eta)),pairmul(t,t))
  for j,e in enumerate(eq1):rows.append((f'global.{b}.input_pair.product.{j}',e))
  for j,e in enumerate(eq2):rows.append((f'global.{b}.input_pair.sum.{j}',e))
  # Reverse the factor chain: first multiply the three common factors,
  # then multiply their common product by this block's private factor0.
  f0,f1,f2,f3=(field(b,j)for j in [118,120,122,124])
  A,B,W=(field(b,j)for j in [128,130,302])
  for k,e in enumerate([psub(pairmul(f1,f2),pscale(A,ci2)),psub(pairmul(A,f3),pscale(B,ci2)),psub(pairmul(f0,B),pscale(W,ci2))],1):
   for j,component in enumerate(e):rows.append((f'global.{b}.factor_product{k}.{j}',component))
 for n,e in common_curve:
  for j,x in enumerate(e):rows.append((n+f'.{j}',x))
 # The last stored weight is eliminated from the linear global relation.
 # In physical scale every contact weight is c^2 times its stored variable.
 qs=[]
 for b in blocks:
  qs.extend([Z(b,300)]+([Z(b,301)]if m==179 else[])+[Z(b,620)])
 gone=Z('i_reciprocal',620);replacement=ci-sum(q for q in qs if q!=gone)
 rows=[(n,sp.expand(e.subs(gone,replacement)))for n,e in rows]
 # Delete old d coordinate pairs: complete occurrence audit below checks
 # they disappeared with their four finite-pair equations.
 deleted_d={oldslot(b,j)for b in blocks for j in [211,212]}
 names=[n for n in oldnames if n not in rename and n not in deleted_d]
 names += [name(b,620)for b in blocks if b!='i_reciprocal']+[str(x)for x in (*Fhat,*xU)]
 assert len(names)==len(set(names))
 ids={n:j+1 for j,n in enumerate(names)};parameters=set(old['parameters']);paramsyms=set(map(sp.Symbol,parameters))
 final=[];seen={};duplicates=[]
 for n,e in rows:
  variables=sorted(e.free_symbols-paramsyms,key=str)
  assert set(map(str,variables))<=set(names),(n,set(map(str,variables))-set(names))
  poly=sp.Poly(e,*variables)if variables else None
  assert poly is None or poly.total_degree()<=2,(n,e)
  terms=[]
  for powers,a in poly.terms()if poly is not None else[((),e)]:
   mon=sorted(ids[str(v)]for v,power in zip(variables,powers)for _ in range(power))
   terms.append({'monomial':mon,'coefficient':str(a)})
  terms.sort(key=lambda t:t['monomial']);key=json.dumps(terms,sort_keys=True)
  if key in seen:
   duplicates.append({'name':n,'identical_to':seen[key]});continue
  seen[key]=n;final.append({'name':n,'terms':terms})
 assert {j for r in final for t in r['terms']for j in t['monomial']}==set(range(1,len(names)+1))
 assert len(names)==(1185 if m==163 else 1355),(m,len(names))
 ans=dict(old);ans.update({'variables':len(names),'variable_names':names,'residuals':final,
 'global_contact_gauge':True,'global_contact_weights':len(qs),'global_contact_sum_elimination':str(gone)+' = '+str(replacement),
 'global_shared_source_labels':common,'global_shared_coordinate_count_before_input_chart':len(common),
 'global_input_chart_removed_coordinates':sorted(deleted_d),'global_input_chart_added_coordinates':list(map(str,(*Fhat,*xU))),
 'global_duplicate_rows_removed':duplicates,'global_modified_last_gate_rows':replaced,
 'global_gauge_predecessor_sha256':hashlib.sha256(oldbytes).hexdigest(),
 'global_gauge_status':'proved transfer under retained arithmetic interfaces; U_em remains unverified',
 'global_gauge_finite_verification':'complete rational quadratic table; independent verifier in undecidability/verify_global_gauge.py',
 'global_gauge_scope':'no abc assumption added; the retained arithmetic interfaces and U_em are still hypotheses',
 'global_chart_equivalence':'exact over Q(sqrt(2)) including tangent and zero-d boundaries',
 'global_factor_product_reordered':True})
 return ans

if __name__=='__main__':
 out=ROOT/'undecidability/coefficients/jones1980_global_gauge';out.mkdir(exist_ok=True)
 for m in [163,179]:
  d=build(m);p=out/f'global_gauge_m{m}_quadrics.json'
  p.write_text(json.dumps(d,separators=(',',':'),sort_keys=True)+'\n')
  cert={
   'interface_coordinates':m,'variables':d['variables'],'quadratic_rows':len(d['residuals']),
   'degree':4,'shared_source_coordinates':d['global_shared_coordinate_count_before_input_chart'],
   'duplicate_rows_removed':len(d['global_duplicate_rows_removed']),
   'table_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
   'predecessor_sha256':d['global_gauge_predecessor_sha256'],
   'source_universality_hypothesis':'U_em','source_universality_verified':False,
   'unconditional_undecidability_claim':False,
   'retained_arithmetic_interfaces':True,'new_abc_assumption':False,
   'private_contacts_per_block':2 if m==163 else 3,'integer_input_blocks':12,
   'common_input_chart_coordinates_added':4,'private_input_chart_coordinates_removed':24,
   'arithmetic_proof':'undecidability/papers/global_gauge_quartic_checkpoint.tex',
   'independent_verifier':'undecidability/verify_global_gauge.py'
  }
  (out/f'global_gauge_m{m}_certificate.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
  print({'m':m,'N':d['variables'],'rows':len(d['residuals']),'duplicates':len(d['global_duplicate_rows_removed']),'sha256':cert['table_sha256']})
