# v145: sparse radix and exact contact compression

This is a conditional quartic construction under precisely the premises of v143, with 8 certified integer source coordinates. The general and specified systems have respectively 594 and 612 rational variables and 529 and 545 quadratic residuals. The sum-of-squares convention and the scalar premises are unchanged.

## Sparse support

Use the natural nonnegative source of v142, comprising 63 variables and 51 quadrics, homogenized with the dummy coordinate 1. In the signed-power packing, the only sums that need to be unique among all unordered pairs (including repetitions) are those corresponding to actual source monomials. Collisions exclusively between unused monomials are harmless. The fixed pairing and exponent list in build.mjs were obtained by searching for this weaker property. There are 64 signed positions, 2080 unordered pairs, 136 potentially used monomials uniformly in the source parameters, and 73 nonsingleton pair-sum classes. None of the potentially used monomials belong to a nonsingleton class. This is a finite integer claim, independently checkable without evaluating the large radix powers.

The maximum exponent is 37 instead of 46. With the center chosen as in v142, this saves nine squarings. Use block width L=64 rather than 51, and test the entire padded block: offsets 51 through 63 have zero coefficient because all position sums are multiples of L and actual equation offsets lie between 0 and 50. The original coefficient bounds and carry argument apply, including the dummy-square positive highest term. Computing the seed B^64 instead of B^51 saves two further registers.

Use b=4f² rather than b=f², with f nonzero forced by the existing scalar equation k² den=(1+chain k²)² for k=f. Hence integer f gives b>=4, and every required b=4^n, n>=1, has f=2^(n-1). Replace the scalar and weighted comparison uses of f² by b/4. The source positivity triangle for f is now unnecessary (three coordinates and one row); b modulo 3 is still 0 or 1. The g-interval guard remains unchanged. The source prefix has 183 variables and 171 rows rather than 197 and 183.

## Exact chart changes

For contact center c0, T=(t-c0)², replace the auxiliary (t+3)² by the affine expression T+2(c0+3)t+9-c0².

The contact gate of v143 is
g=1+E²+(C-q)²/q, tau(1+q)=g, b_pole=7q tau².
Replace g and tau² by v=q tau and use
v(1+q)=q(1+E²)+(C-q)², b_pole=7v tau.
The quadratic system forces q nonzero, since q=0 gives C=0 contrary to the existing inverse equation. Thus the old gate is recovered without dividing by 1+q; even the exceptional fiber q=-1 is equivalent. These changes save two coordinates and two rows per contact.

In the fixed reference chart put pi=eta+S+T, d=pi F=eta G, x=eta pi, y=-(eta+T)x-Dd. The existing curve row is D(F+G)=(S-T)eta-T². It implies (eta+T)²-x=-D(F+G). Also x(F+G)=(eta+pi)d and d²=xFG. Expansion therefore gives
y²-x³+Dx=Dx[1-d(S-T)+DFG].
The prescribed nonzero x-coordinate and prescribed y-coordinate of P0 already satisfy the elliptic curve equation. Consequently the unit row d(S-T)-DFG=1 follows, and its two rational components can be deleted. No analogous deletion is asserted for the private pairs.

## Accounting

General: 612-14-4=594 coordinates, 547-12-4-2=529 rows. Specified: 632-14-6=612 coordinates, 565-12-6-2=545 rows. The builder is pinned to the same v128 source as its predecessors; the two systems were instantiated with five exact integer parameter fixtures each, with support, quadratic degree and census checked. This is not an unconditional proof of undecidability or an independent verification of the inherited arithmetic conjectures. The Pell quotient certificates remain.
