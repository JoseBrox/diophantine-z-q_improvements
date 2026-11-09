# Reproducing the mathematical data

## Requirements and full verification

All exact computational checks use **Python 3.10 or newer and its standard library**. The published data support offline reproduction. TeX is needed only to rebuild the PDFs.

From the repository root:

~~~sh
python3 scripts/verify.py --full
~~~

The verifier checks the publication manifest and quartic provenance, copies the inputs to a temporary directory, restores compressed data with hash checks, and runs every supplied reconstruction. It leaves published inputs unchanged. A failed equality, hash, or bound stops the verification. A receipt can be saved outside the publication tree with the optional argument --receipt /path/to/verification.json.

The 34 stages reconstruct every source dependency and the leading **297- and 342-variable quartics**. The shared-weight builder reads the exact 301- and 351-coordinate systems. Its independent checker verifies retained and changed rows, the invertible scalar normalization, every expanded coefficient, degree, content, support, and exact height. Both the data and independent certificates are compared byte for byte with the distributed files.

The **27- and 29-variable weighted specifications** are rebuilt from the complete guarded source algebras. The independent checker recomputes weights, literal finite sums, degree and norm recurrences, finite selector ranges, and small-algebra examples. The 29-variable fixed exponent 137731 is certified by the effective arithmetic estimate. The 27-variable example at the same exponent is an algebraic fixture; no numerical defining threshold is certified for it. Its degree bound is uniform because the coefficient parameter has degree zero.

The additional structural stages check the number-field finite-difference identities and elliptic examples, and the restricted quadratic-input obstruction. They are finite checks supporting full proofs, not proofs of general projection assertions by enumeration.

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

The two leading few-variable modules are standalone. Their default commands reconstruct in temporary directories and compare the source and specification byte for byte with the distributed certificate. An optional --output DIRECTORY retains the reconstruction. The other individual scripts may write generated reports beside their sources; use the top-level verifier to preserve every distributed byte.

### Weighted specifications

After reproducing the two source algebras above, run:

~~~sh
python3 computation/few_variables/weighted_elimination/build_weighted_specification.py computation/few_variables/trace27_nontorsion/example_L137731/polynomial-specification.json computation/few_variables/weighted_elimination/weighted27
python3 computation/few_variables/weighted_elimination/build_weighted_specification.py computation/few_variables/effective29_nontorsion/certificate/polynomial-specification.json computation/few_variables/weighted_elimination/weighted29
python3 computation/few_variables/weighted_elimination/check_weighted_specification.py computation/few_variables/weighted_elimination/weighted27 computation/few_variables/weighted_elimination/weighted29 --output computation/few_variables/weighted_elimination/verification.json
~~~

### Number fields and input normalization

The following programs use exact integers and rational arithmetic. The number-field checker writes its certificate in the current directory; the input-map checker takes an explicit output path. The full verifier runs both in an isolated copy.

~~~sh
python3 computation/number_fields/check_norm_image_reduction.py
python3 computation/input_normalization/check_quadratic_input_obstruction.py --output computation/input_normalization/quadratic-input-obstruction-certificate.json
~~~

## What the verification establishes

A passing receipt establishes the finite assertions stated in that receipt. Complete quartic coefficient tables and the finite-algebra expression graphs are exact polynomial specifications. The enormous few-variable polynomials are specified and bounded without expanding all their terms: the determinant, resultant, trace, and finite-product inequalities are proved in their papers and independently checked by the programs.

Coefficient verification does not prove the global arithmetic inputs in [Arithmetic inputs](arithmetic_inputs.md). It also does not produce a numerical sufficient parameter for an ineffective existence theorem. The 27-variable and 297-variable results retain this explicit limitation.

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
