#!/usr/bin/env python3
"""Identify the private numerator point across disjoint input contact families.

Input: the complete published v89 shared source. Output: its exact coefficient
DAG after identifying only blocki.UA with shared.UA. Completeness is the new
common-index CRT theorem, under the retained source arithmetic premises.
This finite transformation does not establish those arithmetic premises.
"""
from pathlib import Path
import argparse
import copy
import gzip
import hashlib
import json
import re
from build_joint_few_variable import Dag

ROOT=Path(__file__).resolve().parents[2]
ROUTES=('general25','explicit27','abc11')


def common_name(name):
    return re.sub(r'^block[0-9]+\.UA(?=\.|$)','shared.UA',name)


def build_document(repo,route):
    assert route in ROUTES
    folder=repo/'undecidability/joint_sources'/route
    raw=gzip.decompress((folder/'joint_source.json.gz').read_bytes())
    parent=json.loads(raw)
    receipt=json.loads((folder/'certificate.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==receipt['joint_source_sha256']
    k=receipt['copies'];assert k>=1
    variables=[];indices={};vmap=[]
    for old in parent['variables']:
        assert old['index']==len(vmap)
        name=common_name(old['name'])
        if name not in indices:
            indices[name]=len(variables)
            variables.append({'index':len(variables),'name':name,'category':old['category']})
        else:
            assert name.startswith('shared.UA.')
            assert variables[indices[name]]['category']==old['category']
        vmap.append(indices[name])
    retained=sum(not v['category'].startswith('finite.') for v in variables)
    assert all((v['index']<retained)==(not v['category'].startswith('finite.')) for v in variables)
    assert parent['retained_base_count']-retained==2*(k-1)
    assert len(parent['variables'])-len(variables)==5*(k-1)
    dag=Dag();nmap=[]
    for op,*args in parent['coefficient_dag']:
        if op=='variable':j=dag.node(op,vmap[args[0]])
        elif op in ('int','parameter'):j=dag.node(op,*args)
        elif op=='pow':j=dag.node(op,nmap[args[0]],args[1])
        elif op in ('add','mul','neg'):j=dag.node(op,*(nmap[a] for a in args))
        else:raise AssertionError(op)
        nmap.append(j)
    blocks={}
    def rational(x):return {a:nmap[x[a]] for a in ('numerator','denominator')}
    for old in parent['finite_blocks']:
        b=copy.deepcopy(old);b['name']=common_name(old['name'])
        if old['kind']=='point_block':
            b['A']=rational(old['A']);b['B']=rational(old['B'])
            b['variable_nodes']=[nmap[j] for j in old['variable_nodes']]
        elif old['kind']=='pole':
            b['variable']=vmap[old['variable']]
            b['generator_node']=nmap[old['generator_node']]
            b['coefficient_nodes_ascending']=[nmap[j] for j in old['coefficient_nodes_ascending']]
            b['original_root']=rational(old['original_root'])
            b['original_square_input']=rational(old['original_square_input'])
        else:raise AssertionError(old['kind'])
        if b['name'] in blocks:
            assert b['name']=='shared.UA' and blocks[b['name']]==b
        else:blocks[b['name']]=b
    finite=list(blocks.values());guards=sorted({nmap[j] for j in parent['guard_numerators']})
    points=sum(b['kind']=='point_block' for b in finite)
    poles=sum(b['kind']=='pole' for b in finite)
    e={'general25':2,'explicit27':3,'abc11':1}[route]
    common_points=2 if route=='abc11' else 8
    assert points==k+common_points and poles==e*k
    expected=(5*k+6 if route=='abc11' else (3+2*e)*k+18)
    assert retained+1==expected
    summary={
        'scope':'Complete source identification; simultaneous completeness proved by the common-index CRT theorem under retained source arithmetic premises.',
        'parent_source':str((folder/'joint_source.json.gz').relative_to(repo)),
        'parent_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),
        'source':receipt['source'],'source_sha256':receipt['source_sha256'],
        'source_family_parameter':receipt['source_family_parameter'],
        'source_pole_policy':receipt['source_pole_policy'],
        'route':route,'copies':k,'shared_point_roles':(['H','UA'] if route=='abc11' else ['S','T','Z','H','UA','US','UT','UZ']),
        'private_point_roles':['A'],'common_numerator_index_rule':'h=0 mod u_d; h=1 mod v_d; h=p_d mod p_d^2; j=0 mod u_d; j=n_i mod v_d; j=h*n_i mod p_d^5',
        'additional_prime_selection_premise':False,
        'retained_source_arithmetic_premises':True,
        'ordinary_rational_abc_required':route=='abc11',
        'retained_coordinate_counts':{'inputs':k,'common_point_coordinates':2*common_points,
            'private_root_coordinates':2*k,'common_contact_parameter':1,'private_pole_parameters':2*e*k,'single_joint_encoder':1},
        'tuple_total_variables':retained+1,'mixed_integer_transfer_variables':retained+3 if k==9 else None,
        'finite_point_blocks':points,'finite_quadratic_pole_blocks':poles,
        'finite_algebra_rank_exponent_base2':2*points+poles,
        'finite_algebra_rank':1<<(2*points+poles),
        'coordinate_savings_from_parent':2*(k-1),
        'finite_generator_savings_from_parent':3*(k-1),
        'joint_coefficient_nodes':len(dag.nodes),'joint_retained_guard_nodes':len(guards),
        'terminal_zero_roots_allowed':True,
        'source_contact_substitution':receipt.get('slope_substitution',receipt.get('contact_substitution')),
        'input_substitution':receipt.get('input_substitution','Unchanged shifted general input X_i^2+1'),
    }
    document={'schema':'common-numerator-source/v1','summary':summary,'variables':variables,
        'retained_base_count':retained,'coefficient_dag':dag.nodes,'finite_blocks':finite,
        'guard_numerators':guards,'point_block_multiplication':parent['point_block_multiplication'],
        'encoder':parent['encoder'],'parent_variable_map':vmap,'parent_coefficient_node_map':nmap,
        'original_variable_maps':[{j:vmap[v] for j,v in m.items()} for m in parent['original_variable_maps']],
        'original_coefficient_node_maps':[[nmap[j] for j in m] for m in parent['original_coefficient_node_maps']]}
    out=(json.dumps(document,separators=(',',':'))+'\n').encode()
    certificate=copy.deepcopy(summary);certificate['joint_source_sha256']=hashlib.sha256(out).hexdigest()
    return out,certificate


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path,default=ROOT/'undecidability/common_numerator_sources')
    args=parser.parse_args()
    for route in ROUTES:
        raw,cert=build_document(args.repo,route)
        folder=args.output/route;folder.mkdir(parents=True,exist_ok=True)
        (folder/'common_source.json.gz').write_bytes(gzip.compress(raw,mtime=0))
        (folder/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
        print(route,cert['mixed_integer_transfer_variables'],cert['joint_source_sha256'])

if __name__=='__main__':main()
