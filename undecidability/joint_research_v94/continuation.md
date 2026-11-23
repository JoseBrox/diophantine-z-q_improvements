# Contact spacing: a compatibility gap and an adaptive route

This is a research checkpoint, not a new variable-count claim. The proved
progression construction remains the one in
`undecidability/general_contact_v94/affine_contact_progressions.tex`.
The local calculations below identify a more specific next step and the
checks required before a new complete table can be claimed.

## Why fixed dyadic translations were not immediately justified

If every integer-witness contact list lay in one fixed subgroup
`2^(-L) Z_2`, translations `i/2^(L+e)`, with `2^e` larger than every
index difference, would separate the lists uniformly. This is the exact
fixed-place separation lemma already used for the ordinary-abc interface.

Such a bound looks plausible at first because the integer input label
`beta=51X^2+2504` has `v_2(beta)<=3`, and both general and specified
scalar normalizers satisfy `v_2(R_X) in {2,3}`. These facts follow directly
from the source formulas, including the odd numerator factors and the odd
denominators `1+149^2*r_X` and `1+25*r_X`.

However, the scalar construction makes the reference point formal at the
odd primes in the input-dependent scalar support. Its index must annihilate
the corresponding elliptic reduction orders. The retained interfaces give
no uniform bound on the powers of two dividing those orders. Prescribing
one bounded value of `v_2(h)` or `v_2(a)` therefore has an unresolved
compatibility condition with those odd-place requirements. The fact that
the place being prepared is odd does not remove the two-part of its
reduction order.

Accordingly, no fixed numerical dyadic offset, and no smaller complete
quartic count obtained from such offsets, has been accepted here.

## The coefficient algebra if fixed offsets were available

Write the common contact gauge as `rho`, with retained inverse `epsilon`.
For the general chart put

\[
 t=\lambda/\rho,\qquad u=(\lambda-1)^2,\qquad f=u^2.
\]

For fixed rational offsets `delta_i`, two additional registers

\[
 V=\rho t-1,\qquad A=uV
\]

would give affine replacements

\[
 \begin{aligned}
 t_i&=t+\delta_i\epsilon,\\
 u_i&=u+2\delta_iV+\delta_i^2,\\
 f_i&=f+4\delta_iA+6\delta_i^2u+4\delta_i^3V+\delta_i^4.
 \end{aligned}
\]

The two defining equations are quadratic. The old gauge guards and the
root square equation give `V^2=u`, so these formulas recover every omitted
square and fourth-power row. Every substitution is affine in the retained
registers. This is a valid algebraic recipe; completeness requires the
missing fixed-offset arithmetic statement.

In the specified chart let `A_0=22t-3`, `u=rho*A_0^2`, and
`f=rho*A_0^4`. Registers `V=rho*A_0`, `A=u*A_0` would instead give

\[
 \begin{aligned}
 t_i&=t+\delta_i,\\
 u_i&=u+44\delta_iV+484\delta_i^2\rho,\\
 f_i&=f+88\delta_iA+2904\delta_i^2u
        +42592\delta_i^3V+234256\delta_i^4\rho.
 \end{aligned}
\]

Again the two register definitions and all transformed rows remain
quadratic. This calculation alone does not provide arithmetic completeness.

## Adaptive spacing from an already stored scalar coordinate

A more promising approach allows the two-adic depth of the reference to
grow with the annihilation orders. Let `H_2=v_2(h)>=6`, choose the relative
scalar depth `v_2(a/h)=8`, and put `K=v_2(a)=H_2+8`. Here `a` is the
scalar label of the integer-defining interface, not the Pell parameter
of the outer Jones source.

The relevant source formulas are in
`undecidability/papers/shared_quartic_checkpoint.tex` (ordered joint scalar
preparation), `papers/quartic/scalar_point163_179_20261120_v82.tex`
(physical normalized scalar and secant charts), and
`papers/quartic_existence/paired_contact56_20261119_v81.tex`
(the elementary two-adic formal-parameter computation on the same curve).

The curve is `E: y^2=x^3-(11-6 sqrt(2))x`, with `P_0=2R_0`.
For every nonzero even integer `n`, the proved local computation gives

\[
 v_2(z([n]R_0))=v_2(n)+\tfrac12,\qquad
 v_2(x([n]R_0))=-2v_2(n)-1,
\]

and `n^2 Tr(x([n]R_0))` is in `Z_2`.

### The relative depth and the actual scalar pole

Write `f=1/x(H)`, `Z=2z(Q_2)/z(H)`, `L=Z^2/R`,
`Jhat=f^2+L`, and

\[
 \widehat\tau=\frac{N(Jhat)}{\operatorname{Tr}(L)},
 \qquad \tau=\widehat\tau/R^4.
\]

For `r=v_2(R)` in `{2,3}`, the proposed depth choice gives
`v_2(Z)=8`, `v_2(L)=16-r`, and `v_2(f^2)=4H_2+6`.
The latter is strictly greater than `v_2(L)`. In the basis
`1,sqrt(2)`, the real component of `Z^2` has valuation exactly 16:
the square of the real component has valuation 16 and twice the
square of the imaginary component has valuation at least 17.
Consequently

\[
 v_2(\operatorname{Tr}(L))=17-r,
 \qquad v_2(\tau)=15-5r.
\]

The actual scalar pole input `R(R+9792)*tau^2` therefore has valuation
`30-8r`, namely 14 or 6. Its square class is unchanged, since
`1+9792/R` is a two-adic square. Thus the proposed relative depth
satisfies the scalar preparation at two independently of `H_2`.

The remaining compatibility task is to combine this exact relative
depth with every odd-place annihilation and precision congruence in
the ordered preparation. Allowing `H_2` to exceed the two-parts of
the finitely many relevant reduction orders appears to resolve the
obstruction that defeated a fixed absolute depth. This join must be
checked against the full retained recurrence interface before use.

### Contact valuation bounds

For `a in 6Z` with `K=v_2(a)>=2`, use the source Lucas sequence

\[
 U_0=0,\quad U_1=1,\quad
 U_{n+1}=(a+1)U_n-U_{n-1},\qquad
 t_L=U_a,\quad b_L=U_{a-1}/(a-1).
\]

The exact valuations are

\[
 v_2(t_L)=2K+1,\qquad v_2(b_L-1)=K.
\]

For the first identity, `U_3=a(a+2)` has valuation `K+1`.
The trace sequence has `V_3=(a+1)^3-3(a+1)=2 mod 4`;
the addition and doubling identities then give
`v_2(U_(3m)/U_3)=v_2(m)`. Take `m=a/3`.
For the second identity, put `n=a-1=6l-1` and regard `U_n(P)`
as a polynomial in its recurrence coefficient `P`. At `P=1`,
`U_n(1)=-1` and `U_n'(1)=-2l`, so Taylor expansion at `P=1`
gives `U_n(a+1)= -1 mod 2^(K+1)`. Since `a-1` is odd,
`v_2(U_n(a+1)-(a-1))=K` proves the assertion.

The point labels are `2 beta_i`, `a`, `t_L`, and `(b_L-1)/2`.
Their two-adic valuations are at most 4, exactly `K`, exactly
`2K+1`, and exactly `K-1`, respectively. The displayed formal
calculation consequently puts every general contact position in

\[
                       2^{-(4K+4)}\mathbb Z_2.
\]

For the specified interface, both rational components of `x(Q_3)`
have valuation at least `-4K-3`; the two physical shifts are
`13+S_0/2` and `17+(S_0-S_1)/2`, where
`S_0+S_1 sqrt(2)=sum x(Q_i)`. They yield the same lower bound
`-4K-4`. All fixed contact constants have valuation at least `-1`.

### A sufficiently deep existing coordinate

Let `rho_sec` be the normalized secant intercept for the scalar
numerator points `U_2=[h]Q_2`, `V_2=[h-1]Q_2`.
Their formal parameters have valuations `H_2+K+1/2` and
`K+1/2`. In the secant formula

\[
 \rho_{\rm sec}
 =\frac{y(U_2)x(-V_2)-y(-V_2)x(U_2)}{x(-V_2)-x(U_2)},
\]

the numerator terms have distinct valuations, differing by `H_2`,
and the denominator terms differ by `2H_2`. Hence

\[
 v_2(\rho_{\rm sec})=-H_2-3K-\tfrac32.
\]

The existing common scalar register is `r_*=Z*rho_sec`. If
`r_*=r_0+r_1 sqrt(2)`, the half-integral valuation forces

\[
 v_2(r_1)=-2H_2-2K-2.
\]

The candidate adaptive spacing is therefore

\[
                   D=2^{-24}r_1.
\]

With `K=H_2+8`, it has valuation `-4H_2-42`, while the contact
bound is `-4H_2-36`. For any distinct original block indices in
`{0,...,11}`, `v_2(i-j)<=3`, so `v_2((i-j)D)` is strictly below
that contact bound. The fixed-place separation argument would then
separate all the lists. The spacing is rational and fixed before
contact primes are selected. Its real sign is irrelevant to this
valuation argument and to the later large-slope asymptotics.

The coordinate `r_1` is named `common_scalar_r_imag` in the general
table and `int_b_113` in the specified table. Thus it is already
available; no new extraction coordinate is needed for the candidate.

## The remaining complete-table work

In the specified table the free common spacing can be replaced by
`2^(-24)*int_b_113` by affine substitution.

For the general table, the stored root contact coordinate represents
`lambda/rho`. Its complete occurrence audit finds only the aggregate
rows, its root square row, and the common mixed-square row. Reinterpret
that one coordinate as the physical `lambda`, substitute old
`t=epsilon*lambda` and old `d=epsilon*D`, and use the retained gauge
inverse to replace

\[
 \begin{aligned}
 2\rho(t+id)&=2(\lambda+iD),\\
 u&=(\lambda-1)^2,\\
 v&=D(\lambda-1),\qquad w=D^2.
 \end{aligned}
\]

These equations are quadratic. The four common fourth-power
coefficient rows remain unchanged. Exact complete coefficient
transformation, guard reconstruction, deterministic rebuilding,
independent verification, and a fresh audit of the ordered arithmetic
choice remain necessary. Until those are completed, this file records
a route and its precise obligations, not a revised result census.
