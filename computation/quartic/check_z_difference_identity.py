#!/usr/bin/env python3
"""Check the compressed z(H-P) identity against the elliptic addition law.

The calculation is exact in Q(sqrt(2))(x)[S]/(S^2-x+D/x).
It imports no polynomial producer and makes no numerical specialization.
"""
from pathlib import Path
import json
from cypari2 import Pari

pari = Pari()
pari.allocatemem(128000000, silent=True)
# Introduce the main residue variable first, followed by the coefficient
# variables, to keep PARI's polynomial variable priorities explicit.
pari("hq='hq; hx='hx; hr='hr;")
pari('rho=Mod(hr,hr^2-2); dd=11-6*rho; xp=(57-28*rho)/8; yp=(-660+417*rho)/32;')
pari('ss=Mod(hq,hq^2-hx+dd/hx);')
pari('gg=-((39-36*rho)+(8-14*rho)*ss)/(8*(xp*hx+dd));')
pari('nn=(-660+417*rho)+(-228+112*rho)*ss;')
pari('den=(-704+384*rho)+(660-417*rho)*ss+(6888-5040*rho)*gg;')
pari('slope=(hx*ss+yp)/(hx-xp); xv=slope^2-hx-xp; yv=-hx*ss+slope*(hx-xv);')
checks = {
    'point_P_on_curve': 'yp^2-xp^3+dd*xp',
    'H_on_curve': '(hx*ss)^2-hx^3+dd*hx',
    'g_cleared_equation': '8*(xp*hx+dd)*gg+(39-36*rho)+(8-14*rho)*ss',
    'reciprocal_abscissa_identity': 'hx*gg^2*xv-1',
    'z_difference_identity': 'nn*yv+den*xv',
    'N_zero_value_of_S': '-(-660+417*rho)/(-228+112*rho)-yp/xp',
    'N_zero_curve_factorization': 'hx^2-(yp/xp)^2*hx-dd-(hx-xp)*(hx+dd/xp)',
    'reduced_N_coefficients': '(3+2*rho)*nn-((-312-69*rho)+(-236-120*rho)*ss)',
    'reduced_D_coefficients': '(3+2*rho)*den-((-576-256*rho)+(312+69*rho)*ss+(504-1344*rho)*gg)',
}
results = {}
for name, expression in checks.items():
    value = pari(expression)
    assert value == 0, (name, value)
    results[name] = str(value)
report = {
    'status': 'PASS', 'pari_version': str(pari('version()')),
    'method': 'Exact function-field reduction against the elliptic addition law; no producer imported.',
    'curve': 'y^2=x^3-(11-6*sqrt(2))*x',
    'H_coordinates': ['x', 'x*S'],
    'field_relation': 'S^2=x-(11-6*sqrt(2))/x',
    'g': '-((39-36*rho)+(8-14*rho)*S)/(8*(x(P)*x+D))',
    'z_H_minus_P': 'N/D0',
    'N': '(-660+417*rho)+(-228+112*rho)*S',
    'D0': '(-704+384*rho)+(660-417*rho)*S+(6888-5040*rho)*g',
    'common_unit_used_in_source': '3+2*rho',
    'checks': results,
    'exceptional_H_classes_to_exclude_before_division': ['E[2](K)', 'P+E[2](K)', '-P+E[2](K)'],
    'important_branch': 'N=0 includes H=-P+(0,0), so excluding only indices h=0,1 is insufficient.',
    'scope': 'An exact rational-function identity on its stated nonzero domain. The arithmetic argument excluding exceptional H is separate.'
}
folder = Path(__file__).resolve().parent / 'family_abc97_v17'
folder.mkdir(exist_ok=True)
output = folder / 'z-difference-identity.json'
output.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'exact_identities': len(results), 'output': str(output)}, indent=2))
