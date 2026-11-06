# Independent audit of the 855-variable presentation

## Result and scope

The independent checker `verify_compact_polynomial.py` passes on circuit
SHA-256 `6a1174891dccdd55bfc4cb6e7486cca2a4fde99ee8a755adaac0174f370da55b`.
It imports no producer code. Its exact checks establish the DAG's integer
polynomial syntax, variable and finite-branch inventories, the sum-of-squares
identity, coverage of every saved equation denominator by the common guard,
and the stated degree and coefficient-norm upper bounds. Its separate direct
formula evaluator agrees with all 297 rational residuals at six reproducible
finite-field samples. Those samples are consistency checks, not proofs of
identities or of the source arithmetic theorem.

The algebraic review below explains why the source-to-formula transformations
preserve rational solutions. This audit is conditional on the original source
system and the separately proved anchor replacement; it does not independently
establish that the source defines the integers. No claim about global optimality
or exact expanded degree or height is made.

Run from the repository root:

```sh
python3 research/optimization/verify_compact_polynomial.py
```

The complete receipt is `verification-855.json`.

## Exact structural results

There are 855 rational coordinates: the input, 633 point coordinates, three
anchor coordinates, three proxy coordinates, one root approximation, 210 pole
coordinates, one common coordinate denominator, two contact coordinates, and
one inverse for the common nonzero guard. Thus there are 854 existential
witnesses.

Each branch is exactly the sum of the squares of the 297 saved rational
equation numerators and the square of `inverse * guard_product - 1`.
There are 1,681 recorded nonzero numerators and 1,602 distinct syntactic factors
in their product after repeated factors and nonzero integer units are removed.
Every saved rational equation denominator is a product of such factors and
nonzero integer units. Therefore clearing denominators loses no information
when the guard equation holds. Over the rationals the branch polynomial is
zero precisely when all 298 squared expressions are zero.

The two formal parameters denote finite integer choices, not additional
quantified variables. Their sets are `j = 0,...,211` and the 256 signed
squarefree products of `2,3,5,7,11,13,17`. Their product gives 54,272 branches.
For a finite product over a field, vanishing is equivalent to vanishing of one
factor. Sharing the 855 variable names between the factors expresses the
required finite disjunction without extra coordinates.

Independently recomputed bounds are

\[
\deg P\le 31\,785\,384\,984\,576,
\qquad
H(P)\le\|P\|_1\le 2^{371\,648\,804\,230\,144}.
\]

Here the degree and binary logarithm bounds for one branch are 585,668,208
and 6,847,892,177. The checker uses `deg(fg) <= deg(f)+deg(g)`,
`||fg||_1 <= ||f||_1 ||g||_1`, and the triangle inequality for sums.
An addition of `k` terms adds `ceil(log2(k))` to the largest available binary
norm bound. Fixed parameter bounds are taken from their actual finite sets.
The full-product bounds are the branch bounds multiplied by 54,272.

## Correspondence with the frozen source

The receipt pins all six module JSON files, `shared.json`, `archive_build.py`,
and `reciprocal_kernel.py` by SHA-256. The module call graph has one root,
one anchor, one height batch, 41 comparisons, 41 comparison batches, and 42
pole blocks. There are six root elliptic points and five private points per
comparison, hence 211 points in all.

The field is `K = Q(sqrt(2))`, with `d = 3-sqrt(2)` and
`D = d^2 = 11-6sqrt(2)`. Pair multiplication is
`(a,b)(c,e)=(ac+2be,ae+bc)`, and inversion is
`(a,-b)/(a^2-2b^2)`. The denominator is nonzero precisely when the field
element is nonzero. The doubled-point formulas and affine subtraction formulas
in the new builder agree with the field formulas in the source. In particular,
for subtracting `(r,s)` from `(x,y)`, the line slope is `(y+s)/(x-r)`, its
intercept is `lambda*x-y`, the output abscissa is `lambda^2-x-r`, and the
output ordinate is `intercept-lambda*x_output`.

The height test orders are `1,1,1,1,48,48`. The 41 comparison orders are
23 copies of 1, two of 16, eight of 64, two of 16, and six of 64, in that
order. The independent evaluator reads the ordered norm-tree plans from the
pinned source JSON rather than reconstructing their grouping algorithm.
It checks both components of all field tests, all four primary logarithm
ratios, all five alternate ratios, and all 41 contacts. The contact constants
47027, 3, 25878772920, 2401 and 343/32 agree with the source. The contact
list has the initial five tests followed by four tests for each of the nine
scalars consisting of the denominator and the eight denominator-scaled
coordinates of the four root points.

The source shared chain starts at 3 and squares 24 times. Its final value
is `C = 3^(2^24)`. The previously proved packed anchor has three witnesses
and residual

\[
u^2+6v^2-2w^2-3(f_0^2+f_0f_1-f_1^2)^2+2C^4.
\]

The builder uses precisely this expression. Thus its literal power constant
is `2*3^(2^26)`; no power-chain coordinates remain in this presentation.
The anchor's arithmetic equivalence is established in `anchor-proof.tex`,
not by the finite-field tests in this audit.

## Why the source elliptic charts can be replaced by doubled points

Write `E: y^2=x^3-Dx`. The full source chart has

\[
f=u^2,\quad v^2+df=1,\quad w^2-df=1,\quad h=vw,
\quad zh+u=0,\quad xf=1,\quad yz+x=0.
\]

It forces `u,x,y,h,v,w,z` to be nonzero. Set
`r1=1/u`, `r2=v/u`, `r3=w/u`. Then

\[
r_1^2=x,\quad r_2^2=x-d,\quad r_3^2=x+d,
\quad r_1r_2r_3=y.
\]

Let `s1=r1+r2+r3`, `s2=r1*r2+r1*r3+r2*r3`, and put
`a=x+s2`, `b=s1*s2-y`. Direct expansion gives

\[
s_1^2=3x+2s_2,\qquad s_2^2=3x^2-D+2s_1y,
\qquad b^2=a^3-Da,\qquad 3a^2-D=2bs_1.
\]

The ordinate `b` cannot vanish: otherwise the last two identities would give
both `a(a^2-D)=0` and `3a^2-D=0`, contradicting `D != 0`.
The tangent slope at `(a,b)` is therefore `s1`, and the doubling formulas
give exactly `(x,y)`.

Conversely let `Q=(a,b)` lie on `E`, with `b != 0`, and suppose the doubled
point has nonzero abscissa and ordinate. Set

\[
c=a^2+D,\quad m=a^2-2da-D,\quad n=a^2+2da-D.
\]

Then

\[
x(2Q)=\frac{c^2}{4b^2},\qquad y(2Q)=\frac{cmn}{8b^3}.
\]

Consequently `c,m,n` are nonzero and a full source chart is obtained by
`u=2b/c`, `v=m/c`, `w=n/c`, `h=vw`, `z=-u/h`, and `f=u^2`.
All seven source equations follow by direct substitution. Thus the
replacement is exact, including the affine and nonvanishing restrictions.

For each halfpoint write `b=b0+b1*sqrt(2)`. Among the 212 rational integers
`j=0,...,211`, at most one satisfies `b0+j*b1=0`. Since all 211 ordinates
are nonzero, one common `j` avoids zero for every point. The three-coordinate
square-root chart with coordinate `C=b0+j*b1` therefore covers all simultaneous
halfpoints. Its inverse formulas and quartic relation are proved in
`square_root_compression.tex`; the separate exact symbolic checker verifies
the polynomial identities. The denominator `j^2-2` never vanishes for these
integer choices.

## Nonvanishing in the private compressed source charts

The private source chart uses

\[
f=u^2,\quad v^2+df=1,\quad p^2=x-Df,\quad xf=1,
\quad y=xp.
\]

It already forces `u,x` nonzero. If `v=0`, then `u^2=1/d`.
Taking norms to Q gives `N(u)^2=1/7`, impossible for a rational number.
If `p=0`, then `x=+d` or `x=-d`, and `u^2=1/x` again has norm `1/7`,
equally impossible. Thus `v,p,y` are nonzero. A full chart is recovered by
`w=p*u/v`, `h=v*w`, and `z=-1/p`. In particular the introduction of
direct divisions by these ordinates does not remove source solutions.

The source common negative logarithm `h` is also necessarily nonzero.
For the private beta point its source equations imply `A*h=G4(D*f_beta^2)`,
where

\[
G_4(T)=1-\frac25T-\frac2{15}T^2-\frac{14}{195}T^3.
\]

The integer cubic `195-78T-26T^2-14T^3` has nonzero leading coefficient
and no root modulo 19, as exhaustively checked in the receipt. It is therefore
irreducible over Q and cannot have a root in the quadratic field K. Thus
`h=0` is impossible. The source relation `h*p_H=G16(D*f_H^2)` gives
`log_H=-h`, while `log_i=-Gi/p_i`. The retained source ratios consequently
equal `log_i/log_H`, with the correct signs. This proves that replacing
the ratio equations by direct rational quotients neither gains nor loses
solutions. This nonvanishing argument is essential; generic nonvanishing
alone would not justify the replacement.

## Elimination of two variables from every pole block

The source equation for `U` is

\[
U(1+bt^2)=b(1-bt^2).
\]

If its left-hand coefficient were zero, then `b != 0`, and the right-hand
side would equal `2b`, a contradiction. Hence every old solution has

\[
U=\frac{b(1-bt^2)}{1+bt^2},\qquad h=e(17b-U^2).
\]

The builder substitutes these two uniquely determined values and keeps the
five coordinates `t,e,p,q,s`. This also handles `b=0`: then `U=h=0`, the
remaining equations force `p=s=0`, and the old freedom in `q` is retained.

## Limits of the audit

The exact structural checker does not reconstruct every source residual as a
formal multivariate polynomial identity. The source-to-formula correspondence
is supported by the displayed algebraic proofs, manual reading of the pinned
templates, and six independent modular evaluations of all residuals. The
modular evaluations alone are not certificates of symbolic equivalence.
The separate original-system arithmetic and anchor arguments remain explicit
dependencies. The circuit is an exact finite definition of an integer
polynomial, but its expanded coefficient table is not produced here.
