"""Verify the R-square exclusion without an optimizer or symbolic library.

Checks the finite unit-exponent model, rebinds every certificate inequality
to an actual nonzero term of the pinned physical source, and adds the
integer inequalities to a strict contradiction. No floating point is used.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from argparse import ArgumentParser
import hashlib,json

def check(source,certificate):
 data=json.loads(source.read_text());cert=json.loads(certificate.read_text())
 count=cert['count'];assert count in (163,179)
 units={(0,0),(1,0),(-1,0),(-2,0),(0,1)}
 if count==179:units.add((0,-1))
 kinds=[(0,-1),(1,1),(-1,2)] if count==163 else [(1,1),(1,-1),(-1,2),(-1,-2)]
 def bound(ac,ar,d):return (0 if (ac,ar)==(0,-1) else d if ac==1 else 2*d)
 for d in (0,1,2):
  sums={(0,0)}
  for _ in range(d):sums={(x+a,y+b) for x,y in sums for a,b in units}
  polygon={(x,y) for x in range(-4,3) for y in range(-2,3)
           if all(ac*x+ar*y<=bound(ac,ar,d) for ac,ar in kinds)}
  assert sums==polygon
 rows={r['name']:r['terms'] for r in data['rows']}
 assert len(rows)==len(data['rows'])
 totals=Counter();rhs=0
 for witness in cert['rows']:
  mult=witness['multiplier'];assert type(mult)==int and mult>0
  name=witness['row'];term=witness['term']
  assert term in rows[name] and Fraction(term['coefficient'])!=0
  rest=[];c=term['c_power'];r=term['R_power']
  for i in term['monomial']:
   if i in (112,113,114):r+={112:2,113:1,114:-1}[i]
   elif i in (400,401,402):c+={400:1,401:-1,402:-2}[i]
   else:rest.append(i)
  # The selected monomial is a distinct physical monomial, so no
  # cancellation has been hidden by treating it separately.
  key=(term['parameter_power'],term['c_power'],term['R_power'],tuple(term['monomial']))
  assert sum((t['parameter_power'],t['c_power'],t['R_power'],tuple(t['monomial']))==key for t in rows[name])==1
  ac,ar,d=witness['kind'];assert d==2-len(rest) and (ac,ar) in kinds
  coefficients=Counter()
  for i in rest:
   coefficients[str(('c',('var',i)))]+=ac
   coefficients[str(('R',('var',i)))]+=ar
  coefficients[str(('c',('row',name)))]-=ac
  coefficients[str(('R',('row',name)))]-=ar
  coefficients={k:v for k,v in coefficients.items() if v}
  assert coefficients==witness['coefficients']
  b=bound(ac,ar,d)-ac*c-ar*r
  assert b==witness['rhs']
  for k,v in coefficients.items():totals[k]+=mult*v
  rhs+=mult*b
 assert all(v==0 for v in totals.values())
 assert rhs==cert['contradiction_rhs'] and rhs<0
 return {'variables':count,'selected_inequalities':len(cert['rows']),
         'contradiction':f'0 <= {rhs}','verified':True,
         'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),
         'scope':cert['scope']}

if __name__=='__main__':
 p=ArgumentParser();p.add_argument('--source-root',type=Path,required=True)
 p.add_argument('--certificate-root',type=Path,default=Path(__file__).resolve().parent)
 p.add_argument('--report',type=Path)
 args=p.parse_args()
 results=[check(args.source_root/f'source{n}.json',args.certificate_root/f'two_unit_farkas_{n}.json') for n in (163,179)]
 if args.report:args.report.write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
