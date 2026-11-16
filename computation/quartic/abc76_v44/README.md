# The 76-variable quartic

This package specifies the polynomial family proved in
[`quartic_abc76_20261116_v44.tex`](../../../papers/quartic_existence/quartic_abc76_20261116_v44.tex).
The family has 76 total rational variables, including the input, and is the
sum of 66 primitive integral quadratic squares. Its expanded polynomial has
1250 coordinate monomials, 1253 terms when powers of the coefficient parameter
`B` are separated, and coefficient height

```text
max(20828275368498373068800, B^2 + 275933278576697172).
```

The defining assertion uses ordinary rational `abc` and the exact retained
elliptic-group, simultaneous-prime, trace-height, and pole-realization inputs
specified in the paper. The integer coefficient `B` must be a sufficiently
large fixed odd integer. Its sufficient threshold remains ineffective;
`B = 81` is an algebraic fixture, not a certified defining member.

## Contents

- `quadratic-family.json`: every coordinate and all 66 primitive quadratic rows.
- `polynomial-family.json`: the full expanded coefficient table, in the same
  coordinate order, with powers of `B` recorded separately.
- `construction-report.json`: counts, coefficient height, and source binding.
- `build.py`: exact sparse-rational producer using only Python's standard library.
- `check.py`: independent SymPy reconstruction and algebraic checks; it does not
  import the producer.
- `independent-verification.json`: the expected complete verification report.

The input source is the current balanced 78-variable quadratic table at
`computation/quartic/abc78_balanced_v40/quadratic-family.json`, pinned by SHA-256
`30c877255a00abfa70207fcbc2efc59ed6331aee1246eb4f9d1995af9a55c76c`.
Exactly two cube-weight coordinates and their defining rows are removed.
Twelve rational rows are changed, and 54 named rows are preserved.

## Reproduction

Run these commands from the repository root. Python 3 and SymPy are required
for the independent checker.

```bash
python computation/quartic/abc76_v44/check.py
```

This checks the committed tables and compares the result byte for byte with
`independent-verification.json`. It also runs the producer in an isolated
temporary directory and compares all three generated tables byte for byte.

To write regenerated coefficient tables to a separate directory, pass a
directory to the producer:

```bash
python computation/quartic/abc76_v44/build.py --output /tmp/abc76-tables
```

To save the independent verification report elsewhere, pass a **file** to
the checker:

```bash
python computation/quartic/abc76_v44/check.py --output /tmp/abc76-verification.json
```

Calling the producer without `--output` replaces the package's three generated
coefficient/report files. The checker reads the committed coefficient tables
even when its report is written elsewhere.

## Verification scope

The independent check reconstructs the changed field equations in the basis
`1, sqrt(2)`, verifies the retained rows and every quartic coefficient, and
checks degree, content, support, coefficient height, the exact pole scaling,
the four distinct contact valuation classes, the contact identity and allowed
zero-contact pole stratum. Negative controls reject an inverted pole scaling,
an unscaled pole factor, and omission of the even-reciprocal-valuation condition.

The finite checks certify these algebraic statements. The proof that the
source defines the integers, including all zero strata, local extraction,
height soundness and completeness, is in the manuscript. The retained
infinite arithmetic inputs are not proved by the finite verification.
