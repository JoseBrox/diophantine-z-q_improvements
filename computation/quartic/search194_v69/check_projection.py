#!/usr/bin/env python3
"""Independently check the two-factor unit obstruction without an SMT solver.

For each allowed extra unit, the constant terms and the same squared C2
coordinate in the two detectors already give incompatible exponents.
This concerns the recorded unit basis and factor forms only.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product
import argparse
import json

ROOT = Path(__file__).resolve().parent


def main(output):
    base = {(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (-1, -2)}
    extras = {(a[0]+b[0]-c[0], a[1]+b[1]-c[1])
              for a, b, c in product(base, repeat=3)} - base
    assert len(extras) == 32
    model_hashes = {}
    for name in ('A4_B4', 'A1_B3', 'A1_A3'):
        path = ROOT / 'models' / (name + '.json')
        raw = path.read_bytes()
        model = json.loads(raw)
        assert {tuple(v) for v in model['base_units'].values()} | {(0, 0)} == base
        assert {tuple(v) for v in model['extra_unit_candidates']} == extras
        assert model['quadratic_tests']['C2'] == [66, [-6, 0], 9]
        assert model['physical_contact_weights'] == ['u', 'u*v']
        model_hashes[name] = sha256(raw).hexdigest()
    cases = []
    for extra in sorted(extras):
        units = base | {extra}
        sums = {(a[0]+b[0], a[1]+b[1]) for a, b in product(units, repeat=2)}
        excluded = []
        for p0, p1 in product((9, 11), repeat=2):
            difference = (p0-p1, -p1)
            pairs = [(e0, (e0[0]+difference[0], e0[1]+difference[1]))
                     for e0 in sums
                     if (e0[0]+difference[0], e0[1]+difference[1]) in sums]
            assert not pairs, (extra, p0, p1, pairs)
            excluded.append(dict(p0=p0, p1=p1, required_difference=list(difference)))
        cases.append(dict(extra_unit=list(extra),
                          constant_term_exponents=[list(e) for e in sorted(sums)],
                          excluded=excluded))
    report = dict(schema='support194-independent-projection/v69', status='PASS',
        method='Exhaustive integer set arithmetic; no SMT solver or producer imported.',
        input_model_sha256=model_hashes, checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        unit_bases=32, exponent_pairs_per_basis=4, incompatible_pairs=128,
        common_squared_coordinate=66, physical_coordinate_profile=[-6, 0],
        necessary_difference='E1-E0=(p0-p1,-p1)',
        real_coordinate_weights_already_excluded=True,
        integer_weight_parity_needed=False, cases=cases,
        scope='Only the original five physical units, one listed quadratic monomial extension, and the recorded comparison powers 9 or 11 in each detector. This is not a variable lower bound for other constructions.')
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'unit_bases', 'incompatible_pairs', 'scope')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'projection_certificate.json')
    main(parser.parse_args().output)
