#!/usr/bin/env python3
"""Rebuild physical pole obstructions and check the realization checkpoint."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    'computation/pole_parameters/general21_alignment_v75',
    'negative_results/computation/pole_parameters/raw_abscissa_v75',
    'negative_results/computation/pole_parameters/odd_coset_raw_v76',
    'negative_results/computation/pole_parameters/native_pole_ramification_v75',
    'negative_results/computation/pole_parameters/adaptive_prepared_pairs_v76',
]
PAPERS = [
    ('papers/pole_parameters/contact_alignment_20261117_v76.tex',
     'data/audits/tex_contact_alignment_20261117_v76.json'),
    ('negative_results/papers/pole_parameters/raw_abscissa_preparation_20261117_v75.tex',
     'data/audits/tex_raw_abscissa_20261117_v76.json'),
    ('negative_results/papers/pole_parameters/odd_coset_raw_20261117_v76.tex',
     'data/audits/tex_odd_coset_raw_20261117_v76.json'),
    ('negative_results/papers/pole_parameters/native_pole_ramification_20261117_v75.tex',
     'data/audits/tex_native_pole_ramification_20261117_v75.json'),
    ('negative_results/papers/pole_parameters/adaptive_prepared_pairs_20261117_v76.tex',
     'data/audits/tex_adaptive_prepared_pairs_20261117_v76.json'),
]


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding_path(folder, name):
    if name.startswith(('negative_results/', 'computation/', 'papers/', 'data/')):
        return ROOT/name
    return folder/name


def run(work, script):
    start = time.monotonic()
    process = subprocess.run([sys.executable, '-B', str(work/script)], cwd=work,
                             capture_output=True, text=True)
    if process.returncode:
        raise RuntimeError(script+'\n'+(process.stdout+process.stderr)[-12000:])
    print(script+': PASS', flush=True)
    return {'script': script, 'status': 'PASS',
            'seconds': round(time.monotonic()-start, 3)}


def verify(report_path=None):
    original = {}
    for package in PACKAGES:
        folder = ROOT/package
        manifest = read(folder/'manifest.json')
        bindings = manifest.get('files', manifest.get('sha256', {}))
        assert bindings, package
        for name, checksum in bindings.items():
            assert digest(binding_path(folder, name)) == checksum, (package, name)
        if 'external_reviewed_paper' in manifest:
            binding = manifest['external_reviewed_paper']
            assert digest(ROOT/binding['path']) == binding['sha256']
        for name, binding in manifest.get('external_files', {}).items():
            assert digest(ROOT/name) == binding, name
        for name, binding in manifest.get('bindings', {}).items():
            assert digest(ROOT/name) == binding, name
        review = read(folder/'independent_review.json')
        assert review['status'].startswith('PASS'), package
        bindings = review.get('reviewed_file_sha256', review.get('sha256', {}))
        for name, checksum in bindings.items():
            assert digest(binding_path(folder, name)) == checksum, name
        if 'certificate_sha256' in review:
            assert digest(folder/'certificate.json') == review['certificate_sha256']
        for path in folder.rglob('*.json'):
            original[str(path.relative_to(ROOT))] = path.read_bytes()

    stages = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v76-') as temporary:
        work = Path(temporary)
        shutil.copytree(ROOT/'computation', work/'computation',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        shutil.copytree(ROOT/'data', work/'data')
        for package in PACKAGES[1:]:
            shutil.copytree(ROOT/package, work/package,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for package in PACKAGES:
            stages.append(run(work, package+'/check.py'))
            stages.append(run(work, package+'/check_independent.py'))
            if package.endswith('raw_abscissa_v75'):
                stages.append(run(work, package+'/check_division.py'))
        for name, contents in original.items():
            assert (work/name).read_bytes() == contents, name

    alignment, raw, odd, native, adaptive = [read(ROOT/p/'certificate.json') for p in PACKAGES]
    assert all(record['status'] == 'PASS' for record in [alignment, raw, odd, native, adaptive])
    assert not alignment['general21_completeness_claimed']
    assert not alignment['actual_elliptic_witness_claimed']
    assert raw['p'] == 76777 and raw['v_physical_u'] == -1
    assert [r['b_valuation'] for r in raw['candidate_raw_factors']] == [-1, -5]
    assert [r['actual_trace_radicand_valuation'] for r in raw['candidate_raw_factors']] == [1, 1]
    division = read(ROOT/PACKAGES[1]/'division_certificate.json')
    assert division['literal_abscissa_valuations'] == [2, 2]
    assert division['modulus'] == 76777**3
    assert odd['prime'] == 85817 and odd['valuation_u'] == -1
    assert odd['valuation_V'] == 6 and odd['valuation_b'] == -11
    assert odd['valuation_trace_square_radicand'] == 1
    assert odd['V_over_p6_mod_p'] == 33198
    fixture = native['physical_norm_counterexample']
    assert fixture['prime'] == 100003 and fixture['valuations']['b'] == -7
    assert fixture['all_pre_pole_whole_character_guards']
    assert fixture['native_pre_pole_guards']['guard_nonzero_evaluations'] == 1920
    assert fixture['balanced_denominators_checked_positive'] == 768
    assert native['fixed_point_contact_counts'] == [10, 14, 18]
    assert native['minimum_genus_for_degree_two'] == [4, 6, 8]
    assert adaptive['prime_certificate']['prime'] == 100003
    assert len(adaptive['fixtures']) == 2
    for fixture in adaptive['fixtures']:
        assert fixture['preparation']['intrinsic_pole_prepared']
        assert fixture['preparation']['square_reduced_denominator']
    independent = read(ROOT/PACKAGES[4]/'independent_certificate.json')
    assert independent['fresh_prime_valuations_second_fixture'] == {
        'u': 0, 'w': -4, 'V': 0, 'C': -1, 'b': -4, '2-V': 3}
    assert not independent['producer_imported'] and not independent['cas_used']

    rendered = []
    for paper, receipt in PAPERS:
        entry = next(e for e in read(ROOT/receipt)['papers'] if e['paper'] == paper)
        assert entry['source_sha256'] == digest(ROOT/paper), paper
        assert entry['returncode'] == 0 and entry['warnings'] == [], paper
        assert entry['all_rendered_pages_reviewed'] and entry['pages'] > 0
        rendered.append({'paper': paper, 'pages': entry['pages'],
                         'source_sha256': entry['source_sha256']})

    criteria = read(ROOT/'data/criteria_20261117_v76.json')
    previous = read(ROOT/'data/criteria_20261117_v75.json')
    for name in previous:
        if name != 'schema':
            assert criteria[name] == previous[name], name
    assert criteria['schema'] == 'diophantine-research-criteria/v76'
    assert not criteria['targets_21_and_9_proved']
    assert not criteria['new_obstructions']['global_realization_disproved']
    assert criteria['new_obstructions']['odd_coset']['pole_valuation'] == -11
    assert criteria['new_obstructions']['native_cover']['contact_counts'] == [10, 14, 18]
    results = read(ROOT/'data/results_20261117_v75.json')
    current = {r['id']: r for r in results['current_constructions']}
    assert current['general25']['variables'] == 25
    assert current['ordinary_abc11']['variables'] == 11
    for path in [p+'/README.md' for p in PACKAGES]+['docs/results_20261117_v76.md']:
        text = (ROOT/path).read_text()
        assert '$' not in text and r'\operatorname' not in text, path
    report = {'schema': 'diophantine-exact-verification/v76', 'status': 'PASS',
              'python': platform.python_version(), 'stages': stages,
              'rebuilt_json_files_compared': len(original), 'packages': len(PACKAGES),
              'rendered_manuscripts': rendered,
              'physical_raw_pole_valuations': [-1, -5],
              'physical_odd_coset_pole_valuation': -11,
              'physical_native_norm_pole_valuation': -7,
              'prepared_abstract_adaptive_counterexamples': 2,
              'native_degree_two_cover_genus_bounds': [4, 6, 8],
              'new_defining_variable_count': False,
              'global_21_or_9_realization_proved': False,
              'global_21_or_9_realization_disproved': False,
              'arithmetic_foundations_complete_independent_audit': False}
    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    verify(parser.parse_args().report)
