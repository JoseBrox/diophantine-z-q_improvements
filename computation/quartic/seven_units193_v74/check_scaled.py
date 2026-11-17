#!/usr/bin/env python3
"""Independent exact reconstruction and all-N height proof for compact193.

Does not import the producer or a computer algebra system. Every parameter
rescaling and every quartic coefficient is checked with integer arithmetic.
"""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
from math import comb,gcd
import json
HERE=Path(__file__).resolve().parent
EXPECTED={
 'compact':('primitive',126616122944180358034867798936,6,2770,2775),
 'compact_fewer_monomials':('fewer_monomials',484991541504995159662206970923766531374664106904986910720,13,2626,2631)}

def verify(folder):
    source_name,H0,cross,monomial_count,term_count=EXPECTED[folder]
    target=HERE/folder;source=HERE/source_name
    old=json.loads((source/'quadratic-family.json').read_text());new=json.loads((target/'quadratic-family.json').read_text());P=json.loads((target/'polynomial-family.json').read_text());T=json.loads((target/'parameter-transformation.json').read_text())
    assert T['source']==source_name
    assert T['source_quadratic_sha256']==sha256((source/'quadratic-family.json').read_bytes()).hexdigest()
    w={int(i):int(a)for i,a in T['weights'].items()};assert set(w)==set(range(1,194)) and w[1]==0
    assert {i for i,a in w.items()if a}=={44,45,46,47,52,53,54,55,56,57,99,100}
    assert set(w.values())=={0,-1}
    nr={x['name']:x for x in T['row_normalizations']};assert len(nr)==167
    assert old['coordinates']==new['coordinates'] and new['variables']==193
    assert len(new['residuals'])==len(old['residuals'])==167
    pullbacks=[]
    for previous,current in zip(old['residuals'],new['residuals']):
        assert previous['name']==current['name'] and previous['id']==current['id']
        assert len({tuple(t['monomial'])for t in current['terms']})==len(current['terms'])
        shift=nr[current['name']]['C_shift'];assert isinstance(shift,int)
        want={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in previous['terms']}
        got={}
        for t in current['terms']:
            assert 0<=t['parameterPower']<=1 and len(t['monomial'])<=2
            exponent=t['parameterPower']-sum(w[i] for i in t['monomial'])-shift
            key=exponent,tuple(t['monomial']);assert key not in got;got[key]=int(t['coefficient'])
        assert got==want,current['name']
        # At C=149 this gcd1 proves primitive rows for every C=149^N:
        # any common prime other than149 divides the same base coefficients;
        # divisibility by149 depends only on whether the exponent is zero.
        assert gcd(*(int(t['coefficient'])*149**t['parameterPower']for t in current['terms']))==1
        pullbacks.append(current['name'])
    expanded=defaultdict(int)
    for row in new['residuals']:
        terms=row['terms']
        for i,t in enumerate(terms):
            for j in range(i,len(terms)):
                s=terms[j];key=t['parameterPower']+s['parameterPower'],tuple(sorted(t['monomial']+s['monomial']))
                expanded[key]+=(1 if i==j else 2)*int(t['coefficient'])*int(s['coefficient'])
    expanded={k:c for k,c in expanded.items()if c};given={}
    for t in P['terms']:
        key=t['parameterPower'],tuple(t['monomial']);assert key not in given;given[key]=int(t['coefficient'])
    assert expanded==given and len(expanded)==term_count
    assert max(a for a,m in expanded)==2 and max(len(m)for a,m in expanded)==4
    assert expanded[0,(1,1,1,1)]==1
    assert not any(a and m==(1,1,1,1)for a,m in expanded)
    assert {i for a,m in expanded for i in m}==set(range(1,194))
    coefficients=defaultdict(dict)
    for (a,m),c in expanded.items():coefficients[m][a]=c
    assert len(coefficients)==monomial_count
    mixed=[(m,p)for m,p in coefficients.items()if len({1 if c>0 else-1 for c in p.values()})>1]
    assert len(mixed)==1 and mixed[0][1]=={0:-578,2:289}
    assert any(p=={0:H0}or p=={0:-H0}for p in coefficients.values())
    assert any(p=={2:22201}for p in coefficients.values())
    # A shorter certificate also proves the exact height for all real C>=149.
    linear_max=max(abs(p[1])for p in coefficients.values()if set(p)=={1})
    assert linear_max==384444691473074 and linear_max**2<=22201*H0
    multi=[p for p in coefficients.values()if len(p)>1]
    assert len(multi)==5
    for p in multi:
        if p=={0:-578,2:289}:continue
        assert set(p)=={0,2} and p[2]==1 and 0<p[0]
        assert 22201*p[0]<=22200*H0
    assert max(abs(p[2])for p in coefficients.values()if set(p)=={2})==22201
    assert max(abs(p[0])for p in coefficients.values()if set(p)=={0})==H0
    finite=[]
    for N in range(1,cross):
        C=149**N;actual=max(abs(sum(c*C**a for a,c in p.items()))for p in coefficients.values());assert actual==H0
        finite.append({'N':N,'exact_height':str(actual)})
    assert 22201*149**(2*(cross-1))<H0<22201*149**(2*cross)
    C0=149**cross;margins=[None]*3
    for p in coefficients.values():
        for sign in (-1,1):
            for k in range(3):
                margin=22201*comb(2,k)*C0**(2-k)+sign*sum(c*comb(a,k)*C0**(a-k)for a,c in p.items()if a>=k)
                assert margin>=0
                margins[k]=margin if margins[k]is None else min(margins[k],margin)
    report={'schema':'independent-compact-quartic193-audit/v74','status':'PASS','variables':193,'quadratic_rows':167,'all_parameter_pullbacks_exact':True,'changed_noninput_coordinates':12,'input_unchanged':True,'diagonal_map_bijective_for_every_nonzero_C':True,'degree':4,'content':1,'all_rows_primitive_for_C_149_power_N':True,'every_coordinate_occurs':True,'quartic_parameter_degree':2,'parameter_separated_terms':term_count,'coordinate_monomials_for_all_N_ge_1':monomial_count,'mixed_coefficient_polynomial':'289*(C^2-2), positive for C>=149','exact_height':{'formula':f'max({H0},149^(2N+2))','constant':str(H0),'leading_coefficient':22201,'parameter_degree':2,'coefficient_crossover_N':cross,'valid_for_every_real_C_ge_149':True,'linear_coefficient_maximum':linear_max,'dominance_checks':{'linear_max_squared_le_22201_H0':True,'all_four_positive_mixed_constants_times22201_le_22200_H0':True},'crossover_is_not_defining_threshold':True,'finite_cases':finite,'tail_certificate':f'All coefficients of22201*(149^{cross}+z)^2 +/- each coefficient polynomial at149^{cross}+z are nonnegative.','tail_inequalities':2*monomial_count,'minimum_tail_coefficients':margins},'source_quadratic_sha256':T['source_quadratic_sha256'],'quadratic_sha256':sha256((target/'quadratic-family.json').read_bytes()).hexdigest(),'quartic_sha256':sha256((target/'polynomial-family.json').read_bytes()).hexdigest(),'scope':'Exact input-preserving rational equivalence, all coefficient identities, degree, primitive rows, support and all-N height. Defining property inherits v73 arithmetic premises; sufficient N remains ineffective.'}
    (target/'independent-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='exact_height'},indent=2));print('Height',report['exact_height']['formula'])
    return report

if __name__=='__main__':
    for folder in EXPECTED:verify(folder)
