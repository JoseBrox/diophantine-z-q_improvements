# Quadratic reference covers and numerator charts

Exact certificates for
[Quadratic reference covers and weighted numerator charts](../../../papers/elliptic_charts/reference_covers_20261116_v47.tex).

The package proves algebraic presentations and their interfaces. **It does not specify a complete defining polynomial or an improved defining-variable count.**

## Contents

- `check.py` checks the three- and four-coordinate reference maps, both compositions, the compact-reference identities, four boundary points, homogeneous input scaling, weighted numerator/ratio identities, the Jacobi difference identity, exact original-trace recovery, the zero-height identity and specialized constants.
- `certificate.json` records those exact checks and the separate block counts.
- `independent_check.py` independently reconstructs the reference maps and uses an original-ideal Buchberger provenance calculation, including parameter-denominator checks.
- `independent-verification.json` records the independent reference-isomorphism and boundary audit. Its scope does not include a full combined defining polynomial.

## Reproduction

From the repository root, with Python and SymPy available:

```bash
python computation/elliptic_charts/reference_covers_v47/check.py
python computation/elliptic_charts/reference_covers_v47/independent_check.py
```

Both commands print receipts without modifying stored files. To generate a receipt at an explicitly chosen path:

```bash
python computation/elliptic_charts/reference_covers_v47/check.py --output /tmp/reference-covers.json
python computation/elliptic_charts/reference_covers_v47/independent_check.py --output /tmp/reference-covers-independent.json
```

The manuscript separates the zero-input and zero-height fibers. Its Kummer-image statement uses the explicitly retained group premise for the project curve. The asymmetric addition interface between the weighted numerator chart and the original fixed difference trace remains unresolved; the separate block counts must not be added as if that conversion were free.
