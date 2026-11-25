# v151: global rational counterexamples to the shared Pell sum

**The joint integrality implication proposed in v148/v150 is false.** This is an unconditional arithmetic obstruction to that proposed source modification, not just a split-prime local example. For every packed prefix with a power-of-two base and false central-binomial divisibility, one can satisfy the entire redesigned rational Pell block, including the actual rational triangular margin rows, while certifying only the sum L=h+j (and the other retained source integers). Neither small nor third ordinate need be integral. In particular this merger cannot give a seven-integer transfer. The preferred v150 compiler is unaffected: it still certifies both h and j individually.

## 1. A global genus-one lemma

Let A,D be positive integers (more generally positive rationals), let beta be a nonzero rational, and let k0,t0 be integers with

    t0^2 = 1 + A*k0^2.

Suppose there is an unbounded progression of positive integers v such that

    H_v=Y_v(G), I_v=X_v(G), D=G^2-1, G>=2,

for a fixed integer G, and that v can be restricted to v congruent to one fixed starting exponent v0 modulo an arbitrary further fixed multiple of the original progression step. This last property is automatic for an arithmetic progression. The Pell sequences are defined by

    X_n(G)+Y_n(G)*sqrt(G^2-1)=(G+sqrt(G^2-1))^n.

For each such v form the projective intersection of two quadrics C_v in coordinates [K:T:I:W]:

    T^2 = W^2 + A*K^2,
    I^2 = W^2 + D*((H_v+beta*k0)*W-beta*K)^2.                 (1)

Write O_v=[k0:t0:I_v:1] and Q_v=[k0:t0:-I_v:1]. For all sufficiently large v, H_v+beta*k0 is nonzero. Then C_v is a geometrically integral smooth genus-one curve over Q. There is an infinite subprogression, with at most finitely many exceptions, on which Q_v is a non-torsion point of C_v with O_v as origin.

**Proof of smoothness and genus.** Set W=1 and consider the degree-four cover of the K-line defined by the square roots of

    f(K)=1+A*K^2,
    g_v(K)=1+D*(H_v+beta*k0-beta*K)^2.

Both have two simple roots over the algebraic closure, and they have no common root: a root of f has real part zero, while a root of g_v has real part (H_v+beta*k0)/beta, which is nonzero. The two square classes are independent, because their simple root sets are disjoint. Thus the cover is geometrically connected. At each of the four branch values there are two points of ramification index two, and there is no ramification at infinity. Riemann-Hurwitz gives 2g-2=4*(-2)+8=0. Alternatively adjunction for the smooth intersection of two quadrics gives genus one. At a finite point, the two Jacobian rows are independent unless both square-root coordinates are zero or the root of one of the two quadratics is multiple; both are excluded. At infinity K is nonzero, and both T,I are nonzero, so the Jacobian rows are independent there as well. In particular (1) is the smooth projective model, and the rational point O_v makes it an elliptic curve over Q.

**Good reduction at a new prime of I_v.** Write t0^2=1+A*k0^2 and define the fixed rational constant

    B_* = (beta^2*D*t0^2 - 4*A)^2
          + 16*A^2*k0^2*beta^2*D.

This is strictly positive if k0!=0; if k0=0, assume beta^2*D!=4*A instead. All applications below have k0>0. Let S consist of 2, the primes dividing t0, and the primes at which any of A,D,beta,B_* is not a unit. This is a finite set independent of v. Let p outside S divide I_v. Then D*H_v^2=-1 mod p, so H_v is a unit. The two roots of g_v modulo p are precisely

    k0, k0+2*H_v/beta.

At the first, f(k0)=t0^2 is a unit by choice of S. If f at the second vanished, expansion would give

    0 = beta^2*D*t0^2 - 4*A + 4*A*k0*H_v*beta*D mod p.

Squaring after moving the last term to the other side, and using D*H_v^2=-1, would imply B_*=0 mod p, a contradiction. Thus f,g_v have disjoint simple root sets in the algebraic closure of F_p. The same Jacobian and genus argument applies to the reduction of (1), including infinity. The displayed model over Z_p is smooth and proper: it is the finite locally free cover of P^1 obtained by adjoining the two indicated square roots in the degree-one line bundle (on either standard affine chart each square equation is monic, and the four monomials 1,T,I,TI form a basis in its trivialization). Smooth geometric fibers give smoothness over the DVR. Its section O_v makes it a good reduction model of the pointed genus-one curve.

Since p divides I_v but p does not divide t0, Q_v and O_v are distinct rational points which reduce to the very same point modulo p. The kernel of reduction on an elliptic curve with good reduction over Q_p is torsion-free for odd p: its formal parameter has integral depth at least one, which is greater than 1/(p-1), so the formal logarithm is an injective homomorphism to the additive group p Z_p. Equivalently use Silverman, *The Arithmetic of Elliptic Curves*, second edition, IV.6.4 and VII.2.2 (see also VII.3.4 for the torsion-depth bound). Therefore Q_v has infinite order. This uses no conjecture about ranks, prime patterns, or the rational points of the project's separate carrier curve.

**Existence of a new prime.** Fix the initial v0 in the progression. For each p in S write e_p=v_p(X_v0(G)). The matrix

    [[G,G^2-1],[1,G]]

has determinant one, so has finite multiplicative order modulo p^(e_p+1). Restrict the progression to v=v0+n*T with T a positive multiple of its original step and all these orders. Then X_v(G)=X_v0(G) modulo p^(e_p+1) for every p in S. Thus the entire contribution of S to X_v(G) is fixed. Since X_v(G) increases without bound as n tends to infinity, every sufficiently large term has a prime divisor outside S. For those terms the preceding argument proves non-torsion. This proves the lemma without needing a primitive divisor theorem or a prime-density assertion.

## 2. Real approximation with dyadic integrality

In the applications t0>0 and I_v>0. For every real K the affine point

    (K, +sqrt(1+A*K^2),
        +sqrt(1+D*(H_v+beta*k0-beta*K)^2))

is defined, and as K varies it lies on a continuous path in the real component containing O_v. Thus the entire positive-sign affine branch is in the identity component of the pointed curve. That component is a circle, as for every real elliptic curve.

Fix any prescribed nonempty real open interval J for K and any 2-adic neighborhood of O_v. Since C_v is projective, C_v(Q_2) is compact; the elliptic formal group at its identity has open subgroups contained in arbitrarily small neighborhoods (this also holds at bad reduction by using a sufficiently deep formal parameter). Choose such an open subgroup U_2 inside the prescribed neighborhood. Its index is finite by compactness. A suitable positive multiple m*Q_v lies in U_2; by also multiplying by 2 it lies in the real identity component. This point still has infinite order, since a torsion relation over R would already be a torsion relation over Q. Its multiples are dense in that real circle and remain in U_2 at 2. Consequently infinitely many rational points of (1) have K in J, on the positive-sign real branch, and are as 2-adically close to O_v as prescribed.

On a bounded interval J, both K and H=H_v+beta*(k0-K) range over bounded intervals. The condition K in Z or H in Z excludes only finitely many rational points there (each value of either ordinate determines the other and leaves at most four sign choices). So one may require **both K and H nonintegral**, avoid any finite collection of additional forbidden values, and require arbitrary strict real inequalities satisfied in an open neighborhood of a point on the branch. Since k0,H_v are integers, one may in particular require K,H in Z_2. No use of the Mordell-Weil theorem, Siegel's theorem, or weak approximation on arbitrary elliptic curves is made: all approximation is by multiples of a proved infinite-order point in the compact groups.

## 3. Application to the full proposed v148/v150 merger

Recall the [v148 core](../shared_pell_core_v148/README.md) and [v150 signed rounding](../shared_pell_rounding_v150/README.md). Fix any actual packed prefix with b a power of two, M>=16, M>=4b, M even, r>=1, 3|Mr, B=2r+1, and b|2^B. The hypotheses hold in particular for the v145/v150 packed prefix with f=1, b=4, g=0. We do NOT assume M divides binomial(2r,r). Choose

    w=2^B/b, s=1, U=wM, Y=sM,
    a=(U+1)*r*Y, P=1+2*U*r^2*Y^2.

All are positive integers. Set c=Y_B(a), d=X_B(a). The retained shifted-trace congruence is satisfied with a positive integer gamma:

    d-(a-2)c=bw+(4a-5)*gamma.

Indeed the recurrence for R_n=X_n(a)-(a-2)Y_n(a) is R_(n+1)=2R_n+(4a-5)Y_n(a), R_0=1, and bw=2^B. The halftrace square has witness zeta=2X_(r+1)(a) by the addition/doubling identities. The first norm is automatic, and c>B and c>a. This stage does not depend on the truth of the binomial divisibility.

Choose a sufficiently large positive integer q divisible by both c and the order of the norm-one Pell matrix at a modulo M*c^2. Then

    F=X_q(a), i'=Y_q(a)/(M*c^2)

are positive integers, and the redesigned second norm F^2-(a^2-1)*(M*i'*c^2)^2=1 holds. We have gcd(c,F)=1, c|q by choice of q, and F^2=1 mod c. Put G=a+F^2*(c+1-a)>=2.

The v95 third-Pell congruence construction applies to every v=B+4q*l, l a nonnegative integer:

    H_v=Y_v(G), I_v=X_v(G),
    j_v=(H_v-c-F^2*(B-c))/(cF) in Z.

To recall the exact argument, G=1 mod c and G=a mod F. Thus H_v=v=B mod c (using c|q), and H_v=Y_v(a)=Y_B(a)=c mod F by the period 4q modulo X_q(a). The numerator defining j_v is divisible by both c and F, which are coprime. Positivity of j_v follows for sufficiently large l. No margin assumption is used.

For the small norm take the integral starting witness

    k0=Y_(r+1)(P), t0=X_(r+1)(P),
    h0=(k0-r-1)/M^2 in Z,

since P=1 mod M^2. Both k0,t0 are positive, and h0>0 by the size of P. Although the binomial margin need not hold at k0, this gives a rational origin for each shared-sum curve. Fix one sufficiently large v from section 1 with A=P^2-1, D=G^2-1, beta=cF/M^2. Fix the certified integer

    L=h0+j_v > 0.

For arbitrary rational k,T,I on (1), set

    H=H_v+beta*(k0-k),
    h=(k-r-1)/M^2,
    j=(H-c-F^2*(B-c))/(cF),
    tau=T.

The definitions give h+j=L exactly. Both Pell norms, both congruence rows, the unchanged first and second norms, and every preceding packed-source equation are satisfied by construction.

At real k*=c/Y, the strict margin polynomial eta=k^2-4(c-kY)^2 equals (c/Y)^2>1. Choose a bounded open interval about k* on which eta>1. Use section 2 to find a rational point of (1) with k in that interval, k,H both nonintegral, and k,H in Z_2. The original triangular margin rows admit rational witnesses, not just a real inequality: eta is 2-adically integral, so 8eta-5 is positive and lies in 3+8Z_2. Write 8eta-5=A0/B0 in lowest terms with B0>0 odd. Then A0*B0 is a positive integer congruent to 3 modulo 8. Legendre's three-square theorem gives A0*B0=z1^2+z2^2+z3^2 with integers zi. Consequently 8eta-5=sum_i (zi/B0)^2; setting u_i=(zi/B0-1)/2 gives precisely

    2*(eta-1)=sum_i u_i*(u_i+1).

These are the retained margin equations, after the normal quadratic helper definitions. All remaining positivity/nonzero conditions are met by the canonical fixed prefix and by the strict real interval. If desired avoid the finitely many k-values where h=0 or j=0. The proposed certified tuple f, g+1, w, s, gamma, i' (or an appropriate shifted nonzero target), L has the required nonzero values in the packed case; only these integers need certification. The omitted h and j are nonintegral because their defining ordinates are nonintegral and their coefficients and offsets are integers.

In particular for each no-instance on the packed cofinite tail, choose f=1, b=4, g=0 as in the v144 obstruction (or any admissible power-of-two base with false digit tuple). The v142/v145 carry equivalence gives M not dividing binomial(2r,r). The construction above gives a full false rational outer source witness with the shared integer L. The same simultaneous integer-tuple realization used by the transfer supplies the hypothetical smaller tuple of nonzero targets under its retained premises. Thus the proposed shared-sum redesign is not merely unable to force integrality: it admits false instances. This is an obstruction to the **proposed** v148/v150 modification, not a claim that the preferred v150 quartic is unsound.

## 4. Scope and more general fixed linear mergers

The proof works without any coprimality of the small and third congruence moduli. In particular, it applies also to the original positive small parameter p and modulus p-1, using its canonical starting k0=Y_(r+1)(p), or to any nontrivial fixed integer affine certificate L=a1*h+a2*j+a0 with a1*a2!=0. Keep the canonical integral starting witnesses and use beta=(a1/a2)*cF/modulus in (1). The fixed B_* is still positive for k0>0. Choose v sufficiently large so H_v+beta*k0!=0 and the certified affine value is nonzero. The same proof varies k on the genus-one curve while keeping that certified integer constant. This establishes a global counterpart of the local affine obstruction in v148. It does NOT rule out nonlinear mergers, additional arithmetic constraints, a different coding source, or a seven-integer construction by some other means.

The crucial distinction from v150 is that its conditional rounding theorem assuming both ordinates integral remains correct in its stated domain; the desired removal of that assumption is false. A successful future source must do something other than replacing two independent congruence certificates by this sum, or must add genuinely restrictive equations which eliminate the genus-one deformation without losing canonical completeness.

## Reference and verification scope

The genus-one and non-torsion proof above is exact and works on arbitrarily large actual packed instances. The only external arithmetic results used are the classical elliptic formal-group/reduction theorem (Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed., IV.6.4, VII.2.2 and VII.3.4), Riemann-Hurwitz, the established v95 Pell identities, and Legendre's three-square theorem. No numerical computation of the astronomical canonical third-Pell witness or of a universal-source rational zero is claimed. The independent [verify.mjs](verify.mjs) checks the disjoint-branch obstruction, a small exact good-reduction profile, a rational nonintegral point obtained by an osculating quadratic on its quartic model, and the finite-prime freezing of the third exponent. These checks are supplemental to the proof, not evidence replacing it. The numerical example is for the general genus-one lemma, not a numerical instantiation of the full packed source.


### Small exact illustration of the genus-one mechanism

For A=D=3, beta=1, k0=1, t0=2, G=2 and v=2, the fixed-sum curve is

    T^2=1+3*K^2, I^2=1+3*(5-K)^2.

It has origin (1,2,7). At the good prime 7 its point (1,2,-7) reduces to the origin. The fixed exclusion constant B_*=432 is a unit at 7. An explicit nonintegral point is

    K=1952365/331837, T=-3397838/331837,
    H=-293180/331837, I=-606613/331837.

Here K+H=5 and both norm residuals vanish exactly. This follows from the rational conic parameter K=2t/(1-3t²), T=(1+3t²)/(1-3t²), and the quartic
F(t)=(1-3t²)²+3(5(1-3t²)-2t)². Its osculating quadratic Q(t)=(-8931t²-1200t+2993)/343 at t=1/3 satisfies

    F(t)-Q(t)^2=15(3t-1)^3(1751t+1115)/117649.

The fourth root t=-1115/1751 yields the displayed point with I=Q(t)/(1-3t²). The abstract non-torsion and approximation proof, rather than this small illustration, supplies the full packed-source obstruction.
