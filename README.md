# Polynomial presentations of the integers over the rationals

Complete proofs and exact computational specifications for integer polynomials

$$F(X,Y_1,\ldots,Y_m)$$

whose rational input projection is the integers, under the arithmetic premises stated in each construction.

**Every variable count includes the input.** Degree means total degree. Coefficient height is the maximum absolute integer coefficient after fixed parameters have been substituted. The priorities are variable count, degree, then coefficient height. No global minimum is claimed.

## Current constructions — 15 November 2026

“None” below means **no additional conjecture beyond the explicitly retained arithmetic premises**. The full independent audit of the prime-pattern, pole-realization and modular-height foundations is not declared complete.

| Construction | Additional height hypothesis | Total variables | Degree | Coefficients and effectiveness |
|:--|:--|--:|:--|:--|
| [Fewest variables under inherited premises](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | None | **25** | **≤ 5,059,009,872,658,432 < 2^53** | Every sufficiently large fixed odd exponent; sufficient threshold ineffective. |
| [Fewest quartic variables under inherited premises](papers/quartic/primitive_quadratic_bases_20261115_v40.tex) | None | **196** | **4, exact** | 176 quadratic squares; **2,994 monomials**. Exact height below; defining threshold ineffective. |
| [Fully specified general polynomial](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | None | **27** | **≤ 99,279,020,543,180,800 < 2^57** | **L=20483**; coefficient height **< 2^(2^70)**. |
| [Fully specified quartic](papers/quartic/laurent_elimination_20261115_v38.tex) | None | **258** | **4, exact** | **N=9682**; 230 quadratic squares; **3,705 monomials**; height **9792² · 149^19364**. |
| [Few variables under weak abc](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | Weak abc at **121/100**; ordinary Szpiro suffices | **13** | **≤ 43,211,777 < 2^26** | Sufficient odd shift ineffective. |
| [Lower degree under stronger weak abc](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | Weak abc at **16/15**; ordinary rational abc suffices | **13** | **≤ 39,858,177 < 2^26** | Sufficient odd shift ineffective. |
| [Fewest quartic variables under abc](papers/quartic/primitive_quadratic_bases_20261115_v40.tex) | Ordinary rational abc | **78** | **4, exact** | 68 quadratic squares; **1,254 monomials**. Exact height below; sufficient shift ineffective. |

All these polynomials have integer content one. The general degree figures are upper bounds for finite, unexpanded determinant specifications. Their support bounds are below **2^1193**, **2^1401**, **2^284**, and **2^283**, in the order 25, 27, weak-abc 13, stronger-abc 13.

The exact height of the 196-variable quartic is

$$H(P_N)=\max\left\{126616122944180358034867798936,\;32561227748626372080\,149^{2N}\right\}.$$

This holds for every **N≥1**. The first term dominates for N=1,2 and the second for N≥3. A sufficient defining N exists under the stated source premises, but no sufficient numerical N is supplied for this family.

The exact height of the 78-variable abc quartic is

$$H(Q_B)=\max\left\{20828275368498373068800,\;B^2+275933278576697172\right\}.$$

Its fixed odd shift **B≥81** must be sufficiently large. B=81 is an algebraic fixture, not a certified defining member. This construction compares the elliptic index with X²+3, uses B+X⁸+T² as its height scale, and has strict absorption coefficient **602/679**. Its ordinary-abc hypothesis is distinct from the weak-abc hypotheses in the 13-variable rows.

The quartic transformations preserve the entire rational solution sets, with explicit invertible maps where coordinates are rescaled. Their sufficient defining parameters are unchanged. The finite-algebra construction permits additional tuples with a zero final pole ordinate; its proof establishes soundness on that larger locus and retains the existing completeness witnesses.

Current specifications: [results JSON](data/results_20261115_v40.json), [proof and verification guide](docs/results_20261115_v40.md), and [research directions](docs/research_directions.md).

## Finite algebras and the general polynomials

The [terminal quadratic extension theorem](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) permits the last quadratic radicand to vanish. Its separator distinguishes all distinct geometric characters even on a nonreduced fiber. Galois descent recovers a rational character from a rational determinant root without assuming a simple eigenvalue. An elementary valuation proof permits the zero final ordinate in the pole equations. Two large guard norms can therefore be omitted.

The [four complete specifications](computation/few_variables/terminal_root_v40) retain the integral point algebra, polynomial root envelopes and subalgebra norms. Every denominator and every preceding radicand remains guarded. The independent checker reconstructs these conditions from the native source circuits and recomputes all bounds. The [single-norm construction](papers/finite_algebra/unit_norm_20261114_v28.tex) and [subalgebra-norm theorem](papers/finite_algebra/subalgebra_norms_20261114_v30.tex) supply the underlying source and its full-unit completeness proof.

## Quartic equations and coefficient height

The [primitive quadratic basis theorem](papers/quartic/primitive_quadratic_bases_20261115_v40.tex) gives exact rational changes of the reference-equation basis, followed where specified by an invertible rational coordinate rescaling. The defining rows remain primitive integer quadrics. Stored matrices and inverses prove equivalence independently of the lattice algorithm used to find them. Independent expansions certify the exact heights and support for every allowed fixed parameter.

Complete coefficient tables are supplied for the [196-variable family](computation/quartic/primitive_basis196_v40) and the [78-variable abc family](computation/quartic/abc78_balanced_v40). The [196/258 coordinate-elimination theorem](papers/quartic/laurent_elimination_20261115_v38.tex) proves the underlying reductions after invertible monomial rescaling, with unit conditions established before division. The [78-variable arithmetic theorem](papers/quartic_existence/quartic_abc78_20261115_v34.tex) supplies the mixed-power height argument and completeness.

The [paired-ratio theorem](papers/elliptic_charts/paired_ratio_redundancy_20261115_v40.tex) shows that the complete ratio equations imply both reciprocal curve equations. It covers identities, torsion points and tangent pairs, and gives a quadratic-compatible uniform scaling of the seven pair coordinates. Deleting the redundant curve rows gives the [196-variable application](papers/quartic/quartic196_redundancy_20261115_v40.tex). For applications prioritizing support rather than coefficient height, tables with **2,853** and **1,113** monomials are retained in [paired_redundancy196_v40](computation/quartic/paired_redundancy196_v40) and [abc78_reduced_v40](computation/quartic/abc78_reduced_v40).

## Reference charts and integer labels

The [three-coordinate reference chart](papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex) describes a point and its translate using two quadrics in three field coordinates. Its exact domain is the complement of four specified elliptic points. Three linear functions are units with explicit linear inverses, and every tangent and two-torsion configuration in the domain is included. The reciprocal abscissas are quadratic in these coordinates; their squares are generally quartic. This chart alone therefore does not lower the total variable count of a defining quartic. [Exact certificates](computation/elliptic_charts/three_coordinate_v40) accompany the all-field proof.

The [integral Pell-label theorem](papers/integer_labels/pell_labels_20261115_v40.tex) obtains exponential growth from two exact integral labels and one finite quadratic choice. It proves sharp bounds and arbitrarily large witnesses with prescribed finite congruence data. A rational local-approximation counterexample explains why this result does not apply directly to approximate elliptic ratios. Its [checker and certificate](computation/integer_labels/pell_compression_v40) verify the identities and exceptional cases. No reduction below 25 variables follows from this theorem alone.

## Height estimates and compatible poles

The [all-point trace theorem](papers/trace_heights/trace_on_all_points_20261113_v25.tex) and [positive weighted trace theorem](papers/trace_heights/weighted_trace_20261114_v27.tex) include the half-integral index and torsion cases required by the sources. The latter also verifies that the selected Gaussian primes annihilate the half-generator using the existing congruences.

The [joint-pole theorem](papers/pole_parameters/joint_pole_realization_20261114_v29.tex) and [common-twist theorem](papers/pole_parameters/common_twists_20261114_v30.tex) reduce pole parameters on specified square-class compatibility loci. The current completeness witnesses are not proved to lie on those loci. These results do not establish a 24-variable construction or a smaller abc variable count. The [ordered square-class surface](papers/pole_parameters/ordered_squareclass_surface_20261115_v33.tex) and [reflection obstruction](papers/pole_parameters/reflection_obstruction_20261115_v33.tex) give further limitations without asserting a global lower bound.

## Rings of integers of number fields

The [definability reductions](papers/number_fields/number_field_definability_20261109_v12.tex) relate the questions for the ring of integers, the rational integers and the rational subfield. The [finite-correspondence theorem](papers/number_fields/finite_correspondences_and_denominators_20261109_v14.tex) excludes several proposed constructions from abelian varieties and finite covers. The [complex-multiplication obstruction](papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.tex) explains why the cyclic-group and trace arguments do not extend unchanged after adjoining i.

**No counterexample for a number field, and no theorem covering every number field, is established here.** Failure of a particular polynomial after scalar extension is not a counterexample to Diophantine definability. The [research guide](docs/research_directions.md#rings-of-integers-of-number-fields) states the remaining denominator and realization problems.

## Reproduction

Use **Python 3.12** for the byte-pinned legacy suite and **SymPy 1.14.0** for symbolic checks. From the repository root:

    python -m pip install sympy==1.14.0
    python -B scripts/verify_v40.py
    python -B scripts/verify_v38.py
    python -B scripts/verify_v34.py
    python -B scripts/verify_v33.py
    python -B scripts/verify_v30.py
    python -B computation/pole_parameters/joint_realization_v29/check.py
    python -B scripts/verify_v28.py
    python -B scripts/verify_release_v27.py
    python -B scripts/verify.py --full

The current verifier reconstructs the specifications in temporary files and checks the independent certificates. It covers terminal nonreduced examples, reference-chart identities and exceptional cases, Pell-label examples, paired-ratio implications, invertible row transformations and complete quartic expansions. The retained verifiers authenticate the sources and supplied 198-variable archive. The full legacy verifier has **126 stages**. Optional PARI rank checks remain separately requested by --with-pari; they are not implied by --full.

The complete TeX manuscripts are the mathematical deliverables. They are compiled and visually inspected before publication. scripts/update_manifest.py records the distributed file hashes. Computational reconstruction certifies the finite identities and coefficients it checks; it does not certify external arithmetic premises or constitute independent non-author mathematical review.

## Attribution and review scope

The 198-variable parent of the current 196-variable construction was supplied in Gabriel Conant's research archive with ChatGPT. Its [original attribution and source](sources/h10_quartic198/README.md) are retained. The [pinned upstream 214-variable source](computation/quartic/balanced214_v24/source) and its hashes remain a separate dependency. The current work is maintained in this repository and does not modify the upstream repository.

The congruent-twist pole realization uses **Jaswal, Hexagon 2611.00331v2, Theorem 1.2**, with the preparation hypotheses stated in the [pole paper](papers/pole_parameters/congruent_twist_poles_20261114_v27.tex). The supplied finite-family strengthening is used only in the separate compatible-pole results. Bibliographies, [arithmetic dependencies](docs/arithmetic_inputs.md), and [THIRD_PARTY.md](THIRD_PARTY.md) retain the source distinctions.

The [reference-chart correction](docs/audits/reference_chart_correction_20261114_v27.md), [physical-normalization correction](docs/audits/scalar_ratio_correction_20261115_v33.md), and [unsupported 233-variable claim audit](docs/audits/recovery_233_20261115_v38.md) remain explicit. No 233-variable result is claimed. Earlier source files and receipts remain available for exact reproduction; their superseded numerical summaries do not replace the current table.

Original project contributions are under **CC BY 4.0**. Third-party material retains its own rights and attribution. See [CONTRIBUTING.md](CONTRIBUTING.md), [THIRD_PARTY.md](THIRD_PARTY.md), and [CITATION.cff](CITATION.cff).
