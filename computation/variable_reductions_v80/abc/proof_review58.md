# Independent review of the 58-variable ordinary-abc quartic

## Result and scope

The new construction has **58 rational variables, including its input,
and 50 integral quadratic residuals**. Their sum of squares has degree
four, content one, 867 coordinate monomials, and 870 terms when powers of
the coefficient parameter are kept separate. For every positive integer
$B$, its coefficient height is

```math
\max\{22838305425411,\ B^2+4091\}.
```

The defining theorem holds for every sufficiently large odd $B$, with an
ineffective sufficient threshold, under ordinary rational $abc$ and the
retained elliptic, formal-comparison, all-point trace, and prime-pattern
inputs. Native-pole completeness uses the precise square classes in
[Burungale, arXiv:2611.16130v1, Theorem B](https://arxiv.org/html/2611.16130v1).
It does not assume the class-one extension used explicitly as an additional
premise by the historical 59-variable construction.

The shared chart and detector originate in notes of **Gabe Conant with
Astra 6.2**. The derivative transfer is the subsequent v79 work, and the
one-helper normalizer is the v80 improvement.

The review has two different parts: exact computation establishes the
specified finite identities and coefficients; the argument below checks
the logical transfer and its quantified arithmetic hypotheses. Neither
part independently proves $abc$ or the cited arithmetic theorems.

## Source maps, complete coefficients, and derivative boundaries

Run from the repository root:

```text
python -B computation/variable_reductions_v80/abc/check58.py
```

This invocation is read-only. The checker imports no producer or earlier
checker. Its physical reconstruction of the unchanged v78 rows is adapted
explicitly from the audited v79 checker; that inheritance is recorded,
not represented as a new independent discovery. It independently derives
the changed equations, their physical interpretation, and the two-curve
pole identities. SymPy expands all 50 squares, independently of the
producer's sparse convolution, and compares every coefficient with the
published table.

The checker verifies 47 rows unchanged from v79, and the three new rows

```math
\alpha=c^{-1}+D_s^2,\qquad
\tau(1+\alpha)=\alpha,\qquad b_s=7\tau^2.
```

The physical values are $D=cD_s$, $u=c^{-1}$, and $b=cb_s$. Thus

```math
\alpha=u+u^2D^2,\qquad
b=7c\tau^2=\frac7u\left(\frac{\alpha}{1+\alpha}\right)^2.
```

The five native-pole rows retain
$e=ce_s$, $u_0=cu_s$, $v_0=cv_s$, $p=p_s$, $q=q_s$,
$p^2=cP_s$, and $q^2=cQ_s$. They give exactly

```math
e^2+bp^2=1,\qquad u_0v_0=e(1-b),\qquad u_0^2-v_0^2=bq^2.
```

In particular the factor seven belongs to the physical input; there is
no additional unstated power of $c$.

The polynomial

```math
G(t)=t^8-102t^6-144t^5+3009t^4+7200t^3
      -17308t^2-32976t+40320
```

has the eight stated distinct shifts, with zero sum and no opposite
pair. The exact identities
$P=tG'-8G$ and $Q=(4t^2-102)G'-32tG$ have degree at most six.
After recovering the stored powers and value of $G$, the two derivative
rows imply

```math
t(H-G')=0,\qquad(4t^2-102)(H-G')=0.
```

Their coefficients generate the nonzero constant $-102$, so $H=G'$ also
at $t=0$. Neither contact coordinate is divided out.
For $B\ge3$, the positive midpoint $x+y=2M^4$ prevents both contact
polynomials from vanishing. A single zero makes $F_a$ nonzero because
the corresponding root is simple; the quotient equation then excludes
that zero. Thus the compiled source recovers $F F_a\ne0$ without a
new inverse coordinate.

Every monomial and all 58 coordinates occur. The $X^4$ coefficient is
one. The only mixed coefficient profiles are $B^2+4091$, $8B+1$,
and $2B+1$. The identities

```math
B^2+4091-(8B+1)=(B-4)^2+4074,
\qquad B^2+4091-(2B+1)=(B-1)^2+4089
```

prove the asserted maximum for every positive $B$, together with the
checked maximum of the fixed coefficients. This algebraic statement
does not identify a sufficient defining value of $B$.

## Universal valuation argument and zero cases

First suppose $v_p(b)$ is negative and odd. In the first native equation,
the valuations of $e^2$ and $bp^2$ have opposite parity. They cannot
cancel, so both are integral; the second term is either zero or has
positive valuation, and $e$ is a unit. The middle equation forces
$u_0,v_0\ne0$ and
$v_p(u_0)+v_p(v_0)=v_p(b)$, an odd integer. Their valuations differ.
Consequently $u_0^2-v_0^2$ has finite even valuation, whereas $bq^2$
has odd valuation or is zero. This contradiction covers every prime,
including two, and every zero-coordinate boundary.

Now let $p\ne7$ and let $\mu=v_p(u)$ be odd. Put $d=v_p(D)$, with
$v_p(0)=+\infty$. The two summands of $\alpha$ have respective
valuations $\mu$ and $2\mu+2d$, of opposite parity. Therefore

```math
A:=v_p(\alpha)=\min\{\mu,2\mu+2d\}.
```

If $\mu<0$, then $A<0$, so $v_p(\tau)=0$ and $v_p(b)=-\mu>0$.
This is uniform in all actual point denominators, including denominator
primes discovered only after prime selection.

If $\mu>0$, both $A<0$ and $A=0$ would give a negative odd valuation
of $b$. In the latter case an arbitrarily deep cancellation in
$1+\alpha$ only makes $v_p(\tau)$ smaller. Thus $A>0$ and the native
obstruction forces $-\mu+2A>0$. It follows that

```math
A>\mu/2,\qquad d>-3\mu/4.
```

These are universal case arguments. The finite valuation grid in the
checker is supplementary regression evidence only. It explicitly includes
the $A=0$ denominator-cancellation cases.

The gate itself excludes $\alpha=-1$, since its residual would equal
one. The branch $D=0$ is retained and gives
$\tau=u/(1+u)$ and $b=7c/(1+c)^2$. The abstract branch $\alpha=0$
is not removed by a fictitious guard: it would imply
$u=-(uD)^2$. For sufficiently large $B$, the derivative-height estimate,
before using any pole conclusion, supplies a positive odd valuation of
$u$ and excludes this branch. No denominator of the new normalizer
depends on that eventual argument.

## Detector extraction and uniform heights

The cleared equation $D\operatorname{Tr}W=\operatorname{Nm}(W-1)$
forces $\operatorname{Tr}W\ne0$, since otherwise $W=1$ in the field
$\mathbb Q(\sqrt2)$ while its trace is zero. If both slot valuations of
$W$ are negative, the norm and trace inequalities give
$v_p(D)\le\max(v_1(W),v_2(W))$. Otherwise a slot is already integral.
There is therefore a slot with $v(W)>-3\mu/4$. The argument also covers
an inert prime, where the two slots have the same valuation.

The four nonconstant detector terms have distinct classes modulo four.
This uses the even valuations of the reciprocal-abscissa products
$J,K'$. A negative minimum is unique, so every term has valuation greater
than $-3\mu/4$. Hence

```math
v(C)>\mu/16,\quad v(J)>5\mu/8,\quad
v(\overline I)>9\mu/16,\quad v(\overline{K'})>13\mu/8.
```

Zero tests satisfy these inequalities with infinite valuation. The exact
parent extraction theorem applies, including tangent fibers, zero
ordinates, and finite two-torsion differences, and gives local
integrality of $X$ and $X(m-X)\equiv0\pmod p$.

The v63 derivative proof gives the intermediate estimate in
$\max(h(x),h(y))$ before replacing that height by a bound involving
$xy$. It remains valid when one slot is zero: one may choose the larger
height slot first, and $G(0)\ne0$. Its multiple-contact estimate uses the
squarefree homogeneous form
$AB\prod_j(2q_jA^4+p_jB^4)$ and loses $(2+\epsilon)h(M)$, not a
factor four more. The polynomial and its constants depend on the fixed
shifts, not on $B$.

Together with $x+y=2M^4$, $\epsilon=1/100$ gives
$\log r^+(u)\ge(193/100)h(M)-O(1)$. The unchanged signed mixed-power
bound gives $h(X)\le(501/997)h(M)+O(1)$. The strict margin is
$92221/99700>0$. The all-point trace-index bound in v65, including its
separate treatment of the difference $(0,0)$, then bounds $m$ whenever
$X\ne0,m$. This contradicts $h(M)\ge\log B$ for sufficiently large
$B$. Excluding seven changes only the fixed exceptional set and constants.

## Exact prime-pattern and CRT quantifiers

The required prime statement is explicitly available for every fixed
finite list in
[Sun, arXiv:2610.20691v3, Theorem 4.1](https://arxiv.org/html/2610.20691v3).
It permits distinct integral coefficients, prescribed divisibility of the
square-denominator parameter, and arbitrary fixed lower bounds for the
primes and slope. Its Gaussian ray conditions and cross-order coprimality
are the ones used by the retained parent. No bound uniform in the number
of coefficients or their sizes is required here.

The logical order of the completeness choices is as follows.

1. Fix the integer input $n\ne0$, its root difference $[n]R_0$, and the
   resulting scaled trace, $M$, and $a=M^4$.
2. Choose bounded real and finite-place neighborhoods of the required
   point functions, avoiding their poles. Fix the associated congruence
   progression for the shared index, as in v65. Enlarge the temporary
   preparation set by every coefficient, denominator, and collision prime
   of the now-fixed contact positions, and by the numerator and denominator
   primes of $a$.
3. Choose $D_0$ clearing the sixteen coefficients
   $\pm D_0^2(a+r)$, and prescribe enough denominator depth and a real
   slope bound for all these fixed neighborhoods. The coefficients are
   distinct because $a$ exceeds the fixed contact diameter.
4. Apply the prime theorem once to this fixed list and preparation data.
   Refine the shared elliptic index on the compatible CRT progression,
   retaining the chosen finite-place neighborhoods and real component.

The arithmetic-dependencies paper v8, Section 2, states the relevant
deductions explicitly. Dividing the two reduction orders by four gives
coprime cross-sign annihilation moduli. Their odd parts avoid the fixed
progression modulus; the only remaining compatibility is the existing
power-of-two condition on the chosen index. At seven the prescribed
Gaussian residue gives both adjacent norms nonzero modulo seven, even
though seven is omitted from the theorem's odd avoidance modulus. The
parent halving lemma puts $R_0$ in the doubled reduction subgroups, so
these divided orders are valid annihilators. Finally the compact-group
progression lemma retains real returns after the compatible finite
congruences are imposed. This is the parent deduction, not an extra
approximation assumption for the new detector.

With $z=N/(D_0^2L^2)$ the sixteen distinct prime values give

```math
F=\frac{\prod_r
 (N-D_0^2(a+r)L^2)(N+D_0^2(a+r)L^2)}{D_0^{32}L^{32}}.
```

At a selected prime exactly one factor vanishes simply, so $v_p(u)=1$.
The successful slot has the unchanged error depths at least three and
reciprocal-product depths at least four. At the other slot the last
detector term has the unique minimum $-4$. Thus $v_p(D)>0$ and
$v_p(\alpha)=v_p(\tau)=v_p(b)=1$.

At an unselected prime outside the temporary set, an integral slope makes
$F$ a unit and $F_a$ integral, hence $v_p(u)\le0$. A nonintegral slope
gives $v_p(u)=2v_p(z)$ from the leading terms
$F=z^{16}+O(z^{14})$ and $F_a=-16az^{14}+O(z^{12})$.
At the temporary fixed places, sufficiently deep denominators give
$v_p(u)=2v_p(z)-v_p(a)$, which is even since $a=M^4$.
This accounts for every positive odd valuation of $u$; no unspecified
auxiliary denominator is assumed to have been fixed in advance.

The one-helper lemma handles every negative odd valuation outside seven,
and even valuations of $u$ give even valuations of $b$ there. At fixed
places, bounded point neighborhoods give $D=O(c^2)$. Writing $D=c^2E$
with bounded $E$ gives the exact formula

```math
\tau=\frac{1+c^3E^2}{1+c+c^3E^2}\longrightarrow1.
```

At two, $c/(a/z^2)$ may be made to lie in $1+8\mathbb Z_2$ and
$v_2(c)$ arbitrarily large positive even; hence
$b\in7\mathbb Q_2^{\times2}$ and $v_2(b)\ge4$.
At seven, $v_7(b)=1+v_7(c)>0$. All negative valuations of $b$ are
therefore even. Real positivity and smallness follow already from
$u>0$, $\alpha\ge u$, and $0<\tau<1$, giving $0<b<7/u$.

## Exact match to the published native-pole theorem

Write a prepared input as $b=A/Q^2$ in lowest terms, with
$0<A<Q^2$. The two-adic assumptions give odd $Q$, even $v_2(A)\ge4$,
and odd normalized unit class seven. If $\beta,\eta$ are the positive
squarefree parts of $A,Q^2-A$, then

```math
\beta\equiv7\pmod8,\qquad \eta\equiv1\pmod8,\qquad
\gcd(\beta,\eta)=1.
```

At an odd prime dividing $\beta$, $1-b$ is a unit congruent to one;
at an odd prime dividing $\eta$, $b$ is such a unit. Removing rational
squares proves exactly the mutual local-square hypotheses of Theorem B.
The theorem permits $\eta=1$.

That theorem supplies a positive squarefree parameter $r\equiv5\pmod8$
and points in the positive abscissa class $\beta$ on $E_r,E_{r\eta}$.
Their ordinates cannot vanish: the positive nonzero two-torsion
abscissas have class five at two, not seven. Scaling the second point
using $1-b=\eta d_0^2$ gives points
$(ba_1^2,y_1)$ and $(ba_2^2,y_2)$ on $E_r,E_{r(1-b)}$.
The source formulas are verified symbolically against both curve
equations in the independent checker. They give the three native equations
with all divisions nonzero. No density or avoidance conclusion beyond
these two points is required for the quartic source.

The exact prepared example

```math
(b,e,p,u_0,v_0,q)
=(112/841,\ 3/4,\ 29/16,\ 27/29,\ 81/116,\ 27/16)
```

also checks the native equations in the required class. It is only an
identity regression example, not an asserted defining contact fixture.

## Input zero and certification limits

The retained zero-input chart takes $H=2R_0$, $s=S$, $t=T$, and zero
paired reciprocal outputs, with $h=t^2/(s-t)$.
The parent exact norm $\operatorname{Nm}(S-T)=7199/328$ excludes its
only displayed division. The trace and $M$ are fixed before contact
selection. All tests vanish, so $W=1$, $D=0$, and
$b=7c/(1+c)^2$. The same preparations and the proved native converse
supply a rational zero; no extra input factor is used.

The exact computation does not prove the arithmetic inputs, produce an
effective defining threshold, or establish a global minimum for the
number of variables. The present review finds the new transfer valid
with its stated premises and complete zero-fiber treatment. The separate
25-, 165-, 180-, and unrestricted-degree 11-variable counts are not reduced
by this certificate.

The final immutable source hashes are recorded in `manual_review58.json`;
they must not be rebound without another review of every changed source.
