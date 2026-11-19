"""Independent exact certification of the strengthened180 fixed member.
No builder or optimizer is imported. The inherited analytic inequalities and
this finite certificate are linked in the companion TeX proof.
"""
from pathlib import Path
from collections import defaultdict,Counter
from fractions import Fraction as F
from math import prod,gcd,lcm,comb,isqrt,factorial
from hashlib import sha256
import importlib.util,json
HERE=Path(__file__).resolve().parent;DIR=HERE/'enhanced/180';BASE=DIR/'anchor_plain';FINAL=DIR/'anchor_scaled'
s=importlib.util.spec_from_file_location('independent',HERE/'check_independent.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
q0=json.loads((DIR/'quadrics.json').read_text());params=json.loads((BASE/'maps.json').read_text());cert=json.loads((BASE/'certificate.json').read_text());A=int(cert['physical_anchor']);U=int(cert['U']);V=int(cert['V']);primes=cert['primes'];assert A==prod(primes)==U*V
assert A**3>=2**316 and A>26*2**20 and 149 in primes
S={2,3,5,7,11,13,17,37,41,2399}
def raw(x):b=51*x*x+2504;return b*(b-1)*(b-2401)*(32*b+343)
for p in primes:
 assert p not in S and all(p%d for d in range(2,isqrt(p)+1))
 assert all(raw(x)%p and (1+25*raw(x))%p for x in range(p))
assert all(raw(x)%16 in (4,8,12) for x in range(16))
assert all(raw(x)%3==1 for x in range(3)) and all(raw(x)%17==13 for x in range(17))
# All finite numerical comparisons needed for the new M^4 endpoint.
assert F(97,50)**4>14 and F(29,20)**2>F(21,10)
assert 1+F(48048,10000)+F(comb(48048,2),10000**2)>14
assert 121*F(97,50)*F(29,20)*F(10001,10000)<350
assert sum(F(7,10)**k/factorial(k) for k in range(5))>2
assert sum(F(4)**k/factorial(k) for k in range(4))>14
left=2**16*(1-F(316*7,10*12012));right=350*(53+F(158*7,10));assert left>right
assert F(12011,12012)>F(1,106)
assert F(23,22)*322*F(7,10)<240
assert 2**316>252 and 2**316-3>9 and F(2**238,A**3)<F(1,2)
# Recover the parameter specialization without using the producer.
by={r['name']:r for r in q0['residuals']};rows=[];cw=[0]+params['parameter_weights'];gauge=[0]+params['parameter_gauge'];assert cw[1]==gauge[1]==0
for name in params['row_order']:
 row=by[name];ts=a.terms(row,180);special=name=='scalar.forced_prime.definition'
 if special:
  assert ts=={(0,(163,163)):1,(0,(78,90)):22201,(1,(78,)):-149}
  ts={(0,(163,163)):1,(0,(78,90)):25,(0,(78,)):-V}
 else:assert len({k+sum(gauge[i] for i in m) for k,m in ts})==1
 scaled={(k+sum(cw[i] for i in m),m):v for (k,m),v in ts.items()};low=min(k for k,m in scaled)
 r={m:v*U**(k-low) for (k,m),v in scaled.items()};g=gcd(*r.values());rows.append({m:v//g for m,v in r.items()})
assert params['operations']==params['shears']==[]
perm={int(i):j for i,j in params['permutation'].items()};assert perm[1]==1 and set(perm)==set(perm.values())==set(range(1,181))
rows=[{tuple(sorted(perm[i] for i in m)):v for m,v in r.items()} for r in rows]
bq,br,bp,bm=a.expansion(BASE);assert rows==[{m:v for (k,m),v in r.items()} for r in br]
# Apply the separate positive integer diagonal, then primitively normalize.
scaleinfo=json.loads((FINAL/'scaling.json').read_text());sc={int(i):F(v) for i,v in scaleinfo['scaling'].items()};assert sc.get(1,F(1))==1 and all(sc.values())
for j,row in enumerate(rows):
 p={m:F(v)*prod(sc.get(i,1) for i in m) for m,v in row.items()};d=lcm(*(v.denominator for v in p.values()));g=gcd(*(int(v*d) for v in p.values()));rows[j]={m:int(v*d)//g for m,v in p.items()}
fq,fr,fp,fm=a.expansion(FINAL);assert rows==[{m:v for (k,m),v in r.items()} for r in fr]
H=max(map(abs,fp.values()));assert H==206625078319751697390503348692624 and H==16*U*U and len(fm)==2850
# Canonical literal constructed independently, then parsed by the separate parser.
parts=[]
for m,p in sorted(fm.items()):
 assert set(p)=={0};v=p[0];body=[]
 if abs(v)!=1 or not m:body.append(str(abs(v)))
 for i,k in sorted(Counter(m).items()):body.append('x'+str(i)+('^'+str(k) if k>1 else ''))
 parts.append(('-' if v<0 else '+' if parts else '')+'*'.join(body))
literal=''.join(parts);assert a.parse_literal(literal)=={m:p[0] for m,p in fm.items()}
assert (FINAL/'quartic180.txt').read_text()==literal
report={'status':'PASS','variables':180,'quadrics':152,'degree':4,'monomials':len(fm),'height':str(H),'height_bits':H.bit_length(),'canonical_bytes':len(literal),'canonical_sha256':sha256(literal.encode()).hexdigest(),'anchor':str(A),'primes':primes,'U':str(U),'V':str(V),'anchor_cube_at_least_2_power':316,'delta_endpoint_left_over_2_300':str(left),'delta_endpoint_right_over_2_300':str(right),'strengthened_divisibilities':['M_j^4 divides Delta','M_j^3 divides nonzero input numerator'],'arithmetic_scope':'Under the same effective source interfaces; sufficient fixed member certified by the strengthened endpoint proof','input_hashes':{str(p.relative_to(HERE)):sha256(p.read_bytes()).hexdigest() for p in [DIR/'quadrics.json',BASE/'maps.json',BASE/'certificate.json',FINAL/'scaling.json',FINAL/'quadrics.json',FINAL/'polynomial.json']}}
assert json.loads((FINAL/'certificate.json').read_text())==report;print(json.dumps(report,indent=2))
