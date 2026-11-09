#!/usr/bin/env python3
"""Rebuild and independently check the explicit 29-variable polynomial.

The fixed default exponent meets the proved effective cutoff. Identification
with the integers remains conditional on the four inherited arithmetic inputs.
Only Python's standard library is required.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def reproduce(exponent, output):
    output.mkdir(parents=True,exist_ok=True)
    source=output/'source.json.gz'
    spec=output/'polynomial-specification.json'
    calls=[
        ['build_forced_prime_source.py','--anchor-exponent',str(exponent),'--output',str(source)],
        ['check_forced_prime_source.py',str(source)],
        ['compile_source.py',str(source),'--output',str(output)],
        ['verify_specification.py',str(source),str(spec)],
    ]
    transcript=[]
    for args in calls:
        run=subprocess.run([sys.executable,str(HERE/args[0]),*args[1:]],
            cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        transcript.append('$ '+' '.join(args)+'\n'+run.stdout)
        if run.returncode:
            (output/'reproduction-transcript.txt').write_text('\n'.join(transcript))
            raise RuntimeError('Stage failed: '+args[0]+'\n'+run.stdout)
    verification=json.loads((output/'verification.json').read_text())
    assert verification['status']=='passed'
    assert verification['external_variables']==29
    assert verification['degree_bound_power_of_two_exponent']==161
    if exponent==137731:
        assert verification['coefficient_height_bound_double_power_of_two_exponent']==171
    example=HERE/'certificate'
    compared=False
    if exponent==137731 and example.exists() and output.resolve()!=example.resolve():
        for name in ('source.json.gz','polynomial-specification.json'):
            if (example/name).read_bytes()!=(output/name).read_bytes():
                raise RuntimeError('Packaged example differs: '+name)
        compared=True
    report={'status':'passed','anchor_exponent':exponent,
        'total_variables':29,'degree_bound_power_of_two_exponent':161,
        'coefficient_height_bound_double_power_of_two_exponent':verification['coefficient_height_bound_double_power_of_two_exponent'],
        'source_and_compiler_independent_checks_passed':True,
        'packaged_example_reproduced_byte_for_byte':compared,
        'selected_member_certified_to_define_Z':True,
        'scope':'Exact algebraic reproduction with the certified fixed-exponent cutoff. The polynomial defines the integers under exactly the four inherited arithmetic inputs.',
        'source_json_sha256':verification['source_json_sha256'],
        'specification_sha256':verification['specification_sha256'],
        'reproducer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (output/'reproduction-transcript.txt').write_text('\n'.join(transcript))
    (output/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--anchor-exponent',type=int,default=137731)
    parser.add_argument('--output',type=Path,
        help='optional output directory; otherwise use a temporary directory')
    args=parser.parse_args()
    if args.output:
        report=reproduce(args.anchor_exponent,args.output.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix='effective29-reproduce-',dir=HERE) as temp:
            report=reproduce(args.anchor_exponent,Path(temp))
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
