# Unscaled shared elliptic chart and one aggregate trace: 437 variables

**Theorem.** Retain exactly the ordinary rational abc, elliptic group, formal comparison, simultaneous prime-pattern and recurrence, trace-height, BB-native pole realization and external Jones coding inputs of the earlier complete ordinary-abc transfer. The system in this directory gives the same coded-instance projection, for every sufficiently large fixed positive odd B_abc. It has **437 rational variables and 384 quadratic residuals**; the sum of their squares is a quartic. The threshold is ineffective. All twelve certified integer inputs remain. There is just one native pole. This is a new projection proof, not a same-witness bijection with v114.

## 1. Outer coding and elliptic chart

Keep exactly the 52 jones1980.* equations of the 507/454 [v114](../abc_gate_fraction_v114/) predecessor. Their variable support has size 76, including the two borrowed square registers int_b_30=b^4 and int_g_29=g^2. Restore these two identities in the new interface. By the source reconstruction in [v108](../abc_pell_integrality_v108/README.md), [v104](../odd_pell_quotient_v104/README.md), and the [theta positivity theorem](../positivity_theta_reduction_20261124/README.md), it suffices to prove the twelve indicated inputs integral and to realize all canonical positive integer tuples. The canonical positive odd quotient has i_half>0. The canonical power quotients and other inputs may all be chosen nonzero as in the frozen predecessor. No assertion about realization of arbitrary zero integer tuples is needed here.

Put K=Q(rho), rho^2=2, Delta=11-6rho, E:y^2=x^3-Delta x, and R0=(1+rho,2rho). Use the reference chart of [v65](../../papers/quartic_existence/quartic_abc68_20261117_v65.tex): a0=1+rho, c0=4-2rho, delta0=-23+17rho and

    a0*u_H*w_H=1,
    v_H*(v_H-a0*(u_H+w_H)-2*c0)=delta0.

Its reference field values are S_H=v_H-c0-a0*u_H, T_H=a0*w_H-v_H+c0, f_H=u_H/v_H and f_HP=w_H/v_H, describing H and H-R0. In particular v_H is nonzero. Write f=1/x, S_Q=y/x.

Use one common point U described by S=S_U, F=f(U), S2=S^2 and F*S2+Delta*F^2=1. Let c*u=1, where u is the global contact quotient below, and Ftilde=cF. For each input X_i use only three private fields t_i,h_i,Gtilde_i, with

    Ftilde*(h_i+S+t_i)=h_i*Gtilde_i,
    Delta*(F+u*Gtilde_i)=(S-t_i)*h_i-t_i^2.

Writing G_i=u*Gtilde_i, these recover the unscaled v65 translated-secant chart with d_i=G_i*h_i. In detail let A=(h+S+t)F-Gh, B=Delta(F+G)-(S-t)h+t^2 and C=FS^2+Delta F^2-1. Then Gh(S-t)-Delta FG-1=C-FB-(S-t)A, proving the fourth chart identity. The pair chart theorem gives two distinct finite points U,V_i with nonzero abscissas, t_i=S_(V_i), G_i=f(V_i), and x(A_i)=h_i(h_i+S+t_i), A_i=U-V_i. It includes the zero ordinates, tangent and finite torsion difference cases. No division by X_i occurs. In particular X_i=0 is harmless for soundness.

## 2. Height aggregation and contact quotients

Store the single scalar T=Tr(sum_i x(A_i)), directly as a sum of quadratic expressions in the pair chart. The positive-weight trace theorem [v27](../../papers/trace_heights/weighted_trace_20261114_v27.tex), specialized to fixed weights all 1 and r=1, gives m_i^2 <= C0 h(T)+J0 simultaneously for the integer R0-labels m_i of A_i, including torsion translates. All constants are fixed for twelve points. This is the same published family height input already used in the earlier general route; it includes all finite difference points of this chart. The proof of that theorem follows from the noncancellation of double poles on the two independent conjugate cyclic subgroups, with positive weights, and the retained von Buhren height theorem. It does not require the abscissas themselves positive.

Use thirteen leaves X_1,...,X_12,T and store their squares. Pair successive entries and replace a pair L,R by L^4+R^4, carrying an unpaired entry to the next layer. At the final pair instead take M=B_abc+2(L^4+R^4). Store each node and its square. The depth is at most four. The positive-fourth-power height lemma of [v58](../../papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex), applied to absolute values, gives

    h(X_i), h(T) <= (1001/997)^4 h(M)+O(1).

The case of a zero summand follows directly from h(x^4)=4h(x); both zero summands give zero heights. At the root use h((M-B_abc)/2)<=h(M)+log 2 for M=B_abc+2s, s>=0: writing s=A/D reduced, the numerator of M is B_abc D+2A and its cancellation with D divides 2. Thus the O(1) is uniform in B_abc. Also M>=B_abc.

Set a=M^8+784 and use a free slope z, independent of the source coefficient named z. At every rational M, a is positive and a nonzero square in Q_2: if v2(M)=0, a=1 modulo 16; otherwise the smaller of valuations 8v2(M) and 4 is attained by a square, and the other term is at least four valuation units higher. The constant 784=28^2 exceeds all radii used below.

Use scales s_i=11,13,17,19,23,29,31,37,41,43,47,53 and shifts 784+-s_i*r for r=1,4,7,8. All shifts are positive and distinct. With x=M^8-z, y=M^8+z, let G_i(t) be the product of the eight shifted linear factors and F_i=G_i(x)G_i(y). Let F_all=product_i F_i and use the derivative at fixed z, varying the center. Encode

    r_i F_i = -(partial_a F_i)/(16a),
    (a*u) sum_i r_i = 12.

For the quadratic coefficient prescription let T0=a^2-z^2, S0=T0+2z^2, P=T0^2, and store PP=P^2, PS=P*S0, SS=S0^2, TP=T0*P, TS=T0*S0. For v=s_i^2 set

    A(v)=PP-130v PS+(4097P+256SS)v^2-8320v^3 S0+4096v^4,
    B(v)=PP-130v PS+(2657P+3136SS)v^2-101920v^3 S0+614656v^4,
    H(v)=4TP-v(260TS+130P)+v^2(8194T0+512S0)-8320v^3,
    D(v)=720v^2(-4T0+8S0-130v).

By the [v109](../abc_aggregate_contacts_v109/) identities F_i=A(v)B(v) and partial_a F_i=2a[H(v)(A(v)+B(v))+D(v)A(v)]. Store only the nonlinear coefficients of A(v)B(v) in v; the affine coefficients are inlined. Thus F_i is an affine expression in retained coordinates, and the row 8r_i F_i+H(A+B)+DA=0 is quadratic. If F_i vanished, exactly one linear factor would vanish (opposite slots cannot both vanish since x+y>0); its derivative is nonzero, contradicting that row. No private inverse of r_i is needed. The global sum row gives F_all' nonzero and u=-16*12*F_all/F_all'. The global unit guard supplies c=1/u.

For each i select the simple-prime support of G_i at the larger-height slot (call it x). Discard the fixed exceptional primes, including bad chart primes and all shift differences, pair sums, and constants of the derivative; discard denominator primes of M (logarithmic cost at most h(M)). The ordinary-abc polynomial radical theorem in [v63](../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex) gives simple-prime weight >=(8-4-2epsilon)h(x)-O(1). At these primes both x and y are integral. If M has positive valuation, y has no root by the nonzero pair sums condition. If M is a unit, discard the multiple-prime support of G(y)=product_j G_j(y), at cost <=(2+epsilon)h(y)+O(1), by the same v63 multiple-prime lemma. When G(y) is a unit, F_all' has valuation zero and u valuation one. If G(y) has one simple factor, both roots have valuation one, and failure of derivative valuation one requires p^2 | 2M^8+d+d' for shifts d,d'. Discard the multiple-prime support of the product over distinct pair sums; the v63 power-multiple lemma costs <=(2+epsilon)h(M)+O(1), independently of the tuple and B_abc. Every surviving prime has v_p(u)=1 and v_p(F_i)>=1 (possibly two, if both simple roots belong to group i). No disjoint-support claim for arbitrary rational witnesses is made.

With epsilon=1/100, h(x)+h(y)+log2 >= h(2M^8)>=8h(M)-log2. The surviving prime product R_i satisfies

    log R_i >= (8-6-3epsilon)*max(h(x),h(y))-(3+epsilon)h(M)-O(1)
            >= (487/100)h(M)-O(1).

Zero slots are covered as in v81; their shifted factors are fixed nonzero constants. The multiple-prime support bound includes arbitrary numbers of fixed factors and depends only on the fixed shifts and exponent, not B_abc.

## 3. Shared detector, selective gates, and pole

For each i let C_i=X_i S-S_H, I_i=X_i t_i-T_H. Use the shared field

    R=c*f_H^2+c^2*F^2+c^3*conj(f_HP)^2

and private field

    W_i=1+R^8+c*C_i^2+c^2*conj(I_i)^4+c^4*conj(G_i)^4.

The compiler stores common coefficients cS^2,cS*S_H,cS_H^2 via cS,cS_H, so c*C_i^2 is already quadratic in X_i,X_i^2 and those coefficients. It stores I_i by a quadratic definition, J_i by uJ_i=conj(I_i)^2, and Q_i=conj(Gtilde_i)^2. Hence the private W_i is quadratic in the retained fields. R and its three successive squares are shared. All these equations are written in the two rational components of K.

The scalar D_i is defined by D_i Tr(W_i)=Nm(W_i-1), where Nm is the field norm. The trace cannot vanish: otherwise W_i=1 by the norm equation, a contradiction. Define

    Rgate_i=F_i D_i, Tgate_i=u+Rgate_i^2,
    Vgate_i*Tgate_i=D_i^2, c*(Wgate_i-1)=Vgate_i^2,
    W=product_i Wgate_i, alpha=u+(W-1)^2,
    tau*(1+alpha)=alpha, b_s=7*tau^2.

Each gate is quadratic. At any good prime with v_p(u)=1, put s=v_p(F_i), d=v_p(D_i). In the gate denominator the two valuations 1 and 2s+2d have different parity, so it is nonzero. For finite d the valuation of Vgate_i is 2d-min(1,2s+2d). At s>=1 this is nonnegative exactly when d>=1; at s=0 it is always nonnegative. The zero D_i case gives Vgate_i=0 and Wgate_i=1. For any s, Wgate_i has valuation min(0,1+2v_p(Vgate_i)); if integral, it is 1 modulo p.

The five final quadratic native-pole equations are

    p^2=c*P0, b_s*P0+e^2=u^2,
    U0*V0+b_s*e-u*e=0,
    q^2=c*Q0, b_s*Q0-U0^2+V0^2=0.

After scaling e,U0,V0 by 1/u, these are the BB-native equations for b=7c*tau^2, as in [v107](../abc_bb_native_v107/README.md) and [v113](../abc_shared_native_pole_v113/). At any good prime v_p(u)=1, alpha=u+(W-1)^2 has different-parity terms; alpha,tau and b are nonzero. Square reduced denominator of b forces v_p(alpha)>1/2 by the v81/v113 argument, so W=1 modulo p. Each factor has nonpositive valuation, hence all are units. At the primes of R_i, the active gate therefore forces v_p(D_i)>0.

At each slot of K over such a prime, the terms of R have pairwise distinct nonzero valuation classes modulo four (reciprocal abscissas have even valuations at good unramified primes). Thus if R is integral, each term is strictly positive in valuation. In W_i the valuations of its nonconstant terms are respectively 0, odd, 2 or 6, and 4 modulo eight (the last uses v(G_i) even). Every negative minimum is unique. If both slots had negative W_i valuation, the norm-error identity would give v_p(D_i)<=max(v_1(W_i),v_2(W_i))<0, impossible. Thus one slot is integral. At that slot all nonconstant terms have nonnegative valuation, yielding

    v(R)>0, v(C_i)>0, v(conj(I_i))>0,
    v(conj(G_i))>0,
    v(f_H)>0, v(F)>0, v(conj(f_HP))>0.

The formal points at the corresponding two places therefore have parameters z_Q=-1/S_Q of positive valuation, with S_Q nonzero. If v(X_i)>0 the desired local congruence is immediate. Otherwise divide C_i and I_i by the respective formal S_Q; the two actual parameter ratios z(U)/z(H) and z(V_i)/z(H-R0) are congruent to X_i up to an additive error of positive valuation. Their logarithm ratios are j/h and l/(h-1) with integer R0-labels j,l,h (use multiplication by 2 to remove torsion) and formal logarithms differ by the retained relative order-four unit from the parameters. At least one of h,h-1 is a p-adic unit, so X_i is p-integral. In the unit case both logarithm ratios reduce to X_i, and j-l=m_i gives X_i congruent to m_i modulo p. This argument uses only the established formal comparison, valid also at an inert prime. Thus p divides X_i(m_i-X_i) with X_i locally integral.

If X_i=A/Q is neither 0 nor m_i, this proves log R_i<=2h(X_i)+log(1+|m_i|). The strict margin 487/100 > 2*(1001/997)^4 implies h(M)<=C log(1+|m_i|)+C'. The aggregate trace bound then gives m_i^2<=C''log(1+|m_i|)+C''', bounding both |m_i| and h(M) uniformly in B_abc, a contradiction for sufficiently large B_abc. Hence all input values are integers. This completes the source-instance soundness proof.

## 4. Ordered completeness

For canonical nonzero integer inputs put A_i=[X_i]R0. This fixes the aggregate trace, the tree and a before prime selection. Apply the [v103 common-numerator CRT theorem](../abc_common_numerator_v103/common_numerator.tex) to the 192 distinct fixed contact positions +- (a+-s_i*r). Choose H,U and V_i=U-A_i with the same fixed differences and local comparison precision as that theorem. In particular, at a selected prime of group i the successful slot has all four formal points H,U,H-R0,V_i at the indicated places, with comparison errors C_i,I_i of valuation at least three. The raw reciprocal abscissas have valuation at least two. The shared R has positive valuation, and W_i=1 mod p there. At the other slot W_i either has a pole or is 1 mod p: the distinct valuation classes above exclude nonconstant terms of valuation zero except R^8, and an integral R has positive valuation. The norm-error identity then gives v_p(D_i)>0, including D_i=0. At this prime v_p(u)=1, v_p(F_i)=1, v_p(F_j)=0 for j different from i. The active and inactive gate computations above make every Wgate_j congruent to 1, so v_p(alpha)=1 and v_p(b)=1.

At the finitely many prepared places and at real infinity choose the slope with sufficiently large absolute value, with all point chart functions bounded on the prescribed neighborhoods. One may first choose allowed H,U outside the finitely many zeros of all C_i and poles of the required functions (fix an allowed H, then avoid the finitely many fibers of the nonconstant S_U; X_i!=0). As in v103, shrink the neighborhoods to fix nonzero valuations and use the finite avoidance and common reference/numerator CRT. In these neighborhoods u~z^2/a, c~a/z^2, W_i-1~c C_i^2 and D_i~c^2 Nm(C_i^2)/2, uniformly. Since F_i~z^16, the gate Rgate_i has nonzero leading term of order z^12; its square dominates u in Tgate_i. Thus Vgate_i tends to zero sufficiently fast, Wgate_i tends to 1, alpha~u, tau~1 and b~7c. These are open fixed-place conditions preserved by the retained supplier; all gate denominators are nonzero there. At real infinity b lies in (0,1). At two, the proved square property of a makes c a square of arbitrarily large positive even valuation and b in 7Q_2^2 of the requisite depth. At seven b has positive valuation. Include all center denominators and numerator primes, contact differences, bad chart primes and other fixed exceptions in temporary completeness avoidance. This is not a change of the fixed soundness exceptional set.

Outside this preparation set, at a nonselected prime with integral slope, F_all is a unit, so v_p(u)<=0. For nonintegral slope the leading terms and the prepared unit a give v_p(u)=2v_p(z), even. When v_p(u)<0 is odd, the two terms of alpha have opposite valuation parity; v_p(alpha)<=v_p(u)<0 and tau is a unit, so b has positive valuation outside seven. When v_p(u) is even, v_p(b) is even outside seven. All these assertions allow arbitrary new point denominators. The real and fixed-place choices make every gate denominator globally nonzero. Thus b is BB-prepared, and the same published native-pole realization theorem supplies its single five-equation quadratic block. Fill all registers by their definitions. This supplies a complete rational zero over every canonical source witness and proves projection completeness.

## 5. Census and verification

The table uses 76 outer variables, 104 chart/input-square variables, 27 height variables, 29 contact variables, 24 common detector variables, 156 private detector variables, and 21 product/pole variables, totaling **437**. There are 52 untouched outer residuals and 332 new residuals, totaling **384**. Every coordinate occurs, all residuals have ordinary degree at most two with coefficients in the same integer parameter ring, and the sum of squares has degree exactly four.

Run node build.js from this directory, optionally with --write. The deterministic compiler pins the frozen v114 source blob, preserves all outer equations by named monomial comparison, checks the field/contact polynomial expansions and derivative difference, verifies support and degree, and checks the strict rational height margin and 1,313 gate valuation fixtures. Those are exact algebraic checks, not a proof of the inherited arithmetic hypotheses or a full historical repository regression. The arguments above establish the conditional source-instance projection. No unconditional undecidability claim or optimality assertion is made.
