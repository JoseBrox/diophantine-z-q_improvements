#!/usr/bin/env python3
"""Rebuild the even-valuation sources and exact actual-weight certificates."""
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
import time

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    'computation/few_variables/seven_contact11_v74',
    'computation/few_variables/even_valuation11_v75',
    'computation/few_variables/even_valuation25_v75',
    'computation/pole_parameters/general21_recovery_v74',
    'computation/pole_parameters/halfpoint_trace_v74',
    'computation/pole_parameters/even_halfpoint_trace_v75',
]
PAPERS = [
    ('papers/conditional_few_variables/seven_contact_detector_20261117_v74.tex',
     'data/audits/tex_seven_contact_20261117_v74.json'),
    ('papers/conditional_few_variables/even_valuation_detector_20261117_v75.tex',
     'data/audits/tex_even_valuation_20261117_v75.json'),
    ('papers/few_variables25/even_valuation25_20261117_v75.tex',
     'data/audits/tex_even_valuation25_20261117_v75.json'),
    ('papers/pole_parameters/coupled_weight_lifting_20261117_v74.tex',
     'data/audits/tex_coupled_weight_20261117_v74.json'),
]
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root, path, *arguments):
    start = time.monotonic()
    process = subprocess.run([sys.executable, '-B', str(root/path), *map(str, arguments)],
                             cwd=root, capture_output=True, text=True)
    if process.returncode:
        raise RuntimeError(path + '\n' + (process.stdout + process.stderr)[-12000:])
    print(path + ': PASS', flush=True)
    return {'script': path, 'arguments': list(map(str, arguments)),
            'status': 'PASS', 'seconds': round(time.monotonic()-start, 3)}


def verify(report_path=None):
    for name in PACKAGES:
        folder = ROOT/name
        manifest = read(folder/'manifest.json')
        bindings = manifest.get('sha256', manifest.get('files', manifest))
        base = ROOT if 'sha256' in manifest else folder
        for filename, checksum in bindings.items():
            assert digest(base/filename) == checksum, (name, filename)
        if 'external_reviewed_paper' in manifest:
            binding = manifest['external_reviewed_paper']
            assert digest(ROOT/binding['path']) == binding['sha256']
    for name in PACKAGES[:3]:
        review = read(ROOT/name/'independent_review.json')
        assert review['status'].startswith('PASS')
        bindings = review.get('reviewed_file_sha256', review.get('sha256', {}))
        assert bindings, name
        for filename, checksum in bindings.items():
            assert digest(ROOT/filename) == checksum, filename

    # Work in an isolated tree: several independent checkers deliberately
    # overwrite their own exact certificate, so no published input is touched.
    original = {}
    for name in PACKAGES:
        for path in (ROOT/name).rglob('*.json'):
            original[str(path.relative_to(ROOT))] = path.read_bytes()
    stages = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v75-') as temporary:
        work = Path(temporary)
        shutil.copytree(ROOT/'computation', work/'computation',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        shutil.copytree(ROOT/'data', work/'data')
        seven, even, general, coupled, half, half_even = PACKAGES
        for package, arguments in [
                (seven, []), (even, []), (even, ['--contacts', '7']),
                (general, ['--L', '3'])]:
            stages.append(run(work, package+'/build_source.py', *arguments))
            check_arguments = (['--specification', work/package/'seven_contact']
                               if arguments == ['--contacts', '7'] else [])
            stages.append(run(work, package+'/check.py', *check_arguments))
        for package in PACKAGES[:3]:
            stages.append(run(work, package+'/independent_math_check.py'))
        for package in [coupled, half, half_even]:
            stages.append(run(work, package+'/check.py'))
            stages.append(run(work, package+'/check_independent.py'))
        stages.append(run(work, half_even+'/check.py', '--contacts', '9'))
        stages.append(run(work, half_even+'/check_independent.py', '--contacts', '9'))
        for name, contents in original.items():
            assert (work/name).read_bytes() == contents, name

    seven = read(ROOT/PACKAGES[0]/'specification/independent_certificate.json')
    even = read(ROOT/PACKAGES[1]/'specification/independent_certificate.json')
    even_seven = read(ROOT/PACKAGES[1]/'seven_contact/independent_certificate.json')
    general = read(ROOT/PACKAGES[2]/'specification/independent_certificate.json')
    for record, degree in [(seven, 357309057), (even, 230932097),
                           (even_seven, 356146817)]:
        assert record['status'] == 'PASS'
        assert record['bounds']['degree_bound'] == degree
        assert record['characters'] == 384
        assert record['corruption_controls_rejected'] == 2
        assert not record['nine_coordinate_completeness_claimed']
    assert general['status'] == 'PASS' and general['variables'] == 25
    assert general['degree_bound'] == 4863007848923136
    assert general['native_character_evaluations'] == 72
    assert general['corruption_controls_rejected'] == 2
    assert not general['general21_realization_claimed']
    for folder, degree, nodes, guards in [
            (PACKAGES[1]+'/specification', 230932097, 1865, 32),
            (PACKAGES[2]+'/specification', 4863007848923136, 6039, 101)]:
        constructed = read(ROOT/folder/'construction.json')
        assert constructed['bounds']['degree_bound'] == degree
        assert constructed['nodes'] == nodes and constructed['guards'] == guards

    half = read(ROOT/PACKAGES[4]/'certificate.json')
    even_half = read(ROOT/PACKAGES[5]/'certificate.json')
    nine_half = read(ROOT/PACKAGES[5]/'nine_contact_certificate.json')
    genera = {'weight': 12, 'squared_slope': 90,
              'twisted_squared_slope': 91, 'slope': 181}
    assert half['genera'] == even_half['genera'] == genera
    assert nine_half['genera'] == {'weight': 12, 'squared_slope': 116,
                                  'twisted_squared_slope': 117, 'slope': 233}
    for record in [half, even_half, nine_half]:
        assert record['status'] == 'PASS'
        assert not record['rational_witness_proved']
        assert not record['nine_coordinate_completeness_claimed']
        assert not record['fixed_shift_is_defining_threshold']
    coupled = read(ROOT/PACKAGES[3]/'certificate.json')
    assert coupled['status'] == 'PASS' and not coupled['general21_realization_claimed']
    assert not coupled['fixtures_are_prepared_elliptic_witnesses']
    assert coupled['mismatched_pair_rejected']['gcd_degree'] == 0
    assert coupled['direct_normalized_pair_lift']['gcd_degree'] == 1
    assert coupled['direct_normalized_mismatched_pair_rejected']['gcd_degree'] == 0

    records = read(ROOT/'data/results_20261117_v75.json')
    previous = read(ROOT/'data/results_20261117_v74.json')
    current = {r['id']: r for r in records['current_constructions']}
    old = {r['id']: r for r in previous['current_constructions']}
    for name, row in current.items():
        if name not in ('general25', 'ordinary_abc11'):
            assert row == old[name], name
    for name, history, degree, count in [
            ('general25', 'general25_v72', 4863007848923136, 25),
            ('ordinary_abc11', 'ordinary_abc11_v71', 230932097, 11)]:
        row = current[name]
        assert row['variables'] == count and int(row['degree_upper_bound']) == degree
        assert degree < int(old[name]['degree_upper_bound'])
        assert records['superseded_constructions'][history] == old[name]
        assert row['integer_content'] == 1 and not row['parameter_effective']
    assert records['superseded_constructions']['quartic194'] == previous['superseded_constructions']['quartic194']
    for key in ('new_variable_reduction', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established',
                'arithmetic_foundations_complete_independent_audit'):
        assert records[key] is False, key
    criteria = read(ROOT/'data/criteria_20261117_v75.json')
    assert not criteria['targets_21_and_9_proved']
    assert not criteria['general21']['complete_definition_proved']
    assert not criteria['ordinary_abc9']['complete_definition_proved']
    assert criteria['ordinary_abc9']['height_absorption_margin'] == '38695561/597203000'
    assert not criteria['interrupted_mod53_lift_obstruction']['obstruction_reproduced']

    rendered = []
    for paper, receipt in PAPERS:
        entries = read(ROOT/receipt)['papers']
        record = next(r for r in entries if r['paper'] == paper)
        assert record['source_sha256'] == digest(ROOT/paper)
        assert record['returncode'] == 0 and record['warnings'] == []
        assert record['pages'] > 0 and record['all_rendered_pages_reviewed']
        rendered.append({'paper': paper, 'source_sha256': record['source_sha256'],
                         'pages': record['pages']})
    readme = (ROOT/'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    historical_guide = (ROOT/'docs/results_20261117_v75.md').read_text()
    for value in ('4,863,007,848,923,136', '230,932,097', '**193-variable quartic**',
                  'data/results_20261117_v75.json'):
        assert value in historical_guide, value
    assert 'docs/results_20261117_v75.md' in readme
    assert re.search(r'\[historical results JSON\]\((data/results_20261117_v75\.json)\)', readme)
    for path in ['README.md', 'docs/results_20261117_v75.md'] + [p+'/README.md' for p in PACKAGES]:
        contents = (ROOT/path).read_text()
        assert '$' not in contents and r'\operatorname' not in contents, path
    report = {'schema': 'diophantine-exact-verification/v75', 'status': 'PASS',
              'python': platform.python_version(), 'stages': stages,
              'rebuilt_json_files_compared': len(original),
              'complete_constructions': [
                  {'variables': 25, 'degree_upper_bound': 4863007848923136,
                   'native_characters_checked': 72},
                  {'variables': 11, 'degree_upper_bound': 230932097,
                   'native_characters_checked': 384}],
              'complete_seven_contact_degree_upper_bounds': [357309057, 356146817],
              'actual_halfpoint_weight_genus': 12,
              'actual_physical_slope_genera': {'seven_contacts': 181, 'nine_contacts': 233},
              'coupled_normalized_weight_lifting_verified': True,
              'rendered_manuscripts': rendered,
              'complete_integer_families_under_retained_premises': True,
              'sufficient_defining_parameters_effective': False,
              'global_21_or_9_realization_proved': False,
              'arithmetic_foundations_complete_independent_audit': False}
    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    verify(parser.parse_args().report)
