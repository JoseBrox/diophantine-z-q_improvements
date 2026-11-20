# Polynomial presentations of the integers over the rationals

Complete proofs and exact computational specifications for integer polynomials

```math
F(X,Y_1,\ldots,Y_m)
```

whose rational input projection is the integers, under the arithmetic premises stated in each construction.

**Every variable count includes the input.** Degree means total degree. Coefficient height is the maximum absolute integer coefficient after the fixed parameters have been substituted. We optimize variable count, then degree, then coefficient height. No global minimum is claimed.

## Current constructions — 20 November 2026

The reductions **193→165, 229→180, 68→62 and 13→11** come from **notes of Gabe Conant with Astra 6.2**. They have been audited and integrated here, with further degree, coefficient and hypothesis improvements. The [source audit](docs/results_20261119_v78.md) distinguishes those contributions from the subsequent work. The [v81 continuation](docs/results_20261119_v81.md) further reduces the ordinary-abc quartic through **62→59→58→56 variables**, using a nonlinear contact rechart and the published pole theorem directly. The [v82 continuation](docs/results_20261120_v82.md) reduces the general quartics to **163 and 179 variables**, with complete ordered witness constructions.

“None” in the height-hypothesis column means **no additional conjecture beyond the arithmetic premises explicitly retained in the proof**. A complete independent audit of all inherited elliptic, prime-pattern, pole-realization and height foundations has not been established.

| Construction | Additional height hypothesis | Total variables | Degree | Coefficients and effectiveness |
|:--|:--|--:|:--|:--|
| [General few-variable family](papers/few_variables25/four_contact_scalar_20261119_v78.tex) | None | **25** | **≤ 87,778,394,112** | Four-contact scalar and projective two-root encoder; sufficient odd exponent ineffective. |
| [General quartic family](papers/quartic/scalar_point163_179_20261120_v82.tex) | None | **163** | **4, exact** | 137 quadratic squares; 2,789 monomials; defining threshold ineffective. |
| [Fully specified general polynomial](papers/few_variables25/four_contact_scalar_20261119_v78.tex) | None | **27** | **≤ 335,647,080,448** | Explicit `L=143`; coefficient height < `2^(2^46)`. |
| [Fully specified quartic](papers/quartic/scalar_point163_179_20261120_v82.tex) | None | **179** | **4, exact** | 151 quadratic squares; 3,036 monomials; 748-bit exact height. |
| [Few-variable family under abc](papers/conditional_few_variables/twelve_contact_first_scale_20261119_v78.tex) | Ordinary rational abc | **11** | **≤ 6,361,985** | Twelve contacts at the first height scale; sufficient fixed odd shift ineffective. |
| [Quartic family under abc](papers/quartic_existence/paired_contact56_20261119_v81.tex) | Ordinary rational abc | **56** | **4, exact** | 46 quadratic squares; 809 monomials; sufficient fixed odd shift ineffective. |

The unrestricted-degree bounds describe complete finite determinant specifications; those enormous polynomials have not been fully expanded. All displayed quartics are exactly expanded. Every construction has integer content one, with primitive normalization where needed. Small coefficient fixtures and coefficient-height cutoffs are not sufficient defining parameters.

The [results JSON](data/results_20261120_v82.json) records the exact specifications, source assumptions and parameter qualifications. Weaker fixed-exponent versions of abc and alternative coefficient presentations are retained in the [detailed proof guide](docs/results_20261119_v78.md#weaker-hypotheses-and-generalizations).

## Coefficients and explicit files

The general quartic family has exact coefficient height

```math
H(F_N)=\max\{126616122944180358034867798936,\;149^{4N+2}\},\qquad N\ge1.
```

A sufficient defining `N` exists under the retained premises, but its value is ineffective. The [complete 163-variable coefficient table](computation/variable_reductions_v82/general/quartic163/polynomial.json) and [quadratic equations](computation/variable_reductions_v82/general/quartic163/quadrics.json) are supplied.

For the fully specified 179-variable quartic, put `C0=A0*B_*^4`, where `A0=645904574641049503754777843805872291231896003979` and `B_*=14904184670611231`. Its exact coefficient height is `C0²`, of **748 bits**. The [expanded coefficient table](computation/variable_reductions_v82/general/quartic179/polynomial.json), [quadratic equations](computation/variable_reductions_v82/general/quartic179/quadrics.json), and [independent reconstruction](computation/variable_reductions_v82/general/check.py) are supplied. This reduces the variable count while increasing the height from the preceding 108-bit, 180-variable member; that member and the original presentation from Gabe Conant with Astra 6.2 remain in their dated packages.

The 56-variable conditional quartic has exact height `B²+377888002299` for every positive integer `B`; every sufficiently large fixed odd `B` is defining under its stated premises. The threshold is ineffective. Its [expanded coefficient table](computation/variable_reductions_v81/abc/quartic56/polynomial.json), [quadratic equations](computation/variable_reductions_v81/abc/quartic56/quadrics.json), and [independent reconstruction](computation/variable_reductions_v81/abc/check56.py) are supplied. The previous coefficient presentations and all their checks remain in their dated packages.

## Contributors and citation

This repository belongs to the ℤℚ Diophantine Project, which uses the collective agentic notes from Stefan Baranczuk, Jose Brox, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry. The main repository for the project is [Elliot Glazer's](https://github.com/elliotglazer/diophantine-z-q).

This repository includes updated results and more related work: polynomial witnesses of unrestricted degree but lower number of variables, results conditional on the abc conjecture, etc.

Cite this work as "ℤℚ Diophantine Project contributors. ℤ is Diophantine in ℚ. 2026. https://github.com/elliotglazer/diophantine-z-q". If you want to include any of the related results specific to this repository, please add "https://github.com/JoseBrox/diophantine-z-q_improvements" to the end of the reference.

## Source attribution

The new shared-product quartics, positive-factor encodings, weak-abc single-pole construction and related realization notes were supplied in **Gabe Conant's notes with Astra 6.2**, in `H10-quartic-constructions.zip` and `H10-eleven-variable-constructions.zip`. The [attribution record](computation/coauthor_audit_v78/ATTRIBUTION.md) identifies the original material and subsequent audit work. The supplied source bytes and checksum lists are preserved.

The earlier 198-variable archive retains its own [Gabriel Conant and ChatGPT attribution](sources/h10_quartic198/README.md). The arithmetic inputs include the separately identified Sun, Jaswal and Burungale results and the supplied simultaneous-twist strengthening. Their exact statements, versions, use and review limitations are recorded in [arithmetic inputs](docs/arithmetic_inputs.md), the individual proofs and [THIRD_PARTY.md](THIRD_PARTY.md).

Original project contributions are under **CC BY 4.0**. Third-party material retains its rights and attribution. See [CONTRIBUTING.md](CONTRIBUTING.md) and [CITATION.cff](CITATION.cff).

## Number-field results

The [Pasten–Vidaux continuation](docs/results_20261119_v81.md) gives a separate [ten-variable definition of the rational subfield inside K](papers/number_fields/ten_coordinate_rationality_20261119_v81.tex), under abc over K, an elliptic curve over Q whose positive rank stays unchanged over K, and the stated published pole theorem. The proof amplifies odd valuations, uses the cubic rational map `(T³−2)/(T³−3)`, and encodes six algebraic roots with one guarded determinant coordinate. Zywina's theorem supplies the stable-rank curve for quadratic K. Composing with the eleven-variable rational construction gives **110 variables for the integers inside K**, and **220 for the ring of integers when K is quadratic**, retaining that construction's arithmetic premises. These are existence bounds over K, with an ineffective correction; they do not change the rational-variable table above.

## Open reductions and proved obstructions

The unrestricted-degree counts **25 and 11**, and the ordinary-abc quartic count **56**, remain unchanged in v82. The general quartic improvements retain the shared square coordinate for `R²`; eliminating it is still open. A proved [parity obstruction](papers/quartic/hyperbolic_parity_20261119_v79.tex) rules out one proposed full-pair compression in the retained integral Laurent chart; it does not establish a lower bound for arbitrary quartics.

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
