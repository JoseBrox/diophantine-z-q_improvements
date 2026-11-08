# The polynomial in 29 variables

The [few-variable paper](../../papers/few_variables/few_variables_20261108_v8.pdf) gives the construction and proof of an integer polynomial in **29 total variables**, including the input, with

$$
\deg F\le2^{174},\qquad
\max|\operatorname{coeff}(F)|\le2^{2^{177}}.
$$

Its rational input projection is $\mathbb Z$ under the four arithmetic inputs identified in the [dependency paper](../../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf). A fixed-prime scalar contact supplies the required elliptic-index bound.

## Exact construction and verification

The self-contained package is [forced_prime29](forced_prime29/README.md). From the repository root, run:

```sh
python3 computation/few_variables/forced_prime29/reproduce.py
```

Python 3.10 or newer with its standard library is sufficient. The command regenerates the guarded rational source and the one-polynomial specification. Independent checks verify the contact identity, unchanged source operations, finite numerical inequalities, monic relations, nonzero guards, quadratic zero/nonzero cases, degree majorant and coefficient majorant.

The specification uses an integer coefficient graph and explicitly bounded determinant, trace, resultant and finite-product operations. It defines one polynomial exactly. Its full monomial expansion is not stored. The coefficient-bound equality certificate verifies that weighted companion norms sharpen only the bound annotations, preserving the polynomial and its exact degree majorant.

The package's [23-file manifest](forced_prime29/manifest.json) records its portable dependency set and hashes. Its reproduction requires no earlier source directory or network access. The top-level `python3 scripts/verify.py` runs these checks in an isolated copy and preserves all published files.

## Supporting elliptic calculations

Two independent checkers accompany the separate topic papers:

| Checker | Mathematical result |
|:--|:--|
| `verify_elliptic_chart.py` | The exact point and finite-field identities used in the [elliptic-chart obstruction](../../papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.pdf). |
| `verify_quadratic_height.py` | The exact recurrence and numerical constants in the [quadratic elliptic-height estimate](../../papers/elliptic_heights/elliptic_heights_20261108_v8.pdf). |

Run them from the repository root:

```sh
python3 computation/few_variables/verify_elliptic_chart.py
python3 computation/few_variables/verify_quadratic_height.py
```

The [finite-algebra paper](../../papers/finite_algebra/finite_algebra_20261107_v7.pdf) proves the general one-coordinate elimination theorem. The [arithmetic-input page](../../docs/arithmetic_inputs.md) explains the precise distinction between the finite computational certificates and the global hypotheses of the Diophantine construction.
