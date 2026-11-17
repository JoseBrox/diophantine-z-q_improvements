# Full auxiliary points in the general source

This package specifies a complete **25-variable** integer polynomial family under the arithmetic premises retained by the general source. Counts include the input. The four root points retain integer indices in `2E(K)`. The five auxiliary points use cubic charts covering the guarded affine points of `E(K)`.

The degree bound is **4,924,857,429,000,192**, strictly below `2^53`. The encoder degree is at most 1,048,576, the support bound is strictly below `2^1193`, and integer content is one. The native circuit has 6,169 integer arithmetic nodes, 101 recorded guards and 128 retained norm factors.

The same auxiliary enlargement preserves soundness of the corresponding 21-variable actual-trace source. Simultaneous rational realization of its two actual square equations remains unproved. No 21-variable completeness claim is made.

## Fixed exponent and coefficient bounds

`L` is a fixed odd integer at least three. Every sufficiently large fixed `L` defines the integers, under the retained arithmetic premises. The sufficient threshold is ineffective. The stored **L = 3 member is an algebraic fixture**, not a numerically certified defining member.

Degree and support bounds are uniform in `L`. The coefficient L1 norm is reconstructed for each supplied `L`. The fixed powers of 76,249 remain integer circuit nodes; their coefficient norm bounds are propagated with their actual fixed exponents.

| Fixed exponent | Coefficient L1 norm bound |
| --- | --- |
| L = 3 | `2^34765159307149312` |
| L = 5 | `2^38018481590894592` |

## Reconstruction

From the repository root:

```sh
python computation/few_variables/full_auxiliary25_v72/build_source.py --L 3
python computation/few_variables/full_auxiliary25_v72/check.py
```

The repository is discovered from the script location. Explicit paths and the inherited metadata argument names are supported:

```sh
python computation/few_variables/full_auxiliary25_v72/build_source.py --repo . --name general25 --parameter 5 --output verification_full_auxiliary25_L5
python computation/few_variables/full_auxiliary25_v72/check.py --repo . --specification verification_full_auxiliary25_L5
```

`dependencies.json` pins 19 reused project files by SHA-256, including the full auxiliary point-algebra audit. All dependencies are read without modification. The complete finite list of in-memory compiler adjustments is recorded in `construction.json`. Parent-specification pins are relative to the directory containing the specification files.

## Independent checks

The verifier repeats exact polynomial checks of the rank-four point multiplication table, primitive quartic, discriminant, cubic coordinate identity, weighted degrees and coefficient norm estimates. A separate iterative traversal verifies guard factorization, subalgebra support, root envelopes, denominator retention and the full degree bound. Two deliberate corruptions, of a degree and a guard record, are rejected.

The native detector is independently evaluated at 72 finite characters of actual rational elliptic point charts, at two split primes. The chosen auxiliary indices include `3/2`, `9/2` and `15/2`. These evaluations cover the identity sign pattern, every individual ordinate-sign flip and deterministic mixed patterns. They do not enumerate all `4^9` point characters. Whole-character completeness follows from the algebraic chart isomorphism in the proof, which maps every original complete witness to the enlarged source.

The final pole root may vanish; the first pole radicand and all point radicands remain units. These finite checks verify the circuit and bounds. They do not prove the retained external arithmetic premises, certify a sufficient numerical exponent, or establish the 21-variable rational realization condition.

## Files

| File | Purpose |
| --- | --- |
| `build_source.py` | Family builder with `--L`, `--parameter`, `--repo` and `--output` |
| `check.py` | Independent exact algebra, circuit, guard and degree verification |
| `dependencies.json` | SHA-256 pins for reused code |
| `specification/source.json` | Complete native integer circuit for L = 3 |
| `specification/subalgebra_parent.json` | Parent subalgebra norm specification |
| `specification/polynomial.json` | Final terminal-root polynomial specification |
| `specification/construction.json` | Construction bounds and exact adjustments |
| `specification/independent_certificate.json` | Verification certificate |

The proof is in `papers/few_variables25/full_auxiliary25_20261117_v72.tex`.
