#!/usr/bin/env python3
"""Exact finite certificates of the unshifted contact exclusions.

No producer is imported.  The indexed checks use the complete coefficient
DAG and literal product ancestry.  The quartic checks use their unoptimized
quadratic rows, recording forced gate values until an equation becomes -1=0.
The already supplied row-operation certificates transport this contradiction
to the final quadratic systems.  This does not claim a contradiction for
their sum-of-squares polynomial over a field containing i.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTACTS = (2399, -1, -2)
INDEXED = (
    "research/phase3/finite_fibre/polynomial-41/polynomial-specification.json",
    "research/phase3/finite_fibre/polynomial-43-semilocal/polynomial-specification.json",
    "research/phase2/finite_fibre/polynomial-43-conic/polynomial-specification.json",
    "research/phase2/finite_fibre/polynomial-45-conic-semilocal/polynomial-specification.json",
)
QUARTICS = (
    "research/phase3/quartic/quartic-direct/polynomial.json.gz",
    "research/phase3/quartic/quartic-direct-small-coefficients/polynomial.json.gz",
    "research/phase2/quartic/quartic-best/polynomial.json.gz",
    "research/phase2/quartic/quartic-small-coefficients/polynomial.json.gz",
)


def read(path):
    b = (ROOT / path).read_bytes()
    if path.endswith('.gz'):
        b = gzip.decompress(b)
    return json.loads(b), sha256(b).hexdigest()


def indexed(path):
    s, digest = read(path)
    dag = s['coefficient_dag']
    support, degree, bits = [], [], []
    for n in dag:
        op = n[0]
        if op == 'int':
            su, de, bi = frozenset(), 0, max(1, abs(n[1]).bit_length())
        elif op in ('variable', 'algebra_generator', 'parameter'):
            su, de, bi = frozenset(((op, n[1]),)), 1, 1
        elif op == 'pow':
            su, de, bi = support[n[1]], degree[n[1]] * n[2], bits[n[1]] * n[2]
        else:
            assert op in ('add', 'mul', 'neg'), op
            su = frozenset().union(*(support[j] for j in n[1:]))
            if op == 'add':
                de = max(degree[j] for j in n[1:])
                bi = max(bits[j] for j in n[1:]) + max(1, len(n[1:]).bit_length())
            else:
                de = sum(degree[j] for j in n[1:])
                bi = sum(bits[j] for j in n[1:])
        support.append(su); degree.append(de); bits.append(bi)

    @lru_cache(None)
    def product_path(parent, child):
        if parent == child:
            return (parent,)
        n = dag[parent]
        if n[0] == 'mul':
            children = n[1:]
        elif n[0] == 'pow' and n[2] > 0:
            children = (n[1],)
        elif n[0] == 'neg':
            children = (n[1],)
        else:
            return ()
        for k in children:
            p = product_path(k, child)
            if p:
                return (parent,) + p
        return ()

    @lru_cache(None)
    def polynomial(i):
        n = dag[i]
        if n[0] == 'int': return {0: n[1]} if n[1] else {}
        if n[0] == 'variable':
            assert n[1] == 0
            return {1: 1}
        if n[0] == 'add':
            out = {}
            for j in n[1:]:
                for e, c in polynomial(j).items(): out[e] = out.get(e, 0) + c
            return {e: c for e, c in out.items() if c}
        if n[0] == 'neg': return {e: -c for e, c in polynomial(n[1]).items()}
        factors = [polynomial(j) for j in n[1:]] if n[0] == 'mul' else [polynomial(n[1])] * n[2]
        assert n[0] in ('mul', 'pow')
        out = {0: 1}
        for fac in factors:
            out2 = {}
            for e, c in out.items():
                for f, b in fac.items(): out2[e + f] = out2.get(e + f, 0) + c * b
            out = {e: c for e, c in out2.items() if c}
        return out

    candidates = []
    guard = s['materialized_guard_node']
    for cert in s['source_guard_factor_certificates']:
        i = cert['numerator']
        if support[i] <= {('variable', 0)} and degree[i] <= 10 and bits[i] <= 4096:
            ancestry = product_path(guard, i)
            if ancestry: candidates.append((i, polynomial(i), ancestry))
    results = []
    for a in CONTACTS:
        found = []
        for i, p, ancestry in candidates:
            remainder = [0, 0]
            for e, c in p.items(): remainder[e % 2] += c * a ** (e // 2)
            if remainder == [0, 0] and p:
                found.append({'factor_node': i, 'polynomial': sorted(p.items()),
                              'multiplicative_ancestry': list(ancestry)})
        assert found, (path, a, candidates)
        results.append({'input_minimal_polynomial': [ -a, 0, 1 ], 'vanishing_factors': found})
    # Every algebra branch retains all point quartics, so rank-1 is positive.
    recipe = s['finite_algebra_recipe']
    minimum_rank = 4 ** recipe['point_count']
    assert minimum_rank > 1
    assert s['polynomial_recipe']['H'] == 'det(I-V*M_{G*lambda})=sum_{k=0}^{rank} a_k V^k'
    assert s['polynomial_recipe']['Rtilde'].startswith('sum_{k=0}^{rank-1}')
    return {'path': path, 'sha256': digest, 'total_variables': s['total_external_variables'],
            'minimum_algebra_rank': minimum_rank, 'contacts': results,
            'conclusion': 'G=0; H=1; every reciprocal residual is 1; all high coefficients and reversed traces are 0; every branch factor and the full indexed polynomial equal 1.'}


def quartic(path):
    s, digest = read(path)
    derivation = s['derivation']
    gates, rows = derivation['gates'], derivation['source_rows']
    results = []
    for a in CONTACTS:
        zero, one = (F(0), F(0)), (F(1), F(0))
        def add(x, y): return x[0]+y[0], x[1]+y[1]
        def neg(x): return -x[0], -x[1]
        def mul(x, y): return x[0]*y[0]+a*x[1]*y[1], x[0]*y[1]+x[1]*y[0]
        def inv(x):
            n = x[0]*x[0]-a*x[1]*x[1]
            assert n
            return x[0]/n, -x[1]/n
        def short(x):
            return all(max(abs(v.numerator).bit_length(), v.denominator.bit_length()) <= 4096 for v in x)
        known = {0: (F(0), F(1))}
        steps = []
        def linear(terms):
            out = zero
            for i, n, d in terms:
                if i != -1 and i not in known: return None
                out = add(out, mul((F(n,d), F(0)), one if i == -1 else known[i]))
            return out
        def partial_row(row):
            assert row.get('K_constant', [0,1])[0] == 0
            out = {}
            for mon, n, d in row['terms']:
                coefficient = (F(n,d), F(0)); unknown = []
                for v in mon:
                    if v in known: coefficient = mul(coefficient, known[v])
                    else: unknown.append(v)
                key = tuple(sorted(unknown))
                out[key] = add(out.get(key, zero), coefficient)
            return {k:v for k,v in out.items() if v != zero}
        contradiction = None
        for gate in gates:
            op, output = gate['operation'], gate['variable']
            if op == 'mul':
                vals = [linear(t) for t in gate['arguments']]
                if any(v is None for v in vals): continue
                value = mul(*vals)
            elif op == 'quadratic':
                value = zero
                for mon, n, d in gate['polynomial']:
                    if any(v not in known for v in mon): value = None; break
                    t = (F(n,d), F(0))
                    for v in mon: t = mul(t, known[v])
                    value = add(value, t)
                if value is None: continue
            elif op == 'inv':
                arg = linear(gate['arguments'][0])
                if arg is None: continue
                if arg == zero:
                    p = partial_row(rows[gate['row']])
                    assert p == {(): neg(one)}, (path,a,gate,p)
                    contradiction = {'gate_variable': output, 'source_row': gate['row'],
                                     'row_after_forced_substitution': '-1',
                                     'inverse_argument': gate['arguments'][0]}
                    break
                value = inv(arg)
            else:
                continue
            if not short(value): continue
            # Validate that a literal source equation forces this gate value.
            row = rows[gate['row']]
            if row.get('K_constant', [0,1])[0]: continue
            before = partial_row(row)
            assert set(before) <= {(), (output,)} and before.get((output,),zero) != zero, (gate,before)
            known[output] = value
            assert partial_row(row) == {}, (gate,value,row)
            steps.append({'variable':output,'source_row':gate['row'],
                          'value':[str(value[0]),str(value[1])]})
        assert contradiction, (path,a)
        results.append({'input_minimal_polynomial':[-a,0,1],
                        'forced_gate_steps':steps,'contradiction':contradiction})
    return {'path':path,'sha256':digest,'total_variables':len(s['variables']),
            'contacts':results,
            'scope':'Contradiction for the raw quadratic system. Certified reversible row operations transfer it to the final residual system. It is not a contradiction for the literal sum of squares over nonreal fields.'}


def main():
    result = {'status':'PASS','arithmetic':'Exact integer and Fraction arithmetic; no numerical roots.',
              'indexed':[indexed(p) for p in INDEXED],
              'quadratic_systems':[quartic(p) for p in QUARTICS],
              'scope':'Unshifted beta=X^2+2 artifacts only; no claim is made about beta-shift2402 artifacts.'}
    result['checker_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    dest = HERE/'contact-exclusions-verification_20261106_v1.json'
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','indexed_polynomials':len(result['indexed']),
                      'quadratic_systems':len(result['quadratic_systems']),
                      'contacts_each':len(CONTACTS),'receipt':str(dest.relative_to(ROOT))}))


if __name__ == '__main__': main()
