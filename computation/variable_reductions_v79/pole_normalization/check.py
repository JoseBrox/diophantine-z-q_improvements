#!/usr/bin/env python3
"""Independently recover the physical poles from four published v78 tables.

No v78 producer or checker is imported.  The only inputs are the literal
quadratic rows, source-coordinate IDs and their published Laurent weights.
This checks algebraic normalization, not the external arithmetic premises.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
C, c = s.symbols('C c', nonzero=True)
x = {i: s.Symbol('x'+str(i), nonzero=True) for i in range(1, 612)}


def recover(folder):
    q = json.loads((folder/'quadrics.json').read_text())
    weights = {int(k): int(v) for k, v in
               json.loads((folder/'weights.json').read_text())['weights'].items()}
    ids = {z['id']: z['source_id'] for z in q['coordinates']}
    units = {400: c, 401: 1/c, 402: 1/c**2}
    rows = {}
    for row in q['residuals']:
        val = 0
        for term in row['terms']:
            mon = 1
            for index in term['monomial']:
                source = ids[index]
                mon *= units[source] if source in units else c**(-weights.get(source, 0))*x[source]
            val += int(term['coefficient'])*C**term['parameterPower']*mon
        rows[row['name']] = s.expand(val)
    return rows


def unit_ratio(left, right):
    """Require equality of zero sets by a nonzero rational Laurent unit."""
    ratio = s.factor(s.cancel(left/right))
    assert ratio != 0 and ratio.free_symbols <= {C, c}, ratio
    coeff, factors = ratio.as_coeff_Mul()
    assert coeff != 0 and coeff.is_Rational
    assert all(v.is_Integer for v in factors.as_powers_dict().values())
    assert set(factors.as_powers_dict()) <= {C, c, s.Integer(1)}
    assert s.cancel(left-ratio*right) == 0
    return str(ratio)


def audit(folder, count):
    rows = recover(folder)
    # This square identity is the only shared scalar relation used below.
    scalar = c*x[112]-C*x[113]**2
    scalar_unit = unit_ratio(rows['scalar.r_power_2.definition'], scalar)
    sx = {x[112]: C*x[113]**2/c}
    records = []
    roles = [(3,4,5,6,82,83,84,85,81),
             (7,8,9,10,96,97,98,99,95)]
    if count == 3:
        roles.append((503,504,505,506,582,583,584,585,581))
    for j, (ie,iu,ip,iq,ib,ip2,iv,iq2,it) in enumerate(roles):
        # Solve the *literal published* power rows, not their labels.
        psq = s.solve(rows[f'detector{j}.p2.definition'].subs(sx), x[ip2])
        qsq = s.solve(rows[f'detector{j}.q2.definition'].subs(sx), x[iq2])
        assert len(psq) == len(qsq) == 1
        square_sub = {x[ip2]: psq[0], x[iq2]: qsq[0]}
        b = c*x[ib]
        if j == 1:
            e, u, v = c*x[ie], c*x[iu], c*x[iv]
            p, q = c*x[ip]/x[113], c*x[iq]/x[113]
        else:
            e, u, v = x[ie]/c, x[iu], x[iv]
            p, q = x[ip]/(C*c*x[113]), x[iq]/x[113]
        native = [3*e**2-34*e-289+17*b*p**2,
                  e*(17-b)-17*u*v,
                  u**2+34*u*v-867*v**2-17*b*q**2]
        names = ['firstConic','Bh.definition','secondConic']
        factors = {}
        for name, residual in zip(names, native):
            old = rows[f'detector{j}.{name}'].subs(square_sub)
            factors[name] = unit_ratio(residual, old)
        qj = x[300] if j == 0 else (
            c-x[300] if count == 2 else x[301] if j == 1
            else c-x[300]-x[301])
        inv = x[310+j]
        unit_ratio(rows[f'shared.inverse{j}'], c-qj*inv)
        g = 1+x[305]**2+(c-qj)**2/qj
        unit_ratio(rows[f'shared.gate{j}'].subs(inv, c/qj), 2*c*x[it]-g)
        gamma2 = s.Rational(408**2, 409**2)
        unit_ratio(rows[f'balanced.detector{j}.poleInput.definition'],
                   c*x[ib]*(1+qj)-gamma2*(c*x[it])**2)
        # Eliminate the gate and pole coordinate and identify the physical b.
        result = s.solve(rows[f'balanced.detector{j}.poleInput.definition'], x[ib])[0]*c
        result = s.cancel(result.subs(x[it], g/(2*c)))
        assert s.cancel(result-gamma2*g**2/(4*(1+qj))) == 0
        # The formerly suspected c^{-2} factor is explicitly rejected.
        assert s.cancel(result-gamma2*g**2/(4*c**2*(1+qj))) != 0
        records.append({'block': j, 'b': str(b), 'e': str(e), 'u': str(u),
                        'v': str(v), 'p': str(p), 'q': str(q),
                        'native_residual_to_published_residual': factors,
                        'physical_input': '(408/409)^2*g_j^2/(4*(1+q_j))',
                        'incorrect_extra_inverse_c_square_rejected': True})
    return {'path': str(folder.relative_to(ROOT)), 'scalar_relation_unit': scalar_unit,
            'input_sha256': {name: sha256((folder/name).read_bytes()).hexdigest()
                             for name in ['quadrics.json','weights.json']},
            'pole_blocks': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    folders = [('computation/coauthor_audit_v78/H10-quartics/quartics/general-physical',2),
               ('computation/coauthor_audit_v78/H10-quartics/quartics/explicit-physical',3),
               ('computation/coauthor_audit_v78/work_general/enhanced/165',2),
               ('computation/coauthor_audit_v78/work_general/enhanced/180',3)]
    result = {'schema': 'diophantine-physical-pole-normalization/v79', 'status': 'PASS',
              'source_attribution': 'Gabe Conant with Astra 6.2; v78 project audit and continuation',
              'assumptions': ['C != 0', 'c != 0', 'x113 != 0'],
              'tables': [audit(ROOT/path,n) for path,n in folders],
              'scope': 'Exact native-pole and gate normalization from literal quadratic tables. No new variable reduction or arithmetic premise is asserted.'}
    text = json.dumps(result, indent=2)+'\n'
    target = HERE/'certificate.json'
    if args.write:
        target.write_text(text)
    else:
        assert target.read_text() == text
    print(json.dumps({'status':'PASS','tables':len(result['tables']),
                      'pole_blocks':sum(len(t['pole_blocks']) for t in result['tables'])}))


if __name__ == '__main__':
    main()
