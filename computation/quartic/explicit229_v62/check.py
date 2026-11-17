#!/usr/bin/env python3
"""Independent exact verification of the center-3/11 229-coordinate quartic.

This script deliberately does not import the producer.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb, gcd
from pathlib import Path
import json

R = Path(__file__).resolve().parent
SOURCE_DIGEST = '304f94843c1a4ac94fcd5f1295fee8b532e7f0424e638314d892c556e2fbfdf9'
K = 9063965991649194484576286065455625302


def read(name):
    return json.loads((R / name).read_bytes())


def parse(terms):
    result = defaultdict(F)
    for t in terms:
        result[(int(t['parameterPower']), tuple(sorted(t['monomial']))) ] += F(t['coefficient'])
    return {key: c for key, c in result.items() if c}


def add(*polys):
    out = defaultdict(F)
    for p in polys:
        for key, c in p.items():
            out[key] += c
    return {key: c for key, c in out.items() if c}


def scale(p, c):
    return {key: c * a for key, a in p.items() if c * a}


def times(a, b):
    out = defaultdict(F)
    for (u, m), c in a.items():
        for (v, n), d in b.items():
            out[(u + v, tuple(sorted(m + n)))] += c * d
    return {key: c for key, c in out.items() if c}


def variable(i, power=0):
    return {(power, (i,)): F(1)}


def kplus(a, b):
    return add(a[0], b[0]), add(a[1], b[1])


def ktimes(a, b):
    return (add(times(a[0], b[0]), scale(times(a[1], b[1]), 2)),
            add(times(a[0], b[1]), times(a[1], b[0])))


def shifted(coefficients, base):
    return [sum(c * comb(a, j) * base ** (a - j)
                for a, c in coefficients.items() if a >= j)
            for j in range(max(coefficients, default=0) + 1)]


def univariate_multiply(a, b):
    result = defaultdict(F)
    for i, c in a.items():
        for j, d in b.items():
            result[i+j] += c*d
    return {i: c for i, c in result.items() if c}


def check_contacts(new):
    theta = [F(0), F(-1,2), F(-1), F(1,2399), F(-32,407)]
    center = F(3,11)
    alpha = [(22*t-3)**2 for t in theta]
    P = {0:F(1)}
    F_contact = {0:F(1)}
    for t, aa in zip(theta, alpha):
        P = univariate_multiply(P, {1:F(1), 0:-aa})
        F_contact = univariate_multiply(F_contact, {1:F(1), 0:-t})
        F_contact = univariate_multiply(F_contact, {1:F(1), 0:t-center})
    e = [(-1)**j * P.get(5-j,0) for j in range(6)]
    L = 7878870169
    assert [int(L*x) for x in e] == [7878870169,6786192246520,
        1229741066709366,42042541279847500,476802068222265625,1738195040039062500]
    r_t = {2:F(484),1:F(-132),0:F(9)}
    composition = defaultdict(F)
    power = {0:F(1)}
    for j in range(6):
        for k,c in power.items():composition[k] += P[j]*c
        power = univariate_multiply(power,r_t)
    assert {k:c for k,c in composition.items() if c} == {k:22**10*c for k,c in F_contact.items()}
    # Directly substitute physical t,r,s,v,w in all twelve target rows.
    # The keys below are (power of C, power of q, formal monomial).
    by_name={row['name']:row for row in new['residuals']}
    for j,(ti,ri,si,vi,wi) in enumerate([(2,74,75,76,None),
            (86,87,88,89,91),(200,201,202,203,205)]):
        substitutions={77:(0,1,(),F(1)),ti:(0,1,('t',),F(1)),
            ri:(0,1,('r',),F(1)),si:(0,1,('s',),F(1)),
            vi:(-1 if j==0 else 0,1,('v',),F(L))}
        if wi is not None:substitutions[wi]=(0,1,('w',),F(1))
        def substituted(suffix):
            out=defaultdict(F)
            for term in by_name[f'additive.detector{j}.{suffix}']['terms']:
                cp=term['parameterPower']; qp=-2; mon=(); coefficient=F(term['coefficient'])
                for i in term['monomial']:
                    c,q,m,k=substitutions[i];cp+=c;qp+=q;mon+=m;coefficient*=k
                out[cp,qp,tuple(sorted(mon))]+=coefficient
            return {key:c for key,c in out.items() if c}
        def expected(terms):
            out=defaultdict(F)
            for mon,c in terms.items():
                qp=0
                if j==0:
                    qp=-mon.count('w');mon=tuple(x for x in mon if x!='w')
                out[0,qp,tuple(sorted(mon))]+=c
            return {key:c for key,c in out.items() if c}
        assert substituted('contactSquare') == expected({('t','t'):F(484),('t',):F(-132),():F(9),('r',):F(-1)})
        assert substituted('contactFourthPower') == expected({('r','r'):F(1 if j==0 else -1),('s',):F(-1 if j==0 else 1)})
        combination={('r','s'):F(L),('s',):-L*e[1],('s','w'):-L*e[1],
            ('r',):L*e[2],('r','w'):L*e[2],('v',):F(-L)}
        relation={('s','v'):F(L),('s',):-L*e[3],('s','w'):-L*e[3],
            ('r',):L*e[4],('r','w'):L*e[4],():-L*e[5],('w',):-L*e[5]}
        assert substituted('contactCombination') == expected(combination)
        sign=1 if j==0 else -1
        assert substituted('contactRelation') == expected({key:sign*c for key,c in relation.items()})
    assert len(set(theta+[center-t for t in theta])) == 10
    assert max(theta+[center-t for t in theta])-min(theta+[center-t for t in theta]) == F(25,11)
    assert all(F(3,22)!=t for t in theta+[center-t for t in theta])


def main():
    assert sha256((R / 'source/quadratic195.json').read_bytes()).hexdigest() == SOURCE_DIGEST
    old, new, certificate = read('source/quadratic195.json'), read('quadratic.json'), read('graft.json')
    assert old['variables'] == 195 and new['variables'] == 229
    assert len(old['residuals']) == 175 and len(new['residuals']) == 207
    assert new['inputCoordinate'] == old['inputCoordinate'] == 1
    assert new['coordinates'][:195] == old['coordinates']
    clone = {c['clonedFrom195Id']: c['id'] for c in new['coordinates'][195:]}
    expected_local = {c['id'] for c in old['coordinates']
                      if 'detector1' in c['name'] or 'det1' in c['name']}
    assert set(clone) == expected_local and len(clone) == 34
    assert clone == {int(k): v for k, v in certificate['cloned_coordinate_map'].items()}
    # The old block's local coordinates have no outside consumers except t1.
    outside_uses = defaultdict(set)
    for row in old['residuals']:
        local_row = 'detector1' in row['name'] or 'det1' in row['name']
        if not local_row:
            for term in row['terms']:
                for i in set(term['monomial']) & expected_local:
                    outside_uses[i].add(row['name'])
    assert dict(outside_uses) == {86: {'inverse_vieta.unweighted.aggregate'}}

    changed_contacts={22,24,25,34,36,37}
    for a, b in zip(old['residuals'][:174], new['residuals'][:174]):
        if a['id'] not in changed_contacts:assert a == b
    old_aggregate = parse(old['residuals'][174]['terms'])
    first_aggregate = parse(new['residuals'][174]['terms'])
    assert first_aggregate == add(old_aggregate, {(0, (77, 77)): F(12)})
    clones = new['residuals'][175:206]
    original_rows = [r for r in old['residuals']
                     if 'detector1' in r['name'] or 'det1' in r['name']]
    assert len(clones) == len(original_rows) == 31
    for a, b in zip(original_rows, clones):
        # The newly chosen contact equations are shared by all three detectors.
        a = new['residuals'][a['id']-1]
        expected = {(p, tuple(sorted(clone.get(i, i) for i in m))): c
                    for (p, m), c in parse(a['terms']).items()}
        assert parse(b['terms']) == expected
        assert b['clonedFrom195Row'] == a['id']
        assert b['name'] == a['name'].replace('detector1', 'detector2').replace('det1', 'det2')
    check_contacts(new)

    # Recover both components independently by multiplication in Q[rho]/(rho^2-2).
    q = variable(77)
    D = ({(0, ()): F(11)}, {(0, ()): F(-6)})
    recovered = (times(q, variable(192)), times(q, variable(193)))
    for ids, cp in [((152, 153, 156, 157, 160, 161), 0),
                    ((162, 163, 166, 167, 170, 171), 1),
                    ((172, 173, 176, 177, 180, 181), 1)]:
        f0, f1, g0, g1, s0, s1 = ids
        fg = (add(variable(f0, cp), variable(g0)),
              add(variable(f1, cp), variable(g1)))
        linear = ktimes(D, fg)
        linear = times(q, linear[0]), times(q, linear[1])
        secant = variable(s0), variable(s1)
        recovered = kplus(recovered, kplus(ktimes(secant, secant), linear))
    assert recovered == tuple(parse(t) for t in certificate['sum_components_numerators'])
    t0, t1, t2 = variable(2), variable(86), variable(clone[86])
    assert old_aggregate == add(recovered[0], scale(times(q, q), 14),
                                scale(times(q, add(t0, scale(t1, -1))), 2))
    expected_second = add(recovered[1], scale(times(q, q), -8),
        scale(times(q, add(t0, scale(t1, -2), t2)), 2))
    second_aggregate = parse(new['residuals'][206]['terms'])
    assert second_aggregate == expected_second
    # Combining the rows recovers the stated independent shift identities.
    expected_v2 = add(recovered[0], scale(recovered[1], -1),
                     scale(times(q, q), 34), scale(times(q, add(t1, scale(t2, -1))), 2))
    assert add(first_aggregate, scale(second_aggregate, -1)) == expected_v2
    guards = []
    for a, b in [(77, 78), (90, 91), (clone[90], clone[91])]:
        wanted = {(0, ()): F(1), (0, tuple(sorted((a, b)))): F(-1)}
        matches = [r['id'] for r in new['residuals'] if parse(r['terms']) == wanted]
        assert len(matches) == 1
        guards += matches

    expanded = defaultdict(F)
    for row in new['residuals']:
        p = parse(row['terms'])
        assert all(len(m) <= 2 and c.denominator == 1 and a in (0, 1)
                   for (a, m), c in p.items())
        terms = list(p.items())
        for i, j in combinations_with_replacement(range(len(terms)), 2):
            (a, m), c = terms[i]
            (b, n), d = terms[j]
            expanded[(a + b, tuple(sorted(m + n)))] += c * d * (1 if i == j else 2)
    expanded = {key: int(c) for key, c in expanded.items() if c}
    assert expanded == parse(read('polynomial.json')['terms'])
    assert len(expanded) == 3322
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert len(profiles) == 3312
    assert {i for a, m in expanded for i in m} == set(range(1, 230))
    assert max(len(m) for a, m in expanded) == 4
    assert expanded[(0, (1, 1, 1, 1))] == 1
    assert gcd(*expanded.values()) == 1
    for p in profiles.values():
        sign = 1 if p[max(p)] > 0 else -1
        coefficients = shifted({a: sign * c for a, c in p.items()}, 149)
        assert coefficients[0] > 0 and all(c >= 0 for c in coefficients)
    assert {0: K} in profiles.values() or {0: -K} in profiles.values()
    assert {2: 22201} in profiles.values()
    for n in range(1, 8):
        c = 149 ** n
        assert max(abs(sum(v * c ** a for a, v in p.items())) for p in profiles.values()) == K
    for p in profiles.values():
        for sign in (-1, 1):
            difference = defaultdict(int, {2: 22201})
            for a, c in p.items():
                difference[a] += sign * c
            assert all(c >= 0 for c in shifted(difference, 149 ** 8))

    report = dict(status='PASS', scope='Finite algebra and coefficient certificate; arithmetic threshold separately required.',
        source_sha256=SOURCE_DIGEST, variables=229, rows=207,
        unchanged_parent_rows=168, changed_parent_rows=[22,24,25,34,36,37,175],
        cloned_coordinates=34, cloned_rows=31, additional_aggregate_rows=1,
        literal_unit_guards=guards, all_recovery_coordinates_counted=True,
        degree=4, content=1, coordinate_monomials=3312, parameter_terms=3322,
        coefficient_height=f'max({K},149^(2*N+2))', coefficient_crossover_N=8,
        reflection_center='3/11', midpoint='3/22',
        contact_coefficients_reconstructed=True, contact_width='25/11',
        all_twelve_contact_rows_verified=True, fixed_N=15,
        fixed_coefficient_height='149^32',fixed_coefficient_bits=(149**32).bit_length(),
        support_uniform='Every C>=149', no_new_coordinate_for_component1=True,
        input_fixed=True, all_coordinates_used=True,
        output_sha256={name: sha256((R/name).read_bytes()).hexdigest()
                       for name in ['quadratic.json', 'polynomial.json', 'graft.json']})
    (R/'certificate.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
