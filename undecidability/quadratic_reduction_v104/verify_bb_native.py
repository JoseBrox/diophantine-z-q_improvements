#!/usr/bin/env python3
"""Independent complete row reconstruction and physical CM-pole audit."""
from __future__ import annotations
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def expression(row,names):
 return s.expand(sum(s.sympify(t['coefficient'])*s.prod(s.Symbol(names[i-1]) for i in t['monomial']) for t in row['terms']))

def same_up_to_sign(actual,expected):
 assert s.expand(actual-expected)==0 or s.expand(actual+expected)==0

def physical_maps():
 e,u,v,p,q,b,R,eps,sigma=s.symbols('e u v p q b R eps sigma',nonzero=True)
 oldphys=[3*e*e-34*e-289+17*b*p*p,17*e-e*b-17*u*v,u*u+34*u*v-867*v*v-17*b*q*q]
 newphys=[9*e*e-9+7*b*p*p,9*e-7*e*b-9*u*v,9*u*u-9*v*v-7*b*q*q]
 charts={
  'general.detector0':(1,eps**2,eps,R**2,R**2,R/eps,R),
  'general.detector1':(1,eps**2,eps,1,R**2,1/eps,R),
  'specified.detector0':(R**2,1,R,eps**2,R**2,eps*R**2,R**2),
  'specified.detector1':(R**2,1,R,eps**2,eps**2,eps*R**2,eps*R),
  'specified.detector2':(eps**2,1,eps,eps**2,eps**2,eps**3,eps**2),
  'scalar':(sigma,sigma,sigma,sigma,sigma,sigma,sigma),
 }
 output={}
 for name,(s1,s2,S,gp,gq,pm,qm) in charts.items():
  E=e*s1;B=b*s2;U=u*S;V=v*S;P=p*p*s1*s1/s2;Q=q*q*s1
  assert s.cancel(S*S-s1*s2)==0
  assert s.cancel((p*pm)**2-gp*P)==0
  assert s.cancel((q*qm)**2-gq*Q)==0
  old=[3*E*E-34*E*s1-289*s1*s1+17*B*P,17*E*s2-E*B-17*U*V,U*U+34*U*V-867*V*V-17*B*Q]
  new=[9*E*E-9*s1*s1+7*B*P,9*E*s2-7*E*B-9*U*V,9*U*U-9*V*V-7*B*Q]
  for physical,stored in ((oldphys,old),(newphys,new)):
   for target,actual,mult in zip(physical,stored,(s1*s1,S*S,S*S)):
    assert s.cancel(actual-mult*target)==0
  output[name]={'sigma1':str(s1),'sigma2':str(s2),'uv_scale':str(S),'square_multiplier_p':str(gp),'square_multiplier_q':str(gq),'p_coordinate_multiplier':str(pm),'q_coordinate_multiplier':str(qm)}
 return output

def point_construction():
 # BB's two points yield the native CM equations without any analytic calculation here.
 d,n,a,b,U,V=s.symbols('d n a b U V',nonzero=True)
 e=n/(d*a*a);p=U/(d*d*a*a);u=b/a;v=e*(1-d)/u;q=V/(d*d*a*b)
 first=s.factor(e*e+d*p*p-1)
 second=s.factor(u*u-v*v-d*q*q)
 curve1=U*U-d**3*a**4+d*n*n
 curve2=V*V-d**3*b**4+d*n*n*(1-d)**2
 assert s.cancel(first-curve1/(d**3*a**4))==0
 assert s.cancel(u*v-e*(1-d))==0
 assert s.cancel(second+curve2/(d**3*a*a*b*b))==0
 # A fully prepared rational pole example, not a full integer-definition witness.
 d=Fraction(112,841);b=Fraction(144,841);e=Fraction(3,4);p=Fraction(29,16);u=Fraction(27,29);v=Fraction(81,116);q=Fraction(27,16)
 assert d==Fraction(7,9)*b and 0<b<1
 assert d/7==Fraction(4,29)**2
 assert e*e+d*p*p==1 and u*v==e*(1-d) and u*u-v*v==d*q*q
 return {'d':str(d),'b':str(b),'e':str(e),'p':str(p),'u':str(u),'v':str(v),'q':str(q),'scope':'One exact prepared CM-pole witness; not a full-source witness or proof of BB'}

def audit(interface):
 src=ROOT/f'undecidability/quadratic_reduction_v103/denominator_{interface}_quadrics.json';raw=src.read_bytes();old=json.loads(raw)
 dest=HERE/f'bb_native_{interface}_quadrics.json';out=dest.read_bytes();new=json.loads(out)
 cert=json.loads((HERE/f'bb_native_{interface}_certificate.json').read_bytes())
 assert hashlib.sha256(raw).hexdigest()==new['bb_native_predecessor_sha256']
 assert hashlib.sha256(out).hexdigest()==cert['table_sha256']
 assert new['variable_names']==old['variable_names'] and new['variables']==old['variables']
 names=new['variable_names'];oldrows={r['name']:r for r in old['residuals']};newrows={r['name']:r for r in new['residuals']}
 assert list(newrows)==list(oldrows)
 labels=['b','g','t','m','w','s','h','c','gamma','j','i']
 if interface=='general':labels+=['power_delta','power_alpha'];eps=s.Symbol('int_b_160');eps2=s.Symbol('int_b_161');rho=s.Symbol('int_b_159');expected=(963,818,39,117)
 else:eps=s.Symbol('int_b_163');eps2=s.Symbol('int_b_164');rho=s.Symbol('int_b_162');expected=(1140,991,44,132)
 # Pin both common unit rows directly, without relying on their labels.
 retained_short=[expression(r,names) for r in old['residuals'] if len(r['terms'])==2]
 assert any(s.expand(p-(rho*eps-1))==0 or s.expand(p+(rho*eps-1))==0 for p in retained_short)
 assert any(s.expand(p-(eps2-eps*eps))==0 or s.expand(p+(eps2-eps*eps))==0 for p in retained_short)
 changed={};squares=0;pole_records=[]
 for label in labels:
  local='i_reciprocal' if label=='i' else label
  z=lambda n:s.Symbol(f'int_{local}_{n}')
  R,R2=z(90),z(89)
  same_up_to_sign(expression(oldrows[f'integer.{label}.unit.R_square'],names),R2-R*R)
  roles=[(0,3,4,66,64,65,67,5,6),(1,7,8,75,73,74,76,9,10)]
  if interface=='specified':roles +=[(2,166,167,176,174,175,177,168,169)]
  roles +=[('scalar',11,12,84,82,83,85,13,14)]
  for detector,ei,ui,vi,bi,pi,qi,psi,qsi in roles:
   E,U,V,B,P,Q,ps,qs=map(z,(ei,ui,vi,bi,pi,qi,psi,qsi))
   if detector=='scalar':
    sigma=z(81);s1=s2=gp=gq=sigma
    rownames=[f'integer.{label}.v82.scalar.{k}' for k in ('first','middle','second')]
    square_names=[f'integer.{label}.v82.scalar.{k}' for k in ('p2','q2')]
    # Scalar sigma is forced nonzero by its retained inverse equation and R!=0.
    same_up_to_sign(expression(oldrows[f'integer.{label}.v82.scalar.inverse'],names),sigma*z(88)-R2*R2)
    same_up_to_sign(expression(oldrows[f'integer.{label}.v82.scalar.input'],names),sigma*B-R2-9792*R)
   else:
    if interface=='general':s1=s.Integer(1);s2=eps2;gp=R2 if detector==0 else s.Integer(1);gq=R2
    elif detector in (0,1):s1=R2;s2=s.Integer(1);gp=eps2;gq=R2 if detector==0 else eps2
    else:s1=eps2;s2=s.Integer(1);gp=gq=eps2
    prefix=f'integer.{label}.detector{detector}.'
    rownames=[prefix+k for k in ('firstConic','Bh.definition','secondConic')]
    square_names=[prefix+k for k in ('p2.definition','q2.definition')]
   oldexpected=[3*E*E-34*E*s1-289*s1*s1+17*B*P,17*E*s2-E*B-17*U*V,U*U+34*U*V-867*V*V-17*B*Q]
   newexpected=[9*E*E-9*s1*s1+7*B*P,9*E*s2-7*E*B-9*U*V,9*U*U-9*V*V-7*B*Q]
   for n,p in zip(rownames,oldexpected):assert s.expand(expression(oldrows[n],names)-p)==0,n
   for n,p in zip(rownames,newexpected):assert s.expand(expression(newrows[n],names)-p)==0,n;changed[n]=True
   for n,p in zip(square_names,(ps*ps-gp*P,qs*qs-gq*Q)):
    same_up_to_sign(expression(oldrows[n],names),p);assert newrows[n]==oldrows[n];squares+=1
   pole_records.append({'label':label,'role':str(detector),'sigma1':str(s1),'sigma2':str(s2)})
 for name,row in oldrows.items():
  if name not in changed:assert newrows[name]==row,name
 assert new['bb_native_changed_rows']==[n for n in oldrows if n in changed]
 assert (len(names),len(newrows),len(pole_records),len(changed))==expected
 for field in ('integer_blocks','ordinary_integer_inputs','reciprocal_integer_inputs','parameters','source_coding_theorem','source_coding_theorem_independently_reproved','source_universality_hypothesis'):
  assert new[field]==old[field]
 for field in ('bb_native_old_non_cm_pole_required','bb_native_route_k_required','bb_native_original_theorem_5_3_required','bb_native_cr3_required','bb_native_proposition_n_required','unconditional_undecidability_claim'):
  assert new[field] is False
 assert new['bb_native_retained_non_pole_arithmetic_interfaces'] is True
 assert cert['variables']==len(names) and cert['quadratic_rows']==len(newrows)
 support=set();parameters=[s.Symbol(p) for p in new['parameters']]
 for row in new['residuals']:
  for t in row['terms']:
   assert len(t['monomial'])<=2;support.update(t['monomial'])
   assert all(c.is_Integer for c in s.Poly(s.sympify(t['coefficient']),*parameters).coeffs())
 assert support==set(range(1,len(names)+1))
 return {'interface':interface,'variables':len(names),'quadratic_rows':len(newrows),'poles':len(pole_records),'changed_rows':len(changed),'unchanged_rows':len(newrows)-len(changed),'pinned_square_rows':squares,'source_sha256':hashlib.sha256(raw).hexdigest(),'table_sha256':hashlib.sha256(out).hexdigest(),'status':'PASS'}

def main():
 print(json.dumps({'physical_maps':physical_maps(),'point_construction':point_construction(),'results':[audit(x) for x in ('general','specified')],'scope':'Exact physical maps and complete coefficient audit. External BB point existence and retained non-pole arithmetic interfaces are not proved by this finite check.'},sort_keys=True))
if __name__=='__main__':main()
