#!/usr/bin/env python3
"""Replace a fixed-power chain by its quadratic ceiling-binary circuit.

Only the power circuit changes.  The full rational equivalence uses the
retained positive-alpha row to prove b>0 before interpreting any power row.
Source-universality and arithmetic qualifications are inherited unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPONENT = 5**60
START_EXPONENT = 5
REMAINING_BITS = 137


def ceiling_chain(exponent=EXPONENT, bits=REMAINING_BITS):
    values = [(exponent + (1 << k) - 1) // (1 << k)
              for k in range(bits, -1, -1)]
    assert values[0] == START_EXPONENT and values[-1] == exponent
    assert all(2*a-b in (0, 1) for a, b in zip(values, values[1:]))
    return values


def build(source):
    raw = Path(source).read_bytes()
    old = json.loads(raw)
    names = old['variable_names']
    rows = old['residuals']
    old_chain = old['power_chain']
    assert len(old_chain) == 169 and old_chain[-1][0] == EXPONENT
    removed_names = {n for n in names if n.startswith('power_') and n != 'power_001'}
    assert len(removed_names) == 165
    removed_rows = {r['name'] for r in rows if
                    r['name'].startswith('jones1980.power_') and
                    r['name'] != 'jones1980.power_001.definition'}
    removed_rows.add('jones1980.q.quotient')
    assert len(removed_rows) == 166
    occurrence = {n: [] for n in sorted(removed_names)}
    for row in rows:
        support = {names[j-1] for t in row['terms'] for j in t['monomial']}
        for n in support & removed_names:
            occurrence[n].append(row['name'])
            assert row['name'] in removed_rows, (n, row['name'])
    exponents = ceiling_chain()
    added_names = [f'ceiling_power_{j:03}' for j in range(1, len(exponents)-1)]
    assert len(added_names) == 136
    new_names = [n for n in names if n not in removed_names] + added_names
    assert len(new_names) == len(set(new_names))
    ids = {n: j+1 for j, n in enumerate(new_names)}
    new_rows = []
    for row in rows:
        if row['name'] in removed_rows:
            continue
        new_rows.append({'name': row['name'], 'terms': sorted([
            {'coefficient': t['coefficient'],
             'monomial': sorted(ids[names[j-1]] for j in t['monomial'])}
            for t in row['terms']], key=lambda t: t['monomial'])})
    circuit_names = ['B5'] + added_names + ['q']
    circuit = []
    for j, (a, e) in enumerate(zip(exponents, exponents[1:]), 1):
        previous, current = circuit_names[j-1:j+1]
        digit = 2*a-e
        monomial = sorted([ids[current]] + ([ids['b']] if digit else []))
        row_name = f'jones1980.ceiling_power.{j:03}'
        new_rows.append({'name': row_name, 'terms': sorted([
            {'coefficient': '1', 'monomial': monomial},
            {'coefficient': '-1', 'monomial': [ids[previous], ids[previous]]}],
            key=lambda t: t['monomial'])})
        circuit.append({'row': row_name, 'coordinate': current,
                        'previous_coordinate': previous, 'exponent': e,
                        'previous_exponent': a, 'subtracted_digit': digit})
    saving = len(removed_names) - len(added_names)
    assert saving == 29
    assert len(new_rows) == len(rows)-saving
    support = {j for row in new_rows for t in row['terms'] for j in t['monomial']}
    assert support == set(range(1, len(new_names)+1))
    result = dict(old)
    result.update(variables=len(new_names), variable_names=new_names,
                  residuals=new_rows,
                  outer_coordinates=old['outer_coordinates']-saving,
                  outer_residuals=old['outer_residuals']-saving,
                  power_chain_predecessor=old_chain,
                  power_chain_kind='ceiling binary with the existing b^3 and b^5 prefix',
                  power_chain=circuit,
                  power_multiplications=139,
                  ceiling_power_predecessor_sha256=hashlib.sha256(raw).hexdigest(),
                  ceiling_power_removed_coordinates=sorted(removed_names),
                  ceiling_power_added_coordinates=added_names,
                  ceiling_power_removed_rows=sorted(removed_rows),
                  ceiling_power_removed_occurrences=occurrence,
                  ceiling_power_saving=saving,
                  ceiling_power_nonzero_proof='The retained alpha>0, g,t,m,theta>0, u,y>0 imply b>x*y>=0 independently of all power rows.',
                  ceiling_power_proof='undecidability/papers/ceiling_power_quartic_checkpoint.tex')
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.source:
        assert args.output
        cases = [(None, args.source, args.output)]
    else:
        out = ROOT/'undecidability/coefficients/jones1980_ceiling_power'
        cases = [(m, ROOT/f'undecidability/coefficients/jones1980_{stage}/{stage}_m{m}_quadrics.json',
                  out/f'ceiling_power_m{m}_quadrics.json')
                 for m, stage in [(163, 'detector_pell'), (179, 'detector_pell'), (56, 'pell_core')]]
    for m, source, output in cases:
        result = build(source)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n')
        certificate = {
            'interface_coordinates': m, 'variables': result['variables'],
            'quadratic_rows': len(result['residuals']), 'degree': 4,
            'coordinate_saving': result['ceiling_power_saving'],
            'source_table': str(source.relative_to(ROOT)),
            'predecessor_sha256': result['ceiling_power_predecessor_sha256'],
            'table_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'power_exponent': EXPONENT, 'retained_prefix_exponents': [3, 5],
            'ceiling_steps': 137, 'power_coordinates': 139,
            'source_universality_hypothesis': result.get('source_universality_hypothesis'),
            'source_universality_verified': result.get('source_universality_verified', False),
            'unconditional_undecidability_claim': False,
            'retained_arithmetic_interfaces': True,
            'proof': result['ceiling_power_proof'],
            'independent_verifier': 'undecidability/verify_ceiling_power.py'}
        output.with_name(output.name.replace('_quadrics.json', '_certificate.json')).write_text(
            json.dumps(certificate, sort_keys=True, indent=2)+'\n')
        print(json.dumps({k: certificate[k] for k in ['interface_coordinates', 'variables', 'quadratic_rows', 'coordinate_saving']}))


if __name__ == '__main__':
    main()
