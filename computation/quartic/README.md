# Current quartic coefficient families

All counts include the input. The rational projections equal the integers under the arithmetic premises stated in the corresponding papers.

| Family | Variables | Quadratic equations | Ordinary monomials | Terms with parameter powers separate | Defining parameter |
|:--|--:|--:|--:|--:|:--|
| family279 | 279 | 253 | 3692 | 3693 | Every sufficiently large $N$; threshold ineffective |
| family322 | 322 | 294 | 4992 | 4993 | Every $N\ge27464$ |

The fixed coefficient is $A_N=80989^{2N+1}$. Both families have exact degree four, integer content one, and support independent of positive $A_N$. Their coefficient height is $A_N^2+1$ for $N\ge23$. This is an algebraic coefficient threshold, not a sufficient defining threshold.

From the repository root:

~~~sh
python3 computation/quartic/build_quartic_even.py
python3 computation/quartic/check_quartic_even.py
python3 computation/quartic/build_quartic279.py
python3 computation/quartic/check_quartic279.py
~~~

The first pair constructs and checks family322 from the pinned family342 table. The second constructs and checks family279 directly from family297. The 279 scripts import only the polynomial utilities of their respective producer or independent checker. No checker imports producer code. Each script accepts explicit source and output roots.

Each family directory contains the full quadratic table, expanded quartic, construction report, and independent verification certificate. Checkers reconstruct every changed row, compare every retained row, verify coordinate incidence, and independently expand the sum of squares. The mathematical proofs establish the unrestricted local valuation implications and global projections; finite checks have their recorded scope.

The complete source chain is in PROVENANCE.json. The current proofs are [the 279-variable theorem](../../papers/quartic_existence/quartic279_20261109_v13.pdf) and [the 322-variable theorem](../../papers/quartic/quartic322_20261109_v13.pdf).

## Arithmetic scope

The projection theorems retain the stated elliptic group and index-height assertions, contact-height theorem, pole obstruction and realization, and simultaneous prime-pattern results. Quantitative separation follows from the cited estimates in the prime-selection paper. The 279-variable construction uses the proved four-block contact-height amplification and aggregate trace height with an ineffective additive constant. The 322-variable construction uses the effective two-component sum-height estimate. Finite coefficient checks do not establish those arithmetic premises or determine an ineffective threshold.
