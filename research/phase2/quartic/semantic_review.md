# Independent semantic review of the shared quartic compiler

Reviewed source SHA-256:
`d46246a2d303a2a396d0de46840c0b8fd32961830d7db6306835393241b4ef44`
for `build_shared_quartic.py`.

This is a review of the mathematical meaning of the compiler source in its
default mode (`share_height=False`). The independent sparse-polynomial and
gate checker is a separate artifact. This review does not certify the
underlying arithmetic inputs or the extra prime-pattern theorem.

## Field and elliptic arithmetic

The two-coordinate arithmetic is the exact arithmetic of Q(sqrt(2)).
Multiplication uses the three-product identity
`(a0 b0+2 a1 b1, (a0+a1)(b0+b1)-a0 b0-a1 b1)`;
the norm is `a0^2-2 a1^2`; the inverse is the conjugate divided by
the norm. Every field division therefore carries its precise nonzero
norm guard.

Each point begins as a four-coordinate affine halfpoint on
`y^2=x^3-(11-6 sqrt(2))x`. The two curve residuals are correct, as
are the doubling slope `(3x^2-D)/(2y)` and resulting abscissa/ordinate.
The explicit nonzero guards on the doubled abscissa and ordinate retain
the domain of the arithmetic source. The inverse of the halfpoint
ordinate norm excludes doubling the identity. The full halfpoint chart
is used here, so no finite-chart or square-root-compression argument is
silently needed by this compiler.

For `difference(a,b)`, the slope `(y(a)+y(b))/(x(a)-x(b))`
gives `a-b`, and the ordinate `nu-slope*x_new` with
`nu=slope*x(a)-y(a)` has the correct sign. The subtraction guard
is exactly the source's abscissa-inequality guard. The five targets
are `[4]P,[4]A,[4]S,[4]T,[4]Z`, obtained by two doublings.

The reciprocal logarithm recurrence has the correct sign and length:
precision 16 uses G_3 and precision 64 uses G_15, multiplied by
`z=-x/y`. The primary and conjugate shifted ratios have the right
denominators. The eighteen tests consist of ten order-one reciprocal
abscissas, four ratio differences, and four differences from the proxies,
with orders `(16,64,64,64)` for each latter group. The Lucas residual
is exactly the stated monic equation.

## Square rescalings and grouped products

For each abscissa component x the compiler imposes
`eps^2-eps=0`, `eps*x=0`, and `x^2+eps!=0`.
Over Q these force precisely `eps=0,A=x^2` when x is nonzero,
and `eps=1,A=1` when x is zero. Thus this replacement of finite
zero/nonzero branches introduces no extraneous branch.

The detector identity used by the compiler is exact:

`A^-5 F_5(A lambda) = product_theta (lambda-theta/A)`.

Let `c=(t-1)^-1`, `r=R`, and `v=c/r`. The common multiplier
for all squared tests of order m is computed as

`q_m=(r*c^2)*v^(2m)=R^(1-2m)*(t-1)^(-2m-2)`.

The coefficient recurrence in `product_coefficients` computes the
elementary symmetric polynomials of the field elements `D_j^2`.
Horner evaluation at q_m therefore gives exactly
`product_j (1+q_m D_j^2)` for that order group. Multiplying the
three groups recovers the specified W without changing a condition or
assuming that any test is nonzero.

Writing `W=W0+W1 sqrt(2)`, the trace is `2W0/Norm(W)` and
the pole input is

`R*(Norm(W)/W0)^2/4`.

The single inverse of W0 enforces both required guards over Q: if W0
is nonzero then W is nonzero, and its norm is nonzero because Q(sqrt(2))
is a field. Conversely a nonzero W with nonzero reciprocal trace has
nonzero W0. This equivalence is an arithmetic statement about rational
coordinate solutions; no claim that the norm is anisotropic over an
algebraic closure is needed.

## Pole and scalar equations

The pole equations are precisely
`p^2=B(1-e)(1+3e)` and
`B q^2=(s^2-Bh)(s^2+3Bh)`, with `B=17b`.
Computing q^2 as a multiplication gate keeps the second row quadratic.
For the nine coordinate poles, U=b and `h=e(B-b^2)`, so their
preparation parameter is zero. For the scalar pole the full expression
`U=b(1-bt^2)/(1+bt^2)` is retained with its denominator guard.
All pole inputs are guarded nonzero, as in the reviewed shared source.

The scalar correction bits give exactly the signed squarefree products
of `{2,3,5,7,11,13,17}`. Its six scalar tests and their orders are
correct. The initial norm-tree node `1+test0^2/r` is precisely
`N_r(1,test0/r)`; the remaining tests are divided by their assigned
powers of r and joined by `N_r(a,b)=a^2+r b^2`. The tree retains
the constant leaf 1 on its all-left path, which is the property used
by the scalar soundness and unit arguments. Regrouping the remaining
leaves by order is compatible with those arguments; an exact identity
with a differently bracketed old norm root is not being assumed.

## Semilocal size anchor

The input form `r=f0^2+f0*f1-f1^2` is the proved simultaneous
semilocal test for the two reciprocal-abscissa components. The equation
`u^2+6v^2-2w^2-3r^2+2K=0` uses
`K=C^4=3^(2^26)` for the original scale `C=3^(2^24)`.
Thus the fixed symbol K is correct; it is not a coordinate. In the
smaller-coefficient mode, the start `3^16` followed by 22 squarings
produces exactly this K. The three anchor witnesses retain both
soundness and completeness of the previously proved anchor.

## Gate and export interpretation

Scalar-normalized multiplication and inverse cache entries preserve their
values by their recorded rational scaling factors. Every arithmetic
coordinate has a quadratic defining row. Inverses remain equations with
right side 1. Removing unused multiplication gates preserves all source
and inverse rows and all dependencies of their retained coordinates.
Clearing a residual's rational denominators and dividing by its integer
content multiply that residual by a nonzero rational constant, so its
zero set is unchanged. Summing the resulting squared integer residuals
gives a quartic with the same rational solutions.

The coefficient bit bound reported over Z[K] concerns the formal
coefficients before substituting the fixed huge integer K. A final
ordinary integer coefficient-height bound must include that substitution.
The root checker is responsible for checking the emitted variable map,
rows, sparse expansion, and exact numerical counts; this semantic review
does not replace those checks.

No source-formula, domain, or variable-accounting error was found in the
reviewed default mode. Subsequent reviews of the sharing argument and
precision refinements are recorded below.

## Addendum: shared height, precision 52, and blocked logarithms

The independent arithmetic proof in
`../new_polynomials/sharing_review.tex` establishes the additional
`share_height=True` mode under the same stated arithmetic inputs.
The shared point preserves the scalar local conditions by a compatible
fixed progression, and its scalar pole witnesses are chosen after the
common index. Thus this mode has no unproved sharing step in the present
source argument.

The subsequently reviewed compiler SHA-256 is
`cafae7e33cc285adf39e699d82053970373be8e794c1cd64991cef8395d638e9`.
It includes precision 52 and the optional scalar order 32. The independent
mathematical review of `precision52.tex` verifies that the degree-12
reciprocal logarithm has relative precision 52, the enlarged label bound
`|a|>(21H)^(13/2)` suffices for the Lucas contradiction, and the semilocal
anchor with `C=3^(2^26)` implies that bound. At this precision the fixed
symbol is `K=C^4=3^(2^28)`; the source, metadata and explicit repeated
squaring mode use this value. The precision-64 constant remains
`3^(2^26)`.

For the blocked polynomial evaluation, write
`G(w)=sum_r w^(b*r) sum_j c_(b*r+j) w^j`.
The compiler constructs the inner sums with exact rational coefficients
and evaluates the outer sum by Horner's rule in `w^b`. Its block size is
three for G_12 and four for the other supported truncations. This is
exactly the original polynomial, with no division and no new guard.
The degree-15 evaluation uses six nonconstant field products and the
degree-12 evaluation five; the last G_12 chunk is constant. An unused
power gate in the degree-three case is removed by the existing dependency
pruning. None of these arithmetic changes modifies the source zero set.

Finally, lowering the two scalar-height orders from 48 to 32 is justified
by `scalar32.tex`: the enlarged size bound implies `|a|>(20H)^4`,
which yields the same final scalar-height contradiction. Completeness
preserves the required integrality and unit conditions with the smaller
orders. The constructor rejects scalar order 32 unless precision is 52,
and uses the selected order for exactly those two scalar leaves.

The root's separately run sparse-polynomial checker certifies the emitted
counts and coefficients. This semantic review does not substitute for
that certificate and does not independently certify the underlying source
arithmetic or the additional prime-pattern theorem.

## Addendum: two-coordinate field gates and direct quotients

The subsequent builder SHA-256
`c095b91696ece76db09771e23e54936dd8eb2118b6eb56c89347a0362046121e`
uses two quadratic output equations for field products, two equations for
field inverses, and direct two-output quotient equations in the cases
where a separate mathematical argument already forces the denominator
nonzero. The full independent domain proof is in
`field_quotient_domains.tex`.

For the doubling slope, y=0 on the curve would give x=0 or x^2=D;
then 3x^2-D is -D or 2D and cannot vanish. Thus the direct slope
equation itself excludes every zero denominator. Every finite doubled
point has nonzero square abscissa. It cannot be a nonidentity point of
order two: zero abscissa is excluded by the doubling formula, while the
other two torsion abscissas have norm 7 and are not squares in
Q(sqrt(2)). Hence its ordinate is nonzero as well. This argument applies
to every finite point of 2E(K), including the constructed differences.

These facts justify the direct quotients for z=-x/y and for
z(S)/z(J0). The source's global nonvanishing lemma for G_J, with
J=3,12,15, then makes every logarithm denominator nonzero. The direct
logarithm ratios are therefore valid. The subtraction slope correctly
retains its explicit abscissa-inequality inverse; it is not covered by
these domain arguments.

The rational solution set is preserved by all these changes. The full
sparse expansion and numerical variable counts remain the responsibility
of the separately run structural checker, and the arithmetic status of
the source construction is unchanged.
