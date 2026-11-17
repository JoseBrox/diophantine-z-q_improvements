# Candidate explicit quartic in 229 variables (74,007 ASCII bytes)

**Submission status:** focused mathematical improvement for review, **not** an accepted or published upstream record.

**Upstream base inspected:** `elliotglazer/diophantine-z-q@970ec6bf338dc47fad151132a4122fd5c899e348` (Version 19). The proposed Version 20 PR #153 currently contains a different 247-variable candidate. This proposal should not modify that PR or any frozen release.

**Original source:** `JoseBrox/diophantine-z-q_improvements@7501669160c1662a742ddd54baed364a47c82ddc`, `computation/quartic/explicit229_v62/quadratic.json`; exact source SHA-256 `f0e6fc3f62525d7b251a10fc5f4cf0e6663c3f6f08beeef3cb28092b2e1555a8`. The compact construction is documented at `papers/quartic/quartic229_compact_20261117_v68.tex` in José Brox's repository.

## Mathematical statement and proof (relative to source arithmetic)

Specialize the 207 quadratic residuals `Q_j` of the pinned 229-coordinate construction at `C=149^15`. The integer lists `a_i` (229 entries) and `b_j` (207 entries) in `transformation.json` define

```text
old_x_i = 149^(a_i) * new_y_i,
R_j(new_y) = 149^(b_j) * Q_j(149^(a_1)*new_y_1, ..., 149^(a_229)*new_y_229),
P_hat(new_y) = sum_{j=1}^{207} R_j(new_y)^2.
```

Here `a_1=0`, and every scaling factor is a nonzero rational number. The diagonal map is an automorphism of rational affine 229-space fixing the input. Each transformed quadratic row is an integer polynomial with content one (all 1,132 source terms were checked). Since rational sums of squares are zero exactly when every term is zero, the projection of `P_hat=0` onto the distinguished input is **exactly the same** as the projection of the source 207-row system. This transfers soundness and integer completeness **provided the retained arithmetic premises of the source construction hold**, with no new conditions.

A full arithmetic exposition and the diagonal exponent tables appear in `paper.tex`. Its retained arithmetic body matches the preceding `source_paper.tex` apart from the theorem-label replacement, which was checked by exact text comparison.

## Independent exact computation

Independent BigInt recomputation from the authenticated source data, performed on 17 November 2026 without importing the author's polynomial producer, found:

- 207/207 transformed rows match coefficientwise; each has integer content one.
- 3,312/3,312 fully expanded quartic coefficients match the supplied `polynomial.json`.
- All 229 variables occur, including input `x1`; degree four, content one, input fourth-power coefficient one.
- Exact maximum coefficient: `149^30 = 156887395160328947946897503379992916684449577190738324732588533001`, 217 bits.
- Reconstructed **canonical one-line ASCII text exactly equals** `quartic229-N15.txt`, comprising **74,007 bytes**, with no whitespace, compression, parameters or omitted terms.
- The pinned upstream reference measuring script and notation were compared byte-for-byte to their copies in this package. The reference report records `within_limit: true`. The text SHA-256 is `45bdea1ea7876bf6ec10b5427f9403cf1f94c144fab35817aa545bcb2cea1975`.

Reproduce from this directory:

```sh
python -B build.py
python -B check.py
python -B upstream/measure_plain_text.py polynomial.json --verify-text quartic229-N15.txt
# Optional second checker, requires SymPy:
python -B check_independent.py --package . --repo . --manuscript paper.tex --output independent_certificate_replay.json
```

The main checker uses the Python standard library and is independent of the builder; the second checker uses sparse SymPy rings, a separate literal parser and the inverse coordinate substitution. Its local source paths in this proposed upstream package replace only the original repository path lookups.

## What is verified, and what remains open

**Established here:** the input-preserving rational equivalence, transformed row integrality, fully expanded coefficients, degree, variable count, coefficient height and strict size bound. Exact reconstruction, byte comparison and polynomial-ring verification are distinct from review of the source arithmetic.

**Not independently established here:** the inherited prime-pattern, modular-height, elliptic-group and prepared-pole theorems, nor a complete independent audit of the fixed `N=15` arithmetic realization argument. Their source statements and application hypotheses still require the project reviewers' checks. The original source review records this limitation; the mathematical claim is conditional on its retained premises. The original producer and independent checker certificates report the same scope.

**Not an official record release:** Upstream policy requires a complete incorporated current TeX project, matching PDF, pinned build and hashes, cross-family Protocol B review and collaborator approval before promotion. This is a focused candidate note for maintainers to integrate. No old version, release artifact, current-manuscript selector, rule or review gate is changed.

## Attribution and AI involvement

The source 195-variable quadratic construction and the new 229-coordinate inverse-Vieta graft are due to José Brox's project. The upstream three-detector method is attributed in the source's `PROVENANCE.json` to Gemini Carbon, building on Brox's work. The reflected center `3/11` was an already documented sibling choice. The exact diagonal normalization and compact representation are documented in José Brox's v68 package. GPT-6 independently recomputed every transformation and expanded coefficient in JavaScript BigInt arithmetic, compared the canonical literal text and prepared this candidate submission; this does **not** constitute a formal proof or an authorized Protocol B outside review. No claim of fresh human or external-model acceptance is made.

## Review and release routing

Review the precise source and theorem dependencies at the pinned commits, reproduce the checkers, run Protocol B on the eventual exact PR head, and integrate only after resolving any blockers. The open upstream **PR #153** independently proposes a 247-variable candidate, so a future official 229-variable release should advance the published integer version rather than overwrite the Version 20 draft or frozen files.
