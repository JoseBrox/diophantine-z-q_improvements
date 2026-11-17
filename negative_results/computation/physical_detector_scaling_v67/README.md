# Exact obstructions with the physical detector weights

The formal units are u=x77 and v=x90. The two physical contact weights are q0=u and q1=u*v. `check_mapping.py` composes the complete retained coordinate maps and checks this normalization and the comparison-square identities. The original unit helper is u^(-1)*v^(-2); its proposed replacement is u^(-1)*v^2.

`model.json` specifies one literal rational reference row and three physical field-factor rows. `farkas_certificate.json` contains ten nonnegative integer multipliers proving infeasibility of the stated diagonal Laurent quadratization for both unit bases. Their sums are `0<=-12` and `0<=-20`, respectively. The obstruction has no weight bound and supplies no general lower bound on the number of variables.

```sh
python check.py --output certificate.json
python check_mapping.py --repo /path/to/repository --output mapping_certificate.json
```

Both checkers use only the Python standard library. The first reconstructs the actual factor components, verifies the nonzero selected terms, proves the necessary common row multipliers from full squares, and checks the exact integer certificate. When the source table is present, it also verifies its hash and the literal reference row. The second verifies every selected diagonal coordinate map through the source, parameter balancing, affine centering and Laurent transformations. No numerical optimizer or SMT solver is needed.

The independent full-coordinate audit additionally uses SymPy 1.14.0 and imports no construction code:

```sh
python check_mapping_independent.py --repo /path/to/repository --output mapping_independent_certificate.json
```

It composes all 198 source coordinates and checks 71 literal test, factor, product, trace and pole equations up to exact nonzero Laurent factors. The factor outputs have unit direction `(1,2j)` for detector `j`. These checks certify the stated transformations and selected consumer identities, without asserting a new defining polynomial or a general variable lower bound.

The independent physical-support expansion and integer-matrix audit is reproduced by `scripts/verify_v67.py` together with both coordinate checkers. Its [review](independent_review.md) and [certificate](independent_audit.json) pin the manuscript, source table, model and checker versions. The audit reconstructs the selected terms independently and checks all twenty coefficients in the exact inequality cancellation.
