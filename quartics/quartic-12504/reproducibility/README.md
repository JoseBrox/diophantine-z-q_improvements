# Reproducing the 12,504-variable quartic

This directory contains the checks and construction tools for the exact
quartic in its parent directory. There are 12,504 total variables, including
input 0, and 12,503 existential witnesses. The polynomial has degree four,
135,721 nonzero monomials, and largest absolute coefficient
685783949153203534233601, strictly below 2^80.

The uncompressed coefficient table has 3,239,486 bytes and SHA-256
`7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca`.
Every coefficient is an integer. Each line after the comment gives a
coefficient followed by its repeated variable indices.

Run from any directory with Python 3.12 and no third-party packages:

```sh
python3 -E -B /path/to/quartics/quartic-12504/reproducibility/run.py \
  --output /path/to/a/new/reproduction-directory --stage-seconds 300
```

Use a fresh output directory outside the package. The runner reads package
files without changing them. It puts generated files, logs, and verification
reports in the requested output directory. It rejects optimized Python
execution and invokes every child with `-E -B` so environment settings cannot
disable assertions or create bytecode in the package.

The complete construction was frozen on Linux with CPython 3.12. The runner
first checks that the current gzip/zlib implementation reproduces the exact
frozen source bytes. It stops immediately if this compatibility check fails.
The final report records Python, platform, and zlib versions. Exact-byte
regeneration is checked, so a platform or interpreter that serializes
differently must fail rather than silently report reproduction. The frozen
artifact's algebraic replay uses exact Python integers and rational numbers
and can be run separately with the unchanged checker on a writable copy.

The command performs these checks in order:

1. Check every file in `manifest.json`, the pinned source and checker
   identities, and the exact source entry.
2. Run the unchanged original parity, anchor, sieve-constant, and quotient
   arithmetic checkers against their frozen inputs, and the finite reciprocal
   arithmetic checks.
3. Independently audit all reciprocal-source modules and their flattening.
   Compare the complete audit report with the frozen report, except elapsed
   time, and compare the newly reconstructed construction map byte-for-byte.
4. Run all 38 malformed-source rejection tests and five separate tests that
   resource exhaustion is never counted as semantic rejection.
5. Copy the frozen final artifact to the output directory and replay its
   complete certificate. Expand the full sum of squares and check the exact
   integer polynomial, monomial count, degree, variable count, and strict
   coefficient bound. Run the certificate mutation tests separately.
6. Regenerate the source using its frozen compiler. Compare every audited
   source file's digest, then independently audit this new source.
7. Build a new quadratic lift, perform the recorded norm, chart, ordinate,
   parity, and batch reductions, optimize, and merge proportional
   coordinates. Replay independently after every step. Compare the final
   coefficient table, residual rows, variable map, and weights exactly with
   the frozen artifact. All certificate records must also agree after
   removing only the elapsed time in `final.report.seconds`.

The final `SUMMARY.json` says `PASS: FROZEN REPLAY AND CLEAN REPRODUCTION`
only after all checks finish. A timeout, failed assertion, changed byte, or
unfinished stage is not a successful reproduction. Each subprocess has the
specified time limit. For an external total time or memory budget, invoke
the runner through a process-group supervisor.

`verify_certificate.py` is the unchanged, independently reviewed checker
from the frozen construction, renamed from `verify_named_source.py`.
Its SHA-256 is
`d2079177a4960740c5b7d42fbd0756dfc4ce8953cc947cee91c8786ba26fa8ba`.
The reduction tools in `tools/` and the auditor in `source-audit/` are also
unchanged copies. The runner is a release wrapper; it supplies paths and
checks exact outputs without changing any algebraic rule.

The source ID is
`reciprocal64-beta16-compressed-s1-b5e836d77643`. It uses high precision 64,
beta precision 16, 24 anchor squarings, and compressed primary charts.
The source is a distinct named entry. It is not a relabeling of the older
15,672-variable source. Historical files retain their original proposal
wording and report scope.

These computations establish the finite construction and the exact
projection-preserving reduction to the named source. The mathematical
argument that the source defines the integers, including the analytic
estimates and global nonvanishing, is in the accompanying proof and
independent reviews. A successful computation does not replace that proof.
