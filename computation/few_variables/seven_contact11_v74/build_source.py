#!/usr/bin/env python3
"""Seven-contact full-auxiliary eleven-coordinate source and finite specification.

The scale is a=M^8 and the contact set has seven shifts. This changes the
physical weight map to degree seven in z^2. It is not a nine-coordinate
completeness result, and is not claimed to improve the final total degree.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, inspect, json, sys, textwrap
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def check_dependencies():
    pins=json.loads((HERE/'dependencies.json').read_text())
    for rel,digest in pins['sha256'].items():
        assert hashlib.sha256((REPO/rel).read_bytes()).hexdigest()==digest,rel
    return pins

check_dependencies()
base=load('seven_contact_full_aux_base',REPO/'computation/few_variables/full_auxiliary11_v71/build_source.py')
old=base.old
patch_compiler=base.patch_compiler

def patch_contact():
    text=textwrap.dedent(inspect.getsource(old.Derivative11.build))
    replacements={
        'aa, zz = M**4, self.z**2':'aa, zz = M**8, self.z**2',
        'shifts = [-10,-8,-5,1,2,3,4,6,7]':'shifts = [-7,-6,-4,1,3,5,8]',
        'u = -9*G/primitive_denominator':'u = -7*G/primitive_denominator',
    }
    for before,after in replacements.items():
        assert text.count(before)==1,before
        text=text.replace(before,after)
    scope=dict(old.__dict__)
    exec(compile(text,__file__,'exec'),scope)
    old.Derivative11.build=scope['build']
    return replacements

CONTACT_CHANGES=patch_contact()

def make_source(B=3):
    source=base.make_source(B)
    source.update(format='point-block-guarded-source/seven-contact-v74',
        name='ordinary_abc11_seven_contact',
        proof='papers/conditional_few_variables/seven_contact_detector_20261117_v74.tex',
        arithmetic_status='Ordinary rational abc and the retained v63/v71 arithmetic premises; seven-contact height and preparation transfer as proved in the companion paper. Complete eleven-variable family; actual nine-variable realization remains unproved.')
    return source

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--B',type=int,default=3)
    ap.add_argument('--output',type=Path,default=HERE/'specification')
    args=ap.parse_args()
    compiler_changes=patch_compiler()
    source=make_source(args.B)
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    old._terminal.ROOT=output
    parent=old.parent_specification(source)
    generator='computation/few_variables/seven_contact11_v74/build_source.py'
    parent['native_source_generator']=generator
    parent['parent_pin_base']='containing specification directory'
    parent_path=output/'subalgebra_parent.json'
    parent_path.write_text(json.dumps(parent,indent=2)+'\n')
    final=old._terminal.compile_specification(source,parent,parent_path)
    final['native_source_generator']=generator
    (output/'source.json').write_bytes(old.canonical(source))
    (output/'polynomial.json').write_text(json.dumps(final,indent=2)+'\n')
    report=dict(status='PASS',scope='Exact circuit construction; finite verification in check.py',
        source_sha256=hashlib.sha256(old.canonical(source)).hexdigest(),
        nodes=len(source['coefficient_dag']),guards=len(source['guard_numerators']),
        bounds=final['bounds'],contact_changes=CONTACT_CHANGES,
        compiler_changes=compiler_changes,family_parameter=source['family_parameter'],
        physical_weight_degree_in_squared_slope=7,nine_coordinate_completeness_claimed=False)
    (output/'construction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','nodes','guards','bounds']},indent=2))

if __name__=='__main__':main()
