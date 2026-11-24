# A 54-variable ordinary-abc quartic by asymmetric contacts

**Theorem.** Under the arithmetic premises of the v81 56-variable quartic (including ordinary rational abc), with the retained Gaussian prime supplier in its stated congruence class, the enclosed 44 integral quadrics define the integers by their sum of squares for every sufficiently large positive integer B congruent to 1 modulo 8. The 54 coordinates include the input. The coefficient cutoff remains ineffective. No new global point-realization assumption is used.

This is a new contact construction, not a diagonal rescaling of the v81 contact circuit. The elliptic and pole mechanisms originate in the constructions credited in [v81](../../papers/quartic_existence/paired_contact56_20261119_v81.tex); the asymmetric contact argument below is the new change.

## 1. Source and the new weight

Keep the first 35 residuals (before the height equation) and their point, gate, pole and zero-fibre interpretations from the v81 table. In particular use its coordinates X, T_sc=2x8, c=x43, u=x44=1/c, and d_s=x42=uD. The gate uses alpha=u+d_s^2, tau=alpha/(1+alpha), and physical pole argument b=7c tau^2. The pole and gate have exactly their old equations. Only the height equation and the contact circuit change.

Put M=B+8(X^8+T_sc^2), a=M+16, x=a-z, y=a+z. Define
\[
P(R)=\prod_{r\in\{1,4,7,8\}}(R-r^2),\quad
A=P(x^2),\quad H=P(y^2)/y^4,
\qquad c=H^2/A-1+1/H.
\]
Require these displayed rational expressions to be defined, with c nonzero. The quadrics below force every such condition. There is no restriction on signs or on z in soundness.

## 2. Height lower bound for the positive odd radical of u

For a nonzero value of the fixed split degree-eight polynomial G(t)=P(t^2), write T(t) for the logarithmic prime weight of v_p(G(t))=1, outside a fixed exceptional set S; write J_k(t) for the weight of v_p(G(t))>=k. Include all old bad primes, 2 and 7, primes of the nonzero roots and all root differences in S. It is independent of B, X, M and z.

The standard rational-abc binary-form estimate used in [v63](../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex), section "The derivative height estimate" and its preceding simple-support lemma, gives for epsilon=1/100
\[
T(t)\ge(4-2\epsilon)h(t)-O(1),\qquad
J_k(t)\le (2+\epsilon)h(t)/(k-1)+O(1)\quad(k\ge2).
\]
Indeed, for t=a_0/b_0 in lowest terms the numerator product is coprime to b_0 outside S, its size is at most exp(8h(t)+O(1)), and its radical is at least exp((6-epsilon)h(t)-O(1)). The surplus of log size over log radical bounds the total of (v_p-1)log p, hence J_k. Subtracting J_2 from the radical yields T. The bounds remain valid for t=0, since G(0) is a nonzero constant. All constants are uniform.

For a prime p counted by T(x), let k=v_p(H). The first and third terms of c have valuations 2k-1 and -k. If k<=0 the first is strictly smaller and negative odd. If k>=1 the third is strictly smaller and negative; it is odd unless k is positive even. The constant -1 cannot cancel either negative minimum. A positive valuation of H is the positive valuation of G(y), since at primes outside S a zero of G(y) has y a unit, a nonintegral y gives v_p(H)=4v_p(y)<0, and a positive valuation of y gives v_p(H)=-4v_p(y)<0. Thus the discarded T(x) primes belong to J_2(y).

For a prime counted by T(y) we have v_p(H)=1. If l=v_p(A)<=2 then the third term has valuation -1, strictly smaller than the first valuation 2-l and the constant valuation zero. Only J_3(x) must be discarded. In particular we do not discard primes dividing the denominator of M, and do not have to bound a collision polynomial in M.

Let R denote log r^+_odd,S(u). We obtain
\[
R\ge L_x-O(1),\quad R\ge L_y-O(1),
\qquad L_x=3.98h(x)-2.01h(y),\quad L_y=3.98h(y)-1.005h(x).
\]
If h(x)>=h(y), then (2L_x+L_y)/3 >= 2.305 h(x). Otherwise L_y>=2.975h(y). Therefore R>=2.30 max(h(x),h(y))-O(1). Since x+y=2(M+16), elementary height inequalities give
\[
R\ge (23/20)h(M)-O(1).
\]
This is the key saving: the height parameter itself, rather than a high power of it, can be used as the midpoint.

## 3. Soundness

The previous gate and pole obstruction at every p outside S with positive odd mu=v_p(u) apply verbatim. In particular alpha cannot vanish on a sufficiently large B fibre: the height lower bound supplies such a prime, at which alpha=u+(uD)^2 has summands of different valuation parity. The gate forces v_p(D)>-3mu/4. Exactly the v81 norm/trace argument and four-term distinct-valuation detector then yield p dividing the numerator of X(m-X) for the retained integral point index m, when X is neither 0 nor m. All point-chart and nonzero guards used in that argument are unchanged.

For s=X^8+T_sc^2>=0, M=B+8s implies h(s)<=h(M)+log 8, uniformly in positive integral B (the cancellation in the denominator of B+8s divides 8). The v58 signed mixed-power estimate with kappa=1001/1000 therefore gives h(X)<=(501/997)h(M)+O(1). The retained height bound for T_sc similarly bounds m^2 by O(h(M)+1), because 2h(T_sc)<=h(s)+8h(X)+log 2 (zero T_sc poses no problem). Hence if X is not 0 or m, the radical upper bound of v81 gives
\[
(23/20-1002/997)h(M)\le\log(1+|m|)+O(1).
\]
The difference is positive, exactly 2891/19940. The trace-index bound makes h(M) bounded independently of B, contrary to M>=B. Thus X is integral on all sufficiently large fibres. No effective value of the cutoff is asserted.

## 4. Integer completeness and all contact primes

Fix an integer X=n. For n nonzero choose the difference point and its multiplication family as in v81, so T_sc and M are fixed before prime selection. For n=0 use exactly the fixed zero fibre of v81 (all raw tests zero). The v81 two-adic trace lemma gives T_sc integral at two in both cases. With the new factor-eight padding, B congruent to 1 modulo 8 gives a=M+16 congruent to 1 modulo 8 in Z_2, so a is a dyadic square unit.

Apply the retained simultaneous Gaussian prime supplier to the sixteen distinct slope positions +/- (a+r) for r in {-8,-7,-4,-1,1,4,7,8}. They are distinct since a>16. They are the zeros of G(a-z) and G(a+z). Use z=N/(D_0^2 L^2) and p_d=N-d D_0^2 L^2, with D_0 fixed to clear contact denominators. All p_d are distinct positive primes, outside the enlarged finite preparation set S_n. This set includes S, numerator and denominator primes of a, contact positions, their pairwise differences, and the nonzero values of y=a+z at each contact position (for x-contacts these are 2a plus or minus a radius, and for y-contacts they are nonzero radii). The set is fixed before selecting primes and can include the same other finite local preparation requirements as in v81. Include 2 with arbitrarily deep divisibility of L. The retained supplier has Gaussian generators congruent to 9 modulo 16; consequently every p_d is 1 modulo 8, as is N. This is the same supplier congruence recorded in the project's common-numerator proof; it is not an extra prime-pattern hypothesis.

At each selected prime, exactly one of G(x),G(y) has valuation one; the other is a unit, and y is a unit. If it is G(x), the term H^2/A has valuation -1. If it is G(y), the term 1/H has valuation -1. All other terms are integral in each case. Thus v_p(u)=1. The same v81 multiplication-family preparation at each selected prime (the orders and labels are unchanged) supplies the required good-slot depths and opposite-slot units. Consequently v_p(D)>0, v_p(alpha)=1, v_p(tau)=1, and v_p(b)=1. This uses the old preparation only at the same contact depth one.

Now check every nonselected prime outside S_n. The numerator products of G(x) and G(y) factor exactly into their respective eight selected primes over (D_0 L)^16. If z is integral at p, then the denominator D_0^2 L^2 is a unit: otherwise N would be divisible by p and all distinct p_d would be divisible by p. So both G(x) and G(y) are units. If y is a unit, c is integral (possible cancellation is allowed). If v_p(y)>0 then v_p(H)=-4v_p(y) and the first term of c uniquely dominates with negative even valuation. Thus no positive odd valuation of u occurs in either case.

If z is nonintegral outside S_n, a is a unit. At infinity the rational-function expansion of c, with fixed a, is
\[
H^2/A = 1+16a/z+O(z^{-2}),\qquad 1/H=O(z^{-4}),
\qquad c=16a/z+O(z^{-2}).
\]
All expansion coefficients are p-integral for p outside S_n, because the polynomials are monic and a integral. Since 16a is a unit, the leading term dominates. The denominator of z is a square (there is no common prime divisor of N and D_0 L, by distinctness), so v_p(c)=-v_p(z) is positive even. This includes all uncontrolled slope denominator primes.

At the fixed places in S_n take z sufficiently large in the local absolute value, as permitted by the original supplier and point preparation. The same leading expansion makes c small and nonzero; there is no need for its valuation to be even at odd fixed primes. The v81 bounded-point preparations give W-1=O(c), D=O(c^2), alpha=c^{-1}+O(c^2), tau=1+O(c) there and at the real place. In particular the gate denominator is nonzero. At two, z has dyadic square class 1 (N=1 mod 8 and square denominator), and a is a square, so the leading expansion gives c a dyadic square of arbitrarily deep even valuation. At seven v_7(c)>0, and tau is a unit. At real positive infinity c>0 since a>0, and 0<b<1. This also shows c is a nonzero rational on the constructed witness, independent of any cancellation elsewhere.

Finally for every p outside seven, a negative odd valuation of u gives positive odd valuation of b by the unchanged normalizer lemma, regardless of the point denominators. Even valuations of u give even valuations of b. The only positive odd valuations of u outside the preparation set are the selected primes, already checked. At prepared primes u has negative valuation, and seven has the separate preparation. Thus b has square reduced denominator, 0<b<1, dyadic square class 7, and v_2(b)>=4. The v81 prepared-pole completeness lemma (or its BB product equivalent) applies to the actual b. Fill the unchanged point and detector witnesses and the new contact registers. For n=0 the gate simplifies exactly as in v81, and the same checks apply. No positive-prime condition or denominator hypothesis on arbitrary rational solutions has been imported from these completeness witnesses.

## 5. Exact compilation

The old 45 coordinates through M remain (the height row now has coefficients -32 on x8^2 and -8 on x30^2). The old alpha coordinate x56 is moved to x54. Replace the old ten contact coordinates x46,...,x55 by eight coordinates z,r_x,r_y,s_x,s_y,A,H,q, in this order. Here a=M+16 is an affine expression, not a coordinate. With P(R)=sum_{j=0}^4 p_j R^j the eight rows are
\[
\begin{aligned}
r_x&=(M+16-z)^2,& r_y&=(M+16+z)^2,\\
s_x&=r_x^2,&s_y&=r_y^2,\\
A&=p_0+p_1r_x+p_2s_x+p_3r_xs_x+s_x^2,\\
Hs_y&=p_0+p_1r_y+p_2s_y+p_3r_ys_y+s_y^2,\\
qH&=1,&(c+1-q)A&=H^2.
\end{aligned}
\]
The second value equation excludes y=0 because P(0) is nonzero. The inverse row forces H nonzero; the last row forces A nonzero. The retained c u=1 excludes c=0. These are all required new guards and every row is quadratic. Conversely the displayed rational expressions give all eight registers. Thus the complete count is 45+8+1=54, with 44 residuals and a primitive quartic sum of squares, not merely a partial encoding of the contact formulas.

The exact coefficient tables are provided alongside this proof. Run verify.py with repository root as its working directory. It independently checks all unchanged rows, the height change, the expanded new identities, the full coefficient expansion, degree and primitive content, and finite valuation and asymptotic identities. These computations verify the algebra and rational margins; the arithmetic theorem follows from the proofs above and the retained source premises.

## Fixture and verification

The expanded ASCII fixture `expanded-B1.txt` has 788 monomials, coefficient height 5531402752, and 11174 bytes. It is not asserted to define the integers. The theorem concerns sufficiently large fixed B congruent to 1 modulo 8. The row and expanded coefficient tables retain their full symbolic dependence on B.
