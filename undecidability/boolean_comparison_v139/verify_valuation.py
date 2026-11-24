# Independent integer valuation fixture; quantified proof is in README.
count=0
for mu in range(1,20,2):
 for k in (1,5,7):
  for a in range(-80,81,2):
   t=a-min(a,k*mu)
   assert t>=0 and (t>0)==(a>k*mu)
   count+=1
harm=0
for x in range(31):
 for y in range(31):
  if x>0 and y>0:continue
  for tr in range(min(x,y),min(x,y)+9):
   if x!=y and tr!=min(x,y):continue
   assert (x+y-tr>0)==(max(x,y)>0)
   harm+=1
print(count,harm)
