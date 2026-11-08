# Polynomial presentations of the integers over the rationals

Defining-polynomial constructions under stated arithmetic hypotheses, unconditional structural theorems, and reproducible exact computations.

For an integer polynomial $F(X,Y_1,\ldots,Y_m)$, its rational input projection is

$$
\{x\in\mathbb Q:\exists\boldsymbol y\in\mathbb Q^m,\ F(x,\boldsymbol y)=0\}.
$$

**Every variable count includes the input.** Degree means total degree. Coefficient height is the largest absolute integer coefficient after the fixed constants are substituted.

## Main results

| Construction | Total variables | Degree | Coefficient information |
|:--|--:|:--|:--|
| [Fewest variables: existence theorem](papers/few_variables27/few_variables27_cubic_20261108_v9.pdf) | **27** | $\le 2^{158}$ | A sufficiently large fixed coefficient parameter exists; its threshold is ineffective. |
| [Best quartic: existence theorem](papers/quartic_existence/quartic317_family_20261108_v9.pdf) | **317** | **4, exact** | $H(P_N)<2^{1520}80989^{4N+2}$; a sufficient numerical $N$ is not determined. |
| [Explicit construction with few variables](papers/few_variables/explicit29_effective_20261108_v10.pdf) | **29** | $<2^{166}$ | $\le 2^{\,2^{175}}$ |
| [Explicit quartic](papers/quartic/quartic370_20261108_v10.pdf) | **370** | **4, exact** | $<2^{1791357}$ |

All four are **proved conditional projection theorems**: under the arithmetic premises stated in their papers, the indicated polynomials have rational input projection exactly $\mathbb Z$. No global minimality in the number of variables is claimed.

The **27-variable and 317-variable results are existence theorems for computable families**. Every sufficiently large fixed parameter gives a defining polynomial. The threshold depends on an ineffective additive constant in a published height theorem, so no displayed numerical parameter is certified to select a defining member. The parameters occur only in coefficients and do not increase the variable counts or degree bounds. The **29-variable and 370-variable constructions specify all their constants**.

The 27-variable family uses the sum of four elliptic traces to control all four integer labels with two comparison scales. A single chart, quartic in its auxiliary variable, represents every required square root in $\mathbb Q(\sqrt2)$, and finite-algebra elimination adds one coordinate. The 317-variable quartic combines the trace-height comparison with direct square-abscissa charts and the input map $51X^2+2504$.

The explicit 370-variable quartic uses the three scales $1,S_0^2,(S_0+S_1)^2$, where $S_0+S_1\sqrt2$ is the sum of four elliptic abscissas. An effective height theorem bounds all four integer labels using those two rational linear forms. The quartic is the sum of squares of **342 quadratic equations**. Its complete coefficient table has **5,837 nonzero coordinate monomials**, integer content one, and a largest coefficient with exactly **1,791,357 binary digits**. The fixed integer $80989^{54929}$ is a coefficient.

## Read the papers

Each paper has definitions, proofs, an explicit account of its dependencies, and a ready-to-read PDF.

| Mathematical result | PDF | LaTeX |
|:--|:--|:--|
| **Degree and variable lower bounds:** degree four is necessary for one equation; quadratic and cubic systems need at least four total coordinates | [Read](papers/lower_bounds/lower_bounds_20261108_v8.pdf) | [Source](papers/lower_bounds/lower_bounds_20261108_v8.tex) |
| **The 317-variable quartic family:** a proved existence theorem, exact quadratic system, and uniform coefficient estimate | [Read](papers/quartic_existence/quartic317_family_20261108_v9.pdf) | [Source](papers/quartic_existence/quartic317_family_20261108_v9.tex) |
| **The explicit 370-variable quartic:** rational projection and every coefficient | [Read](papers/quartic/quartic370_20261108_v10.pdf) | [Source](papers/quartic/quartic370_20261108_v10.tex) |
| **The 27-variable family:** a proved existence theorem with degree at most $2^{158}$ | [Read](papers/few_variables27/few_variables27_cubic_20261108_v9.pdf) | [Source](papers/few_variables27/few_variables27_cubic_20261108_v9.tex) |
| **The explicit 29-variable construction:** rational source, finite-algebra elimination, and coefficient bounds | [Read](papers/few_variables/explicit29_effective_20261108_v10.pdf) | [Source](papers/few_variables/explicit29_effective_20261108_v10.tex) |
| **Aggregate trace heights:** linear height comparisons, exclusion of constant abelian translates, and a number-field corollary | [Read](papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) | [Source](papers/trace_heights/aggregate_trace_height_20261108_v9.tex) |
| **Optimal square predicates:** degree six and degree four in the one auxiliary variable are minimal; an explicit test has coefficient height seven | [Read](papers/square_predicates/quadratic_square_predicates_20261108_v10.pdf) | [Source](papers/square_predicates/quadratic_square_predicates_20261108_v10.tex) |
| **Effective sum heights:** an all-place height comparison for sums of elliptic abscissas, with explicit constants | [Read](papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) | [Source](papers/effective_sums/effective_elliptic_sums_20261108_v10.tex) |
| **Square roots in quadratic extensions:** a single quartic chart over every number field, with one-variable square tests | [Read](papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf) | [Source](papers/quadratic_squares/quadratic_square_chart_20261108_v9.tex) |
| **Square-abscissa subgroup charts:** exact coverage of the nonzero integer multiples under the stated group hypothesis | [Read](papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf) | [Source](papers/square_abscissa/square_abscissa_charts_20261108_v9.tex) |
| **Scalar contact normalization:** exact finite-field avoidance, local squareclasses, and lower-degree normalization | [Read](papers/scalar_normalization/scalar_normalization_20261108_v9.pdf) | [Source](papers/scalar_normalization/scalar_normalization_20261108_v9.tex) |
| **Arithmetic dependencies:** source statements, finite avoidance, zero preparation, and the corrected arithmetic proof | [Read](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) | [Source](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex) |
| **Finite algebraic choices:** elimination with one additional coordinate over every number field | [Read](papers/finite_algebra/finite_algebra_20261107_v7.pdf) | [Source](papers/finite_algebra/finite_algebra_20261107_v7.tex) |
| **Systems and field extensions:** combining equations without extra coordinates, and the obstruction to one unchanged formula in all fields | [Read](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf) | [Source](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.tex) |
| **Elliptic point presentations:** a sharp two-parameter bound for the specified geometric presentation | [Read](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.pdf) | [Source](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.tex) |
| **Elliptic height bounds:** explicit quadratic growth and finite-product coefficient estimates | [Read](papers/elliptic_heights/elliptic_heights_20261108_v8.pdf) | [Source](papers/elliptic_heights/elliptic_heights_20261108_v8.tex) |
| **Elliptic logarithms:** local truncation estimates, real nonvanishing, and integer coefficient formulas | [Read](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.pdf) | [Source](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.tex) |

The [29-variable source paper](papers/few_variables/few_variables_20261108_v8.pdf) and [389-variable source paper](papers/quartic/quartic389_20261108_v9.pdf) remain as proof and replication dependencies. The [baseline quartic paper](papers/quartic/quartic392_20261108_v8.pdf) supplies the full arithmetic comparison construction used by the quartic proofs. Its [LaTeX source](papers/quartic/quartic392_20261108_v8.tex) and exact data remain available for independent verification.

## Arithmetic scope and effectiveness

The common arithmetic inputs are the specified elliptic group and index-height results, the contact-height theorem, pole obstruction and realization, and Sun's simultaneous prime-pattern theorem. The dependency paper derives the precise fixed-avoidance and zero-preparation statements used by the constructions and incorporates the corrected upstream arithmetic argument. The quartics also retain the quantitative weighted prime-pattern premise stated in their papers.

The aggregate height comparison uses [Von Buhren's Theorem 1.1](https://www.numdam.org/item/10.5802/jtnb.981.pdf). The paper verifies the hypotheses, including all abelian translates defined over the algebraic closure. This is an application of a published theorem, with an effective geometric slope and an ineffective additive constant. Enlarging a fixed coefficient absorbs that constant in the 27-variable and 317-variable existence proofs.

The lower bounds, optimal square predicates, effective elliptic sum-height theorem, quadratic square-root chart, aggregate height theorem for the specified points, finite-algebra elimination, equation combination, field-extension obstruction, elliptic presentation obstruction, upper-height estimates, logarithm estimates, and exact coefficient identities are unconditional mathematical statements. The square-abscissa subgroup identification uses the explicitly stated elliptic group hypothesis. A computational certificate verifies its listed finite assertions; it does not prove the global arithmetic inputs. See [Arithmetic inputs](docs/arithmetic_inputs.md).

## Several equations and number fields

Over $\mathbb Q$, a quadratic system becomes one quartic by summing its squares, with the same coordinates. Over a fixed number field, $s$ equations of degree at most $d$ can be combined without additional coordinates into one equation of degree at most $\lceil\sqrt{s}\rceil d$.

The unconditional lower bounds apply to every infinite input projection contained in a ring of $S$-integers over a number field. A single polynomial needs degree at least four, and any finite system needs at least three total coordinates. More sharply, in three coordinates the defining equations must have a common irreducible factor of degree at least four. Thus quadratic and cubic systems need at least four total coordinates, even with nonzero conditions and finite alternatives.

For every quadratic extension $K/F$ of number fields, square membership has a complete polynomial test of **total degree six with one auxiliary variable over $F$**, including zero. Degree six and degree four in that auxiliary variable are both minimal for this form of definition, even if finitely many polynomial equalities and finite alternatives are allowed. Over $\mathbb Q(\sqrt2)$ the displayed test has ten monomials and coefficient height seven. That height is optimal within the stated integral linear-multiplier family. The two inputs are the components of the element of $K$; all quantified coordinates range over $F$. These are square tests, not definitions of a ring of integers. With two auxiliary variables, two quadratic equations or one quartic suffice. The aggregate trace-height theorem also has a number-field version under its stated independence hypotheses.

A polynomial's input projection can change after a field extension. The field paper proves that no one unchanged existential formula defines rings of integers in every finite extension, and gives an exact quadratic-field counterexample for the published baseline quartic. This leaves open the possibility of a different defining polynomial for each number field.

## Reproduce the data

Python 3.10 or newer, with the standard library, suffices for the supplied exact computational certificates:

```bash
python3 scripts/verify.py --full
```

This checks the publication manifest, reconstructs the explicit constructions, verifies the fixed-coefficient families and their uniform bounds, and runs independent identity and coefficient checkers. The published files remain unchanged. The 27-variable family example at $L=137731$ is an algebraic reproducibility fixture; its parameter is **not** certified to exceed the ineffective defining threshold.

The [reproducibility guide](docs/reproducibility.md) gives individual commands and the verification boundary. The [data-format guide](docs/data_format.md) explains the complete quartic tables and finite polynomial specifications. [MANIFEST.json](MANIFEST.json) records sizes and SHA-256 hashes; [data/results.json](data/results.json) records exact counts, bounds, effectiveness, and theorem scope.

To rebuild the PDFs with a standard TeX installation:

```bash
python3 scripts/build_papers.py
```

## Sources and license

The papers identify the mathematical sources, including [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), the cited OpenAI preprint, Sun's theorem, Von Buhren's height theorem, and the primary references for the structural results. Computational provenance files pin source commits and exact input bytes.

Original project contributions are licensed under **Creative Commons Attribution 4.0 International**: [license](LICENSE). Third-party material retains its existing notices and rights; see [attribution](THIRD_PARTY.md). [CITATION.cff](CITATION.cff) provides citation metadata. The repository includes computer-assisted mathematical writing and verification; each theorem has its hypotheses and proof stated in its paper.
