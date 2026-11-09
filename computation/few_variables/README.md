# Few-variable polynomial specifications

Every variable count includes the input. The leading specifications under the inherited arithmetic premises use nine quartic point generators, nonzero quadratic pole generators, and one coordinate for guarded finite-algebra elimination.

| Specification | Total variables | Degree bound | Effectiveness |
|:--|--:|:--|:--|
| [active27](active_elimination/active27/construction-certificate.json) | 27 | less than 2^87 | All sufficiently large odd exponents; sufficient threshold ineffective. |
| [active29](active_elimination/active29/construction-certificate.json) | 29 | less than 2^89 | Fixed exponent 137731 is certified; height at most 2^(2^99). |

The [current compiler](active_elimination/README.md) isolates the branches on which the source guard is nonzero and constructs one element separating those branches. It uses 262144 characteristic-polynomial factors. The independent checker recomputes the coefficient bounds without importing builder code; seven exact examples test disappearing branches, inactive nilpotents, real and complex factors, and rational recovery. Matrices and finite-algebra generators are formal polynomial operations, not extra quantified coordinates.

The guarded input algebras are reproduced by [trace27_nontorsion](trace27_nontorsion/README.md) and [effective29_nontorsion](effective29_nontorsion/README.md). Their older elimination outputs and the weighted-elimination module remain exact source and verification dependencies. The numerical 27-variable example at exponent 137731 is an algebraic fixture and is not certified to exceed the ineffective defining threshold.

The nonzero-witness argument permits a single conic chart and removes quadratic zero strata. Its proof retains the restricted-converse and descent hypotheses of simultaneous realization. Every required denominator is guarded. The [forced_prime29](forced_prime29/README.md) module supplies the arithmetic source.

Run python3 scripts/verify.py --full from the repository root for complete checks in a temporary copy. Python 3.10 or newer and its standard library suffice for the polynomial certificates. See the [reproducibility guide](../../docs/reproducibility.md) for commands and verification boundaries.


## Separate family under additional abc

The [conditional13 module](conditional13/README.md) specifies a different family with 13 total coordinates and degree below 2^44. It assumes rational abc as an additional hypothesis. Its fixed positive odd input shift has an ineffective sufficient threshold; the supplied shift3 is only a reproduction fixture. The full rational source uses three point roles, two pole certificates, and six order-one tests.
