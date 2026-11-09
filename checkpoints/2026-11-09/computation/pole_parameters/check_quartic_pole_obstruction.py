#!/usr/bin/env python3
"""Exact finite certificate for a locally insoluble quartic pole equation.

All arithmetic is integral or rational. The accompanying proof treats
every m >= 1 and every p-adic argument; no finite search is substituted
for those quantified statements.
"""
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path
import json


def valuation(q, p):
    assert q
    numerator, denominator = abs(q.numerator), q.denominator
    answer = 0
    while numerator % p == 0:
        numerator //= p
        answer += 1
    while denominator % p == 0:
        denominator //= p
        answer -= 1
    return answer


p, c, a = 1013, 409, 204
trial_divisors = list(range(2, isqrt(p)+1))
assert all(p % d for d in trial_divisors)
assert p % 4 == 1 and gcd(c*a, p) == 1
assert pow(c, (p-1)//2, p) == p-1
assert pow(p-1, (p-1)//2, p) == 1
unit = c*a*a % p
assert pow(unit, (p-1)//2, p) == p-1
assert [c % m for m in (8, 3, 17)] == [1, 1, 1]
b1 = c*F(a, p)**2
assert b1 == F(17020944, 1026169) and 0 < b1 < 17
assert 17*b1.denominator-b1.numerator == 423929
assert [valuation(b1, q) for q in (2, 3, 17)] == [4, 2, 2]
assert b1.denominator == p*p and valuation(b1, p) == -2

# If v_p(v)=m, the reduced residue of bv^2 is unit*s^2 with
# s nonzero. Exhausting the finite residue field certifies the
# unique potential cancellation case in the infinite local proof.
assert all((1+unit*s*s) % p for s in range(p))
nonzero_squares = {s*s % p for s in range(1, p)}
assert len(nonzero_squares) == (p-1)//2
assert not nonzero_squares.intersection({unit*s % p for s in nonzero_squares})

# Symbolic cases are recorded exactly. Here j=v_p(v) and m>=1:
# j<m:  v(1+bv^2)=2*(j-m)<0;
# j>=m or v=0: v(1+bv^2)=0.
# The resulting RHS valuation is -2*m+2*v(1+bv^2), negative
# and even; its leading squareclass is always the nonsquare unit.
cases = [
    {'condition': 'j<m', 'innerValuation': '2*(j-m)',
     'rightHandSideValuation': '4*j-6*m', 'leadingSquareclass': 'nonsquare'},
    {'condition': 'j>=m or v=0', 'innerValuation': '0',
     'rightHandSideValuation': '-2*m', 'leadingSquareclass': 'nonsquare'}]

# Representative exact members additionally verify the fixed family
# identity; the proof of all m uses the same coprimality and unit c.
members = []
for m in (1, 2, 3, 10, 100):
    b = c*F(a, p**m)**2
    assert 0 < b < 17 and b.denominator == p**(2*m)
    assert [valuation(b, q) for q in (2, 3, 17, p)] == [4, 2, 2, -2*m]
    members.append({'m': m, 'valuationAtObstructionPrime': -2*m,
                    'reducedDenominatorExponent': 2*m})

report = {
    'status': 'PASS',
    'equation': 'Y^2=1+b*(1+b*v^2)^2',
    'extractionEquation': 'y^2=T^2+kappa*R*(1+R*s^2)^2',
    'provedExtraction': 'For odd v_p(R) and v_p(kappa)=0, a solution forces T!=0 and 2*v_p(T)<v_p(R).',
    'family': 'b_m=409*(204/1013^m)^2 for every integer m>=1',
    'firstInput': str(b1),
    'firstInputUpperBoundNumeratorDifference': 423929,
    'squareReducedDenominator': '1013^(2*m)',
    'preparedValuationsAt2_3_17': [4, 2, 2],
    'squareclassUnit': c,
    'squareclassResiduesModulo8_3_17': [1, 1, 1],
    'obstructionPrime': p,
    'primalityTrialDivisors': trial_divisors,
    'obstructionPrimeResidueModulo4': p % 4,
    'EulerExponent': (p-1)//2,
    'EulerPowerOf409': pow(c, (p-1)//2, p),
    'leadingUnitResidue': unit,
    'completeResiduesCheckedForCancellation': p,
    'valuationCases': cases,
    'projectiveInfinity': 'The leading coefficient b_m^3 has nonsquare leading unit, so neither point at infinity is rational over Q_1013.',
    'representativeFamilyMembers': members,
    'infiniteFamilyLimit': '0',
    'generalProofInPaper': 'Every finite nonempty set of fixed nonzero rational kappa values is excluded by the cyclotomic-order lemma, quadratic reciprocity, and the same local obstruction.',
    'scope': 'The finite certificate treats kappa=1; the paper proves failure for every finite set of fixed nonzero rational coefficients. The restricted comparison-prime-selected subfamily is not excluded. No defining-polynomial variable reduction is asserted.'}
destination = Path(__file__).with_name('quartic-pole-obstruction.json')
destination.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({key: report[key] for key in ('status', 'firstInput',
      'preparedValuationsAt2_3_17', 'obstructionPrime', 'EulerPowerOf409')}))
