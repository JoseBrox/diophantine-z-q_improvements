#!/usr/bin/env python3
"""Independent audit of the changes from the frozen 41-variable source.

No producer is imported or executed. Exact AST comparisons account for every
changed mathematical statement; unchanged pole and scalar formulas are matched
to a pinned historical text. Independent rational/field/polynomial arithmetic
checks the new identities. The generic specification checker separately checks
all emitted DAG substitutions, denominators, finite branches, and majorants.

This is a reproducible implementation audit, not a formal proof of the source's
arithmetic hypotheses or a claim that finite testing proves such hypotheses.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import gzip
import hashlib
import json
from math import prod
from pathlib import Path
from textwrap import dedent

HERE = Path(__file__).resolve().parent
CASES = (
    ('source-29.json.gz', 28, 13, 22,
     '0df39065f88e6c87a323ec9fd366171837d04edfa511c471d35a84cccad230aa'),
    ('source-31-semilocal.json.gz', 30, 14, 23,
     '66f0b361e3c75e506caa858fa14fdba5a08902cab670c73cdcc871c51fad1031'),
)


def require(value, explanation):
    if not value:
        raise ValueError(explanation)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def statements(text):
    return ast.parse(dedent(text)).body


def normal(node):
    if isinstance(node, list):
        return [normal(n) for n in node]
    return ast.dump(node, include_attributes=False)


def methods(path):
    tree = ast.parse(path.read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    return {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}


class SmallChange(ast.NodeTransformer):
    def __init__(self, constants=None, replace_scalar_point=False):
        self.constants = constants or {}
        self.replace_scalar_point = replace_scalar_point

    def visit_Constant(self, node):
        if type(node.value) is int and node.value in self.constants:
            node.value = self.constants[node.value]
        if node.value == 'Norm_K/Q(x(S)-x([index]P))':
            node.value = 'Norm_K/Q(x(S-P)-x([index]P))'
        return node

    def visit_Subscript(self, node):
        if (self.replace_scalar_point and isinstance(node.value, ast.Name)
                and node.value.id == 'points' and isinstance(node.slice, ast.Constant)
                and node.slice.value == 'S'):
            return ast.Name(id='scalar_point', ctx=ast.Load())
        return self.generic_visit(node)


def changed(node, **options):
    return SmallChange(**options).visit(deepcopy(node))


def audit_AST():
    baseline = HERE/'baseline_source_41.txt'
    provenance = json.loads((HERE/'provenance.json').read_text())
    baseline_record = next(r for r in provenance['inherited_code']
                           if r['output'] == 'build_source.py')
    require(digest(baseline.read_bytes()) == baseline_record['historical_sha256'],
            'Pinned baseline source differs')
    helper_baseline = HERE/'baseline_field_circuit.txt'
    helper_record = next(r for r in provenance['inherited_code'] if r['output'] == 'field_circuit.py')
    require(digest(helper_baseline.read_bytes()) == helper_record['historical_sha256'],
            'Pinned rational arithmetic helper differs')
    classes = lambda path: {n.name:n for n in ast.parse(path.read_text()).body if isinstance(n,ast.ClassDef)}
    hc, hn = classes(helper_baseline), classes(HERE/'field_circuit.py')
    require(normal(hc['Circuit']) == normal(hn['Circuit']) and normal(hc['Rational']) == normal(hn['Rational']),
            'Rational arithmetic or guard implementation changed')
    original_methods = {n.name:n for n in hc['Builder'].body if isinstance(n,ast.FunctionDef)}
    checked_field_methods = []
    for method in hn['Builder'].body:
        require(isinstance(method,ast.FunctionDef) and method.name in original_methods,
                'Unexpected field arithmetic helper statement')
        require(normal(method)==normal(original_methods[method.name]), 'Field method changed: '+method.name)
        checked_field_methods.append(method.name)
    old, new = methods(baseline), methods(HERE/'build_source.py')
    unchanged = sorted(set(old)-{'__init__', 'point', 'build'})
    require(set(new) == set(old)|{'fixed_point'}, 'Unexpected source routine')
    for name in unchanged:
        require(normal(old[name]) == normal(new[name]), 'Changed inherited routine: '+name)

    oi, ni = old['__init__'].body, new['__init__'].body
    require(len(oi) == len(ni) == 29, 'Constructor shape changed')
    expected = statements('''
        assert share_height and normalize_scalar and parametrize_poles and fixed_scales
        self.fourfold_points = {}
    ''') + deepcopy(oi[2:])
    expected[19] = changed(expected[19], constants={9:3})
    expected[28] = changed(expected[28], constants={9:3})
    require(normal(expected) == normal(ni), 'Constructor has an unaccounted change')

    op, np = old['point'].body, new['point'].body
    expected = deepcopy(op[:10]) + statements('''
        twice = self.double({'x': a, 'y': b})
        if name in ('A', 'S', 'T', 'Z'):
            fourfold = self.double(twice)
            self.fourfold_points[name] = fourfold
            base = self.fixed_point()
            negative_base = {'x': base['x'], 'y': self.scale(base['y'], -1)}
            point = self.difference(fourfold, negative_base)
            chart = 'P+4R'
        else:
            point = twice
            chart = '2R'
    ''') + deepcopy(op[11:13]) + statements('''
        self.events.append({'operation': 'point', 'name': name, 'chart': chart,
            'halfpoint_x': [self.rr(v) for v in a],
            'halfpoint_y': [self.rr(v) for v in b],
            'output_x': [self.rr(v) for v in point['x']],
            'output_y': [self.rr(v) for v in point['y']]})
        return point
    ''')
    require(normal(expected) == normal(np), 'Point chart has an unaccounted change')
    require(normal(new['fixed_point'].body) == normal(statements('''
        return {'x': self.field(Fraction(57,8), Fraction(-7,2)),
                'y': self.field(Fraction(-165,8), Fraction(417,32))}
    ''')), 'Fixed generator differs')

    ob, nb = old['build'].body, new['build'].body
    require(len(ob) == 54 and len(nb) == 63, 'Build statement count changed')
    expected = deepcopy(ob[:5]) + statements('''
        beta = 2*self.X*self.X+3
        base = self.fixed_point()
        targets = [base]+roots
    ''') + deepcopy(ob[8:26]) + statements('''
        product_x = self.field(1)
        for point in roots:
            product_x = self.mul(product_x, point['x'])
        C0, C1 = product_x
        scales = [self.c.rational(1), C0*C0, (1+C1*C1)**2]
        for index, scale in enumerate(scales):
            self.c.nonzero(scale, 'odd-product height scale'+str(index))
        self.events.append({'operation': 'odd_product_height_scales',
            'root_names': ['A', 'S', 'T', 'Z'],
            'product_components': [self.rr(x) for x in product_x],
            'scales': [self.rr(x) for x in scales]})
    ''') + deepcopy(ob[29:34]) + statements("scalar_point = self.fourfold_points['S']")
    expected += [changed(ob[34], replace_scalar_point=True)] + statements('''
        self.events.append({'operation': 'shifted_scalar_and_anchor_point',
            'point': 'S-P=4R_S',
            'x': [self.rr(x) for x in scalar_point['x']],
            'y': [self.rr(y) for y in scalar_point['y']]})
    ''') + deepcopy(ob[35:37]) + [changed(ob[37], replace_scalar_point=True)]
    expected += deepcopy(ob[38:41]) + statements('''
        count = 29+(2 if self.anchor_kind == 'semilocal' else 0)
        assert self.base_count+1 == count
        assert len(self.relations) == 13+(self.anchor_kind == 'semilocal')
        degree_power = 22+(self.anchor_kind == 'semilocal')
    ''')
    metadata = deepcopy(ob[46])
    replacements = {
        'source_commit':'14e8f601fe0d9173d4a5f084aedc3e07066a7688',
        'additional_arithmetic_input':'Inherited exponent-24 height and simultaneous prime-pattern hypotheses, including Sun arXiv:2610.20691v2 Theorem4.1; odd-product identity proved separately',
    }
    for key, value in zip(metadata.value.keys, metadata.value.values):
        if isinstance(key, ast.Constant) and key.value in replacements:
            value.value = replacements[key.value]
    expected += [metadata]+deepcopy(ob[47:52])+statements('''
        result['beta_formula'] = '2*input.X^2+3'
        result['odd_root_chart'] = 'P+4R for A,S,T,Z; 2R for H,UA,US,UT,UZ'
        result['comparison_targets'] = 'P,A,S,T,Z (direct targets)'
        result['height_point'] = 'S-P=4R_S'
        result['odd_product_height_proof'] = '../odd_product_construction.tex'
        result['arithmetic_profile'] = {'height_exponent': 24, 'height_log2_upper_bound': 4783227,
            'formal_orders': [16,64,64,64], 'scalar_order': 48,
            'new_asymmetric_depth_prime_separation_used': False}
        return result
    ''')
    require(normal(expected) == normal(nb), 'Build has an unaccounted change')
    return {
        'unchanged_inherited_methods': unchanged,
        'unchanged_field_arithmetic_methods': checked_field_methods,
        'rational_arithmetic_and_guards_AST_identical': True,
        'all_constructor_point_and_build_changes_accounted_exactly': True,
        'baseline_sha256': digest(baseline.read_bytes()),
        'builder_sha256': digest((HERE/'build_source.py').read_bytes()),
        'changes': ['nine comparison pole blocks to three odd-product blocks',
            'four root charts P+4R, five charts 2R',
            'direct targets P,A,S,T,Z', 'beta=2X^2+3',
            'scalar and anchor point S-P=4R_S', 'corresponding count and provenance metadata'],
    }


class Poly:
    """Small exact Laurent polynomials; deliberately independent of the producer."""
    dimensions = 6

    def __init__(self, value=0):
        if isinstance(value, Poly): self.terms = dict(value.terms)
        elif isinstance(value, dict): self.terms = {e:Fraction(c) for e,c in value.items() if c}
        else: self.terms = {(0,)*self.dimensions:Fraction(value)} if value else {}

    @classmethod
    def variable(cls, i):
        a=[0]*cls.dimensions; a[i]=1
        return cls({tuple(a):1})

    def __add__(self, other):
        out=dict(self.terms)
        for e,c in Poly(other).terms.items(): out[e]=out.get(e,0)+c
        return Poly(out)
    __radd__=__add__
    def __neg__(self): return Poly({e:-c for e,c in self.terms.items()})
    def __sub__(self,other): return self+-Poly(other)
    def __rsub__(self,other): return Poly(other)+-self
    def __mul__(self,other):
        out={}
        for e,c in self.terms.items():
            for f,d in Poly(other).terms.items():
                g=tuple(a+b for a,b in zip(e,f));out[g]=out.get(g,0)+c*d
        return Poly(out)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0:
            require(len(self.terms)==1,'Nonmonomial Laurent inverse')
            e,c=next(iter(self.terms.items()));return Poly({tuple(n*a for a in e):c**n})
        out=Poly(1);a=self
        while n:
            if n&1:out=out*a
            a=a*a;n//=2
        return out
    def __truediv__(self,other): return self*Poly(other)**-1
    def __rtruediv__(self,other): return Poly(other)*self**-1
    def __eq__(self,other): return self.terms==Poly(other).terms


def fadd(a,b): return a[0]+b[0],a[1]+b[1]
def fneg(a): return -a[0],-a[1]
def fsub(a,b): return fadd(a,fneg(b))
def fmul(a,b): return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def fscale(a,k): return a[0]*k,a[1]*k
def finv(a):
    n=a[0]*a[0]-2*a[1]*a[1]
    return a[0]/n,-a[1]/n
def fdiv(a,b): return fmul(a,finv(b))
def fsquare(a): return fmul(a,a)


def audit_identities():
    A,B,Y,t,u,v=[Poly.variable(i) for i in range(6)]
    require(Y**4-4*A*Y**2+8*B**2 == (Y**2-2*A)**2-4*(A**2-2*B**2),
            'Quartic derivative identity failed')
    require(Poly(Fraction(1,4))*Y**2+2*B**2/Y**2-A
            == (Y**4-4*A*Y**2+8*B**2)/(4*Y**2), 'Point root reconstruction failed')
    require(2*(Y/2)*(B/Y)==B,'Imaginary ordinate identity failed')
    for epsilon in (0,1):
        den=t*t+3*B;enum=t*t+(4*epsilon-1)*B;pnum=-4*B*t*(1-epsilon)
        require(pnum*pnum==B*(den-enum)*(den+3*enum),'Conic identity failed')
    R=Y/(A**5*B**6)
    for m in (1,16,64):
        require(R/(B**(2*m+2)*R**(2*m))==A**(10*m-5)*B**(10*m-8)/Y**(2*m-1),
                'Normalized detector weight identity failed')
    require((A*v-u)**2-A*v*(A*v-u)+v*v == v*v-A*u*v+u*u,
            'Lucas invariant failed')

    ff=lambda a=0,b=0:(Fraction(a),Fraction(b))
    D=ff(11,-6);R0=(ff(1,1),ff(0,2))
    x,y=R0
    require(fsquare(y)==fsub(fmul(fsquare(x),x),fmul(D,x)),'R0 not on curve')
    slope=fdiv(fsub(fscale(fsquare(x),3),D),fscale(y,2))
    xp=fsub(fsquare(slope),fscale(x,2));yp=fsub(fmul(slope,fsub(x,xp)),y)
    require((xp,yp)==(ff(Fraction(57,8),Fraction(-7,2)),ff(Fraction(-165,8),Fraction(417,32))),
            'P is not 2R0')
    require(fmul(fsquare(ff(3,-1)),ff(3,-1))==ff(45,-29),'Cubic twist coefficient differs')

    # Work entirely with small integers: M/H^2 > 2^9=512>441.
    require(9566463-2*4783227==9 and 512>441>400,'Shifted anchor comparison failed')
    require(1+3*(2**23-1)//2>9566463,'Semilocal anchor is not large enough')
    require(1199 not in [34**2,35**2] and 34**2<1199<35**2,'Input exceptional-value check failed')
    require(2**16*518513917206770054130*204**2 < 23**24,'Scalar real bound failed')
    local_primes=(2,3,11,17,37,67,71)
    rows=[]
    for p in local_primes:
        two_valuation=int(p==2);odd_unit=p//(2 if p==2 else 1)
        two_units={1:(0,0),3:(1,1),5:(0,1),7:(1,0)}[odd_unit%8]
        v3=int(p==3);unit3=p//(3 if p==3 else 1)
        v17=int(p==17);unit17=p//(17 if p==17 else 1)
        rows.append((two_valuation,*two_units,v3,int(unit3%3==2),v17,int(pow(unit17,8,17)==16)))
        require(all((t*t+t+23)%p for t in range(p)), 'Scalar normalizer has an adjustment-prime root')
    require(rows==[(1,0,0,0,1,0,0),(0,1,1,1,0,0,1),(0,1,1,0,1,0,1),
                  (0,0,0,0,1,1,0),(0,0,1,0,0,0,1),(0,1,1,0,0,0,0),(0,1,0,0,1,0,1)],
            'Displayed local squareclass vectors differ')
    basis={}
    for row in rows:
        mask=sum(a<<i for i,a in enumerate(row))
        while mask:
            pivot=mask.bit_length()-1
            if pivot in basis: mask^=basis[pivot]
            else: basis[pivot]=mask;break
    require(len(basis)==7,'Local squareclass basis is singular')
    delta=lambda q:q*q+q+23
    require(delta(Fraction(2401))==25*349*661
            and 1024*delta(Fraction(-343,32))==25*5209
            and 4*delta(Fraction(1,2))==5*19,'Contact normalizer resultants differ')
    return {'point_quartic_and_derivative_identities':True,
        'two_pole_conic_charts_exact':True,
        'detector_weight_identities_orders':[1,16,64],
        'Lucas_recurrence_invariant_exact':True,
        'fixed_generator_equals_twice_R0':True,
        'shifted_anchor_integer_inequalities':True,
        'scalar_real_normalization_integer_inequality':True,
        'scalar_local_squareclass_basis_rank':len(basis),
        'scalar_normalizer_contact_and_local_checks':True}


def audit_source_file(name, b, m, exponent, expected_hash):
    raw=gzip.decompress((HERE/name).read_bytes());src=json.loads(raw)
    require(digest(raw)==expected_hash,'Source bytes differ: '+name)
    require(src['retained_base_count']==b and len(src['variables'])==b+m,'Source variable count differs')
    require(src['total_polynomial_variables_after_finite_algebra']==b+1,'Wrong final count')
    require(src['finite_generator_count']==m and src['monic_degree_product']=={'base':2,'exponent':exponent},
            'Finite rank differs')
    require(src['comparison_orders']==[1]*10+[16,64,64,64]+[16,64],'Comparison orders differ')
    require(len(src['comparison_tests'])==16,'Missing comparison test')
    require(src['closed_equations']==[],'Unexpected closed residual')
    require([v['index'] for v in src['variables']]==list(range(b+m)),'Noncanonical variables')
    require([r['variable'] for r in src['finite_monic_relations']]==list(range(b,b+m)),
            'Noncanonical algebra roots')
    points=[e for e in src['events'] if e['operation']=='point']
    require([p['name'] for p in points]==['A','S','T','Z','H','UA','US','UT','UZ'],'Point list differs')
    require([p['chart'] for p in points]==['P+4R']*4+['2R']*5,'Point parity charts differ')
    require(len([e for e in src['events'] if e['operation']=='detector'])==3,'Wrong detector count')
    scalar=next(e for e in src['events'] if e['operation']=='scalar_norm')
    require(scalar['orders']==[1,1,1,1,48,48],'Scalar precision changed')
    require(len(src['finite_parameters'])==5 and prod(len(v) for v in src['finite_parameters'].values())==2**18,
            'Wrong finite parameter ranges')
    require(set(src['finite_parameters'])=={'scalar_correction','pole_chart_detector0',
        'pole_chart_detector1','pole_chart_detector2','pole_chart_scalar'},'Unexpected finite parameter')
    require(all(v==[0,1] for k,v in src['finite_parameters'].items() if k!='scalar_correction'),
            'Conic chart range changed')
    primes=(2,3,11,17,37,67,71,5,19,23,349,661,5209)
    corrections=set()
    for mask in range(1<<len(primes)):
        a=prod(p for i,p in enumerate(primes) if mask>>i&1);corrections.update((a,-a))
    require(set(src['finite_parameters']['scalar_correction'])==corrections and len(corrections)==2**14,
            'Scalar correction set differs')
    if src['anchor_kind']=='finite':
        require(src['indexed_guard_polynomials'][0]['index_last']=={'base':2,'exponent':9566463},
                'Anchor range differs')
        shifted=next(e for e in src['events'] if e['operation']=='shifted_scalar_and_anchor_point')
        require(src['indexed_guard_polynomials'][0]['variable_field_argument']==shifted['x'],
                'Anchor does not use the shifted scalar point')
    else:
        require(src['indexed_guard_polynomials']==[],'Unexpected indexed semilocal anchor')
    return {'file':name,'raw_sha256':digest(raw),'retained_coordinates':b,
            'final_total_variables':b+1,'finite_generators':m,'rank_power_of_two_exponent':exponent,
            'comparison_pole_blocks':3,'scalar_pole_blocks':1,'finite_source_branches':2**18}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'source-semantic-verification.json')
    args=parser.parse_args()
    report={'status':'passed','AST_audit':audit_AST(),'exact_identity_audit':audit_identities(),
            'sources':[audit_source_file(*case) for case in CASES],
            'checker_sha256':digest(Path(__file__).read_bytes()),
            'scope':'Exact structural audit accounts for every mathematical change from the pinned baseline. Independent exact small identities and frozen source inventories are checked. Source-to-polynomial DAG conversion and bounds are checked separately. Arithmetic hypotheses and the mathematical completeness proof are not certified by this program.'}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
