# Quartic with a packed semilocal anchor

This polynomial has **12,465 total variables**, including input 0, **degree 4**, and **130,427 nonzero monomials**. There are 11,908 quadratic residuals, each with weight one.

The anchor replacement saves eleven variables. Its exact rational projection equivalence is proved in `anchor-proof.tex`. The characterization of the full source as the integers retains the arithmetic hypotheses and review status of the upstream manuscript. This package does not independently prove those deep arithmetic inputs.

`polynomial.expanded.txt` is the complete coefficient table. Each line gives an integer coefficient followed by the variable indices of its monomial; repetition means exponentiation. `residuals.json.gz` gives the complete quadratic system, whose sum of squares is the polynomial.

Run from the repository root:

```sh
python3 -E -B research/optimization/quartic-anchor-packed-large/verify_anchor.py research/optimization/quartic-anchor-packed-large --baseline quartics/quartic-12504
```

The verifier first replays the pinned released certificate without changing its receipt, checks any subsequent rational eliminations and row operations, matches all six old anchor rows, checks private-variable incidence and the nonzero constant chain, and independently expands every coefficient. It imports no producer code. The copied `parent` files make the local transformation reproducible even when the parent was an intermediate variant. The pinned upstream package is still needed to replay its earlier certificate.

Nothing in this directory has been committed or submitted as a pull request.
