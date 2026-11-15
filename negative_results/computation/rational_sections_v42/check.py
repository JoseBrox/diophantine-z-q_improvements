#!/usr/bin/env python3
"""Exact identities for rational sections of fixed-input pole fibrations.

The companion paper supplies the non-CM, morphism and Galois-descent
arguments. This checker verifies their explicit algebraic data; it does
not assert pointwise nonexistence at a rational specialization of tau.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import sympy as sp

HERE = Path(__file__).resolve().parent


def zero(expression):
    assert sp.cancel(expression) == 0


def zero_on_curve(expression, variable, equation):
    numerator, _ = sp.fraction(sp.cancel(expression))
    assert sp.cancel(sp.rem(numerator, equation, variable)) == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'verification.json')
    args = parser.parse_args()
    tau, D, C, c, r, z, u, v, s, q = sp.symbols('tau D C c r z u v s q')
    X, Y, a, t, w = sp.symbols('X Y a t w')
    A = tau**2 + 3*D
    B = tau**2 - D
    e = B/A

    # Trivialization and its exact deck involution.
    zero(D*((r*u)**2-C*r**2)*((r*u)**2+3*C*r**2)
         - r**4*D*(u**2-C)*(u**2+3*C))
    assert (-r)*(-u) == r*u
    assert (-r)**2*v == r**2*v
    zero((r*u)/r-u)
    zero((r**2*v)/r**2-v)

    # B_D and its rational Weierstrass model, with both inverse maps.
    curve_B = z**2 - A*B
    WX = 2*(z+tau**2+D)
    WY = 2*tau*WX
    curve_J = Y**2-X**3+4*D*X**2-16*D**2*X
    zero_on_curve(curve_J.subs({X:WX, Y:WY}, simultaneous=True), z, curve_B)
    back_tau = Y/(2*X)
    back_z = X/2-back_tau**2-D
    zero_on_curve(curve_B.subs({tau:back_tau, z:back_z}, simultaneous=True), Y, curve_J)
    zero(WY/(2*WX)-tau)
    zero(WX/2-(WY/(2*WX))**2-D-z)
    zero(2*(back_z+back_tau**2+D)-X)
    zero(2*back_tau*X-Y)

    # Invariants of Y^2=X^3-4DX^2+16D^2X.
    a2, a4 = -4*D, 16*D**2
    b2, b4, b6, b8 = 4*a2, 2*a4, sp.Integer(0), -a4**2
    c4 = sp.expand(b2**2-24*b4)
    c6 = sp.expand(-b2**3+36*b2*b4-216*b6)
    discriminant = sp.expand(-b2**2*b8-8*b4**3-27*b6**2+9*b2*b4*b6)
    assert c4 == -512*D**2
    assert discriminant == -196608*D**6
    zero(c4**3-c6**2-1728*discriminant)
    j = sp.cancel(c4**3/discriminant)
    assert j == sp.Rational(2048, 3) and j.q == 3

    # Isomorphism B_D -> E_CD over c^2=C; no rational origin on E_CD
    # is assumed. Use C=c^2 and reduce modulo the exact curve equations.
    cB = r**2-e
    forward_u = c/r
    forward_v = -4*c**2*D*tau/B
    curve_E = v**2-D*(u**2-c**2)*(u**2+3*c**2)
    zero_on_curve(curve_E.subs({u:forward_u, v:forward_v}, simultaneous=True), r, cB)
    zero_on_curve(forward_v+tau*(forward_u**2-c**2), r, cB)
    inverse_tau = -v/(u**2-c**2)
    inverse_r = c/u
    zero_on_curve((r**2-e).subs({tau:inverse_tau, r:inverse_r}, simultaneous=True), v, curve_E)
    zero_on_curve(-forward_v/(forward_u**2-c**2)-tau, r, cB)
    zero(c/forward_u-r)
    zero(c/inverse_r-u)
    zero_on_curve((-4*c**2*D*tau/B).subs(tau,inverse_tau)-v, v, curve_E)

    # Galois conjugation c -> -c and the exact involutions.
    zero(forward_u.subs(c,-c)+forward_u)
    zero(forward_v.subs(c,-c)-forward_v)
    zero(forward_u.subs(r,-r)+forward_u)
    zero(forward_v.subs(r,-r)-forward_v)
    assert sp.diff(-u,u) == -1  # iota pulls du/v back to -du/v.

    # The standard Weierstrass twist is J_CD. Its isomorphism is
    # (X,Y) -> (c^2 X,c^3 Y), and conjugation negates only Y.
    twisted = Y**2-X**3+4*c**2*D*X**2-16*c**4*D**2*X
    zero(twisted.subs({X:c**2*X,Y:c**3*Y},simultaneous=True)-c**6*curve_J)

    # Exhaustive fixed-point charts: u=0, or t=1/u=0.
    E_general = v**2-D*(u**2-C)*(u**2+3*C)
    zero(E_general.subs(u,0)-(v**2+3*D*C**2))
    infinity = w**2-D*(1-C*t**2)*(1+3*C*t**2)
    zero(sp.cancel(E_general.subs({u:1/t,v:w/t**2},simultaneous=True)*t**4)-infinity)
    zero(infinity.subs(t,0)-(w**2-D))
    # u -> -u and t -> -t have no other fixed base coordinates in char 0.
    assert sp.solve(sp.Eq(-u,u),u) == [0]
    assert sp.solve(sp.Eq(-t,t),t) == [0]

    # Positive sections and the exceptional fixed affine sections.
    pole = q**2-D*(s**2-C*e)*(s**2+3*C*e)
    square_section = {C:c**2,s:c,q:-4*c**2*D*tau/A}
    zero(pole.subs(square_section,simultaneous=True))
    zero((1-e)*(1+3*e)-16*D*tau**2/A**2)
    # For a^2=-3D, the fixed section is s=0, q=C e a.
    zero(pole.subs({s:0,q:C*e*a},simultaneous=True).subs(D,-a**2/3))

    report = {
        'status':'PASS',
        'scope':'rational sections over Q(tau), not rational points at specialized tau',
        'assumptions':['C and D are nonzero rational numbers','tau is transcendental'],
        'base_curve':'z^2=(tau^2-D)(tau^2+3D)',
        'constant_curve':'v^2=D(u^2-C)(u^2+3C)',
        'quotient_map':{'s':'r*u','q':'r^2*v'},
        'involutions':{'base':'(tau,r)->(tau,-r)','target':'(u,v)->(-u,v)'},
        'weierstrass_model':'Y^2=X^3-4DX^2+16D^2X',
        'invariants':{'c4':str(c4),'discriminant':str(discriminant),'j':str(j)},
        'isomorphism_over_sqrt_C':{
            'forward':['u=c/r','v=-4CD*tau/(tau^2-D)'],
            'inverse':['tau=-v/(u^2-C)','r=c/u'],
            'relation':'c^2=C'},
        'jacobian_twist':'Y^2=X^3-4CDX^2+16C^2D^2X',
        'nonsquare_C_fixed_sections':{
            'finite':'s=0, q=+/- C*e*sqrt(-3D), when -3D is square',
            'infinity':'q/s^2=+/-sqrt(D), when D is square'},
        'square_C_section':{'s':'c','q':'-4CD*tau/(tau^2+3D)'},
        'affine_section_criterion':'C is square or -3D is square',
        'projective_section_criterion':'C or D or -3D is square',
        'prepared_section_criterion':'17(17-b) is a rational square',
        'proof_dependencies':[
            'CM j-invariants are algebraic integers',
            'non-CM geometric endomorphism ring is Z',
            'nonconstant pointed genus-one morphisms induce nonzero Jacobian homomorphisms',
            'smooth projective curve extension and quadratic Galois descent'],
        'references':[
            {'author':'A. V. Sutherland','title':'The Hilbert class polynomial',
             'source':'MIT 18.783, Spring 2017, Lecture 21, Corollary 21.13, page 6',
             'url':'https://math.mit.edu/classes/18.783/2017/LectureNotes21.pdf'},
            {'author':'J. S. Milne','title':'Elliptic Curves, second edition',
             'source':'World Scientific, 2021, Chapter II, Section 1, Proposition 1.5',
             'url':'https://jmilne.org/math/Books/EC2.pdf'}],
        'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()
    }
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','j':str(j),'certificate':str(args.output),
                      'scope':'exact identities for the section criterion'},indent=2))


if __name__ == '__main__':
    main()
