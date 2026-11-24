#!/usr/bin/env python3
"""Verify the scalar-point quartics and the precise scope of the new research.

This gate checks exact coefficients, physical maps, algebraic descent, finite
fixtures, source pins, and the current-record transition. Arithmetic existence
theorems and actual detector realization are not inferred from finite tests.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'computation/variable_reductions_v82'
PAPERS={
    'papers/quartic/scalar_point163_179_20261120_v82.tex',
    'papers/elliptic_divisibility/prepared_eds_divisibility_20261120_v82.tex',
    'papers/pole_parameters/genus_one_sound_criterion_20261120_v82.tex',
}
CONTRIBUTORS_HASH='7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'
GENUS_PAPER='papers/pole_parameters/genus_one_sound_criterion_20261120_v82.tex'


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def historical_genus_hash():
    """Authenticate the published initial review by exact reverse edits."""
    certificate=read(PACKAGE/'abc/revision_review.json')
    source=(ROOT/GENUS_PAPER).read_text()
    assert hashlib.sha256(source.encode()).hexdigest()==certificate['final_sha256']
    previous=len(source)
    for edit in certificate['reverse_edits']:
        start,end=edit['start'],edit['end']
        assert 0<=start<=end<=previous
        assert source[start:end]==edit['final_text']
        source=source[:start]+edit['initial_text']+source[end:]
        previous=start
    restored=hashlib.sha256(source.encode()).hexdigest()
    assert restored==certificate['initial_sha256']
    return restored


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    import sympy
    from importlib.metadata import version
    assert sympy.__version__=='1.14.0'
    assert version('passagemath-pari')=='10.8.14'

    manifest=read(PACKAGE/'manifest.json')
    assert set(manifest['papers'])==PAPERS
    actual={str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*')
            if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
    assert actual==set(manifest['files'])
    pins={PACKAGE/k:v for k,v in manifest['files'].items()}
    pins.update({ROOT/k:v for k,v in manifest['papers'].items()})
    for p,h in pins.items():
        assert sha(p)==h,str(p.relative_to(ROOT))
    review=read(PACKAGE/'manual_review.json')
    assert review['status']=='PASS under the stated arithmetic premises'
    original_genus_hash=historical_genus_hash()
    for name,h in review['reviewed_sha256'].items():
        current_hash=original_genus_hash if name==GENUS_PAPER else sha(ROOT/name)
        assert current_hash==h,name
    assert review['actual_rational_realization_proved'] is False
    assert review['non_author_mathematical_review_claimed'] is False
    followup=read(PACKAGE/'manual_review_followup.json')
    assert followup['status']=='PASS'
    assert followup['initial_review_sha256']==sha(PACKAGE/'manual_review.json')
    assert followup['actual_rational_realization_proved'] is False
    for name,h in followup['reviewed_sha256'].items():
        assert sha(ROOT/name)==h,name
    audit=read(PACKAGE/'abc/independent_review/manual_review.json')
    assert audit['status']=='PASS' and audit['reverse_edit_verified']
    assert audit['initial_reviewed_manuscript_sha256']==original_genus_hash
    assert audit['final_manuscript_sha256']==sha(ROOT/GENUS_PAPER)
    for name,h in audit['independent_review_files'].items():
        assert sha(PACKAGE/'abc/independent_review'/name)==h,name
    for name in ('check_genus_one.py','certificate.json','common_level_scope.md'):
        assert sha(PACKAGE/'abc'/name)==audit['package_source_pins'][name],name
    assert sha(PACKAGE/'abc/tex_review_followup.json')==audit['package_source_pins']['tex_review.json']

    previous=read(ROOT/'data/results_20261119_v81.json')
    current=read(ROOT/'data/results_20261120_v82.json')
    before={r['id']:r for r in previous['current_constructions']}
    after={r['id']:r for r in current['current_constructions']}
    assert set(after)==set(before)-{'quartic165','quartic180'}|{'quartic163','quartic179'}
    for key in set(before)-{'quartic165','quartic180'}:
        assert before[key]==after[key],'Unintended construction change: '+key
    assert current['historical_constructions']==previous['historical_constructions']+[before['quartic165'],before['quartic180']]
    assert current['source_attribution']==previous['source_attribution']
    assert current['number_field_results']==previous['number_field_results']
    assert current['related_paper_audit']==previous['related_paper_audit']
    assert current['arithmetic_foundations_complete_independent_audit'] is False
    assert current['targets_21_and_9_proved'] is current['targets_21_and_9_disproved'] is False
    assert current['unchanged_variable_counts']=={
        'general_polynomial':25,'explicit_polynomial':27,
        'ordinary_abc_unrestricted_degree':11,'ordinary_abc_quartic':56}
    for count,rows,terms in [(163,137,2789),(179,151,3036)]:
        r=after[f'quartic{count}']
        assert (r['variables'],r['degree'],r['quadratic_rows'],r['monomials'],r['integer_content'])==(count,4,rows,terms,1)
        assert r['retained_R_square'] is True
        assert r['additional_hypothesis'] is None
        assert r['parameter_effective']==(count==179)
        c=read(ROOT/r['certificate'])
        assert c['input']==1 and c['variables']==count
        assert c['quadrics']==rows and c['monomials']==terms
    assert after['quartic163']['exact_height']=='max(126616122944180358034867798936,149^(4N+2)) for every N>=1'
    c0=645904574641049503754777843805872291231896003979*14904184670611231**4
    assert int(after['quartic179']['exact_height'])==c0*c0
    assert after['quartic179']['height_bits']==(c0*c0).bit_length()==748
    research=current['new_research_results']
    assert research['prepared_elliptic_divisibility']['total_coordinates']==5
    assert research['prepared_elliptic_divisibility']['external_input_identified_with_quotient'] is False
    assert research['genus_one_criterion']['sound_total_coordinates']==10
    assert research['genus_one_criterion']['actual_input_rational_realization_proved'] is False
    assert research['genus_one_criterion']['counterexample_claimed_at_actual_detector'] is False
    progression=research['genus_one_criterion']['quadratic_progression_suffices']
    assert progression['one_fixed_source_constant_required'] is True
    assert progression['actual_realization_on_any_progression_proved'] is False
    assert all(r['defines_Z_in_Q'] is False for r in research.values())

    readme=(ROOT/'README.md').read_text()
    contributors=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    assert contributors and hashlib.sha256(contributors.group().encode()).hexdigest()==CONTRIBUTORS_HASH
    assert 'notes of Gabe Conant with Astra 6.2' in readme
    assert '[v82 records](data/results_20261120_v82.json)' in readme
    rows=[line for line in readme.split("## Fewest variables currently recorded for undecidability", 1)[0].splitlines() if '| Ordinary rational abc |' in line]
    assert len(rows)==2
    assert any('| **11** |' in row and '4, exact' not in row for row in rows)
    assert any('| **56** | **4, exact** |' in row for row in rows)
    assert '| **163** | **4, exact** |' in readme and '| **179** | **4, exact** |' in readme
    assert '$' not in readme and r'\(' not in readme and r'\[' not in readme

    builds=read(ROOT/'data/audits/tex_build_20261120_v82.json')
    assert {r['paper'] for r in builds['papers']}==PAPERS
    for row in builds['papers']:
        source_hash=original_genus_hash if row['paper']==GENUS_PAPER else sha(ROOT/row['paper'])
        assert source_hash==row['source_sha256']
        assert row['returncode']==row['overfull_boxes']==row['undefined_references']==0
        assert row['all_rendered_pages_reviewed'] and row['pages']>0
        assert len(row['page_sha256'])==row['pages']
    final_builds=read(ROOT/'data/audits/tex_build_20261120_v82_followup.json')
    assert {r['paper'] for r in final_builds['papers']}==PAPERS
    for row in final_builds['papers']:
        assert sha(ROOT/row['paper'])==row['source_sha256']
        assert row['returncode']==row['overfull_boxes']==row['undefined_references']==0
        assert row['all_rendered_pages_reviewed'] and row['pages']>0
        assert len(row['page_sha256'])==row['pages']
    final_genus=next(r for r in final_builds['papers'] if r['paper']==GENUS_PAPER)
    assert final_genus['pdf_sha256']==audit['package_source_pins']['genus_one_sound_criterion_20261120_v82.pdf']

    stages=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    def run(script,*arguments):
        result=subprocess.run([sys.executable,'-B',str(script),*map(str,arguments)],
            cwd=ROOT,env=env,capture_output=True,text=True)
        if result.returncode:
            raise RuntimeError(str(script)+'\n'+result.stdout[-10000:]+result.stderr[-10000:])
        label=str(script.relative_to(ROOT))
        stages.append({'script':label,'arguments':list(map(str,arguments)),'status':'PASS'})
        print(label+': PASS',flush=True)

    run(PACKAGE/'general/check.py')
    with tempfile.TemporaryDirectory(prefix='diophantine-v82-') as temporary:
        target=Path(temporary)
        run(PACKAGE/'general/build.py','--output',target)
        for count in (163,179):
            for name in ('quadrics.json','polynomial.json','maps.json','certificate.json'):
                p=Path(f'quartic{count}')/name
                assert (target/p).read_bytes()==(PACKAGE/'general'/p).read_bytes(),str(p)
    run(PACKAGE/'eds/check_eds_detector.py')
    run(PACKAGE/'eds/check_eds_detector.py','--pari')
    run(PACKAGE/'abc/check_genus_one.py')
    run(PACKAGE/'abc/check_independent.py')
    independent=read(PACKAGE/'general/independent.json')
    assert [r['variables'] for r in independent['checks']]==[163,179]
    for name,h in independent['published_dependencies_sha256'].items():
        assert sha(ROOT/name)==h,name
    for p,h in pins.items():
        assert sha(p)==h,'Verification modified '+str(p.relative_to(ROOT))
    report={
        'schema':'diophantine-exact-verification/v82','status':'PASS',
        'python':platform.python_version(),'sympy':sympy.__version__,
        'passagemath-pari':version('passagemath-pari'),'stages':stages,
        'current_quartic_counts':[163,179],'regenerated_json_byte_identical':True,
        'published_inputs_unchanged':True,'historical_review_hashes_preserved':True,
        'unchanged_variable_counts':current['unchanged_variable_counts'],
        'elliptic_divisibility_is_not_an_integer_definition':True,
        'actual_genus_one_realization_remains_unproved':True,
        'quadratic_progression_criterion_proved':True,
        'independent_Kummer_reconstruction_preserved':True,
        'initial_genus_source_authenticated_by_exact_reverse_edits':True,
        'tex_papers_reviewed':len(builds['papers']),
        'tex_pages_reviewed':sum(r['pages'] for r in builds['papers']),
        'scope':'Exact physical maps, expansions, algebraic descent, finite fixtures and review pins. '
            'Universal arithmetic arguments are in the manuscripts under their stated premises; '
            'neither actual detector realization nor an effective family threshold is inferred.'}
    output=json.dumps(report,indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(output)
    print(output)


if __name__=='__main__':
    main()
