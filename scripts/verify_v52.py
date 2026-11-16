#!/usr/bin/env python3
"""Verify the field-aligned scalar and unchanged defining-variable records."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
CONTRIBUTORS_HASH='bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def main(output):
    package=ROOT/'computation/pole_parameters/detector_field_norm_v52'
    with tempfile.TemporaryDirectory(prefix='diophantine-v52-') as directory:
        generated=Path(directory)/'certificate.json'
        run=subprocess.run([sys.executable,'-B',str(package/'check.py'),
                            '--output',str(generated),'--repo',str(ROOT)],
                           cwd=ROOT,capture_output=True,text=True)
        if run.returncode:
            raise ValueError(run.stdout+run.stderr)
        if generated.read_bytes()!=(package/'certificate.json').read_bytes():
            raise ValueError('Reconstructed scalar certificate differs.')
        certificate_hash=hashlib.sha256(generated.read_bytes()).hexdigest()
    current=json.loads((ROOT/'data/results_20261116_v52.json').read_text())
    previous=json.loads((ROOT/'data/results_20261116_v51.json').read_text())
    if current['current_constructions']!=previous['current_constructions']:
        raise ValueError('The auxiliary scalar family must not change the established records.')
    assert current['new_variable_reduction'] is False
    assert current['new_coefficient_improvement'] is False
    assert current['adaptive_complements']['actual_uniform_rational_realization_proved'] is False
    theorem=current['new_auxiliary_theorems'][0]
    assert theorem['total_variables']==25 and theorem['label_degree']==4
    assert theorem['scalar_contact_degree']==16 and theorem['norm_field_d']==2
    assert theorem['actual_prescribed_trace_realization_proved'] is False
    assert theorem['numeric_defining_degree_asserted'] is False
    readme=(ROOT/'README.md').read_text()
    match=re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)',readme)
    if not match or hashlib.sha256(match.group().encode()).hexdigest()!=CONTRIBUTORS_HASH:
        raise ValueError('The user contribution and citation section changed.')
    report={
        'schema':'diophantine-exact-verification/v52','status':'PASS',
        'python':platform.python_version(),
        'certificate':str((package/'certificate.json').relative_to(ROOT)),
        'certificate_sha256':certificate_hash,
        'construction_records_unchanged_from':'data/results_20261116_v51.json',
        'current_records':'data/results_20261116_v52.json',
        'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'established_general_counts':[25,13],'abc_quartic_variables':71,
        'new_auxiliary_source_variables':25,
        'actual_uniform_rational_realization_proved':False,
        'new_defining_variable_count':False,
        'numeric_degree_bound_for_new_scalar_assigned':False,
        'scope':'Exact field norm identities, degree-four integrality-reflecting label, degree-sixteen contact polynomial, uniform coefficient-dominance checks, local preparation and source hashes. The manuscript proves the full transfer under retained arithmetic premises. Bare conic points do not establish prescribed-trace realization.',
        'external_arithmetic_foundation_audited':False,
    }
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    main(parser.parse_args().report)
