#!/usr/bin/env python3
"""Exact checks for local solubility at every prepared conic parameter.

The universal assertion is proved in the companion note.  This verifier checks
its polynomial identities, the exceptional residue calculations, all smooth
unit quartics over small prime fields, and local certificates at every bad prime
of the previously published fixed-parameter counterexamples.  It does not use
numerical ranks, floating point, BSD, or an assumed local-to-global principle.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json
import sys
import sympy as sp


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def native_guard_audit():
    """Audit all four live v40 pole-stage guard specifications."""
    source_folder = REPOSITORY/'computation/few_variables/unit_norm_v28'
    sys.path.insert(0, str(source_folder))
    sys.dont_write_bytecode = True
    from build_sources import make_source
    output = []
    for name in ('general25','explicit27','weak13','abc13'):
        source = make_source(name)
        path = REPOSITORY/'computation/few_variables/terminal_root_v40/specifications'/f'{name}.json'
        spec = json.loads(path.read_text())
        nodes = source['coefficient_dag']
        dependencies = []
        for op, *args in nodes:
            if op == 'variable':
                deps = {args[0]}
            elif op in ('int', 'parameter'):
                deps = set()
            elif op in ('pow', 'neg'):
                deps = dependencies[args[0]].copy()
            elif op in ('add','mul'):
                deps = set().union(*(dependencies[a] for a in args))
            else:
                raise AssertionError(op)
            dependencies.append(deps)
        names = {v['name']: v['index'] for v in source['variables']}
        variable_nodes = {a[1]: i for i,a in enumerate(nodes) if a[0]=='variable'}
        poles = []
        for event in source['events']:
            if event['operation'] != 'rescaled_zero_pole':
                continue
            label = event['label']
            tau_index, s_index = names[label+'.conic_parameter'], names[label+'.s']
            conic = event['e']['denominator']
            tau_only = [f['node'] for f in spec['subalgebra_norm_factors']
                        if tau_index in dependencies[f['node']]
                        and s_index not in dependencies[f['node']]]
            assert tau_only == [conic], (name,label,tau_only,conic)
            assert variable_nodes[tau_index] not in source['guard_numerators']
            assert label+'.p' not in names
            # Check the only tau-only guard specializes to 51*d_numerator.
            dn, dd = event['square_class']['numerator'], event['square_class']['denominator']
            a, b, T = sp.symbols('dn dd T')
            if nodes[dn][0] == 'int': a = sp.Integer(nodes[dn][1])
            if nodes[dd][0] == 'int': b = sp.Integer(nodes[dd][1])
            substitutions = {dn:a, dd:b, variable_nodes[tau_index]:T}
            cache = {}
            def expression(i):
                if i in substitutions: return substitutions[i]
                if i in cache: return cache[i]
                op,*args = nodes[i]
                if op=='int': out = sp.Integer(args[0])
                elif op=='add': out = sum(expression(j) for j in args)
                elif op=='mul': out = sp.prod(expression(j) for j in args)
                elif op=='pow': out = expression(args[0])**args[1]
                elif op=='neg': out = -expression(args[0])
                else: raise AssertionError((i,op))
                cache[i] = out
                return out
            assert sp.expand(expression(conic).subs(T,0)-51*a)==0
            poles.append({'label':label,'only_tau_dependent_s_independent_guard':conic,
                'tau_zero_specialization':'51*d_numerator',
                'first_ordinate_p_is_not_stored_or_guarded':True})
        output.append({'source':name,'specification_sha256':sha256(path.read_bytes()).hexdigest(),
            'poles':poles,'earlier_point_guards':'assumed; unaffected by pole parameters',
            'finite_ordinate_guards':'nonzero local q witnesses can be chosen; final q guard relaxed in v40'})
    return output


def val(a, p):
    a = F(a)
    if not a:
        return None
    def vp(n):
        n = abs(n)
        k = 0
        while n % p == 0:
            n //= p
            k += 1
        return k
    return vp(a.numerator) - vp(a.denominator)


def unit(a, p):
    v = val(a, p)
    assert v is not None
    a = F(a) / F(p) ** v
    modulus = 8 if p == 2 else p
    return a.numerator * pow(a.denominator, -1, modulus) % modulus


def local_square(a, p):
    if not a:
        return True
    v = val(a, p)
    if v % 2:
        return False
    u = unit(a, p)
    return u == 1 if p == 2 else pow(u, (p-1)//2, p) == 1


def support(a):
    a = F(a)
    assert a
    return set(map(int, sp.factorint(abs(a.numerator)))) | \
        set(map(int, sp.factorint(a.denominator)))


def prepared(b):
    b = F(b)
    return (0 < b < 17 and isqrt(b.denominator)**2 == b.denominator
            and all(local_square(b, p) for p in (2, 3, 17))
            and all(val(b, p) >= k for p, k in ((2, 3), (3, 1), (17, 2))))


def local_certificate(D, A, p):
    """Certify a smooth projective local point, by independently tested cases."""
    if local_square(D, p):
        return {'type': 'infinity', 'square': str(D)}
    if local_square(-3*D, p):
        return {'type': 's_zero', 'square': str(-3*D)}
    if local_square(A, p):
        return {'type': 'q_zero_first_factor', 'square': str(A)}
    if local_square(-3*A, p):
        return {'type': 'q_zero_second_factor', 'square': str(-3*A)}
    if p == 3:
        value = D * (1-A) * (1+3*A)
        assert value and local_square(value, 3)
        return {'type': 's_one', 'radicand': str(value)}
    assert p not in (2, 3, 17), (D, A, p)
    assert val(D, p) % 2 == val(A, p) % 2 == 0
    dd, aa = unit(D, p), unit(A, p)
    assert dd and aa
    # Discriminant -2^12 * 3 * D^6 * A^6 is a unit after rescaling.
    assert (-2**12 * 3 * pow(dd, 6, p) * pow(aa, 6, p)) % p
    return {'type': 'smooth_genus_one_reduction', 'D_residue': dd,
            'A_residue': aa, 'Hasse_lower_bound_positive': p+1 > 2*isqrt(p)+1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'verification.json')
    args = parser.parse_args()
    tau, D, C, A, s, q = sp.symbols('tau D C A s q')
    e = (tau**2-D)/(tau**2+3*D)
    identities = {
        'near_one': sp.factor(e-1 + 4*D/(tau**2+3*D)),
        'near_minus_third': sp.factor(-3*e-1 + 4*tau**2/(tau**2+3*D)),
        'elliptic_cover': sp.expand((D*s*q)**2 -
            (D*s*s)*(D*s*s-D*A)*(D*s*s+3*D*A) -
            D**2*s**2*(q*q-D*(s*s-A)*(s*s+3*A))),
        'polynomial_twist': sp.factor(D*C*e*(tau**2+3*D)**2 -
            D*C*(tau**2-D)*(tau**2+3*D)),
    }
    for name, value in identities.items():
        assert value == 0, name
    quartic = D*(s*s-A)*(s*s+3*A)
    discriminant = sp.factor(sp.discriminant(quartic, s))
    assert discriminant == -2**12 * 3 * D**6 * A**6

    # These are all smooth unit quartics, including the residual nonsquare case
    # used in the proof.  Projective points at infinity are counted explicitly.
    finite_field = []
    for p in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        squares = Counter(y*y % p for y in range(p))
        minimum = p+1
        minimum_restricted = p+1
        count = restricted = 0
        for dd in range(1, p):
            for aa in range(1, p):
                total = squares[dd] + sum(squares[
                    dd*(x*x-aa)*(x*x+3*aa) % p] for x in range(p))
                assert total > 0
                assert (total-(p+1))**2 <= 4*p
                count += 1
                minimum = min(minimum, total)
                if squares[dd] == squares[-3*dd % p] == 0:
                    restricted += 1
                    minimum_restricted = min(minimum_restricted, total)
        finite_field.append({'p': p, 'quartics': count, 'minimum_points': minimum,
            'remaining_case_quartics': restricted,
            'remaining_case_minimum': minimum_restricted if restricted else None})

    # At 3, after the local square scaling D=17, unit tau implies e=2 mod 3,
    # C=1 mod 3, and the radicand at s=1 is 1 mod 3.
    three_residues = []
    for u in (1, 2):
        ee = (u*u-17)*pow(u*u+51, -1, 3) % 3
        value = 17*(1-ee)*(1+3*ee) % 3
        assert (ee, value) == (2, 1)
        three_residues.append({'tau': u, 'e': ee, 's_one_radicand': value})

    # Exact certificate for every possible bad reduction prime. Outside this
    # support the displayed quartic already has smooth genus-one reduction.
    cases = [
        ('fixed_e_minus_third', F(204,55)**2, F(1), F(204,55), F(0)),
        ('fixed_old_tau_one', F(204,61)**2, F(1), F(204,61), F(61,204)),
        ('fixed_old_tau_seventeen', F(204,101)**2, F(1), F(204,101), F(101,12)),
        ('different_input_class', 409*F(204,1001)**2, F(409), F(204,1001), F(1)),
    ]
    fixed = []
    branch_counts = Counter()
    for label, b, dd, t, tt in cases:
        assert prepared(b) and b == dd*t*t
        DD, CC = 17*dd, 17*(17-b)
        EE = (tt*tt-DD)/(tt*tt+3*DD)
        AA = EE*CC
        assert AA and DD > 0
        primes = sorted({2,3,17} | support(DD) | support(AA))
        certs = {}
        for p in primes:
            cert = local_certificate(DD, AA, p)
            branch_counts[cert['type']] += 1
            certs[str(p)] = cert
        fixed.append({'label': label, 'b': str(b), 'd': str(dd), 't': str(t),
            'tau': str(tt), 'D': str(DD), 'C': str(CC), 'e': str(EE), 'A': str(AA),
            'local_certificates': certs,
            'other_primes': 'smooth genus-one reduction',
            'real_place': 'positive leading coefficient'})

    # Invalid-preparation control: retain all three exceptional local square
    # conditions and all valuation/real inequalities, but give b a negative odd
    # valuation at 409. At tau=0 both D and A then have odd valuation -1. For
    # every integer v(s), the radicand valuation is either -1+4v(s) or -3,
    # both odd; neither factor can vanish. Infinity is also unavailable.
    bad_b = F(204,55)**2 / 409
    bad_d, bad_t = F(1,409), F(204,55)
    assert bad_b == bad_d*bad_t*bad_t
    assert not prepared(bad_b) and 0 < bad_b < 17
    assert all(local_square(bad_b,p) for p in (2,3,17))
    assert [val(bad_b,p) for p in (2,3,17)] == [4,2,2]
    bad_D, bad_A = 17*bad_d, -F(17,3)*(17-bad_b)
    assert val(bad_D,409) == val(bad_A,409) == -1
    assert not local_square(bad_D,409)
    invalid = {'b': str(bad_b), 'd': str(bad_d), 'tau': '0', 'prime': 409,
        'all_other_preparation_conditions': True, 'square_denominator': False,
        'valuation_D': -1, 'valuation_A': -1,
        'radicand_valuation_if_v_s_le_minus_one': '4*v(s)-1',
        'radicand_valuation_if_v_s_ge_zero': -3,
        'local_result': 'no projective Q_409 point'}

    # Exercise all valuation branches, including syntactically extracted square
    # representatives with both positive and negative valuations. No finite grid
    # is used as a substitute for the universal proof.
    grid = 0
    small_primes = [int(p) for p in list(sp.primerange(2, 80))]
    for bb in (F(204,55)**2, F(204,61)**2,
               409*F(204,1001)**2, 577*F(204,1193)**2):
        if not prepared(bb):
            continue
        for multiplier in (F(1), F(3,17), F(5,7), F(1,204)):
            dd = bb/multiplier**2
            DD, CC = 17*dd, 17*(17-bb)
            for a in range(-4, 5):
                for denominator in (1, 2, 3, 5, 7, 17):
                    tt = F(a, denominator)
                    EE = (tt*tt-DD)/(tt*tt+3*DD)
                    AA = EE*CC
                    assert AA
                    for p in small_primes:
                        cert = local_certificate(DD, AA, p)
                        branch_counts[cert['type']] += 1
                        grid += 1

    report = {
        'status': 'PASS',
        'scope': 'local solubility for all rational shared parameters; no rational simultaneous realization or variable saving asserted',
        'universal_symbolic_identities': list(identities),
        'quartic_discriminant': str(discriminant),
        'finite_field_checks': finite_field,
        'three_adic_residue_checks': three_residues,
        'fixed_global_counterexamples_local_certificates': fixed,
        'invalid_preparation_control': invalid,
        'native_source_guard_audit': native_guard_audit(),
        'exact_local_branch_grid': grid,
        'branch_counts': dict(sorted(branch_counts.items())),
        'verification_method': 'exact rational arithmetic, polynomial identities, finite-field enumeration, valuation and square-residue certificates',
        'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = args.output
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': report['status'], 'finite_field_quartics': sum(
        item['quartics'] for item in finite_field), 'local_grid': grid,
        'fixed_cases': len(fixed), 'certificate': str(output)}, indent=2))


if __name__ == '__main__':
    main()
