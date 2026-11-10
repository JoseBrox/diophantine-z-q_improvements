#!/usr/bin/env python3
"""Build the guarded source with two combined scalar/comparison pole inputs.

The fixed odd exponent is a coefficient choice. No numerical sufficient
exponent is certified. The arithmetic projection theorem is supplied by
the accompanying proof, not by successful coefficient reconstruction.
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
from field_circuit import Circuit,Rational
from compile_source import compile_source


class MergedBuilder(PreferredBuilder):
    def __init__(self,anchor_exponent):
        if type(anchor_exponent) is not int or anchor_exponent<3 or anchor_exponent%2!=1:
            raise ValueError('anchor_exponent must be a fixed odd integer >=3')
        self.forced_exponent=anchor_exponent;self.forced_prime=76249
        self.high_order=self.input_order=self.scalar_order=3
        self.high_precision=self.input_precision=4
        self.scalar_switch_exponent=3;self.scalar_norm_exponent=3
        self.c=Circuit();self.D=self.field(11,-6)
        self.relations=[];self.closed_equations=[];self.events=[]
        self.fourfold_points={};self.parametrize_poles=True
        self.X=self.c.variable('input.X','retained.input')
        self.point_names=['A','S','T','Z','H','UA','US','UT','UZ']
        self.abscissas={name:tuple(self.c.variable(name+'.a'+str(j),'retained.point')
                                 for j in range(2)) for name in self.point_names}
        self.slope=self.c.variable('slope.lambda','retained.slope')
        self.c.nonzero(self.slope,'nonzero common comparison slope')
        self.pole_structural=[tuple(self.c.variable('detector%d.%s'%(r,k),'retained.pole')
                                    for k in ('conic_parameter','s')) for r in range(2)]
        self.base_count=len(self.c.variables)
        self.conic_charts={f'detector{r}':self.c.parameter(f'pole_chart_detector{r}',1)
                           for r in range(2)}

    def scalar_phi(self,R,D,label):
        numerator=R*D
        denominator=1+numerator
        result=numerator/denominator
        self.events.append({'operation':'linear_scalar_normalization','label':label,
            'coefficient':self.rr(R),'input':self.rr(D),'output':self.rr(result),
            'denominator':self.rr(denominator)})
        return result

    def build(self):
        points={name:self.point(name) for name in self.point_names}
        roots=[points[name] for name in ('A','S','T','Z')]
        H=points['H'];Ui=[points[name] for name in ('UA','US','UT','UZ')]
        beta=216*self.X**4+450459
        differences=[self.difference(p,q) for p,q in zip([H]+Ui,[self.fixed_point()]+roots)]
        tests=[self.reciprocal(p) for p in [H]+Ui]
        tests += [self.conj(self.reciprocal(p)) for p in differences]
        denominator=self.logarithm(H,4)
        alternate=self.logarithm(differences[0],4)
        L=[self.div(self.logarithm(p,4),denominator) for p in Ui]
        Lprime=[self.conj(self.div(self.logarithm(p,4),alternate)) for p in differences[1:]]
        tests += [self.sub(u,v) for u,v in zip(L,Lprime)]
        tests.append(self.sub(L[0],self.field(beta)))
        u,v,w=L[1:];um2=self.sub(u,self.field(2))
        lucas=self.sub(self.add(self.square(v),self.mul(self.square(um2),self.square(w))),
                       self.add(self.mul(self.mul(u,um2),self.mul(v,w)),self.field(1)))
        tests.append(lucas)
        assert len(tests)==16
        comparison_orders=[1]*10+[3]*6
        scalar_point=self.fourfold_points['S']
        scalar_tests=list(self.reciprocal(H)+self.reciprocal(scalar_point)+
            self.div(self.parameter_at_identity(scalar_point),self.parameter_at_identity(H)))
        assert len(scalar_tests)==6
        raw=self.c.rational(1)
        for factor in (beta,beta-1,beta-2401,32*beta+343,2*beta-1):raw*=factor
        prime_power=Rational(self.c,self.c.power(self.c.node('int',76249),
                                  (self.forced_exponent+1)//2),self.c.one)
        contact_power=Rational(self.c,self.c.power(self.c.node('int',76249),
                                    self.forced_exponent),self.c.one)
        scalar_denominator=1+17*(prime_power+1)*raw
        rs=102**2*contact_power*raw/(scalar_denominator**2)
        self.c.nonzero(rs,'scalar contact coefficient')
        trace=2*sum((p['x'][0] for p in roots),self.c.rational(0))
        scales=[self.c.rational(1),(1+rs*trace**2)**2]
        self.events.append({'operation':'combined_height_scales','beta':self.rr(beta),
            'trace':self.rr(trace),'raw_scalar_contact':self.rr(raw),
            'scalar_contact':self.rr(rs),'scalar_denominator':self.rr(scalar_denominator),
            'scales':[self.rr(a) for a in scales]})
        self.events.append({'operation':'comparison_and_scalar_tests',
            'comparison':[[self.rr(v) for v in D] for D in tests],
            'scalar':[self.rr(D) for D in scalar_tests],
            'L':[[self.rr(v) for v in D] for D in L],
            'Lprime':[[self.rr(v) for v in D] for D in Lprime],
            'comparison_orders':comparison_orders,'scalar_orders':[3]*6,
            'formal_precision':4})
        base=[Fraction(0),Fraction(-1,2),Fraction(-1),Fraction(1,2399),Fraction(-32,407)]
        contacts=[[theta+shift for shift in shifts for theta in base] for shifts in ((2,4),(6,8))]
        poles=[-1,-2]
        for r,a in enumerate(scales):
            self.c.nonzero(a,f'detector{r}.scale')
            t=a*self.slope;delta=t-poles[r]
            self.c.nonzero(delta,f'detector{r}.normalizer')
            F=self.c.rational(1)
            for theta in contacts[r]:
                factor=t-theta;self.c.nonzero(factor,f'detector{r}.contact{theta}');F*=factor
            R=F/delta**10;combined=rs*R
            self.c.nonzero(R,f'detector{r}.contact function')
            self.c.nonzero(combined,f'detector{r}.combined coefficient')
            W=self.field(1)
            comparison_weights=[]
            for C,order in zip(tests,comparison_orders):
                weight=combined/(delta**2*combined**(2*order))
                comparison_weights.append(weight)
                W=self.mul(W,self.add(self.field(1),self.scale(self.square(C),weight)))
            normalized_scalar=[]
            for j,D in enumerate(scalar_tests):
                E=self.field(R**3*self.scalar_phi(R,D,f'detector{r}.scalar{j}'))
                normalized_scalar.append(E)
                W=self.mul(W,self.add(self.field(1),self.scale(self.square(E),combined/combined**6)))
            norm=W[0]**2-2*W[1]**2
            self.c.nonzero(norm,f'detector{r}.product norm')
            self.c.nonzero(W[0],f'detector{r}.trace numerator')
            # 4*combined/Tr(W^-1)^2=combined*Norm(W)^2/W_0^2.
            pole=combined*norm**2/W[0]**2
            self.zero_pole(pole,self.pole_structural[r],f'detector{r}')
            self.events.append({'operation':'combined_detector','index':r,'scale':self.rr(a),
                'argument':self.rr(t),'contacts':[str(theta) for theta in contacts[r]],
                'normalizing_point':poles[r],'delta':self.rr(delta),'F':self.rr(F),
                'contact_function':self.rr(R),'combined_coefficient':self.rr(combined),
                'normalized_scalar':[[self.rr(v) for v in E] for E in normalized_scalar],
                'comparison_weights':[self.rr(weight) for weight in comparison_weights],
                'scalar_weight':self.rr(combined/combined**6),
                'product_components':[self.rr(v) for v in W],
                'pole_input':self.rr(pole),'pole_square_multiplier':4})
        assert self.base_count==24 and len(self.relations)==11
        assert [r['degree'] for r in self.relations]==[4]*9+[2]*2
        return {
            'format':'shared-point-source-coefficient-dag/v1',
            'status':'Exact raw-comparison combined-pole coefficient family under the stated inherited arithmetic inputs. The chosen numerical exponent is not certified sufficient.',
            'source_commit':'34454098637ba9100b19071da55a38199589f5e0',
            'source_builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'additional_arithmetic_input':'Retains the elliptic group, pole obstruction and realization, simultaneous prime-pattern inputs, and the full modular realization used by the proved exponent-7/3 contact-height theorem. Uses the proved aggregate trace-height theorem. No additional abc hypothesis is used. Simultaneous preparation and global soundness are proved separately in the companion paper.',
            'family_parameter':{'name':'L','value':self.forced_exponent,'quantified':False,
                'constraint':'odd integer L>=3','sufficient_threshold_exists':True,
                'effective_threshold_known':False,'selected_member_certified_to_define_Z':False},
            'anchor_kind':'forced_prime_with_two_combined_poles','share_scalar_height_point':True,
            'retained_base_count':24,'total_polynomial_variables_after_finite_algebra':25,
            'variables':self.c.variables,'coefficient_dag':self.c.nodes,
            'finite_monic_relations':self.relations,'finite_generator_count':11,
            'monic_degree_product':{'base':2,'exponent':20},
            'closed_equations':[],'guard_numerators':sorted(self.c.guards),
            'all_quadratic_roots_nonzero':True,'guard_descriptions':self.c.guard_descriptions,
            'indexed_guard_polynomials':[],
            'finite_parameters':{f'pole_chart_detector{r}':[0] for r in range(2)},
            'comparison_tests':[[self.rr(v) for v in D] for D in tests],
            'scalar_tests':[self.rr(D) for D in scalar_tests],
            'comparison_orders':comparison_orders,'scalar_orders':[3]*6,
            'events':self.events,'counts':dict(Counter(v['category'] for v in self.c.variables)),
            'beta_formula':'216*input.X^4+450459','formal_precision':4,
            'comparison_normalization':'none',
            'scalar_normalization':'R*D/(1+R*D)',
            'scalar_switch_exponent':3,'scalar_norm_denominator_exponent':3,
            'common_index_divisible_by_selected_primes':True,
            'scalar_contact':self.rr(rs),'height_scales':[self.rr(a) for a in scales],
            'source_helpers':{name:hashlib.sha256((PINNED/name).read_bytes()).hexdigest()
                              for name in ('build_forced_prime_source.py','field_circuit.py',
                                           'compile_source.py','finite_algebra_core.py')},
            'semantics':'Twenty-four retained rational coordinates; nine finite quartic point roots and two nonzero quadratic pole roots. One finite-algebra coordinate gives 25. Every division is guarded. The scalar pole parameter pair is absent; its local requirements use linear normalization in both combined comparison products. Comparison functions are unnormalized. Extra common-index divisibility by the selected primes is used only in the completeness proof, not as an additional coordinate or equation.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--anchor-exponent',type=int,default=3)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();source=MergedBuilder(args.anchor_exponent).build()
    raw=(json.dumps(source,separators=(',',':'))+'\n').encode()
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'source.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    spec=compile_source(source,hashlib.sha256(raw).hexdigest())
    spec['arithmetic_status']='Under the stated inherited premises, the companion proof establishes sufficiently large fixed odd exponents. This selected numerical exponent has no certified sufficient threshold.'
    encoded=(json.dumps(spec,separators=(',',':'))+'\n').encode()
    (args.output/'source-polynomial-specification.json').write_bytes(encoded)
    receipt={'source_sha256':hashlib.sha256(raw).hexdigest(),
        'integer_specification_sha256':hashlib.sha256(encoded).hexdigest(),
        'retained_coordinates':24,'total_coordinates':25,'finite_point_quartics':9,
        'finite_pole_quadratics':2,'rank':2**20,
        'rational_source_nodes':len(source['coefficient_dag']),
        'integer_source_nodes':len(spec['coefficient_dag']),
        'selected_member_certified_to_define_Z':False,'family_parameter':source['family_parameter']}
    (args.output/'source-construction-certificate.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
