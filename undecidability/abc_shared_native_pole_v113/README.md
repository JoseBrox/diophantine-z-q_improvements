# One selectively gated native pole for the 557-variable quartic

**519 existential rational variables and 466 quadratic residuals**, under ordinary rational abc, the same retained arithmetic premises as v112, and the same external Jones coding theorem. Twelve native poles become one; all twelve integer certificates remain. The sufficiently large fixed odd height coefficient may increase. No unconditional undecidability or global minimum is asserted.

## Shared derivative and good primes

Keep every non-pole equation of [v112](../abc_aggregate_theta_v112/README.md), including its common reference and numerator points, theta deletion, and all inverse contacts c_i and u_i=1/c_i. Use the same a=M^4+432, eight-shift polynomials G_i(t), x=M^4-z, y=M^4+z and F_i=G_i(x)G_i(y) as [v109](../abc_aggregate_contacts_v109/README.md). Write k=12, G=product G_i, F=product F_i. Introduce u by u sum_i c_i=k. The retained equations imply c_i=-F_i'/(16 F_i), prime denoting differentiation in the common center at fixed slope. Thus u=-16k F/F', with F'!=0. No contact factor vanishes by the v109 proof.

For each i there is a set R_i of primes with both v_p(u)=v_p(u_i)=1 and

    log product_{p in R_i} p >= (193/100) h(M)-O(1).

Indeed choose x of larger height. The v63/v110 simple-prime lemma for degree-eight G_i(x) gives (8-4-2epsilon)h(x)-O(1). Outside the fixed exceptional set its simple prime is a simple prime of G(x). If M has negative valuation, the other argument is nonintegral; the derivative summand G'(x)G(y) has strictly smaller valuation than G(x)G'(y), also for G_i. If M has positive valuation, the other argument has no zero by the exclusion of all pair sums modulo p. If M is a unit, discard multiple-prime support of G(y), costing (2+epsilon)h(y)+O(1), independent of its fixed degree. When G(y) is a unit both quotients have valuation one. Otherwise G(y) has one simple factor. Failure of global derivative valuation one requires p^2 dividing 2M^4+d+d' for a pair of shifts d,d' of G; discard multiple-prime support of the product over distinct nonzero pair sums, costing (2+epsilon)h(M)+O(1) by v63. All surviving primes have global valuation one. If the other simple factor belongs to another group, the i-th quotient has valuation one since G_i(y) is a unit; if it belongs to i, every other group is a unit in both slots and the same derivative calculation applies to F_i. Take epsilon=1/100 and 2h(x)>=4h(M)-log 2. The asserted lower bound follows, with fixed exceptions, uniform in B and the tuple. Zero arguments are treated by the larger-height slot as in v81/v109; bounded heights are absorbed into the additive constant. This is the v110 cross-contact analysis with the eight-shift groups of v109.

## Scalar gate and pole

Let d_i be the retained scaled norm-error coordinate at suffix 42, i.e. d_i=D_{s,i}=u_i D_i in v81 notation, where D_i is the old physical norm error. Define

    A_i u = u^2 + u_i^2,
    S_i = d_i^2, H_i = A_i S_i,
    V_i (1+H_i) = S_i,
    u (W_i-1) = V_i^2,
    W = product_i W_i,
    alpha = u + (W-1)^2,
    tau (1+alpha) = alpha,
    b = 7 u^(-1) tau^2.

Here u!=0; if 1+H_i=0 the V_i row forces S_i=0 and then H_i=0, a contradiction. The tau row excludes alpha=-1. The five scaled native pole equations are those of v81 with the global c=sum c_i/k and u=1/c. The b_s=7 tau^2 register and seven additional native-pole registers realize the physical input b. The two scaled square rows are multiplied by k for integral coefficients.

For odd nu=v_p(u), the summands of alpha have different valuation parity (zero summands are allowed). Hence alpha,tau!=0 at such a prime. If nu<0, v_p(alpha)<=nu<0, tau is a unit and v_p(b)=-nu>0 for p!=7, independent of all V_i and W_i. If nu>0, the pole obstruction and the original v81 normalizer argument give v_p(alpha)>nu/2. At nu=1 this implies v_p(W-1)>0. Every W_i has valuation min(0,2v_p(V_i)-1) with no cancellation. Since W is a unit every W_i is a unit and every V_i has positive valuation.

At a prime in R_i both u,u_i have valuation one, so v_p(A_i)>=1, with cancellation permitted. If d_i!=0 and v_p(d_i)<=0,

    v_p(V_i)=2v_p(d_i)-v_p(1+A_i d_i^2)
       <=max(2v_p(d_i),-v_p(A_i))<=0,

contradiction. If d_i=0 the desired positive valuation is infinite. Thus v_p(d_i)>0 and v_p(D_i)=v_p(c_i d_i)>=0. The soundness calculation of v81 applies: its bound v_p(D_i)>-3/4 suffices for a successful slot of the four-test expression, yielding local integrality of X_i and a prime divisor of X_i(m_i-X_i). No further individual pole condition is used in this extraction.

If X_i is neither 0 nor its integer label m_i, the numerator-product estimate bounds log product R_i by 2h(X_i)+log(1+|m_i|). The unchanged v109 strict height margin, leaf/tree inequalities and trace bound then bound h(M) uniformly in B, contradicting M>=B for sufficiently large B. All X_i are integers. The lower bound on R_i also ensures nonempty R_i at large B, so alpha,b are nonzero in every solution. No extra nonzero variable is required. The v112 source-instance soundness follows.

## Ordered completeness

Use the v109/v112 ordered point and contact choices for the integer witnesses. At the prime selected for i, v_p(u)=v_p(u_i)=1 and v_p(u_j)<=0 for j!=i, because the other F_j are units and their derivatives integral. All u_j are nonzero globally by the retained equations. The v81/v103 successful-slot proof gives v_p(D_i)>0, hence v_p(d_i)>0. Now A_i has valuation >=1, so the denominator of V_i is a unit and V_i has positive valuation. For j!=i, v_p(A_j)=2v_p(u_j)-1<=-1 is odd. The denominator summands have different parity, so v_p(V_j)=max(2v_p(d_j),-v_p(A_j))>=1, also for d_j=0. Consequently W_j=1 modulo p for all j, W-1 has positive valuation, alpha has valuation one, and b has valuation one.

At the fixed prepared places and real infinity u_i~u~z^2/a, and the original norm-error estimates give d_i=O(c_i)=O(a/z^2) uniformly on the retained bounded point neighborhoods. Therefore A_i~2u, H_i and V_i tend to zero, W tends to one and alpha~u. In particular all new divisor conditions hold at sufficiently large real slope and sufficiently deep prepared local slopes. These preparations precede prime selection and are preserved by the common reference/numerator CRT. At two the v109 square-class preparation a in Q_2^{times 2} gives b in 7 Q_2^{times 2} of arbitrarily large positive even valuation; at seven b has positive valuation. Really 0<b<1 for sufficiently large slope.

At a nonselected prime outside the finite preparation set with integral slope, F is a unit, giving v_p(u)<=0. At negative slope valuation, a is a unit and the leading derivative coefficient gives v_p(u)=2v_p(z), even. All negative odd valuations are harmless by the new alpha normalizer, independently of point denominators. At even valuations b has even valuation outside seven. Thus b has square denominator and the requisite real and dyadic preparations. Apply the same published-pole completeness theorem of v81 used in v109, now just once. All other v112 rows remain unchanged. This supplies the required source-instance projection without asserting full auxiliary-zero-set equivalence.

## Exact count and replay

Remove ten coordinates (suffixes 33–41 and 56) and eight rows from each of twelve old pole blocks. The retained 386 rows are untouched. Add one reciprocal u, five coordinates per group A_i,S_i,H_i,V_i,W_i, eleven product registers, alpha,tau and eight native-pole registers. This is 82 coordinates and 80 rows, giving 557-120+82=519 and 482-96+80=466. All residuals have integer coefficients and degree at most two; their sum of squares has degree exactly four.

The builder checks all removed-coordinate occurrences, all retained equations by variable name, full support and degrees, and exact census. Run node build.js. Its exact checks were executed on the frozen predecessor before commit. No full repository regression or independent proof of inherited arithmetic premises is claimed.

References: [v109](../abc_aggregate_contacts_v109/README.md), [v110](../abc_selective_pole_v110/README.md), [v81](../../papers/quartic_existence/paired_contact56_20261119_v81.tex), [v103](../abc_common_numerator_v103/common_numerator.tex).
