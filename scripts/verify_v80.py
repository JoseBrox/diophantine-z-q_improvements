#!/usr/bin/env python3
"""Rebuild and independently verify the 58-variable ordinary-abc quartic.

The finite checks below do not prove the arithmetic inputs or make the
sufficient defining parameter effective. Those distinctions are enforced
in the records and detailed in the source proof and independent review.
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
PACKAGE = ROOT / 'computation/variable_reductions_v80'
PAPER = 'papers/quartic_existence/one_helper58_20261119_v80.tex'
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


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
    assert set(manifest['papers']) == {PAPER}
    actual_files = {str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob('*')
                    if path.is_file() and path.name != 'manifest.json'
                    and '__pycache__' not in path.parts}
    assert actual_files == set(manifest['files']), 'Incomplete package manifest'
    for path, expected in pins.items():
        assert digest(path) == expected, str(path.relative_to(ROOT))

    previous = read(ROOT / 'data/results_20261119_v79.json')
    current = read(ROOT / 'data/results_20261119_v80.json')
    before = {row['id']: row for row in previous['current_constructions']}
    after = {row['id']: row for row in current['current_constructions']}
    assert set(after) == set(before) - {'ordinary_abc_quartic59'} | {'ordinary_abc_quartic58'}
    for name in set(before) - {'ordinary_abc_quartic59'}:
        assert after[name] == before[name], 'Unintended change to ' + name
    assert current['historical_constructions'] == (
        previous['historical_constructions'] + [before['ordinary_abc_quartic59']])
    record = after['ordinary_abc_quartic58']
    claim = read(ROOT / record['certificate'])
    assert (record['variables'], record['degree'], record['quadratic_rows'],
            record['monomials'], record['parameter_separated_terms'],
            record['integer_content']) == (58, 4, 50, 867, 870, 1)
    assert record['exact_height'] == 'max(22838305425411,B^2+4091)'
    assert record['parameter_effective'] is False
    assert record['additional_hypothesis'] == 'ordinary rational abc'
    assert record['stronger_beta_one_twist_premise_required'] is False
    assert record['pole_completeness_source'] == (
        'Burungale, arXiv:2611.16130v1, Theorem B; beta congruent to 7 modulo 8')
    assert current['arithmetic_foundations_complete_independent_audit'] is False
    assert current['targets_21_and_9_proved'] is False
    assert current['targets_21_and_9_disproved'] is False
    assert current['source_attribution'] == previous['source_attribution']
    assert current['source_attribution']['name'] == 'Gabe Conant'
    assert current['source_attribution']['collaborating_model'] == 'Astra 6.2'
    assert current['unchanged_variable_counts'] == {
        'general_polynomial': 25, 'general_quartic': 165,
        'explicit_quartic': 180, 'ordinary_abc_unrestricted_degree': 11}
    assert current['further_variable_reduction_beyond_supplied_records_proved'] is True
    assert current['re_audit_v79']['exact_reconstruction'] == 'PASS'
    assert current['re_audit_v79']['coefficient_files_unchanged'] is True
    assert current['re_audit_v79']['original_review_pins_preserved'] is True

    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert 'notes of Gabe Conant with Astra 6.2' in readme
    abc_rows = [line for line in readme.split("## Fewest variables currently recorded for undecidability", 1)[0].splitlines() if '| Ordinary rational abc |' in line]
    assert len(abc_rows) == 2
    record_link = re.search(r'\[results JSON\]\((data/results_[^)]*\.json)\)', readme)
    assert record_link
    latest = read(ROOT / record_link.group(1))
    latest_quartic = next(row for row in latest['current_constructions']
                          if row['id'].startswith('ordinary_abc_quartic'))
    latest_unrestricted = next(row for row in latest['current_constructions']
                               if re.fullmatch(r'ordinary_abc\d+', row['id']))
    assert latest_quartic['degree'] == 4 and latest_quartic['variables'] <= 58
    assert latest_unrestricted['variables'] <= 11
    assert any(f"| **{latest_quartic['variables']}** | **4, exact** |" in line for line in abc_rows)
    assert any(f"| **{latest_unrestricted['variables']}** |" in line and '4, exact' not in line
               for line in abc_rows)
    assert '$' not in readme and r'\(' not in readme and r'\[' not in readme

    builds = read(ROOT / 'data/audits/tex_build_20261119_v80.json')
    assert {row['paper'] for row in builds['papers']} == {PAPER}
    for row in builds['papers']:
        assert digest(ROOT / row['paper']) == row['source_sha256']
        assert row['returncode'] == row['overfull_boxes'] == row['undefined_references'] == 0
        assert row['all_rendered_pages_reviewed'] and row['pages'] > 0
        assert len(row['page_sha256']) == row['pages']
    manual = read(PACKAGE / 'abc/manual_review58.json')
    assert manual['status'] == (
        'PASS under the explicitly retained arithmetic premises and the cited Theorem B')
    for name, expected in manual['reviewed_sha256'].items():
        assert digest(ROOT / name) == expected, 'Reviewed source changed: ' + name
    # Original review hashes remain independent of the newly written review.
    prior_manual = read(ROOT / 'computation/variable_reductions_v79/abc/manual_review59.json')
    for name, expected in prior_manual['reviewed_sha256'].items():
        assert digest(ROOT / name) == expected, 'Historical reviewed source changed: ' + name
    prior_audit = read(ROOT / 'data/audits/re_audit_20261119_v79_v80.json')
    assert prior_audit['status'] == 'PASS'
    assert prior_audit['regenerated_json_byte_identical'] is True
    assert prior_audit['published_inputs_unchanged'] is True
    assert prior_audit['manual_review_source_hashes_preserved'] is True
    assert len(prior_audit['stages']) == 4

    stages = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

    def run(script, cwd=ROOT):
        result = subprocess.run([sys.executable, '-B', str(script)], cwd=cwd,
                                env=env, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(str(script) + '\n' + result.stdout[-12000:] + result.stderr[-12000:])
        stages.append({'script': str(script.relative_to(cwd)), 'status': 'PASS'})
        print(stages[-1]['script'] + ': PASS', flush=True)

    # Regeneration is isolated and cannot rewrite a published coefficient file.
    with tempfile.TemporaryDirectory(prefix='diophantine-v80-') as temporary:
        destination = Path(temporary)
        builder = Path('computation/variable_reductions_v80/abc/build58.py')
        parent = Path(read(PACKAGE / 'abc/quartic58/maps.json')['parent'])
        for relative in (builder, parent):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        run(destination / builder, destination)
        for name in ('quadrics.json', 'polynomial.json', 'maps.json', 'certificate.json'):
            relative = Path('computation/variable_reductions_v80/abc/quartic58') / name
            assert (destination / relative).read_bytes() == (ROOT / relative).read_bytes(), name

    run(PACKAGE / 'abc/check58.py')
    independent = read(PACKAGE / 'abc/independent58.json')
    assert independent['status'] == 'PASS' and independent['variables'] == 58
    assert independent['unchanged_v79_rows'] == 47
    assert independent['coordinate_monomials'] == claim['monomials'] == 867
    assert independent['parameter_separated_terms'] == claim['parameter_separated_terms'] == 870
    assert independent['height_and_regression']['strict_margin'] == '92221/99700'
    assert independent['native_twist_identities']['theorem_B_required_classes'] == (
        'beta=7 mod8, eta=1 mod8; eta=1 allowed')
    for name, expected in independent['input_sha256'].items():
        assert digest(ROOT / name) == expected, name
    for path, expected in pins.items():
        assert digest(path) == expected, 'Verification modified ' + str(path.relative_to(ROOT))

    report = {
        'schema': 'diophantine-exact-verification/v80', 'status': 'PASS',
        'python': platform.python_version(), 'sympy': sympy.__version__,
        'stages': stages, 'published_inputs_unchanged': True,
        'regenerated_json_byte_identical': True,
        'manual_review_source_hashes_preserved': True,
        'historical_v79_review_source_hashes_preserved': True,
        'quartic': {'variables': 58, 'degree': 4, 'quadrics': 50,
                    'coordinate_monomials': 867, 'parameter_separated_terms': 870,
                    'content': 1, 'exact_height': record['exact_height'],
                    'sufficient_defining_parameter_effective': False},
        'published_native_twist_classes': 'beta=7 mod8, eta=1 mod8',
        'stronger_beta_one_twist_premise_required': False,
        'tex_papers_reviewed': len(builds['papers']),
        'tex_pages_reviewed': sum(row['pages'] for row in builds['papers']),
        'unchanged_variable_counts': current['unchanged_variable_counts'],
        'scope': 'Exact coefficient and physical-map reconstruction, temporary regeneration, '
                 'native twist identities, finite certificates, source/review pins and '
                 'current-record consistency. Universal valuation and completeness arguments '
                 'are reviewed in the proof; this finite gate does not establish the retained '
                 'arithmetic theorems, rational abc, or an effective sufficient defining shift.',
    }
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output)
    print(output)


if __name__ == '__main__':
    main()
