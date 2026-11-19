# Polynomial presentations of the integers over the rationals

Complete proofs and exact computational specifications for integer polynomials

```math
F(X,Y_1,\ldots,Y_m)
```

whose rational input projection is the integers, under the arithmetic premises stated in each construction.

**Every variable count includes the input.** Degree means total degree. Coefficient height is the maximum absolute integer coefficient after fixed parameters have been substituted. The priorities are variable count, degree, then coefficient height. No global minimum is claimed.

## Current constructions — 19 November 2026

The coauthor reductions **193→165, 229→180, 68→62 and 13→11** have been audited and integrated, with further degree, coefficient and hypothesis improvements. “None” in the table means **no additional conjecture beyond the explicitly retained arithmetic premises**. The independent audit of all elliptic, prime-pattern, pole-realization and height foundations is not declared complete.

| Construction | Additional height hypothesis | Total variables | Degree | Coefficients and effectiveness |
|:--|:--|--:|:--|:--|
| [General few-variable family](papers/few_variables25/four_contact_scalar_20261119_v78.tex) | None | **25** | **≤ 87,778,394,112** | Four-contact scalar and projective two-root encoder; sufficient odd exponent ineffective. |
| [General quartic family](papers/quartic/shared_product_audit_20261119_v78.tex) | None | **165** | **4, exact** | 139 quadratic squares; **2,607 monomials**; exact height below; defining threshold ineffective. |
| [Fully specified general polynomial](papers/few_variables25/four_contact_scalar_20261119_v78.tex) | None | **27** | **≤ 335,647,080,448** | Explicit `L=143`; coefficient height **< 2^(2^46)**. |
| [Fully specified quartic](papers/quartic/shared_product_audit_20261119_v78.tex) | None | **180** | **4, exact** | 152 quadratic squares; **2,850 monomials**; **108-bit** exact height; fully expanded literal. |
| [Few variables under weak abc](papers/conditional_few_variables/weak11_audit_and_transfer_20261119_v78.tex) | Weak abc at `121/100` | **11** | **≤ 32,542,081** | Full auxiliary charts and ordered guard recovery; sufficient shift ineffective. |
| [Lower degree under stronger weak abc](papers/conditional_few_variables/weak11_audit_and_transfer_20261119_v78.tex) | Weak abc at `16/15` | **11** | **≤ 19,366,273** | Same variable count and retained arithmetic inputs; sufficient shift ineffective. |
| [Few variables under ordinary abc](papers/conditional_few_variables/twelve_contact_first_scale_20261119_v78.tex) | Ordinary rational abc | **11** | **≤ 6,361,985** | Twelve contacts at the first height scale; sufficient shift ineffective. |
| [Small-height ordinary-abc quartic](papers/quartic_existence/abc_quartic_audit_20261119_v78.tex) | Ordinary rational abc | **62** | **4, exact** | 50 quadratic squares; **840 monomials**; height **B+1** on the stated cofinal family. |
| [Weak-abc quartic](papers/quartic_existence/abc_quartic_audit_20261119_v78.tex) | Weak abc at `9/8` | **63** | **4, exact** | 51 quadratic squares; **863 monomials**; sufficient shift ineffective. |
| [Weak-abc quartic](papers/quartic_existence/abc_quartic_audit_20261119_v78.tex) | Weak abc at `17/14` | **64** | **4, exact** | 52 quadratic squares; **866 monomials**; sufficient shift ineffective. |
| [Eight-contact weak-abc quartic](papers/quartic_existence/abc_quartic_audit_20261119_v78.tex) | Weak abc at `7/5` | **67** | **4, exact** | 55 quadratic squares; **905 monomials**; sufficient shift ineffective. |

Every count includes the input. The few-variable degrees are upper bounds for complete finite determinant specifications, not claims of full expansion or exact degree. All rows admit integer content one; the projective 25-variable polynomial is primitively normalized if necessary. No global minimum is claimed.

The enhanced 165-variable quartic has exact height

```math
H(F_N)=\max\{126616122944180358034867798936,\;149^{2N+2}\},\qquad N\ge1.
```

The new shared-factor packing strengthens local extraction without changing its 165 coordinates. The sufficient defining `N` remains ineffective. The explicit 180-variable polynomial uses the certified anchor

```math
A=51132150162547763354407979038657
```

and has exact height

```math
206625078319751697390503348692624.
```

Its [literal polynomial](computation/coauthor_audit_v78/work_general/enhanced/180/anchor_scaled/quartic180.txt) has **59,084 bytes**. The coauthor's [sparser 180-variable presentation](computation/coauthor_audit_v78/H10-quartics/quartics/explicit/quartic180.txt) remains available: **2,648 monomials, 54,695 bytes**, and a larger 161-bit height.

For the 62-variable small-height family, `B=n⁴` with positive odd `n`, and

```math
H=\max(4091n^2,n^4+1).
```

Thus `H=B+1` for odd `n≥65`. This is a coefficient-height cutoff, not a sufficient defining parameter. A [752-monomial presentation](computation/coauthor_audit_v78/work_abc/small_gate62/sparse/polynomial.json) has height `B+758541`; a balanced 825-monomial presentation has height `B+4091`.

The eight-contact argument gives an eleven-variable family for **every fixed weak-abc exponent `1<κ<3/2`**, with suitable source parameters. Its quartic extension uses `61+r` coordinates when the explicit absorption inequality in the proof holds, also covering every fixed exponent below `3/2`. The 63- and 64-variable rows improve the supplied hypothesis exponents without increasing their counts.

Current specifications: [results JSON](data/results_20261119_v78.json), [complete audit and proof guide](docs/results_20261119_v78.md), [source and certificate package](computation/coauthor_audit_v78), and [research directions](docs/research_directions.md). The two original coauthor packages and the new workstreams remain separately attributable. The verification gate materializes their pinned sources and byte-compares the regenerated data.

The [historical results JSON](data/results_20261117_v75.json) preserves the preceding complete records and their earlier versions. The following constructions remain reproducible and are superseded by the current table above. Their numerical bounds in the older papers and thematic sections below refer to the named historical sources.

| Historical source | Variables | Certified numerical bound |
|:--|--:|:--|
| [Reconstructed quartic, v74](docs/results_20261117_v74.md) | **193** | Degree 4; 2,770 or 2,626 monomials. |
| [Preceding quartic, v73](docs/results_20261117_v73.md) | **194** | Degree 4; 2,765 or 2,621 monomials. |
| [Explicit quartic, v68](docs/results_20261117_v68.md) | **229** | Degree 4; 3,312 monomials; 74,007 ASCII bytes. |
| [Ordinary-abc quartic, v65](docs/results_20261117_v65.md) | **68** | Degree 4; **1,078 monomials**. |
| [General few-variable family, v72](docs/results_20261117_v72.md) | 25 | Degree at most 4,924,857,429,000,192. |
| [General few-variable family, v75](docs/results_20261117_v75.md) | 25 | Degree at most 4,863,007,848,923,136. |
| [Ordinary-abc family, v71](docs/results_20261117_v71.md) | 11 | Degree at most 232,094,337. |
| [Ordinary-abc family, v75](docs/results_20261117_v75.md) | 11 | Degree at most 230,932,097. |

The [physical-coordinate audit, v67](docs/results_20261117_v67.md), [v76](docs/results_20261117_v76.md), [v77](docs/results_20261117_v77.md), and [new ancillary](negative_results/papers/pole_parameters/ancillary_audit_20261119_v78.tex) results preserve the precise scope of physical-lift, diagonal and selector-density obstructions. **The complete 21-variable general and 9-variable ordinary-abc targets remain unproved.** These counterexamples to specified universal specializations do not prove those global targets impossible.

## Contributors and citation

This repository belongs to the ℤℚ Diophantine Project, which uses the collective agentic notes from Stefan Baranczuk, Jose Brox, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry. The main repository for the project is [Elliot Glazer's](https://github.com/elliotglazer/diophantine-z-q).

This repository includes updated results and more related work: polynomial witnesses of unrestricted degree but lower number of variables, results conditional on the abc conjecture, etc.

Cite this work as "ℤℚ Diophantine Project contributors. ℤ is Diophantine in ℚ. 2026. https://github.com/elliotglazer/diophantine-z-q". If you want to include any of the related results specific to this repository, please add "https://github.com/JoseBrox/diophantine-z-q_improvements" to the end of the reference.

## Eleven variables under ordinary abc

The [twelve-contact theorem](papers/conditional_few_variables/twelve_contact_first_scale_20261119_v78.tex) gives a complete **11-variable family of degree at most 6,361,985**, under ordinary rational abc and the precisely retained elliptic, trace-height, prime-pattern and intrinsic-pole inputs. Set

```math
\beta=X^2+B,\qquad T=\mathrm{Tr}x(A),\qquad M=\beta^4+T^4,\qquad a=M.
```

For the twelve shifts `{-9,-8,-7,-5,-4,-3,-2,-1,6,10,11,12}`, put

```math
F(a,z)=\prod_c((a+c)^2-z^2),\qquad u=-24F/F_a.
```

The shifts are nonzero, distinct, have sum zero and contain no opposite pair. The intermediate derivative-height estimate gives `log r⁺(u) ≥ (39/40)h(M)−O(1)`, with exact strict absorption margin `18863/40040`. The all-integer congruence

```math
n^2\mathrm{Tr}x([n]P)-57/4\in16\mathbb Z_2
```

supplies the two-adic square class of the prepared first scale. This is proved using the integral formal group and duplication. The former guard `a²−z²≠0` is unnecessary; the stronger estimate includes that boundary.

Use the six positive balanced tests, and write the actual intrinsic input as

```math
e=7u\left(\frac{\mathrm{Nm}(W)}{(1+u)W_0}\right)^2.
```

Removing its displayed rational square by an invertible change of the pole parameters gives a smaller terminal equation, including zero ordinates. Ordered recovery of automatic point, height, balancing and detector guards leaves guard degree 650 and separator degree 49,052 in rank 128. The defining degree bound is `1+128(1+650+49052)`; the support is less than `2²¹²` and content is one.

The count is **1 input + 6 point coordinates + 1 contact parameter + 2 pole parameters + 1 encoder = 11**. The sufficient fixed odd shift remains ineffective; `B=3` is an algebraic fixture. The [complete source and independent checks](computation/coauthor_audit_v78/work_root/twelve/abc11) specify every denominator and coefficient majorant.

The original nine-coordinate actual-trace criteria below concern their explicitly recorded source architectures. The new eleven-variable construction supplies no automatic global rational square for those criteria. Their physical realization requirements remain open.

## A single actual-trace target for nine variables

The [derivative trace criterion](papers/pole_parameters/single_trace_derivative_criterion_20261117_v64.tex) replaces the two free parameters of the v63 derivative source's single pole block by one finite quadratic equation:

```math
Y^2=V^2+w(2-V),\qquad V=\mathrm{Tr}(W^{-1}),\quad w=\frac{u}{(1+u)^2}.
```

The resulting nine-coordinate source is sound at every sufficiently large fixed odd shift under the same stated arithmetic premises and ordinary abc. Completeness requires rational squareness at the **actual** detector trace. The paper verifies extraction, the stated local preparation, all denominator and character guards, and zero terminal roots. It does not prove global rational realization.

It is enough to obtain actual witnesses for every sufficiently large positive integer: a sign involution supplies negative inputs, and multiplying by `∏_{1≤m<N}(X²−m²)` includes the finitely many remaining integers with **no added variables**. This weaker realization hypothesis is also unproved. **The established ordinary-abc count remains 11, and the general count remains 25.** [Criterion metadata and checks](data/criteria_20261117_v64.json) are separate from the construction records.

The [arithmetic reduction](papers/pole_parameters/actual_trace_arithmetic_20261117_v70.tex) places the fixed-tuple problem on an actual detector-weight curve of genus at most **36**. An exact fixture has genus **24**, while its slope curve has genus **449**; both polynomial specifications and the genus certificates are independently reconstructed. A rational point must still solve the physical degree-nine equation, give a rational-square squared slope, and satisfy all original guards and preparation. The fixture shift `B=3` is not asserted sufficient for a defining polynomial.

The [halfpoint calculation](papers/conditional_few_variables/seven_contact_detector_20261117_v74.tex) uses the actual tuple `X=1, B=3, A=P, H=U=P/2` in the enlarged auxiliary domain. Its weight curve has **genus 12**. With seven contacts, its squared-slope and physical-slope covers have genera **90** and **181**. The [even-valuation revision](papers/conditional_few_variables/even_valuation_detector_20261117_v75.tex) gives another genus-12 weight curve; its physical-slope genera are **181** with seven contacts and **233** with nine. Exact coefficient reconstructions and degree-preserving Bezout identities certify these figures. No guarded rational point or physical lift is asserted.

The [coupled-weight theorem](papers/pole_parameters/coupled_weight_lifting_20261117_v74.tex) proves that the general source's physical weight pair determines the common slope birationally, including after normalization `w=u/(1+u)^2`. A paired polynomial gcd gives exact rational lifting and detects incompatible weight pairs; exceptional higher-degree fibers require rational-root testing. Both actual square equations, physical guards and integer-input realization remain necessary.

The [actual-trace curve theorem](negative_results/papers/pole_parameters/curves_and_abelian_families_20261117_v69.tex) applies at a fixed rational input to the nine-variable derivative route and the specified general 21-variable route, with their point roles independent. Every fixed algebraic curve in either guarded locus has only finitely many rational points; no curve over the rationals of normalization genus zero or one maps nonconstantly into it. The first fixed-point covers have genus at least eight and four, respectively. The derivative fiber has two rational boundary points at infinity and is everywhere locally soluble; those points do not supply guarded rational witnesses.

The [vertical-valuation theorem](negative_results/papers/pole_parameters/vertical_and_fixed_slope_20261117_v70.tex) further excludes nonconstant rational maps from abelian varieties whose images contain prepared points. The general statement fixes the input and allows all nine point roles to vary; the derivative statement also fixes the root. A separate proposition allows that root to vary when the slope has a fixed rational affine dependence on the scale, and forces both root and slope to be constant. These conclusions concern families. **Individual rational witnesses and the global 21/9 realization criteria remain open.** The [proof guide](docs/results_20261117_v70.md) gives the hypotheses and exact checks.

## Restrictions on point-role reductions

The [point-role theorem](negative_results/papers/integer_labels/point_role_restrictions_20261117_v66.tex) proves that every nonzero relation of total degree at most two among the four root indices, including a fixed finite menu, excludes infinitely many positive inputs in every fixed arithmetic progression of the general source. Scalar-contact divisibility forces the Lucas parameter to grow faster than the resultant bound permits. Within the exact multiplication witnesses, this also excludes deleting two point roles by independent fixed group expressions, even with finite menus and a different order of choices. Arbitrary source witnesses and other couplings are outside that conclusion.

The single shifted coupling `U_S=Z+H` admits explicit integral Lucas values with `b=(a-1)h` and `h=-4r mod(a-1)`. This meets any compatible finite scalar congruences fixed in advance. Joint comparison-prime, trace-scale and real realization remains unproved. The [proof guide and certificates](docs/results_20261117_v66.md) keep these statements separate from the unchanged construction records.

## Elliptic sums over arbitrary number fields

The [cyclic-group height theorem](papers/effective_sums/elliptic_sum_heights_over_number_fields_20261117_v63.tex) applies to every elliptic curve over every number field. For finite points `Q_i=[n_i]P+T_i` in one cyclic group modulo torsion, `M=max(1,|n_i|)`, and every integral `c`, it gives

```math
h\left(\sum_i x(Q_i)+c\right)
\ge \max_i h(x(Q_i))-O_{E,K,P,r}(\log(M+2)),
```

with an effective constant. The finite-place loss is explicit; the archimedean estimate uses David–Hirata-Kohno's published elliptic-logarithm theorem with fixed periods. Arbitrary torsion translates, zero indices and negative indices are included. The same method gives effective finiteness of `S`-integral abscissa sums.

Zywina's rank-one existence theorem, cited as a preprint, supplies suitable curves over every number field on which this controls the entire finite point domain. The result concerns algebraic sums. A field trace can still cancel, and no definition of every number-field ring of integers, or counterexample to such a definition, is asserted.

The [power-shift theorem](papers/number_fields/power_shifts_and_finite_exceptions_20261117_v69.tex) removes finite exceptional inputs without adding a witness coordinate. If a degree-`D` polynomial in `N` total coordinates defines a subset of a degree-`d` number field containing every sufficiently large positive rational integer and only finitely many nonintegral elements, it gives a single equation for the ring of integers in **`dN` total coordinates**, of degree at most **`2dD`**. The fixed shift may satisfy any prescribed integer congruence. With finite error relative to the rational integers themselves, the count remains `N`; a square shift gives degree at most `2D` whenever the field has no quadratic subfield, including every odd-degree field. The theorem supplies a conditional reduction; the required all-field detector remains unconstructed.

The separate [rank-stable contact obstruction](negative_results/papers/number_fields/rank_stable_adjacent_contacts_20261117_v63.tex) rules out directly inserting base-field rank-stable curves into the adjacent-index conjugate detector: the two contacts force a fixed non-torsion multiple to reduce to the identity, which occurs at only finitely many base primes. A different comparison architecture or a curve that does not descend is needed for that route.

## Sun’s revised construction and finite exceptions

The [version-pinned audit](docs/audits/sun_v2_20261117_v69/audit.md) compares Sun’s arXiv:2611.14605v2 with v1 and checks its main arithmetic reduction under the explicitly retained suppliers. Its 26 and 16 existential unknowns mean **27 and 17 total coordinates**, respectively. The revised aggregate sum-trace estimate removes one ordinary pole block. The odd-index certificates can also be omitted from the revised source, reducing a branch-rank bound from `2⁴²` to `2²⁴` without changing its coordinate count. A fixed shift can replace the unspecified multiplication map in that presentation; no numerical degree bound competitive with the current records is claimed.

The audit found no essential invalid implication in the reconstructed reduction, and records which imported foundations remain unaudited. The mixed-parity product-height example does not refute v1, whose relevant indices are odd. The [new power-shift theorem](papers/number_fields/power_shifts_and_finite_exceptions_20261117_v69.tex), [bibliography](docs/audits/sun_v2_20261117_v69/references.bib), and [proof guide](docs/results_20261117_v69.md) state the transferable improvements. Sun’s paper does not establish the missing actual-trace realization for 21 or 9 variables.

## Elliptic index divisibility and amplified congruences

The [primitive-denominator theorem](papers/elliptic_divisibility/simple_primitive_denominators_20261117_v60.tex) gives a simple primitive denominator prime for every sufficiently large index in a fixed coprime progression, under any fixed weak-abc exponent `1<κ<2`. Under exponent `4/3`, every sufficiently large index is allowed. Duplication gives the simple-support coefficient `2/κ-1`; the progression makes the nonprimitive support strictly smaller.

The [index-pole theorem](papers/elliptic_divisibility/elliptic_index_poles_20261117_v60.tex) uses that prime to force `h ∣ j` for `H=[h]P` and `U=[j]P`. It proves infinitely many complete witnesses for every nonzero integer quotient. Formal-logarithm truncation then forces `X-j/h` to vanish to any prescribed fixed order at the simple reference-denominator primes, without another free coordinate. The finite isogeny restrictions, exceptional indices, real and fixed-place preparation, and whole-character guards are included. A separate height condition is still needed to turn those congruences into equality.

The [pole-cancelling coordinate](papers/elliptic_heights/pole_cancelling_quotient_height_20261117_v60.tex) `X²x(U)-x(H)` has a proved height lower bound and local expansion. Its proposed use in the specified derivative detector is excluded by the separate [denominator-support theorem](negative_results/papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex): all positive odd contact primes must lie in the denominator of `H`, which cannot support a height growing quadratically with `j/h`. The theorem extends to every fixed rational replacement generically nonconstant in `U` within the stated support architecture; Siegel's theorem handles its constant specializations. It concerns intended integer witnesses and does not exclude other sources. The construction counts above are unchanged.

The separate [input-only helper theorem](negative_results/papers/pole_parameters/input_only_weight_false_witnesses_20261117_v61.tex) proves that the displayed degree-eight input weight does give `3h(X) ≤ ĥ(H)+O(1)` under abc, but still admits every noninteger `X=2+1/q` outside a fixed finite set. A local inverse for the formal-logarithm ratio and compatible index progressions produce complete witnesses with an unrestricted integer quotient. Controlling the input height alone therefore does not close this source's equality gap.

The [six-contact coupling obstruction](negative_results/papers/pole_parameters/six_contact_mobius_obstruction_20261117_v63.tex) covers every integer exponent at least four and every fixed finite menu of those exponents. One arithmetic progression of odd coefficient shifts defeats all twelve Möbius symmetries at the prescribed input and root point. The [cofinite extension](negative_results/papers/pole_parameters/cofinite_mobius_coupling_obstruction_20261117_v64.tex) propagates the obstruction to an infinite progression of positive inputs at each obstructed shift, so finitely many input factors cannot repair those prescribed-index sources. It does not exclude the derivative construction, every fixed coefficient shift, or every nine-variable definition.

## Rational pole levels

The [varying-level theorem](papers/pole_parameters/varying_level_pole_fibers_20261117_v61.tex) proves that, for every prepared `d`, all fibers

```math
y^2=d\left(\left((1-d)\frac{d+r^2}{d-r^2}\right)^2-s^4\right)
```

are everywhere locally soluble. Under the retained simultaneous-twist theorem, infinitely many rational levels `0<r<√d` have infinitely many rational points. Two fixed elliptic curves supply these levels and witnesses, and their combined projection is Zariski dense with all-character guard avoidance. The cleared pole polynomial again has degree nine, twelve monomials and coefficient height four. An exact nonsquare-complement example has `d=112/225`, `r=44/69`, `s=29/15` and `y=23548/10125`.

The theorem does not prescribe the good level as an existing detector coordinate or synchronize two actual detector inputs. Both free pole coordinates remain; no defining-variable count changes. The [proof and independent certificates](computation/pole_parameters/varying_levels_v61) distinguish the infinite existence theorem from the finite algebra and local checks.

## Finite algebras and the general polynomials

The [even-valuation theorem](papers/few_variables25/even_valuation25_20261117_v75.tex) gives the complete **25-variable** family of degree at most **4,863,007,848,923,136**, improving the previous **4,924,857,429,000,192** bound of the [full auxiliary-point construction](papers/few_variables25/full_auxiliary25_20261117_v72.tex). Four root points retain integral indices in `2E(K)`; the five auxiliary points range over guarded affine `E(K)` through cubic radicands. The first ten reciprocal-abscissa factors use their even valuations to remove an extra square. This strengthens local extraction and preserves the original whole-character completeness witnesses. The [integer circuit](computation/few_variables/even_valuation25_v75) has 6,039 arithmetic nodes and 101 recorded guards, with 128 retained subalgebra norm factors and support strictly below `2¹¹⁹²`. The stored `L=3` member is an algebraic fixture, not a certified defining member.

The same enlargement preserves the sound **21-coordinate** two-detector source. Simultaneous rational realization at the two actual traces remains unproved. The complete 25-variable family retains its four free pole parameters and all whole-character guards.

The [terminal quadratic extension theorem](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) permits the last quadratic radicand to vanish. Its separator distinguishes all distinct geometric characters even on a nonreduced fiber. Galois descent recovers a rational character from a rational determinant root without assuming a simple eigenvalue. An elementary valuation proof permits the zero final ordinate in the pole equations. Two large guard norms can therefore be omitted.

The [four complete specifications](computation/few_variables/terminal_root_v40) retain the integral point algebra, polynomial root envelopes and subalgebra norms. Every denominator and every preceding radicand remains guarded. The independent checker reconstructs these conditions from the native source circuits and recomputes all bounds. The [single-norm construction](papers/finite_algebra/unit_norm_20261114_v28.tex) and [subalgebra-norm theorem](papers/finite_algebra/subalgebra_norms_20261114_v30.tex) supply the underlying source and its full-unit completeness proof.

## Quartic equations and coefficient height

The [primitive quadratic basis theorem](papers/quartic/primitive_quadratic_bases_20261115_v40.tex) gives exact rational changes of the reference-equation basis, followed where specified by an invertible rational coordinate rescaling. The defining rows remain primitive integer quadrics. Stored matrices and inverses prove equivalence independently of the lattice algorithm used to find them. Independent expansions certify the exact heights and support for every allowed fixed parameter.

Complete coefficient tables are supplied for the [193-variable family](computation/quartic/seven_units193_v74), [229-variable explicit polynomial](computation/quartic/explicit229_compact_v68), and [68-variable abc family](computation/quartic/abc68_v65). The [193-variable theorem](papers/quartic/quartic193_20261117_v74.tex) retains three translated point charts, four polynomial cross comparisons and a homogeneous Lucas circuit. It recovers the required ratios at each consumed prime, where the reciprocal tests force their denominators to be nonzero. A refinement of the reference progression synchronizes the two formal depths and proves integer completeness. Seven contact units and five equations suffice after an input-preserving Laurent change. A second diagonal change lowers coefficient growth to `149^(2N+2)`. Independent checks reconstruct every quadratic row, both transformations and the entire quartic expansion in both coefficient bases.

The [229-variable theorem](papers/quartic/quartic229_compact_20261117_v68.tex) uses three complete detectors to control both components of the elliptic abscissa sum. Its thirty contacts remain distinct on the full finite point domain, including torsion translates. Exact finite-prime accounting proves the sufficient parameter `N=15`. A fixed rational diagonal coordinate change and primitive row normalization give exact coefficient height `149³⁰`, with the entire rational witness set preserved. The [fully expanded polynomial](computation/quartic/explicit229_compact_v68/quartic229-N15.txt) contains all 3,312 integer-coefficient terms in **74,007 ASCII bytes**, with decimal coefficients, standard coordinate names, no parameters and no trailing newline. It meets the upstream strict 100,000-byte notation rule. The [pinned upstream measurement](computation/quartic/explicit229_compact_v68/official_measurement.json) and independent coefficient reconstruction verify the size, input-preserving map and exact height; upstream record acceptance is a separate review process.

The [effective torsion-sum theorem](papers/effective_sums/effective_torsion_sums_20261117_v62.tex) gives an explicit logarithmic loss for abscissa sums over totally real fields, allowing arbitrary torsion translates and zero or negative indices. Its ramification allowance is at most the logarithmic discriminant divided by the field degree. The theorem controls the algebraic sum; the rational trace is a separate question.

The [68-variable arithmetic theorem](papers/quartic_existence/quartic_abc68_20261117_v65.tex) propagates the unit reference chart through every detector equation. It recovers the two weighted reciprocal products quadratically, replaces separate ratios by affine inverse comparison errors, and retains only the rational half-trace of the quadratic difference-abscissa output. All recovery coordinates, comparison squares and nonzero constraints are included in its 68-coordinate count. The proof covers soundness, nonzero integer completeness and zero input; independent exact expansion certifies the degree, support and coefficient height.

The [five-factor local theorem](papers/quartic/revised_detector_factors_20261117_v66.tex) gives a revised arithmetic interface for the general quartics. It proves valuation separation at every odd contact depth, retains all comparison and reciprocal thresholds, and checks selected-contact residues and fixed-place preparation. A smaller complete quadratic table is not yet available.

The [paired-ratio theorem](papers/elliptic_charts/paired_ratio_redundancy_20261115_v40.tex) shows that the complete ratio equations imply both reciprocal curve equations. It covers identities, torsion points and tangent pairs, and gives a quadratic-compatible uniform scaling of the seven pair coordinates. The [193-variable construction](papers/quartic/quartic193_20261117_v74.tex) instead uses polynomial cross comparisons and a homogeneous Lucas circuit; its exact source tables specify every retained relation.

The [mixed-power height theorem](papers/elliptic_heights/mixed_power_height_20261116_v45.tex) gives explicit bounds for every rational expression `x^(2n)+y²`, `n ≥ 3`, under a specified fixed weak-abc inequality. In the 68-variable construction, the residual is `X(m-X)` and the scale is `B+X⁸+T_sc²`. Recovering the unscaled physical trace contributes `2h(X)` only after the same strict absorption `602/679`, so it does not require a new coordinate.

## Reference charts and integer labels

The [inverse reference-square theorem](papers/elliptic_charts/inverse_reference_squares_20261116_v48.tex) gives a complete five-field-coordinate quadratic graph for both squared reciprocal abscissas. Its proof includes both exceptional linear-equation fibers without an additional nonzero condition or a square root of the translator abscissa. The [exact certificates](computation/elliptic_charts/inverse_reference_squares_v48) verify its identities and exceptional fibers.

The [three-coordinate reference chart](papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex) describes a point and its translate by two quadrics, including every tangent and two-torsion configuration in its specified domain. Its unit coordinates have explicit polynomial inverses. The [68-variable construction](papers/quartic_existence/quartic_abc68_20261117_v65.tex) uses those existing units in `v_HJ=u_HF` and `v_HK=w_HG` to recover the physical weighted products without a new inverse coordinate. Both reference comparison functions are affine, so the complete detector conversion stays quadratic.

The [quadratic reference and height rescaling](papers/elliptic_charts/scaled_reference_height_20261116_v43.tex) makes both reference reciprocal abscissas linear. It preserves quadratic point and ratio rows and recovers the original fixed-index height with one rational coordinate. The reference, point, ratio and height blocks use **32 rational coordinates on the nonzero-scale locus**; their necessary explicit quadratic guard adds one, giving **33 in total**, the same as the original blocks. Detector conversion remains separate. No smaller complete quartic follows.

The [quadratic reference-cover theorem](papers/elliptic_charts/reference_covers_20261116_v47.tex) gives polynomially inverse presentations with three and four field coordinates, including all four points over the two identity-reference boundaries. The four-coordinate form makes both reference reciprocal abscissas linear and remains quadratic after input scaling. Its weighted numerator and ratio equations give the physical detector products directly. A separate Jacobi chart recovers the original difference trace with one rational helper and classifies its entire zero-scale fiber. [Universal exact certificates](computation/elliptic_charts/reference_covers_v47) verify the maps and identities. These chart results alone gave no reduction below the historical 68-coordinate record; the current 62-coordinate construction uses the shared detector described above.

The [integral Pell-label theorem](papers/integer_labels/pell_labels_20261115_v40.tex) obtains exponential growth from two exact integral labels and one finite quadratic choice. It proves sharp bounds and arbitrarily large witnesses with prescribed finite congruence data. Its [checker and certificate](computation/integer_labels/pell_compression_v40) verify the identities and exceptional cases. Its application requires exact integral labels; no reduction below 25 variables follows from this theorem alone.

## Height estimates and compatible poles

The [trace-conic criterion](papers/pole_parameters/trace_conic_criterion_20261117_v57.tex) gives a simpler current target for **21/9**:

```math
\mathcal C_j=V_j^2+w_j(2-V_j),\qquad V_j=\mathrm{Tr}(W_j^{-1}).
```

A rational-square value excludes every relevant negative odd pole. The test uses the actual detector trace and physical weight, and is positive at every prepared character. It has compatible local squares at all prescribed preparation places and selected contacts. Each block may independently multiply its radicand by a class from

```math
\{1,\ 1+24V_j,\ 1+3(V_j-1)^2\}.
```

These trace-dependent classes preserve every consumed contact, so they require **no additional height hypothesis or height budget**, including in the general Lucas source. The same theorem permits the class `δ_c=(q²-2q-1)²+4q(q²-1)V`, where `q=2+wc²` and `c` is a fixed guarded function of existing source coordinates. In particular `c=λ` uses the retained common slope, preserves fixed-place preparation and adds no coordinate. Thus the allowed class can vary with the actual slope and auxiliary points without a height penalty. The untwisted equation is a rational conic; the linear-class equation is a cubic elliptic equation with reference point `(49,336)` in its stated Weierstrass coordinates. The complete finite-algebra count would be **21 or 9**, with every guard included, **if the simultaneous actual-trace realization is proved**. That global rational realization remains open. The degrees of these small radicands are not full defining-polynomial degree bounds.

The [cubic rank theorem](papers/pole_parameters/cubic_trace_rank_20261117_v57.tex) proves that the reference point `(49,336)` has infinite order for **every rational `0<w ≤ 1/4`**. Its exact torsion classification has projective finite-field certificates and an independent group-law check. Arithmetic progressions of its multiples give infinitely many free traces `1<V<2`, arbitrarily close to the reference at the real and any prescribed finite places. This supplies a positive-rank family throughout the general source's normalized range; matching those traces to the actual elliptic detector functions remains unproved.

The [small trace-class theorem](papers/pole_parameters/small_trace_classes_20261117_v58.tex) also permits `V+2`, `V²-V+2`, and `1+w(2-V)`, with no lost contact prime, new coordinate, or height budget. Its smallest radicand is

```math
(V+2)\bigl(V^2+w(2-V)\bigr)=V^3+(2-w)V^2+4w.
```

This block has total degree **3**, **4 monomials**, and coefficient height **4**. The source proof includes the existing selected-prime splitting, every fixed-place preparation, and every point-algebra character guard. The finite menu may vary with the input. These block measurements do not give a complete defining-polynomial bound, and actual simultaneous rational realization remains unproved.

The [all-point trace theorem](papers/trace_heights/trace_on_all_points_20261113_v25.tex) and [positive weighted trace theorem](papers/trace_heights/weighted_trace_20261114_v27.tex) include the half-integral index and torsion cases required by the sources. The latter also verifies that the selected Gaussian primes annihilate the half-generator using the existing congruences.

For this smallest cubic, `x=V+2` gives `E_w:y²=x(x²-(w+4)x+4(w+1))`. The [same paper](papers/pole_parameters/small_trace_classes_20261117_v58.tex) proves that **`(4,4)` has infinite order for every rational `0<w ≤ 1/4`**. An exact division-polynomial certificate and an independent tangent/chord calculation prove the torsion exclusions. This supplies positive rank throughout the normalized weight range; prescribing `x=2+Tr(W⁻¹)` for both actual detectors remains unproved.

The [joint-pole theorem](papers/pole_parameters/joint_pole_realization_20261114_v29.tex) and [common-twist theorem](papers/pole_parameters/common_twists_20261114_v30.tex) reduce pole parameters on specified square-class compatibility loci. The current completeness witnesses are not proved to lie on those loci. These results do not establish a 24-variable construction or a smaller abc variable count.

The [shared-parameter local theorem](papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex) proves that **every rational conic parameter** is locally admissible for every prepared input. A finite family can use the same parameter at every completion.

The [fixed-fiber theorem](papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex) proves that one rational witness with nonzero ordinate gives infinitely many witnesses at that same parameter. In all four native sources, the extracted square-class scalars are positive rational numbers independent of the auxiliary points and finite-algebra characters. Thus every conic denominator is nonzero for every rational parameter, and the remaining pole norms can be avoided within the chosen rational fibers. The same paper gives independent auxiliary cyclic return sets preserving preparation and every earlier guard. The unresolved step toward **24 variables** is the existence of a common rational fiber for actual detector tuples; no additional pole-guard theorem is required.

The [early-scalar theorem](papers/pole_parameters/square_complement_baseline_20261116_v43.tex) preserves the general source with the same 25-coordinate census and gives a baseline with a nonzero rational square complement. Its actual guarded detector inputs can simultaneously have square complements at any prescribed finite set of rational primes. This is a finite-local realization theorem; global rational square complements and a common rational pole fiber remain open. The modified family has no newly certified effective exponent or coefficient bound.

The [doubled-source norm map](papers/pole_parameters/doubled_source_congruent_twists_20261116_v43.tex) constructs rational congruent-number points directly from native doubled elliptic points, with explicit abscissa square class. Matching that class to the required detector class remains unresolved. The [current common-fiber and reference guide](docs/common_fibers_and_reference_charts_20261116_v43.md) gives the formulas, complete block counts, exact checks, and remaining proof targets.

The [varying-input quadric theorem](papers/pole_parameters/varying_input_quadric_20261116_v44.tex) gives a positive parametrization at a fixed conic parameter: after allowing the detector input to vary within its prescribed square class, the pole surface is birational to a smooth quadric with an explicit rational point. The theorem gives exact maps, a rational parametrization and arbitrarily small positive input examples. Matching these coefficient inputs to the actual elliptic detector functions remains the arithmetic step; no smaller defining count is assigned to this result.

The separate [abelian-parameter obstruction](negative_results/papers/rational_fibers/abelian_parameter_obstruction_20261116_v44.tex) rules out uniform rational square-complement or pole-witness identities on an abelian parameter space when the detector argument is nonconstant, even with varying twist classes. Fixed-argument rational fibers, ramified covers and individual arithmetic witnesses remain open. The [fixed-argument ramification theorem](negative_results/papers/rational_fibers/fixed_argument_complement_ramification_20261116_v44.tex) additionally excludes uniform square-complement sections after surjective abelian couplings of the full independent auxiliary product at a fixed slope. Proper coupled subfamilies and individual rational witnesses remain open. The [duplication sign obstruction](negative_results/papers/elliptic_charts/duplicated_reference_signs_20261116_v44.tex) identifies an allowed quartic reference progression with incompatible doubled formal-parameter signs. These results delimit particular proposed reductions; neither proves a minimum variable count.

The [native square-complement theorem](papers/pole_parameters/guarded_complement_reduction_20261116_v45.tex) proves that every complement `17(17-b_i)` is a unit of the entire point algebra at a prepared actual tuple. The proof uses splitting over `ℚ(√2)` and the odd valuation of `w_i/17`. If the two actual complements can be realized as rational squares for each integer input, both complete pole blocks can be removed: the conditional census is **21 variables**, or **9** in either conditional source. **That additional realization theorem is unproved; these are targets, not established record counts.** The same paper gives infinitely many prepared free inputs at one common pole parameter, without asserting native trace matching.

The [finite-class complement theorem](papers/pole_parameters/finite_complement_classes_20261116_v46.tex) weakens that realization target. Finitely many levels `17m²` and positive square classes supported on the **original exceptional prime set** can be allowed without adding retained coordinates. At the single level 17, it is enough that both actual complements have even valuation outside that fixed set. All whole-algebra guards remain automatic. The paper proves the same conditional **21/9** census and gives an infinite prepared free-input family with nonsquare complement class 409, allowed when 409 belongs to the exceptional set. **Actual native realization remains unproved**, so this criterion gives no smaller defining bound.

The [detector-field norm scalar](papers/pole_parameters/detector_field_norm_scalar_20261116_v52.tex) gives a further **25-variable** family under the retained arithmetic premises. Its degree-four input polynomial reflects rational integrality, while a fixed rescaling supplies the scalar contact-height argument. The scalar is an explicit norm from `ℚ(√2)` for every rational input, and both prepared physical weights can be chosen as norms from that same field. The unchanged conditional sources also admit this norm preparation. Thus their bare conics `u_i²-2y_i²=4w_i/17` have rational points. Matching `u_i` to the actual detector traces remains unproved; no numerical defining-polynomial degree is assigned to this family.

The [adaptive complement theorem](papers/pole_parameters/adaptive_native_complements_20261116_v50.tex) permits trace-dependent levels and varying quadratic classes with no new retained coordinate. Its exact change of presentation is

```math
w_i^*=\frac{w_i}{(1+w_i)^2},\qquad W_i^*=(1+w_i)W_i,\qquad
V_i^*=\mathrm{Tr}((W_i^*)^{-1}),\qquad J_i^*=\mathrm{Norm}((W_i^*)^{-1}).
```

It preserves each actual detector output `b_i=4w_i^*/(V_i^*)²`. At a hypothetical negative odd pole, `(w_i^*,V_i^*,J_i^*)` reduces to `(0,0,0)`. Consequently the level multiplier `m_i=1/(1-V_i^*+J_i^*)` retains pole exclusion, although it may have poles at good contacts. Its denominator and complement are units at every prepared point-algebra character. The earlier [bounded norm levels](papers/pole_parameters/bounded_norm_levels_20261116_v48.tex) remain a separate permitted family.

The class `d_i=1-4w_i^*/17` is automatically a local unit at the relevant primes and lies in `[16/17,1)` on prepared real tuples. Its bare norm conic contains the fixed point `(1,1)`. The exact remaining **21/9** target is

```math
(m_iV_i^*)^2-d_i y_i^2=\frac{4w_i^*}{17},\qquad i=0,1,
```

with the first coordinates prescribed by the actual coupled detector tuple. Further classes may depend on the existing auxiliary data, subject to the proved local and whole-character conditions. **Simultaneous prescribed-trace rational realization remains unproved.** This historical adaptive-level construction retains 25 and 13 coordinates; the current weak-abc and ordinary-abc families above both use 11. [Exact certificates](computation/pole_parameters/adaptive_levels_v50) verify the identities and specified local examples, not uniform rational realization.

The [norm-compatible preparation](papers/pole_parameters/norm_compatible_scalar_20261116_v47.tex) makes both associated norm conics rationally soluble throughout a prepared integer-input family. For the general source it uses an explicit degree-eight input polynomial reflecting integrality and a scalar that is a norm from `ℚ(√10657)`, preserving the 25-coordinate source and its height argument. The conditional sources already admit the same bare-norm preparation without changing their scalar. The unresolved equations require the first conic coordinates to equal the **actual prescribed detector traces**; bare conic solubility does not imply the 21/9 target.

The [actual prescribed-trace benchmark](papers/pole_parameters/admissible_levels_native_traces_20261116_v47.tex) realizes both equations for `X=-1` and `X=1`, at the algebraic fixture `B=3`, after fixed positive exceptional-unit rescalings. It retains the actual point functions, detector products, traces and coupled arguments. [Three exact arithmetic implementations](computation/pole_parameters/native_trace_fixture_v47) check both equations and all **128 complement guards** over the **64 point-algebra characters**. The same paper allows general fixed levels with nonnegative even valuations outside the exceptional set; their complement guards must be established directly. This benchmark does not give uniform completeness or a sufficient defining shift. The separate [polynomial-level local theorem](papers/pole_parameters/polynomial_levels_local_20261116_v47.tex) gives explicit comparison and reference-product powers that preserve local extraction for levels `cM(X)²`, without asserting global realization.

The separate [signed finite-class obstruction](negative_results/papers/pole_parameters/finite_nonsquare_class_obstruction_20261116_v47.tex) proves that every finite set of nontrivial rational square classes fails uniformly for the original general scalar, even with arbitrary guarded auxiliary tuples and rational level multipliers. It leaves the rational-square class available and does not apply to the redesigned norm-compatible scalar.

## Reweighted detectors and rational square tests

The [quadratic reweighting theorem](papers/pole_parameters/reweighted_elliptic_detectors_20261116_v53.tex) gives complete revised general and conditional sources under their retained arithmetic premises. The general source uses the physical weight `w=u/(1+u)²` throughout the detector and one extra contact factor in each scalar numerator. The conditional source uses `W(t)=∏ᵢ(1+C_i²/F(t))`, with the symmetric final comparison `r+s̄-2X`. It retains the original weight and satisfies `W-1=O(w³)` at fixed preparation places. The full local extraction, height, ordered completeness and whole-character guard arguments retain **25 and 13 variables**. No numerical defining degree bound is transferred to these changed families.

The [guarded rational-square criterion](papers/pole_parameters/native_square_criterion_20261116_v53.tex) uses the actual trace and norm `V=Tr(W⁻¹)`, `J=Norm(W⁻¹)`:

```math
\mathcal R_a=
\left(1-\frac{V}{1+w}+\frac{J}{(1+w)^2}\right)
\left(1+\frac{a^2(1-V/2)}w\right).
```

A rational-square value excludes every required negative odd detector pole. The radicand is positive at every prepared character, and its reference value at `W=1` is exactly `w²/(1+w)²`. Fixed nonzero exceptional-set units are admissible coefficients; so are the proved source-dependent choices `a=1+wc²` for existing guarded rational source functions `c`. These choices add no rational coordinate or nonzero guard. The flat choice `a=1` has an exact prescribed-coordinate elliptic form, and the conditional detector has a trace-preserving reference involution.

**Two simultaneous rational-square values on actual prepared detector tuples would give 21 variables, or 9 under the conditional source hypotheses. This global realization theorem remains unproved.** The proved local preparation and exact finite-algebra count do not replace it. The [current proof guide](docs/results_20261117_v65.md) states the precise conditions and their limitations.

### A single cover and finite square-class alternatives

The [signed mixed-power theorem and single-cover criterion](papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex) place both input and trace heights in

```math
t=\bigl((X^2+B)^e+T^e\bigr)^d+z^2,
\qquad T=\mathrm{Tr}x(A).
```

Under the stated weak-abc inequality, one actual native square condition gives soundness with a nine-coordinate census. The optimized height arguments have degrees **48**, **48**, and **96** in the retained coordinates for exponents `25/24`, `16/15`, and `121/100`, respectively. Ordinary abc permits degree **48**. The height theorem covers `x^d+y²` and `x^d-y²` with arbitrary rational denominators and nonzero output; its coefficient is `(2κ-1)/(d-κ(d/2+2))`. Positivity of the actual root trace also permits odd inner exponents. These are argument degrees, not full defining-polynomial degree bounds. **Rational realization for every prescribed integer input remains unproved**, including the required restriction on the prime preparation.

Both this criterion and the two-block 21/9 criterion permit any **fixed finite menu of positive exceptional-unit square classes**, such as `{1,2}`. A finite product of the existing quadratic-branch polynomials encodes the choices without a new coordinate. The selected class may vary with the input; its allowed prime support must remain fixed. This relaxed realization property does not impose the optional exceptional-place square neighborhoods used to prepare class one. No uniform realization theorem is asserted.

### Variable square classes with controlled height

The [variable-class theorem](papers/pole_parameters/variable_squareclasses_20261117_v57.tex) allows each conditional native radicand to use a positive exceptional-unit multiple of any class in

```math
\{1,\ (X^2+B)^2+\mathrm{Tr}(x(A))^2,\ 1+X^4\}.
```

The varying classes may have prime support outside the exceptional set. Their height budget is absorbed by source powers, with no new coordinate or guard. Under ordinary abc, the two-cover choice has exponent **6** and contraction `135/136`. The [sharp single-cover criterion](papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex) has argument degree **60** and contraction `520251/726142`, using inner exponent five and outer exponent six. For weak exponents `25/24`, `16/15`, and `121/100`, its optimized argument degrees are **72**, **80**, and **168**. These optimize the stated power criteria, not the complete defining degree. The nine-coordinate census remains conditional on actual rational realization for every integer input. **That realization is unproved**, and no unrestricted 21-variable transfer of these varying classes is asserted.

### A prepared pole block with coefficient height four

The [intrinsic pole theorem](papers/pole_parameters/intrinsic_pole_20261117_v56.tex) uses

```math
Y^2=d(d+v^2)^2s^4-d(d-v^2)^2(1-d)^2.
```

Its radicand has **degree 9**, **12 monomials**, **content 1**, and **coefficient height 4**. The equation alone, without chart guards, excludes negative odd valuations of `d` at **every prime**, including two. For `0<d<1` with square reduced denominator, `d ∈ 7·(ℚ₂×)²` and `v_2(d) ≥ 4`, the stated application of **Burungale, arXiv:2611.16130v1, Theorem B** gives a dense rational witness projection and avoidance of every whole-character guard. It retains two free coordinates per pole. The complete [general source transfer](papers/pole_parameters/general_intrinsic_transfer_20261117_v57.tex) and [conditional source transfer](papers/pole_parameters/conditional_intrinsic_transfer_20261117_v57.tex) verify that preparation and every character guard, retaining **25 and 13 variables**. The general transfer changes only the early scalar; the conditional transfer keeps the fast detector and uses `d=7b`. No new complete determinant-degree or coefficient bound is assigned to these source variants.

The [scalar-precision theorem](papers/pole_parameters/precision_transfer_20261117_v56.tex) gives a complete general source with scalar orders two, reciprocal orders one, the eighth-order logarithm `ℓ₈=z(1-2Df²/5)`, and sixth-order comparisons. Its squared Lucas parameter gives strict height exponents `7/4` and `7/6`. The source retains **25 variables** and all original arithmetic premises; no new determinant degree bound is assigned.

## Rings of integers of number fields

The [definability reductions](papers/number_fields/number_field_definability_20261109_v12.tex) relate the questions for the ring of integers, the rational integers and the rational subfield, and prove descent implications between number fields.

**No counterexample for a number field, and no theorem covering every number field, is established here.** Failure of a particular polynomial after scalar extension is not a counterexample to Diophantine definability. The [research guide](docs/research_directions.md#rings-of-integers-of-number-fields) states the remaining denominator and realization problems.

## Negative results

The [fixed-slope incidence theorem](negative_results/papers/rational_fibers/fixed_slope_trace_finiteness_20261117_v59.tex) proves finiteness for the actual first trace on a fixed smooth genus-one trace curve, allowing all independent point roles of the stated reweighted sources. It excludes infinite fixed-slope propagation; individual witnesses, a varying slope, point-dependent curve coefficients and the untwisted conic remain open. Its scope is distinct from the new derivative detector.

The [prepared-cover obstruction](negative_results/papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex) gives `d=112/225` for which `y²=d((1-d)²-s⁴)` is soluble over every completion of `ℚ` and has no rational point. An exact Cassels pairing on `E_791` proves the obstruction, with two independent arithmetic certificates. This excludes the specified one-coordinate pole specialization on all prepared inputs; it does not assert that this input is an actual detector value.

The [intrinsic-specialization theorem](negative_results/papers/pole_parameters/intrinsic_specializations_20261117_v57.tex) excludes every finite rational-function menu for `s(d)` and identifies the positive abscissa classes of the relevant rank-one congruent curves. Relations coupling both pole coordinates and higher-rank constructions remain outside its scope.

The [deterministic contact-coupling theorem](negative_results/papers/pole_parameters/order_three_inert_obstruction_20261117_v56.tex) excludes the specified order-three height substitution with prescribed root `A=[X]P`, for **every positive odd shift**. Its certificate covers all **81,421 residues** of the shift at one inert prime and gives infinitely many failing integer inputs, independently of the auxiliary points. Other couplings and free slopes remain open.

The [rational-product finiteness theorem](negative_results/papers/pole_parameters/rational_detector_products_20261117_v56.tex) shows that a rational actual conditional product `W` satisfying the pole implication has no nonexceptional odd contact. Requiring this in both blocks permits only finitely many integer inputs. This does not exclude nonrational products or arbitrary individual witnesses.

The [fixed-fiber genus theorem](negative_results/papers/pole_parameters/fixed_flat_fibers_20261116_v53.tex) gives geometrically integral simultaneous square covers of genera **236** and **332** for two actual fixed point tuples in the faster conditional detector. Their four rational points over infinity lie outside the guarded domain. The exact coefficient fixture is `B=3`, with no sufficient defining-shift assertion. These computations do not exclude finite rational witnesses or varying auxiliary indices.

The [fixed-trace obstruction theorem](negative_results/papers/pole_parameters/fixed_trace_obstructions_20261116_v51.tex) excludes both normalized traces equalling one at the original general-source input `X=4`, uniformly in the slope, auxiliary tuple and odd exponent. It also excludes every finite fixed set of trace targets from uniform completeness for that source. For both conditional six-contact sources, a separate real scale bound excludes simultaneous unit traces at every prepared slope when `B ≥ 19`. Varying prescribed-trace norm equations and modified scalar sources remain outside these obstructions.

The [affine scalar-coupling theorem](negative_results/papers/integer_labels/affine_scalar_coupling_obstruction_20261116_v50.tex) proves that every fixed finite set of identities `S=[m]A+[k]P` loses an infinite progression of integer inputs for the original general scalar source. Its explicit `S=A+[2]P` counterexample is `X=11` at `p=80287`. Altered scalar constructions and other couplings are outside its scope.

The [automatic-level finiteness theorem](negative_results/papers/pole_parameters/automatic_level_finiteness_20261116_v48.tex) excludes uniform conditional completeness from the choice `a=wNorm(W)`, including fixed finite rational rescalings. The [tangent-completion theorem](negative_results/papers/elliptic_charts/tangent_completion_20261116_v48.tex) proves that all quadrics in the specified compressed pairing, even after adjoining the physical trace, leave its false tangent family. These results concern those constructions; they leave bounded native levels and different paired-point embeddings open.

The separate [obstructions and lower bounds](negative_results/README.md) directory contains the proved negative results, organized by subject with their exact hypotheses and limitations. It includes pole-predicate counterexamples, restrictions on elliptic-point compression, contact-height counterfamilies, and obstructions to extending a fixed formula to number fields. Shared computational dependencies remain linked from the corresponding papers and index.

The [actual multiplication-surface obstruction](negative_results/papers/rational_fibers/actual_multiplication_surface_20261117_v58.tex) excludes uniform rational square identities even after imposing `A=[n]P`, `U=[n]H` for a fixed nonzero integer `n` and letting the slope be any nonconstant rational function of `H`. The specified safe trace classes are included. Individual rational witnesses, constant slopes, proper subfamilies and ramified covers remain open. The separate [two-square height obstruction](negative_results/papers/contact_heights/two_square_height_20261117_v58.tex) gives fixed-output families with unbounded rational height for powers of two; it does not impose the actual inner detector form.

The [pole-compression guide](negative_results/docs/pole_compression_obstructions_20261115_v41.md) presents the all-rational-coefficient conic-chain classification and the automatic-conic counterfamilies. These concern the specified predicates and prepared inputs; they do not assert a global minimum for defining polynomials.

## Reproduction

Use **Python 3.12** for the byte-pinned legacy suite and **SymPy 1.14.0** for symbolic checks. From the repository root:

    python -m pip install sympy==1.14.0
    python -B scripts/verify_v78.py
    python -B scripts/verify_v77.py
    python -B scripts/verify_v76.py
    python -B scripts/verify_v75.py
    python -B scripts/verify_v74.py
    python -B scripts/verify_v73.py
    python -B scripts/verify_v72.py
    python -B scripts/verify_v71.py
    python -B scripts/verify_v70.py
    python -B scripts/verify_v69.py
    python -B scripts/verify_v68.py
    python -B scripts/verify_v67.py
    python -B scripts/verify_v66.py
    python -B scripts/verify_v65.py
    python -B scripts/verify_v64.py
    python -B scripts/verify_v63.py
    python -B scripts/verify_v62.py
    python -B scripts/verify_v61.py
    python -B scripts/verify_v60.py
    python -B scripts/verify_v59.py
    python -B scripts/verify_v58.py
    python -B scripts/verify_v57.py
    python -B scripts/verify_v56.py
    python -B scripts/verify_v53.py
    python -B scripts/verify_v52.py
    python -B scripts/verify_v51.py
    python -B scripts/verify_v50.py
    python -B scripts/verify_v49.py
    python -B scripts/verify_v48.py
    python -B scripts/verify_v47.py
    python -B scripts/verify_v46.py
    python -B scripts/verify_v45.py
    python -B scripts/verify_v44.py
    python -B scripts/verify_v43.py
    python -B scripts/verify_v42.py
    python -B scripts/verify_v41.py
    python -B scripts/verify_v40.py
    python -B scripts/verify_v38.py
    python -B scripts/verify_v34.py
    python -B scripts/verify_v33.py
    python -B scripts/verify_v30.py
    python -B computation/pole_parameters/joint_realization_v29/check.py
    python -B scripts/verify_v28.py
    python -B scripts/verify_release_v27.py
    python -B scripts/verify.py --full

The current verifiers reconstruct specifications and certificates in temporary files. They cover the single-cover height coefficients and square-class menus, the intrinsic pole coefficient table, the complete precision-transfer exponents and Lucas witnesses, the independent inert-prime certificate, the reweighted source identities, the guarded square criterion and prescribed-coordinate elliptic identity, the independent fixed-fiber Bézout and genus certificates, the detector-field scalar norm and integrality-reflection certificates, fixed-trace inert-prime certificates, the conditional positive-interval derivative identities, normalization norm restrictions, adaptive levels, the exact pole-preserving normalization, varying classes, norm-one incidence identities and the separate affine scalar-coupling obstruction, as well as the complete 193-, 194-, 229-, and 68-variable quartics and their coefficient expansions, complete variable-difference charts including torsion and tangent fibers, unit-reference product recovery and the scaled physical trace, the complete inverse reference-square graph, bounded native norm levels, automatic-level finiteness examples, both full tangent quadratic-identity spaces, weighted-product boundary certificates and input-rescaling identities, finite complement classes, the native complement guard and mixed-power height identities, the abelian-parameter and duplication obstructions, the revised scalar identities and source census, exact quadratic reference and height rescaling with its nonzero guard, the norm map, normalization and local cancellation counterexamples, fixed-class branch and quotient identities, native fixed-fiber guards, rational-section maps, K3 branch and resolution identities, independently checked mixed reference signs, local pole cases, Tunnell coefficients, terminal nonreduced examples, reference-chart identities and exceptional cases, Pell-label examples, paired-ratio implications, invertible row transformations and complete quartic expansions. The retained verifiers authenticate the sources and supplied 198-variable archive. The full legacy verifier has **126 stages**. Optional PARI rank checks remain separately requested by --with-pari; they are not implied by --full. The new local and automatic-conic certificates do not use PARI, analytic ranks, or BSD.

The complete TeX manuscripts are the mathematical deliverables. They are compiled and visually inspected before publication. scripts/update_manifest.py records the distributed file hashes. Computational reconstruction certifies the finite identities and coefficients it checks; it does not certify external arithmetic premises or constitute independent non-author mathematical review.

## Attribution and review scope

The 198-variable parent of the historical 195-variable construction was supplied in Gabriel Conant's research archive with ChatGPT. Its [original attribution and source](sources/h10_quartic198/README.md) are retained. The [pinned upstream 214-variable source](computation/quartic/balanced214_v24/source) and its hashes remain a separate dependency. The current work is maintained in this repository and does not modify the upstream repository.

The congruent-twist pole realization uses **Jaswal, Hexagon 2611.00331v2, Theorem 1.2**, with the preparation hypotheses stated in the [pole paper](papers/pole_parameters/congruent_twist_poles_20261114_v27.tex). The supplied finite-family strengthening is used only in the separate compatible-pole results. Bibliographies, [arithmetic dependencies](docs/arithmetic_inputs.md), and [THIRD_PARTY.md](THIRD_PARTY.md) retain the source distinctions.

The [reference-chart correction](docs/audits/reference_chart_correction_20261114_v27.md), [physical-normalization correction](docs/audits/scalar_ratio_correction_20261115_v33.md), and [unsupported 233-variable claim audit](docs/audits/recovery_233_20261115_v38.md) remain explicit. No 233-variable result is claimed. Earlier source files and receipts remain available for exact reproduction; their superseded numerical summaries do not replace the current table.

Original project contributions are under **CC BY 4.0**. Third-party material retains its own rights and attribution. See [CONTRIBUTING.md](CONTRIBUTING.md), [THIRD_PARTY.md](THIRD_PARTY.md), and [CITATION.cff](CITATION.cff).
