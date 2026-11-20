"""Read-only independent source reconstruction and exact expansion for v82.

Reads literal published v78 tables, never imports either v82 producer, and
rebuilds the new point/scalar equations directly over Q(theta)/(theta^2-2).
"""
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from math import gcd
from pathlib import Path
from argparse import ArgumentParser
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=None
MANUSCRIPT=None
C,c,R,theta=s.symbols('C c R theta',nonzero=True)
xx={i:s.Symbol(f'v{i}') for i in range(1,612)}
rev={v:i for i,v in xx.items()}
PRIMES=(23,149,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793)
ANCHOR=reduce(lambda x,y:x*y,PRIMES,1)
BOOST_PRIMES=(263,2161,2437,2837,3793)
BOOST=reduce(lambda x,y:x*y,BOOST_PRIMES,1)
NORMALIZER=ANCHOR*BOOST**4
INDEX_BOUND=ANCHOR**3*BOOST**9

def field(expr):
 p=s.Poly(s.expand(expr),theta)
 return s.rem(p,s.Poly(theta**2-2,theta)).as_expr().expand()

def conjugate(expr):return expr.xreplace({theta:-theta})
def pair(i,imag=1):return xx[i]+imag*theta*xx[i+1]
def components(expr):
 e=field(expr);return e.coeff(theta,0),e.coeff(theta,1)

def canon(expr,keep_R=False):
 out=defaultdict(Fraction)
 for t in s.Add.make_args(s.expand(expr)):
  a,p=t.as_coeff_Mul();ex=p.as_powers_dict()
  k,e,r=(int(ex.pop(z,0)) for z in (C,c,R))
  mon=[]
  for v,n in ex.items():
   if v==1:continue
   assert v in rev and n>=0,(v,n)
   mon.extend([rev[v]]*int(n))
  out[k,e,r,tuple(sorted(mon))]+=Fraction(a)
 out={m:a for m,a in out.items() if a}
 assert out
 lower=tuple(min(m[i] for m in out) for i in range(3))
 if keep_R:lower=(lower[0],lower[1],0)
 out={(k-lower[0],e-lower[1],r-lower[2],mon):a for (k,e,r,mon),a in out.items()}
 scale=out[min(out)]
 return {m:a/scale for m,a in out.items()}

def expected(variant):
 folder=ROOT/f'computation/coauthor_audit_v78/work_general/enhanced/{variant}'
 q=json.loads((folder/'quadrics.json').read_text());w=json.loads((folder/'weights.json').read_text())
 labels={v['id']:v['source_id'] for v in q['coordinates']}
 cw={int(i):v for i,v in w['weights'].items()}
 deleted=('inverse_vieta.','cleared.E2.0','cleared.E2.1','scalar.W2.',
  'scalar.b.','scalar.p2.','scalar.firstConic','scalar.Bh.',
  'scalar.q2.','scalar.secondConic','parity_scalar.',
  'scalar.ratio1_unscaled_square.','scalar.r_power_2.',
  'shared.c_unit','shared.c_inverse_square')
 replace={xx[112]:c*R**2/C,xx[113]:c*R/C,
          xx[192]:c*xx[192]/R,xx[193]:c*xx[193]/R}
 # Old (X,Y)=(A+cB,A-cB); new (X,Y)=(A+c^3B,A-c^3B).
 change={}
 for i,j in ((68,66),(69,67)):
  change[xx[i]]=(xx[i]+xx[j]+(xx[i]-xx[j])/c**2)/2
  change[xx[j]]=(xx[i]+xx[j]-(xx[i]-xx[j])/c**2)/2
 out={}
 for row in q['residuals']:
  name=row['name']
  if name.startswith(deleted):continue
  expr=0
  for t in row['terms']:
   term=s.Integer(t['coefficient'])*C**t['parameterPower']
   for j in t['monomial']:
    i=labels[j]
    if i in (400,401,402):term*=c**{400:1,401:-1,402:-2}[i]
    else:term*=xx[i]*c**(-cw[i])
   expr+=term
  expr=expr.xreplace(replace)
  if variant==165 and name=='new.aggregate':
   expr=expr.subs(xx[192],R*xx[192])
  if not name.startswith('new.det0.factor2.'):
   expr=expr.xreplace(change)
  out[name]=s.expand(expr)

 f2=pair(64,2)/c;S=pair(17)/c;TH=pair(150)/c
 A=C*pair(33)/c;FU=C*pair(54,2)/c;FV=pair(23,2)/c
 Z=pair(102);J=pair(109);L=J-f2;D=11-6*theta
 U,V,W,rr,P,rr2=(pair(i) for i in (182,184,186,190,192,194))
 M=-2*S-W
 fresh={
  'v82.point.product':U*V-L*P,
  'v82.point.r':P*W-R*rr,
  'v82.point.sum':rr*(U+V-W-4*S)+D*R*L,
  'v82.point.pair':L*P+W*(U+V)-M**2,
  'v82.point.r2':rr2-rr**2,
  'v82.point.fusquare':FU*rr2-U**2,
  'v82.point.fvsquare':FV*rr2-V**2,
  'v82.point.primary':A*(U+M)-2*S*Z,
  'v82.comparison.E2':pair(35)/c-A*conjugate(V+M)-2*conjugate(TH)*conjugate(Z),
  'v82.scalar.field':R*L-Z**2,
 }
 for name,expr in fresh.items():
  for i,e in enumerate(components(expr)):out[f'{name}.{i}']=e
 out['v82.scalar.partial_trace']=field(xx[111]*(L+conjugate(L))-J*conjugate(J))
 sig,B,E,U1,V1,P1,Q1,P2,Q2=(xx[i] for i in (104,105,11,12,107,13,14,106,108))
 out.update({
  'v82.scalar.inverse':xx[111]*sig-R**4,
  'v82.scalar.input':B*sig-R**2-9792*R,
  'v82.scalar.p2':sig*P2-P1**2,
  'v82.scalar.q2':sig*Q2-Q1**2,
  'v82.scalar.first':3*E**2-34*E*sig-289*sig**2+17*B*P2,
  'v82.scalar.middle':E*(17*sig-B)-17*U1*V1,
  'v82.scalar.second':U1**2+34*U1*V1-867*V1**2-17*B*Q2,
 })
 out['scalar.forced_prime.definition']=1+22201*R*xx[101]/(C*c)-149*C*xx[101]/c
 if variant==180:
  out={n:s.expand(e.subs(C,1)) for n,e in out.items()}
  out['scalar.forced_prime.definition']=1+25*R*xx[101]/c-NORMALIZER*xx[101]/c
 return out

def check(variant):
 count=163 if variant==165 else 179
 folder=HERE/f'quartic{count}'
 q=json.loads((folder/'quadrics.json').read_text())
 maps=json.loads((folder/'maps.json').read_text())
 pol=json.loads((folder/'polynomial.json').read_text())
 cert=json.loads((folder/'certificate.json').read_text())
 labels={v:int(k) for k,v in maps['source_labels'].items()}
 cws={int(k):v for k,v in maps['c_weights'].items()}
 rws={int(k):v for k,v in maps['R_weights'].items()}
 kws={int(k):v for k,v in maps['parameter_weights'].items()}
 assert labels[1]==1 and cws[1]==rws[1]==kws[1]==0
 assert len(labels)==count and set(labels)==set(range(1,count+1))
 assert not {188,189}.intersection(labels.values())
 want=expected(variant)
 physical=json.loads((HERE/f'source{count}.json').read_text())
 assert len(physical['rows'])==len(want)
 assert {r['name'] for r in physical['rows']}==set(want)
 for row in physical['rows']:
  e=sum(Fraction(t['coefficient'])*C**t['parameter_power']*c**t['c_power']*R**t['R_power']
        *s.prod(R**2 if i==112 else xx[i] for i in t['monomial']) for t in row['terms'])
  assert canon(e)==canon(want[row['name']]),row['name']
 unit_value={400:c,401:1/c,402:1/c**2,112:R**2,113:R,114:1/R}
 unit_rows={
  'unit.c_inverse':{(400,401):1,():-1},
  'unit.c_inverse_square':{(402,):1,(401,401):-1},
  'unit.R_square':{(112,):1,(113,113):-1},
 }
 if variant==180:unit_rows['unit.R_inverse']={(113,114):1,():-1}
 else:
  # The R=0 fiber is ruled out before an inverse Laurent map is used.
  assert all(rws[i]==0 for i in (1,45,100)) and rws[101]==-1
  assert all(kws[i]==0 for i in (1,45,100)) and kws[101]==1
  assert maps['row_c_R_weights']['inputSquare.definition'][1]==0
  assert maps['row_c_R_weights']['scalar.rPair1.definition'][1]==0
  assert maps['row_c_R_weights']['scalar.four_contact_product.definition'][1]==0
  assert maps['row_c_R_weights']['scalar.forced_prime.definition'][1]==-1
 got_names=set();used=set();expanded=defaultdict(int)
 ys=s.symbols(f'y1:{count+1}');yindex={y:i+1 for i,y in enumerate(ys)}
 for row in q['residuals']:
  name=row['name'];assert name not in got_names;got_names.add(name)
  ordinary=0;back=0
  for t in row['terms']:
   assert len(t['monomial'])<=2
   used.update(t['monomial'])
   ordinary+=int(t['coefficient'])*C**t['parameterPower']*s.prod(ys[i-1] for i in t['monomial'])
   x=s.Integer(t['coefficient'])*C**t['parameterPower']
   for j in t['monomial']:
    i=labels[j]
    if i in unit_value:x*=unit_value[i]
    else:x*=xx[i]*c**(-cws[i])*R**(-rws[i])*(C**(-kws[i]) if variant==165 else 1)
   back+=x
  if name in unit_rows:
   literal={tuple(sorted(labels[i] for i in t['monomial'])):int(t['coefficient']) for t in row['terms']}
   assert all(t['parameterPower']==0 for t in row['terms'])
   assert literal==unit_rows[name]
  else:
   actual=canon(back);target=canon(want[name])
   if actual!=target:
    print('MISMATCH',variant,name)
    print('actual-only',list((actual.items()-target.items()))[:5])
    print('target-only',list((target.items()-actual.items()))[:5])
    raise AssertionError(name)
   if variant==165 and name in ('inputSquare.definition','scalar.rPair1.definition',
                                'scalar.four_contact_product.definition','scalar.forced_prime.definition'):
    # Unlike the ordinary Laurent comparison, preserve every R power here.
    # This checks the actual R=0 fibers of the four input rows.
    substitute={xx[101]:C*c*xx[611]/R}
    target_guard=want[name]*(R if name=='scalar.forced_prime.definition' else 1)
    assert canon(back.subs(substitute),keep_R=True)==canon(target_guard.subs(substitute),keep_R=True),name
  # Independent expansion uses SymPy's multiplication and collection.
  for term in s.Add.make_args(s.expand(ordinary**2)):
   a,p=term.as_coeff_Mul();powers=p.as_powers_dict();k=int(powers.pop(C,0));mon=[]
   for v,n in powers.items():
    if v==1:continue
    assert v in yindex and n>=0
    mon.extend([yindex[v]]*int(n))
   expanded[k,tuple(sorted(mon))]+=int(a)
 expanded={k:v for k,v in expanded.items() if v}
 stored={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in pol['terms']}
 assert expanded==stored
 assert got_names==set(want)|set(unit_rows)
 assert used==set(range(1,count+1))
 assert gcd(*expanded.values())==1 and max(len(m) for k,m in expanded)==4
 support={m for k,m in expanded}
 assert cert['variables']==count and cert['quadrics']==len(q['residuals'])
 assert cert['monomials']==len(support) and cert['parameter_separated_terms']==len(expanded)
 if variant==165:
  varying={(k,m):a for (k,m),a in expanded.items() if k}
  assert sorted((k,a) for (k,m),a in varying.items())==[(2,-6615898),(2,-298),(4,22201)]
  assert 22201*149**2>6615898
  assert max(abs(a) for (k,m),a in expanded.items() if k==0)==126616122944180358034867798936
  assert len(support)==len(expanded)
  height='max(126616122944180358034867798936,149^(4*N+2)) for N>=1'
 else:
  assert max(map(abs,expanded.values()))==NORMALIZER**2==cert['height']
  assert cert['height_bits']==748
  assert cert['anchor']['scalar_index_lower_bound']==INDEX_BOUND
  height=str(cert['height'])
 return {'variables':count,'quadrics':len(q['residuals']),'monomials':len(support),
         'parameter_separated_terms':len(expanded),'degree':4,'content':1,
         'independently_reconstructed_physical_rows':len(want),'height':height,
         'files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.json')}}

def endpoint():
 assert BOOST==14904184670611231 and ANCHOR%BOOST==0
 assert set(BOOST_PRIMES)<=set(PRIMES)
 derived_normalizer=1;derived_index=1
 for p in PRIMES:
  mu=5 if p in BOOST_PRIMES else 1
  derived_normalizer*=p**mu
  derived_index*=p**(9*mu//4+1)
 assert derived_normalizer==NORMALIZER and derived_index==INDEX_BOUND
 assert INDEX_BOUND>=2**960 and INDEX_BOUND>2**239
 assert NORMALIZER**2==(ANCHOR*BOOST**4)**2
 assert (NORMALIZER**2).bit_length()==748
 assert Fraction(2**20*2723,3003)>307000
 # (1/3-5/36036) exceeds the logarithmic derivative at s=0.
 assert Fraction(1,3)-Fraction(5,36036)>Fraction(5,324)
 assert Fraction(121*3*5*10001,2*2*10000)<500
 # Four binomial terms already prove 14^(1/36036)<10001/10000.
 assert 1+Fraction(36036,10000)+Fraction(36036*36035,2*10000**2)+Fraction(36036*36035*36034,6*10000**3)>14
 for p in PRIMES:
  assert s.isprime(p)
  for x in range(p):
   beta=(51*x*x+2504)%p
   r=beta*(beta-1)*(beta-2401)*(32*beta+343)%p
   assert r*(1+25*r)%p
 assert Fraction(24482500,100**4)<17
 assert 1*2*2402*375==1801500 and 149**3>149**2+1
 return {'anchor':ANCHOR,'boost':BOOST,'normalizer_numerator':NORMALIZER,
         'scalar_index_lower_bound':INDEX_BOUND,'scalar_index_ge_2_power960':True,
         'all_input_anchor_residue_checks':sum(PRIMES),'effective_endpoint':True,
         'uniform_real_R_over_100':True,'normalizer_height_constant':1801500}

def coordinate_identities():
 # These are universal rational identities, separately from the compiled
 # coefficient comparison above. No point is chosen by sampling.
 z=s.Symbol('z',nonzero=True)
 u,v,w,m,rr,p,rr2,fu,fv,A,D=s.symbols('u v w m rr p rr2 fu fv A D')
 S=-z*(m+w)/2
 U,V,W,MM,rrn,P,rr2n=z*u,z*v,z*w,z*m,z*rr,R*p,z*z*rr2
 L=z*z/R
 old=[u*v-p,p*w-rr,rr*(u+v+w+2*m)+D,
      p+w*(u+v)-m*m,rr2-rr*rr,fu*rr2-u*u,
      fv*rr2-v*v,A*(u+m)-2*S]
 new=[U*V-L*P,P*W-R*rrn,rrn*(U+V-W-4*S)+D*R*L,
      L*P+W*(U+V)-MM*MM,rr2n-rrn*rrn,
      fu*rr2n-U*U,fv*rr2n-V*V,A*(U+MM)-2*S*z]
 mult=[z*z,R*z,z*z,z*z,z*z,z*z,z*z,z]
 assert all(s.expand(n-k*o)==0 for n,k,o in zip(new,mult,old))
 assert s.expand(MM+2*S+W)==0
 # Exact sign in the changed comparison: t2=-(V0+M0).
 bz,bt,bth,aa=s.symbols('bz bt bth aa',nonzero=True)
 dv=-bz*bt
 assert s.expand(aa*dv+2*bth*bz-dv*(aa-2*bth/bt))==0
 # The weighted label error does not assume A integral first.
 hh,mm,nn,AA,CC=s.symbols('hh mm nn AA CC')
 assert s.expand((hh*AA-mm)-((hh-1)*(AA-CC)-nn)-(hh-1)*CC-(AA-(mm-nn)))==0
 # Native equations: a common sigma^2 factor, with only tau inverted.
 tau=s.Symbol('tau',nonzero=True)
 b,e,nu,nv,np,nq=s.symbols('b e nu nv np nq')
 sig=1/tau;BB=b/tau;EE=e/tau;UU=nu/tau;VV=nv/tau;PP=np/tau;QQ=nq/tau
 P2=np*np/tau;Q2=nq*nq/tau
 oldn=[3*e*e-34*e-289+17*b*np*np,
       e*(17-b)-17*nu*nv,nu*nu+34*nu*nv-867*nv*nv-17*b*nq*nq]
 newn=[3*EE*EE-34*EE*sig-289*sig*sig+17*BB*P2,
       EE*(17*sig-BB)-17*UU*VV,UU*UU+34*UU*VV-867*VV*VV-17*BB*Q2]
 assert all(s.cancel(n-o/tau**2)==0 for n,o in zip(newn,oldn))
 assert s.cancel(sig*P2-PP*PP)==s.cancel(sig*Q2-QQ*QQ)==0
 # Fixed reference point, independently doubled on y^2=x^3-d^2*x.
 rt=s.sqrt(2);dd=3-rt;xr=1+rt;yr=2*rt
 slope=s.simplify((3*xr*xr-dd*dd)/(2*yr))
 xp=s.simplify(slope*slope-2*xr);yp=s.simplify(slope*(xr-xp)-yr)
 zp=s.radsimp(-xp/yp)
 assert s.simplify(zp-(232+86*rt)/357)==0
 assert s.simplify(zp*zp.xreplace({rt:-rt})-s.Rational(328,1071))==0
 assert set(s.factorint(328))|set(s.factorint(1071))=={2,3,7,17,41}
 # The retained scalar input registers recover the stated r polynomial.
 input_x=s.Symbol('input_x');beta=51*input_x**2+2504;pair_register=(beta-3)**2/4
 contact=512*pair_register**2-15531948*input_x**2*pair_register-767410608*pair_register-291790992*input_x**2-14315517724
 assert s.expand(contact-beta*(beta-1)*(beta-2401)*(32*beta+343))==0
 # r=R*x101/c and 1+25*r-N*x101/c=0 give R=N*r/(1+25*r).
 scalar_r,normalizer=s.symbols('scalar_r normalizer',nonzero=True)
 actual_R=normalizer*scalar_r/(1+25*scalar_r)
 assert s.cancel(1+25*scalar_r-normalizer*scalar_r/actual_R)==0
 return {'point_row_identities':8,'eliminated_M_identity':True,
         'new_comparison_sign':True,'weighted_label_identity':True,
         'native_residual_identities':3,'native_square_identities':2,
         'fixed_reference_norm':'328/1071','scalar_contact_polynomial':True,
         'fixed_normalizer_identity':True}

def report():
 arithmetic=json.loads((HERE/'arithmetic.json').read_text())
 proof=MANUSCRIPT if MANUSCRIPT is not None else ROOT/arithmetic['manuscript']
 proof_hash=hashlib.sha256(proof.read_bytes()).hexdigest()
 assert proof_hash==arithmetic['manuscript_sha256']
 assert arithmetic['scalar_bounds']=={'quotient':'9/4','reference':'7/4'}
 assert arithmetic['comparison_power']==11 and Fraction(11-Fraction(1,4),4)==Fraction(43,16)
 assert arithmetic['weighted_radical_power']==3 and arithmetic['integer_residual']=='a*Delta'
 assert Fraction(7,18)*5==Fraction(arithmetic['general_height_exponent'])<2
 assert arithmetic['synchronized_minimum_depth']==1
 assert 12*1-11==1 and 8*1-5==3
 assert arithmetic['fixed_index_lower_bound_power2']==960
 dependencies={}
 for variant in (165,180):
  for name in ('quadrics.json','weights.json'):
   p=ROOT/f'computation/coauthor_audit_v78/work_general/enhanced/{variant}/{name}'
   dependencies[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 weighted=ROOT/'papers/trace_heights/weighted_trace_20261114_v27.tex'
 dependencies[str(weighted.relative_to(ROOT))]=hashlib.sha256(weighted.read_bytes()).hexdigest()
 local={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        for name in ('README.md','build.py','check.py','source163.json','source179.json','arithmetic.json')}
 return {'checks':[check(165),check(180)],'coordinate_identities':coordinate_identities(),
         'effective':endpoint(),'published_dependencies_sha256':dependencies,
         'package_sha256':local,'manuscript_sha256':proof_hash,
         'arithmetic_scope':'Exact deductions verified; the global theorem retains the manuscript arithmetic interfaces.'}

if __name__=='__main__':
 parser=ArgumentParser(description=__doc__)
 parser.add_argument('--repository',type=Path)
 parser.add_argument('--manuscript',type=Path)
 parser.add_argument('--record',action='store_true',help='explicitly replace the receipt after an audited change')
 args=parser.parse_args()
 MANUSCRIPT=args.manuscript
 if args.repository:ROOT=args.repository.resolve()
 else:
  ROOT=next((p for p in HERE.parents if (p/'computation/coauthor_audit_v78/work_general/enhanced/165/quadrics.json').is_file()),None)
  if ROOT is None:parser.error('repository root not found; use --repository')
 result=report();path=HERE/'independent.json'
 if args.record:path.write_text(json.dumps(result,indent=2)+'\n')
 else:assert result==json.loads(path.read_text()),'independent receipt mismatch'
 for item in result['checks']:
  print(f"Verified {item['variables']} variables, {item['quadrics']} quadrics, {item['monomials']} monomials; degree 4, content 1.")
 print('Complete physical maps, universal identities, independent expansions and arithmetic inequalities verified.')
