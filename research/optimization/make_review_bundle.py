#!/usr/bin/env python3
"""Write a review/checkpoint archive with the exact baseline needed offline.

No git mutation or network operation is performed. Added research files
are under research/optimization and research/phase2; references are unchanged.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
REVISION = '28e87b1b62af0effd954605af7f70b2699dd5672'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=REPO.parent/'research_checkpoint.zip')
    args = parser.parse_args()
    files = [p for p in sorted(HERE.rglob('*'))
             if p.is_file() and '__pycache__' not in p.parts
             and p.name != 'manifest.json']
    phase2 = [p for p in sorted((REPO/'research/phase2').rglob('*'))
              if p.is_file() and '__pycache__' not in p.parts]
    baseline = [p for p in sorted((REPO/'quartics/quartic-12504').rglob('*'))
                if p.is_file() and '__pycache__' not in p.parts]
    reference_names = ['quartic_12504.tex', 'README.md', 'CITATION.bib',
                       'CONTRIBUTING.md', 'THIRD_PARTY_NOTICES.md']
    references = [REPO/name for name in reference_names if (REPO/name).exists()]
    manifest = {
        'baseline_revision': REVISION,
        'scope': 'New research files only. Arithmetic interpretations remain conditional on the stated source inputs; the shared-point outputs also use Sun Theorem 4.1. No commits or pushes.',
        'research_files': [dict(path=str(p.relative_to(HERE)), bytes=p.stat().st_size,
                                sha256=digest(p)) for p in files],
        'phase2_files': [dict(path=str(p.relative_to(REPO)), bytes=p.stat().st_size,
                             sha256=digest(p)) for p in phase2],
        'unchanged_baseline_files': [dict(path=str(p.relative_to(REPO)),
                                         bytes=p.stat().st_size, sha256=digest(p))
                                     for p in baseline],
        'unchanged_reference_files': [dict(path=p.name, bytes=p.stat().st_size,
                                          sha256=digest(p)) for p in references],
    }
    mf = HERE/'manifest.json'
    mf.write_text(json.dumps(manifest, indent=2)+'\n')
    state = {
        'baseline_revision': REVISION,
        'prepared_local_branch': 'research/polynomial-optimization',
        'commits_made': False,
        'pushes_or_pull_requests_made': False,
        'paper': 'research/optimization/diophantine_optimization.tex',
        'primary_verification': 'research/phase2/verification/all-checks.json',
        'comparison_verification': 'research/optimization/verification/all-checks.json',
        'best_total_variable_bound': 43,
        'indexed_specification_emitted_and_checked': True,
        'large_indexed_matrices_and_products_expanded': False,
        'original_source_558_implemented_and_checked': True,
        'best_emitted_circuit_total_variables': 853,
        'best_quartic_total_variables': 1367,
        'best_fully_expanded_integer_quartic_total_variables': 1391,
        'conditional_mrdp_bounds_for_N_42': {'ce_Q_subset_witnesses': 463,
                                            'rational_solvability_unknowns': 380},
        'lower_bounds_unconditional': {'degree': 4, 'total_variables': 3, 'witnesses': 2},
        'arithmetic_scope': '558 and older comparison outputs preserve the original source projection. 43/45 and the new quartics use the stated source lemmas and Sun Theorem 4.1. The full external arithmetic inputs are not independently certified here.',
        'open_tasks': [
            'Independent audit of the source restricted 2-converse and fixed-field coefficient transfer.',
            'Independent audit of the full five-contact height theorem with its explicit numerical constant.',
            'Independent review of the simultaneous prime-pattern input, shared-point completeness and scalar normalization.',
            'Seek further reductions in retained elliptic/pole coordinates and in quadratic arithmetic evaluation.',
            'Human mathematical review, typesetting, and review of the proposed fork changes before any commit.',
        ],
        'number_fields': 'Released equation accepts every Q(i) input. No counterexample to the existence of a field-dependent definition of O_K in K was found; the general question is not settled here.',
    }
    phase2_state = REPO/'research/phase2/continuation_state.json'
    if phase2_state.exists():
        state['continuation'] = json.loads(phase2_state.read_text())
    top_readme = '''# Research checkpoint and review package

Start with `research/optimization/diophantine_optimization.tex` and
`research/optimization/README.md`. The paper is standalone LaTeX.

The proposed fork additions are `research/optimization/` and `research/phase2/`.
`quartics/quartic-12504/` is the unchanged pinned baseline included so the
checks can run without fetching GitHub. `reference_upstream/` holds unchanged
source and attribution files. These reference copies are not proposed edits.

From this archive's root, run:

    python3 -E -B research/phase2/verify_phase2.py
    python3 -E -B research/optimization/verify_all.py

The supplied receipts state what was checked. The source arithmetic theorems
and the additional prime-pattern input are separate dependencies.
Consult research/phase2/README.md and research/phase2/continuation_state.json
for the preferred 43/45/558 specifications, 1367/1391 quartics, stronger lower
bounds and remaining arithmetic review tasks. Earlier variants are comparisons.
`STATE.json` records the main results and priorities for continuing research.
`research/optimization/manifest.json` hashes every research and reference file.

To review in the fork, use the pinned revision recorded in STATE.json and
copy only the two research directories into your checkout. No commit, push, or pull
request has been made. PR_DRAFT.md is a reviewable description, not a submitted PR.
'''
    with ZipFile(args.output, 'w', ZIP_DEFLATED, compresslevel=6) as z:
        z.writestr('README.md', top_readme)
        z.writestr('STATE.json', json.dumps(state, indent=2)+'\n')
        for p in [*files, *phase2, mf, *baseline]:
            z.write(p, str(p.relative_to(REPO)))
        for p in references:
            z.write(p, 'reference_upstream/'+p.name)
    with ZipFile(args.output) as z:
        bad = z.testzip()
        if bad is not None:
            raise SystemExit('Archive CRC failure: '+bad)
    print(json.dumps({'file': str(args.output.resolve()),
                      'bytes': args.output.stat().st_size,
                      'sha256': digest(args.output),
                      'research_files': len(files)+1,
                      'phase2_files': len(phase2),
                      'baseline_files': len(baseline),
                      'reference_files': len(references),
                      'archive_crc_check': 'PASS'}, indent=2))


if __name__ == '__main__':
    main()
