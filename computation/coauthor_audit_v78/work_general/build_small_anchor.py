"""Specialize the enhanced180 table at an explicitly certified smaller anchor."""
from pathlib import Path
from collections import defaultdict,Counter
from math import gcd,prod,comb
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'H10-quartics/quartics/explicit';SOURCE=HERE/'enhanced/180/quadrics.json'
PRIMES=[23,149,263,631,1063,1171,1439,2161,2437,2851,3343]
A=prod(PRIMES);U=3593614808933267;V=14228611824350171
assert A==U*V and A**3>=2**316
q=json.loads(SOURCE.read_text());roles={x['source_id']:x['id'] for x in q['coordinates']};assert (roles[101],roles[113],roles[400])==(78,90,163)
oldsrc=json.loads((OLD/'source.json').read_text());d={r['name']:r for r in q['residuals']};q['residuals']=[d[r['name']] for r in oldsrc['residuals']]
gauge=json.loads((OLD/'parameter-map.json').read_text());weights=json.loads((OLD/'fixed-map.json').read_text())['weights'];assert len(weights)==180
rows=[]
for row in q['residuals']:
 special=row['name']=='scalar.forced_prime.definition';out=Counter();ts=[]
 if not special:assert len({t['parameterPower']+sum(gauge[i-1] for i in t['monomial']) for t in row['terms']})==1
 for t in row['terms']:
  m=tuple(t['monomial']);a=int(t['coefficient']);k=t['parameterPower']
  if special:
   assert (a,k,m) in [(1,0,(163,163)),(22201,0,(78,90)),(-149,1,(78,))]
   a=25 if m==(78,90) else -V if m==(78,) else 1;k=0
  ts.append((k+sum(weights[i-1] for i in m),m,a))
 lo=min(k for k,m,a in ts)
 for k,m,a in ts:out[m]+=a*U**(k-lo)
 g=gcd(*out.values());rows.append({m:a//g for m,a in out.items() if a})
def expand(rows):
 out=defaultdict(int)
 for row in rows:
  for m,a in row.items():
   for n,b in row.items():out[tuple(sorted(m+n))]+=a*b
 return {m:a for m,a in out.items() if a}
def render(p):
 s=[]
 for m,a in sorted(p.items()):
  parts=[str(abs(a))] if abs(a)!=1 or not m else []
  parts.extend('x'+str(i)+('^'+str(n) if n>1 else '') for i,n in sorted(Counter(m).items()))
  s.append(('-' if a<0 else '+' if s else '')+'*'.join(parts))
 return ''.join(s)
def save(path,data):path.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
operations=json.loads((OLD/'operations.json').read_text());oldperm={int(i):j for i,j in json.loads((OLD/'permutation.json').read_text()).items()};shears=json.loads((OLD/'shears.json').read_text());report=[]
for variant in ['plain','row_ops','old_shears']:
 result=[r.copy() for r in rows]
 if variant!='plain':
  for i,j,b,d in operations:
   out=Counter({m:d*a for m,a in result[i-1].items()});out.update({m:b*a for m,a in result[j-1].items()});out={m:a for m,a in out.items() if a};g=gcd(*out.values());result[i-1]={m:a//g for m,a in out.items()}
 if variant=='old_shears':perm=oldperm
 else:
  p=expand(result);freq=Counter(i for m in p for i in set(m));order=[1]+sorted((i for i in freq if i!=1),key=lambda i:(-freq[i],i));perm={i:j+1 for j,i in enumerate(order)}
 result=[{tuple(sorted(perm[i] for i in m)):a for m,a in r.items()} for r in result]
 if variant=='old_shears':
  for i,j,c in shears:
   tmp=[]
   for row in result:
    out=defaultdict(int)
    for m,a in row.items():
     n=m.count(i);rest=tuple(k for k in m if k!=i)
     for e in range(n+1):out[tuple(sorted(rest+(i,)*(n-e)+(j,)*e))]+=a*comb(n,e)*c**e
    tmp.append({m:a for m,a in out.items() if a})
   result=tmp
 p=expand(result);H=max(map(abs,p.values()));literal=render(p);out=HERE/'enhanced/180'/('anchor_'+variant);out.mkdir(exist_ok=True)
 def terms(p):return [{'monomial':list(m),'coefficient':str(a)} for m,a in sorted(p.items())]
 save(out/'quadrics.json',{'variables':180,'inputCoordinate':1,'residuals':[{'name':q['residuals'][j]['name'],'terms':terms(row)} for j,row in enumerate(result)]});save(out/'polynomial.json',{'variables':180,'inputCoordinate':1,'terms':terms(p)});(out/'quartic180.txt').write_text(literal)
 cert={'variant':variant,'physical_anchor':str(A),'primes':PRIMES,'U':str(U),'V':str(V),'variables':180,'quadrics':152,'degree':max(map(len,p)),'monomials':len(p),'height':str(H),'height_bits':H.bit_length(),'bytes':len(literal),'sha256':sha256(literal.encode()).hexdigest(),'source_sha256':sha256(SOURCE.read_bytes()).hexdigest()};save(out/'certificate.json',cert);save(out/'maps.json',{'parameter_weights':weights,'parameter_gauge':gauge,'row_order':[r['name'] for r in q['residuals']],'operations':operations if variant!='plain' else [],'permutation':perm,'shears':shears if variant=='old_shears' else []});report.append(cert)
print(json.dumps(report,indent=2))
