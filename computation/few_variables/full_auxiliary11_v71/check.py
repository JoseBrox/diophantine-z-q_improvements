#!/usr/bin/env python3
"""Independent finite audit of the full-E auxiliary integer circuit.

The existing independent iterative verifier is given the proved new point
weights. It does not import the producer's bound or support traversals.
Native arithmetic is checked against chord-and-tangent calculations at
all 64 sign characters, including genuinely half-integral auxiliary indices.
These finite checks do not prove nine-coordinate realization.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
import argparse,hashlib,importlib.util,inspect,json,shutil,sys
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
from build_source import old,patch_compiler,make_source,REPO,check_dependencies

def module(name,path):
    ss=importlib.util.spec_from_file_location(name,path)
    mm=importlib.util.module_from_spec(ss);ss.loader.exec_module(mm);return mm

def norm_and_degree_bounds():
    a,b=sp.symbols('a b')
    A=a**3+6*a*b*b-11*a+12*b
    B=3*a*a*b+2*b**3+6*a-11*b
    l1=lambda q:sum(abs(int(v)) for v in sp.Poly(q,a,b).coeffs())
    assert l1(A)==30 and l1(B)==22
    # Bound every weighted matrix column directly from the table.
    scales=(1,F(16),F(16),F(80))
    U=((0,1,0,0),(60,0,0,2),(44,0,0,0),(0,30,44,0))
    V=((0,0,1,0),(44,0,0,0),(30,0,0,1),(0,22,30,0))
    W=((0,0,0,1),(0,30,44,0),(0,22,30,0),(1868,0,0,0))
    out={}
    for name,cols,limit in [('U',U,16),('V',V,16),('W',W,80)]:
        bounds=[sum(F(c)*scales[i]/scales[j] for i,c in enumerate(col))
                for j,col in enumerate(cols)]
        assert max(bounds)<=limit,(name,bounds)
        out[name]=[str(x) for x in bounds]
    assert 30**2+2*22**2<2**11
    Aprime=6*30**3+9*30*22**2+4*22**3
    Bprime=4*30**3+6*30*22**2+3*22**3
    assert Bprime<2**18
    assert 2*Aprime+2*(2*30**2+22**2)*80<2**20
    assert (4*30+3*22)*16<2**12
    assert 2*30**2+22**2<2**12
    return {'coefficient_l1':[30,22],'basis_scales':[1,16,16,80],
            'weighted_columns':out,'point_norm_radicand_log2':11,
            'point_primitive_radicand_log2':20,'primitive_root_log2':12}

def universal_point_algebra():
    """Exact matrices and discriminant, without importing a producer routine."""
    a,b,z=sp.symbols('a b z')
    I=sp.eye(4)
    U=sp.Matrix([(0,1,0,0),(2*a,0,0,2),(2*b,0,0,0),(0,a,-2*b,0)]).T
    V=sp.Matrix([(0,0,1,0),(2*b,0,0,0),(a,0,0,-1),(0,b,-a,0)]).T
    W=sp.Matrix([(0,0,0,1),(0,a,-2*b,0),(0,b,-a,0),(a*a-2*b*b,0,0,0)]).T
    def zero(matrix):
        assert all(sp.expand(entry)==0 for entry in matrix)
    zero(U*U-2*a*I-2*W);zero(V*V-a*I+W)
    zero(U*V-2*b*I);zero(U*W-a*U+2*b*V)
    zero(V*W-b*U+a*V);zero(W*W-(a*a-2*b*b)*I)
    zero(U*V-V*U);zero(U*W-W*U);zero(V*W-W*V)
    Z=(2*a+b)*U-2*(a+b)*V
    ap=6*a**3-9*a*b*b-4*b**3
    bp=-4*a**3+6*a*b*b+3*b**3
    quartic=z**4-4*ap*z*z+8*bp*bp
    assert sp.expand(Z.charpoly(z).as_expr()-quartic)==0
    zero(Z*Z-2*ap*I-2*(2*a*a-b*b)*W)
    discriminant=2**15*bp**2*(2*a*a-b*b)**4*(a*a-2*b*b)**2
    assert sp.expand(sp.discriminant(quartic,z)-discriminant)==0
    h0,h1=sp.symbols('h0 h1')
    A=h0**3+6*h0*h1*h1-11*h0+12*h1
    B=3*h0*h0*h1+2*h1**3+6*h0-11*h1
    assert sp.expand((h0+sp.sqrt(2)*h1)**3-(11-6*sp.sqrt(2))*(h0+sp.sqrt(2)*h1)-A-sp.sqrt(2)*B)==0
    assert sp.Poly(A*A-2*B*B,h0,h1).total_degree()==6
    assert sp.Poly(ap.subs({a:A,b:B}),h0,h1).total_degree()==9
    # Every nonzero matrix entry respects the integer basis weights.
    weights=[0,2,2,3]
    for matrix,weight in [(U,2),(V,2),(W,3)]:
        matrix=matrix.subs({a:A,b:B})
        for i in range(4):
            for j in range(4):
                if matrix[i,j]!=0:
                    deg=sp.Poly(matrix[i,j],h0,h1).total_degree()
                    assert deg+weights[i]<=weight+weights[j]
    return {'status':'PASS','multiplication_relations':6,'commutators':3,
            'primitive_characteristic_quartic':str(quartic),
            'discriminant_factorization':str(discriminant),
            'auxiliary_stage_degrees':[6,9],'basis_weights':weights,
            'coefficient_chart_identity':True}

def adapted_spec_checker():
    check=module('independent_full_aux_subcheck',REPO/'computation/few_variables/subalgebra_norms_v30/check.py')
    text=Path(check.__file__).read_text()
    repl={
        '(2,2,4), (4,4,6), (x,x,x^y)':
            "(2,2,4 if block['name']=='A' else 3), (4,4,7), (x,x,x^y)",
        'td += [(8,11,4,6),(12,20,6,12)]':
            "td += ([(8,11,4,7),(12,20,6,12)] if points[i]['name']=='A' else [(6,11,3,7),(9,20,5,12)])",
    }
    for a,b in repl.items():
        assert a in text,a;text=text.replace(a,b)
    exec(compile(text,check.__file__,'exec'),check.__dict__)
    return check,repl

def adapted_native_checker():
    check=module('independent_full_aux_native',REPO/'computation/few_variables/derivative11_v63/check_native.py')
    old_multiple=check.multiple
    R0=(check.K(1,1),check.K(0,2))
    assert check.add(R0,R0)==check.P
    def multiple(q):
        q=F(q);m=2*q
        assert m.denominator==1
        m=int(m)
        sign=-1 if m<0 else 1;m=abs(m)
        ans=None;base=R0
        while m:
            if m&1:ans=check.add(ans,base)
            base=check.add(base,base);m//=2
        return (ans[0],sign*ans[1]) if ans is not None else None
    check.multiple=multiple
    text=inspect.getsource(check.audit)
    before="chart={name:(ksqrt(point[0]),point[1]/ksqrt(point[0])) for name,point in points.items()}"
    after="chart={name:((ksqrt(point[0]),point[1]/ksqrt(point[0])) if name=='A' else point) for name,point in points.items()}"
    assert before in text;text=text.replace(before,after)
    before="""        assert hh**2 == points[name][0]
        assert jj**2 == hh**4-D
        assert hh*jj == points[name][1]"""
    after="""        if name=='A':
            assert hh**2 == points[name][0]
            assert jj**2 == hh**4-D
            assert hh*jj == points[name][1]
        else:
            assert hh == points[name][0]
            assert jj**2 == hh**3-D*hh
            assert jj == points[name][1]"""
    assert before in text;text=text.replace(before,after)
    exec(compile(text,check.__file__,'exec'),check.__dict__)
    return check

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=REPO)
    parser.add_argument('--specification',type=Path,default=HERE/'specification')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    pins=check_dependencies()
    elementary=norm_and_degree_bounds()
    algebra=universal_point_algebra()
    patch_compiler()
    output=args.specification.resolve()
    source=json.loads((output/'source.json').read_text())
    assert source==make_source(source['family_parameter']['value'])
    parent_path=output/'subalgebra_parent.json'
    parent=json.loads(parent_path.read_text())
    final=json.loads((output/'polynomial.json').read_text())
    subcheck,adjustments=adapted_spec_checker()
    olddir=output/'independent_old_cache'
    (olddir/'specifications').mkdir(parents=True,exist_ok=True)
    oldspec=old._subalgebra._old.compile_specification(source)
    (olddir/'specifications'/(source['name']+'.json')).write_text(json.dumps(oldspec))
    subcheck.OLD=olddir
    pa=subcheck.verify_spec(source,parent)
    shutil.rmtree(olddir)
    term=module('independent_full_aux_terminal',REPO/'computation/few_variables/terminal_root_v40/check.py')
    term.ROOT=output
    ta=term.verify_spec(source,parent,final,parent_path)
    controls=0
    for mutation in ['degree','guard']:
        bad=deepcopy(final)
        if mutation=='degree':bad['bounds']['degree_bound']-=1
        else:bad['subalgebra_norm_factors'].pop(0)
        try:term.verify_spec(source,parent,bad,parent_path)
        except AssertionError:controls+=1
        else:raise AssertionError('Corruption accepted: '+mutation)
    native=adapted_native_checker()
    records=[]
    for p in [1000000007,1000000009]:
        for n,h in [(1,F(1,2)),(2,F(3,2)),(3,F(5,2))]:
            r=native.audit(source,p,n,h)
            r['auxiliary_index']=str(r['auxiliary_index'])
            r['actual_indices']={k:str(v) for k,v in r['actual_indices'].items()}
            records.append(r)
    report={'status':'PASS','scope':__doc__,'source_sha256':hashlib.sha256((output/'source.json').read_bytes()).hexdigest(),
        'elementary_point_bounds':elementary,'universal_point_algebra':algebra,
        'checker_adjustments':adjustments,'pinned_dependencies':pins,
        'degree_bound':final['bounds']['degree_bound'],
        'coefficient_log2_l1_bound':final['bounds']['coefficient_log2_l1_bound'],
        'subalgebra_audit':pa,'terminal_audit':ta,'corruption_controls_rejected':controls,
        'actual_tuple_prime_pairs':len(records),'characters':sum(r['characters_checked'] for r in records),
        'native_records':records,'nine_coordinate_completeness_claimed':False}
    certificate=args.output or output/'independent_certificate.json'
    certificate.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','degree_bound','coefficient_log2_l1_bound','characters','corruption_controls_rejected']},indent=2))

if __name__=='__main__':main()
