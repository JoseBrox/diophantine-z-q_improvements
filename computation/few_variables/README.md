# Few-variable polynomial specifications

Every variable count includes the input. The leading specifications use nine quartic point generators, nonzero quadratic pole generators, and one coordinate for guarded finite-algebra elimination.

| Specification | Total variables | Degree bound | Effectiveness |
|:--|--:|:--|:--|
| [weighted27](weighted_elimination/weighted27/construction-certificate.json) | 27 | less than $2^{151}$ | All sufficiently large odd exponents; sufficient threshold ineffective. |
| [weighted29](weighted_elimination/weighted29/construction-certificate.json) | 29 | less than $2^{157}$ | Fixed exponent 137731 is certified; height at most $2^{2^{168}}$. |

The [weighted compiler](weighted_elimination/README.md) constructs exact polynomial specifications using directly scaled characteristic polynomials and resultants. Weighted principal minors control coefficient degrees. Its independent checker recomputes all bounds and tests nine small algebras. Formal matrices, generators, and finite selector indices are not extra quantified coordinates. The expanded polynomials are not materialized.

The guarded input algebras are reproduced by [trace27_nontorsion](trace27_nontorsion/README.md) and [effective29_nontorsion](effective29_nontorsion/README.md). Their older elimination outputs are retained solely as exact source and verification dependencies; the weighted specifications above are the leading constructions. The numerical 27-variable example at exponent 137731 is only an algebraic fixture and is not certified to exceed the ineffective defining threshold.

The nonzero-witness argument permits a single first-conic chart and removes all quadratic zero strata. Its proof retains the restricted-converse and descent hypotheses used by simultaneous realization. All remaining denominators are guarded. The [forced_prime29](forced_prime29/README.md) module supplies the arithmetic source; the elliptic chart and height checkers support the structural theorems.

Run `python3 scripts/verify.py --full` from the repository root for complete checks in a temporary copy. Python 3.10 or newer and its standard library suffice. See the [reproducibility guide](../../docs/reproducibility.md) for individual commands and the verification boundary.
