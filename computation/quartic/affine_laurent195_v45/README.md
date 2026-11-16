# A quartic in 195 variables

The [theorem](../../../papers/quartic/quartic195_20261116_v45.tex) gives 195 total variables, 175 quadratic rows, exact degree 4, integer content 1, and 2956 nonzero monomials for every fixed C=149^N with N≥1. Its exact coefficient height is

```text
max(126616122944180358034867798936,149^(2N+2)).
```

The fixed coefficient controls the height for N≤5; the parameter term controls it for N≥6. This is a coefficient crossover, not a certified sufficient defining parameter. The inherited sufficient defining threshold is ineffective. No additional abc hypothesis is used; all arithmetic premises of the pinned source remain explicit.

`transformation.json` specifies the triangular affine map, Laurent exponents and row multipliers, deleted square, coordinate numbering, and fixed-parameter scaling. The literal inverse guard is retained, so the complete rational zero sets are in input-preserving bijection. `quadratic-family.json` and `polynomial-family.json` specify all coefficients.

The producer uses sparse rational arithmetic. The independent checker reconstructs the source identities and complete expansion without importing the producer, and proves uniform row primitivity, support and coefficient height. Optimization/search software is unnecessary for reproduction.

From the repository root:

```sh
python -B computation/quartic/affine_laurent195_v45/build.py --output /tmp/quartic195
python -B computation/quartic/affine_laurent195_v45/check.py --output /tmp/quartic195-check.json
```
