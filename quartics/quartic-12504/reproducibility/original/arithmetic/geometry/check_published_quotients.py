if not __debug__:
    raise RuntimeError('Run without -O; assertions are part of validation.')

"""Tiny exact check: published GR2006 quotient models give the required j's.

The modular identification is Theorem 4.2 of GR2006, not a conclusion of
this arithmetic checker. All computations below use rational arithmetic.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import argparse

ROWS = {
    30: [-43, -686, -2915, -1372, -172],
    42: [-43, 600, -986, -600, -43],
    70: [-43, 256, -130, -768, -387],
    105: [-43, 2, 505, 12, -1548],
}
PARAMETERS = {30: Q(1, 2401), 42: Q(32, 375), 70: Q(1, 225), 105: Q(5, 1029)}
# Independent published Table 3 Jacobian short-Weierstrass coefficients.
JACOBIANS = {
    30: [Q(-5762401, 3), Q(-27665272798, 27)],
    42: [Q(-129649, 3), Q(-90882286, 27)],
    70: [Q(-50401, 3), Q(-22628702, 27)],
    105: [Q(-1053721, 3), Q(-2163135238, 27)],
}

def quartic_j(row):
    a,b,c,d,e = map(Q, row)
    i = 12*a*e - 3*b*d + c*c
    j = 72*a*c*e + 9*b*c*d - 27*a*d*d - 27*b*b*e - 2*c*c*c
    disc = 4*i**3-j**2
    assert disc != 0
    return 6912*i**3/disc

def legendre_j(t):
    return 256*(1-t+t*t)**3/(t*t*(1-t)**2)

def orbit(t):
    return {t, 1-t, 1/t, 1/(1-t), t/(t-1), (t-1)/t}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    records = []
    for m,row in ROWS.items():
        j = quartic_j(row)
        a,b = JACOBIANS[m]
        assert j == 1728*4*a**3/(4*a**3+27*b*b)
        assert j == legendre_j(PARAMETERS[m])
        records.append({'m':m, 'quartic':row, 'j':str(j), 'legendre_parameter':str(PARAMETERS[m])})
    # Branch normalization: b210=infinity,b105=0,b70=1,b42=lambda,b30=mu.
    # Omit b30 -> j(lambda); omit b42 -> j(mu).
    # Omit b70 -> j(mu/lambda); omit b105 -> j((mu-1)/(lambda-1)).
    solutions=[]
    for lam in orbit(PARAMETERS[30]):
        for mu in orbit(PARAMETERS[42]):
            if lam == mu:
                continue
            if legendre_j(mu/lam) != quartic_j(ROWS[70]):
                continue
            if legendre_j((mu-1)/(lam-1)) != quartic_j(ROWS[105]):
                continue
            solutions.append([str(lam),str(mu)])
    assert solutions == [['2401','-343/32']], solutions
    result = {'schema':'published-quotient-check/v1', 'status':'PASS',
              'source':'Gonzalez-Rotger, JMSJ 58(4) (2006), Theorem 4.2 and Tables 2-3, pp938-939',
              'rows':records, 'normalized_branch_solutions':solutions,
              'scope':'Exact invariants and branch recovery from published modular identifications; not a substitute for the published identification theorem.'}
    if args.output:args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
