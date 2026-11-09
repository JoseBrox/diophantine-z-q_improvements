#!/usr/bin/env python3
"""Independently certify source structure, operator bounds and all degree cases.

No code is imported from the specification builder.  The companion-column
bounds are checked as inequalities, and the final product is bounded by a
literal sum of every separately evaluated factor.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from math import factorial, prod
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SOURCES={
 13: ROOT/'computation/few_variables/conditional13/certificate/source-polynomial-specification.json',
 27: ROOT/'computation/few_variables/trace27_nontorsion/example_L137731/polynomial-specification.json',
 29: ROOT/'computation/few_variables/effective29_nontorsion/certificate/polynomial-specification.json',
}


def ceil_log(value):
    assert value>0
    answer=value.bit_length()-1
    return answer+(value != 1<<answer)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def inspect_graph(source,certificate):
    nodes=source['coefficient_dag']; relations=source['monic_relations']
    p=certificate['point_generator_count']; m=len(relations); s=m-p
    assert p>=1 and m>p
    assert [r['maximum_degree'] for r in relations]==[4]*p+[2]*s
    weights=certificate['generator_weights']; logs=certificate['generator_operator_log2_norm_bounds']
    assert len(weights)==len(logs)==m
    tags=[]; dependencies=[]
    for index,node in enumerate(nodes):
        op=node[0]
        if op=='algebra_generator':
            j=node[1]; assert 0<=j<m
            tags.append(tuple(int(j==p+k) for k in range(s)))
            dependencies.append(frozenset([j]))
        elif op in ('int','variable','parameter'):
            tags.append((0,)*s); dependencies.append(frozenset())
        else:
            operands=node[1:2] if op in ('neg','pow') else node[1:]
            assert operands and all(0<=k<index for k in operands)
            dependencies.append(frozenset().union(*(dependencies[k] for k in operands)))
            if any(tags[k] is None for k in operands):tags.append(None)
            elif op=='add':
                tags.append(tags[operands[0]] if all(tags[k]==tags[operands[0]] for k in operands) else None)
            elif op=='mul':tags.append(tuple(sum(tags[k][j] for k in operands) for j in range(s)))
            elif op=='pow':
                assert isinstance(node[2],int) and node[2]>=0
                tags.append(tuple(e*node[2] for e in tags[node[1]]))
            elif op=='neg':tags.append(tags[node[1]])
            else:raise AssertionError(op)
    assert tags[source['materialized_guard_node']]==(1,)*s
    for j,relation in enumerate(relations):
        coeff=relation['coefficient_nodes_ascending']
        assert len(coeff)==relation['maximum_degree']
        used=frozenset().union(*(dependencies[k] for k in coeff))
        assert not used if j<p else used.issubset(frozenset(range(p)))
        if j>=p:assert nodes[coeff[1]]==['int',0]
    memo={}
    def estimate(index,remove_poles=False):
        key=index,remove_poles
        if key in memo:return memo[key]
        node=nodes[index]; op=node[0]
        if op=='int':answer=(0,ceil_log(max(1,abs(node[1]))))
        elif op=='parameter':answer=(0,ceil_log(max(1,abs(node[2]))))
        elif op=='variable':answer=(1,0)
        elif op=='algebra_generator':
            j=node[1]
            answer=(0,0) if remove_poles and j>=p else (weights[j],logs[j])
        elif op=='neg':answer=estimate(node[1],remove_poles)
        elif op=='pow':answer=tuple(node[2]*v for v in estimate(node[1],remove_poles))
        else:
            terms=[estimate(k,remove_poles) for k in node[1:]]
            if op=='mul':answer=(sum(v[0] for v in terms),sum(v[1] for v in terms))
            elif op=='add':answer=(max(v[0] for v in terms),max(v[1] for v in terms)+ceil_log(len(terms)))
            else:raise AssertionError(op)
        memo[key]=answer;return answer
    for j,relation in enumerate(relations):
        d=relation['maximum_degree']; assert weights[j]>=1 and logs[j]>=0
        nonzero=[(i,k) for i,k in enumerate(relation['coefficient_nodes_ascending']) if nodes[k]!=['int',0]]
        margin=ceil_log(max(1,len(nonzero)))
        for i,k in nonzero:
            degree,log_norm=estimate(k)
            assert degree<=(d-i)*weights[j]
            # Each companion-column summand is <=2^-margin after scaling.
            # There are at most 2^margin such summands; their sum is <=1.
            assert log_norm-(d-i)*logs[j]<=-margin
    guard=estimate(source['materialized_guard_node'])
    point_guard=estimate(source['materialized_guard_node'],True)
    assert guard==(certificate['guard_weight'],certificate['guard_operator_log2_norm_bound'])
    assert point_guard==(certificate['point_guard_weight'],certificate['point_guard_operator_log2_norm_bound'])
    assert guard==tuple(point_guard[k]+sum((weights,logs)[k][p:]) for k in (0,1))
    assert not source['closed_equations'] and not source['indexed_guard_polynomials']
    assert all(len(values)==1 for values in source['source_finite_parameters'].values())
    return {'coefficient_nodes':len(nodes),'point_relations':p,'quadratic_relations':s,
            'checked_companion_columns':m,'guard_pole_multidegree':list(tags[source['materialized_guard_node']]),
            'point_guard_bound_obtained_by':'Reevaluate the guard DAG with every pole generator replaced by 1; no division of norms.'}


def check_directory(directory):
    raw=(directory/'polynomial-specification.json').read_bytes(); spec=json.loads(raw)
    c=json.loads((directory/'construction-certificate.json').read_text())
    source_raw=SOURCES[c['total_variables']].read_bytes(); source=json.loads(source_raw)
    assert sha(raw)==c['output_specification_sha256']
    assert sha(source_raw)==c['input_specification_sha256']==spec['source_specification_sha256']
    assert spec['format']=='integer-polynomial-indexed-finite-algebra/active-separation-v2'
    changed={'format','source_specification_sha256','finite_algebra_recipe','polynomial_recipe','bounds'}
    assert {k:v for k,v in source.items() if k not in changed}=={k:v for k,v in spec.items() if k not in changed}
    assert spec['family_parameter']==c['family_parameter']
    assert spec['arithmetic_status']==c['arithmetic_status']
    assert c['family_parameter']['quantified'] is False
    assert c['family_parameter']['selected_member_certified_to_define_Z']==(c['total_variables']==29)
    graph=inspect_graph(source,c)
    ds=[r['maximum_degree'] for r in source['monic_relations']]
    p=graph['point_relations']; s=graph['quadratic_relations']; m=p+s
    b=prod(ds[:p]); n=prod(ds)
    assert b==c['point_algebra_rank'] and n==c['rank']
    assert c['total_variables']==c['retained_base_variables']+1==source['total_external_variables']
    w=c['generator_weights']; gamma=c['generator_operator_log2_norm_bounds']
    wg=c['point_guard_weight']; eg=c['point_guard_operator_log2_norm_bound']
    entry_degree=max(sum((d-1)*x for d,x in zip(ds,w))+max(w),sum((d-1)*x for d,x in zip(ds[:p],w[:p]))+wg)
    entry_log=max(sum((d-1)*x for d,x in zip(ds,gamma))+max(gamma),sum((d-1)*x for d,x in zip(ds[:p],gamma[:p]))+eg)
    rd=2*entry_degree; rl=ceil_log(n)+ceil_log(1+m*n*n+b*b)+2*entry_log
    u=[d*(d-1)*wi for d,wi in zip(ds[:p],w[:p])]
    v=[d*(d-1)*gi+ceil_log(factorial(2*d-1)*d**d) for d,gi in zip(ds[:p],gamma[:p])]
    assert u==c['native_discriminant_weights'] and v==c['native_discriminant_operator_log2_norm_bounds']
    t=2*c['guard_weight']; mu=2*c['guard_operator_log2_norm_bound']
    sigma=sum(d*(d-1) for d in ds[:p])
    total_degree=total_log=0
    # Literal summation deliberately does not use W_1*b^2 or the builder's
    # closed-form formula. Every degree case is independently evaluated.
    for r in range(1,b+1):
        cd=r*t; cl=r*(mu+ceil_log(b))
        ed=cd; el=cl+ceil_log(b)
        dd=2*cd+2*sum(u); dl=2*cl+2*sum(v)
        S=r*(s+1)+sigma
        kd=S*rd+dd; kl=S*(1+rl)+dl+p+1
        big_cd=rd+kd; big_cl=3+rl+kl
        bd=dd+ed+m*big_cd+max(w)
        bl=dl+el+ceil_log(m+1)+m*big_cl+max(gamma)
        hd=n*(bd+1); hl=n*(bl+ceil_log(n)+1)
        assert hd>=b*t and hl>=b*(mu+ceil_log(b))
        assert bd==c['beta_degree_slope']*r+c['beta_degree_intercept']
        assert bl==c['beta_log_norm_slope']*r+c['beta_log_norm_intercept']
        total_degree += hd if r==b else 2*hd
        total_log += hl if r==b else 2*hl+ceil_log(b+1)
    assert total_degree==c['degree_bound']==spec['bounds']['degree_bound']
    assert total_log==c['coefficient_l1_norm_log2_bound']==spec['bounds']['coefficient_l1_norm_log2_bound']
    assert total_degree<1<<c['degree_bound_power_of_two_exponent']
    assert total_log<1<<c['coefficient_height_bound_double_power_of_two_exponent']
    assert c['exact_factor_count']==c['degree_cases']==b
    assert spec['polynomial_recipe']['beta']=='D*E*(C^m+sum_{i=1}^m D^i*C^(m-i)*theta_i)'
    assert spec['polynomial_recipe']['Q_r']=='H_r^2+sum_{j=r+1}^b a_j^2 if r<b; H_b if r=b'
    assert spec['polynomial_recipe']['root_separation_exponent']=='S_r=r*(s+1)+sum_{i=1}^p d_i*(d_i-1).'
    return {'directory':directory.name,'status':'PASS','source_sha256':sha(source_raw),
            'specification_sha256':sha(raw),'graph_verification':graph,'cases_summed':b,
            'degree_bound':total_degree,'coefficient_l1_norm_log2_bound':total_log,
            'family_parameter':c['family_parameter']}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directories',type=Path,nargs='+')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    records=[check_directory(d) for d in args.directories]
    receipt={'status':'PASS','constructions':records,
             'scope':'Exact source dependency and homogeneous guard checks, independent companion-column inequalities, direct extraction of the point guard, and literal sum of every case bound. Global arithmetic premises and the ineffective threshold are not proved by this computation.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','constructions':len(records),'degree_bounds':[r['degree_bound'] for r in records]},indent=2))

if __name__=='__main__':main()
