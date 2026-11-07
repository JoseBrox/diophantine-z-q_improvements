# Polynomial presentations of the integers over the rationals

Explicit polynomial constructions, degree and coordinate lower bounds, and reproducible exact computations.

For an integer polynomial (P(T,Y_1,\ldots,Y_m)), the rational input projection is

$$
\{t\in\mathbb Q:\exists(y_1,\ldots,y_m)\in\mathbb Q^m,
P(t,y_1,\ldots,y_m)=0\}.
$$

All variable counts include the input (T). Degree means total degree; coefficient height means the largest absolute integer coefficient after the fixed constants have been substituted.

## Read the papers

Each paper has a complete standalone LaTeX source and a ready-to-read PDF. The documents are organized by mathematical result.

| Result | PDF | LaTeX |
|:--|:--|:--|
| **Degree four is the lower bound:** degree and coordinate obstructions for (S)-integers in any number field | [Read](papers/lower_bounds/lower_bounds_20261107_v7.pdf) | [Source](papers/lower_bounds/lower_bounds_20261107_v7.tex) |
| **Best quartic in this collection:** 456 total variables, complete coefficient table | [Read](papers/quartic/quartic_20261107_v7.pdf) | [Source](papers/quartic/quartic_20261107_v7.tex) |
| **Fewest variables in this collection:** the 29-variable construction and the lower-degree 31-variable alternative | [Read](papers/few_variables/few_variables_20261107_v7.pdf) | [Source](papers/few_variables/few_variables_20261107_v7.tex) |
| **Finite algebraic choices:** explicit elimination with one additional coordinate, over every number field | [Read](papers/finite_algebra/finite_algebra_20261107_v7.pdf) | [Source](papers/finite_algebra/finite_algebra_20261107_v7.tex) |
| **Systems and field extensions:** combining equations without extra coordinates and an obstruction to using one formula in all fields | [Read](papers/systems_and_fields/systems_and_field_extensions_20261107_v7.pdf) | [Source](papers/systems_and_fields/systems_and_field_extensions_20261107_v7.tex) |
| **Elliptic point charts:** a sharp two-parameter bound for the specified elliptic point presentation | [Read](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.pdf) | [Source](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.tex) |

## Mathematical scope

The lower bounds, finite-algebra elimination theorem, equation-combination theorem, field-extension obstruction, elliptic chart obstruction, and stated algebraic and coefficient calculations are **unconditional**.

The assertions that the explicit 29-, 31-, and 456-variable polynomials have input projection exactly (\mathbb Z) are **conditional theorems**. They require four precisely stated arithmetic inputs: the elliptic group and index-height statements, the contact-height bound, pole obstruction and realization, and simultaneous prime patterns. The quartic also requires a stated weighted prime-selection input. The papers state these premises and prove the implications from them. The Lucas growth estimate and local index-depth estimates are proved directly. See [Arithmetic inputs](docs/arithmetic_inputs.md).

The computational checkers certify the finite algebra, polynomial identities, source transformations, and numerical bounds. They do not certify those global arithmetic premises. The repository therefore does not claim an independent unconditional proof that (\mathbb Z) is Diophantine in (\mathbb Q).

## Explicit constructions

These are the best representatives for the stated objectives **within this collection**; no global minimality in the number of variables is claimed.

| Construction | Total variables | Degree | Coefficient height |
|:--|--:|:--|:--|
| [Fewest variables](computation/few_variables/construction29/polynomial-29-preferred/) | **29** | (\le 2^{2093605}) | (\le 2^{\,2^{6280501}}) |
| [Smaller-degree alternative](computation/few_variables/construction29/polynomial-31-preferred/) | **31** | (\le 2^{180}) | (\le 2^{\,2^{184}}) |
| [Best quartic](computation/quartic/polynomial-456/) | **456** | **4, exact** | (64\cdot3^{105665812}), exact |

The quartic is the sum of squares of 426 listed quadratic residuals. It has primitive integer coefficients and 27,784 distinct nonzero coordinate monomials. Its fixed coefficient (S=3^{52832906}) is a constant, not a variable. A reciprocal-power chain with exponents (1,3,7,15,31), together with a seven-coordinate model for each of four pole certificates, gives the stated coordinate count.

The 29- and 31-variable polynomials are specified by exact finite expression graphs, determinants, and indexed products. Their degree and height entries are proved upper bounds; their enormous expanded monomial tables are not stored. The improved height bound uses

$$
h(x([n]P))\le n^2\log23534-\log574,
\qquad h_0(x([n]P))\le30n^2.
$$

The [data-format guide](docs/data_format.md) explains the two representations.

## Lower bounds and the use of several equations

Over any number field (K), an infinite input projection contained in a ring of (S)-integers requires at least three total coordinates. A single polynomial requires total degree at least four, and each essential coordinate must have individual degree at least two. The coordinate bound also applies to finite systems, with nonzero conditions and finite alternatives. Thus any quartic presentation of the integers, once its existence is established, is optimal in degree.

Several equations can have smaller individual degree. Over (\mathbb Q), a quadratic system becomes one quartic by summing its squares, with exactly the same coordinates. Over an arbitrary number field, (s) equations of degree at most (d) can be combined without adding coordinates into one equation of degree at most (\lceil\sqrt{s}\rceil d), using a specified anisotropic form.

A polynomial's meaning can change after extending the ground field. For the listed quartic, the exact specialization

$$
Q_{456}\!\left(\tfrac12\mathbf e_0+Y\mathbf e_{79}\right)
=Y^2+\frac{16081968676531905}{16}
$$

admits the nonintegral input (1/2) over (\mathbb Q(\sqrt{-16081968676531905})). The field paper proves a general bounded-degree version of this obstruction. It does not exclude a different defining polynomial for each number field.

## Reproduce the results

Python 3.10 or newer suffices for the final coefficient tables, both small-variable specifications, and the exact local and field calculations:

```bash
python3 scripts/verify.py
```

The command verifies the file manifest, restores losslessly compressed data in a temporary directory, rebuilds the final constructions, runs independent checkers, and compares the reconstructed polynomial data byte for byte. It leaves the published files unchanged. To include the complete baseline circuit replay, also install Node.js 18 or newer and run:

```bash
python3 scripts/verify.py --full
```

The [reproducibility guide](docs/reproducibility.md) describes the verification boundary and individual commands. [MANIFEST.json](MANIFEST.json) records file sizes and SHA-256 hashes. [data/results.json](data/results.json) records the numerical results and their precise status.

To rebuild all six PDFs with a standard TeX installation:

```bash
python3 scripts/build_papers.py
```

## Sources, attribution, and license

The arithmetic sources include [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), the cited OpenAI preprint, and the cited work of Sun. Source locations, commit pins, and the relevant literature are recorded in the papers and computational provenance files. The independent structural results cite their own primary references, including Siegel's theorem, Kollár's cubic unirationality theorem, and Faltings's theorem.

Original material in this repository is licensed under **Creative Commons Attribution 4.0 International**: [license text](LICENSE). Third-party material retains its existing notices and rights; see [attribution](THIRD_PARTY.md). [CITATION.cff](CITATION.cff) supplies citation metadata. The repository includes computer-assisted mathematical writing and verification; every mathematical claim is subject to the explicit hypotheses and proof supplied for it.
