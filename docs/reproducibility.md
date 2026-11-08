# Reproducing the mathematical data

## Requirements

All computational verification uses **Python 3.10 or newer and its standard library**. The supplied data permit offline execution. A TeX installation is needed only to rebuild the papers; the document build uses `pdflatex`, AMS packages, `lmodern`, `mathtools`, `geometry`, `booktabs`, `longtable`, `microtype`, `xcolor` and `hyperref`.

## Complete verification

From the repository root, run:

```sh
python3 scripts/verify.py
```

The verifier checks the published file manifest, copies the computational inputs to a temporary directory, restores the compressed tables with hash checks, and runs the full computation there. Published inputs remain unchanged. Each failed equality, hash or bound stops the verification and identifies its stage.

The quartic stage reconstructs the pinned source coefficient table, rebuilds the 392-coordinate quadratic system and complete quartic, and independently checks every equation and coefficient. It also verifies the finite prime, congruence, index-size and coefficient-height certificates.

The 29-variable stage regenerates its rational source and finite-algebra specification, checks the exact scalar contact and the retained source semantics, recomputes the contact-height constant, and independently verifies all monic relations, guards, finite cases, degree bounds and coefficient bounds. The equality certificate checks that the weighted-norm refinement leaves the polynomial itself unchanged.

Supporting stages reproduce the elliptic-chart finite-field calculations, the quadratic elliptic-height constants, the anisotropic-form coefficient and residue-field calculations, and the imaginary-quadratic specialization of the 392-variable quartic. The uniform arguments supporting these finite calculations are proved in the corresponding papers.

## Running individual checks

Restore the four compressed quartic JSON files before running the individual quartic scripts:

```sh
python3 scripts/restore_data.py
```

Restoration verifies the exact uncompressed byte length and SHA-256 hash before writing each file. The restored JSON files are ignored by Git. The top-level verifier performs this step automatically in its temporary copy.

The following commands are run from the repository root:

```sh
python3 computation/quartic/build_quartic392.py
python3 computation/quartic/verify_quartic392.py
python3 computation/quartic/check_field_specialization392.py
python3 computation/few_variables/forced_prime29/reproduce.py
python3 computation/few_variables/verify_elliptic_chart.py
python3 computation/few_variables/verify_quadratic_height.py
python3 computation/field_extensions/verify_anisotropic_examples.py
```

The individual producers and checkers write their generated data or verification receipts to their own directories. Use the top-level verifier when all published files should remain byte-identical.

## Reading the verification results

A passing receipt verifies the finite assertions listed in that receipt. The coefficient tables and expression graphs are exact polynomial specifications. The 29-variable degree and coefficient bounds are verified from its finite-algebra expression without expanding the final polynomial, using the norm and degree inequalities proved in the paper.

The global arithmetic inputs needed to identify the rational projections with $\mathbb Z$ are stated in [Arithmetic inputs](arithmetic_inputs.md). The finite checkers do not independently establish those global theorems.

## Rebuilding the papers

```sh
python3 scripts/build_papers.py
```

The build runs LaTeX twice per paper and rejects missing references and overfull boxes. Inspect rendered pages after substantive changes. The published collection consists of nine topic papers:

| Topic | Paper |
|:--|:--|
| Degree and coordinate lower bounds | [Lower bounds](../papers/lower_bounds/lower_bounds_20261108_v8.pdf) |
| The polynomial with 29 variables | [Few variables](../papers/few_variables/few_variables_20261108_v8.pdf) |
| The quartic with 392 variables | [Quartic construction](../papers/quartic/quartic392_20261108_v8.pdf) |
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

The 29-variable package also has its own portable `manifest.json`, and the compressed quartic tables have a separate uncompressed-byte inventory. These serve distinct purposes: integrity of the published tree, portability of the finite-algebra module, and exact restoration of the compressed data.
