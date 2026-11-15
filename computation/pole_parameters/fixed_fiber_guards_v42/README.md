# Fixed pole fibers and independent detector indices

The companion paper is
`papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex`.

It proves three statements:

1. For a prepared input, any rational second-pole witness with nonzero
   ordinate at one fixed rational conic parameter gives infinitely many
   witnesses at that same parameter. The associated elliptic twist has odd
   valuation at 17, so its rational torsion is exactly its two-torsion.
   Odd multiples preserve the prescribed abscissa square class.
2. Each native detector's extracted coefficient `d` is a positive scalar
   after the input, root abscissas, and comparison slope have been fixed.
   It is independent of auxiliary points and finite-algebra characters.
   Thus one shared rational parameter with nonzero second ordinates is
   enough to impose all native pole-stage guards without moving that
   parameter or earlier data. Additional polynomial guards must remain
   nonzero after the parameter is fixed.
3. From one actual guarded prepared tuple, the auxiliary cyclic indices can
   vary independently in a Cartesian product of infinite return sets,
   keeping all point-stage guards and preparation conditions. Differences
   are recomputed exactly, and rational half-point charts provide the
   retained square-abscissa coordinates. This does not assert independent
   variation or surjectivity of the resulting detector values.

No simultaneous global rational realization theorem or variable saving is
proved. The 24-variable general and 12-variable conditional constructions
remain targets contingent on that separate global assertion.

## Reproduce the checks

From the repository root, with Python 3 and SymPy available:

```sh
python3 computation/pole_parameters/fixed_fiber_guards_v42/check.py
```

To leave the committed certificate untouched:

```sh
python3 computation/pole_parameters/fixed_fiber_guards_v42/check.py --output /tmp/fixed_fiber_guards_v42.json
```

The checker uses exact rational and symbolic arithmetic. It:

- imports the four actual native builders and independently traverses
  their coefficient DAGs to check all extracted coefficient dependencies;
- verifies `b = d*t^2` by a separate multiplicative normal form;
- checks that comparison scales use only the fixed data, auxiliary roles
  enter the detector inputs, and finite source equations consist of point
  blocks and pole quadratics, with differences rationally recovered;
- verifies the duplication chart, pole-to-elliptic map, and first conic;
- verifies the mod-5 three-division obstruction and an auxiliary exact
  check of the exceptional square-twist torsion;
- checks six prepared examples, for each recovering rational witnesses
  from the first four positive odd multiples on the associated curve;
- records a countercontrol showing why positivity at only one character
  would not suffice if the extracted coefficient were not scalar.

The default circuit fixtures are general exponent `L=3`, explicit exponent
`L=20483`, and conditional shifts `B=3`. The paper's parity argument proves
the uniform coefficient-dependency statement; these finite checks audit
the native implementations at those parameters. The general and
conditional fixtures are not asserted to be defining members of their
ineffective families.

`verification.json` records the exact checks and hashes of the checker and
source builder. It does not certify the inherited arithmetic premises,
the universal density and recurrence proofs, or a common rational fiber.
