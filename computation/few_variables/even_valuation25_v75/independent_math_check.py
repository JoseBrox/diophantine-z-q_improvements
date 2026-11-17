#!/usr/bin/env python3
"""Producer-free structural and finite semantic audit of the revised general25.

The generic modular assignments below check formal detector arithmetic; they
are not point witnesses or an exhaustive identity proof. The separate native
checker covers actual point characters, and independent_review.md supplies the
arithmetic transfer argument.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import comb, prod
from pathlib import Path
from random import Random
import json

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]

def event(source,name):
    return next(e for e in source['events'] if e['operation']==name)

def evaluate(source,p,seed):
    rng=Random(p+1000003*seed)
    assignments=[rng.randrange(1,p) for _ in source['variables']]
    values=[]
    for op,*args in source['coefficient_dag']:
        if op=='int':v=args[0]
        elif op=='parameter':v=args[1]
        elif op=='variable':v=assignments[args[0]]
        elif op=='neg':v=-values[args[0]]
        elif op=='add':v=sum(values[i]for i in args)
        elif op=='mul':v=prod(values[i]for i in args)
        elif op=='pow':v=pow(values[args[0]],args[1],p)
        else:raise AssertionError(op)
        values.append(v%p)
    return assignments,values

def detector_check(source,p,seed):
    assignments,values=evaluate(source,p,seed)
    def inv(v):return pow(v,-1,p)
    def rat(o):return values[o['numerator']]*inv(values[o['denominator']])%p
    def field(o):return tuple(rat(q) for q in o)
    def add(a,b):return((a[0]+b[0])%p,(a[1]+b[1])%p)
    def mul(a,b):return((a[0]*b[0]+2*a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0])%p)
    def scale(a,c):return(a[0]*c%p,a[1]*c%p)
    def const(f):
        f=Fraction(f);return f.numerator*inv(f.denominator)%p
    names={v['name']:v['index']for v in source['variables']}
    X=assignments[names['input.X']];slope=assignments[names['slope.lambda']]
    L=source['family_parameter']['value']
    beta=(216*pow(X,4,p)+450459)%p
    raw=prod([beta,beta-1,beta-2401,32*beta+343,2*beta-1])%p
    rho_den=(1+17*(pow(76249,(L+1)//2,p)+1)*raw)%p
    rho=pow(102,2,p)*pow(76249,L,p)*raw*pow(rho_den,-2,p)%p
    hs=event(source,'combined_height_scales')
    roots=[e for e in source['events']if e['operation']=='point_block'and e['name']in('A','S','T','Z')]
    trace=2*sum(rat(e['x'][0])for e in roots)%p
    assert rat(hs['beta'])==beta and rat(hs['raw_scalar_contact'])==raw
    assert rat(hs['scalar_contact'])==rho and rat(hs['trace'])==trace
    scales=[1,(1+rho*trace*trace)%p]
    assert [rat(q)for q in hs['scales']]==scales
    tests=event(source,'comparison_and_scalar_tests')
    C=[field(q)for q in tests['comparison']]
    S=[rat(q)for q in tests['scalar']]
    shared=[]
    for e in (e for e in source['events']if e['operation']=='combined_detector'):
        j=e['index'];t=scales[j]*slope%p;delta=(t-e['normalizing_point'])%p
        F=prod((t-const(c))%p for c in e['contacts'])%p
        R=F*pow(delta,-10,p)%p;q=rho*R%p
        assert rat(e['scale'])==scales[j]and rat(e['argument'])==t
        assert rat(e['delta'])==delta and rat(e['F'])==F
        assert rat(e['contact_function'])==R and rat(e['combined_coefficient'])==q
        W=(1,0)
        for i,(c,a)in enumerate(zip(C,tests['comparison_orders'])):
            weight=pow(delta,-2,p)*pow(q,1-2*a,p)%p
            assert rat(e['comparison_weights'][i])==weight
            numerator=c if i<10 else mul(c,c)
            W=mul(W,add((1,0),scale(numerator,weight)))
        G=[]
        for i,(s,k)in enumerate(zip(S,tests['scalar_orders'])):
            g=pow(R,k,p)*(R*s%p)*inv((1+R*s)%p)%p
            assert field(e['normalized_scalar'][i])==(g,0)
            weight=pow(q,1-2*k,p)
            assert rat(e['scalar_weights'][i])==weight
            W=scale(W,(1+g*g*weight)%p);G.append(g)
        assert W==field(e['product_components'])
        norm=(W[0]*W[0]-2*W[1]*W[1])%p
        traceW=2*W[0]*inv(norm)%p
        assert rat(e['pole_input'])==4*q*pow(traceW,-2,p)%p
        shared.append({'q':q,'R':R,'delta':delta,'G':G,'C':C,'S':S})
    assert len(shared)==2
    return shared

def main():
    sp=HERE/'specification/source.json';source=json.loads(sp.read_text())
    oldpath=REPO/'computation/few_variables/full_auxiliary25_v72/specification/source.json'
    old=json.loads(oldpath.read_text())
    newnodes=source['coefficient_dag'];oldnodes=old['coefficient_dag']
    prefix=next(i for i,(a,b)in enumerate(zip(newnodes,oldnodes))if a!=b)
    assert prefix==2567 and len(newnodes)==6039
    assert source['variables']==old['variables']
    assert source['finite_blocks'][:9]==old['finite_blocks'][:9]
    assert {g for g in source['guard_numerators']if g<prefix}=={g for g in old['guard_numerators']if g<prefix}
    labels=lambda d:Counter(name for _,name in d['guard_descriptions']if name!='division')
    assert labels(source)==labels(old)
    assert len(source['guard_numerators'])==len(old['guard_numerators'])==101
    for name in ['point_block','combined_height_scales']:
        assert [e for e in source['events']if e['operation']==name]==[e for e in old['events']if e['operation']==name]
    tests=dict(event(source,'comparison_and_scalar_tests'))
    assert tests.pop('comparison_powers')==[1]*10+[2]*6
    assert tests==event(old,'comparison_and_scalar_tests')
    assert tests['comparison_orders']==[1]*11+[3]*3+[1,3]
    assert tests['scalar_orders']==[1]*4+[3]*2
    final=json.loads((HERE/'specification/polynomial.json').read_text())
    policy=final['terminal_root_policy'];poles=source['finite_blocks'][-2:]
    assert policy['suppressed_source_guard_nodes']==[poles[-1]['generator_node']]
    assert poles[0]['generator_node']in source['guard_numerators']
    assert policy['zero_terminal_root_allowed']and policy['preceding_radicands_required_units']
    assert not policy['terminal_square_multiplier_independently_required_nonzero']
    b=final['bounds'];rank=4**9*4
    assert b['full_rank']==b['separator_variable_degree_bound']==rank==1048576
    assert b['degree_bound']==rank*(4637555553+170132+1)==4863007848923136
    assert b['total_variables']==25 and b['guard_factors']==128 and b['integer_content']==1
    D=b['degree_bound'];support=comb(D+25,25)-comb(D-rank+24,25)
    assert support==int(b['monomial_upper_bound'])and support<2**1192
    assert final['multiply_by_input']is False
    completed=[]
    for p in [1000000007,1000000009]:
        for seed in range(1,65):
            detector_check(source,p,seed)
            completed.append([p,seed])
    report={'schema':'general25-even-valuation-independent-math/v75','status':'PASS','producer_modules_imported':False,'source_sha256':sha256(sp.read_bytes()).hexdigest(),'parent_source_sha256':sha256(oldpath.read_bytes()).hexdigest(),'unchanged_prefix_nodes':prefix,'all_point_blocks_variables_and_precomparison_guards_equal':True,'all_16_field_tests_6_scalar_tests_and_orders_equal':True,'nondivision_guard_label_multiset_equal':True,'native_guards':101,'only_suppressed_native_guard':'detector1.q','nonterminal_pole_guard_retained':True,'generic_modular_assignments':len(completed),'detector_products_reconstructed':2*len(completed),'generic_assignment_cases':completed,'independently_reconstructed':['beta','rho','trace scale','both ten-contact functions','all field and scalar weights','all normalized scalar numerators','both revised detector products','both reciprocal-trace pole inputs'],'degree_upper_bound':b['degree_bound'],'support_strict_power_of_two':1192,'scope':'Exact structural prefix/guard comparisons and exact finite modular semantic evaluations. Generic assignments are not actual point witnesses and are not an exhaustive polynomial identity proof. The separate native checker and the written proof review supply their complementary stated assertions; no 21-variable realization is asserted.'}
    (HERE/'independent_math_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ['status','unchanged_prefix_nodes','generic_modular_assignments','detector_products_reconstructed','degree_upper_bound']},indent=2))

if __name__=='__main__':main()
