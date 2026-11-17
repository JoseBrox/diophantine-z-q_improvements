#!/usr/bin/env python3
"""Complete eleven-variable source using the even valuations of abscissas.

The first four detector tests need no extra squaring before balancing.
Both the original nine contacts and the seven-contact arithmetic variant
are specified. Completeness in nine variables is not asserted.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,inspect,json,sys,textwrap
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module);return module

def check_dependencies():
    pins=json.loads((HERE/'dependencies.json').read_text())
    for rel,digest in pins['sha256'].items():
        assert hashlib.sha256((REPO/rel).read_bytes()).hexdigest()==digest,rel
    return pins

check_dependencies()
base=load('even_valuation_full_auxiliary_base',REPO/'computation/few_variables/full_auxiliary11_v71/build_source.py')
old=base.old;patch_compiler=base.patch_compiler

def patch_detector():
    text=textwrap.dedent(inspect.getsource(old.Derivative11.build))
    before="""        C2 = self.square(C)
        denominator = self.add(self.field(1), self.scale(C2, u))
        self.c.nonzero(self.norm(denominator), 'balanced%d.denominator norm'%i)
        Di = self.div(C2, denominator)"""
    after="""        if i < 2:
            xx = [H['x'], U['x']][i]
            denominator = self.add(xx, self.field(u))
            self.c.nonzero(self.norm(denominator), 'balanced%d.denominator norm'%i)
            Di = self.inv(denominator)
        elif i < 4:
            point = [HminusP, UminusA][i-2]
            numerator = self.square(point['dx'])
            denominator = self.add(point['X'], self.scale(numerator, u))
            self.c.nonzero(self.norm(denominator), 'balanced%d.denominator norm'%i)
            Di = self.conj(self.div(numerator, denominator))
        else:
            C2 = self.square(C)
            denominator = self.add(self.field(1), self.scale(C2, u))
            self.c.nonzero(self.norm(denominator), 'balanced%d.denominator norm'%i)
            Di = self.div(C2, denominator)"""
    replacements={before:after,
        'aa, zz = M**4, self.z**2':'aa, zz = M**(8 if self.contact_count == 7 else 4), self.z**2',
        'shifts = [-10,-8,-5,1,2,3,4,6,7]':'shifts = ([-7,-6,-4,1,3,5,8] if self.contact_count == 7 else [-10,-8,-5,1,2,3,4,6,7])',
        'u = -9*G/primitive_denominator':'u = -len(shifts)*G/primitive_denominator'}
    for a,b in replacements.items():
        assert text.count(a)==1,a;text=text.replace(a,b)
    scope=dict(old.__dict__);exec(compile(text,__file__,'exec'),scope)
    old.Derivative11.build=scope['build']
    return replacements

CHANGES=patch_detector()

def make_source(B=3,contacts=9):
    assert contacts in (7,9)
    builder=base.FullAuxiliary11(B);builder.contact_count=contacts
    source=builder.build()
    source.update(format='point-block-guarded-source/even-valuation-v75',
        name='ordinary_abc11_even_valuation_'+str(contacts),contact_count=contacts,
        balancing='C/(1+u*C) for four abscissa tests; C^2/(1+u*C^2) for two comparisons',
        proof='papers/conditional_few_variables/even_valuation_detector_20261117_v75.tex',
        arithmetic_status='Ordinary rational abc and the retained v63/v71 premises. Even-valuation abscissa balancing preserves extraction and complete eleven-variable witnesses. Seven contacts additionally use the v74 scale transfer. No nine-variable completeness claim.')
    return source

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--B',type=int,default=3);ap.add_argument('--contacts',type=int,choices=[7,9],default=9)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();adjustments=patch_compiler()
    source=make_source(args.B,args.contacts)
    output=(args.output or HERE/('specification' if args.contacts==9 else 'seven_contact')).resolve()
    output.mkdir(parents=True,exist_ok=True);old._terminal.ROOT=output
    parent=old.parent_specification(source);generator='computation/few_variables/even_valuation11_v75/build_source.py'
    parent['native_source_generator']=generator;parent['parent_pin_base']='containing specification directory'
    parent_path=output/'subalgebra_parent.json';parent_path.write_text(json.dumps(parent,indent=2)+'\n')
    final=old._terminal.compile_specification(source,parent,parent_path);final['native_source_generator']=generator
    (output/'source.json').write_bytes(old.canonical(source));(output/'polynomial.json').write_text(json.dumps(final,indent=2)+'\n')
    report=dict(status='PASS',source_sha256=hashlib.sha256(old.canonical(source)).hexdigest(),
        nodes=len(source['coefficient_dag']),guards=len(source['guard_numerators']),
        bounds=final['bounds'],contact_count=args.contacts,compiler_adjustments=adjustments,
        detector_changes=CHANGES,family_parameter=source['family_parameter'],
        nine_coordinate_completeness_claimed=False)
    (output/'construction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','nodes','guards','contact_count','bounds']},indent=2))

if __name__=='__main__':main()
