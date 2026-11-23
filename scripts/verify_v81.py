#!/usr/bin/env python3
"""Verify paired contacts, amplified field descent and their exact scope.

The gate checks finite algebra and immutable review pins. It does not prove
abc, the retained arithmetic theorems, or an effective defining parameter.
All producer regeneration takes place in an isolated temporary tree.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT/'computation/variable_reductions_v81'
FIELD = ROOT/'computation/number_fields/pasten_vidaux_v81'
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'
QUARTIC_PAPER = 'papers/quartic_existence/paired_contact56_20261119_v81.tex'
FIELD_PAPERS = {
    'papers/number_fields/amplified_rationality_descent_20261119_v81.tex',
    'papers/number_fields/ten_coordinate_rationality_20261119_v81.tex',
}


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest(package, papers):
    manifest=read(package/'manifest.json')
    assert set(manifest['papers'])==papers
    actual={str(p.relative_to(package)) for p in package.rglob('*')
            if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
    assert actual==set(manifest['files']), 'Incomplete package manifest: '+str(package)
    pins={package/name:value for name,value in manifest['files'].items()}
    pins.update({ROOT/name:value for name,value in manifest['papers'].items()})
    for path,expected in pins.items():
        assert digest(path)==expected, str(path.relative_to(ROOT))
    return pins


def check_manual(path):
    manual=read(path)
    assert manual['status'].lower().startswith('pass')
    pins=manual.get('reviewed_sha256',manual.get('sha256'))
    assert pins
    for name,expected in pins.items():
        assert digest(ROOT/name)==expected, 'Reviewed source changed: '+name


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    import sympy
    assert sympy.__version__=='1.14.0'
    pins=check_manifest(PACKAGE,{QUARTIC_PAPER})
    pins.update(check_manifest(FIELD,FIELD_PAPERS))

    previous=read(ROOT/'data/results_20261119_v80.json')
    current=read(ROOT/'data/results_20261119_v81.json')
    before={r['id']:r for r in previous['current_constructions']}
    after={r['id']:r for r in current['current_constructions']}
    assert set(after)==set(before)-{'ordinary_abc_quartic58'}|{'ordinary_abc_quartic56'}
    for key in set(before)-{'ordinary_abc_quartic58'}:
        assert after[key]==before[key], 'Unintended record change: '+key
    assert current['historical_constructions']==previous['historical_constructions']+[before['ordinary_abc_quartic58']]
    assert current['source_attribution']==previous['source_attribution']
    assert current['source_attribution']['name']=='Gabe Conant'
    assert current['source_attribution']['collaborating_model']=='Astra 6.2'
    assert current['arithmetic_foundations_complete_independent_audit'] is False
    assert current['targets_21_and_9_proved'] is False
    assert current['targets_21_and_9_disproved'] is False
    assert current['unchanged_variable_counts']=={
        'general_polynomial':25,'general_quartic':165,'explicit_quartic':180,
        'ordinary_abc_unrestricted_degree':11}
    record=after['ordinary_abc_quartic56']
    assert (record['variables'],record['degree'],record['quadratic_rows'],
            record['monomials'],record['parameter_separated_terms'],
            record['integer_content'])==(56,4,46,809,812,1)
    assert record['exact_height']=='B^2+377888002299'
    assert record['parameter_effective'] is False
    assert record['additional_hypothesis']=='ordinary rational abc'
    assert record['stronger_beta_one_twist_premise_required'] is False
    assert record['pole_completeness_source']==(
        'Burungale, arXiv:2611.16130v1, Theorem B; beta congruent to 7 modulo 8')

    field_records={r['id']:r for r in current['number_field_results']}
    assert set(field_records)=={'rationality_selector16','rationality_selector10'}
    for count in (16,10):
        row=field_records[f'rationality_selector{count}']
        assert row['variables']==count and row['defined_set']=='Q'
        assert row['ambient_field']=='K, a number field'
        assert row['coefficients']=='integers' and row['effective'] is False
        assert row['composition_retains_original_Z_over_Q_arithmetic_inputs'] is True
        assert row['Z_in_K_variables_from_N_variable_Q_definition']==f'{count}*N'
        assert row['O_K_variables_from_N_variable_Q_definition']==f'{count}*[K:Q]*N'
        assert row['proof'] in FIELD_PAPERS
        assert len(row['hypotheses'])>=3
    assert current['related_paper_audit']['does_not_reduce_Z_over_Q_variable_counts'] is True

    readme=(ROOT/'README.md').read_text()
    contributors=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    assert contributors and hashlib.sha256(contributors.group().encode()).hexdigest()==CONTRIBUTORS_HASH
    assert 'notes of Gabe Conant with Astra 6.2' in readme
    rows=[line for line in readme.splitlines() if '| Ordinary rational abc |' in line]
    assert len(rows)==2
    current_link=re.search(r'\[results JSON\]\((data/results_[^)]*\.json)\)',readme)
    assert current_link
    latest=read(ROOT/current_link.group(1))
    latest_quartic=next(r for r in latest['current_constructions']
                        if r['id'].startswith('ordinary_abc_quartic'))
    latest_few=next(r for r in latest['current_constructions']
                    if re.fullmatch(r'ordinary_abc\d+',r['id']))
    assert latest_quartic['degree']==4 and latest_quartic['variables']<=56
    assert latest_few['variables']<=11
    assert any(f"| **{latest_quartic['variables']}** | **4, exact** |" in line for line in rows)
    assert any(f"| **{latest_few['variables']}** |" in line and '4, exact' not in line for line in rows)
    assert '$' not in readme and r'\(' not in readme and r'\[' not in readme

    check_manual(PACKAGE/'abc/manual_review56.json')
    check_manual(FIELD/'manual_review.json')
    check_manual(FIELD/'compression_manual_review.json')
    # Neither historical proofs nor original review hashes are regenerated.
    check_manual(ROOT/'computation/variable_reductions_v80/abc/manual_review58.json')
    check_manual(ROOT/'computation/variable_reductions_v79/abc/manual_review59.json')

    builds=read(ROOT/'data/audits/tex_build_20261119_v81.json')
    assert {r['paper'] for r in builds['papers']}=={QUARTIC_PAPER}|FIELD_PAPERS
    for row in builds['papers']:
        assert digest(ROOT/row['paper'])==row['source_sha256']
        assert row['returncode']==row['overfull_boxes']==row['undefined_references']==0
        assert row['all_rendered_pages_reviewed'] and row['pages']>0
        assert len(row['page_sha256'])==row['pages']

    stages=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')

    def run(script,cwd=ROOT):
        result=subprocess.run([sys.executable,'-B',str(script)],cwd=cwd,env=env,
                              capture_output=True,text=True)
        if result.returncode:
            raise RuntimeError(str(script)+'\n'+result.stdout[-12000:]+result.stderr[-12000:])
        stages.append({'script':str(script.relative_to(cwd)),'status':'PASS'})
        print(stages[-1]['script']+': PASS',flush=True)

    with tempfile.TemporaryDirectory(prefix='diophantine-v81-') as temporary:
        destination=Path(temporary)
        builder=Path('computation/variable_reductions_v81/abc/build56.py')
        parent=Path(read(PACKAGE/'abc/quartic56/maps.json')['parent'])
        for relative in (builder,parent):
            target=destination/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/relative,target)
        run(destination/builder,destination)
        for name in ('quadrics.json','polynomial.json','maps.json','certificate.json'):
            relative=Path('computation/variable_reductions_v81/abc/quartic56')/name
            assert (destination/relative).read_bytes()==(ROOT/relative).read_bytes(),name

    run(PACKAGE/'abc/check56.py')
    run(PACKAGE/'general/check.py')
    run(FIELD/'independent_check.py')
    run(FIELD/'compression_check.py')
    independent=read(PACKAGE/'abc/independent56.json')
    assert independent['status']=='PASS' and independent['variables']==56
    assert independent['retained_parent_rows']==32 and independent['contact_coordinates']==9
    assert independent['coordinate_monomials']==809
    assert independent['height_and_regression']['strict_margin']=='92221/99700'
    assert independent['two_adic_exact_checks']['finite_checks_are_not_uniform_proof'] is True
    for name,expected in independent['input_sha256'].items():
        assert digest(ROOT/name)==expected,name
    for path,expected in pins.items():
        assert digest(path)==expected,'Verification modified '+str(path.relative_to(ROOT))

    report={
        'schema':'diophantine-exact-verification/v81','status':'PASS',
        'python':platform.python_version(),'sympy':sympy.__version__,'stages':stages,
        'published_inputs_unchanged':True,'regenerated_json_byte_identical':True,
        'manual_review_source_hashes_preserved':True,'historical_review_hashes_preserved':True,
        'quartic':{'variables':56,'degree':4,'quadrics':46,'coordinate_monomials':809,
                   'content':1,'exact_height':record['exact_height'],
                   'sufficient_defining_parameter_effective':False},
        'number_field_rationality_counts':[16,10],
        'number_field_counts_are_not_Z_over_Q_records':True,
        'unchanged_variable_counts':current['unchanged_variable_counts'],
        'tex_papers_reviewed':len(builds['papers']),
        'tex_pages_reviewed':sum(r['pages'] for r in builds['papers']),
        'scope':'Exact coefficients, physical maps, finite algebra and immutable proof-review pins. '
                'The universal arguments are proved in the manuscripts under their stated '
                'arithmetic inputs; this finite gate proves neither those inputs nor effectiveness.'}
    output=json.dumps(report,indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(output)
    print(output)


if __name__=='__main__':
    main()
