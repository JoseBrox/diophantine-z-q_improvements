# Polynomial presentations of the integers over the rationals

Defining-polynomial constructions under stated arithmetic hypotheses, unconditional structural theorems, and reproducible exact computations.

For an integer polynomial $F(X,Y_1,\ldots,Y_m)$, its rational input projection is

$$
\{x\in\mathbb Q:\exists\boldsymbol y\in\mathbb Q^m,\ F(x,\boldsymbol y)=0\}.
$$

**Every variable count includes the input.** Degree means total degree. Coefficient height is the largest absolute integer coefficient after fixed constants are substituted.

## Main results

| Construction | Total variables | Degree | Coefficient information |
|:--|--:|:--|:--|
| [Fewest variables: existence theorem](papers/few_variables27/few_variables27_nontorsion_20261109_v11.pdf) | **27** | $<2^{154}$ | Every sufficiently large fixed odd coefficient exponent works; the sufficient threshold is ineffective. |
| [Best quartic: existence theorem](papers/quartic_existence/quartic301_20261109_v11.pdf) | **301** | **4, exact** | $H(P_N)<2^{1520}80989^{4N+2}$; a sufficient numerical $N$ is not determined. |
| [Explicit construction with few variables](papers/few_variables/explicit29_nontorsion_20261109_v11.pdf) | **29** | $<2^{161}$ | $H(F)\le2^{\,2^{171}}$; the fixed exponent is $137731$. |
| [Explicit quartic](papers/quartic/quartic351_20261109_v11.pdf) | **351** | **4, exact** | Every coefficient is specified with $A=80989^{54929}$; $H(P)<2^{1791357}$. |

These are **proved conditional projection theorems**: under the arithmetic premises stated in their papers, the indicated polynomials have rational input projection exactly $\mathbb Z$. The quartics also retain the source's quantitative weighted prime-selection premise. The collection makes no claim of a global minimum in the number of variables.

The distinction between the two quartic rows is effectiveness. The **301-variable family** has a proved sufficiently-large-parameter theorem, but its proof does not identify a numerical sufficient parameter. The **351-variable quartic** has a certified fixed parameter and fully specified integer coefficients. The same distinction separates the 27-variable family from the explicit 29-variable polynomial. Fixed parameters are coefficients; they do not count as variables.

The 351-variable polynomial is the sum of squares of **323 quadratic equations**, has **4,990 nonzero coordinate monomials**, and has integer content one. Its largest coefficient has exactly **1,791,357 binary digits**. The 301-variable family uses **275 quadratic equations** and has **4,305 coordinate monomials** for every $N\ge27464$; that algebraic support threshold is not a sufficient parameter for its defining theorem.

The local construction combines tests of orders $1,10,40$ in factors

$$
1+\sum_j q_{m_j}^{\,2^j}D_j^{\,2^{j+1}}.
$$

At the relevant primes, their summands have distinct valuation classes. The valuation and trace argument gives all required orders at one common place. Existing formal-logarithm coordinates supply many fourth and eighth powers, keeping every defining equation quadratic. The proof includes denominator exceptions and simultaneous completeness.

For the few-variable constructions, the inherited simultaneous-realization argument supplies nonzero ordinates on its auxiliary elliptic curves. A single conic chart then suffices, and quadratic zero strata can be omitted. The papers prove this consequence from the retained restricted-converse and descent hypotheses; it is not inferred from a bare solvability assertion. The finite-algebra constructions retain **27 and 29 total coordinates** while reducing their degree and coefficient bounds.

## Read the papers

Each paper contains definitions, proofs, precise dependencies, and a ready-to-read PDF.

| Result | PDF | LaTeX |
|:--|:--|:--|
| Degree and coordinate lower bounds | [Read](papers/lower_bounds/lower_bounds_20261108_v8.pdf) | [Source](papers/lower_bounds/lower_bounds_20261108_v8.tex) |
| The 27-variable family, degree less than $2^{154}$ | [Read](papers/few_variables27/few_variables27_nontorsion_20261109_v11.pdf) | [Source](papers/few_variables27/few_variables27_nontorsion_20261109_v11.tex) |
| The 301-variable quartic family | [Read](papers/quartic_existence/quartic301_20261109_v11.pdf) | [Source](papers/quartic_existence/quartic301_20261109_v11.tex) |
| The explicit 29-variable polynomial, degree less than $2^{161}$ | [Read](papers/few_variables/explicit29_nontorsion_20261109_v11.pdf) | [Source](papers/few_variables/explicit29_nontorsion_20261109_v11.tex) |
| The explicit 351-variable quartic | [Read](papers/quartic/quartic351_20261109_v11.pdf) | [Source](papers/quartic/quartic351_20261109_v11.tex) |
| Local tests with different required orders: valuation proof and exact circuits | [Read](papers/local_tests/mixed_valuation_tests_20261109_v11.pdf) | [Source](papers/local_tests/mixed_valuation_tests_20261109_v11.tex) |
| A sharp degree-four threshold for finite scalar fibers over every number field | [Read](papers/scalar_heights/cubic_scalar_height_obstruction_20261109_v11.pdf) | [Source](papers/scalar_heights/cubic_scalar_height_obstruction_20261109_v11.tex) |
| Effective heights of elliptic sums with coprime indices | [Read](papers/coprime_sums/coprime_elliptic_sums_20261109_v11.pdf) | [Source](papers/coprime_sums/coprime_elliptic_sums_20261109_v11.tex) |
| Optimal degree-six square predicates over quadratic extensions | [Read](papers/square_predicates/quadratic_square_predicates_20261108_v10.pdf) | [Source](papers/square_predicates/quadratic_square_predicates_20261108_v10.tex) |
| Effective heights of arbitrary elliptic abscissa sums | [Read](papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) | [Source](papers/effective_sums/effective_elliptic_sums_20261108_v10.tex) |
| Aggregate elliptic trace heights | [Read](papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) | [Source](papers/trace_heights/aggregate_trace_height_20261108_v9.tex) |
| Square-root charts over quadratic extensions | [Read](papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf) | [Source](papers/quadratic_squares/quadratic_square_chart_20261108_v9.tex) |
| Square-abscissa charts for the elliptic subgroup | [Read](papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf) | [Source](papers/square_abscissa/square_abscissa_charts_20261108_v9.tex) |
| Scalar contact normalization | [Read](papers/scalar_normalization/scalar_normalization_20261108_v9.pdf) | [Source](papers/scalar_normalization/scalar_normalization_20261108_v9.tex) |
| Arithmetic dependencies and the corrected source argument | [Read](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) | [Source](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex) |
| Eliminating finite algebraic choices with one extra coordinate | [Read](papers/finite_algebra/finite_algebra_20261107_v7.pdf) | [Source](papers/finite_algebra/finite_algebra_20261107_v7.tex) |
| Combining equations and extending number fields | [Read](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf) | [Source](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.tex) |
| An obstruction to one-parameter elliptic point presentations | [Read](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.pdf) | [Source](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.tex) |
| Explicit elliptic height estimates | [Read](papers/elliptic_heights/elliptic_heights_20261108_v8.pdf) | [Source](papers/elliptic_heights/elliptic_heights_20261108_v8.tex) |
| Uniform formal-logarithm estimates | [Read](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.pdf) | [Source](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.tex) |

### Proof and replication dependencies

The following complete results supply the arithmetic arguments and exact source circuits used by the leading constructions.

| Result | PDF | LaTeX |
|:--|:--|:--|
| Two-scale quartic source and trace-height argument | [Read](papers/quartic_existence/quartic317_family_20261108_v9.pdf) | [Source](papers/quartic_existence/quartic317_family_20261108_v9.tex) |
| Three-scale quartic source and effective parameter | [Read](papers/quartic/quartic370_20261108_v10.pdf) | [Source](papers/quartic/quartic370_20261108_v10.tex) |
| Exact arithmetic source for the quartic families | [Read](papers/quartic/quartic389_20261108_v9.pdf) | [Source](papers/quartic/quartic389_20261108_v9.tex) |
| Baseline quartic arithmetic contract | [Read](papers/quartic/quartic392_20261108_v8.pdf) | [Source](papers/quartic/quartic392_20261108_v8.tex) |
| Few-variable arithmetic source and finite-algebra proof | [Read](papers/few_variables/few_variables_20261108_v8.pdf) | [Source](papers/few_variables/few_variables_20261108_v8.tex) |

## Arithmetic scope

The common arithmetic inputs are the specified elliptic group and index-height assertions, the contact-height theorem, pole obstruction and realization, and simultaneous prime patterns. The few-variable constructions retain the restricted-converse and descent hypotheses used in the source realization proof. The quartics additionally use the stated quantitative weighted prime-selection premise. The [arithmetic input guide](docs/arithmetic_inputs.md) separates these inputs from finite coefficient verification.

The aggregate trace-height argument applies [Von Buhren's Theorem 1.1](https://www.numdam.org/item/10.5802/jtnb.981.pdf) after verifying its geometric hypotheses. Its additive constant is ineffective. Enlarging a fixed coefficient absorbs that constant in the 27-variable and 301-variable existence theorems. The explicit 29-variable and 351-variable constructions instead use the proved effective height estimate for the two components of an elliptic sum.

## Structural results and number fields

The lower-bound paper proves that a single equation with infinite input projection contained in a ring of $S$-integers over a number field has **degree at least four**. Any finite system needs at least three total coordinates. In three coordinates, its equations must have a common irreducible factor of degree at least four; thus quadratic and cubic systems need at least four total coordinates. These statements include the specified open conditions and finite alternatives.

Over $\mathbb Q$, any finite quadratic system becomes one quartic by summing its squares, without adding coordinates. Over a fixed number field, $s$ equations of degree at most $d$ can be combined, without extra coordinates, into one equation of degree at most $\lceil\sqrt{s}\rceil d$.

For every quadratic extension $K/F$ of number fields, square membership has a complete **degree-six polynomial test using two input components and one auxiliary coordinate over $F$**. Degree six, and degree four in that auxiliary coordinate, are optimal in the stated class of equality-based definitions. Over $\mathbb Q(\sqrt2)$ the displayed polynomial has ten monomials and coefficient height seven. These are square predicates, not definitions of rings of integers.

The scalar-height paper proves a separate sharp degree threshold over **every number field**: no rational function of two variables with numerator and denominator of degree at most three is finite-to-one on any nonempty archimedean open set. A suitable quartic has finite fibers. This concerns arbitrary pairs; it does not rule out height comparisons on a restricted set of elliptic multiples.

For pairwise coprime elliptic indices and positive abscissas over a totally real field, the sum-height paper gives an effective bound with loss at most the finite-place height of the fixed base point. On the specified curve, adding a fixed abscissa when the number of summands is even removes the loss entirely. Coprimality is an additional hypothesis and is not assumed before it is established by the arithmetic construction.

No one unchanged existential formula can define rings of integers in every finite extension. The field paper proves this obstruction and gives an exact quadratic-field counterexample for the baseline quartic. It does not exclude a different defining polynomial for each number field.

## Reproduce the results

Python 3.10 or newer and its standard library suffice:

~~~sh
python3 scripts/verify.py --full
~~~

The verifier reconstructs the pinned source circuits, independently checks every quartic coefficient, rebuilds the 27- and 29-variable specifications, and checks their degree and coefficient bounds. It works in a temporary copy and leaves published inputs unchanged. The numerical 27-variable example is an algebraic reproducibility fixture and is **not** certified to exceed the ineffective defining threshold.

The [reproducibility guide](docs/reproducibility.md) gives individual commands and verification boundaries. The [data-format guide](docs/data_format.md) explains the complete coefficient tables and finite-algebra specifications. [MANIFEST.json](MANIFEST.json) records file sizes and SHA-256 hashes; [data/results.json](data/results.json) records exact bounds, effectiveness, and theorem scope.

To rebuild the PDFs with a standard TeX installation:

~~~sh
python3 scripts/build_papers.py
~~~

## Sources and license

The papers identify the underlying sources, including [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), the cited OpenAI preprint, Sun's theorem, Von Buhren's height theorem, and primary references for the structural results. Computational provenance pins source commits and exact input bytes.

Original project contributions are licensed under **Creative Commons Attribution 4.0 International**: [license](LICENSE). Third-party material retains its existing notices and rights; see [attribution](THIRD_PARTY.md). [CITATION.cff](CITATION.cff) provides citation metadata. The repository includes computer-assisted mathematical writing and verification; the hypotheses and proof of each theorem are stated in its paper.
