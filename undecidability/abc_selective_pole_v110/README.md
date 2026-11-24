# One selective pole for all integer inputs (ordinary abc)

## Theorem

Under ordinary rational abc and the elliptic, trace, comparison, finite prime-pattern, local-preparation and recurrence inputs of the repository's v63/v88/common-numerator sources, for each fixed k>=1 there is a polynomial whose rational input projection is Z^k using **3k+8** total rational coordinates (including the k inputs). Applying the mixed-integer universal source and finite-wrapper transfer gives a **36-variable** undecidability family for unrestricted degree (k=9), rather than 52. The sufficient fixed odd coefficient B remains ineffective. No extra pole-realization premise is needed: the normalized BB product pole from v88 is used. No unconditional H10(Q) claim or quartic count is asserted here.

The novelty is a common derivative quotient and one selectively weighted detector. It does not attempt to identify the square classes of independent pole inputs.

## Rational source and all guards

Use the curve E/K, K=Q(sqrt(2)), E: y^2=x^3-(11-6sqrt(2))x, and generator P of 2E(K) from the v63 source. Use the square-abscissa point charts of that source for A_i, H and U: two rational components of h, then x=h^2, y=h j, j^2=h^4-(11-6sqrt(2)). Retain all its point, affine difference and quotient guards, for each pair H-P,U-A_i. Write A_i=[m_i]P; H,U are common. With f(Q)=1/x(Q), zeta(Q)=-x(Q)/y(Q), define Y_i=X_i^2+1, r=zeta(U)/zeta(H), r'_i=conjugate(zeta(U-A_i)/zeta(H-P)), and the six K-valued tests

    C_i = (f(H), f(U), conjugate(f(H-P)), conjugate(f(U-A_i)),
           r-r'_i, r-Y_i).

Use beta_i=Y_i^2+B, T_i=Tr x(A_i), and positive leaves M_i=beta_i^4+T_i^4. Pair successive nodes, replacing a pair L,R by L^4+R^4, carrying an unpaired node. The root is M; maximum depth is ceil(log2 k). Set a=M^4. In particular a is a rational square, independently of the dyadic trace of any individual input.

Choose k distinct primes s_i>10 (for k=9 take 11,13,17,19,23,29,31,37,41). Set S_i=s_i times {-10,-8,-5,1,2,3,4,6,7}, G_i(t)=product_{c in S_i}(t+c), G=product_i G_i. The total shifts are distinct, nonzero, have no opposite pair, and sum to zero, by primality and the properties of the nine base shifts. Increase the fixed lower bound on B, depending only on k, so a>max |c| for every tuple.

Retain a single rational slope z. Write x_-=a-z, x_+=a+z, F=G(x_-)G(x_+), F_a=partial_a F with z formally held fixed, and u=-18k F/F_a. Guard F,F_a,u,1+u nonzero. For a rational L and field test C define

    w(L)=u/(u+L^2),
    D(C)=C^2/(1+u C^2),
    V(C,L)=w(L)^2 D(C).

Use both L=G_i(x_-) and L=G_i(x_+) for every one of the six tests of input i. Set

    W=product_{i,j,side} (1+V(C_ij,G_i(x_side))^2/u),
    V0=Tr(W^(-1)),
    e=28u/((1+u)^2 V0^2),
    d=7u,
    q^2=(1-e)(v^4-d^2)(s^4-d^2).

Here v,s are the only two ordinary pole parameters. The root q is finite, not an ordinary coordinate. The only additional guards are all displayed divisors (field norms for field divisors), and e nonzero. No nonzero test or pole ordinate is required. The normalized BB product identity has e=d[2/((1+u)V0)]^2, so the pole obstruction of v88 applies. For clarity, at a negative odd valuation of e, d has odd valuation, each quartic factor has valuation min(4v_p(v),2v_p(d)) or min(4v_p(s),2v_p(d)), even because the two possible finite valuations are unequal; 1-e has odd valuation. The product cannot be a rational square. This proves the needed local obstruction directly, also for zero v or s.

## Selective valuation lemma

At every good odd unramified prime where nu=v_p(u) is odd (valuation normalized by v_p(p)=1),

    v_p(w(L))=max(0,nu-2v_p(L)),
    v_p(D(C))=max(2v_p(C),-nu).

The first equality also holds for L=0 with w=1, the second for C=0 with infinite valuation. Both follow from unequal parity of the two summands in their denominators. For nu<0, every w has nonnegative valuation, and every D has valuation at least -nu; hence W is congruent to 1 in both embeddings and V0 to 2. Then e has positive odd valuation, outside 2,7. At even nu its valuation is even outside 7.

For nu>0 odd each factor in W has valuation min(0,2v_p(V)-nu)<=0; equal summand valuations are impossible. Let Q be the maximum valuation of W over the two slots (or the single unramified place). Since v_p(V0)>=-Q, the pole obstruction forces

    0 < v_p(e) <= nu+2Q.

In a slot attaining Q every factor has valuation greater than -nu/2, hence v_p(V)>nu/4. In particular if nu=1 and v_p(L)>=1, w(L) is a unit and v_p(C)>0. Thus all six tests of every such active i are positive in the same successful slot. The original v63 formal-comparison implication gives Y_i locally integral and Y_i=m_i mod p. If both sides contact different inputs, both sets of tests are active; no exclusivity hypothesis is required for soundness.

If nu=1 and v_p(L)<=0, then v_p(w)>=1 and v_p(D)>=-1, so v_p(V)>=1. Such inactive factors have residue 1, regardless of actual poles of their raw tests. This is the key completeness mechanism.

## Enough active primes for each input

Use the two abc radical lemmas of v63 (simple-prime support for a fixed split polynomial of degree k0, and multiple-prime support for fixed nonzero pair sums at 2M^4). Work outside the fixed union of all bad primes, shift differences, nonzero pair sums, 18k and 2,7. Choose x as the larger-height of x_-,x_+, and y the other. For each i start with simple primes of G_i(x), of total logarithmic weight at least (9-4-2epsilon)h(x)-O(1). At such a prime x is integral and exactly one factor of the full G(x) vanishes simply.

If v_p(M)<0, y is nonintegral, and the first summand G'(x)G(y) of F_a has strictly smaller valuation than G(x)G'(y). Hence v_p(u)=1. Here the gate with L=G_i(x) is active even though the other slot may have negative valuation. If v_p(M)>0, y reduces to the negative of x, so the absence of opposite shifts makes G(y) a unit and again v_p(u)=1.

For M a unit, if G(y) is a unit we again get v_p(u)=1. Discard primes with v_p(G(y))>=2: their logarithmic weight is at most (2+epsilon)h(y)+O(1), **independent of the degree of G**, by the first radical lemma. If G(y) also has a simple factor, say y+c', write the two vanishing factors as x+c,y+c'. Then F_a modulo p^2 is their sum times a unit. A failure of derivative valuation one requires p^2 dividing 2M^4+c+c'. Discard the multiple-prime support of the product over all distinct pair sums, of logarithmic weight at most (2+epsilon)h(M)+O(1) by the second radical lemma. This is valid even if c,c' belong to different input blocks. It is essential to use the multiple-prime estimate rather than discard every collision prime.

Every remaining prime has nu=1 and v_p(G_i(x))=1. Call its product R_i. Taking epsilon=1/100 and using h(x)>=h(y), h(x+y)=h(2M^4)>=4h(M)-log 2, we obtain

    log R_i >= (3-3epsilon) max(h(x_-),h(x_+))
                  -(2+epsilon)h(M)-O(1)
            >= 393/100 h(M)-O(1).

These constants may depend on the fixed k and shifts but not on B or the rational solution. F nonzero ensures that neither polynomial value is zero. Zero arguments x or y cause no issue in the height estimates.

For k=9 the positive fourth-power lemma of v58, at kappa=1001/1000, gives h(beta_i),h(T_i)<= (1001/997)^5 h(M)+O(1), counting the four tree levels and the leaf. Also 2h(Y_i)<=h(beta_i). If Y_i != m_i, local extraction gives

    log R_i <= h(Y_i)+log(1+|m_i|).

The strict absorption inequality (1001/997)^5/2 < 393/100 holds exactly. Thus h(M)<=C log(1+|m_i|)+O(1). The trace estimate m_i^2<=C' h(T_i)+J bounds |m_i|, and then h(M), independently of B. Since M>=B^4, this contradicts large B. Consequently Y_i=m_i in Z and the denominator argument for Y_i=X_i^2+1 forces X_i in Z. For arbitrary fixed k the same proof works by choosing a rational abc exponent kappa>1 sufficiently close to 1 so that (1/(4/kappa-3))^(1+ceil(log2 k))/2<393/100. The radical estimate uses ordinary abc as before.

## Completeness and ordering of choices

For integer inputs put n_i=X_i^2+1, A_i=[n_i]P. This fixes T_i,M,a before selecting primes. The 18k rational contact positions ±(a+c) are distinct since a>max |c| and the shifts are distinct. Use the simultaneous common-numerator theorem, its two-index CRT lemma, and its fixed-place/real preparation, with these positions and labels n_i. They require only a fixed finite disjoint contact list, arbitrary prescribed denominator divisibility and sufficiently large real slope. The proof chooses H,U independently with the stated CRT residues for the assigned n_i. At a selected prime exactly one linear factor vanishes simply and the derivative is a unit, so nu=1; the assigned input has all six original tests positive in the successful slot by that theorem's formal estimates. Every other gate (including the assigned input's opposite side) is inactive, with its weighted factor congruent to 1 by the selective lemma. Therefore W=1 mod p in the successful slot. At the other slot each factor's reciprocal is integral with residue 0 or 1, by the same unequal-parity argument. Hence V0 is a unit at these odd primes and v_p(e)=1.

For nonselected primes outside temporary avoidance, if z is integral F is a unit; if z has negative valuation, the leading terms give v_p(u)=2v_p(z) since a is a unit. In the fixed-place preparation include the supports of a, all contact differences, all fixed bad primes, and the original point-chart conditions. Because the sum of all shifts is zero,

    u ~ z^2/a

as z tends to infinity at each fixed place or the real place. Thus fixed-place valuations of u are negative even for sufficiently deep denominator (a=M^4). The original v63/common-numerator bounded-neighborhood preparation makes all raw tests bounded, and nonzero tests have fixed valuation at the prepared finite places; identically zero tests are allowed. For each nonzero test, D~1/u there, while w(G_i(x_side))~u/G_i(x_side)^2 tends to zero. Consequently W tends to 1 and V0 to 2, with all division guards satisfied. The same estimates at both real embeddings hold with u>0 for large real slope (all a+c>0). Since a is a square, e=28u/((1+u)^2 V0^2) is in 7 Q_2^{times 2} with arbitrarily large positive dyadic valuation; at 7 it has positive valuation. The real slope makes 0<e<1. All negative odd valuations of u are harmless by the selective lemma; all even valuations of u give even valuations of e away from 7. Thus e has square reduced denominator. These arguments include actual point denominators arising after the CRT.

Apply the same BB normalized product-pole theorem as v88 with d=7u, e=d times the displayed nonzero rational square. It supplies v,s and q. The selected-character guard does not include q or any auxiliary pole denominator beyond those explicitly listed. This establishes simultaneous completeness under exactly the inherited arithmetic premises.

## Coefficient specification and variable count

The coefficient prescription is entirely finite. Use the rank-four point multiplication table of common_numerator_transfers.tex (section Finite algebra), for each square-abscissa chart; in particular use the basis 1,U,V,W, j=(U+V sqrt(2))/2, with U^2=2A+2W,V^2=A-W,UV=2B,UW=AU-2BV,VW=BU-AV,W^2=A^2-2B^2 for j^2=A+B sqrt(2). Compute differences of finite points by the guarded affine chord formulas of v63/direct_input13. All formulae in this note are a coefficient DAG: evaluate the products in the displayed order, with F_a the sum of the 18k products deleting one linear factor. For each quotient in K over the base algebra use the numerator/denominator rule (N/D)^(-1)=conjugate(N)D/Norm(N), retaining Norm(N) as a guard. Use all explicit nonzero guards as norms of their numerators. Clear the terminal radicand N/D by q_new^2=ND and recover q=q_new/D. Use the one-coordinate determinant recipe of joint_finite_algebra_encoder.tex, after clearing constant rational denominators. It tolerates zero terminal roots and unselected characters at which guards vanish. This specifies the polynomial without expanding it.

There are k rational inputs, 2(k+2) ordinary point coordinates, one slope, two pole parameters and one joint encoder: 3k+8. For undecidability, substitute the exact BDHMS mixed source and the rank-sixteen monic wrapper of finite_wrapper_transfer.tex, keeping its S guard, one generator xi (which also recovers m), and the two ordinary positivity parameters. The last input n=m/S^2 is an algebra element, not an ordinary variable. Make this wrapper the first finite stage, then the point tensor factors, then the sole terminal pole. The finite algebra has rank 16*4^11*2=2^27. Twenty-two point generators (U,V for each point), xi and the terminal root suffice; hence ell=25 in the determinant formula.

The ordinary count is 8 integer-source coordinates +22 point coordinates +1 slope +2 pole coordinates +2 positivity coordinates +1 encoder =36. The fixed coefficient B is not a variable. The wrapper proof supplies exactly the same nonrecursive source-instance projection as the prior 52-variable transfer.

The supplied degree ledger uses the conservative denominator-pair rule above, the existing uniform mixed-source degree delta<2^211, the point matrix degree bounds, and the determinant formula of joint_finite_algebra_encoder.tex. All source guards can be accounted for by the quotient norm guards plus the explicit nonzero point, ordinate, F,u,e and trace guards. The bound is deliberately loose. This is an exact coefficient recipe, not an expanded polynomial. As in the predecessor, the universal-source theorem and the retained arithmetic interfaces are not established by this computation.

References: [v63 derivative detector](../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex), [v58 height theorem](../../papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex), [v22 direct comparison](../../papers/conditional_few_variables/direct_input13_20261110_v22.tex), [common numerator](../papers/common_numerator_transfers.tex), [v88 BB product pole](../../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex), [finite algebra](../papers/joint_finite_algebra_encoder.tex), [mixed-source wrapper](../papers/finite_wrapper_transfer.tex).
