# The ordinary-abc eleven-variable family

The [manuscript](../../../papers/conditional_few_variables/derivative_detector11_20261117_v59.tex) proves the source, its ordered completeness and every finite-algebra guard. Ordinary rational abc and the precisely retained arithmetic inputs are required. A sufficient fixed odd shift exists but is not numerically specified.

The complete native circuit is [source.json](specification/source.json); the integer polynomial is specified by [polynomial.json](specification/polynomial.json). The latter gives the free point-algebra tables, square extractions, every support factor, separator and final rank-128 determinant. There are **11 total rational coordinates**, including the input. Its degree is at most **5,444,199,553**, support is below $2^{309}$ and integer content is one. No production-sized expansion is asserted.

Rebuild a member from the repository root:

```sh
python -B computation/few_variables/derivative11_v59/build_source.py --shift 3 --output /tmp/derivative11
```

The fixed shift is an integer coefficient, never a quantified coordinate. **The stored shift 3 is an algebraic fixture, not a certified defining member.** The degree and support bounds are uniform; the coefficient norm bound is computed for the chosen shift.

| Check | Certified scope |
|:--|:--|
| `check_algebra.py` | Symbolic factorizations, derivative content, local expression degrees, height constants and exact valuation fixtures |
| `check_completeness.py` | Independent integer-polynomial arithmetic, odd valuations and uniform real bounds |
| `check_source_lemmas.py` | Independent input-height, quotient, both-slot valuation and exact contraction fixtures |
| `check_native.py` | Original elliptic group law, all detector formulas and all guards on 384 exact reductions of actual point tuples |
| `check_specification.py` | Exact circuit regeneration; independent iterative denominator, support, square-extraction and determinant-bound audit |

Every checker accepts `--output PATH`. The integrated verifier regenerates and compares all certificates. The arithmetic existence theorems are proved or explicitly cited in the paper; they are not inferred from these computations. This package establishes eleven variables under its stated assumptions and does not assert nine.

The finite-algebra compiler and guard arithmetic are reused without modifying their checked implementations in `unit_norm_v28` and their pinned helper packages. The native source here is distinct and is independently evaluated against its displayed mathematical formulas.
