from math import gcd
from sympy import primerange
for m in [1,2,3]:
 for l in list(primerange(3,83)):
  s={i*i%l for i in range(l)}
  bad=[]
  for d in range(1,l):
   if d in s:continue
   for k in range(1,l):
    line=[d*((d+x*x)**2*(k*pow(x,m,l))**4-(d-x*x)**2*(1-d)**2)%l for x in range(l)]
    if all(e not in s for e in line):bad.append((d,k))
  if bad:print(m,l,bad[:24],flush=True)
