#!/usr/bin/env python3
"""Reproduce every shared source DAG and certify counts and degree bounds.

The degree calculation bounds entries of multiplication matrices without
materializing the enormous tensor matrices. Infinite arithmetic completeness
is proved in the accompanying TeX under its expressly retained premises.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'undecidability'
sys.path.insert(0,str(BASE/'code'))
import build_joint_few_variable as general
import build_joint_abc as abc
from finite_algebra_encoder import degree_bound, verify_examples
import sympy as sp


def verify_point_table():
    A,B=sp.symbols('A B')
    U=sp.Matrix([[0,2*A,2*B,0],[1,0,0,A],[0,0,0,-2*B],[0,2,0,0]])
    V=sp.Matrix([[0,2*B,A,0],[0,0,0,B],[1,0,0,-A],[0,0,-1,0]])
    W=sp.Matrix([[0,0,0,A*A-2*B*B],[0,A,B,0],[0,-2*B,-A,0],[1,0,0,0]])
    I=sp.eye(4)
    equalities=[U*U-2*A*I-2*W,V*V-A*I+W,U*V-2*B*I,
                U*W-A*U+2*B*V,V*W-B*U+A*V,W*W-(A*A-2*B*B)*I]
    assert all(all(sp.expand(x)==0 for x in r) for r in equalities)
    assert U*V==V*U and U*W==W*U and V*W==W*V
    assert (U*U)/2-A*I==W


def operator_degree_ledger(document):
    nodes=document['coefficient_dag']
    variables=document['variables']
    retained=document['retained_base_count']
    weights={v['index']:1 if v['index']<retained else 0 for v in variables}
    terminal={b['variable'] for b in document['finite_blocks'] if b['kind']=='pole'}
    dependencies=[]
    for op,*args in nodes:
        if op in ('int','parameter'):mask=0
        elif op=='variable':mask=2 if args[0] in terminal else 1 if args[0]>=retained else 0
        elif op=='pow':mask=dependencies[args[0]]
        else:
            mask=0
            for j in args:mask|=dependencies[j]
        dependencies.append(mask)
    assert all(not(dependencies[j]&2) for j in document['guard_numerators'])
    assert document['point_block_multiplication']=={
        'basis':['1','U','V','W'],'U^2':'2*A+2*W','V^2':'A-W',
        'U*V':'2*B','U*W':'A*U-2*B*V','V*W':'B*U-A*V','W^2':'A^2-2*B^2'}
    def degrees():
        out=[]
        for op,*args in nodes:
            if op in ('int','parameter'):d=0
            elif op=='variable':d=weights[args[0]]
            elif op=='pow':
                assert isinstance(args[1],int) and args[1]>=0
                d=out[args[0]]*args[1]
            elif op=='mul':d=sum(out[j] for j in args)
            elif op in ('add','neg'):d=max((out[j] for j in args),default=0)
            else:raise AssertionError(op)
            out.append(d)
        return out
    base_degrees=degrees()
    finite_indices=set()
    separating_indices=set()
    for b in document['finite_blocks']:
        if b['kind']!='point_block':continue
        # All coefficients of the actual point multiplication tables are
        # integral polynomials in retained variables, with denominator one.
        for q in ('A','B'):
            assert nodes[b[q]['denominator']]==['int',1]
            assert dependencies[b[q]['numerator']]==0
        a=base_degrees[b['A']['numerator']]
        bdeg=base_degrees[b['B']['numerator']]
        d0=max(a,bdeg)
        assert len(b['variable_nodes'])==3
        for nid,w in zip(b['variable_nodes'],(d0,d0,2*d0)):
            assert nodes[nid][0]=='variable'
            vid=nodes[nid][1]
            assert vid>=retained and vid not in finite_indices
            finite_indices.add(vid);weights[vid]=w
        separating_indices.update(nodes[j][1] for j in b['variable_nodes'][:2])
    point_degrees=degrees()
    poles=[]
    for b in document['finite_blocks']:
        if b['kind']!='pole':continue
        c=b['coefficient_nodes_ascending']
        # The monic leading coefficient is implicit in the source schema.
        assert b['monic'] is True and b['degree']==2
        assert len(c)==2 and nodes[c[1]]==['int',0]
        assert all(not(dependencies[j]&2) for j in c)
        vid=b['variable'];assert vid>=retained and vid not in finite_indices
        finite_indices.add(vid);separating_indices.add(vid);weights[vid]=point_degrees[c[0]]
        poles.append(weights[vid])
    assert finite_indices=={v['index'] for v in variables if v['index']>=retained}
    final_degrees=degrees()
    guard_degree=sum(final_degrees[j] for j in document['guard_numerators'])
    maximum_generator_degree=max(weights[j] for j in separating_indices)
    d=guard_degree+maximum_generator_degree
    points=sum(b['kind']=='point_block' for b in document['finite_blocks'])
    rank_exponent=2*points+len(poles)
    rank=1<<rank_exponent
    ell=len(separating_indices)+1
    assert ell==2*points+len(poles)+1
    D=degree_bound(rank,ell,d)
    # The ternary replacement doubles degree; summing squares doubles it again.
    eta=15616+233856*4+(233952*4+467712*4**2)*9**59
    final=max(4*D,2*eta)
    return {'finite_algebra_rank_exponent_base2':rank_exponent,'finite_algebra_rank':str(rank),
            'guard_multiplication_degree_bound':guard_degree,
            'maximum_generator_multiplication_degree_bound':maximum_generator_degree,
            'gamma_multiplication_degree_bound':d,'gamma_count':ell,
            'separating_generators':'U,V for each point and each pole root; W=U^2/2-A on every rational fiber',
            'difference_characteristic_degree':str(ell*(rank+1)**2),
            'joint_certificate_degree_upper_bound':str(D),
            'mixed_transfer_degree_upper_bound':str(final),
            'mixed_transfer_degree_strictly_less_than_power2':final.bit_length(),
            'degree_formula':'2*n*(J+1)*(1+d*(1+2*ell*J+2*ell*J**2+2*J)), J=ell*(n+1)**2',
            'method':'Exact integer upper bounds for polynomial multiplication-matrix entries; full matrices and final polynomial not expanded.'}


def verify():
    (ROOT/'.verification').mkdir(exist_ok=True)
    results={}
    verify_point_table()
    with tempfile.TemporaryDirectory(prefix='joint-source-',dir=ROOT/'.verification') as tmp:
        out=Path(tmp)
        for route in ('general25','explicit27','abc11'):
            if route=='abc11':
                import contextlib,io
                with contextlib.redirect_stdout(io.StringIO()):abc.build(ROOT,out/route,9)
                summary=json.loads((out/route/'certificate.json').read_text())
            else:summary=general.build(ROOT,out,route,9)
            fresh=(out/route/'joint_source.json').read_bytes()
            stored=gzip.decompress((BASE/'joint_sources'/route/'joint_source.json.gz').read_bytes())
            assert fresh==stored,(route,'DAG specification differs')
            expected=json.loads((BASE/'joint_sources'/route/'certificate.json').read_text())
            assert summary==expected,(route,'certificate differs')
            doc=json.loads(stored)
            assert hashlib.sha256(stored).hexdigest()==summary['joint_source_sha256']
            degrees=operator_degree_ledger(doc)
            assert degrees['finite_algebra_rank_exponent_base2']==summary['finite_algebra_rank_exponent_base2']
            results[route]={'variables':summary['mixed_integer_transfer_variables'],
                           'tuple_coordinates':summary['tuple_total_variables'],
                           'joint_source_sha256':summary['joint_source_sha256'],
                           'coefficient_nodes':len(doc['coefficient_dag']),
                           'guard_nodes':len(doc['guard_numerators']),
                           **degrees}
    examples=verify_examples()
    assert examples==json.loads((BASE/'certificates/finite_algebra_encoder.json').read_text())
    return {'status':'PASS','routes':results,'finite_encoder_edge_cases':'four exact checks passed',
            'point_multiplication_table':'all symbolic identities and rational generation by U,V verified',
            'scope':'Complete finite source maps, all coefficient DAG nodes and guards, matrix-entry degree bounds and numerical counts; retained arithmetic premises are not proved by computation.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    result=verify();text=json.dumps(result,indent=2)+'\n'
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(text)
    print(text,end='')
