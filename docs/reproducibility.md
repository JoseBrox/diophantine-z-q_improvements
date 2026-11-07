# Reproducing the mathematical data

## Requirements

- Python 3.10 or newer. The final-construction and exact-arithmetic checkers use only the standard library.
- Node.js 18 or newer for the full baseline source-circuit replay.
- A TeX installation with `pdflatex`, AMS packages, `lmodern`, `mathtools`, `geometry`, `booktabs`, `longtable`, `microtype`, and `hyperref` to rebuild the papers.

No network connection, package installation, account, computer algebra system, or secret is required to run the supplied verification.

## One command

From the repository root:

```bash
python3 scripts/verify.py
python3 scripts/verify.py --full
```

The first command verifies the published manifest and runs the checks below in a temporary copy. It leaves all tracked data unchanged. The second also replays the baseline circuit's identification with the arithmetic source system. Each stage fails immediately if its required equality, hash, or bound fails.

The final quartic stage rebuilds the complete 456-coordinate residual system and expanded coefficient table, compares them byte for byte with the published data, and independently checks all substitutions and coefficients. The few-variable stage rebuilds both source systems and both finite-algebra specifications, then independently verifies their semantic expressions, guards, branch counts, degree bounds, and coefficient bounds.

The supporting stages independently enumerate the height-constant primes, check the complete local residue tables, verify the exact formal-depth constants, reproduce the two reductions modulo 17, expand the stated anisotropic forms, and specialize the entire quartic and all residuals for the quadratic-extension counterexample. Where a script also checks individual point examples, these are identified as finite examples; the uniform statements are proved in the papers.

## Individual checks

To materialize the three compressed quartic tables at their original paths, run:

```bash
python3 scripts/restore_data.py
```

The restored files are ignored by Git. Their original byte lengths and SHA-256 hashes are checked before they are written. Individual commands include:

```bash
python3 computation/quartic/verify_quartic456.py
python3 computation/few_variables/construction29/reproduce_preferred.py
python3 computation/few_variables/verify_elliptic_chart.py
python3 computation/field_extensions/verify_anisotropic_examples.py
python3 computation/field_extensions/check_field_extension.py computation/quartic/polynomial-456
```

Individual checkers may refresh their own local receipts. Use the top-level command when the published tree must remain byte-identical.

## Mathematical interpretation

A passing calculation verifies exactly the finite claims described by its receipt. The global arithmetic premises required to identify the polynomial projections with $\mathbb Z$ are stated separately in [Arithmetic inputs](arithmetic_inputs.md). Neither a file hash, a full coefficient expansion, nor successful TeX compilation proves those premises.

The degree and height bounds for the indexed constructions are checked without expanding the final polynomial. This is sufficient because the exact finite-algebra expression is specified and the paper proves the norm and degree inequalities used by the checker.

## Papers and manifest

```bash
python3 scripts/build_papers.py
```

The build runs LaTeX twice per paper and rejects missing references and overfull boxes. Inspect the rendered pages after substantive changes. PDF bytes can depend on the TeX distribution and its timestamp settings; regenerated PDFs need not have the same byte hash as the published PDF.

`MANIFEST.json` hashes the distributed files, excluding the manifest itself and generated verification/build files. Any intentional change to a published object requires refreshing this manifest with `python3 scripts/update_manifest.py` after verification and review.
