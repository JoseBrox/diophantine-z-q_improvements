#!/usr/bin/env python3
"""Independent exact audit of the 456-variable quartic.

This checker imports no producer. It works in named coordinates, reconstructs
every unchanged source equation from the valid 474-coordinate data, checks
the new power and pole templates, and expands every coefficient independently.
"""
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
from math import gcd, lcm
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def poly(ts, names):
    result = defaultdict(Q)
    for t in ts:
        result[(t.get('sPower', 0), tuple(sorted(names[i] for i in t['monomial'])))] += Q(t['coefficient'])
    return {m: a for m, a in result.items() if a}


def plus(*ps):
    result = defaultdict(Q)
    for p in ps:
        for m, a in p.items(): result[m] += a
    return {m: a for m, a in result.items() if a}


def times(a, b):
    result = defaultdict(Q)
    for (s, m), x in a.items():
        for (t, n), y in b.items(): result[(s+t, tuple(sorted(m+n)))] += x*y
    return {m: x for m, x in result.items() if x}


def scalar(k, p): return {m: k*a for m, a in p.items() if k*a}
def atom(n): return {(0, (n,)): Q(1)}
def const(n): return {(0, ()): Q(n)} if n else {}
def square(p): return times(p, p)


def evaluate(p, substitutions):
    result = {}
    for (s, m), coefficient in p.items():
        term = {(s, ()): coefficient}
        for name in m: term = times(term, substitutions.get(name, atom(name)))
        result = plus(result, term)
    return result


def normalize(p):
    assert p
    den = lcm(*(v.denominator for v in p.values()))
    g = gcd(*(abs(v.numerator*(den//v.denominator)) for v in p.values()))
    f = Q(den, g)
    if p[min(p)] < 0: f = -f
    return scalar(f, p)


def same(a, b):
    # Primitive equality up to sign, independent of each coordinate ordering.
    assert a and b
    keys = set(a) | set(b)
    key = next(iter(a))
    assert key in b
    ratio = a[key]/b[key]
    assert ratio != 0 and all(a.get(k, 0) == ratio*b.get(k, 0) for k in keys)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=HERE / 'source')
    parser.add_argument('--directory', type=Path, default=HERE / 'polynomial-456')
    args = parser.parse_args()
    srcpath = args.source / 'parent474-residuals.json'
    assert sha(srcpath) == '9bd49b7542507f32e06cbc424cf223ec2b5226826b980876c7f0750edfa0e09c'
    old = json.loads(srcpath.read_text())
    semantic = json.loads((args.source / 'semantic-values.json').read_text())
    assert semantic['source_sha256'] == '96fb871cff3cf08582a55c82ffc51d118fe93ea0a524e842bf7decb4d4be39f9'
    new = json.loads((args.directory / 'residuals.json').read_text())
    oldnames = {z['id']: z['name'] for z in old['coordinates']}
    sourcenames = {z['sourceId']: z['name'] for z in old['coordinates']}
    newnames = {z['id']: z['name'] for z in new['coordinates']}
    source = {r['name']: poly(r['terms'], oldnames) for r in old['residuals']}
    target = {r['name']: poly(r['terms'], newnames) for r in new['residuals']}
    assert len(newnames) == len(set(newnames.values())) == 456
    assert len(target) == len(new['residuals']) == 426
    assert newnames[0] == 'input'
    assert new['fixedParameter'] == {'name': 'S', 'value': '3^52832906', 'coordinate': False}
    assert new['scalarOrder'] == 31

    raw = poly(semantic['values']['scalar.r']['terms'], sourcenames)
    bscalar = poly(semantic['values']['scalar.b']['terms'], sourcenames)
    rname = 'scalar.r.quadratic'
    lead = raw[(0, (rname,))]
    lower = plus(raw, scalar(-lead, atom(rname)))
    def replace_raw(name):
        return scalar(1/lead, plus(atom(name), scalar(-1, lower)))
    rawmap = {rname: replace_raw('scalar.normalizedR')}
    substitutions = {f'correction.partial.{i}': const(1) for i in (3, 5, 7, 11, 13, 17, 'sign')}
    corrected = evaluate(evaluate(source['scalar.correctedR.definition'], rawmap), substitutions)
    cname = 'scalar.correctedR.quadratic'
    ca = corrected[(0, (cname,))]
    replacement = plus(scalar(-1/ca, corrected), atom(cname))
    assert all(s == 0 and len(m) <= 1 for s, m in replacement)
    substitutions[cname] = replacement
    substitutions['scalar.UplusB'] = scalar(2, bscalar)
    aliases = {'inputSquarePlus1200': atom('inputBetaMinus3Over2')}
    power_stems = ['scalar.rInverse32.' + n for n in
                   ('half.half.half.half.square', 'half.half.half.square',
                    'half.half.square', 'half.square', 'square')]
    for stem, exponent in zip(power_stems[:3] + power_stems[4:], (3, 7, 15, 31)):
        aliases[stem + '.quadratic'] = atom(f'scalar.inversePower{exponent}')
    ignored = {'shiftedInputSquare.definition', 'scalar.correctedR.definition',
               'scalar.t2.definition', 'scalar.preparationT.definition', 'scalar.UplusB.definition'}
    ignored.update(f'correction.partialProduct{i}' for i in range(1, 8))
    ignored.update(n + '.definition' for n in power_stems)
    old_pole_suffixes = ('p2.definition', 'firstConic', 'U2.definition', 'Bh.definition',
                         's2.definition', 'q2.definition', 'secondConic')
    for prefix in ('detector0', 'detector1', 'detector2', 'scalar'):
        ignored.update(prefix + '.' + suffix for suffix in old_pole_suffixes)
    checked = set()
    for name, p in source.items():
        if name in ignored: continue
        local_raw = {rname: replace_raw('scalar.rawR')} if name == 'scalar.r.definition' else rawmap
        expected = evaluate(evaluate(evaluate(p, local_raw), substitutions), aliases)
        same(target[name], expected)
        checked.add(name)

    z = atom('inputFourthPower.X2'); y = atom('inputBetaMinus3Over2'); x = atom('input')
    templates = {
        'inputFourthPower.beta.definition': plus(scalar(108, square(z)), const(225228), scalar(-1, y)),
        'inputFourthPower.X2.definition': plus(square(x), scalar(-1, z)),
        'scalar.normalizerDelta.definition': plus(atom('scalar.normalizerDelta'), const(-1), scalar(-289, square(atom('scalar.rawR')))),
        'scalar.normalization.definition': plus(scalar(10404, times(atom('scalar.rawR'), atom('scalar.rInverse'))), scalar(-1, square(atom('scalar.normalizerDelta')))),
    }
    last = atom('scalar.rInverse')
    exponents = [-1]
    for n in (3, 7, 15, 31):
        current = atom(f'scalar.inversePower{n}')
        templates[f'scalar.inversePower{n}.definition'] = plus(times(atom('scalar.normalizedR'), current), scalar(-1, square(last)))
        exponents.append(2*exponents[-1]-1)
        assert exponents[-1] == -n
        last = current
    assert exponents == [-1, -3, -7, -15, -31]
    assert 1 + 2*exponents[-1] == -61

    for prefix in ('detector0', 'detector1', 'detector2', 'scalar'):
        b = bscalar if prefix == 'scalar' else atom(prefix + '.B')
        u, p, vv, w = [atom(prefix + '.' + n) for n in ('eOverB', 'p', 'sOverB', 'qOverB')]
        h, v2, ff = [atom(prefix + '.' + n) for n in
                     ('normalizedH', 'sRatioSquared', 'secondProduct')]
        templates[prefix + '.firstConic'] = plus(scalar(17, square(p)), scalar(-289, b),
                times(plus(scalar(3, u), const(-34)), plus(scalar(17, u), scalar(-1, h))))
        templates[prefix + '.normalizedH.definition'] = plus(h, scalar(-1, times(u, plus(const(17), scalar(-1, b)))))
        templates[prefix + '.sRatioSquared.definition'] = plus(v2, scalar(-1, square(vv)))
        templates[prefix + '.secondProduct.definition'] = plus(ff, scalar(-1, times(plus(v2, scalar(-1, h)), plus(v2, scalar(3, h)))))
        templates[prefix + '.secondConic'] = plus(scalar(17, square(w)), scalar(-1, times(b, ff)))

        # Check the precise old scaled chart, including its gate normalizations.
        eo, so, po, qo = [atom(prefix + '.' + n) for n in ('scaled_e', 's', 'p', 'q')]
        gates = {prefix + '.p2.quadratic': square(po),
                 prefix + '.U2.quadratic': square(b if prefix != 'scalar' else atom('scalar.b.quadratic')),
                 prefix + '.s2.quadratic': square(so),
                 prefix + '.q2.quadratic': square(qo)}
        for label, oldvar in [('p2.definition', prefix + '.p2.quadratic'),
                              ('U2.definition', prefix + '.U2.quadratic'),
                              ('s2.definition', prefix + '.s2.quadratic'),
                              ('q2.definition', prefix + '.q2.quadratic')]:
            original = evaluate(source[prefix + '.' + label], substitutions)
            same(original, plus(atom(oldvar), scalar(-1, gates[oldvar])))
        first = evaluate(source[prefix + '.firstConic'], gates)
        same(first, plus(scalar(17, times(b, square(po))), scalar(-1, times(plus(scalar(17, b), scalar(-1, eo)), plus(scalar(17, b), scalar(3, eo))))))
        bhname = prefix + '.Bh.quadratic'
        bhrow = evaluate(evaluate(source[prefix + '.Bh.definition'], substitutions), gates)
        coefficient = bhrow[(0, (bhname,))]
        old_bh = plus(scalar(-1/coefficient, bhrow), atom(bhname))
        gates[bhname] = old_bh
        second = evaluate(source[prefix + '.secondConic'], gates)
        H = times(eo, plus(scalar(17, b), scalar(-1, square(b))))
        same(second, plus(scalar(17, times(b, square(qo))), scalar(-1, times(plus(square(so), scalar(-1, H)), plus(square(so), scalar(3, H))))))

        # Verify the two birational rescaling identities as polynomial identities.
        first_expected = plus(scalar(17, square(p)), scalar(-1, times(b, times(plus(const(17), scalar(-1, u)), plus(const(17), scalar(3, u))))))
        assert plus(first_expected, scalar(-1, templates[prefix + '.firstConic'])) == times(
            plus(scalar(3, u), const(-34)), templates[prefix + '.normalizedH.definition'])
        hvalue = times(u, plus(const(17), scalar(-1, b)))
        Fvalue = times(plus(square(vv), scalar(-1, hvalue)), plus(square(vv), scalar(3, hvalue)))
        second_expected = plus(scalar(17, square(w)), scalar(-1, times(b, Fvalue)))
        substitution = {prefix + '.scaled_e': times(b, u), prefix + '.s': times(b, vv), prefix + '.q': times(b, w)}
        transformed_first = evaluate(plus(scalar(17, times(b, square(po))), scalar(-1, times(plus(scalar(17, b), scalar(-1, eo)), plus(scalar(17, b), scalar(3, eo))))), substitution)
        transformed_second = evaluate(plus(scalar(17, times(b, square(qo))), scalar(-1, times(plus(square(so), scalar(-1, H)), plus(square(so), scalar(3, H))))), substitution)
        assert transformed_first == times(b, first_expected)
        assert transformed_second == times(times(square(b), b), second_expected)

    for name, expected in templates.items():
        same(target[name], expected); checked.add(name)
    assert checked == set(target)
    assert set().union(*(set(m) for p in target.values() for s, m in p)) == set(newnames.values())
    assert max(len(m) for p in target.values() for s, m in p) == 2

    table = defaultdict(int)
    for row in new['residuals']:
        terms = row['terms']
        coefficients = [Q(t['coefficient']) for t in terms]
        assert all(a.denominator == 1 for a in coefficients)
        assert gcd(*(abs(a.numerator) for a in coefficients)) == 1
        for i, a in enumerate(terms):
            for j, b in enumerate(terms):
                key = (a['sPower'] + b['sPower'], tuple(sorted(a['monomial'] + b['monomial'])))
                table[key] += coefficients[i].numerator*coefficients[j].numerator
    table = {k: a for k, a in table.items() if a}
    saved = json.loads((args.directory / 'polynomial.json').read_text())
    recorded = {(t['sPower'], tuple(t['monomial'])): int(t['coefficient']) for t in saved['terms']}
    assert recorded == table
    assert table[(0, (0, 0, 0, 0))] == 1
    assert max(len(m) for s, m in table) == 4
    grouped = defaultdict(dict)
    for (s, m), a in table.items(): grouped[m][s] = a
    anchor = next(i for i, name in newnames.items() if name == 'anchor.U')
    assert grouped[(anchor, anchor)] == {2: 64}
    others = [p for m, p in grouped.items() if m != (anchor, anchor)]
    s2 = max(abs(p.get(2, 0)) for p in others)
    lower = max(abs(p.get(0, 0)) + abs(p.get(1, 0)) for p in others)
    assert s2 == 8 and lower.bit_length() == 767
    assert len(grouped) == 27784 and len(table) == 27791
    report = {'status': 'PASS', 'totalVariables': 456, 'quadraticResiduals': 426,
              'degree': 4, 'ordinaryMonomials': len(grouped), 'coefficientParameterTerms': len(table),
              'coefficientContent': 1, 'exactCoefficientHeight': '64*3^105665812',
              'scalarOrder': 31, 'inversePowerExponents': exponents,
              'weightedSquareDenominatorExponent': -61,
              'sourceRowsChecked': len(source), 'finalRowsChecked': len(checked),
              'fourPoleRescalingsChecked': True, 'everyCoefficientChecked': True,
              'producerImported': False,
              'scope': 'Exact algebraic and coefficient certificate; arithmetic input-projection hypotheses remain separate.',
              'sha256': {name: sha(args.directory / name) for name in
                         ('residuals.json', 'polynomial.json', 'transformation-certificate.json')}}
    (args.directory / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__': main()
