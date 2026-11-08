# Polynomials with few variables

The explicit construction with the strongest bounds is [effective29](effective29/README.md): 29 total variables, degree less than $2^{166}$, and coefficient height at most $2^{2^{175}}$. Its fixed exponent $137731$ meets the proved effective threshold. The 27-variable family remains the smallest existence result; its sufficient defining coefficient threshold is ineffective. The source packages below remain available for the underlying arithmetic and finite-algebra proofs.

All counts include the input variable. Two principal constructions and their supporting arithmetic source are supplied:

| Construction | Total variables | Degree bound | Coefficients |
|:--|--:|:--|:--|
| [27-variable family](../../papers/few_variables27/few_variables27_cubic_20261108_v9.pdf) | 27 | $2^{158}$ | A computable family; every sufficiently large fixed odd coefficient exponent works. The sufficient threshold is ineffective. |
| [29-variable polynomial](../../papers/few_variables/explicit29_effective_20261108_v10.pdf) | 29 | $<2^{166}$ | Fully specified, with coefficient height at most $2^{2^{175}}$. |
| [29-variable source](../../papers/few_variables/few_variables_20261108_v8.pdf) | 29 | $2^{174}$ | Fully specified, with coefficient height at most $2^{2^{177}}$. |

Their rational input projections are the integers under the four arithmetic inputs identified in the [dependency paper](../../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf). The 27-variable proof additionally uses von Buhren's published uniform height theorem. Its ineffective additive constant prevents the present proof from specifying a numerical exponent known to suffice; it is not an additional conjecture.

## The 27-variable family

The complete module is [trace27_cubic_family](trace27_cubic_family/README.md). From the repository root, run:

```sh
python3 computation/few_variables/trace27_cubic_family/reproduce.py --anchor-exponent 137731
```

The command regenerates the sample rational source and finite-algebra specification, checks the nine point charts and scalar normalization independently, and verifies a degree bound uniform in the fixed coefficient parameter. The sample exponent is an algebraic reproducibility example, **not a certified sufficient exponent** for defining the integers.

The construction uses the square of the sum of four abscissa traces as its second comparison scale. A uniform height theorem makes these two scales sufficient. Nine direct elliptic charts use a cubic change of basis to represent each remaining square root by one monic quartic, with a proof that the selected component never vanishes. The finite algebra has nine quartic and three quadratic generators, maximum rank $2^{21}$, and eight finite source cases.

## The explicit 29-variable polynomial

The complete module is [effective29](effective29/README.md). Run `python3 computation/few_variables/effective29/reproduce.py` from the repository root. It reconstructs the certified fixed-exponent source and exact polynomial specification, verifies the effective three-scale construction and automatic point-chart conditions, and checks the degree and coefficient bounds independently. The source and specification are compared byte for byte with the distributed certificate.

## The supporting 29-variable source

The self-contained module is [forced_prime29](forced_prime29/README.md). Run:

```sh
python3 computation/few_variables/forced_prime29/reproduce.py
```

Independent checks verify the fixed-prime contact identity, retained source operations, finite numerical inequalities, monic relations, nonzero guards, quadratic zero/nonzero cases, degree majorant and coefficient majorant. The weighted companion-norm certificate concerns the bound annotations and leaves the polynomial unchanged.

Its [portable manifest](forced_prime29/manifest.json) records the dependencies and hashes. No earlier source directory or network access is required.

## Exact specifications and supporting results

All three modules use integer coefficient graphs and explicitly bounded determinant, trace, resultant and finite-product operations. These specify ordinary polynomials exactly; a full monomial expansion is unnecessary. The [finite-algebra paper](../../papers/finite_algebra/finite_algebra_20261107_v7.pdf) proves the one-coordinate elimination theorem.

The supporting mathematical papers include [aggregate trace heights](../../papers/trace_heights/aggregate_trace_height_20261108_v9.pdf), [square-root charts over quadratic extensions](../../papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf), [square abscissas](../../papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf), and [scalar normalization](../../papers/scalar_normalization/scalar_normalization_20261108_v9.pdf). Their unconditional statements and arithmetic hypotheses are distinguished in the papers.

The separate `verify_elliptic_chart.py` and `verify_quadratic_height.py` programs check the exact identities and constants supporting the elliptic-chart and height papers. All programs use Python 3.10 or newer and its standard library. The top-level `python3 scripts/verify.py` runs the complete collection in an isolated copy, preserving published files. See [Arithmetic inputs](../../docs/arithmetic_inputs.md) for the distinction between these finite certificates and the global arithmetic assumptions.
