#!/usr/bin/env python3
"""Exact implementation of the one-coordinate finite-algebra encoder.

The input matrices are multiplication by g,g*theta_1,...,g*theta_m.
`specification` returns finite symbolic data; `factor` builds any factor
of the final polynomial, and `polynomial` builds their unexpanded product.
Large project algebras are specified by the TeX and source circuits, not
expanded by this small illustrative verification program.
"""
from __future__ import annotations
import json
import math
import sympy as sp


def specification(matrices):
    matrices = tuple(sp.Matrix(a) for a in matrices)
    assert matrices and matrices[0].rows == matrices[0].cols
    n = matrices[0].rows
    assert n >= 1 and all(a.shape == (n,n) for a in matrices)
    assert all(a*b == b*a for a in matrices for b in matrices)
    ell = len(matrices); N = n+1; J = ell*N*N
    Z = sp.Dummy('spectral')
    chi = sp.Poly(1,Z)
    for a in matrices:
        augmented = sp.diag(a,sp.zeros(1))
        difference = sp.kronecker_product(augmented,sp.eye(N))-sp.kronecker_product(sp.eye(N),augmented)
        chi *= sp.Poly.from_list(difference.charpoly().all_coeffs(),gens=Z)
    assert chi.degree()==J and chi.LC()==1
    coefficients = tuple(chi.all_coeffs())
    R = sp.expand(2+N+sum(v*v for a in matrices for v in a)+sum(c*c for c in coefficients[1:]))
    B0 = N*R
    K = R*(2*B0)**(J-1)
    return {'matrices':matrices,'n':n,'ell':ell,'J':J,'coefficients':coefficients,
            'R':R,'B0':B0,'K':K}


def element_matrix(spec,s):
    assert 0 <= s <= spec['J']
    D = spec['coefficients'][s]**2
    if D == 0:
        return sp.zeros(spec['n'])
    C = D+(4*spec['ell']*spec['B0']+2)*spec['K']
    out = sp.zeros(spec['n'])
    for i,a in enumerate(spec['matrices']):
        out += D*C**(i+1)*D**(spec['ell']-1-i)*a
    return out


def determinant(spec,s,U):
    matrix = element_matrix(spec,s)
    return sp.Poly((sp.eye(spec['n'])-U*matrix).det(method='domain-ge'),U)


def factor(spec,s,U):
    H = determinant(spec,s,U).as_expr()
    return H*H+sum(a*a for a in spec['coefficients'][s+1:])


def polynomial(spec,U):
    """A factored SymPy expression specifying the full polynomial exactly."""
    return sp.Mul(*(factor(spec,s,U) for s in range(spec['J']+1)),evaluate=False)


def degree_bound(n,ell,d):
    J=ell*(n+1)**2
    return 2*n*(J+1)*(1+d*(1+2*J*(1+ell*(J+1))))


def constant_stratum(spec):
    assert all(not a.free_symbols for a in spec['coefficients'])
    s=max(i for i,a in enumerate(spec['coefficients']) if a!=0)
    # Wrong lower strata have a nonzero rational-square tail; wrong higher
    # strata have D=0 and determinant exactly one. Only this H can vanish.
    for j in range(spec['J']+1):
        if j<s: assert sum(a*a for a in spec['coefficients'][j+1:])>0
        elif j>s: assert element_matrix(spec,j)==sp.zeros(spec['n'])
    return s


def verify_examples():
    U=sp.Symbol('U'); examples=[]
    # A quadratic field without rational characters.
    t=sp.Matrix([[0,2],[1,0]])
    spec=specification([sp.eye(2),t]);s=constant_stratum(spec)
    H=determinant(spec,s,U)
    disc=int(sp.discriminant(H.as_expr(),U))
    assert H.degree()==2 and disc>0 and math.isqrt(disc)**2!=disc
    examples.append({'algebra':'Q[t]/(t^2-2)','guard':'1','rational_character':False,
                     'last_nonzero_coefficient':s,'selected_determinant_degree':H.degree(),
                     'check':'positive nonsquare quadratic discriminant'})
    # A nonmonogenic algebra with two independent nilpotent generators.
    e=sp.zeros(4);e[1,0]=1;e[3,2]=1
    f=sp.zeros(4);f[2,0]=1;f[3,1]=1
    spec=specification([sp.eye(4),e,f]);s=constant_stratum(spec)
    beta=element_matrix(spec,s);lam=beta[0,0]
    H=determinant(spec,s,U)
    assert lam!=0 and H==sp.Poly((1-U*lam)**4,U) and H.set_domain(sp.QQ).eval(1/lam)==0
    examples.append({'algebra':'Q[e,f]/(e^2,f^2)','guard':'1','rational_character':True,
                     'nonreduced':True,'nonmonogenic':True,
                     'last_nonzero_coefficient':s,'selected_determinant_degree':H.degree(),
                     'check':'exact fourth power and explicit rational root'})
    # Every character is excluded by a nilpotent guard.
    t=sp.Matrix([[0,0],[1,0]])
    spec=specification([t,t*t]);s=constant_stratum(spec)
    H=determinant(spec,s,U)
    assert s==0 and H.as_expr()==1
    examples.append({'algebra':'Q[t]/(t^2)','guard':'t','rational_character_with_nonzero_guard':False,
                     'last_nonzero_coefficient':s,'selected_determinant':'1'})
    # A denominator depending on a preceding root vanishes on excluded
    # characters but not on the permitted ones: t^2=1, y^2=2/(t+1).
    # With v=(t+1)y, the monic tower is t^2=1, v^2=2(t+1).
    t=sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
    v=sp.Matrix([[0,0,2,2],[0,0,2,2],[1,0,0,0],[0,1,0,0]])
    assert t*t==sp.eye(4) and v*v==2*(t+sp.eye(4)) and t*v==v*t
    g=t+sp.eye(4)
    spec=specification([g,g*t,g*v]);s=constant_stratum(spec)
    beta=element_matrix(spec,s);H=determinant(spec,s,U)
    values=[]
    for sign in [-1,1]:
        character=sp.Matrix([[1,1,2*sign,2*sign]])
        lam=(character*beta[:,0])[0]
        assert lam!=0 and H.set_domain(sp.QQ).eval(1/lam)==0
        values.append(lam)
    assert values[0]!=values[1]
    assert H==sp.Poly((1-U*values[0])*(1-U*values[1]),U)
    examples.append({'algebra':'Q[t,v]/(t^2-1,v^2-2(t+1))','guard':'t+1',
                     'denominator_vanishes_on_excluded_characters':True,
                     'permitted_rational_characters':2,'selected_determinant_degree':H.degree(),
                     'check':'two distinct explicit rational roots; inactive nilpotent factor contributes one'})
    return {'status':'PASS','examples':examples,
            'scope':'Exact finite examples covering nonrational, nonmonogenic, zero-guard, and character-dependent denominator cases; the general theorem is proved in TeX.'}

if __name__=='__main__':
    print(json.dumps(verify_examples(),indent=2))
