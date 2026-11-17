# Independent review: actual-trace arithmetic covers

## Verdict and scope

**PASS for the exact algebraic fixture and the stated genus computations.**
The four integer polynomials in the supplied certificate have been independently
reconstructed, coefficient for coefficient, from the actual elliptic points.
The two supplied modulo-101 Bézout identities have been verified by a separate
standard-library implementation. No author code, SymPy code, or symbolic
algebra producer is imported by this review's checker.

The fixture uses `X=1`, `B=3`, `A=P`, `H=U=5P`. It is an actual point tuple
for the six arithmetic test functions. It is not a prepared witness for the
Diophantine definition, and no assertion that `B=3` exceeds the ineffective
soundness threshold follows. The verification neither finds a rational
point satisfying every lift/preparation condition nor proves that one is
absent. It gives no new variable count.

## Independent computational reconstruction

`check_independent.py` uses exact `fractions.Fraction` arithmetic in
`Q(sqrt(2))` and computes the multiples of `P` by consecutive additions.
It checks the curve equation, the supplied coordinates of `4P` and `5P`,
the subtraction `5P-P=4P`, and the nonzero abscissa/ordinate and distinct
abscissa conditions used in the affine differences.

It then forms all six actual detector factors individually, multiplies
their numerators and denominators, and takes the reciprocal trace by
conjugation. This independently reconstructs the primitive common integer
pair `N,D`. A separate product-rule recurrence reconstructs the physical
map's integer pair `A_physical,B_physical`.

The reduction modulo 101 uses direct power-sum homogeneous composition,
not the author's Horner implementation. Both supplied Bézout polynomial
pairs are checked by exact multiplication. Independent Euclidean gcd
calculations give the same squarefreeness results. The reconstruction and
all these checks pass.

| Polynomial | Exact degree |
|---|---:|
| `N` | 24 |
| `D` | 24 |
| `A_physical` | 9 |
| `B_physical` | 8 |
| `P_u` | 50 |
| `P_t` | 450 |
| `P_t(z^2)` | 900 |

The final hashes and the computational outcome are in
`independent_certificate.json`.

## Actual trace and clearing squares

Put `c=f(5P)` and `d=conjugate(f(4P))`. The actual six tests are
`(c,c,d,d,0,0)`: since `U=H`, `A=P` and `X=1`, the two quotient tests
are `r-r'=1-1=0` and `r-X=1-1=0`. No free trace coordinate has been
substituted.

For `alpha=c^2`, `beta=d^2`, define

```math
L_\alpha(u)=u(1+u\alpha)^2+\alpha^2,\qquad
Q=L_\alpha L_\beta,\qquad
S=u^2(1+u\alpha)^2(1+u\beta)^2.
```

The repeated actual tests give `W=(Q/S)^2`. Therefore

```math
V=\operatorname{Tr}\bigl((S/Q)^2\bigr)
 =\frac{(S\bar Q)^2+(\bar S Q)^2}{(Q\bar Q)^2}
 =\frac ND.
```

The reported numerator `2(A^2+2B^2)` when `S*bar(Q)=A+B*sqrt(2)` is
correct. The common integer normalization of numerator and denominator
does not change this rational function. Their reductions are coprime
modulo 101, with both degrees preserved; consequently they are coprime
over `Q` as well.

The terminal radicand is exactly

```math
\mathcal C(u)=V(u)^2+\frac{u}{(1+u)^2}(2-V(u))
 =\frac{P_u(u)}{(1+u)^2D(u)^2},
\qquad
P_u=N^2(1+u)^2+uD(2D-N).
```

Thus the change of ordinate is `Y0=(1+u)D(u)Y`. The denominator is an
actual rational square and creates no extra quadratic extension. The
change is birational on the open set where `(1+u)D(u)` is nonzero. The
excluded denominator zeros must not be reintroduced as source witnesses.

## General fixed-test genus bound

For any fixed actual six-test tuple with `r>=1` nonzero tests, each nontrivial
factor of `W` is a quotient of polynomials of degree at most 3 over
`Q(sqrt(2))`. The numerator and denominator of the reciprocal trace can
therefore be chosen with degrees at most `6r`. After clearing the square
denominator above, the radicand polynomial has degree at most `12r+2`.
Removing square factors cannot increase this degree, so the smooth
quadratic cover has genus at most `6r<=36`.

The cover is genuine when at least one test is nonzero: each reciprocal
factor vanishes at `u=0`, so `V=O(u^r)` and
`C(u)=2u+O(u^2)`. The simple zero proves that the radicand is not a square
in `Q(u)`. The point `u=0` is used for the function-field argument only;
it is forbidden by the source guards. If all six tests were zero, the
equation would instead split as `Y^2=4`; the nonzero-test hypothesis must
be retained in a general statement.

## Physical substitution and exact genera

For this fixture, `a=(4^4+(57/4)^4)^4>10`. The physical weight is

```math
u=A(t)/B(t)=-18F(a,z)/F_a(a,z),\qquad t=z^2.
```

Here the nine contact roots `(a+c)^2` are distinct and every `a+c` is
positive. At each root, exactly one factor of `F` vanishes and the
corresponding summand of `F_a` is nonzero. This also proves directly that
the numerator and denominator of the degree-9 rational map are coprime.
The recorded integer pair is independently reproduced.

Write `P_t(t)=B(t)^50 P_u(A(t)/B(t))`. Its degree is 450; its leading
term comes only from the degree-50 term of `P_u` and the ninth power
degree of `A`. The Bézout identities modulo 101 prove squarefreeness of
both `P_u` and `P_t` over `Q`, because their full degrees survive the
reduction. In addition, `P_t(0)=42 mod 101`, so it is nonzero.

Consequently:

| Smooth curve | Squarefree polynomial degree | Genus |
|---|---:|---:|
| `Y0^2=P_u(u)` | 50 | 24 |
| `Y1^2=P_t(t)` | 450 | 224 |
| `Y2^2=t P_t(t)` | 451 | 225 |
| `Y1^2=P_t(z^2)` | 900 | 449 |

The last two squarefreeness conclusions follow because the first has
the extra simple root `t=0`, and the second can have a repeated root
only at `z=0` or above a repeated root of `P_t`. Both possibilities
are excluded. The even-degree covers have no additional ramification
at infinity; the odd-degree companion quotient has one branch there.

## Jacobian decomposition

The two maps from `C: Y1^2=P_t(z^2)` are

```math
(z,Y1)\longmapsto(z^2,Y1),\qquad
(z,Y1)\longmapsto(z^2,zY1).
```

They give the quotients by `(z,Y1)->(-z,Y1)` and
`(z,Y1)->(-z,-Y1)`, respectively. They are defined over `Q` and extend
to the smooth projective curves. Their differential pullbacks are

```math
2z^{2k+1}\,dz/Y1\quad(0\le k\le223),\qquad
2z^{2k}\,dz/Y1\quad(0\le k\le224).
```

Together these are the full basis `z^j dz/Y1`, `0<=j<=448`. Hence the
induced homomorphism from the product of the two quotient Jacobians
to `Jac(C)` is an isogeny over `Q`. The dimensions agree:
`224+225=449`.

The genus-225 curve is the second or companion quotient. It is not a
constant quadratic twist over `Q` of the genus-224 quotient.

## Rational lifting and source guards

A rational point on the weight curve does not automatically give a source
witness. For a finite candidate `(u,Y0)`, solve

```math
uB(t)-A(t)=0
```

over `Q`. Retain only rational squares `t=z^2`, with `B(t)!=0`, and
recover `Y=Y0/((1+u)D(u))`. Equivalently, a point on the `t` quotient
lifts to the `z` curve only when its `t` coordinate is a rational square.
The quotient ordinate changes by `Y1=B(t)^25 Y0`.

All of the following conditions still have to be checked:

- `u!=0,-1`, `N(u)!=0` and `D(u)!=0`;
- every balanced denominator norm `Norm(1+u*C_i^2)` and the detector
  product norm;
- all inherited point, difference, quotient and syntactic denominator
  guards, including the source contact guard `a^2-z^2!=0`;
- the whole-character nonvanishing and preparation conditions if the
  point is to count toward the actual-trace completeness criterion;
- the real prepared range `z>a+10` and every required fixed-place and
  selected-contact condition.

The notation `t=z^2` here differs from the inherited contact variable
`a^2-z^2`; its nonzero guard must not be lost by renaming.

The rational point at `u=0` and the projective points at infinity are
outside this guarded affine source. If lifting from the companion
quotient, division by `z` also requires care at `t=0`; the prepared range
already excludes this value. No rational-point or lifting search is part
of the verified computation.

## Status of manuscript review

**PASS.** The complete manuscript has now been read. Its nonzero-test
hypothesis, singular-affine-point caveat, physical inverse-map conditions,
guard list, companion quotient, differential proof and distinction between
an algebraic fixture and a sufficiently large defining shift are correctly
scoped. The manuscript and producer hashes are pinned in the independent
certificate. Milne's cited primary PDF was checked: it is *Abelian
Varieties*, version 2.0 (2008), and Chapters I and III concern abelian and
Jacobian varieties, respectively.

## Added exact local example

The updated manuscript's slope `z=a+12` was independently checked using
the reconstructed physical map. Its weight equals the supplied rational
number. At 17, precisely the shift `-5` gives a contact factor of valuation
one; all other contact factors have valuation zero. The weight satisfies
`v17(u)=1` and `u/17=1 mod 17`. Evaluation in the square-root slot
`rho=244 mod 289` gives `c=d=0 mod 289`; in the other slot the residues
are `c=2,d=1 mod 17`.

The four successful-slot detector factors are 1 modulo 17, while each
of the four opposite-slot factors has valuation -1. Hence the reciprocal
trace and the radicand are both 1 modulo 17; the radicand is a nonzero
17-adic square.

At 31, independent evaluation in both split slots `rho=8,23` checks
that every balanced denominator and detector factor is a unit and gives

```math
u=9,\qquad V=22,\qquad w=19,\qquad \mathcal C=11\pmod{31}.
```

Euler's criterion gives `11^15=-1 mod 31`, so the same positive actual
radicand is not a rational square. Both 17 and 31 belong to the retained
fixed exceptional set (which contains all primes up to 76176). This is
therefore a local arithmetic illustration, not an outside-exceptional-set
selected-contact theorem or a counterexample to the prepared realization
criterion. The final manuscript explicitly identifies both primes as
exceptional and disclaims full preparation, as required.
