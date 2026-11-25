# v150: signed binomial rounding for the coprime Pell merger

**Partial rational shared-certificate result.** The redesigned modulus of v148 does support the complete binomial equivalence *if* the two small/third Pell ordinates are integral. In particular the change p -> p+1 does not create a rounding gap. The [subsequent v151 global obstruction](../shared_pell_global_obstruction_v151/README.md) disproves joint rational-ordinate integrality from this single sum, with full false packed-source witnesses. The conditional rounding theorem remains valid; no seven-integer construction follows here.

Use the equations and hypotheses of [v148](../shared_pell_core_v148/README.md), including the retained shifted first trace

    d-(a-2)c=bw+(4a-5)gamma,

where b is a positive integer, 2<=b<=M/4, gamma is integral and 3|Mr. The first norm and halftrace then recover c,d in Z by v106. Assume k,H in Z, as in v148. The remaining assumptions of its theorem are satisfied for the packed prefix: M=N^2, N a multiple of 4, 0<=S,T<N, r=(N-1)((S+T+1)N+T+1), so N^2-1<=r<2N^3 and M^2>3r+2 for N>=8 (indeed N is much larger). The scalar nonzero guards give w,s nonzero. Replace i=2i_half+1 by a nonzero integer i=M i', using i' as the certified nonzero quotient for this partial construction only.

## 1. Exact signed indices and an absolute perturbation bound

The v148 coprime-modulus argument applies with signed P=1+2Ur^2Y^2, U=wM, Y=sM, and gives h,j in Z, |c|=Y_(2r+1)(|a|), |d|=X_(2r+1)(|a|), |k|=Y_(r+1)(|P|). In its signed small-index congruence k=epsilon Y_l(P), reduction modulo M^2 gives epsilon*l=r+1, since P=1 mod M^2. With l<B=2r+1 the only possibility is epsilon=1 and l=r+1, using M^2>3r+2. Thus k has sign sigma^r, sigma=sgn(w).

Put U=|w|M, Z=|s|M, a1=|a|=r Z(U+sigma), P0=2U r^2 Z^2, so |P|=P0+sigma>a1>=2. Here U,Z>=16. Let C=|c|, K=|k|, rho=(U+sigma)^(2r)/U^r. The strict margin gives |C/K-Z|<1/2. Write f_n(x)=Y_n(x)/(2x)^(n-1), the normalized Pell polynomial from the independently proved binomial certificate. Its elementary bounds are 1-(n-2)/(4x^2)<=f_n(x)<=1; it decreases in n and increases in x for x>=2. Therefore the exact identity is

    C/K = rho * Q * F0,
    Q=(1+sigma/P0)^(-r),
    F0=f_(2r+1)(a1)/f_(r+1)(P0+sigma).

We have 1-eps<=F0<=1, with eps=(2r-1)/(4 a1^2)<1/(2 Z^2 (U-1)^2). Bernoulli's inequality gives |Q-1|<=2r/P0=1/(r U Z^2) and Q<=2 (for the positive sign use 1-(1+x)^(-r)<=rx). Consequently

    |C/K-rho| <= rho*(|Q-1|+Q*eps)
              < delta*rho,   delta=2/(Z^2 U)<=1/2048.

The error is absolute, not one-sided. The first-Pell sign and power argument needs only this absolute bound.

## 2. Both signs, exact power, exact rounding

Since rho>(U-2)^r and delta<1/16, the margin gives

    Z>(15/16)(U-2)^r-1/2 > (7/8)(U-2)^r,
    a1>2 U 4^r.

For the latter, (7/8)r*(U-1)/U*((U-2)/4)^r >=735/256>2, as in v101. Write d=epsilon X_B(a), c=kappa Y_B(a) with epsilon,kappa in {+1,-1}. The recurrence identities in v101 for R_B^- = X_B(a)-(a-2)Y_B(a) and R_B^+ = X_B(a)+(a-2)Y_B(a) give

    R_B^- = 2^B mod (4a-5),
    2^B R_B^+ = 1 mod (4a-5).

These are valid for either sign of a. With |bw|<=2U and |4a-5|>4U 4^r+1, opposite signs epsilon,kappa would imply 0<|bw*2^B-epsilon|<|4a-5| and divisibility by 4a-5, a contradiction. Equal signs force bw=epsilon*2^B, by the same size bound. Thus |bw|=2^B, b is a power of two, epsilon=kappa=sigma, and s has sign sigma^(r+1) by the margin and the sign of k.

Set T_sigma=sum_(j=0)^r binomial(2r,j) sigma^j U^(r-j). The binomial tail estimate from v101 applies with no parameter change:

    |rho-T_sigma| < (4^r/U)/(1-1/U) <= 2/15.

Here U=2*4^r*M/b and M>=4b. The perturbation bound, together with the margin, gives

    |C/K-rho| < delta*(Z+1/2)/(1-delta) < 1/4

for Z,U>=16. Hence |Z-T_sigma|<1/2+1/4+2/15<1; both integers agree. Since M divides U and Z, M divides the central binomial coefficient. This proves the complete signed binomial soundness conditional only on the remaining ordinate integrality.

## 3. Canonical completeness with the changed parameter

For b a power of two and M|binomial(2r,r), use the original positive canonical choices w=2^(2r+1)/b, U=wM, Z=T_+, s=Z/M, a=r Z(U+1), c=Y_B(a), d=X_B(a), gamma=(d-(a-2)c-bw)/(4a-5). The original proof supplies integral positive gamma and the halftrace square. Choose instead k=Y_(r+1)(P0+1) and tau=X_(r+1)(P0+1). The new modulus congruence gives positive integral h=(k-r-1)/M^2. Since rho=Z+tail and the tail is <2/15, the absolute perturbation bound in section 1 gives |C/K-rho|<1/4 (now using rho<Z+2/15 directly). Hence |c/k-Z|<1/2. The positive integer eta=k^2-4(c-kY)^2 is at least one, so the original three-triangular-number witnesses exist.

Take the second Pell exponent a sufficiently large multiple of the order of the Pell matrix modulo M c^2, and divide its ordinate by M c^2 to give i'>0. Apply the v95 positive third-Pell congruence construction to obtain integral j>0 and H,I. Their defining congruences and the second norm use i=M i'. Thus the new certified sum L=h+j is a positive integer, and every yes-instance of the packed source has a canonical shared-quotient witness with both ordinates integral.

## 4. Exact remaining obstacle

All signed rounding, prefix-size, coprimality and canonical-witness issues for this particular merger have now been resolved. The only extra hypothesis in the soundness theorem is k,H in Z. Proving only one of these integrality conditions is not sufficient by the preceding arguments. For example k in Z implies the common reduced denominator of h,j divides M^2; at each prime of that denominator cF is a unit and H has negative valuation. Integrality of H alone similarly bounds the common denominator by |cF|, not necessarily 1. No implication ruling out these remaining primes is asserted. The split-prime obstruction of v148 shows that neither of the two rational norms plus a fixed affine shared certificate alone can establish the unrestricted joint ordinate integrality by a purely local argument. A new arithmetic constraint or a different source is still needed.

The preferred v150 compiler keeps both separate integer certificates and the original signed binomial block. This note is a checkpoint, not a seven-integer bound. The finite rational-arithmetic verifier checks the signed perturbation bounds for representative parameter grids; it does not establish the missing integral-ordinate implication.
