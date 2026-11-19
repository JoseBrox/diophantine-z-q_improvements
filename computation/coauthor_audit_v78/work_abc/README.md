# Independent abc quartic audit and extensions

The proof is `abc_quartic_audit_20261119.tex`. All defining claims retain the exact arithmetic premises of the pinned v65 construction, and every sufficient defining threshold remains ineffective.

## Recommended integration files

- `small_gate62/`: constant-free gates in 62 variables, with primitive, balanced, sparse, and height presentations.
- `build_small_gate62.py`, `check_small_gate62.py`: producer and independent verifier. The verifier checks the changed physical gate, exact zero-reference fiber, native twist witness identities, all coefficient transfers, and every expanded coefficient.
- `weak_quartics/`: 63-, 64-, and 67-coordinate integer-contact constructions under fixed weak abc exponents 9/8, 17/14, and 7/5.
- `build_weak_quartics.py`, `check_weak_quartics.py`: producer and independent verifier; neither checker imports its producer.
- `audit.json`: precise scope and file hashes.

The `height62/` presentation is superseded by `small_gate62/height/`. The one-unit, Belyi-search, and contact-equivalence scripts are exploratory and are not proofs of optimality.

## Reproduction

Python 3.11 or later and SymPy are sufficient. By default the scripts use the attached coauthor parent at `../H10-quartics/abc62`. When relocated, set `ABC62_PARENT` to that directory. Only the parent's `quadrics.json`, `parameter-scaling.json`, and `sparsity.json` are needed by the new checkers; the original physical-source reconstruction is separately audited by the coauthor checkers.

```sh
ABC62_PARENT=/absolute/path/to/abc62 python3 -B check_small_gate62.py
ABC62_PARENT=/absolute/path/to/abc62 python3 -B check_weak_quartics.py
```

All rational coordinate counts include the input. The primary 62-variable height presentation has 50 quadratic squares, 840 monomials, content one, and exact height `max(4091*n^2,n^4+1)` for positive integer n. Thus its height is B+1 for B=n^4 and odd n≥65. The sparse presentation has 752 monomials and exact height B+758541 for odd n≥3.

The weak families have respectively 51, 52, 55 quadratic squares and 863, 866, 905 monomials. Their exact height is B+1 for odd n≥17207, 17207, 192405, respectively. These numerical cutoffs certify coefficient height, not integer definition.

The original fractional-contact 63/64-coordinate polynomials also work at the weakened exponents 9/8 and 17/14, without any coefficient change. The new integer-contact charts give a general quartic family for every fixed weak abc exponent strictly below 3/2, with the count and strict inequality stated in the proof.

No further reduction below 62 coordinates has been proved in this audit.
