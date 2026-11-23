#!/usr/bin/env python3
"""Reconstruct fixed-trace obstructions and check unchanged construction records."""
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
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


def main(output):
    import sympy
    if sympy.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    package = ROOT/'negative_results/computation/fixed_traces_v51'
    checks = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v51-') as directory:
        for script, certificate in [('check.py','certificate.json'),
                                    ('check_chamber.py','chamber_certificate.json'),
                                    ('check_positive_scale.py','positive_scale_certificate.json'),
                                    ('check_negative_scale.py','negative_scale_certificate.json')]:
            generated = Path(directory)/certificate
            run = subprocess.run([sys.executable, '-B', str(package/script),
                                  '--output', str(generated)], cwd=ROOT,
                                 capture_output=True, text=True)
            if run.returncode:
                raise ValueError(script+':\n'+run.stdout+run.stderr)
            if generated.read_bytes() != (package/certificate).read_bytes():
                raise ValueError('Reconstruction differs: '+certificate)
            checks.append({'script':str((package/script).relative_to(ROOT)),
                           'status':'PASS',
                           'certificate':str((package/certificate).relative_to(ROOT)),
                           'sha256':hashlib.sha256(generated.read_bytes()).hexdigest()})
            print(script+': PASS',flush=True)
    readme = (ROOT/'README.md').read_text()
    match = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    if not match or hashlib.sha256(match.group().encode()).hexdigest() != CONTRIBUTORS_HASH:
        raise ValueError('The user contribution and citation section changed.')
    current = json.loads((ROOT/'data/results_20261116_v51.json').read_text())
    previous = json.loads((ROOT/'data/results_20261116_v50.json').read_text())
    if current['current_constructions'] != previous['current_constructions']:
        raise ValueError('The obstruction update must not change the construction records.')
    assert current['new_variable_reduction'] is False
    assert current['new_coefficient_improvement'] is False
    assert current['adaptive_complements']['actual_uniform_rational_realization_proved'] is False
    assert current['adaptive_complements']['realization_targets'] == [21,9]
    assert 'sufficient_scaled_norm_one_target' not in current['adaptive_complements']
    proof = (ROOT/'papers/pole_parameters/adaptive_native_complements_20261116_v50.tex').read_text()
    assert 'A sufficient norm-one incidence' not in proof
    report = {
        'schema':'diophantine-exact-verification/v51','status':'PASS',
        'python':platform.python_version(),'sympy':sympy.__version__,
        'checks':checks,
        'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'construction_records_unchanged_from':'data/results_20261116_v50.json',
        'current_records':'data/results_20261116_v51.json',
        'established_general_counts':[25,13],'abc_quartic_variables':71,
        'actual_uniform_rational_realization_proved':False,
        'new_defining_variable_count':False,
        'scope':'Exact inert-prime certificate at an actual integer input, native normalization identities, scalar-prepared norm-orbit examples, and exact algebra supporting the conditional real-interval and all-slope scale proofs. Universal obstruction statements follow from the manuscript proofs. The full varying prescribed-trace rational realization remains unproved.',
        'external_arithmetic_foundation_audited':False,
    }
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    main(parser.parse_args().report)
