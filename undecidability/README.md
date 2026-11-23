# Variable bounds for undecidability over the rationals

Here `N` counts existential rational unknowns in a decision problem. The
integer input specifying an instance occurs in its coefficients and is not
counted. This is a separate objective from minimizing the total coordinates
of a polynomial defining the integers. All recorded numbers are upper bounds;
no global least value is claimed.

## Current unrestricted-degree results

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

## Current corrected quartic transfers

| Integer interface | Rational unknowns | Quadratic residuals | Additional height hypothesis |
|:--|--:|--:|:--|
| General | **979** | **829** | No additional abc |
| Specified | **1147** | **997** | No additional abc |
| Ordinary abc | **704** | **595** | Ordinary rational abc |

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
**1147**. See the [current v97 checkpoint](../docs/results_20261123_v97.md).
The general sufficient defining coefficient may have to be increased.

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
