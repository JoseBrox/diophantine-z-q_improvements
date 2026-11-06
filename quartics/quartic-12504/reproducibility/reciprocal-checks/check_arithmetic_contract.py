"""Finite checks supporting, but not replacing, the arithmetic proof review."""
from fractions import Fraction as F
from math import comb
import json
from check_reciprocal_probe import independent_coefficients


def truncated_product(a, b, n):
    out = [F(0)]*n
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i+j < n:
                out[i+j] += x*y
    return out


def composition(a, w, n):
    out = [F(0)]*n
    power = [F(1)]+[F(0)]*(n-1)
    for c in a:
        out = [x+c*y for x, y in zip(out, power)]
        power = truncated_product(power, w, n)
    return out


def fm(x, y):
    return x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def inv(x):
    norm = x[0]*x[0]-2*x[1]*x[1]
    assert norm
    return x[0]/norm, -x[1]/norm


def gvalue(f, count):
    w = fm((F(11), F(-6)), fm(f, f))
    out, power = (F(0), F(0)), (F(1), F(0))
    for c in independent_coefficients(count):
        out = tuple(x+c*y for x, y in zip(out, power))
        power = fm(power, w)
    return out


def main():
    formal = []
    for m in (4, 13, 16):
        n = m+1
        # f=z² F(t), t=Dz⁴, F=1-tF²: signed Catalan coefficients.
        fseries = [F((-1)**j*comb(2*j, j), j+1) for j in range(n)]
        w = [F(0)]+truncated_product(fseries, fseries, n-1)
        actual = composition(independent_coefficients(m), w, n)
        expected = [F((-1)**j*comb(2*j, j), 4*j+1) for j in range(n)]
        assert actual[:m] == expected[:m]
        assert actual[m] != expected[m]
        formal.append({'terms': m, 'matched_through_w_degree': m-1,
                       'first_omitted_coefficient_really_changes': True})
    cs = independent_coefficients(16)
    assert cs[6] == F(-418, 16575)
    assert cs[12]/cs[6] == F(1195701, 3387461)
    assert cs[10]/cs[12] == F(735, 559)
    assert cs[11]/cs[12] == F(49, 43)
    for c in cs[1:]:
        assert c.numerator % 2 == 0 and c.numerator % 4 != 0
        assert c.denominator % 2 == 1
    assert 3*((1 << 23)-1) > 4*(4783227+5)
    assert F(16+24, 20*(2*16-24)) == F(1, 4)
    assert F(3*((1 << 25)-1), 2) > F(52, 2*52-96)*4783232
    assert F(13+24, 20*(2*13-24)) == F(37, 40)
    assert 3*((76177-1)//4) >= 4*16
    # Direct forward/reverse ratio maps, including nonrational field pairs.
    fvalues = [(F(0), F(0)), (F(1, 2), F(-1, 3)), (F(-2), F(1)),
               (F(456,1681), F(224,1681)), (F(3,5), F(2,7))]
    pvalues = [(F(1),F(0)), (F(2),F(1)), (F(-1),F(1)),
               (F(-3567,1681),F(5289,6724)), (F(0),F(1))]
    gs = [gvalue(f, 4 if i == 1 else 16) for i, f in enumerate(fvalues)]
    lam = fm(gs[0], inv(pvalues[0]))
    lzero = tuple(-x for x in lam)
    for p, g in zip(pvalues[1:], gs[1:]):
        c = fm(g, inv(fm(p, lam)))
        a = fm(c, p)
        assert fm(a, lam) == g
        z = tuple(-x for x in inv(p))
        assert fm(fm(z, g), inv(lzero)) == c
    print(json.dumps({'status': 'PASS', 'formal_change_of_parameter': formal,
                      'normalization_constants': 'PASS', 'two_adic_coefficients': 'PASS',
                      'anchor_and_beta_inequalities': 'PASS', 'compressed_ratio_examples': 'PASS',
                      'scope': 'Finite identities and sample maps only; uniform proofs require independent mathematical review'}, indent=2))


if __name__ == '__main__':
    main()
