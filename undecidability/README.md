# Variable bounds for undecidability over the rationals

Here `N` counts existential rational unknowns in a decision problem. The
integer input specifying an instance occurs in its coefficients and is not
counted. This is a separate objective from minimizing the total coordinates
of a polynomial defining the integers. All recorded numbers are upper bounds;
no global least value is claimed.

## Current frontier (v127)

See the [continuation report](../docs/results_20261124_v127.md) and the [current frontier ledger](frontier_20261124_v127.json). The new exact quartic tables and finite-algebra transfers give:

| Route | Quartic unknowns | Quadratic residuals | Unrestricted degree | Alternative published coding source |
|:--|--:|--:|--:|--:|
| General | **884** | 749 | **48** | 52 |
| Specified | **1049** | 912 | **50** | 54 |
| Ordinary rational abc | **302** | 251 | **36** | 36 |

The [theta reduction](positivity_theta_reduction_20261124/README.md) gives the two general quartics. The [signed-abscissa transfer](abc_signed_abscissa_v119/README.md), [mean-shifted cubic](abc_mean_shifted_curve_v120/README.md), and [exact elimination](exact_multiroute_elimination_v121/README.md) give the 323-variable predecessor; the [nested parity selector](abc_nested_selector_v122/README.md) improves it to 319 variables; the [scalar alternate failures](abc_scalar_failures_v123/README.md) give a 312-variable construction; the [exact normalized moments](abc_normalized_moments_v124/README.md) reduce it further to 309 variables; the [Sun-audit interpolation](abc_interpolated_mean_v125/README.md) and [paired denominator bound](abc_paired_height_v126/README.md) give 303 and the current 302 variables, respectively. The earlier 519-variable stage is superseded, with its proof retained. The [direct-index](direct_index_transfer_v111/README.md) and [selective-pole](abc_selective_pole_v110/README.md) theorems give the unrestricted-degree results. These are proved transfers under their stated retained arithmetic and coding premises, with Sun's ten-integer coding theorem accepted by the project for 48/50 ([review clarification](../docs/audits/sun_september_20261124/README.md)). The specified direct-index route is algorithmically specified and uses the full-family modular contact-height premise rather than the old fixed L=143 interface. The [shorter logarithm and whole-guard tagged encoder](direct_index_transfer_v127/README.md) give strict parametric total-degree bounds 11·2^96 δ and 11·2^98 δ for the Sun-source 48/50 transfers, where δ is defined in the proof. No numerical value for the full source's δ is claimed. The target near 263 and every global minimum remain open.

## Earlier unrestricted-degree results (v108 baseline)

The [common-numerator proof](papers/common_numerator_transfers.tex) and
[finite-wrapper proof](papers/finite_wrapper_transfer.tex)
([PDF](papers/finite_wrapper_transfer.pdf)) give:

| Source route | Additional height hypothesis | Rational unknowns | Degree strictly below |
|:--|:--|--:|--:|
| General two-detector source | No additional abc hypothesis | **82** | `2^532` |
| Specified three-detector source, `L=143` | No additional abc hypothesis | **100** | `2^578` |
| Ordinary-abc source | Ordinary rational abc | **52** | `2^425` |

These are proved transfer theorems **under the source's retained arithmetic
premises**. Those premises have not all been independently proved here.
The current v88 Bhargava–Burungale product poles are used; the former native
pole converse premise is not reintroduced. The general and abc sufficient
fixed parameters remain ineffective. The stored general `L=143` and abc
`B=3` sources are algebraic fixtures, not certified defining members.
The 100-variable source uses its specified sufficient parameter.

The new [paired spectral theorem](papers/paired_spectral_encoder.tex)
([PDF](papers/paired_spectral_encoder.pdf)) gives these smaller degree
ceilings using the same source algebras and the same variable counts.
The complete coefficient recipe and independent degree ledger are in
[alternative_v93](alternative_v93). Earlier degree bounds below identify
the historical encoders; all historical specifications remain unchanged.

**Certificates and replay:** [finite-wrapper identity/count ledger](certificates/finite_wrapper_transfer.json), [paired-spectral degree ledger](alternative_v93/certificate.json), and [machine-readable records](results.json). The independent [v90](../scripts/verify_v90.py) and [v93](../scripts/verify_v93.py) gates check the stored source hashes, finite-algebra ranks, variable counts, and strict degree ceilings. They do not independently establish the infinite arithmetic premises of the integer predicates. The final large determinant polynomials are specified by finite coefficient recipes, not fully expanded.

## Earlier corrected quartic transfers (v108 baseline)

| Integer interface | Rational unknowns | Quadratic residuals | Additional height hypothesis |
|:--|--:|--:|:--|
| General | **887** | **750** | No additional abc |
| Specified | **1052** | **913** | No additional abc |
| Ordinary abc | **605** | **528** | Ordinary rational abc |

The [v108 report](../docs/results_20261124_v108.md),
[general/specified proofs and tables](c_integrality_reduction_v106/README.md),
and [abc proof and table](abc_pell_integrality_v108/README.md) specify these
quartics completely. They retain 12 / 10 / 12 integer predicates and the
stated arithmetic interfaces. The [integrated checker](../scripts/verify_v108.py)
and [receipt](certificates/verification_v108.json) audit all thirteen new
complete tables and the separate arithmetic checkpoints. The original
reported 948/1127/649 artifacts were not located: 948/1127 were independently
reconstructed, and a new 605-variable abc construction improves on 649.

The [corrected-source theorem](source_repair_v93/corrected_jones_source.tex)
([PDF](source_repair_v93/corrected_jones_source.pdf)) uses Jones's 1980
Theorem 2 and the independently proved `n^6` binomial block. The new tables
therefore do not assume `U_em`; they retain all arithmetic premises of the
integer interfaces and cite the classical coding theorem externally.
This is a new source, not a proof that the old expanded source was correct.
The [complete tables](source_repair_v93/coefficients) include every quadratic
row and every parameter. Squaring and summing gives degree exactly four.

The [ceiling power circuit](papers/ceiling_power_quartic_checkpoint.tex)
saves 29 coordinates in every route. The [fixed dyadic contact grid](papers/abc_fixed_contact_offsets_v93.tex)
saves 22 further coordinates in the abc route. Its general tuple certificate
uses `48k+8` coordinates and `41k+5` quadratic rows, including the k inputs.
Completeness is proved for nonzero integer tuples, which includes all
positive witnesses used in the source reduction. All twelve integer tests
remain. The [common contact progression](general_contact_v94/affine_contact_progressions.tex)
saves 26 further variables in each general route, and the
[signed source theorem](source_repair_v93/signed_binomial_positivity.tex)
saves five in all routes. Their complete compositions and independent
checks are recorded in the [v94 report](../docs/results_20261123_v94.md);
source correction and degree improvements are in the
[v93 report](../docs/results_20261123_v93.md).
The [one-quotient Pell theorem](pell_crt_v95/one_quotient_pell.tex) removes
one integrality predicate, saving another **60 / 75 / 47** variables.
The [v95 report](../docs/results_20261123_v95.md) records the complete
eleven-block systems and exact coefficient audits. The
[half-trace square](pell_halftrace_v96/halftrace_guard.tex) then absorbs
the s-nonzero guard, saving one more variable and row in each route.
The [v96 report](../docs/results_20261123_v96.md) records those
eleven-predicate systems. The [new Pell power source](pell_power_v97/pell_power_replacement.tex)
then recovers the fixed exponent using two extra integer predicates and
the remaining source constraints. The complete thirteen-predicate systems
reach **979 / 704** in the general / abc routes; the specified route keeps
**1147**. See the [v97 checkpoint](../docs/results_20261123_v97.md).
The general sufficient defining coefficient may have to be increased.
The [signed-power proof](pell_signed_q_v98/signed_q_and_absorbed_bound.tex)
removes both added positivity wrappers by a signed prefix estimate and an
absorbed integer margin. The abc chart also reuses its existing fourth
power. These complete systems have **973 / 1147 / 697** variables;
see the [v98 report](../docs/results_20261123_v98.md) and
[full tables](pell_signed_q_v98). These changes keep all thirteen integer
certificates in the general and abc constructions.
The [product identity](pell_product_v99/pell_product_elimination.tex)
then removes one square register from each route by an exact polynomial
inverse lift. This gives **972 / 1146 / 696** variable counts,
with **826 / 996 / 591** quadratic residuals. See the
[v99 report](../docs/results_20261123_v99.md) and [full tables](pell_product_v99).
The [aggregate-spacing proof](aggregate_spacing_v100/aggregate_spacing.tex)
then determines the spacing from already fixed difference points. Its
affine substitution removes one variable in the general and specified
systems. These counts are **971 / 1145 / 696**; see the
[v100 report](../docs/results_20261123_v100.md) and
[complete tables](aggregate_spacing_v100).
The [signed first-Pell theorem](pell_signed_branch_v101/signed_branch_projection.tex)
then admits both trace signs, recovers binomial divisibility with an
alternating sum, and reconstructs positive witnesses for the same coding
prefix. Deleting its sign square gives **970 / 1145 / 695**
counts; see the [v101 report](../docs/results_20261123_v101.md).
The [contact-endpoint rechart](contact_endpoint_v102/contact_endpoint_reuse.tex)
then reuses two endpoint powers to eliminate two shared coefficients and
two rows. The intermediate counts are **968 / 1143 / 695**, with
**823 / 994 / 590** residuals; see the [v102 report](../docs/results_20261123_v102.md).
The [c-integrality checkpoint](c_integrality_checkpoint_v102/README.md)
gives an exact counterfamily for the three-norm subsystem, while leaving
the full-source integrality question open and retaining the c predicate.
The [shared-denominator theorem](quadratic_reduction_v103/contact_denominator_compression.tex)
([PDF](quadratic_reduction_v103/contact_denominator_compression.pdf)) then replaces
fourteen or twelve private contact-combination coordinates by nine common
coefficients, giving **963 / 1140 / 695** and **818 / 991 / 590** rows.
This preserves each entire rational zero set bijectively. The
[v103 report](../docs/results_20261124_v103.md) and
[complete tables](quadratic_reduction_v103) supply the proof and exact audit.
The [new source-frontier checkpoint](source_frontier_v103/README.md) proves
an integral-trace criterion and identifies a unary-exponential source;
neither removes an integer predicate at this stage.

The [input-comparison identity](input_comparison_v105/README.md)
independently reconstructs **948 / 1127** from v102 and gives **943 / 1124**
after combining the shared denominators with
[BB-native poles](quadratic_reduction_v104/README.md). Under ordinary abc,
the [common numerator](abc_common_numerator_v103/README.md),
[odd quotient](odd_pell_quotient_v104/README.md),
[point rechart](abc_point_rechart_v105/README.md), and
[directly scaled chart](abc_scaled_point_v106/README.md) give
**675, 674, 656, and 645** variables. All zero-input fibers and changed
coordinate occurrences are included in the exact audits.

The [signed Pell classification](pell_classification_reconstructed_v105/README.md)
then leads to a [new integrality theorem](pell_integrality_replacement_v106/README.md):
when the source supplies `3|a`, the retained integral shifted trace and
one half-trace square force c and d to be integers. Deleting the complete
c predicate gives the current **887 / 1052 / 605** bounds, with full
shared-contact reconstruction and canonical completeness witnesses.
The [abc pole audit](abc_bb_native_v107/README.md) also supplies all twelve
remaining native CM poles directly from Bhargava–Burungale, without changing
the table. Other arithmetic interfaces and the external coding theorem remain.

The target near **263** remains open. The
[second-quotient counterexample](pell_quotient_obstruction_v109/README.md)
isolates the missing c-square divisibility; it is a subsystem counterexample,
not a full-source one. A [three-power outer compiler](unary_outer_checkpoint_v109/README.md)
is proved for the alternative unary exponential source, but its lower
circuits and exponential graphs remain uncompiled, so it supplies no new N.

### Method and intermediate improvements

Sun's mixed-domain representation uses eight arbitrary integer unknowns
and one nonnegative integer unknown. The substitution

```math
L(s,t,u)=s^2+t^2+u^2+u
```

represents every nonnegative integer and is at least `-1/4` over the
rationals. Requiring its value to be an integer therefore forces it to be
nonnegative. It replaces one input with three coordinates, a net cost of two.

The initial [independent-block theorem](papers/transfer_general_degree.tex)
([PDF](papers/transfer_general_degree.pdf)) gives `9m+2`, hence
**227 / 245 / 101**. Its common degree bound `2*eta(58,4)` is much smaller
than the new joint bounds, so it remains a useful tradeoff.

The [guarded finite-algebra encoder](papers/joint_finite_algebra_encoder.tex)
([PDF](papers/joint_finite_algebra_encoder.pdf)) combines any finite set of
root-existence conditions with one rational encoding coordinate. Its proof
allows nilpotents, repeated roots and denominators vanishing on excluded
characters. Merging only the nine encoders gives `9m-6`, hence
**219 / 237 / 93**, without sharing any ordinary witnesses.

The further reduction proves simultaneous witness construction. Seven
point roles and one translated contact parameter can be common in the
general sources. This gives joint certificates for `Z^k` in **`9k+16`**
or **`11k+16`** total coordinates. The ordinary-abc variant shares its
reference point and a scaled contact parameter, first lifting each input
to `X_i^2+1`; its count is **`7k+4`**. Set `k=9` and add the wrapper's two
coordinates to obtain the earlier 99/117/69 bounds.

The [complete compressed source circuits](joint_sources) specify every
coefficient node, finite block, coordinate map and guard. The final
polynomials are given by finite determinant formulas and have not been
fully expanded. The [exact certificate](certificates/shared_integer_transfers.json)
records all counts, hashes and matrix-entry degree bounds.

The [common-numerator theorem](papers/common_numerator_transfers.tex)
([PDF](papers/common_numerator_transfers.pdf)) replaces every private
numerator point by one common point. Its index is chosen independently of
the reference index. The all-sign coprimality clause of the retained prime
supplier allows different target residues at the disjoint input contact
families. Prime-power refinements preserve the formal depths, and the
existing contact weights suppress bounded comparisons at fixed places.
The new tuple counts are **`7k+18` / `9k+18` / `5k+6`**, giving
**83 / 101 / 53**, with the original degree ceilings `2^413 / 2^477 / 2^263`
(now `2^302 / 2^349 / 2^212` using the paired spectral encoder).
The [new complete circuits](common_numerator_sources) and
[exact certificate](certificates/common_numerator_transfers.json) are supplied.

The [finite-wrapper theorem](papers/finite_wrapper_transfer.tex) then
absorbs the mixed universal equation and one positivity witness into a
rank-sixteen finite algebra. Its generators recover the ninth input and
the omitted witness; all **nine integer predicates remain**. Two monic
relations and a single additional guard suffice. The old encoder handles
the new finite generators, so no new ordinary variable is introduced.
This gives the headline **82 / 100 / 52** bounds, at a higher degree.
The manuscript gives the full source coefficient recipe, both directions,
denominator rescalings, a general equation-absorption principle and the
[certified degree ledger](certificates/finite_wrapper_transfer.json).
The [executable compiler and format guide](finite_wrapper_sources/README.md)
turn any supplied sparse source polynomial into the whole coefficient DAG;
the stored demonstration is explicitly nonuniversal.

## Historical quartic checkpoints: old source universality unresolved

The [direct quadratic compilation](papers/jones1980_quartic_transfer.tex)
([PDF](papers/jones1980_quartic_transfer.pdf)) proves an exact equivalence
with a precisely displayed emended 28-variable positive-integer system.
It uses twelve integrality inputs, a 169-step signed power chain,
geometric-quotient integrality, automatic positivity on a cofinite instance
tail and Pell powers restoring positive witnesses.

The source audit found that Jones's 1980 announcement prints **Greek alpha**
in a coefficient where the builder uses **Latin a**. Matiyasevich's
1999 author-written chapter supports Latin a, but has a separate impossible
Pell row. The full universality proof for this precise emended system has
not been verified. We state that missing assertion explicitly as **`U_em`**.
It is separate from abc and from the integer predicate's arithmetic premises.
The new independent Pell audit also exposes an `n^2` versus `n^6`
discrepancy in the natural identification with the modern binomial bridge.
The old source parameter is preserved literally in every table above.

The [shared-reference construction](papers/shared_quartic_checkpoint.tex)
first gave 2086/2278/846. A [reciprocal-input rechart](papers/reciprocal_reference_checkpoint.tex)
then removes one coordinate and one row in each general system.
The [common-point theorem](papers/common_points_quartic_checkpoint.tex)
([PDF](papers/common_points_quartic_checkpoint.pdf)) identifies 54/50
actual common physical coordinates, including the newly shared input
numerator point, giving the intermediate 1601/1837 bounds. The subsequent
[global-contact theorem](papers/global_gauge_quartic_checkpoint.tex) gives
1185/1355, and the [Pell-core theorem](papers/pell_index_optimization.tex)
([PDF](papers/pell_index_optimization.pdf)) removes nine more coordinates
from each complete system, also improving the abc checkpoint. Further
[scalar-point](papers/scalar_rechart_quartic_checkpoint.tex),
[scalar-norm](papers/scalar_norm_compression.tex), and
[detector-trace](papers/detector_trace_compression.tex) reductions give the
current general and specified counts:

| Integer interface | Independent combined system | Current checkpoint | Quadratic residuals | Additional height hypothesis |
|:--|--:|--:|--:|:--|
| General, 163 coordinates | 2,195 | **1,074** | 924 | No additional abc |
| Specified, 179 coordinates | 2,387 | **1,254** | 1,080 | No additional abc |
| Ordinary-abc, 56 coordinates | 911 | **808** | 696 | Ordinary rational abc |

The physical function dictionary, all normalization weights, and the
stronger common-index precision are proved before the registers are
identified. The current construction uses one global contact gauge. Its proof controls
foreign contact poles and fixed-place limits; it does not assume that the
contacts of arbitrary rational solutions are disjoint. Every residual is
supplied in the [independent tables](coefficients/jones1980),
[shared-reference tables](coefficients/jones1980_shared),
[reciprocal tables](coefficients/jones1980_shared_reciprocal) and
[common-point tables](coefficients/jones1980_common_points),
[global-gauge tables](coefficients/jones1980_global_gauge), and
[Pell-core tables](coefficients/jones1980_pell_core),
[scalar-norm tables](coefficients/jones1980_scalar_norm),
[detector-trace tables](coefficients/jones1980_detector_trace), and
[current combined tables](coefficients/jones1980_detector_pell).
Their sums of squares have degree exactly four. The complete tables are
reconstructed row by row, including every removed duplicate.
**Their undecidability interpretation remains conditional on `U_em`** and
all selected interface premises. A quartic bound near 263 has not been
established.

The [literal Mishchenko–Treier audit](papers/mt_source_audit.tex)
([PDF](papers/mt_source_audit.pdf)) proves a reversible **62/50 to 57/45**
reduction. Its universality is unresolved because of discrepancies in its
Pell and product equations. This does not independently reprove the alleged
universal **57-positive-integer-variable / 47-quadratic** theorem.

The earlier **2,539 / 2,779 / 934** candidates were registered first in the
[baseline checkpoint](checkpoints/baseline_20261123.md). Their historical
status is preserved in the registry.

## Further exact reductions of the combined system

The [scalar rechart](papers/scalar_rechart_quartic_checkpoint.tex) shares
one scalar abscissa and its products, and removes twelve now-unnecessary
inverse normalizers in the specified interface. It saves 42/32 coordinates.
The [norm-polynomial compression](papers/scalar_norm_compression.tex) then
uses the three common coefficients of `N(K+RQ)/Tr(K)` to eliminate each
private two-component scalar field, saving another 21 coordinates.
The [detector-trace compression](papers/detector_trace_compression.tex)
replaces each private detector product by its appropriately normalized
rational trace. Two common field components suffice; the norm of that
field is inlined as a quadratic expression. This saves ten more coordinates.
Every reduction has full reconstruction maps and an exact occurrence audit.

| Stage, before the nine-coordinate Pell reduction | General | Specified |
|:--|--:|--:|
| Global contact gauge | 1185 | 1355 |
| Scalar rechart | 1143 | 1323 |
| Common norm coefficients | 1122 | 1302 |
| Detector trace | 1112 | 1292 |
| After the separate Pell reduction | **1103** | **1283** |

## Quadratic ceiling-binary power circuit

The [new power theorem](papers/ceiling_power_quartic_checkpoint.tex)
([PDF](papers/ceiling_power_quartic_checkpoint.pdf)) replaces the 168 stored
powers computing `b^(5^60)` by **139 coordinates**. Starting at the existing
`b^5`, its 137 ceiling-binary steps use either `v_next=v^2` or
`b*v_next=v^2`. The unchanged prefix and positivity equations already force
`b>0`. The complete counts are **1074 / 1254 / 808**, with
**924 / 1080 / 696** quadratic residuals. Every non-power row is preserved
literally. The [tables](coefficients/jones1980_ceiling_power) and independent
checker also prove a restricted 139-coordinate lower bound within the stated
nonnegative-exponent triangular monomial chart; no global minimum is claimed.

## Independently proved local improvements

The [Pell-index proof](papers/pell_index_optimization.tex) classifies the
three-Pell block from elementary descent, divisibility and trace residues.
It replaces `G=a+F^2(d^2-a)` by `G=a+F^2(c+1-a)`, removes the separate
`d^2` register, proves two positivity wrappers unnecessary, and replaces
another by `zeta^2=(a-1)(d-1)`. All twelve integrality tests remain.
The theorem also covers arbitrary prescribed indices after a parity adjustment.

The [binomial certificate](papers/binomial_pell_certificate.tex) proves,
for `r>=1`, `M>=2`, and `2<=b<=2M`, an exact polynomial characterization
of `b` being a power of two and `M` dividing `binom(2r,r)`. A one-sided
Pell approximation and integer rounding prove both directions. Setting
`M=n^2` explains the corrected `n^6` parameter. This is an independent
local theorem; it does not verify the complete source coding argument.

The [negative-witness proof](papers/negative_mixed_witness.tex) gives an
explicit specialization, for every mixed source polynomial and instance,
with `Q(n)=25^8(n+9)^4(n+7)^4`. Thus the other eight integer predicates do not
force the ninth input to be nonnegative; that restriction cannot be omitted.
The finite-wrapper theorem retains it.

The [point-chart paper](papers/point_chart_research.tex) proves the exact
chart reduction and specific obstructions to sharing alternate numerator
points or replacing their two parameters by one input-independent parameter.
Those obstructions do not constitute a general lower bound.

## Limitations and further work

The [polynomial integrality obstruction](papers/polynomial_integrality_obstruction.tex)
([PDF](papers/polynomial_integrality_obstruction.pdf)) proves that fewer than
`r` rational-coefficient polynomial integer-value tests cannot recognize all
of `Z^r` inside `Q^r`. Counterexamples exist at infinitely many denominator
primes, with unbounded denominator exponents. The theorem does not exclude
shared existential witnesses or extra equations of a particular source.

The [further-reduction checkpoint](checkpoints/further_reductions_20261123.md)
records the obstruction to applying common-squareclass pole sharing in the
current fresh-prime construction. Next steps are to audit the complete
Jones 1982 proof, seek a new simultaneous point/pole realization theorem,
remove private translated-point registers while preserving degree two,
and compile any resulting improvement with exact source maps.

## Reproduction and recordkeeping

```sh
python -B undecidability/verify_transfer_general_degree.py
python -B undecidability/verify_joint_sources.py
python -B undecidability/verify_jones1980.py
python -B undecidability/verify_shared_reference.py
python -B undecidability/verify_common_numerator.py
python -B undecidability/verify_finite_wrapper.py
python -B undecidability/verify_finite_wrapper_compiler.py
python -B undecidability/verify_reciprocal_reference.py
python -B undecidability/verify_common_points.py
python -B undecidability/verify_global_gauge.py
python -B undecidability/verify_pell_core_reduction.py --include-abc
python -B undecidability/verify_pell_index_optimization.py
python -B undecidability/check_point_chart_lemmas.py
python -B scripts/verify_v92.py
python -B scripts/verify_v91.py
python -B scripts/verify_v90.py
python -B scripts/verify_v89.py
```

The gate rebuilds the complete specifications and checks the recorded source
qualifications. A `PASS` verifies the stated finite identities and counts;
it does not discharge arithmetic foundations or `U_em`. Proofs, source
citations and the verification scope are in the manuscripts. The
[machine-readable registry](results.json) separates proved transfers from
source-audit checkpoints; the [project report](../docs/results_20261123_v92.md)
summarizes the mathematical changes and their limits.
