# Exact separation of the nonzero guard fibers

This directory gives the current finite-algebra specifications for the 27-variable family and the explicit 29-variable construction. The input coefficient circuits remain pinned in `trace27_nontorsion/example_L137731` and `effective29_nontorsion/certificate`.

| Specification | Total variables | Degree upper bound | Coefficient-height bound |
|:--|--:|:--|:--|
| `active27` | 27 | 111295944630211471361441792, strictly below 2^87 | At the supplied numerical fixture only, log2 height <=217401420128398649581869203437, strictly below 2^98 |
| `active29` | 29 | 394212872202031272474705920, strictly below 2^89 | log2 height <=558578343639412157650224021485, strictly below 2^99 |

All variable counts include the input. A specification is a finite expression using integer polynomial operations and determinants; it determines every coefficient. The rank-sized matrices and full monomial lists are not materialized.

## Reproduction

From the repository root:

```sh
python3 computation/few_variables/active_elimination/build_active_specification.py \
  computation/few_variables/trace27_nontorsion/example_L137731/polynomial-specification.json \
  computation/few_variables/active_elimination/active27
python3 computation/few_variables/active_elimination/build_active_specification.py \
  computation/few_variables/effective29_nontorsion/certificate/polynomial-specification.json \
  computation/few_variables/active_elimination/active29
python3 computation/few_variables/active_elimination/check_active_specification.py \
  computation/few_variables/active_elimination/active27 \
  computation/few_variables/active_elimination/active29 \
  --output computation/few_variables/active_elimination/independent-verification.json
python3 computation/few_variables/active_elimination/check_active_degenerations.py \
  --output computation/few_variables/active_elimination/degeneration-certificate.json
```

The independent checker imports no builder code. It verifies every source coefficient dependency, the exponent of every pole generator in the guard, the weighted companion-column inequalities, and extraction of the point guard by substitution. It sums the bounds of all 262144 factors separately. The degeneration checker compares determinant expansion with Newton traces and checks the characteristic polynomial's gcd with its derivative in seven exact small-algebra examples.

## Mathematical scope

The elimination theorem preserves the rational projection of the guarded source without additional hypotheses. Its proof is in `papers/finite_algebra/active_finite_algebra_20261109_v15.tex`.

The assertions that the projections equal the integers retain the source arithmetic premises. The 27-variable degree bound is uniform in the odd fixed exponent, but its sufficient threshold is ineffective. Its numerical example at exponent 137731 is not certified to define the integers. The 29-variable construction uses that exponent with its proved effective source cutoff. Fixed exponents are coefficients and never additional quantified variables.
