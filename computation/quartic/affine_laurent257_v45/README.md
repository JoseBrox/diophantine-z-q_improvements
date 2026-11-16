# An explicit quartic in 257 variables

The [theorem](../../../papers/quartic/quartic257_20261116_v45.tex) specifies a family with 257 total rational variables, including the input, 229 quadratic rows, exact degree 4, integer content 1, and 3679 nonzero coordinate monomials. Every fixed integer N≥9682 is a sufficient defining parameter under precisely the explicit source's arithmetic premises. No additional abc hypothesis is used.

For every N≥1, with C=149^N, its exact coefficient height is

```text
max(484991541504995159662206970923766531374664106904986910720,149^(2N+2)).
```

The fixed coefficient dominates for N≤12; the parameter term dominates for N≥13. In particular, the explicit choice N=9682 gives coefficient height **149^19366**.

`transformation.json` contains the exact triangular affine map, Laurent coordinate weights, deleted square, all row multipliers, coordinate numbering, and fixed-parameter rescaling. The literal guard q1*w1=1 remains unchanged, and the complete rational zero sets are in input-preserving bijection for every nonzero C. The sufficient parameter N=9682 is therefore retained exactly.

`quadratic-family.json` and `polynomial-family.json` specify every coefficient. The producer uses sparse rational arithmetic; reproduction does not require optimization software. The independent checker reconstructs all source identities and the full quartic expansion without importing the producer. It also verifies the nonzero guard, fixed input, degree, content, row primitivity, and exact uniform support and height.

From the repository root:

```sh
python -B computation/quartic/affine_laurent257_v45/build.py --output /tmp/quartic257
python -B computation/quartic/affine_laurent257_v45/check.py --output /tmp/quartic257-check.json
```
