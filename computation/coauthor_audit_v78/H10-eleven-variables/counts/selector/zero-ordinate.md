# A prepared input whose terminal pole ordinate cannot be zero

Let
$$
 P_d(v,s)=d(d+v^2)^2s^4-d(d-v^2)^2(1-d)^2
$$
be the intrinsic polynomial from Brox v56. Its prepared-input theorem concerns $0<d<1$ with square reduced denominator, $d\in7\mathbb Q_2^{\times2}$ and $v_2(d)\ge4$. The rational input
$$
 d=\frac{112}{225}=7(4/15)^2,\qquad 1-d=\frac{113}{225}
$$
satisfies all these conditions. It has rational witnesses to $Y^2=P_d(v,s)$ under the source's theorem. It has **no** rational pair $v,s$ with $P_d(v,s)=0$, even without nonvanishing or sign conditions. This rules out specializing the pole ordinate to zero as a universal black-box reduction using only the inherited preparation. A successful new construction may still arrange that its own actual pole inputs belong to a smaller subclass.

Put $E_N:y^2=x^3-N^2x$ for $N=791=7\cdot113$. If $P_d(v,s)=0$, put $e=(d-v^2)/(d+v^2)$ and $p=2dv/(d+v^2)$. Then $p^2=d(1-e^2)$ and $s^2=(1-d)|e|$. The denominator $d+v^2$ is positive. Also $e\ne0$ because $d$ is nonsquare, and hence $s\ne0$. Define
$$
 x=\frac{N(1-d)}{s^2}=\frac{N}{|e|},\qquad
 a=\frac{113}{4s},\qquad y=axp.
$$
Here $x=da^2$ and so $y^2=x^3(1-e^2)=x^3-N^2x$. Thus $E_N(\mathbb Q)$ would contain a nonzero abscissa of square class $7$.

The Mordell–Weil rank of $E_{791}$ is exactly one. The associated conductor is $32N^2$ and the root number is $-1$ because $N\equiv7\bmod8$. The attached pure-integer interval calculation gives
$$7.489<L'(E_{791},1)<7.642.$$
Hence the analytic rank is one; the Gross–Zagier–Kolyvagin theorem gives the stated algebraic rank. The small-congruent-number tables independently report rank one together with the point $G=(-784,-2940)$.

The complete rational torsion subgroup is $E_N[2]$. For example, at the good primes 3 and 19 the reduction orders are 4 and 20, since they are $3\bmod4$. Prime-to-residue-characteristic torsion injects at good reduction; these two orders bound the torsion order by four, and all four two-torsion points are rational. The standard two-descent character $P\mapsto[x(P)+N]$ takes values $1,N,2N,2$ on the four torsion points, including the derivative value $2N^2$ at the root $x=-N$. But $x(G)+N=7$, outside these four classes. As the character kills doubles, $G$ is an odd multiple of a free generator modulo torsion. The other descent character $P\mapsto[x(P)]$ takes values in $\{1,-1,N,-N\}$ on the torsion (the root value at zero is $-N^2$). Moreover $x(G)=-28^2$ has class $-1$. Therefore every nonzero rational abscissa on $E_N$ has square class in $\{1,-1,N,-N\}$, which excludes $7$.

The plus-sign slice already has points over every rational completion. Set $z=15v$ and clear the square denominator to obtain the genus-one quartic
$$y^2=113(112^2-z^4).$$
It has smooth good reduction outside $2,7,113$, so Hasse's bound and smooth lifting give a local point at every other prime. The rational change back to the affine chart can be arranged by avoiding finitely many boundary points in a local disk. At $2$ and $7$, $113$ is a unit square, so $z=0$ works. At $113$, $112\equiv-1\bmod113$ is a nonzero square, and any $113$-adic $z$ with $z^2=112$ gives $y=0$. A real point is immediate. Thus finite local screening alone cannot certify the hoped-for universal slicing step.

## Numerical certification

Run `python rank791.py`. The conductor and sign formula and the elliptic $L$-derivative formula yield
$$
L'(E_N,1)=2\sum_{m\ge1}\frac{a_m}{m}E_1(cm),\qquad
c=2\pi/\sqrt{32N^2},\qquad E_1(z)=\int_z^\infty e^{-t}\,\frac{dt}{t}.
$$
At a good prime the script computes $a_p$ by counting the cubic's quadratic residues, or uses $a_p=0$ for $p\equiv3\bmod4$. It sets $a_p=0$ at the additive reduction primes and uses the Euler recurrence at good primes. For $m\le12000$ the decreasing integrand in $E_1(cm)=\int_m^\infty e^{-cu}\,du/u$ is bracketed by Riemann sums of mesh $1/16$. Powers of $\exp(-c/16)$ are bounded using $1-u\le e^{-u}\le1-u+u^2/2$ and outward integer rounding. The omitted tail uses $|a_m|\le\tau(m)\sqrt m\le2m$ and $E_1(cm)\le e^{-cm}/(cm)$. No floating-point operation enters the asserted rational enclosure.

References: William Stein, *The Congruent Number Problem*, lecture notes, conductor and sign formula at https://www.williamstein.org/simuw06/notes/notes.pdf; SageMath elliptic $L$-series documentation, `deriv_at1`, https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/lseries_ell.html; Gross–Zagier and Kolyvagin, analytic-rank-one theorem for rational elliptic curves. An independent older computed table is at https://www.asahi-net.or.jp/~KC2H-MSM/ec/eca1/cong0.htm.
