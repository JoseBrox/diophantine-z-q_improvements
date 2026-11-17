#!/usr/bin/env python3
"""Check every coefficient and parse the fully expanded polynomial independently.

Standard library only. This checker imports neither the producer nor the
optimizer nor the upstream measuring implementation.
"""
from collections import Counter,defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
SOURCE_HASH='f0e6fc3f62525d7b251a10fc5f4cf0e6663c3f6f08beeef3cb28092b2e1555a8'
TEXT_HASH='45bdea1ea7876bf6ec10b5427f9403cf1f94c144fab35817aa545bcb2cea1975'
MEASURER_HASH='7ab1ec5cf5838589abf5d31cc44e00a01912d6c490b737a6ad45a1ec3f195a2d'


def parse(raw):
    text=raw.decode('ascii')
    assert text and not any(c.isspace() for c in text)
    pieces=re.findall(r'[+-]?[^+-]+',text)
    assert ''.join(pieces)==text
    result={}
    for j,piece in enumerate(pieces):
        assert j==0 or piece[0]in'+-'
        assert j>0 or piece[0]!='+'
        sign=-1 if piece.startswith('-')else 1
        body=piece[1:]if piece[:1]in'+-'else piece
        factors=body.split('*')
        coefficient=1
        if re.fullmatch('[1-9][0-9]*',factors[0]):
            coefficient=int(factors.pop(0))
            assert coefficient!=1 or not factors,'Unit coefficient must be omitted'
        mon=[];last=0
        for factor in factors:
            match=re.fullmatch(r'x([1-9][0-9]*)(?:\^([234]))?',factor)
            assert match,'Invalid ordinary variable/power'
            i=int(match[1]);power=int(match[2]or'1')
            assert last<i<=229
            last=i;mon.extend([i]*power)
        key=tuple(mon)
        assert key not in result and len(key)<=4
        result[key]=sign*coefficient
    assert list(result)==sorted(result),'Term order is not canonical'
    return result


def table(data):
    result={}
    for term in data['terms']:
        m=tuple(term['monomial']);c=term['coefficient']
        assert list(m)==sorted(m)and m not in result
        assert re.fullmatch(r'-?[1-9][0-9]*',c)
        assert term.get('parameterPower',0)==0
        result[m]=int(c)
    return result


def square(rows):
    p=defaultdict(int)
    for row in rows:
        terms=list(row.items())
        for i,j in combinations_with_replacement(range(len(terms)),2):
            m,c=terms[i];n,d=terms[j]
            p[tuple(sorted(m+n))]+=c*d*(1 if i==j else 2)
    return {m:c for m,c in p.items()if c}


def validate_input_map(transform):
    a=transform['coordinate_powers'];b=transform['row_powers']
    assert transform['base']==149 and transform['fixed_N']==15
    assert transform['variables']==229 and transform['inputCoordinate']==1
    assert transform['fixed_parameter']==str(149**15)
    assert len(a)==229 and all(type(x)is int for x in a)and a[0]==0
    assert len(b)==207 and all(type(x)is int for x in b)
    return a,b


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'certificate.json')
    args=parser.parse_args()
    manifest_raw=(ROOT/'transformation.json').read_bytes()
    manifest=json.loads(manifest_raw)
    a,b=validate_input_map(manifest)
    source_raw=(ROOT/'source/quadratic229-v62.json').read_bytes()
    assert sha256(source_raw).hexdigest()==SOURCE_HASH==manifest['source']['sha256']
    source=json.loads(source_raw)
    assert source['variables']==229 and source['inputCoordinate']==1
    assert len(source['residuals'])==207
    new_rows=[];old_rows=[]
    for j,row in enumerate(source['residuals']):
        old=defaultdict(int)
        for term in row['terms']:
            old[tuple(term['monomial'])]+=int(term['coefficient'])*149**(15*term['parameterPower'])
        old={m:c for m,c in old.items()if c}
        changed={m:Fraction(c)*Fraction(149)**(b[j]+sum(a[i-1]for i in m))for m,c in old.items()}
        assert all(c.denominator==1 for c in changed.values())
        changed={m:int(c)for m,c in changed.items()}
        assert gcd(*changed.values())==1
        assert max(map(len,changed))<=2
        new_rows.append(changed);old_rows.append(old)
    quadratic_raw=(ROOT/'quadratic.json').read_bytes()
    quadratic=json.loads(quadratic_raw)
    assert quadratic['variables']==229 and quadratic['inputCoordinate']==1
    assert len(quadratic['residuals'])==207
    for j,row in enumerate(quadratic['residuals']):
        assert row['id']==j+1
        assert row['name']==source['residuals'][j]['name']
        assert table(row)==new_rows[j]
    expected=square(new_rows)
    original=square(old_rows)
    polynomial_raw=(ROOT/'polynomial.json').read_bytes()
    polynomial=json.loads(polynomial_raw)
    assert polynomial['variables']==229 and polynomial['inputCoordinate']==1
    assert polynomial['degree']==4
    assert table(polynomial)==expected
    literal_raw=(ROOT/'quartic229-N15.txt').read_bytes()
    parsed=parse(literal_raw)
    assert parsed==expected
    assert len(literal_raw)==74007 and sha256(literal_raw).hexdigest()==TEXT_HASH
    assert len(expected)==3312 and set(expected)==set(original)
    assert max(map(len,expected))==4 and gcd(*expected.values())==1
    assert expected[(1,1,1,1)]==1
    assert {i for m in expected for i in m}==set(range(1,230))
    assert max(map(abs,expected.values()))==149**30
    assert max(map(abs,original.values()))==149**32
    assert sum(len(str(abs(c)))for c in expected.values())==21633
    assert sum(len(str(abs(c)))for c in original.values())==95953
    negative_controls={}
    for label,bad in [('trailing_newline',literal_raw+b'\n'),('leading_plus',b'+'+literal_raw),('coefficient_abbreviation',literal_raw.replace(b'x1^4',b'2^1*x1^4',1))]:
        try:parse(bad)
        except (AssertionError,ValueError,UnicodeDecodeError):negative_controls[label]=True
        else:raise AssertionError('Parser accepted '+label)
    bad=dict(manifest,coordinate_powers=[1]+a[1:])
    try:validate_input_map(bad)
    except AssertionError:negative_controls['scaled_input']=True
    else:raise AssertionError('Changed input map accepted')
    changed=dict(expected);changed[(1,1,1,1)]+=1
    assert parsed!=changed;negative_controls['changed_coefficient']=True
    measurer=ROOT/'upstream/measure_plain_text.py'
    assert sha256(measurer.read_bytes()).hexdigest()==MEASURER_HASH
    official=subprocess.run([sys.executable,'-B',str(measurer),str(ROOT/'polynomial.json'),'--verify-text',str(ROOT/'quartic229-N15.txt')],check=True,capture_output=True,text=True)
    official_report=json.loads(official.stdout)
    assert official_report['bytes']==74007 and official_report['within_limit']
    assert official_report['verify_text_matches']and official_report['sha256']==TEXT_HASH
    (ROOT/'official_measurement.json').write_text(json.dumps(official_report,indent=2)+'\n')
    report=dict(schema='compact-explicit229-verification/v68',status='PASS',scope='Exact rational diagonal map, every transformed quadratic and quartic coefficient, standalone literal parser, unchanged monomial support, source input preservation, and upstream canonical measurement. The arithmetic defining theorem is inherited from the pinned N15 source.',variables=229,inputCoordinate=1,input_scaling_exponent=0,quadratic_rows=207,monomials=3312,degree=4,content=1,source_fixed_N=15,source_coefficient_height=str(149**32),coefficient_height=str(149**30),coefficient_height_bits=(149**30).bit_length(),coefficient_height_improvement_factor=149**2,coefficient_digits=21633,bytes=len(literal_raw),strictly_below_100000=True,strictly_below_102400=True,bytes_below_decimal_limit=100000-len(literal_raw),unchanged_coordinate_order=True,unchanged_monomial_support=True,all_rows_primitive=True,all_scalars_nonzero=True,rational_coordinate_inverse='new_x[i]=149^(-coordinate_powers[i-1])*old_x[i]',producer_imported=False,optimizer_required=False,negative_controls=negative_controls,source_sha256=SOURCE_HASH,transformation_sha256=sha256(manifest_raw).hexdigest(),quadratic_sha256=sha256(quadratic_raw).hexdigest(),polynomial_sha256=sha256(polynomial_raw).hexdigest(),literal_sha256=TEXT_HASH,measurer_sha256=MEASURER_HASH,checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
