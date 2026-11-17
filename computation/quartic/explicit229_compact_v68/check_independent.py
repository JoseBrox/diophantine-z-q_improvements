#!/usr/bin/env python3
"""Independent exact verification using SymPy polynomial rings and a strict text parser."""
import argparse,hashlib,json,math,re
from fractions import Fraction
from pathlib import Path
from sympy.polys.rings import ring
from sympy.polys.domains import ZZ

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def power149(n):return Fraction(149**n) if n>=0 else Fraction(1,149**(-n))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--manuscript',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 p=a.package;spec=json.loads((p/'transformation.json').read_text());srcpath=a.repo/spec['source']['path'];source=json.loads(srcpath.read_text())
 assert sha(srcpath)==spec['source']['sha256']==sha(p/spec['source']['local'])
 assert source['variables']==spec['variables']==229 and spec['fixed_N']==15 and spec['base']==149
 assert source['inputCoordinate']==spec['inputCoordinate']==1
 powers=spec['coordinate_powers'];rowpowers=spec['row_powers']
 assert len(powers)==229 and len(rowpowers)==len(source['residuals'])==207 and powers[0]==0
 assert all(type(x) is int for x in powers+rowpowers)
 assert int(spec['fixed_parameter'])==149**15
 R,*xs=ring(','.join('x'+str(i) for i in range(1,230)),ZZ)
 expanded=R.zero;old_expanded=R.zero
 expected=json.loads((p/'quadratic.json').read_text())['residuals']
 assert len(expected)==207
 row_content=[]
 def dense(m):
  e=[0]*229
  for i in m:
   assert type(i) is int and 1<=i<=229;e[i-1]+=1
  return tuple(e)
 def sparse(e):return tuple(i+1 for i,n in enumerate(e) for _ in range(n))
 for j,(old,new) in enumerate(zip(source['residuals'],expected)):
  assert old['name']==new['name'] and old['id']==new['id']==j+1
  coefficients={};original={}
  for term in old['terms']:
   m=term['monomial'];c=Fraction(term['coefficient'])*149**(15*term['parameterPower'])
   exponent=dense(m);original[exponent]=original.get(exponent,Fraction(0))+c
   value=c*power149(rowpowers[j]+sum(powers[i-1] for i in m))
   coefficients[exponent]=coefficients.get(exponent,Fraction(0))+value
  coefficients={m:c for m,c in coefficients.items() if c}
  assert all(c.denominator==1 for c in coefficients.values())
  assert math.gcd(*(abs(int(c)) for c in coefficients.values()))==1
  assert all(sum(m)<=2 for m in coefficients)
  decoded={dense(t['monomial']):int(t['coefficient']) for t in new['terms']}
  assert len(decoded)==len(new['terms']) and decoded==coefficients,(j,old['name'])
  # Check the inverse substitution termwise as well.
  restored={m:Fraction(c)*power149(-rowpowers[j]-sum(e*w for e,w in zip(m,powers))) for m,c in coefficients.items()}
  assert restored=={m:c for m,c in original.items() if c}
  quadratic=R.from_dict({m:int(c) for m,c in coefficients.items()})
  expanded+=quadratic*quadratic
  oq=R.from_dict({m:int(c) for m,c in original.items() if c});old_expanded+=oq*oq
  row_content.append(1)
 actual={sparse(m):int(c) for m,c in expanded.items()}
 before={sparse(m):int(c) for m,c in old_expanded.items()}
 supplied=json.loads((p/'polynomial.json').read_text())
 assert supplied['variables']==229 and supplied['inputCoordinate']==1 and supplied['degree']==4
 comparison={tuple(t['monomial']):int(t['coefficient']) for t in supplied['terms']}
 assert len(comparison)==len(supplied['terms']) and comparison==actual
 assert set(actual)==set(before) and len(actual)==3312
 assert set(i for m in actual for i in m)==set(range(1,230))
 assert max(map(len,actual))==4 and actual[(1,1,1,1)]==1
 assert math.gcd(*(abs(c) for c in actual.values()))==1
 largest=max(map(abs,actual.values()));assert largest==149**30 and largest.bit_length()==217
 assert max(map(abs,before.values()))==149**32
 for m in [(77,77,101,101),(104,104,112,112),(111,111,112,112)]:assert actual[m]==largest
 raw=(p/'quartic229-N15.txt').read_bytes();text=raw.decode('ascii')
 assert raw and not any(ch.isspace() for ch in text) and text[0]!='+'
 tokens=list(re.finditer(r'[+-]?[^+-]+',text));assert ''.join(m.group() for m in tokens)==text
 parsed={};ordered=[]
 for t in tokens:
  item=t.group();sign=-1 if item.startswith('-') else 1
  if item[0] in '+-':item=item[1:]
  factors=item.split('*');c=1
  if not factors[0].startswith('x'):
   assert re.fullmatch(r'[1-9][0-9]*',factors[0]);c=int(factors.pop(0))
   assert not factors or c!=1
  monomial=[];last=0
  for f in factors:
   m=re.fullmatch(r'x([1-9][0-9]*)(?:\^([234]))?',f);assert m,f
   idx=int(m[1]);degree=int(m[2] or '1');assert last<idx<=229;last=idx
   monomial += [idx]*degree
  monomial=tuple(monomial);assert len(monomial)<=4 and monomial not in parsed
  parsed[monomial]=sign*c;ordered.append(monomial)
 assert ordered==sorted(ordered) and parsed==actual
 assert len(raw)==74007 and len(raw)<100000 and sha(p/'quartic229-N15.txt')=='45bdea1ea7876bf6ec10b5427f9403cf1f94c144fab35817aa545bcb2cea1975'
 manuscript=a.manuscript.read_text()
 for marker,values in [('Coordinate exponents',powers),('Row exponents',rowpowers)]:
  block=manuscript.split('\\subsection*{'+marker+'}',1)[1].split('\\end{longtable}',1)[0]
  decoded=[0]*len(values);seen=set()
  for weight,indices in re.findall(r'(?m)^(-?\d+) & ([0-9, ]+)\\\\$',block):
   for token in indices.split(','):
    idx=int(token.strip());assert idx not in seen and 1<=idx<=len(values);seen.add(idx);decoded[idx-1]=int(weight)
  assert decoded==values,marker
 oldpaper=(a.repo/'papers/quartic/quartic229_20261117_v62.tex').read_text()
 section='\\section{Exact specification and arithmetic scope}'
 oldbody=oldpaper.split(section,1)[1].split('\\begin{thebibliography}',1)[0].strip().replace('thm:main','thm:source')
 newbody=manuscript.split(section,1)[1].split('\\section{The fixed quartic with coefficient height',1)[0].strip()
 assert oldbody==newbody,'The retained arithmetic body changed'
 assert sha(p/'upstream/measure_plain_text.py')==spec['official_measurer']['sha256']
 assert sha(p/'upstream/explicit-record-README.md')==spec['official_notation']['sha256']
 report={'status':'PASS','engine':'Independent SymPy sparse polynomial rings, rational termwise maps, strict ASCII parser; no producer or author checker imported','source_sha256':sha(srcpath),'transformation_sha256':sha(p/'transformation.json'),'manuscript_sha256':sha(a.manuscript),'checker_sha256':sha(Path(__file__)),'variables':229,'quadratic_rows':207,'rows_primitive':True,'inverse_map_checked':True,'input_fixed':True,'degree':4,'monomials':3312,'support_unchanged':True,'content':1,'height':str(largest),'height_expression':'149^30','height_bits':217,'coefficient_digits':sum(len(str(abs(c))) for c in actual.values()),'canonical_bytes':len(raw),'strict_limit_bytes':100000,'within_limit':True,'text_sha256':sha(p/'quartic229-N15.txt'),'all_207_row_coefficients_checked':True,'all_3312_expanded_coefficients_checked':True,'complete_literal_text_parsed':True,'manuscript_exponent_tables_checked':True,'retained_arithmetic_body_unchanged_except_theorem_label':True,'scope':'Exact input-preserving rational equivalence and every coefficient, support, height and canonical-text assertion. Retained source arithmetic premises are not independently re-proved.'}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
