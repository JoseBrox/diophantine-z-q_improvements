#!/usr/bin/env python3
"""Build the 456-coordinate quadratic system directly from the valid 474 source.

All data are exact rational polynomials. The scalar order is 31; the four
pole charts are rescaled by their existing, nonzero pole inputs. The source
arithmetic hypotheses are stated in the accompanying mathematical paper.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from math import gcd, lcm
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
FIXED = {'name': 'S', 'value': '3^52832906', 'coordinate': False}
PARENT_SHA = '9bd49b7542507f32e06cbc424cf223ec2b5226826b980876c7f0750edfa0e09c'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(terms):
    p = defaultdict(F)
    for t in terms:
        p[(t.get('sPower', 0), tuple(sorted(t['monomial'])))] += F(t['coefficient'])
    return {k: a for k, a in p.items() if a}


def encode(p):
    return [{'sPower': s, 'monomial': list(m), 'coefficient': str(a)}
            for (s, m), a in sorted(p.items()) if a]


def add(*parts):
    p = defaultdict(F)
    for q in parts:
        for k, a in q.items():
            p[k] += a
    return {k: a for k, a in p.items() if a}


def scale(p, a):
    return {k: v*a for k, v in p.items() if v*a}


def mul(p, q):
    r = defaultdict(F)
    for (s, m), a in p.items():
        for (t, n), b in q.items():
            r[(s+t, tuple(sorted(m+n)))] += a*b
    return {k: a for k, a in r.items() if a}


def v(i):
    return {(0, (i,)): F(1)}


def c(a):
    return {(0, ()): F(a)} if a else {}


def sub(p, i, q):
    r = {}
    for (s, m), a in p.items():
        term = {(s, tuple(j for j in m if j != i)): a}
        for _ in range(m.count(i)):
            term = mul(term, q)
        r = add(r, term)
    return r


def ids(p):
    return {i for s, m in p for i in m}


def primitive(p):
    den = lcm(*(a.denominator for a in p.values()))
    common = gcd(*(abs(a.numerator*(den//a.denominator)) for a in p.values()))
    multiplier = F(den, common)
    if p[min(p)] < 0:
        multiplier = -multiplier
    return scale(p, multiplier)


def write(path, value):
    path.write_text(json.dumps(value, separators=(',', ':')) + '\n')


def construct(parent, semantic):
    coordinates = {z['id']: dict(z) for z in parent['coordinates']}
    rows = {z['id']: read(z['terms']) for z in parent['residuals']}
    labels = {z['id']: z['name'] for z in parent['residuals']}
    byname = {z['name']: z['id'] for z in parent['coordinates']}
    byrow = {z['name']: z['id'] for z in parent['residuals']}
    source_map = {z['sourceId']: z['id'] for z in parent['coordinates']}
    def source_value(name):
        return {(s, tuple(sorted(source_map[i] for i in m))): a
                for (s, m), a in read(semantic['values'][name]['terms']).items()}
    raw_r, pole_b = source_value('scalar.r'), source_value('scalar.b')

    # Change the old raw-contact gate to the actual contact value.
    raw, inv = byname['scalar.r.quadratic'], byname['scalar.rInverse']
    raw_row = byrow['scalar.r.definition']
    leading = raw_r[(0, (raw,))]
    lower = add(raw_r, scale(v(raw), -leading))
    raw_replacement = scale(add(v(raw), scale(lower, -1)), 1/leading)
    assert sub(raw_r, raw, raw_replacement) == v(raw)
    rows = {i: sub(p, raw, raw_replacement) for i, p in rows.items()}
    coordinates[raw]['name'] = 'scalar.rawR'
    delta, normalized, input_square = 474, 475, 476
    for i, name in [(delta, 'scalar.normalizerDelta'),
                    (normalized, 'scalar.normalizedR'),
                    (input_square, 'inputFourthPower.X2')]:
        coordinates[i] = {'id': i, 'sourceId': None, 'name': name, 'kind': 'gate'}
    rows = {i: p if i == raw_row else sub(p, raw, v(normalized))
            for i, p in rows.items()}

    # Normalize the contact with an integral fixed numerator.
    rows[443] = add(v(delta), c(-1), scale(mul(v(raw), v(raw)), -289))
    rows[444] = add(scale(mul(v(raw), v(inv)), 10404), scale(mul(v(delta), v(delta)), -1))
    labels[443], labels[444] = 'scalar.normalizerDelta.definition', 'scalar.normalization.definition'

    # The fourth-power input needs no scalar squareclass choices.
    corrections = [byname[f'correction.partial.{n}'] for n in (3, 5, 7, 11, 13, 17, 'sign')]
    correction_rows = [byrow[f'correction.partialProduct{i}'] for i in range(1, 8)]
    for i in corrections:
        rows = {j: sub(p, i, c(1)) for j, p in rows.items()}
        del coordinates[i]
    for j in correction_rows:
        assert not rows[j]
        del rows[j]
    corrected, corrected_row = byname['scalar.correctedR.quadratic'], byrow['scalar.correctedR.definition']
    p = rows.pop(corrected_row)
    a = p[(0, (corrected,))]
    assert a and all(s == 0 and len(m) <= 1 for s, m in p)
    corrected_replacement = add(scale(p, -1/a), v(corrected))
    rows = {i: sub(p, corrected, corrected_replacement) for i, p in rows.items()}
    del coordinates[corrected]

    y = byname['inputSquarePlus1200']
    rows[byrow['shiftedInputSquare.definition']] = add(scale(mul(v(input_square), v(input_square)), 108), c(225228), scale(v(y), -1))
    labels[byrow['shiftedInputSquare.definition']] = 'inputFourthPower.beta.definition'
    coordinates[y]['name'] = 'inputBetaMinus3Over2'
    rows[445] = add(mul(v(0), v(0)), scale(v(input_square), -1))
    labels[445] = 'inputFourthPower.X2.definition'

    # Prepared scalar witnesses use U=b. The affine pole input is unchanged.
    preparation_rows = [byrow['scalar.' + n] for n in
                        ('t2.definition', 'preparationT.definition', 'UplusB.definition')]
    preparation_coordinates = [byname['scalar.' + n] for n in
                               ('preparation', 't2.quadratic', 'preparationT', 'UplusB')]
    up = byname['scalar.UplusB']
    for j in preparation_rows:
        del rows[j]
    rows = {i: sub(p, up, scale(pole_b, 2)) for i, p in rows.items()}
    for i in preparation_coordinates:
        del coordinates[i]

    # Compute inverse powers 3,7,15,31 using four quadratic division steps.
    power_names = ['scalar.rInverse32.' + n for n in
                   ('half.half.half.half.square', 'half.half.half.square',
                    'half.half.square', 'half.square', 'square')]
    powers = [byname[n + '.quadratic'] for n in power_names]
    power_rows = [byrow[n + '.definition'] for n in power_names]
    retained = powers[:3] + powers[4:]
    retained_rows = power_rows[:3] + power_rows[4:]
    previous = inv
    for exponent, i, j in zip((3, 7, 15, 31), retained, retained_rows):
        rows[j] = add(mul(v(normalized), v(i)), scale(mul(v(previous), v(previous)), -1))
        coordinates[i]['name'] = f'scalar.inversePower{exponent}'
        labels[j] = f'scalar.inversePower{exponent}.definition'
        previous = i
    assert ids(rows[power_rows[3]]) <= set(powers)
    del rows[power_rows[3]]
    del coordinates[powers[3]]

    # Rescale each complete pole chart by its existing nonzero pole input.
    pole_certificates = []
    for prefix in ('detector0', 'detector1', 'detector2', 'scalar'):
        bp = pole_b if prefix == 'scalar' else v(byname[prefix + '.B'])
        assert all(s == 0 and len(m) <= 1 for s, m in bp)
        e, ss, pp, qq = [byname[prefix + '.' + n] for n in ('scaled_e', 's', 'p', 'q')]
        gates = [byname[prefix + '.' + n + '.quadratic'] for n in ('p2', 'U2', 'Bh', 's2', 'q2')]
        rr = [byrow[prefix + '.' + n] for n in
              ('p2.definition', 'firstConic', 'U2.definition', 'Bh.definition',
               's2.definition', 'q2.definition', 'secondConic')]
        e2, hh, ss2, ff, deleted = gates
        templates = [
            add(scale(mul(v(pp), v(pp)), 17), scale(bp, -289),
                mul(add(scale(v(e), 3), c(-34)), add(scale(v(e), 17), scale(v(hh), -1)))),
            add(v(hh), scale(mul(v(e), add(c(17), scale(bp, -1))), -1)),
            add(v(ss2), scale(mul(v(ss), v(ss)), -1)),
            add(v(ff), scale(mul(add(v(ss2), scale(v(hh), -1)), add(v(ss2), scale(v(hh), 3))), -1)),
            add(scale(mul(v(qq), v(qq)), 17), scale(mul(bp, v(ff)), -1)),
        ]
        new_labels = ['firstConic', 'normalizedH.definition',
                      'sRatioSquared.definition', 'secondProduct.definition', 'secondConic']
        for j, p, label in zip(rr[1:5] + rr[6:], templates, new_labels):
            rows[j] = p
            labels[j] = prefix + '.' + label
        del rows[rr[5]]
        del rows[rr[0]]
        del coordinates[deleted]
        del coordinates[e2]
        for i, name in [(e, 'eOverB'), (ss, 'sOverB'), (qq, 'qOverB'),
                        (hh, 'normalizedH'),
                        (ss2, 'sRatioSquared'), (ff, 'secondProduct')]:
            coordinates[i]['name'] = prefix + '.' + name
        pole_certificates.append({'prefix': prefix, 'poleInput': encode(bp),
                                  'oldBaseCoordinates': [e, ss, pp, qq],
                                  'retainedGateCoordinates': gates[1:4],
                                  'deletedCoordinates': [e2, deleted],
                                  'sourceRows': rr})

    index = {i: j for j, i in enumerate(sorted(coordinates))}
    assert len(index) == 456 and len(rows) == 426 and index[0] == 0
    assert set(coordinates) == set().union(*(ids(p) for p in rows.values()))
    out_coords = [{'id': index[i], 'parentId': i if i < 474 else None,
                   'sourceId': z.get('sourceId'), 'name': z['name'], 'kind': z.get('kind', 'gate')}
                  for i, z in sorted(coordinates.items())]
    out_rows = []
    for i, p in sorted(rows.items()):
        assert max(len(m) for s, m in p) <= 2
        p = primitive({(s, tuple(sorted(index[j] for j in m))): a for (s, m), a in p.items()})
        out_rows.append({'id': len(out_rows), 'parentId': i if i < 443 else None,
                         'name': labels[i], 'terms': encode(p)})
    certificate = {'sourceParentSha256': PARENT_SHA,
                   'rawRReplacement': encode(raw_replacement),
                   'correctedRReplacement': encode(corrected_replacement),
                   'scalarOrder': 31, 'inversePowerExponents': [1, 3, 7, 15, 31],
                   'poleRescalings': pole_certificates,
                   'parentToNew': {str(i): j for i, j in index.items()}}
    return out_coords, out_rows, certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=HERE / 'source')
    parser.add_argument('--output', type=Path, default=HERE / 'polynomial-456')
    args = parser.parse_args()
    assert digest(args.source / 'parent474-residuals.json') == PARENT_SHA
    parent = json.loads((args.source / 'parent474-residuals.json').read_text())
    semantic = json.loads((args.source / 'semantic-values.json').read_text())
    coords, rows, cert = construct(parent, semantic)
    args.output.mkdir(parents=True, exist_ok=True)
    write(args.output / 'residuals.json', {'schema': 'quadratic-system/v1', 'fixedParameter': FIXED,
          'parentSha256': PARENT_SHA, 'coordinates': coords, 'residuals': rows,
          'inputParameter': 'beta=216*X^4+450459', 'scalarOrder': 31,
          'scalarNormalization': 'R=102^2*r(beta)/(1+(17*r(beta))^2)^2',
          'scope': 'Exact quadratic realization of the stated arithmetic system; integer projection requires the arithmetic inputs stated in the paper.'})
    table = {}
    for row in rows:
        p = read(row['terms']); table = add(table, mul(p, p))
    assert all(a.denominator == 1 for a in table.values())
    assert table[(0, (0, 0, 0, 0))] == 1
    assert max(len(m) for s, m in table) == 4
    grouped = defaultdict(dict)
    for (s, m), a in table.items(): grouped[m][s] = a.numerator
    anchor = next(z['id'] for z in coords if z['name'] == 'anchor.U')
    assert grouped[(anchor, anchor)] == {2: 64}
    other = [p for m, p in grouped.items() if m != (anchor, anchor)]
    lower_bits = max(abs(p.get(0, 0)) + abs(p.get(1, 0)) for p in other).bit_length()
    s2_bound = max(abs(p.get(2, 0)) for p in other)
    assert s2_bound < 63 and lower_bits < 52832906
    write(args.output / 'polynomial.json', {'schema': 'integer-quartic-symbolic-fixed-constant-v1',
          'fixedParameter': FIXED, 'coordinates': coords, 'terms': encode(table),
          'construction': 'Exact sum of squares of 426 primitive quadratic residuals; S is a fixed integer.'})
    write(args.output / 'transformation-certificate.json', cert)
    report = {'status': 'produced; independent verification required', 'totalVariables': 456,
              'existentialWitnesses': 455, 'quadraticResiduals': 426, 'degree': 4,
              'ordinaryMonomials': len(grouped), 'coefficientParameterTerms': len(table),
              'coefficientContent': 1, 'exactCoefficientHeight': '64*3^105665812',
              'fixedParameter': FIXED, 'otherQuadraticSCoefficientsAtMost': s2_bound,
              'lowerCoefficientEnvelopeBits': lower_bits,
              'sha256': {n: digest(args.output / n) for n in
                         ('residuals.json', 'polynomial.json', 'transformation-certificate.json')}}
    (args.output / 'construction-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
