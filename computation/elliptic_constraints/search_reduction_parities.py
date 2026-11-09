import json
from math import isqrt
from pathlib import Path

def primes(n):
 a=bytearray(b'\1')*(n+1);a[:2]=b'\0\0'
 for i in range(2,isqrt(n)+1):
  if a[i]:a[i*i:n+1:i]=b'\0'*((n-i*i)//i+1)
 return [i for i in range(n+1) if a[i]]

def add(P,Q,D,p):
 if P is None:return Q
 if Q is None:return P
 x,y=P;u,v=Q
 if x==u:
  if (y+v)%p==0:return None
  k=(3*x*x-D)*pow(2*y,-1,p)%p
 else:k=(v-y)*pow(u-x,-1,p)%p
 a=(k*k-x-u)%p
 return a,(k*(x-a)-y)%p

def mul(n,P,D,p):
 Q=None
 while n:
  if n&1:Q=add(Q,P,D,p)
  P=add(P,P,D,p);n>>=1
 return Q

def order(P,D,p,N):
 n=N;q=2
 while q*q<=N:
  if N%q==0:
   while N%q==0:N//=q
   while n%q==0 and mul(n//q,P,D,p) is None:n//=q
  q+=1
 if N>1:
  while n%N==0 and mul(n//N,P,D,p) is None:n//=N
 return n

rows=[]
for p in primes(3000):
 if p in (2,7):continue
 s=next((u for u in range(p) if u*u%p==2),None)
 if s is None:continue
 orders=[]
 for r in (s,p-s):
  D=(11-6*r)%p
  P=((57-28*r)*pow(8,-1,p)%p,(-660+417*r)*pow(32,-1,p)%p)
  assert (P[1]**2-P[0]**3+D*P[0])%p==0
  N=1+sum(1 if (t:=(x*x*x-D*x)%p)==0 else 2 if pow(t,(p-1)//2,p)==1 else 0 for x in range(p))
  orders.append(order(P,D,p,N))
 rows.append({'p':p,'orders':orders,'both_odd':all(n%2 for n in orders)})
examples=[]
for p in (23,113):
 s=next(u for u in range(p) if u*u%p==2)
 for r in (s,p-s):
  D=(11-6*r)%p
  P=((57-28*r)*pow(8,-1,p)%p,(-660+417*r)*pow(32,-1,p)%p)
  n=3 if p==23 else 25
  prime_factor=3 if p==23 else 5
  assert mul(n,P,D,p) is None
  lower=mul(n//prime_factor,P,D,p)
  assert lower is not None
  examples.append({'p':p,'sqrt2':r,'D':D,'P':P,'order':n,
                   'order_multiple':None,'proper_divisor':n//prime_factor,
                   'proper_divisor_multiple':lower})
Path(__file__).with_name('reduction-parity-certificate.json').write_text(json.dumps({
 'status':'passed','scope':'exact finite-field enumeration and explicit order witnesses',
 'rows':rows,'split_good_prime_count':len(rows),
 'both_odd_count':sum(r['both_odd'] for r in rows),'explicit_examples':examples},indent=2)+'\n')
print('split good primes:',len(rows),'both P orders odd:',sum(r['both_odd'] for r in rows))
print([r for r in rows if r['both_odd']][:15])
