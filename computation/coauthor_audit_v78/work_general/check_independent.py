#!/usr/bin/env python3
"""Independent stdlib audit of the supplied shared-product quartics.
This checker imports no producer and regenerates no supplied output.
Arithmetic completeness is proved in shared_product_audit.tex, relative to its
explicitly listed source interfaces; this program certifies finite claims only.
"""
from collections import defaultdict,Counter
from fractions import Fraction as F
from hashlib import sha256
from math import comb,gcd,isqrt,prod
from pathlib import Path
import argparse,json,re

def take(path):return json.loads(path.read_text())
def add(*ps):
 out=defaultdict(int)
 for p in ps:
  for m,a in p.items():out[m]+=a
 return {m:a for m,a in out.items() if a}
def mult(p,q):
 out=defaultdict(int)
 for (k,m),a in p.items():
  for (l,n),b in q.items():out[k+l,tuple(sorted(m+n))]+=a*b
 return {m:a for m,a in out.items() if a}
def terms(row,n):
 out={}
 for t in row['terms']:
  k=t.get('parameterPower',0);m=tuple(t['monomial']);a=int(t['coefficient'])
  assert a and tuple(sorted(m))==m and all(1<=i<=n for i in m)
  assert (k,m) not in out
  out[k,m]=a
 return out
def expansion(folder):
 q=take(folder/'quadrics.json');p=take(folder/'polynomial.json');n=q['variables']
 assert n==p['variables'] and q.get('inputCoordinate',1)==p.get('inputCoordinate',1)==1
 rows=[terms(r,n) for r in q['residuals']]
 assert all(max(map(lambda z:len(z[1]),r))<=2 for r in rows)
 assert all(gcd(*r.values())==1 for r in rows)
 out=add(*(mult(r,r) for r in rows));want=terms(p,n)
 assert out==want
 grouped=defaultdict(dict)
 for (k,m),a in out.items():grouped[m][k]=a
 assert max(map(len,grouped))==4 and grouped[(1,)*4]=={0:1}
 assert {i for m in grouped for i in m}==set(range(1,n+1))
 return q,rows,out,grouped

def independent_balance(source,target,certificate):
 w=[0]+certificate['coordinate_weights'];assert w[1]==0
 assert len(source)==len(target)
 for a,b in zip(source,target):
  new={(k+sum(w[i] for i in m),m):c for (k,m),c in a.items()}
  lo=min(k for k,m in new);g=gcd(*new.values())
  assert {(k-lo,m):c//g for (k,m),c in new.items()}==b

def numeric_transform(source,folder):
 setup=take(folder/'fixed-map.json');gauge=take(folder/'parameter-map.json')
 A=prod([23,149,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793])
 U=int(setup['U']);V=A//U;assert U*V==A
 w=[0]+setup['weights'];gau=[0]+gauge
 assert w[1]==gau[1]==0
 out=[]
 for row in source['residuals']:
  raw=terms(row,source['variables']);special=row['name']=='scalar.forced_prime.definition'
  if special:
   assert raw=={(0,()):1,(0,(78,90)):22201,(1,(78,)):-149}
   raw={(0,()):1,(0,(78,90)):25,(0,(78,)):-V}
  else:assert len({k+sum(gau[i] for i in m) for k,m in raw})==1
  weighted={(k+sum(w[i] for i in m),m):c for (k,m),c in raw.items()}
  low=min(k for k,m in weighted)
  p={m:c*U**(k-low) for (k,m),c in weighted.items()}
  g=gcd(*p.values());out.append({m:c//g for m,c in p.items()})
 for i,j,b,d in take(folder/'operations.json'):
  assert i!=j and d>0
  a=add({m:d*c for m,c in out[i-1].items()},{m:b*c for m,c in out[j-1].items()})
  g=gcd(*a.values());out[i-1]={m:c//g for m,c in a.items()}
 mapping={int(i):j for i,j in take(folder/'permutation.json').items()}
 assert mapping[1]==1 and set(mapping)==set(mapping.values())==set(range(1,181))
 out=[{tuple(sorted(mapping[i] for i in m)):c for m,c in r.items()} for r in out]
 for i,j,c in take(folder/'shears.json'):
  assert i!=1 and i!=j and 2<=i<=180 and 0<=j<=180
  tmp=[]
  for row in out:
   p=defaultdict(int)
   for m,a in row.items():
    k=m.count(i);base=tuple(h for h in m if h!=i)
    for z in range(k+1):
     mon=tuple(sorted(base+(i,)*(k-z)+((j,)*z if j else ())))
     p[mon]+=a*comb(k,z)*c**z
   tmp.append({m:a for m,a in p.items() if a})
  out=tmp
 return out

def parse_literal(s):
 out={}
 assert s and s.isascii() and not any(c.isspace() for c in s)
 for match in re.finditer(r'([+-]?)([^+-]+)',s):
  sign,term=match.groups();a=-1 if sign=='-' else 1;mon=[]
  for f in term.split('*'):
   if f.startswith('x'):
    mm=re.fullmatch(r'x([1-9][0-9]*)(?:\^([1-9][0-9]*))?',f);assert mm
    mon.extend([int(mm[1])]*int(mm[2] or 1))
   else:assert f.isdigit();a*=int(f)
  m=tuple(sorted(mon));assert m not in out and a
  out[m]=a
 assert ''.join(m.group(0) for m in re.finditer(r'([+-]?)([^+-]+)',s))==s
 return out

def main(root):
 used=[]
 def checked(folder):
  used.extend([folder/'quadrics.json',folder/'polynomial.json'])
  return expansion(folder)
 gp,gr,gpol,gm=checked(root/'quartics/general-physical')
 bp,br,bpol,bm=checked(root/'quartics/general')
 ep,er,epol,em=checked(root/'quartics/explicit-physical')
 fp,fr,fpol,fm=checked(root/'quartics/explicit')
 assert (gp['variables'],len(gr),len(gm))==(165,139,2608)
 assert (ep['variables'],len(er),len(em))==(180,152,2856)
 assert (fp['variables'],len(fr),len(fm))==(180,152,2648)
 independent_balance(gr,br,take(root/'quartics/general/certificate.json'))
 K=126616122944180358034867798936
 profiles=[]
 for p in bm.values():
  assert max(p)<=2
  profiles.append(tuple(p.get(i,0) for i in range(3)))
 assert (K,0,0) in profiles or (-K,0,0) in profiles
 assert (0,0,22201) in profiles or (0,0,-22201) in profiles
 for N in range(1,6):
  C=149**N;v=[a+b*C+d*C*C for a,b,d in profiles]
  assert all(v) and max(map(abs,v))==max(K,22201*C*C)
 C=149**6
 for a,b,d in profiles:
  value=a+b*C+d*C*C;s=1 if value>0 else -1
  assert s*value>0 and s*(b+2*d*C)>=0 and s*d>=0
  for t in [-1,1]:
   assert 22201*C*C+t*value>=0
   assert 44402*C+t*(b+2*d*C)>=0
   assert 22201+t*d>=0
 folder=root/'quartics/explicit'
 assert (folder/'source.json').read_bytes()==(root/'quartics/explicit-physical/quadrics.json').read_bytes()
 native=numeric_transform(ep,folder)
 assert native==[{m:c for (k,m),c in r.items() if k==0} for r in fr]
 assert all(k==0 for r in fr for k,m in r)
 literal=(folder/'quartic180.txt').read_text()
 assert parse_literal(literal)=={m:c for (k,m),c in fpol.items()}
 assert len(literal)==54695 and sha256(literal.encode()).hexdigest()=='e6fd2cab3564dd0eb84c388aa252db1b6057f1135fbedfdf248416cd6585fd73'
 H=max(map(abs,fpol.values()));assert H==2584403986888404839167627077886434458396171597584
 primes=[23,149,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793]
 def r(x):b=51*x*x+2504;return b*(b-1)*(b-2401)*(32*b+343)
 for p in primes:
  assert all(p%d for d in range(2,isqrt(p)+1))
  assert all(r(x)%p and (1+25*r(x))%p for x in range(p))
 A=prod(primes);assert A>149**22 and A>26*2**20
 assert all(r(x)%16 in [4,8,12] for x in range(16))
 assert all(r(x)%3==1 for x in range(3))
 assert all(r(x)%17==13 for x in range(17))
 # Complete noncancellation certificate for every odd mu, reduced modulo eight.
 for mu in (1,3,5,7):
  sets=[{(-mu+4*t)%8 for t in range(8)}, {(-2*mu+4*t)%8 for t in range(8)}, {(-3*mu+4*t)%8 for t in range(8)}, {(-4*mu+8*t)%8 for t in range(8)}, {0}]
  assert all(not(sets[i]&sets[j]) for i in range(5) for j in range(i))
 # Reference nonexceptional norms: x(P), x(P)-d, x(P)+d, and d.
 norms=[F(41**2,64),F(17**2,64),F(63**2,64),F(7)]
 assert all(n.numerator%149 and n.denominator%149 for n in norms)
 used.extend([root/'quartics/general/certificate.json']+[folder/name for name in ['source.json','fixed-map.json','parameter-map.json','operations.json','permutation.json','shears.json','quartic180.txt']])
 report={'status':'passed','scope':'finite exact checks; arithmetic proof conditional on the enumerated inherited interfaces','general':{'variables':165,'quadrics':139,'degree':4,'monomials':2608,'height':'max(126616122944180358034867798936,149^(2N+2))','N_range':'all integers N >= 1; defining threshold remains ineffective'},'explicit':{'variables':180,'quadrics':152,'degree':4,'monomials':2648,'height':str(H),'bytes':len(literal),'sha256':sha256(literal.encode()).hexdigest()},'anchor':{'A':str(A),'primes':primes,'residue_fields_checked':len(primes),'residues_checked':sum(primes)},'factor_valuation_residue_classes':'complete modulo-eight check for all odd contact depths','inputs':{str(p.relative_to(root)):sha256(p.read_bytes()).hexdigest() for p in used}}
 return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--out',type=Path);a=p.parse_args();report=main(a.root);s=json.dumps(report,indent=2)+'\n'
 if a.out:a.out.write_text(s)
 print(s)
