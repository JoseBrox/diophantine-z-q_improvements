# Why three of the eight certificates cannot simply be dropped (v144)

This is an obstruction investigation, **not** a six- or seven-integer construction or a general lower bound. In the packed source of v142/v143, deleting the integrality requirement on any one of h, j, i_half, without a replacement condition, destroys soundness of the source projection. The result is stronger than a local counterexample to the Pell index lemma: it applies to the full packed binomial source for every no-instance on the cofinite tail. For the transfer to rational quartics, retain the same arithmetic premises and the already proved simultaneous completeness for the smaller tuple of nonzero targets. These counterexamples do not require arithmetic assumptions in the source itself.

## 1. A fixed false prefix

Fix any no-instance of the inner natural-number source. Choose f=2^e with e>=1, b=f^2=4^e and g=0 in the v142 prefix. All guards and definitions hold. Since there is a nonzero constant in the source, the zero digit tuple is not a solution, so the carry equivalence gives M not dividing binomial(2r,r). We have r>=N^2-1, M>=4b, and 3 divides Mr. Set

    B_idx=2r+1,
    w=2^B_idx/b,

a positive integer (B_idx is greater than the base-two exponent of b). Take an arbitrary positive integer s for now. Write Y=sM, U=wM, a=(U+1)rY, p=2Ur^2Y^2. Thus a is a positive multiple of three, p is even and both exceed one.

As usual define X_n(A)+Y_n(A)*sqrt(A^2-1)=(A+sqrt(A^2-1))^n. Use n as index here; the variable Y without subscript is sM.

## 2. Deleting h: rational small-Pell points fill the forbidden interval

Choose the canonical first norm c=Y_B_idx(a), d=X_B_idx(a), and positive gamma=(d-(a-2)c-bw)/(4a-5). Integrality and positivity of gamma follow from the v101 recurrence for R_n=X_n-(a-2)Y_n, R_(n+1)=2R_n+(4a-5)Y_n. Choose a positive integral odd i so that the second norm is satisfied, and the positive integral j in v95's completeness theorem. Explicitly an odd multiple of B_idx*c can be used as the second index: c is odd, c^2 divides the corresponding Y value by the Pell multiplication formula, and the quotient i is odd. Choose the multiple sufficiently large that i_half=(i-1)/2>0. The first half-trace square is supplied by the half-index of B_idx+1.

Now allow h rational, keeping all the other six certified integer values and the prefix fixed. The small-Pell conic has the rational parametrization

    k = 2v/(1-(p^2-1)v^2),
    tau = (1+(p^2-1)v^2)/(1-(p^2-1)v^2).

On 0<v<1/sqrt(p^2-1) it covers all positive real k. The target k=c/Y is greater than one (c>=a^2-1 and a>=2Y). Choose a real open neighborhood where eta=k^2-4(c-kY)^2>1. At the place 2 choose v near 1/(p+1), where k=1 and tau=p, so that k is 2-adically integral. Weak approximation on Q gives a rational v in both open sets, avoiding the pole. In particular eta is 2-adically integral. The positive rational 8eta-5 is congruent to 3 modulo 8 in Q_2. It is a sum of three rational squares: its reduced denominator is odd, and after clearing that denominator by its square the positive integer is 3 modulo 8, so Legendre's three-square theorem applies. Writing the three squares as (2u_i+1)^2 gives exactly the three rational triangular witnesses for 2(eta-1)=sum_i u_i(u_i+1). Thus the actual positivity rows, not just an inequality, hold.

Set h=(k-r-1)/(p-1). This is rational and satisfies every remaining binomial row. It cannot be an integer: if it were, the v101/v95/v106 soundness argument would give the false binomial divisibility. In particular h is nonzero. Thus omitting its certificate gives a full false source witness, even if a separate nonzero guard on h were kept.

## 3. Two distinct real Pell units allow wrong indices

For the next two omissions, choose s so that the quadratic fields Q(sqrt(a^2-1)) and Q(sqrt(p^2-1)) are distinct. Here a=A0*s, p=P0*s^2, with A0=(U+1)rM and P0=2Ur^2 M^2, so P0/A0^2=2U/(U+1)^2 lies strictly between zero and one. Choose an odd prime q not dividing A0*P0*(A0^4-P0^2), and choose s with A0*s=1 mod q but not mod q^2. The other factor A0*s+1 is a unit at q. Then v_q(a^2-1)=1, whereas p^2-1 is a unit at q. Such s can be chosen positive. The square classes differ, proving the assertion.

The units alpha=a+sqrt(a^2-1) and beta=p+sqrt(p^2-1) have irrational logarithm ratio. Otherwise a nontrivial positive power of one equals a positive power of the other, and that common value belongs to the intersection Q of the distinct quadratic fields. Quadratic conjugation in either field sends the value to its reciprocal, contradicting that it is greater than one.

Let o be the multiplicative order of 2 modulo 4a-5 (the modulus is positive odd). Choose indices

    t=B_idx+2o*n,   l=r+1+(p-1)*m,   n,m>=0.

The elementary density of irrational rotations gives arbitrarily large n,m with t log(alpha)-l log(beta) in any prescribed open interval. Indeed the fractional parts of n*(2o log(alpha))/((p-1)log(beta)) are dense and recur in any open subinterval; for such n choose the corresponding integer m, which grows with n. As t,l tend to infinity,

    Y_t(a)/Y_l(p)
      = [sqrt(p^2-1)/sqrt(a^2-1)] * alpha^t/beta^l
          * (1-alpha^(-2t))/(1-beta^(-2l)).

Choose an interval of log-ratios giving a ratio strictly between Y-1/4 and Y+1/4, with room at both ends for the correction tending to one. This yields arbitrarily large wrong odd indices t>B_idx and l, with

    c=Y_t(a), d=X_t(a), k=Y_l(p), tau=X_l(p),
    |c/k-Y|<1/4, eta>3k^2/4>1.

All four are positive integers. The small quotient h=(k-r-1)/(p-1) is positive integral since Y_l(p)=l mod p-1. The first trace quotient gamma is positive integral since R_t=2^t=2^B_idx=bw mod 4a-5. The half-trace square exists because t is odd: zeta=2X_((t+1)/2)(a). The margin is a positive integer, and its actual triangular rows have witnesses. This shows that keeping both small-Pell and shifted first-trace congruences cannot alone recover the intended index.

## 4. Deleting j or i_half

With the wrong-index witnesses of section 3, choose i positive odd and the second norm as in section 2 but using an odd multiple of t*c. This provides F>1 integral and i_half>0 integral. Put

    G=a+F^2(c+1-a),
    j=(F^2(c-B_idx)-c)/(cF), H=0, I=1.

This positive rational j satisfies the literal third-Pell rows. It is not an integer, either by the v95 index theorem (t!=B_idx) or directly because H=c+F^2(B_idx-c)+cFj is congruent to B_idx modulo c whenever j is integral. Therefore deleting j's integrality predicate gives another full false source witness.

Alternatively keep j integral and delete i_half's predicate. Take F=1, i=0, i_half=-1/2, E=0. The second norm is satisfied, and the shifted input target i_half+1 remains nonzero. Now G=c+1, and take H=Y_B_idx(c+1), I=X_B_idx(c+1), j=(H-B_idx)/c. This j is positive integral by the recurrence modulo c. The other wrong-index witnesses, including h,gamma, and all prefix and margin rows are unchanged. Thus deleting i_half's integrality predicate without separately excluding its new zero-i branch is also unsound. This last obstruction does NOT cover a proposed replacement with a genuine nonzero-i guard and additional arithmetic constraints.

All these constructions satisfy the source rows of v143 after removing the specified certificate, with every other certified target a nonzero integer (g is shifted by one). The v136-v143 simultaneous elliptic completeness extends to seven inputs: choose the recursive scalar for this tuple, keep the same larger multiplier and fixed height constants, and prepare all comparison points and poles for just these inputs. Therefore they are counterexamples to the corresponding unmodified seven-certificate projections under the same interface premises, not a claim of numerical rational witnesses for the enormous coefficients. A six/seven-integer construction with redesigned congruences or a new binomial certificate remains open.

## 5. Checks

verify.mjs gives an exact small rational small-Pell conic fixture, a wrong-index third-Pell fixture, a square-class-separation fixture, and a zero-i third-Pell fixture. The full counterexample proofs above use weak approximation and irrational rotation, not an enormous numerical search. The fixtures check identities and the relevant nonintegrality and local conditions only. No full-CI or general minimality claim.
