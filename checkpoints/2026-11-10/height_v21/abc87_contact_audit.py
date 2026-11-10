"""Independent exact contact, dependency, and coefficient audit for abc87."""
from collections import defaultdict
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import json

ROOT=Path('/workspace/scratch/191d4e871efa/repo/computation/quartic')


def multiply(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c


def factors(roots):
    a=[1]
    for r in roots:a=multiply(a,[-r,1])
    return a


def prime_support(n):
    n=abs(n); out=set();p=2
    while p*p<=n:
        if n%p==0:
            out.add(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.add(n)
    return out


theta=[-5,-2,-1,0,2,3,4,7]
assert len(set(theta))==8 and 0 in theta and 1 not in theta
assert sorted(2-x for x in theta)==theta
P=factors([1,4,9,36])
assert P==[1296,-1800,553,-50,1]
F=factors(theta)
composed=[0]*9
power=[1]
for coefficient in P:
    for i,x in enumerate(power):composed[i]+=coefficient*x
    power=multiply(power,[1,-2,1])
assert F==composed
assert set.union(*(prime_support(x-y) for x,y in combinations(theta,2)))=={2,3,5,7}
assert set.union(*(prime_support(1-x) for x in theta))=={2,3}
# r^2*((r+36/r)^2-50*(r+36/r)+481), in ascending powers.
assert [36**2,-50*36,72+481,-50,1]==P
# Exact residue-class separation of the three nonconstant columns.
for nu,c,h in product((1,3,5,7),range(4),range(2)):
    classes=[0,(-nu+2*c)%8,(-2*nu+4*h)%8,(-4*nu)%8]
    assert len(set(classes))==4
assert [-1+2*4,-2+2*2,-4+4*2]==[7,2,4]
assert 2*Q(11,2)-8==3 and Q(4,3)*2*Q(1,3)==Q(8,9)


def primitive(p):
    p={k:Q(v) for k,v in p.items() if v}
    den=lcm(*(v.denominator for v in p.values()))
    p={k:int(v*den) for k,v in p.items()}
    d=reduce(gcd,p.values())
    if p[min(p)]<0:d=-d
    return {k:v//d for k,v in p.items()}


def poly(*terms):
    p=defaultdict(Q)
    for c,m in terms:p[0,tuple(sorted(m))]+=c
    return primitive(p)


def rows(data):
    ids={c['id']:c['sourceId'] for c in data['coordinates']}
    return {row['name']:primitive({
        (t['parameterPower'],tuple(sorted(ids[x] for x in t['monomial']))):Q(t['coefficient'])
        for t in row['terms']}) for row in data['residuals']}


def uses(rows,i):
    return {name for name,p in rows.items() if any(i in m for _,m in p)}


old_path=ROOT/'family_abc89_v21/quadratic-family-abc89-v21.json'
new_path=ROOT/'family_abc87_v21/quadratic-family-abc87-v21.json'
polynomial_path=ROOT/'family_abc87_v21/polynomial-family-abc87-v21.json'
assert sha256(old_path.read_bytes()).hexdigest()=='30778238b1409e06e5856400122cdaea302241f9912a888e4b303a5f86e68c6a'
old=json.loads(old_path.read_text());new=json.loads(new_path.read_text())
before,after=rows(old),rows(new)
changed,deleted=set(),set()
for j,q in enumerate((30010,30032)):
    prefix=f'detector{j}.'
    R,Z,V,s2,s,s3=q-1,q+1,q+2,q+3,q+4,51000+j
    assert uses(before,V)=={prefix+'contactQuotient.definition',prefix+'contactNormalization'}
    assert uses(before,Z)=={prefix+'contactFourthPower.definition',prefix+'contactQuotient.definition',prefix+'contactNormalization'}
    assert uses(before,s)=={
        prefix+'inverseWeightRelation',prefix+'inverseWeightFourthPower.definition',
        prefix+'factor0.0.scaled.definition',prefix+'factor1.0.scaled.definition'}
    replacements={
        'contactFourthPower.definition':('reciprocalContact.definition',poly((1,[R,Z]),(1,[Z]),(-1,[R,R]),(35,[R]))),
        'contactQuotient.definition':('inverseContact.definition',poly((1,[R,s]),(1,[s]),(-1,[Z,Z]),(-24,[Z]))),
        'inverseWeightRelation':('inverseWeightCubed.definition',poly((1,[s3]),(-1,[s,s2]))),
        'inverseWeightFourthPower.definition':('inverseWeightSquared.definition',poly((1,[s2]),(-1,[s,s]))),
    }
    for name,(newname,p) in replacements.items():
        assert after[prefix+newname]==p
        changed.add(prefix+name)
    deleted.add(prefix+'contactNormalization')
    assert prefix+'contactNormalization' not in after
    for factor in (0,1):
        name=prefix+f'factor{factor}.0.scaled.definition'
        p=dict(before[name]);c=p.pop((0,(s,)))
        p[0,(s2,s2)]=p.get((0,(s2,s2)),0)+c
        assert after[name.replace('.scaled.','.inverseScaled.')]==primitive(p)
        changed.add(name)
    # The reciprocal identity itself excludes r=R+1=0: at R=-1 its lhs=-36.
    assert -(-1)**2+35*(-1)==-36

assert len(changed)==12 and len(deleted)==2
for name,p in before.items():
    if name not in changed|deleted:assert after[name]==p,name
assert len(after)==75 and len(new['coordinates'])==87
assert {c['sourceId'] for c in new['coordinates']}=={c['sourceId'] for c in old['coordinates']}-{30012,30034}
assert all(len(m)<=2 for p in after.values() for _,m in p)
expanded=defaultdict(int)
for row in new['residuals']:
    for a in row['terms']:
        for b in row['terms']:
            key=(a['parameterPower']+b['parameterPower'],tuple(sorted(a['monomial']+b['monomial'])))
            expanded[key]+=int(a['coefficient'])*int(b['coefficient'])
expanded={k:v for k,v in expanded.items() if v}
literal=json.loads(polynomial_path.read_text())
assert expanded=={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in literal['terms']}
profiles=defaultdict(dict)
for (a,m),c in expanded.items():profiles[m][a]=c
assert len(profiles)==918 and len(expanded)==919
assert max(len(m) for _,m in expanded)==4 and reduce(gcd,expanded.values())==1
assert {x for _,m in expanded for x in m}==set(range(1,88))
assert {tuple(sorted(p)) for p in profiles.values()}=={(0,),(1,),(0,2)}
assert profiles[()]=={0:797681,2:1}
assert max(abs(p[0]) for p in profiles.values() if set(p)=={0})==4153456
assert max(abs(p[1]) for p in profiles.values() if set(p)=={1})==4
assert 4*797681>=4**2
assert 1831**2+797681<4153456<=1833**2+797681

report={
    'status':'PASS','variables':87,'quadratic_rows':75,
    'ordinary_monomials':918,'symbolic_terms':919,'degree':4,'content':1,
    'changed_rows_verified':12,'deleted_rows_verified':2,'unchanged_rows_verified':63,
    'complete_dependency_interface_verified':True,'complete_sum_of_squares_reconstruction':True,
    'contacts':theta,'P4_coefficients_ascending':P,'F_coefficients_ascending':F,
    'contact_difference_prime_support':[2,3,5,7],
    'contact_pole_distance_prime_support':[2,3],
    'consumed_prime_cutoff':76176,
    'height_coefficient_under_abc':'1/3','global_absorption_coefficient':'8/9',
    'selected_prime_minimum_term_valuations':[7,2,4],
    'coefficient_height':'max(4153456,B^2+797681)',
    'odd_parameter_threshold_for_quadratic_height_formula':1833,
    'quadratic_sha256':sha256(new_path.read_bytes()).hexdigest(),
    'polynomial_sha256':sha256(polynomial_path.read_bytes()).hexdigest(),
    'scope':'Exact encoding of the new eight-contact arithmetic source, not a zero-set equivalence with the old89 contact polynomial. The accompanying proof checks the changed arithmetic constants and completeness.'
}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
