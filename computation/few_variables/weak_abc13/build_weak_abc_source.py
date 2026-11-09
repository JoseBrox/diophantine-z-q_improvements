#!/usr/bin/env python3
"""Build the thirteen-coordinate family under an ADDITIONAL weak-abc hypothesis at exponent 121/100.

The numerical positive input shift is an algebraic fixture. Its sufficient
threshold is ineffective and no selected value is certified to define Z.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PINNED=HERE.parent/'trace27_nontorsion'
sys.path.insert(0,str(PINNED))
from build_forced_prime_source import PreferredBuilder
from field_circuit import Circuit
from compile_source import compile_source


class WeakABCBuilder(PreferredBuilder):
    def __init__(self,shift):
        if not isinstance(shift,int) or shift<3 or shift%2!=1:
            raise ValueError('shift must be a fixed odd integer >=3')
        self.shift=shift
        self.c=Circuit(); self.D=self.field(11,-6)
        self.relations=[];self.closed_equations=[];self.events=[]
        self.fourfold_points={};self.parametrize_poles=True
        self.X=self.c.variable('input.X','retained.input')
        self.point_names=['A','H','UA']
        self.abscissas={name:tuple(self.c.variable(name+'.a'+str(j),'retained.point') for j in range(2)) for name in self.point_names}
        self.slope=self.c.variable('slope.lambda','retained.slope')
        self.pole_structural=[tuple(self.c.variable('detector%d.%s'%(r,k),'retained.pole') for k in ('conic_parameter','s')) for r in range(2)]
        self.base_count=len(self.c.variables)
        self.conic_charts={f'detector{r}':self.c.parameter(f'pole_chart_detector{r}',1) for r in range(2)}

    def build(self):
        points={name:self.point(name) for name in self.point_names}
        A,H,U=[points[name] for name in self.point_names]
        V0=self.difference(H,self.fixed_point());V1=self.difference(U,A)
        beta=2*self.X**2+self.c.parameter('fixed_input_shift',self.shift)
        L=self.div(self.parameter_at_identity(U),self.parameter_at_identity(H))
        Lprime=self.conj(self.div(self.parameter_at_identity(V1),self.parameter_at_identity(V0)))
        tests=[self.reciprocal(H),self.reciprocal(U),self.conj(self.reciprocal(V0)),self.conj(self.reciprocal(V1)),self.sub(L,Lprime),self.sub(L,self.field(beta))]
        orders=[1,1,1,1,1,1]
        squares=[self.square(test) for test in tests]
        trace=2*A['x'][0]
        compressed=beta**8+trace**8
        scales=[self.c.rational(1),compressed]
        self.events.append({'operation':'conditional_weak_abc_height_scales','beta':self.rr(beta),'trace':self.rr(trace),
            'sum_eighth_powers':self.rr(compressed),'scales':[self.rr(a) for a in scales],
            'height_premise':'ADDITIONAL weak rational abc at exponent 121/100; h(1:beta:trace)<=(121/437)*h(beta^8+trace^8)+C'})
        self.events.append({'operation':'conditional_direct_target_tests','orders':orders,
            'L':[self.rr(a) for a in L],'Lprime':[self.rr(a) for a in Lprime],
            'tests':[[self.rr(a) for a in test] for test in tests],'formal_precision':4})
        contacts=[Fraction(0),Fraction(-1,2),Fraction(-1,4),Fraction(-2,5),Fraction(-1),Fraction(-1,3)]
        for r,scale in enumerate(scales):
            self.c.nonzero(scale,f'detector{r}.scale')
            t=scale*self.slope;delta=t-1
            self.c.nonzero(delta,f'detector{r}.normalizer')
            F=self.c.rational(1)
            for theta in contacts:
                factor=t-theta;self.c.nonzero(factor,f'detector{r}.contact{theta}');F*=factor
            weights={1:delta**4/F}
            W=self.field(1)
            for sq,order in zip(squares,orders):W=self.mul(W,self.add(self.field(1),self.scale(sq,weights[order])))
            norm=W[0]*W[0]-2*W[1]*W[1]
            self.c.nonzero(norm,f'detector{r}.product norm');self.c.nonzero(W[0],f'detector{r}.trace numerator')
            pole=F*norm*norm/(4*delta**8*W[0]*W[0])
            self.zero_pole(pole,self.pole_structural[r],f'detector{r}')
            self.events.append({'operation':'detector','index':r,'scale':self.rr(scale),'slope_argument':self.rr(t),
                'F':self.rr(F),'delta':self.rr(delta),'weights':{str(k):self.rr(v) for k,v in weights.items()},
                'product_components':[self.rr(v) for v in W],'pole_input':self.rr(pole)})
        assert self.base_count==12 and len(self.relations)==5
        assert [r['degree'] for r in self.relations]==[4,4,4,2,2]
        return {
            'format':'shared-point-source-coefficient-dag/v1',
            'status':'Conditional on ADDITIONAL weak rational abc at exponent 121/100 and the stated source arithmetic premises. Every sufficiently large fixed odd shift works; the numerical fixture has no certified sufficient threshold.',
            'source_commit':'14e8f601fe0d9173d4a5f084aedc3e07066a7688',
            'additional_arithmetic_input':'ADDITIONAL weak rational abc at exponent 121/100 conjecture. Retains the specified elliptic group, pole obstruction and nonzero realization, and simultaneous prime-pattern inputs. Uses the proved one-point trace-height theorem with ineffective additive constant. The contact estimate follows from the degree-four rational map t*(t+2)^3/(2*t+1)^3 and weak abc; the scalar estimate uses eighth powers.',
            'family_parameter':{'name':'B','value':self.shift,'quantified':False,'constraint':'odd integer B>=3',
                'sufficient_threshold_exists':True,'effective_threshold_known':False,'selected_member_certified_to_define_Z':False},
            'anchor_kind':'positive_input_shift_under_weak_abc_121_100','share_scalar_height_point':False,
            'retained_base_count':12,'total_polynomial_variables_after_finite_algebra':13,
            'variables':self.c.variables,'coefficient_dag':self.c.nodes,'finite_monic_relations':self.relations,
            'finite_generator_count':5,'monic_degree_product':{'base':2,'exponent':8},
            'closed_equations':[],'guard_numerators':sorted(self.c.guards),
            'all_quadratic_roots_nonzero':True,'guard_descriptions':self.c.guard_descriptions,'indexed_guard_polynomials':[],
            'finite_parameters':{**{f'pole_chart_detector{r}':[0] for r in range(2)},'fixed_input_shift':[self.shift]},
            'comparison_tests':[[self.rr(a) for a in test] for test in tests],'comparison_orders':orders,
            'events':self.events,'counts':dict(Counter(v['category'] for v in self.c.variables)),
            'beta_formula':'2*input.X^2+B','point_chart':'x=h^2; j^2=h^4-D; y=h*j',
            'formal_precision':4,'height_scales':'1,beta^8+(Tr x(A))^8',
            'source_helpers':{name:hashlib.sha256((PINNED/name).read_bytes()).hexdigest() for name in ('build_forced_prime_source.py','field_circuit.py','compile_source.py','finite_algebra_core.py')},
            'semantics':'Twelve retained rational coordinates; three finite point quartics and two finite nonzero pole quadratics. Every displayed division is guarded. No scalar pole, Lucas residual, or omitted equality is present.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--shift',type=int,default=3);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    source=WeakABCBuilder(args.shift).build()
    raw=(json.dumps(source,separators=(',',':'))+'\n').encode()
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'source.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    spec=compile_source(source,hashlib.sha256(raw).hexdigest())
    spec['arithmetic_status']='ADDITIONAL weak rational abc at exponent 121/100 is assumed. This fixed odd input-shift fixture is not certified to exceed the ineffective sufficient threshold. The family defines Z for all sufficiently large shifts under the stated premises.'
    spec['representation_scope']='Complete finite integer coefficient specification of the weak-abc13 source. Its guarded projection is preserved by finite-algebra elimination; no numerical sufficient shift is certified.'
    encoded=(json.dumps(spec,separators=(',',':'))+'\n').encode()
    (args.output/'source-polynomial-specification.json').write_bytes(encoded)
    receipt={'source_sha256':hashlib.sha256(raw).hexdigest(),'integer_specification_sha256':hashlib.sha256(encoded).hexdigest(),
        'retained_coordinates':12,'total_coordinates':13,'finite_point_quartics':3,'finite_pole_quadratics':2,'rank':256,
        'rational_source_nodes':len(source['coefficient_dag']),'integer_source_nodes':len(spec['coefficient_dag']),
        'additional_weak_abc_required':True,'weak_abc_exponent':{'numerator':121,'denominator':100},'selected_member_certified_to_define_Z':False,'family_parameter':source['family_parameter']}
    (args.output/'source-construction-certificate.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
