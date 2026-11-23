#!/usr/bin/env python3
"""Independent exact audit of the thirteen-block general power table.

No builder is imported. The power rows are specified independently below.
The new certificates are reconstructed from the earlier, unprogressed
ordinary o block, with direct contact substitutions at indices12 and13.
This differs from the builder's graded scaling of an already progressed
template and checks every coefficient of that family extension.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
NEW_BLOCKS=[('power_delta',12),('power_alpha',13)]
PREFIXES=('integer.o.','global.o.','scalar_norm.o.','detector_trace.o.')
CROSS={'integer.i.balanced.detector1.poleInput.definition',
       'integer.i.shared.inverse1','integer.i.shared.gate1'}


def expr(row,names):
    return sp.expand(sum(sp.sympify(term['coefficient'])*
                         sp.prod(sp.Symbol(names[i-1]) for i in term['monomial'])
                         for term in row['terms']))


def verify():
    oldpath=ROOT/'undecidability/pell_halftrace_v96/halftrace_m163_quadrics.json'
    sourcepath=ROOT/'undecidability/source_repair_v93/coefficients/corrected_ceiling_m163_quadrics.json'
    target=HERE/'power_general_m163_quadrics.json'
    certificate_path=HERE/'power_general_m163_certificate.json'
    old,source,new,certificate=[json.loads(p.read_bytes()) for p in (oldpath,sourcepath,target,certificate_path)]
    assert certificate['table_sha256']==hashlib.sha256(target.read_bytes()).hexdigest()
    assert certificate['predecessor_sha256']==hashlib.sha256(oldpath.read_bytes()).hexdigest()
    affine_template=ROOT/certificate['template']
    assert certificate['template_sha256']==hashlib.sha256(affine_template.read_bytes()).hexdigest()
    oldnames=old['variable_names']; sourcenames=source['variable_names']; names=new['variable_names']
    removed={name for name in oldnames if name=='power_001' or name.startswith('ceiling_power_')}
    assert len(removed)==137
    core_added=['power_delta','power_alpha','power_b4','power_A','power_C','power_D','power_modulus','power_AC']
    core_added += [f'power_positive_{label}_{i}' for label in ('q','bound') for i in (1,2,3)]
    source_aux=[name for name in sourcenames if name.startswith('int_o_')
                and name not in ('int_o_2','int_o_60','int_o_61')]
    assert len(source_aux)==60
    def renamed(name,label):
        if name=='o':return label
        if name.startswith('int_o_'):return 'int_'+label+'_'+name[len('int_o_'):]
        return name
    expected_names=[name for name in oldnames if name not in removed]+core_added
    expected_names += [renamed(name,label) for label,index in NEW_BLOCKS for name in source_aux]
    assert names==expected_names and len(set(names))==len(names)==979
    oldrows={row['name']:row for row in old['residuals']}
    newrows={row['name']:row for row in new['residuals']}
    sourcerows={row['name']:row for row in source['residuals']}
    removed_rows={name for name in oldrows if name=='jones1980.power_001.definition'
                  or name.startswith('jones1980.ceiling_power.')}
    assert len(removed_rows)==138
    for name in removed:
        occurrences={row['name'] for row in old['residuals']
                     if any(oldnames[i-1]==name for term in row['terms'] for i in term['monomial'])}
        assert occurrences and occurrences<=removed_rows|{'jones1980.B5.definition'}
    newexpressions={name:expr(row,names) for name,row in newrows.items()}
    z=lambda name:sp.Symbol(name)
    b,q,B5,c,s=z('b'),z('q'),z('B5'),z('c'),z('s')
    b4,A,C,D,M,AC=(z('power_'+name) for name in ('b4','A','C','D','modulus','AC'))
    delta,alpha=z('power_delta'),z('power_alpha')
    expected_power={
        'b4.definition':z('int_b_161')*b4-z('int_b_37')**2,
        'A.definition':2*A-b4*B5-8*B5-b+8-10*B5*s+10*s,
        'C.definition':C-5**60-delta*A+delta,
        'AC.definition':AC-A*C,
        'D.norm':D*D-AC*AC+C*C-1,
        'modulus.definition':M-2*b*A+b*b+1,
        'q.congruence':q-D+AC-b*C+alpha*M,
        'positive.q':2*q-2*B5-2-sum(z(f'power_positive_q_{i}')*(z(f'power_positive_q_{i}')+1) for i in (1,2,3)),
        'positive.bound':2*c*c-2*C*C-2-sum(z(f'power_positive_bound_{i}')*(z(f'power_positive_bound_{i}')+1) for i in (1,2,3))}
    for suffix,expected in expected_power.items():
        assert sp.expand(newexpressions['jones1980.pell_power.'+suffix]-expected)==0,suffix
    assert sp.expand(newexpressions['jones1980.B5.definition']-(B5-b*b4))==0
    new_weights=sum(z(f'int_{label}_{suffix}') for label,index in NEW_BLOCKS
                    for suffix in ('153','last_contact_weight'))
    cross_additions={
        'integer.i.balanced.detector1.poleInput.definition':-167281*z('int_i_reciprocal_73')*new_weights,
        'integer.i.shared.inverse1':z('int_i_reciprocal_158')*new_weights,
        'integer.i.shared.gate1':z('int_b_161')*new_weights}
    unchanged=0
    for name,row in oldrows.items():
        if name in removed_rows or name=='jones1980.B5.definition':continue
        expected=expr(row,oldnames)+cross_additions.get(name,0)
        assert sp.expand(newexpressions[name]-expected)==0,name
        unchanged += name not in CROSS

    private_source=[row for row in source['residuals'] if row['name'].startswith(PREFIXES)
                    and row['name'] not in ('integer.o.additive.detector0.contactSquare',
                                            'integer.o.additive.detector0.contactFourthPower')]
    assert len(private_source)==52
    t,u,f=z('int_b_2'),z('int_b_60'),z('int_b_61')
    spacing,v,w=(z('contact_common_'+suffix) for suffix in ('spacing','mixed_square','spacing_square'))
    fourth=[z(f'contact_common_fourth_coefficient_{i}') for i in range(1,5)]
    clone_names=[]
    for label,index in NEW_BLOCKS:
        replacement={z(name):z(renamed(name,label)) for name in sourcenames
                     if name=='o' or name.startswith('int_o_')}
        replacement.update({z('int_o_2'):t+index*spacing,
                            z('int_o_60'):u+2*index*v+index**2*w,
                            z('int_o_61'):f+sum(index**(j+1)*fourth[j] for j in range(4))})
        for row in private_source:
            prefix=next(prefix for prefix in PREFIXES if row['name'].startswith(prefix))
            name=prefix.replace('.o.','.'+label+'.')+row['name'][len(prefix):]
            clone_names.append(name)
            expected=sp.expand(expr(row,sourcenames).subs(replacement,simultaneous=True))
            uses={sourcenames[i-1] for term in row['terms'] for i in term['monomial']}
            if uses&{'int_o_2','int_o_60','int_o_61'}:
                active=sorted(expected.free_symbols,key=str)
                expected=sp.Poly(expected,*active,domain=sp.QQ).clear_denoms(convert=True)[1].primitive()[1].as_expr()
            assert sp.expand(newexpressions[name]-expected)==0,name
    expected_order=[name for name in oldrows if name not in removed_rows]
    expected_order += ['jones1980.pell_power.'+suffix for suffix in expected_power]
    expected_order += clone_names
    assert list(newrows)==expected_order
    assert (new['variables'],len(newrows))==(979,829)
    assert (certificate['variables'],certificate['quadratic_rows'])==(979,829)
    assert new['ordinary_integer_inputs']==old['ordinary_integer_inputs']+['power_delta','power_alpha']
    assert new['integer_blocks']==13 and new['global_contact_weights']==26
    assert new['pell_power_new_integer_inputs_certified'] is True
    assert new['outer_coordinates']==84 and new['outer_residuals']==56
    assert new['affine_contact_active_indices']==old['affine_contact_active_indices']+[12,13]
    assert new['pell_power_exponent']==str(5**60)
    assert new['pell_power_instance_range']=='x > 32*z; only a fixed finite initial segment is removed'
    assert new['source_universality_hypothesis'] is None
    assert new['source_coding_theorem_independently_reproved'] is False
    assert new['unconditional_undecidability_claim'] is False
    assert certificate['fixed_general_parameter_may_be_increased'] is True
    parameters=tuple(map(sp.Symbol,new['parameters']))
    support=set()
    for row in new['residuals']:
        for term in row['terms']:
            assert len(term['monomial'])<=2
            support.update(term['monomial'])
            coefficient=sp.sympify(term['coefficient'])
            assert coefficient.free_symbols<=set(parameters)
            assert sp.Poly(coefficient,*parameters,domain=sp.ZZ)
    assert support==set(range(1,new['variables']+1))
    return {'status':'PASS','variables':979,'quadratic_rows':829,
            'source_power_rows_checked':9,'private_certificate_rows_checked':104,
            'global_contact_sum_rows_checked':3,'new_weight_terms_checked':12,
            'unchanged_rows_checked':unchanged,'integer_blocks':13,'contact_weights':26,
            'independent_template':str(sourcepath.relative_to(ROOT)),
            'independent_template_sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),
            'table_sha256':certificate['table_sha256'],
            'scope':'Complete exact coefficient and support audit; the source theorem and thirteen-family arithmetic completeness are separate proofs.'}


if __name__=='__main__':
    print(json.dumps(verify(),sort_keys=True,indent=2))
