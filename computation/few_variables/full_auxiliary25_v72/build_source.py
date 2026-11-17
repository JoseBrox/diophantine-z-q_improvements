#!/usr/bin/env python3
"""Exact full auxiliary general25 integer polynomial family."""
from pathlib import Path
import argparse,importlib.util,inspect,json,sys,hashlib
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def discover_repo():
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('--repo',type=Path)
    args,_=parser.parse_known_args()
    candidates=[args.repo.resolve()] if args.repo else [q for p in (HERE,*HERE.parents) for q in (p,p/'repo')]
    marker=Path('computation/few_variables/full_auxiliary11_v71/build_source.py')
    for candidate in candidates:
        if (candidate/marker).is_file():return candidate
    raise FileNotFoundError('Cannot find the project checkout; pass --repo PATH')

REPO=discover_repo()
FULL11=REPO/'computation/few_variables/full_auxiliary11_v71'

def check_dependencies():
    pins=json.loads((HERE/'dependencies.json').read_text())
    for relative,expected in pins['sha256'].items():
        actual=hashlib.sha256((REPO/relative).read_bytes()).hexdigest()
        if actual!=expected:raise ValueError('Pinned dependency changed: '+relative)
    return pins

check_dependencies()
ss=importlib.util.spec_from_file_location('full_auxiliary11_builder_for_general',FULL11/'build_source.py')
helper=importlib.util.module_from_spec(ss);sys.modules[ss.name]=helper;ss.loader.exec_module(helper)

# The constructor and all detector operations come from the retained source.
General25=__import__('build_sources').General25
class FullAuxiliary25(General25):
    def point(self,name):
        if name in ('A','S','T','Z'):
            return helper.old.OptimizedArithmetic.point(self,name)
        return helper.FullAuxiliary11.point(self,name)
    def build(self):
        source=super().build()
        source['format']='point-block-guarded-source/v72'
        source['auxiliary_chart']='H,U_A,U_S,U_T,U_Z use x=h,y=j,j^2=h^3-Dh; four root points retain x=h^2'
        source['proof']='papers/few_variables25/full_auxiliary25_20261117_v72.tex'
        source['arithmetic_status']='Full-E auxiliary enlargement of the retained general25 source; same scalar and comparison local implications; old complete subfamily retained. General21 rational realization remains open.'
        return source

def patch():
    text=inspect.getsource(helper.patch_compiler)
    text=text.replace('def patch_compiler():','def patch_general_compiler():')
    text=text.replace("block['name']=='A'","block['name'] in ('A','S','T','Z')")
    text=text.replace("point['name']=='A'","point['name'] in ('A','S','T','Z')")
    exec(compile(text,__file__,'exec'),helper.__dict__)
    return helper.patch_general_compiler()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=REPO)
    parser.add_argument('--L','--parameter',dest='L',type=int,default=3)
    parser.add_argument('--name',choices=['general25'],default='general25')
    parser.add_argument('--output',type=Path,default=HERE/'specification')
    args=parser.parse_args()
    changes=patch()
    source=FullAuxiliary25(args.L).build()
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    parent=helper.old._subalgebra.compile_specification(source)
    parent['native_source_generator']='computation/few_variables/full_auxiliary25_v72/build_source.py'
    parent['parent_pin_base']='containing specification directory'
    parent_path=output/'subalgebra_parent.json'
    parent_path.write_text(json.dumps(parent,indent=2)+'\n')
    helper.old._terminal.ROOT=output
    final=helper.old._terminal.compile_specification(source,parent,parent_path)
    (output/'source.json').write_bytes(helper.old.canonical(source))
    (output/'polynomial.json').write_text(json.dumps(final,indent=2)+'\n')
    report={'status':'PASS','scope':'Exact integer circuit construction; independent checks are in check.py',
        'source_sha256':hashlib.sha256(helper.old.canonical(source)).hexdigest(),
        'nodes':len(source['coefficient_dag']),'guards':len(source['guard_numerators']),
        'bounds':final['bounds'],'compiler_adjustments':changes,
        'family_parameter':source['family_parameter'],
        'coefficient_scope':'The numerical coefficient bound is for the specified fixed L; no numerical L is certified to exceed the sufficient defining threshold.',
        'general21_realization_claimed':False}
    (output/'construction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
