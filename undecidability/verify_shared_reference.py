#!/usr/bin/env python3
"""Verify the finite common-reference checkpoint, explicitly conditional on U_em.

A PASS does not prove U_em or the retained arithmetic interfaces. It checks
the complete sparse specifications, exact row identifications, coefficients,
degree, reciprocal guard, coordinate support, hashes, and qualifications.
"""
from pathlib import Path
import hashlib
import json
import sys
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'undecidability'
sys.path.insert(0,str(BASE/'code'))
import build_shared_reference as compiler

def verify():
    result={}
    for m,N,R,reference_count,duplicate_count in (
        (163,2086,1776,10,8),(179,2278,1944,10,8),(56,846,728,6,4)
    ):
        baseline=BASE/f'coefficients/jones1980/jones1980_m{m}_quadrics.json'
        table,certificate=compiler.build(m,ROOT,baseline)
        path=BASE/f'coefficients/jones1980_shared/shared_reference_m{m}_quadrics.json'
        raw=path.read_bytes()
        expected=(json.dumps(table,separators=(',',':'),sort_keys=True)+'\n').encode()
        assert raw==expected,(m,'complete sparse table mismatch')
        certificate['table_sha256']=hashlib.sha256(raw).hexdigest()
        stored=json.loads(path.with_name(f'shared_reference_m{m}_certificate.json').read_text())
        assert stored==json.loads(json.dumps(certificate)),(m,'certificate mismatch')
        assert table['variables']==N and len(table['residuals'])==R
        assert len(table['shared_reference_ids'])==reference_count
        assert len(table['shared_reference_rows'])==duplicate_count
        assert table['shared_reference_blocks']==12
        assert table['shared_reference_coordinates_saved']==11*reference_count
        assert table['shared_reference_duplicate_rows_removed']==11*duplicate_count
        assert table['outer_coordinates']==252 and table['outer_residuals']==220
        assert table['source_universality_hypothesis']=='U_em'
        assert table['source_universality_verified'] is False
        assert table['unconditional_undecidability_claim'] is False
        assert 'U_em' in table['status'] and 'U_em' in table['source_universality']
        assert 'U_em: universality of the exact emended source' in stored['not_verified']
        assert table['baseline_table_sha256']==hashlib.sha256(baseline.read_bytes()).hexdigest()
        names=table['variable_names'];indices={v:i+1 for i,v in enumerate(names)}
        assert len(names)==len(set(names))==N
        assert len({r['name'] for r in table['residuals']})==R
        parameters=sp.symbols(' '.join(table['parameters']))
        loc=dict(zip(table['parameters'],parameters))
        support=set();quadratic_seen=False
        for row in table['residuals']:
            assert row['terms']
            for term in row['terms']:
                mon=term['monomial']
                assert len(mon)<=2 and mon==sorted(mon)
                assert all(1<=v<=N for v in mon)
                support.update(mon)
                coefficient=sp.sympify(term['coefficient'],locals=loc)
                assert coefficient!=0
                assert sp.Poly(coefficient,*parameters).domain.is_ZZ
                quadratic_seen|=len(mon)==2
        assert support==set(range(1,N+1)) and quadratic_seen
        # The reciprocal input is now represented by a literal unit equation,
        # rather than sharing differently scaled projective reference values.
        unit=[r for r in table['residuals'] if r['name']=='integer.i_reciprocal.unit']
        assert len(unit)==1
        assert unit[0]['terms']==[
            {'monomial':[],'coefficient':'-1'},
            {'monomial':sorted([indices['i'],indices['i_inverse']]),'coefficient':'1'}
        ]
        assert table['ordinary_integer_inputs'][-1]=='i'
        assert table['reciprocal_integer_inputs']==[]
        assert len(table['ordinary_integer_inputs'])==12
        # A constant pure triangular square coefficient survives every allowed
        # specialization, establishing a nonzero homogeneous quadratic part.
        guards=[r for r in table['residuals'] if r['name'].startswith('jones1980.positive.')]
        assert len(guards)==11
        assert all(any(len(t['monomial'])==2 and t['monomial'][0]==t['monomial'][1]
                       and names[t['monomial'][0]-1].startswith('positive_')
                       and t['coefficient']=='-1' for t in r['terms']) for r in guards)
        if m==56:
            assert table['simultaneous_completeness_scope'].startswith('nonzero integer tuples')
        result[str(m)]={'variables':N,'quadratic_residuals':R,
                        'source_universality_verified':False,
                        'table_sha256':certificate['table_sha256']}
    return {
        'status':'PASS',
        'scope':'Exact common-reference sparse systems, row identifications, reciprocal guard, coefficient rings, degree, support, counts and source-hypothesis metadata.',
        'undecidability_hypotheses':['U_em','all retained arithmetic premises of the selected integer interface','ordinary rational abc for m=56'],
        'unconditional_undecidability_claim':False,
        'routes':result,
    }

if __name__=='__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True))
