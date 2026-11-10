# Thirteen variables with direct input comparison

The complete proof is [Direct elliptic index comparison](../../../papers/conditional_few_variables/direct_input13_20261110_v22.tex).
Every count includes the input. Both constructions retain the specified
elliptic group and index-height input, pole obstruction and nonzero
realization, and simultaneous prime-pattern input. Their sufficient odd
coefficient shifts are ineffective. Neither supplied shift-three fixture
is certified to define the integers.

| Variant | Additional weak rational abc exponent | Scale power | Total variables | Certified degree bound | Certified support bound |
|---|---:|---:|---:|---:|---:|
| `weak` | 121/100; ordinary Szpiro suffices | 6 | 13 | 11774654098433 | <2^508 |
| `abc` | 16/15; ordinary rational abc suffices | 4 | 13 | 11212784195585 | <2^507 |

Both weak inequalities follow from ordinary rational abc. No implication
from ordinary Szpiro to the stronger exponent 16/15 is asserted.
No modular-realization premise is needed by these two constructions.

## Rational source and final polynomial

The three elliptic point roles are A=nP, H=hP, and U=uP. The last
local test is `z(U)/z(H)-X`, comparing the index directly to the input.
The separate expression `beta=X^2+B` occurs in the second scale

    beta^d + (Tr x(A))^d,

with d equal to six or four. Its exact uniform height inequality is

    2*h(X) <= h(beta),  B>=3.

The resulting absorption coefficients are 14641/17538 and 8/9.
For each nonzero integer input, completeness uses n=X and U=[hn]P;
negative and even indices are allowed. The cases n=1 and n=-1 can
make comparison tests identically zero, which gives unit local factors.

There are twelve retained rational coordinates: the input, three point
pairs, one slope, and two pole-parameter pairs. Three finite point
quartics and two finite nonzero pole quadratics give an algebra of rank
256. One additional rational coordinate encodes its guarded rational
characters. The exact indexed determinant polynomial is called Q_B.

The final defining family is **F_B=X*Q_B**. This includes the integer
zero, whose elliptic index has no affine point chart. Multiplication
by X adds no variable, increases the degree by at most one, and preserves
the entire coefficient multiset and support size. Consequently the final
specification is `definition-polynomial-specification.json` in each
variant directory. Its referenced `active13/polynomial-specification.json`
specifies Q_B before this last multiplication.

## Exact verification

Each rational source has 1756 circuit nodes; its integer coefficient
graph has 752 nodes. The conversion audit checks three point quartics
and derivatives, two square clearings, and all 48 atomic guards.
The changed scale and direct target identities are also checked by
exact symbolic expansion, with B a formal coefficient.

An independent implementation reconstructs the complete rational
formulas in fifteen finite-field samples per variant. These finite
evaluations are supplementary bounded evidence. The general projection
and completeness are established by the paper's proof.

The bound checker imports no producer. It verifies the source
dependencies, companion-column inequalities, and all 64 finite-algebra
degree cases. A further exact check treats the input factor X and
computes the support bound. No determinant matrix or monomial expansion
is materialized. The ordinary support entries are upper bounds.

For the algebraic fixtures B=3, the upper bounds for the binary
logarithm of the coefficient one-norm are 28598607557817 (`weak`) and
27756172773305 (`abc`). Both are below 2^45. They are not coefficient
bounds for numerically certified defining members.

## Reproduction

Run from the repository root:

```sh
python3 computation/few_variables/direct_input13_v22/build_direct_input_source.py --shift 3 --scale-power 6 --output computation/few_variables/direct_input13_v22/weak/certificate
python3 computation/few_variables/direct_input13_v22/check_direct_input_source.py computation/few_variables/direct_input13_v22/weak/certificate --output computation/few_variables/direct_input13_v22/weak/independent-source-verification.json
python3 computation/few_variables/direct_input13_v22/build_direct_input_specification.py computation/few_variables/direct_input13_v22/weak
python3 computation/few_variables/direct_input13_v22/check_direct_input_bounds.py computation/few_variables/direct_input13_v22/weak --output computation/few_variables/direct_input13_v22/weak/independent-bound-verification.json

python3 computation/few_variables/direct_input13_v22/build_direct_input_source.py --shift 3 --scale-power 4 --output computation/few_variables/direct_input13_v22/abc/certificate
python3 computation/few_variables/direct_input13_v22/check_direct_input_source.py computation/few_variables/direct_input13_v22/abc/certificate --output computation/few_variables/direct_input13_v22/abc/independent-source-verification.json
python3 computation/few_variables/direct_input13_v22/build_direct_input_specification.py computation/few_variables/direct_input13_v22/abc
python3 computation/few_variables/direct_input13_v22/check_direct_input_bounds.py computation/few_variables/direct_input13_v22/abc --output computation/few_variables/direct_input13_v22/abc/independent-bound-verification.json
```

The source builder and compiler reuse the pinned point, pole, rational
arithmetic, and integer-conversion helpers in `trace27_nontorsion`.
Their hashes are recorded in the source. The complete finite-algebra
construction and its independent bound checker are in `active_elimination`.
These dependencies do not alter the stated additional height hypotheses.
