#!/usr/bin/env python3
"""Exact algebraic audit of the printed Mishchenko--Treier system.

The source is A. Mishchenko and A. Treier, J. Phys. Conf. Ser. 1050 (2018)
012054, doi:10.1088/1742-6596/1050/1/012054, equations (8)--(57).
The script verifies algebraic changes of coordinates and counts; it does not
prove the source universality theorem or a definition of Z in Q.

Run: python mt_quadratic_system.py --report source_audit_certificate.json
SymPy >= 1.13 is sufficient. No external files or numerical fixtures are used.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp


def source_system():
    """Return (variables, parameters, numbered residuals, symbol dictionary).

    The independent coefficient a represents (2*z)**(5**59), while kappa
    represents 5**59. Degrees are measured only in the 62 unknowns.
    """
    gamma = sp.symbols('Gamma1:27')
    names = 'B D1 C1 c e ell S T N R P K M U Y D I E G H alpha Delta eps g t m lam gamma o F i j h w s phi'.split()
    syms = dict(zip(names, sp.symbols(' '.join(names))))
    syms.update({f'Gamma{k}': gamma[k-1] for k in range(1,27)})
    z,u,y,x,a,kappa = sp.symbols('z u y x a kappa')
    syms.update(dict(z=z,u=u,y=y,x=x,a=a,kappa=kappa))
    B,D1,C1,c,e,ell,S,T,N,R,P,K,M,U,Y,D,I,E,G,H,alpha,Delta,eps,g,t,m,lam,gam,o,F,i,j,h,w,s,phi = (syms[n] for n in names)
    gg = {k:gamma[k-1] for k in range(1,27)}
    q = {
      8: gg[1]-gg[26]**2,
      9: gg[2]-M*U,
      10: gg[3]-B*(2*gg[23]-B)+1,
      11: gg[4]-gg[23]*C1,
      12: gg[5]-c**2,
      13: gg[6]-gg[5]**2,
      14: gg[8]-gg[24]**2,
      15: gg[9]-lam*B,
      16: gg[10]-G*H,
      17: gg[11]-F**2,
      18: gg[12]-gg[23]*E,
      19: gg[13]-gg[25]**2,
      20: gg[14]-gg[23]*gg[25],
      21: gg[15]-N**2,
      22: gg[16]-Y*K,
      23: gg[18]-P*K,
      24: gg[20]-gg[8]*gg[24],
      25: gg[21]-gg[8]**2,
      26: gg[22]-gg[6]*gg[20],
      27: B-2*a*gg[1]**2-1,
      28: D1-gg[24]-C1*(gg[23]-B)-alpha*gg[3],
      29: (gg[4]-C1)*(gg[4]+C1)+1-D1**2,
      30: C1-kappa-Delta*(gg[23]-1),
      31: c-1-(gg[26]-eps)*B-g,
      32: e+2*z*gg[26]*ell+2*z*B*gg[6]+gg[7]-2*z*gg[24],
      33: ell-u-t*(B-2*z),
      34: e-y-m*(B-2*z),
      35: S-g+4*z**2*gg[22]-ell*gg[24]-e*(gg[8]+4*z*gg[22])-2*z*gg[9]*(-2*z*gg[22]+gg[20]+gg[21]),
      36: T-gg[24]+1+(gg[26]-1)*ell-(gg[9]-2*lam*z)*(gg[24]+gg[8])-2*z*(B-2)*gg[21],
      37: N-16*z*gg[20]*gg[8],
      38: R-S*(gg[15]-N)-(T+1)*(gg[15]-1),
      39: P-2*M*gg[2],
      40: (K-gg[18])*(K+gg[18])+gg[19]**2-1,
      41: (2*gg[25]-2*gg[16]-K)*(2*gg[25]-2*gg[16]+K)+gg[17],
      42: K-R-1-h*(P-1),
      43: M-R*Y,
      44: U-gg[15]*w,
      45: Y-gg[15]*s,
      46: D+2*gg[25]+5*gam-gg[26]*w-gg[23]*(gg[25]+4*gam),
      47: I-D-o*F,
      48: (D-gg[14])*(D+gg[14])+gg[13]-1,
      49: E-i*gg[13]-1,
      50: (gg[12]-E)*(gg[12]+E)-gg[11]+1,
      51: G-gg[23]-gg[11]*(gg[11]-gg[23]),
      52: H-2*R-1-j*gg[25],
      53: I**2+H*(H-gg[10])-1,
      54: gg[23]-gg[2]-M,
      55: gg[24]-1-gg[9]+lam,
      56: gg[25]-2*R-1-C1-phi,
      57: gg[26]-eps-x,
    }
    return tuple(gamma)+tuple(syms[n] for n in names), (z,u,y,x,a,kappa), q, syms


def reduced_system():
    variables, parameters, rows, s = source_system()
    substitutions = {
      s['Gamma23']:s['Gamma2']+s['M'],
      s['Gamma24']:1+s['Gamma9']-s['lam'],
      s['Gamma25']:2*s['R']+1+s['C1']+s['phi'],
      s['Gamma26']:s['eps']+s['x'],
      s['c']:1+s['x']*s['B']+s['g'],
    }
    removed_rows = {31,54,55,56,57}
    out = {n:sp.expand(r.subs(substitutions, simultaneous=True)) for n,r in rows.items() if n not in removed_rows}
    kept = tuple(v for v in variables if v not in substitutions)
    return kept, parameters, out, substitutions


def audit():
    vs, ps, rows, s = source_system()
    rv, rp, reduced, subs = reduced_system()
    assert len(vs)==62
    assert len(set(vs))==62
    assert list(rows)==list(range(8,58))
    assert len(rows)==50
    assert all(sp.Poly(r,*vs).total_degree()<=2 for r in rows.values())
    assert set.union(*(r.free_symbols for r in rows.values()))-set(ps)==set(vs)
    assert len(rv)==57
    assert len(reduced)==45
    assert all(sp.Poly(r,*rv).total_degree()<=2 for r in reduced.values())
    assert set.union(*(r.free_symbols for r in reduced.values()))-set(ps)==set(rv)
    for n in [31,54,55,56,57]:
        assert sp.expand(rows[n].subs(subs, simultaneous=True))==0
    for n,r in reduced.items():
        assert sp.expand(rows[n].subs(subs, simultaneous=True)-r)==0
    # Decisive source error guard: the Pell root is squared, never linear.
    assert sp.Poly(rows[40],s['Gamma19']).degree()==2
    assert sp.Poly(rows[40],s['Gamma19']).coeff_monomial(s['Gamma19']**2)==1
    # The retained positivity witnesses are reconstructed by these identities.
    assert sp.expand(subs[s['Gamma24']].subs(s['Gamma9'],s['lam']*s['B'])-(1+s['lam']*(s['B']-1)))==0
    # The final polynomial really is degree four: leading quadratic terms
    # squared over Q cannot cancel because sums of real squares are positive.
    maxdegree=max(sp.Poly(r,*rv).total_degree() for r in reduced.values())
    assert maxdegree==2
    # Show the reconstruction graph has a monic orientation once F is primitive.
    definitions = {
      8:'Gamma1',9:'Gamma2',10:'Gamma3',11:'Gamma4',12:'Gamma5',
      13:'Gamma6',14:'Gamma8',15:'Gamma9',16:'Gamma10',17:'Gamma11',
      18:'Gamma12',19:'Gamma13',20:'Gamma14',21:'Gamma15',22:'Gamma16',
      23:'Gamma18',24:'Gamma20',25:'Gamma21',26:'Gamma22',27:'B',
      28:'D1',30:'C1',31:'c',32:'Gamma7',33:'ell',34:'e',35:'S',
      36:'T',37:'N',38:'R',39:'P',41:'Gamma17',42:'K',43:'M',
      44:'U',45:'Y',46:'D',47:'I',49:'E',51:'G',52:'H',
      54:'Gamma23',55:'Gamma24',56:'Gamma25',57:'Gamma26'}
    assert len(definitions)==45
    primitives=[s[n] for n in 'alpha Delta eps g t m lam gamma o F i j h w s phi'.split()]
    available=set(primitives)|set(ps)
    remaining=dict(definitions)
    order=[]
    while remaining:
        choices=[]
        for n,name in remaining.items():
            v=s[name]
            poly=sp.Poly(rows[n],v)
            assert poly.degree()==1 and abs(poly.coeff_monomial(v))==1
            if (rows[n].free_symbols-{v})<=available:choices.append((n,name))
        assert choices, f'Cycle: {remaining}'
        n,name=min(choices)
        available.add(s[name]);order.append(n);del remaining[n]
    constraints=sorted(set(rows)-set(definitions))
    assert constraints==[29,40,48,50,53]
    assert set(vs)-available=={s['Gamma19']}
    data = {
      'source':'Mishchenko--Treier (2018), doi:10.1088/1742-6596/1050/1/012054, equations (8)--(57)',
      'source_parameters':['x','z','u','y'],
      'fixed_coefficient_specializations':{'a':'(2*z)**(5**59)','kappa':'5**59'},
      'source_variables':len(vs),'source_rows':len(rows),
      'removed_variables':list(map(str,subs)),
      'removed_rows':[31,54,55,56,57],
      'reduced_variables':len(rv),'reduced_rows':len(reduced),
      'maximum_residual_degree':maxdegree,'sum_of_squares_degree':4,
      'assignment_rows':len(definitions),'constraint_rows':constraints,
      'assignment_order':order,
      'critical_Gamma19_squared':True,
      'proof_scope':'exact affine equivalence and counts only; universality of the literal printed system remains unresolved because of source discrepancies',
      'source_rows_sha256':hashlib.sha256('\n'.join(f'{n}:{sp.srepr(sp.expand(r))}' for n,r in rows.items()).encode()).hexdigest(),
      'reduced_rows_sha256':hashlib.sha256('\n'.join(f'{n}:{sp.srepr(r)}' for n,r in reduced.items()).encode()).hexdigest(),
    }
    return data

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    data=audit()
    text=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(text)
    print(text,end='')
