# Eight-integer transfer by symmetric binary packing (v142)

**619 / 639 rational variables; 554 / 572 quadratic residuals** (general / specified), uniformly in the instance on the cofinite tail. Exactly eight independently certified source integers. This improves the previous 622 / 642 bounds, despite increasing the residual count. No new arithmetic hypothesis is used: retain the inputs of v136, v137 and v139 (including the full-rational-domain scalar height input H4.1, the corresponding aggregate and contact-height estimates, rank-one group, formal/CRT and prime realization inputs, and BB prepared realization). The general threshold is ineffective; the specified one is effective under those inputs.

## 1. A small natural-number source, not a dense quartic

Use the Jones coding theorem and the corrected short-power source of v128 (pinned blob 94da64905107446920903f889265038b161f2f6f), with the v101 signed reconstruction and v97/v98 absorbed margin. First specialize the positive integer coefficients x,z,u,y, with x>32z. Work over the **nonnegative integers for every register of this inner source**.

The 52 named Jones rows have 76 supporting variables. Shift g,t,m in every row to g+1,t+1,m+1. Remove the three corresponding triangular positivity rows and their nine auxiliaries. Replace the three triangular variables in each of the alpha and absorbed eta inequalities by one nonnegative integer slack, so the corresponding equation is 2(alpha-1-slack)=0 or 2(eta-C_*^2-1-slack)=0. Delete the half-trace square and its auxiliary: c,d are already integers in the natural-number domain. Restore the two borrowed square registers by b2=b^2, int_b_30=b2^2, int_g_29=(g+1)^2, introducing one new register b2 (the other two occur in the retained rows). There are 63 natural variables and 51 quadratic equations.

For soundness, the nonnegative ell,e and the strict alpha inequality imply b>xy and q nonzero. Thus b^5>2z, and the shifted t,m enforce the original strict positivity of ell-u,e-y. All original short-power quotients are integral and the old auxiliary parameter is unchanged, so the zero-branch exclusion and signed reconstruction in v101 apply, with no v138-type change in parameter. The original source is recovered. Conversely its canonical positive witnesses satisfy the new natural-domain rows, with integer slacks and nonnegative definitional registers. This proves preservation of the cofinite undecidable instance projection using the same Jones coding theorem. All 63 natural registers below are packed digits, NOT 63 independently certified integers.

## 2. Symmetric sparse exponents

Write the 51 natural-domain quadrics as Q_j, 0<=j<E=51. Homogenize to degree two with one dummy coordinate z_0=1. This gives 64 vertices. A pair is forbidden if its product occurs in any homogenized quadric (linear and constant terms become products with the dummy). The independent symbolic audit in v143 checks all original coefficient polynomials in x,z,u,y, not just one specialization: every one of the 63 variables has a nonzero parameter-independent coefficient, and there are 136 forbidden unordered pairs, including loops. A perfect matching of the complement exists uniformly, for example the 32 pairs

    B5 AE; b E; q4 F2; n2 G; a GH; e H; lam I; Y S;
    p T; power_A U; YK V; el ac; ell c; i_half c02; j c04;
    power_alpha d; q g; gamma h; int_b_30 int_g_29; k m;
    n pell_crt_cF; pk power_AC; power_C power_D; power_delta power_modulus;
    q2 q3; q5 q8; r s; slack_alpha slack_eta; source_b2 source_c_square;
    sr t; tau w; F @dummy.

The compiler finds a matching directly on specialized support and checks it; the fixed matching proves success even if some specialized coefficients vanish. Move the dummy pair last and place the dummy in its minus slot. Let L=E, e_i=floor(3i/2), i=0,...,31, and D=L*2^48. Assign the two vertices of pair i positions n=D +/- L*2^e_i. All positions lie in [3D/4,5D/4], and the dummy position is uniquely minimal.

**Separation lemma.** Except for complementary pairs, every unordered pair of signed powers from this list (including repetitions) has a different sum. To see this, a nonzero positive sum is either a single bit (equal positive summands or a difference of adjacent powers), a sum of two distinct bits, or a positive difference of powers whose binary digits form a consecutive interval of ones. The first type can collide only if three consecutive exponent levels are present; the second can collide with a difference only for an interval of length two, again requiring three consecutive levels. Within each remaining type the endpoints are uniquely determined. Negative sums follow by sign reversal. The exponent set has no three consecutive levels. The only zero sums are complementary pairs, and none is tested. Translating and multiplying by L preserves uniqueness. The further equation offsets j in [0,L-1] are distinguished modulo L. The compiler additionally checks all 2080 pair sums with repetition.

## 3. Two integer code variables suffice

Take independently certified integers f>=2 and 0<=g<N0. Set b=f^2, B=beta*b^2, where beta is a power of four strictly larger than 16(1+sum_j ||Q_j||_1)*64^2. Set N0=B^(2D), V=B^(8D), N=4*N0*V, M=N^2. Move an equation with nonzero constant to the last position, reversing its sign if its constant is negative. Such a row exists (a norm row, for example).

Write Q_j^hom=sum_{i<=k} a_(j,ik) z_i z_k. Define the integer pack

    P = sum_(j,i<=k) w_ik a_(j,ik) B^(4D+j-n_i-n_k),
    w_ii=2, w_ik=1 for i!=k.

The highest term is the positive dummy square in the last equation. Every exponent is between 3D/2 and 5D/2+E-1, hence below 3D. The coefficient norm bound ensures 0<P<B^(3D); the highest coefficient dominates all lower terms. Define

    mask=N0-1-(b-1)*sum_(i>=1) B^n_i,
    C=g+B^n_0,
    K=C^2*P+(B/2)*(V-1)/(B-1),
    S=g+2K*N0,
    T=mask+(B-2)*N0*sum_(j=0..E-1) B^(4D+j),
    R=(S+T+1)*N+T+1, r=(N-1)*R.

These are integers once f,g are integral: the geometric quotients are finite sums and B is even. The two guards are f>=2 and g(N0-1-g)>=0, imposed by the existing three-triangular-number convention. The mask has radix digits B-1 except at active positions where they are B-b. The intervals imply 0<=mask<N0, 0<=g<N0 and 0<C<2N0. Hence 0<C^2P<4B^(7D)<V and 0<=K<2V. Thus 0<=S,T<N. Also r>=N^2-1, M>=16, M>=4b. If f is divisible by 3 then so is N; otherwise b=1 mod 3 and beta=1 mod 3 imply N=1 mod 3. In both cases 3 divides Mr.

**Carry argument.** When b is a power of two, so are B,N. Write N=2^l. The identity

    r=(S+T)N^2+(N-1-S)N+(N-1-T)

gives sigma_2(r)=2l+sigma_2(S+T)-sigma_2(S)-sigma_2(T) by the disjoint binary blocks (no bound on S+T below N is needed). The standard binary digit-sum formula for v_2(binomial(2r,r)) is sigma_2(r), by the valuation of factorials. Consequently M=N^2 divides the central binomial exactly when the binary sum S+T has no carries. This is the carry mechanism of BDHMS, arXiv:2506.20909v3, Lemmas 1.4 and 1.6, with a different packing; the displayed proof gives the needed version directly.

The lower block enforces g AND mask=0, i.e. g=sum_(i>=1) z_i B^n_i with integers 0<=z_i<b. Then C has these digits and the single dummy digit 1. The ordinary coefficient at degree 4D+j of C^2P is exactly 2Q_j(z): separation excludes all foreign unordered pairs and equation offsets, and the factor 2 on the diagonal corrects the cross-term multiplicity in C^2. For every degree the absolute value of the ordinary coefficient is bounded by 2*64^2*b^2*sum_j ||Q_j||_1 < B/2. All degrees are below 8D. The added bias B/2 in every radix digit therefore makes the digits of K lie strictly between 0 and B, with no inter-digit carries or borrows. The upper mask tests the binary digits of 2K against B-2 at precisely the E selected positions. Equivalently it tests K against B/2-1 there. Each positive digit less than B passes exactly when it equals B/2. This means Q_j(z)=0 for all j.

Conversely take any solution in nonnegative integers of the inner source, choose b=4^n larger than its largest digit, f=2^n, and the corresponding g (possibly zero). The lower mask passes and all tested digits equal B/2, giving M|binomial(2r,r). Thus the conjunction of b being a power of two and this binomial divisibility is equivalent to the original source projection.

## 4. Six remaining certified binomial witnesses

Use exactly the six additional integers w,s,h,gamma,j,i_half from v141's outer signed binomial certificate, with i=2*i_half+1. Keep its 24 rows, including the first-Pell half-trace square, but not the old absorbed power_C term. The prefix is integral and has r>=1, M>=16, M>=4b and 3|Mr; this last property implies 3|a for a=(wM+1)r(sM). The nonzero target guards force w,s nonzero. The shifted trace and v106 imply c,d integral; the small congruence makes k integral with |k|>=r+1 and the margin gives |c|>2r+1. The v95 index theorem, v101 signed small-index and linear-trace arguments and alternating truncation recover b a power of two and M dividing the central binomial. Only the binomial part of v101 is needed, not its auxiliary-power recovery. For completeness use the canonical positive binomial witnesses, the odd second index multiple of (2r+1)c (increase it to ensure i>1), positive third-Pell quotient and v106 half-trace. These have nonzero direct targets and shifted targets g+1,i_half+1. Thus the eight certified inputs really suffice: f,g,w,s,h,gamma,j,i_half.

## 5. Quadratic compilation

No giant radix powers are coefficient literals. Compute B^E once, then its 48 iterated squares; keep one inverse for each of the 32 selected powers. Write X=B^D, and let Z_i be the signed factor B^(n_i-D) for vertex i. Both Z_i and its inverse are already available. The Horner circuit with 51 quadratic rows evaluates the weighted homogeneous quadrics in the complementary factors Z_i^(-1), with powers B^j. Multiplication by X^2 recovers P. The other geometric quotients have nonzero denominator B-1 and need only bilinear rows. The square b=f^2 is reused by the elliptic comparison chart. The entire outer source has 197 coordinates and 183 residuals, irrespective of the specialized coefficients.

For the v139 Boolean interface use eight linear targets (shift g and i_half only), so there are eleven aggregate points and 44 Boolean failures; the fixed p<=60 exclusion suffices. The v136 recursive scalar estimates, with its conservative twelve-input height majorant, work for eight inputs with the original larger square multiplier 2^64*149^2*C_parameter^2. Indeed S_n<=2^8 S_0, its 149 valuation persists, the dyadic depth remains 84, and the real lower bound only increases. The v137 linear-target guard works without any further positivity assumption. The v133 weighted height estimate applies to eleven points (or enlarge the constants to their fifteen-point counterparts). Thus the original v139 proof applies with the 8-input counts. The interface adds 422/442 coordinates and 371/389 residuals. This is a uniform quartic transfer under the retained premises; the instances are coefficients, not quantified variables.

Run node build.mjs instance.json 2 or 3, where instance.json supplies decimal integer strings x,z,u,y with x>32z. Fix the universal coefficients z,u,y furnished by Jones's theorem. The builder is uniform for every such choice; they have not been numerically instantiated as a particular nonrecursive set. The supplied fixtures are for x=100,z=u=y=1, not claimed universal or known solvable. Replay, symbolic support and finite arithmetic checks are documented in v143. No full CI or independent proof of the imported premises is claimed.
