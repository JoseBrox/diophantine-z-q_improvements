#!/usr/bin/env python3
"""Verify the explicit 229-variable quartic and separate coupling obstruction."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
PACKAGE='computation/quartic/explicit229_v62'
NEGATIVE='negative_results/computation/six_contact_mobius_v62'
PAPERS=[
    'papers/quartic/quartic229_20261117_v62.tex',
    'papers/effective_sums/effective_torsion_sums_20261117_v62.tex',
    'negative_results/papers/pole_parameters/six_contact_mobius_obstruction_20261117_v62.tex',
]
CONTRIBUTORS_HASH='bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script,*arguments):
    result=subprocess.run([sys.executable,'-B',str(script),*map(str,arguments)],
                          cwd=ROOT,capture_output=True,text=True)
    if result.returncode:
        raise ValueError(result.stdout+result.stderr)
    return result.stdout


def main(output):
    with tempfile.TemporaryDirectory(prefix='diophantine-v62-') as temporary:
        temp=Path(temporary)
        target=temp/'quartic229'
        shutil.copytree(ROOT/PACKAGE,target,ignore=shutil.ignore_patterns('__pycache__'))
        for script in ['build.py','check.py','build_literal.py','check_literal.py']:
            run(target/script)
        run(target/'check_arithmetic.py','--output',target/'arithmetic_certificate.json')
        artifacts=['quadratic.json','polynomial.json','graft.json','contact-change.json',
                   'certificate.json','quartic229-N15.txt','literal_certificate.json',
                   'arithmetic_certificate.json']
        for name in artifacts:
            assert (target/name).read_bytes()==(ROOT/PACKAGE/name).read_bytes(),name
        algebra=json.loads((target/'certificate.json').read_text())
        arithmetic=json.loads((target/'arithmetic_certificate.json').read_text())
        literal=json.loads((target/'literal_certificate.json').read_text())
        negative={}
        for script,name in [('check.py','certificate.json'),
                            ('check_independent.py','independent_certificate.json')]:
            destination=temp/name
            run(ROOT/NEGATIVE/script,'--output',destination)
            assert destination.read_bytes()==(ROOT/NEGATIVE/name).read_bytes()
            negative[name]=json.loads(destination.read_text())

    for certificate in [algebra,arithmetic,literal,*negative.values()]:
        assert certificate['status']=='PASS'
    assert (algebra['variables'],algebra['rows'],algebra['degree'],
            algebra['content'],algebra['coordinate_monomials'])==(229,207,4,1,3312)
    assert algebra['literal_unit_guards']==[26,38,180]
    assert algebra['unchanged_parent_rows']==168
    assert algebra['cloned_coordinates']==34 and algebra['cloned_rows']==31
    assert algebra['all_twelve_contact_rows_verified']
    assert algebra['reflection_center']=='3/11'
    assert algebra['coefficient_crossover_N']==8
    assert arithmetic['sufficient_N']==15 and arithmetic['forced_scalar_exponent_L']==66
    assert arithmetic['all_larger_N'] and arithmetic['scalar_completeness_sufficient_N']==3
    assert len(arithmetic['exceptional_primes'])==14
    assert not arithmetic['arithmetic_foundations_independently_audited']
    assert not arithmetic['targets_21_and_9_proved']
    assert literal['terms']==3312 and literal['variables_including_input']==229
    assert literal['coefficient_height_bits']==232
    assert literal['literal_integer_coefficients'] and literal['family_parameter_absent_from_expression']

    primary=negative['certificate.json']; independent=negative['independent_certificate.json']
    assert primary['source_sha256']==independent['source_sha256']==digest(ROOT/PAPERS[2])
    p_maps={(tuple(row['matrix']),str(row['multiplier'])) for row in primary['mobius_group']['automorphisms']}
    i_maps={(tuple(row['matrix']),str(row['multiplier'])) for row in independent['automorphisms']}
    assert p_maps==i_maps and len(p_maps)==12
    assert independent['ordered_image_triples']==120
    assert independent['uniform_square_gap_cases']==20
    assert {x['progression_modulus'] for x in independent['integer_numerator_fixtures']}=={11629040018}

    current=json.loads((ROOT/'data/results_20261117_v62.json').read_text())
    previous=json.loads((ROOT/'data/results_20261117_v61.json').read_text())
    now={row['id']:row for row in current['current_constructions']}
    then={row['id']:row for row in previous['current_constructions']}
    added=now.pop('explicit_quartic229');removed=then.pop('explicit_quartic257')
    assert now==then and removed['variables']==257
    assert added['variables']==229 and added['quadratic_rows']==207 and added['monomials']==3312
    assert added['parameter']=={'N':15} and added['coefficient_height']=='149^32'
    assert added['largest_coefficient_bits']==232 and added['sufficient_all_larger_N']
    assert current['new_variable_reduction'] and current['new_coefficient_improvement']
    for key in ['native_square_realization','trace_conic_realization']:
        assert not current[key]['proved']
    assert not current['new_eleven_source']['actual_nine_variable_realization_proved']
    assert not current['number_fields']['all_number_fields_theorem_established']
    assert not current['upstream_audit']['requested_version_located']
    assert current['upstream_audit']['audited_version']==19
    assert not current['arithmetic_foundations_complete_independent_audit']
    catalog={x['id']:x for x in json.loads((ROOT/'negative_results/data/results.json').read_text())['theorems']}
    assert current['new_negative_results']==[catalog['six_contact_mobius_obstruction']]
    assert not catalog['six_contact_mobius_obstruction']['all_nine_variable_sources_excluded']

    readme=(ROOT/'README.md').read_text()
    section=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest()==CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    # Historical records remain available after the public table advances.
    assert (ROOT/'data/results_20261117_v62.json').is_file()
    assert (ROOT/'docs/results_20261117_v62.md').is_file()
    assert '**229**' in readme

    builds=json.loads((ROOT/'data/audits/tex_build_20261117_v62.json').read_text())
    assert {row['paper'] for row in builds['papers']}==set(PAPERS)
    for row in builds['papers']:
        assert row['returncode']==0 and row['warnings']==[]
        assert row['source_sha256']==digest(ROOT/row['paper'])
        assert row['all_rendered_pages_reviewed']

    report={'schema':'diophantine-exact-verification/v62','status':'PASS',
            'python':platform.python_version(),
            'current_records':'data/results_20261117_v62.json',
            'retained_records':'data/results_20261117_v61.json',
            'source_sha256':{path:digest(ROOT/path) for path in PAPERS},
            'reproduced_artifact_sha256':{name:digest(ROOT/PACKAGE/name) for name in artifacts},
            'new_explicit_quartic':{'variables':229,'quadratic_rows':207,'degree':4,
                'content':1,'monomials':3312,'sufficient_N':15,'coefficient_height':'149^32',
                'coefficient_bits':232,'literal_expression_verified':True},
            'negative_symmetry_count':12,'independent_square_gap_cases':20,
            'general_counts_unchanged':True,'targets_21_and_9_proved':False,
            'arithmetic_foundations_independently_audited':False,
            'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH}
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    main(parser.parse_args().report)
