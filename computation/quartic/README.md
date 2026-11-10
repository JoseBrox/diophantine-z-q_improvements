# Current quartic coefficient families

All counts include the input. The input projection equals the integers under the arithmetic premises stated in the corresponding paper.

| Family | Additional hypothesis | Variables | Quadratic equations | Ordinary monomials | Terms with parameter powers separate | Defining parameter |
|:--|:--|--:|--:|--:|--:|:--|
| family226_v21 | None beyond the inherited premises | 226 | 200 | 2835 | 2836 | Every sufficiently large $N$; threshold ineffective |
| family262_v21 | None beyond the inherited premises | 262 | 234 | 3494 | 3495 | Every $N\ge9682$ |
| family_abc87_v21 | **Ordinary rational abc** | 87 | 75 | 918 | 919 | Every sufficiently large odd $B$; threshold ineffective |

Each family has exact degree four and integer content one. The ordinary support counts hold for every positive coefficient parameter. In the first two families the fixed coefficient is $A_N=149^{2N+1}$ and the height is $A_N^2+1$ for $N\ge53$. At the explicit defining value $N=9682$, the height is $149^{38730}+1$, with 279599 binary digits. The abc family has coefficient height $\max(4153456,B^2+797681)$ for $B\ge3$. Algebraic coefficient thresholds and sufficient defining thresholds are separate statements.

The full papers prove the [226-variable theorem](../../papers/quartic_existence/quartic226_20261110_v21.pdf), the [262-variable theorem](../../papers/quartic/quartic262_20261110_v21.pdf), and the [87-variable theorem under abc](../../papers/quartic_existence/quartic_abc87_20261110_v21.pdf). No global minimum number of quartic variables is claimed.

## Exact reconstruction

From the repository root, with the distributed dependency tables present:

~~~sh
python3 computation/quartic/build_quartic276_v19.py
python3 computation/quartic/check_quartic276_v19.py
python3 computation/quartic/build_reciprocal_factors_v19.py
python3 computation/quartic/check_reciprocal_factors_v19.py
python3 computation/quartic/build_quartic265_v19.py
python3 computation/quartic/check_quartic265_v19.py
python3 computation/quartic/build_inverse_contact_v21.py
python3 computation/quartic/check_inverse_contact_v21.py
python3 computation/quartic/build_abc_inverse_contact_v21.py
python3 computation/quartic/check_abc_inverse_contact_v21.py
python3 computation/quartic/build_abc_reciprocal_contacts_v21.py
python3 computation/quartic/check_abc_reciprocal_contacts_v21.py
~~~

For all source dependencies and the other papers, run `python3 scripts/verify.py`. The source chain, file hashes, proof hashes, and commands are recorded in [PROVENANCE.json](PROVENANCE.json).

Each current family directory contains the complete quadratic table, expanded quartic, construction report, and independent verification certificate. The checker does not import its producer. It reconstructs every changed row from the field formulas, compares all retained rows with the pinned source, checks every coordinate, and independently expands all coefficients of the sum of squares. The arithmetic premises, valuation arguments, and completeness statements are proved separately in the papers.

## Reciprocal local factors

The common-point chart uses three quadrics in four field coordinates for $H,H-P$, retaining both reciprocal abscissas and both $y/x$ values. Its [general proof](../../papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) treats every exceptional leading coefficient and proves that the relevant denominators are nonzero.

For the inherited-premise families, write $q=R^{-1}-1$. The local equations store

$$q s_1=1,\qquad s_2=s_1^2,\qquad s_4=s_2^2.$$

Multiplying every factor equation by $q^{-4}$ allows terms $q^4B_i^4$ to become $(B_i^2)^2$ using the existing stored squares. In the 226-variable construction this expresses five field fourth powers through existing squares. Its local factors before clearing are

$$\begin{aligned}
T_1&=1+q^5C_2^2+q^2D_H^2+q^4B_1^4,\\
T_2&=1+q^5G^2+q^2A_3^2+q^4B_0^4,\\
T_3&=1+q^5I^4+q^3A_2^2+q^2A_4^2+q^4B_3^4,\\
T_4&=1+q^5C_3^2+q^2C_1^4+q^4B_4^4,\\
T_5&=1+q^5C_4^2+q^2A_1^2+q^4B_2^4.
\end{aligned}$$

The third factor has distinct valuation classes at every consumed contact. The comparison precision is three; the plain formal-parameter error has order four. The proof checks arbitrary witness pole orders, shared prime support, and every exceptional stratum.

The explicit 262-variable construction uses four factors for each of its three detectors:

$$\begin{aligned}
T_1&=1+q^9C_2^4+q^3C_1^4+q^2D_H^2+q^4B_1^4,\\
T_2&=1+q^9G^4+q^3A_3^2+q^2B_0^2+q^4B_2^4,\\
T_3&=1+q^9C_3^4+q^3A_2^2+q^2I^4+q^4B_3^4,\\
T_4&=1+q^9C_4^4+q^3A_1^2+q^2A_4^2+q^4B_4^4.
\end{aligned}$$

The additional equation $w_5s_4=q$ gives $w_5=q^5$. After multiplication by $q^{-4}$, all four factor equations are quadratic in the stored coordinates. The four shared fourth powers $C_2^4,G^4,C_3^4,C_4^4$ use eight rational coordinates. At an active contact, the four nonconstant summands have disjoint valuation classes: $-\nu,\nu,2$ modulo four and $4$ modulo eight, where $\nu$ is the positive odd contact order. The resulting bounds give order three for $C_2,C_3,C_4,G$ and order one for $C_1,I$; every reciprocal abscissa has positive even valuation. These precisions suffice for the global arithmetic proof. The complete system has 262 coordinates and 234 quadratic rows.

The [multiplicity height theorem](../../papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.pdf) gives effective contact exponent $7/3$ without restricting the modular character orders of the contact primes. Two disjoint five-contact sets give exponent $7/6$. The 226-variable construction uses scales $1,T$, with $T$ one quarter of the trace of four root abscissas. The explicit construction uses $1,S_0^2,(S_0+S_1)^2$ and an effective height theorem for the two rational components. The retained scalar normalization yields

$$149^{L_N}M_5(\beta)^3\mid |a-1|,\qquad
L_N=\left\lfloor\frac{19(2N-1)}8\right\rfloor+1.$$

The independent checker verifies the sufficient integer inequalities at $N=9682$, including the resulting depth $L_N=45988$. The preceding integer fails this particular sufficient criterion; this is not a proof that it fails to define the integers.

## Quadratic contact equations

Let $P_5(r)=r^5-e_1r^4+e_2r^3-e_3r^2+e_4r-e_5$, where its five roots are the squared distances of the contact pairs from one. The inverse weight $s_1=q^{-1}$ already occurs in the local factors. Three outputs suffice:

$$r=(t-1)^2,\qquad u=r^2,$$
$$v=ru-e_1(1+s_1)u+e_2(1+s_1)r,\qquad
uv=(1+s_1)(e_3u-e_4r+e_5).$$

Together with $qs_1=1$, these equations are equivalent to $(1+q)P_5(r)=r^5$. They exclude $P_5(r)=0$ and preserve the boundary $r=0$, where $q=s_1=-1$. The removed polynomial output has no use elsewhere in the source. The 226- and 262-variable systems have respectively 200 and 234 quadratic rows. The independent checker reconstructs the contact coefficients from elementary symmetric sums and verifies the general projection identity before expanding every coefficient.

## The abc family

The eight contacts are $\{-3,-2,-1,0,2,3,4,5\}$, and the scales are $1,\beta^4+T^4$, where $\beta=2X^2+B$ and $T$ is a single elliptic trace. Ordinary rational abc and the projective-height estimate give strict absorption coefficient $8/9$.

The contacts are $\{-5,-2,-1,0,2,3,4,7\}$. Put $r=(t-1)^2$ and $P_4(r)=(r-1)(r-4)(r-9)(r-36)$. Reciprocal symmetry gives

$$P_4(r)/r^2=z^2-50z+481,\qquad z=r+36/r.$$

Two shifted contact outputs $R=r-1$, $Z=z-37$ and three inverse weights satisfy

$$R=t^2-2t,\quad RZ+Z-R^2+35R=0,\quad (R+1)s=Z^2+24Z,$$
$$s_2=s^2,\qquad s_3=ss_2.$$

These equations exclude $r=0$ directly, and the point-pair chart excludes $s=0$. The stored factors are $A_i=sT_i$, with $(R+1)\Omega=A_1A_2$. Rescaling the trace by $s^2/r$ gives $s_3b=\eta^2$, exactly the pole input associated to the new contact polynomial. The local and completeness proofs treat this contact set directly; no projection equivalence with a different contact set is asserted.

All contact-equation constant terms vanish. The exact coefficient height is $\max(4153456,B^2+797681)$. The independent checker reconstructs all 75 quadratic rows and 918 ordinary monomials. For odd $B\ge1833$, the height is $B^2+797681$; this is a coefficient statement.

The sufficient odd input shift remains ineffective. The weak abc/Szpiro premise used for the separate 13-variable construction is not asserted sufficient for this quartic.

## Supporting data

Intermediate coefficient tables are retained only where needed for exact reconstruction and source comparisons. In particular, `family228_v19`, `family265_v19`, and `family_abc91_v19` are pinned sources for the contact constructions. The 87-variable builder reads the exact `family_abc89_v21` coefficient table, changes the contact set, and replaces its contact and weight rows. The 89-variable tables remain reconstruction dependencies. The table `family266_v19` is the pinned source of `family265_v19`, and `family276_v19` is a source of `family266_v19`. Their presence does not list them as current best results. The family279 and family273 tables remain algebraic dependencies without an integer-projection theorem for their literal equations. The current proofs use the displayed current local normalizations.
