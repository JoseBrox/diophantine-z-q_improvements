#!/usr/bin/env python3
"""Materialize Gabe Conant's pinned notes with Astra 6.2 and replay v78.

The repository is never modified. Arithmetic premises and universal transfer
arguments are stated in the accompanying papers; this gate checks finite data.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'computation/coauthor_audit_v78'

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pinned_source_bytes(path, row):
    """Recover two frozen source texts after the authorized spelling correction.

    Both the current bytes and the reconstructed historical bytes are pinned.
    This preserves the original archive hashes without reverting public names.
    No mathematical text, source binding, or expected hash is relaxed.
    """
    raw = path.read_bytes()
    current = hashlib.sha256(raw).hexdigest()
    if current == row['sha256']:
        return raw
    repairs = read(ROOT / 'data/audits/source_name_compatibility_20261123.json')
    repair = repairs['files'][row['path']]
    assert current == repair['current_sha256'], row['path']
    assert row['sha256'] == repair['historical_sha256'], row['path']
    before, after = repair['current_text'].encode(), repair['historical_text'].encode()
    assert raw.count(before) == 1, row['path']
    restored = raw.replace(before, after)
    assert hashlib.sha256(restored).hexdigest() == row['sha256'], row['path']
    return restored

def authenticate_reviewed_source(path, expected):
    """Keep the original review pins after the named-attribution correction.

    Exact reverse edits recover the bytes covered by the original review;
    no arithmetic, coefficient or original-source assertion is relaxed.
    """
    if digest(path) == expected:
        return
    revisions = read(ROOT / 'data/audits/attribution_20261119.json')['papers']
    revision = revisions[str(path.relative_to(ROOT))]
    assert revision['previous_sha256'] == expected
    assert revision['current_sha256'] == digest(path)
    current = path.read_text()
    previous = current
    last_start = len(current)
    for edit in reversed(revision['reverse_edits']):
        start, end = edit['current_start'], edit['current_end']
        assert 0 <= start <= end <= last_start
        assert current[start:end] == edit['current_text']
        previous = previous[:start] + edit['previous_text'] + previous[end:]
        last_start = start
    assert hashlib.sha256(previous.encode()).hexdigest() == expected

def materialize(destination):
    """Create the original two archives and new work beside a pinned source tree."""
    target = destination / 'audit_20261119'
    shutil.copytree(PACKAGE, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    bindings = read(PACKAGE / 'source_bindings.json')
    union = {}
    for archive, rows in bindings['source_files'].items():
        for row in rows:
            source = PACKAGE / row['package_override'] if 'package_override' in row else ROOT / row['path']
            raw = pinned_source_bytes(source, row)
            union.setdefault(row['path'], row['sha256'])
            assert union[row['path']] == row['sha256']
            for path in (target/archive/'source'/row['path'], destination/'diophantine'/row['path']):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
    for local, paper in read(PACKAGE/'paper_paths.json').items():
        path = target/local
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/paper, path)
    return target, len(union)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--materialize', type=Path, help='write an offline, directly runnable audit tree and exit')
    args = parser.parse_args()
    import sympy
    assert sympy.__version__ == '1.14.0'
    if args.materialize:
        target, count = materialize(args.materialize.resolve())
        print('Materialized', count, 'pinned upstream files at', target)
        return
    manifest = read(PACKAGE/'manifest.json')
    for name, expected in manifest['files'].items():
        assert digest(PACKAGE/name) == expected, name
    for name, expected in manifest['papers'].items():
        assert digest(ROOT/name) == expected, name
    original_reviews = read(ROOT/'data/audits/tex_build_20261119_v78.json')
    for paper in original_reviews['papers']:
        authenticate_reviewed_source(ROOT/paper['paper'], paper['source_sha256'])
    reviews = read(ROOT/'data/audits/tex_build_20261119_attribution.json')
    assert len(reviews['papers']) == 6
    for paper in reviews['papers']:
        assert digest(ROOT/paper['paper']) == paper['source_sha256']
        assert paper['returncode'] == 0 and paper['overfull_boxes'] == 0
        assert paper['undefined_references'] == 0 and paper['all_rendered_pages_reviewed']
        assert len(paper['page_sha256']) == paper['pages'] > 0
    records = read(ROOT/'data/results_20261119_v78.json')
    assert records['targets_21_and_9_proved'] is False
    assert records['targets_21_and_9_disproved'] is False
    current = {row['id']: row for row in records['current_constructions']}
    degree_records = {
        'general25': ('work_root/four_contact/general25/projective.json', 'degree', 87778394112),
        'explicit27': ('work_root/four_contact/explicit27/reduced.json', 'degree', 335647080448),
        'ordinary_abc11': ('work_root/twelve/abc11/strengthened.json', 'degree', 6361985),
        'weak_abc11': ('work_weak11/full_flip_first/strengthened.json', 'degree_bound', 32542081),
        'strong_weak_abc11': ('work_weak11/full_strong_flip/strengthened.json', 'degree_bound', 19366273),
    }
    for name, (relative, key, bound) in degree_records.items():
        cert = read(PACKAGE/relative)
        assert current[name]['degree_upper_bound'] == cert[key] == bound
        assert current[name]['guard_degree'] == cert['guard_degree']
    for name, variables, monomials in [('quartic165',165,2607),('quartic180',180,2850),
                                      ('ordinary_abc_quartic62',62,840),
                                      ('weak_abc_quartic63',63,863),('weak_abc_quartic64',64,866),
                                      ('weak_abc_quartic67',67,905)]:
        row = current[name]
        assert (row['variables'],row['degree'],row['monomials']) == (variables,4,monomials)
        assert read(ROOT/row['data'])['variables'] == variables
    paper_paths = read(PACKAGE/'paper_paths.json')
    ordinary_review = read(PACKAGE/'work_general/independent_review.json')
    for name, expected in ordinary_review['reviewed_files'].items():
        relative = str(Path(name).relative_to('audit_20261119'))
        path = ROOT/paper_paths[relative] if relative in paper_paths else PACKAGE/relative
        authenticate_reviewed_source(path, expected)
    scalar_review = read(PACKAGE/'work_abc/scalar_independent_review.json')
    for name, record in scalar_review['artifacts'].items():
        relative = 'work_root/'+name
        path = ROOT/paper_paths[relative] if relative in paper_paths else PACKAGE/relative
        authenticate_reviewed_source(path, record['sha256'])
    stages = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v78-') as temporary:
        audit, source_count = materialize(Path(temporary))
        repo = Path(temporary)/'diophantine'
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', ABC62_PARENT=str(audit/'H10-quartics/abc62'))
        originals = {name: (audit/name).read_bytes() for name in manifest['files']
                     if name.endswith(('.json', '.txt')) and not name.startswith('upstream_overrides/')}
        def run(script, *arguments):
            script = audit/script
            result = subprocess.run([sys.executable, '-B', str(script), *map(str, arguments)],
                                    cwd=script.parent, env=env, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(str(script.relative_to(audit))+'\n'+result.stdout[-10000:]+result.stderr[-10000:])
            stages.append({'script': str(script.relative_to(audit)), 'status': 'PASS'})
            print(str(script.relative_to(audit))+': PASS', flush=True)
        # Both supplied packages, including their earlier degree reductions.
        run('H10-quartics/verify.py')
        run('H10-eleven-variables/verify.py')
        # Rebuild and independently expand the strengthened quartic sources.
        run('work_general/check_independent.py', audit/'H10-quartics')
        run('work_general/build_enhanced.py')
        run('work_general/check_enhanced.py')
        run('work_general/build_small_anchor.py')
        run('work_general/build_scaled_anchor.py')
        run('work_general/check_small_anchor.py')
        run('work_abc/build_small_gate62.py')
        run('work_abc/check_small_gate62.py')
        run('work_abc/build_weak_quartics.py')
        run('work_abc/check_weak_quartics.py')
        # Independent replay includes the raw DAG, every denominator and majorant.
        run('work_root/check_scalar_arithmetic.py')
        run('work_root/build_scalar.py', '--route', 'general25')
        run('work_root/build_scalar.py', '--route', 'explicit27')
        run('work_root/check_scalar_circuits.py')
        run('work_root/build_twelve.py')
        run('work_root/check_twelve.py')
        weak = audit/'work_weak11'
        run('work_weak11/build_full_auxiliary.py', '--squareclass', 'flip_first', '--output', weak/'full_flip_first')
        run('work_weak11/build_full_auxiliary.py', '--strong', '--squareclass', 'flip_first', '--output', weak/'full_strong_flip')
        run('work_weak11/strengthen_guards.py', weak/'full_flip_first', weak/'full_strong_flip')
        run('work_weak11/check_strengthened.py', '--repo', repo, weak/'full_flip_first', weak/'full_strong_flip')
        run('work_weak11/check_ancillary.py')
        for name, expected in originals.items():
            assert (audit/name).read_bytes() == expected, 'Regeneration changed '+name
    result = {'schema': 'diophantine-coauthor-audit/v78', 'status': 'PASS',
              'python': platform.python_version(), 'sympy': sympy.__version__,
              'source_files_pinned': source_count, 'publication_files_pinned': len(manifest['files']),
              'tex_papers_reviewed': 6, 'tex_pages_reviewed': reviews['total_reviewed_pages'],
              'stages': stages, 'regenerated_published_data_byte_identical': True,
              'scope': 'Exact source transfers, all quartic coefficients, finite-algebra DAGs and bounds, local finite certificates, and checked effective inequalities. The accompanying proofs retain explicitly stated arithmetic premises; this finite gate does not establish those premises.'}
    text = json.dumps(result, indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    print(text)

if __name__ == '__main__':
    main()
