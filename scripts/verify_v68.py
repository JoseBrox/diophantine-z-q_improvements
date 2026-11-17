#!/usr/bin/env python3
"""Reproduce the compact 229-variable quartic and its canonical byte count."""
import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'computation/quartic/explicit229_compact_v68'
PAPER = 'papers/quartic/quartic229_compact_20261117_v68.tex'
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'
TEXT_HASH = '45bdea1ea7876bf6ec10b5427f9403cf1f94c144fab35817aa545bcb2cea1975'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(arguments):
    process = subprocess.run([sys.executable, '-B', *map(str, arguments)],
        cwd=ROOT, capture_output=True, text=True)
    if process.returncode:
        raise RuntimeError(process.stdout + process.stderr)
    return process.stdout


def main(output):
    package = ROOT / PACKAGE
    with tempfile.TemporaryDirectory(prefix='diophantine-v68-') as directory:
        temporary = Path(directory)
        reproduced = temporary / 'reproduced'
        shutil.copytree(package, reproduced)
        run([reproduced / 'build.py'])
        for name in ('quadratic.json', 'polynomial.json', 'quartic229-N15.txt'):
            assert (reproduced / name).read_bytes() == (package / name).read_bytes(), name
        run([reproduced / 'check.py', '--output', temporary / 'certificate.json'])
        assert (temporary / 'certificate.json').read_bytes() == (package / 'certificate.json').read_bytes()
        assert (reproduced / 'official_measurement.json').read_bytes() == (package / 'official_measurement.json').read_bytes()
        run([package / 'check_independent.py', '--package', package, '--repo', ROOT,
             '--manuscript', ROOT / PAPER, '--output', temporary / 'independent.json'])
        assert (temporary / 'independent.json').read_bytes() == (package / 'independent_certificate.json').read_bytes()

    certificate = json.loads((package / 'certificate.json').read_text())
    independent = json.loads((package / 'independent_certificate.json').read_text())
    official = json.loads((package / 'official_measurement.json').read_text())
    assert certificate['status'] == independent['status'] == 'PASS'
    assert certificate['checker_sha256'] == digest(package / 'check.py')
    assert independent['checker_sha256'] == digest(package / 'check_independent.py')
    assert independent['manuscript_sha256'] == digest(ROOT / PAPER)
    for key in ('inverse_map_checked', 'input_fixed', 'support_unchanged',
                'all_207_row_coefficients_checked', 'all_3312_expanded_coefficients_checked',
                'complete_literal_text_parsed', 'manuscript_exponent_tables_checked',
                'retained_arithmetic_body_unchanged_except_theorem_label'):
        assert independent[key] is True, key
    assert certificate['variables'] == independent['variables'] == 229
    assert certificate['quadratic_rows'] == independent['quadratic_rows'] == 207
    assert certificate['monomials'] == independent['monomials'] == 3312
    assert certificate['degree'] == independent['degree'] == 4
    assert certificate['content'] == independent['content'] == 1
    assert int(certificate['coefficient_height']) == int(independent['height']) == 149**30
    assert independent['height_bits'] == 217
    assert certificate['source_fixed_N'] == 15
    assert certificate['coefficient_height_improvement_factor'] == 22201
    assert certificate['all_rows_primitive'] and certificate['all_scalars_nonzero']
    assert all(certificate['negative_controls'].values())
    assert official['bytes'] == certificate['bytes'] == independent['canonical_bytes'] == 74007
    assert official['within_limit'] and official['verify_text_matches']
    assert official['sha256'] == independent['text_sha256'] == digest(package / 'quartic229-N15.txt') == TEXT_HASH
    assert (package / 'quartic229-N15.txt').stat().st_size < 100000

    results = json.loads((ROOT / 'data/results_20261117_v68.json').read_text())
    records = {item['id']: item for item in results['current_constructions']}
    record = records['explicit_quartic229']
    assert record['variables'] == 229 and record['degree'] == 4
    assert record['coefficient_height'] == '149^30'
    assert record['canonical_ascii_bytes'] == 74007
    assert record['polynomial_sha256'] == TEXT_HASH
    assert record['proof'] == PAPER and record['data'] == PACKAGE
    assert record['parameter'] == {'N': 15}
    previous = json.loads((ROOT / 'data/results_20261117_v65.json').read_text())
    for old in previous['current_constructions']:
        if old['id'] != 'explicit_quartic229':
            assert records[old['id']] == old, old['id']
    for key in ('new_variable_reduction', 'arithmetic_foundations_complete_independent_audit',
                'non_author_review', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established'):
        assert results[key] is False, key

    builds = json.loads((ROOT / 'data/audits/tex_build_20261117_v68.json').read_text())
    assert len(builds['papers']) == 1
    build = builds['papers'][0]
    assert build['paper'] == PAPER and build['source_sha256'] == digest(ROOT / PAPER)
    assert build['returncode'] == 0 and build['warnings'] == []
    assert build['pages'] == 13 and build['all_rendered_pages_reviewed']
    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert '$' not in readme and r'\operatorname' not in readme
    assert r'\(' not in readme and r'\[' not in readme
    assert readme.count('```math') > 0
    assert '74,007' in readme
    record_link = re.search(r'\[results JSON\]\((data/results_[^)]*\.json)\)', readme)
    assert record_link
    latest = json.loads((ROOT / record_link.group(1)).read_text())
    current_229 = next(row for row in latest['current_constructions']
                       if row['id'] == 'explicit_quartic229')
    assert current_229['canonical_ascii_bytes'] == 74007
    assert current_229['polynomial_sha256'] == TEXT_HASH
    assert 'docs/results_20261117_v68.md' in readme
    assert 'explicit229_compact_v68' in readme

    report = dict(schema='diophantine-exact-verification/v68', status='PASS',
        python=platform.python_version(), current_records='data/results_20261117_v68.json',
        source_sha256={PAPER: digest(ROOT / PAPER)},
        certificate_sha256={name: digest(package / name) for name in
            ('certificate.json', 'independent_certificate.json', 'official_measurement.json')},
        checker_sha256={name: digest(package / name) for name in ('check.py', 'check_independent.py')},
        builder_reproduced=True, every_coefficient_independently_reconstructed=True,
        whole_rational_zero_set_bijection=True, input_fixed=True, variables=229,
        degree=4, quadratic_rows=207, monomials=3312, coefficient_height='149^30',
        coefficient_height_bits=217, canonical_ascii_bytes=74007, strict_size_limit_bytes=100000,
        text_sha256=TEXT_HASH, upstream_acceptance_asserted=False,
        targets_21_and_9_proved=False, arithmetic_foundations_independently_audited=False,
        readme_dollar_delimiters=0, readme_operatorname_commands=0,
        contribution_and_citation_section_sha256=CONTRIBUTORS_HASH)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
