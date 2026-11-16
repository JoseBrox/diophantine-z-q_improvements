#!/usr/bin/env python3
"""Exact inert-prime certificate for the specified order-three contact coupling."""
from pathlib import Path
from math import isqrt
import argparse
import json
import sympy as sp

ROOT = Path(__file__).resolve().parent


class Curve:
    """Affine arithmetic over (Z/mZ)[sqrt(2)] on y²=x³-(11-6sqrt(2))x."""
    def __init__(self, modulus):
        self.m = modulus
        self.D = self.f(11, -6)
        R = (self.f(1, 1), self.f(0, 2))
        self.P = self.add(R, R)
        assert self.on(self.P)

    def f(self, a, b=0):
        return a % self.m, b % self.m

    def plus(self, x, y):
        return self.f(x[0]+y[0], x[1]+y[1])

    def minus(self, x, y):
        return self.f(x[0]-y[0], x[1]-y[1])

    def times(self, x, y):
        return self.f(x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])

    def divide(self, x, y):
        inverse = pow((y[0]*y[0]-2*y[1]*y[1]) % self.m, -1, self.m)
        return self.times(x, self.f(y[0]*inverse, -y[1]*inverse))

    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        x, y = P
        a, b = Q
        if x == a:
            if self.plus(y, b) == (0, 0):
                return None
            slope = self.divide(self.minus(self.times(self.f(3), self.times(x, x)), self.D),
                                self.times(self.f(2), y))
        else:
            slope = self.divide(self.minus(b, y), self.minus(a, x))
        u = self.minus(self.minus(self.times(slope, slope), x), a)
        return u, self.minus(self.times(slope, self.minus(x, u)), y)

    def multiply(self, n, P):
        result = None
        while n:
            if n & 1:
                result = self.add(result, P)
            n >>= 1
            if n:
                P = self.add(P, P)
        return result

    def on(self, P):
        if P is None:
            return True
        x, y = P
        return self.times(y, y) == self.minus(self.times(self.times(x, x), x),
                                              self.times(self.D, x))


def algebraic_identities():
    t, u = sp.symbols('t u')
    F = lambda x: x*(x+1)*(2*x+1)*(3*x+1)*(4*x+1)*(5*x+2)/120
    q = lambda x: 7*x*x+5*x+1
    gamma = lambda x: -(2*x+1)/(7*x+3)
    t0 = (1-3*u)/(7*u)
    t1 = -(u+2)/7
    a = u*(u+2)/(3*u-1)
    identities = [gamma(gamma(gamma(t)))-t,
                  F(gamma(t))-F(t)/(7*t+3)**6,
                  q(gamma(t))-q(t)/(7*t+3)**2,
                  gamma(t0)-t1, a*t0-t1,
                  F(t1)-u**6*F(t0),
                  F(t0)-(u-5)*(u+2)*(2*u-3)*(3*u-1)*(4*u+1)*(5*u-4)/(14117880*u**6),
                  q(t0)-(u*u-u+1)/(7*u*u),
                  q(t1)-(u*u-u+1)/7]
    assert all(sp.cancel(f) == 0 for f in identities)
    return len(identities)


def certificate():
    c = json.loads((ROOT/'source_certificate.json').read_text())
    p, N = c['prime'], c['annihilator']
    assert p > 2 and all(p % d for d in range(2, isqrt(p)+1))
    assert p % 8 == 5 and N % p != 0
    E = Curve(p)
    assert E.multiply(N, E.P) is None
    covered = bytearray(p)
    roots = [4*pow(5, -1, p) % p, 3*pow(2, -1, p) % p, 5]
    simple_contacts = []
    for u in roots:
        factors = [u-5, u+2, 2*u-3, 3*u-1, 4*u+1, 5*u-4]
        slopes = [1, 1, 2, 3, 4, 5]
        derivative = 0
        product = 1
        for term in factors:
            product = product*term % p
        for i in range(6):
            term = slopes[i]
            for j in range(6):
                if j != i:
                    term = term*factors[j] % p
            derivative = (derivative+term) % p
        assert product == 0 and derivative != 0
        t = (1-3*u)*pow(7*u, -1, p) % p
        s = -(u+2)*pow(7, -1, p) % p
        a = u*(u+2)*pow(3*u-1, -1, p) % p
        guards = [u, 3*u-1, t, s, a, a-1, t-1, s-1,
                  7*t*t+5*t+1, 7*s*s+5*s+1]
        assert all(v % p for v in guards)
        simple_contacts.append({'root':u, 'derivative':derivative,
                                'denominator_and_scale_guards':True})
    for n, T, u, y in c['rows']:
        A = E.multiply(n, E.P)
        assert A is not None and E.on(A)
        assert 2*A[0][0] % p == T
        assert (pow(y, 4, p)+pow(T, 4, p)) % p == u
        assert y % p
        assert all((v[0]*v[0]-2*v[1]*v[1]) % p for v in A)
        for x in range(1, p):
            covered[(y-x*x) % p] = 1
    assert sum(covered) == p
    f = c['fixture']
    m = p*p
    E2 = Curve(m)
    A = E2.multiply(f['X'], E2.P)
    assert list(A[0]) == f['xA'] and list(A[1]) == f['yA']
    T = 2*A[0][0] % m
    u = (pow(f['X']**2+f['B'], 4, m)+pow(T, 4, m)) % m
    t0 = (1-3*u)*pow(7*u, -1, m) % m
    t1 = -(u+2)*pow(7, -1, m) % m
    a = u*(u+2)*pow(3*u-1, -1, m) % m
    F = lambda t: t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)*pow(120, -1, m) % m
    q = lambda t: (7*t*t+5*t+1) % m
    eta = F(t0)*pow(pow(q(t0), 3, m), -1, m) % m
    weight = F(t0)*pow(4*pow(t0-1, 8, m), -1, m) % m
    result = dict(trace=T, u=u, t0=t0, t1=t1, a=a, F0=F(t0), F1=F(t1),
                  q0=q(t0), q1=q(t1), eta=eta, original_weight=weight)
    assert all(f[key] == value for key, value in result.items())
    assert (F(t1)-pow(u, 6, m)*F(t0)) % m == 0
    assert F(t1)*pow(pow(q(t1), 3, m), -1, m) % m == eta
    assert [F(t0)//p, F(t1)//p] == [44771, 73604]
    assert F(t0) % p == F(t1) % p == 0
    return {
        'schema':'diophantine-order-three-inert/v56', 'status':'PASS',
        'rational_function_identities':algebraic_identities(),
        'prime':p, 'prime_is_inert':True, 'annihilator':N,
        'annihilator_checked':True, 'rows':c['rows'],
        'covered_shift_residues':sum(covered),
        'simple_contacts':simple_contacts, 'fixture':f,
        'scope':('Exact finite certificate for the displayed prescribed-index '
                 'deterministic coupling. The manuscript supplies the lifting '
                 'argument for every positive odd shift and infinitely many '
                 'positive integer inputs. Other couplings are not excluded.'),
        'uniform_rational_realization_excluded_for_this_coupling':True,
        'other_couplings_excluded':False, 'new_defining_variable_bound':False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    text = json.dumps(certificate(), indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')
