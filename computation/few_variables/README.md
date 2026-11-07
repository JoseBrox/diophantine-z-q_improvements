# Exact 29- and 31-variable specifications

The complete proof is in the [small-variable paper](../../papers/few_variables/few_variables_20261107_v7.pdf). This directory contains its executable coefficient specifications, independent checkers, and exact finite data.

```bash
python3 construction29/reproduce_preferred.py
python3 verify_elliptic_chart.py
```

Both commands require only Python 3.10 or newer. The first reconstructs both rational source systems and both polynomial specifications, compares their bytes with the frozen objects, and independently checks the algebraic semantics, every monic finite-algebra relation, all denominator guards, branch factors, degree bounds, and coefficient bounds. The second independently checks the finite-field and point identities supporting the elliptic-chart paper.

| Specification | Total variables | Degree upper bound | Coefficient-height upper bound |
|:--|--:|:--|:--|
| `polynomial-29-preferred` | 29 | $2^{2093605}$ | $2^{2^{6280501}}$ |
| `polynomial-31-preferred` | 31 | $2^{180}$ | $2^{2^{184}}$ |

The source and specification files use finite expression graphs, multiplication matrices, determinants, and indexed finite products. They are exact polynomial definitions; no full expansion of the enormous final polynomials is claimed.

The `MANIFEST.json` allowlist pins the 37 computational dependencies and maps them to the current paper. Relative proof-location strings in the frozen source files are informational metadata and are never opened by the checkers. The relevant proofs are the input-map lemma, finite-algebra theorem, elementary Lucas lemma, exact index-depth proposition, and coefficient-bound section of the paper.

The implementation results are distinct from the four global arithmetic premises needed to conclude that the input projections equal the integers. See [Arithmetic inputs](../../docs/arithmetic_inputs.md).
