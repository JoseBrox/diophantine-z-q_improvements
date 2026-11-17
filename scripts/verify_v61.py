#!/usr/bin/env python3
"""Verify rational pole levels, the input-only counterexample and records."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
PAPER='negative_results/papers/pole_parameters/input_only_weight_false_witnesses_20261117_v61.tex'
PACKAGE='negative_results/computation/input_only_weight_v61'
LEVEL_PAPER='papers/pole_parameters/varying_level_pole_fibers_20261117_v61.tex'
LEVEL_PACKAGE='computation/pole_parameters/varying_levels_v61'
CONTRIBUTORS_HASH='bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    with tempfile.TemporaryDirectory(prefix='diophantine-v61-') as temporary:
        certificate=Path(temporary)/'certificate.json'
        run=subprocess.run([sys.executable,'-B',str(ROOT/PACKAGE/'check.py'),
                            '--output',str(certificate)],cwd=ROOT,capture_output=True,text=True)
        if run.returncode:
            raise ValueError(run.stdout+run.stderr)
        assert certificate.read_bytes()==(ROOT/PACKAGE/'certificate.json').read_bytes()
        result=json.loads(certificate.read_text())
        level_results={}
        for script,name in [('check.py','certificate.json'),
                            ('check_independent.py','independent_certificate.json')]:
            target=Path(temporary)/name
            run=subprocess.run([sys.executable,'-B',str(ROOT/LEVEL_PACKAGE/script),
                                '--output',str(target)],cwd=ROOT,capture_output=True,text=True)
            if run.returncode:
                raise ValueError(run.stdout+run.stderr)
            assert target.read_bytes()==(ROOT/LEVEL_PACKAGE/name).read_bytes()
            level_results[script]=json.loads(target.read_text())
    assert result['status']=='PASS'
    assert result['source_sha256']==digest(ROOT/PAPER)
    expected={'fixed_residue_cases':56,'rational_denominator_cases':45,
              'compatible_index_progression_cases':768,'fixed_depth_inequality_cases':1056,
              'negative_odd_weight_cases':1274,'finite_local_index_bijections':20,
              'local_residues_checked':2515,'local_isometry_checks':7545}
    for key,value in expected.items():
        assert result[key]==value
    assert not result['global_rational_witnesses_computed']
    assert result['global_claim_depends_on_manuscript_proof_and_intrinsic_theorem']
    assert not result['all_two_point_sources_excluded']
    assert not result['new_defining_variable_bound_claimed']
    for level in level_results.values():
        assert level['status']=='PASS'
        assert level['source_sha256']==digest(ROOT/LEVEL_PAPER)
    symbolic=level_results['check.py']
    independent=level_results['check_independent.py']
    assert symbolic['cleared_pole']=={'degree':9,'coefficient_height':4,'monomials':12}
    assert symbolic['local_even_valuation_cases']==625
    assert symbolic['numerical_count_claim'] is None
    assert symbolic['nontrivial_complement_benchmark']['d']=='112/225'
    level_checks={'even_valuation_unit_ratio_cases':1008,
                  'positive_odd_valuation_cases':1050,
                  'smooth_genus_one_reduction_fixtures':2048,
                  'negative_odd_pole_cases':656,
                  'exact_prepared_rational_fibers':4,
                  'exact_rational_witness_pairs':16}
    for key,value in level_checks.items():
        assert independent[key]==value
    assert not independent['arbitrary_prescribed_r_realized']
    assert not independent['new_variable_bound_claimed']
    assert independent['infinite_fiber_claim_verified_by_mathematical_audit_not_finite_search']
    current=json.loads((ROOT/'data/results_20261117_v61.json').read_text())
    previous=json.loads((ROOT/'data/results_20261117_v60.json').read_text())
    assert current['current_constructions']==previous['current_constructions']
    assert not current['new_variable_reduction']
    assert current['verification_script']=='scripts/verify_v61.py'
    assert current['execution_record']=='data/audits/integration_20261117_v61.json'
    assert not current['native_square_realization']['proved']
    assert not current['trace_conic_realization']['proved']
    assert not current['new_eleven_source']['actual_nine_variable_realization_proved']
    assert current['elliptic_index_route']['specified_input_only_height_helper_obstructed']
    assert len(current['new_auxiliary_theorems'])==1
    positive=current['new_auxiliary_theorems'][0]
    assert positive['proof']==LEVEL_PAPER and positive['data']==LEVEL_PACKAGE
    assert positive['every_prepared_input_every_rational_level_locally_soluble']
    assert positive['infinitely_many_rationally_soluble_levels_per_prepared_input']
    assert positive['infinitely_many_rational_points_per_selected_level']
    assert positive['whole_character_guard_avoidance']
    assert positive['retained_free_coordinates']==2
    assert not positive['actual_prescribed_detector_level_realization_proved']
    assert not positive['simultaneous_actual_detector_realization_proved']
    assert not positive['new_defining_variable_count']
    records={x['id']:x for x in json.loads((ROOT/'negative_results/data/results.json').read_text())['theorems']}
    assert current['new_negative_results']==[records['input_only_weight_false_witnesses']]
    assert records['input_only_weight_false_witnesses']['proof']==PAPER
    assert not records['input_only_weight_false_witnesses']['all_nine_variable_sources_excluded']
    readme=(ROOT/'README.md').read_text()
    section=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest()==CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    # Historical releases retain their records after README advances.
    assert (ROOT/'data/results_20261117_v61.json').is_file()
    assert (ROOT/'docs/results_20261117_v61.md').is_file()
    builds=json.loads((ROOT/'data/audits/tex_build_20261117_v61.json').read_text())
    assert {build['paper'] for build in builds['papers']}=={PAPER,LEVEL_PAPER}
    for build in builds['papers']:
        assert build['source_sha256']==digest(ROOT/build['paper'])
        assert build['returncode']==0 and build['warnings']==[]
        assert build['all_rendered_pages_reviewed']
    report={'schema':'diophantine-exact-verification/v61','status':'PASS',
            'python':platform.python_version(),
            'source_sha256':{path:digest(ROOT/path) for path in [PAPER,PACKAGE+'/check.py',
                LEVEL_PAPER,LEVEL_PACKAGE+'/check.py',LEVEL_PACKAGE+'/check_independent.py']},
            'certificate_sha256':{path:digest(ROOT/path) for path in [PACKAGE+'/certificate.json',
                LEVEL_PACKAGE+'/certificate.json',LEVEL_PACKAGE+'/independent_certificate.json']},
            'current_records':'data/results_20261117_v61.json',
            'retained_records':'data/results_20261117_v60.json',
            'finite_exact_checks':expected,
            'independent_varying_level_checks':level_checks,
            'varying_level_symbolic_valuation_cases':625,
            'infinitely_many_rationally_soluble_levels':'Proved under the retained simultaneous-twist theorem; not inferred from enumeration.',
            'prescribed_detector_levels_realized':False,
            'current_construction_counts_unchanged':True,
            'new_defining_variable_bound':False,'targets_21_and_9_proved':False,
            'input_only_false_witnesses_numerically_computed':False,
            'global_false_witness_existence':'Manuscript theorem using local interpolation, CRT and the retained intrinsic-pole realization input.',
            'all_nine_variable_sources_excluded':False,
            'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH}
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    main(parser.parse_args().report)
