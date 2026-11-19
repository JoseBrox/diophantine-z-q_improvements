"""Check retained scalar equations and recover both hybrid aggregate components."""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import sys

root=(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[2]/'source')/'computation/quartic'
v74=root/'seven_units193_v74'
common=(v74/'source/source195.json').read_bytes()
assert common==(root/'explicit229_v62/source/quadratic195.json').read_bytes()
common_by_name={r['name']:r for r in json.loads(common)['residuals']}
explicit={r['name']:r for r in json.loads((root/'explicit229_v62/quadratic.json').read_text())['residuals']}
hybrid={r['name']:r for r in json.loads((v74/'primitive/laurent-source.json').read_text())['rows']}
units={77:(1,0),78:(-1,0),90:(0,1),91:(0,-1),92:(-1,-2)}
def lift(r):
 p=defaultdict(Fraction)
 for t in r['terms']:
  m=t['monomial'];u=tuple(sum(units[i][j] for i in m if i in units) for j in (0,1));z=tuple(i for i in m if i not in units)
  p[t['parameterPower'],z,u]+=Fraction(t['coefficient'])
 return {k:v for k,v in p.items() if v}
def physical(r):return {(t['parameterPower'],tuple(t['monomial']),tuple(t['unitPower'])):Fraction(t['coefficient']) for t in r['terms']}
prefixes=('inputSquare.','testSquare.40.','scalar.','parity_scalar.','sharedT.reference.','inverse_vieta.')
checked=[]
for n,r in hybrid.items():
 if n.startswith(prefixes):
  assert lift(explicit[n])==lift(common_by_name[n])==physical(r),n
  checked.append(n)
assert [n for n in common_by_name if n.startswith('inverse_vieta.') and n not in checked]==['inverse_vieta.alternate.0','inverse_vieta.alternate.1','inverse_vieta.unweighted.aggregate']
# New unscaled elliptic field quantities have component keys (monomial,c power), rho^2=2.
old=physical(hybrid['new.aggregate']);a=defaultdict(int);b=defaultdict(int)
a[(192,),0]=1;b[(193,),0]=1
for i in (201,213,225):
 for v in (i,i+2,i+8):
  for h,delta,co,target in ((0,0,1,a),(1,1,2,a),(1,0,1,b),(0,1,1,b)):
   target[tuple(sorted((i+8+h,v+delta))),1]+=co
source_expected={(0,m,(e,0)):v for (m,e),v in a.items()};source_expected.update({(0,(),(1,0)):14,(0,(2,),(0,0)):2,(0,(86,),(0,0)):-2});assert source_expected==old
print(f'Common scalar source {sha256(common).hexdigest()}. {len(checked)} matching scalar/reference/inverse-Vieta rows.')
print(f'Aggregate Re and Im terms: {len(a)}, {len(b)}. Re checked against complete v74 row.')
if '--json' in sys.argv: print(json.dumps({'rows':checked,'A_im':[[c,m,e] for (m,e),c in sorted(b.items())]}))
