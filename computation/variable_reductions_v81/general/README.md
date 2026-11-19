# A two-term scalar detector and its remaining quadratic-encoding problem

This checkpoint is based on notes of **Gabe Conant with Astra 6.2**. It
proves a local scalar-detection lemma and an exact change of coordinates
in the native pole equations. It does **not** give a smaller defining
quartic. The established general counts remain **165 and 180**.

The retained scalar and point conventions are those of
`papers/quartic/shared_product_audit_20261119_v78.tex` and
`papers/quartic/quartic193_20261117_v74.tex`. The only pole input used in
the local implication below is the existing prohibition of negative odd
valuations, at primes outside its stated exceptional set. This package
does not establish that arithmetic input independently.

## 1. A universal local implication

Let $K=\mathbb Q(\sqrt2)$, let $R>0$ be rational, and let

```math
 Z\in K,\qquad f\in K^\times,\qquad
 J=\frac{Z^2}{R^5}+\frac{f^2}{R^4},\qquad
 \tau=\frac{N_{K/\mathbb Q}(J)}{\operatorname{Tr}_{K/\mathbb Q}(J)},
 \qquad b=R(R+9792)\tau^2.
```

At both real embeddings, $J$ is strictly positive. Thus its norm,
trace, and $\tau$ are nonzero, and $b>0$. This includes $Z=0$.

**Lemma.** Let $p\nmid 2\cdot9792$, let
$\mu=v_p(R)>0$ be odd, and suppose that $b$ does not have negative
odd $p$-adic valuation. There is a valuation slot $w$ of $K$
above $p$ for which

```math
                 v_w(Z)>\frac{9\mu}{4},\qquad
                 v_w(f)>\frac{7\mu}{4}.
```

Here valuations are normalized by $v_w(p)=1$; the two slots are
counted with multiplicity at an inert prime, and $v_w(0)=+\infty$.

**Proof.** Since $p\nmid9792$,

```math
 v_p(b)=\mu+2v_p(\tau)
```

is odd. The assumed obstruction makes it positive, so
$v_p(\tau)>-\mu/2$. If $w_1,w_2$ are the two valuations of $J$,
the trace inequality gives

```math
 v_p(\tau)=w_1+w_2-v_p(\operatorname{Tr}J)
                         \le\max(w_1,w_2).
```

Choose a slot where $v_w(J)>-\mu/2$. The two finite summand valuations
in $J$ are

```math
              2v_w(Z)-5\mu\quad\hbox{and}\quad2v_w(f)-4\mu.
```

The first is odd and the second is even. They cannot tie; if $Z=0$,
only the second is present. Therefore each present summand has valuation
greater than $-\mu/2$. Rearranging proves both inequalities. No
assumption on the parity of $v_w(f)$ was needed. $\square$

For the intended application, $f=f(H)=1/x(H)$ and
$Z=2z(Q_2)/z(H)$. The lemma controls the quotient and the reference
point at the **same** slot. Thus it supplies the local inequalities
needed by the existing scalar formal-logarithm argument; it does not
replace them by absolute depths of unrelated numerator points.

## 2. Real bounds and a precise local preparation condition

If $R\ge1$, $|Z^{(i)}|\le M_Z$, and
$|f^{(i)}|\le M_f$ at both real embeddings, put
$A=M_Z^2+M_f^2$. Then

```math
 0<J^{(i)}\le A R^{-4},\qquad
 0<\tau\le\frac{A}{2R^4},\qquad
 0<b\le\frac{9793A^2}{4R^6}.
```

The middle inequality follows from $xy/(x+y)\le(x+y)/4$ for
positive $x,y$. These are uniform bounds on the existing fixed real
neighborhoods.

Trace cancellation must be addressed in a converse. The following
explicit sufficient condition isolates that issue. At a fixed prime,
suppose there is $\lambda\in\mathbb Q^\times$ such that, in both
slots,

```math
 Z=\lambda(1+\epsilon_w),\qquad v_w(\epsilon_w)\ge h,
 \qquad v_w\left(\frac{R f^2}{\lambda^2}\right)\ge h,
 \qquad h\ge2.
```

Then $J=\lambda^2R^{-5}(1+\eta_w)$, with
$v_w(\eta_w)\ge h$. Its norm is $\lambda^4R^{-10}$ times a unit,
and its trace is $2\lambda^2R^{-5}$ times a unit. Consequently

```math
                 v_p(\tau)=2v_p(\lambda)-5v_p(R)-v_p(2).
```

This statement also covers $p=2$, because $h\ge2$ makes
$(\eta_1+\eta_2)/2$ integral of positive valuation. It is a
sufficient **local pattern**, not a proof that the required global
elliptic witnesses exist. A full converse must realize such patterns
simultaneously with the real conditions, the original point guards, and
the later reference progression. The prospective choice is
$\lambda=a/h_H$, using the actual formal-logarithm quotient and
choosing its depth strictly below that of the reference contribution.
That ordered realization has not been promoted to a defining theorem
in this package.

## 3. An exact homogeneous chart for the native pole

Write $d=9792$. The native equations are

```math
 \begin{aligned}
 3e^2-34e-289+17bp^2&=0,\\
 e(17-b)-17uv&=0,\\
 u^2+34uv-867v^2-17bq^2&=0,
 \end{aligned}
 \qquad b=R(R+d)\tau^2.
```

For $\tau\ne0$, define

```math
 \sigma=\tau^{-1},\quad B=b/\tau,\quad
 (E,U,V,P,Q)=(e,u,v,p,q)/\tau,\quad
 P_2=p^2/\tau,\quad Q_2=q^2/\tau.
```

They satisfy the quadratic equations

```math
 \begin{aligned}
 \tau\sigma&=1,&B\sigma&=R^2+dR,\\
 \sigma P_2&=P^2,&\sigma Q_2&=Q^2,\\
 3E^2-34E\sigma-289\sigma^2+17BP_2&=0,\\
 E(17\sigma-B)-17UV&=0,\\
 U^2+34UV-867V^2-17BQ_2&=0.
 \end{aligned}
```

Conversely these equations recover
$b=\tau B$ and $(e,u,v,p,q)=\tau(E,U,V,P,Q)$, and give exactly
the original equations and input. Each of the three displayed native
residuals is multiplied by $\sigma^2$. The first row itself guards
$\tau$ and $\sigma$; none of $e,u,v,p,q$ is inverted.
Thus all zero auxiliary-coordinate cases are included.

## 4. The exact remaining encoding problem

Set $\widehat J=R^4J$ and $\widehat\tau=R^4\tau$. Using the
already stored field square $f^2$, the two field equations

```math
 R\widehat J=Z^2+Rf^2,\qquad
 \widehat\tau\operatorname{Tr}(\widehat J)=N(\widehat J)
```

have quadratic component expressions. However the inverse relation in
the homogeneous pole chart becomes

```math
                         \widehat\tau\sigma=R^4.
```

Introducing the shared register $S_R=R^2$ makes its right side
$S_R^2$, which is quadratic, but retains precisely the register
whose removal is sought. Omitting this relation loses the prescribed
pole input. Replacing $R^4$ by $R^2$ weakens the quotient bound
to $v_w(Z)>5\mu/4$, which does not preserve the existing scalar
height argument and its third powers of the contact radical.

No complete input-preserving quadratic encoding below the current
counts has been obtained here. The next concrete task is to remove this
remaining fourth-power relation by a valid reassociation with the point
or pole equations, or to find a quadratic point chart retaining the
scaled quotient $Z/R$ without requiring its own $R^2$ register.
Every downstream equation and every zero fiber would then have to be
checked before claiming a smaller defining polynomial.

## Reproduction and scope of the certificate

Run, from the repository root:

```sh
python -B computation/variable_reductions_v81/general/check.py
```

The checker imports no construction producer. It verifies the rational
coordinate identities in both directions, the rescaled norm/trace
identities, and the exact parity and linear identities used in the
universal valuation proof. It compares its result with the immutable
`independent.json`; its default invocation writes no files. The
certificate is not a finite-prime substitute for the proof, a global
completeness certificate, or a new polynomial census.
