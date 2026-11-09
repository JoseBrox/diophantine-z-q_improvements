# Further four-coordinate rationality conditions

Research checkpoint, 9 November 2026. These conditions do not define the
integers. The degree-eleven condition is now proved to miss infinitely
many rational integers by the rational-map theorem below.
They use the exact point stability of `E:y²=x³+9` over each of the eight
quadratic fields certified in the companion paper.

## Slopes: degree eleven

Put

`F(W,U)=U²W-9W³-1`

and define the integer polynomial

`R(T,Z,W,S)=T*((T²Z²W-9W³-1)²-2*(Z²S-9S³-1)²)`.

It has four total coordinates, degree 11, coefficient height 162, and
11 monomials. Its expanded terms are

```
 T^5 Z^4 W^2 + 81 T W^6 - T
 -18 T^3 Z^2 W^4 -2 T^3 Z^2 W +18 T W^3
 -2 T Z^4 S^2 -162 T S^6
 +36 T Z^2 S^4 +4 T Z^2 S -36 T S^3.
```

For nonzero t, nonsquareness of 2 makes both residuals vanish. They
represent two points of E in the projective chart X≠0, with slopes
`u1=t*z` and `u2=z`. Exact point stability makes the points rational.
The denominator slope cannot vanish: otherwise a rational point of E
would have ordinate zero, requiring a rational cube root of -9.
Consequently the projection is

`{0} union { (y(P)/x(P))/(y(Q)/x(Q)) : P,Q in E(Q), x(P)x(Q)≠0 }`,

a Diophantine subset of Q inside each of the eight quadratic fields.
It contains both 1 and -1, by changing the sign of the ordinate.

This equation is solvable at every input in every characteristic-zero
local field: `x/y` is a uniformizer at O, so any fixed ratio is realized
by two sufficiently small nonzero local parameter values. The same
formal-logarithm and Chinese-remainder argument as in the companion
paper shows that its actual rational projection is dense in every
finite product of completions of Q.

Its global coverage is not all of Q. Corvaja--Zannier, with an appendix
by Masser, *Rational and integral values of rational functions at
rational points*, arXiv:2608.28255v1 (28 August 2026), Theorem 1.1,
proves that a finite union of rational-map images of finitely generated
subgroups of semiabelian varieties misses infinitely many rational
integers. Apply it to `E×E`, its finitely generated rational point
group, and the rational function `y(P)*x(Q)/(x(P)*y(Q))`. The explicit
chart above ensures this function is defined on every nonzero-input
witness; the leading factor adds only the finite exceptional value 0.
Hence this condition fails integer completeness as well as rational
completeness. Primary source:
https://arxiv.org/html/2608.28255v1.

A bounded search using
`n*(-2,1)+k*(0,3)` with |n|≤30 and k=0,1,2 found no slope ratios 2 or
3. This is only computational evidence about those particular inputs;
the source theorem does not identify them as excluded values. The
search and exact expansion are reproduced by
`check_rationality_filters.py`, with PASS output in
`rationality-filter-certificate.json`.

The same source theorem rules out obtaining a set containing all
integers by any fixed finite sums, products, or ratios of values supplied
by fixed abelian varieties, including finite unions and added finite
sets. Each such expression is a rational map on a product of abelian
varieties; Mordell--Weil supplies finite generation. Additional
restrictions on those point tuples only shrink the image. This does
not cover arbitrary algebraic correspondences, or constructions with
unrestricted additional affine witnesses whose outputs are not fixed
rational functions of the abelian points.

## Ordinates: degree nine, with an elementary obstruction

An even lower-degree rationality condition is

`S(T,V,X,Y)=T*((T²V²-X³-9)²-2*(V²-Y³-9)²)`.

Its projection is exactly zero together with ratios of nonzero rational
ordinates of E. The proof again uses point stability and the absence
of a rational point with ordinate zero. The polynomial has four total
coordinates, degree 9, coefficient height 81, and 11 monomials:

```
 T^5 V^4 + T X^6 -81 T
 -2 T^3 V^2 X^3 -18 T^3 V^2 +18 T X^3
 -2 T V^4 -2 T Y^6 +4 T V^2 Y^3 +36 T V^2 -36 T Y^3.
```

This projection is proper for an elementary local reason: every
rational ordinate y on E has v_7(y) divisible by 3. If v_7(x)<0,
then `2v_7(y)=3v_7(x)`, so v_7(y) is a multiple of 3. If v_7(x)≥0,
the ordinate cannot have positive valuation because `x³=-9=5 mod 7`
has no solution (the nonzero cubes modulo 7 are 1 and 6). It therefore
has valuation zero. Every ratio of ordinates consequently has
7-adic valuation divisible by 3, and 7 is excluded.

Unlike the slope and abscissa constructions, this ordinate condition
does not have local universality. Its smaller degree is not an
improvement to the locally universal obstruction theorem, nor to a
definition of the rational subfield or the integers.
