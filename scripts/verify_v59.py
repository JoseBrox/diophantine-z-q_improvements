#!/usr/bin/env python3
"""Verify the complete ordinary-abc eleven-variable source and scoped finiteness result."""
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
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'
PACKAGE = 'computation/few_variables/derivative11_v59'
JOBS = (
    (PACKAGE,'check_algebra.py','algebra_certificate.json'),
    (PACKAGE,'check_completeness.py','completeness_certificate.json'),
    (PACKAGE,'check_source_lemmas.py','source_lemmas_certificate.json'),
    (PACKAGE,'check_native.py','native_certificate.json'),
    (PACKAGE,'check_specification.py','specification_certificate.json'),
    ('negative_results/computation/fixed_slope_trace_v59','check.py','certificate.json'),
)
PAPERS = (
    'papers/conditional_few_variables/derivative_detector11_20261117_v59.tex',
    'negative_results/papers/rational_fibers/fixed_slope_trace_finiteness_20261117_v59.tex',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    results, hashes, certificate_hashes = [], {}, {}
    with tempfile.TemporaryDirectory(prefix='diophantine-v59-') as directory:
        for index,(relative,script,certificate) in enumerate(JOBS):
            generated = Path(directory)/f'certificate-{index}.json'
            package = ROOT/relative
            run = subprocess.run([sys.executable,'-B',str(package/script),'--output',str(generated)],
                                 cwd=ROOT,capture_output=True,text=True)
            if run.returncode:
                raise ValueError(run.stdout+run.stderr)
            if generated.read_bytes() != (package/certificate).read_bytes():
                raise ValueError(f'Regenerated certificate differs: {relative}/{certificate}')
            result = json.loads(generated.read_text())
            assert result['status']=='PASS'
            results.append(result)
            hashes[f'{relative}/{script}'] = digest(package/script)
            certificate_hashes[f'{relative}/{certificate}'] = digest(generated)
    algebra,completeness,lemmas,native,specification,incidence = results
    assert algebra['coordinate_census']['total']==11
    assert algebra['sun_prime_positions']==32
    assert algebra['height_parameters']['strict_margin']=='87545567/198403000'
    assert completeness['odd_valuation_fixtures']==7296
    assert lemmas['uniform_input_height_cases']==3684
    assert lemmas['coordinates']['total']==11
    assert native['characters']==384 and native['guard_count']==38
    assert native['finite_rank']==specification['full_rank']==128
    assert native['source_sha256']==specification['source_sha256']
    assert specification['degree_upper_bound']==5444199553
    assert specification['monomials_strict_power_of_two']==309
    assert all(row['support_factors']==41 and row['rational_denominators']==83
               for row in specification['fixtures'])
    assert incidence['conditional']['nonzero_parity_vectors_checked']==7
    assert incidence['general']['nonzero_parity_vectors_checked']==511
    assert not incidence['variable_slope_or_point_dependent_curve_coefficients_excluded']
    assert not incidence['new_defining_variable_bound_proved']
    current=json.loads((ROOT/'data/results_20261117_v59.json').read_text())
    previous=json.loads((ROOT/'data/results_20261117_v58.json').read_text())
    assert current['current_constructions'][:-1]==previous['current_constructions']
    new=current['current_constructions'][-1]
    assert new['id']=='ordinary_abc11' and new['variables']==11
    assert new['degree_upper_bound']=='5444199553'
    assert new['ordinary_abc_only'] and not new['weaker_fixed_exponent_transfer_proved']
    assert current['new_eleven_source']['proved_under_stated_premises']
    assert not current['new_eleven_source']['actual_nine_variable_realization_proved']
    assert not current['trace_conic_realization']['proved']
    assert not current['native_square_realization']['proved']
    assert not current['new_eleven_source']['external_foundations_independently_audited']
    readme=(ROOT/'README.md').read_text()
    match=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    assert match and hashlib.sha256(match.group().encode()).hexdigest()==CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    assert '**11**' in readme and '5{,}444{,}199{,}553' in readme
    builds=json.loads((ROOT/'data/audits/tex_build_20261117_v59.json').read_text())
    assert [row['paper'] for row in builds['papers']]==list(PAPERS)
    for row in builds['papers']:
        assert row['returncode']==0 and row['warnings']==[]
        assert row['all_rendered_pages_reviewed']
        assert row['source_sha256']==digest(ROOT/row['paper'])
        hashes[row['paper']]=row['source_sha256']
    assert lemmas['source_sha256']==hashes[PAPERS[0]]
    for relative in ('build_source.py','specification/source.json','specification/polynomial.json',
                     'specification/construction.json'):
        hashes[f'{PACKAGE}/{relative}']=digest(ROOT/PACKAGE/relative)
    report={
        'schema':'diophantine-exact-verification/v59','status':'PASS',
        'python':platform.python_version(),'source_sha256':hashes,
        'certificate_sha256':certificate_hashes,
        'current_records':'data/results_20261117_v59.json',
        'retained_records':'data/results_20261117_v58.json',
        'new_construction':{'hypothesis':'Ordinary rational abc and retained arithmetic inputs',
                            'variables':11,'degree_upper_bound':5444199553,
                            'monomials_strict_power_two':309,'integer_content':1,
                            'sufficient_shift_effective':False},
        'native_actual_point_character_evaluations':384,
        'denominator_and_square_extraction_independent_check':True,
        'fixed_slope_incidence_scope':'The stated earlier reweighted sources, fixed positive first-block coefficients and fixed smooth genus-one trace curve.',
        'individual_rational_witnesses_excluded':False,
        'targets_21_and_9_proved':False,
        'external_arithmetic_foundation_independently_audited':False,
        'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'scope':'Exact polynomial circuits, finite algebraic and valuation computations, complete census and independently checked determinant bounds. Infinite arithmetic existence and universal height results are the cited manuscript proofs, not computational inferences.',
    }
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    main(parser.parse_args().report)
