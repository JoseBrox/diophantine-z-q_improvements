#!/usr/bin/env python3
"""Independent exact checks for the v28 formulas, specifications and bounds.

Universal polynomial identities are distinguished from finite-field tests.
No check here establishes the infinite arithmetic premises or full-unit
completeness theorem; those are separately stated in the manuscript.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import sys
sys.dont_write_bytecode = True
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
from build_sources import make_source
from build import compile_specification, canonical
sys.path.insert(0,str(HERE.parent/'direct_input13_v22'))
from check_direct_input_source import QuadraticArithmetic


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def symbolic_identities():
    A,B,Z=sp.symbols('A B Z')
    eye=sp.eye(4)
    # Columns are images of 1,U,V,W. Independently transcribed from the paper.
    U=sp.Matrix([[0,2*A,2*B,0],[1,0,0,A],[0,0,0,-2*B],[0,2,0,0]])
    V=sp.Matrix([[0,2*B,A,0],[0,0,0,B],[1,0,0,-A],[0,0,-1,0]])
    W=sp.Matrix([[0,0,0,A*A-2*B*B],[0,A,B,0],[0,-2*B,-A,0],[1,0,0,0]])
    matrices=[eye,U,V,W]
    def zero(M):
        require(all(sp.expand(x)==0 for x in M),'Point multiplication identity')
    for M,N in itertools.product(matrices,repeat=2):
        zero(M*N-N*M)
        column=(M*N)[:,0]
        zero(M*N-sum((column[k]*matrices[k] for k in range(4)),sp.zeros(4)))
    zero(U*U+2*V*V-4*A*eye);zero(U*V-2*B*eye)
    zero(U*U/4-V*V/2-W)
    primitive=(2*A+B)*U-2*(A+B)*V
    Ap=6*A**3-9*A*B**2-4*B**3
    Bp=-4*A**3+6*A*B**2+3*B**3
    f=Z**4-4*Ap*Z**2+8*Bp**2
    require(sp.expand(primitive.charpoly(Z).as_expr()-f)==0,'Primitive characteristic polynomial')
    corrupted=U.copy();corrupted[0,1]+=1
    require(any(sp.expand(v)!=0 for v in corrupted*V-V*corrupted),'Point-table corruption control')
    expected=2**15*Bp**2*(2*A*A-B*B)**4*(A*A-2*B*B)**2
    require(sp.expand(sp.discriminant(f,Z)-expected)==0,'Primitive discriminant')
    m0,m1=2*A+B,-A-B;norm=m0*m0-2*m1*m1
    zero(norm*U*primitive-m0*primitive**2+4*m1*Bp*eye)
    zero(norm*V*primitive+m1*primitive**2-2*m0*Bp*eye)
    # Bound column norms after substituting coefficient l1 majorants.
    scales=[1,16,16,64];caps=[16,16,64]
    maxima=[]
    for M,cap in zip((U,V,W),caps):
        columns=[]
        for j in range(4):
            column=0
            for i in range(4):
                polynomial=sp.Poly(M[i,j],A,B)
                bound=sum(abs(int(c))*28**e[0]*18**e[1] for e,c in polynomial.terms())
                column+=F(bound*scales[i],scales[j])
            columns.append(column)
        require(max(columns)<=cap,'Weighted point-block norm')
        maxima.append(str(max(columns)))
    # Difference formulas hold in the ideal of the two curve equations.
    x,y,a,b,D=sp.symbols('x y a b D')
    d=x-a;xn=(x+a)*(x*a-D)+2*y*b
    yn=(y*a+b*x)*d*d-(y+b)*xn
    G=sp.groebner([y*y-x**3+D*x,b*b-a**3+D*a],y,b,x,a,D)
    rx=(y+b)**2-(x+a)*d*d-xn
    ry=(y+b)*x*d*d-y*d**3-(y+b)*xn-yn
    require(G.reduce(sp.expand(rx))[1]==0,'Homogeneous abscissa identity')
    require(sp.expand(ry)==0,'Homogeneous ordinate identity')
    # Invertible pole rescaling, with b=d*t^2, including the ordinate.
    d,t,tau,s=sp.symbols('d t tau s',nonzero=True)
    bv=d*t*t;B0=17*bv
    eo=((t*tau)**2-B0)/((t*tau)**2+3*B0)
    en=(tau*tau-17*d)/(tau*tau+51*d)
    require(sp.cancel(eo-en)==0,'Conic rescaling')
    vo=B0*eo*(B0-bv*bv)
    oldrad=((bv*s)**2-vo)*((bv*s)**2+3*vo)/B0
    newrad=17*d*(s*s-17*en*(17-bv))*(s*s+51*en*(17-bv))
    require(sp.cancel(oldrad-(bv*t/17)**2*newrad)==0,'Second ordinate rescaling')
    require(sp.cancel(-4*B0*t*tau/((t*tau)**2+3*B0)+68*d*t*tau/(tau*tau+51*d))==0,'First ordinate rescaling')
    require(sp.cancel(oldrad-(bv*t)**2*newrad)!=0,'Wrong rescaling negative control')
    # The torsion polynomial used by the retained density proof.
    require(all((3*k**4+8*k**3-18*k*k-9)%5 for k in range(5)),'Mod-five torsion test')
    return dict(point_product_identities=16,primitive_characteristic_polynomial=True,
        primitive_discriminant=True,primitive_recovery_identities=2,
        weighted_point_operator_norms=maxima,point_table_corruption_rejected=True,homogeneous_difference_identities=2,
        pole_rescaling_identities=3,wrong_ordinate_rescaling_rejected=True,
        torsion_polynomial_mod_five=True)


def structural_check(source,spec):
    nodes=source['coefficient_dag'];base=source['retained_base_count']
    blocks=source['finite_blocks'];points=[b for b in blocks if b['kind']=='point_block']
    poles=[b for b in blocks if b['kind']=='pole'];p=len(points);s=len(poles)
    weights={};logs={}
    for block in points:
        for node,w,l in zip(block['variable_nodes'],(2,2,4),(4,4,6)):
            require(nodes[node][0]=='variable','Block generator node')
            weights[nodes[node][1]]=w;logs[nodes[node][1]]=l
    # Iterative traversal, independently of the producer's recursive code.
    degrees=[];norms=[];factorizations=[]
    ceil=lambda n:(max(1,n)-1).bit_length()
    for index,(op,*a) in enumerate(nodes):
        if op=='int':
            deg=0;log=ceil(abs(a[0]));fs=Counter() if a[0]==1 else Counter({index:1})
        elif op=='parameter':
            deg=0;log=ceil(abs(a[1]));fs=Counter({index:1})
        elif op=='variable':
            deg=1 if a[0]<base else weights.get(a[0],None)
            log=0 if a[0]<base else logs.get(a[0],None)
            fs=Counter({index:1})
        elif op=='neg':
            deg=degrees[a[0]];log=norms[a[0]];fs=factorizations[a[0]].copy();fs[-1]+=1
        elif op=='pow':
            deg=None if degrees[a[0]] is None else degrees[a[0]]*a[1]
            log=None if norms[a[0]] is None else norms[a[0]]*a[1]
            fs=Counter({k:e*a[1] for k,e in factorizations[a[0]].items()})
        elif op in ('add','mul'):
            deg=None if any(degrees[k] is None for k in a) else (max(degrees[k] for k in a) if op=='add' else sum(degrees[k] for k in a))
            log=None if any(norms[k] is None for k in a) else ((max(norms[k] for k in a)+ceil(len(a))) if op=='add' else sum(norms[k] for k in a))
            fs=Counter({index:1}) if op=='add' else sum((factorizations[k] for k in a),Counter())
        else:raise AssertionError(op)
        # Normalize -1 atom and formal unary negation to a parity bit.
        sign=fs.pop(-1,0)
        for k in list(fs):
            if nodes[k]==['int',-1]:sign+=fs.pop(k)
            elif nodes[k]==['int',1]:fs.pop(k)
        if sign%2:fs[-1]=1
        degrees.append(deg);norms.append(log);factorizations.append(fs)
    def normalized(sign,factors):
        c=Counter(dict(factors))
        if sign==-1:c[-1]+=1
        if c[-1]%2:c[-1]=1
        else:c.pop(-1,None)
        return +c
    support=set();pole_nodes={b['generator_node'] for b in poles}
    require(set(r['node'] for r in spec['guard_factorizations'])==set(source['guard_numerators']),'Guard list completeness')
    for record in spec['guard_factorizations']:
        fs=factorizations[record['node']]
        require(normalized(record['sign'],record['factors'])==fs,'Exact guard factorization')
        support.update(k for k in fs if k!=-1 and k not in pole_nodes)
    for block,r in zip(poles,spec['quadratic_reductions']):
        native=block['coefficient_nodes_ascending'][0]
        c=factorizations[native].copy();c[-1]+=1
        if c[-1]%2:c[-1]=1
        else:c.pop(-1,None)
        recovered=Counter(r['odd_factor_nodes'])
        for k,e in r['square_multiplier_factors']:recovered[k]+=2*e
        require(normalized(r['sign'],recovered.items())==c,'Exact quadratic square extraction')
        support.update(k for k in c if k!=-1)
        require(r['degree_bound']==sum(degrees[k] for k in r['odd_factor_nodes']),'Quadratic degree')
        require(r['operator_log2_norm_bound']==sum(norms[k] for k in r['odd_factor_nodes']),'Quadratic norm')
        require(r['root_weight']==(r['degree_bound']+1)//2,'Root weight')
        require(r['root_log2_norm_bound']==(r['operator_log2_norm_bound']+1)//2+1,'Root norm')
        # Cleared radicand is exactly numerator*denominator, up to sign.
        square=block['original_square_input'];expected=factorizations[square['numerator']]+factorizations[square['denominator']]
        require(normalized(1,expected.items())==c,'Rational square clearing')
    support={k for k in support if nodes[k][0]!='int'}
    require(support==set(r['node'] for r in spec['support_factor_bounds']),'Full support coverage')
    for row in spec['support_factor_bounds']:
        require(row['degree']==degrees[row['node']] and row['log_norm']==norms[row['node']],'Support bounds')
    # Every recorded rational denominator must be covered, including factors
    # introduced by cancellation and inverse-coordinate reconstruction.
    rational_count=0
    def inspect(obj):
        nonlocal rational_count
        if isinstance(obj,dict):
            if set(('numerator','denominator'))<=obj.keys():
                rational_count+=1
                factors=factorizations[obj['denominator']]
                require(all(k==-1 or nodes[k][0]=='int' or k in support for k in factors),'Uncovered rational denominator')
            for value in obj.values():inspect(value)
        elif isinstance(obj,list):
            for value in obj:inspect(value)
    inspect(source['events']);inspect(blocks)
    require(hashlib.sha256(canonical(source)).hexdigest()==spec['native_source_sha256'],'Canonical source hash')
    b=4**p;n=b*2**s;rad=spec['quadratic_reductions'];V=base+1
    t=sum(degrees[k] for k in support);tl=sum(norms[k] for k in support)
    zd=48;zl=78+ceil(2+2*p);dd=144*p;dl=234*p
    cd=288+dd;cl=5*(1+zl)+p+dl+zl+3
    sd=2*max(r['degree_bound']+4*p for r in rad)
    sl=ceil(b)+ceil(1+s*b*b)+2*max(r['operator_log2_norm_bound']+6*p for r in rad)
    qd=s*sd;ql=s*sl+2*s-1
    pd=qd+max((p+1)*cd,*[i*dd+(p+1-i)*cd+6 for i in range(1,p+1)])
    pl=ql+ceil(p+1)+max((p+1)*cl,*[i*dl+(p+1-i)*cl+12 for i in range(1,p+1)])
    xd=max((s-j-1)*sd+sum(r['degree_bound'] for r in rad[:j])+rad[j]['root_weight'] for j in range(s))
    xl=ceil(s)+max((s-j-1)*(sl+2)+sum(r['operator_log2_norm_bound'] for r in rad[:j])+rad[j]['root_log2_norm_bound'] for j in range(s))
    od=max(pd,(p+1)*dd+xd);ol=1+max(pl,(p+1)*dl+xl)
    degree=n*(b*t+od+1);norm=n*(b*tl+ol+1)
    bc=spec['bounds']
    expected=dict(total_variables=V,point_blocks=p,pole_quadratics=s,point_rank=b,full_rank=n,
        support_weight=t,support_operator_log2_norm_bound=tl,separator_degree_bound=od,
        separator_operator_log2_norm_bound=ol,degree_before_input_factor=degree,
        degree_bound=degree+int(source['multiply_by_input']),separator_variable_degree_bound=n,
        coefficient_l1_log2_bound=norm,integer_content=1)
    for key,value in expected.items():require(bc[key]==value,'Final bound '+key)
    support_count=math.comb(degree+V,V)-math.comb(degree-n+V-1,V)
    require(int(bc['monomial_upper_bound'])==support_count,'Support formula')
    for value,key in ((expected['degree_bound'],'degree_strict_power_of_two'),(norm,'coefficient_height_double_power_exponent'),(support_count,'support_strict_power_of_two')):
        require(value<2**bc[key] and bc[key]==value.bit_length(),'Strict power bound '+key)
    return dict(guards=len(source['guard_numerators']),rational_denominators=rational_count,
        support_factors=len(support),point_blocks=p,pole_squares=s,degree_bound=expected['degree_bound'],
        coefficient_l1_log2_bound=norm,canonical_source_sha256=spec['native_source_sha256'])


def uniform_degree_checks():
    records=[]
    for name,params in [('general25',(3,5,101,20483)),('explicit27',(3,5,20483,20485)),('weak13',(3,5,101)),('abc13',(3,5,101))]:
        degrees=[]
        for parameter in params:
            source=make_source(name,parameter)
            spec=compile_specification(source)
            structural_check(source,spec)
            degrees.append(spec['bounds']['degree_bound'])
        require(len(set(degrees))==1,'Parameter-independent degree fixtures')
        records.append(dict(name=name,parameters=list(params),degree_bound=degrees[0],
            scope='Finite implementation checks; uniformity follows from the fixed nonconstant exponents in the proof.'))
    return records


def full_recipe_examples():
    a0,a1=sp.Rational(1),sp.Rational(-7,4)
    A=a0**4+12*a0*a0*a1*a1+4*a1**4-11
    B=4*a0**3*a1+8*a0*a1**3+6
    M1=sp.Matrix([[0,2*A,2*B,0],[1,0,0,A],[0,0,0,-2*B],[0,2,0,0]])
    M2=sp.Matrix([[0,2*B,A,0],[0,0,0,B],[1,0,0,-A],[0,0,-1,0]])
    z=(2*A+B)*M1-2*(A+B)*M2
    T=sp.symbols('T')
    f=z.charpoly(T).as_expr()
    disc=sp.discriminant(f,T);dd=disc*disc
    Z=2+sum(c*c for c in sp.Poly(f,T).all_coeffs()[1:])
    K=(2*Z)**5*(1+dd);C=dd+4*Z*K
    z_roots=sp.polys.polytools.ground_roots(sp.Poly(f,T))
    require(len(z_roots)==2,'Rational point-block characters')
    records=[]
    for c in (4,2,-1):
        q=sp.Matrix([[0,c],[1,0]]);S=4*(1+4*c*c);Q=2*S
        Omega=Q*(C*C*sp.eye(8)+dd*C*sp.kronecker_product(z,sp.eye(2)))+dd*dd*sp.kronecker_product(sp.eye(4),q)
        characteristic=Omega.charpoly(T).as_expr()
        require(sp.gcd(characteristic,sp.diff(characteristic,T))==1,'Full-recipe eigenvalue separation')
        require(characteristic.subs(T,0)!=0,'Full-recipe nonzero eigenvalues')
        factors=sp.factor_list(characteristic,T)[1]
        linear=sum(sp.degree(factor,T)*mult for factor,mult in factors if sp.degree(factor,T)==1)
        require(linear==(4 if c==4 else 0),'Full-recipe rational characters')
        records.append(dict(point_pair=['1','-7/4'],radicand=c,dimension=8,
            rational_character_count=int(linear),irreducible_factor_degrees=[int(sp.degree(g,T)) for g,m in factors]))
    # A guard may vanish on one character but not the others: the new
    # construction then intentionally excludes the entire retained base.
    one_root=next(iter(z_roots));guard=z-one_root*sp.eye(4)
    require(guard.det()==0 and guard!=sp.zeros(4),'Partial-zero guard example')
    require((sp.eye(8)-T*guard.det()*Omega).det()==1,'Partial-zero norm guard exclusion')
    return dict(examples=records,partial_zero_guard_excludes_whole_base=True)


def modular_check(source,p,seed):
    rng=random.Random(seed);Q=QuadraticArithmetic(p)
    require(sp.isprime(p) and sp.legendre_symbol(2,p)==1,'Prime splits 2')
    rt=int(sp.sqrt_mod(2,p));inv2=pow(2,-1,p)
    variables=[rng.randrange(1,p) for _ in source['variables']]
    names={v['name']:v['index'] for v in source['variables']}
    points={}
    for block in (b for b in source['finite_blocks'] if b['kind']=='point_block'):
        name=block['name']
        while True:
            h=(rng.randrange(1,p),rng.randrange(1,p));x=Q.sq(h)
            a,b=Q.sub(Q.sq(x),Q.f(11,-6));aa=(a+rt*b)%p;bb=(a-rt*b)%p
            if aa and bb and sp.legendre_symbol(aa,p)==sp.legendre_symbol(bb,p)==1:break
        jp=int(sp.sqrt_mod(aa,p));jm=int(sp.sqrt_mod(bb,p))
        if rng.randrange(2):jp=-jp%p
        if rng.randrange(2):jm=-jm%p
        j=((jp+jm)*inv2%p,(jp-jm)*pow(2*rt,-1,p)%p)
        variables[names[name+'.a0']],variables[names[name+'.a1']]=h
        variables[names[name+'.U']]=2*j[0]%p;variables[names[name+'.V']]=2*j[1]%p
        variables[names[name+'.W']]=(j[0]**2-2*j[1]**2)%p
        points[name]=(x,Q.mul(h,j))
    values=[]
    for op,*a in source['coefficient_dag']:
        if op=='int':v=a[0]%p
        elif op=='variable':v=variables[a[0]]
        elif op=='parameter':v=a[1]%p
        elif op=='neg':v=-values[a[0]]%p
        elif op=='add':v=sum(values[k] for k in a)%p
        elif op=='mul':v=math.prod(values[k] for k in a)%p
        elif op=='pow':v=pow(values[a[0]],a[1],p)
        else:raise AssertionError(op)
        values.append(v)
    def r(obj):return values[obj['numerator']]*pow(values[obj['denominator']],-1,p)%p
    def field(obj):return tuple(r(c) for c in obj)
    for event in (e for e in source['events'] if e['operation']=='point_block'):
        require(field(event['x'])==points[event['name']][0] and field(event['y'])==points[event['name']][1],'Point event')
    P=(Q.f(F(57,8),F(-7,2)),Q.f(F(-165,8),F(417,32)))
    conditional=source['name'] in ('weak13','abc13')
    X=variables[names['input.X']];lam=variables[names['slope.lambda']]
    if conditional:
        A,H,U=[points[k] for k in ('A','H','UA')]
        V0=Q.difference(H,P);V1=Q.difference(U,A)
        L=Q.div(Q.parameter(U),Q.parameter(H));Lp=Q.conj(Q.div(Q.parameter(V1),Q.parameter(V0)))
        tests=[Q.reciprocal(H),Q.reciprocal(U),Q.conj(Q.reciprocal(V0)),Q.conj(Q.reciprocal(V1)),Q.sub(L,Lp),Q.sub(L,Q.f(X))]
        ev=next(e for e in source['events'] if e['operation']=='conditional_direct_target_tests')
        require([field(v) for v in ev['tests']]==tests,'Conditional tests')
        B=source['family_parameter']['value'];d=source['scale_power'];beta=(X*X+B)%p
        scales=[1,(pow(beta,d,p)+pow(2*A[0][0],d,p))%p]
        scalar=[]
    else:
        H=points['H'];Ui=[points[k] for k in ('UA','US','UT','UZ')];roots=[points[k] for k in ('A','S','T','Z')]
        V=[Q.difference(a,b) for a,b in zip([H]+Ui,[P]+roots)]
        L=[Q.div(Q.parameter(a),Q.parameter(H)) for a in Ui]
        Lp=[Q.conj(Q.div(Q.parameter(a),Q.parameter(V[0]))) for a in V[1:]]
        beta=(216*pow(X,4,p)+450459)%p
        tests=[Q.reciprocal(a) for a in [H]+Ui]+[Q.conj(Q.reciprocal(a)) for a in V]+[Q.sub(a,b) for a,b in zip(L,Lp)]+[Q.sub(L[0],Q.f(beta))]
        u,v,w=L[1:];u2=Q.sub(u,Q.f(2))
        tests+=[Q.sub(Q.add(Q.sq(v),Q.mul(Q.sq(u2),Q.sq(w))),Q.add(Q.mul(Q.mul(u,u2),Q.mul(v,w)),Q.f(1)))]
        SP=Q.difference(points['S'],P)
        scalar=list(Q.reciprocal(H)+Q.reciprocal(SP)+Q.div(Q.parameter(SP),Q.parameter(H)))
        ev=next(e for e in source['events'] if e['operation']=='comparison_and_scalar_tests')
        require([field(a) for a in ev['comparison']]==tests and [r(a) for a in ev['scalar']]==scalar,'General tests')
        raw=math.prod((beta,beta-1,beta-2401,32*beta+343,2*beta-1))%p;L0=source['family_parameter']['value']
        rho=102**2*pow(76249,L0,p)*raw*pow(1+17*(pow(76249,(L0+1)//2,p)+1)*raw,-2,p)%p
        trace=sum(a[0][0] for a in roots)*2%p
        if source['name']=='general25':scales=[1,(1+rho*trace*trace)%p]
        else:
            t0=sum(a[0][0] for a in roots)%p;t1=sum(a[0][1] for a in roots)%p
            scales=[1,pow(1+rho*t0*t0,2,p),pow(1+rho*(t0+t1)**2,2,p)]
        ev=next(e for e in source['events'] if e['operation']=='combined_height_scales')
        require(r(ev['scalar_contact'])==rho,'Scalar coefficient')
        require([r(a) for a in ev['scales']]==scales,'General scales')
    detector_events=[e for e in source['events'] if e['operation'] in ('detector','combined_detector')]
    pole_events=[e for e in source['events'] if e['operation']=='rescaled_zero_pole']
    relations=[b for b in source['finite_blocks'] if b['kind']=='pole']
    for j,(event,pole_event,rel) in enumerate(zip(detector_events,pole_events,relations)):
        t=scales[j]*lam%p;delta=(t-1 if conditional else t+j+1)%p
        if conditional:
            contacts=[F(0),F(-1,2),F(-1,4),F(-2,5),F(-1),F(-1,3)]
            poly=math.prod(t-Q.q(c) for c in contacts)%p;weight=pow(delta,4,p)*pow(poly,-1,p)%p
            W=Q.f(1)
            for test in tests:W=Q.mul(W,Q.add(Q.f(1),Q.scale(Q.sq(test),weight)))
            norm=(W[0]*W[0]-2*W[1]*W[1])%p
            bv=poly*norm*norm*pow(4*pow(delta,8,p)*W[0]*W[0],-1,p)%p
        else:
            base=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
            contacts=[a+shift for shift in (4*j+2,4*j+4) for a in base]
            poly=math.prod(t-Q.q(a) for a in contacts)%p;R=poly*pow(delta,-10,p)%p;w=rho*R%p
            W=Q.f(1)
            for test,order in zip(tests,[1]*11+[3]*3+[1,3]):
                weight=pow(delta,-2,p)*pow(w,1-2*order,p)%p
                W=Q.mul(W,Q.add(Q.f(1),Q.scale(Q.sq(test),weight)))
            for k,test in enumerate(scalar):
                order=1 if k<4 else 3
                E=pow(R,order,p)*(R*test)*pow(1+R*test,-1,p)%p
                W=Q.mul(W,Q.add(Q.f(1),Q.f(E*E*pow(w,1-2*order,p)%p)))
            norm=(W[0]*W[0]-2*W[1]*W[1])%p;bv=w*norm*norm*pow(W[0],-2,p)%p
        require(field(event['product_components'])==W,'Detector product')
        require(r(event['pole_input'])==bv==r(pole_event['input']),'Pole input')
        dc=r(pole_event['square_class']);tm=r(pole_event['square_multiplier'])
        require(bv==dc*tm*tm%p,'Pole square decomposition')
        tau=variables[names[f'detector{j}.conic_parameter']];sv=variables[names[f'detector{j}.s']]
        e=(tau*tau-17*dc)*pow(tau*tau+51*dc,-1,p)%p
        rad=17*dc*(sv*sv-17*e*(17-bv))*(sv*sv+51*e*(17-bv))%p
        require(r(pole_event['e'])==e and r(pole_event['radicand'])==rad==r(rel['original_square_input']),'Rescaled pole formula')
    return dict(prime=p,seed=seed,point_blocks=len(points),tests=len(tests),pole_inputs=len(detector_events))


def small_determinants():
    # Exact rank-two instances of the same separating construction. Distinct
    # rational factors correspond to rational characters; irreducibles do not.
    U=sp.symbols('U');records=[]
    for c in (F(-1),F(2),F(4),F(1,10000),F(0)):
        M=sp.Matrix([[0,sp.Rational(c.numerator,c.denominator)],[1,0]])
        S=1+sum(x*x for x in M);omega=2*S*sp.eye(2)+M
        delta=sp.Rational(c.numerator,c.denominator)
        P=sp.Poly((sp.eye(2)-U*delta*omega).det(),U)
        roots=sp.polys.polytools.ground_roots(P)
        square=c>0 and math.isqrt(c.numerator)**2==c.numerator and math.isqrt(c.denominator)**2==c.denominator
        require(bool(roots)==square,'Rational-character test')
        if c==0:require(P.as_expr()==1,'Nilpotent boundary excluded')
        records.append(dict(radicand=str(c),rational_roots=[str(r) for r in roots],polynomial=str(P.as_expr())))
    # Nonseparating element over Q(sqrt(2)) wrongly gives a rational root.
    require((sp.eye(2)-U*sp.eye(2)).det().subs(U,1)==0,'Negative control setup')
    # Without the scalar guard norm, a nilpotent zero-radicand block is admitted.
    N=sp.Matrix([[0,0],[1,0]])
    require((sp.eye(2)-U*(2*sp.eye(2)+N)).det().subs(U,F(1,2))==0,'Guard omission negative control')
    return dict(examples=records,nonseparating_element_rejected=True,omitted_guard_counterexample=True)


def run(directory):
    report=dict(schema='unit-norm-independent-verification/v28',status='PASS',symbolic=symbolic_identities(),
        determinant_examples=small_determinants(),full_recipe_examples=full_recipe_examples(),
        uniform_degree_fixtures=uniform_degree_checks(),constructions=[],negative_controls=[],scope='Exact symbolic identities and syntactic factor/degree certificates; finite-field source evaluations are bounded tests. The full-unit completeness theorem and infinite arithmetic premises are NOT certified by these computations.')
    for name in ('general25','explicit27','weak13','abc13'):
        source=make_source(name);spec=json.loads((directory/(name+'.json')).read_text())
        record=dict(name=name,**structural_check(source,spec));samples=[];skipped=0
        for p in (1009,1033,1201):
            for seed in range(16):
                try:samples.append(modular_check(source,p,2800+seed))
                except ValueError:skipped+=1
        require(len(samples)>=24,'Too few nonsingular source samples')
        record.update(finite_field_reconstructions=samples,singular_samples_skipped=skipped)
        report['constructions'].append(record)
        # Bound and factor corruption controls must fail without regeneration.
        corrupted=json.loads(json.dumps(spec));corrupted['bounds']['degree_bound']-=1
        try:structural_check(source,corrupted)
        except AssertionError:report['negative_controls'].append(name+': lowered degree rejected')
        else:raise AssertionError('Lowered-degree mutation was accepted')
        corrupted=json.loads(json.dumps(spec));corrupted['quadratic_reductions'][0]['sign']*=-1
        try:structural_check(source,corrupted)
        except AssertionError:report['negative_controls'].append(name+': reversed radicand sign rejected')
        else:raise AssertionError('Wrong-sign mutation was accepted')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory',type=Path,default=HERE/'specifications')
    ap.add_argument('--output',type=Path,default=HERE/'verification.json')
    args=ap.parse_args();report=run(args.directory)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],constructions=len(report['constructions']),
        finite_field_reconstructions=sum(len(r['finite_field_reconstructions']) for r in report['constructions']),
        corruption_tests=len(report['negative_controls'])),indent=2))
