#!/usr/bin/env python3
"""Independent audit of the fixed-prime source and its semantic change.

No producer is imported. Unchanged arithmetic routines and the unchanged
comparison construction are tied to the previously reviewed source by
canonical Python AST digests. The changed scalar contact is independently
expanded as a small polynomial identity with a formal prime-power symbol.
The integer, valuation-boundary, congruence and profile checks are exact.
"""
import ast
import argparse
import sys
sys.dont_write_bytecode = True
from functools import lru_cache
import gzip
import hashlib
import json
from math import isqrt, prod
from pathlib import Path
from fractions import Fraction

from finite_algebra_check_core import check, plus, times, power, expander
from check_direct_points import verify_direct_points

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
    class NormalizePointDescription(ast.NodeTransformer):
        def visit_Constant(self,node):
            if node.value == 'S-P (direct difference)':
                return ast.copy_location(ast.Constant(value='S-P=4R_S'),node)
            return node
    method=NormalizePointDescription().visit(ast.parse(ast.unparse(method)).body[0])
    answer=[]
    skip_height=False
    for n in method.body:
        name=assigned_name(n)
        if name=='result': break
        if name in ('product_x','sum_x'): skip_height=True
        if name=='contacts': skip_height=False
        if skip_height: continue
        if name in ('indexed_guards','count','degree_power'): continue
        if isinstance(n,ast.Assert): continue
        if isinstance(n,ast.If):
            if isinstance(n.test,ast.Attribute) and n.test.attr=='normalize_scalar': continue
            if any(isinstance(a,ast.Attribute) and a.attr=='anchor_kind' for a in ast.walk(n.test)): continue
        answer.append(n)
    return answer


def check_source(source):
    ell,m,h=76249,20,2093448
    k=source['family_parameter']['value']
    check(type(k) is int and k>=3 and k%2==1,'Invalid fixed coefficient exponent')
    check(all(ell%d for d in range(2,isqrt(ell)+1)),'Composite fixed prime')
    check(ell>76176 and ell%24==1 and ell%17==4,'Wrong prime congruences')
    theta=[Fraction(0),Fraction(1),Fraction(2401),Fraction(-343,32),Fraction(1,2)]
    values=[]
    for t in theta:
        q=(t-450459)/216
        values.append(q.numerator*pow(q.denominator,-1,ell)%ell)
    tests=[pow(t,(ell-1)//4,ell) for t in values]
    check(all(t not in (0,1) for t in tests),'A contact root exists modulo ell')
    image=set()
    for x in range(ell):
        b=(216*pow(x,4,ell)+450459)%ell
        r=b*(b-1)*(b-2401)*(32*b+343)*(2*b-1)%ell
        image.add(r)
        check((1+17*r)%ell!=0,'Linear normalizer has a root modulo ell')
    minimum=k
    depth=(m-1)*minimum+1
    check(ell>2**16,'Wrong lower bound for ell')
    check(102**2==36*17**2 and ell>36,'Real normalization bound fails')
    check(2*19<39 and 19<2*10 and 19<20,'Invalid strict height exponents')
    check(12>=10 and 40>=39 and 40<76176,'Insufficient formal precision')
    check(5*49<256 and 34<64,'Invalid elementary cutoff constants')

    check(source['anchor_kind']=='forced_prime' and not source['indexed_guard_polynomials'],'Unexpected size condition')
    check(source['retained_base_count']==26 and source['total_polynomial_variables_after_finite_algebra']==27,'Wrong external count')
    check(source['finite_generator_count']==12 and source['monic_degree_product']=={'base':2,'exponent':21},'Wrong finite algebra')
    check(source['counts']=={'retained.input':1,'retained.point':18,'retained.slope':1,'retained.pole':4,'retained.scalar_pole':2,'finite.point':9,'finite.pole':2,'finite.scalar_pole':1},'Wrong coordinate inventory')
    check(source['comparison_orders']==[1]*10+[10,39,39,39,10,39],'Wrong assigned comparison orders')
    check(source['arithmetic_profile']=={'height_exponent':19,'height_log2_upper_bound':2093448,'formal_orders':[12,40,40,40],'assigned_comparison_orders':[10,39,39,39],'scalar_order':20,'inherited_height_exponent':19,'new_asymmetric_depth_prime_separation_used':False,'forced_prime':ell,'forced_exponent':k,'minimum_forced_contact_valuation':minimum,'minimum_scalar_index_valuation':depth},'Wrong arithmetic profile')
    check(len(source['finite_parameters'])==3 and all(v==[0] for v in source['finite_parameters'].values()),'Wrong single conic chart')
    check(prod(len(v) for v in source['finite_parameters'].values())==1,'Wrong source branch count')
    check(source['all_quadratic_roots_nonzero'] is True and
          all(r['generator_node'] in source['guard_numerators']
              for r in source['finite_monic_relations'] if r['kind']!='point'),
          'Missing non-torsion pole-root guard')
    events=source['events']
    norm=next(e for e in events if e['operation']=='scalar_norm')
    event=next(e for e in events if e['operation']=='normalized_scalar_contact')
    check(norm['orders']==[1,1,1,1,20,20] and norm['r']==event['normalized_contact'],'Changed scalar norm contact or orders')
    check(event['forced_prime']==ell and event['forced_exponent']==k and event['correction']==1,'Wrong contact constants')
    check(source['beta_formula']=='216*input.X^4+450459' and source['scalar_correction_fixed']==1,'Wrong beta or correction')
    check(next(e for e in events if e['operation']=='shifted_scalar_and_anchor_point')['point']=='S-P (direct difference)','Wrong scalar point')

    nodes=source['coefficient_dag']; X={(0,):1}; Z={(1,):1}
    one={():1}; beta=plus(times({():216},power(X,4)),{():450459})
    raw=times(beta,plus(beta,{():-1}),plus(beta,{():-2401}),plus(times({():32},beta),{():343}),plus(times({():2},beta),{():-1}))
    normalizer=plus(one,times({():17},plus(times({():ell},Z),one),raw))
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
            if nodes[a[0]]==['int',ell]:
                if a[1]==k: return times({():ell},power(Z,2))
                if a[1]==(k+1)//2: return times({():ell},Z)
                raise ValueError('Unexpected scalar prime-power exponent')
            check(a[1]<100,'Unexpected large power in contact');return power(expand(a[0]),a[1])
        raise ValueError('Unexpected contact operation '+op)
    def equals(row,num,den=one):
        check(times(expand(row['numerator']),den)==times(num,expand(row['denominator'])),'Incorrect rational contact identity')
    equals(event['raw_contact'],raw)
    equals(event['positive_normalizer'],normalizer)
    equals(event['normalized_contact'],times({():102**2*ell},power(Z,2),raw),power(normalizer,2))
    check(event['positive_normalizer']['numerator'] in source['guard_numerators'],'Missing normalizer denominator guard')
    return {'prime':ell,'prime_trial_division_bound':isqrt(ell),'nonquartic_residues':values,'fourth_power_tests':tests,'normalization_exponent':k,'minimum_contact_valuation':minimum,'minimum_scalar_index_valuation':depth,'linear_normalizer_residues_checked':ell,'raw_contact_image_size':len(image),'linear_normalizer_has_no_root':True,'scalar_contact_identity_checked_exactly':True,'external_variables':27,'finite_rank_exponent':21,'finite_source_branches':1,'nonzero_pole_roots_required':3,'selected_anchor_sufficient':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    provenance=json.loads((HERE/'inherited-method-reference.json').read_text())
    new=methods(HERE/'build_forced_prime_source.py')
    check(set(new)==set(provenance['method_names']),'Arithmetic method inventory changed')
    for name,expected in provenance['unchanged_method_ast_sha256'].items():
        method=new[name]
        if name=='finite_square':
            method=ast.parse(ast.unparse(method)).body[0]
            inserted=ast.parse("self.c.nonzero(z, name + '.nontorsion pole root')").body[0]
            matches=[node for node in method.body if ast_hash(node)==ast_hash(inserted)]
            check(len(matches)==1,'Missing exact non-torsion root restriction')
            method.body=[node for node in method.body if node not in matches]
            annotations=[node for node in method.body if isinstance(node,ast.Assign)
                and isinstance(node.targets[0],ast.Subscript)
                and isinstance(node.targets[0].slice,ast.Constant)
                and node.targets[0].slice.value=='zero_stratum_rule']
            check(len(annotations)==1 and annotations[0].value.value==
                'The source guard Z!=0 excludes a zero radicand. Retain only Z²=radicand with nonzero Z.',
                'Changed nonzero-stratum annotation')
            annotations[0].value=ast.Constant(value=
                'If radicand is zero use the linear relation Z=0; otherwise retain Z²=radicand and guard Z!=0. This is a finite case split.')
        check(ast_hash(method)==expected,'Unaccounted method change: '+name)
    point_reference=json.loads((HERE/'direct-point-reference.json').read_text())
    point_method=ast.parse(ast.unparse(new['point'])).body[0]
    def point_annotation(node):
        if not isinstance(node,ast.Assign): return False
        target=node.targets[0]
        if isinstance(target,ast.Name) and target.id=='automatic': return True
        return isinstance(target,ast.Subscript) and isinstance(target.slice,ast.Constant) and target.slice.value in ('automatic_nonzero_nodes','automatic_nonzero_proof')
    point_method.body=[node for node in point_method.body if not point_annotation(node)]
    check(ast_hash(point_method)==point_reference['point_method_ast_sha256'],
          'Unaccounted change in the reviewed direct point and scalar-shift construction')
    family_reference=json.loads((HERE/'family-semantic-reference.json').read_text())
    check(ast_hash(comparison_core(new['build']))==family_reference['unchanged_comparison_core_ast_sha256'],
          'Unaccounted comparison, point-source, or scalar-tree change')
    height=[]; collecting=False
    for n in new['build'].body:
        name=assigned_name(n)
        if name=='sum_x': collecting=True
        if name=='contacts': collecting=False
        if collecting: height.append(n)
    check(ast_hash(height)==family_reference['sum_trace_block_ast_sha256'],'Unaccounted trace-scale change')
    raw=gzip.decompress(args.source.read_bytes()) if args.source.suffix=='.gz' else args.source.read_bytes()
    source=json.loads(raw)
    family=source['family_parameter']
    check(family=={'name':'L','value':family['value'],'quantified':False,
        'constraint':'odd integer L>=3','sufficient_threshold_exists':True,
        'effective_threshold_known':False,'selected_member_certified_to_define_Z':False},
        'Missing or overstated ineffective-anchor status')
    check(all(v['name']!='L' for v in source['variables']),'Anchor exponent became a variable')
    heights=[e for e in source['events'] if e['operation']=='sum_trace_height_scales']
    check(len(heights)==1,'Wrong trace height event count')
    event=heights[0]
    check(event['root_names']==['A','S','T','Z'] and len(event['scales'])==2,'Wrong trace scope')
    det=[e for e in source['events'] if e['operation']=='detector']
    check(len(det)==2 and [e['scale'] for e in det]==event['scales'],'Wrong detector scales')
    nodes=source['coefficient_dag']
    one={():1}
    trace=event['trace']; sums=event['sum_components']
    point_events={e['name']:e for e in source['events'] if e['operation']=='point'}
    frontier=set()
    def collect(index):
        op,*args=nodes[index]
        if op=='int': return
        if op in ('neg','pow'): collect(args[0])
        elif op=='mul':
            for child in args: collect(child)
        else: frontier.add(index)
    for name in event['root_names']:
        for row in point_events[name]['output_x']:
            collect(row['numerator']); collect(row['denominator'])
    ex=expander(nodes,atoms={node:i for i,node in enumerate(sorted(frontier))})
    for component in (0,1):
        expected_num={}; expected_den=one
        for name in event['root_names']:
            row=point_events[name]['output_x'][component]
            nn,dd=ex(row['numerator']),ex(row['denominator'])
            expected_num=plus(times(expected_num,dd),times(nn,expected_den))
            expected_den=times(expected_den,dd)
        row=sums[component]
        check(times(ex(row['numerator']),expected_den)==times(expected_num,ex(row['denominator'])),
              'Sum component does not equal the sum of the four point abscissas')
    check(times(ex(trace['numerator']),ex(sums[0]['denominator']))==
          times({():2},ex(sums[0]['numerator']),ex(trace['denominator'])),
          'Trace is not twice the rational sum component')
    check(nodes[event['scales'][0]['numerator']]==nodes[event['scales'][0]['denominator']]==['int',1],
          'First scale is not one')
    sc=event['scales'][1]
    check(times(ex(sc['numerator']),power(ex(trace['denominator']),2))==
          times(power(ex(trace['numerator']),2),ex(sc['denominator'])),
          'Second scale is not trace squared')
    report=check_source(source)
    report.update(verify_direct_points(source))
    report.update(status='passed',source_sha256=digest(raw),
        builder_sha256=digest((HERE/'build_forced_prime_source.py').read_bytes()),
        checker_sha256=digest(Path(__file__).read_bytes()),
        unchanged_source_methods_checked=len(provenance['unchanged_method_ast_sha256']),
        comparison_source_unchanged_outside_height_block=True,
        trace_and_scale_identities_checked=True,
        family_parameter=family,
        scope='Exact expression-family inventory, direct point chart identities, reviewed direct scalar shift, inherited source preservation, trace scale and scalar contact identities, and finite arithmetic checks. This does not certify the selected exponent sufficient; the sufficient threshold is ineffective.')
    output=args.output or args.source.with_name('source-verification.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
