#!/usr/bin/env python3
"""Verify a two-row parity obstruction to a specified Laurent compression.

Standard-library only. This reads the pinned Laurent source, reconstructs the
full replacement F=(U+V)/2, F'=(U-V)/(2c), and checks an integer-weight parity
certificate. It does not call a solver and does not assert global optimality.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'computation/quartic/seven_units193_v74/primitive/laurent-source.json'
ASSIGNMENT=ROOT/'computation/coauthor_audit_v78/H10-quartics/quartics/general-physical/assignment.json'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    raw=SOURCE.read_bytes();source=json.loads(raw)
    rows={r['name']:r for r in source['rows']}
    assignment=json.loads(ASSIGNMENT.read_bytes())
    assert assignment['groups'][3]==['A1','B3','A4']
    assert assignment['partial']==3 and assignment['high'][3]=='B0'
    # The first raw reciprocal occurs in a nontrivial bilinear point row.
    row=rows['new1.d_piF.0']
    monomials={tuple(t['monomial']):(int(t['coefficient']),t['parameterPower'],tuple(t['unitPower'])) for t in row['terms']}
    assert monomials[(201,205)]==(-1,0,(0,0))
    # F1=x205 is replaced by (U+V)/2. Hence the two quadratic monomials
    # s1*U and s1*V have the same c exponent and nonzero coefficients.
    reconstructed=defaultdict(Fraction)
    for t in row['terms']:
        terms={(t['parameterPower'],t['unitPower'][0],()):Fraction(int(t['coefficient']))}
        for i in t['monomial']:
            factors=[((205,),Fraction(1,2)),((229,),Fraction(1,2))] if i==205 else [((i,),Fraction(1))]
            new=defaultdict(Fraction)
            for (k,e,m),v in terms.items():
                for a,b in factors:new[k,e,tuple(sorted(m+a))]+=v*b
            terms=new
        for k,v in terms.items():reconstructed[k]+=v
    assert reconstructed[0,0,(201,205)]==Fraction(-1,2)
    assert reconstructed[0,0,(201,229)]==Fraction(-1,2)
    # A1 and A4 are raw reciprocals. B3 is a raw reciprocal too. The
    # physical odd pair c*A1^2-c^3*A4^2 becomes c*U*V; the even term
    # is c^2*B3^2. Checking scalar components is already sufficient.
    U,V,B,c='U','V','B','c'
    # Coefficient-level identity in Z[c,U,V]:
    # c*((U+V)/2)^2-c^3*((U-V)/(2c))^2 = c*U*V.
    out=defaultdict(Fraction)
    for sign in [1,-1]:
        # First square (U+V), minus second square (U-V).
        scale=Fraction(sign,4)
        out[1,('U','U')]+=scale
        out[1,('V','V')]+=scale
        out[1,('U','V')]+=scale*2*(1 if sign==1 else -1)
    out={k:v for k,v in out.items()if v}
    assert out=={(1,('U','V')):Fraction(1)}
    # Unknowns [w(s1),w(U),w(V),w(B),r_point,r_factor].
    # Row1/row2 enforce the two s1 monomials to be quadratic without
    # any unit factor. Row3/row4 enforce cUV and c^2 B^2 similarly.
    matrix=[
        [1,1,0,0,-1,0],
        [1,0,1,0,-1,0],
        [0,1,1,0,0,-1],
        [0,0,0,2,0,-1],
    ]
    rhs=[0,0,-1,-2]
    # Sum of all four equations is 0=1 mod2. This is a complete
    # certificate of impossibility for integral weights, independent
    # of any size bound or the supplied list of unit powers.
    multiplier=[1,1,1,1]
    reduced=[sum(a*row[j]for a,row in zip(multiplier,matrix))%2 for j in range(6)]
    reduced_rhs=sum(a*b for a,b in zip(multiplier,rhs))%2
    assert reduced==[0]*6 and reduced_rhs==1
    result={
      'schema':'hyperbolic-integral-weight-parity/v79','status':'PASS',
      'source':str(SOURCE.relative_to(ROOT)),'source_sha256':sha256(raw).hexdigest(),
      'source_row':'new1.d_piF.0',
      'factor_assignment':assignment['groups'][3],
      'replacement':'A1=(U+V)/2; A4=(U-V)/(2*c)',
      'required_factor_monomials':['c*U*V','c^2*B3^2'],
      'variables':['w(s1)','w(U)','w(V)','w(B3)','r_point','r_factor'],
      'integer_weight_equations':{'matrix':matrix,'rhs':rhs},
      'modulo_two_certificate':{'multiplier':multiplier,'left':reduced,'right':reduced_rhs},
      'also_covers':'Any changes of the odd factor exponent by an even integer and of the even square exponent by an even integer; any number of stored c powers.',
      'scope':'Only the specified full hyperbolic substitution with retained raw reciprocal point equation and termwise integral diagonal Laurent compilation to quadrics. Does not exclude different charts, nonlinear transformations, other equations, arithmetic restrictions, or a smaller quartic.'
    }
    target=args.report or Path(__file__).with_name('hyperbolic_parity_certificate.json')
    text=json.dumps(result,indent=2)+'\n'
    if args.report:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    else:assert json.loads(target.read_text())==result
    print(text)
if __name__=='__main__':main()
