# Reproducing the mathematical data

## Requirements and full verification

All polynomial construction checks and the finite structural algebra use **Python 3.10 or newer and its standard library**. The optional exact elliptic rank, descent, and function-field calculations additionally require **cypari2** (tested with version 2.2.4 and PARI/GP 2.17.2). The published data support offline reproduction. TeX is needed only to rebuild the PDFs.

From the repository root:

~~~sh
python3 scripts/verify.py --full
~~~

The verifier checks the publication manifest and quartic provenance, copies the inputs to a temporary directory, restores compressed data with hash checks, and runs every supplied reconstruction. It leaves published inputs unchanged. A failed equality, hash, or bound stops the verification. A receipt can be saved outside the publication tree with the optional argument --receipt /path/to/verification.json.

The standard-library stages reconstruct every source dependency and the leading **238- and 318-variable quartics**, and the separately labelled additional-abc quartic. The parity construction and independent checker verify every retained row, every reduced power, all local factors, and the complete sum of squares. The shared-weight builder reads the exact 301- and 351-coordinate systems. Its independent checker verifies retained and changed rows, the invertible scalar normalization, every expanded coefficient, degree, content, support, and exact height. Both the data and independent certificates are compared byte for byte with the distributed files.

The **25- and 29-variable specifications**, together with the 13-variable additional-hypothesis specification, are rebuilt from complete guarded source algebras. The independent checkers verify conversion, every point quartic and denominator guard, weighted matrix bounds, and all finite-product cases. The 25-variable degree calculation uses formal coefficient symbols to establish uniformity in the fixed odd exponent. Its $L=3$ fixture is not certified to define the integers. The explicit 29-variable exponent $137731$ has a separately certified effective threshold. The older 27-variable specification is retained only as an exact source and proof dependency.

The additional structural stages check the number-field finite-difference identities and elliptic examples, and the restricted quadratic-input obstruction. They are finite checks supporting full proofs, not proofs of general projection assertions by enumeration.

The release [verification receipt](../data/verification-v18.json) records the completed standard-library and optional PARI stages. It distinguishes exact identities from separately labelled bounded searches.

## Individual quartic commands

Restore the compressed source tables, then reconstruct dependencies in order:

~~~sh
python3 scripts/restore_data.py
python3 computation/quartic/build_quartic392.py
python3 computation/quartic/verify_quartic392.py
python3 computation/quartic/build_quartic389.py
python3 computation/quartic/check_quartic389.py
python3 computation/quartic/verify_detector_normalizations.py
python3 computation/quartic/build_quartic370.py
python3 computation/quartic/check_quartic370.py
python3 computation/quartic/build_quartic329.py
python3 computation/quartic/check_quartic329.py
python3 computation/quartic/build_quartic317.py
python3 computation/quartic/check_quartic317.py
python3 computation/quartic/build_quartic_mixed.py
python3 computation/quartic/check_quartic_mixed.py
python3 computation/quartic/build_quartic_shared_weights.py
python3 computation/quartic/check_quartic_shared_weights.py
python3 computation/quartic/build_quartic_even.py
python3 computation/quartic/check_quartic_even.py
python3 computation/quartic/build_quartic279.py
python3 computation/quartic/check_quartic279.py
python3 computation/quartic/build_quartic273.py
python3 computation/quartic/check_quartic273.py
python3 computation/quartic/build_quartic267.py
python3 computation/quartic/check_quartic267.py
python3 computation/quartic/build_quartic263.py
python3 computation/quartic/check_quartic263.py
python3 computation/quartic/build_quartic259_v17.py
python3 computation/quartic/check_quartic259_v17.py
python3 computation/quartic/build_quartic249_v17.py
python3 computation/quartic/check_quartic249_v17.py
python3 computation/quartic/build_quartic248_v17.py
python3 computation/quartic/check_quartic248_v17.py
python3 computation/quartic/build_quartic_abc97_v17.py
python3 computation/quartic/check_quartic_abc97_v17.py
python3 computation/quartic/build_fixed_difference_v18.py
python3 computation/quartic/check_fixed_difference_v18.py
python3 computation/quartic/build_quartic318_v18.py
python3 computation/quartic/check_quartic318_v18.py
python3 computation/elliptic_constraints/check_fixed_difference_chart.py
python3 computation/quartic/check_coordinate_budget.py
~~~

The 329-coordinate step is an algebraic dependency needed to reconstruct the exact 317-coordinate source. All fixed source hashes are checked before they are used. The new quartic builders do not depend on unreported searches or unpublished intermediate polynomials.

## Few-variable and supporting checks

~~~sh
python3 computation/few_variables/effective29_nontorsion/reproduce.py
python3 computation/few_variables/trace27_nontorsion/reproduce.py --anchor-exponent 137731
python3 computation/few_variables/forced_prime29/reproduce.py
python3 computation/square_predicates/check_square_predicates.py
python3 computation/square_predicates/check_height7_linear_multiplier.py
python3 computation/effective_sums/check_effective_elliptic_sums.py
python3 computation/quadratic_squares/check_quadratic_square_chart.py
python3 computation/scalar_normalization/check_scalar_normalization.py
~~~

The explicit and source few-variable modules are standalone. Their default commands reconstruct in temporary directories and compare the source and specification byte for byte with the distributed certificate. An optional --output DIRECTORY retains the reconstruction. The other individual scripts may write generated reports beside their sources; use the top-level verifier to preserve every distributed byte.

### Weighted specifications

After reproducing the two source algebras above, run:

~~~sh
python3 computation/few_variables/weighted_elimination/build_weighted_specification.py computation/few_variables/trace27_nontorsion/example_L137731/polynomial-specification.json computation/few_variables/weighted_elimination/weighted27
python3 computation/few_variables/weighted_elimination/build_weighted_specification.py computation/few_variables/effective29_nontorsion/certificate/polynomial-specification.json computation/few_variables/weighted_elimination/weighted29
python3 computation/few_variables/weighted_elimination/check_weighted_specification.py computation/few_variables/weighted_elimination/weighted27 computation/few_variables/weighted_elimination/weighted29 --output computation/few_variables/weighted_elimination/verification.json
~~~

### Separation on the nonzero guard locus

The leading few-variable specifications are rebuilt with the following commands. Each builder reads the guarded source specification; the independent checker imports no builder implementation.

~~~sh
python3 computation/few_variables/active_elimination/build_active_specification.py computation/few_variables/trace27_nontorsion/example_L137731/polynomial-specification.json computation/few_variables/active_elimination/active27
python3 computation/few_variables/active_elimination/build_active_specification.py computation/few_variables/effective29_nontorsion/certificate/polynomial-specification.json computation/few_variables/active_elimination/active29
python3 computation/few_variables/active_elimination/check_active_specification.py computation/few_variables/active_elimination/active27 computation/few_variables/active_elimination/active29 --output computation/few_variables/active_elimination/independent-verification.json
python3 computation/few_variables/active_elimination/check_active_degenerations.py --output computation/few_variables/active_elimination/degeneration-certificate.json
~~~

### Number fields and input normalization

The following programs use exact integers and rational arithmetic. The number-field checker writes its certificate in the current directory; the input-map checker takes an explicit output path. The full verifier runs both in an isolated copy.

~~~sh
python3 computation/number_fields/check_norm_image_reduction.py
python3 computation/input_normalization/check_quadratic_input_obstruction.py --output computation/input_normalization/quadratic-input-obstruction-certificate.json
~~~

### Uniform scalar normalization and witness constraints

~~~sh
python3 computation/scalar_normalization/check_uniform_scalar_normalization.py
python3 computation/elliptic_constraints/search_reduction_parities.py
python3 computation/elliptic_constraints/check_large_split_orders.py
~~~

The scalar checker verifies the two resultant computations, exact polynomial identities, all residue classes at the avoidance primes, local square conditions, and rational bounds. The elliptic checkers verify explicit reduction-order counterexamples and the stated finite enumeration. The large-prime check uses exact modular group arithmetic, prime-quotient witnesses, primality checks, and two independent finite-field point counts. Its example at 77017 satisfies the displayed rational congruences, without asserting the stronger Gaussian-generator conditions. The papers prove the uniform statements and specify the scope of each obstruction.

### Disjoint contacts and elliptic ranks

The contact checker factors every determinant and exclusion value specifying the exceptional primes. It uses exact integer arithmetic and does not claim to prove the underlying height premise by testing examples.

~~~sh
python3 computation/contact_heights/check_contact_height_amplification.py --output computation/contact_heights/contact-height-certificate.json
python3 -m pip install cypari2
python3 scripts/verify.py --full --with-pari
~~~

The standard-library rationality-filter checker expands the degree-eleven slope and degree-nine ordinate polynomials and repeats the explicitly bounded point search. The infinite-omission theorem uses the cited Corvaja–Zannier theorem and the proved rational-map containment, not this search.

The optional PARI stages also check the prepared fixed-pole counterexamples, with matching exact rank bounds and squareclass descent. The elliptic-ratio stage recomputes matching lower and upper rank bounds for the explicit curves and all eight quadratic twists, exact torsion orders, the polynomial expansion, and finite local identities. It uses unconditional 2-descent bounds, without analytic rank or BSD. Without `--with-pari`, the full verifier checks integrity of the stored rank certificate but does not rerun its descent calculations. The receipt states whether this stage was run.

## What the verification establishes

A passing receipt establishes the finite assertions stated in that receipt. Complete quartic coefficient tables and the finite-algebra expression graphs are exact polynomial specifications. The enormous few-variable polynomials are specified and bounded without expanding all their terms: the determinant, resultant, trace, and finite-product inequalities are proved in their papers and independently checked by the programs.

Coefficient verification does not prove the global arithmetic inputs in [Arithmetic inputs](arithmetic_inputs.md). It also does not produce a numerical sufficient parameter for an ineffective existence theorem. The 25-variable and 238-variable results retain this explicit limitation.

The nonzero pole-witness strengthening uses the retained restricted-converse and descent hypotheses and the source simultaneous-realization construction. Its mathematical proof is in both leading few-variable papers. It is not a conclusion of enumerating finite cases.

## Rebuilding the papers

~~~sh
python3 scripts/build_papers.py
~~~

The build requires pdflatex and the AMS, lmodern, mathtools, geometry, booktabs, longtable, microtype, xcolor, and hyperref packages. It runs three passes per paper and rejects undefined or duplicate references, unresolved rerun requests, and overfull boxes. The [main paper index](../README.md#read-the-papers) links every PDF and editable TeX source. Rendered pages should be inspected after substantive edits.

PDF bytes can depend on the TeX distribution and timestamp settings even when the mathematical text is unchanged. Source and data integrity are recorded separately.

## Integrity and provenance

MANIFEST.json records the distributed file sizes and SHA-256 hashes. The quartic PROVENANCE.json binds exact source bytes, builders, independent checkers, mathematical proof files, and the data-format guide. Compressed-source metadata additionally records the uncompressed byte length and hash of each restored table.

After a reviewed change, refresh the publication manifest with:

~~~sh
python3 scripts/update_manifest.py
~~~

## Exceptional correspondences and pole parameters

~~~sh
python3 computation/number_fields/check_exceptional_correspondence.py
python3 computation/pole_parameters/check_fixed_e_obstruction.py
~~~

The first checker uses only exact rational arithmetic. It verifies the smooth exceptional surface, its birational formulas, and the exceptional lines. The second requires cypari2 and verifies the prepared inputs, their elliptic images, exact ranks, torsion, and the squareclass obstruction. PARI's rank bounds are unconditional; BSD is not used. The full verifier runs these checks in its temporary copy.


## Separate family under additional abc

The full verifier also rebuilds the [weak-abc13 source](../computation/few_variables/weak_abc13/README.md), audits all three point quartics, both pole clearings and every atomic guard, then reconstructs its final 64-factor finite-algebra specification and independently checks the bounds. That module's README gives all four standalone commands.

These stages check the exact coefficient family and the degree bound uniform in its fixed shift. They neither verify the additional conjectures nor certify that the supplied shift 3 exceeds the ineffective defining threshold. The earlier conditional13 module remains only as a reconstruction dependency.

The 13-variable family uses weak abc at exponent 121/100, which follows from ordinary abc or ordinary Szpiro. The additional-abc quartic uses ordinary rational abc. Both retain the stated elliptic and pole-realization premises. The exact quartic monomial counts are obtained by expanding the full sum of squares. For the determinant polynomials, `computation/few_variables/check_monomial_bounds.py` instead proves uniform support upper bounds; it does not report exact support counts.

The following optional PARI commands check two retained-parameter counterexamples and the compressed elliptic subtraction identity:

~~~sh
python3 computation/pole_parameters/check_fixed_tau_obstruction.py
python3 computation/pole_parameters/check_fixed_tau17_obstruction.py
python3 computation/quartic/check_z_difference_identity.py
~~~

The common-parameter and product-contact obstructions use only the standard library:

~~~sh
python3 computation/pole_parameters/check_pole_merger_obstructions.py --output computation/pole_parameters/pole-merger-obstructions.json
python3 computation/few_variables/check_monomial_bounds.py
~~~

## Restricted abc and dense pole obstructions

~~~sh
python3 computation/restricted_abc/check_frey_denominator.py
python3 computation/pole_parameters/check_small_fixed_tau17_obstruction.py
python3 computation/pole_parameters/check_quartic_pole_obstruction.py
python3 computation/contact_heights/check_evaluation_height.py
~~~

These exact checks certify finite constants and algebraic identities used by the corresponding proofs. The height and density theorems are established mathematically in the papers.


## Local normalization and the refined height estimate

The following exact checks use only the Python standard library:

~~~sh
python3 computation/local_tests/check_rational_normalization.py
python3 computation/contact_heights/check_nebentypus_height.py
~~~

The local checker includes equal-valuation cancellation, the mixed even-valuation inequalities, disjoint contact and pole residues, and the complete finite exceptional-prime calculation. Its finite cases support the general proofs in the local-normalization paper. The height checker verifies the character-order arithmetic, the fixed-prime constant, and the explicit bounds; it does not replace the modular-realization premise by a computation.

The default verifier checks the rational identities and pinned rank inputs for the small fixed-pole obstruction. Only `--with-pari` reruns its exact two-descent. This keeps the documented standard-library route independent of optional packages.


## Twenty-five-variable source and degree certificate

~~~sh
python3 computation/few_variables/merged25/build_merged_source.py --anchor-exponent 3 --output computation/few_variables/merged25/certificate
python3 computation/few_variables/merged25/check_merged_source.py computation/few_variables/merged25/certificate --output computation/few_variables/merged25/independent-source-verification.json
python3 computation/few_variables/active_elimination/build_active_specification.py computation/few_variables/merged25/certificate/source-polynomial-specification.json computation/few_variables/merged25/active25
python3 computation/few_variables/merged25/check_merged_bounds.py --output computation/few_variables/merged25/independent-bound-verification.json
~~~

The source checker proves the source-to-integer conversion, the point quartics, square clearings, and atomic guard coverage exactly. It also independently evaluates every new rational formula over fifteen finite-field samples; these samples are explicitly supplementary evidence rather than a general identity proof. The degree checker independently sums all 262,144 cases and verifies the uniform symbolic coefficient envelope. These calculations accompany the mathematical projection proof and do not certify that the numerical fixture exceeds its ineffective threshold.

The current full run passes 89 standard-library stages; enabling PARI passes 95 stages. The receipts are [standard-library verification](../data/verification-standard-v18.json) and [verification with PARI](../data/verification-v18.json).

## Six-contact product obstruction

The unrestricted contact-product counterfamily is checked using exact rational polynomial identities, its contact permutation, and the scale family:

~~~sh
python3 computation/pole_parameters/check_six_contact_product.py
~~~

The certificate is `computation/pole_parameters/six-contact-product-verification.json`. Its scope is the unrestricted contact product; it does not assert that the counterfamily satisfies the other equations of the thirteen-variable source.
