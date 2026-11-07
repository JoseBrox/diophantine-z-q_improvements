#!/usr/bin/env python3
"""Independent exact audit of the two preferred height/order profiles.

Imports checker utilities only, never either source producer. The complete
method ASTs are compared after the explicitly specified parameter changes.
All cutoff inequalities requiring large constants are checked by small exact
integer comparisons. Source-to-polynomial algebra is checked separately.
"""
from __future__ import annotations

import ast
from copy import deepcopy
import gzip
import json
from pathlib import Path

from check_source_semantics import (HERE, require, digest, statements, normal,
                                    methods, audit_AST, audit_identities)

PROFILES = [
    {'name':'height', 'builder':'build_source_height.py', 'source':'source-29-height.json.gz',
     'sha':'f7711a8283f661ee1e26edd2d6f26405491d1525bd9cceef392400f8f58ccd4e',
     'total':29, 'high':128, 'input':24, 'high_truncation':128, 'input_truncation':24,
     'scalar':100510416, 'anchor_exponent':2093967, 'anchor_q':23,
     'working_height_exponent':24,
     'arithmetic':'Inherited H19<2^2093966 contact-height bound (used with exponent24) and simultaneous prime-pattern hypotheses; odd-product identity and optimized cutoff proved separately'},
    {'name':'small-orders', 'builder':'build_source_small_orders.py', 'source':'source-31-small-orders.json.gz',
     'sha':'1fd43a602f141b0f777d5899f2e9f1245df6efbf8e64fa0ae5d608075990d431',
     'total':31, 'high':39, 'input':10, 'high_truncation':40, 'input_truncation':12,
     'scalar':20, 'anchor_exponent':9566463, 'anchor_q':26,
     'working_height_exponent':19,
     'arithmetic':'Inherited H19<2^2093966 exponent19 contact-height bound and simultaneous prime-pattern hypotheses; odd-product identity and semilocal size inequalities proved separately'},
]


class Integers(ast.NodeTransformer):
    def __init__(self, table): self.table=table
    def visit_Constant(self,node):
        if type(node.value) is int and node.value in self.table: node.value=self.table[node.value]
        return node


class AnchorConstants(ast.NodeTransformer):
    def __init__(self, profile): self.profile=profile
    def visit_BinOp(self,node):
        if (isinstance(node.op,ast.Pow) and isinstance(node.left,ast.Constant)
                and node.left.value==2 and isinstance(node.right,ast.Constant) and node.right.value==24):
            node.right.value=self.profile['anchor_q']
        return self.generic_visit(node)
    def visit_Constant(self,node):
        if node.value==9566463: node.value=self.profile['anchor_exponent']
        return node


def transformed(node, table): return Integers(table).visit(deepcopy(node))


def audit_profile(p):
    old=methods(HERE/'build_source.py');new=methods(HERE/p['builder'])
    require(set(old)==set(new),'Profile method list changed')
    for name in set(old)-{'__init__','scalar_norm','build'}:
        require(normal(old[name])==normal(new[name]),'Unaccounted profile method change: '+name)
    expected=deepcopy(old['__init__'])
    if p['name']=='small-orders':
        expected.args.kw_defaults[0].value='semilocal'
        expected.body=statements("assert anchor == 'semilocal', 'This small-order profile uses its semilocal size bound.'")+expected.body
    require(normal(expected)==normal(new['__init__']),'Profile constructor changed beyond its stated domain')
    require(normal(transformed(old['scalar_norm'],{48:p['scalar']}))==normal(new['scalar_norm']),
            'Scalar norm changed beyond its assigned order')
    body=deepcopy(old['build'].body)
    body[12]=transformed(body[12],{64:p['high_truncation']})
    body[13]=transformed(body[13],{64:p['high_truncation']})
    body[15]=transformed(body[15],{16:p['input_truncation'],64:p['high_truncation']})
    body[22]=statements('orders = [1]*10+[%d,%d,%d,%d]+[%d,%d]' %
        (p['input'],p['high'],p['high'],p['high'],p['input'],p['high']))[0]
    body[24]=transformed(body[24],{64:p['high']})
    body[42]=AnchorConstants(p).visit(body[42])
    metadata=body[50].value
    for key,value in zip(metadata.keys,metadata.values):
        if isinstance(key,ast.Constant) and key.value=='additional_arithmetic_input': value.value=p['arithmetic']
    profile={'height_exponent':p['working_height_exponent'],'height_log2_upper_bound':2093966,
             'formal_orders':[p['input_truncation']]+[p['high_truncation']]*3}
    if p['name']=='small-orders':profile['assigned_comparison_orders']=[p['input']]+[p['high']]*3
    profile['scalar_order']=p['scalar']
    if p['name']=='height':profile['inherited_height_exponent']=19
    profile['new_asymmetric_depth_prime_separation_used']=False
    body[61]=statements("result['arithmetic_profile'] = "+repr(profile))[0]
    body.insert(61,statements("result['optimized_cutoff_proof'] = '../height_cutoff.tex'")[0])
    require(normal(body)==normal(new['build'].body),'Profile contains an unaccounted build change')

    raw=gzip.decompress((HERE/p['source']).read_bytes());src=json.loads(raw)
    require(digest(raw)==p['sha'],'Preferred source checksum differs')
    require(src['arithmetic_profile']==profile,'Arithmetic profile differs')
    require(src['retained_base_count']==p['total']-1
            and src['total_polynomial_variables_after_finite_algebra']==p['total'],'Wrong declared count')
    require(src['comparison_orders']==[1]*10+[p['input']]+[p['high']]*3+[p['input'],p['high']],
            'Wrong assigned comparison orders')
    scalar=next(e for e in src['events'] if e['operation']=='scalar_norm')
    require(scalar['orders']==[1]*4+[p['scalar']]*2,'Wrong scalar order')
    if p['name']=='height':
        require(src['indexed_guard_polynomials'][0]['index_last']=={'base':2,'exponent':2093967},
                'Wrong optimized finite cutoff')
    else:
        require(src['anchor_kind']=='semilocal' and not src['indexed_guard_polynomials'],
                'Small-order profile has an unsupported finite anchor')
    return {'profile':p['name'],'source':p['source'],'source_sha256':digest(raw),
            'builder_sha256':digest((HERE/p['builder']).read_bytes()),
            'all_method_changes_accounted_exactly':True,'arithmetic_profile':profile,
            'total_variables':p['total']}


def main():
    audit_AST();audit_identities()
    h=2093966;E=h+1
    require(48*E==100510416 and E==2093967,'Linear-cutoff parameter arithmetic failed')
    require(h>=20 and 28**4<2**20 and 16<18,'Finite-cutoff rational inequalities failed')
    require(2+3*(2**25-1)>40*(h+6),'Semilocal cutoff does not dominate (64H)^20')
    require(2*19<39 and 19<2*10 and 19<20,'Small-order strict thresholds failed')
    require(5*49<256 and 34<64,'Small-order constants failed')
    require(40>=39 and 12>=10 and 128<76176,'Formal precisions or prime threshold failed')
    report={'status':'passed','profiles':[audit_profile(p) for p in PROFILES],
            'exact_cutoff_parameter_inequalities':True,
            'no_asymmetric_depth_prime_hypothesis':True,
            'checker_sha256':digest(Path(__file__).read_bytes()),
            'proof':'../height_cutoff.tex',
            'scope':'All source-method changes are exact AST identities, checked against the independently audited odd-product source. Numerical cutoff and parameter inequalities are exact. The contact-height, group and prime-pattern inputs remain explicitly inherited arithmetic assumptions.'}
    (HERE/'height-profile-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
