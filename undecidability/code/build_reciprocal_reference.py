#!/usr/bin/env python3
"""Save one coordinate in the general shared-reference quartic tables.

Finite rational-chart equivalence only: U_em and the retained arithmetic
interfaces are not verified here. Input-square register 37 stores 1/v in
the new chart; registers 77 and 78 are rescaled by existing nonzero units.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
import sympy as sp

DEFAULT_REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(DEFAULT_REPO/'undecidability/code'))
from quadratic_utils import SOURCES,rechart179

A_STAR=31871408200417997055663403729056374200285490894971474529459671866624515112811224229504038750608191413928644277259

def changed_rows(m):
    """Local indices; index 0 denotes the outer inverse v."""
    z={j:sp.Symbol('z'+str(j)) for j in range(0,m+1)}
    v,t,h,r,R=z[0],z[37],z[77],z[78],z[90]
    C=sp.Symbol('C_parameter')
    p0,p1=(117,118) if m==163 else (118,119)
    ans={
      'inputSquare.definition':1-v*t,
      'scalar.rPair1.definition':2601*t*t+255102*t*v-4*h*v+6255001*v*v,
      'scalar.four_contact_product.definition':15531948*t*h+291790992*t*v-512*h*h+767410608*h*v+14315517724*v*v+(r*v if m==163 else r*R),
      'scalar.forced_prime.definition':22201*r*R+v*R-149*C*C*r if m==163 else 25*r*R-A_STAR*r+v*v,
      'input.cleared.0':v*(-z[17]+z[23]+2504*z[p0])+51*t*z[p0],
      'input.cleared.1':v*(-z[18]+z[24]+2504*z[p1])+51*t*z[p1],
    }
    return ans,z

def audit_chart(m,repo):
    src=json.loads((repo/SOURCES[m]).read_text())
    if m==179:src,_=rechart179(src)
    formulas,z=changed_rows(m)
    v,t,h,r=z[0],z[37],z[77],z[78]
    q=sp.Symbol('q',nonzero=True);C=sp.Symbol('C_parameter')
    q0,q1,q2=(159,160,161) if m==163 else (162,163,164)
    subst={**z,1:1/v,37:t/(v*q),77:h/(v*q),78:r/v if m==163 else r/(v*v*q*q),q0:q,q1:1/q,q2:1/q**2}
    factors={'inputSquare.definition':v*v,
      'scalar.rPair1.definition':v*v*q*q,
      'scalar.four_contact_product.definition':v*v*q*q,
      'scalar.forced_prime.definition':v if m==163 else v*v*q*q,
      'input.cleared.0':v*q,'input.cleared.1':v*q}
    changed=[]
    for row in src['residuals']:
        touch=any({1,37,77,78}&set(a['monomial']) for a in row['terms'])
        if not touch:continue
        name=row['name'];assert name in formulas
        p=sum(sp.Integer(a['coefficient'])*C**a.get('parameterPower',0)*sp.prod(subst[j] for j in a['monomial']) for a in row['terms'])
        assert sp.cancel(factors[name]*p-formulas[name])==0,name
        assert sp.Poly(formulas[name],*z.values()).total_degree()==2
        changed.append(name)
    assert set(changed)==set(formulas)
    return formulas,z,{'affected_rows':sorted(changed),'unit_ids':[q0,q1,q2],
      'old_coordinates_in_new_chart':{'37':'t/(v*q)','77':'h/(v*q)','78':'r/v' if m==163 else 'r/(v^2*q^2)'},
      'nonzero_row_multipliers':{k:str(v) for k,v in factors.items()},
      'exact_substitution_identities':True,'all_affected_rows_enumerated':True}

def build(m,repo,baseline):
    data=json.loads(baseline.read_text());assert m in (163,179)
    assert data['source_universality_hypothesis']=='U_em'
    assert data['source_universality_verified'] is False
    assert data['unconditional_undecidability_claim'] is False
    formulas,z,chart=audit_chart(m,repo)
    oldnames=data['variable_names'];oldids=dict(enumerate(oldnames,1))
    assert oldnames[-1]=='i'
    newnames=oldnames[:-1];newids={n:j+1 for j,n in enumerate(newnames)}
    expected={'integer.i.inputSquare.definition','integer.i_reciprocal.unit'}
    iidx=len(oldnames)
    assert {r['name'] for r in data['residuals'] if any(iidx in t['monomial'] for t in r['terms'])}==expected
    refs=data['shared_reference_ids']
    def localname(j):return 'i_inverse' if j==0 else f'int_b_{j}' if j in refs else f'int_i_reciprocal_{j}'
    def serialize(expr):
        out=[]
        for exps,c in sp.Poly(sp.expand(expr),*z.values()).terms():
            mon=sorted(newids[localname(j)] for j,e in zip(z,exps) for _ in range(e))
            assert len(mon)<=2
            out.append({'monomial':mon,'coefficient':str(c)})
        return sorted(out,key=lambda x:x['monomial'])
    rows=[]
    for row in data['residuals']:
        name=row['name']
        if name=='integer.i_reciprocal.unit':continue
        if name.startswith('integer.i.') and name[len('integer.i.'):] in formulas:
            p=formulas[name[len('integer.i.'):]]
            rows.append({'name':name,'terms':serialize(p)})
        else:
            terms=[{'monomial':sorted(newids[oldids[j]] for j in t['monomial']),'coefficient':t['coefficient']} for t in row['terms']]
            rows.append({'name':name,'terms':terms})
    assert len(newnames)==data['variables']-1
    assert len(rows)==len(data['residuals'])-1
    assert {j for r in rows for t in r['terms'] for j in t['monomial']}==set(range(1,len(newnames)+1))
    result=dict(data)
    result.update({'variables':len(newnames),'variable_names':newnames,'residuals':rows,
      'outer_coordinates':data['outer_coordinates']-1,'outer_residuals':data['outer_residuals']-1,
      'ordinary_integer_inputs':[i for i in data['ordinary_integer_inputs'] if i!='i'],
      'reciprocal_integer_inputs':['i_inverse'],
      'reciprocal_nonzero_guard':'i_inverse*int_i_reciprocal_37=1; register37 stores the source input i=1/i_inverse',
      'reciprocal_register_chart':chart,
      'shared_reference_baseline_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),
      'reciprocal_chart_savings':{'coordinates':1,'residuals':1}})
    cert={k:v for k,v in result.items() if k not in ['variable_names','residuals','power_chain']}
    cert['quadratic_residuals']=len(rows)
    cert['verified']=['six exact rational-chart identities against each source table','complete occurrence audit for changed registers','literal new reciprocal unit row','unchanged ten shared reference registers','degree and coordinate support','complete materialized table']
    cert['not_verified']=['U_em: universality of the exact emended source','external arithmetic premises','minimality of the variable count']
    return result,cert

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',type=Path,default=DEFAULT_REPO)
    ap.add_argument('--baseline',type=Path,default=DEFAULT_REPO/'undecidability/coefficients/jones1980_shared')
    ap.add_argument('--out',type=Path,default=DEFAULT_REPO/'undecidability/coefficients/jones1980_shared_reciprocal')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    for m in (163,179):
        result,cert=build(m,args.repo,args.baseline/f'shared_reference_m{m}_quadrics.json')
        target=args.out/f'reciprocal_reference_m{m}_quadrics.json'
        target.write_text(json.dumps(result,separators=(',',':'),sort_keys=True)+'\n')
        cert['table_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        (args.out/f'reciprocal_reference_m{m}_certificate.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'m':m,'N':result['variables'],'quadrics':len(result['residuals']),'sha256':cert['table_sha256']}))
if __name__=='__main__':main()
