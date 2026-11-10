# Current quartic coefficient families

All counts include the input. The input projection equals the integers under the arithmetic premises stated in the corresponding paper.

| Family | Additional hypothesis | Variables | Quadratic equations | Ordinary monomials | Terms with parameter powers separate | Defining parameter |
|:--|:--|--:|--:|--:|--:|:--|
| family228_v19 | None beyond the inherited premises | 228 | 202 | 2829 | 2830 | Every sufficiently large $N$; threshold ineffective |
| family265_v19 | None beyond the inherited premises | 265 | 237 | 3485 | 3486 | Every $N\ge14521$ |
| family_abc91_v19 | **Ordinary rational abc** | 91 | 79 | 926 | 927 | Every sufficiently large odd $B$; threshold ineffective |

Each family has exact degree four and integer content one. The ordinary support counts hold for every positive coefficient parameter. In the first two families the fixed coefficient is $A_N=149^{2N+1}$ and the height is $A_N^2+1$ for $N\ge53$. At the explicit defining value $N=14521$, the height is $149^{58086}+1$, with 419333 binary digits. The abc family has coefficient height $\max(4153456,B^2+797683)$ for $B\ge3$. Algebraic coefficient thresholds and sufficient defining thresholds are separate statements.

The full papers prove the [228-variable theorem](../../papers/quartic_existence/quartic228_20261110_v19.pdf), the [265-variable theorem](../../papers/quartic/quartic265_20261110_v19.pdf), and the [91-variable theorem under abc](../../papers/quartic_existence/quartic_abc91_20261110_v19.pdf). No global minimum number of quartic variables is claimed.

## Exact reconstruction

From the repository root, with the distributed dependency tables present:

~~~sh
python3 computation/quartic/build_quartic276_v19.py
python3 computation/quartic/check_quartic276_v19.py
python3 computation/quartic/build_reciprocal_factors_v19.py
python3 computation/quartic/check_reciprocal_factors_v19.py
python3 computation/quartic/build_quartic265_v19.py
python3 computation/quartic/check_quartic265_v19.py
~~~

For all source dependencies and the other papers, run `python3 scripts/verify.py`. The source chain, file hashes, proof hashes, and commands are recorded in [PROVENANCE.json](PROVENANCE.json).

Each current family directory contains the complete quadratic table, expanded quartic, construction report, and independent verification certificate. The checker does not import its producer. It reconstructs every changed row from the field formulas, compares all retained rows with the pinned source, checks every coordinate, and independently expands all coefficients of the sum of squares. The arithmetic premises, valuation arguments, and completeness statements are proved separately in the papers.

## Reciprocal local factors

The common-point chart uses three quadrics in four field coordinates for $H,H-P$, retaining both reciprocal abscissas and both $y/x$ values. Its [general proof](../../papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) treats every exceptional leading coefficient and proves that the relevant denominators are nonzero.

For the inherited-premise families, write $q=R^{-1}-1$. The local equations store

$$q s_1=1,\qquad s_2=s_1^2,\qquad s_4=s_2^2.$$

Multiplying every factor equation by $q^{-4}$ allows terms $q^4B_i^4$ to become $(B_i^2)^2$ using the existing stored squares. In the 228-variable construction this eliminates five field coordinates. Its local factors before clearing are

$$\begin{aligned}
T_1&=1+q^5C_2^2+q^2D_H^2+q^4B_1^4,\\
T_2&=1+q^5G^2+q^2A_3^2+q^4B_0^4,\\
T_3&=1+q^5I^4+q^3A_2^2+q^2A_4^2+q^4B_3^4,\\
T_4&=1+q^5C_3^2+q^2C_1^4+q^4B_4^4,\\
T_5&=1+q^5C_4^2+q^2A_1^2+q^4B_2^4.
\end{aligned}$$

The third factor has distinct valuation classes at every consumed contact. The comparison precision is three; the plain formal-parameter error has order four. The proof checks arbitrary witness pole orders, shared prime support, and every exceptional stratum.

The explicit 265-variable construction uses four factors for each of its three detectors:

$$\begin{aligned}
T_1&=1+q^9C_2^4+q^3C_1^4+q^2D_H^2+q^4B_1^4,\\
T_2&=1+q^9G^4+q^3A_3^2+q^2B_0^2+q^4B_2^4,\\
T_3&=1+q^9C_3^4+q^3A_2^2+q^2I^4+q^4B_3^4,\\
T_4&=1+q^9C_4^4+q^3A_1^2+q^2A_4^2+q^4B_4^4.
\end{aligned}$$

The additional equation $w_5s_4=q$ gives $w_5=q^5$. After multiplication by $q^{-4}$, all four factor equations are quadratic in the stored coordinates. The four shared fourth powers $C_2^4,G^4,C_3^4,C_4^4$ use eight rational coordinates. At an active contact, the four nonconstant summands have disjoint valuation classes: $-\nu,\nu,2$ modulo four and $4$ modulo eight, where $\nu$ is the positive odd contact order. The resulting bounds give order three for $C_2,C_3,C_4,G$ and order one for $C_1,I$; every reciprocal abscissa has positive even valuation. These precisions suffice for the global arithmetic proof. The complete system has 265 coordinates and 237 quadratic rows.

The [multiplicity height theorem](../../papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.pdf) gives effective contact exponent $7/3$ without restricting the modular character orders of the contact primes. Two disjoint five-contact sets give exponent $7/6$. The 228-variable construction uses scales $1,T$, with $T$ one quarter of the trace of four root abscissas. The explicit construction uses $1,S_0^2,(S_0+S_1)^2$ and an effective height theorem for the two rational components. The retained scalar normalization yields

$$149^{L_N}M_5(\beta)^3\mid |a-1|,\qquad
L_N=\left\lfloor\frac{19(2N-1)}8\right\rfloor+1.$$

The independent checker verifies the sufficient integer inequalities at $N=14521$, including the resulting depth $L_N=68973$. The preceding integer fails this particular sufficient criterion; this is not a proof that it fails to define the integers.

## The abc family

The eight contacts are $\{-3,-2,-1,0,2,3,4,5\}$, and the scales are $1,\beta^4+T^4$, where $\beta=2X^2+B$ and $T$ is a single elliptic trace. Ordinary rational abc and the projective-height estimate give strict absorption coefficient $8/9$.

The reciprocal coordinates satisfy

$$s_4=s_2^2,\qquad q s_4=s_3,\qquad q s_3=s_2.$$

The nonzero branch gives $s_j=q^{-j}$. On the zero branch the cleared factor equations force both numerator reciprocal abscissas to vanish; the exact point-pair chart then gives $0=1$. Thus no extra nonvanishing coordinate is needed. Two fourth-power field coordinates are removed and one additional inverse-weight coordinate per detector is added, giving 91 total rational coordinates.

The sufficient odd input shift remains ineffective. The weak abc/Szpiro premise used for the separate 13-variable construction is not asserted sufficient for this quartic.

## Supporting data

Intermediate coefficient tables are retained only where needed for exact reconstruction and source comparisons. In particular, `family266_v19` is the pinned source of `family265_v19`, and `family276_v19` is a source of `family266_v19`. Their presence does not list them as current best results. The family279 and family273 tables remain algebraic dependencies without an integer-projection theorem for their literal equations. The current proofs use the displayed current local normalizations.
