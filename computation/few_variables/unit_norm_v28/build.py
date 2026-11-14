#!/usr/bin/env python3
"""Exact determinant specifications and certified degree/height majorants.

Run with --output DIR to reconstruct every specification and bound in an
independent directory. --native-sources additionally exports the full native
integer circuits; they are not required to interpret the finite recipe.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
from build_sources import make_source
HERE=Path(__file__).resolve().parent
NAMES=('general25','explicit27','weak13','abc13')


def canonical(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()


def ell(n):
    if n<1:
        raise ValueError('Positive integer required')
    return (n-1).bit_length()


def compile_specification(source):
    nodes=source['coefficient_dag'];blocks=source['finite_blocks']
    base=source['retained_base_count']
    p=sum(r['kind']=='point_block' for r in blocks);s=len(blocks)-p
    if [r['kind'] for r in blocks] != ['point_block']*p+['pole']*s:
        raise ValueError('Unexpected block order')
    weights={};logs={}
    for block in blocks[:p]:
        for k,index in enumerate(block['variable_nodes']):
            variable=nodes[index][1]
            weights[variable]=(2,2,4)[k]
            logs[variable]=(4,4,6)[k]

    @lru_cache(None)
    def bound(index):
        op,*args=nodes[index]
        if op=='int':
            return (0,ell(abs(args[0])) if args[0] else 0)
        if op=='parameter':
            return 0,ell(max(1,abs(args[1])))
        if op=='variable':
            if args[0]<base:
                return 1,0
            if args[0] not in weights:
                raise ValueError('A point-algebra coefficient depends on a pole root')
            return weights[args[0]],logs[args[0]]
        if op=='neg':
            return bound(args[0])
        if op=='pow':
            return tuple(v*args[1] for v in bound(args[0]))
        values=[bound(i) for i in args]
        if op=='mul':
            return tuple(sum(v[k] for v in values) for k in (0,1))
        if op=='add':
            return max(v[0] for v in values),max(v[1] for v in values)+ell(len(values))
        raise ValueError('Unsupported operation: '+op)

    @lru_cache(None)
    def factors(index):
        op,*args=nodes[index]
        if op=='int' and abs(args[0])==1:
            return args[0],()
        if op=='int' and args[0]==0:
            raise ValueError('Literal zero in a required nonzero expression')
        if op=='neg':
            sign,fs=factors(args[0]);return -sign,fs
        if op=='pow':
            if args[1]==0:return 1,()
            sign,fs=factors(args[0])
            return sign**args[1],tuple((a,e*args[1]) for a,e in fs)
        if op=='mul':
            sign=1;fs=Counter()
            for a in args:
                sign_a,fs_a=factors(a);sign*=sign_a;fs.update(dict(fs_a))
            return sign,tuple(sorted(fs.items()))
        return 1,((index,1),)

    poles={r['generator_node'] for r in blocks[p:]}
    support=set();guard_records=[]
    for guard in source['guard_numerators']:
        sign,fs=factors(guard)
        support.update(a for a,e in fs if a not in poles)
        guard_records.append(dict(node=guard,sign=sign,factors=fs))
    radicands=[]
    for block in blocks[p:]:
        sign,fs=factors(block['coefficient_nodes_ascending'][0])
        sign=-sign # The monic equation is q^2 + a_0 = 0.
        support.update(a for a,e in fs)
        odd=[a for a,e in fs if e%2]
        square=[(a,e//2) for a,e in fs if e//2]
        degree=sum(bound(a)[0] for a in odd)
        log_norm=sum(bound(a)[1] for a in odd)
        radicands.append(dict(name=block['name'],native_constant_node=block['coefficient_nodes_ascending'][0],
            sign=sign,odd_factor_nodes=odd,square_multiplier_factors=square,
            degree_bound=degree,operator_log2_norm_bound=log_norm,
            root_weight=(degree+1)//2,root_log2_norm_bound=(log_norm+1)//2+1))
    support=sorted(a for a in support if nodes[a][0]!='int')
    if poles & set(support):
        raise ValueError('Pole dependence in the point-algebra support')
    support_records=[dict(node=a,degree=bound(a)[0],log_norm=bound(a)[1]) for a in support]
    t=sum(a['degree'] for a in support_records)
    t_log=sum(a['log_norm'] for a in support_records)
    b=4**p;n=b*2**s
    Z_d=48;Z_l=ell(2+2*p)+78
    D_d=144*p;D_l=234*p
    C_d=288+D_d
    C_l=5*(1+Z_l)+p+D_l+Z_l+3
    S_d=2*max(r['degree_bound']+4*p for r in radicands)
    S_l=ell(b)+ell(1+s*b*b)+2*max(r['operator_log2_norm_bound']+6*p for r in radicands)
    Q_d=s*S_d;Q_l=s*S_l+2*s-1
    point_d=Q_d+max([(p+1)*C_d]+[i*D_d+(p+1-i)*C_d+6 for i in range(1,p+1)])
    point_l=Q_l+ell(p+1)+max([(p+1)*C_l]+[i*D_l+(p+1-i)*C_l+12 for i in range(1,p+1)])
    xi_d=max((s-j)*S_d+sum(r['degree_bound'] for r in radicands[:j-1])+radicands[j-1]['root_weight'] for j in range(1,s+1))
    xi_l=ell(s)+max((s-j)*(S_l+2)+sum(r['operator_log2_norm_bound'] for r in radicands[:j-1])+radicands[j-1]['root_log2_norm_bound'] for j in range(1,s+1))
    omega_d=max(point_d,(p+1)*D_d+xi_d)
    omega_l=1+max(point_l,(p+1)*D_l+xi_l)
    degree=n*(b*t+omega_d+1)
    norm_log=n*(b*t_log+omega_l+1)
    V=base+1
    support_bound=math.comb(degree+V,V)-math.comb(degree-n+V-1,V)
    bounds=dict(total_variables=V,point_blocks=p,pole_quadratics=s,point_rank=b,full_rank=n,
        support_weight=t,support_operator_log2_norm_bound=t_log,
        point_basis_maximum_weight=4*p,point_basis_maximum_log2_scale=6*p,
        separator_degree_bound=omega_d,separator_operator_log2_norm_bound=omega_l,
        degree_before_input_factor=degree,degree_bound=degree+int(source['multiply_by_input']),
        degree_strict_power_of_two=(degree+int(source['multiply_by_input'])).bit_length(),
        separator_variable_degree_bound=n,monomial_upper_bound=str(support_bound),
        support_strict_power_of_two=support_bound.bit_length(),coefficient_l1_log2_bound=norm_log,
        coefficient_height_double_power_exponent=norm_log.bit_length(),integer_content=1,
        quantities=dict(Z_degree=Z_d,Z_log2_norm=Z_l,D_degree=D_d,D_log2_norm=D_l,
            C_degree=C_d,C_log2_norm=C_l,S_degree=S_d,S_log2_norm=S_l,Q_degree=Q_d,Q_log2_norm=Q_l))
    return dict(schema='unit-norm-polynomial-specification/v28',name=source['name'],
        native_source_sha256=hashlib.sha256(canonical(source)).hexdigest(),
        native_source_generator='computation/few_variables/unit_norm_v28/build_sources.py',
        native_source_arguments=dict(name=source['name'],parameter=source['family_parameter']['value']),
        native_source_nodes=len(nodes),family_parameter=source['family_parameter'],
        external_variables=source['variables'][:base]+[dict(index=base,name='U',category='single finite-algebra witness')],
        point_blocks=blocks[:p],quadratic_reductions=radicands,guard_factorizations=guard_records,
        support_factor_bounds=support_records,recipe=RECIPE,bounds=bounds,
        multiply_by_input=source['multiply_by_input'],
        arithmetic_scope=('Inherited arithmetic premises; the unsquared scale changes the ineffective sufficient exponent threshold.'
            if source['name']=='general25' else 'The sufficient parameter and arithmetic assumptions of the source are unchanged.'),
        norm_scope=('L=20483 is a certified defining choice under the inherited premises.' if source['name']=='explicit27'
            else 'Coefficient norm bound only for the stored fixture; it is not a certified defining parameter.'))


RECIPE={
 'native_source':'Run the exact native_source_generator at native_source_arguments; all circuit nodes are integer arithmetic operations.',
 'point_basis':['1','U_i','V_i','W_i'],
 'point_table':{'U_i^2':'2*A_i+2*W_i','V_i^2':'A_i-W_i','U_i*V_i':'2*B_i',
   'U_i*W_i':'A_i*U_i-2*B_i*V_i','V_i*W_i':'B_i*U_i-A_i*V_i','W_i^2':'A_i^2-2*B_i^2'},
 'B':'Tensor product of the free rank-four point blocks over the retained integer polynomial ring.',
 'c_j':'sign times the product of odd_factor_nodes in quadratic_reductions; original root = square_multiplier * new root.',
 'A':'B[q_1,...,q_s]/(q_j^2-c_j)',
 'T':'Product of the nodes in support_factor_bounds, each once; nonzero fixed integer factors are omitted.',
 'Delta':'det_B(M_T)',
 'point_primitive':'z_i=(2*A_i+B_i)*U_i-2*(A_i+B_i)*V_i',
 'point_quartic':'f_i(Z)=Z^4-4*(6*A_i^3-9*A_i*B_i^2-4*B_i^3)*Z^2+8*(-4*A_i^3+6*A_i*B_i^2+3*B_i^3)^2',
 'Z':'2+sum of squares of the nonleading coefficients of every point_quartic',
 'S':'b*(1+sum_{j=1}^s sum_{k,l=1}^b (M_c_j^B[k,l])^2)',
 'delta_i':'Disc(f_i)',
 'D':'product(delta_i^2)',
 'K':'(2*Z)^5 * product(1+delta_i^2)',
 'C':'D+4*Z*K',
 'J':'4*S',
 'Q':'2*S*J^(s-1)',
 'Xi':'sum_{j=1}^s J^(s-j)*(product_{k<j} c_k)*q_j',
 'Omega':'Q*(C^(p+1)+sum_{i=1}^p D^i*C^(p+1-i)*z_i)+D^(p+1)*Xi',
 'P':'det_A(I-U*Delta*M_Omega)',
 'final':'input.X*P when multiply_by_input is true; otherwise P',
 'semantic_scope':'Delta=0 gives P=1. Delta!=0 gives exactly a rational character of the guarded native source. Existence of a full-unit witness for every integer input is proved separately; equivalence at every original base tuple is NOT asserted.',
 'basis_order':'Lexicographic tensor basis in point-block order (1,U,V,W), followed by square exponents 0,1 in pole order.'}


def build(output: Path, native_sources=False):
    output.mkdir(parents=True,exist_ok=True)
    results=[]
    for name in NAMES:
        source=make_source(name)
        specification=compile_specification(source)
        (output/(name+'.json')).write_text(json.dumps(specification,indent=2)+'\n')
        if native_sources:
            (output/(name+'-native-source.json')).write_bytes(canonical(source))
        results.append(dict(name=name,**specification['bounds'],family_parameter=specification['family_parameter'],
            native_source_sha256=specification['native_source_sha256'],norm_scope=specification['norm_scope']))
    report=dict(schema='unit-norm-bounds/v28',builder_sha256=hashlib.sha256((HERE/'build_sources.py').read_bytes()).hexdigest(),
        constructions=results,scope='Certified upper bounds, not expanded degrees or support counts. Arithmetic assumptions are not certified by these computations.')
    (output/'bounds.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'specifications')
    parser.add_argument('--native-sources',action='store_true')
    args=parser.parse_args()
    for result in build(args.output,args.native_sources)['constructions']:
        print(result['name'],result['degree_bound'],'<2^'+str(result['degree_strict_power_of_two']),
            'height <2^(2^'+str(result['coefficient_height_double_power_exponent'])+')')
