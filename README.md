# Polynomial presentations of the integers over the rationals

Complete proofs and exact computational specifications for integer polynomials

```math
F(X,Y_1,\ldots,Y_m)
```

whose rational input projection is the integers, under the arithmetic premises stated in each construction.

**Every variable count includes the input.** Degree means total degree. Coefficient height is the maximum absolute integer coefficient after fixed parameters have been substituted. The priorities are variable count, degree, then coefficient height. No global minimum is claimed.

## Current constructions — 16 November 2026

“None” below means **no additional conjecture beyond the explicitly retained arithmetic premises**. The full independent audit of the prime-pattern, pole-realization and modular-height foundations is not declared complete.

| Construction | Additional height hypothesis | Total variables | Degree | Coefficients and effectiveness |
|:--|:--|--:|:--|:--|
| [Fewest variables under inherited premises](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | None | **25** | $\le 5{,}059{,}009{,}872{,}658{,}432 < 2^{53}$ | Every sufficiently large fixed odd exponent; sufficient threshold ineffective. |
| [Fewest quartic variables under inherited premises](papers/quartic/quartic195_20261116_v45.tex) | None | **195** | **4, exact** | 175 quadratic squares; **2,956 monomials**. Exact height below; defining threshold ineffective. |
| [Fully specified general polynomial](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | None | **27** | $\le 99{,}279{,}020{,}543{,}180{,}800 < 2^{57}$ | $L=20483$; coefficient height $<2^{2^{70}}$. |
| [Fully specified quartic](papers/quartic/quartic257_20261116_v45.tex) | None | **257** | **4, exact** | $N=9682$; 229 quadratic squares; **3,679 monomials**; exact height $149^{19366}$. |
| [Few variables under weak abc](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | Weak abc at $121/100$; ordinary Szpiro suffices | **13** | $\le 43{,}211{,}777 < 2^{26}$ | Sufficient odd shift ineffective. |
| [Lower degree under stronger weak abc](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) | Weak abc at $16/15$; ordinary rational abc suffices | **13** | $\le 39{,}858{,}177 < 2^{26}$ | Sufficient odd shift ineffective. |
| [Fewest quartic variables under abc](papers/quartic_existence/quartic_abc71_20261116_v49.tex) | Ordinary rational abc | **71** | **4, exact** | 59 quadratic squares; **1,187 monomials**. Exact height below; sufficient shift ineffective. |

All these polynomials have integer content one. The general degree figures are upper bounds for finite, unexpanded determinant specifications. Their support bounds are below $2^{1193}$, $2^{1401}$, $2^{284}$, and $2^{283}$, in the order 25, 27, weak-abc 13, stronger-abc 13.

The exact height of the 195-variable quartic is

```math
H(P_N)=\max\left\{126616122944180358034867798936,\;149^{2N+2}\right\}.
```

This holds for every $N\ge1$. The first term dominates for $N=1,\ldots,5$ and the second for $N\ge6$. This coefficient crossover does not specify a sufficient defining parameter. A sufficient defining $N$ exists under the stated source premises, but no sufficient numerical $N$ is supplied for this family.

The exact height of the 71-variable abc quartic is

```math
H(Q_B)=B^2+1.
```

Its fixed odd shift $B\ge81$ must be sufficiently large. No numerical sufficient defining value is supplied; $B=81$ is only an algebraic test value. The reference translator is $R_0$ and the input comparison is $\beta=X$. The scaled physical trace $T_{\mathrm{sc}}=X^2\operatorname{Tr}x(U-V)$ is affine in an existing point coordinate, so the height scale $B+X^8+T_{\mathrm{sc}}^2$ requires no separate rational trace coordinate. The strict absorption coefficient remains $602/679$. Its ordinary-abc hypothesis is distinct from the weak-abc hypotheses in the 13-variable rows.

The 71-variable quartic uses the complete three-coordinate unit reference chart and a six-coordinate variable-difference point chart over $\mathbb Q(\sqrt2)$. Its quadratic product-recovery equations use a reference coordinate that is already a unit, so no additional guard is needed. Inverse comparison errors control every relevant torsion branch. The paired chart includes exact nonzero two-torsion differences and all allowed tangent pairs. Zero contact weight is impossible for nonzero input, and zero input has a separate literal completeness witness. The retained prime congruences and simultaneous-twist premise supply completeness for every integer, including odd and negative inputs.

The coefficient-basis transformations and the 195/257-coordinate eliminations preserve their corresponding full rational solution sets. The finite-algebra construction permits a zero final pole ordinate and proves soundness on that larger locus.

Current specifications: [results JSON](data/results_20261116_v51.json), [proof and verification guide](docs/results_20261116_v51.md), and [research directions](docs/research_directions.md).

The [fixed-fiber and detector-index theorems](docs/common_parameter_guard_reduction_20261116_v42.md) show that one common rational pole fiber with nonzero ordinates suffices for all remaining pole guards, and give independent auxiliary-index families with unchanged square-class scalars. The common rational fiber itself remains unproved. Proved obstructions and lower bounds are collected separately in [negative_results](negative_results/README.md).

## Contributors and citation

This repository belongs to the ℤℚ Diophantine Project, which uses the collective agentic notes from Stefan Baranczuk, Jose Brox, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry. The main repository for the project is [Elliot Glazer's](https://github.com/elliotglazer/diophantine-z-q).

This repository includes updated results and more related work: polynomial witnesses of unrestricted degree but lower number of variables, results conditional on the abc conjecture, etc.

Cite this work as "ℤℚ Diophantine Project contributors. ℤ is Diophantine in ℚ. 2026. https://github.com/elliotglazer/diophantine-z-q". If you want to include any of the related results specific to this repository, please add "https://github.com/JoseBrox/diophantine-z-q_improvements" to the end of the reference.

## Finite algebras and the general polynomials

The [terminal quadratic extension theorem](papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex) permits the last quadratic radicand to vanish. Its separator distinguishes all distinct geometric characters even on a nonreduced fiber. Galois descent recovers a rational character from a rational determinant root without assuming a simple eigenvalue. An elementary valuation proof permits the zero final ordinate in the pole equations. Two large guard norms can therefore be omitted.

The [four complete specifications](computation/few_variables/terminal_root_v40) retain the integral point algebra, polynomial root envelopes and subalgebra norms. Every denominator and every preceding radicand remains guarded. The independent checker reconstructs these conditions from the native source circuits and recomputes all bounds. The [single-norm construction](papers/finite_algebra/unit_norm_20261114_v28.tex) and [subalgebra-norm theorem](papers/finite_algebra/subalgebra_norms_20261114_v30.tex) supply the underlying source and its full-unit completeness proof.

## Quartic equations and coefficient height

The [primitive quadratic basis theorem](papers/quartic/primitive_quadratic_bases_20261115_v40.tex) gives exact rational changes of the reference-equation basis, followed where specified by an invertible rational coordinate rescaling. The defining rows remain primitive integer quadrics. Stored matrices and inverses prove equivalence independently of the lattice algorithm used to find them. Independent expansions certify the exact heights and support for every allowed fixed parameter.

Complete coefficient tables are supplied for the [195-variable family](computation/quartic/affine_laurent195_v45), [257-variable explicit family](computation/quartic/affine_laurent257_v45), and [71-variable abc family](computation/quartic/abc71_v49). The [195-variable theorem](papers/quartic/quartic195_20261116_v45.tex) centers the Lucas residual and its square, then eliminates an inverse-weight square by a Laurent coordinate change. The literal unit guard is retained, so the complete rational zero sets are in input-preserving bijection. A fixed-parameter rescaling gives the stated exact coefficient height. The [257-variable theorem](papers/quartic/quartic257_20261116_v45.tex) uses the corresponding affine centering with the existing inverse coordinate, and preserves the effective sufficient parameter $N=9682$. All transformations and both full polynomial expansions have independent exact certificates.

The [71-variable arithmetic theorem](papers/quartic_existence/quartic_abc71_20261116_v49.tex) propagates the unit reference chart through every detector equation. It recovers the two weighted reciprocal products quadratically, replaces separate ratios by affine inverse comparison errors, and uses the scaled physical difference trace already present in the point chart. All recovery coordinates, comparison squares and nonzero constraints are included in its 71-coordinate count. The proof covers soundness, nonzero integer completeness and zero input; independent exact expansion certifies the degree, support and coefficient height.

The [paired-ratio theorem](papers/elliptic_charts/paired_ratio_redundancy_20261115_v40.tex) shows that the complete ratio equations imply both reciprocal curve equations. It covers identities, torsion points and tangent pairs, and gives a quadratic-compatible uniform scaling of the seven pair coordinates. This redundancy is used in the source of the current [195-variable construction](papers/quartic/quartic195_20261116_v45.tex). The retained source tables give the exact dependencies of its complete polynomial specification.

The [mixed-power height theorem](papers/elliptic_heights/mixed_power_height_20261116_v45.tex) gives explicit bounds for every rational expression $x^{2n}+y^2$, $n\ge3$, under a specified fixed weak-abc inequality. In the 71-variable construction, the residual is $X(m-X)$ and the scale is $B+X^8+T_{\mathrm{sc}}^2$. Recovering the unscaled physical trace contributes $2h(X)$ only after the same strict absorption $602/679$, so it does not require a new coordinate.

## Reference charts and integer labels

The [inverse reference-square theorem](papers/elliptic_charts/inverse_reference_squares_20261116_v48.tex) gives a complete five-field-coordinate quadratic graph for both squared reciprocal abscissas. Its proof includes both exceptional linear-equation fibers without an additional nonzero condition or a square root of the translator abscissa. The [exact certificates](computation/elliptic_charts/inverse_reference_squares_v48) verify its identities and exceptional fibers.

The [three-coordinate reference chart](papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex) describes a point and its translate by two quadrics, including every tangent and two-torsion configuration in its specified domain. Its unit coordinates have explicit polynomial inverses. The [71-variable construction](papers/quartic_existence/quartic_abc71_20261116_v49.tex) uses those existing units in $v_HJ=u_HF$ and $v_HK=w_HG$ to recover the physical weighted products without a new inverse coordinate. Both reference comparison functions are affine, so the complete detector conversion stays quadratic.

The [quadratic reference and height rescaling](papers/elliptic_charts/scaled_reference_height_20261116_v43.tex) makes both reference reciprocal abscissas linear. It preserves quadratic point and ratio rows and recovers the original fixed-index height with one rational coordinate. The reference, point, ratio and height blocks use **32 rational coordinates on the nonzero-scale locus**; their necessary explicit quadratic guard adds one, giving **33 in total**, the same as the original blocks. Detector conversion remains separate. No smaller complete quartic follows.

The [quadratic reference-cover theorem](papers/elliptic_charts/reference_covers_20261116_v47.tex) gives polynomially inverse presentations with three and four field coordinates, including all four points over the two identity-reference boundaries. The four-coordinate form makes both reference reciprocal abscissas linear and remains quadratic after input scaling. Its weighted numerator and ratio equations give the physical detector products directly. A separate Jacobi chart recovers the original difference trace with one rational helper and classifies its entire zero-scale fiber. [Universal exact certificates](computation/elliptic_charts/reference_covers_v47) verify the maps and identities. Combining these blocks within a smaller complete quartic remains unproved; the ordinary-abc record stays **71**.

The [integral Pell-label theorem](papers/integer_labels/pell_labels_20261115_v40.tex) obtains exponential growth from two exact integral labels and one finite quadratic choice. It proves sharp bounds and arbitrarily large witnesses with prescribed finite congruence data. Its [checker and certificate](computation/integer_labels/pell_compression_v40) verify the identities and exceptional cases. Its application requires exact integral labels; no reduction below 25 variables follows from this theorem alone.

## Height estimates and compatible poles

The [all-point trace theorem](papers/trace_heights/trace_on_all_points_20261113_v25.tex) and [positive weighted trace theorem](papers/trace_heights/weighted_trace_20261114_v27.tex) include the half-integral index and torsion cases required by the sources. The latter also verifies that the selected Gaussian primes annihilate the half-generator using the existing congruences.

The [joint-pole theorem](papers/pole_parameters/joint_pole_realization_20261114_v29.tex) and [common-twist theorem](papers/pole_parameters/common_twists_20261114_v30.tex) reduce pole parameters on specified square-class compatibility loci. The current completeness witnesses are not proved to lie on those loci. These results do not establish a 24-variable construction or a smaller abc variable count.

The [shared-parameter local theorem](papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex) proves that **every rational conic parameter** is locally admissible for every prepared input. A finite family can use the same parameter at every completion.

The [fixed-fiber theorem](papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex) proves that one rational witness with nonzero ordinate gives infinitely many witnesses at that same parameter. In all four native sources, the extracted square-class scalars are positive rational numbers independent of the auxiliary points and finite-algebra characters. Thus every conic denominator is nonzero for every rational parameter, and the remaining pole norms can be avoided within the chosen rational fibers. The same paper gives independent auxiliary cyclic return sets preserving preparation and every earlier guard. The unresolved step toward **24 variables** is the existence of a common rational fiber for actual detector tuples; no additional pole-guard theorem is required.

The [early-scalar theorem](papers/pole_parameters/square_complement_baseline_20261116_v43.tex) preserves the general source with the same 25-coordinate census and gives a baseline with a nonzero rational square complement. Its actual guarded detector inputs can simultaneously have square complements at any prescribed finite set of rational primes. This is a finite-local realization theorem; global rational square complements and a common rational pole fiber remain open. The modified family has no newly certified effective exponent or coefficient bound.

The [doubled-source norm map](papers/pole_parameters/doubled_source_congruent_twists_20261116_v43.tex) constructs rational congruent-number points directly from native doubled elliptic points, with explicit abscissa square class. Matching that class to the required detector class remains unresolved. The [current common-fiber and reference guide](docs/common_fibers_and_reference_charts_20261116_v43.md) gives the formulas, complete block counts, exact checks, and remaining proof targets.

The [varying-input quadric theorem](papers/pole_parameters/varying_input_quadric_20261116_v44.tex) gives a positive parametrization at a fixed conic parameter: after allowing the detector input to vary within its prescribed square class, the pole surface is birational to a smooth quadric with an explicit rational point. The theorem gives exact maps, a rational parametrization and arbitrarily small positive input examples. Matching these coefficient inputs to the actual elliptic detector functions remains the arithmetic step; no smaller defining count is assigned to this result.

The separate [abelian-parameter obstruction](negative_results/papers/rational_fibers/abelian_parameter_obstruction_20261116_v44.tex) rules out uniform rational square-complement or pole-witness identities on an abelian parameter space when the detector argument is nonconstant, even with varying twist classes. Fixed-argument rational fibers, ramified covers and individual arithmetic witnesses remain open. The [fixed-argument ramification theorem](negative_results/papers/rational_fibers/fixed_argument_complement_ramification_20261116_v44.tex) additionally excludes uniform square-complement sections after surjective abelian couplings of the full independent auxiliary product at a fixed slope. Proper coupled subfamilies and individual rational witnesses remain open. The [duplication sign obstruction](negative_results/papers/elliptic_charts/duplicated_reference_signs_20261116_v44.tex) identifies an allowed quartic reference progression with incompatible doubled formal-parameter signs. These results delimit particular proposed reductions; neither proves a minimum variable count.

The [native square-complement theorem](papers/pole_parameters/guarded_complement_reduction_20261116_v45.tex) proves that every complement $17(17-b_i)$ is a unit of the entire point algebra at a prepared actual tuple. The proof uses splitting over $\mathbb Q(\sqrt2)$ and the odd valuation of $w_i/17$. If the two actual complements can be realized as rational squares for each integer input, both complete pole blocks can be removed: the conditional census is **21 variables**, or **9** in either conditional source. **That additional realization theorem is unproved; these are targets, not established record counts.** The same paper gives infinitely many prepared free inputs at one common pole parameter, without asserting native trace matching.

The [finite-class complement theorem](papers/pole_parameters/finite_complement_classes_20261116_v46.tex) weakens that realization target. Finitely many levels $17m^2$ and positive square classes supported on the **original exceptional prime set** can be allowed without adding retained coordinates. At the single level 17, it is enough that both actual complements have even valuation outside that fixed set. All whole-algebra guards remain automatic. The paper proves the same conditional **21/9** census and gives an infinite prepared free-input family with nonsquare complement class 409, allowed when 409 belongs to the exceptional set. **Actual native realization remains unproved**, so the established general counts remain **25 and 13**.

The [adaptive complement theorem](papers/pole_parameters/adaptive_native_complements_20261116_v50.tex) permits trace-dependent levels and varying quadratic classes with no new retained coordinate. Its exact change of presentation is

```math
w_i^*=\frac{w_i}{(1+w_i)^2},\qquad W_i^*=(1+w_i)W_i,\qquad
V_i^*=\operatorname{Tr}((W_i^*)^{-1}),\qquad J_i^*=\operatorname{Norm}((W_i^*)^{-1}).
```

It preserves each actual detector output $b_i=4w_i^*/(V_i^*)^2$. At a hypothetical negative odd pole, $(w_i^*,V_i^*,J_i^*)$ reduces to $(0,0,0)$. Consequently the level multiplier $m_i=1/(1-V_i^*+J_i^*)$ retains pole exclusion, although it may have poles at good contacts. Its denominator and complement are units at every prepared point-algebra character. The earlier [bounded norm levels](papers/pole_parameters/bounded_norm_levels_20261116_v48.tex) remain a separate permitted family.

The class $d_i=1-4w_i^*/17$ is automatically a local unit at the relevant primes and lies in $[16/17,1)$ on prepared real tuples. Its bare norm conic contains the fixed point $(1,1)$. The exact remaining **21/9** target is

```math
(m_iV_i^*)^2-d_i y_i^2=\frac{4w_i^*}{17},\qquad i=0,1,
```

with the first coordinates prescribed by the actual coupled detector tuple. Further classes may depend on the existing auxiliary data, subject to the proved local and whole-character conditions. **Simultaneous prescribed-trace rational realization remains unproved. The established general counts remain 25 and 13.** [Exact certificates](computation/pole_parameters/adaptive_levels_v50) verify the identities and specified local examples, not uniform rational realization.

The [norm-compatible preparation](papers/pole_parameters/norm_compatible_scalar_20261116_v47.tex) makes both associated norm conics rationally soluble throughout a prepared integer-input family. For the general source it uses an explicit degree-eight input polynomial reflecting integrality and a scalar that is a norm from $\mathbb{Q}(\sqrt{10657})$, preserving the 25-coordinate source and its height argument. The conditional sources already admit the same bare-norm preparation without changing their scalar. The unresolved equations require the first conic coordinates to equal the **actual prescribed detector traces**; bare conic solubility does not imply the 21/9 target.

The [actual prescribed-trace benchmark](papers/pole_parameters/admissible_levels_native_traces_20261116_v47.tex) realizes both equations for $X=-1$ and $X=1$, at the algebraic fixture $B=3$, after fixed positive exceptional-unit rescalings. It retains the actual point functions, detector products, traces and coupled arguments. [Three exact arithmetic implementations](computation/pole_parameters/native_trace_fixture_v47) check both equations and all **128 complement guards** over the **64 point-algebra characters**. The same paper allows general fixed levels with nonnegative even valuations outside the exceptional set; their complement guards must be established directly. This benchmark does not give uniform completeness or a sufficient defining shift. The separate [polynomial-level local theorem](papers/pole_parameters/polynomial_levels_local_20261116_v47.tex) gives explicit comparison and reference-product powers that preserve local extraction for levels $cM(X)^2$, without asserting global realization.

The separate [signed finite-class obstruction](negative_results/papers/pole_parameters/finite_nonsquare_class_obstruction_20261116_v47.tex) proves that every finite set of nontrivial rational square classes fails uniformly for the original general scalar, even with arbitrary guarded auxiliary tuples and rational level multipliers. It leaves the rational-square class available and does not apply to the redesigned norm-compatible scalar.

## Rings of integers of number fields

The [definability reductions](papers/number_fields/number_field_definability_20261109_v12.tex) relate the questions for the ring of integers, the rational integers and the rational subfield, and prove descent implications between number fields.

**No counterexample for a number field, and no theorem covering every number field, is established here.** Failure of a particular polynomial after scalar extension is not a counterexample to Diophantine definability. The [research guide](docs/research_directions.md#rings-of-integers-of-number-fields) states the remaining denominator and realization problems.

## Negative results

The [fixed-trace obstruction theorem](negative_results/papers/pole_parameters/fixed_trace_obstructions_20261116_v51.tex) excludes both normalized traces equalling one at the original general-source input $X=4$, uniformly in the slope, auxiliary tuple and odd exponent. It also excludes every finite fixed set of trace targets from uniform completeness for that source. For both conditional six-contact sources, a separate real scale bound excludes simultaneous unit traces at every prepared slope when $B\ge19$. Varying prescribed-trace norm equations and modified scalar sources remain outside these obstructions.

The [affine scalar-coupling theorem](negative_results/papers/integer_labels/affine_scalar_coupling_obstruction_20261116_v50.tex) proves that every fixed finite set of identities $S=[m]A+[k]P$ loses an infinite progression of integer inputs for the original general scalar source. Its explicit $S=A+[2]P$ counterexample is $X=11$ at $p=80287$. Altered scalar constructions and other couplings are outside its scope.

The [automatic-level finiteness theorem](negative_results/papers/pole_parameters/automatic_level_finiteness_20261116_v48.tex) excludes uniform conditional completeness from the choice $a=w\operatorname{Norm}(W)$, including fixed finite rational rescalings. The [tangent-completion theorem](negative_results/papers/elliptic_charts/tangent_completion_20261116_v48.tex) proves that all quadrics in the specified compressed pairing, even after adjoining the physical trace, leave its false tangent family. These results concern those constructions; they leave bounded native levels and different paired-point embeddings open.

The separate [obstructions and lower bounds](negative_results/README.md) directory contains the proved negative results, organized by subject with their exact hypotheses and limitations. It includes pole-predicate counterexamples, restrictions on elliptic-point compression, contact-height counterfamilies, and obstructions to extending a fixed formula to number fields. Shared computational dependencies remain linked from the corresponding papers and index.

The [pole-compression guide](negative_results/docs/pole_compression_obstructions_20261115_v41.md) presents the all-rational-coefficient conic-chain classification and the automatic-conic counterfamilies. These concern the specified predicates and prepared inputs; they do not assert a global minimum for defining polynomials.

## Reproduction

Use **Python 3.12** for the byte-pinned legacy suite and **SymPy 1.14.0** for symbolic checks. From the repository root:

    python -m pip install sympy==1.14.0
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

The current verifiers reconstruct specifications and certificates in temporary files. They cover fixed-trace inert-prime certificates, the conditional positive-interval derivative identities, normalization norm restrictions, adaptive levels, the exact pole-preserving normalization, varying classes, norm-one incidence identities and the separate affine scalar-coupling obstruction, as well as the complete 195-, 257-, and 71-variable quartics and their coefficient expansions, complete variable-difference charts including torsion and tangent fibers, unit-reference product recovery and the scaled physical trace, the complete inverse reference-square graph, bounded native norm levels, automatic-level finiteness examples, both full tangent quadratic-identity spaces, weighted-product boundary certificates and input-rescaling identities, finite complement classes, the native complement guard and mixed-power height identities, the abelian-parameter and duplication obstructions, the revised scalar identities and source census, exact quadratic reference and height rescaling with its nonzero guard, the norm map, normalization and local cancellation counterexamples, fixed-class branch and quotient identities, native fixed-fiber guards, rational-section maps, K3 branch and resolution identities, independently checked mixed reference signs, local pole cases, Tunnell coefficients, terminal nonreduced examples, reference-chart identities and exceptional cases, Pell-label examples, paired-ratio implications, invertible row transformations and complete quartic expansions. The retained verifiers authenticate the sources and supplied 198-variable archive. The full legacy verifier has **126 stages**. Optional PARI rank checks remain separately requested by --with-pari; they are not implied by --full. The new local and automatic-conic certificates do not use PARI, analytic ranks, or BSD.

The complete TeX manuscripts are the mathematical deliverables. They are compiled and visually inspected before publication. scripts/update_manifest.py records the distributed file hashes. Computational reconstruction certifies the finite identities and coefficients it checks; it does not certify external arithmetic premises or constitute independent non-author mathematical review.

## Attribution and review scope

The 198-variable parent of the current 195-variable construction was supplied in Gabriel Conant's research archive with ChatGPT. Its [original attribution and source](sources/h10_quartic198/README.md) are retained. The [pinned upstream 214-variable source](computation/quartic/balanced214_v24/source) and its hashes remain a separate dependency. The current work is maintained in this repository and does not modify the upstream repository.

The congruent-twist pole realization uses **Jaswal, Hexagon 2611.00331v2, Theorem 1.2**, with the preparation hypotheses stated in the [pole paper](papers/pole_parameters/congruent_twist_poles_20261114_v27.tex). The supplied finite-family strengthening is used only in the separate compatible-pole results. Bibliographies, [arithmetic dependencies](docs/arithmetic_inputs.md), and [THIRD_PARTY.md](THIRD_PARTY.md) retain the source distinctions.

The [reference-chart correction](docs/audits/reference_chart_correction_20261114_v27.md), [physical-normalization correction](docs/audits/scalar_ratio_correction_20261115_v33.md), and [unsupported 233-variable claim audit](docs/audits/recovery_233_20261115_v38.md) remain explicit. No 233-variable result is claimed. Earlier source files and receipts remain available for exact reproduction; their superseded numerical summaries do not replace the current table.

Original project contributions are under **CC BY 4.0**. Third-party material retains its own rights and attribution. See [CONTRIBUTING.md](CONTRIBUTING.md), [THIRD_PARTY.md](THIRD_PARTY.md), and [CITATION.cff](CITATION.cff).
