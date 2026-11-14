#!/usr/bin/env python3
"""Exact indexed specifications and bounds for finite-algebra elimination.

No large determinant or source polynomial is expanded. The source circuits
are reused at their pinned versions. Run --source-checkout PATH to authenticate
the existing files in a complete checkout. Standard library only.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path

HERE = Path(__file__).resolve().parent

def ell(n: int) -> int:
    if n < 1:
        raise ValueError('positive integer required')
    return (n-1).bit_length()

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def authenticate(c: dict, root: Path) -> None:
    spec = root/c['source_specification']
    if sha256(spec) != c['source_specification_sha256']:
        raise ValueError(f"changed source specification: {spec}")
    raw=(root/c['source_certificate']).read_bytes()
    git_sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if git_sha != c['source_certificate_git_blob_sha']:
        raise ValueError('changed source certificate')
    src=json.loads(raw)
    fields={'generator_weights':'generator_weights',
            'generator_log_norms':'generator_operator_log2_norm_bounds',
            'guard_weight':'guard_weight','guard_log_norm':'guard_operator_log2_norm_bound',
            'point_guard_weight':'point_guard_weight',
            'point_guard_log_norm':'point_guard_operator_log2_norm_bound'}
    for key, old in fields.items():
        if c[key] != src[old]:
            raise ValueError(f'input mismatch: {key}')
    s=json.loads(spec.read_text())
    if len(s['monic_relations']) != c['p']+c['s']:
        raise ValueError('wrong generator count')
    if s.get('closed_equations') or s.get('indexed_guard_polynomials'):
        raise ValueError('the theorem requires no further residual equations')

def bounds(c: dict) -> dict:
    p,s=c['p'],c['s']; ds=c['point_degrees']
    if len(ds)!=p or min(ds)<2 or s<1:
        raise ValueError('invalid degrees')
    b=math.prod(ds); n=b*(1<<s); w=c['generator_weights']; gam=c['generator_log_norms']
    if len(w)!=p+s or len(gam)!=p+s:
        raise ValueError('invalid weights')
    u=sum(c['discriminant_weights']); v=sum(c['discriminant_log_norms'])
    if c['discriminant_weights'] != [d*(d-1)*a for d,a in zip(ds,w[:p])]:
        raise ValueError('invalid discriminant degrees')
    point_basis_degree=sum((d-1)*a for d,a in zip(ds,w[:p]))
    point_basis_norm=sum((d-1)*a for d,a in zip(ds,gam[:p]))
    # Z bounds the point roots. S bounds the absolute values of all radicands.
    Z_d=2*max(d*a for d,a in zip(ds,w[:p]))
    Z_l=ell(2+sum(ds))+2*max(d*a for d,a in zip(ds,gam[:p]))
    S_d=2*max(2*a+point_basis_degree for a in w[p:])
    S_l=ell(b)+ell(1+s*b*b)+2*max(2*a+point_basis_norm for a in gam[p:])
    k=max((d*(d-1)-2)//2 for d in ds)
    D_d=2*u; D_l=2*v
    C_d=(k+1)*Z_d+D_d
    K_l=k*(1+Z_l)+p+D_l
    C_l=K_l+Z_l+3  # C=D+4 Z K; the sum costs one bit.
    Q_d=s*S_d
    Q_l=s*S_l+(2*s-1)
    point_d=Q_d+max([(p+1)*C_d]+[i*D_d+(p+1-i)*C_d+w[i-1] for i in range(1,p+1)])
    point_l=Q_l+ell(p+1)+max([(p+1)*C_l]+[i*D_l+(p+1-i)*C_l+gam[i-1] for i in range(1,p+1)])
    xi_d=max((s-j)*S_d+2*sum(w[p:p+j-1])+w[p+j-1] for j in range(1,s+1))
    xi_l=ell(s)+max((s-j)*(S_l+2)+2*sum(gam[p:p+j-1])+gam[p+j-1] for j in range(1,s+1))
    alpha_d=max(point_d,(p+1)*D_d+xi_d)
    alpha_l=1+max(point_l,(p+1)*D_l+xi_l)
    t=2*c['guard_weight']; a_l=2*c['guard_log_norm']+ell(b)
    degree=0; log_norm=0; tail_dominated=0; norm_tail_dominated=0
    for r in range(1,b+1):
        dr=(1<<s)*r
        H_d=dr*(r*t+alpha_d+1)
        H_l=dr*(r*a_l+ell(r)+alpha_l+ell(n)+1)
        if r==b:
            degree+=H_d; log_norm+=H_l
        else:
            tail_dominated += H_d < b*t
            norm_tail_dominated += H_l < b*a_l
            degree+=2*max(H_d,b*t)
            log_norm+=2*max(H_l,b*a_l)+ell(b+1)
    U_degree=(1<<s)*b*b
    V=c['total_variables']
    support=math.comb(degree+V,V)-math.comb(degree-U_degree+V-1,V)
    final_degree=degree+int(c['multiply_by_input'])
    return dict(name=c['name'],total_variables=V,point_rank=b,full_rank=n,
        degree_before_input_factor=degree,degree_bound=final_degree,
        degree_strict_power_of_two=final_degree.bit_length(),U_degree_bound=U_degree,
        support_bound=str(support),support_strict_power_of_two=support.bit_length(),
        coefficient_l1_log2_bound=str(log_norm),coefficient_height_double_power_exponent=log_norm.bit_length(),
        norm_bound_scope=c['norm_bound_scope'],old_degree_bound=c['old_degree_bound'],
        degree_tail_dominated_cases=tail_dominated,norm_tail_dominated_cases=norm_tail_dominated,
        quantities=dict(point_root_degree=Z_d,point_root_log_norm=Z_l,
            radicand_bound_degree=S_d,radicand_bound_log_norm=S_l,
            discriminant_separation_exponent=k,D_degree=D_d,D_log_norm=D_l,
            C_degree=C_d,C_log_norm=C_l,Q_degree=Q_d,Q_log_norm=Q_l,
            separator_degree=alpha_d,separator_log_norm=alpha_l,
            guard_square_degree=t,characteristic_coefficient_log_slope=a_l),
        status='Upper bounds, not expanded degrees or support counts. The rational projection is proved in the companion paper.',
        arithmetic_scope='The original arithmetic assumptions and sufficient coefficient thresholds are unchanged.')

RECIPE={
 'coefficient_ring':'Z[retained base coordinates]; fixed source parameters are coefficients',
 'source_fields':['coefficient_dag','monic_relations','materialized_guard_node','external_variables','source_finite_parameters'],
 'source_interpretation':'Use only the native algebra, coefficient circuit and nonzero condition from the pinned source; replace its old elimination formula.',
 'source_monic_relations':'Each relation is Z^d plus the sum of coefficient_nodes_ascending[k]*Z^k for 0<=k<d. For a pole relation q_j^2+a_0=0, use c_j=-a_0.',
 'parameter_family':'For a different permitted fixed parameter, run the source builder at the pinned commit with that parameter, retain its native coefficient algebra and nonzero condition, and apply these same finite operations. The degree weights remain uniform as certified by the source; fixture coefficient-norm bounds do not become uniform.',
 'B':'R[z_1,...,z_p]/(f_1,...,f_p)',
 'A':'B[q_1,...,q_s]/(q_j^2-c_j)',
 'guard':'G=g*q_1*...*q_s; g is the coefficient of q_1*...*q_s in the monic normal form of G; all other pole-degree components vanish.',
 'basis':'lexicographic monomials in native generator order, with exponent below the corresponding monic degree',
 'T':'g^2 * product(c_j)',
 'a_j':'coefficient of v^j in det_B(I-v*M_T), for 0<=j<=b',
 'Z':'2 + sum of squares of all nonleading coefficients of all f_i',
 'S':'b*(1 + sum_{j=1}^s sum_{u,v=1}^b (M_c_j^B[u,v])^2)',
 'delta_i':'Disc(f_i)=(-1)^(d_i*(d_i-1)/2)*Res(f_i,f_i_prime)',
 'kappa':'max_i (d_i*(d_i-1)-2)/2',
 'D':'product(delta_i^2)',
 'K':'(2*Z)^kappa * product(1+delta_i^2)',
 'C':'D+4*Z*K',
 'J':'4*S',
 'Q':'2*S*J^(s-1)',
 'Xi':'sum_{j=1}^s J^(s-j)*(product_{k<j} c_k)*q_j',
 'Omega':'Q*(C^(p+1)+sum_{i=1}^p D^i*C^(p+1-i)*z_i)+D^(p+1)*Xi',
 'E_r':'a_r - sum_{j=0}^r a_j*T^(r-j)',
 'omega_r':'E_r*Omega',
 'H_r':'sum_{j=0}^{2^s*r} (-U)^j * sum of all j-by-j principal minors of M_omega_r^A; the j=0 term is 1',
 'P':'H_b * product_{r=1}^{b-1}(H_r^2+sum_{j=r+1}^b a_j^2)',
 'final':'P for the 25- and 27-variable sources; input.X*P for the direct-input 13-variable sources',
 'scope':'Finite integer-polynomial operations. No numerical root selection, division, change of arithmetic premise, or additional variable.'
}

def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--source-checkout',type=Path);args=ap.parse_args()
    inputs=json.loads((HERE/'inputs.json').read_text()); reports=[]
    for c in inputs:
        if args.source_checkout: authenticate(c,args.source_checkout)
        result=bounds(c);reports.append(result)
        folder=HERE/c['name'];folder.mkdir(exist_ok=True)
        spec=dict(format='integer-polynomial-indexed-finite-algebra/triangular-v24',
            source_commit=c['source_commit'],source_specification=c['source_specification'],
            source_specification_sha256=c['source_specification_sha256'],
            total_variables=c['total_variables'],multiply_by_input=c['multiply_by_input'],
            fixed_parameter=c['fixed_parameter'],
            construction=RECIPE,bounds=result)
        (folder/'polynomial-specification.json').write_text(json.dumps(spec,indent=2)+'\n')
        (folder/'construction-certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    report=dict(schema='triangular-elimination-bounds/v24',inputs_sha256=sha256(HERE/'inputs.json'),
        complete_checkout_sources_authenticated=bool(args.source_checkout),constructions=reports)
    (HERE/'bounds.json').write_text(json.dumps(report,indent=2)+'\n')
    for r in reports:
        print(r['name'],r['degree_bound'],'<2^'+str(r['degree_strict_power_of_two']),
              'support <2^'+str(r['support_strict_power_of_two']),
              'log2 l1 <=',r['coefficient_l1_log2_bound'],
              'height <2^(2^'+str(r['coefficient_height_double_power_exponent'])+')')
if __name__=='__main__': main()
