#!/usr/bin/env python3
"""Verify uniform complement guards and the reference normalizer checkpoint."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('computation/pole_parameters/uniform_complement_guard_v77')
PAPER = Path('papers/pole_parameters/uniform_complement_guard_20261117_v77.tex')
RECEIPT = Path('data/audits/tex_uniform_complement_guard_20261117_v77.json')


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(report_path=None):
    folder = ROOT/PACKAGE
    manifest = read(folder/'manifest.json')
    for name, checksum in manifest['files'].items():
        assert digest(folder/name) == checksum, name
    for name, checksum in manifest['external_files'].items():
        assert digest(ROOT/name) == checksum, name
    review = read(folder/'independent_review.json')
    assert review['status'].startswith('PASS')
    for name, checksum in review['reviewed_file_sha256'].items():
        path = ROOT/name if name.startswith(('papers/', 'computation/')) else folder/name
        assert digest(path) == checksum, name

    original = {name: (folder/name).read_bytes() for name in
                ['certificate.json', 'independent_certificate.json']}
    stages = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v77-') as temporary:
        work = Path(temporary)
        shutil.copytree(folder, work/PACKAGE,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        sources = read(folder/'certificate.json')['source_bindings']
        for binding in sources.values():
            relative = binding['source']
            assert digest(ROOT/relative) == binding['source_sha256']
            (work/relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/relative, work/relative)
        for script in ['check.py', 'check_independent.py']:
            process = subprocess.run([sys.executable, '-B', str(work/PACKAGE/script)],
                                     cwd=work, capture_output=True, text=True)
            if process.returncode:
                raise RuntimeError(script+'\n'+process.stdout+process.stderr)
            stages.append({'script': str(PACKAGE/script), 'status': 'PASS'})
        for name, contents in original.items():
            assert (work/PACKAGE/name).read_bytes() == contents, name

    producer = read(folder/'certificate.json')
    independent = read(folder/'independent_certificate.json')
    assert producer['status'] == independent['status'] == 'PASS'
    assert independent['producer_imported'] is False
    assert independent['cas_used'] is False
    assert independent['native_polynomial_identity_verified']
    assert independent['positive_integer_margin'] == 1108398992054805009292439980
    assert independent['sound_source_variables'] == 9
    assert independent['aligned_normalizer']['reference_square_identity_verified']
    assert independent['global_complement_square_realization_proved'] is False
    assert producer['nine_variable_completeness_proved'] is False

    receipt = next(entry for entry in read(ROOT/RECEIPT)['papers']
                   if entry['paper'] == str(PAPER))
    assert receipt['source_sha256'] == digest(ROOT/PAPER)
    assert receipt['returncode'] == 0 and receipt['warnings'] == []
    assert receipt['all_rendered_pages_reviewed'] and receipt['pages'] > 0

    criteria = read(ROOT/'data/criteria_20261117_v77.json')
    previous = read(ROOT/'data/criteria_20261117_v76.json')
    assert criteria['schema'] == 'diophantine-research-criteria/v77'
    for name, value in previous.items():
        if name != 'schema':
            assert criteria[name] == value, name
    assert criteria['targets_21_and_9_proved'] is False
    latest = criteria['uniform_complement_guard']
    assert latest['all_character_complement_units_proved']
    assert latest['aligned_normalizer_complete_eleven_source_transfer_proved']
    assert latest['selected_actual_square_realization_proved'] is False
    assert latest['new_complete_variable_bound_proved'] is False
    current = {row['id']: row for row in read(ROOT/'data/results_20261117_v75.json')['current_constructions']}
    assert current['general25']['variables'] == 25
    assert current['ordinary_abc11']['variables'] == 11

    result = {
        'schema': 'diophantine-exact-verification/v77', 'status': 'PASS',
        'stages': stages, 'rebuilt_json_files_compared': len(original),
        'paper': str(PAPER), 'source_sha256': digest(ROOT/PAPER),
        'rendered_pages_reviewed': receipt['pages'],
        'uniform_full_auxiliary_complement_guard_proved': True,
        'reference_aligned_eleven_source_transfer_proved': True,
        'new_complete_variable_bound_proved': False,
        'global_21_or_9_realization_proved': False,
        'global_21_or_9_realization_disproved': False,
        'new_coefficient_source_compiled': False,
        'arithmetic_foundations_complete_independent_audit': False,
    }
    if report_path:
        Path(report_path).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    main(parser.parse_args().report)
