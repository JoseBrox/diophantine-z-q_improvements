#!/usr/bin/env python3
"""Independent finite audit for the full-E general25 integer circuit."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import argparse,importlib.util,inspect,json,sys,hashlib,shutil
sys.dont_write_bytecode=True
import build_source as builder
HERE=Path(__file__).resolve().parent
REPO=builder.helper.REPO

def module(name,path):
    ss=importlib.util.spec_from_file_location(name,path)
    mm=importlib.util.module_from_spec(ss);ss.loader.exec_module(mm);return mm

def spec_checker(pubcheck):
    text=inspect.getsource(pubcheck.adapted_spec_checker)
    text=text.replace('def adapted_spec_checker():','def adapted_general_spec_checker():')
    text=text.replace("block['name']=='A'","block['name'] in ('A','S','T','Z')")
    text=text.replace("points[i]['name']=='A'","points[i]['name'] in ('A','S','T','Z')")
    exec(compile(text,__file__,'exec'),pubcheck.__dict__)
    return pubcheck.adapted_general_spec_checker()

def native_checker(pubcheck):
    native=module('general25_direct_native',REPO/'computation/few_variables/unit_norm_v28/check.py')
    cyclic=pubcheck.adapted_native_checker()
    labels={'A':F(2),'S':F(3),'T':F(4),'Z':F(5),'H':F(3,2),
            'UA':F(3),'US':F(9,2),'UT':F(6),'UZ':F(15,2)}
    points={name:cyclic.multiple(n) for name,n in labels.items()}
    charts={name:((cyclic.ksqrt(P[0]),P[1]/cyclic.ksqrt(P[0]))
                  if name in ('A','S','T','Z') else P)
            for name,P in points.items()}
    def prepare(name,Q,p,rt,sign_seed):
        h,j=charts[name]
        idx=list(labels).index(name)
        # For seeds0..18, cover the identity and each single sign flip;
        # other seeds supply deterministic mixed characters.
        if sign_seed==0:sp,sm=1,1
        elif sign_seed<=18:
            sp=-1 if sign_seed-1==2*idx else 1
            sm=-1 if sign_seed-1==2*idx+1 else 1
        else:
            mask=(1103515245*sign_seed+12345)%2**18
            sp=-1 if (mask>>(2*idx))&1 else 1
            sm=-1 if (mask>>(2*idx+1))&1 else 1
        jp=sp*cyclic.embedding(j,rt,p)%p
        jm=sm*cyclic.embedding(j,-rt,p)%p
        jmK=((jp+jm)*pow(2,-1,p)%p,(jp-jm)*pow(2*rt,-1,p)%p)
        hm=Q.f(h.a,h.b)
        x=Q.f(points[name][0].a,points[name][0].b)
        y=Q.mul(hm,jmK) if name in ('A','S','T','Z') else jmK
        return hm,jmK,(x,y)
    native.prepare_actual=prepare
    text=inspect.getsource(native.modular_check)
    start=text.index("    for block in (b for b in source['finite_blocks'] if b['kind']=='point_block'):")
    end=text.index('    values=[]',start)
    text=text[:start]+"""    for block in (b for b in source['finite_blocks'] if b['kind']=='point_block'):
        name=block['name']
        h,j,point=prepare_actual(name,Q,p,rt,seed)
        variables[names[name+'.a0']],variables[names[name+'.a1']]=h
        variables[names[name+'.U']]=2*j[0]%p
        variables[names[name+'.V']]=2*j[1]%p
        variables[names[name+'.W']]=(j[0]**2-2*j[1]**2)%p
        points[name]=point
"""+text[end:]
    exec(compile(text,__file__,'exec'),native.__dict__)
    return native,labels

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=REPO)
    parser.add_argument('--specification',type=Path,default=HERE/'specification')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    pins=builder.check_dependencies()
    saved=sys.modules['build_source']
    try:
        sys.modules['build_source']=builder.helper
        pubcheck=module('independent11_for_general',builder.FULL11/'check.py')
    finally:
        sys.modules['build_source']=saved
    elementary=pubcheck.norm_and_degree_bounds()
    algebra=pubcheck.universal_point_algebra()
    builder.patch()
    output=args.specification.resolve()
    source=json.loads((output/'source.json').read_text())
    assert source==builder.FullAuxiliary25(source['family_parameter']['value']).build()
    parent_path=output/'subalgebra_parent.json'
    parent=json.loads(parent_path.read_text());final=json.loads((output/'polynomial.json').read_text())
    subcheck,adjust=spec_checker(pubcheck)
    cache=output/'independent_old_cache';(cache/'specifications').mkdir(parents=True,exist_ok=True)
    oldspec=builder.helper.old._subalgebra._old.compile_specification(source)
    (cache/'specifications/general25.json').write_text(json.dumps(oldspec))
    subcheck.OLD=cache
    pa=subcheck.verify_spec(source,parent)
    shutil.rmtree(cache)
    term=module('independent_general_terminal',REPO/'computation/few_variables/terminal_root_v40/check.py');term.ROOT=output
    ta=term.verify_spec(source,parent,final,parent_path)
    controls=0
    for mutation in ('degree','guard'):
        bad=deepcopy(final)
        if mutation=='degree':bad['bounds']['degree_bound']-=1
        else:bad['subalgebra_norm_factors'].pop(0)
        try:term.verify_spec(source,parent,bad,parent_path)
        except AssertionError:controls+=1
        else:raise AssertionError(mutation)
    native,labels=native_checker(pubcheck)
    records=[native.modular_check(source,p,seed)
             for p in (1000000007,1000000009) for seed in range(36)]
    report={'status':'PASS','scope':__doc__,'variables':25,
        'degree_bound':final['bounds']['degree_bound'],
        'source_sha256':hashlib.sha256((output/'source.json').read_bytes()).hexdigest(),
        'point_algebra':algebra,'elementary_bounds':elementary,
        'pinned_dependencies':pins,
        'independent_subalgebra_audit':pa,'independent_terminal_audit':ta,
        'corruption_controls_rejected':controls,'checker_adjustments':adjust,
        'actual_point_indices':{k:str(v) for k,v in labels.items()},
        'native_character_evaluations':len(records),'native_records':records,
        'all_characters_exhausted':False,'general21_realization_claimed':False}
    certificate=args.output or output/'independent_certificate.json'
    certificate.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','variables','degree_bound','native_character_evaluations','corruption_controls_rejected']},indent=2))

if __name__=='__main__':main()
