#!/usr/bin/env python3
"""Exact finite tests for the finite-support extension of BB Theorem 2.3.
No L-value, rank, or rational-point computation is asserted by this checker.
The infinite conclusions use the written genus-point proof and cited theorems.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import prod, isqrt, gcd
import json
import random
import sympy as sp


def rank2(rows, ncols):
    rows = list(rows)
    rank = 0
    for col in range(ncols):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] >> col & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] >> col & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def det2(matrix):
    n = len(matrix)
    return int(rank2([sum((x & 1) << j for j, x in enumerate(row)) for row in matrix], n) == n)


def lbit(a, p):
    x = pow(a % p, (p - 1) // 2, p)
    assert x in (1, p - 1)
    return int(x != 1)


def residue_bits(r):
    return int(r in (3, 7)), int(r in (3, 5))


def build_matrix(residues, off):
    t = len(residues)
    A = [[0] * t for _ in range(t)]
    for i in range(t):
        for j in range(t):
            if i != j:
                A[i][j] = off[i][j] & 1
        A[i][i] = sum(A[i]) & 1
    return A


def descent_test(residues, off, J_indices, first_edge_leaf):
    t = len(residues)
    A = build_matrix(residues, off)
    y, z = zip(*(residue_bits(r) for r in residues))
    rows = []
    for i in range(t):
        rows.append(sum(A[i][q] << q for q in range(t)) | (y[i] << (t + i)))
    for i in range(t):
        rows.append((z[i] << i) | sum((A[i][q] ^ (y[i] if i == q else 0)) << (t + q) for q in range(t)))
    a = sum(1 << q for q in J_indices)
    b = a
    for ell, leaf in first_edge_leaf:
        b |= z[leaf] << ell
    vector = a | (b << t)
    assert all((row & vector).bit_count() % 2 == 0 for row in rows)
    corank = 2 * t - rank2(rows, 2 * t)
    assert corank == 1
    return corank


def genus_sum(residues, off):
    t = len(residues)
    @lru_cache(None)
    def residue(mask):
        r = 1
        for i in range(t):
            if mask >> i & 1:
                r = r * residues[i] % 8
        return r
    @lru_cache(None)
    def gamma(mask):
        inds = [i for i in range(t) if mask >> i & 1]
        if not inds:
            raise ValueError('factor 1 is excluded')
        r = residue(mask)
        if r not in (1, 3, 7):
            return 0
        A = build_matrix([residues[i] for i in inds], [[off[i][j] for j in inds] for i in inds])
        if r in (3, 7):
            # All cofactors agree; verify this finite identity as well.
            values = [det2([[A[i][j] for j in range(len(inds)) if j != v] for i in range(len(inds)) if i != v]) for v in range(len(inds))]
        else:
            z = [residue_bits(residues[i])[1] for i in inds]
            values = [det2([[A[i][j] for j in range(len(inds)) if j != v] + [z[i]] for i in range(len(inds))]) for v in range(len(inds))]
        assert len(set(values)) == 1
        return values[0]
    @lru_cache(None)
    def partitions(mask, need7, need3):
        if not mask:
            return int(not need7 and not need3)
        low = mask & -mask
        ans = 0
        sub = mask
        while sub:
            if sub & low:
                r = residue(sub)
                if gamma(sub):
                    if r == 1:
                        ans ^= partitions(mask ^ sub, need7, need3)
                    elif r == 7 and need7:
                        ans ^= partitions(mask ^ sub, False, need3)
                    elif r == 3 and need3:
                        ans ^= partitions(mask ^ sub, need7, False)
            sub = (sub - 1) & mask
        return ans
    answer = partitions((1 << t) - 1, True, True)
    assert answer == 1
    return answer


def actual_primes(J, K):
    """Choose subdivision primes first, then the moving prime p0."""
    assert prod(J) % 8 == 7
    assert all(lbit(prod(J), q) == 0 for q in K)
    original = list(J) + list(K)
    edges = [(J[0], q, 'J') for q in J[1:]] + [(None, q, 'K') for q in K]
    ells = []
    for a, b, kind in edges:
        for ell in sp.primerange(3, 5000000):
            ell = int(ell)
            if ell % 8 != 1 or ell in original or ell in ells:
                continue
            if all(lbit(q, ell) == int(q in (a, b)) for q in original) and all(lbit(q, ell) == 0 for q in ells):
                ells.append(ell)
                break
        else:
            raise RuntimeError('finite search bound insufficient')
    deg = {p: int(len(J) > 1) if p != J[0] else len(J) - 1 for p in J}
    for p0 in sp.primerange(3, 5000000):
        p0 = int(p0)
        if p0 % 8 != 3 or p0 in original or p0 in ells:
            continue
        if all(lbit(p0, p) == ((deg[p] & 1) ^ residue_bits(p % 8)[0]) for p in J) and all(lbit(p0, ell) == int(kind == 'K') for ell, (_, _, kind) in zip(ells, edges)):
            break
    else:
        raise RuntimeError('finite search bound insufficient')
    n = prod(J + [p0] + ells)
    records = []
    for bits in product((0, 1), repeat=len(K)):
        selected = [q for q, bit in zip(K, bits) if bit]
        k = prod(selected)
        if k % 8 != 1 or any(lbit(k, p) for p in J):
            continue
        primes = list(J) + [p0] + ells + selected
        off = [[0 if i == q else lbit(primes[q], primes[i]) for q in range(len(primes))] for i in range(len(primes))]
        residues = [p % 8 for p in primes]
        first = [(len(J) + 1 + i, i + 1) for i in range(len(J) - 1)]
        corank = descent_test(residues, off, range(len(J)), first)
        genus = genus_sum(residues, off)
        records.append({'k': k, 'D': n * k, 'descent_corank': corank, 'genus_sum_mod_2': genus})
    return {'j': prod(J), 'J': J, 'K': K, 'subdivision_primes': ells, 'moving_prime': p0, 'n': n, 'curves': records}


def random_graph(rng, r, s):
    # Enumerate arbitrary reciprocity-compatible symbols, then constrain each
    # K-prime by (j/q)=+1. Residues are exact formal Legendre-symbol data.
    while True:
        jr = [rng.choice((1, 3, 5, 7)) for _ in range(r)]
        if prod(jr) % 8 == 7:
            break
    kr = [rng.choice((1, 3, 5, 7)) for _ in range(s)]
    original_res = jr + [3] + kr
    t0 = len(original_res)
    off0 = [[0] * t0 for _ in range(t0)]
    def setpair(i, q, val):
        yi, _ = residue_bits(original_res[i])
        yq, _ = residue_bits(original_res[q])
        off0[i][q] = val
        off0[q][i] = val ^ (yi * yq)
    for i in range(t0):
        for q in range(i + 1, t0):
            setpair(i, q, rng.randrange(2))
    deg = [r - 1] + [1] * (r - 1)
    for i in range(r):
        setpair(i, r, (deg[i] & 1) ^ residue_bits(jr[i])[0])
    for q in range(r + 1, t0):
        # Change the last J symbol to make the q-row sum on J zero.
        val = sum(off0[q][i] for i in range(r - 1)) & 1
        setpair(q, r - 1, val)
    edges = [(0, i) for i in range(1, r)] + [(r, r + 1 + i) for i in range(s)]
    residues_all = original_res + [1] * len(edges)
    t = len(residues_all)
    off = [[0] * t for _ in range(t)]
    for i in range(t0):
        for q in range(t0):
            off[i][q] = off0[i][q]
    for z, (a, b) in enumerate(edges, t0):
        off[z][a] = off[a][z] = off[z][b] = off[b][z] = 1
    checks = 0
    for selected_bits in product((0, 1), repeat=s):
        subset = [r + 1 + i for i, bit in enumerate(selected_bits) if bit]
        if prod([residues_all[i] for i in subset]) % 8 != 1:
            continue
        if any(sum(off[i][q] for q in subset) & 1 for i in range(r)):
            continue
        inds = list(range(r + 1)) + list(range(t0, t)) + subset
        relabel = {v: i for i, v in enumerate(inds)}
        rs = [residues_all[i] for i in inds]
        of = [[off[i][q] for q in inds] for i in inds]
        first = [(relabel[t0 + i], i + 1) for i in range(r - 1)]
        descent_test(rs, of, range(r), first)
        genus_sum(rs, of)
        checks += 1
    return checks


def algebra_checks():
    c, s, t, r = sp.symbols('c s t r')
    A, B, C, D = s*s-c, s*s+c, t*t-c, t*t+c
    degree7 = B*C-(1-c)*r*r*A*D
    z = (1-c)*r*A*D
    degree9_residual = (1-c)*A*B*C*D-z*z
    assert sp.expand(degree9_residual-(1-c)*A*D*degree7) == 0
    P = sp.Poly(degree7, c, s, t, r)
    assert P.total_degree() == 7 and max(map(abs, P.coeffs())) == 1
    # Published BB example and its degree-seven coordinate.
    cv, sv, tv = Fraction(112,225), Fraction(28,15), Fraction(644,825)
    rad = (1-cv)*(sv**4-cv**2)*(tv**4-cv**2)
    zv = Fraction(isqrt(rad.numerator),isqrt(rad.denominator))
    assert zv*zv == rad
    rv = zv/((1-cv)*(sv*sv-cv)*(tv*tv+cv))
    assert (sv*sv+cv)*(tv*tv-cv) == (1-cv)*rv*rv*(sv*sv-cv)*(tv*tv+cv)
    d, k, V, S, Y = sp.symbols('d k V S Y')
    e = d*k*k
    scaled_BB = (1-e)*((k*V)**4-e*e)*((k*S)**4-e*e)-(k**4*Y)**2
    normalized = (1-e)*(V**4-d*d)*(S**4-d*d)-Y*Y
    assert sp.expand(scaled_BB-k**8*normalized) == 0
    j, rr, hh, kk = sp.symbols('j rr hh kk')
    dd = j*rr**2
    # Substitute the complement 1-d=kk*hh² before comparing.
    native = dd*(dd+(rr*V)**2)**2*(hh*S)**4-dd*(dd-(rr*V)**2)**2*(kk*hh**2)**2
    shared = rr**6*hh**4*j*((j+V*V)**2*S**4-kk*kk*(j-V*V)**2)
    assert sp.expand(native-shared) == 0
    assert sp.expand((j*(j+V*V)**2-j*(j-V*V)**2)-(2*j*V)**2) == 0
    base, alpha, beta, complement = sp.symbols('base alpha beta complement')
    di = alpha**2*base
    # Uniform sharing uses only existing inputs and finite square roots:
    # d_i=alpha²*d_1 and 1-d_i=beta²*(1-d_a).
    uniform_native = di*(di+(alpha*V)**2)**2*(beta*S)**4-di*(di-(alpha*V)**2)**2*(beta**2*complement)**2
    representative = base*(base+V*V)**2*S**4-base*(base-V*V)**2*complement**2
    assert sp.expand(uniform_native-alpha**6*beta**4*representative) == 0
    trivial = d*(d+V*V)**2*(1-d)**2-d*(d-V*V)**2*(1-d)**2
    assert sp.expand(trivial-(2*d*V*(1-d))**2) == 0
    return {'degree':7,'coefficient_height':1,'monomials':len(P.terms()),'example':{'c':str(cv),'s':str(sv),'t':str(tv),'r':str(rv),'z':str(zv)},'normalized_BB_identity':True,'native_parameter_sharing_identity':True,'uniform_sharing_finite_choice_identity':True,'trivial_complement_terminal_identity':True}



def independent_class_numbers():
    records = []
    primes = [3,7,113,137]
    for mask in range(1,1 << len(primes)):
        ps = [p for i,p in enumerate(primes) if mask >> i & 1]
        h0 = prod(ps)
        if h0 % 8 not in (1,3,7):
            continue
        disc = -h0 if h0 % 4 == 3 else -4*h0
        hclass = 0
        for a in range(1,isqrt(abs(disc)//3)+1):
            for b in range(-a,a+1):
                top = b*b-disc
                if top % (4*a):
                    continue
                c = top//(4*a)
                if c < a or gcd(gcd(a,b),c) != 1:
                    continue
                if (abs(b) == a or a == c) and b < 0:
                    continue
                hclass += 1
        rank2class = len(ps)-1+int(h0%4 == 1)
        assert hclass % (1 << rank2class) == 0
        gamma_exact = (hclass//(1 << rank2class)) & 1
        A = build_matrix([p%8 for p in ps],[[0 if i==q else lbit(ps[q],ps[i]) for q in range(len(ps))] for i in range(len(ps))])
        if h0 % 8 in (3,7):
            gamma_matrix = det2([row[1:] for row in A[1:]])
        else:
            gamma_matrix = det2([row[1:]+[residue_bits(ps[i]%8)[1]] for i,row in enumerate(A)])
        assert gamma_exact == gamma_matrix
        records.append({'h0':h0,'discriminant':disc,'class_number':hclass,'gamma':gamma_exact})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report')
    args = parser.parse_args()
    concrete = [actual_primes([7], [113,137,193]), actual_primes([3,5,17], [409])]
    rng = random.Random(261116130)
    random_count = 0
    for r, s, repeats in [(1,0,2),(1,1,20),(1,2,30),(1,3,30),(2,1,30),(2,2,30),(3,0,20),(3,1,20),(3,2,10)]:
        for _ in range(repeats):
            random_count += random_graph(rng,r,s)
    report = {'status':'passed','scope':'Exact finite descent/genus identities and polynomial identities; infinite rank conclusions rely on the written proof and TYZ.', 'algebra':algebra_checks(),'independent_class_number_checks':independent_class_numbers(),'concrete_families':concrete,'deterministic_formal_graph_fibres_checked':random_count}
    out = json.dumps(report, indent=2)
    if args.report:
        with open(args.report,'w') as f:
            f.write(out+'\n')
    print(out)

if __name__ == '__main__':
    main()
