# Polynomial presentations of the integers over the rationals

Complete proofs and exact computational specifications for integer polynomials

```math
F(X,Y_1,\ldots,Y_m)
```

whose rational input projection is the integers, under the arithmetic premises stated in each construction.

**Every defining-polynomial variable count includes the input.** The separate [undecidability category](#fewest-variables-currently-recorded-for-undecidability) counts existential rational unknowns; its instance input is encoded in the coefficients. **The 25 / 27 / 11 bounds for defining the integers are not in conflict with the 52 / 54 / 36 unrestricted-degree undecidability bounds:** they answer different questions and use different variable-counting conventions. Degree means total degree. Coefficient height is the maximum absolute integer coefficient after the fixed parameters have been substituted. We optimize variable count, then degree, then coefficient height. No global minimum is claimed.

## Current constructions — 24 November 2026

The reductions **193→165, 229→180, 68→62 and 13→11** come from **notes of Gabe Conant with Astra 6.2**. They have been audited and integrated here, with further degree, coefficient and hypothesis improvements. The [source audit](docs/results_20261119_v78.md) distinguishes those contributions from the subsequent work. The [v81 continuation](docs/results_20261119_v81.md) further reduces the ordinary-abc quartic through **62→59→58→56 variables**, using a nonlinear contact rechart and the published pole theorem directly. The [v82 continuation](docs/results_20261120_v82.md) reduces the general quartics to **163 and 179 variables**, with complete ordered witness constructions.

The [Bhargava–Burungale v2 audit](docs/results_20261123_v88.md) now lowers the degrees in **all five current few-variable routes**, using a normalized product pole, a class-seven scalar and balanced squareclass representatives. It also proves an overlapping-support simultaneous-twist theorem, two-test quadratic arithmetic in the BB index model, and a three-square interval wrapper. The last improvement saves one rational variable relative to the paper's still-unspecified parameter `r`; it is not a new numerical defining-variable record. All new proofs, complete specifications, independent checks and [all-route qualifications](docs/bb_all_route_status_20261123_v88.md) are supplied. The [24 November BB-native quartic replacement](papers/quartic/bb_native_quartics_20261124.tex) additionally replaces the older native non-CM pole in the 163- and 179-variable systems without introducing variables; it is the **preferred version** of these two quartics. It uses the congruent-number theorem directly and retains all other stated arithmetic inputs. The exact new tables and independent Laurent reconstruction are [here](computation/bb_native_quartic_20261124/README.md). The [current pole-dependency map](docs/current_pole_dependencies_20261124.md) identifies which active constructions now depend directly on Bhargava–Burungale and distinguishes the archived Theorem 5.3/Route K material.

“None” in the height-hypothesis column means **no additional conjecture beyond the arithmetic premises explicitly retained in the proof**. A complete independent audit of all inherited elliptic, prime-pattern, pole-realization and height foundations has not been established.

| Construction | Additional height hypothesis | Total variables | Degree | Coefficients and effectiveness | Expanded TXT size (kB) |
|:--|:--|--:|:--|--:|--:|
| [General few-variable family](papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) | None | **25** | **≤ 48,318,382,080** | Balanced BB product pole and projective encoder; sufficient odd exponent ineffective. | Not expanded; <2^825 (L=143 fixture bound) |
| [General BB-native quartic family](papers/quartic/bb_native_quartics_20261124.tex) | None | **163** | **4, exact** | 137 quadratic squares; **2,771 monomials**; class-seven congruent-number poles, all other inputs retained. The [earlier BB-parameter result](docs/results_20261120_v87.md) belongs to the historical v82 presentation. | [60.638](computation/bb_native_quartic_20261124/expanded/quartic163-N1.txt) (N=1 algebraic fixture) |
| [Fully specified general polynomial](papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) | None | **27** | **≤ 183,368,679,424** | Explicit `L=143`; coefficient height < `2^(2^45)`. | Not expanded; <2^941 (L=143 upper bound) |
| [Fully specified BB-native quartic](papers/quartic/bb_native_quartics_20261124.tex) | None | **179** | **4, exact** | 151 quadratic squares; **3,012 monomials**; 748-bit exact height. | [66.484](computation/bb_native_quartic_20261124/expanded/quartic179.txt) |
| [Few-variable family under abc](papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) | Ordinary rational abc | **11** | **≤ 3,261,569** | Twelve contacts and normalized BB product pole; sufficient fixed odd shift ineffective. | Not expanded; <2^215 (B=3 fixture bound) |
| [Asymmetric-contact quartic (current abc record)](computation/asymmetric_contact54_20261124/README.md) | Ordinary rational \(abc\) | **54** | **4, exact** | 44 quadratic squares; 788 coordinate monomials; sufficiently large fixed B congruent to 1 modulo 8, cutoff ineffective. | [11.174](computation/asymmetric_contact54_20261124/expanded-B1.txt) (B=1 algebraic fixture) |
| [Previous quartic family under abc](papers/quartic_existence/paired_contact56_20261119_v81.tex) | Ordinary rational abc | **56** | **4, exact** | 46 quadratic squares; 809 monomials; sufficient fixed odd shift ineffective. | [11.564](computation/expanded_text_v84/quartic56-B3.txt) (B=3 fixture) |

The [asymmetric-contact improvement](computation/asymmetric_contact54_20261124/README.md) replaces the derivative contact quotient by a two-slot rational weight and removes two quadratic coordinates. It gives the current **54-variable ordinary-abc quartic**, retaining the previous group, height and prime-pattern premises and the published class-seven pole theorem. Its complete coefficient table and independent reconstruction are included. The previous 56-variable entry remains for historical comparison and verification.

The two eleven-variable routes under weak rational abc at exponents `121/100` and `16/15` have degree bounds **16,460,929** and **9,808,001**, respectively. Their sufficient odd shifts remain ineffective. See the [v88 theorem](papers/few_variables25/bb_product_degree_transfer_20261123_v88.pdf) for all five degree improvements and retained assumptions.

The last column gives **decimal kB (1 kB = 1,000 bytes)** for single-line ASCII, fully expanded TXT files with `x1` as the input, `x2`, ... as other variables, and no final newline. Numeric quartic sizes are **measured exactly**. The 163-variable `N=1`, 54-variable `B=1` and 56-variable `B=3` members are algebraic **fixtures, not certified defining members**. The other entries are extremely loose **upper bounds for the indicated stored circuit member**, not measurements or predictions of the first defining member. See [fully expanded TXT files and exact size formulas](docs/busy_beaver_and_expanded_sizes_20261120_v84.md).

The unrestricted-degree bounds describe complete finite determinant specifications; those enormous polynomials have not been fully expanded. All displayed quartics are exactly expanded. Every construction has integer content one, with primitive normalization where needed. Small coefficient fixtures and coefficient-height cutoffs are not sufficient defining parameters.

The [results JSON](data/results_20261123_v88.json) records all five new finite-algebra specifications and parameter qualifications; the [v82 records](data/results_20261120_v82.json) preserve the unchanged quartic specifications. The new fixture TXT upper bounds use the same exact character-count argument as v84, replayed in the v88 gate. Weaker fixed-exponent versions of abc and alternative coefficient presentations are retained in the [detailed proof guide](docs/results_20261119_v78.md#weaker-hypotheses-and-generalizations).

## Fewest variables currently recorded for undecidability

The [undecidability category](undecidability/README.md) counts existential
rational unknowns; the integer instance is encoded in coefficients.
The [v113 continuation](docs/results_20261124_v113.md) gives the current bounds, complete quartic tables, direct-index and selective-pole proofs, and the [current frontier ledger](undecidability/frontier_20261124_v113.json).

| Degree restriction | Additional height hypothesis | Rational unknowns | Status |
|:--|:--|--:|:--|
| Unrestricted degree | No additional abc hypothesis | **52** | Direct-index transfer under the stated modular, trace-height and other retained inputs; **48** additionally importing Sun 2026 |
| Unrestricted degree, specified source | No additional abc hypothesis | **54** | Algorithmically specified direct-index transfer, retaining full-family modular and abscissa-sum inputs; **50** additionally importing Sun 2026 |
| Unrestricted degree | Ordinary rational abc | **36** | One selective derivative pole and finite-algebra encoding; retained arithmetic premises |
| Quartic transfer | No additional abc hypothesis | **884** | Theta positivity deletion; 749 residuals; 12 integer predicates |
| Quartic transfer, specified source | No additional abc hypothesis | **1,049** | Theta positivity deletion; 912 residuals; 10 integer predicates |
| Quartic transfer | Ordinary rational abc | **519** | Aggregate contacts, theta deletion and one shared native pole; 466 residuals; 12 integer predicates |

The smaller 48/50 bounds use an additional external source theorem from [Sun's 2026 preprint](https://arxiv.org/abs/2609.01594), not independently audited here. The 52/54/36 bounds use the previous published mixed-domain source. All new transfers have their stated retained arithmetic premises; no unconditional undecidability or global minimality is claimed. The unrestricted-degree recipes have finite uniform degrees, without a new numerical degree comparison claim here. The [v108 continuation](docs/results_20261124_v108.md) preserves the earlier tables and the interrupted-results reconstruction.

**Historical v108 quartic proof trail:** the [new arithmetic theorem](undecidability/pell_integrality_replacement_v106/pell_integrality_replacement.tex)
proves c-integrality from the retained norm, shifted trace, the source's
modulo-three condition, and one half-trace square. The complete
[887/1052 tables](undecidability/c_integrality_reduction_v106/README.md) and
[605 table](undecidability/abc_pell_integrality_v108/README.md) include all
coordinate and shared-contact changes. Their native pole realizations use
Bhargava–Burungale directly, including the [twelve abc poles](undecidability/abc_bb_native_v107/README.md).
The reported 948/1127 stage has been independently reconstructed; the original
reported 649 artifact remains unlocated. The [integrated verification receipt](undecidability/certificates/verification_v108.json)
records the exact tables and their limits. The target near 263 is still open.

**Proof trail for the 82 / 100 / 52 unrestricted-degree results:** the [common-numerator theorem](undecidability/papers/common_numerator_transfers.tex) first gives 83 / 101 / 53 unknowns; the [finite-wrapper theorem](undecidability/papers/finite_wrapper_transfer.tex) absorbs one coordinate into a rank-sixteen finite algebra, giving 82 / 100 / 52; the [paired-spectral theorem](undecidability/papers/paired_spectral_encoder.tex) gives the strict degree ceilings in the table without changing these counts. The exact [finite-wrapper certificate](undecidability/certificates/finite_wrapper_transfer.json), [paired-spectral degree certificate](undecidability/alternative_v93/certificate.json), [results registry](undecidability/results.json), and independent [v90](scripts/verify_v90.py) and [v93](scripts/verify_v93.py) verification scripts record the counts, source hashes, and degree arithmetic. These are transfer theorems *under the retained arithmetic premises*; the gigantic determinant polynomials are specified but not expanded, and no global minimality is asserted.

The [corrected-source proof](undecidability/source_repair_v93/corrected_jones_source.tex)
([PDF](undecidability/source_repair_v93/corrected_jones_source.pdf)) replaces
the questionable expanded source by a new system reduced to **Jones's 1980
Theorem 2**, using the independently proved binomial certificate with
`p=2*w*s^2*r^2*n^6`. Only two quadratic rows change, without additional
coordinates. This removes the old emendation premise `U_em` from the new
transfers. Jones's coding theorem remains an explicitly cited external
result; its coding proof and every inherited integrality foundation have
not been independently reproved here. The historical `n^2` tables and their
`U_em` qualification remain unchanged.

The [ceiling-binary power theorem](undecidability/papers/ceiling_power_quartic_checkpoint.tex)
reduces 168 power coordinates to 139, saving **29 variables** in every
quartic route. The [fixed-contact theorem](undecidability/papers/abc_fixed_contact_offsets_v93.tex)
then saves **22 more** in the abc route by separating all contact families
with fixed dyadic offsets and sharing one contact square. The
[complete corrected tables](undecidability/source_repair_v93/coefficients)
retain all twelve integrality certificates. Earlier global contact,
scalar-point, norm-polynomial, and detector-trace reductions remain part
of the general systems.
The [shared contact progression](undecidability/general_contact_v94/affine_contact_progressions.tex)
saves another **26 variables** in each general route. The
[signed binomial theorem](undecidability/source_repair_v93/signed_binomial_positivity.tex)
then saves **five** in every route by recovering two positive signs and
retaining one essential nonzero guard. The
[final general tables](undecidability/general_contact_v94) and signed abc
table retain all twelve integer certificates.
The [one-quotient Pell theorem](undecidability/pell_crt_v95/one_quotient_pell.tex)
then replaces two congruence quotients by one integer J. The
[eleven-block tables](undecidability/pell_crt_v95) save **60 / 75 / 47**
further variables, with full support and global-gauge reconstruction audits.
Finally, the [half-trace square](undecidability/pell_halftrace_v96/halftrace_guard.tex)
selects the required sign and excludes the zero-s branch in one equation,
saving another variable and row in all routes. The
[eleven-predicate tables](undecidability/pell_halftrace_v96) have eleven
integer certificates.
The [new Pell power certificate](undecidability/pell_power_v97/pell_power_replacement.tex)
([PDF](undecidability/pell_power_v97/pell_power_replacement.pdf)) then
replaces the long power circuit with two additional integer inputs. It
resolves the earlier geometric-quotient integrality cycle and gives
**979 / 704** variables in the general / abc routes, with thirteen integer
certificates. The specified route retains **1147**. The general sufficient
fixed coefficient may have to be increased.
The [signed-power continuation](undecidability/pell_signed_q_v98/signed_q_and_absorbed_bound.tex)
([PDF](undecidability/pell_signed_q_v98/signed_q_and_absorbed_bound.pdf))
removes both newly introduced positivity wrappers. Signed prefix estimates
recover the positive power at the end, while the existing integer Pell
margin absorbs the auxiliary index bound. Reusing an existing fourth power
in the abc chart gives **973 / 1147 / 697** variable counts.
No integer predicate is removed or added in this last step.
The [exact product elimination](undecidability/pell_product_v99/pell_product_elimination.tex)
then replaces `p=2*U*sr2` by `p=2*a*sr-2*sr^2`, using the retained
`a=(U+1)*sr`. Removing the duplicate square register saves one coordinate
and row in every route, giving **972 / 1146 / 696** counts.
The [fixed aggregate-spacing theorem](undecidability/aggregate_spacing_v100/aggregate_spacing.tex)
then replaces the free contact spacing by one sixteenth of a retained
aggregate fixed before prime selection. Its affine coordinate formula
saves one more variable in each general route, giving
**971 / 1145 / 696** counts without an additional supplier premise.
The [signed first-Pell theorem](undecidability/pell_signed_branch_v101/signed_branch_projection.tex)
then removes the sign square from both short-power systems. An alternating
binomial truncation handles negative witnesses, and positive witnesses
are rebuilt for the same coding prefix. These counts are
**970 / 1145 / 695**; this is projection equivalence, not a lift of every
signed auxiliary solution to the former sign-selected system.
The [contact-endpoint identities](undecidability/contact_endpoint_v102/contact_endpoint_reuse.tex)
then replace two common power coefficients with the already stored
second-contact square and fourth power. This exact guarded rechart gives
the intermediate **968 / 1143 / 695** quartic counts.
The [shared-denominator identity](undecidability/quadratic_reduction_v103/contact_denominator_compression.tex)
([PDF](undecidability/quadratic_reduction_v103/contact_denominator_compression.pdf))
then replaces private contact combinations by nine common polynomial coefficients.
It gives **963 / 1140 / 695**, with **818 / 991 / 590** quadratic residuals,
by a bijective rational reconstruction of the complete previous zero sets.
A [new source checkpoint](undecidability/source_frontier_v103/README.md) proves
that an integral first Pell trace would already force c to be integral;
it keeps the c predicate and records a different classical exponential source.

The [paired spectral encoder](undecidability/papers/paired_spectral_encoder.tex)
([PDF](undecidability/papers/paired_spectral_encoder.pdf)) lowers the
unrestricted-degree ceilings by removing diagonal spectral zeros, pairing
opposite differences, and separating the eigenvalue and coefficient bounds.
The **83 / 101 / 53** tradeoffs now have degree ceilings
`2^302 / 2^349 / 2^212`. The earlier **99 / 117 / 69** tradeoffs improve to
`2^384 / 2^430 / 2^278`. Variable counts and source arithmetic premises are
unchanged. The [full coefficient recipe and degree certificates](undecidability/alternative_v93)
cover nilpotents, repeated roots, and denominators at excluded characters.

All displayed bounds retain the chosen integer predicate's stated arithmetic
premises. “No additional abc” does not assert their independent proof.
The general and abc sufficient parameters remain ineffective; stored small
members are algebraic fixtures. The specified route uses its stated sufficient
parameter. No global minimum is claimed. The alleged historical universal
**57-positive-integer-variable / 47-quadratic** system has not been
independently reproved, and a quartic bound near **263** is not established.
The [registry](undecidability/results.json) and
[project research document](docs/research_directions.md#undecidability-in-bounded-numbers-of-rational-unknowns)
record all qualifications and historical tradeoffs.

## Direct Bhargava–Burungale pole without Route K (24 November 2026)

An [audited eight-multiplier pole replacement](docs/bb_direct_route_k_replacement_20261124.md) combines Bhargava–Burungale v2, Lemma 2.2 with the project's previously proved degree-seven equation. It yields a **single integer polynomial of degree 56 in four total variables** (one input, three witnesses) with square-denominator soundness outside \(\{2,3,5\}\), and completeness for the original Route K prepared inputs. The coefficient identity, sample witness and residue selection have an [independent exact checker](scripts/verify_bb_direct_route_k_20261124.py). This is a **standalone pole predicate**, not a four-variable definition of the integers or a new global quartic count. Replacing the historical Route K consumers in Lean and the global compiler remains a separate migration.

## Coefficients and explicit files

The general quartic family has exact coefficient height

```math
H(F_N)=\max\{126616122944180358034867798936,\;149^{4N+2}\},\qquad N\ge1.
```

A sufficient defining `N` exists under the retained premises of the **new Bhargava–Burungale-native family**, but its value remains ineffective. **Historical v87 fixed 163-variable Busy Beaver choice (for the unmodified v82 system).** The sharpened quantitative-record bound is now `t1 = 2^20*(16*kappa+2^186+1)*(2^186+3)`, where `kappa = 27160+16032*product(3*j+1 for j=2,...,90)`. This is an ordinary explicit **249-digit integer with t1 < 2^826**. The one fixed quartic at `N=BB(t1)` has exact coefficient height `149^(4*BB(t1)+2) < BB(2^1010)`, retaining the v22/v86 arithmetic, weighted-geometry and compiler dependencies. The [v87 TeX proof](papers/quartic/bb163_compact_record_20261120_v87.tex), [detailed report](docs/results_20261120_v87.md) and [exact integer checker](scripts/verify_v87.py) document the improvement without modifying any historical coefficient table.

**Earlier v86 fixed 163-variable Busy Beaver coefficient choice.** The uploaded [Version 22 proof](docs/results_20261120_v86.md) bounds the defining parameter using quantitative von Buhren records and an explicit selector machine. Our sharpened proof takes `t0 = 2^20*(2^620+2^186+1)*(2^186+3)`, `N = BB(t0)` and `C = 149^N`, with `t0 < 2^827` and exact coefficient height `149^(4*BB(t0)+2) < BB(2^1012)`. This is an actual fixed BB-relative coefficient specification, **not** a numerical decimal expansion or a proof independent of the retained arithmetic/geometry/compiler lemmas. See [complete v86 TeX](papers/quartic/bb163_fixed_20261120_v86.tex) and [review](docs/results_20261120_v86.md).

The historical [v84 Busy Beaver coefficient specialization](docs/busy_beaver_and_expanded_sizes_20261120_v84.md) gives an exact symbolic specification of all 2,789 expanded monomials in the **old v82 system**: only the coefficients of `x78^2*x90`, `x78*x90` and `x78^2` vary, respectively as `-6615898*149^(2*BB(t))`, `-298*149^(2*BB(t))`, and `22201*149^(4*BB(t))`. For every **sufficiently large fixed Busy Beaver index** `t`, the polynomial defines the integers under the inherited premises. The original *qualitative* theorem did not certify a numerical index; its earlier limitation is now superseded by the quantitative v22 proof and the explicit v87 choice above. The [older effectivity checkpoint](docs/explicit_BB_threshold_20261120_v85.md) remains a correct conditional estimate, but the v86/v87 record arguments avoid needing to compute its ineffective height constant. A [Busy Beaver–oracle index procedure](docs/busy_beaver_and_expanded_sizes_20261120_v84.md#one-exact-busy-beaveroracle-index-not-an-evaluated-numeral) specifies one working index rigorously, but does not evaluate it to a decimal numeral. The [symbolic expanded TXT](computation/expanded_text_v84/quartic163-BB_t-symbolic.txt) is **60.931 kB**, but its three coefficients are not in decimal. The exact size of the true decimal-expanded file is given in the linked supplement.

The **current BB-native 163-variable system** has [2,771 expanded monomials](computation/bb_native_quartic_20261124/quartic163/polynomial.json), [137 quadrics](computation/bb_native_quartic_20261124/quartic163/quadrics.json) and a [full decimal N=1 algebraic fixture](computation/bb_native_quartic_20261124/expanded/quartic163-N1.txt). Its three parameter-dependent monomials are unchanged. The [historical v82 table](computation/variable_reductions_v82/general/quartic163/polynomial.json) is retained separately.

For the fully specified 179-variable quartic, put `C0=A0*B_*^4`, where `A0=645904574641049503754777843805872291231896003979` and `B_*=14904184670611231`. Its exact coefficient height is `C0²`, of **748 bits**. The **current BB-native system** supplies its [3,012-term expanded coefficient table](computation/bb_native_quartic_20261124/quartic179/polynomial.json), [151 quadratic equations](computation/bb_native_quartic_20261124/quartic179/quadrics.json), [complete decimal TXT](computation/bb_native_quartic_20261124/expanded/quartic179.txt), and [independent Laurent reconstruction](computation/bb_native_quartic_20261124/check.py). The original [v82 coefficients](computation/variable_reductions_v82/general/quartic179/polynomial.json) and their checker remain preserved as historical artifacts. This reduces the variable count while increasing the height from the preceding 108-bit, 180-variable member; that member and the original presentation from Gabe Conant with Astra 6.2 remain in their dated packages.

The 56-variable conditional quartic has exact height `B²+377888002299` for every positive integer `B`; every sufficiently large fixed odd `B` is defining under its stated premises. The threshold is ineffective. Its [expanded coefficient table](computation/variable_reductions_v81/abc/quartic56/polynomial.json), [quadratic equations](computation/variable_reductions_v81/abc/quartic56/quadrics.json), and [independent reconstruction](computation/variable_reductions_v81/abc/check56.py) are supplied. The previous coefficient presentations and all their checks remain in their dated packages.

## Contributors and citation

This repository belongs to the ℤℚ Diophantine Project, which uses the collective agentic notes from Stefan Baranczuk, Jose Brox, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry. The main repository for the project is [Elliot Glazer's](https://github.com/elliotglazer/diophantine-z-q).

This repository includes updated results and more related work: polynomial witnesses of unrestricted degree but lower number of variables, results conditional on the abc conjecture, etc.

Cite this work as "ℤℚ Diophantine Project contributors. *ℤ is Diophantine in ℚ*. 2026. https://github.com/elliotglazer/diophantine-z-q". If you want to include any of the related results specific to this repository, please add "https://github.com/JoseBrox/diophantine-z-q_improvements" to the end of the reference.

## Source attribution

The **fixed Busy Beaver–coefficient 163-variable quartic** in v86/v87 uses **Elliot Glazer's agentic research notes and Version 22 manuscript** for the explicit Busy Beaver record argument and the inherited quantitative geometry and compiler. Version 22 credits its Busy Beaver estimate and receiving-source checks to an **OpenAI Codex agent** within Elliot Glazer's research program. The original 163-variable polynomial and exact coefficient tables are from **Jose Brox's scalar-point construction**, building on **Gabe Conant's notes with Astra 6.2**; the v86/v87 quantitative refinements are subsequent work. See the [per-source attribution record](THIRD_PARTY.md#busy-beaver-effectivity-elliot-glazers-agentic-notes-v86v87), [v86 proof](papers/quartic/bb163_fixed_20261120_v86.tex) and [v87 proof](papers/quartic/bb163_compact_record_20261120_v87.tex).


The new shared-product quartics, positive-factor encodings, weak-abc single-pole construction and related realization notes were supplied in **Gabe Conant's notes with Astra 6.2**, in `H10-quartic-constructions.zip` and `H10-eleven-variable-constructions.zip`. The [attribution record](computation/coauthor_audit_v78/ATTRIBUTION.md) identifies the original material and subsequent audit work. The supplied source bytes and checksum lists are preserved.

The earlier 198-variable archive retains its own [Gabriel Conant and ChatGPT attribution](sources/h10_quartic198/README.md). The arithmetic inputs include the separately identified Sun, Jaswal and Burungale results and the supplied simultaneous-twist strengthening. Their exact statements, versions, use and review limitations are recorded in [arithmetic inputs](docs/arithmetic_inputs.md), the individual proofs and [THIRD_PARTY.md](THIRD_PARTY.md).

Original project contributions are under **CC BY 4.0**. Third-party material retains its rights and attribution. See [CONTRIBUTING.md](CONTRIBUTING.md) and [CITATION.cff](CITATION.cff).

## Number-field results

The [Pasten–Vidaux continuation](docs/results_20261119_v81.md) gives a separate [ten-variable definition of the rational subfield inside K](papers/number_fields/ten_coordinate_rationality_20261119_v81.tex), under abc over K, an elliptic curve over Q whose positive rank stays unchanged over K, and the stated published pole theorem. The proof amplifies odd valuations, uses the cubic rational map `(T³−2)/(T³−3)`, and encodes six algebraic roots with one guarded determinant coordinate. Zywina's theorem supplies the stable-rank curve for quadratic K. Composing with the eleven-variable rational construction gives **110 variables for the integers inside K**, and **220 for the ring of integers when K is quadratic**, retaining that construction's arithmetic premises. These are existence bounds over K, with an ineffective correction. The [joint rationality continuation](papers/number_fields/joint_rationality_20261124/README.md) replaces separate rationality tests by 7k+3 coordinates for k tests, improving 110/220 to **80/157** under the stated retained premises. The [monic-absorption continuation](papers/number_fields/absorbed_joint_rationality_20261124/README.md) then gives **79 coordinates for Z inside K** and, by composing with v110's joint integer predicate, **21d+58 coordinates for the ring of integers of a degree-d field K (100 for quadratic K)**. The latter retains ordinary rational abc, the v110 arithmetic premises, and the stable-rank and height hypotheses over K. These do not change the rational-variable table above.

## Open reductions and proved obstructions

The unrestricted-degree counts **25 and 11**, and the ordinary-abc quartic count **56**, remain unchanged. The [exact-square checkpoint](computation/actual_square_v83/README.md) isolates the remaining actual-trace requirement and proves further prepared-fibre obstructions. The general quartic improvements retain the shared square coordinate for `R²`. The [v88 obstruction](negative_results/R_square_reweighting_v88/R_square_obstruction_20261123_v88.tex) excludes deleting it by diagonal Laurent reweighting in both existing units; different charts and nonlinear row combinations remain open. A proved [parity obstruction](papers/quartic/hyperbolic_parity_20261119_v79.tex) rules out one proposed full-pair compression in the retained integral Laurent chart; it does not establish a lower bound for arbitrary quartics.

The new [elliptic divisibility detector](papers/elliptic_divisibility/prepared_eds_divisibility_20261120_v82.tex) uses five coordinates for a prepared subrelation in which every nonzero integral quotient occurs, under ordinary abc and the published pole realization. It does not identify that quotient with an external rational input. A [one-parameter genus-one criterion](papers/pole_parameters/genus_one_sound_criterion_20261120_v82.tex) would give ten coordinates if its actual detector fibers have rational points. Every prepared scalar fiber is locally soluble, but an exact prepared counterexample rules out inferring rational points from those local conditions alone. Neither result is a new definition of the integers.

The complete general and conditional **21/9-variable targets remain unproved**. The main unresolved step is global rational realization at the actual elliptic detector values, with every physical lift and denominator condition satisfied. Local solubility, a rational point on an auxiliary cover, and successful finite searches do not establish that step.

The [research directions](docs/research_directions.md), [actual-trace criteria](data/criteria_20261117_v64.json), [physical-lift checkpoint](docs/results_20261117_v76.md), and [reference-normalization theorem](docs/results_20261117_v77.md) give precise formulations. [Proved obstructions](negative_results/README.md) exclude specified constructions and specializations; they do not establish a global lower bound on the number of variables.

For number fields, the [definability reductions](papers/number_fields/number_field_definability_20261109_v12.tex) relate the ring of integers, the rational integers and the rational subfield. No counterexample to Diophantine definability for a number field, or theorem covering every number field, is established here.

## Historical results

The [historical results JSON](data/results_20261117_v75.json) and dated proof guides preserve superseded constructions and their full checks. Historical numerical bounds apply to their named sources, rather than the current table.

- [v65](docs/results_20261117_v65.md), [v66](docs/results_20261117_v66.md) and [v67](docs/results_20261117_v67.md): earlier quartic constructions and point-coordinate audits.
- [v68](docs/results_20261117_v68.md) and its [canonical polynomial package](computation/quartic/explicit229_compact_v68): the preceding fully expanded explicit quartic.
- [v69](docs/results_20261117_v69.md) and [v70](docs/results_20261117_v70.md): source audits, trace arithmetic and geometric obstructions.
- [v71](docs/results_20261117_v71.md), [v72](docs/results_20261117_v72.md), [v73](docs/results_20261117_v73.md), [v74](docs/results_20261117_v74.md) and [v75](docs/results_20261117_v75.md): enlarged point charts, reconstructed quartics and even-valuation improvements.

## Reproduction

Use **Python 3.12**, **SymPy 1.14.0**, and **PassageMath PARI 10.8.14**. The new genus-one certificate uses exact algebraic rank bounds from PARI/GP. From the repository root:

```sh
python -m pip install sympy==1.14.0 passagemath-pari==10.8.14
python -B scripts/verify_v92.py
python -B scripts/verify_v91.py
python -B scripts/verify_v90.py
python -B scripts/verify_v89.py
python -B scripts/verify_v88.py --report /tmp/v88-verification.json
python -B scripts/verify_v84.py --report /tmp/v84-verification.json
python -B scripts/verify_v83.py --report /tmp/v83-verification.json
python -B scripts/verify_v82.py --report /tmp/v82-verification.json
python -B scripts/verify_v81.py --report /tmp/v81-verification.json
python -B scripts/verify_v80.py --report /tmp/v80-verification.json
python -B scripts/verify_v79.py --report /tmp/v79-verification.json
python -B scripts/verify_v78.py --report /tmp/v78-verification.json
python -B scripts/verify.py --full --receipt /tmp/legacy-verification.json
```

The full current sequence, including every intervening regression gate, is specified in [the CI workflow](.github/workflows/verify.yml). The [reproducibility guide](docs/reproducibility.md) describes source restoration, coefficient formats and optional arithmetic checks.

The verifiers reconstruct exact identities, guards, coefficient tables and finite certificates in temporary directories. Their receipts identify what was checked. Computational reconstruction does not prove the external arithmetic premises or constitute independent non-author mathematical review. The v82 gate includes the exact PARI descent for its new counterexample; the older optional PARI checks remain opt-in.

The complete TeX manuscripts are the mathematical deliverables. Affected papers are compiled and visually inspected before publication; `scripts/update_manifest.py` records the distributed file hashes.
