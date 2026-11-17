#!/usr/bin/env python3
"""Verify elliptic index arithmetic and the separate quotient-height obstructions."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'
JOBS = (
    ('computation/elliptic_divisibility/primitive_denominators_v60','check.py','certificate.json'),
    ('computation/elliptic_divisibility/index_poles_v60','check.py','certificate.json'),
    ('computation/elliptic_heights/quotient_height_v60','check.py','certificate.json'),
    ('negative_results/computation/denominator_support_v60','check.py','certificate.json'),
    ('negative_results/computation/denominator_support_v60','check_carrier.py','carrier_certificate.json'),
)
PAPERS = (
    'papers/elliptic_divisibility/simple_primitive_denominators_20261117_v60.tex',
    'papers/elliptic_divisibility/elliptic_index_poles_20261117_v60.tex',
    'papers/elliptic_heights/pole_cancelling_quotient_height_20261117_v60.tex',
    'negative_results/papers/pole_parameters/square_rescaled_weight_perturbation_20261117_v60.tex',
    'negative_results/papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    results, hashes, certificates = [], {}, {}
    with tempfile.TemporaryDirectory(prefix='diophantine-v60-') as temporary:
        for index,(relative,script,certificate) in enumerate(JOBS):
            generated = Path(temporary)/f'{index}.json'
            package = ROOT/relative
            run = subprocess.run([sys.executable,'-B',str(package/script),'--output',str(generated)],
                                 cwd=ROOT,capture_output=True,text=True)
            if run.returncode:
                raise ValueError(run.stdout+run.stderr)
            if generated.read_bytes() != (package/certificate).read_bytes():
                raise ValueError(f'Regenerated certificate differs: {relative}/{certificate}')
            result = json.loads(generated.read_text())
            assert result['status']=='PASS'
            results.append(result)
            hashes[f'{relative}/{script}'] = digest(package/script)
            certificates[f'{relative}/{certificate}'] = digest(generated)
    primitive,index,height,support,carrier = results
    assert primitive['reduction_order_checks']==1992
    assert primitive['good_primes_checked']==166
    assert primitive['strict_gap']=='311/44100'
    assert len(primitive['coprime_index_examples'])==7
    assert primitive['coprime_index_examples'][-1]['kappa']=='1999/1000'
    assert index['valuation_fixtures']==19744
    assert index['formal_series_terms_verified']==13
    assert index['uniform_initial_two_adic_depth']==4
    assert index['free_coordinates_added']==0
    assert not index['external_input_equality_proved']
    assert not index['growth_condition_existentially_encoded']
    assert not index['new_defining_variable_bound_claimed']
    assert height['generic_group_law_cases']==32
    assert height['rational_height_fixtures']==252
    assert support['local_support_valuation_cases']==1326
    assert support['alpha_delta']=='187845767/200600400'
    assert support['three_alpha_delta_minus_one']=='120978967/66866800'
    assert not support['all_two_point_sources_excluded']
    assert not support['new_defining_variable_bound_claimed']
    assert carrier['counts']=={'nonconstant_verified':1404,'constant_specialization':16,'denominator_guard':12}
    assert carrier['parameter_height_fixtures']==96

    current=json.loads((ROOT/'data/results_20261117_v60.json').read_text())
    previous=json.loads((ROOT/'data/results_20261117_v59.json').read_text())
    assert current['current_constructions']==previous['current_constructions']
    assert not current['new_variable_reduction']
    assert current['current_ordinary_abc_variables']==11
    assert current['verification_script']=='scripts/verify_v60.py'
    assert current['execution_record']=='data/audits/integration_20261117_v60.json'
    assert not current['native_square_realization']['proved']
    assert not current['trace_conic_realization']['proved']
    assert not current['new_eleven_source']['actual_nine_variable_realization_proved']
    assert not current['arithmetic_foundations_complete_independent_audit']
    route=current['elliptic_index_route']
    assert route['index_divisibility_complete'] and route['formal_log_amplification_proved']
    assert not route['external_input_equality_proved']
    assert not route['growth_condition_existentially_encoded']
    assert route['quotient_height_derivative_application_obstructed']
    assert route['fixed_rational_carrier_extension_proved']
    assert not route['new_defining_variable_bound']
    catalog=json.loads((ROOT/'negative_results/data/results.json').read_text())
    records={r['id']:r for r in catalog['theorems']}
    for record in current['new_negative_results']:
        assert records[record['id']]==record
        assert record['proof'].startswith('negative_results/')
        assert not record['all_nine_variable_sources_excluded']

    readme=(ROOT/'README.md').read_text()
    match=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    assert match and hashlib.sha256(match.group().encode()).hexdigest()==CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    current_link=re.search(r'\[results JSON\]\((data/results_\d{8}_v\d+\.json)\)',readme)
    assert current_link and (ROOT/current_link.group(1)).is_file()
    # The historical construction remains certified after README advances.
    assert any(row['id']=='ordinary_abc11' and row['variables']==11 and
               row['degree_upper_bound']=='5444199553'
               for row in current['current_constructions'])
    builds=json.loads((ROOT/'data/audits/tex_build_20261117_v60.json').read_text())
    assert [row['paper'] for row in builds['papers']]==list(PAPERS)
    for row in builds['papers']:
        assert row['returncode']==0 and row['warnings']==[]
        assert row['all_rendered_pages_reviewed']
        assert row['source_sha256']==digest(ROOT/row['paper'])
        hashes[row['paper']]=row['source_sha256']
    assert primitive['manuscript_sha256']==hashes[PAPERS[0]]
    assert height['manuscript_sha256']==hashes[PAPERS[2]]
    assert support['manuscript_sha256']==hashes[PAPERS[4]]
    assert carrier['lemma_sha256']==carrier['architecture_sha256']==hashes[PAPERS[4]]
    report={
        'schema':'diophantine-exact-verification/v60','status':'PASS',
        'python':platform.python_version(),'source_sha256':hashes,
        'certificate_sha256':certificates,
        'current_records':'data/results_20261117_v60.json',
        'retained_records':'data/results_20261117_v59.json',
        'current_construction_counts_unchanged':True,
        'new_defining_variable_bound':False,
        'primitive_reduction_order_checks':1992,
        'amplified_valuation_fixtures':19744,
        'quotient_formal_coefficients':32,'quotient_rational_height_fixtures':252,
        'support_valuation_fixtures':1326,'carrier_cases':carrier['counts'],
        'carrier_parameter_height_fixtures':96,
        'external_input_equality_proved':False,
        'quotient_height_derivative_application_obstructed':True,
        'all_nine_variable_constructions_excluded':False,
        'targets_21_and_9_proved':False,
        'external_arithmetic_foundation_independently_audited':False,
        'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'scope':'Exact arithmetic, formal identities, finite isogeny identities and specified valuation/height fixtures. The infinite prime, completeness and finiteness statements are the manuscript proofs under their stated hypotheses, not conclusions from these computations.',
    }
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    main(parser.parse_args().report)
