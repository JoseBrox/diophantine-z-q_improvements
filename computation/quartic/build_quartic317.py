#!/usr/bin/env python3
"""Build the parity-free aggregate-trace quartic family in317 total variables."""
from collections import defaultdict
from fractions import Fraction
from math import gcd,lcm
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
SOURCE_PIN='9a9ece7045ebc14f1101aaf85bb7566434d4c411c9820669015242ba5df4170b'

def plus(*polys):
    r=defaultdict(Fraction)
    for p in polys:
        for k,c in p.items():r[k]+=c
    return {k:c for k,c in r.items() if c}
def mul(p,q):
    r=defaultdict(Fraction)
    for (e,m),a in p.items():
        for (f,n),b in q.items():r[e+f,tuple(sorted(m+n))]+=a*b
    return {k:c for k,c in r.items() if c}
def primitive(p):
    den=lcm(*(c.denominator for c in p.values()))
    z={k:int(c*den) for k,c in p.items()}
    common=gcd(*z.values())
    if z[min(z)]<0:common=-common
    return {k:c//common for k,c in sorted(z.items())}

def main():
    raw=(HERE/'family329/quadratic-family329.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SOURCE_PIN
    old=json.loads(raw)
    removed={x['id'] for x in old['coordinates'] if '.odd.' in x['name']}
    assert len(removed)==12
    coords=[];mapping={}
    for x in old['coordinates']:
        if x['id'] in removed:continue
        mapping[x['id']]=len(coords)+1
        coords.append(dict(x,id=mapping[x['id']]))
    old_input=old['inputCoordinate']
    old_square=next(x['id'] for x in old['coordinates'] if x['sourceId']==248)
    X=mapping[old_input];Y=mapping[old_square]
    replacement={j:{(0,(mapping[j],)):Fraction(1)} for j in mapping}
    replacement[old_input]={(0,(X,)):Fraction(1,2),(0,()):Fraction(-1,2)}
    replacement[old_square]={(0,(Y,)):Fraction(1,4),(0,(X,)):Fraction(-1,2),(0,()):Fraction(1,4)}
    rows=[];deleted_rows=[];changed=[]
    for row in old['residuals']:
        if any(j in removed for t in row['terms'] for j in t['monomial']):
            assert '.odd.' in row['name']
            deleted_rows.append(row['sourceId']);continue
        p={}
        for t in row['terms']:
            a=int(t['coefficient'])
            if row['sourceId']==492 and a==4896:a=9792
            term={(t['parameterPower'],()):Fraction(a)}
            for j in t['monomial']:term=mul(term,replacement[j])
            p=plus(p,term)
        q=primitive(p)
        terms=[{'parameterPower':e,'monomial':list(m),'coefficient':str(a)} for (e,m),a in q.items()]
        rows.append(dict(row,terms=terms))
        if any(j in {old_input,old_square} for t in row['terms'] for j in t['monomial']) or row['sourceId']==492:
            changed.append(row['sourceId'])
    coeff=defaultdict(int)
    for row in rows:
        for a in row['terms']:
            for b in row['terms']:
                coeff[a['parameterPower']+b['parameterPower'],tuple(sorted(a['monomial']+b['monomial']))]+=int(a['coefficient'])*int(b['coefficient'])
    coeff={k:a for k,a in coeff.items() if a}
    terms=[{'parameterPower':e,'monomial':list(m),'coefficient':str(a)} for (e,m),a in sorted(coeff.items())]
    out=HERE/'family317';out.mkdir(exist_ok=True)
    ir={'format':'integer-quadratic-family-v2','variables':len(coords),'inputCoordinate':1,
        'fixedParameter':old['fixedParameter'],'source':{'sha256':SOURCE_PIN,'construction':'quartic-family329'},
        'coordinates':coords,'residuals':rows}
    poly={'format':'integer-quartic-family-v2','variables':len(coords),'degree':4,'inputCoordinate':1,
          'fixedParameter':old['fixedParameter'],'coordinates':coords,'terms':terms}
    (out/'quadratic-family317.json').write_text(json.dumps(ir,indent=2)+'\n')
    (out/'polynomial-family317.json').write_text(json.dumps(poly,indent=2)+'\n')
    ordinary=defaultdict(dict)
    for (e,m),a in coeff.items():ordinary[m][e]=a
    height=max(sum(abs(a) for a in p.values()) for p in ordinary.values())
    report={'status':'Exact family; defining parameters exist above an ineffective threshold.',
        'variables':len(coords),'quadraticResiduals':len(rows),'degree':max(len(m) for e,m in coeff),
        'symbolicTerms':len(terms),'ordinaryMonomialsForSufficientlyLargeN':len(ordinary),
        'deletedOddChartSourceRows':deleted_rows,'changedSourceRows':changed,
        'inputSubstitution':{'oldInput':'(X-1)/2','oldInputSquare':'(Y-2*X+1)/4','newInputSquareEquation':'Y=X^2'},
        'inputLabel':'beta=51*X^2+2504','scalarShift':9792,
        'heightBound':{'coefficientSumBitLength':height.bit_length(),'formula':f'H(P_N)<2^{height.bit_length()}*80989^(4*N+2)'},
        'warning':'The sufficient threshold forN is not determined effectively; no explicit defining member is claimed.'}
    (out/'construction-report317.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','variables','quadraticResiduals','degree','symbolicTerms','ordinaryMonomialsForSufficientlyLargeN','heightBound']},indent=2))

if __name__=='__main__':main()
