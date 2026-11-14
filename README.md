# Polynomial presentations of the integers over the rationals

Complete mathematical proofs and exact computational specifications for integer polynomials

$$F(X,Y_1,\ldots,Y_m)$$

whose rational input projection is the integers, under the arithmetic premises stated in each construction.

**Every variable count includes the input.** Degree is total degree. Coefficient height is the maximum absolute integer coefficient after fixed parameters have been substituted. The priorities are variable count, degree, then coefficient height. No global minimum is claimed.

## Current constructions — 14 November 2026

“None” in the additional-hypothesis column means **no additional conjecture beyond the explicitly retained arithmetic premises**. It does not mean that a finite coefficient computation has verified those premises. The full independent audit of the prime-pattern, pole-realization and modular-height foundations is not declared complete.

| Construction | Additional height hypothesis | Total variables | Degree | Coefficients and effectiveness |
|:--|:--|--:|:--|:--|
| [Fewest variables under inherited premises](papers/finite_algebra/unit_norm_20261114_v28.tex) | None | **25** | **< 2^56** | Every sufficiently large fixed odd exponent; sufficient threshold ineffective. |
| [Fewest quartic variables under inherited premises](papers/quartic_existence/quartic204_20261114_v27.pdf) | None | **204** | **4, exact** | 186 quadratic squares; **3,046 monomials**. Sufficient defining threshold ineffective. |
| [Fully specified general polynomial](papers/finite_algebra/unit_norm_20261114_v28.tex) | None | **27** | **< 2^59** | Fixed exponent **L=20483**; coefficient height **< 2^(2^72)**. |
| [Fully specified quartic](papers/quartic/explicit260_20261114_v27.pdf) | None | **260** | **4, exact** | **N=9682**; 232 quadratic squares; **3,704 monomials**; height **149^38730+1**. |
| [Few variables under weak abc](papers/finite_algebra/unit_norm_20261114_v28.tex) | Weak abc at **121/100**; ordinary Szpiro suffices | **13** | **≤ 155,568,385 < 2^28** | Sufficient odd shift ineffective. |
| [Lower degree under stronger weak abc](papers/finite_algebra/unit_norm_20261114_v28.tex) | Weak abc at **16/15**; ordinary rational abc suffices | **13** | **≤ 126,445,825 < 2^27** | Sufficient odd shift ineffective. |
| [Fewest quartic variables under abc](papers/quartic_existence/quartic_abc79_20261114_v27.pdf) | Ordinary rational abc | **79** | **4, exact** | 71 quadratic squares; **1,139 monomials**. Uses the stated simultaneous-twist theorem of Jaswal; sufficient shift ineffective. |

The general degree bounds are upper bounds for explicitly specified, unexpanded determinant polynomials, not exact degrees. The exact general degree majorants are **64,674,204,453,175,296** for 25 variables and **442,502,070,853,959,680** for the fully specified 27-variable polynomial. Their support bounds are respectively below **2^1282** and **2^1457**. The two 13-variable support bounds are below **2^306** and **2^303**.

The balanced 204-variable coefficient height is exactly

$$H(P_N)=\max\{(5898050446009651968\cdot31581660^{28})^2,\;31581660^{28}149^{2N}\}.$$

The second term dominates for **N≥57**. This is a coefficient threshold, **not** a sufficient defining threshold. No particular small member of this family is certified to define the integers.

For the 79-variable family, the exact height is `max(C*, B^2+C0)`, with both integers specified in its complete coefficient certificate. A [lower-coefficient 81-variable alternative](papers/pole_parameters/congruent_twist_poles_20261114_v27.pdf) uses the same new pole equations, has **929 monomials**, and height

$$\max(4153456,B^2+630511).$$

It has exactly the same rational input projection as the new 79-variable family at every fixed shift. The variable-first optimization prefers 79; the 81-variable alternative is retained for its smaller coefficients. The **B=3** tables are algebraic fixtures, not certified defining members.

Machine-readable current results are in [data/results_20261114_v28.json](data/results_20261114_v28.json). The [current guide](docs/results_20261114_v28.md) distinguishes the arithmetic assumptions, effective parameters, source dependencies, and review scope.

## Joint pole realization and reference-point restrictions in v29

The [new joint-realization theorem](papers/pole_parameters/joint_pole_realization_20261114_v29.tex)
replaces **2r retained pole parameters by 2** when the input and complement
square classes match. It includes the old and the congruent-number pole
systems, explicit witness maps, exact finite-choice encoding, and the precise
arithmetic hypotheses. This is a proved reduction on its compatibility locus,
**not a new 25- or 13-variable record**.

The existing 13-variable prime witnesses have incompatible first square
classes. At fixed scales, replacing them by matching classes leads to a
**genus-four curve** in that route, and generically to genus **9** for two
ten-contact blocks or **27** for three. The [reference-point theorem](papers/elliptic_charts/progression_density_20261114_v29.tex)
also proves density after arbitrary label-dependent infinite restrictions
on the reference indices. These results identify restrictions on a new
completeness proof, not an absolute variable lower bound.
See the [proof and verification guide](docs/joint_pole_realization_20261114_v29.md).

## General degree improvements in v28

The [complete TeX manuscript](papers/finite_algebra/unit_norm_20261114_v28.tex)
replaces the product over nonzero ranks by **one norm determinant**. A separate
completeness proof ensures that every required integer input admits witnesses
with every conjugate denominator nonzero. This is not an equivalence on every
old retained base tuple. A rank-four point basis, homogeneous elliptic
differences and invertible rescaling of the pole parameters lower the degree
further. Only the 25-variable family replaces the squared comparison scale by
`1+rho*T^2`; its ineffective sufficient exponent may consequently change.

The explicit 27-variable exponent **L=20483** and the conditional arithmetic
sources are unchanged. Their coefficient and degree bounds improve through
algebraic presentation and the justified restriction to the full-unit locus.
The 25- and 13-variable counts have not decreased. The exact [specifications,
code and certificates](computation/few_variables/unit_norm_v28) separate
universal polynomial identities from finite implementation examples.

## Quartic reductions and their proofs

The [204-variable construction](papers/quartic_existence/quartic204_20261114_v27.pdf) replaces two seven-field point blocks by two five-field reciprocal point pairs. Their differences are recovered rather than stored. One recovered index is allowed to be half-integral; the other is multiplied by two so that the Lucas equation still has integer labels. The nonzero fourth Lucas point is retained: deleting that condition would allow the trivial solutions with its index zero.

A [positive weighted trace-height theorem](papers/trace_heights/weighted_trace_20261114_v27.pdf) proves the height bound on the enlarged point domain, with weights 1 and R². It includes negative and repeated indices, torsion differences, and varying rational weights. The proof checks the exceptional abelian translates and the embedding hypotheses of von Buhren's published theorem. A quadratic-reciprocity lemma shows that the existing Gaussian prime congruences also annihilate the required half-generator in the residue groups. Thus completeness does not require a stronger prime-distribution premise.

The [complete five-coordinate reference chart](papers/elliptic_charts/compressed_reference_20261114_v27.pdf) gives the reduction from 81 to 79 variables and, independently, from 262 to 260. It proves both directions on every rational solution, including vanishing intermediate leading coefficients. The 260-variable replacement preserves the source input projection for **every fixed N**, so the effective parameter N=9682 is unchanged. The same exact replacement gives a 224-variable version of the older 226 family, retained as an additional application rather than a new best count.

The [congruent-twist pole equations](papers/pole_parameters/congruent_twist_poles_20261114_v27.pdf) are

$$e^2+bp^2=1,\qquad uv=e(1-b),\qquad u^2-v^2=bq^2.$$

Their negative-odd-valuation obstruction is elementary. The paper verifies the prepared-input application of **Jaswal, Hexagon 2611.00331v2, Theorem 1.2**, including the square input, the two square classes and the scaling of both elliptic points. The source is cited in the papers and [THIRD_PARTY.md](THIRD_PARTY.md). This use is separate from that paper's other height and prime-pattern claims; the complete external arithmetic audit is not represented as finished.

## Earlier improvements now integrated

The [triangular finite-algebra separation theorem](papers/finite_algebra/triangular_separation_20261113_v24.pdf) improves the general degree and coefficient-height bounds without changing any rational input projection or arithmetic premise. Its proof includes nonreal roots, vanishing radicands and inactive nonreduced components. The complete indexed specifications, bounds, and thirteen exact test examples are retained in [triangular_elimination_v24](computation/few_variables/triangular_elimination_v24).

The [212-variable additive construction](papers/quartic_existence/quartic212_20261113_v25.pdf), [81-variable reciprocal construction](papers/quartic_existence/quartic_abc81_20261113_v25.pdf), [all-point trace theorem](papers/trace_heights/trace_on_all_points_20261113_v25.pdf), and [214-variable coefficient balancing](papers/quartic/coefficient_balancing_20261113_v24.pdf) are retained as proved predecessors and exact reconstruction dependencies. The pinned upstream 214 numerical source is included with its attribution and source hashes. It is not silently replaced by a newer upstream revision.

The [product-height theorem](papers/elliptic_heights/product_height_20261113_v23.pdf) characterizes equality by a common 2-adic valuation of the nonzero elliptic indices, and the [local-precision paper](papers/local_tests/height_precision_20261113_v23.pdf) supplies the earlier 49/13/25 improvement under the stated source inputs. Their [Sun and PR30 audit](docs/audits/sun_pr30_20261113.md) retains its explicit outstanding source checks.

## Correction and review scope

The printed v26 reference-chart table omitted

$$(171357/235298+(2519877/7529536)\sqrt2)fS.$$

Without this term one of the required polynomial identities fails. The [v27 erratum](docs/audits/reference_chart_correction_20261114_v27.md) records the finding and repair. The corrected equations have been authenticated against all six original component rows, and all five ideal-membership certificates, two converse identities, and exceptional-case calculations have been checked exactly. The current 79-variable coefficient table is newly reconstructed from those corrected equations; no byte comparison with unavailable earlier v26 coefficient files is claimed.

Independent **implementations** check the algebra and coefficients. They are not independent non-author mathematical reviews. Passing code, PDF builds and manifests do not certify the external arithmetic premises, complete source coverage, or a numerical defining threshold. Historical preparation receipts retain their original dates and limitations; the v27 integration records describe the unchanged earlier computations; the v28 checks and current CI describe the new general constructions.

## Reproduction

Use **Python 3.12** for the byte-pinned legacy suite, and **SymPy 1.14.0** for the additional symbolic checks. The new coefficient producers and most checkers use only the standard library. From the repository root:

```sh
python -m pip install sympy==1.14.0
python -B computation/pole_parameters/joint_realization_v29/check.py
python -B scripts/verify_v28.py
python -B scripts/verify_release_v27.py
python -B scripts/verify.py --full
```

The v28 verifier authenticates nineteen inputs, reconstructs all four general specifications and their bounds, and independently checks the published certificates. The earlier cumulative verifier checks all v23–v27 improvements and authenticates the native general-polynomial sources. The separate legacy verifier checks the existing **126 stages**, source provenance, and the publication manifest. Optional PARI rank checks remain separately requested by `--with-pari`; they are not implied by `--full`.

The v28 result is supplied as a complete TeX manuscript; it was compiled and visually reviewed without adding a new PDF. Every earlier PDF has its complete TeX source beside it. `scripts/build_release_v27.py --build-pdfs` rebuilds the current proof set and records its source/PDF hashes; `scripts/update_manifest.py` records the distributed files. PDF hashes from older local preparation receipts are historical outputs, not substitutes for the current build record.

## Other established results and retained sources

The subject directories also retain finite-algebra guards, effective elliptic sums, formal logarithms, contact-height estimates, local counterexamples to proposed pole simplifications, degree and coordinate lower bounds, and number-field reductions. The [arithmetic inputs](docs/arithmetic_inputs.md), [legacy reproducibility guide](docs/reproducibility.md), and [data format](docs/data_format.md) describe the pinned pre-v27 sources; numerical best-count statements in those historical source documents are superseded by the current table above. No general positive theorem or counterexample for rings of integers of arbitrary number fields is claimed here.

Original project contributions are under CC BY 4.0. Third-party sources retain their own rights and attribution. See [CONTRIBUTING.md](CONTRIBUTING.md), [THIRD_PARTY.md](THIRD_PARTY.md), and [CITATION.cff](CITATION.cff).
