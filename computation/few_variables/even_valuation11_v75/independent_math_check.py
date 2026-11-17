#!/usr/bin/env python3
"""Producer-free source-prefix, guard-policy and symbolic identity checks."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]

def digest(p):return sha256(p.read_bytes()).hexdigest()

def main():
    x,y,d,u,delta,X=s.symbols('x y d u delta X',nonzero=True)
    # These identities justify both direct fraction compilation and exact
    # equivalence of the new guards on the already guarded old open set.
    assert s.cancel((1/x)/(1+u/x)-1/(x+u))==0
    assert s.cancel((delta**2/X)/(1+u*delta**2/X)-delta**2/(X+u*delta**2))==0
    assert s.cancel((1+u/x)-(x+u)/x)==0
    assert s.cancel((1+u*delta**2/X)-(X+u*delta**2)/X)==0
    # Check the identity used to obtain positive difference abscissae at
    # every real point character of the original completeness subfamily.
    xq,xr,yq,yr=s.symbols('xq xr yq yr')
    numerator=(xq*yr+xr*yq)**2-xq*xr*((yq+yr)**2-(xq+xr)*(xq-xr)**2)
    reduced=s.expand(numerator).subs({yq**2:xq**3-d*xq,yr**2:xr**3-d*xr})
    assert s.expand(reduced)==0
    assert s.expand((11-6*s.sqrt(2))*(11+6*s.sqrt(2)))==49

    variants=[]
    for k,folder,oldfolder,expected_nodes,expected_degree in [
        (9,'specification','full_auxiliary11_v71/specification',1865,230932097),
        (7,'seven_contact','seven_contact11_v74/specification',1815,356146817)]:
        source_path=HERE/folder/'source.json'
        source=json.loads(source_path.read_text())
        oldpath=REPO/'computation/few_variables'/oldfolder/'source.json'
        old=json.loads(oldpath.read_text())
        newnodes=source['coefficient_dag'];oldnodes=old['coefficient_dag']
        prefix=next(i for i,(a,b) in enumerate(zip(newnodes,oldnodes))if a!=b)
        assert prefix==(963 if k==9 else 942)
        assert {g for g in source['guard_numerators']if g<prefix}=={g for g in old['guard_numerators']if g<prefix}
        for operation in ['point_block','moving_contact_height']:
            assert [e for e in source['events']if e['operation']==operation]==[e for e in old['events']if e['operation']==operation]
        event=next(e for e in source['events']if e['operation']=='balanced_actual_detector')
        oldevent=next(e for e in old['events']if e['operation']=='balanced_actual_detector')
        assert event['original_tests']==oldevent['original_tests']
        labels={name:node for node,name in source['guard_descriptions']}
        required=['height.M','height.nonzero signed argument','contact.G','contact.H','contact.u','contact.one_plus_u','detector.product norm','detector.trace numerator','intrinsic.input','intrinsic.Y.denominator']+[f'balanced{i}.denominator norm' for i in range(6)]
        assert all(name in labels and labels[name]in source['guard_numerators']for name in required)
        final=json.loads((HERE/folder/'polynomial.json').read_text())
        policy=final['terminal_root_policy'];pole=source['finite_blocks'][-1]
        assert policy['suppressed_source_guard_nodes']==[pole['generator_node']]
        assert policy['zero_terminal_root_allowed'] and policy['preceding_radicands_required_units']
        assert not policy['terminal_square_multiplier_independently_required_nonzero']
        b=final['bounds']
        assert b['total_variables']==11 and b['full_rank']==128
        assert b['degree_bound']==1+128*(b['scalar_guard_degree_bound']+b['separator_degree_bound']+1)==expected_degree
        assert b['integer_content']==1
        assert len(newnodes)==expected_nodes and len(source['guard_numerators'])==32
        alpha=Fraction(997,1001);kappa=Fraction(1001,1000);power=16 if k==7 else 8
        Q=(2*kappa-1)/(power-kappa*(power//2+2))
        margin=(k-6-Fraction(3,100))/2-Q*(Fraction(201,100)+1/(2*alpha))
        assert margin==(Fraction(38695561,597203000) if k==7 else Fraction(44272779,198801800))
        variants.append({'contacts':k,'source_sha256':digest(source_path),'unchanged_source_sha256':digest(oldpath),'unchanged_prefix_nodes':prefix,'all_point_and_contact_events_equal':True,'all_six_original_tests_equal':True,'precontact_guards_equal':True,'required_guard_labels':required,'only_suppressed_native_guard':'terminal intrinsic.Y','nodes':expected_nodes,'native_guards_before_terminal_suppression':32,'degree_upper_bound':expected_degree,'height_margin':str(margin)})
    report={'schema':'even-valuation-independent-math/v75','status':'PASS','producer_modules_imported':False,'direct_fraction_and_guard_identities':True,'Kummer_difference_identity_mod_curve_equations':True,'curve_coefficient_norm':49,'global_K_square_assumption_used':False,'variants':variants,'scope':'Exact source-prefix and guard-policy verification plus symbolic algebra. The parity and arithmetic transfer proofs are reviewed in independent_review.md; retained infinite premises and unresolved actual-trace realization remain explicit.'}
    (HERE/'independent_math_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
