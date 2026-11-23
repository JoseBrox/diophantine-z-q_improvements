#!/usr/bin/env python3
"""Attach two ordinary general integer blocks to the proved power core.

The input blocks use progression indices12 and13. Their four weights enter
the same global contact sum as the eleven retained blocks, giving26 weights.
The general defining coefficient is chosen sufficiently large for this fixed
thirteen-block family; no effective numerical threshold is asserted.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import hashlib
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
NEW_BLOCKS = [('power_delta',12), ('power_alpha',13)]
PREFIXES = ('integer.o.', 'global.o.', 'scalar_norm.o.', 'detector_trace.o.')
GRADES = {'contact_common_spacing':1, 'contact_common_mixed_square':1,
          'contact_common_spacing_square':2,
          **{f'contact_common_fourth_coefficient_{i}':i for i in range(1,5)}}
CROSS_ROWS = {'integer.i.balanced.detector1.poleInput.definition',
              'integer.i.shared.inverse1', 'integer.i.shared.gate1'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rename(name,label):
    if name == 'o':
        return label
    if name.startswith('int_o_'):
        return 'int_'+label+'_'+name[len('int_o_'):]
    return name


def rename_row(name,label):
    for prefix in PREFIXES:
        if name.startswith(prefix):
            return prefix.replace('.o.','.'+label+'.')+name[len(prefix):]
    raise ValueError(name)


def build():
    predecessor = ROOT/'undecidability/pell_halftrace_v96/halftrace_m163_quadrics.json'
    template_path = ROOT/'undecidability/general_contact_v94/signed_affine_contact_m163_quadrics.json'
    old = json.loads(predecessor.read_bytes())
    template = json.loads(template_path.read_bytes())
    spec = importlib.util.spec_from_file_location('pell_power_core', HERE/'build_power_core.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    core = module.build_core(old)
    assert all(label in core['variable_names'] for label,index in NEW_BLOCKS)
    tnames = template['variable_names']
    auxiliary = [name for name in tnames if name.startswith('int_o_')]
    source_rows = [row for row in template['residuals'] if row['name'].startswith(PREFIXES)]
    assert len(auxiliary) == 60 and len(source_rows) == 52
    assert template['affine_contact_blocks'].index('o') == 9
    newnames = core['variable_names'] + [rename(name,label) for label,index in NEW_BLOCKS for name in auxiliary]
    assert len(set(newnames)) == len(newnames)
    ids = {name:i+1 for i,name in enumerate(newnames)}
    rows = []
    added_cross_terms = {}
    for row in core['residuals']:
        terms = [{'coefficient':term['coefficient'],
                  'monomial':sorted(ids[core['variable_names'][j-1]] for j in term['monomial'])}
                 for term in row['terms']]
        if row['name'] in CROSS_ROWS:
            prototypes = []
            for term in row['terms']:
                factors = [core['variable_names'][j-1] for j in term['monomial']]
                for weight in ('int_j_153','int_j_last_contact_weight'):
                    if weight in factors:
                        assert factors.count(weight) == 1
                        prototypes.append((term['coefficient'],factors,weight))
            assert len(prototypes) == 2
            additions=[]
            for label,index in NEW_BLOCKS:
                for coefficient,factors,weight in prototypes:
                    target_weight=weight.replace('int_j_','int_'+label+'_',1)
                    newfactors=[target_weight if name==weight else name for name in factors]
                    terms.append({'coefficient':coefficient,'monomial':sorted(ids[name] for name in newfactors)})
                    additions.append({'coefficient':coefficient,'monomial_names':newfactors})
            added_cross_terms[row['name']]=additions
        rows.append({'name':row['name'],'terms':terms})
    clone_multipliers = {}
    for label,index in NEW_BLOCKS:
        ratio=Fraction(index,9)
        for row in source_rows:
            changed=any(tnames[j-1] in GRADES for term in row['terms'] for j in term['monomial'])
            name=rename_row(row['name'],label)
            if not changed:
                terms=[{'coefficient':term['coefficient'],
                        'monomial':sorted(ids[rename(tnames[j-1],label)] for j in term['monomial'])}
                       for term in row['terms']]
            else:
                accum=defaultdict(Fraction)
                for term in row['terms']:
                    factors=[tnames[j-1] for j in term['monomial']]
                    grade=sum(GRADES.get(factor,0) for factor in factors)
                    coefficient=Fraction(term['coefficient'])*ratio**grade
                    monomial=tuple(sorted(ids[rename(factor,label)] for factor in factors))
                    accum[monomial]+=coefficient
                accum={monomial:coefficient for monomial,coefficient in accum.items() if coefficient}
                denominator=lcm(*(value.denominator for value in accum.values()))
                integer={monomial:int(value*denominator) for monomial,value in accum.items()}
                content=gcd(*integer.values())
                clone_multipliers[name]=str(Fraction(denominator,content))
                terms=[{'coefficient':str(coefficient//content),'monomial':list(monomial)}
                       for monomial,coefficient in sorted(integer.items())]
            rows.append({'name':name,'terms':terms})
    new=dict(core)
    new.update(variables=len(newnames),variable_names=newnames,residuals=rows,
               integer_blocks=13,global_contact_weights=26)
    new['affine_contact_blocks']=old['affine_contact_blocks']+[label for label,index in NEW_BLOCKS]
    new['affine_contact_active_indices']=old['affine_contact_active_indices']+[index for label,index in NEW_BLOCKS]
    new['power_general_contact_indices']={label:index for label,index in NEW_BLOCKS}
    new['power_general_core_inputs_certified']=[label for label,index in NEW_BLOCKS]
    new['pell_power_new_integer_inputs_certified']=True
    new['power_general_arithmetic_proof']='undecidability/pell_power_v97/thirteen_general_blocks.tex'
    new['power_general_predecessor']=str(predecessor.relative_to(ROOT))
    new['power_general_predecessor_sha256']=sha(predecessor)
    new['power_general_template']=str(template_path.relative_to(ROOT))
    new['power_general_template_sha256']=sha(template_path)
    new['power_general_added_cross_terms']=added_cross_terms
    new['power_general_clone_multipliers']=clone_multipliers
    new['power_general_parameter_scope']='C_parameter=149^N with one sufficiently large fixed N for this thirteen-block family; the prior eleven-block threshold is not asserted unchanged'
    new['power_general_projection_scope']='Same undecidable coding instance set on the retained cofinite tail, via the proved Pell power core and thirteen general integer certificates'
    for label,index in NEW_BLOCKS:
        new['global_contact_sum_elimination'] += ' - int_'+label+'_153 - int_'+label+'_last_contact_weight'
    assert (new['variables'],len(rows)) == (979,829)
    assert max(len(term['monomial']) for row in rows for term in row['terms']) == 2
    assert {i for row in rows for term in row['terms'] for i in term['monomial']} == set(ids.values())
    certificate={
        'variables':new['variables'],'quadratic_rows':len(rows),'degree':4,
        'integer_blocks':13,'global_contact_weights':26,
        'predecessor':str(predecessor.relative_to(ROOT)),'predecessor_sha256':sha(predecessor),
        'template':str(template_path.relative_to(ROOT)),'template_sha256':sha(template_path),
        'new_integer_inputs':[label for label,index in NEW_BLOCKS],
        'new_auxiliary_coordinates':120,'new_certificate_rows':104,
        'new_contact_indices':dict(NEW_BLOCKS),
        'changed_global_sum_rows':sorted(added_cross_terms),
        'added_global_sum_terms':added_cross_terms,
        'outer_coordinates':new['outer_coordinates'],'outer_quadratic_rows':new['outer_residuals'],
        'unconditional_undecidability_claim':False,
        'retained_arithmetic_interfaces':True,
        'source_coding_theorem_independently_reproved':False,
        'fixed_general_parameter_may_be_increased':True,
        'source_proof':'undecidability/pell_power_v97/pell_power_replacement.tex',
        'interface_proof':new['power_general_arithmetic_proof']}
    return new,certificate


if __name__=='__main__':
    table,certificate=build()
    target=HERE/'power_general_m163_quadrics.json'
    target.write_text(json.dumps(table,sort_keys=True,separators=(',',':'))+'\n')
    certificate['table_sha256']=sha(target)
    target.with_name('power_general_m163_certificate.json').write_text(json.dumps(certificate,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'variables':table['variables'],'rows':len(table['residuals']),
                      'sha256':certificate['table_sha256']}))
