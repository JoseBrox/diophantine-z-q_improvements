#!/usr/bin/env python3
"""Check the frozen preferred source DAGs and their finite triangular shape.

This is a source-format and reproducibility check. The separate finite-algebra
compiler and independent audit check the final indexed polynomial construction.
"""
from collections import Counter
import gzip
import hashlib
import json
from math import prod
from pathlib import Path

from build_shared_source import SharedBuilder

HERE=Path(__file__).resolve().parent
CASES=[
    ('source-43-conic.json.gz','finite',42,20,29,
     'bdad2cd825cfd5e342a3bae01132cbbbbee179db5d8c2dc31e17475572b73f85'),
    ('source-45-conic-semilocal.json.gz','semilocal',44,21,30,
     'cc3f38bc2f464551c0eb86c5724afc52903dda393618aca2de25d4b5217abdc5')]


def check_case(name,anchor,base,generators,rank_exp,digest):
    raw=gzip.decompress((HERE/name).read_bytes())
    assert hashlib.sha256(raw).hexdigest()==digest
    obj=json.loads(raw)
    rebuilt=SharedBuilder(anchor=anchor,share_height=True,
        normalize_scalar=True,parametrize_poles=True,fixed_scales=True).build()
    assert raw==(json.dumps(rebuilt,separators=(',',':'))+'\n').encode('ascii')
    nodes=obj['coefficient_dag']; variables=obj['variables']
    assert [v['index'] for v in variables]==list(range(len(variables)))
    assert all(v['category'].startswith('retained.') for v in variables[:base])
    assert all(v['category'].startswith('finite.') for v in variables[base:])
    assert len(variables)==base+generators
    deps=[]
    for index,node in enumerate(nodes):
        op=node[0]
        if op=='int':
            assert len(node)==2 and isinstance(node[1],int)
            dependency=0
        elif op=='parameter':
            assert node[1] in obj['finite_parameters']
            dependency=0
        elif op=='variable':
            assert 0<=node[1]<len(variables)
            dependency=1<<node[1]
        else:
            assert op in ('add','mul','neg','pow')
            children=node[1:2] if op in ('neg','pow') else node[1:]
            assert all(isinstance(c,int) and 0<=c<index for c in children)
            if op=='pow':assert isinstance(node[2],int) and node[2]>=0
            dependency=0
            for child in children:dependency|=deps[child]
        deps.append(dependency)
    relations=obj['finite_monic_relations']
    assert len(relations)==generators
    assert [r['variable'] for r in relations]==list(range(base,len(variables)))
    for relation in relations:
        assert relation['monic'] is True
        coeffs=relation['coefficient_nodes_ascending']
        assert len(coeffs)==relation['degree']
        assert all(0<=c<len(nodes) for c in coeffs)
        assert all(deps[c]>>relation['variable']==0 for c in coeffs)
        assert nodes[relation['generator_node']]==['variable',relation['variable']]
    assert prod(r['degree'] for r in relations)==2**rank_exp
    assert obj['monic_degree_product']=={'base':2,'exponent':rank_exp}
    assert obj['retained_base_count']==base
    assert obj['total_polynomial_variables_after_finite_algebra']==base+1
    assert all(0<=g<len(nodes) for g in obj['guard_numerators'])
    assert not obj['closed_equations']
    params=obj['finite_parameters']
    assert len(params['scalar_correction'])==16384
    assert len(set(params['scalar_correction']))==16384
    assert all(v!=0 for v in params['scalar_correction'])
    charts=[k for k in params if k.startswith('pole_chart_')]
    assert len(charts)==10 and all(params[k]==[0,1] for k in charts)
    assert not any(k.startswith('zero_component') for k in params)
    assert len(params)==11
    assert obj['pole_first_conics_parametrized']
    assert obj['height_scales_without_case_parameters']
    assert obj['scalar_contact_normalized']
    assert obj['scalar_preparation_fixed_zero']
    return {'file':name,'status':'PASS','retained_base':base,
        'finite_generators':generators,'finite_rank_power_of_two':rank_exp,
        'relation_degrees':dict(Counter(r['degree'] for r in relations)),
        'dag_nodes':len(nodes),'guard_count':len(obj['guard_numerators']),
        'uncompressed_sha256':digest}


def main():
    results=[check_case(*case) for case in CASES]
    print(json.dumps({'status':'PASS','scope':'Frozen-byte reproducibility, '
        'integer DAG well-formedness, triangular monicity, counts, finite '
        'parameter lists and guard references. Arithmetic projection and final '
        'finite-algebra compilation are separately proved and checked.',
        'sources':results},indent=2))


if __name__=='__main__':main()
