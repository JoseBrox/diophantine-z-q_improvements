#!/usr/bin/env python3
"""Independent exact exponent, row, occurrence, and coefficient audit."""
from pathlib import Path
from fractions import Fraction
import hashlib
import importlib.util
import json
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]


def named(row, names):
    return {(tuple(sorted(names[j-1] for j in t['monomial']))):
            sp.sympify(t['coefficient']) for t in row['terms']}


def main():
    reports = []
    for m, stage, expected in [(163, 'detector_pell', (1074, 924)),
                               (179, 'detector_pell', (1254, 1080)),
                               (56, 'pell_core', (808, 696))]:
        source = ROOT/f'undecidability/coefficients/jones1980_{stage}/{stage}_m{m}_quadrics.json'
        path = ROOT/f'undecidability/coefficients/jones1980_ceiling_power/ceiling_power_m{m}_quadrics.json'
        old = json.loads(source.read_bytes())
        new = json.loads(path.read_bytes())
        cert = json.loads(path.with_name(path.name.replace('_quadrics.json', '_certificate.json')).read_text())
        assert cert['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert cert['predecessor_sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
        assert (new['variables'], len(new['residuals'])) == expected
        assert new['variables'] == len(new['variable_names']) == old['variables']-29
        assert new['outer_coordinates'] == old['outer_coordinates']-29
        old_names, new_names = old['variable_names'], new['variable_names']
        old_rows = {r['name']: named(r, old_names) for r in old['residuals']}
        new_rows = {r['name']: named(r, new_names) for r in new['residuals']}
        assert len(new_rows) == len(new['residuals'])
        removed = set(old_names)-set(new_names)
        assert len(removed) == 165
        dropped = set(old_rows)-set(new_rows)
        assert len(dropped) == 166
        for n in old_rows.keys() & new_rows.keys():
            assert old_rows[n] == new_rows[n], n
        for n in removed:
            occurrences = sorted(r for r, terms in old_rows.items() if any(n in t for t in terms))
            assert set(occurrences) <= dropped
            assert occurrences == sorted(new['ceiling_power_removed_occurrences'][n])
        exponents = {'b': 1, 'B5': 5}
        previous = 'B5'
        digits = []
        for j in range(1, 138):
            current = 'q' if j == 137 else f'ceiling_power_{j:03}'
            row = new_rows[f'jones1980.ceiling_power.{j:03}']
            assert row[tuple(sorted((previous, previous)))] == -1
            positive = [t for t, c in row.items() if c == 1]
            assert len(positive) == 1 and len(row) == 2
            mon = positive[0]
            assert current in mon and set(mon) <= {current, 'b'}
            digit = len(mon)-1
            assert digit in (0, 1)
            e = 2*exponents[previous]-digit
            exponents[current] = e
            digits.append(digit)
            previous = current
        assert exponents['q'] == 5**60
        assert sum(digits) == 78
        assert new['power_multiplications'] == 139
        # The independently reconstructed exponent recurrence proves the huge
        # identity.  Small exact examples also check positive and negative bases.
        for base in [Fraction(2), Fraction(-2), Fraction(2, 3), Fraction(-3, 2)]:
            for exponent in range(1, 80):
                height = exponent.bit_length()
                e, value = 1, base
                for k in range(height-1, -1, -1):
                    target = (exponent+(1 << k)-1)//(1 << k)
                    digit = 2*e-target
                    assert digit in (0, 1)
                    value = value*value/(base if digit else 1)
                    e = target
                assert value == base**exponent
        params = set(map(sp.Symbol, new['parameters']))
        support = set()
        for r in new['residuals']:
            for t in r['terms']:
                assert len(t['monomial']) <= 2
                c = sp.sympify(t['coefficient'])
                assert c.free_symbols <= params
                assert sp.Poly(c, *sorted(params, key=str)).domain.is_ZZ
                support.update(t['monomial'])
        assert support == set(range(1, new['variables']+1))
        for key in ['source_universality_hypothesis', 'source_universality_verified',
                    'unconditional_undecidability_claim', 'ordinary_integer_inputs']:
            assert new[key] == old[key]
        spec = importlib.util.spec_from_file_location('ceiling_builder', ROOT/'undecidability/code/build_ceiling_power.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        rebuilt = json.dumps(builder.build(source), sort_keys=True, separators=(',', ':'))+'\n'
        assert rebuilt.encode() == path.read_bytes()
        reports.append({'interface': m, 'variables': expected[0], 'quadratic_rows': expected[1],
                        'power_coordinates': 139, 'saving': 29})
    print(json.dumps({'status': 'PASS', 'systems': reports,
          'scope': 'Exact exponent recurrence, all unchanged rows, full removed-coordinate occurrence audit, parameter-polynomial domains, support, hashes, and byte-identical rebuild. Mathematical nonvanishing is proved in the accompanying manuscript.'}, indent=2))


if __name__ == '__main__':
    main()
