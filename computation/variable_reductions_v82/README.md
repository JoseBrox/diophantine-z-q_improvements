# The v82 continuation

This package develops the constructions and notes of **Gabe Conant with Astra 6.2**.
All variable counts include the input when there is an input coordinate.

| Package | Proved result | Limitation |
|---|---|---|
| [general](general/README.md) | Complete quartics in 163 and 179 variables, with exact physical maps and expanded coefficients | Retains the stated arithmetic premises; the 163-variable threshold is ineffective; the shared R-square register remains |
| [eds](eds/README.md) | Five-coordinate prepared elliptic divisibility subrelation; every nonzero integral quotient occurs | Does not identify an external rational input with that quotient |
| [abc](abc/README.md) | One-parameter sound genus-one criterion, everywhere-local solubility, and an exact prepared global counterexample | Actual detector rational realization remains unproved; no ten-variable definition is claimed |

The complete mathematical deliverables are the three TeX manuscripts named in
`manifest.json`. The [v82 proof guide](../../docs/results_20261120_v82.md)
states the deductions, dependencies, and unresolved steps.

Run the complete read-only gate from the repository root:

```sh
python -m pip install sympy==1.14.0 passagemath-pari==10.8.14
python -B scripts/verify_v82.py --report /tmp/v82-verification.json
```

The quartic producer is solver-free. The checker reconstructs the physical
rows from the published source and expands the sums of squares independently;
the main gate also regenerates the producer tables into a temporary directory.
The new PARI checks use algebraic rank bounds. Finite checks do not establish
the external arithmetic premises or the open global realization statement.

`manual_review.json` binds the separate proof review and explicitly records
its limits. `manifest.json` binds all package files and the three manuscripts.
Earlier review hashes and regression checks remain active. The added
`manual_review_followup.json` binds the quadratic-progression corollary,
corrected encoder reference, separate review, and final rendering. Exact
reverse edits authenticate the initially reviewed genus-one source; its
original review and TeX hashes have not been rewritten.
