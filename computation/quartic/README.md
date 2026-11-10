# Current quartic coefficient families

All counts include the input. The input projection equals the integers under the arithmetic assumptions stated in the corresponding paper.

| Family | Additional hypothesis | Variables | Quadratic equations | Ordinary monomials | Terms with parameter powers separate | Defining parameter |
|:--|:--|--:|--:|--:|--:|:--|
| family238_v18 | None beyond the inherited premises | 238 | 212 | 2924 | 2925 | Every sufficiently large $N$; threshold ineffective |
| family318_v18 | None beyond the inherited premises | 318 | 290 | 5060 | 5061 | Every $N\ge27464$ |
| family_abc93_v18 | **Ordinary rational abc** | 93 | 81 | 920 | 921 | Every sufficiently large odd $B$; threshold ineffective |

Each family has exact degree four and integer content one. The ordinary support counts hold for every positive integer coefficient parameter. In family238_v18 the fixed coefficient is $A_N=149^{2N+1}$ and the height is $A_N^2+1$ for $N\ge53$. In family318_v18 the base is $80989$ and the corresponding coefficient threshold is $N\ge23$. In family_abc93_v18 the fixed coefficient is the odd input shift $B$ and the coefficient height for $B\ge3$ is $\max(4153456,B^2+797687)$. These coefficient thresholds do not certify the ineffective defining thresholds.

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
python3 computation/quartic/build_quartic263.py
python3 computation/quartic/check_quartic263.py
python3 computation/quartic/build_quartic259_v17.py
python3 computation/quartic/check_quartic259_v17.py
python3 computation/quartic/build_quartic249_v17.py
python3 computation/quartic/check_quartic249_v17.py
python3 computation/quartic/build_quartic248_v17.py
python3 computation/quartic/check_quartic248_v17.py
python3 computation/quartic/build_quartic_abc97_v17.py
python3 computation/quartic/check_quartic_abc97_v17.py
python3 computation/quartic/build_fixed_difference_v18.py
python3 computation/quartic/check_fixed_difference_v18.py
python3 computation/quartic/build_quartic318_v18.py
python3 computation/quartic/check_quartic318_v18.py
python3 computation/elliptic_constraints/check_fixed_difference_chart.py
~~~

The intermediate families are exact reconstruction dependencies. Each current family directory contains the complete quadratic table, expanded quartic, construction report, and independent verification certificate. No coefficient checker imports a producer. The checkers reconstruct every changed row, compare retained rows with their pinned source, verify coordinate incidence, and expand every coefficient of the sum of squares independently. Their finite algebraic checks support the mathematical projection proofs; they do not establish the inherited arithmetic premises or abc.

The source chain is in [PROVENANCE.json](PROVENANCE.json). The current papers prove the [238-variable theorem](../../papers/quartic_existence/quartic238_20261110_v18.pdf), the [318-variable theorem](../../papers/quartic/quartic318_20261110_v18.pdf), and the [93-variable theorem under abc](../../papers/quartic_existence/quartic_abc93_20261110_v18.pdf).

## Symmetric ten-contact normalization

For the scales $a=1,T$, where $T$ is one quarter of the trace of the sum of four root abscissas, put $t=a\lambda$ and $r=(t-1)^2$. The contacts are $\Theta\cup(2-\Theta)$, with the five-contact set $\Theta=\{0,-1/2,-1,1/2399,-32/407\}$. Their product is $F_{10}(t)=P_5(r)$, evaluated with four quadratic outputs. The only new exceptional prime beyond the inherited cutoff is $2029147$.

The literal equations are

$$F_{10}(t)(1+q)=r^2r^3,\qquad (1+q)b=(408/409)^2\tau^2.$$

For $t\ne1$, they give $R=F_{10}/(t-1)^{10}$ and $q=R^{-1}-1$. The strata $t=1$ and $q=0$ have radical one. The local weight outputs satisfy $q_2=q^2$, $q_4=q_2^2$, and $q q_7=q_4^2$; the last coordinate may be free when $q=0$, which the proof handles explicitly. At every consumed contact it equals $q^7$.

The proved bound $h(a)<2^{330671}M_5(a)^{7/2}$ gives exponent $7/4$ for the ten contacts. This permits plain formal parameters in every comparison. The scalar norm denominator uses $R_s^4$, forcing $149^{L_N}M_5(\beta)^3\mid c=|a-1|$. The sharper height bound is $h(\beta)\le2^{330670}149^{-L_N}c(1+\log c/3)$; the integral Lucas bound $(c-5)\log(c-2)$ gives the final contradiction for sufficiently large fixed $N$. These statements use the source's modular realization and the retained elliptic, pole, and prime-pattern inputs, with no additional abc.

## Eight-contact normalization under abc

The additional-abc family uses the contacts $\{-3,-2,-1,0,2,3,4,5\}$ and two scales $1,a$, where $a=\beta^4+T^4$, $\beta=2X^2+B$, and $T$ is a single elliptic trace. With $r=(t-1)^2$, the quadratic equations

$$
u=qr,\qquad k=ur,\qquad k^2-30ku+273u^2-820uq+576q^2=kr
$$

give $qF_8(t)=r^3$ and $k=(t-1)^{10}/F_8(t)=1/R$ after the proof excludes $q=0$. The contact product is not a separate coordinate. The fourth-power scale is computed from

$$
S=\beta^2+T^2,\quad p=\beta T,\quad a=S^2-2p^2.
$$

The abc contact and projective-height estimates have respective coefficients $1/3$ and $4/3$, giving strict absorption coefficient $8/9$. Three elliptic point roles and six local tests of order one suffice. The input-comparison value is a coordinate, with $\beta=L_0-I_0$ and one row $I_0-L_0+2X^2+B=0$; this gives the quadratic coefficient-height dependence on $B$. The sufficient input shift remains ineffective.

The compressed formula for the shared point difference is checked against the elliptic addition law by `check_z_difference_identity.py`, using exact PARI function-field arithmetic through `cypari2`. The full paper excludes all exceptional point classes before interpreting its quotients. The general coefficient reconstruction itself uses only the Python standard library.

The family279 and family273 files are coefficient dependencies only: no integer-projection theorem is asserted for their literal tables. The current projection theorems are proved from the displayed current normalizations.


## Four-coordinate common point and direct ratios

The current families use three quadratic equations in $S=y(H)/x(H)$, $T=y(H-P)/x(H-P)$, $f=1/x(H)$, and $g=1/x(H-P)$. The [general chart proof](../../papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) treats every leading-coefficient exception and proves $fg\ne0$ from the equations themselves. The direct relations $L_iI_i=V_iS$ and $L'_iK_i=Q_iT$ compute both ratios from the existing numerator-pair coordinates.

`build_fixed_difference_v18.py` reads the pinned quadratic sources in `family248_v17` and `family_abc97_v17`. Its independent checker reconstructs the three field equations, the direct ratios, the exact invertible six-row rational change, all retained rows, and the entire quartic. The determinant of the row change is $-1/362963666515968$. A separate standard-library program proves the general chart's polynomial identities by exact expansion. The older coefficient tables are reconstruction dependencies; the displayed current theorems are the 238-, 318-, and 93-variable results.


The fully specified 318-variable family uses the same common-point equations and normalizes each numerator logarithm by the shared correction factor. `build_quartic318_v18.py` reads the pinned family322 source. Its independent checker reconstructs 22 changed rows, compares 268 unchanged rows, verifies each correction factor, and expands all coefficients. The new potential boundary is excluded arithmetically in the full proof. The certified defining parameter $N=27464$ and exact height $80989^{109858}+1$ are retained.
