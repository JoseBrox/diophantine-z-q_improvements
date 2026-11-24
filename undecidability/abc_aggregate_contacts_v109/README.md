# One aggregate height and common contact coefficients: 560 variables

**Conditional theorem.** Under ordinary rational abc and exactly the retained arithmetic premises of the 605-variable v108 ordinary-abc transfer, the system in this directory gives the same recursively enumerable source-instance projection, for every sufficiently large fixed odd B_abc. The sufficient threshold may increase. This is not a full-old-zero-set equivalence, nor an unconditional result about H10(Q).

## Construction

Use the full v108 predecessor, including the c-integrality replacement, all twelve retained integer certificates, the common numerator and the scaled elliptic charts. Only the contact rows are replaced. For certificate i let X_i be its input and T_i its scaled trace. Keep the old height leaf M_i=B+2(X_i^8+T_i^2) and its square register. Build a binary tree by pairing successive nodes (carrying the last unpaired node to the next level), using M_parent=1+2(M_left^4+M_right^4). Store each parent and its square. There are eleven parents; the maximum depth is four. Write M for the root.

Set a=M^4+432. Use the already retained common free slope z and z^2 (here z is int_b_48, not the source coefficient named z). For the twelve certificates take scales s_i=11,13,17,19,23,29,31,37,41,43,47,53, in the order of the predecessor's ordinary_integer_inputs. Let v_i=s_i^2. The common positive center exceeds all scaled radii. Put

    T=a^2-z^2, S=T+2z^2, P=T^2,
    F_i=product_{r in {1,4,7,8}} (P-2r^2 v_i S+r^4 v_i^2).

The sixteen contact positions for each i are ±(a±s_i r). All 192 positions are distinct: the positive radii s_i r are distinct by unique factorization (the s_i are distinct primes >8), and a>432>max(s_i r). Equivalently F_i=G_i(M^4-z)G_i(M^4+z) with G_i(t)=product_{r in {1,4,7,8}} ((t+432)^2-s_i^2 r^2). Each G_i has eight distinct positive shifts, and every pair sum is nonzero.

Write PP=P^2, PS=PS, SS=S^2, TP=TP, TS=TS for the five stored monomial registers (on the right juxtaposition means multiplication). Define the following polynomials in an indeterminate v with coefficients affine in these common registers:

    A(v)=PP-130v PS+(4097P+256SS)v^2-8320v^3 S+4096v^4,
    B(v)=PP-130v PS+(2657P+3136SS)v^2-101920v^3 S+614656v^4,
    H(v)=4TP-v(260TS+130P)+v^2(8194T+512S)-8320v^3,
    D(v)=720v^2(-4T+8S-130v).

A is the product of the factors at radii 1,8 and B that at radii 4,7. For the derivation L=2T partial_P+partial_S, LA=H and LB=H+D. Therefore F_i=A(v_i)B(v_i) and partial_a F_i=2a[H(v_i)(A(v_i)+B(v_i))+D(v_i)A(v_i)].

Store nine common coefficients f_j, 0<=j<=8, satisfying a f_j=[v^j] A(v)B(v). As a>0 this is equivalent to f(v_i)=F_i/a. For each i retain the old physical inverse contact c_i (stored at suffix 43), with its unit row c_i epsilon_i=1, and impose

    H(v_i)(A(v_i)+B(v_i))+D(v_i)A(v_i)+8c_i f(v_i)=0.

All equations are quadratic. They imply partial_a F_i+16c_i F_i=0. Neither F_i nor its derivative can vanish: if one slot of G_i vanishes, its root is simple, the opposite slot is nonzero because their arguments sum to 2M^4>0 and all shifts are positive. Consequently the derivative would be nonzero. The converse follows from the equation and c_i nonzero. Thus u_i=1/c_i=-16F_i/(partial_a F_i), exactly the physical derivative quotient for the changed contacts. The retained detector equations, guards and BB-native poles give the original extraction for this u_i.

## Soundness

Use the positive-power and signed mixed-power estimates of [v58](../../papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex), with kappa=1001/1000. The positive fourth-power lemma bounds the heights of both positive arguments by (1001/997) h(sum of their fourth powers)+O(1). For parent=1+2sum the sum's height is at most h(parent)+log 2. Iteration therefore bounds every h(M_i) by C h(M)+O(1), where C=(1001/997)^4. Constants are uniform in B. The v81 argument on the unchanged leaf gives h(X_i)<=501/997 h(M_i)+O(1) and 2h(T_i)<=h(M_i)+8h(X_i)+O(1). A zero sum in the leaf already makes the corresponding input zero.

Apply the derivative radical estimate in [v63](../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex) to each G_i: eight shifts, exponent four, epsilon=1/100. In its proof, before passing to h(t), the estimate is (8-6-3epsilon) max(h(M^4-z),h(M^4+z))-(2+epsilon)h(M)-O(1). Since the sum of those two arguments is 2M^4, it gives log r^+(u_i)>=193/100 h(M)-O(1). At a zero argument use the other slot, as in [v81](../../papers/quartic_existence/paired_contact56_20261119_v81.tex). Enlarge the fixed exceptional set to the finite union of the sets required by these fixed shift lists and charts. It is independent of B and of the solution.

The unchanged v81 normalizer and pole valuation proof makes every prime in this odd positive support a prime of X_i(m_i-X_i) with X_i locally integral, where m_i is the label of its difference point. If X_i is neither zero nor m_i, write X_i=A/Q in lowest terms; then log r^+(u_i)<=2h(X_i)+log(1+|m_i|). The strict inequality 2(501/997)C<193/100 is checked exactly in the builder. It follows that h(M)<=C' log(1+|m_i|)+O(1). The retained trace bound m_i^2<=C_0(h(T_i)+2h(X_i))+J_0 now bounds |m_i|, and hence h(M), uniformly in B. But M>=B, a contradiction for sufficiently large fixed odd B. Thus every certified input is an integer. No assumption of disjoint reductions modulo p for arbitrary rational witnesses is used.

## Completeness

For every positive integer source witness use the v103 simultaneous common-reference/common-numerator CRT construction with differences A_i=[X_i]R_0. Fix all scaled traces and leaves before selecting primes. The two-adic trace lemma in v81 gives M_i odd in Z_2; all parents are odd, and a=M^4+432 is a nonzero two-adic square (congruent to 1 modulo 8). The union of contact lists is fixed and distinct as above, so the retained simultaneous prime-pattern theorem and v103 CRT proof apply without changes to their moduli or precision requirements. At each selected prime assigned to i, u_i has valuation one and the successful-slot test bounds are exactly those of v103; every other contact factor is a unit there.

For each i, outside the finite preparation set, a nonselected prime at which z is integral has F_i a unit; at a prime with v_p(z)<0, v_p(u_i)=2v_p(z) is even. At the fixed places use sufficiently deep slope denominator and the asymptotic u_i ~ z^2/a, yielding negative valuation there. These assertions follow from the factorization into distinct selected prime linear factors, and the leading derivative coefficient -16a times z^14 (the shifts are centered symmetrically at a). Include all primes of the now fixed centers and all nonzero contact differences in temporary avoidance. This does not enlarge the soundness exceptional set. The unchanged uniform normalizer lemma covers all negative odd valuations, including actual point denominators; at even valuations square factors preserve parity. At real infinity and the fixed places the raw point tests stay bounded and c_i~a/z^2, tau_i~1 and b_i~7c_i, by v103. Hence the actual pole input has square reduced denominator, is between zero and one, and is in 7 Q_2^{times 2} with arbitrarily large prescribed positive valuation; the prime 7 has positive valuation. The unchanged BB pole theorem applies separately to each i. All remaining source rows are unchanged. The new registers are obtained by evaluation and division by a only. This proves the required source-instance completeness under the retained premises, without requiring that an arbitrary old contact solution extends.

## Exact census and verification

Delete seven private coordinates and eight rows for each of twelve certificates. Add 22 tree coordinates/rows, eight common monomial/center coordinates/rows, and nine common product coefficients/rows; add twelve derivative rows. Thus 605-84+39=560 variables and 528-96+51=483 quadratic residuals. The old slope and its square are retained. Their sum of squares is a quartic over the same integer parameter ring; a nonzero quadratic leading part cannot cancel in a sum of squares over Q.

The exact table preserves all 432 non-contact rows by named monomials. The deterministic JS builder uses exact BigInt coefficients, checks deleted coordinate occurrences, full support, degree, the strict rational height margin, and for each of the twelve scales expands both pair products, their two derivatives and the product derivative independently of the stated coefficient formulas. Run node build.js from any directory; use --write to regenerate the table. The builder's checks were executed on the frozen predecessor through the GitHub connector when publishing this checkpoint; no claim is made about a separately run full repository CI suite.

References: [v108 table and predecessor proof](../abc_pell_integrality_v108/), [v103 common numerator](../abc_common_numerator_v103/common_numerator.tex), [v107 BB-native pole audit](../abc_bb_native_v107/). All source-coding premises of v108, including Jones's theorem, are retained. No new prime-pattern or rational-realization premise is added.
