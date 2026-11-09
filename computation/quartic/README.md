# Current quartic coefficient families

All counts include the input. The rational projections equal the integers under the arithmetic premises stated in the corresponding papers.

| Family | Variables | Quadratic equations | Ordinary monomials | Terms with parameter powers separate | Defining parameter |
|:--|--:|--:|--:|--:|:--|
| family267 | 267 | 241 | 3422 | 3423 | Every sufficiently large $N$; threshold ineffective |
| family322 | 322 | 294 | 4992 | 4993 | Every $N\ge27464$ |

The fixed coefficient is $A_N=80989^{2N+1}$. Both families have exact degree four, integer content one, and support independent of positive $A_N$. Their coefficient height is $A_N^2+1$ for $N\ge23$. This is an algebraic coefficient threshold, not a sufficient defining threshold.

From the repository root:

~~~sh
python3 computation/quartic/build_quartic_even.py
python3 computation/quartic/check_quartic_even.py
python3 computation/quartic/build_quartic279.py
python3 computation/quartic/check_quartic279.py
python3 computation/quartic/build_quartic273.py
python3 computation/quartic/check_quartic273.py
python3 computation/quartic/build_quartic267.py
python3 computation/quartic/check_quartic267.py
~~~

The first pair constructs and checks family322 from the pinned family342 table. The next pair constructs and checks the retained family279 source directly from family297. The following pairs reconstruct family273 and the current family267 from their pinned predecessors. The intermediate families are computational dependencies. The 279 scripts import only the polynomial utilities of their respective producer or independent checker. No checker imports producer code. Each script accepts explicit source and output roots.

Each family directory contains the full quadratic table, expanded quartic, construction report, and independent verification certificate. Checkers reconstruct every changed row, compare every retained row, verify coordinate incidence, and independently expand the sum of squares. The mathematical proofs establish the unrestricted local valuation implications and global projections; finite checks have their recorded scope.

The complete source chain is in PROVENANCE.json. The current proofs are [the 267-variable theorem](../../papers/quartic_existence/quartic267_20261109_v15.pdf) and [the 322-variable theorem](../../papers/quartic/quartic322_20261109_v13.pdf).

## Arithmetic scope

The projection theorems retain the stated elliptic group and index-height assertions, contact-height theorem, pole obstruction and realization, and simultaneous prime-pattern results. Quantitative separation follows from the cited estimates in the prime-selection paper. The 267-variable construction uses the proved four-block contact-height amplification and aggregate trace height with an ineffective additive constant. The 322-variable construction uses the effective two-component sum-height estimate. Finite coefficient checks do not establish those arithmetic premises or determine an ineffective threshold.

## The contact normalization

For both positive rational scales $a=1,T$, the construction uses $t=a\lambda$, $\delta=t-1$ and

$$
R=\frac{F_{20}(t)}{\delta^{22}},\qquad e=\frac{\delta^{20}}{F_{20}(t)},\qquad q=\frac{\delta^{18}}{F_{20}(t)}.
$$

Here $T$ is one quarter of the trace of the sum of the four root abscissas. Each detector evaluates $F_{20}(t)$ and $(t-1)^{20}$ together in six coordinates. The scale enters only through $t$, and its square and scaled numerator powers are unnecessary. The literal clearing equations are $F_{20}(t)e=(t-1)^{20}$, $q\delta^2=e$, and $e\delta^2b=\tau^2$.

At a prepared finite prime, $v(e)=0$ and $v(q)=v(R)=-2v(t)$. The identity $R=\delta^{-2}\prod_\theta(1+(1-\theta)/\delta)$ supplies the needed local squareclasses when $t$ has sufficiently negative valuation. The prime-pattern theorem permits the fixed rational scales after denominator clearing. These statements are proved in the current paper.

The 267-coordinate checker reconstructs both normalization blocks and the linear trace scale directly, then checks every changed and retained row, all coordinate incidences, the complete sum of squares, and the coefficient support and height. The family279 and family273 tables are retained only as pinned coefficient dependencies. Their previous scaled numerator was not the polynomial used in their projection argument; no integer-projection theorem is asserted for those coefficient sources. The family267 proof establishes the projection using its corrected literal equations.
