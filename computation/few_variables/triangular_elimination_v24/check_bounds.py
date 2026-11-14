#!/usr/bin/env python3
"""Independent closed-sum checks of the numerical degree certificates.
Does not import build.py. Uses exact integers; requires only the standard library.
"""
import json, math, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

def ceil_log(n): return (n-1).bit_length()
def s1(n): return n*(n+1)//2
def s2(n): return n*(n+1)*(2*n+1)//6

def verify(c,r):
    assert c['name']==r['name']
    p,s=c['p'],c['s'];ds=c['point_degrees'];b=math.prod(ds);d=2**s;n=d*b
    w=c['generator_weights'];g=c['generator_log_norms'];u=sum(di*(di-1)*wi for di,wi in zip(ds,w));v=sum(c['discriminant_log_norms'])
    zd=2*max(di*wi for di,wi in zip(ds,w));zl=ceil_log(2+sum(ds))+2*max(di*gi for di,gi in zip(ds,g))
    bd=sum((di-1)*wi for di,wi in zip(ds,w));bl=sum((di-1)*gi for di,gi in zip(ds,g))
    sd=4*max(w[p:])+2*bd;sl=ceil_log(b)+ceil_log(1+s*b*b)+4*max(g[p:])+2*bl
    k=max(di*(di-1)//2-1 for di in ds);dd=2*u;dl=2*v;cd=(k+1)*zd+dd;cl=k*(zl+1)+p+dl+zl+3
    terms_d=[s*sd+(p+1)*cd]+[s*sd+i*dd+(p+1-i)*cd+w[i-1]for i in range(1,p+1)]
    terms_d +=[(p+1)*dd+(s-j)*sd+sum(2*x for x in w[p:p+j-1])+w[p+j-1] for j in range(1,s+1)]
    ad=max(terms_d)
    point_logs=[(p+1)*cl]+[i*dl+(p+1-i)*cl+g[i-1]for i in range(1,p+1)]
    xl=ceil_log(s)+max((s-j)*(sl+2)+sum(2*x for x in g[p:p+j-1])+g[p+j-1]for j in range(1,s+1))
    al=1+max(s*sl+2*s-1+ceil_log(p+1)+max(point_logs),(p+1)*dl+xl)
    t=2*c['guard_weight'];aa=2*c['guard_log_norm']+ceil_log(b)
    h=lambda j:d*j*(j*t+ad+1)
    # Binary search the initial interval where the tail coefficients dominate.
    lo,hi=0,b
    while hi-lo>1:
        m=(lo+hi)//2
        if h(m)<b*t:lo=m
        else:hi=m
    cut=lo
    baseline=d*(t*(2*b*b*b+b)//3+(ad+1)*b*b)
    correction=2*(cut*b*t-d*(t*s2(cut)+(ad+1)*s1(cut)))
    deg=baseline+correction
    assert deg==r['degree_before_input_factor']
    assert cut==r['degree_tail_dominated_cases']
    assert deg+int(c['multiply_by_input'])==r['degree_bound']<c['old_degree_bound']
    assert ad==r['quantities']['separator_degree']
    assert al==r['quantities']['separator_log_norm']
    e=d*b*b;V=c['total_variables'];support=math.comb(deg+V,V)-math.comb(deg-e+V-1,V)
    assert e==r['U_degree_bound'] and str(support)==r['support_bound']
    assert support<2**r['support_strict_power_of_two']
    assert r['degree_bound']<2**r['degree_strict_power_of_two']
    # Exact independent summation of norm bounds, including all ceiling changes.
    norm=0;norm_cut=0
    for j in range(1,b+1):
        hj=d*j*(j*aa+ceil_log(j)+al+ceil_log(n)+1)
        if j<b and hj<b*aa:norm_cut+=1
        norm += hj if j==b else 2*max(hj,b*aa)+ceil_log(b+1)
    assert norm_cut==r['norm_tail_dominated_cases']
    assert str(norm)==r['coefficient_l1_log2_bound']
    assert norm<2**r['coefficient_height_double_power_exponent']
    return dict(name=c['name'],status='PASS',degree_bound=r['degree_bound'],tail_dominated_cases=cut,
                closed_sum_degree=deg,coefficient_l1_log2_bound=str(norm))

inputs=json.loads((HERE/'inputs.json').read_text()); report=json.loads((HERE/'bounds.json').read_text())
assert hashlib.sha256((HERE/'inputs.json').read_bytes()).hexdigest()==report['inputs_sha256']
assert len(inputs)==len(report['constructions'])==4
assert {c['name'] for c in inputs}=={'general25','explicit27','weak13','abc13'}
results=[verify(c,r)for c,r in zip(inputs,report['constructions'])]
# Deliberately corrupted bound must be rejected.
bad=dict(report['constructions'][0]);bad['degree_before_input_factor']-=1
try: verify(inputs[0],bad)
except AssertionError: rejected=True
else: rejected=False
assert rejected
out=dict(status='PASS',implementations='Direct case summation versus closed sums with a binary-searched correction interval.',
         source_bounds='Reused pinned source certificates; no arithmetic foundational audit is implied.',
         negative_control='A one-unit alteration of the degree bound is rejected.',results=results)
(HERE/'independent-bound-verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
