# Reproducibility and evidence guide

## Fast self-contained checks

From this repository root, using Python 3.10+ and the standard library:

```sh
python3 scripts/check_archive_integrity.py
python3 scripts/report_benchmarks.py
```

`check_archive_integrity.py` rehashes every item from the source `MANIFEST.json`, checks the existence of the editorially revised manuscript, and checks the six benchmark rows. Neither command calls Sage, PARI, or a network service.

## Original research checkers

The research archive includes producers (construction code), independent algebraic checkers, proof notes, JSON receipts, and complete sparse tables. The following are selected original entry points, retained *unchanged*:

```sh
python3 -E -B research/phase3/compression/check_direct_source.py
python3 -E -B research/phase3/number_fields/check_quartic_base_change_20261106_v1.py
python3 -E -B research/phase3/number_fields/check_contact_exclusions_20261106_v1.py
python3 -E -B research/phase3/number_fields/check_real_anchor_20261106_v1.py
python3 -E -B research/phase3/number_fields/verify_division_norm_specs_independent_20261106_v1.py
```

Some are computationally substantial. Some scripts assume the **original project root at upstream git revision** `28e87b1b62af0effd954605af7f70b2699dd5672`, with root-level source files that are stored under `reference_upstream/` here. In particular, `research/phase3/verification_index.py` itself asserts a pinned `git rev-parse HEAD` and reads `quartic_12504.tex` from the original checkout's root; its historic receipt is not a portable CI test. For exact historical reproduction, place `research/` alongside an unchanged clone of that original revision and follow the original `research/phase3/README.md` instructions.

## Artifact formats

- `research/phase3/finite_fibre/polynomial-41/polynomial-specification.json`: indexed determinant/product and coefficient-DAG specification, **not** an expanded coefficient list.
- `research/phase3/finite_fibre/polynomial-43-semilocal/polynomial-specification.json`: analogous reduced-degree variant.
- `research/phase2/finite_fibre/polynomial-558/polynomial-specification.json`: source-preserving indexed alternative.
- `research/phase3/quartic/quartic-direct-translated/polynomial.json.gz`: complete sparse 1,315-variable quartic with a fixed symbolic integer coefficient `S` (substitute `S=3^(2^27)`).
- `research/phase3/quartic/quartic-direct-small-coefficients-1335/polynomial.json.gz`: complete sparse 1,335-variable ordinary integer quartic.
- `quartics/quartic-12504/polynomial.expanded.txt.gz`: released expanded 12,504-variable quartic.
- `research/phase3/verification-index.json`: historic index of checked artifacts and review receipts.

JSON.gz files are GZIP-compressed **JSON**, not opaque pickle data. The original archive includes exact coefficient tables, source systems, and verification programs; no data were omitted from this package to make it more compact.

## Checksum policy

`MANIFEST.json` is the original archive's integrity manifest, containing paths, byte sizes and SHA-256 checksums for **412 original entries**. Its 412 source files are copied without changes. The original ZIP also contained `README.txt` and `MANIFEST.json` itself. The archived research TeX is retained byte-for-byte, while the publication copy in `paper/` is edited independently. Files added by this repackaging—new `README.md`, `paper/`, `data/`, `docs/`, `scripts/`, and CI workflow—do not appear in that historical manifest; this is deliberate.

## Mathematical limitations

The checksum test proves bytes agree with the supplied archive. The independent checkers prove what their receipts explicitly describe. None independently proves the difficult arithmetic lemmas, Sun's prime-pattern theorem, or that the resulting polynomial vanishing condition characterizes Z in Q.


## Large circuit transfer

The original `research/optimization/polynomial-855/polynomial-circuit.json` is 6,295,588 bytes. On GitHub it is supplied as the lossless `polynomial-circuit.json.gz` because of the connection's per-request payload limit. Run `python3 scripts/restore_large_sources.py` to reconstruct the original file byte for byte. The original SHA-256 hash is checked against `MANIFEST.json` (and the integrity test can validate it directly from gzip).
