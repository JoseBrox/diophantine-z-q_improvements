"""Independent exact audit of the abc91 -> abc89 rational projection.

No producer module is imported. The mathematical reconstruction is recorded
in abc89_projection_audit.md; this checks its complete literal interface.
"""
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json

ROOT = Path('/workspace/scratch/191d4e871efa/repo/computation/quartic')


def primitive(p):
    p = {k: Fraction(v) for k, v in p.items() if v}
    den = lcm(*(v.denominator for v in p.values()))
    p = {k: int(v * den) for k, v in p.items()}
    divisor = reduce(gcd, p.values())
    if p[min(p)] < 0:
        divisor = -divisor
    return {k: v // divisor for k, v in p.items()}


def poly(*terms):
    p = defaultdict(Fraction)
    for coefficient, monomial in terms:
        p[0, tuple(sorted(monomial))] += coefficient
    return primitive(p)


def get_rows(data):
    ids = {c['id']: c['sourceId'] for c in data['coordinates']}
    return {
        row['name']: primitive({
            (term['parameterPower'], tuple(sorted(ids[x] for x in term['monomial']))):
            Fraction(term['coefficient']) for term in row['terms']
        })
        for row in data['residuals']
    }


def uses(rows, identifier):
    return {name for name, p in rows.items()
            if any(identifier in monomial for _, monomial in p)}


old_path = ROOT / 'family_abc91_v19/quadratic-family-abc91-v19.json'
new_path = ROOT / 'family_abc89_v21/quadratic-family-abc89-v21.json'
expanded_path = ROOT / 'family_abc89_v21/polynomial-family-abc89-v21.json'
assert sha256(old_path.read_bytes()).hexdigest() == \
    'bbf424ee41a12729b2292812c118f7cc2a1a279762bc7232954a2ae477f869ab'
old, new = json.loads(old_path.read_text()), json.loads(new_path.read_text())
before, after = get_rows(old), get_rows(new)
changed, deleted = set(), set()

for j, q in enumerate((30010, 30032)):
    prefix = f'detector{j}.'
    r, u, v, s2, s4, s3 = q-1, q+1, q+2, q+3, q+4, 51000+j
    argument = 37 if j == 0 else 30030
    F0, F1, G0, G1 = q+5, q+6, q+7, q+8
    W0, W1, tau, b = q+9, q+10, q+11, q+12

    # Every occurrence of the removed q and the repurposed c,k is covered.
    assert uses(before, r) == {
        prefix+'deltaSquared.definition',prefix+'firstContactProduct.definition',
        prefix+'inverseContact.definition',prefix+'weight.definition'}
    assert uses(before, q) == {
        prefix+'firstContactProduct.definition', prefix+'weight.definition',
        prefix+'inverseWeightCubed.definition', prefix+'inverseWeightSquared.definition'}
    assert uses(before, u) == {
        prefix+'firstContactProduct.definition', prefix+'inverseContact.definition',
        prefix+'weight.definition'}
    assert uses(before, v) == {
        prefix+'inverseContact.definition', prefix+'weight.definition',
        prefix+'poleInput.definition'}

    assert before[prefix+'firstContactProduct.definition'] == poly((1,[q,r]),(-1,[u]))
    assert before[prefix+'inverseContact.definition'] == poly((1,[u,r]),(-1,[v]))
    assert before[prefix+'weight.definition'] == poly(
        (1,[v,v]),(-30,[v,u]),(273,[u,u]),(-820,[u,q]),(576,[q,q]),(-1,[v,r]))
    assert before[prefix+'inverseWeightCubed.definition'] == poly((1,[q,s4]),(-1,[s3]))
    assert before[prefix+'inverseWeightSquared.definition'] == poly((1,[q,s3]),(-1,[s2]))
    assert before[prefix+'inverseWeightFourthPower.definition'] == poly((1,[s2,s2]),(-1,[s4]))

    replacements = {
        'deltaSquared.definition': ('shiftedContactSquare.definition', poly(
            (1,[argument,argument]),(-2,[argument]),(-1,[r]))),
        'firstContactProduct.definition': ('contactFourthPower.definition', poly((1,[r,r]),(2,[r]),(-1,[u]))),
        'inverseContact.definition': ('contactQuotient.definition', poly(
            (1,[u,s2]),(-30,[r,s2]),(-1,[v,s2]),(-1,[r,s3]),(-1,[s3]))),
        'weight.definition': ('contactNormalization', poly(
            (1,[u,v]),(1,[v]),(244,[u]),(-820,[r]))),
        'inverseWeightCubed.definition': ('inverseWeightRelation', poly((1,[s3,s3]),(-1,[s2,s4]))),
        'poleInput.definition': ('poleInput.normalized.definition', poly((1,[s3,b]),(-1,[tau,tau]))),
    }
    for old_name, (new_name, p) in replacements.items():
        assert after[prefix+new_name] == p, new_name
        changed.add(prefix+old_name)
    assert prefix+'inverseWeightSquared.definition' not in after
    deleted.add(prefix+'inverseWeightSquared.definition')

    # The factors have exactly the old right hand sides, with lhs s4*T replaced
    # by s3*A. This applies to both field components, including conjugation signs.
    for k, identifier in enumerate((F0,F1,G0,G1)):
        name = prefix+f'factor{k//2}.{k%2}.reciprocal.definition'
        p = before[name]
        lhs = (0,tuple(sorted([s4,identifier])))
        assert lhs in p
        assert all(identifier not in m for key in p if key != lhs for m in [key[1]])
        wanted = dict(p)
        coefficient = wanted.pop(lhs)
        wanted[0,tuple(sorted([s3,identifier]))] = coefficient
        assert after[name.replace('.reciprocal.', '.scaled.')] == primitive(wanted)
        changed.add(name)
        assert uses(before, identifier) == {
            name, prefix+'product.0.definition', prefix+'product.1.definition'}

    assert before[prefix+'product.0.definition'] == poly((1,[F0,G0]),(2,[F1,G1]),(-1,[W0]))
    assert before[prefix+'product.1.definition'] == poly((1,[F0,G1]),(1,[F1,G0]),(-1,[W1]))
    assert after[prefix+'product.0.normalized.definition'] == poly((1,[F0,G0]),(2,[F1,G1]),(-1,[r,W0]),(-1,[W0]))
    assert after[prefix+'product.1.normalized.definition'] == poly((1,[F0,G1]),(1,[F1,G0]),(-1,[r,W1]),(-1,[W1]))
    changed.update((prefix+'product.0.definition',prefix+'product.1.definition'))
    assert uses(before, W0) == {prefix+'product.0.definition',prefix+'reciprocalTrace.definition'}
    assert uses(before, W1) == {prefix+'product.1.definition',prefix+'reciprocalTrace.definition'}
    assert uses(before, tau) == {prefix+'reciprocalTrace.definition',prefix+'poleInput.definition'}
    trace = poly((1,[W0,W0]),(-2,[W0,tau]),(-2,[W1,W1]))
    assert before[prefix+'reciprocalTrace.definition'] == trace
    assert after[prefix+'reciprocalTrace.definition'] == trace
    assert before[prefix+'poleInput.definition'] == poly((1,[v,b]),(-1,[tau,tau]))

assert len(changed)==24 and len(deleted)==2
for name,p in before.items():
    if name not in changed|deleted:
        assert after[name]==p,name
assert len(before)==79 and len(after)==77
assert len(new['coordinates'])==89
assert {c['sourceId'] for c in new['coordinates']} == \
    {c['sourceId'] for c in old['coordinates']}-{30010,30032}
assert all(len(m)<=2 for p in after.values() for _,m in p)

# Reconstruct the entire sum of squares independently from the literal rows.
expanded = defaultdict(int)
for row in new['residuals']:
    terms = row['terms']
    for left in terms:
        for right in terms:
            key = (left['parameterPower']+right['parameterPower'],
                   tuple(sorted(left['monomial']+right['monomial'])))
            expanded[key] += int(left['coefficient'])*int(right['coefficient'])
expanded = {key:value for key,value in expanded.items() if value}
literal = json.loads(expanded_path.read_text())
assert expanded == {(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient'])
                    for t in literal['terms']}
profiles=defaultdict(dict)
for (a,m),c in expanded.items():
    profiles[m][a]=c
assert len(expanded)==937 and len(profiles)==936
assert max(len(m) for _,m in expanded)==4
assert reduce(gcd,expanded.values())==1
assert {i for _,m in expanded for i in m}==set(range(1,90))
assert {tuple(sorted(p)) for p in profiles.values()}=={(0,),(1,),(0,2)}
assert profiles[()]=={0:797681,2:1}
constant_max=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
linear_max=max(abs(p[1]) for p in profiles.values() if set(p)=={1})
assert constant_max==4153456
assert 4*797681>=linear_max**2
assert 1831**2+797681<4153456<=1833**2+797681

report={
    'status':'PASS',
    'old_variables':91,'new_variables':89,'quadratic_rows':77,
    'changed_rows_verified':24,'deleted_rows_verified':2,'unchanged_rows_verified':53,
    'removed_source_coordinates':[30010,30032],
    'all_repurposed_and_scaled_coordinate_uses_accounted_for':True,
    'complete_sum_of_squares_reconstruction':True,
    'ordinary_monomials':936,'symbolic_terms':937,'degree':4,'content':1,
    'coefficient_height_for_positive_integer_B': 'max(4153456,B^2+797681)',
    'largest_absolute_linear_parameter_coefficient':linear_max,
    'odd_parameter_threshold_for_quadratic_height_formula':1833,
    'final_affine_coordinates':['R=r-1','U=u-1','V=v+29'],
    'old_source_sha256':sha256(old_path.read_bytes()).hexdigest(),
    'new_quadratic_sha256':sha256(new_path.read_bytes()).hexdigest(),
    'new_polynomial_sha256':sha256(expanded_path.read_bytes()).hexdigest(),
    'arithmetic_scope':'Exact rational projection preserving every unchanged point and pole coordinate. No new arithmetic hypotheses or completeness preparation.',
}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
