#!/usr/bin/env python3
"""Check every source and transformed coefficient independently of build.py.

Source authentication uses the Git blob identity read through GitHub. Source
rows were reconstructed from the published manuscript; their sum of squares
is checked against that exact published polynomial.  The checker does not
import the producer and does not verify the arithmetic source theorem.
"""
from __future__ import annotations
import copy
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = 'f6a32cc2f7ebcc37a952c5ce737169608cfe27c2'
SCALED = {90, 91, 93, 117, 118, 120}
EXPECTED_M = {35:2, 36:1, 37:1, 38:1, 60:1, 63:1, 65:1}


def read_poly(terms: list[dict]) -> dict:
    out = defaultdict(int)
    for t in terms:
        a = t['parameterPower']
        m = tuple(sorted(t['monomial']))
        if not isinstance(a, int) or a < 0 or any(not 1 <= i <= 214 for i in m):
            raise ValueError('Invalid monomial.')
        out[a,m] += int(t['coefficient'])
    return {m:c for m,c in out.items() if c}


def expand(rows: list[dict]) -> dict:
    """Unordered term pairs, unlike the producer's ordered double loop."""
    result = Counter()
    for row in rows:
        terms = list(read_poly(row['terms']).items())
        for i, ((a,u),c) in enumerate(terms):
            result[a+a,tuple(sorted(u+u))] += c*c
            for (b,v),d in terms[i+1:]:
                result[a+b,tuple(sorted(u+v))] += 2*c*d
    return {k:v for k,v in result.items() if v}


def check_transport(old: list[dict], new: list[dict]) -> None:
    if [r['id'] for r in old] != list(range(1,189)) or [r['id'] for r in new] != list(range(1,189)):
        raise ValueError('Missing or permuted row.')
    for a,b in zip(old,new):
        left = Counter()
        for (p,m),c in read_poly(a['terms']).items():
            left[2*p+sum(i in SCALED for i in m),m] += c*149**p
        right = Counter()
        k = EXPECTED_M.get(a['id'],0)
        if b['divided_C_power'] != k or b['row_sign'] not in (-1,1):
            raise ValueError('Wrong row normalization.')
        for (p,m),c in read_poly(b['terms']).items():
            right[p+k,m] += c*b['row_sign']
        if dict(left) != dict(right):
            raise ValueError(f"Failed exact row identity {a['id']}")


def main() -> None:
    stages=[]
    def passed(name: str) -> None:
        stages.append(dict(name=name,status='PASS'))
    original_raw=(HERE/'source/polynomial214.json').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(original_raw)).encode()+b'\0'+original_raw).hexdigest()
    if blob != PIN:
        raise ValueError('The source polynomial does not match the published Git blob.')
    passed('Exact source polynomial authentication against the public Git blob')
    original=json.loads(original_raw)
    source=json.loads((HERE/'source/quadratic214.json').read_text())
    old=source['residuals']
    old_poly=read_poly(original['terms'])
    assert expand(old)==old_poly
    assert len(old)==188 and len(old_poly)==2920
    passed('Independent expansion of all 188 reconstructed source rows')
    old_profiles=defaultdict(dict)
    for (a,m),c in old_poly.items(): old_profiles[m][a]=c
    assert len(old_profiles)==2919
    a53=149**107
    tops=[(m,p) for m,p in old_profiles.items() if 2 in p]
    assert len(tops)==1 and tops[0][1]=={0:1,2:1}
    assert all(set(p)<={0,1} and abs(p.get(0,0))+abs(p.get(1,0))*a53 < a53*a53+1
               for m,p in old_profiles.items() if 2 not in p)
    passed('Original height A^2+1 for N>=53, separately from any defining threshold')
    system=json.loads((HERE/'quadratic-family-balanced214-v24.json').read_text())
    new=system['residuals']
    assert system['variables']==214 and system['inputCoordinate']==1
    assert set(system['scaled_coordinates'])==SCALED and 1 not in SCALED
    check_transport(old,new)
    passed('All 188 exact invertible coordinate and row transformations')
    assert all(max(len(m) for _,m in read_poly(r['terms']))<=2 and
               max(a for a,_ in read_poly(r['terms']))<=1 for r in new)
    assert all(math.gcd(*read_poly(r['terms']).values())==1 for r in new)
    for r in new:
        rp=defaultdict(dict)
        for (a,m),c in read_poly(r['terms']).items():rp[m][a]=c
        assert all(len(p)==1 for p in rp.values())
        g0=math.gcd(*(p.get(0,0) for p in rp.values()))
        g1=math.gcd(*(p.get(1,0) for p in rp.values()))
        assert math.gcd(g0,g1)==1 and math.gcd(g0,149)==1
    passed('Quadratic degrees and primitive integer rows after every C=149^N specialization')
    polynomial=json.loads((HERE/'polynomial-family-balanced214-v24.json').read_text())
    quartic=read_poly(polynomial['terms'])
    assert quartic==expand(new)
    passed('Independent full expansion and equality of every transformed quartic coefficient')
    profiles=defaultdict(dict)
    for (a,m),c in quartic.items(): profiles[m][a]=c
    assert len(quartic)==2924 and len(profiles)==2919
    assert max(len(m) for m in profiles)==4
    assert {i for m in profiles for i in m}==set(range(1,215))
    assert profiles[(1,1,1,1)]=={0:1}
    passed('All coordinates occur; exact degree four and integer content one')
    counts=Counter(tuple(sorted(p)) for p in profiles.values())
    assert counts=={(0,):2508,(1,):331,(2,):75,(0,2):5}
    assert all(p[0]*p[2]>0 for p in profiles.values() if set(p)=={0,2})
    passed('Exact support for every positive parameter, including all five mixed coefficients')
    K=31581660**28; J=5898050446009651968; A0=(J*K)**2
    assert profiles[(112,112,112,112)]=={0:A0}
    assert profiles[(109,109,117,117)]=={2:K}
    linear, other=0,0
    for p in profiles.values():
        if set(p)=={1}:
            assert p[1]**2<=A0*K; linear+=1
        else:
            assert abs(p.get(0,0))*K+abs(p.get(2,0))*A0<=A0*K; other+=1
    assert linear==331 and other==2588
    passed('All 2919 exact height-envelope inequalities and both attaining coefficients')
    assert 149**56 < J*31581660**14 <149**57
    assert A0<149**214+1 and K<149**108
    passed('Exact coefficient threshold N=57 and strict height improvement for all N>=53')
    corrupted=copy.deepcopy(new)
    corrupted[34]['terms'][0]['coefficient']=str(int(corrupted[34]['terms'][0]['coefficient'])+1)
    try:
        check_transport(old,corrupted)
    except ValueError:
        passed('Rejection of a deliberately corrupted transformed coefficient')
    else:
        raise AssertionError('Negative control was not rejected.')
    report=dict(schema='balanced214-independent-verification/v24',status='PASS',
        stages=stages,stage_count=len(stages),source_git_blob=PIN,
        source_sha256=hashlib.sha256(original_raw).hexdigest(),
        transformed_polynomial_sha256=hashlib.sha256((HERE/'polynomial-family-balanced214-v24.json').read_bytes()).hexdigest(),
        scope='Exact finite coefficient and projection-transport checks only. The proof of equivalence is in the companion paper. Arithmetic foundations, numerical defining threshold, and non-author acceptance are not certified.')
    (HERE/'independent-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f"PASS: {len(stages)} exact checks; all 188 rows and 2919 coefficient profiles.")

if __name__=='__main__': main()
