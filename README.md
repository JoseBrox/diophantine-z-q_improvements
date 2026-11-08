# Polynomial presentations of the integers over the rationals

Explicit polynomial constructions under stated arithmetic hypotheses, unconditional degree and variable lower bounds, and reproducible exact computations.

For an integer polynomial $F(X,Y_1,\ldots,Y_m)$, its rational input projection is

$$
\{x\in\mathbb Q:\exists\boldsymbol y\in\mathbb Q^m,\ F(x,\boldsymbol y)=0\}.
$$

**Every variable count includes the input.** Degree means total degree. Coefficient height means the largest absolute integer coefficient after the fixed constants are substituted.

## Main results

| Construction | Total variables | Degree | Coefficient height |
|:--|--:|:--|:--|
| [Fewest variables in this collection](papers/few_variables/few_variables_20261108_v8.pdf) | **29** | $\le 2^{174}$ | $\le 2^{\,2^{177}}$ |
| [Best quartic in this collection](papers/quartic/quartic392_20261108_v8.pdf) | **392** | **4, exact** | $<2^{1791357}$ |

These are completed **conditional projection theorems**: under the arithmetic premises stated in the papers, each polynomial has rational input projection exactly $\mathbb Z$. Their algebraic specifications and numerical bounds are proved. No global minimality in the number of variables is claimed.

The 29-variable construction uses a fixed prime to force the required elliptic-index size through an existing scalar pole condition. Its remaining finite algebraic choices are eliminated with one coordinate. Weighted multiplication-operator norms give the coefficient estimate for the specified polynomial.

The quartic is the sum of squares of **364 quadratic equations**. Its complete table has **6,204 nonzero coordinate monomials**, primitive integer coefficients, and a largest coefficient with exactly **1,791,357 binary digits**. The fixed integer $A=80989^{54929}$ is a coefficient, not a variable.

## Read the papers

Each result has a standalone paper with definitions, proofs of the stated implications, an explicit account of its dependencies, and a ready-to-read PDF.

| Mathematical result | PDF | LaTeX |
|:--|:--|:--|
| **Degree and variable lower bounds:** degree four is necessary for a single equation; quadratic and cubic systems need at least four total coordinates | [Read](papers/lower_bounds/lower_bounds_20261108_v8.pdf) | [Source](papers/lower_bounds/lower_bounds_20261108_v8.tex) |
| **The 392-variable quartic:** fixed-prime divisibility, soundness, completeness, and every coefficient | [Read](papers/quartic/quartic392_20261108_v8.pdf) | [Source](papers/quartic/quartic392_20261108_v8.tex) |
| **The 29-variable construction:** the rational source, finite-algebra elimination, and quantitative bounds | [Read](papers/few_variables/few_variables_20261108_v8.pdf) | [Source](papers/few_variables/few_variables_20261108_v8.tex) |
| **Arithmetic dependencies:** exact source statements, finite avoidance, zero preparation, and the corrected arithmetic proof | [Read](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) | [Source](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex) |
| **Finite algebraic choices:** elimination with one additional coordinate over every number field | [Read](papers/finite_algebra/finite_algebra_20261107_v7.pdf) | [Source](papers/finite_algebra/finite_algebra_20261107_v7.tex) |
| **Systems and field extensions:** combining equations without extra coordinates, and the obstruction to one unchanged formula in all fields | [Read](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf) | [Source](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.tex) |
| **Elliptic point charts:** a sharp two-parameter bound for the specified elliptic point presentation | [Read](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.pdf) | [Source](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.tex) |
| **Elliptic height bounds:** explicit quadratic growth and finite-product coefficient estimates | [Read](papers/elliptic_heights/elliptic_heights_20261108_v8.pdf) | [Source](papers/elliptic_heights/elliptic_heights_20261108_v8.tex) |
| **Elliptic logarithms:** uniform local truncation estimates, real nonvanishing, and integer coefficient formulas | [Read](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.pdf) | [Source](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.tex) |

## Arithmetic scope

The common arithmetic inputs are the specified elliptic group and index-height results, the contact-height theorem, pole obstruction and realization, and Sun's simultaneous prime-pattern theorem. The dependency paper derives the precise fixed-avoidance and zero-preparation statements used in the 29-variable proof. It incorporates the corrected upstream arithmetic argument. The quartic additionally retains the quantitative weighted prime-pattern premise stated in its paper.

The lower bounds, finite-algebra elimination, equation combination, field-extension obstruction, elliptic chart obstruction, quadratic upper-height bound, logarithm estimates, and exact coefficient calculations are unconditional. The checkers certify finite identities and numerical claims; they do not prove the deep arithmetic premises. See [Arithmetic inputs](docs/arithmetic_inputs.md).

## Several equations and number fields

Over $\mathbb Q$, a quadratic system becomes one quartic by summing its squares, with the same coordinates. Over a fixed number field, $s$ equations of degree at most $d$ can be combined without additional coordinates into one equation of degree at most $\lceil\sqrt{s}\rceil d$.

The unconditional lower bounds apply to every infinite input projection contained in a ring of $S$-integers over a number field. A single polynomial needs degree at least four, and any finite system needs at least three total coordinates. More sharply, in three coordinates the defining equations must have a common irreducible factor of degree at least four. Thus quadratic and cubic systems need at least four total coordinates, even with nonzero conditions and finite alternatives.

A polynomial's interpretation need not survive a field extension. For the listed quartic, exact substitution gives

$$
P_{392}\!\left(\tfrac12\mathbf e_1+Y\mathbf e_{293}\right)=Y^2+D/16
$$

for a specified positive integer $D$. Consequently it accepts the nonintegral input $1/2$ over $\mathbb Q(\sqrt{-D})$. The field paper proves a general bounded-degree obstruction to a single unchanged existential formula defining all rings of integers. It does not exclude a different polynomial for each number field.

## Reproduce the data

Python 3.10 or newer, with the standard library, suffices for every supplied computational certificate:

```bash
python3 scripts/verify.py --full
```

This verifies the publication manifest, restores compressed coefficient tables in a temporary directory, reconstructs the complete quartic and the 29-variable specification, and runs the independent checkers. The published files remain unchanged. No network access or computer algebra system is required.

The [reproducibility guide](docs/reproducibility.md) gives individual commands and the verification boundary. The [data-format guide](docs/data_format.md) explains the complete quartic table and the finite expression for the 29-variable polynomial. [MANIFEST.json](MANIFEST.json) records file sizes and SHA-256 hashes; [data/results.json](data/results.json) records exact counts, bounds, and theorem scope.

To rebuild all nine PDFs with a standard TeX installation:

```bash
python3 scripts/build_papers.py
```

## Sources and license

The papers identify the mathematical sources, including [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), the cited OpenAI preprint, Sun's theorem, and the primary references for the structural results. Computational provenance files pin the source commits and exact input bytes.

Original project contributions are licensed under **Creative Commons Attribution 4.0 International**: [license](LICENSE). Third-party material retains its existing notices and rights; see [attribution](THIRD_PARTY.md). [CITATION.cff](CITATION.cff) provides citation metadata. The repository includes computer-assisted mathematical writing and verification; each theorem has the hypotheses and proof stated in its paper.
