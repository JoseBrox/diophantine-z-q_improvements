# Independent review of the 59-coordinate ordinary-abc quartic

## Conclusion and scope

The normalized construction in `build59.py` has an exact quadratic
compilation in 59 rational coordinates, including the input. Its 51
quadratic residuals have a sum of squares of degree four, integer content
one, and 873 coordinate monomials. The coefficient height for every positive
integer $B$ is

```math
\max\{22838305425411, B^2+4092\}.
```

The transfer from the retained 62-coordinate construction is valid under
ordinary rational $abc$ and the elliptic, formal comparison, trace-index,
simultaneous prime-pattern, and simultaneous-twist premises explicitly
retained in the subject paper. The proof gives every sufficiently large
odd $B$, with an ineffective sufficient threshold. The coefficient
height formula does not provide that threshold.

The translated-secant chart, shared detector and Laurent packing originate
in notes of **Gabe Conant with Astra 6.2**, audited in v78. The single
derivative quotient, derivative interpolation and ratio normalizer are the
subsequent v79 transfer.

This review checks the new transfer and its edge cases. It does not replace
the retained arithmetic premises by numerical evidence. The independent
checker certifies the exact algebra described below; the universal
valuation and existence arguments are mathematical proofs.

## Exact algebra and source equivalence

Run, from the repository root:

```text
python -B computation/variable_reductions_v79/abc/check59.py
```

The default invocation is read-only. It imports neither a builder nor an
earlier checker. Its dependencies are the pinned parent
`computation/coauthor_audit_v78/work_abc/small_gate62/primitive/quadrics.json`,
the four files in `quartic59`, and SymPy. It compares the result with
`independent59.json`. The optional `--write` regenerates that certificate
only after an intentional review.

The check has the following distinct parts.

1. It reconstructs the 31 nonunit retained physical equations directly in
   $\mathbb Q(\sqrt2)$, using the supplied physical labels and stated
   Laurent weights, and checks each up to its nonzero constant row
   multiplier. It checks the literal $cc^{-1}=1$ equation separately.
2. It verifies all 32 retained rows against the pinned parent after the
   declared coordinate relabeling, and independently constructs all 19
   new rows from the displayed mathematical formulas.
3. It derives $G,P,Q$ by exact polynomial differentiation, verifies the
   derivative converse and all new physical contact scalings, and checks
   the native pole input normalization.
4. It expands the complete sum of squares in SymPy, independently of the
   producer's hand-written sparse convolution, and compares every integer
   coefficient of every parameter-separated term.
5. It verifies the support, all 59 used coordinates, the coefficient-one
   $X^4$ term, the mixed coefficient profiles, the slope leading terms,
   the local normalizer identity, and the exact rational height constants.

The retained chart equations are unchanged. Thus all their tangent,
zero-ordinate, finite two-torsion difference, and reference-chart branches
have exactly the same algebraic meaning as in the parent. The arithmetic
interpretation of that complete chart remains a retained premise.

The first native pole has the physical-to-stored map

```math
D=c z_{42},\quad b=c z_{34},\quad e=c z_{35},\quad
u_0=c z_{36},\quad v_0=c z_{38},\quad p=z_{37},\quad q=z_{39}.
```

Its square helpers satisfy $p^2=c z_{40}$, $q^2=c z_{41}$.
Multiplying its three main rows by $c^2$ gives precisely

```math
e^2+bp^2=1,\qquad u_0v_0=e(1-b),\qquad u_0^2-v_0^2=bq^2.
```

The new pole-input row is $z_{34}=z_{33}^2$, where

```math
z_{33}=\tau,\qquad
b=c\tau^2=\frac{u g^2}{(1+u)^2},\qquad u=c^{-1}.
```

There is no extra factor $c^{-2}$ in this physical input. The contact
quotient $u$ and the native pole coordinate $u_0$ are different
quantities.

## Contact interpolation, guards and count

For the shifts

```math
\{-8,-7,-2,-1,3,4,5,6\},
```

the polynomial is

```math
G(t)=t^8-102t^6-144t^5+3009t^4+7200t^3
      -17308t^2-32976t+40320.
```

The shifts are distinct, nonzero, have sum zero, and no two have zero sum,
including a shift paired with itself. With $a=M^4$, $M\ge B\ge3$,
every pair sum $2a+r+s$ is at least $146$. Thus the two eight-contact
lists are disjoint before prime selection.

Set

```math
P=tG'-8G,\qquad Q=(4t^2-102)G'-32tG.
```

Both have degree at most six. Every power occurring in $G,P,Q$ is a
product of at most two among $1,t,t^2,t^4$. After imposing the two power
equations and the exact value equation, the two derivative equations give

```math
t(H-G')=0,\qquad (4t^2-102)(H-G')=0.
```

Their coefficients have the constant combination

```math
(4t^2-102)-4t\cdot t=-102.
```

Consequently $H=G'(t)$ at every rational point, including $t=0$.
There is no division by $t$, $x$, $y$, or $xy$, and no deleted
zero-coordinate fiber. This saves the two cubic-power coordinates.

Each of the ten stored contact coordinates has physical value $c$ times
its stored value. The derivative sum has physical value $c^2$ times its
stored value. The quotient row is exactly

```math
F_a+16cF=0,
\qquad F=G(x)G(y),\quad F_a=G'(x)G(y)+G(x)G'(y).
```

The unit equation gives $c\ne0$. If $F=0$, exactly one of $G(x)$,
$G(y)$ vanishes: both vanishing would force
$x+y=-(r+s)$, incompatible with $x+y=2M^4>16$. Since the roots of $G$
are simple, exactly one vanishing factor makes $F_a\ne0$, a
contradiction. If $F_a=0$, the quotient equation first gives $F=0$,
already excluded. Thus the system recovers

```math
u=-16F/F_a\ne0,
```

with no additional inverse registers.

The 44 retained coordinates and 15 new coordinates give 59 in total. The
new coordinates are $M,M^2$, ten contact coordinates, the derivative
sum, and the two ratio-normalizer helpers. The 32 retained plus 19 new
residuals give 51 equations. No assertion of algebraic independence is
needed for this census or for the sum-of-squares equivalence over
$\mathbb Q$.

## The ratio normalizer and its denominators

The physical normalizer is

```math
g=\frac{1+uD^2}{1+u^3D^2},\qquad
\tau=\frac{g}{1+c},\qquad b=c\tau^2.
```

In stored coordinates put $J_s=D_s^2=D^2/c^2$ and $\lambda=g/c$.
The cleared ratio equation is

```math
\lambda(c+J_s)=1+cJ_s.
```

If $c+J_s=0$, this equation forces $c^2=1$. The case $c=1$
would require the rational square $J_s=-1$, which is impossible. The
case $c=-1$ is $u=-1$. The derivative radical lower bound below
excludes $u=-1$ for every sufficiently large $B$, before either the
pole soundness argument or the conclusion that $X$ is integral is used.
Thus both $c+J_s$ and $1+c$ are automatically nonzero in the defining
range. Equivalently the physical denominator $1+u^3D^2$ is nonzero.

No inverse of $g$ is used in soundness. Its numerator is nonzero at each
consumed odd-valuation prime by parity; in the integer construction it is
nonzero because $c>0$ and $g\to1$ at the real preparation. The fiber
$D=0$ is allowed throughout and gives $g=1$.

The shared trace denominator also has an automatic guard. If
$\operatorname{Tr}W=0$, the equation
$D\operatorname{Tr}W=\operatorname{Nm}(W-1)$ would imply $W=1$ in
the field, contradicting $\operatorname{Tr}1=2$. This also excludes
$W=0$.

## Universal odd-valuation proof

Let $p$ be a prime, $\mu=v_p(u)$ odd, and $d=v_p(D)$, with
$d=+\infty$ permitted. When $d$ is finite, both
$\mu+2d$ and $3\mu+2d$ are odd and cannot equal zero. Hence

```math
v_p(g)=\min(0,\mu+2d)-\min(0,3\mu+2d).
```

For $\mu<0$, the first argument of the minimum is larger than the
second. Therefore $v_p(g)\ge0$ for every $d$, regardless of poles in
the actual auxiliary point coordinates. Since
$v_p(u/(1+u)^2)=-\mu$,

```math
v_p(b)=-\mu+2v_p(g)>0
```

is odd. This uniform conclusion is why the denominator $1+u^3D^2$ is
needed; the unnormalized expression $g=1+uD^2$ does not supply it.

For $\mu>0$, there are three intervals for $2d$.

| Interval | $v_p(g)$ | $v_p(b)$ |
|---|---:|---:|
| $2d>-\mu$ | $0$ | $\mu$ |
| $-3\mu<2d<-\mu$ | $\mu+2d$ | $3\mu+4d$ |
| $2d<-3\mu$ | $-2\mu$ | $-3\mu$ |

The endpoints cannot occur because $2d$ is even and $\mu$ is odd.
For $D=0$, the first case applies with infinite $d$.

The native pole equations exclude a negative odd valuation of $b$,
including all zero-coordinate cases. Indeed the first equation forces
$v_p(e)=0$: a negative valuation of $e^2$ is even, while a negative
valuation of $bp^2$ is odd, so they cannot cancel; the latter term must
have positive valuation if it is nonzero. Then the middle equation gives
$v_p(u_0)+v_p(v_0)=v_p(b)$, an odd integer. Their valuations cannot be
equal. The third equation then has a left side of even valuation and a
right side of odd valuation, a contradiction. If the right side is zero,
it would instead force equal valuations, again a contradiction.

The last interval is therefore impossible. In the middle interval the
odd integer $3\mu+4d$ must be positive. All surviving cases give

```math
d>-3\mu/4.
```

This proof is universal. The finite valuation grid in the checker is only
an additional regression check of the formula and inequality.

## Extraction from the shared detector

At a consumed good prime, $v_p(c)=-\mu$, with $\mu>0$ odd. If both
slot valuations $w_1,w_2$ of $W$ are negative, then

```math
v_p\operatorname{Nm}(W-1)=w_1+w_2,\qquad
v_p\operatorname{Tr}W\ge\min(w_1,w_2),
```

so $v_p(D)\le\max(w_1,w_2)$. This includes an inert prime, where the
two valuations coincide. If either slot is already integral there is
nothing to prove. In either case the preceding inequality for $D$
gives a slot with $v(W)>-3\mu/4$.

At that slot the four nonconstant terms in

```math
W=1+cC^4+c^2J^2-c^3\overline I^{\,4}-c^4\overline{K'}^{\,2}
```

have respective valuation classes $-\mu,-2\mu,-3\mu,0$ modulo four.
The even valuations of $J,K'$ are the retained reciprocal-abscissa
property. A negative minimum is consequently unique and cannot cancel.
Every one of these terms has valuation greater than $-3\mu/4$, giving

```math
v(C)>\mu/16,\quad v(J)>5\mu/8,\quad
v(\overline I)>9\mu/16,\quad v(\overline{K'})>13\mu/8.
```

All four raw tests are positive. A zero raw test has infinite valuation
and satisfies the same conclusion. The retained inverse-parameter
extraction theorem now gives local integrality of $X$ and
$X(m-X)\equiv0\pmod p$. No extra nontorsion, nontangent or nonzero
ordinate hypothesis has been introduced.

## Height argument and uniformity in the shift

The intermediate estimate proved in v63 is

```math
\log r^+_{\mathrm{odd},S}(u)
\ge (k-6-3\epsilon)\max\{h(x),h(y)\}
      -(2+\epsilon)h(M)-O(1).
```

Its proof precedes the optional replacement of the larger slot height by
half the product height, and never divides by $xy$. Thus it applies
here when $x=0$ or $y=0$. Its hypotheses are satisfied by the fixed
eight shifts and the nonzero contact values just checked. Its constant
and exceptional set depend on the fixed shifts, not on $B$.

Since $x+y=2M^4$,
$\max(h(x),h(y))\ge2h(M)-O(1)$. With $k=8$ and
$\epsilon=1/100$,

```math
\log r^+_{\mathrm{odd},S}(u)\ge\frac{193}{100}h(M)-O(1).
```

In particular $u=-1$, whose radical on the left is one, forces $h(M)$
bounded by a fixed constant. Since $M\ge B$, this proves the eventual
guard independently of all pole conditions.

For a nonintegral input, $X(m-X)\ne0$ because $m\in\mathbb Z$.
The extraction conclusion implies that the consumed radical divides its
reduced numerator, so

```math
\log r^+_{\mathrm{odd},S}(u)
\le2h(X)+\log(1+|m|).
```

The retained signed mixed-power estimate with
$\kappa=1001/1000$ gives

```math
h(X)\le\frac{2\kappa-1}{8-6\kappa}
             h(X^8+T_{\mathrm{sc}}^2)+O(1)
\le\frac{501}{997}h(M)+O(1).
```

The second inequality is uniform in positive integer $B$: adding $B$
to a nonnegative rational leaves its reduced denominator unchanged and
does not decrease the height. Also
$2h(T_{\mathrm{sc}})\le h(X^8+T_{\mathrm{sc}}^2)+8h(X)+O(1)$.
Together with the retained trace-index bound, this gives
$m^2=O(h(M)+1)$. The exact strict margin is

```math
\frac{193}{100}-2\frac{501}{997}
=\frac{92221}{99700}>0.
```

Consequently a nonintegral solution would bound $h(M)$ by a fixed
constant, whereas $h(M)\ge\log B$. This proves exclusion of all
nonintegral inputs for sufficiently large $B$.

## Integer completeness and the order of choices

Fix a nonzero integer $X$. The retained construction first fixes the
root difference $A=[X]R_0$, its scaled trace, $M$, and $a=M^4$.
It fixes bounded real and local neighborhoods for the remaining point
functions. Thus both eight-contact lists and all their collision values
are fixed before contact prime selection.

Clear the rational contact denominators and enlarge the **preparation**
set by their coefficient, denominator and collision primes. This is a
finite set depending on the chosen integer witness. It is separate from
the fixed exceptional set in the soundness height estimate. Use the
retained simultaneous prime-pattern theorem on the sixteen signed
linear forms, with finite avoidance and the same formal-index
refinements. For a sufficiently large real slope, the first eight forms
can be negated to have positive leading sign; this does not change their
prime support.

More explicitly, choose $D_0>0$ with $D_0^2(a+r)\in\mathbb Z$ for all
eight shifts and use the permitted prepared form

```math
z=\frac{N}{D_0^2L^2},\qquad
p_{r,\pm}=N\pm D_0^2(a+r)L^2.
```

The supplied sixteen primes give the exact factorization

```math
F=\frac{\prod_r p_{r,-}p_{r,+}}{D_0^{32}L^{32}}.
```

The eight minus signs from the quadratic factors cancel. This identity
accounts for every numerator prime of the contact product; it does not
assume that the subsequently chosen auxiliary points have no new
denominator primes.

At each selected simple contact exactly one linear factor has valuation
one and all other contact factors are units. The derivative identity
therefore gives $v_p(u)=1$. At the successful slot the retained
preparation gives $v(C),v(\overline I)\ge3$ and
$v(J),v(\overline{K'})\ge4$, so $W\equiv1$. At the other slot the
reciprocal products are units and the fourth term has the unique minimum
$-4$. Therefore $v_p(D)>0$, $g$ is a unit and $v_p(b)=1$.

Outside the finite preparation set, positive odd valuations of $u$
can only occur at these selected primes. For an integral slope at a
prime, $F,F_a$ are integral and a positive valuation of their quotient
requires a numerator factor of $F$. If the slope has valuation
$-h<0$, its contact product has valuation $-16h$, while its derivative
has valuation at least $-14h$, so $v_p(u)\le-2h<0$; cancellation in
$F_a$ can only decrease this quotient valuation further. The leading
factor 16 is a unit outside the preparation set. Thus a new denominator
prime cannot become an unprepared positive odd contact prime.

New **negative** odd valuations of $u$, including those introduced by
$F_a$, are harmless for every actual point denominator by the universal
ratio-normalizer proof. Their valuations of $b$ are positive odd. If
$v_p(u)$ is even, then $v_p(u/(1+u)^2)$ and hence $v_p(b)$ are even.
This last statement includes $v_p(u)=0$ and an arbitrarily deep
cancellation in $1+u$.

It remains to handle the finite preparation set and real infinity.
The exact leading terms are

```math
F=z^{16}+O(z^{14}),\qquad F_a=-16az^{14}+O(z^{12}),
\qquad u\sim z^2/a,\quad c\sim a/z^2.
```

They hold at real infinity and at every fixed nonarchimedean place as
the slope denominator is deepened. On the fixed point neighborhoods the
raw tests remain bounded, so

```math
W-1=O(c),\qquad \operatorname{Tr}W\to2,\qquad D=O(c^2).
```

The trace limit is nonzero also over $\mathbb Q_2$; its valuation is
eventually one, a fixed loss absorbed by increasing the depth. Writing
$D=c^2E$, with $E$ bounded locally, gives the exact identity

```math
g=\frac{1+c^3E^2}{1+cE^2}\longrightarrow1.
```

This bound is uniform on those fixed neighborhoods, so no control of
auxiliary denominators at subsequently discovered primes is assumed.

At the real place $c>0$ for sufficiently large slope, and
$b\sim c>0$ tends to zero. Thus $0<b<1$. At each fixed finite place,
$a=M^4$ is a rational square, so the leading valuation
$v_p(c)=4v_p(M)-2v_p(z)$ is even and can be made arbitrarily large.
The quotient $c/(a/z^2)$ tends to one. At two prescribe it to lie in
$1+8\mathbb Z_2$, ensuring that $c$ is a two-adic square. Prescribe
enough further depth to make $g,1+c$ units and $v_2(c)\ge4$. Then
$b=c(g/(1+c))^2$ is a two-adic square with $v_2(b)\ge4$. At the
other fixed places, the same preparation makes $v_p(b)=v_p(c)>0$
even.

All these are finitely many local and real conditions specified before
the selected prime choices, exactly as allowed by the retained
simultaneous prime-pattern premise. Every negative valuation of the
actual rational $b$ is now even, so its reduced denominator is a
square. The small-input pole lemma from v78 applies to this actual $b$:
it requires only $0<b<1$, a square reduced denominator, and the stated
two-adic square and depth. It imposes no additional congruence condition
on the odd numerator primes. Its simultaneous-twist premise is retained
without strengthening.

For $X=0$, the exact parent zero fiber has $H=2R_0$, $s=S$, $t=T$,
zero paired reciprocal quantities, and $h=t^2/(s-t)$. Its denominator
is nonzero since $\operatorname{Nm}(S-T)=7199/328$. It fixes the scaled
trace and hence $M$ before the slope choice. All raw tests vanish, so
$W=1,D=0,g=1$ and $b=c/(1+c)^2$. The same real and finite-place
preparation and small-input pole lemma apply. No extra input factor is
multiplied into the polynomial.

## Limits of this certificate

The proof and exact computation establish the reduction from 62 to 59
coordinates under the stated premises. They do not establish a new
unconditional Diophantine definition, prove rational $abc$, produce an
effective defining shift, or certify the retained group, prime-pattern,
trace-index or simultaneous-twist assertions computationally. They also
do not certify the discarded unnormalized intermediate constructions.

The universal parity argument above supplies the missing guarantee for
new negative odd derivative poles; its replacement by a finite search
would be insufficient.

## Reviewed source snapshot

The mathematical review above applies to the final manuscript
`papers/quartic_existence/single_derivative59_20261119_v79.tex`, with SHA-256

```text
5d35d232d518964499797d961d1f3fbfaa795c89fa3f0acb5fc999b6ff786266
```

The reviewed producer `build59.py` has SHA-256

```text
a47075c0ac60b90b225bcfbcb1596a4f00aac381bb31cb73bb4e2e30870d2d77
```

The exact coefficient and map file hashes are recorded in
`independent59.json`. The complete immutable review snapshot, including the
checker and this review, is recorded in `manual_review59.json`. These
pins record the reviewed files; they must not be rebound after a source
change without a new review.
