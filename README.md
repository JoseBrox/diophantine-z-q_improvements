# Polynomial presentations of the integers over the rationals

Complete proofs and exact computational specifications for integer polynomials

```math
F(X,Y_1,\ldots,Y_m)
```

whose rational input projection is the integers, under the arithmetic premises stated in each construction.

**Every variable count includes the input.** Degree means total degree. Coefficient height is the maximum absolute integer coefficient after the fixed parameters have been substituted. We optimize variable count, then degree, then coefficient height. No global minimum is claimed.

## Current constructions — 23 November 2026

The reductions **193→165, 229→180, 68→62 and 13→11** come from **notes of Gabe Conant with Astra 6.2**. They have been audited and integrated here, with further degree, coefficient and hypothesis improvements. The [source audit](docs/results_20261119_v78.md) distinguishes those contributions from the subsequent work. The [v81 continuation](docs/results_20261119_v81.md) further reduces the ordinary-abc quartic through **62→59→58→56 variables**, using a nonlinear contact rechart and the published pole theorem directly. The [v82 continuation](docs/results_20261120_v82.md) reduces the general quartics to **163 and 179 variables**, with complete ordered witness constructions.

The [Bhargava–Burungale v2 audit](docs/results_20261123_v88.md) now lowers the degrees in **all five current few-variable routes**, using a normalized product pole, a class-seven scalar and balanced squareclass representatives. It also proves an overlapping-support simultaneous-twist theorem, two-test quadratic arithmetic in the BB index model, and a three-square interval wrapper. The last improvement saves one rational variable relative to the paper's still-unspecified parameter `r`; it is not a new numerical defining-variable record. All new proofs, complete specifications, independent checks and [all-route qualifications](docs/bb_all_route_status_20261123_v88.md) are supplied.

“None” in the height-hypothesis column means **no additional conjecture beyond the arithmetic premises explicitly retained in the proof**. A complete independent audit of all inherited elliptic, prime-pattern, pole-realization and height foundations has not been established.

| Construction | Additional height hypothesis | Total variables | Degree | Coefficients and effectiveness | Expanded TXT size (kB) |
|:--|:--|--:|:--|--:|--:|
| [General few-variable family](papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) | None | **25** | **≤ 48,318,382,080** | Balanced BB product pole and projective encoder; sufficient odd exponent ineffective. | Not expanded; <2^825 (L=143 fixture bound) |
| [General quartic family](papers/quartic/scalar_point163_179_20261120_v82.tex) | None | **163** | **4, exact** | 137 quadratic squares; 2,789 monomials; [fixed Busy Beaver member](docs/results_20261120_v87.md), t=t1<2^826, source dependencies retained. | [60.907](computation/expanded_text_v84/quartic163-N1.txt) (N=1 fixture; [BB formula](docs/busy_beaver_and_expanded_sizes_20261120_v84.md)) |
| [Fully specified general polynomial](papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) | None | **27** | **≤ 183,368,679,424** | Explicit `L=143`; coefficient height < `2^(2^45)`. | Not expanded; <2^941 (L=143 upper bound) |
| [Fully specified quartic](papers/quartic/scalar_point163_179_20261120_v82.tex) | None | **179** | **4, exact** | 151 quadratic squares; 3,036 monomials; 748-bit exact height. | [66.905](computation/expanded_text_v84/quartic179.txt) |
| [Few-variable family under abc](papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) | Ordinary rational abc | **11** | **≤ 3,261,569** | Twelve contacts and normalized BB product pole; sufficient fixed odd shift ineffective. | Not expanded; <2^215 (B=3 fixture bound) |
| [Quartic family under abc](papers/quartic_existence/paired_contact56_20261119_v81.tex) | Ordinary rational abc | **56** | **4, exact** | 46 quadratic squares; 809 monomials; sufficient fixed odd shift ineffective. | [11.564](computation/expanded_text_v84/quartic56-B3.txt) (B=3 fixture) |

The two eleven-variable routes under weak rational abc at exponents `121/100` and `16/15` have degree bounds **16,460,929** and **9,808,001**, respectively. Their sufficient odd shifts remain ineffective. See the [v88 theorem](papers/few_variables25/bb_product_degree_transfer_20261123_v88.pdf) for all five degree improvements and retained assumptions.

The last column gives **decimal kB (1 kB = 1,000 bytes)** for single-line ASCII, fully expanded TXT files with `x1` as the input, `x2`, ... as other variables, and no final newline. Numeric quartic sizes are **measured exactly**. The 163-variable `N=1` and 56-variable `B=3` members are algebraic **fixtures, not certified defining members**. The other entries are extremely loose **upper bounds for the indicated stored circuit member**, not measurements or predictions of the first defining member. See [fully expanded TXT files and exact size formulas](docs/busy_beaver_and_expanded_sizes_20261120_v84.md).

The unrestricted-degree bounds describe complete finite determinant specifications; those enormous polynomials have not been fully expanded. All displayed quartics are exactly expanded. Every construction has integer content one, with primitive normalization where needed. Small coefficient fixtures and coefficient-height cutoffs are not sufficient defining parameters.

The [v88 results JSON](data/results_20261123_v88.json) records all five new finite-algebra specifications and parameter qualifications; the [v82 records](data/results_20261120_v82.json) preserve the unchanged quartic specifications. The new fixture TXT upper bounds use the same exact character-count argument as v84, replayed in the v88 gate. Weaker fixed-exponent versions of abc and alternative coefficient presentations are retained in the [detailed proof guide](docs/results_20261119_v78.md#weaker-hypotheses-and-generalizations).

## Coefficients and explicit files

The general quartic family has exact coefficient height

```math
H(F_N)=\max\{126616122944180358034867798936,\;149^{4N+2}\},\qquad N\ge1.
```

A sufficient defining `N` exists under the retained premises, but its value is ineffective. **New v87 fixed 163-variable Busy Beaver choice.** The sharpened quantitative-record bound is now `t1 = 2^20*(16*kappa+2^186+1)*(2^186+3)`, where `kappa = 27160+16032*product(3*j+1 for j=2,...,90)`. This is an ordinary explicit **249-digit integer with t1 < 2^826**. The one fixed quartic at `N=BB(t1)` has exact coefficient height `149^(4*BB(t1)+2) < BB(2^1010)`, retaining the v22/v86 arithmetic, weighted-geometry and compiler dependencies. The [v87 TeX proof](papers/quartic/bb163_compact_record_20261120_v87.tex), [detailed report](docs/results_20261120_v87.md) and [exact integer checker](scripts/verify_v87.py) document the improvement without modifying any historical coefficient table.

**Earlier v86 fixed 163-variable Busy Beaver coefficient choice.** The uploaded [Version 22 proof](docs/results_20261120_v86.md) bounds the defining parameter using quantitative von Buhren records and an explicit selector machine. Our sharpened proof takes `t0 = 2^20*(2^620+2^186+1)*(2^186+3)`, `N = BB(t0)` and `C = 149^N`, with `t0 < 2^827` and exact coefficient height `149^(4*BB(t0)+2) < BB(2^1012)`. This is an actual fixed BB-relative coefficient specification, **not** a numerical decimal expansion or a proof independent of the retained arithmetic/geometry/compiler lemmas. See [complete v86 TeX](papers/quartic/bb163_fixed_20261120_v86.tex) and [review](docs/results_20261120_v86.md).

The [Busy Beaver coefficient specialization](docs/busy_beaver_and_expanded_sizes_20261120_v84.md) gives an exact symbolic specification of all 2,789 expanded monomials: only the coefficients of `x78^2*x90`, `x78*x90` and `x78^2` vary, respectively as `-6615898*149^(2*BB(t))`, `-298*149^(2*BB(t))`, and `22201*149^(4*BB(t))`. For every **sufficiently large fixed Busy Beaver index** `t`, the polynomial defines the integers under the inherited premises. The original *qualitative* theorem did not certify a numerical index; its earlier limitation is now superseded by the quantitative v22 proof and the explicit v87 choice above. The [older effectivity checkpoint](docs/explicit_BB_threshold_20261120_v85.md) remains a correct conditional estimate, but the v86/v87 record arguments avoid needing to compute its ineffective height constant. A [Busy Beaver–oracle index procedure](docs/busy_beaver_and_expanded_sizes_20261120_v84.md#one-exact-busy-beaveroracle-index-not-an-evaluated-numeral) specifies one working index rigorously, but does not evaluate it to a decimal numeral. The [symbolic expanded TXT](computation/expanded_text_v84/quartic163-BB_t-symbolic.txt) is **60.931 kB**, but its three coefficients are not in decimal. The exact size of the true decimal-expanded file is given in the linked supplement.

The [complete 163-variable coefficient table](computation/variable_reductions_v82/general/quartic163/polynomial.json) and [quadratic equations](computation/variable_reductions_v82/general/quartic163/quadrics.json) are supplied.

For the fully specified 179-variable quartic, put `C0=A0*B_*^4`, where `A0=645904574641049503754777843805872291231896003979` and `B_*=14904184670611231`. Its exact coefficient height is `C0²`, of **748 bits**. The [expanded coefficient table](computation/variable_reductions_v82/general/quartic179/polynomial.json), [quadratic equations](computation/variable_reductions_v82/general/quartic179/quadrics.json), and [independent reconstruction](computation/variable_reductions_v82/general/check.py) are supplied. This reduces the variable count while increasing the height from the preceding 108-bit, 180-variable member; that member and the original presentation from Gabe Conant with Astra 6.2 remain in their dated packages.

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

The [Pasten–Vidaux continuation](docs/results_20261119_v81.md) gives a separate [ten-variable definition of the rational subfield inside K](papers/number_fields/ten_coordinate_rationality_20261119_v81.tex), under abc over K, an elliptic curve over Q whose positive rank stays unchanged over K, and the stated published pole theorem. The proof amplifies odd valuations, uses the cubic rational map `(T³−2)/(T³−3)`, and encodes six algebraic roots with one guarded determinant coordinate. Zywina's theorem supplies the stable-rank curve for quadratic K. Composing with the eleven-variable rational construction gives **110 variables for the integers inside K**, and **220 for the ring of integers when K is quadratic**, retaining that construction's arithmetic premises. These are existence bounds over K, with an ineffective correction; they do not change the rational-variable table above.

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
