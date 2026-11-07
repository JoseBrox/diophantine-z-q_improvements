#!/usr/bin/env python3
"""Independent semantic audit of the final correction-free sources.

No producer is imported. The preferred common program is specialized at each
of its two fixed profiles and compared, statement for statement, with the
independently audited profile source after precisely the proved input-map,
normalizer and correction-deletion changes. Small arithmetic checks are exact.
"""
import ast
from copy import deepcopy
import gzip
import json
from pathlib import Path

from check_source_semantics import (HERE, require, digest, statements, normal,
                                    methods, audit_AST, audit_identities)
from check_height_profiles import PROFILES, audit_profile, Integers
from verify_explicit_height_constant import verify as verify_explicit_height_constant

ARITHMETIC = 'Inherited H19<2^2093448 contact-height bound and simultaneous prime-pattern hypotheses; odd-product identity, correction-free input map, and profile cutoff inequalities proved separately'
SOURCES = [
    ('source-29-preferred.json.gz','56f7685781adf0ed07cd3b2f6151110354998555dbf63a34fbea6d15edddc6a3'),
    ('source-31-preferred.json.gz','d62fb492a67271c8a3da695ea5d28a8af8e63480a5fe551a963a7e4299a37a5c'),
]


class Specialize(ast.NodeTransformer):
    def __init__(self,p):
        self.values={'high_order':p['high'],'input_order':p['input'],
            'high_precision':p['high_truncation'],'input_precision':p['input_truncation'],
            'scalar_order':p['scalar'],'height_exponent':p['working_height_exponent'],
            'anchor_exponent':2093449,'anchor_q':26}
    def visit_Attribute(self,node):
        if isinstance(node.value,ast.Name) and node.value.id=='self' and node.attr in self.values:
            return ast.Constant(value=self.values[node.attr])
        return self.generic_visit(node)


class FoldLists(ast.NodeTransformer):
    def visit_BinOp(self,node):
        node=self.generic_visit(node)
        if isinstance(node.op,ast.Add) and isinstance(node.left,ast.List) and isinstance(node.right,ast.List):
            return ast.List(elts=node.left.elts+node.right.elts,ctx=ast.Load())
        if (isinstance(node.op,ast.Mult) and isinstance(node.left,ast.List)
                and isinstance(node.right,ast.Constant) and type(node.right.value) is int):
            return ast.List(elts=node.left.elts*node.right.value,ctx=ast.Load())
        return node


def canonical(body):
    return normal([FoldLists().visit(deepcopy(n)) for n in body])


def target_name(n):
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name):return n.targets[0].id
    return None


def metadata_key(n):
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript):
        t=n.targets[0]
        if isinstance(t.value,ast.Name) and t.value.id=='result' and isinstance(t.slice,ast.Constant):return t.slice.value
    return None


def common_constructor(new):
    old=methods(HERE/'build_source.py')['__init__'].body
    expected=deepcopy(old[:1])+statements('''
        if anchor == 'finite':
            self.high_order, self.input_order = 128, 24
            self.high_precision, self.input_precision = 128, 24
            self.scalar_order, self.height_exponent = 100485552, 24
        else:
            self.high_order, self.input_order = 39, 10
            self.high_precision, self.input_precision = 40, 12
            self.scalar_order, self.height_exponent = 20, 19
        self.anchor_exponent = 2093449
        self.anchor_q = 26
    ''')+deepcopy(old[1:25])+statements('self.correction = self.c.rational(1)')+deepcopy(old[27:])
    require(normal(expected)==normal(new['__init__'].body),'Common constructor has an unaccounted change')


def expected_build(ref,p):
    answer=[]
    for original in ref['build'].body:
        n=deepcopy(original);name=target_name(n);key=metadata_key(n)
        if name=='beta':
            answer+=statements('beta=216*self.X**4+450459')
        elif name in ('corrections','primes') or isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='mask':
            continue
        elif isinstance(n,ast.If) and isinstance(n.test,ast.Attribute) and n.test.attr=='normalize_scalar' and any(target_name(k)=='delta_beta' for k in n.body):
            answer+=statements('''
                if self.normalize_scalar:
                    raw_contact = rbeta
                    delta_beta = 1+(17*rbeta)**2
                    self.c.nonzero(delta_beta, 'scalar.positive normalizer')
                    rbeta = 102**2*rbeta/(delta_beta**2)
                    self.events.append({'operation': 'normalized_scalar_contact',
                        'raw_contact': self.rr(raw_contact),
                        'positive_normalizer': self.rr(delta_beta),
                        'normalized_contact': self.rr(rbeta),
                        'fixed_square_root': '102',
                        'formula': '102^2*r/(1+(17*r)^2)^2', 'correction': 1})
            ''')
        elif name=='result':
            for i,(k,v) in enumerate(zip(n.value.keys,n.value.values)):
                if isinstance(k,ast.Constant) and k.value=='additional_arithmetic_input':n.value.values[i]=ast.Constant(ARITHMETIC)
                if isinstance(k,ast.Constant) and k.value=='finite_parameters':
                    pairs=[(kk,vv) for kk,vv in zip(v.keys,v.values) if kk is None or kk.value!='scalar_correction']
                    v.keys=[k for k,_ in pairs];v.values=[v for _,v in pairs]
            answer.append(n)
        elif isinstance(n,ast.If) and isinstance(n.test,ast.Attribute) and n.test.attr=='normalize_scalar':
            for st in n.body:
                if metadata_key(st)=='scalar_normalization_proof':st.value.value='../../common_conic/scalar_normalization.tex'
            answer.append(n)
        elif key=='beta_formula':
            n.value.value='216*input.X^4+450459';answer.append(n)
        elif key=='optimized_cutoff_proof':continue
        elif key=='arithmetic_profile':
            profile={'height_exponent':p['working_height_exponent'],'height_log2_upper_bound':2093448,
                'formal_orders':[p['input_truncation']]+[p['high_truncation']]*3,
                'assigned_comparison_orders':[p['input']]+[p['high']]*3,
                'scalar_order':p['scalar'],'inherited_height_exponent':19,
                'new_asymmetric_depth_prime_separation_used':False}
            answer+=statements("result['arithmetic_profile']="+repr(profile))
        elif isinstance(n,ast.Return):
            answer+=statements('''
                result['correction_free_input_map']=True
                result['scalar_correction_fixed']=1
                result['profile_cutoff_proof']='../height_cutoff.tex'
                return result
            ''')
        else:
            if isinstance(n,ast.If) and isinstance(n.test,ast.Compare):
                # The fixed source's semilocal coefficient uses q=26 in both profiles.
                for st in ast.walk(n):
                    if isinstance(st,ast.Constant) and st.value==9566463:st.value=2093449
                    if isinstance(st,ast.BinOp) and isinstance(st.op,ast.Pow) and isinstance(st.left,ast.Constant) and st.left.value==2 and isinstance(st.right,ast.Constant) and st.right.value in (23,26):
                        st.right.value=26
            answer.append(n)
    return answer


def arithmetic_checks():
    C=450459;r=lambda b:b*(b-1)*(b-2401)*(32*b+343)*(2*b-1)
    require(C>2401 and C%8==3 and C%27==18,'Input-map congruences differ')
    require((32*C+343)==17**2*49879 and 49879%17==1,'17-adic lift differs')
    rows=[]
    for x in range(17):
        fourth=pow(x,4,17);b=(216*fourth+C)%17;rr=r(b)%17
        rows.append([x,fourth,b,rr])
        require((x==0 and b==10 and rr==0) or (x!=0 and pow(rr,8,17)==1),'Bad 17-adic residue')
    require({a[1] for a in rows}=={0,1,4,13,16},'Fourth-power image differs')
    require(216==2**3*3**3 and 216%8==0 and 216%27==0, 'Integrality or small-prime coefficient failed')
    for b in range(3,32,8):require(r(b)%4==0 and (r(b)//4)%8==1,'2-adic square unit differs')
    require(r(18)%9==0 and (r(18)//9)%3==1,'3-adic square unit differs')
    require((10*9*6*2)%17==9 and 102**2<17**4,'Local multiplier or real bound differs')
    return {'integer_input_residues_mod17':rows,'local_square_units_checked':True,
        'normalizer_real_bound_numerator':102**2,'normalizer_real_bound_denominator':17**4,
        'scalar_correction_fixed_to_one':True}


def main():
    audit_AST(); audit_identities()
    exact_height=verify_explicit_height_constant()
    require(exact_height['height_constant_bit_length']==2093448,'Wrong exact H19 bit length')
    h=2093448;E=h+1
    require(48*E==100485552 and E==2093449,'Finite-cutoff parameter arithmetic failed')
    require(h>=20 and 28**4<2**20 and 16<18,'Finite-cutoff rational inequalities failed')
    require(2+3*(2**25-1)>40*(h+6),'Semilocal cutoff does not dominate (64H)^20')
    require(2*19<39 and 19<2*10 and 19<20,'Small-order strict thresholds failed')
    require(5*49<256 and 34<64,'Small-order constants failed')
    require(40>=39 and 12>=10 and 128<76176,'Formal precision or prime threshold failed')
    new=methods(HERE/'build_preferred_source.py');common_constructor(new)
    records=[]
    for historical_profile,(filename,sha) in zip(PROFILES,SOURCES):
        audit_profile(historical_profile)
        p=dict(historical_profile)
        if p['name']=='height':
            p.update(scalar=100485552,anchor_exponent=2093449)
        ref=methods(HERE/p['builder'])
        constants={2093966:2093448,2093967:2093449,100510416:100485552}
        ref={name:Integers(constants).visit(deepcopy(method)) for name,method in ref.items()}
        require(set(new)==set(ref),'Preferred method list differs')
        specialized={k:Specialize(p).visit(deepcopy(v)) for k,v in new.items()}
        for name in set(new)-{'__init__','build'}:
            require(canonical(specialized[name].body)==canonical(ref[name].body),'Unaccounted preferred method: '+name)
        require(canonical(specialized['build'].body)==canonical(expected_build(ref,p)),
                'Preferred source has an unaccounted mathematical change: '+p['name'])
        raw=gzip.decompress((HERE/filename).read_bytes());s=json.loads(raw)
        require(digest(raw)==sha,'Preferred source checksum differs')
        require(s['total_polynomial_variables_after_finite_algebra']==p['total'],'Preferred count differs')
        require(len(s['finite_parameters'])==4 and all(v==[0,1] for v in s['finite_parameters'].values()),'Correction choices remain')
        require(not any(n[0]=='parameter' and n[1]=='scalar_correction' for n in s['coefficient_dag']),'Correction parameter remains in DAG')
        require(s['beta_formula']=='216*input.X^4+450459' and s['scalar_correction_fixed']==1,'Wrong input map')
        require(s['comparison_orders']==[1]*10+[p['input']]+[p['high']]*3+[p['input'],p['high']], 'Wrong preferred comparison orders')
        records.append({'profile':p['name'],'source':filename,'source_sha256':sha,'total_variables':p['total'],
                        'original_finite_branches':16,'source_method_changes_checked_exactly':True})
    report={'status':'passed','sources':records,'arithmetic_checks':arithmetic_checks(),
        'explicit_height_constant_check':exact_height,
        'point_conic_and_direct_polynomial_identities_checked':True,
        'exact_cutoff_parameter_inequalities':True,
        'builder_sha256':digest((HERE/'build_preferred_source.py').read_bytes()),
        'checker_sha256':digest(Path(__file__).read_bytes()),
        'scope':'Exact implementation-semantic changes, rational identities, and exact finite arithmetic are checked. The written proof establishes the input integrality equivalence and all local implications; inherited group, height and prime-pattern inputs remain assumptions. The separate generic checker verifies source-to-polynomial conversion and bounds.'}
    (HERE/'preferred-source-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
