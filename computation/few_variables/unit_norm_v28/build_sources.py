#!/usr/bin/env python3
"""Construct guarded sources using free rank-four point algebras.

The retained coordinates and arithmetic tests are inherited from the pinned
v19/v22 sources. The changes are proved in unit_norm_20261114_v28.tex:
a homogeneous elliptic difference, multiplicative field norms, birational
pole rescaling, and (only for general25) an unsquared comparison scale.
No matrix of the full production rank is materialized here.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PINNED = HERE.parent / 'trace27_nontorsion'
for directory in ('trace27_nontorsion', 'merged25_v19',
                  'effective27_v19', 'direct_input13_v22'):
    sys.path.insert(0, str(HERE.parent / directory))
from field_circuit import Rational
from build_merged_source import MergedBuilder
from build_effective_source import EffectiveBuilder
from build_direct_input_source import DirectInputABCBuilder


class OptimizedArithmetic:
    """Exact operations in the point algebra, followed by square extensions."""

    @staticmethod
    def field_key(a):
        return tuple((v.n, v.d) for v in a)

    def remember_norm(self, a, norm):
        if not hasattr(self, '_norm_cache'):
            self._norm_cache = {}
        self._norm_cache[self.field_key(a)] = norm
        return a

    def norm(self, a):
        if not hasattr(self, '_norm_cache'):
            self._norm_cache = {}
        key = self.field_key(a)
        if key not in self._norm_cache:
            self._norm_cache[key] = a[0]**2 - 2*a[1]**2
        return self._norm_cache[key]

    def mul(self, a, b):
        result = (a[0]*b[0] + 2*a[1]*b[1], a[0]*b[1] + a[1]*b[0])
        return self.remember_norm(result, self.norm(a)*self.norm(b))

    def inv(self, a):
        norm = self.norm(a)
        return self.remember_norm((a[0]/norm, -a[1]/norm), 1/norm)

    def conj(self, a):
        return self.remember_norm((a[0], -a[1]), self.norm(a))

    def scale(self, a, r):
        return self.remember_norm((a[0]*r, a[1]*r), self.norm(a)*r*r)

    def point(self, name):
        self.c.point_count += 1
        h = self.abscissas[name]
        x = self.square(h)
        A, B = self.sub(self.square(x), self.D)
        u = self.c.variable(name+'.U', 'finite.point_block')
        v = self.c.variable(name+'.V', 'finite.point_block')
        w = self.c.variable(name+'.W', 'finite.point_block')
        # The basis is 1,U,V,W, NOT eight monomials in three generators.
        # U=2*j0, V=2*j1, W=j0^2-2*j1^2.
        j = self.remember_norm((u/2, v/2), w)
        point = {'h': h, 'j': j, 'x': x, 'y': self.mul(h, j)}
        self.relations.append(dict(name=name, kind='point_block', degree=4,
            A=self.rr(A), B=self.rr(B),
            variable_nodes=[u.n, v.n, w.n]))
        self.inv(point['x'])
        self.inv(point['y'])
        if name == 'S':
            self.fourfold_points[name] = self.difference(point, self.fixed_point())
        self.events.append(dict(operation='point_block', name=name,
            h=[self.rr(a) for a in h], A=self.rr(A), B=self.rr(B),
            j=[self.rr(a) for a in j], x=[self.rr(a) for a in point['x']],
            y=[self.rr(a) for a in point['y']]))
        return point

    def difference(self, a, b):
        x,y = a['x'],a['y']
        xx,yy = b['x'],b['y']
        dx = self.sub(x,xx)
        self.c.nonzero(self.norm(dx), 'difference abscissa denominator')
        numerator_x = self.add(
            self.mul(self.add(x,xx),self.sub(self.mul(x,xx),self.D)),
            self.scale(self.mul(y,yy),2))
        numerator_y = self.sub(
            self.mul(self.add(self.mul(y,xx),self.mul(yy,x)),self.square(dx)),
            self.mul(self.add(y,yy),numerator_x))
        return {'dx':dx,'X':numerator_x,'Y':numerator_y}

    def reciprocal(self, point):
        if 'dx' in point:
            return self.div(self.square(point['dx']),point['X'])
        return self.inv(point['x'])

    def parameter_at_identity(self, point):
        if 'dx' in point:
            return self.scale(self.div(self.mul(point['X'],point['dx']),point['Y']),-1)
        if 'h' in point:
            return self.scale(self.div(point['h'],point['j']),-1)
        return self.scale(self.div(point['x'],point['y']),-1)

    def logarithm(self, point, precision):
        if precision != 4:
            raise ValueError('This source implements only the fourth-order truncation.')
        return self.parameter_at_identity(point)

    def split_square(self, a):
        def split(node):
            factors = self.c.factors(node)
            odd = {k:e%2 for k,e in factors.items() if e%2}
            half = {k:e//2 for k,e in factors.items() if e//2}
            return self.c.from_factors(odd),self.c.from_factors(half)
        numerator, numerator_square = split(a.n)
        denominator, denominator_square = split(a.d)
        d = Rational(self.c,numerator,denominator)
        t = Rational(self.c,numerator_square,denominator_square)
        return d,t

    def zero_pole(self, b, structural, label):
        self.c.pole_count += 1
        tau,s = structural
        self.c.nonzero(b,label+'.nonzero input')
        d,t = self.split_square(b)
        self.c.nonzero(d,label+'.square class')
        self.c.nonzero(t,label+'.square multiplier')
        denominator = tau*tau+51*d
        self.c.nonzero(denominator,label+'.rescaled conic denominator')
        e = (tau*tau-17*d)/denominator
        v = 17*e*(17-b)
        radicand = 17*d*(s*s-v)*(s*s+3*v)
        self.finite_square(label+'.q',radicand,kind='pole')
        self.events.append(dict(operation='rescaled_zero_pole',label=label,
            input=self.rr(b),square_class=self.rr(d),square_multiplier=self.rr(t),
            e=self.rr(e),radicand=self.rr(radicand),
            inverse_coordinate_map='old_tau=t*tau; old_s=b*s; old_q=(b*t/17)*q'))

    def finish(self, name):
        explicit = name == 'explicit27'
        conditional = name in ('weak13','abc13')
        parameter = dict(name='B' if conditional else 'L',
            value=self.shift if conditional else self.forced_exponent,
            quantified=False, sufficient_threshold_exists=True,
            effective_threshold_known=explicit,
            selected_member_certified_to_define_Z=explicit and self.forced_exponent>=20483)
        if explicit:
            parameter['certified_sufficient_lower_bound'] = 20483
        return dict(format='point-block-guarded-source/v28',name=name,
            retained_base_count=self.base_count,total_external_variables=self.base_count+1,
            variables=self.c.variables,coefficient_dag=self.c.nodes,
            finite_blocks=self.relations,guard_numerators=sorted(self.c.guards),
            guard_descriptions=self.c.guard_descriptions,events=self.events,
            fixed_parameters={'fixed_input_shift':self.shift} if conditional else {},
            family_parameter=parameter,
            multiply_by_input=conditional,
            scale_power=self.scale_power if conditional else None,
            unsquared_comparison_scale=name=='general25',
            proof='papers/finite_algebra/unit_norm_20261114_v28.tex',
            arithmetic_status='Retains the explicitly stated arithmetic premises; finite verification is not an independent arithmetic audit.')


class General25(OptimizedArithmetic,MergedBuilder):
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
        comparison_orders=[1]*11+[3]*3+[1,3]
        scalar_orders=[1]*4+[3]*2
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
        scales=[self.c.rational(1),1+rs*trace**2]
        self.events.append({'operation':'combined_height_scales','beta':self.rr(beta),
            'trace':self.rr(trace),'raw_scalar_contact':self.rr(raw),
            'scalar_contact':self.rr(rs),'scalar_denominator':self.rr(scalar_denominator),
            'scales':[self.rr(a) for a in scales]})
        self.events.append({'operation':'comparison_and_scalar_tests',
            'comparison':[[self.rr(v) for v in D] for D in tests],
            'scalar':[self.rr(D) for D in scalar_tests],
            'L':[[self.rr(v) for v in D] for D in L],
            'Lprime':[[self.rr(v) for v in D] for D in Lprime],
            'comparison_orders':comparison_orders,'scalar_orders':scalar_orders,
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
            normalized_scalar=[];scalar_weights=[]
            for j,D in enumerate(scalar_tests):
                order=scalar_orders[j]
                E=self.field(R**order*self.scalar_phi(R,D,f'detector{r}.scalar{j}'))
                normalized_scalar.append(E)
                weight=combined/combined**(2*order)
                scalar_weights.append(weight)
                W=self.mul(W,self.add(self.field(1),self.scale(self.square(E),weight)))
            norm=self.norm(W)
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
                'scalar_weights':[self.rr(weight) for weight in scalar_weights],
                'product_components':[self.rr(v) for v in W],
                'pole_input':self.rr(pole),'pole_square_multiplier':4})
        assert self.base_count==24 and len(self.relations)==11
        assert [r['degree'] for r in self.relations]==[4]*9+[2]*2
        return self.finish('general25')


class Explicit27(OptimizedArithmetic,EffectiveBuilder):
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
        comparison_orders=[1]*11+[3]*3+[1,3]
        scalar_orders=[1]*4+[3]*2
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
        aggregate=[sum((p['x'][k] for p in roots),self.c.rational(0)) for k in range(2)]
        scales=[self.c.rational(1),(1+rs*aggregate[0]**2)**2,
                (1+rs*(aggregate[0]+aggregate[1])**2)**2]
        self.events.append({'operation':'combined_height_scales','beta':self.rr(beta),
            'aggregate_components':[self.rr(v) for v in aggregate],'raw_scalar_contact':self.rr(raw),
            'scalar_contact':self.rr(rs),'scalar_denominator':self.rr(scalar_denominator),
            'scales':[self.rr(a) for a in scales]})
        self.events.append({'operation':'comparison_and_scalar_tests',
            'comparison':[[self.rr(v) for v in D] for D in tests],
            'scalar':[self.rr(D) for D in scalar_tests],
            'L':[[self.rr(v) for v in D] for D in L],
            'Lprime':[[self.rr(v) for v in D] for D in Lprime],
            'comparison_orders':comparison_orders,'scalar_orders':scalar_orders,
            'formal_precision':4})
        base=[Fraction(0),Fraction(-1,2),Fraction(-1),Fraction(1,2399),Fraction(-32,407)]
        contacts=[[theta+shift for shift in shifts for theta in base] for shifts in ((2,4),(6,8),(10,12))]
        poles=[-1,-2,-3]
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
            normalized_scalar=[];scalar_weights=[]
            for j,D in enumerate(scalar_tests):
                order=scalar_orders[j]
                E=self.field(R**order*self.scalar_phi(R,D,f'detector{r}.scalar{j}'))
                normalized_scalar.append(E)
                weight=combined/combined**(2*order)
                scalar_weights.append(weight)
                W=self.mul(W,self.add(self.field(1),self.scale(self.square(E),weight)))
            norm=self.norm(W)
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
                'scalar_weights':[self.rr(weight) for weight in scalar_weights],
                'product_components':[self.rr(v) for v in W],
                'pole_input':self.rr(pole),'pole_square_multiplier':4})
        assert self.base_count==26 and len(self.relations)==12
        assert [r['degree'] for r in self.relations]==[4]*9+[2]*3
        return self.finish('explicit27')


class Conditional13(OptimizedArithmetic,DirectInputABCBuilder):
    def build(self):
        points={name:self.point(name) for name in self.point_names}
        A,H,U=[points[name] for name in self.point_names]
        V0=self.difference(H,self.fixed_point());V1=self.difference(U,A)
        beta=self.X**2+self.c.parameter('fixed_input_shift',self.shift)
        L=self.div(self.parameter_at_identity(U),self.parameter_at_identity(H))
        Lprime=self.conj(self.div(self.parameter_at_identity(V1),self.parameter_at_identity(V0)))
        tests=[self.reciprocal(H),self.reciprocal(U),self.conj(self.reciprocal(V0)),self.conj(self.reciprocal(V1)),self.sub(L,Lprime),self.sub(L,self.field(self.X))]
        orders=[1,1,1,1,1,1]
        squares=[self.square(test) for test in tests]
        trace=2*A['x'][0]
        compressed=beta**self.scale_power+trace**self.scale_power
        scales=[self.c.rational(1),compressed]
        self.events.append({'operation':'conditional_weak_abc_height_scales','beta':self.rr(beta),'trace':self.rr(trace),
            'sum_even_powers':self.rr(compressed),'power':self.scale_power,'target':self.rr(self.X),'scales':[self.rr(a) for a in scales],
            'height_premise':self.premise+'; direct-input height h(X)<=h(beta)/2'})
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
            norm=self.norm(W)
            self.c.nonzero(norm,f'detector{r}.product norm');self.c.nonzero(W[0],f'detector{r}.trace numerator')
            pole=F*norm*norm/(4*delta**8*W[0]*W[0])
            self.zero_pole(pole,self.pole_structural[r],f'detector{r}')
            self.events.append({'operation':'detector','index':r,'scale':self.rr(scale),'slope_argument':self.rr(t),
                'F':self.rr(F),'delta':self.rr(delta),'weights':{str(k):self.rr(v) for k,v in weights.items()},
                'product_components':[self.rr(v) for v in W],'pole_input':self.rr(pole)})
        assert self.base_count==12 and len(self.relations)==5
        assert [r['degree'] for r in self.relations]==[4,4,4,2,2]
        return self.finish('weak13' if self.scale_power == 6 else 'abc13')


def make_source(name: str, parameter: int | None = None) -> dict:
    if name == 'general25':
        return General25(3 if parameter is None else parameter).build()
    if name == 'explicit27':
        return Explicit27(20483 if parameter is None else parameter).build()
    if name in ('weak13','abc13'):
        return Conditional13(3 if parameter is None else parameter,
            6 if name == 'weak13' else 4).build()
    raise ValueError('Unknown construction: '+name)


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name',choices=['general25','explicit27','weak13','abc13'])
    parser.add_argument('--parameter',type=int)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    args.output.write_text(json.dumps(make_source(args.name,args.parameter),
        separators=(',',':'))+'\n')
