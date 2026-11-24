#!/usr/bin/env python3
"""Independent exact checks for the signed first-Pell projection theorem.

No coefficient-table builder is imported. The zero-s divisor candidates are
exhaustive after the manuscript's reduction to b-1 | 5**60 and b>32.
The signed binomial fixtures verify their indicated local core, not the
astronomical third Pell witness or the entire coding source.
"""
from fractions import Fraction
from math import comb
from pathlib import Path
import argparse
import json
import sympy as sp


def pell(a, n):
    """Polynomial Pell sequences evaluated exactly at an integer parameter."""
    x0, x1, y0, y1 = 1, a, 0, 1
    if n == 0:
        return x0, y0
    for _ in range(1, n):
        x0, x1 = x1, 2*a*x1-x0
        y0, y1 = y1, 2*a*y1-y0
    return x1, y1


def v5(n):
    assert n != 0
    n = abs(n)
    out = 0
    while n % 5 == 0:
        n //= 5
        out += 1
    return out


def verify():
    a, b, s, u, t = sp.symbols('a b s u t')
    a0 = (b**9+8*b**5+b-8)/2
    h0 = (sum(b**j for j in range(9))
          + 8*sum(b**j for j in range(5))+1)/2
    astar = a0+5*(b**5-1)*s
    mstar = 2*b*astar-b*b-1
    assert sp.expand(a0-1-(b-1)*h0) == 0
    assert sp.expand(mstar-(b**5-1)*(b**5+8*b+1+10*b*s)) == 0
    # This polynomial congruence proves 2 H(1+125t) = 50 (mod 125).
    congruence = sp.Poly(sp.expand((2*h0.subs(b, 1+125*t)-50)/125), t)
    assert all(c.q == 1 for c in congruence.all_coeffs())
    assert h0.subs(b, 1) == 25
    for parity in (0, 1):
        assert int((2*h0).subs(b, parity)) % 2 == 0

    symbolic_pell_checks = 0
    xs, ys = [sp.Integer(1), a], [sp.Integer(0), sp.Integer(1)]
    for _ in range(1, 10):
        xs.append(sp.expand(2*a*xs[-1]-xs[-2]))
        ys.append(sp.expand(2*a*ys[-1]-ys[-2]))
    modulus = 2*b*a-b*b-1
    for j in range(10):
        rminus = xs[j]-(a-b)*ys[j]
        rplus = xs[j]+(a-b)*ys[j]
        rnext = xs[j+1]-(a-b)*ys[j+1]
        assert sp.expand(xs[j]**2-(a*a-1)*ys[j]**2-1) == 0
        assert sp.expand(rnext-b*rminus-modulus*ys[j]) == 0
        assert sp.expand(rminus*rplus-1-modulus*ys[j]**2) == 0
        symbolic_pell_checks += 3

    L = 5**60
    zero_s_candidates = []
    for exponent in range(3, 61):
        bv = 1+5**exponent
        hv = (sum(bv**j for j in range(9))
              +8*sum(bv**j for j in range(5))+1)//2
        av = (bv**9+8*bv**5+bv-8)//2
        assert bv > 32 and av-1 == (bv-1)*hv
        assert hv > 25 and hv % 125 == 25 and v5(hv) == 2
        assert L % (av-1) != 0
        zero_s_candidates.append(exponent)

    parameter_checks = 0
    signed_power_checks = 0
    negative_parameter_checks = 0
    for bv in range(2, 35):
        for sv in (-bv**16, -1, 0, 1, bv**16):
            av = (bv**9+8*bv**5+bv-8)//2+5*(bv**5-1)*sv
            mv = 2*bv*av-bv*bv-1
            assert av % 5 == 1 and abs(av) >= 2 and mv != 0
            assert mv == (bv**5-1)*(bv**5+8*bv+1+10*bv*sv)
            parameter_checks += 1
            if av < 0:
                negative_parameter_checks += 1
            for index in (0, 5, 10, 15):
                xv, yv = pell(av, index)
                assert xv*xv-(av*av-1)*yv*yv == 1
                assert yv % 5 == 0
                for sign_c in (-1, 1):
                    for sign_d in (-1, 1):
                        qv = sign_d*xv-(av-bv)*sign_c*yv
                        assert qv % (bv**5-1) in (1, bv**5-2)
                        assert (qv**4-1) % (bv**5-1) == 0
                        signed_power_checks += 1

    # All four independent signs of the first Pell coordinates.
    first_sign_checks = 0
    for av in (*range(-12, -1), *range(2, 13)):
        mv = 4*av-5
        for index in (3, 5, 7, 9):
            xv, yv = pell(av, index)
            assert yv > 0
            for tau in (-1, 1):
                for kappa in (-1, 1):
                    bw_residue = tau*xv-(av-2)*kappa*yv
                    if tau == kappa:
                        assert (bw_residue-tau*2**index) % abs(mv) == 0
                    else:
                        assert (bw_residue*2**index-tau) % abs(mv) == 0
                    first_sign_checks += 1

    normalization_checks = 0
    truncation_checks = 0
    for rv in range(1, 9):
        for uv in (16, 17, 32, 64):
            for zv in (16, 17, 32):
                for sigma in (-1, 1):
                    av = rv*zv*(uv+sigma)
                    pv = 2*rv*rv*zv*zv*uv
                    cv = pell(av, 2*rv+1)[1]
                    kv = pell(pv, rv+1)[1]
                    rho = Fraction((uv+sigma)**(2*rv), uv**rv)
                    error = rho-Fraction(cv, kv)
                    assert 0 < error < rho/(zv*zv*(uv-1)**2)
                    assert Fraction(zv, 1)+Fraction(1, 2) < Fraction(zv*zv*(uv-1)**2-1, 4)
                    normalization_checks += 1
            for sigma in (-1, 1):
                rho = Fraction((uv+sigma)**(2*rv), uv**rv)
                trunc = sum(comb(2*rv, j)*sigma**j*uv**(rv-j)
                            for j in range(rv+1))
                tail_bound = Fraction(4**rv, uv-1)
                assert abs(rho-trunc) < tail_bound
                truncation_checks += 1

    # Local signed-binomial core: both signs of w and both parities of r.
    # These do not claim the source-prefix bounds r>=M>=b**128, nor do
    # they construct the enormous independent third-Pell completion.
    local_core_fixtures = []
    for rv, mv, bv in ((15, 16, 2), (15, 16, 4),
                       (30, 16, 2), (30, 16, 4), (31, 32, 8)):
        assert mv >= 16 and mv >= 4*bv
        assert comb(2*rv, rv) % mv == 0
        B = 2*rv+1
        for sigma in (-1, 1):
            wv = sigma*2**B//bv
            uv = abs(wv)*mv
            zv = sum(comb(2*rv, j)*sigma**j*uv**(rv-j)
                     for j in range(rv+1))
            assert zv > 0 and zv % mv == 0
            sv = sigma**(rv+1)*(zv//mv)
            yy = sv*mv
            av = (wv*mv+1)*rv*yy
            pv = 2*wv*rv*rv*yy*yy*mv
            dx, cy = pell(av, B)
            dv, cv = sigma*dx, sigma*cy
            tau, kv = pell(pv, rv+1)
            assert dv*dv-(av*av-1)*cv*cv == 1
            assert tau*tau-(pv*pv-1)*kv*kv == 1
            assert (kv-rv-1) % (pv-1) == 0
            hv = (kv-rv-1)//(pv-1)
            assert (dv-bv*wv-(av-2)*cv) % (4*av-5) == 0
            gamma = (dv-bv*wv-(av-2)*cv)//(4*av-5)
            assert dv == bv*wv+(av-2)*cv+(4*av-5)*gamma
            assert kv == rv+1+hv*(pv-1)
            eta = kv*kv-4*(cv-kv*yy)**2
            assert eta > 0 and 2*abs(cv-kv*yy) < abs(kv)
            assert abs(bv*wv) == 2**B
            assert (cv > 0) == (sigma > 0)
            assert (sv > 0) == (sigma**(rv+1) > 0)
            halftrace_rhs = 2*(av*dv+(av*av-1)*cv+1)
            if sigma < 0:
                assert halftrace_rhs < 0
            else:
                assert halftrace_rhs == (2*pell(av, rv+1)[0])**2

            rho_num, rho_den = (uv+sigma)**(2*rv), uv**rv
            error_num = rho_num*abs(kv)-abs(cv)*rho_den
            assert 0 < error_num
            assert 4*error_num < abs(kv)*rho_den
            assert 4*abs(rho_num-zv*rho_den) < rho_den
            assert abs(av) > 2*uv*4**rv
            assert abs(4*av-5) > 4*uv*4**rv+1
            assert Fraction(4**rv, uv) == Fraction(bv, 2*mv)
            local_core_fixtures.append({
                'r':rv, 'M':mv, 'b':bv, 'sign_w':sigma,
                'sign_s':1 if sv > 0 else -1,
                'sign_a':1 if av > 0 else -1,
                'halftrace_square_exists':sigma > 0,
                'largest_checked_coordinate_bits':max(abs(cv).bit_length(), abs(kv).bit_length()),
            })

    growth_checks = 0
    for rv in range(6, 41):
        uv = 4**rv
        assert 2*rv < uv and Fraction(2*rv, uv) <= Fraction(1, 2)
        assert (uv-2)**rv * 2 >= uv**rv
        assert Fraction(7, 16)*uv > 1
        assert uv > 7*rv+2
        assert Fraction(6*rv+1, 32)+1 <= rv-2
        growth_checks += 1
    assert Fraction(2, 15) < Fraction(1, 4)
    assert 5**60 < 2**640

    return {
        'status':'PASS',
        'proof':'undecidability/pell_signed_branch_v101/signed_branch_projection.tex',
        'independent_of_table_builders':True,
        'symbolic_parameter_checks':3,
        'symbolic_pell_identities':symbolic_pell_checks,
        'zero_s_divisor_candidates_exhaustive_after_proved_reduction':zero_s_candidates,
        'zero_s_divisor_candidates_count':len(zero_s_candidates),
        'parameter_fixtures':parameter_checks,
        'negative_auxiliary_parameter_fixtures':negative_parameter_checks,
        'four_sign_power_fixtures_including_zero_index':signed_power_checks,
        'four_sign_first_pell_congruence_fixtures':first_sign_checks,
        'normalized_ratio_fixtures':normalization_checks,
        'alternating_tail_fixtures':truncation_checks,
        'signed_binomial_local_core_fixtures':local_core_fixtures,
        'elementary_growth_fixtures':growth_checks,
        'local_fixture_scope':'First and small Pell norms, congruence quotients, strict old margin, signed truncation and bounds; no coding prefix or third Pell equation asserted',
        'equivalence_scope':'Coding-prefix and instance projection; auxiliary witnesses may be chosen anew',
        'positive_auxiliary_values_for_all_zeros_claimed':False,
        'not_machine_verified':['Quantified source equivalence', 'Full coefficient-table deletion',
                                'Jones coding theorem', 'Retained arithmetic integer interfaces'],
        'unconditional_undecidability_claim':False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=verify()
    path=Path(__file__).with_name('signed_branch_lemmas_certificate.json')
    if args.write:
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        assert json.loads(path.read_text()) == result
    summary={k:v for k,v in result.items() if k not in {
        'signed_binomial_local_core_fixtures',
        'zero_s_divisor_candidates_exhaustive_after_proved_reduction'}}
    summary['signed_binomial_local_core_count']=len(result['signed_binomial_local_core_fixtures'])
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__':
    main()
