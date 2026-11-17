#!/usr/bin/env python3
"""Regenerate the fully expanded, literal integer polynomial at N=15."""
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
FAMILY_DIGEST = '72d80d57ad9514b184649bfa11dbc43dfce035b6248fa09f93ceb7011bd1cfd7'
N = 15


def main():
    raw = (ROOT / 'polynomial.json').read_bytes()
    assert sha256(raw).hexdigest() == FAMILY_DIGEST
    family = json.loads(raw)
    fixed_parameter = 149 ** N
    polynomial = defaultdict(int)
    for term in family['terms']:
        monomial = tuple(sorted(term['monomial']))
        polynomial[monomial] += int(term['coefficient']) * fixed_parameter ** term['parameterPower']
    polynomial = {m: c for m, c in polynomial.items() if c}
    assert len(polynomial) == 3312
    assert max(map(len, polynomial)) == 4
    lines = [
        '# Integer quartic in x1,...,x229; distinguished input x1.',
        '# Fixed specialization N=15. All 3312 terms are listed with literal integer coefficients.',
        'P =',
    ]
    for monomial, coefficient in sorted(polynomial.items()):
        sign = '+' if coefficient > 0 else '-'
        factors = [str(abs(coefficient))]
        for variable, power in sorted(Counter(monomial).items()):
            factors.append(f'x{variable}' + (f'^{power}' if power != 1 else ''))
        lines.append(f'  {sign} ' + '*'.join(factors))
    target = ROOT / 'quartic229-N15.txt'
    target.write_text('\n'.join(lines) + '\n', encoding='ascii')
    print(json.dumps({'artifact': target.name, 'bytes': target.stat().st_size,
                      'sha256': sha256(target.read_bytes()).hexdigest(),
                      'terms': len(polynomial), 'fixed_N': N}, indent=2))


if __name__ == '__main__':
    main()
