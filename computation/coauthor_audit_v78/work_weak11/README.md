# Weak eleven-variable audit and preferred improvements

This directory contains an integration-ready audit of the coauthor single-pole weak-abc construction, improvements that preserve its eleven-variable count, and independent checks of the ancillary realization obstructions. No shared repository files were edited by this subtask.

## Preferred results

All counts include the rational input. The finite algebra has rank 128.

| Weak-abc exponent κ | Scale power e | Band k | Coauthor degree bound | Preferred degree bound | Guard degree | Separator degree | Support bound |
|---|---:|---:|---:|---:|---:|---:|---:|
| 121/100 | 6 | 6 | 33,344,385 | **32,542,081** | 490 | 253,744 | less than 2^235 |
| 16/15 | 4 | 5 | 19,861,377 | **19,366,273** | 418 | 150,880 | less than 2^228 |

The preferred specifications are `full_flip_first/` and `full_strong_flip/`. In each directory retain these five files:

- `native.json`: exact rational coefficient DAG and finite algebra source;
- `polynomial.json`: independently replayed parent integral-algebra certificate;
- `compact.json`: the independently replayed coauthor compact-guard intermediate;
- `strengthened.json`: the final certificate with ten further automatic factors and explicit recovery order;
- `compiler_adjustments.json`: the full auxiliary point-degree adjustments.

The degree bounds are uniform in the fixed odd shift B. The coefficient one-norm bounds, respectively 2^131679488 and 2^83631616, apply to the reproducibility fixture B=3. B=3 has **not** been certified to exceed the ineffective sufficient defining threshold.

## Arithmetic scope

The defining-polynomial claim retains the project's elliptic group/index-chart statement, trace-height bound, simultaneous prime-pattern supply with congruence/order compatibility, and native pole obstruction and prepared converse including density and finite-character avoidance. It additionally assumes the indicated weak-abc inequality. It is not an unconditional independent proof of the existential definability of Z in Q.

The proof gives an eleven-variable family for every fixed 1<κ<3/2 after choosing sufficient scale and band exponents. Odd positive scale exponents are allowed by positivity of β and the root trace. The named records above retain the original even choices. A split triple of degree m with s rational branch contacts gives the more general sufficient range κ<2m/s; the positive-contact guard deletions require even s. The guarded odd-s variant requires odd band and locally square prepared slopes.

No ten- or nine-variable completeness theorem is asserted. The diagonal and zero-ordinate ancillary obstructions concern universal realization over all prepared inputs; the explicit obstructed values have not been identified as forced actual detector inputs.

## Proofs to integrate

1. `weak11_audit_and_transfer.tex` and its rendered PDF: scalar height bound, pointwise valuations, all prime classes in completeness, full auxiliary charts, ten automatic guard factors in their proper order, pole squareclass rebalance, and determinant bounds.
2. `ancillary_audit.tex` and its rendered PDF: exact scope of the diagonal Hasse failure, selector density, fixed-twist slices, zero-ordinate and point-restriction results; independent analytic rank certificate; exact local-2 trace lemma; and intrinsic-pole normalization.
3. `tex_review.json`: source and PDF hashes, every rendered page hash, and actual visual review statements for the final versions.

The last proof contains the stronger trace statement

    n² Tr x([n]P) − 57/4 ∈ 16 Z₂,

so Tr x([n]P) is itself a nonzero Q₂-square. Thus β^e+T^e is a Q₂-square for any integral β and e≥2, including odd e. A global square denominator is automatic for even e; the proof does not assert that extra global parity statement for odd e. The ordinary scale M=β⁴+T⁴ and every positive integral power of it satisfy both properties.

## Independent checkers

- `check_full_auxiliary.py`: replays source arithmetic and all six original physical tests against v71; independently recompiles the parent certificate with the correct full-chart weights; verifies all denominator and old automatic-guard coverage; proves the exact identity b=d t² inside the replayed DAG.
- `check_strengthened.py`: first invokes the preceding checker, then independently reconstructs the ten new removed atoms and their recovery order and recomputes the final degree, support, and fixture coefficient bounds. It imports neither producer. It rejects an altered degree, a missing retained guard, and an altered recovery order.
- `check_ancillary.py`: imports no attachment checker. It enumerates all primitive pairs at the Hasse-descent moduli, independently checks all 60 exceptional finite-field fibers, and gives a second exact analytic derivative certificate for E_791. It also verifies the intrinsic normalization and duplication identities symbolically.
- `ancillary_independent_certificate.json`: resulting primitive-pair counts, finite-field witnesses, exact derivative interval, and algebraic identities.

Run from this workspace:

```bash
python3 -B audit_20261119/work_weak11/check_strengthened.py --repo diophantine
python3 -B audit_20261119/work_weak11/check_ancillary.py
```

The independent derivative certificate gives

    6489867793040175244734154791093 / 10^30
      ≤ L′(E_791,1) ≤
    8941913002135842990365653860323 / 10^30.

The interval is strictly positive. The root number is −1, so the analytic rank is one; the forward Gross–Zagier–Kolyvagin theorem gives algebraic rank one without BSD. The primary conductor/sign/formula/theorem references are given explicitly in `ancillary_audit.tex`.

## Producers and dependencies

The producers are `build_full_auxiliary.py` and `strengthen_guards.py`. Both accept `--repo`; the first additionally accepts `--coauthor-root` so the source locations can be changed during integration. Preferred regeneration commands are:

```bash
python3 -B build_full_auxiliary.py --repo ../../diophantine --coauthor-root ../H10-eleven-variables --squareclass flip_first --output full_flip_first
python3 -B build_full_auxiliary.py --repo ../../diophantine --coauthor-root ../H10-eleven-variables --strong --squareclass flip_first --output full_strong_flip
python3 -B strengthen_guards.py --repo ../../diophantine full_flip_first full_strong_flip
```

The initial relative paths assume this directory's current placement. When relocating the scripts, supply the corresponding explicit paths; the checkers likewise accept `--repo`.

Required coauthor sources are only `counts/poles/build_weak11.py` and `counts/poles/finite_bounds.py`, with the latter's ordinary upstream compiler dependencies. The required pinned repository components are:

- `computation/few_variables/trace27_nontorsion/field_circuit.py`;
- `computation/few_variables/unit_norm_v28/build_sources.py` and `build.py`;
- `computation/few_variables/subalgebra_norms_v30/` producer and independent checker;
- `computation/few_variables/full_auxiliary11_v71/build_source.py` and its retained ancestors;
- `computation/few_variables/full_auxiliary11_v71/specification/source.json` as the test/point-coordinate reference.

Python 3 and SymPy suffice for the checkers in the supplied workspace; the exact analytic certificate uses Python integer/Fraction arithmetic, not a numerical library or an external rank database.

Do not integrate the experimental `full_*` variants other than the two preferred directories as record results. The limited Belyi database scan found no higher split map in its inspected subset and supplies no nonexistence theorem. Its checkout is not a deliverable dependency.

## Rendering

In the repaired workspace the two proofs compile with Latin Modern after including both TeX trees:

```bash
env 'TEXMF={/usr/share/texmf,/usr/share/texlive/texmf-dist}' TEXFORMATS=/workspace/scratch/7097ce35f5b7/tex-cache TEXFONTMAPS=/workspace/scratch/7097ce35f5b7/tex-cache: TEXMFVAR=/workspace/scratch/7097ce35f5b7/tex-cache pdflatex -interaction=nonstopmode -halt-on-error weak11_audit_and_transfer.tex
```

Repeat for resolved references and for `ancillary_audit.tex`. The explicit `lm.map` addition in each preamble avoids relying on the incomplete local font map. No extra packages were installed.
