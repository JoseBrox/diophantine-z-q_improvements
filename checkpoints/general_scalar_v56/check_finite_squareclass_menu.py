#!/usr/bin/env python3
"""Exact discriminants for the fixed finite squareclass-menu audit."""
import json
from pathlib import Path
import sympy as s

Y, M = s.symbols('Y M')
reports = []
for values in [(1,), (1, 2), (1, 2, 3), (1, 2, 3, 5)]:
    m = len(values)
    poly = s.prod(Y**2-d*M for d in values)
    expected = 4**m*s.prod(values)*M**(m*(2*m-1))
    expected *= s.prod((values[i]-values[j])**4
                       for i in range(m) for j in range(i+1, m))
    actual = s.discriminant(poly, Y)
    assert s.expand(actual-expected) == 0
    reports.append({'representatives': values, 'degree': 2*m,
                    'discriminant': str(s.factor(actual)),
                    'nonconstant_guard_factors': ['M']})
result = {'status': 'PASS', 'menus': reports,
          'new_free_coordinates': 0,
          'new_realization_theorem': False,
          'encoding': 'finite product of existing quadratic branch encoders'}
Path(__file__).with_name('finite_squareclass_menu_certificate.json').write_text(
    json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
