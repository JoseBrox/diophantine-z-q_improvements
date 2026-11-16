#!/usr/bin/env python3
"""Exact birational maps for the varying-input pole surface.

The calculations use polynomial remainders and exact rational arithmetic.
They certify the displayed maps and inverse maps, projection parametrization,
and positive-range rational curve. No prescribed detector lift is checked.
"""
from pathlib import Path
import argparse
import json
import sympy as s

HERE = Path(__file__).resolve().parent
D, e, tau, p = s.symbols('D e tau p')
x, y, sigma, u, V, Q = s.symbols('x y sigma u V Q')
a, b, c, h, xi = s.symbols('a b c h xi')
records = []


def check(name, expression, relation=None, variable=None):
    numerator = s.fraction(s.together(expression))[0]
    if relation is not None:
        numerator = s.rem(s.Poly(numerator, variable), s.Poly(relation, variable)).as_expr()
    assert s.expand(numerator) == 0, (name, s.factor(numerator))
    records.append(name)


def run():
    records.clear()
    Fq = x*x-D*y*y-e*(sigma*sigma+3*D)
    R = 289*V*V-D
    A = u*u-e*R
    Fs = Q*Q-D*A*(u*u+3*e*R)
    den = sigma*sigma+3*D
    N = e*den
    alpha = (sigma*x-D*y)/N
    beta = (x-sigma*y)/N
    zz = (sigma*sigma-D)/den
    rr = -4*D*sigma/den

    check('conic.parametrization', rr*rr-D*(1-zz)*(1+3*zz))
    check('conic.inverse.parameter', -rr/(1-zz)-sigma)
    check('norm.factorization',
          (sigma+xi)*(x-y*xi)-(sigma*x-D*y+(x-sigma*y)*xi), xi*xi-D, xi)
    check('norm.ratio', alpha*alpha-D*beta*beta-(sigma*sigma-D)/N, Fq, x)
    check('quadric.norm', x*x-D*y*y-N, Fq, x)

    uf, Vf, Qf = 1/beta, alpha/(17*beta), rr/(beta*beta)
    Rf = 289*Vf*Vf-D
    Af = uf*uf-e*Rf
    check('surface.forward', Qf*Qf-D*Af*(uf*uf+3*e*Rf), Fq, x)
    check('open.forward.R', Rf-(sigma*sigma-D)/(N*beta*beta), Fq, x)
    check('open.forward.A', Af-4*D/(den*beta*beta), Fq, x)

    sr = -Q/A
    xr = u*(17*sr*V-D)/R
    yr = u*(17*V-sr)/R
    check('quadric.reverse', xr*xr-D*yr*yr-e*(sr*sr+3*D), Fs, Q)
    # These identities describe exactly how the two dense open sets match.
    check('open.reverse.den', sr*sr+3*D-4*D*u*u/A, Fs, Q)
    check('open.reverse.sigma2D', sr*sr-D-4*D*e*R/A, Fs, Q)
    check('open.reverse.betaNumerator', xr-sr*yr-4*D*e*u/A, Fs, Q)

    # Composition is checked in stages using the already verified norm and
    # open-locus identities, avoiding enormous unreduced rational expressions.
    check('inverse.forward.sigma', -Qf/(4*D/(den*beta*beta))-sigma)
    norm_g = (sigma*sigma-D)/N
    check('inverse.forward.x', (sigma*alpha-D*beta)/norm_g-x, Fq, x)
    check('inverse.forward.y', (alpha-sigma*beta)/norm_g-y, Fq, x)
    Nr = e*(sr*sr+3*D)
    check('inverse.reverse.beta', (xr-sr*yr)/Nr-1/u, Fs, Q)
    check('inverse.reverse.alpha', (sr*xr-D*yr)/Nr-17*V/u, Fs, Q)
    check('inverse.reverse.r', -4*D*sr/(sr*sr+3*D)-Q/(u*u), Fs, Q)

    e0 = (tau*tau-D)/(tau*tau+3*D)
    p0 = -4*D*tau/(tau*tau+3*D)
    check('first.conic', p0*p0-D*(1-e0)*(1+3*e0))
    check('first.conic.inverse', -p0/(1-e0)-tau)
    check('quadric.basepoint', tau*tau-D-e0*(tau*tau+3*D))
    check('surface.basepoint', (289*p0)**2-D*(17**2-289*e0)*(17**2+867*e0))

    H = a*a-D*b*b-e*c*c
    L = tau*a-D*b-e*tau*c
    k = -2*L/H
    xp, yp, sp = tau+k*a, 1+k*b, tau+k*c
    base_relation = tau*tau-D-e*(tau*tau+3*D)
    check('projection.identity',
          xp*xp-D*yp*yp-e*(sp*sp+3*D)-base_relation)
    direction = {a: x-tau, b: y-1, c: sigma-tau}
    check('projection.inverse',
          (H+2*L).subs(direction, simultaneous=True)-Fq+base_relation)

    # The explicit curve has R=u^2 and lies in the required affine open set
    # when h, 1-Dh^2 and p are nonzero.
    uc = (1-D*h*h)/(2*h)
    Vc = (1+D*h*h)/(34*h)
    Qc = p*uc*uc
    Rc = 289*Vc*Vc-D
    first_relation = p*p-D*(1-e)*(1+3*e)
    check('curve.hyperbola', Rc-uc*uc)
    check('curve.surface', Qc*Qc-D*(uc*uc-e*Rc)*(uc*uc+3*e*Rc), first_relation, p)
    check('curve.constant.sigma', -Qc/(uc*uc-e*Rc)+p/(1-e))
    sc = uc/Vc
    qc = Qc/(Vc*Vc)
    bc = (D/s.Integer(17))/(Vc*Vc)
    Cc = 17*(17-bc)
    check('curve.native.b', bc-68*D*h*h/(1+D*h*h)**2)
    check('curve.native.s', sc-17*(1-D*h*h)/(1+D*h*h))
    check('curve.native.C.square', Cc-sc*sc)
    check('curve.native.q', qc-p*sc*sc)
    check('curve.native.pole', qc*qc-D*(sc*sc-e*Cc)*(sc*sc+3*e*Cc), first_relation, p)
    check('curve.positive.gap', 17-bc-17*(1-D*h*h)**2/(1+D*h*h)**2)
    check('curve.small.limit', s.limit(bc, h, 0))
    check('curve.ordinate.limit', s.limit(qc, h, 0)-289*p)

    # Independent exact rational instance: D=2, tau=3, h=1/10.
    numeric = {D: s.Integer(2), tau: s.Integer(3), h: s.Rational(1, 10)}
    en = e0.subs(numeric)
    pn = p0.subs(numeric)
    un, Vn, Qn = [s.cancel(t.subs({D: 2, h: s.Rational(1, 10), p: pn}))
                 for t in (uc, Vc, Qc)]
    bn = s.cancel(bc.subs(numeric))
    assert 0 < bn < 17 and all(t != 0 for t in (un, Vn, Qn))
    assert s.cancel(Qn*Qn-2*(un*un-en*(289*Vn*Vn-2))
                    *(un*un+3*en*(289*Vn*Vn-2))) == 0
    # A smaller parameter verifies the stated 0<b<1 prepared real range.
    assert 0 < bc.subs({D: 2, h: s.Rational(1, 100)}) < 1
    bad_beta = (x+sigma*y)/N
    assert s.cancel(alpha*alpha-D*bad_beta*bad_beta-(sigma*sigma-D)/N) != 0
    assert s.cancel(289*Vc*Vc+D-uc*uc) != 0

    return {
        'schema': 'varying-input-quadric/v44',
        'status': 'PASS',
        'exactIdentities': len(records),
        'checkedIdentities': list(records),
        'surface': 'Q^2=D*(u^2-e*(289*V^2-D))*(u^2+3*e*(289*V^2-D))',
        'quadric': 'x^2-D*y^2=e*(sigma^2+3*D)',
        'sourceOpen': 'u*(289*V^2-D)*(u^2-e*(289*V^2-D)) != 0',
        'quadricOpen': '(sigma^2+3*D)*(sigma^2-D)*(x-sigma*y) != 0',
        'rationalPoint': '(x,y,sigma)=(tau,1,tau)',
        'hypotheses': 'D>0, tau!=0, tau^2!=D; e=(tau^2-D)/(tau^2+3*D)',
        'rationality': 'Exact inverse maps and projection from the specified rational point.',
        'positiveCurve': 'u=(1-D*h^2)/(2*h), V=(1+D*h^2)/(34*h), Q=p*u^2',
        'nativeInput': 'b=68*D*h^2/(1+D*h^2)^2',
        'numericInstance': {k: str(v) for k, v in
                            [('D', s.Integer(2)), ('tau', s.Integer(3)), ('e', en),
                             ('p', pn), ('h', s.Rational(1, 10)),
                             ('u', un), ('V', Vn), ('Q', Qn), ('b', bn)]},
        'negativeControls': ['wrong sign in beta', 'wrong sign in the norm hyperbola'],
        'scope': 'Rationality with freely varying V and fixed weights, including products. No prescribed elliptic detector lift, simultaneous fixed-V solution, or variable saving is asserted.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = json.dumps(run(), indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(raw)
    else:
        assert (HERE/'certificate.json').read_text() == raw
    print(raw)
