#!/usr/bin/env python3
"""Specify elimination by separating the nonzero-guard part of an etale algebra.

The output is an exact finite indexed polynomial recipe, not a monomial
expansion. Arithmetic projection hypotheses of the supplied source are unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path


def clog(n):
    assert n > 0
    return (n-1).bit_length()


def inspect_source(spec):
    nodes=spec['coefficient_dag']; rels=spec['monic_relations']
    p=next(i for i,r in enumerate(rels) if r['maximum_degree']!=4)
    assert p==9 and all(r['maximum_degree']==2 for r in rels[p:])
    s=len(rels)-p; dependencies=[]; exponents=[]; bounds=[]
    weights=[]; logs=[]
    # All coefficient nodes precede the final guard, but generator nodes can
    # precede their defining coefficients: use a recursive bound below.
    for op,*args in nodes:
        if op=='algebra_generator':
            dependencies.append({args[0]})
            exponents.append(tuple(int(args[0]==p+j) for j in range(s)))
        elif op in ('int','variable','parameter'):
            dependencies.append(set()); exponents.append((0,)*s)
        else:
            ix=args[:1] if op in ('neg','pow') else args
            dependencies.append(set().union(*(dependencies[k] for k in ix)))
            es=[exponents[k] for k in ix]
            if op=='add':
                out=es[0] if all(e==es[0] for e in es) else None
            elif op=='mul':
                out=tuple(sum(e[j] for e in es) for j in range(s)) if all(e is not None for e in es) else None
            elif op=='pow': out=tuple(args[1]*v for v in es[0]) if es[0] is not None else None
            elif op=='neg': out=es[0]
            else: raise ValueError(op)
            exponents.append(out)
    for i,r in enumerate(rels):
        deps=set().union(*(dependencies[k] for k in r['coefficient_nodes_ascending']))
        assert not deps if i<p else deps.issubset(set(range(p)))
        if i>=p: assert nodes[r['coefficient_nodes_ascending'][1]]==['int',0]
    assert exponents[spec['materialized_guard_node']]==(1,)*s
    cache={}
    def bound(k):
        if k in cache: return cache[k]
        op,*a=nodes[k]
        if op=='int': out=(0,clog(max(1,abs(a[0]))))
        elif op=='variable':out=(1,0)
        elif op=='parameter':out=(0,clog(max(1,abs(a[1]))))
        elif op=='algebra_generator':out=(weights[a[0]],logs[a[0]])
        elif op=='neg':out=bound(a[0])
        elif op=='pow':out=tuple(a[1]*x for x in bound(a[0]))
        elif op=='mul':out=tuple(sum(bound(k)[j] for k in a) for j in (0,1))
        elif op=='add':out=(max(bound(k)[0] for k in a),max(bound(k)[1] for k in a)+clog(len(a)))
        else:raise ValueError(op)
        cache[k]=out;return out
    for r in rels:
        d=r['maximum_degree']
        coeff=[(j,k) for j,k in enumerate(r['coefficient_nodes_ascending']) if nodes[k]!=['int',0]]
        weights.append(max([1]+[(bound(k)[0]+d-j-1)//(d-j) for j,k in coeff]))
        logs.append(max([0]+[(bound(k)[1]+d-j-1)//(d-j) for j,k in coeff])+clog(max(1,len(coeff))))
    g,eta=bound(spec['materialized_guard_node'])
    old=spec['bounds']
    assert weights==old['generator_weights']
    assert logs==old['generator_operator_log2_norm_bounds']
    assert g==old['materialized_guard_weight'] and eta==old['materialized_guard_operator_log2_norm_bound']
    assert not spec['closed_equations'] and not spec['indexed_guard_polynomials']
    assert all(len(v)==1 for v in spec['source_finite_parameters'].values())
    # Re-evaluate the guard after removing its homogeneous pole factor.
    gcache={}
    def point_guard_bound(k):
        if k in gcache: return gcache[k]
        op,*a=nodes[k]
        if op=='algebra_generator' and a[0]>=p: out=(0,0)
        elif op in ('int','variable','parameter','algebra_generator'): out=bound(k)
        elif op=='neg':out=point_guard_bound(a[0])
        elif op=='pow':out=tuple(a[1]*x for x in point_guard_bound(a[0]))
        elif op=='mul':out=tuple(sum(point_guard_bound(k)[j] for k in a) for j in (0,1))
        elif op=='add':out=(max(point_guard_bound(k)[0] for k in a),max(point_guard_bound(k)[1] for k in a)+clog(len(a)))
        else:raise ValueError(op)
        gcache[k]=out;return out
    wg,etag=point_guard_bound(spec['materialized_guard_node'])
    assert wg+sum(weights[p:])==g and etag+sum(logs[p:])==eta
    return p,weights,logs,g,eta,wg,etag


def certify(spec):
    p,w,gamma,g,eta,wg,etag=inspect_source(spec)
    ds=[r['maximum_degree'] for r in spec['monic_relations']]
    m=len(ds); s=m-p; b=math.prod(ds[:p]); n=math.prod(ds)
    lb=clog(b);ln=clog(n)
    basis_weight=sum((d-1)*v for d,v in zip(ds,w))
    basis_log=sum((d-1)*v for d,v in zip(ds,gamma))
    matrix_degree=max(basis_weight+max(w),sum((d-1)*v for d,v in zip(ds[:p],w[:p]))+wg)
    matrix_log=max(basis_log+max(gamma),sum((d-1)*v for d,v in zip(ds[:p],gamma[:p]))+etag)
    Rdeg=2*matrix_degree
    Rlog=ln+clog(1+m*n*n+b*b)+2*matrix_log
    t=2*g;mu=2*eta
    adeg=b*t;alog=b*(mu+lb)
    elog=alog+lb
    delta_degrees=[d*(d-1)*wi for d,wi in zip(ds[:p],w[:p])]
    delta_logs=[d*(d-1)*gi+clog(math.factorial(2*d-1)*d**d) for d,gi in zip(ds[:p],gamma[:p])]
    Ddeg=2*adeg+2*sum(delta_degrees);Dlog=2*alog+2*sum(delta_logs)
    sigma=sum(d*(d-1) for d in ds[:p])
    S=b*(s+1)+sigma
    Kdeg=S*Rdeg+Ddeg
    Klog=S*(1+Rlog)+p+1+Dlog
    Cdeg=Rdeg+Kdeg
    Clog=3+Rlog+Klog
    beta_degree=adeg+Ddeg+m*Cdeg+max(w)
    beta_log=Dlog+elog+clog(m+1)+m*Clog+max(gamma)
    Hdegree=n*(beta_degree+1)
    Hlog=n*(beta_log+ln+1)
    assert Hdegree>=adeg and Hlog>=alog
    degree_slope=(3+2*m)*t+m*(s+1)*Rdeg
    degree_intercept=2*(m+1)*sum(delta_degrees)+m*(sigma+1)*Rdeg+max(w)
    norm_slope=(3+2*m)*(mu+lb)+m*(s+1)*(1+Rlog)
    norm_intercept=(2*(m+1)*sum(delta_logs)+lb+clog(m+1)
        +m*(sigma*(1+Rlog)+p+4+Rlog)+max(gamma))
    assert degree_slope*b+degree_intercept==beta_degree
    assert norm_slope*b+norm_intercept==beta_log
    degree=n*(degree_slope*b*b+(degree_intercept+1)*(2*b-1))
    norm_log=n*(norm_slope*b*b+(norm_intercept+ln+1)*(2*b-1))+(b-1)*clog(b+1)
    return dict(method='separating_nonzero_guard_fibers_by_the_guard_product',
        total_variables=spec['total_external_variables'],retained_base_variables=spec['retained_base_variables'],
        point_generator_count=p,generator_count=m,point_algebra_rank=b,rank=n,
        generator_weights=w,generator_operator_log2_norm_bounds=gamma,
        guard_weight=g,guard_operator_log2_norm_bound=eta,
        point_guard_weight=wg,point_guard_operator_log2_norm_bound=etag,
        pole_exponents_in_guard=[1]*(m-p),native_discriminant_weights=delta_degrees,
        native_discriminant_operator_log2_norm_bounds=delta_logs,
        generator_matrix_entry_degree_bound=matrix_degree,generator_matrix_entry_log2_norm_bound=matrix_log,
        root_bound_degree=Rdeg,root_bound_log2_norm_bound=Rlog,
        guard_square_weight=t,guard_square_operator_log2_norm_bound=mu,
        coefficient_degree_bound=adeg,coefficient_log2_norm_bound=alog,
        idempotent_numerator_operator_log2_norm_bound=elog,
        D_degree_bound=Ddeg,D_log2_norm_bound=Dlog,root_separation_exponent=S,
        K_degree_bound=Kdeg,K_log2_norm_bound=Klog,
        C_degree_bound=Cdeg,C_log2_norm_bound=Clog,
        beta_weight=beta_degree,beta_operator_log2_norm_bound=beta_log,
        H_degree_bound=Hdegree,H_log2_norm_bound=Hlog,
        beta_degree_slope=degree_slope,beta_degree_intercept=degree_intercept,
        beta_log_norm_slope=norm_slope,beta_log_norm_intercept=norm_intercept,
        degree_cases=b,exact_factor_count=b,degree_bound=degree,
        degree_bound_power_of_two_exponent=clog(degree),
        coefficient_l1_norm_log2_bound=norm_log,
        coefficient_height_bound_double_power_of_two_exponent=clog(norm_log),
        semantic_scope='Exactly the rational base projection of the supplied guarded finite algebra; source arithmetic hypotheses unchanged.',
        expansion_status='Specified by finite integer polynomial operations; rank-sized matrices and monomial expansion are not materialized.')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('input',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args()
    raw=args.input.read_bytes();source=json.loads(raw);certificate=certify(source)
    out=dict(source);out['format']='integer-polynomial-indexed-finite-algebra/active-separation-v2'
    out['source_specification_sha256']=hashlib.sha256(raw).hexdigest()
    out['finite_algebra_recipe']={
        'base_point_algebra':'B is the tensor product of the first nine scalar monic quartics.',
        'quadratic_extensions':'A=B[q_1,...,q_s]/(q_j^2-c_j); c_j is minus the constant node of relation 9+j.',
        'source_guard':'G=g*product(q_j), with g in B; g is obtained by substituting 1 for every pole generator in the source guard DAG.',
        'T':'g^2*product(c_j) in B; it equals G^2 in A.',
        'standard_basis':'Native monomial basis, with each exponent smaller than its monic degree.',
        'native_discriminants':'delta_i=(-1)^(d_i*(d_i-1)/2)*Res(f_i,f_i_prime); only the nine scalar point discriminants are used.'}
    out['polynomial_recipe']={
        'theorem':'Elimination theorem in active_finite_algebra_20261109_v15.tex',
        'notation':'b=rank(B), n=rank(A), m=number of native generators; theta_i indexed 1,...,m.',
        'matrix_root_bound':'R=n*(1+sum_{i=1}^m sum_{u,v=1}^n (M_theta_i[u,v])^2+sum_{u,v=1}^b (M_g_on_B[u,v])^2)',
        'coefficients':'det_B(I-v*M_T)=sum_{j=0}^b a_j*v^j; a_0=1.',
        'for_each_case':'r=1,...,b; c=a_r; h_r(z)=sum_{j=0}^r a_j*z^(r-j); E=c-h_r(T).',
        'D':'c^2*product_{i=1}^p delta_i^2',
        'root_separation_exponent':'S_r=r*(s+1)+sum_{i=1}^p d_i*(d_i-1).' ,
        'K':'(2*R)^S_r*(1+c^2)*product_{i=1}^p(1+delta_i^2)',
        'C':'D+4*R*K',
        'beta':'D*E*(C^m+sum_{i=1}^m D^i*C^(m-i)*theta_i)',
        'H_r':'det_A(I-U*M_beta)',
        'Q_r':'H_r^2+sum_{j=r+1}^b a_j^2 if r<b; H_b if r=b',
        'product':'product_{r=1}^b Q_r',
        'source_parameters':'Use the unique listed value of each source_finite_parameter.',
        'only_external_variables':'The retained source base variables and U. All matrix entries, algebra generators, coefficient variables and finite indices are eliminated coefficient operations.'}
    out['bounds']=certificate
    args.output.mkdir(parents=True,exist_ok=True);dest=args.output/'polynomial-specification.json'
    dest.write_text(json.dumps(out,indent=2)+'\n')
    certificate=dict(certificate,input_specification_sha256=hashlib.sha256(raw).hexdigest(),
        output_specification_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
        family_parameter=source['family_parameter'],arithmetic_status=source['arithmetic_status'])
    (args.output/'construction-certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({k:certificate[k] for k in ['total_variables','degree_bound','degree_bound_power_of_two_exponent','coefficient_height_bound_double_power_of_two_exponent','exact_factor_count']},indent=2))


if __name__=='__main__':main()
