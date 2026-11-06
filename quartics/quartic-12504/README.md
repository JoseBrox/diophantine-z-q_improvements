# The 12,504-variable quartic

This is the exact polynomial in [Version 2](../../quartic_12504.pdf).
Variable 0 is the rational input; the remaining 12,503 variables are rational witnesses.

| Quantity | Value |
| --- | ---: |
| Total degree | 4 |
| Nonzero monomials | 135,721 |
| Nonzero quadratic residuals | 11,939 |
| Largest absolute coefficient | 685783949153203534233601 |

Every coefficient has absolute value strictly below `2^80`. Every variable occurs.
The polynomial is the unweighted sum of the squares of the residuals.

## Literal specification

[`polynomial.expanded.txt`](polynomial.expanded.txt) contains the full integer
coefficient table. After its comment line, each line gives a coefficient followed
by a nondecreasing list of variable indices. Repeated indices indicate powers.
For example, `-6 0 2 2` means `-6 X_0 X_2^2`. The compressed copy has identical
uncompressed bytes. The table has 3,239,486 bytes and SHA-256
`7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca`.

The [verification receipt](verification.json) binds this table to its source and
transformation certificate. The [manuscript source](../../quartic_12504.tex)
proves the arithmetic characterization of the source system. The
[dependency inventory and reviews](../../docs/quartic-12504/README.md)
record the separate arithmetic, source-construction and algebraic checks.

## Reproduce the checks

See [reproducibility instructions](reproducibility/README.md) for the complete
source regeneration, mutation tests, certificate replay and coefficient expansion.
The exact-byte reproduction environment is Linux with CPython 3.12.14.

```sh
python3 -E -B quartics/quartic-12504/reproducibility/run.py \
  --output build/quartic-reproduction --stage-seconds 180
```

For a shorter exact algebraic replay, copy this directory to a writable location
and run `python verify_certificate.py .` there. That command writes a fresh
verification receipt. It checks the certificate and full polynomial, but does
not rerun the source-construction audit or prove the arithmetic theorems.

The named source uses reciprocal-coordinate logarithms with high precision 64,
beta precision 16, 41 outer comparisons, 24 anchor squarings and scalar order 48.
Its historical proposal metadata is preserved byte for byte. Acceptance is
documented by the accompanying reviews and final release checks; no earlier
source hash has been silently reassigned.
