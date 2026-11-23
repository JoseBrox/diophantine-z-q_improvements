# Independent audit of the signed binomial positivity reduction

Reviewed on 23 November 2026 against
`undecidability/source_repair_v93/signed_binomial_positivity.tex`, with the
Pell lemmas checked in `undecidability/papers/pell_index_optimization.tex`
and `undecidability/papers/binomial_pell_certificate.tex`.

**Conclusion:** the quantified local theorem and the five-coordinate
reduction pass independent mathematical review. This is a proof audit,
not an independent proof of the external coding theorem or of the
rational integer interfaces.

## Decisive checks

1. The inequality `k^2 > 4(c-k s M)^2`, with nonzero integral `s` and
   `M >= 16`, forces both `k != 0` and `c != 0` before any Pell
   classification. Consequently the existing reciprocal row recovers
   the nonzero integer `i` without a circular sign assumption.

2. If `w=0`, the small norm forces `k=+1` or `k=-1`. The inequality
   then forces `c=k s M`. With `Y=s M`, the first large norm becomes
   `d^2=(r Y^2)^2-Y^2+1`. Its gaps above `(r Y^2-1)^2` and below
   `(r Y^2)^2` are respectively `(2r-1)Y^2` and `Y^2-1`, both positive.
   Thus zero is excluded without assuming a sign for `w`.

3. For either sign of `a`, let `A=|a|` and `C=|c|`. Pell
   classification gives `C=Y_t(A) >= 2A`. The bridge
   `G=a+F^2(c+1-a)` is at least `c+1 >= 5` when `c>0`, and at most
   `c+1 <= -3` when `c<0`. The third Pell equation is therefore
   nondegenerate in all four sign combinations of `a,c`.

4. The square-divisibility and signed trace lemmas imply
   `B == +/-t (mod C)`. The alternative `B=C-t` is excluded because
   `C` and `t` have the same parity whereas `B=2r+1` is odd. The root
   equation then selects exactly `d=X_B(a)`, including negative `a`.

5. With `sigma=sign(w)`, `U=|w|M`, and `Z=|s|M`, one has
   `A=rZ(U+sigma)` and `P=|p|=2r^2 Z^2 U`. The growth estimate bounds
   the small Pell index by `4r`. The modulus `|p-1|=P-sigma>5r+1`
   consequently forces its index to be `r+1` and
   `sign(k)=sigma^r`. This checks both the `P-1` and `P+1` cases.

6. The normalized Pell estimate and its monotonicity in the parameter
   have complete proofs in the cited binomial paper. Their application
   here is valid for both `U-1` and `U+1`. The resulting size estimate
   is `A > 2 U 4^r`; the displayed numerical lower bound
   `735/256 > 2` is correct for the complete range `U>=16`, `r>=1`.

7. For negative `c`, the linear congruence is the multiplicative inverse
   of the positive-branch congruence: `bw 2^B == 1 (mod 4a-5)`.
   Its nonzero remainder has absolute value strictly smaller than
   `|4a-5|`, excluding that branch. For positive `c`, the ordinary
   congruence has remainder of absolute value smaller than the modulus,
   forcing `bw=2^B` exactly. This gives `w>0`, and the previously
   established sign relation gives `s>0`.

## Boundary and implementation checks

The nonzero guard on `s` is essential to this argument. The paper's
explicit example with `r=1`, `M=256`, `b=16`, `w=1`, `s=0`,
`a=p=c=0`, `k=h=i=F=d=1`, `tau=zeta=j=o=0`, and `gamma=3` satisfies
all the displayed equations and the strict inequality, despite
`256` not dividing `binomial(2,1)`. Every component of this example was
checked directly.

Once the two signs are recovered, the six old positivity coordinates
can be restored without changing any retained coordinate. The
transformation therefore deletes six coordinates and two rows, adds
one inverse coordinate and one quadratic unit row, and saves exactly
five coordinates and one row. This equivalence applies to the corrected
`n^6` block. It does not assert the same result for the historical
`n^2` parameter.

The arithmetic proof and the coefficient-table transformation are
separate checks. Exact table regeneration and occurrence/support audits
are supplied by the signed-positivity producer and independent verifier
in `undecidability/source_repair_v93/`.
