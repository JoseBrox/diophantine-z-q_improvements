#!/usr/bin/env python3
"""Independent audit of the fixed-prime source and its semantic change.

No producer is imported. Unchanged arithmetic routines and the unchanged
comparison construction are tied to the previously reviewed source by
canonical Python AST digests. The changed scalar contact is independently
expanded as a small polynomial identity with a formal prime-power symbol.
The integer, valuation-boundary, congruence and profile checks are exact.
"""
import ast
from functools import lru_cache
import gzip
import hashlib
import json
from math import isqrt, prod
from pathlib import Path
from fractions import Fraction

from finite_algebra_check_core import check, plus, times, power

HERE=Path(__file__).resolve().parent

def digest(x): return hashlib.sha256(x).hexdigest()
def canonical(x):
    if isinstance(x,list): return [canonical(v) for v in x]
    return ast.dump(x,include_attributes=False)
def ast_hash(x): return digest(json.dumps(canonical(x),separators=(',',':')).encode())
def methods(path):
    tree=ast.parse(path.read_text())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='PreferredBuilder')
    return {n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
def assigned_name(n):
    return n.targets[0].id if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) else None

def comparison_core(method):
    answer=[]
    for n in method.body:
        name=assigned_name(n)
        if name=='result': break
        if name in ('indexed_guards','count','degree_power'): continue
        if isinstance(n,ast.Assert): continue
        if isinstance(n,ast.If):
            if isinstance(n.test,ast.Attribute) and n.test.attr=='normalize_scalar': continue
            if any(isinstance(a,ast.Attribute) and a.attr=='anchor_kind' for a in ast.walk(n.test)): continue
        answer.append(n)
    return answer


def check_source(source):
    ell,k,m,h=76249,137715,20,2093448
    check(all(ell%d for d in range(2,isqrt(ell)+1)),'Composite fixed prime')
    check(ell>76176 and ell%24==1 and ell%17==4,'Wrong prime congruences')
    theta=[Fraction(0),Fraction(1),Fraction(2401),Fraction(-343,32),Fraction(1,2)]
    values=[]
    for t in theta:
        q=(t-450459)/216
        values.append(q.numerator*pow(q.denominator,-1,ell)%ell)
    tests=[pow(t,(ell-1)//4,ell) for t in values]
    check(all(t not in (0,1) for t in tests),'A contact root exists modulo ell')
    check(k%20==15,'Wrong valuation congruence')
    q=k//20
    minimum=2*k+1-20*q
    check(minimum==1-2*k+60*(q+1)==k+16,'Wrong piecewise valuation minimum')
    depth=(m-1)*minimum+1
    check(ell>2**16 and 16*depth>20*(h+6),'Forced index does not exceed cutoff')
    check(102**2<17**4,'Real normalization bound fails')
    check(2*19<39 and 19<2*10 and 19<20,'Invalid strict height exponents')
    check(12>=10 and 40>=39 and 40<76176,'Insufficient formal precision')
    check(5*49<256 and 34<64,'Invalid elementary cutoff constants')

    check(source['anchor_kind']=='forced_prime' and not source['indexed_guard_polynomials'],'Unexpected size condition')
    check(source['retained_base_count']==28 and source['total_polynomial_variables_after_finite_algebra']==29,'Wrong external count')
    check(source['finite_generator_count']==13 and source['monic_degree_product']=={'base':2,'exponent':22},'Wrong finite algebra')
    check(source['counts']=={'retained.input':1,'retained.point':18,'retained.slope':1,'retained.pole':6,'retained.scalar_pole':2,'finite.point':9,'finite.pole':3,'finite.scalar_pole':1},'Wrong coordinate inventory')
    check(source['comparison_orders']==[1]*10+[10,39,39,39,10,39],'Wrong assigned comparison orders')
    check(source['arithmetic_profile']=={'height_exponent':19,'height_log2_upper_bound':2093448,'formal_orders':[12,40,40,40],'assigned_comparison_orders':[10,39,39,39],'scalar_order':20,'inherited_height_exponent':19,'new_asymmetric_depth_prime_separation_used':False,'forced_prime':ell,'forced_exponent':k,'minimum_forced_contact_valuation':minimum,'minimum_scalar_index_valuation':depth},'Wrong arithmetic profile')
    check(len(source['finite_parameters'])==4 and all(v==[0,1] for v in source['finite_parameters'].values()),'Wrong conic choices')
    check(prod(len(v) for v in source['finite_parameters'].values())==16,'Wrong source branch count')
    events=source['events']
    norm=next(e for e in events if e['operation']=='scalar_norm')
    event=next(e for e in events if e['operation']=='normalized_scalar_contact')
    check(norm['orders']==[1,1,1,1,20,20] and norm['r']==event['normalized_contact'],'Changed scalar norm contact or orders')
    check(event['forced_prime']==ell and event['forced_exponent']==k and event['correction']==1,'Wrong contact constants')
    check(source['beta_formula']=='216*input.X^4+450459' and source['scalar_correction_fixed']==1,'Wrong beta or correction')
    check(next(e for e in events if e['operation']=='shifted_scalar_and_anchor_point')['point']=='S-P=4R_S','Wrong scalar point')

    nodes=source['coefficient_dag']; X={(0,):1}; Z={(1,):1}
    one={():1}; beta=plus(times({():216},power(X,4)),{():450459})
    raw=times(beta,plus(beta,{():-1}),plus(beta,{():-2401}),plus(times({():32},beta),{():343}),plus(times({():2},beta),{():-1}))
    normalizer=plus(one,times({():17**2},power(Z,2),power(raw,2)))
    @lru_cache(None)
    def expand(index):
        op,*a=nodes[index]
        if op=='int':return {():a[0]} if a[0] else {}
        if op=='variable':
            check(a[0]==0,'Noninput coordinate in scalar contact');return X
        if op=='neg':return {m:-c for m,c in expand(a[0]).items()}
        if op=='add':return plus(*(expand(t) for t in a))
        if op=='mul':return times(*(expand(t) for t in a))
        if op=='pow':
            if nodes[a[0]]==['int',ell] and a[1]>=k:
                quotient,remainder=divmod(a[1],k)
                check(quotient<=8 and remainder<=2,'Unexpected prime-power multiple')
                return times({():ell**remainder},power(Z,quotient))
            check(a[1]<100,'Unexpected large power in contact');return power(expand(a[0]),a[1])
        raise ValueError('Unexpected contact operation '+op)
    def equals(row,num,den=one):
        check(times(expand(row['numerator']),den)==times(num,expand(row['denominator'])),'Incorrect rational contact identity')
    equals(event['raw_contact'],raw)
    equals(event['positive_normalizer'],normalizer)
    equals(event['normalized_contact'],times({():102**2*ell},power(Z,2),raw),power(normalizer,2))
    check(event['positive_normalizer']['numerator'] in source['guard_numerators'],'Missing normalizer denominator guard')
    return {'prime':ell,'prime_trial_division_bound':isqrt(ell),'nonquartic_residues':values,'fourth_power_tests':tests,'normalization_exponent':k,'minimum_contact_valuation':minimum,'minimum_scalar_index_valuation':depth,'binary_cutoff_margin':16*depth-20*(h+6),'scalar_contact_identity_checked_exactly':True,'external_variables':29,'finite_rank_exponent':22,'finite_source_branches':16}


def main():
    provenance=json.loads((HERE/'source-semantic-reference.json').read_text())
    new=methods(HERE/'build_forced_prime_source.py')
    check(set(new)==set(provenance['method_names']),'Arithmetic method inventory changed')
    for name,expected in provenance['unchanged_method_ast_sha256'].items():
        check(ast_hash(new[name])==expected,'Unaccounted method change: '+name)
    check(ast_hash(comparison_core(new['build']))==provenance['comparison_core_ast_sha256'],'Unaccounted comparison or point-source change')
    raw=gzip.decompress((HERE/'source.json.gz').read_bytes())
    check(digest(raw)==provenance['fixed_source_sha256'],'Source differs from reviewed frozen expression graph')
    report=check_source(json.loads(raw))
    report.update(status='passed',source_sha256=digest(raw),builder_sha256=digest((HERE/'build_forced_prime_source.py').read_bytes()),checker_sha256=digest(Path(__file__).read_bytes()),unchanged_source_methods_checked=len(provenance['unchanged_method_ast_sha256']),comparison_source_unchanged=True,scope='Exact source identity, inventory, semantic preservation and finite arithmetic checks; mathematical infinite valuation cases and global completeness are proved in the paper under its four cited inputs.')
    (HERE/'source-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
