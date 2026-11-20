"""Compile the pinned physical rows and supplied integer Laurent weights.

This producer uses only Python's standard library and no solver. The source
tables are the complete physical definitions. The independent checker derives
them again from the published v78 tables and the new field equations.

Use --output DIRECTORY to reproduce without modifying the published files.
"""
from argparse import ArgumentParser
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd,lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
PRIMES=(23,149,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793)
ANCHOR=reduce(lambda a,b:a*b,PRIMES,1)
BOOST_PRIMES=(263,2161,2437,2837,3793)
BOOST=reduce(lambda a,b:a*b,BOOST_PRIMES,1)
NORMALIZER=ANCHOR*BOOST**4
INDEX_BOUND=ANCHOR**3*BOOST**9

def serial(poly):
 return [{'parameterPower':k,'monomial':list(m),'coefficient':str(a)}
         for (k,m),a in sorted(poly.items())]

def build(count,destination):
 source=json.loads((HERE/f'source{count}.json').read_text())
 maps=json.loads((HERE/f'quartic{count}/maps.json').read_text())
 index={int(k):v for k,v in maps['source_labels'].items()}
 cw={int(k):v for k,v in maps['c_weights'].items()}
 rw={int(k):v for k,v in maps['R_weights'].items()}
 kw={int(k):v for k,v in maps['parameter_weights'].items()}
 rc=maps['row_c_R_weights'];rk=maps['row_parameter_weights']
 units=[(0,0,()),(1,0,(400,)),(-1,0,(401,)),(-2,0,(402,)),
        (0,1,(113,)),(0,2,(112,))]
 if count==179:units.append((0,-1,(114,)))
 for x,y in product(units[1:].copy(),repeat=2):
  z=(x[0]+y[0],x[1]+y[1],tuple(sorted(x[2]+y[2])))
  if z not in units:units.append(z)
 choose={}
 for a,b,m in sorted(units,key=lambda z:(len(z[2]),z[2])):
  choose.setdefault((a,b),m)
 rows=[]
 for row in source['rows']:
  name=row['name'];hc,hr=rc[name];poly=defaultdict(Fraction)
  for t in row['terms']:
   mon=t['monomial'];n2=mon.count(112);rest=tuple(i for i in mon if i!=112)
   e=t['c_power']+sum(cw[i] for i in rest)-hc
   r=t['R_power']+2*n2+sum(rw[i] for i in rest)-hr
   k=t['parameter_power']+sum(kw[i] for i in rest)-rk[name] if count==163 else 0
   m=tuple(sorted(rest+choose[e,r]))
   assert len(m)<=2 and k>=0
   poly[k,m]+=Fraction(t['coefficient'])
  poly={m:a for m,a in poly.items() if a}
  den=lcm(*(a.denominator for a in poly.values()))
  poly={m:int(a*den) for m,a in poly.items()}
  common=gcd(*poly.values());poly={m:a//common for m,a in poly.items()}
  rows.append((name,poly))
 rows.extend([
  ('unit.c_inverse',{(0,(400,401)):1,(0,()):-1}),
  ('unit.c_inverse_square',{(0,(402,)):1,(0,(401,401)):-1}),
  ('unit.R_square',{(0,(112,)):1,(0,(113,113)):-1}),
 ])
 if count==179:rows.append(('unit.R_inverse',{(0,(113,114)):1,(0,()):-1}))
 rows=[(n,{(k,tuple(index[i] for i in mon)):a for (k,mon),a in p.items()}) for n,p in rows]
 expanded=defaultdict(int)
 for _,p in rows:
  for ((k,m),a),((l,n),b) in product(p.items(),repeat=2):
   expanded[k+l,tuple(sorted(m+n))]+=a*b
 expanded={m:a for m,a in expanded.items() if a}
 assert len(index)==count and index[1]==1
 assert len(rows)=={163:137,179:151}[count]
 assert gcd(*expanded.values())==1 and max(len(m) for k,m in expanded)==4
 support={m for k,m in expanded}
 parameter='C=149^N' if count==163 else None
 certificate={
  'status':'conditional defining theorem under the retained arithmetic interfaces',
  'variables':count,'quadrics':len(rows),'degree':4,'content':1,
  'monomials':len(support),'parameter_separated_terms':len(expanded),
  'input':1,'parameter':parameter,
  'attribution':'Based on notes of Gabe Conant with Astra 6.2; v82 scalar and point changes',
  'theorem_source':'papers/quartic/scalar_point163_179_20261120_v82.tex',
  'height_formula':'max(126616122944180358034867798936,149^(4*N+2))' if count==163 else None,
  'height':max(map(abs,expanded.values())) if count==179 else None,
  'height_bits':max(map(abs,expanded.values())).bit_length() if count==179 else None,
  'anchor':{'base':ANCHOR,'boost':BOOST,'boost_primes':list(BOOST_PRIMES),
            'normalizer_numerator':NORMALIZER,'primes':list(PRIMES),
            'normalizer_prime_exponents':{str(p):5 if p in BOOST_PRIMES else 1 for p in PRIMES},
            'scalar_index_lower_bound':INDEX_BOUND} if count==179 else None,
  'retained_R_square':True,'deleted_source_coordinates':[188,189],
  'added_source_coordinates':[114] if count==179 else [],
  'aggregate':'unweighted' if count==179 else 'scalar point weighted by R',
 }
 output=destination/f'quartic{count}';output.mkdir(parents=True,exist_ok=True)
 docs={'quadrics.json':{'variables':count,'parameter':parameter,'input':1,
                      'residuals':[{'name':n,'terms':serial(p)} for n,p in rows]},
       'polynomial.json':{'variables':count,'parameter':parameter,'input':1,'terms':serial(expanded)},
       'certificate.json':certificate,'maps.json':maps}
 for filename,obj in docs.items():
  (output/filename).write_text(json.dumps(obj,indent=2 if filename in ('certificate.json','maps.json') else None)+'\n')
 return {k:certificate[k] for k in ('variables','quadrics','monomials','degree','content','height_bits')}

if __name__=='__main__':
 parser=ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args()
 for count in (163,179):print(json.dumps(build(count,args.output)))
