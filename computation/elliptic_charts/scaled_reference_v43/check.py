#!/usr/bin/env python3
"""Exact generic identities for the scaled reference and trace blocks."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE/'verification.json')
    args = parser.parse_args()
    ell, J, alpha, c, delta = s.symbols('ell J alpha c delta')
    a = delta+c*c
    D = a*delta
    gamma = alpha-delta*J-1
    Q = alpha*gamma+c*ell*(1-delta*J)+2*delta*J
    basis = s.groebner([J-ell*ell, Q], alpha, J, ell,
                       domain=s.QQ.frac_field(c, delta))
    checked = []

    def chart_zero(expr, name):
        numerator = s.fraction(s.cancel(expr))[0]
        assert basis.reduce(numerator)[1] == 0, name
        checked.append(name)

    def zero(expr, name):
        assert s.cancel(expr) == 0, name
        checked.append(name)

    v, S, T = 1/ell, alpha/ell, gamma/ell
    chart_zero(ell**2*(v*(v+T-S)+delta), 'old first chart row')
    chart_zero(ell**2*(S*T+c*(T-S)+2*c*v+2*delta), 'old second chart row')
    fH = (1-alpha-c*ell)/a
    gH = (alpha-delta*J-c*ell)/a
    hH = ((c+delta*ell)*alpha+c*delta*J-2*delta*ell-c)/a
    kH = ((c+delta*ell)*gamma+c-c*delta*J+2*delta*ell)/a
    zero(fH-(v-S-c)/(a*v), 'first linear reciprocal abscissa')
    zero(gH-(v+T-c)/(a*v), 'second linear reciprocal abscissa')
    chart_zero(fH*gH-J/a, 'reciprocal product')
    chart_zero(ell*hH+alpha*fH, 'first polynomial reciprocal ordinate')
    chart_zero(ell*kH+gamma*gH, 'second polynomial reciprocal ordinate')
    chart_zero(hH*hH-fH+D*fH**3, 'first reciprocal cubic')
    chart_zero(kH*kH-gH+D*gH**3, 'second reciprocal cubic')
    for value, expected in ((1, (0, 0, 1/a, c/a)),
                            (0, (1/a, -c/a, 0, 0))):
        sub = {ell: 0, J: 0, alpha: value}
        actual = tuple(s.cancel(x.subs(sub)) for x in (fH, hH, gH, kH))
        assert all(s.cancel(x-y) == 0 for x, y in zip(actual, expected))
        assert s.diff(Q, alpha).subs(sub) == 2*value-1
    checked.append('both smooth boundary points and all four reciprocal values')

    f, h, g, k, slope, FU, FV, L, L0 = s.symbols('f h g k slope FU FV L L0')
    # Use separate symbols to check all degrees before substituting scalings.
    fs, hs, gs, ks, ss, Fs, Gs, kap = s.symbols('fs hs gs ks ss Fs Gs kap')
    original_pair = [FU-f*f, FV-g*g, h*h-f+D*f*FU,
                     slope*(f-g)-h-k,
                     slope*(h-k)-1+D*(FU+f*g+FV)]
    scaled_pair = [Fs-fs*fs, Gs-gs*gs, hs*hs-kap*fs+D*fs*Fs,
                   ss*(fs-gs)-hs-ks,
                   ss*(hs-ks)-kap+D*(Fs+fs*gs+Gs)]
    substitution = {fs: ell**2*f, gs: ell**2*g, hs: ell**3*h,
                    ks: ell**3*k, ss: ell*slope, Fs: ell**4*FU,
                    Gs: ell**4*FV, kap: ell**4}
    exponents = (4, 4, 6, 3, 4)
    for j, (old, new, power) in enumerate(zip(original_pair, scaled_pair, exponents)):
        zero(new.subs(substitution)-ell**power*old, f'point row {j+1}, exponent {power}')
    scaled_ratios = [hs*L+fs*alpha, (kap-D*Fs)*L+hs*alpha,
                     ks*L0+gs*gamma, (kap-D*Gs)*L0+ks*gamma]
    old_ratios = [h*L+f*S, (1-D*FU)*L+h*S,
                  k*L0+g*T, (1-D*FV)*L0+k*T]
    for j, (old, new, power) in enumerate(zip(old_ratios, scaled_ratios, (3, 4, 3, 4))):
        zero(new.subs(substitution)-ell**power*old, f'ratio row {j+1}, exponent {power}')
    zero((ss*ss+D*(fs+gs)).subs(substitution)
         -ell**2*(slope*slope+D*(f+g)), 'difference abscissa scaling')

    variables = (ell, J, alpha, kap, fs, hs, gs, ks, ss, Fs, Gs, L, L0)
    rows = [J-ell*ell, Q, kap-J*J]+scaled_pair+scaled_ratios
    degrees = [s.Poly(row, *variables).total_degree() for row in rows]
    assert degrees == [2]*12
    checked.append('all twelve field chart, point and ratio rows are quadratic')

    j0, j1, trace, imag, n0, n1, rho = s.symbols('j0 j1 trace imag n0 n1 rho')
    trace_row = (j0+rho*j1)*(trace/2+rho*imag)-(n0+rho*n1)
    reduced = s.rem(s.expand(trace_row), rho*rho-2, rho)
    real = j0*trace/2+2*j1*imag-n0
    imaginary = j0*imag+j1*trace/2-n1
    zero(reduced-real-rho*imaginary, 'exact rational trace splitting')
    assert s.Poly(real, j0, j1, trace, imag, n0, n1).total_degree() == 2
    assert s.Poly(imaginary, j0, j1, trace, imag, n0, n1).total_degree() == 2
    assert s.Matrix([[j0, 2*j1], [j1, j0]]).det() == j0*j0-2*j1*j1

    ell0, ell1, zeta, kap0 = s.symbols('ell0 ell1 zeta kap0')
    fourth = s.rem(s.expand((ell0+rho*ell1)**4), rho*rho-2, rho)
    real_fourth = s.expand(fourth).coeff(rho, 0)
    assert real_fourth == ell0**4+12*ell0*ell0*ell1*ell1+4*ell1**4
    assert all(coefficient > 0 for coefficient in s.Poly(real_fourth, ell0, ell1).coeffs())
    assert s.Poly(kap0*zeta-1, kap0, zeta).total_degree() == 2
    checked.append('exact positive rational fourth-power nonzero guard')

    # The nonzero hypothesis is real: a boundary point supports a degenerate
    # scaled pair, with both comparison ratios arbitrary nonzero beta.
    beta = s.symbols('beta', nonzero=True)
    boundary = {ell: 0, J: 0, alpha: 1, kap: 0,
                fs: -1/(D*beta**2), hs: 1/(D*beta**3),
                gs: 0, ks: 0, ss: -1/beta,
                Fs: 1/(D*D*beta**4), Gs: 0, L: beta, L0: beta}
    for row in rows:
        zero(row.subs(boundary), 'explicit degenerate boundary row')
    zero((ss*ss+D*(fs+gs)).subs(boundary), 'degenerate height numerator')

    old_count = 2*5+2*7+2*4+1
    new_count = 2*4+2*7+2*4+2
    assert old_count == 33 and new_count == 32
    guarded_count = new_count+1
    assert guarded_count == old_count == 33
    parents = ['papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex',
               'papers/trace_heights/trace_on_all_points_20261113_v25.tex',
               'papers/elliptic_charts/compressed_reference_20261114_v27.tex']
    report = {
        'status': 'PASS',
        'scope': 'exact reference, scaled point/ratio and trace block equivalence on ell!=0; no full defining-polynomial bound',
        'checks': checked,
        'field_row_degrees': degrees,
        'chart_boundary': [{'ell': 0, 'J': 0, 'alpha': 1, 'point': 'O'},
                           {'ell': 0, 'J': 0, 'alpha': 0, 'point': 'P'}],
        'counts': {'unscaled_block': old_count, 'scaled_block': new_count,
                   'saving_on_nonzero_locus': 1, 'nonzero_guard_coordinates': 1,
                   'guarded_scaled_block': guarded_count, 'net_guarded_saving': 0},
        'nonzero_guard': 'kappa_0*zeta=1; kappa_0=ell_0^4+12*ell_0^2*ell_1^2+4*ell_1^4',
        'excluded_from_count': ['detector conversion', 'contact and pole conversion'],
        'parent_sha256': {path: sha256((ROOT/path).read_bytes()).hexdigest() for path in parents},
        'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'identities': len(checked),
                      'certificate': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
