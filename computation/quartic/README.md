# Exact quartic constructions

The leading quartics have **297** and **342 total variables**, including the input. Both are sums of squares of complete primitive integer quadratic systems. The fixed coefficient is $A_N=80989^{2N+1}$.

| Construction | Quadratic equations | Ordinary monomials | Defining parameter |
|:--|--:|--:|:--|
| [297-variable family](family297/construction-report297.json) | 271 | 4268 | All sufficiently large $N$; sufficient threshold ineffective. |
| [342-variable explicit polynomial](family342/construction-report342.json) | 314 | 4938 | Every $N\ge27464$; explicit member $A=80989^{54929}$. |

Both have exact degree four and content one. Support is constant for positive $A_N$, and the exact height for $N\ge23$ is $A_N^2+1$. These algebraic thresholds do not certify a defining member of the 297-variable family. The explicit polynomial's largest coefficient is $80989^{109858}+1$, with 1,791,283 binary digits.

## Complete specification

Each family directory contains a complete quadratic-system table, a complete expanded polynomial table, a construction report, and an independent-verification certificate. Coordinate identifiers repeat in a monomial according to exponent. Separate powers of the fixed coefficient abbreviate huge integers without adding a variable. See the [data-format guide](../../docs/data_format.md).

The builder reads the pinned 301- and 351-coordinate systems. It replaces three order-specific weights by $q$, $q^{19}$, and $q^{79}$, computed with squaring equations and a shared reciprocal cube. An invertible affine change replaces the scalar auxiliary coordinate by the actual contact product. The [shared-weight paper](../../papers/local_tests/shared_local_weights_20261109_v12.pdf) proves the valuation and simultaneous-completeness arguments, treats zero weights and denominator primes, and establishes the exact coefficient height. Separate papers state the [297-variable theorem](../../papers/quartic_existence/quartic297_20261109_v12.pdf) and [342-variable theorem](../../papers/quartic/quartic342_20261109_v12.pdf).

## Reproduction

After reconstructing source dependencies as in the [reproducibility guide](../../docs/reproducibility.md), run from this directory:

~~~sh
python3 build_quartic_shared_weights.py
python3 check_quartic_shared_weights.py
~~~

The independent checker does not import the producer. It checks every unchanged and changed quadratic row, reverses the affine substitution, expands the sum of squares independently, and compares every final coefficient. Exact support, content, degree, height, and local finite valuation assertions are also checked. The top-level verifier compares reconstructed data and certificates byte for byte in a temporary copy.

The source systems and their papers are proof and replication dependencies. `PROVENANCE.json` records the exact construction chain and hashes. Reconstruction requires no optimizer or search output.

## Arithmetic scope

Projection theorems retain the stated elliptic group and index-height results, contact-height theorem, pole obstruction and realization, and simultaneous prime-pattern results. The quantitative prime separation is derived from the cited estimates in the [prime-selection paper](../../papers/prime_selection/prime_selection_20261109_v12.pdf). The 297-variable theorem uses aggregate trace height with an ineffective additive constant; the 342-variable theorem uses the effective two-component sum-height bound. Exact coefficient checks do not establish these global arithmetic inputs.
