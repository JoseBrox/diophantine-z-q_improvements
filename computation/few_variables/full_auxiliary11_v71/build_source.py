#!/usr/bin/env python3
"""Exact full-E auxiliary eleven-coordinate integer circuit.

The source repository is imported read only.  A retains the original
square-abscissa chart; H and U use x=h, y=j, j^2=h^3-Dh.  The same native
denominator guards retain the nonzero auxiliary radicands.  The output is
an explicitly specified eleven-coordinate family. Nine-coordinate
completeness is not asserted.

The old degree majorants are safe for cubic point radicands.  Coefficient
majorants need adjusted point basis scales: (1,16,16,80).  The narrowly
listed in-memory compiler changes below preserve these valid majorants.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent

def discover_repo():
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('--repo',type=Path)
    args,_=parser.parse_known_args()
    if args.repo is not None:
        candidates=[args.repo.resolve()]
    else:
        candidates=[]
        for parent in (HERE,*HERE.parents):
            candidates.extend([parent,parent/'repo'])
    marker=Path('computation/few_variables/derivative11_v63/build_source.py')
    for candidate in candidates:
        if (candidate/marker).is_file():
            return candidate
    raise FileNotFoundError('Cannot find the project checkout; pass --repo PATH')

REPO=discover_repo()

def check_dependencies():
    pins=json.loads((HERE/'dependencies.json').read_text())
    for relative,expected in pins['sha256'].items():
        actual=hashlib.sha256((REPO/relative).read_bytes()).hexdigest()
        if actual!=expected:
            raise ValueError('Pinned dependency changed: '+relative)
    return pins

check_dependencies()
PATH=REPO/'computation/few_variables/derivative11_v63/build_source.py'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('native_derivative63',PATH)
old=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)

class FullAuxiliary11(old.Derivative11):
    def point(self,name):
        if name=='A':
            return super().point(name)
        self.c.point_count+=1
        h=self.abscissas[name]
        x=h
        a,b=self.sub(self.mul(self.square(h),h),self.mul(self.D,h))
        u=self.c.variable(name+'.U','finite.point_block')
        v=self.c.variable(name+'.V','finite.point_block')
        w=self.c.variable(name+'.W','finite.point_block')
        j=self.remember_norm((u/2,v/2),w)
        point={'h':h,'j':j,'x':x,'y':j}
        self.relations.append(dict(name=name,kind='point_block',degree=4,
            A=self.rr(a),B=self.rr(b),variable_nodes=[u.n,v.n,w.n]))
        # Inverting y retains W!=0; W^2=Norm(h^3-Dh), so the whole
        # point algebra is etale on the guarded locus.
        self.inv(x);self.inv(j)
        self.events.append(dict(operation='point_block',name=name,
            chart='full_auxiliary',h=[self.rr(q) for q in h],
            A=self.rr(a),B=self.rr(b),j=[self.rr(q) for q in j],
            x=[self.rr(q) for q in x],y=[self.rr(q) for q in j]))
        return point

    def build(self):
        result=super().build()
        result['format']='point-block-guarded-source/v71'
        result['name']='ordinary_abc11_full_auxiliary'
        result['auxiliary_chart']='H,U: x=h, y=j, j^2=h^3-Dh; A retains x=h^2'
        result['proof']='papers/conditional_few_variables/full_auxiliary11_20261117_v71.tex'
        result['arithmetic_status']=('Ordinary rational abc and the v63 retained '
            'arithmetic inputs; full-E auxiliary soundness as proved in the '
            'companion manuscript; completeness inherited from the old subfamily. '
            'This is an eleven-coordinate source, not a proof of nine-coordinate completeness.')
        return result

def patch_compiler():
    # These are literal source replacements in private module dictionaries;
    # no source-repository file is changed.
    old_compiler=old._subalgebra._old
    text=Path(old_compiler.__file__).read_text()
    replacements={
        'weights[variable]=(2,2,4)[k]':
            "weights[variable]=(2,2,4 if block['name']=='A' else 3)[k]",
        'logs[variable]=(4,4,6)[k]':'logs[variable]=(4,4,7)[k]',
        'b=4**p;n=b*2**s':
            "b=4**p;n=b*2**s\n    point_basis_weight=sum(4 if block['name']=='A' else 3 for block in blocks[:p])",
        '+4*p':'+point_basis_weight',
        'point_basis_maximum_weight=4*p':'point_basis_maximum_weight=point_basis_weight',
        'D_l=234*p':'D_l=242*p',
        '+6*p':'+7*p',
        'point_basis_maximum_log2_scale=6*p':'point_basis_maximum_log2_scale=7*p',
    }
    for a,b in replacements.items():
        assert a in text,a
        text=text.replace(a,b)
    exec(compile(text,old_compiler.__file__,'exec'),old_compiler.__dict__)
    sub=old._subalgebra
    text=Path(sub.__file__).read_text()
    sub_replacements={
        'degree=8, operator_log2_norm=11,':
            "degree=(8 if point['name']=='A' else 6), operator_log2_norm=11,",
        'root_weight=4, root_operator_log2_norm=6)':
            "root_weight=(4 if point['name']=='A' else 3), root_operator_log2_norm=7)",
        'degree=12, operator_log2_norm=20,':
            "degree=(12 if point['name']=='A' else 9), operator_log2_norm=20,",
        'root_weight=6, root_operator_log2_norm=12)':
            "root_weight=(6 if point['name']=='A' else 5), root_operator_log2_norm=12)",
    }
    for a,b in sub_replacements.items():
        assert a in text,a
        text=text.replace(a,b)
    # Reloading the subalgebra module would otherwise reload its original
    # child compiler. Save and restore the adjusted module after execution.
    exec(compile(text,sub.__file__,'exec'),sub.__dict__)
    sub._old=old_compiler
    return {'old_compiler_replacements':replacements,
            'subalgebra_replacements':sub_replacements,
            'point_basis_scales':[1,16,16,80]}

def make_source(B=3):
    return FullAuxiliary11(B).build()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=REPO)
    parser.add_argument('--B','--shift','--parameter',dest='B',type=int,default=3)
    parser.add_argument('--name',choices=['ordinary_abc11_full_auxiliary'],
                        default='ordinary_abc11_full_auxiliary')
    parser.add_argument('--output',type=Path,default=HERE/'specification')
    args=parser.parse_args()
    changes=patch_compiler()
    source=make_source(args.B)
    output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    old._terminal.ROOT=output
    parent=old.parent_specification(source)
    generator='computation/few_variables/full_auxiliary11_v71/build_source.py'
    parent['native_source_generator']=generator
    parent['parent_pin_base']='containing specification directory'
    parent_path=output/'subalgebra_parent.json'
    parent_path.write_text(json.dumps(parent,indent=2)+'\n')
    final=old._terminal.compile_specification(source,parent,parent_path)
    final['native_source_generator']=generator
    (output/'source.json').write_bytes(old.canonical(source))
    (output/'polynomial.json').write_text(json.dumps(final,indent=2)+'\n')
    report={'status':'PASS','scope':'Exact integer circuit construction; independent checks are in check.py',
        'source_sha256':hashlib.sha256(old.canonical(source)).hexdigest(),
        'nodes':len(source['coefficient_dag']),'guards':len(source['guard_numerators']),
        'bounds':final['bounds'],'compiler_adjustments':changes,
        'family_parameter':source['family_parameter'],
        'arithmetic_scope':'eleven-variable full-E auxiliary enlargement; no 9/21 completeness',
        'coefficient_scope':'The numerical coefficient bound is for the specified fixed B; no numerical B is certified to exceed the sufficient defining threshold.'}
    (output/'construction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
