# v147: one common numerator and selective concentric contacts

**527 / 560 rational variables, 476 / 507 quadratic residuals (general / specified).** Eight independently certified source integers. One recursive scalar pole, two/three comparison poles. All results are conditional on the retained arithmetic and coding premises, including the full all-sign Gaussian prime-pattern assertion (its opposite-order pairwise coprimality is needed here). The specified coefficient threshold remains effective relative to the retained quantitative premises; the general threshold is ineffective. No ordinary abc hypothesis is added to these routes.

## 1. Unweighted common-numerator chart

Use the notation of v131/v143/v146, with K=Q(rho), rho²=2, D=11-6rho, d=3-rho, E: y²=x³-Dx, R0=(1+rho,2rho), P0=2R0. The reference H,H-P0, three growth pairs, scalar extraction, recursive scalar normalization, and eight-integer packed source of v145/v146 remain unchanged. Denote the eight nonzero rational targets by k_i (the existing shifts of g and i_half included). Write f(Q)=1/x(Q), S_Q=y(Q)/x(Q), z(Q)=-1/S_Q on the formal chart.

Store one common numerator U by the three fields F,S,X satisfying FX=1, S²+DF=X. For each i store only T_i,G_i,eta_i, with pi_i=eta_i+S+T_i and rows

    pi_i F=eta_i G_i,
    D(F+G_i)=(S-T_i)eta_i-T_i².

Indeed, with d_i=pi_i F=eta_i G_i, the second row implies S²=(S-T_i)pi_i-D(F+G_i), and hence

    1=F(S²+DF)=d_i(S-T_i)-DFG_i=G_i(T_i²+DG_i).

This recovers the full unscaled v131 finite-difference chart, including its tangent and finite torsion cases. In particular G_i is nonzero, V_i=(1/G_i,T_i/G_i), A_i=U-V_i is finite and x(A_i)=eta_i pi_i. The field d_i need not be stored. No scaling by a possibly nonintegral target is used in this chart.

Form the unweighted aggregate U_0+rho V_0 = sum x(A)+11d+2^32, with the sum over the eight private and three growth differences. The two real embeddings are at least 2^32, since x(A)>=-d in each embedding. Set t_0=lambda, t_1=lambda+U_0; in the specified route also t_2=t_1+2^32+V_0². As in v131, the trace estimate (or the effective two-coordinate torsion-sum estimate) bounds B² by K(1+max_j h(t_j)), where B is the maximum of 1 and the absolute difference labels, including the odd b=2m+1. Here and below h is the inherited logarithmic height. Constants depend only on the fixed contact choices and the retained estimates, not on witnesses or the scalar coefficient N.

## 2. Fixed dilations and the dominance gate

Let Theta_0={0,-1/2,-1,1/2399,-32/407}; set r=2 or 3/11 in the general or specified route. Use the ten roots Theta=Theta_0 union (r-Theta_0) and center c0=r/2. For 0<=i<8 take l_i=16^i, Theta_i=c0+l_i(Theta-c0), and G_i^contact(t)=prod_{theta in Theta_i}(t-theta). These are pairwise disjoint fixed sets; the ratio of maximum to minimum absolute nonzero distances from c0 is less than 16 for either original set. All their absolute positions are less than 2^30, so the shifts t_j-t_j' separate all the contact positions. Each polynomial is monic of degree ten and is a degree-five polynomial in (t-c0)^2. Thus all eight reciprocal equations share the same five powers.

Put q_ij=1/G_i^contact(t_j), q_j=(sum_i q_ij)/8, C=sum_j q_j, u C=1. Enlarge the fixed exceptional set S to contain the old good-prime exclusions, p<=60, and all primes in denominators of, and differences between, the distinct fixed roots in each union (and fixed dilation factors). At a prime outside S, if t_j is nonintegral then all q_ij have positive even valuation; if t_j is integral then at most one q_ij has negative valuation, and that valuation equals v(q_j). Write M_ij for the product of primes outside S at which v(q_ij) is negative odd. The old reflected contact bound applies to (t_j-c0)/l_i+c0, not to a new unproved modular contact family. Fixed affine height changes and the fixed added exceptional primes give

    h(t_j) <= H M_ij^(7/6)

for every i,j, with effective H in the specified case. In particular B² <= K' max_j M_ij^(7/6) for EACH i, increasing K' since radicals are at least one.

For a shared rational harmonic value E_g defined below use, for each j, the following gate (j1,j2 are the other contact indices, in their fixed builder order):

    alpha_j=1/q_j+E_g^4+q_j1^4/q_j^3
                    [+q_j2^4/q_j^2, if three contacts],
    tau_j(1+alpha_j)=alpha_j,
    pole_j=7 q_j tau_j².

The actual quadratic equations are q_j V1=q_j1², and in the three-contact case q_j V2=q_j2², with the other squares stored; then alpha'_j=1+q_j E_g^4+V1² [+V2 q_j2²], tau_j(q_j+alpha'_j)=alpha'_j, v_j=q_j tau_j, pole_j=7v_j tau_j. These force q_j nonzero: q_j=0 forces all other q's zero, contradicting u C=1. The literal square E_g^4 is computed by two squarings.

At a consumed prime v(q_j)=-e with e positive odd, the four summands of alpha_j have pairwise distinct valuation classes modulo 4 (omitting zero terms with infinite valuation). In particular alpha_j is nonzero. The native pole obstruction implies v(alpha_j)>e/2: otherwise v(tau_j)<=e/2 and the pole has negative odd valuation. It follows that

    v(E_g)>e/8,
    v(q_j1)>-5e/8, and v(q_j2)>-3e/8 (if present).

Thus v(C)=-e, v(u)=e. The normalized coefficients omega_ij=q_ij/(8C) are all integral at p, with exactly one nonzero residue, namely 1 at the unique active group (i,j). For a different j, a negative q_ij must equal the valuation of its q_j; this proves the assertion even if arbitrary witnesses have coincident contact primes. At any positive odd v(q_j), the same distinct classes show alpha_j has negative valuation (the 1/q_j term is negative), hence tau_j is a unit. This last property is necessary because the sum of reciprocals may acquire positive odd valuation even when every summand has even valuation.

## 3. Shared primary and selective alternate test

Store the rational mean mu and field J by

    8 C mu = sum_ij q_ij k_i,
    8 C J  = sum_ij q_ij J_i.

Store ell with ell S=2 S_H. Add to the unchanged v143 reference and growth Boolean fractions B_1(F), B_1((ell-mu)^2), where B_n(L)=L/(u^n+L). Let W_g=u+sum of these reference, common-primary and growth fractions. There are fewer than 60 fractions. They have the same Boolean property as in v139: at v(u)>0 odd, n odd and v(L) even (including zero L), they are integral and their residue is 0 exactly when v(L)>n v(u).

Store T0 and U_T by mu T0=2 conj(S_(H-P0)), U_T=u T0². Define private field fractions by

    L_i=(conj(T_i)-T0)^2+U_T conj(G_i),
    J_i(U_T+L_i)=L_i.

Finally use

    W=W_g²+C J²,  E_g Tr(W)=Nm(W).

The identities are all quadratic with the stored squares and U_T. At a consumed prime, each slot of W_g is integral; its valuation is positive iff every Boolean fraction passes there, since p>60. At most one slot passes, because H and H-P0 cannot both be formal at the same good slot. An inert prime cannot pass. The summands of W have even and odd valuations, so v(W)>0 iff v(W_g)>0 and v(J)>e/2. This implies W is not identically zero at any consumed prime, and the norm/trace equation has nonzero trace there. If both slot valuations of W were nonpositive, v(Nm W/Tr W) would be at most their maximum. Since E_g has positive valuation, there is a unique successful slot. Importantly the growth tests have been established without assuming any private J_i integral.

The unchanged v143 growth precision gives M_ij³ | Delta_idx for the nonzero integral Lucas residual, |Delta_idx|<=10 B^4. The contact-height bound for any i gives B²<=constant B^(14/9) in this case. The scalar bound A=|a|>=149^(9N+7) contradicts this for sufficiently large fixed N. Thus Delta_idx=0; v143 gives log B>A/4+log A for A>100.

Only now discard the prime factors of the numerators and denominators of the eight nonzero targets; their union radical P_bad has log P_bad<=2 sum_i h(k_i). At a remaining consumed prime, mu reduces to the unit k_i of the active group, and the reference opposite slope has negative valuation, so v(T0)<0. The threshold U_T has odd valuation e+2v(T0). For every private index l the two terms of L_l have distinct parities (v(G_l) is even by the good curve equation). Equality v(L_l)=v(U_T) could occur only when v(G_l)=0 and 2v(conj(T_l)-T0)>e+2v(T0). But then conj(T_l) has the negative valuation of T0, contrary to G_l(T_l²+D G_l)=1 when G_l is a unit. Thus all J_l are integral Boolean in the successful slot, with residue zero iff v(L_l)>v(U_T); a zero denominator is excluded by the equations because U_T is nonzero here.

Since J has positive valuation and the normalized coefficients have a unique active residue 1, that group's J_i passes. Therefore its opposite G_i has positive valuation and v(conj(T_i)-T0)>v(T0)+e/2. In particular both U and V_i are formal at the respective slots, and the two relative formal parameter ratios are congruent to k_i modulo p:

    2 S_H/S = ell = k_i mod p,
    2 conj(S_(H-P0))/conj(T_i) = mu T0/conj(T_i) = k_i mod p.

The relative logarithm congruence of v131 applies; multiplying by the integral reference labels rather than dividing by them recovers the integral difference label m_i=2 nu(A_i) modulo p. This also works if a reference label is divisible by p. Thus k_i=m_i mod p.

If k_i differs from m_i, M_ij<=P_bad |num(k_i-m_i)|<=2 P_bad B exp(h(k_i)). The estimate for this particular i gives

    log B <= (7/5)(2 sum_l h(k_l)+h(k_i))+C_*
           <= (119/5) delta_N A+C_*,

where h(k_l)<=delta_N A and delta_N tends to zero by v136/v143. Choose delta_N<1/100, and A large enough that log A>C_*. This contradicts Lucas growth. All eight targets are integral. The unchanged sparse packing and binomial source argument finish soundness. All new constants are fixed independently of N; the effective variant can select a sufficiently large N from the inherited effective estimates. No independent integrality test is deleted.

## 4. Ordered completeness

Choose canonical nonzero positive targets and the scalar/growth labels as in v143. Fix A_i=[k_i]R0 and the growth differences before computing the aggregate and the finite contact position list. Apply the retained all-sign Gaussian supplier to all 80 times the number of contact lists, with a common square denominator and the fixed-place preparation. This uses the full hypothesis from the arithmetic dependencies and v103 common-numerator lemma, in particular pairwise coprimality of opposite divided orders at distinct primes and their cross-coprimality with primary orders. These are not consequences of mere distinctness of the primes. The required half-generator annihilators, short interval, avoidance of fixed congruence moduli and nonzero k_i, and synchronized reference depths are as in v103/v143. For each selected prime of group i, choose H=[h]P0 with the original primary and opposite reference conditions and scalar preparations. Choose one U=[j_idx]R0, with j_idx=0 modulo the primary annihilator, j_idx=k_i modulo the opposite one, and j_idx=h k_i modulo a sufficiently high power of that selected prime. As in v103, the primary two-parts are compatible with the initial progression (multiple of 64), the opposite moduli are odd, and prime powers are independent of the divided orders. Keep the fixed-place and real recurrence neighborhoods by CRT. Thus U and V_i approximate [h k_i]R0 and [(h-1)k_i]R0 in their formal slots at that prime. Growth pairs retain their previous separate numerators. This uses no shared-numerator requirement at the scalar pole.

At a selected prime of (i,j), q_ij and q_j have valuation -1, all others are integral, and mu=k_i mod p with k_i a unit. The two relative slope comparisons at the prepared common numerator give ell=k_i and conj(T_i)/T0=1 mod p, by the relative formal logarithm estimate (or arbitrary local precision followed by its unit correction). The reciprocal valuations of U,V_i are positive even. Consequently the selected private J_i is positive in valuation and all inactive J_l are integral in the successful slot by the preceding threshold argument. Hence J has valuation at least one, W_g has positive valuation by the unchanged growth/reference preparation and common-primary comparison, and W has positive valuation. The other slot fails W_g, hence has W valuation <=0. The harmonic E_g then has valuation at least one. The gate alpha_j has valuation exactly one (the other terms have valuations >=4, >=3, >=2 respectively). Thus tau_j and the selected pole have valuation one.

For nonselected primes outside the finite preparation set, the linear contact factors have the inherited prime-factor support from the supplier: each individual q_ij has nonnegative valuation. Their sums q_j can acquire odd positive valuation; the new gate covers precisely this case. Even valuation of q_j gives even valuation of the nonzero pole outside 7, regardless of auxiliary denominators. At prescribed fixed places and in the real large-slope limit, q_j is asymptotic to lambda^(-10) by monicity and averaging, C to (#contacts)lambda^(-10), and u tends to infinity. The normalized mean tends to the arithmetic mean of the fixed positive targets, which is nonzero. Choose point neighborhoods avoiding zeros of required slopes and 1+conj(G_i) (finitely many excluded point fibers), and retain the old scalar/reference preparation. The private J_i tend to conj(G_i)/(1+conj(G_i)) with bounded values; W_g is asymptotic to u, W to u² and E_g to u²/2. The E_g^4 term dominates alpha_j, so tau_j tends to 1 and the pole is asymptotic to 7lambda^(-10). This gives positive real values below 1, the required dyadic squareclass 7 with arbitrarily large even depth, and positive seven-adic valuation. All new denominators are nonzero in these prepared witnesses. The inherited BB realization supplies the pole coordinates. This is simultaneous conditional completeness, not a numerical solution of a particular universal instance.

## 5. Compilation and status

The builder is uniform in the positive integer source parameters (x>32z), pins the same v128 source table as v146, retains the exact 183/171 packed prefix and all its eight input certifications, and generates the 527/476 and 560/507 tables. Five parameter fixtures in each route passed exact compilation and all-degree/support checks. See the independent finite checks in verify.mjs. Neither a full CI replay nor proofs of the inherited elliptic, height, Gaussian supplier or native-pole arithmetic premises are claimed. The output is a conditional upper bound, not a lower bound or an unconditional undecidability theorem.
