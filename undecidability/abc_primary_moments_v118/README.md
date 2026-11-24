# Global primary moments and shortened alternate tests (373 variables)

**Theorem.** Under exactly the arithmetic and external Jones coding hypotheses of [v117](../abc_boolean_reciprocal_v117/README.md), the twelve-input transfer admits the quartic specified here, with **373 variables and 322 quadratic residuals**. The sufficient fixed odd shift remains ineffective.

## 1. Contact and denominator exclusions

Retain the v117 reciprocal charts, height tree, and shared coefficient circuit, but change the common center to a=M^32+784. The positivity, distinctness and dyadic square preparation follow verbatim from v115: the nonzero valuations of M^32 are separated from v2(784)=4 by at least 4, while for a unit M, M^32+784 is 1 modulo 8.

For each group the proof of v115, with exponent 32 rather than 8, now gives log R_i >= (2851/100)h(M)-O(1): the simple/multiple-prime bound is (8-6-3/100)max(h(x),h(y))-(3+1/100)h(M)-O(1), and max(h(x),h(y)) >=16h(M)-O(1). As before each retained prime has v(u)=1, at most two active groups, all active normalized weights omega_i=au*r_i units and their sum 12.

Further discard all primes dividing any reduced denominator of any of the twelve inputs X_j. The logarithmic cost is at most sum h(X_j) <=12C h(M)+O(1), where C=(1001/997)^4 by the unchanged fourth-power tree. Thus the new R_i satisfy
```
log R_i >= (2851/100-12C)h(M)-O(1).
```
The exact absorption inequality 2851/100>14C is checked by the compiler. At every retained prime all twelve rational inputs are integral, even when they are not integers globally. The exceptional-set enlargement here is a height-accounted exclusion, not a restriction on rational zeros.

## 2. Common selector and bounded primary ratio

As in v117, write f_H,f_U,f_HP for the three common reciprocal abscissas, and C0=h_U/h_H. Replace the three separate selectors by
```
R=c*f_H^2+c^2*f_U^2+c^3*conj(f_HP)^2,
chi0=1/(1+R).
```
At a retained prime the terms of R have distinct nonzero valuation classes modulo four, since each finite reciprocal abscissa valuation is even. Hence R has positive valuation exactly when the three formal conditions hold, and otherwise negative valuation. The selector chi0 is integral and Boolean, with residue 1 in the successful case. At most one slot can succeed, as in v117.

Let
```
eta=1/(1+u*C0^2),
Cbd=C0*eta, chi=chi0*eta.
```
At v(u)=1 the denominator of eta has unequal-parity terms. Thus eta is integral, with residue 1 exactly for integral C0, and residue 0 otherwise. The bounded primary ratio Cbd is always integral: if v(C0)<0 its valuation is -1-v(C0)>=0, otherwise it is v(C0). At a selected slot with chi=1 modulo p, C0 is integral and Cbd=C0 modulo p. These statements also cover C0=0. All fraction definitions are quadratic after storing C0^2: the row for eta is eta*(c+C0^2)=c.

## 3. Alternate tests and two moments

Use I_i=conj(L_i)-X_i, Fhat_i=c*f(V_i), and
```
I2_i=I_i^2, J_i=I2_i^2+conj(Fhat_i)^2,
D_i=J_i/(u+J_i).
```
The valuation classes of the two terms of J_i are 0 and 2 modulo 4, because Fhat_i has odd valuation when nonzero. In particular they do not cancel at finite equal valuations and v(J_i) cannot equal 1. Each D_i is integral, has Boolean residue, and vanishes modulo p exactly when v(I_i)>=1 and v(conj(f(V_i)))>0. Thus the private detector uses three field registers rather than four.

Define
```
Z0=1-Tr(chi)+au*Tr(chi*sum r_i*D_i),
Z1=au*sum r_i*X_i-12*Tr(chi*Cbd),
Z2=au*sum r_i*X_i^2-12*Tr(chi*Cbd^2).
```
All three are integral at every retained prime: this includes inactive group terms because every X_i and D_i is integral and every normalized weight is integral. As in v117, Z0=0 modulo p forces a unique selected slot and successful alternate tests for every active group.

The remaining two equations Z1=Z2=0 modulo p force every active X_i to equal C0 in the selected residue field. If one weight is active this follows from Z1. For two active weights a,b and errors E,F, these equations imply aE+bF=0 and aE^2+bF^2=0 (subtract the first moment times 2*C0 from the second). Substitution gives a(a+b)E^2/b=0; all factors a,b,a+b=12 are units. Hence E=F=0. This is valid at colliding contacts and makes no assumption about the signs of real weights.

To combine the three tests use
```
Z=Z0^4+c*Z1^2+c^2*Z2^4,
alpha=u+Z^2.
```
The three summands of Z have valuation classes 0, odd, and 2 modulo four. Therefore v(Z)>0 is equivalent to positive valuation of each Z_j. The unchanged native pole and tau equation force v(alpha)>1/2 at every retained prime, hence v(Z)>0. We recover every primary and alternate local comparison at the active groups. The v117 formal-logarithm argument gives X_i=m_i modulo p. Applying the new radical bound and strict absorption inequality to each i proves all X_i integral, exactly as in v115.

## 4. Completeness and the fixed-place preparation

For canonical integer witnesses retain the same ordered v115/v117 choice of differences, trace, height center, primes, common reference and numerator. At each selected prime the successful slot has C0 integral and congruent to the assigned X_i; both alternate conditions hold. Thus chi=1 there, every other group is inactive, and each of Z0,Z1,Z2 is zero modulo p. This gives v(alpha)=1 and v(b)=1.

At fixed prepared places and real infinity choose bounded point neighborhoods with nonzero C0, which is possible by avoiding finitely many fibers as in v115. The raw reciprocal ordinates, ratios and f-values are bounded. As the absolute slope tends to infinity, u~z^2/a, c~a/z^2, chi0 tends to 1, eta tends to 0, Cbd tends to 0, each J_i remains bounded, and each D_i tends to 0. The weights au*r_i tend to 1. Consequently Z0 tends to 1, Z1 and Z2 remain bounded, and Z remains bounded; alpha~u and b~7c. All divisors are nonzero in sufficiently small fixed-place neighborhoods. The real and dyadic BB preparation and the other valuation parities are precisely those in v117, since alpha is still u plus a rational square. The native pole supplies the remaining witnesses. No point is chosen anew after the prime and CRT stages.

## 5. Exact census

The compiler preserves all 52 Jones rows in 76 outer variables. It uses 130 point/input-square registers, 29 height registers, 29 contact registers, 14 common detector registers, 72 private detector registers, and 23 aggregation/pole registers. There are 270 new quadratic residuals. Run `node build.js` to regenerate or check the exact table; the compiler checks every original outer equation by named monomials, exact contact coefficient expansions, the new strict height margin, full support, 7973 valuation cases and 940 weighted Boolean cases. The arithmetic projection proof is above; these finite checks are not a proof of the imported arithmetic premises.
