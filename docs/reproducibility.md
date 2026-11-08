# Reproducing the mathematical data

## Requirements

All computational verification uses **Python 3.10 or newer and its standard library**. The supplied data permit offline execution. A TeX installation is needed only to rebuild the papers; the document build uses `pdflatex`, AMS packages, `lmodern`, `mathtools`, `geometry`, `booktabs`, `longtable`, `microtype`, `xcolor` and `hyperref`.

## Complete verification

From the repository root, run:

```sh
python3 scripts/verify.py
```

The verifier checks the published file manifest, copies the computational inputs to a temporary directory, restores the compressed tables with hash checks, and runs the full computation there. Published inputs remain unchanged. Each failed equality, hash or bound stops the verification and identifies its stage. An optional receipt can be saved outside the distributed tree:

```sh
python3 scripts/verify.py --receipt /path/to/verification.json
```

The quartic stage reconstructs the pinned coefficient source and its 392-coordinate quadratic system. It then constructs the **370-variable explicit quartic** and the **317-variable quartic family**, including the 329-coordinate algebraic stage used in the derivation. Independent polynomial-dictionary checks compare every residual and every expanded coefficient. The three detector normalizations are checked after their affine changes of coordinates. The finite prime, congruence, index-size and coefficient-height certificates are also verified.

The **29-variable explicit construction with effective sum heights** is regenerated from its rational source. The checks cover its exact scalar contact, retained source semantics, contact-height constant, monic relations, guards, finite cases, degree bound and coefficient bound. Its weighted-norm certificate verifies the bound annotations without changing the polynomial.

The **27-variable family** is regenerated with the sample coefficient exponent `137731`. Its checks independently verify the nine cubic square-root charts, the scalar normalization and all 76,249 residue classes, the finite-algebra specification, and a degree bound uniform in the fixed coefficient exponent. The sample is supplied to make the algebraic computation reproducible. **No published certificate asserts that this particular exponent is sufficiently large to define the integers.** The theorem proves that all sufficiently large odd exponents work; its sufficient threshold is ineffective.

Supporting stages verify the complete degree-six, degree-ten and quartic square tests, the exact discriminant, the finite group calculation, the height-seven coefficient reduction, the effective elliptic sum-height identities, the general quadratic-extension square chart, the scalar normalization identity, elliptic-chart calculations, elliptic-height constants, anisotropic forms, and the stated quadratic-field specialization of the 392-variable arithmetic source. The corresponding papers prove the uniform arguments behind these finite calculations.

## Running individual checks

Restore the four compressed source tables before running the individual quartic scripts:

```sh
python3 scripts/restore_data.py
```

Restoration verifies the exact uncompressed byte length and SHA-256 hash before writing each file. The restored JSON files are ignored by Git. The top-level verifier performs this step automatically in its temporary copy.

Run the following commands in order from the repository root to reproduce the quartic constructions:

```sh
python3 computation/quartic/build_quartic392.py
python3 computation/quartic/verify_quartic392.py
python3 computation/quartic/build_quartic389.py
python3 computation/quartic/check_quartic389.py
python3 computation/quartic/build_quartic370.py
python3 computation/quartic/check_quartic370.py
python3 computation/quartic/verify_detector_normalizations.py
python3 computation/quartic/build_quartic329.py
python3 computation/quartic/check_quartic329.py
python3 computation/quartic/build_quartic317.py
python3 computation/quartic/check_quartic317.py
```

The few-variable constructions and supporting identity certificates can be checked independently:

```sh
python3 computation/few_variables/effective29/reproduce.py
python3 computation/few_variables/forced_prime29/reproduce.py
python3 computation/few_variables/trace27_cubic_family/reproduce.py --anchor-exponent 137731
python3 computation/quadratic_squares/check_quadratic_square_chart.py
python3 computation/scalar_normalization/check_scalar_normalization.py
python3 computation/square_predicates/check_square_predicates.py
python3 computation/square_predicates/check_height7_linear_multiplier.py
python3 computation/effective_sums/check_effective_elliptic_sums.py
```

Individual producers and checkers write their generated data or verification receipts to their own directories. Use the top-level verifier when all published files should remain byte-identical. The [quartic data description](../computation/quartic/README.md) and [few-variable data description](../computation/few_variables/README.md) identify the exact outputs.

## Scope of a passing check

A passing receipt verifies the finite assertions listed in that receipt. The coefficient tables and expression graphs are exact polynomial specifications. The few-variable degree and coefficient bounds are checked without expanding the enormous final polynomials, using the finite-algebra inequalities proved in the accompanying paper.

The global arithmetic inputs needed to identify the rational projections with the integers are stated in [Arithmetic inputs](arithmetic_inputs.md). The finite checkers do not independently establish those global inputs. Likewise, the 27-variable and 317-variable existence theorems use a published height theorem with an ineffective additive constant. Algebraic verification of their families does not certify a numerical sufficient coefficient parameter.

## Rebuilding the papers

```sh
python3 scripts/build_papers.py
```

The build runs LaTeX three times per paper and rejects missing references, multiply defined references, unresolved rerun requests and overfull boxes. Inspect rendered pages after substantive changes. The collection has twenty separately readable papers:

| Topic | Paper |
|:--|:--|
| Degree and coordinate lower bounds | [Lower bounds](../papers/lower_bounds/lower_bounds_20261108_v8.pdf) |
| Twenty-seven variables: existence and uniform degree | [27-variable family](../papers/few_variables27/few_variables27_cubic_20261108_v9.pdf) |
| Twenty-nine variables: fully specified coefficients and effective sum heights | [29-variable polynomial](../papers/few_variables/explicit29_effective_20261108_v10.pdf) |
| Twenty-nine-variable arithmetic source and finite-algebra proof | [Source and proof](../papers/few_variables/few_variables_20261108_v8.pdf) |
| Quartic with 317 variables: existence | [317-variable family](../papers/quartic_existence/quartic317_family_20261108_v9.pdf) |
| Quartic with 370 variables: fully specified coefficients | [370-variable quartic](../papers/quartic/quartic370_20261108_v10.pdf) |
| Quartic arithmetic source with 389 variables | [389-variable quartic](../papers/quartic/quartic389_20261108_v9.pdf) |
| Quadratic arithmetic source for the quartics | [392-variable source and proof](../papers/quartic/quartic392_20261108_v8.pdf) |
| Uniform aggregate trace heights | [Trace heights](../papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) |
| Optimal square predicates over quadratic extensions | [Degree-six square tests](../papers/square_predicates/quadratic_square_predicates_20261108_v10.pdf) |
| Effective heights of abscissa sums | [Effective sum heights](../papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) |
| A square-root chart over quadratic extensions | [Quadratic squares](../papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf) |
| Direct charts for the elliptic subgroup | [Square abscissas](../papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf) |
| Scalar contact normalization | [Scalar normalization](../papers/scalar_normalization/scalar_normalization_20261108_v9.pdf) |
| Elimination of guarded finite algebraic choices | [Finite algebra](../papers/finite_algebra/finite_algebra_20261107_v7.pdf) |
| Systems of equations and number fields | [Systems and field extensions](../papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf) |
| Limits of one-parameter elliptic charts | [Elliptic charts](../papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.pdf) |
| Quadratic upper bounds for elliptic heights | [Elliptic heights](../papers/elliptic_heights/elliptic_heights_20261108_v8.pdf) |
| Uniform formal logarithm truncations | [Elliptic logarithms](../papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.pdf) |
| Precise arithmetic dependencies | [Arithmetic dependencies](../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) |

Each PDF has an editable TeX source beside it. Regenerated PDF bytes may vary with the TeX distribution and timestamp settings even when the mathematical text is unchanged.

## File integrity

`MANIFEST.json` records the distributed file lengths and SHA-256 hashes. It excludes the manifest itself and generated verification/build files. After an intentional change has been verified and reviewed, refresh it with:

```sh
python3 scripts/update_manifest.py
```

The explicit 29-variable module has its own portable `manifest.json`, and the compressed quartic source tables have a separate uncompressed-byte inventory. These serve distinct purposes: integrity of the published tree, portability of that finite-algebra module, and exact restoration of the compressed source data.
