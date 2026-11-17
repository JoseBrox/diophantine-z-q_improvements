#!/usr/bin/env python3
"""Exact construction of the 194-coordinate quartic from the SAT Laurent certificate.
Coefficients lie in Z[C]; C=149^N is fixed, never quantified.
"""
from fractions import Fraction as Q
from collections import defaultdict
from pathlib import Path
from hashlib import sha256
import itertools,json,math,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE
SOURCE=HERE/'source/reversed_reference_basis.json'
MODEL=HERE/'coordinate-model.json';SOL=HERE/'laurent-certificate.json'
# A monomial key is (C exponent, active-coordinate tuple, (u,v) exponent).
def clean(d):return {k:c for k,c in d.items()if c}
def add(*ps):
 r=defaultdict(Q)
 for p in ps:
  for k,c in p.items():r[k]+=c
 return clean(r)
def scale(p,c):return {k:c*v for k,v in p.items()if c*v}
def mul(p,q):
 r=defaultdict(Q)
 for (a,m,e),c in p.items():
  for (b,n,f),d in q.items():r[(a+b,tuple(sorted(m+n)),(e[0]+f[0],e[1]+f[1]))]+=c*d
 return clean(r)
def con(c):return {(0,(),(0,0)):Q(c)}if c else{}
def cp(k):return {(k,(),(0,0)):Q(1)}
def unit(e):return {(0,(),tuple(e)):Q(1)}
def var(i):return {(0,(i,),(0,0)):Q(1)}
def fa(a,b):return add(a[0],b[0]),add(a[1],b[1])
def fs(a,c):return scale(a[0],c),scale(a[1],c)
def fm(a,b):return add(mul(a[0],b[0]),scale(mul(a[1],b[1]),2)),add(mul(a[0],b[1]),mul(a[1],b[0]))
def fv(i,imag=1):return var(i),scale(var(i+1),imag)
def fu(e):return unit(e),{}
def fc(k):return cp(k),{}
def fn(c):return con(c),{}
def bar(a):return a[0],scale(a[1],-1)
def support(ps):return {(m,e)for p in ps for a,m,e in p}
def parse(row,base):
 out=defaultdict(Q)
 for t in row['terms']:
  m=[];e=[0,0]
  for i in t['monomial']:
   if i in base:e=[a+b for a,b in zip(e,base[i])]
   else:m.append(i)
  out[(t['parameterPower'],tuple(m),tuple(e))]+=Q(t['coefficient'])
 return clean(out)
def serial_laurent(p):return [{'parameterPower':a,'monomial':list(m),'unitPower':list(e),'coefficient':str(c)}for (a,m,e),c in sorted(p.items())]

def build(restore=False):
 model=json.loads(MODEL.read_text());sol=json.loads(SOL.read_text());src=json.loads(SOURCE.read_text())
 assert sol['status']=='sat';assert sol['model_sha256']==sha256(MODEL.read_bytes()).hexdigest()
 base={int(k):tuple(v)for k,v in model['base_units'].items()};active=set(model['active'])
 old={r['name']:parse(r,base)for r in src['residuals']}
 original_path=HERE/'source/source195.json'
 reference_names=[]
 if restore:
  mapping=json.loads((HERE/'source/reference-row-map.json').read_text())
  reference_names=mapping['names'];original=json.loads(original_path.read_text());original_rows={r['name']:parse(r,base)for r in original['residuals']}
  assert len({tuple(sol['row_weights'][n])for n in reference_names})==1
  for j,n in enumerate(reference_names):
   assert old[n]==add(*[scale(original_rows[nn],Q(mapping['matrix'][j][k]))for k,nn in enumerate(reference_names)])
 groups={};u=fu((1,0));ui=fu((-1,0));one=fn(1);D=(con(11),con(-6))
 def fld(n,z):groups[n]=list(z)
 pairs={1:(201,203,205,207,209,211),3:(213,215,217,219,221,223),4:(225,227,229,231,233,235)}
 raws={}
 for role,ids in pairs.items():
  s,t,F,G,h,d=map(fv,ids);p=fa(fa(h,s),t)
  fld(f'new{role}.d_piF',fa(d,fs(fm(p,F),-1)))
  fld(f'new{role}.sum',fa(fa(fm(D,fa(F,G)),fs(fm(fa(s,fs(t,-1)),h),-1)),fm(t,t)))
  fld(f'new{role}.d_Gh',fa(d,fs(fm(G,h),-1)))
  fld(f'new{role}.unit',fa(fa(one,fs(fm(d,fa(s,fs(t,-1))),-1)),fm(D,fm(F,G))))
  raws['A'+str(role)]=F;raws['B'+str(role)]=bar(G)
  Ei={1:31,3:39,4:43}[role]
  fld(f'cleared.E{role}',fa(fa(fv(Ei),fs(fm(fv(17),bar(t)),-1)),fm(bar(fv(150)),s)))
 fld('cleared.E2',fa(fa(fm((var(113),{}),fv(35)),fm(fv(17),bar(fa(fv(184),fv(188))))),fm(bar(fv(150)),fa(fv(182),fv(188)))))
 for role,E,J in [(1,31,60),(2,35,66),(3,39,68),(4,43,70)]:
  fld(f'cleared.E{role}.square',fa(fm(fm(fc(1),u),fv(J,2)),fs(fm(fv(E),fv(E)),-1)))
 # The two ordinary retained raw-square helpers are physical, without unit offsets.
 fld('new.square.237',fa(fv(237),fs(fm(raws['A4'],raws['A4']),-1)))
 # Store G4² before conjugation, consistently with the old helper convention.
 G4=fv(231)
 fld('new.square.239',fa(fv(239),fs(fm(G4,G4),-1)))
 beta_st=(add(scale(var(45),51),scale(unit((1,0)),2504)),{})
 fld('input.cleared',fa(fa(fv(29),fs(fv(17),-1)),fm(beta_st,fv(201))))
 fld('input.cleared.square',fa(fm(u,fv(62,2)),fs(fm(fv(29),fv(29)),-1)))
 fld('input.cleared.fourth',fa(fm(u,fv(116)),fs(fm(fv(62,2),fv(62,2)),-1)))
 # Physical A=C*x33/u; Ccal=x46/u, P=x41/u, Qcal=x48/u,
 # H=(x50+2rho*x51)/u, H²=(x72+4rho*x73)/u.
 A_st=fm(fc(1),fv(33));w=fv(225);S=fm(ui,fv(17))
 fld('homogeneous.C',fa(fv(46),fs(fm(fa(A_st,fs(u,-1)),fa(w,fs(S,4))),-1)))
 fld('homogeneous.Q',fa(fm(u,fv(48)),fs(fm(fa(A_st,u),fv(41)),-1)))
 fld('homogeneous.H',fa(fa(fa(fa(fm(u,fv(50,2)),fs(fm(fv(41),fv(41)),-1)),fs(fm(fv(46),fv(46)),-1)),fm(fv(46),fv(48))),fm(fm(u,u),fm(w,w))))
 fld('homogeneous.H.square',fa(fm(u,fv(72,4)),fs(fm(fv(50,2),fv(50,2)),-1)))
 fld('homogeneous.P.ratio',fa(fm(fv(41),fv(213)),fs(fm(fv(17),w),-2)))
 agg=add(scale(var(2),2),scale(var(86),-2),scale(unit((1,0)),14),var(192))
 for ids in pairs.values():
  s,t,F,G,h,d=map(fv,ids);p=fa(fa(h,s),t)
  agg=add(agg,mul(unit((1,0)),fm(h,p)[0]))
 groups['new.aggregate']=[agg]
 # Complete physical test values. A quadratic slot squares one of these
 # field functions; a linear slot uses the listed fourth/squared value.
 quad={
  'C2':fm(fm(fc(1),ui),fv(66,2)),
  'C3':fm(fm(fc(1),ui),fv(68,2)),
  'C4':fm(fm(fc(1),ui),fv(70,2)),
  'GL':fm(ui,fv(72,4)),
  'A1':raws['A1'],'B1':raws['B1'],'A3':raws['A3'],'B3':raws['B3']}
 linear={
  'DH':fm(ui,fv(64,2)),
  'B0':fm(ui,bar(fv(19,2))),
  'A2':fm(fm(fc(1),ui),fv(54,2)),
  'B2':fm(ui,bar(fv(23,2))),
  'A4':fv(237),'B4':bar(fv(239)),
  'C1':fm(fm(fc(1),ui),fv(114))}
 n4=fm(ui,fv(116));alphas=[1,1,1,0,-1]
 for det in(0,1):
  assign=sol['assignments'][str(det)];direction=(1,det)
  for k in range(5):
   out=fm(fm(fc(alphas[k]),fu((1,2*det))),fv(118+16*det+2*k))
   z=fa(one,fs(out,-1))
   if k==4:z=fa(z,fm(fu((4,4*det)),fm(n4,n4)))
   for name,slot in assign['quadratic'].items():
    if slot//2==k:
     power=1+2*(slot%2);z=fa(z,fm(fu((power,power*det)),fm(quad[name],quad[name])))
   for name,slot in assign['linear'].items():
    kk=slot if slot<4 else 4
    if kk==k:
     power=2 if slot<4 else slot-3;z=fa(z,fm(fu((power,power*det)),linear[name]))
   fld(f'new.det{det}.factor{k}',z)
 # Bind unchanged rows exactly and check every literal/selected support.
 expanded=[];laurent=[]
 weights={int(k):tuple(v)for k,v in sol['weights'].items()}
 representations={0:{(0,0):()},1:{(0,0):()},2:{(0,0):()}}
 for budget in(1,2):
  for k in range(budget+1):
   for ids in itertools.combinations_with_replacement(sorted(base),k):
    e=tuple(sum(base[i][j]for i in ids)for j in(0,1))
    if e not in representations[budget]or(len(ids),ids)<(len(representations[budget][e]),representations[budget][e]):representations[budget][e]=ids
 for row in model['rows']:
  name=row['name'];ps=groups.get(name,[old[name]]if name in old else None)
  assert ps is not None,name
  expected={(tuple(m),tuple(e))for m,e in row['terms']}
  if name.startswith('new.det'):
   det=int(name[7]);k=int(name[-1])
   for label,slot in sol['assignments'][str(det)]['quadratic'].items():
    if slot//2==k:
     i,e,p0=model['quadratic_tests'][label];power=p0+2*(slot%2);ee=(e[0]+power,e[1]+det*power)
     expected.update(((i+a,i+b),ee)for a,b in[(0,0),(0,1),(1,1)])
   for label,slot in sol['assignments'][str(det)]['linear'].items():
    if(slot if slot<4 else 4)==k:
     i,e=model['linear_tests'][label];power=2 if slot<4 else slot-3;ee=(e[0]+power,e[1]+det*power)
     expected.update(((i+a,),ee)for a in(0,1))
  assert support(ps)==expected,(name,support(ps)-expected,expected-support(ps))
  if name in reference_names:ps=[original_rows[name]]
  rr=tuple(sol['row_weights'][name])
  for comp,p in enumerate(ps):
   named=name if len(ps)==1 else name+'.'+str(comp)
   laurent.append({'name':named,'group':name,'terms':serial_laurent(p),'rowUnitDivision':list(rr)})
   out=defaultdict(Q)
   for(a,m,e),c in p.items():
    assert len(m)<=2 and set(m)<=active
    ex=tuple(e[j]+sum(weights[i][j]for i in m)-rr[j]for j in(0,1))
    ids=representations[2-len(m)].get(ex)
    assert ids is not None,(named,m,ex)
    out[(a,tuple(sorted(m+ids)))]+=c
   expanded.append((named,clean(out)))
 # Literal unit guards, all needed before inverting the transformation.
 guards=[('unit.u',{(0,()):1,(0,(77,78)):-1}),
 ('unit.v',{(0,()):1,(0,(90,91)):-1}),
 ('unit.old_square',{(0,(77,92)):1,(0,(91,91)):-1}),
 ('unit.v_inv_cube',{(0,(90,901)):1,(0,(91,91)):-1}),
 ('unit.u_over_v',{(0,(902,)):1,(0,(77,91)):-1}),
 ('unit.inv_uv',{(0,(903,)):1,(0,(78,91)):-1})]
 expanded+=guards
 allids=sorted(active|set(base));assert len(allids)==194;renumber={i:j+1 for j,i in enumerate(allids)};assert renumber[1]==1
 normalized=[];normalizations=[]
 for name,p in expanded:
  lo=min(a for a,m in p);p={(a-lo,m):Q(c)for(a,m),c in p.items()}
  lcm=math.lcm(*(c.denominator for c in p.values()));gcd=math.gcd(*(abs(int(c*lcm))for c in p.values()));mult=Q(lcm,gcd)
  terms=[{'parameterPower':a,'monomial':[renumber[i]for i in m],'coefficient':str(int(c*mult))}for(a,m),c in sorted(p.items())]
  normalized.append({'id':len(normalized)+1,'name':name,'terms':terms});normalizations.append({'name':name,'C_shift':-lo,'rational_multiplier':str(mult)})
 assert max(len(t['monomial'])for r in normalized for t in r['terms'])==2
 poly=defaultdict(int)
 for row in normalized:
  ts=row['terms']
  for t in ts:
   for s in ts:
    key=t['parameterPower']+s['parameterPower'],tuple(sorted(t['monomial']+s['monomial']))
    poly[key]+=int(t['coefficient'])*int(s['coefficient'])
 poly={k:c for k,c in poly.items()if c}
 assert poly.get((0,(1,1,1,1)))==1
 coeffs=defaultdict(dict)
 for(a,m),c in poly.items():coeffs[m][a]=c
 heights=[];signstable=True;roots=[]
 for m,cs in coeffs.items():
  if len({1 if c>0 else-1 for c in cs.values()})>1:signstable=False;roots.append({'monomial':list(m),'coefficients':cs})
 report={'status':'PASS','variables':194,'quadratic_rows':len(normalized),'coordinate_degree':4,'content':1,'input_coordinate':1,'parameter':'C=149^N,N>=1; sufficient definingN remains ineffective','parameter_separated_quartic_terms':len(poly),'generic_coordinate_monomials':len(coeffs),'coefficient_sign_stable_in_positive_C':signstable,'mixed_sign_coefficient_polynomials':len(roots),'maximum_parameter_degree':max(a for a,m in poly),'source_sha256':sha256(SOURCE.read_bytes()).hexdigest(),'model_sha256':sha256(MODEL.read_bytes()).hexdigest(),'solution_sha256':sha256(SOL.read_bytes()).hexdigest(),'arithmetic_scope':'Retained source premises plus separately audited cleared comparison and implicit-ratio transfer. This producer verifies algebra, supports, degree and expansion, not the external arithmetic premises.'}
 table={'format':'cleared-comparison-quartic194/v71','variables':194,'inputCoordinate':1,'fixedParameter':{'symbol':'C','domain':'149^N,N>=1','quantified':False},'coordinates':[{'id':renumber[i],'source_id':i}for i in allids],'residuals':normalized}
 report['reference_basis']='original v45 primitive basis'if restore else 'reversed v69 reference basis'
 report['original_source_sha256']=sha256(original_path.read_bytes()).hexdigest()
 outdir=HERE/('primitive'if restore else 'fewer_monomials');outdir.mkdir(exist_ok=True)
 for filename,data in [('quadratic-family.json',table),('polynomial-family.json',{'variables':194,'terms':[{'parameterPower':a,'monomial':list(m),'coefficient':str(c)}for(a,m),c in sorted(poly.items())]}),('laurent-source.json',{'rows':laurent}),('transformation.json',{'base_units':model['base_units'],'weights':sol['weights'],'row_weights':sol['row_weights'],'old_to_new':renumber,'normalizations':normalizations,'literal_guards':[name for name,p in guards],'factor_assignments':sol['assignments']}),('construction-report.json',report),('mixed-coefficients.json',roots)]:
  (outdir/filename).write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 build(True)
 build(False)
