# Few-variable polynomial specifications

Every variable count includes the input. The leading modules use nine quartic point generators, nonzero quadratic pole generators, and one coordinate for guarded finite-algebra elimination.

| Module | Total variables | Degree bound | Effectiveness |
|:--|--:|:--|:--|
| [trace27_nontorsion](trace27_nontorsion/README.md) | 27 | less than 2^154 | Every sufficiently large fixed odd exponent works; sufficient threshold ineffective. |
| [effective29_nontorsion](effective29_nontorsion/README.md) | 29 | less than 2^161 | Fixed exponent 137731 is certified; coefficient height at most 2^(2^171). |

Each directory contains a complete standalone builder, independent source checker, finite-algebra compiler, independent specification checker, exact data, and an end-to-end reproduction command. Python's standard library suffices. Source and polynomial specifications are reproduced byte for byte. Formal matrix entries, generators, and finite selector indices are not additional quantified coordinates.

The nonzero-witness argument in the accompanying papers permits a single first-conic chart and removes all quadratic zero strata. Its proof uses the restricted-converse and descent inputs already retained in the source realization argument. All remaining denominators are guarded, and the omitted point factors are proved automatically nonzero at every rational retained base.

The numerical 27-variable example at exponent 137731 is only an algebraic reproducibility fixture. No numerical member is certified to exceed its ineffective threshold.

The [forced_prime29](forced_prime29/README.md) module remains as the exact arithmetic and finite-algebra source for the proof dependencies. The elliptic chart and height identity checkers in this directory support the corresponding unconditional theorems.

For full checks in a temporary copy, run python3 scripts/verify.py --full from the repository root. See the [reproducibility guide](../../docs/reproducibility.md) for all commands and the mathematical verification boundary.
