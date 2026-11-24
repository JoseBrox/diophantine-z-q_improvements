## Current BB-native quartics (24 November 2026)

The [new proof](../papers/quartic/bb_native_quartics_20261124.tex), [result ledger](results_20261124_bb_native.md) and [complete coefficient package](../computation/bb_native_quartic_20261124/README.md) now supply the **preferred 163- and 179-variable general quartics**, replacing the old native non-CM pole input by the congruent-number criterion from Bhargava–Burungale v2. The new 137/151-row quadratic systems have 2,771/3,012 expanded monomials and the same exact coefficient heights as the historical v82 systems. No Route K/CR₃/old Theorem 5.3 assumption enters these **new** defining polynomials. All other elliptic, geometry, comparison, height and prime-pattern premises remain inherited, and the fixed 179 coefficient specification is retained. The historical v82/Busy Beaver materials are preserved without changing their claims.

## Bhargava–Burungale v2 audit and transfers (v88)

The [v88 audit](results_20261123_v88.md) and [complete route map](bb_all_route_status_20261123_v88.md) supersede the numerical summary in this historical source map. All five current few-variable routes now use the stated class-seven product criterion of Bhargava–Burungale v2, Lemma 2.2, after the separately proved preparation and square-factor normalization. The 25/27 routes use the new scalar; the weak-abc11 routes use seven times their old weight and additional preparation at seven. This replaces their old pole-converse input. Their other elliptic, height, modular and quantified prime-pattern premises remain explicit.

The finite-support twist extension allows overlapping complement prime supports. The BB index model admits two tests instead of five, direct quadratic relations, and an interval wrapper with one fewer rational variable. These are proved subsystem improvements; the paper's unspecified index-presentation parameter r remains unevaluated. No new numerical defining-variable record is claimed, and the 21/9 actual-realization gap remains open. The detailed audit checks BB's external theorem interfaces without claiming an independent proof of every inherited project foundation.

> **Source map through v59.** The numerical table below is historical. Current records are in the [v82 result table](../data/results_20261120_v82.json) and [v82 proof guide](results_20261120_v82.md). The 56-variable quartic uses Burungale, arXiv:2611.16130v1, Theorem B in its stated square class seven; it does not require the square-class-one strengthening retained in the v79 construction. Other elliptic, comparison, trace and prime-pattern inputs remain explicit in its proof.

# Arithmetic inputs, theorem scope, and effectiveness

The construction theorems identify rational input projections with $\mathbb Z$ under the arithmetic inputs stated in each paper. Every variable count includes the input. A finite coefficient specification and a certified sufficient value of its fixed parameter are separate conclusions.

## Scalar-point and divisibility results added in v82

The [163/179 quartic transfer](../papers/quartic/scalar_point163_179_20261120_v82.tex) retains the named group, relative formal-logarithm, modular contact-height, native-pole realization, and quantified prime-pattern/recurrence interfaces of its source constructions. Its new local scalar and ordered global witness arguments are proved in the manuscript. The 163-variable family additionally uses the existing positive weighted trace theorem, whose application of von Buhren's published family height theorem has constants independent of the family parameter and an ineffective additive constant. The 179-variable member uses the retained effective unweighted bound. The finite coefficient check is not a proof of these external foundations.

The [prepared elliptic divisibility subrelation](../papers/elliptic_divisibility/prepared_eds_divisibility_20261120_v82.tex) uses ordinary rational abc for eventual odd primitive denominator primes; a direct exponent-one proof is included, with Cornelissen–Zahidi Proposition 3.10(iii) and Silverman Lemma 13 as primary antecedents. It uses the recorded generator for LMFDB 256.b1 and exactly Burungale's published class-seven pole theorem. It does not assume a separate inert-prime conjecture and does not identify an external input with the elliptic quotient.

The [ten-coordinate criterion](../papers/pole_parameters/genus_one_sound_criterion_20261120_v82.tex) has an additional **unproved actual-input rational-point hypothesis**. Everywhere-local solubility of its prepared fibers is proved. The prepared global counterexample uses unconditional algebraic rank bounds from PARI, not BSD, and is not asserted to occur at the actual source tuple. Neither research result changes the 25/11 definition records.

## Number-field descent added in v81

The rationality-descent additions in v81 have a separate scope, specified
in the [v81 guide](results_20261119_v81.md). Their essential inputs are
the height inequality for the six roots of `(T^3-2)(T^3-3)` with truncated
coefficient greater than 7/2, and an E/Q with
`0 < rank E(Q) = rank E(K)`. Ordinary abc over K supplies the first
condition; [Zywina's Theorem 1.2](https://arxiv.org/html/2505.16960v1)
supplies the second for quadratic K/Q. The architecture is due to
[Pasten and Vidaux, arXiv:2611.24748v1](https://arxiv.org/html/2611.24748v1).
Prepared pole completeness and density use precisely Burungale's
published beta-seven, eta-one Theorem B. Composition with a Z-over-Q
polynomial retains **all** its original arithmetic inputs. The finite
exception correction remains ineffective. These field results do not
impose the unresolved square equality at the original 25/11 detectors.

## Constructions at the v59 checkpoint

| Construction | Total variables | Degree | Monomials | Sufficient fixed parameter |
|:--|--:|:--|:--|:--|
| [General finite-algebra family](../papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | 25 | $\le5059009872658432<2^{53}$ | $<2^{1193}$ | Every sufficiently large odd exponent; ineffective threshold |
| [Fully specified general polynomial](../papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | 27 | $\le99279020543180800<2^{57}$ | $<2^{1401}$ | $L=20483$ is sufficient |
| [General quartic](../papers/quartic/quartic195_20261116_v45.tex) | 195 | Exactly 4 | Exactly 2,956 | Every sufficiently large $N$; ineffective threshold |
| [Fully specified quartic](../papers/quartic/quartic257_20261116_v45.tex) | 257 | Exactly 4 | Exactly 3,679 | $N=9682$ is sufficient |
| [Weak-abc $121/100$ family](../papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | 13 | $\le43211777<2^{26}$ | $<2^{284}$ | Every sufficiently large odd $B$; ineffective threshold |
| [Weak-abc $16/15$ family](../papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | 13 | $\le39858177<2^{26}$ | $<2^{283}$ | Every sufficiently large odd $B$; ineffective threshold |
| [Ordinary-abc derivative family](../papers/conditional_few_variables/derivative_detector11_20261117_v59.tex) | 11 | $\le5444199553<2^{33}$ | $<2^{309}$ | Every sufficiently large odd $B$; ineffective threshold |
| [Ordinary-abc quartic](../papers/quartic_existence/quartic_abc71_20261116_v49.tex) | 71 | Exactly 4 | Exactly 1,187 | Every sufficiently large odd $B\ge81$; ineffective threshold |

The first four rows add no abc or Szpiro conjecture to their retained arithmetic premises. Ordinary Szpiro supplies the weak exponent $121/100$; ordinary rational abc supplies both displayed weak exponents. The 71-variable quartic uses ordinary rational abc. All eight retain their applicable elliptic, height, pole and prime-pattern inputs. The full independent audit of these arithmetic foundations is not declared complete.

All listed polynomials have integer content one. The five unrestricted-degree constructions are unexpanded finite determinant specifications with certified upper bounds. The three quartics are fully expanded. Their exact heights are, respectively,

$$
\max\{126616122944180358034867798936,149^{2N+2}\},\qquad
149^{19366},\qquad B^2+1.
$$

The first height formula holds for every $N\ge1$; the last holds for the permitted odd $B\ge81$. Neither algebraic range supplies an effective defining threshold. The fully specified 27-variable coefficient height is below $2^{2^{70}}$. See the [current records](../data/results_20261117_v59.json) for the exact source binding of every figure.

## Retained elliptic and prime-pattern inputs

The [arithmetic-dependency paper](../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex) identifies the quantified source statements. The specified curve over $K=\mathbb Q(\sqrt2)$ and point $P$ supply the cyclic doubled subgroup and the index-height bounds. The [all-point trace theorem](../papers/trace_heights/trace_on_all_points_20261113_v25.tex), [aggregate trace-height theorem](../papers/trace_heights/aggregate_trace_height_20261108_v9.tex), and [weighted trace theorem](../papers/trace_heights/weighted_trace_20261114_v27.tex) give the formulations needed by the corresponding sources, including the stated torsion and half-index cases.

The simultaneous prime-pattern input must provide prime values together with finite congruences, denominator divisibility, fixed avoidance, conjugate reduction-order conditions and compatible real approximation. The [prime-selection paper](../papers/prime_selection/prime_selection_20261109_v12.tex) derives the form used from the pinned Sun source, arXiv:2610.20691v2. The finite exceptional set and all coefficient divisibility conditions are fixed before prime selection. A finite residue check alone does not establish this global existence input.

## Contact heights and source soundness

The general sources use the full normalized modular realization, not just an unproved numerical height inequality. The [differential-evaluation](../papers/contact_heights/evaluation_of_differentials_20261109_v17.tex), [scalar-character](../papers/contact_heights/nebentypus_and_contact_heights_20261110_v18.tex), and [multiplicity](../papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.tex) papers state the required normalization and derive the five-contact bounds. Two disjoint contact blocks give the scalar-height improvement used in the source soundness proof. The complete [precision-two transfer](../papers/pole_parameters/precision_transfer_20261117_v56.tex) retains reciprocal orders one and uses an eighth-order formal logarithm for sixth-order comparisons. Its count is 25; no numerical determinant bound is assigned to that alternate circuit.

The conditional [direct-comparison theorem](../papers/conditional_few_variables/direct_input13_20261110_v22.tex) uses weak rational abc for six-contact and binary-power height bounds. If an extracted root index $n$ differs from the input $X$, both contact radicals divide the numerator of $X-n$. Strict height absorption and the trace-index bound contradict a sufficiently large fixed shift. The [height amplification paper](../papers/contact_heights/input_height_amplification_20261110_v22.tex) states the general inequality and its hypotheses.

The [71-variable quartic](../papers/quartic_existence/quartic_abc71_20261116_v49.tex) uses the ordinary-abc eight-contact estimate, the [mixed-power height theorem](../papers/elliptic_heights/mixed_power_height_20261116_v45.tex), and the scaled physical trace already in its point chart. Its absorption coefficient is $602/679$. Recovering the unscaled trace is included in the proof and costs no additional coordinate. Every inverse, auxiliary square, torsion branch and zero-input witness is covered by the complete system.

## Pole realization and intrinsic transfers

The finite-algebra records use the pole implications, nonzero realization and complete guard statements specified in their source papers. The [nonzero-witness theorem](../papers/pole_parameters/pole_witness_density_20261109_v14.tex) makes the required converse and descent inputs explicit. Bare solubility would not justify the nonzero ordinate or every algebra-character guard.

The [intrinsic pole theorem](../papers/pole_parameters/intrinsic_pole_20261117_v56.tex) offers a separate pole block of degree nine and coefficient height four. Its local implication excludes negative odd valuations at every prime without a guard. For the specified positive prepared inputs with square reduced denominator and two-adic class seven, Burungale, arXiv:2611.16130v1, Theorem B, supplies a dense rational witness projection. The theorem verifies that source's hypotheses; it does not independently reprove the entire external arithmetic argument.

The complete [general intrinsic transfer](../papers/pole_parameters/general_intrinsic_transfer_20261117_v57.tex) and [conditional intrinsic transfer](../papers/pole_parameters/conditional_intrinsic_transfer_20261117_v57.tex) check the early scalar, reduced denominators, ordered preparation and whole-character guards needed to use this block. They retain 25 and 13 variables. Their changed circuits have no new complete numerical degree or coefficient specification; the numerical table above remains attached to the earlier certified circuits.

## Finite algebra and exact computation

The [single-norm encoder](../papers/finite_algebra/unit_norm_20261114_v28.tex), [subalgebra-norm theorem](../papers/finite_algebra/subalgebra_norms_20261114_v30.tex), and [terminal-root theorem](../papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) distinguish rational characters from arbitrary algebraic roots. The final quadratic ordinate may vanish; all preceding radicands and required denominators remain guarded. The complete character-descent argument covers the resulting nonreduced final fiber.

The [71-variable coefficient package](../computation/quartic/abc71_v49), [195-variable package](../computation/quartic/affine_laurent195_v45), and [257-variable package](../computation/quartic/affine_laurent257_v45) contain exact full expansions and independent checks. Parameter powers are fixed coefficients, not quantified coordinates. Passing computations certify their listed identities, counts, coefficients and finite arithmetic assertions; they do not prove an unproved arithmetic realization theorem.

## The 21/9 realization gap

The [trace-conic criterion](../papers/pole_parameters/trace_conic_criterion_20261117_v57.tex) is the simpler current target: each actual value $V^2+w(2-V)$, optionally multiplied by $1+24V$ or $1+3(V-1)^2$, must be a rational square. These classes lose no contact and preserve the original height arguments in both the general and conditional sources. Its complete finite-algebra count is proved under the stated rational realization hypothesis; that hypothesis remains open.

The [native-square criterion](../papers/pole_parameters/native_square_criterion_20261116_v53.tex) gives a complete 21/9 census if actual guarded detector tuples satisfy its simultaneous rational square conditions. The [single-cover theorem](../papers/pole_parameters/single_cover_criterion_20261117_v56.tex) gives a conditional nine-coordinate criterion with a more restricted contact argument. The [variable-class theorem](../papers/pole_parameters/variable_squareclasses_20261117_v57.tex) permits certain input- and root-dependent classes with controlled height in the conditional source. **None proves uniform rational realization.** Arbitrary rational trace and norm coordinates cannot replace the actual detector functions.

The [prepared covering obstruction](../negative_results/papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex) gives an everywhere locally soluble one-coordinate specialization with no rational point. Its exact Cassels pairing shows why local congruences or positive elliptic rank alone cannot settle the required abscissa class. The obstruction is to that specified prepared-input family, not to every actual source coupling.

## Signed height and small-class criteria

The [signed mixed-power theorem](../papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex) proves its rational-height bound directly from the stated weak abc inequality, including both signs and arbitrary denominator cancellation. The optimized single-cover argument degrees are 48 for fixed classes and 60 for the permitted varying menu under ordinary abc. They do not certify a complete defining polynomial without actual rational realization. The [small trace classes](../papers/pole_parameters/small_trace_classes_20261117_v58.tex) use the existing Sun modulus containing three, retaining selected primes congruent to one modulo 24 and the original order conditions. They introduce no additional arithmetic hypothesis or lost contact. The actual multiplication-surface obstruction uses characteristic-zero Riemann–Hurwitz; it does not exclude individual rational witnesses.

For the smallest trace cubic, the point $(4,4)$ has infinite order for every rational $0<w\le1/4$. This uses the same Mazur torsion theorem cited for the earlier cubic, together with exact division-polynomial and independent group-law computations. It supplies no actual prescribed-trace realization hypothesis.

## Ordinary-abc derivative detector

The [eleven-variable theorem](../papers/conditional_few_variables/derivative_detector11_20261117_v59.tex) uses ordinary rational abc through two specific consequences: the homogeneous squarefree-form radical bound in Rudnick–Sarnak–Zaharescu, Appendix A.2, equation (A.2), and the fixed exponent $1001/1000$ for the binary- and signed-power height lemmas. The first consequence is not asserted from either previously used weak exponent. Its fixed forms yield a bound on multiple prime factors whose height coefficient is independent of the contact degree. The exact absorption margin is $87545567/198403000$.

Completeness applies **Sun, arXiv:2610.20691v3, Theorem 4.1**, to thirty-two fixed distinct integer coefficients after square-denominator dilation. The theorem explicitly allows every fixed finite number of positions. The argument checks all new derivative-denominator primes directly, then uses the prepared intrinsic Burungale theorem with its full parameter density. All three original elliptic point roles, their group and formal-comparison assertions, the one-point trace-height theorem and the one-coordinate finite-algebra encoder are retained. The sufficient shift remains ineffective.

The separate fixed-slope incidence theorem uses Poincare complete reducibility and Mordell–Lang after proving the rational endomorphism ring and nonconstancy on every relevant abelian translate. It concerns the stated earlier reweighted sources and supplies no nonexistence claim for individual witnesses or the derivative source.
