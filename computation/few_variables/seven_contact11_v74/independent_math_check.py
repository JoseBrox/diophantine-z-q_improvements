#!/usr/bin/env python3
"""Producer-free symbolic contact and guard-structure checks for seven contacts.

Reads the published coefficient DAG directly. No construction or existing
verification module is imported. Infinite arithmetic inputs remain premises.
"""
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import sympy as s
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]

def main():
    source_path=HERE/'specification/source.json';source=json.loads(source_path.read_text())
    old=json.loads((REPO/'computation/few_variables/full_auxiliary11_v71/specification/source.json').read_text())
    event=next(e for e in source['events']if e['operation']=='moving_contact_height')
    oldevent=next(e for e in old['events']if e['operation']=='moving_contact_height')
    Mnode=event['M']['numerator'];assert Mnode==oldevent['M']['numerator']
    assert source['coefficient_dag'][:Mnode+1]==old['coefficient_dag'][:Mnode+1]
    assert {g for g in source['guard_numerators']if g<=Mnode}=={g for g in old['guard_numerators']if g<=Mnode}
    def point_events(d):return[e for e in d['events']if e['operation']=='point_block']
    assert point_events(source)==point_events(old)
    def detector(d):return next(e for e in d['events']if e['operation']=='balanced_actual_detector')
    assert detector(source)['original_tests']==detector(old)['original_tests']
    M,z=s.symbols('M z');nodes=source['coefficient_dag'];names={v['index']:v['name']for v in source['variables']}
    @lru_cache(None)
    def value(i):
        if i==Mnode:return M
        op,*data=nodes[i]
        if op=='int':return s.Integer(data[0])
        if op=='parameter':return s.Integer(data[1])
        if op=='variable':
            assert names[data[0]]=='contact.z',(i,names[data[0]])
            return z
        if op=='neg':return -value(data[0])
        if op=='add':return s.Add(*(value(j)for j in data))
        if op=='mul':return s.Mul(*(value(j)for j in data))
        if op=='pow':return value(data[0])**data[1]
        raise AssertionError(op)
    def rat(obj):return value(obj['numerator'])/value(obj['denominator'])
    shifts=(-7,-6,-4,1,3,5,8);assert event['shifts']==list(shifts)
    a,Z=s.symbols('a Z');G=s.prod((a+c)**2-Z for c in shifts);GA=s.diff(G,a);H=s.Poly(GA/2,a,Z,domain=s.ZZ)
    assert gcd(*(int(c)for c in H.coeffs()))==1
    assert s.Poly(G,Z).degree()==7 and s.Poly(GA,Z).degree()==6
    assert s.Poly(G,Z).LC()==-1 and s.Poly(GA,Z).LC()==14*a
    assert len(set(shifts))==7 and sum(shifts)==0 and all(c+d for c in shifts for d in shifts)
    F=G.subs({a:M**8,Z:z*z});Fa=GA.subs({a:M**8,Z:z*z})
    assert s.expand(rat(event['A'])-M**8)==0
    assert s.expand(rat(event['Z'])-z*z)==0
    assert s.expand(rat(event['t'])-(M**16-z*z))==0
    assert s.expand(rat(event['G'])-F)==0
    assert s.expand(rat(event['G_A'])-Fa)==0
    assert s.expand(2*rat(event['H'])-Fa)==0
    assert s.expand(value(event['u']['numerator'])*Fa+14*F*value(event['u']['denominator']))==0
    # Verify w=u/(1+u)^2 by its numerator/denominator identities.
    # Keeping the already verified contact factors unexpanded avoids a costly
    # generic rational-function gcd in the high scale M^8.
    un=value(event['u']['numerator']);ud=value(event['u']['denominator'])
    assert value(event['w']['numerator'])==un*ud
    assert value(event['w']['denominator'])==(un+ud)**2
    labels={label:node for node,label in source['guard_descriptions']}
    required=['height.M','height.nonzero signed argument','contact.G','contact.H','contact.u','contact.one_plus_u','detector.product norm','detector.trace numerator','intrinsic.input']+[f'balanced{i}.denominator norm'for i in range(6)]
    assert all(name in labels and labels[name]in source['guard_numerators']for name in required)
    final=json.loads((HERE/'specification/polynomial.json').read_text())
    policy=final['terminal_root_policy'];pole=source['finite_blocks'][-1]
    assert policy['suppressed_source_guard_nodes']==[pole['generator_node']]
    assert policy['zero_terminal_root_allowed'] and policy['preceding_radicands_required_units']
    assert not policy['terminal_square_multiplier_independently_required_nonzero']
    assert len(source['coefficient_dag'])==1940 and len(source['guard_numerators'])==32
    assert final['bounds']['degree_bound']==1+128*(2349744+441732+1)==357309057
    kappa=Fraction(1001,1000);alpha=4/kappa-3;Q=(2*kappa-1)/(16-10*kappa);gamma=Fraction(97,200);C=Fraction(201,100)
    margin=gamma-Q*(C+1/(2*alpha));assert margin==Fraction(38695561,597203000)>0
    report={'schema':'independent-seven-contact-math/v74','status':'PASS','source_sha256':sha256(source_path.read_bytes()).hexdigest(),'point_and_original_test_DAG_prefix_exactly_v71':True,'unchanged_prefix_nodes':Mnode+1,'contact_polynomials_reconstructed_symbolically':True,'seven_shifts':list(shifts),'scale_exponent':8,'signed_argument_exponent':16,'physical_weight_degrees':[7,6],'primitive_half_derivative':True,'leading_terms':{'G':'-Z^7','G_a':'14*a*Z^6'},'guard_labels_checked':required,'only_native_guard_suppressed':'terminal intrinsic.Y','strict_height_margin':str(margin),'source_nodes':1940,'native_guards':32,'degree_bound':357309057,'scope':'Exact symbolic circuit, guard structure and finite arithmetic. Existence, height and prime-pattern theorems remain the stated retained premises; no nine-variable realization asserted.'}
    (HERE/'independent_math_certificate.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
