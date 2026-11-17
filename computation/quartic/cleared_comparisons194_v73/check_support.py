#!/usr/bin/env python3
"""Independent standard-library check of the concrete 194 support witness.

No solver is imported. This verifies every listed Laurent support and every
selected detector test against the proposed monomial change of variables.
It does not certify coefficient reconstruction or arithmetic completeness.
"""
from pathlib import Path
from hashlib import sha256
from itertools import combinations_with_replacement,product
import json,argparse
HERE=Path(__file__).resolve().parent

def verify(model_path,result_path):
    raw=Path(model_path).read_bytes();D=json.loads(raw);R=json.loads(Path(result_path).read_text())
    assert R['status']=='sat'
    assert R['model_sha256']==sha256(raw).hexdigest()
    active=set(D['active']);units={int(i):tuple(e)for i,e in D['base_units'].items()}
    assert len(active)==186 and len(units)==8 and not(active&set(units))
    assert len(active)+len(units)==194
    assert units=={77:(1,0),78:(-1,0),90:(0,1),91:(0,-1),92:(-1,-2),901:(0,-3),902:(1,-1),903:(-1,-1)}
    weights={int(i):tuple(e)for i,e in R['weights'].items()};rw={k:tuple(v)for k,v in R['row_weights'].items()}
    assert set(weights)==active and weights[1]==(0,0)
    rows={r['name']:r for r in D['rows']};assert len(rows)==len(D['rows']) and set(rw)==set(rows)
    options={}
    for k in range(3):
        options[k]={}
        for mon in combinations_with_replacement([0]+sorted(units),k):
            e=tuple(sum(units.get(i,(0,0))[d]for i in mon)for d in range(2))
            options[k].setdefault(e,tuple(i for i in mon if i))
    checked=[]
    def one(row,m,e,label):
        m=tuple(m);assert len(m)<=2 and all(i in active for i in m)
        exponent=tuple(e[d]+sum(weights[i][d]for i in m)-rw[row][d]for d in range(2))
        assert exponent in options[2-len(m)],(row,m,exponent)
        output=tuple(sorted(m+options[2-len(m)][exponent]));assert len(output)<=2
        checked.append({'row':row,'source':label,'monomial':m,'unit_exponent':exponent,'compiled_monomial':output})
    for row in D['rows']:
        for m,e in row['terms']:one(row['name'],m,e,'literal')
    for det in (0,1):
        A=R['assignments'][str(det)]
        assert set(A['quadratic'])==set(D['quadratic_tests']) and sorted(A['quadratic'].values())==list(range(8))
        assert set(A['linear'])==set(D['linear_tests']) and sorted(A['linear'].values())==list(range(7))
        for name,(i,e,base)in D['quadratic_tests'].items():
            slot=A['quadratic'][name];q=base+2*(slot%2);exp=(e[0]+q,e[1]+det*q)
            row=D['rows'][D['factor_rows'][f'{det},{slot//2}']]['name']
            for aa,bb in ((0,0),(0,1),(1,1)):one(row,(i+aa,i+bb),exp,'quadratic:'+name)
        for name,(i,e)in D['linear_tests'].items():
            slot=A['linear'][name];q=2 if slot<4 else slot-3;exp=(e[0]+q,e[1]+det*q)
            row=D['rows'][D['factor_rows'][f'{det},{slot if slot<4 else 4}']]['name']
            for aa in(0,1):one(row,(i+aa,),exp,'linear:'+name)
    # Exact polynomial unit equations. Each row has two signed monomials.
    guards=[[(1,()),(-1,(77,78))],[(1,()),(-1,(90,91))],[(1,(77,92)),(-1,(91,91))],[(1,(901,90)),(-1,(91,91))],[(1,(902,)),(-1,(77,91))],[(1,(903,)),(-1,(78,91))]]
    for equation in guards:
        value={}
        for c,m in equation:
            assert len(m)<=2
            e=tuple(sum(units[i][d]for i in m)for d in range(2))
            value[e]=value.get(e,0)+c
        assert not any(value.values())
    nonzero={77,78,90,91}
    # First two guards force four units nonzero. The remaining rows are
    # nonzero monomial equalities with exactly one newly introduced unit.
    for new,dependencies in [(92,[77,91]),(901,[90,91]),(902,[77,91]),(903,[78,91])]:
        assert set(dependencies)<=nonzero;nonzero.add(new)
    assert nonzero==set(units)
    return {'schema':'independent-quartic194-support-certificate/v71','model_sha256':sha256(raw).hexdigest(),'result_sha256':sha256(Path(result_path).read_bytes()).hexdigest(),'coordinates':194,'active_coordinates':186,'unit_coordinates':8,'rows_checked':len(rows),'support_and_test_terms_checked':len(checked),'compiled_max_degree':max(len(t['compiled_monomial'])for t in checked),'unit_guard_rows':6,'all_unit_nonvanishing_proved':True,'input_unchanged':True,'weight_range':{str(d):[min(e[d]for e in weights.values()),max(e[d]for e in weights.values())]for d in range(2)},'status':'PASS: exact support and unit certificate only; coefficient rows and arithmetic transfer remain separate obligations.','unit_guards':guards,'term_certificate':checked}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model',type=Path,default=HERE/'coordinate-model.json')
    ap.add_argument('--result',type=Path,default=HERE/'laurent-certificate.json')
    ap.add_argument('--output',type=Path,default=HERE/'quartic194_support_certificate.json')
    a=ap.parse_args();C=verify(a.model,a.result);a.output.write_text(json.dumps(C,indent=2)+'\n')
    print(json.dumps({k:v for k,v in C.items()if k not in ['term_certificate','unit_guards']},indent=2))
if __name__=='__main__':main()
