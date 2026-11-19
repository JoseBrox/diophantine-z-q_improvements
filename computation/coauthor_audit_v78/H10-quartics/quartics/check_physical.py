"""Check a shared-product coefficient family from the pinned upstream Laurent table.
Example: python check_gated.py path/to/primitive/laurent-source.json path/to/gated175
No solver or third-party dependencies are required.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd, comb
from pathlib import Path
import json


# A term records the exponents of C, c, and the remaining source coordinate tuple.
def pm(a=1, k=0, e=0, m=()):
    return {(k, e, tuple(sorted(m))): Fraction(a)} if a else {}


def plus(*args):
    out = defaultdict(Fraction)
    for arg in args:
        for m, a in arg.items():
            out[m] += a
    return {m: a for m, a in out.items() if a}


def times(*args):
    out = pm()
    for arg in args:
        out = plus(*(pm(a*b,k+l,e+f,m+n) for (k,e,m),a in out.items() for (l,f,n),b in arg.items()))
    return out


def neg(p):
    return {m:-a for m,a in p.items()}


def diff(a,b):
    return plus(a,neg(b))


def square(p):
    return times(p,p)


one=pm()
c=pm(e=1)
cinv=pm(e=-1)
C=pm(k=1)


def X(i):
    return pm(m=(i,))


def expected(archive, variant, assignment=None):
    src=json.loads(archive.read_text())
    expected={}
    for r in src['rows']:
        n=r['name']
        if n.startswith(('additive.detector','balanced.detector','detector0.normOver','detector1.normOver','new.det1.factor','amplified.det1.product')):
            continue
        parts=[]
        for t in r['terms']:
            k=t['parameterPower']; e=t['unitPower'][0]
            coordinate=one
            for i in t['monomial']:
                if n.startswith('amplified.det0.product4.') and i in (79,80):
                    # F_i has multiplier C^[1,1,1,0,-1]_i*c. Product stages have
                    # multipliers c/C, c, C*c, C*c. Hence W=C*c*x79.
                    coordinate=times(coordinate,pm(k=-1,e=-1),X(302+i-79))
                else:
                    coordinate=times(coordinate,X(i))
            parts.append(times(pm(int(t['coefficient']),k,e),coordinate))
        expected[n]=plus(*parts)
    if variant in (172,173,187,188):
        # One archived slot has physical q*A4², and one q²*A2². We keep
        # the same tests and interchange the two exponents so F4 squares natively.
        F4=(X(229),X(230))
        A4_sq=(plus(square(F4[0]),times(pm(2),square(F4[1]))),times(pm(2),*F4))
        A2_sq=tuple(times(pm(1+j),C,cinv,X(54+j)) for j in (0,1))
        for j in (0,1):
            n=f'new.det0.factor4.{j}'
            expected[n]=plus(expected[n],neg(times(c,X(237+j))),neg(times(square(c),A2_sq[j])),times(c,A2_sq[j]),times(square(c),A4_sq[j]))
        for n in list(expected):
            if n.startswith('new.square.237.'):
                del expected[n]
    if variant in (180,181,183,187,188,190):
        # Reuse the first pole tester with independent variables. Its p,q witnesses
        # share only the same scalar normalizer x112, exactly as in upstream.
        third={3:503,4:504,5:505,6:506,81:581,82:582,83:583,84:584,85:585}
        for n,p in list(expected.items()):
            if n.startswith('detector0.'):
                expected[n.replace('detector0','detector2')]={(k,e,tuple(sorted(third.get(i,i) for i in m))):a for (k,e,m),a in p.items()}
        # Physical scalar-point abscissa is (x192 + sqrt(2)*x193)/c.
        # Each other difference has abscissa h*(h+s+t), including finite two-torsion.
        S0=times(cinv,X(192));S1=times(cinv,X(193))
        for i in (201,213,225):
            hr,hi=X(i+8),X(i+9)
            pr,pi=plus(hr,X(i),X(i+2)),plus(hi,X(i+1),X(i+3))
            S0=plus(S0,times(hr,pr),times(pm(2),hi,pi))
            S1=plus(S1,times(hi,pr),times(hr,pi))
        T0,T1,T2=[times(cinv,X(i)) for i in (2,86,502)]
        expected['new.aggregate']=plus(times(pm(2),diff(T0,T1)),pm(26),S0)
        expected['new.aggregate_shift']=plus(times(pm(2),diff(plus(T0,T2),times(pm(2),T1))),pm(-8),S1)
    q0=X(300)
    W0,W1=X(302),X(303)
    contacts=[(2,74,75,76,82,81),(86,87,88,89,96,95)]
    raw_weights=[q0,diff(c,q0)]
    if variant in (180,181,183,187,188,190):
        contacts.append((502,574,575,576,582,581))
        raw_weights=[q0,X(301),diff(c,plus(q0,X(301)))]
    for j,(t,r,s,v,b,nr) in enumerate(contacts):
        q=raw_weights[j]
        other=diff(c,q)
        inv=X(310+j)
        tau=times(c,X(nr))
        # t,r,s,v here are physical values after the common c dehomogenization.
        T,R,S,V=(times(cinv,X(i)) for i in (t,r,s,v))
        if j==0: V=times(C,V)
        one_plus_inv=plus(one,times(cinv,inv))
        n=f'additive.detector{j}.'
        expected[n+'contactSquare']=diff(square(diff(T,one)),R)
        expected[n+'contactFourthPower']=diff(square(R),S)
        expected[n+'contactCombination']=plus(times(pm(3813373161796),R,S),times(one_plus_inv,plus(times(pm(122376041313918),R),times(pm(-35893742479489),S))),neg(V))
        expected[n+'contactRelation']=plus(times(S,V),times(one_plus_inv,plus(pm(-39896049934224),times(pm(141822723674536),R),times(pm(-192222345736537),S))))
        if variant in (180,181,183,187,188,190):
            # Recompute L and L*e_i from the five paired contact roots, independently
            # of the supplied integer constants. P_5(r) = product(r - (22*theta-3)^2).
            theta=[Fraction(0),Fraction(-1,2),Fraction(-1),Fraction(1,2399),Fraction(-32,407)]
            es=[Fraction(1)]
            for z in theta:
                root=(22*z-3)**2
                es=[a+b for a,b in zip(es+[Fraction(0)],[Fraction(0)]+[root*t for t in es])]
            from math import lcm
            L=lcm(*(t.denominator for t in es))
            V=times(pm(Fraction(1,L)),V)
            expected[n+'contactSquare']=diff(square(diff(times(pm(22),T),pm(3))),R)
            expected[n+'contactCombination']=plus(times(R,S),times(one_plus_inv,plus(times(pm(-es[1]),S),times(pm(es[2]),R))),neg(V))
            expected[n+'contactRelation']=diff(times(S,V),times(one_plus_inv,plus(times(pm(es[3]),S),times(pm(-es[4]),R),pm(es[5]))))
        expected[f'balanced.detector{j}.poleInput.definition']=diff(times(pm(167281),c,X(b),plus(one,q)),times(pm(166464),square(tau)))
        expected[f'shared.inverse{j}']=diff(c,times(q,inv))
        if variant==177:
            H0,H1=X(304),X(305)
            g=X(306+j)
            expected[f'shared.gate{j}']=diff(times(plus(one,q),diff(g,H0)),plus(one,square(other)))
            expected[f'shared.norm{j}']=plus(times(pm(4),g,tau),neg(square(g)),times(pm(2),square(H1)))
            expected['shared.square.real']=plus(H0,neg(square(W0)),times(pm(-2),square(W1)))
            expected['shared.square.imag']=diff(H1,times(pm(2),W0,W1))
        else:
            Wnorm=diff(square(W0),times(pm(2),square(W1)))
            Enorm=diff(square(diff(W0,one)),times(pm(2),square(W1)))
            D,E=X(305),X(306)
            if variant==176:
                expected['shared.normW']=diff(X(304),Wnorm)
                expected['shared.norm_error']=plus(times(diff(one,D),X(304)),times(pm(-2),W0),one)
            else:
                expected['shared.norm_error']=diff(times(pm(2),W0,D),Enorm)
            if variant in (165,166,168,172,180,181,183,187):
                # Multiply 2*tau=1+D²+(c-q)²/q by q, then remove
                # q*(c/q)-c to express this in the independent inverse variable.
                expected[f'shared.gate{j}']=diff(times(pm(2),tau),plus(one,square(D),times(c,inv),times(pm(-2),c),q))
            else:
                expected['shared.norm_error_square']=diff(E,square(D))
                expected[f'shared.gate{j}']=diff(times(pm(2),tau),plus(one,square(other),times(q,E)))
    if variant in (165,166,168,180,181,183):
        assert assignment and not assignment['kept']
        G=assignment['groups'];hy=assignment['hyperbolic']
        partial=assignment.get('partial')
        four=partial is not None
        assert len(G)==(4 if four else 5) and all(len(f)==3 for f in G)
        if four:
            assert sorted(list(hy)+[partial])==list(range(4))
            for n in list(expected):
                if n.startswith(('new.det0.factor4.','amplified.det0.product4.')):
                    del expected[n]
                elif n.startswith('amplified.det0.product3.'):
                    # Product of the first four F's is C^3*c times the previous
                    # stage stored in x132,133. That product itself is now stored.
                    expected[n]=plus(*(times(pm(v,k,e),*(times(pm(k=-3,e=-1),X(302+i-132)) if i in (132,133) else X(i) for i in m)) for (k,e,m),v in expected[n].items()))
        native={'C1':(60,1,-1,2),'C2':(66,1,-1,2),'C3':(68,1,-1,2),'C4':(70,1,-1,2),'H':(72,0,-1,4),'A1':(205,0,0,1),'B1':(207,0,0,-1),'A3':(217,0,0,1),'B3':(219,0,0,-1),'A4':(229,0,0,1),'B4':(231,0,0,-1)}
        linear={'DH':(64,0,-1,2),'B0':(19,0,-1,-2),'A2':(54,1,-1,2),'B2':(23,0,-1,-2)}
        high=assignment.get('high')
        if high:
            assert (set(high)==set(linear) and len(high)==4) if four else high in linear
            native['N']=(62,0,-1,2)
        assert sorted(sum(G,[])+(high if four else ([high] if high else [])))==sorted(list(native)+list(linear))
        def pwr2(x,y):
            return plus(square(x),times(pm(2),square(y))),times(pm(2),x,y)
        sub={}
        for j in hy:
            i,k,e,h=native[G[j][0]]
            l,t,u,g=native[G[j][2]]
            for b in (0,1):
                # inverse of (X,Y)=(A+cB,A-cB) in the native coordinates
                sub[i+b]=times(pm(Fraction(1,2*(h if b else 1)),-k,-e),plus(X(i+b),X(l+b)))
                sub[l+b]=times(pm(Fraction(1,2*(g if b else 1)),-t,-u-1),diff(X(i+b),X(l+b)))
        for n in list(expected):
            if n.startswith(('new.square.237.','new.square.239.','amplified.C1.power4.')) or (high and n.startswith('input.cleared.fourth.')):
                del expected[n]
        for j,group in enumerate(G):
            for b in (0,1):
                # Factor output C^alpha*c*f, special term c^4*(N^4)^2.
                eq=plus(one if b==0 else {},neg(times(pm(k=[1,1,1,0,-1][j],e=1),X(118+2*j+b))))
                if four or j==4:
                    if high:
                        i,k,e,h=linear[high[j] if four else high]
                        eq=plus(eq,times(pm(k=2*k,e=4+2*e),pwr2(X(i),times(pm(h),X(i+1)))[b]))
                    else:
                        eq=plus(eq,times(pm(e=4),pwr2(times(cinv,X(116)),times(cinv,X(117)))[b]))
                for power,label in enumerate(group,1):
                    if j==partial and power in (1,3):
                        if power==3:continue
                        # In the partial pair only X=A+cB is added. Check first
                        # its field definition, then c*X*(A-cB)=c*A²-c³*B².
                        def native_field(s):
                            i,k,e,h=native[s]
                            return times(pm(k=k,e=e),X(i)),times(pm(h,k,e),X(i+1))
                        a0,a1=native_field(group[0]);b0,b1=native_field(group[2])
                        U0,U1=X(610),X(611)
                        wantU=(plus(a0,times(c,b0)),plus(a1,times(c,b1)))
                        expected[f'shared.partial_pair.{b}']=diff((U0,U1)[b],wantU[b])
                        V0,V1=diff(a0,times(c,b0)),diff(a1,times(c,b1))
                        def XY(u0,u1,v0,v1):
                            return plus(times(u0,v0),times(pm(2),u1,v1)),plus(times(u0,v1),times(u1,v0))
                        exact=diff(pwr2(a0,a1)[b],times(square(c),pwr2(b0,b1)[b]))
                        assert XY(*wantU,V0,V1)[b]==exact
                        eq=plus(eq,times(c,XY(U0,U1,V0,V1)[b]))
                        continue
                    if label in linear:
                        i,k,e,h=linear[label];term=times(pm(h if b else 1,k,e),X(i+b))
                    else:
                        i,k,e,h=native[label]
                        term=times(pm(k=2*k,e=2*e),pwr2(X(i),times(pm(h),X(i+1)))[b])
                    if j in hy and power==3:
                        term=neg(term)
                    eq=plus(eq,times(pm(e=power),term))
                expected[f'new.det0.factor{j}.{b}']=eq
        for n,p in list(expected.items()):
            expected[n]=plus(*(times(pm(v,k,e),*(sub.get(i,X(i)) for i in m)) for (k,e,m),v in p.items()))
    return expected


def normalized(p):
    lo_C=min(k for k,e,m in p);lo_c=min(e for k,e,m in p)
    p={(k-lo_C,e-lo_c,m):v for (k,e,m),v in p.items()}
    scale=p[min(p)]
    return {m:v/scale for m,v in p.items()}


def inspect(source,package):
    q=json.loads((package/'quadrics.json').read_text())
    variant=q['variables']
    assert variant in (165,166,168,172,173,175,176,177,180,181,183,187,188,190)
    weights=json.loads((package/'weights.json').read_text())
    w={int(i):e for i,e in weights['weights'].items()}
    old={z['id']:z['source_id'] for z in q['coordinates']}
    assert set(old)==set(range(1,variant+1)) and len(set(old.values()))==variant
    assert old[q['inputCoordinate']]==1 and w[1]==0
    eqs=expected(source,variant,json.loads((package/'assignment.json').read_text()) if variant in (165,166,168,180,181,183) else None)
    seen=set(); expanded=defaultdict(int)
    for row in q['residuals']:
        n=row['name'];assert n not in seen;seen.add(n)
        terms=row['terms']
        assert all(len(t['monomial'])<=2 for t in terms)
        for a,b in combinations_with_replacement(terms,2):
            k=a['parameterPower']+b['parameterPower'];m=tuple(sorted(a['monomial']+b['monomial']))
            expanded[k,m]+=int(a['coefficient'])*int(b['coefficient'])*(1 if a is b else 2)
        if n=='shared.c_inverse_square':
            assert variant in (165,180)
            assert {(t['parameterPower'],tuple(old[i] for i in t['monomial']),int(t['coefficient'])) for t in terms}=={(0,(402,),1),(0,(401,401),-1)}
            continue
        if n=='shared.c_unit':
            assert {(t['parameterPower'],tuple(old[i] for i in t['monomial']),int(t['coefficient'])) for t in terms}=={(0,(),-1),(0,(400,401),1)}
            continue
        back=[]
        for t in terms:
            k=t['parameterPower'];mon=[old[i] for i in t['monomial']]
            e=mon.count(400)-mon.count(401)-2*mon.count(402)-sum(w.get(i,0) for i in mon)
            back.append(pm(int(t['coefficient']),k,e,[i for i in mon if i not in (400,401,402)]))
        if normalized(plus(*back)) != normalized(eqs[n]):
            a,b=normalized(plus(*back)),normalized(eqs[n])
            print(n,"actual",set(a.items())-set(b.items()),"expected",set(b.items())-set(a.items()))
            raise AssertionError(n)
    assert seen==set(eqs)|({'shared.c_unit','shared.c_inverse_square'} if variant in (165,180) else {'shared.c_unit'})
    expanded={m:v for m,v in expanded.items() if v}
    file=json.loads((package/'polynomial.json').read_text())
    assert file['variables']==variant and len(file['terms'])==len(expanded)
    assert expanded=={(z['parameterPower'],tuple(z['monomial'])):int(z['coefficient']) for z in file['terms']}
    degree=max(k for k,m in expanded)
    coeffs=defaultdict(lambda:[0]*(degree+1))
    for (k,m),v in expanded.items():coeffs[m][k]=v
    assert coeffs[1,1,1,1]==[1]+[0]*degree
    assert {i for m in coeffs for i in m}==set(old)
    # Every coefficient retains its sign for C >=149, certified by C=149+z.
    for p in coeffs.values():
        shifted=[sum(comb(k,j)*149**(k-j)*p[k] for k in range(j,degree+1)) for j in range(degree+1)]
        assert shifted[0] and (min(shifted)>=0 or max(shifted)<=0)
    return dict(variables=variant,degree=max(map(len,coeffs)),quadratic_rows=len(seen),coordinate_monomials=len(coeffs),separated_terms=len(expanded),parameter_degree=degree,constant_input_fourth_power=1,source_sha256=sha256(source.read_bytes()).hexdigest())


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('package',type=Path)
    args=parser.parse_args()
    print(json.dumps(inspect(args.source,args.package),indent=2))
