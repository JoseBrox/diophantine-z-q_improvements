#!/usr/bin/env python3
"""Independent exact reconstruction checks for the v30 finite specifications.

The producer's degree, affine-support and separator routines are not imported.
Finite algebra examples are tests; the universal implications are proved in TeX.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as sp
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = HERE.parent / 'unit_norm_v28'
sys.path.insert(0, str(OLD))
from build_sources import make_source
NAMES = ('general25', 'explicit27', 'weak13', 'abc13')


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()


def lg(n):
    return (max(1, n)-1).bit_length()


def low_basis(vectors):
    """Low-pivot elimination, independent of the producer's high-pivot code."""
    pivots = {}
    for x in vectors:
        require(isinstance(x, int) and x >= 0, 'Invalid binary vector')
        while x:
            low = x & -x
            if low not in pivots:
                pivots[low] = x
                break
            x ^= pivots[low]
    return tuple(pivots[k] for k in sorted(pivots))


def same_span(a, b):
    return len(low_basis(a)) == len(low_basis(b)) == len(low_basis((*a, *b)))


def arrays(source):
    """Iterative DAG bounds, factorization and affine parity support."""
    nodes = source['coefficient_dag']
    base = source['retained_base_count']
    points = [b for b in source['finite_blocks'] if b['kind'] == 'point_block']
    variables = {}
    for i, block in enumerate(points):
        x, y = 1 << (2*i), 1 << (2*i+1)
        for node, weight, norm, offset, dirs in zip(block['variable_nodes'],
                (2,2,4), (4,4,6), (x,x,x^y), ((x^y,),(x^y,),())):
            variables[nodes[node][1]] = (weight,norm,offset,dirs)
    ds, ls, supports, factorizations = [], [], [], []
    for index, (op, *a) in enumerate(nodes):
        if op == 'int':
            d, l, aff = 0, lg(abs(a[0])), (0,())
            fac = Counter({index:1})
        elif op == 'parameter':
            d, l, aff = 0, lg(abs(a[1])), (0,())
            fac = Counter({index:1})
        elif op == 'variable':
            if a[0] < base:
                d,l,off,dirs = 1,0,0,()
            elif a[0] in variables:
                d,l,off,dirs = variables[a[0]]
            else:
                d,l,off,dirs = None,None,None,None
            aff = None if off is None else (off,dirs)
            fac = Counter({index:1})
        elif op == 'neg':
            d,l,aff = ds[a[0]],ls[a[0]],supports[a[0]]
            fac = factorizations[a[0]].copy(); fac[-1] += 1
        elif op == 'pow':
            child,e = a
            d = None if ds[child] is None else e*ds[child]
            l = None if ls[child] is None else e*ls[child]
            if not e: aff = (0,())
            elif supports[child] is None: aff = None
            else:
                off,dirs = supports[child]; aff = (off if e%2 else 0,dirs)
            fac = Counter({v:e*m for v,m in factorizations[child].items()})
        elif op in ('add','mul'):
            d = None if any(ds[v] is None for v in a) else (max(ds[v] for v in a) if op=='add' else sum(ds[v] for v in a))
            l = None if any(ls[v] is None for v in a) else (max(ls[v] for v in a)+lg(len(a)) if op=='add' else sum(ls[v] for v in a))
            if any(supports[v] is None for v in a): aff = None
            elif op == 'add':
                off = supports[a[0]][0]
                dirs = [r for v in a for r in supports[v][1]] + [off^supports[v][0] for v in a]
                aff = off,low_basis(dirs)
            else:
                off = 0
                for v in a: off ^= supports[v][0]
                aff = off,low_basis(r for v in a for r in supports[v][1])
            fac = Counter({index:1}) if op=='add' else sum((factorizations[v] for v in a),Counter())
        else: raise AssertionError('Unrecognized circuit operation: '+op)
        sign = fac.pop(-1,0)
        for node in list(fac):
            if nodes[node] == ['int',-1]: sign += fac.pop(node)
            elif nodes[node] == ['int',1]: fac.pop(node)
        if sign%2: fac[-1] = 1
        ds.append(d);ls.append(l);supports.append(aff);factorizations.append(+fac)
    return ds,ls,supports,factorizations,points


def normalized(sign, factors):
    result = Counter(dict(factors))
    if sign == -1: result[-1] += 1
    if result[-1]%2: result[-1] = 1
    else: result.pop(-1,None)
    return +result


def verify_spec(source, spec):
    nodes = source['coefficient_dag'];base = source['retained_base_count']
    ds,ls,affs,factors,points = arrays(source)
    poles = [b for b in source['finite_blocks'] if b['kind']=='pole']
    old = json.loads((OLD/'specifications'/(source['name']+'.json')).read_text())
    require(spec['schema']=='subalgebra-norm-polynomial-specification/v30','Schema')
    require(spec['native_source_sha256']==digest(canonical(source)),'Source hash')
    require(spec['native_source_arguments']==dict(name=source['name'],parameter=source['family_parameter']['value']),'Source generation arguments')
    require(spec['family_parameter']==source['family_parameter'],'Fixed coefficient parameter')
    require(spec['point_blocks']==points,'Unchanged point blocks')
    require(spec['external_variables']==old['external_variables'],'Retained variable accounting')
    require(spec['multiply_by_input']==source['multiply_by_input'],'Input zero factor')
    require(len(spec['quadratic_reductions'])==len(poles),'Number of pole roots')
    guard_rows = spec['guard_factorizations']
    require(len(guard_rows)==len(set(source['guard_numerators'])),'Guard duplication or omission')
    require({g['node'] for g in guard_rows}==set(source['guard_numerators']),'Every source guard')
    support = set();pole_nodes = {b['generator_node'] for b in poles}
    for row in guard_rows:
        require(normalized(row['sign'],row['factors'])==factors[row['node']],'Exact factorization')
        support.update(v for v in factors[row['node']] if v != -1 and v not in pole_nodes)
    for block,row in zip(poles,spec['quadratic_reductions']):
        native = block['coefficient_nodes_ascending'][0]
        target = factors[native].copy();target[-1] += 1
        target = normalized(1,target.items())
        rec = Counter(row['odd_factor_nodes'])
        for node,e in row['square_multiplier_factors']:rec[node] += 2*e
        require(normalized(row['sign'],rec.items())==target,'Pole square extraction')
        square = block['original_square_input']
        require(normalized(1,(factors[square['numerator']]+factors[square['denominator']]).items())==target,'Rational square clearing')
        support.update(v for v in target if v != -1)
        d,l = sum(ds[v] for v in row['odd_factor_nodes']),sum(ls[v] for v in row['odd_factor_nodes'])
        require((row['degree_bound'],row['operator_log2_norm_bound'],row['root_weight'],row['root_log2_norm_bound'])==(d,l,(d+1)//2,(l+1)//2+1),'Pole majorants')
    support = {v for v in support if nodes[v][0]!='int'}
    guards = spec['subalgebra_norm_factors']
    require(len(guards)==len(support) and {g['node'] for g in guards}==support,'Full norm-factor coverage')
    dimensions = Counter()
    for g in guards:
        off,dirs = affs[g['node']]
        require(same_span(dirs,g['affine_directions']) and same_span(dirs,(*g['affine_directions'],off^g['affine_offset'])),'Affine support coset')
        basis = low_basis((off,*dirs));reported=g['subspace_basis']
        require(same_span(basis,reported),'Guard subalgebra support')
        require(len(reported)==len(low_basis(reported)),'Independent listed subspace basis')
        dim=len(basis);rank=1<<dim
        swapped=[]
        for v in basis:
            w=0
            for i in range(len(points)):
                w ^= ((v>>(2*i))&1)<<(2*i+1)
                w ^= ((v>>(2*i+1))&1)<<(2*i)
            swapped.append(w)
        require(same_span(basis,swapped),'Galois-stable norm algebra')
        require((g['subspace_dimension'],g['subalgebra_rank'])==(dim,rank),'Subalgebra rank')
        require((g['element_degree_bound'],g['element_operator_log2_norm_bound'])==(ds[g['node']],ls[g['node']]),'Factor degree and coefficient bounds')
        require((g['scalar_norm_degree_bound'],g['scalar_norm_log2_l1_bound'])==(rank*ds[g['node']],rank*ls[g['node']]),'Scalar norm bounds')
        dimensions[dim]+=1
    # All rational denominators recorded by the source must still be covered.
    count=0
    def visit(obj):
        nonlocal count
        if isinstance(obj,dict):
            if {'numerator','denominator'}<=obj.keys():
                count+=1
                require(all(v==-1 or nodes[v][0]=='int' or v in support for v in factors[obj['denominator']]),'Uncovered denominator')
            for v in obj.values():visit(v)
        elif isinstance(obj,list):
            for v in obj:visit(v)
    visit(source['events']);visit(source['finite_blocks'])
    td=[]
    for i in range(len(points)):
        td += [(8,11,4,6),(12,20,6,12)]
    td += [(r['degree_bound'],r['operator_log2_norm_bound'],r['root_weight'],r['root_log2_norm_bound']) for r in spec['quadratic_reductions']]
    tower=spec['quadratic_tower']
    require(len(tower)==len(td),'Tower length')
    es=[];vs=[]
    for i,(row,(d,l,w,h)) in enumerate(zip(tower,td)):
        require((row['degree'],row['operator_log2_norm'],row['root_weight'],row['root_operator_log2_norm'])==(d,l,w,h),'Tower majorants')
        k=(d+3)//4;g=(l+1)//2;e=2*k;v=g+k*lg(base+1)
        require((row['envelope_power'],row['envelope_constant_exponent'],row['envelope_degree'],row['envelope_log2_l1'])==(k,g,e,v),'Root envelope')
        es.append(e);vs.append(v)
    termds=[];termls=[]
    for i,row in enumerate(spec['separator_term_bounds']):
        d=es[i]+td[i][2]+sum(v[0] for v in td[:i])+2*sum(es[i+1:])
        l=1+vs[i]+td[i][3]+sum(v[1] for v in td[:i])+2*(len(td)-i-1)+2*sum(vs[i+1:])
        require(row==dict(index=i,degree=d,operator_log2_norm=l),'Separator term bound')
        termds.append(d);termls.append(l)
    require(len(termds)==len(td),'All separator terms')
    gd=sum(g['scalar_norm_degree_bound'] for g in guards)
    gl=sum(g['scalar_norm_log2_l1_bound'] for g in guards)
    od=max(termds);ol=max(termls)+lg(len(td));n=4**len(points)*2**len(poles)
    deg=n*(gd+od+1);norm=n*(gl+ol+1);variables=base+1
    monomials=math.comb(deg+variables,variables)-math.comb(deg-n+variables-1,variables)
    expected=dict(total_variables=variables,point_blocks=len(points),pole_quadratics=len(poles),full_rank=n,
        guard_factors=len(guards),scalar_guard_degree_bound=gd,scalar_guard_log2_l1_bound=gl,
        separator_degree_bound=od,separator_operator_log2_norm_bound=ol,
        degree_before_input_factor=deg,degree_bound=deg+int(source['multiply_by_input']),
        strict_degree_power_of_two=(deg+int(source['multiply_by_input'])).bit_length(),
        separator_variable_degree_bound=n,coefficient_log2_l1_bound=norm,
        coefficient_height_double_power_exponent=norm.bit_length(),monomial_upper_bound=str(monomials),
        support_strict_power_of_two=monomials.bit_length(),integer_content=1)
    require(spec['bounds']==expected,'Complete final bound dictionary')
    require(expected['degree_bound']<old['bounds']['degree_bound'],'Strict improvement over v28')
    return dict(name=source['name'],native_source_sha256=spec['native_source_sha256'],
        source_nodes=len(nodes),source_guards=len(guard_rows),rational_denominators=count,
        norm_factors=len(guards),norm_dimension_distribution={str(k):v for k,v in sorted(dimensions.items())},
        degree_bound=expected['degree_bound'],coefficient_log2_l1_bound=norm,
        specification_sha256=digest(canonical(spec)))


def symbolic_checks():
    A,B=sp.symbols('A B');I=sp.eye(4)
    U=sp.Matrix([[0,2*A,2*B,0],[1,0,0,A],[0,0,0,-2*B],[0,2,0,0]])
    V=sp.Matrix([[0,2*B,A,0],[0,0,0,B],[1,0,0,-A],[0,0,-1,0]])
    W=sp.Matrix([[0,0,0,A*A-2*B*B],[0,A,B,0],[0,-2*B,-A,0],[1,0,0,0]])
    Ap=6*A**3-9*A*B**2-4*B**3;Bp=-4*A**3+6*A*B**2+3*B**3
    M=2*A*A-B*B;N=A*A-2*B*B;Z=(2*A+B)*U-2*(A+B)*V
    checks=[W*W-N*I,Z*Z-2*Ap*I-2*M*W,
        (U+sp.sqrt(2)*V)**2/4-(A+sp.sqrt(2)*B)*I,
        (U-sp.sqrt(2)*V)**2/4-(A-sp.sqrt(2)*B)*I,
        (U+sp.sqrt(2)*V)*(U-sp.sqrt(2)*V)/4-W]
    for c in checks: require(all(sp.expand(x)==0 for x in c),'Quadratic-tower identity')
    require(sp.expand(Ap**2-M**2*N-2*Bp**2)==0,'Primitive radicand product')
    require(sp.expand((I+U*U).det()-(1+4*A+8*B*B)**2)==0,'Rank-two norm removes a square')
    require(sp.expand((I+W).det()-(1-A*A+2*B*B)**2)==0,'Second rank-two norm')
    require(sp.expand(U.det()-8*B*B)==0,'Full-rank norm')
    require(28**2+2*18**2 < 2**11,'Norm-radicand coefficient bound')
    apcap=6*28**3+9*28*18**2+4*18**3
    mcap=2*28**2+18**2
    require(2*apcap+2*mcap*64 < 2**20,'Primitive-radicand coefficient bound')
    require((2*28+18)*16+2*(28+18)*16 < 2**12,'Primitive operator bound')
    # A non-stable subspace cannot be silently used as a rational norm algebra.
    require(not same_span((1,),(2,)),'Non-stable subspace corruption control')
    require(sp.expand((I+U*U).det()-(1+4*A+8*B*B))!=0,'Missing norm power negative control')
    return dict(matrix_identities=len(checks),scalar_identity=True,exact_norm_identities=3,
        operator_bounds=[11,20,12],nonstable_subspace_rejected=True,incorrect_full_norm_rejected=True)


def tower_examples():
    """Exact regular-representation examples, with no floating-point roots."""
    t=sp.Symbol('t');records=[]
    cases=[(3,2,'square'),(3,2,'nonsquare'),(3,2,'negative'),(3,2,'tiny'),
           (3,2,'dependent_square'),(3,2,'zero_guard'),(0,1,'square'),(-3,2,'square'),(1,0,'square')]
    for aa,bb,kind in cases:
        A,B=sp.Rational(aa),sp.Rational(bb);I=sp.eye(4)
        U=sp.Matrix([[0,2*A,2*B,0],[1,0,0,A],[0,0,0,-2*B],[0,2,0,0]])
        V=sp.Matrix([[0,2*B,A,0],[0,0,0,B],[1,0,0,-A],[0,0,-1,0]])
        W=U*U/2-A*I;N=A*A-2*B*B;Ap=6*A**3-9*A*B**2-4*B**3;M=2*A*A-B*B
        Z=(2*A+B)*U-2*(A+B)*V
        c={'square':4*I,'nonsquare':2*I,'negative':-I,'tiny':I/sp.Integer(10)**12,
           'dependent_square':(U+I)**2,'zero_guard':I+W}[kind]
        G=c.det()
        c0=N*I;c1=2*Ap*I+2*M*W
        envelopes=[int(sp.ceiling(1+sum(abs(v) for v in x))) for x in (c0,c1,c)]
        lift=lambda x:sp.diag(x,x)
        cs=[lift(c0),lift(c1),lift(c)]
        qs=[lift(W),lift(Z),sp.BlockMatrix([[sp.zeros(4),c],[I,sp.zeros(4)]]).as_explicit()]
        omega=sp.zeros(8)
        for i in range(3):
            term=2*envelopes[i]*qs[i]
            for k in range(i):term=term*cs[k]
            for k in range(i+1,3):term=term*(4*envelopes[k]**2)
            omega+=term
        if not G:
            require((sp.eye(8)-t*G*omega).det()==1,'Zero guard excludes a nonreduced boundary')
            records.append(dict(A=aa,B=bb,case=kind,guard='0',polynomial_is_one=True));continue
        char=omega.charpoly(t).as_expr();poly=sp.Poly(char,t)
        require(poly.eval(0)!=0,'Nonzero separating values')
        require(sp.gcd(poly,poly.diff()).degree()==0,'All eight values separated')
        roots=sp.polys.polytools.ground_roots(poly)
        expected=0
        # Enumerate rational characters of the point block from the equations.
        wroots=sp.polys.polytools.ground_roots(sp.Poly(t*t-N,t))
        for w in wroots:
            uroots=sp.polys.polytools.ground_roots(sp.Poly(t*t-2*A-2*w,t))
            vroots=sp.polys.polytools.ground_roots(sp.Poly(t*t-A+w,t))
            for u,v in itertools.product(uroots,vroots):
                if u*v!=2*B:continue
                cv={'square':sp.Rational(4),'nonsquare':sp.Rational(2),'negative':sp.Rational(-1),
                    'tiny':sp.Rational(1,10**12),'dependent_square':(u+1)**2}[kind]
                expected+=len(sp.polys.polytools.ground_roots(sp.Poly(t*t-cv,t)))
        require(len(roots)==expected,'Rational zero/character equivalence in the exact example')
        # Two independent ways of clearing the recursive separator.
        phi=sp.zeros(8)
        for q,cj,m in reversed(list(zip(qs,cs,envelopes))):phi=q/(2*m)+cj*phi/(4*m*m)
        den=math.prod(4*m*m for m in envelopes)
        require(phi*den==omega,'Cleared separator versus nested recursion')
        records.append(dict(A=aa,B=bb,case=kind,guard=str(G),rank=8,
            rational_character_count=expected,distinct_nonzero_eigenvalues=True,
            characteristic_sha256=digest(str(poly.as_expr()).encode())))
    # A repeated radicand is not grounds for reducing the free-algebra rank.
    I=sp.eye(4);q0=sp.kronecker_product(sp.Matrix([[0,2],[1,0]]),sp.eye(2));q1=sp.kronecker_product(sp.eye(2),sp.Matrix([[0,2],[1,0]]))
    bad=q0+q1
    require(bad.det()==0,'Dependent-squareclass nonseparating control')
    return dict(examples=records,dependent_squareclass_collision_detected=True)


def split_character_checks(directory):
    """Check every norm factor on all 64 split characters of each 13-var source."""
    prime=1000000007
    require(sp.isprime(prime) and prime%4==3,'Exact prime fixture')
    sqrt2=pow(2,(prime+1)//4,prime)
    require(sqrt2*sqrt2%prime==2,'Split coefficient field')
    records=[]
    for name in ('weak13','abc13'):
        source=make_source(name);nodes=source['coefficient_dag']
        spec=json.loads((directory/(name+'.json')).read_text())
        pblocks=[r for r in source['finite_blocks'] if r['kind']=='point_block']
        values=[2*i+11 for i in range(len(source['variables']))]
        roots=[];point_pairs=[]
        for i,block in enumerate(pblocks):
            found=False
            for x in range(2+7*i,90):
                for y in range(1+3*i,30):
                    A=(x**4+12*x*x*y*y+4*y**4-11)%prime
                    B=(4*x**3*y+8*x*y**3+6)%prime
                    rr=[(A+sqrt2*B)%prime,(A-sqrt2*B)%prime]
                    rt=[pow(v,(prime+1)//4,prime) for v in rr]
                    if all(v and z*z%prime==v for v,z in zip(rr,rt)):
                        point_pairs.append((x,y));roots+=rt
                        values[1+2*i]=x;values[2+2*i]=y;found=True;break
                if found:break
            require(found,'Split point fixture')
        norm_factors=spec['subalgebra_norm_factors'];all_values=[]
        for sign in range(64):
            for i,block in enumerate(pblocks):
                xi=(-roots[2*i] if sign&(1<<(2*i)) else roots[2*i])%prime
                eta=(-roots[2*i+1] if sign&(1<<(2*i+1)) else roots[2*i+1])%prime
                uvw=((xi+eta)%prime,(xi-eta)*pow(sqrt2,-1,prime)%prime,xi*eta%prime)
                for node,value in zip(block['variable_nodes'],uvw):values[nodes[node][1]]=value
            evaluated=[]
            for op,*a in nodes:
                if op=='int':v=a[0]
                elif op=='parameter':v=a[1]
                elif op=='variable':v=values[a[0]]
                elif op=='neg':v=-evaluated[a[0]]
                elif op=='pow':v=pow(evaluated[a[0]],a[1],prime)
                elif op=='add':v=sum(evaluated[k] for k in a)
                elif op=='mul':
                    v=1
                    for k in a:v=v*evaluated[k]%prime
                else:raise AssertionError('Unknown circuit operation')
                evaluated.append(v%prime)
            all_values.append([evaluated[f['node']] for f in norm_factors])
        certificate=[];zero_factors=0
        for j,f in enumerate(norm_factors):
            vals=[row[j] for row in all_values];groups={}
            for sign,value in enumerate(vals):
                restriction=tuple((sign&v).bit_count()%2 for v in f['subspace_basis'])
                if restriction in groups:require(groups[restriction]==value,'Constant on every subalgebra-character fiber')
                groups[restriction]=value
            require(len(groups)==f['subalgebra_rank'],'Every subalgebra character realized')
            small=math.prod(groups.values())%prime;full=math.prod(vals)%prime
            require(pow(small,64//len(groups),prime)==full,'Exact smaller/full norm identity')
            transformed=vals[:];step=1
            while step<64:
                for k in range(0,64,2*step):
                    for q in range(step):
                        a,b=transformed[k+q],transformed[k+q+step]
                        transformed[k+q]=(a+b)%prime;transformed[k+q+step]=(a-b)%prime
                step*=2
            actual=[k for k,v in enumerate(transformed) if v]
            dirs=f['affine_directions'];off=f['affine_offset']
            for v in actual:
                require(same_span(dirs,(*dirs,v^off)),'Fourier support inside the recorded affine space')
            if not small:zero_factors+=1
            certificate.append((f['node'],small,len(actual)))
        require(zero_factors==0,'Nonzero full-unit finite-field fixture')
        records.append(dict(name=name,prime=prime,point_pairs=point_pairs,full_point_characters=64,
            norm_factors=len(norm_factors),all_character_fibers_checked=True,all_affine_supports_checked=True,
            smaller_norms_sha256=digest(canonical(certificate))))
    return records


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--directory',type=Path,default=HERE/'specifications');ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    constructions=[];mutations=[]
    for name in NAMES:
        source=make_source(name);spec=json.loads((args.directory/(name+'.json')).read_text())
        constructions.append(verify_spec(source,spec))
        for label,mutate in [
            ('degree',lambda s:s['bounds'].__setitem__('degree_bound',s['bounds']['degree_bound']-1)),
            ('guard_omission',lambda s:s['subalgebra_norm_factors'].pop()),
            ('rank',lambda s:s['subalgebra_norm_factors'][-1].__setitem__('subalgebra_rank',1)),
            ('root_bound',lambda s:s['quadratic_tower'][-1].__setitem__('envelope_power',0)),
            ('source_hash',lambda s:s.__setitem__('native_source_sha256','0'*64))]:
            altered=deepcopy(spec);mutate(altered)
            try:verify_spec(source,altered)
            except AssertionError:mutations.append(name+':'+label)
            else:raise AssertionError('Undetected mutation: '+name+':'+label)
    symbolic=symbolic_checks();examples=tower_examples();split_checks=split_character_checks(args.directory)
    report=dict(schema='subalgebra-norm-exact-verification/v30',status='PASS',constructions=constructions,
        symbolic_checks=symbolic,finite_algebra_checks=examples,split_character_checks=split_checks,mutation_controls=mutations,
        global_variable_count_improvement=False,independent_mathematical_review=False,
        scope='Independent circuit, factor, affine-support, norm-rank, degree and coefficient-bound checks; symbolic identities and nine exact small regular-representation examples. Production determinants are not expanded. Universal separation and completeness are proved in the manuscript; inherited infinite arithmetic assumptions are not computationally certified.')
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
