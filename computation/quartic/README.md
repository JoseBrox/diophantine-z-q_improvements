# Exact quartic constructions

The leading quartics have **301** and **351 total variables**, including the input. Both are sums of squares of explicitly listed primitive integer quadratic equations. The fixed coefficient parameter is A_N=80989^(2N+1).

| Construction | Quadratic equations | Ordinary monomials | Defining parameter |
|:--|--:|--:|:--|
| [301-variable family](family301/construction-report301.json) | 275 | 4305 | All sufficiently large N; sufficient threshold ineffective. |
| [351-variable explicit polynomial](family351/construction-report351.json) | 323 | 4990 | Every N at least 27464; explicit member A=80989^54929. |

The monomial counts hold algebraically for N at least 27464. That condition is not asserted sufficient for the 301-variable projection theorem. Both families have exact degree four, content one, and coefficient height less than 2^1520 times 80989^(4N+2). The explicit member's largest coefficient has 1,791,357 binary digits.

## Complete specification

Each family directory contains:

- quadratic-family301.json or quadratic-family351.json: every coordinate and quadratic equation;
- polynomial-family301.json or polynomial-family351.json: the complete expanded quartic coefficient table;
- construction-report301.json or construction-report351.json: the exact changes, grouping, counts, and coefficient bound;
- independent-verification301.json or independent-verification351.json: the independent finite check results.

Each monomial lists repeated coordinate identifiers, and each term separately records a power of the fixed parameter. This is a lossless abbreviation for integer coefficients, not an extra variable. The [data-format guide](../../docs/data_format.md) explains the representation.

## Construction and proof

The builder uses the pinned 317- and 370-coordinate systems directly. It replaces the products of local tests by factors whose nonconstant terms have different valuation classes, allowing orders 1, 10, and 40 in the same factor. Existing logarithm powers and a small set of new squaring equations supply the needed values. The literal trace-clearing equations are retained.

The [local proof](../../papers/local_tests/mixed_valuation_tests_20261109_v11.pdf) proves both the common-place valuation conclusion and simultaneous completeness, including zero tests, empty contact radicals, all prepared primes, square denominators, and real approximation. Separate papers state the [301-variable existence theorem](../../papers/quartic_existence/quartic301_20261109_v11.pdf) and the [351-variable explicit theorem](../../papers/quartic/quartic351_20261109_v11.pdf).

## Reproduction

The repository verifier reconstructs all dependencies before these two commands:

~~~sh
python3 build_quartic_mixed.py
python3 check_quartic_mixed.py
~~~

Run them from this directory after the source reconstruction commands in the [reproducibility guide](../../docs/reproducibility.md). The independent checker does not import the producer. It reconstructs the field constants, verifies every retained and changed quadratic row, expands sums of squares by a separate algorithm, and compares the entire coefficient table. It also verifies exact counts, content, degree, parameter noncancellation, and the explicit coefficient height. The local finite tests in mixed-identities.json supplement the uniform mathematical proof.

The baseline and source directories are proof and replication dependencies. PROVENANCE.json pins their exact source commits and bytes, and records the full construction chain. No optimizer or search output is needed to reconstruct the displayed polynomials.

## Arithmetic scope

The projection theorem retains the specified elliptic group and index-height results, contact-height theorem, pole obstruction and realization, simultaneous prime patterns, and the quantitative weighted prime-selection premise. Coefficient checks prove none of those deep inputs. The 301-variable family also uses a proved aggregate trace-height theorem with an ineffective additive constant. The 351-variable construction uses the proved effective two-component sum-height theorem and its certified numerical parameter.
