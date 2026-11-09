# Current quartic coefficient families

All counts include the input. The input projection equals the integers under the arithmetic assumptions stated in the corresponding paper.

| Family | Additional hypothesis | Variables | Quadratic equations | Ordinary monomials | Terms with parameter powers separate | Defining parameter |
|:--|:--|--:|--:|--:|--:|:--|
| family263 | None beyond the inherited premises | 263 | 237 | 3312 | 3313 | Every sufficiently large $N$; threshold ineffective |
| family322 | None beyond the inherited premises | 322 | 294 | 4992 | 4993 | Every $N\ge27464$ |
| family_abc98 | **Ordinary rational abc** | 98 | 86 | 882 | 885 | Every sufficiently large odd $B$; threshold ineffective |

Each family has exact degree four and integer content one. The ordinary support counts hold for every positive integer coefficient parameter. In family263 and family322 the fixed coefficient is $A_N=80989^{2N+1}$ and the coefficient height is $A_N^2+1$ for $N\ge23$. In family_abc98 the fixed coefficient is the odd input shift $B$ and the coefficient height for $B\ge3$ is $\max(11600064,2B^4+169997)$. These coefficient thresholds do not certify the ineffective defining thresholds.

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
python3 computation/quartic/build_quartic_abc98.py
python3 computation/quartic/check_quartic_abc98.py
~~~

The intermediate families are exact reconstruction dependencies. Each current family directory contains the complete quadratic table, expanded quartic, construction report, and independent verification certificate. No coefficient checker imports a producer. The checkers reconstruct every changed row, compare retained rows with their pinned source, verify coordinate incidence, and expand every coefficient of the sum of squares independently. Their finite algebraic checks support the mathematical projection proofs; they do not establish the inherited arithmetic premises or abc.

The source chain is in [PROVENANCE.json](PROVENANCE.json). The current papers prove the [263-variable theorem](../../papers/quartic_existence/quartic263_20261109_v16.pdf), the [322-variable theorem](../../papers/quartic/quartic322_20261109_v13.pdf), and the [98-variable theorem under abc](../../papers/quartic_existence/quartic_abc98_20261109_v16.pdf).

## Symmetric twenty-contact normalization

For each of the scales $a=1,T$, where $T$ is one quarter of the trace of the sum of four root abscissas, put $t=a\lambda$ and $r=(t-1)^2$. The twenty contacts are symmetric about one, so their product is $F_{20}(t)=P_{10}(r)$. Five successive quadratic outputs compute $r,r^2,r^4,r^5,P_{10}(r)$. Every exponent from zero through ten is a sum of two elements of $\{0,1,2,4,5\}$.

The literal normalization is

$$
F_{20}(t)q=r^4r^5,\qquad k=qr^2,\qquad kb=\tau^2.
$$

On the nonzero domain, $q=(t-1)^{18}/F_{20}(t)$ and $k=1/R$, where $R=F_{20}(t)/(t-1)^{22}$. The possible stratum $t=1$ has contact radical one and is treated without division. The proof verifies all fixed-place and real preparation conditions for these literal equations. It uses the inherited contact estimate and aggregate trace height, with no additional conjecture.

## Six-contact normalization under abc

The additional-abc family uses the contacts $\{-2,-1,0,2,3,4\}$ and two scales $1,a$, where $a=\beta^6+T^6$, $\beta=2X^2+B$, and $T$ is a single elliptic trace. With $r=(t-1)^2$, the quadratic equations

$$
u=qr,\qquad k=ur,\qquad kr-14k+49u-36q=r^2
$$

give $qF_6(t)=r^2$ and $k=(t-1)^8/F_6(t)=1/R$. The contact product need not be retained as a separate coordinate. The sixth-power scale is computed from

$$
S=\beta^2+T^2,\quad p=\beta T,\quad V=S^2-3p^2,\quad a=SV.
$$

The abc contact and projective-height estimates have respective coefficients $2/3$ and $2/5$, giving the strict absorption coefficient $8/15$. Three elliptic point roles and six local tests of order one suffice. The sufficient input shift remains ineffective.

The compressed formula for the shared point difference is checked against the elliptic addition law by `check_z_difference_identity.py`, using exact PARI function-field arithmetic through `cypari2`. The full paper excludes all exceptional point classes before interpreting its quotients. The general coefficient reconstruction itself uses only the Python standard library.

The family279 and family273 files are coefficient dependencies only: no integer-projection theorem is asserted for their literal tables. The current projection theorems are proved from the displayed current normalizations.
