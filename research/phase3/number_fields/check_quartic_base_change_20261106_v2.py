#!/usr/bin/env python3
"""Check the Gaussian sections of the fresh final quartic tables.

Every specialization is computed from both the complete expanded table
and the quadratic residual list. The previous four receipts are unchanged.
The reused helpers perform only exact sparse arithmetic over Q(i)[T,S];
no quartic producer is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import gzip
import importlib.util
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
_ms=importlib.util.spec_from_file_location('gaussian_arithmetic',HERE/'check_quartic_base_change_20261106_v1.py')
arith=importlib.util.module_from_spec(_ms)
_ms.loader.exec_module(arith)


def restrict(terms,u,v,offsets):
    out={}
    allowed={0,u,v}|set(offsets)
    for mon,k,c in terms:
        if not set(mon)<=allowed:continue
        exponent=k
        for coordinate,(coefficient,power) in offsets.items():
            count=mon.count(coordinate)
            c*=coefficient**count
            exponent+=power*count
        key=(mon.count(0),mon.count(u),mon.count(v),exponent)
        out[key]=out.get(key,0)+c
    return {m:c for m,c in out.items() if c}


def check(path,u,v,offsets):
    raw=gzip.decompress(path.read_bytes());s=json.loads(raw)
    expanded=restrict(s['expanded_polynomial'],u,v,offsets)
    residual_sum={}; restricted=[]
    for row in s['residuals']:
        r=restrict(row['terms'],u,v,offsets);restricted.append(r)
        for m,c in arith.square_three(r).items():residual_sum[m]=residual_sum.get(m,0)+c
    residual_sum={m:c for m,c in residual_sum.items() if c}
    assert expanded==residual_sum
    assert expanded[(0,2,0,0)]==expanded[(0,0,2,0)]==1
    remainder={m:c for m,c in expanded.items() if m not in ((0,2,0,0),(0,0,2,0))}
    assert all(a==b==0 for t,a,b,k in remainder)
    R={(t,k):(F(c),F(0)) for (t,a,b,k),c in remainder.items()}
    one={(0,0):(F(1),F(0))}
    upoly=arith.scale(arith.add(one,arith.scale(R,-1)),F(1,2))
    vre=arith.scale(arith.add(one,R),F(1,2))
    vpoly={m:(-b,a) for m,(a,b) in vre.items()}
    assert arith.substitute(expanded,upoly,vpoly)=={}
    independently_substituted={}
    for r in restricted:
        evaluated=arith.substitute(r,upoly,vpoly)
        independently_substituted=arith.add(independently_substituted,arith.multiply(evaluated,evaluated))
    assert independently_substituted=={}
    return {'path':str(path.relative_to(ROOT)),'source_sha256':sha256(raw).hexdigest(),
            'total_variables':len(s['variables']),'residual_count':len(s['residuals']),
            'gaussian_witness_indices':[u,v],
            'other_nonzero_witnesses':{str(i):{'coefficient':c,'power_of_S':e} for i,(c,e) in offsets.items()},
            'fixed_constants':s['fixed_constants'],
            'restriction_terms_T_u_v_S':[[list(m),c] for m,c in sorted(expanded.items())],
            'gaussian_witness_rule':'u=(1-R)/2; v=i*(1+R)/2; all remaining witnesses zero except the listed offsets',
            'conclusion':'The literal quartic has input projection equal to the entire field over every characteristic-zero field containing i.',
            'scope':'Generic exact identity from the expanded polynomial and independently squared residuals; not a claim about equivalence of arbitrary nonreal SOS systems under variable elimination.'}


def main():
    rows=[check(ROOT/'research/phase3/quartic/quartic-direct-translated/polynomial.json.gz',72,73,{55:(8,1),56:(-2,1),57:(-6,1)}),
          check(ROOT/'research/phase3/quartic/quartic-direct-small-coefficients-1338/polynomial.json.gz',95,96,{}),
          check(ROOT/'research/phase3/quartic/quartic-direct-small-coefficients-1335/polynomial.json.gz',92,93,{})]
    result={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'arithmetic_helper_sha256':sha256((HERE/'check_quartic_base_change_20261106_v1.py').read_bytes()).hexdigest(),
            'cases':rows,'previous_artifacts':'The four v1 checks and their receipts are unchanged.'}
    target=HERE/'quartic-base-change-verification_20261106_v2.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','total_variables':[r['total_variables'] for r in rows],
                      'receipt':str(target.relative_to(ROOT))}))


if __name__=='__main__':main()
