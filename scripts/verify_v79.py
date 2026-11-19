#!/usr/bin/env python3
"""Rebuild the 59-variable abc quartic and verify the v79 exact audits.

Published inputs remain unchanged. The arithmetic proof and its retained
premises are separate from the finite assertions checked by this gate.
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
PACKAGE = ROOT / 'computation/variable_reductions_v79'
PAPERS = {
    'papers/quartic_existence/single_derivative59_20261119_v79.tex',
    'papers/quartic/hyperbolic_parity_20261119_v79.tex',
}
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    import sympy
    assert sympy.__version__ == '1.14.0'

    manifest = read(PACKAGE / 'manifest.json')
    pins = {PACKAGE / name: expected for name, expected in manifest['files'].items()}
    pins.update({ROOT / name: expected for name, expected in manifest['papers'].items()})
    assert set(manifest['papers']) == PAPERS
    for path, expected in pins.items():
        assert digest(path) == expected, str(path.relative_to(ROOT))

    previous = read(ROOT / 'data/results_20261119_v78.json')
    current = read(ROOT / 'data/results_20261119_v79.json')
    before = {row['id']: row for row in previous['current_constructions']}
    after = {row['id']: row for row in current['current_constructions']}
    assert set(after) == set(before) - {'ordinary_abc_quartic62'} | {'ordinary_abc_quartic59'}
    for name in set(before) - {'ordinary_abc_quartic62'}:
        assert after[name] == before[name], 'Unintended change to ' + name
    assert current['historical_constructions'] == [before['ordinary_abc_quartic62']]
    record = after['ordinary_abc_quartic59']
    claim = read(ROOT / record['certificate'])
    assert (record['variables'], record['degree'], record['quadratic_rows'],
            record['monomials'], record['parameter_separated_terms'],
            record['integer_content']) == (59, 4, 51, 873, 876, 1)
    assert record['exact_height'] == 'max(22838305425411,B^2+4092)'
    assert record['parameter_effective'] is False
    assert record['additional_hypothesis'] == 'ordinary rational abc'
    assert current['arithmetic_foundations_complete_independent_audit'] is False
    assert current['targets_21_and_9_proved'] is False
    assert current['targets_21_and_9_disproved'] is False
    assert current['source_attribution']['name'] == 'Gabe Conant'
    assert current['source_attribution']['collaborating_model'] == 'Astra 6.2'
    assert current['unchanged_variable_counts'] == {
        'general_polynomial': 25, 'general_quartic': 165,
        'explicit_quartic': 180, 'ordinary_abc_unrestricted_degree': 11}
    assert current['further_variable_reduction_beyond_supplied_records_proved'] is True

    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert 'notes of Gabe Conant with Astra 6.2' in readme
    abc_rows = [line for line in readme.splitlines() if '| Ordinary rational abc |' in line]
    assert len(abc_rows) == 2
    assert any('| **59** | **4, exact** |' in line for line in abc_rows)
    assert any('| **11** | **≤ 6,361,985** |' in line for line in abc_rows)
    assert '[results JSON](data/results_20261119_v79.json)' in readme
    assert '$' not in readme and r'\(' not in readme and r'\[' not in readme

    builds = read(ROOT / 'data/audits/tex_build_20261119_v79.json')
    assert {row['paper'] for row in builds['papers']} == PAPERS
    for row in builds['papers']:
        assert digest(ROOT / row['paper']) == row['source_sha256']
        assert row['returncode'] == row['overfull_boxes'] == row['undefined_references'] == 0
        assert row['all_rendered_pages_reviewed'] and row['pages'] > 0
        assert len(row['page_sha256']) == row['pages']
    manual = read(PACKAGE / 'abc/manual_review59.json')
    assert manual['status'] == 'PASS under the explicitly retained arithmetic premises'
    for name, expected in manual['reviewed_sha256'].items():
        assert digest(ROOT / name) == expected, 'Reviewed source changed: ' + name

    stages = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

    def run(script, cwd=ROOT):
        result = subprocess.run([sys.executable, '-B', str(script)], cwd=cwd,
                                env=env, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(str(script) + '\n' + result.stdout[-12000:] + result.stderr[-12000:])
        stages.append({'script': str(script.relative_to(cwd)), 'status': 'PASS'})
        print(stages[-1]['script'] + ': PASS', flush=True)

    # The builder runs only in a minimal temporary tree, not the checkout.
    with tempfile.TemporaryDirectory(prefix='diophantine-v79-') as temporary:
        destination = Path(temporary)
        builder = Path('computation/variable_reductions_v79/abc/build59.py')
        parent = Path(read(PACKAGE / 'abc/quartic59/maps.json')['parent'])
        for relative in (builder, parent):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        run(destination / builder, destination)
        for name in ('quadrics.json', 'polynomial.json', 'maps.json', 'certificate.json'):
            relative = Path('computation/variable_reductions_v79/abc/quartic59') / name
            assert (destination / relative).read_bytes() == (ROOT / relative).read_bytes(), name

    run(PACKAGE / 'abc/check59.py')
    run(PACKAGE / 'pole_normalization/check.py')
    run(PACKAGE / 'quartics/check_hyperbolic_parity.py')
    independent = read(PACKAGE / 'abc/independent59.json')
    assert independent['status'] == 'PASS' and independent['variables'] == 59
    assert independent['coordinate_monomials'] == claim['monomials'] == 873
    assert independent['height_and_regression']['strict_margin'] == '92221/99700'
    for path, expected in pins.items():
        assert digest(path) == expected, 'Verification modified ' + str(path.relative_to(ROOT))

    report = {
        'schema': 'diophantine-exact-verification/v79', 'status': 'PASS',
        'python': platform.python_version(), 'sympy': sympy.__version__,
        'stages': stages, 'published_inputs_unchanged': True,
        'regenerated_json_byte_identical': True,
        'manual_review_source_hashes_preserved': True,
        'quartic': {'variables': 59, 'degree': 4, 'quadrics': 51,
                    'coordinate_monomials': 873, 'parameter_separated_terms': 876,
                    'content': 1, 'exact_height': record['exact_height'],
                    'sufficient_defining_parameter_effective': False},
        'general_pole_blocks_independently_decoded': 10,
        'parity_obstruction_scope': current['new_scoped_obstruction']['scope'],
        'tex_papers_reviewed': len(builds['papers']),
        'tex_pages_reviewed': sum(row['pages'] for row in builds['papers']),
        'unchanged_variable_counts': current['unchanged_variable_counts'],
        'scope': 'Exact coefficient and physical-map reconstruction, temporary regeneration, '
                 'finite certificates, source/review pins and current-record consistency. '
                 'The universal arithmetic proof retains the premises named in the manuscript; '
                 'this finite gate does not establish those premises or an effective defining shift.',
    }
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
