#!/usr/bin/env python3
"""Check intrinsic transfers, trace criteria, cubic rank and prepared obstructions."""
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
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'
PACKAGES = (
    'computation/pole_parameters/intrinsic_source_transfers_v57',
    'computation/pole_parameters/variable_squareclasses_v57',
    'negative_results/computation/intrinsic_specializations_v57',
    'negative_results/computation/prepared_sha_v57',
    'computation/pole_parameters/trace_conic_v57',
    'computation/pole_parameters/cubic_trace_rank_v57',
)
PAPERS = (
    'papers/pole_parameters/general_intrinsic_transfer_20261117_v57.tex',
    'papers/pole_parameters/conditional_intrinsic_transfer_20261117_v57.tex',
    'papers/pole_parameters/variable_squareclasses_20261117_v57.tex',
    'negative_results/papers/pole_parameters/intrinsic_specializations_20261117_v57.tex',
    'negative_results/papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex',
    'papers/pole_parameters/trace_conic_criterion_20261117_v57.tex',
    'papers/pole_parameters/cubic_trace_rank_20261117_v57.tex',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    hashes, certificates = {}, {}
    with tempfile.TemporaryDirectory(prefix='diophantine-v57-') as temporary:
        jobs = [(p, 'check.py', 'certificate.json') for p in PACKAGES]
        jobs.append((PACKAGES[3], 'independent_check.py', 'independent_certificate.json'))
        jobs.append((PACKAGES[5], 'independent_check.py', 'independent_certificate.json'))
        for i, (relative, script, certificate) in enumerate(jobs):
            package = ROOT/relative
            generated = Path(temporary)/f'certificate-{i}.json'
            result = subprocess.run([sys.executable, '-B', str(package/script),
                                     '--output', str(generated)], cwd=ROOT,
                                    capture_output=True, text=True)
            if result.returncode:
                raise ValueError(result.stdout+result.stderr)
            original = package/certificate
            if original.read_bytes() != generated.read_bytes():
                raise ValueError(f'Certificate differs: {relative}/{certificate}')
            hashes[str((package/script).relative_to(ROOT))] = digest(package/script)
            certificates[str(original.relative_to(ROOT))] = digest(generated)

    scalar, classes, specialization, sha, conic, rank = [
        json.loads((ROOT/p/'certificate.json').read_text()) for p in PACKAGES]
    assert scalar['coordinate_count'] == 25
    assert scalar['physical_weight_change'] is False
    assert scalar['intrinsic_pole_input'] == 'd=b'
    assert scalar['denominator_coprimality']['integer_fixture_full_gcd'] == 1
    assert not scalar['new_smaller_variable_bound']
    assert classes['conditional_retained_coordinates'] == 9
    assert classes['optional_menu_of_forms'] == [
        '1', '(X^2+B)^2+Trace(x(A))^2', '1+X^4']
    assert [x['height_argument_total_degree'] for x in classes['single_cover_rows']] == [224,384,1536]
    assert not classes['actual_uniform_rational_realization_proved']
    assert not classes['new_nine_variable_defining_bound']
    assert not classes['general_21_variable_transfer_proved']
    assert specialization['prepared_counterexample'] == '112/169'
    assert sha['prepared_d'] == '112/225'
    assert sha['global_pairing'] == -1 and sha['rank'] == 1
    assert sha['abscissa_image'] == [-791,-1,1,791]
    assert sha['excluded_abscissa_class'] == -7
    independent = json.loads((ROOT/PACKAGES[3]/'independent_certificate.json').read_text())
    assert independent['status'] == 'PASS'
    assert independent['pure_selmer_dimension'] == 3
    assert independent['pairing_local_113']['hilbert_symbol'] == -1
    assert independent['abscissa_squareclass_image'] == sha['abscissa_image']
    assert conic['radicand'] == 'V^2+w(2-V)'
    assert conic['admissible_trace_class'] == '1+3(V-1)^2'
    assert conic['linear_trace_class']['product_total_degree'] == 3
    assert conic['linear_trace_class']['product_monomials'] == 5
    assert conic['linear_trace_class']['product_coefficient_height'] == 47
    assert [x['total_coordinates'] for x in conic['census_conditional_on_actual_rational_realization']] == [21,9]
    assert not conic['rational_realization_proved']
    assert not conic['new_complete_defining_count_proved']
    assert conic['adaptive_class']['new_free_coordinates'] == 0
    assert conic['adaptive_class']['bad_pole_fixtures_including_negative_auxiliary_valuations'] == 3264
    assert not conic['adaptive_class']['lost_contact_primes']
    assert not conic['adaptive_class']['actual_global_realization_proved']
    assert rank['status'] == 'PASS'
    assert rank['non_torsion_for_all_rational_0_lt_w_le_1_over4']
    assert rank['all_rational_torsion_candidates'] == ['-96/49','100/49','296/49']
    assert len(rank['projective_no_root_certificates']) == 11
    assert not rank['actual_detector_trace_matching_proved']
    rank_independent = json.loads((ROOT/PACKAGES[5]/'independent_certificate.json').read_text())
    assert rank_independent['status'] == 'PASS'
    assert [x['n'] for x in rank_independent['group_law_checks']] == [8,10,12]
    assert [x['x_denominator_degree'] for x in rank_independent['group_law_checks']] == [30,48,70]
    division_data = ROOT/PACKAGES[5]/'division_data.json'
    assert rank_independent['certificate_sha256'] == digest(division_data)
    hashes[str(division_data.relative_to(ROOT))] = digest(division_data)

    current = json.loads((ROOT/'data/results_20261117_v57.json').read_text())
    previous = json.loads((ROOT/'data/results_20261117_v56.json').read_text())
    assert current['current_constructions'] == previous['current_constructions']
    assert not current['new_variable_reduction']
    assert not current['variable_squareclass_realization']['proved']
    assert not current['native_square_realization']['proved']
    assert not current['single_cover_realization']['proved']
    assert not current['trace_conic_realization']['proved']
    assert all(not t['new_variable_bound'] for t in current['new_auxiliary_theorems'])
    assert current['verification_script'] == 'scripts/verify_v57.py'
    readme = (ROOT/'README.md').read_text()
    match = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert match and hashlib.sha256(match.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    for relative in PAPERS:
        hashes[relative] = digest(ROOT/relative)
    report = {
        'schema':'diophantine-exact-verification/v57', 'status':'PASS',
        'python':platform.python_version(),
        'certificate_sha256':certificates, 'source_sha256':hashes,
        'current_records':'data/results_20261117_v57.json',
        'construction_records_unchanged_from':'data/results_20261117_v56.json',
        'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'established_general_counts':[25,13], 'abc_quartic_variables':71,
        'intrinsic_source_transfer_counts':[25,13],
        'conditional_variable_squareclass_target':9,
        'trace_conic_targets':[21,9],
        'trace_classes_without_height_loss':['1','1+24V','1+3(V-1)^2'],
        'adaptive_trace_class_without_new_coordinates':True,
        'positive_rank_for_all_rational_normalized_weights':True,
        'cubic_rank_direct_group_law_independent_check':True,
        'single_cover_height_argument_degrees':[224,384,1536],
        'prepared_cover_obstruction':{'input':'112/225','local_solubility':True,
                                      'rational_point':False,'independent_exact_check':True},
        'actual_uniform_rational_realization_proved':False,
        'new_defining_variable_count':False,
        'new_full_defining_degree_or_coefficient_bound':False,
        'external_arithmetic_foundation_audited':False,
        'scope':('Exact scalar residues, height inequalities, specialization identities, '
                 'adaptive-class identities, cubic torsion certificates with an independent '
                 'group-law audit, and two independent Cassels-pairing data checks. Universal proofs '
                 'and cited descent theory are stated in the manuscripts. No global '
                 'rational realization or 21/9 defining bound is certified.'),
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
