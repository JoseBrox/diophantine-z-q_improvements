# Further four-coordinate rationality conditions

Research checkpoint, 9 November 2026. These conditions do not define the
integers, and completeness for the rational subfield is not asserted.
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

Its global coverage is unknown. A bounded search using
`n*(-2,1)+k*(0,3)` with |n|≤30 and k=0,1,2 found no slope ratios 2 or
3. This is only computational evidence, not a nonexistence theorem.
No defining-polynomial claim should use completeness of this condition.

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
