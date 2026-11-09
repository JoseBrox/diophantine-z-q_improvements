# Source dependency: weighted finite-algebra elimination

This module is retained for exact reproduction of a general elimination theorem. The leading 27- and 29-variable specifications are in [active_elimination](../active_elimination/README.md).

This directory specifies two polynomials with the same rational input projections as the verified guarded sources. All variable counts include the input.

| Construction | Total variables | Degree bound | Coefficient bound |
|:--|--:|:--|:--|
| Sufficiently-large-parameter family | 27 | less than `2^151` | The sufficient parameter remains ineffective. |
| Fixed exponent `L=137731` | 29 | less than `2^157` | at most `2^(2^168)` |

The assertions that the projections equal the integers retain the source arithmetic hypotheses. The elimination theorem and bound calculations are unconditional algebraic statements.

The family example in `weighted27` uses `L=137731` only to supply a concrete coefficient specification. That exponent is **not certified** to exceed the ineffective threshold for the 27-variable theorem. The 29-variable source has its own effective proof certifying the same numerical exponent.

## Polynomial specification

For each separating element, form

`H(V) = det(I - V M_(G lambda)) = sum a_k V^k`.

For each `d=1,...,n`, let `H_d(V)=sum_(k=0)^d a_k V^k` and `g_d=Res(H_d,H_d')`, with Sylvester degrees `d,d-1`. The factor is `H_d(g_d U)^2 + sum_(k>d) a_k^2` for `d<n`; the last factor is `H_n(g_n U)`. Multiply over every specified selector and degree case. This is an integer polynomial in the retained coordinates and the one extra variable `U`.

`polynomial-specification.json` in each result directory contains the full integer coefficient graph, monic relations, guards, finite ranges, and polynomial recipe. Determinants and products are specified by exact finite operations; their enormous expanded monomial tables are not materialized.

## Reproduce

From the repository root, after the source verifiers have passed:

```bash
python3 computation/few_variables/weighted_elimination/build_weighted_specification.py computation/few_variables/trace27_nontorsion/example_L137731/polynomial-specification.json computation/few_variables/weighted_elimination/weighted27
python3 computation/few_variables/weighted_elimination/build_weighted_specification.py computation/few_variables/effective29_nontorsion/certificate/polynomial-specification.json computation/few_variables/weighted_elimination/weighted29
python3 computation/few_variables/weighted_elimination/check_weighted_specification.py computation/few_variables/weighted_elimination/weighted27 computation/few_variables/weighted_elimination/weighted29 --output computation/few_variables/weighted_elimination/verification.json
```

Only the Python standard library is required. The producer reconstructs weighted bounds from the source graph. The independent checker directly evaluates the defining integer sums and checks small finite algebras including complex residue factors, zero guards, inactive nilpotents, selector collisions, and degree drops. It recovers a rational character from every tested successful branch. These finite checks do not establish the global arithmetic premises.
