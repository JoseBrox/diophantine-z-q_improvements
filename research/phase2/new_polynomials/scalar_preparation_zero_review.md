# Independent review of the scalar preparation-zero refinement

The proof in `scalar_preparation_zero.tex` is valid under the same stated
source arithmetic and simultaneous prime-pattern assumptions as the shared
construction. It changes the arithmetic presentation, rather than merely
eliminating a variable from every old witness. Its resulting construction
bounds are 43 total coordinates with the indexed exclusion and 45 with
the semilocal anchor, after the separate finite-algebra construction.

## Scalar soundness and denominator parity

For rational input, beta=X^2+2 has no negative odd valuation: when its
valuation is negative it equals twice the valuation of X. Thus the
infinity contact contributes no odd prime to the scalar radical. At a
finite old contact outside the exceptional primes, delta(beta) is a unit
by the displayed resultant evaluations. The new parameter

`R=(204/23^12)^2*r_beta/delta(beta)^4`

has the same positive odd valuation as r_beta there, while every correction
is a unit. The same norm-tree valuation argument therefore imposes the
same assigned divisibility orders and gives the unchanged height estimate.
This verifies exactly the needed scalar soundness implication.

For integer beta, the parity correction at the six resultant primes is
independent of the seven local squareclass-basis primes. At primes dividing
delta outside the resultant set, neither r_beta nor the correction is
divisible; the numerator of the fixed normalizer is also a unit because
delta has no roots modulo 2, 3 or 17. The valuation of R is then a
multiple of four. At the resultant primes the correction makes the full
valuation even, including the denominator at 23. All other valuations
are nonnegative. This proves the square-denominator assertion, rather
than assuming it from the local square conditions.

The exact real estimate follows by bounding the five factors of r_beta
by beta, beta, 1202 beta, 204 beta, and 2 beta for beta>=2, and using
delta(beta)>beta^2. The correction maximum and the fixed normalizer then
give 0<cR<1. The normalizer supplies valuations at least 4, 2, 2
at 2, 3, 17 respectively. These are stronger than the preparation-zero
pole requirements.

## Simultaneous real and local choices

Let G be the compact closure of the cyclic orbit in the product of the
two real elliptic groups, and let m=|G/G^0|. For every positive integer
k, the closure of k times that orbit is [k]G. Multiplication by k is
surjective on G^0, so this closure contains G^0; if m divides k, it
equals G^0. Accordingly an arithmetic progression whose modulus and
residue are divisible by m is dense in G^0. Its positive tail is also
dense.

This gives the required common annulus: choose a relatively compact open
set near the identity in G^0, avoiding the identity in both projections,
so f(H) is uniformly small and z(H) is bounded away from zero. The
projection to each real circle is surjective, so such sets exist even
when G^0 is a proper subtorus of the product. Choose h0 in a sufficiently
divisible local subgroup and in that annulus. Next choose S in its
required finite-index subgroup near the real identity, with the required
size and local depth. Then f(S) and z(S)/z(H) are uniformly small on
the annulus. The scalar norm root is consequently uniformly close to 1.

After the roots have been fixed, local continuity prescribes h modulo L.
Taking both h0 and L divisible by 64m preserves the real component.
The reversed reduction orders still give gcd(U,L)=64, gcd(V,L)=4,
and gcd(U,V)=4. These statements remain true when m adds further
factors to L: all new odd factors other than 7 are excluded by the prime
pattern, 7 is excluded by its fixed Gaussian congruence, and the two-adic
valuations of U and V are fixed. The CRT conditions are therefore
compatible, and the resulting progression is dense in G^0.

The finitely many comparison pole loci have empty interior in the annulus.
Their coordinate maps are nonconstant rational functions on a real
elliptic circle, composed with multiplication by nonzero root labels or
fixed translations. Removing their finite inverse images in each circle
leaves a nonempty relatively open subset. Thus comparison bounds can be
fixed before the prime-pattern modulus, and the final progression still
attains them together with the scalar real bound.

At each prime in the finite support of cR, the initial local construction
can make all six normalized scalar leaves arbitrarily divisible. This
remains possible when the valuation of R is negative, since R is a
fixed nonzero rational number. Making the leaves deep enough makes all
nonconstant norm-tree summands divisible; its constant-left path gives
W=1 modulo the prime. The final progression preserves these units.
Therefore b=cRW^2 has square denominator, all required local square
classes, the stated valuation lower bounds, and 0<b<4<17. The original
preparation-zero pole lemma supplies the remaining witnesses.

The author has incorporated the suggested explicit choice |W-1|<1/2,
which immediately supplies W!=0 as well as |W|<2, and has corrected
the minor missing backslash in the correction set. The reviewed source
SHA-256 is
`78e8ce21b3ecb52751587af17dc8147e22bf9f631f6041e6fabce64a8e37ebb1`.

## Verification scope

`verify_scalar_preparation_zero.py` independently recomputes the fixed
contact resultants, the seven local squareclass span by exhaustive
enumeration of its 128 products, the prime support, and the exact integer
normalizer inequality. It imports no producer or source checker. This
finite check complements the mathematical argument above; it does not
prove the external arithmetic hypotheses or verify an emitted final
polynomial.

## Final exact refinements: conic parameters and unconditional scales

The first pole conic can be parametrized exactly when B!=0. Retain a
new conic parameter t and a finite chart sigma in {0,1}, impose
`D=t^2+3B!=0`, and define

`e=(t^2+(4*sigma-1)*B)/D`.

On chart zero put `p=-4Bt/D`; on chart one put p=0. On chart zero,
`1-e=4B/D` and `1+3e=4t^2/D`, proving the required identity
`p^2=B(1-e)(1+3e)`. Chart one has e=1. Conversely, an old point
with e!=1 gives `t=p/(e-1)` and `D=-4B/(e-1)!=0`, while e=1
forces p=0 and is represented by chart one with t=0. The other zero
point e=-1/3,p=0 occurs on chart zero with t=0. Thus no old solution
is lost, and no derivative guard on the removed p generator may remain.

This replaces one retained coordinate e by one retained conic parameter
and removes one finite quadratic generator per pole. Across ten poles,
the maximum algebra rank drops from 2^39 to 2^29 (from 2^40 to 2^30
with the semilocal anchor), with no change to the retained-coordinate
count. The new conic parameter is distinct from the deleted preparation
parameter.

The root-coordinate scales may simultaneously be replaced by
`A0=x0^2` and `A1=(1+x1^2)^2`. Every finite point in 2E(K) has
a nonzero square abscissa, whose rational component x0 is positive.
Thus both scales are always nonzero rational squares. The exact rational
height identity `h(1+x^2)=log(a^2+b^2)>=2h(x)` for reduced x=a/b
gives the original 7H field-height bound with a smaller constant.
The full independent proof is in
`../quartic/field_quotient_domains.tex`. These scales remove all eight
old zero/nonzero scale choices. Neither refinement requires a new
arithmetic input.
