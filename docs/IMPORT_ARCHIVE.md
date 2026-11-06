# Archive provenance and repository layout

The repository incorporates the **extracted** research package dated **6 November 2026**. Source and receipt files are stored in their corresponding folders; the full research set is not represented by an opaque ZIP alone.

## Source of the files

The starting attachment was `diophantine_research_20261106_v3_final.zip`. It contains a SHA-256 manifest for **412 frozen files**, as well as the original `README.txt` and `MANIFEST.json`. The complete-repository package additionally introduced navigation and documentation, a polynomial benchmark table, and a separate paper path. These later files are not covered by the frozen-source manifest.

Folders preserve historical paths because verification scripts, hash reports and construction metadata use them as identifiers:

- `research/optimization/` — early optimization series, with experimental scripts and certificates.
- `research/phase2/` — the finite-fibre indexed 558-variable polynomial and earlier compact quartics.
- `research/phase3/` — direct-Lucas and shared-point constructions, preferred 41/43-variable indexed polynomials, 1,315/1,335-variable quartics, and number-field checks.
- `quartics/quartic-12504/` — released reference quartic and independent certificate.
- `reference_upstream/` — archived reference material and notices.

The original research manuscript is retained **unaltered** at `research/phase3/diophantine_optimization_20261106_v3.tex`. The paper at `paper/diophantine_optimization_20261106_v3.tex` is an **editorially revised** copy. Its compilation was checked with `pdflatex`, and a compiled PDF is included.

## What the integrity test does

```sh
python3 scripts/check_archive_integrity.py
```

This verifies sizes and SHA-256 hashes of all 412 frozen source files and checks the six reported best-polynomial constructions against their archived construction records. It also checks the publication TeX exists and prints both the original and edited manuscript hashes. **The published TeX is not expected to have the original hash.**

Because the underlying source is dated, historical `verification.json` files are records of the earlier executions. They are not assertions that every expensive source checker was rerun after import. The [reproducibility guide](REPRODUCIBILITY.md) identifies the original entry points and assumptions.

## Maintaining the repository

Preserve `MANIFEST.json` and the 412 frozen files. Put editorial corrections in `paper/`, modern documentation in `docs/`, and newly developed results in additional, dated research directories. Update `data/polynomial_benchmarks.csv` and `.json` consistently, then run the integrity and benchmarking scripts. Do not silently change historic verification files or conflate sample tests with proofs of mathematical equivalences.


## Large circuit transfer

The original `research/optimization/polynomial-855/polynomial-circuit.json` is 6,295,588 bytes. On GitHub it is supplied as the lossless `polynomial-circuit.json.gz` because of the connection's per-request payload limit. Run `python3 scripts/restore_large_sources.py` to reconstruct the original file byte for byte. The original SHA-256 hash is checked against `MANIFEST.json` (and the integrity test can validate it directly from gzip).
