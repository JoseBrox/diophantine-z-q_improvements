# Quartic with 71 total variables

The companion paper is
[`quartic_abc71_20261116_v49.tex`](../../../papers/quartic_existence/quartic_abc71_20261116_v49.tex).
Its polynomial family has 71 total variables, including the input, degree four,
integer content one, and 1187 nonzero coordinate monomials. It is the sum of
59 primitive integral quadratic squares.

The fixed parameter `B` is an odd integer at least 81. The coefficient height
is exactly `B^2+1` throughout that range. The largest absolute coefficient
independent of `B` is 3554, and the complete expansion has 1190 terms when
different powers of `B` are stored separately. The parameter is a coefficient,
not a quantified variable.

Under ordinary rational abc and the elliptic-group, simultaneous-prime,
trace-height, and simultaneous congruent-twist premises stated in the paper,
every sufficiently large fixed odd `B` gives rational input projection exactly
the integers. The sufficient threshold is ineffective. In particular, the
test value 81 is not asserted to give a defining member.

## Exact specification

`quadratic-family.json` specifies the coordinate order and all 59 primitive
quadratic rows. `polynomial-family.json` is their full sum of squares.
Each term stores its integer coefficient, its power of `B`, and a sorted list
of coordinate identifiers, with repetition giving the exponent. An empty list
is the constant coordinate monomial.

`basis-transformation.json` records the fixed unimodular four-row reference
matrix and the subsequent constant-elimination operation with pivot row 40.
The producer uses these fixed operations; it does not run a basis search.
They preserve the complete common rational zero set. The construction report
records all counts, coefficient bounds, and the source-table authentication.

The three-coordinate reference chart exposes its two ordinate ratios affinely.
Its automatic unit permits both detector products to be recovered by quadratic
equations. A six-coordinate varying-difference chart includes tangent and
nonzero-abscissa two-torsion differences. The scaled trace is an affine
expression in an existing pair coordinate. All four product helpers and both
comparison squares occur in the count; no nonzero guard has been omitted.
The paper treats the zero input separately.

## Reproduction

From the repository root:

```sh
python -B computation/quartic/abc71_v49/build.py --output /tmp/abc71-v49
python -B computation/quartic/abc71_v49/check.py --tables /tmp/abc71-v49 --output /tmp/abc71-v49/check.json
python -B computation/quartic/abc71_v49/pair-check.py --output /tmp/abc71-v49/pair.json
python -B computation/quartic/abc71_v49/independent-pair-check.py --output /tmp/abc71-v49/fibers.json
```

The producer and full coefficient checker use Python's standard library.
The universal pair-identity checker additionally uses SymPy. The finite-field
checker uses the standard library.

`check.py` reconstructs every defining row with independent rational-pair
arithmetic, verifies the stored basis operations and their inverses, expands
the sum of squares independently, and checks the exact parameter coefficient
profiles. It imports neither the producer nor the retained source table.
Its zero-input fixture tests literal algebraic consistency only; it is not
a prepared arithmetic witness for an allowed positive `B`.

`pair-check.py` verifies twenty exact polynomial identities and fixed-data
checks, including zero ordinates, the two-torsion difference, the scaled
reciprocal helpers, and the zero-input specialization.
`independent-pair-check.py` compares the entire paired chart with an independent
elliptic addition implementation over seven small odd fields. It checks 880
coefficient fibers and 12080 solutions, including all 68 two-torsion-difference
fibers and their 744 solutions. The all-field proof is in the paper; the finite
checks are supplementary.

The three verification receipts are `independent-verification.json`,
`pair-certificate.json`, and `independent-pair-verification.json`.
These computations certify the displayed finite algebra and coefficients;
they do not certify the external arithmetic premises.
