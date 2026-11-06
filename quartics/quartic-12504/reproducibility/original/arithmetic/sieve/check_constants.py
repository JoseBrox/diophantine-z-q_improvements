if not __debug__:
    raise RuntimeError('Run without -O; assertions are part of validation.')

from fractions import Fraction as F
from math import prod,gcd
from pathlib import Path
import json
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
R=47027;W=25878772920;c=18484837801;V=32*W
small=[2,3,5,7,11,13,17,19,23,29]
D=[F(0),F(1),F(2401),F(-343,32)]
assert R==31*37*41 and W==4*prod(small) and V==828120733440
assert c%8==1 and gcd(c,W)==1
assert all(c%q==(3 if q==7 else 1) for q in small if q!=2)
diffs=sorted({x-y for x in D for y in D if x!=y and (x-y).denominator==1})
sums=sorted({x+y for x in D for y in D if (x+y).denominator==1})
assert diffs==list(map(F,[-2401,-2400,-1,1,2400,2401]))
assert all(int(x)%31!=0 for x in diffs)
assert all(int(x)%31!=3 for x in sums)
local=[]
for q in [31,37,41]:
 ds={int(t.numerator)*pow(t.denominator,-1,q)%q for t in D}
 ss=ds|{(3-x)%q for x in ds}
 outside=[x for x in range(q) if x not in ss];b,e=outside[:2]
 gamma=pow(V,-1,q)
 if (e-b)%q==(-gamma)%q:b,e=e,b
 v=pow((e-b)%q,-1,q);u=b*v%q
 vals=[gamma*v%q]+[(u-s*v)%q for s in ss]
 assert all(x not in [0,q-1] for x in vals)
 local.append({'q':q,'slope_residues':sorted(ss),'b':b,'e':e,'u':u,'v':v,'all_values_and_successors_nonzero':True})
data={'R':R,'W':W,'c':c,'V0':V,'W_prime_factors':small,'c_mod_8':c%8,'c_mod_odd_primes':{str(q):c%q for q in small if q!=2},'integral_contact_differences':[int(x) for x in diffs],'integral_contact_sums':[int(x) for x in sums],'sum_residues_mod31':[int(x)%31 for x in sums],'local_witnesses':local,'max_prime_positions':41,'max_GT_complexity':39}
if args.output:args.output.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
