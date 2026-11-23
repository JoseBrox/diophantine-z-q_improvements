#!/usr/bin/env python3
"""Rebuild the BB v2 transfers and verify their independent exact certificates.

The proof supplies the arithmetic implications. This gate checks the finite
algebra, every changed circuit, parameter qualifications and scoped exclusions.
It never alters a historical source or a published polynomial specification.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

import verify_v78

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'computation/bhargava_burungale_v88'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, *arguments):
    result = subprocess.run([sys.executable, '-B', str(script), *map(str, arguments)],
                            cwd=script.parent,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(str(script)+'\n'+result.stdout[-6000:]+result.stderr[-6000:])
    print(script.name+': PASS', flush=True)


def build(work):
    audit, count = verify_v78.materialize(work)
    for name in ('build_scalar_bb.py', 'build_twelve_bb.py', 'check_scalar_arithmetic.py'):
        shutil.copy2(PACKAGE/name, audit/'work_root'/name)
    target = audit/'work_root'
    run(target/'check_scalar_arithmetic.py')
    run(target/'build_twelve_bb.py', '--output', work/'bb_twelve')
    for route in ('general25', 'explicit27'):
        run(target/'build_scalar_bb.py', '--route', route, '--output', work/'bb_general')
    run(PACKAGE/'check_degrees.py', '--work-root', work, '--report', work/'independent_degrees.json')
    run(PACKAGE/'check_semantic_normalization.py', '--work-root', work, '--report', work/'semantic_normalization.json')
    for strong, name in ((False, 'weak_flip_first'), (True, 'strong_flip_first')):
        arguments = ['--work-root', work, '--output', work/'bb_weak'/name,
                     '--normalization', 'flip_first']
        if strong:
            arguments.append('--strong')
        run(PACKAGE/'build_weak_bb.py', *arguments)
    run(PACKAGE/'check_weak_bb.py', '--repo', work/'diophantine',
        work/'bb_weak/weak_flip_first', work/'bb_weak/strong_flip_first',
        '--report', work/'independent_weak.json')
    return audit, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--materialize', type=Path,
                        help='build a complete offline source tree and exact data at this new destination')
    args = parser.parse_args()
    import sympy
    assert sympy.__version__ == '1.14.0'
    if args.materialize:
        work = args.materialize.resolve()
        work.mkdir(parents=True, exist_ok=True)
        _, count = build(work)
        print('Materialized and independently checked', count, 'pinned source files.')
        return
    with tempfile.TemporaryDirectory(prefix='diophantine-v88-') as directory:
        work = Path(directory)
        audit, count = build(work)
        files = []
        for folder in ('bb_twelve', 'bb_general', 'bb_weak'):
            for published in sorted((PACKAGE/folder).rglob('*.json')):
                relative = published.relative_to(PACKAGE)
                assert (work/relative).read_bytes() == published.read_bytes(), relative
                files.append(str(relative))
        assert len(files) == 23
        for source, published in [
            (work/'independent_degrees.json', PACKAGE/'independent_degrees.json'),
            (work/'independent_weak.json', PACKAGE/'independent_weak.json'),
            (work/'semantic_normalization.json', PACKAGE/'semantic_normalization.json'),
            (audit/'work_root/scalar_arithmetic_certificate.json', PACKAGE/'scalar_arithmetic_certificate.json')]:
            assert source.read_bytes() == published.read_bytes(), published
        run(PACKAGE/'finite_twists_check.py', '--report', work/'finite_twists_certificate.json')
        assert (work/'finite_twists_certificate.json').read_bytes() == (PACKAGE/'finite_twists_certificate.json').read_bytes()
        height = work/'height'
        height.mkdir()
        shutil.copy2(PACKAGE/'check_height_improvements.py', height/'check_height_improvements.py')
        run(height/'check_height_improvements.py')
        assert (height/'certificate.json').read_bytes() == (PACKAGE/'height_certificate.json').read_bytes()
        negative = ROOT/'negative_results/R_square_reweighting_v88'
        run(negative/'check_two_unit_certificate.py',
            '--source-root', ROOT/'computation/variable_reductions_v82/general',
            '--report', work/'R_square_certificate.json')
        assert (work/'R_square_certificate.json').read_bytes() == (negative/'verification.json').read_bytes()
        records = json.loads((ROOT/'data/results_20261123_v88.json').read_text())
        assert records['variable_count_convention'] == 'includes the input'
        assert records['new_numerical_variable_record'] is False
        assert records['targets_21_and_9_proved'] is False
        assert records['route_bounds']['general25']['degree_upper_bound'] == 48318382080
        assert records['route_bounds']['explicit27']['degree_upper_bound'] == 183368679424
        assert records['route_bounds']['ordinary_abc11']['degree_upper_bound'] == 3261569
        assert records['route_bounds']['weak_abc11']['degree_upper_bound'] == 16460929
        assert records['route_bounds']['strong_weak_abc11']['degree_upper_bound'] == 9808001
        baseline = json.loads((ROOT/'data/results_20261120_v82.json').read_text())
        expected_current = [dict(id=key, **row) for key, row in records['route_bounds'].items()]
        expected_current += [row for row in baseline['current_constructions']
                             if row['id'] not in records['route_bounds']]
        assert records['current_constructions'] == expected_current
        assert len(expected_current) == 11
        for row in records['route_bounds'].values():
            digits = row['coefficient_log2_l1_bound_for_stored_member']*31//100+2
            monomial = row['variables']*(6+len(str(row['degree_upper_bound'])))
            term_power = (digits+monomial+2).bit_length()
            assert row['expanded_txt_kB_strict_power_two_fixture'] == row['support_strict_power_two']+term_power-9
        review = json.loads((ROOT/'data/audits/tex_build_20261123_v88.json').read_text())
        assert review['all_rendered_pages_reviewed'] is True
        for paper in review['papers']:
            assert digest(ROOT/paper['paper']) == paper['source_sha256']
            assert digest(ROOT/paper['pdf']) == paper['pdf_sha256']
            assert paper['returncode'] == paper['overfull_boxes'] == paper['undefined_references'] == 0
            assert len(paper['page_sha256']) == paper['pages'] > 0
    result = dict(schema='diophantine-bhargava-burungale-audit/v88', status='PASS',
                  source_files_pinned=count, regenerated_specification_files=len(files),
                  regeneration_byte_identical=True, new_producer_imported_by_independent_checker=False,
                  degree_bounds=[3261569, 48318382080, 183368679424, 16460929, 9808001],
                  source_name_recovery='Two exact historical texts reconstructed only in temporary pinned archives.',
                  scope='Exact circuits, all pole identities, determinant bounds, scalar constants, finite twist identities, height/interval identities and scoped Farkas certificates. Infinite arithmetic statements use the written proofs and explicitly retained sources.')
    text = json.dumps(result, indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
