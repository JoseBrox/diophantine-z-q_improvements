#!/usr/bin/env python3
"""Verify complete common-numerator source maps, counts and degree bounds.

Finite checks support the companion proof under the retained source premises;
they are not an independent proof of those arithmetic premises.
"""
from pathlib import Path
from collections import defaultdict
import argparse
import gzip
import hashlib
import json
import sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'undecidability'
sys.path.insert(0,str(BASE/'code'))
sys.path.insert(0,str(BASE))
from build_common_numerator import build_document
from verify_joint_sources import operator_degree_ledger,verify_point_table


def independently_replay(parent,doc):
    vmap=doc['parent_variable_map'];nmap=doc['parent_coefficient_node_map']
    oldvars=parent['variables'];newvars=doc['variables'];nodes=doc['coefficient_dag']
    assert len(vmap)==len(oldvars) and len(nmap)==len(parent['coefficient_dag'])
    aliases=defaultdict(list)
    for old in oldvars:
        parts=old['name'].split('.')
        expected=('.'.join(['shared',*parts[1:]]) if parts[0].startswith('block') and parts[1]=='UA' else old['name'])
        new=newvars[vmap[old['index']]]
        assert new['name']==expected and new['category']==old['category']
        aliases[new['index']].append(old['index'])
    k=doc['summary']['copies']
    repeated=[a for a in aliases.values() if len(a)>1]
    assert len(repeated)==5 and all(len(a)==k for a in repeated)
    assert len({v['name'] for v in newvars})==len(newvars)
    for j,old in enumerate(parent['coefficient_dag']):
        op,*args=old
        if op=='variable':expected=[op,vmap[args[0]]]
        elif op in ('int','parameter'):expected=old
        elif op=='pow':expected=[op,nmap[args[0]],args[1]]
        else:expected=[op,*[nmap[a] for a in args]]
        assert nodes[nmap[j]]==expected
    assert set(nmap)==set(range(len(nodes)))
    assert sorted({nmap[j] for j in parent['guard_numerators']})==doc['guard_numerators']
    assert [{j:vmap[v] for j,v in m.items()} for m in parent['original_variable_maps']]==doc['original_variable_maps']
    assert [[nmap[j] for j in m] for m in parent['original_coefficient_node_maps']]==doc['original_coefficient_node_maps']
    shared=[b for b in doc['finite_blocks'] if b['name']=='shared.UA']
    assert len(shared)==1
    assert all(not (b['name'].startswith('block') and b['name'].endswith('.UA')) for b in doc['finite_blocks'])


def exact_crt_identities():
    a,b,h,j,n=sp.symbols('a b h j n')
    assert sp.expand(((9+16*a)-1)**2+(16*b)**2-64*((1+2*a)**2+4*b*b))==0
    assert sp.expand(((9+16*a)+1)**2+(16*b)**2-4*((5+8*a)**2+64*b*b))==0
    assert sp.Poly((1+2*a)**2+4*b*b,a,b,modulus=2).as_expr()==1
    assert sp.Poly((5+8*a)**2+64*b*b,a,b,modulus=2).as_expr()==1
    assert ((1-1)**2+3**2)%7==2 and ((1+1)**2+3**2)%7==6
    e=j-h*n
    assert sp.cancel(j/h-(j-n)/(h-1)+e/(h*(h-1)))==0
    return {'primary_annihilator_2_adic_depth':4,'opposite_annihilator_odd':True,
            'seven_automatically_avoided':True,'full_ratio_identity':'j/h-(j-n)/(h-1)=-(j-h*n)/(h*(h-1))'}


def verify():
    results={};verify_point_table()
    for route,N in [('general25',83),('explicit27',101),('abc11',53)]:
        raw,summary=build_document(ROOT,route)
        folder=BASE/'common_numerator_sources'/route
        stored=gzip.decompress((folder/'common_source.json.gz').read_bytes())
        assert raw==stored
        assert summary==json.loads((folder/'certificate.json').read_text())
        doc=json.loads(stored)
        parent=json.loads(gzip.decompress((BASE/'joint_sources'/route/'joint_source.json.gz').read_bytes()))
        independently_replay(parent,doc)
        assert summary['mixed_integer_transfer_variables']==N
        assert summary['coordinate_savings_from_parent']==16
        assert summary['additional_prime_selection_premise'] is False
        degrees=operator_degree_ledger(doc)
        assert degrees['finite_algebra_rank_exponent_base2']==summary['finite_algebra_rank_exponent_base2']
        results[route]={'variables':N,'tuple_coordinates':summary['tuple_total_variables'],
            'joint_source_sha256':hashlib.sha256(stored).hexdigest(),
            'coefficient_nodes':len(doc['coefficient_dag']),'guard_nodes':len(doc['guard_numerators']),
            **degrees}
    return {'status':'PASS','routes':results,'formal_index_identities':exact_crt_identities(),
            'scope':'Exact source-map replay, complete coefficient circuits and guards, polynomial multiplication-table identities, degree and count bounds; simultaneous completeness is proved in the manuscript under the retained source premises.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);args=ap.parse_args()
    result=verify();out=json.dumps(result,indent=2)+'\n'
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(out)
    print(out,end='')
