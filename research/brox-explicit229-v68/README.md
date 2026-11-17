# Explicit 229-variable quartic: proposed upstream research contribution

This **candidate** is a self-contained mathematical/evidence package for the `elliotglazer/diophantine-z-q` review process; it is not a claim of official upstream release or Protocol B acceptance.

Read [REVIEW_NOTE.md](REVIEW_NOTE.md) for the statement, a proof of the input-preserving rational coordinate equivalence, source dependencies, verified scope, limitations and attribution. The complete arithmetic text is [paper.tex](paper.tex); [source_paper.tex](source_paper.tex) is the previous 229-variable arithmetic argument for comparison.

The final literal polynomial is [quartic229-N15.txt](quartic229-N15.txt): 229 total variables including input, degree 4, 3,312 monomials, maximum coefficient `149^30`, canonical text **74,007 bytes**, SHA-256 `45bdea1ea7876bf6ec10b5427f9403cf1f94c144fab35817aa545bcb2cea1975`.

## Data and exact checks

- `source/quadratic229-v62.json`: authenticated 207-row source with parameter `C=149^N` (pin and hash in `transformation.json`).
- `transformation.json`: all 229 coordinate scalings and 207 row normalizations.
- `quadratic.json`: all transformed integer quadrics.
- `polynomial.json`: all 3,312 expanded integer-coefficient monomials.
- `quartic229-N15.txt`: complete canonical ASCII expression.
- `build.py`: deterministic reproduction of the three final algebra artifacts.
- `check.py`: standalone exact rational/integer checker; does not import the builder.
- `check_independent.py`: independent SymPy reconstruction, strict parsing, inverse substitution, comparison of arithmetic text and printed exponent tables; only local path resolution was adapted from José Brox's original checker for this folder.
- `upstream/measure_plain_text.py` and `upstream/explicit-record-README.md`: unchanged pinned upstream copies.

From this directory:

```sh
python -B build.py
python -B check.py
python -B upstream/measure_plain_text.py polynomial.json --verify-text quartic229-N15.txt
python -B check_independent.py --package . --repo . --manuscript paper.tex --output independent_certificate_replay.json
```

The final command requires SymPy; the first three need only the Python standard library. The original verification receipts `certificate.json` and `official_measurement.json` are supplied for comparison, not as independent proof of the source arithmetic hypotheses.

## Integrating into Elliot's repository

Place this folder under `research/brox-explicit229-v68/` on a feature branch whose base is the current upstream `main`. Open a **focused candidate-note pull request**, not an official version bump. Follow `AGENT-INSTRUCTIONS.md`, `CONTRIBUTING.md`, `.github/pull_request_template.md`, `docs/research-review/README.md`, and `docs/release-policy.md` from upstream `main`. Upstream maintainers—not this note—must incorporate any accepted improvement into a complete current TeX/PDF manuscript and obtain the required independent approvals.

At preparation time, upstream PR #153 separately proposed a 247-variable Version 20 quartic. Preserve that work and the frozen Version 19 records. The mathematical source relies on precisely the previously retained prime-pattern, modular-height, elliptic-group and prepared-pole inputs: this package does not separately re-prove them.
