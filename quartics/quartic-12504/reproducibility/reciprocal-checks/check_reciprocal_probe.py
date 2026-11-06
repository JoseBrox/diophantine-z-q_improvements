"""Independent exact verifier for the isolated reciprocal-G circuits.

No producer or archive builder is imported. Coefficients are obtained from
sqrt(1-w) times the binomial elliptic integral, not the producer recurrence.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path


def add(*terms):
    out = {}
    for scalar, p in terms:
        for mon, c in p.items():
            out[mon] = out.get(mon, F(0)) + scalar*c
    return {m: c for m, c in out.items() if c}


def mul(p, q):
    out = {}
    for m, a in p.items():
        for n, b in q.items():
            k = tuple(sorted(m+n))
            out[k] = out.get(k, F(0)) + a*b
    return {m: c for m, c in out.items() if c}


def fm(p, q):
    return add((1, mul(p[0], q[0])), (2, mul(p[1], q[1]))), add((1, mul(p[0], q[1])), (1, mul(p[1], q[0])))


def independent_coefficients(n):
    sqrt = [F(1)]
    for k in range(1, n):
        sqrt.append(sqrt[-1] * (F(k-1)-F(1, 2))/k)
    integral = [F(comb(2*k, k), 4**k*(4*k+1)) for k in range(n)]
    return [sum(sqrt[i]*integral[j-i] for i in range(j+1)) for j in range(n)]


def decode_row(row):
    out = {}
    for c, variables in row:
        mon = tuple(variables)
        assert type(c) is int and c and mon == tuple(sorted(mon))
        assert all(type(v) is int and v >= 0 for v in mon)
        assert mon not in out and len(mon) <= 2
        out[mon] = F(c)
    return out


def substitute(poly, env):
    result = {}
    for mon, c in poly.items():
        term = {(): c}
        for v in mon:
            assert v in env
            term = mul(term, env[v])
        result = add((1, result), (1, term))
    return result


def validate(data):
    assert data['kind'] == 'reciprocal-G-circuit'
    assert data['input_count'] == 2
    precision = data['precision']
    assert precision in (13, 16, 52, 64)
    cs = independent_coefficients((precision+3)//4)
    assert data['coefficient_list'] == [str(x) for x in cs]
    targets = data['targets']
    assert targets == list(range(2, 2+len(targets)))
    assert len(targets) == len(data['rows'])
    env = {0: {(0,): F(1)}, 1: {(1,): F(1)}}
    rows = []
    for target, raw in zip(targets, data['rows']):
        row = decode_row(raw)
        lead = row.get((target,), F(0))
        assert lead
        rest = {mon: -c/lead for mon, c in row.items() if mon != (target,)}
        assert all(target not in mon for mon in rest)
        env[target] = substitute(rest, env)
        rows.append(row)
    actual = []
    assert len(data['outputs']) == 2
    for raw in data['outputs']:
        expr = {}
        for term in raw:
            num, den = term['coefficient']; mon = tuple(term['monomial'])
            assert type(num) is int and type(den) is int and den > 0 and num
            assert mon == tuple(sorted(mon)) and len(mon) <= 2 and mon not in expr
            expr[mon] = F(num, den)
        actual.append(substitute(expr, env))
    f = (env[0], env[1])
    w = fm(({(): F(11)}, {(): F(-6)}), fm(f, f))
    power = ({(): F(1)}, {})
    expected = ({}, {})
    for c in cs:
        expected = tuple(add((1, a), (c, b)) for a, b in zip(expected, power))
        power = fm(power, w)
    assert tuple(actual) == expected
    expansion = {}
    for row in rows:
        expansion = add((1, expansion), (1, mul(row, row)))
    maximum = max((abs(x) for x in expansion.values()), default=F(0))
    assert maximum.denominator == 1
    return {'status': 'PASS', 'precision': precision, 'bound_output': data['bound_output'],
            'hscale': data['hscale'], 'rational_targets': len(targets),
            'isolated_residuals': len(rows), 'isolated_monomials': len(expansion),
            'isolated_max_abs_coefficient': str(maximum.numerator),
            'isolated_coefficient_bits': maximum.numerator.bit_length(),
            'isolated_below_2_80': maximum < 2**80,
            'scope': 'Exact G output identities and isolated squared-row expansion; not a whole-source or quartic acceptance'}


def mutations(data):
    cases = []
    bad = copy.deepcopy(data); bad['coefficient_list'][-1] = '0'; cases.append(('wrong coefficient', bad))
    bad = copy.deepcopy(data); bad['precision'] = 12; cases.append(('unreviewed precision', bad))
    bad = copy.deepcopy(data); bad['targets'][0] = 0; cases.append(('input overwritten', bad))
    bad = copy.deepcopy(data); bad['rows'][0][0][0] += 1; cases.append(('changed first defining row', bad))
    bad = copy.deepcopy(data); bad['rows'][0].append([1, [0, 0, 0]]); cases.append(('cubic residual', bad))
    bad = copy.deepcopy(data); bad['rows'][0].append([1, [1000000]]); cases.append(('undeclared dependency', bad))
    bad = copy.deepcopy(data); bad['outputs'][0][0]['coefficient'][0] += 1; cases.append(('wrong output', bad))
    bad = copy.deepcopy(data); bad['outputs'].reverse(); cases.append(('output pair reversed', bad))
    rejected = []
    for name, bad in cases:
        try:
            validate(bad)
        except (AssertionError, ValueError, KeyError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise AssertionError('Malformed circuit accepted: '+name)
    return rejected


def expected_cases():
    """The reviewed probe contract, independent of the supplied index."""
    cases = {}
    for precision, scales in ((16, (1,)), (52, (1, 2, 3, 4)), (64, (1, 2, 3, 4))):
        for scale in scales:
            for bound in (False, True):
                name = f'g{precision}-scale{scale}-'+('bound' if bound else 'direct')+'.json'
                targets = (4 if precision == 16 else 10) + (2 if bound else 0)
                cases[name] = (precision, scale, bound, targets)
    assert len(cases) == 18
    return cases


def validate_packet(index, read_file):
    """Require all 18 named cases, their exact parameters and byte digests."""
    expected = expected_cases()
    assert type(index) is list and len(index) == len(expected)
    seen = set()
    accepted = []
    for entry in index:
        assert type(entry) is dict and set(entry) == {'file', 'targets', 'sha256'}
        name = entry['file']
        assert type(name) is str and name in expected and name not in seen
        seen.add(name)
        precision, scale, bound, targets = expected[name]
        assert type(entry['targets']) is int and entry['targets'] == targets
        digest = entry['sha256']
        assert type(digest) is str and len(digest) == 64
        assert all(c in '0123456789abcdef' for c in digest)
        raw = read_file(name)
        assert type(raw) is bytes and hashlib.sha256(raw).hexdigest() == digest
        data = json.loads(raw)
        assert type(data) is dict
        assert type(data['precision']) is int and data['precision'] == precision
        assert type(data['hscale']) is int and data['hscale'] == scale
        assert type(data['bound_output']) is bool and data['bound_output'] is bound
        assert type(data['input_count']) is int and data['input_count'] == 2
        assert type(data['targets']) is list
        assert all(type(v) is int for v in data['targets'])
        assert data['targets'] == list(range(2, 2+targets))
        accepted.append((entry, data))
    assert seen == set(expected)
    return accepted


def packet_mutations(index, contents):
    """Exercise coverage/digest checks without changing any supplied file."""
    cases = [('empty index', [], contents), ('missing case', index[:-1], contents)]
    bad = copy.deepcopy(index); bad[-1] = copy.deepcopy(bad[0])
    cases.append(('duplicate case', bad, contents))
    bad = copy.deepcopy(index); bad[0]['file'] = '../'+bad[0]['file']
    cases.append(('unreviewed file name', bad, contents))
    bad = copy.deepcopy(index); bad[0]['sha256'] = '0'*64
    cases.append(('wrong digest', bad, contents))
    bad = copy.deepcopy(index); bad[0]['targets'] += 2
    cases.append(('wrong indexed target count', bad, contents))
    name = index[0]['file']
    changed = dict(contents); changed[name] += b' '
    cases.append(('changed file bytes', index, changed))
    for key, value in (('precision', 13), ('hscale', 99), ('bound_output', 'false'),
                       ('input_count', True), ('targets', [])):
        bad = copy.deepcopy(index)
        data = json.loads(contents[name]); data[key] = value
        changed = dict(contents); changed[name] = json.dumps(data).encode('utf-8')
        bad[0]['sha256'] = hashlib.sha256(changed[name]).hexdigest()
        cases.append(('mismatched '+key, bad, changed))
    rejected = []
    for name, bad, changed in cases:
        try:
            validate_packet(bad, changed.__getitem__)
        except (AssertionError, ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise AssertionError('Malformed probe packet accepted: '+name)
    return rejected


def main():
    if not __debug__:
        raise RuntimeError('This checker requires Python assertions; do not use -O')
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    index = json.loads((args.directory/'index.json').read_text())
    contents = {name: (args.directory/name).read_bytes() for name in expected_cases()}
    accepted = validate_packet(index, contents.__getitem__)
    coverage_rejections = packet_mutations(index, contents)
    reports = []
    for entry, data in accepted:
        report = dict(file=entry['file'], **validate(data))
        report['verified_sha256'] = entry['sha256']
        report['malformed_circuits_rejected'] = mutations(data)
        reports.append(report)
    coverage = {'status': 'PASS', 'expected_cases': len(expected_cases()),
                'verified_cases': len(reports),
                'malformed_packets_rejected': coverage_rejections,
                'files': [dict(file=e['file'], sha256=e['sha256']) for e, _ in accepted]}
    (args.directory/'independent-coverage.json').write_text(json.dumps(coverage, indent=2)+'\n')
    (args.directory/'independent-check.json').write_text(json.dumps(reports, indent=2)+'\n')
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    main()
