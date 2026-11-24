# v150: interpolated alternate slopes and reciprocal comparison poles

**510 / 542 rational variables; 459 / 489 quadratic residuals**, general / specified. Eight source integers, one scalar pole and two/three comparison poles. This composes v149 (fractional-linear scalar recursion) with a revised comparison interface. The packed 183-register, 171-row source is unchanged. The full v147 arithmetic premises, including the all-sign order compatibility, recurrence, and H4.1, are retained. The general parameter is ineffective; the specified parameter is effective relative to its inherited estimates.

## 1. Absolute alternate comparisons and normalized growth ratios

Use the physical charts and unweighted aggregate of v147. In its notation, the primary reference and opposite reference are H and H-P0, with P0=2R0. The common numerator U and each private V_i give A_i=U-V_i. At every consumed prime let e=v_p(u)>0 be odd, with C=1/u. The group weights and normalized mean mu are unchanged.

Keep T0 with mu*T0=2*conj(S_(H-P0)), but remove T0^2 and U_T=u*T0^2. Use

    L_i=(conj(T_i)-T0)^2+u*conj(G_i),
    J_i(u+L_i)=L_i.

All equations are quadratic. Here T_i is the slope and G_i the reciprocal abscissa of V_i. At a successful slot, after the same costed exclusion of the numerator and denominator primes of the eight targets, mu is a unit and T0 has negative valuation. The two summands of L_i have distinct parities. If v(L_i)=e, the even square cannot give this valuation: G_i would be a unit and 2v(conj(T_i)-T0)>e. Then conj(T_i) has the negative valuation of T0, contradicting the curve identity G_i(T_i^2+D G_i)=1 (conjugated at this slot). Therefore the fractions J_i are integral Boolean there; residue zero is equivalent to v(L_i)>e. A passing private test has v(G_i)>0 and v(conj(T_i)-T0)>e/2, and gives the required alternate ratio modulo p. The old private height-budget proof still applies.

For a growth pair keep its primary ratio r_j and two formal tests. Replace the absolute alternate error by a second ratio r'_j satisfying

    r'_j conj(T_j)=2 conj(S_(H-P0)).

The failure B_5((r_j-r'_j)^2), in place of B_3 of the absolute error square, requires v(r_j-r'_j)>5e/2. Both ratios are defined in a passing slot by the reciprocal formal tests. Relative order-four formal logarithm precision implies h r_j agrees with the primary integral R0 label, and (h-1)r'_j with the opposite one, modulo p^3. These are absolute congruences after multiplication by the integer indices, even if h or h-1 is divisible by p. Subtraction gives the difference label modulo p^3 and in particular integrality modulo p of the primary ratio. The same Lucas residual and B_5 test yield M_ij^3|Delta_idx. No stronger growth precision or height estimate is needed.

### Completeness without synchronized formal depths

The stronger absolute private error above requires changing the order of the local choices; merely replacing its threshold in the v147 witnesses would not suffice. Fix the integer targets, scalar and growth labels, and all difference points before choosing the contact prime pattern, as in v147. The mean mu is then fixed by the contacts and targets. At each selected prime of group i it is congruent to the p-unit k_i. Impose h=2 modulo p in the common reference progression (using the prime avoidance and short-interval coprimality in v103/v147). Thus both h and h-1 are p-units, and both formal depths are positive, but they need not be equal. Retain the scalar finite-place and real requirements, disjoint from these fresh primes.

Choose the growth pairs as the original exact multiples of H and H-P0. The normalized relative log comparisons now have precision at least four at both slots independently of their depths; they pass B_5. This avoids any need to synchronize the reference depths.

For the common numerator index j, keep the primary residue 0 modulo the primary annihilator and the opposite residue k_i modulo the opposite annihilator of R0. In the opposite slot, V_i=[j-k_i]R0 ranges on the formal group. The step of the common index progression is a p-unit multiple of the opposite reduction order (the orders at all selected primes are prime to p). Its formal logarithm generates the ideal p^d Z_p, where d is the depth of H-P0, since h-1 and 2 are p-units. More explicitly, if r is the reduction order of R0, the formal logarithm of [r]R0 has this depth; the progression step and 2(h-1) are both multiples of r by p-units. Hence, by the formal-logarithm isometry, varying j along this progression to sufficient p-power precision approximates any formal parameter of valuation at least d. Prescribe the opposite parameter z(V_i) to approximate

    mu*z(H-P0)/2

with difference of valuation strictly greater than 2d. Since T_i=-1/z(V_i), this makes v(conj(T_i)-T0)>0 in the successful slot. The prescribed parameter has depth d, and the relative logarithm estimate shows j-k_i = (h-1)*mu modulo p; thus j=h*k_i modulo p. The primary ratio 2*z(U)/z(H) agrees with mu modulo p since h is a unit. The primary formal condition holds by the original annihilator congruence. Each required p-power precision is independent of the other selected primes and fixed-place conditions; apply the full compatible CRT and real recurrence as in v103/v147.

This also gives the old fixed-place and real bounded point neighborhoods. The mean tends to the nonzero mean of the canonical positive targets as the large slope goes to infinity; avoid the same finitely many zero slopes and 1+conj(G_i)=0 fibers. Thus T0 is bounded and J_i tends to conj(G_i)/(1+conj(G_i)). The revised growth ratios are likewise bounded on these neighborhoods.

## 2. Remove the stored field square of the global detector

Put W_g=u+sum B over all retained reference, common-primary and growth tests. Store Q by u Q=J^2, where J is the normalized selective sum of private fractions. Now use the affine field expression

    W=W_g+Q,        E_g Tr(W)=Nm(W).

This replaces W_g^2+C J^2 and its separately stored square and sum. At a consumed prime W_g is integral at every slot by the Boolean proof, with positive valuation precisely when every such test passes, since p>60. The term Q has odd valuation 2v(J)-e (or is zero). If negative it dominates W_g, and if positive then v(W)>0 exactly when v(W_g)>0. Therefore positivity in a slot still implies all reference and growth tests and v(J)>e/2, before the private integrality argument. At most one slot succeeds because H and H-P0 cannot both be formal in the same slot. An inert prime cannot succeed. In particular W cannot vanish identically at a consumed prime, and the same norm/trace inequality as v147 yields a successful slot from v(E_g)>0. At selected primes the private Boolean values are integral and J has positive valuation, so the harmonic value is positive in valuation. At fixed places W_g is asymptotic to u, J bounded and Q tends to 0, hence W~u, E_g~u/2. This is sufficient for the following gate.

## 3. Contact dominance without the three stored squared weights

The contact groups, weights q_j, all q_ij, C=sum q_j, and height estimates are unchanged. For each list put

    X=q_j1^2/q_j,
    A=E_g^2                                      (two lists),
    Y=q_j2^2/q_j, A=(E_g^2+Y)^2                  (three lists),
    alpha'=1+q_j A+X^2, alpha=alpha'/q_j.

In the three-list version E_g^2+Y is a single squared-sum register, in place of all three common q_j^2 registers and the old E_g^4 register. In the two-list version use E_g^2 instead of E_g^4. In the compiler q_j is a linear expression in its group weights, so the quotient rows q_j X=q_j1^2 and q_j Y=q_j2^2 are literal quadrics with no intermediate weight squares. If q_j=0 these rows force all other q's zero, contradicting C u=1.

Whenever v(q_j) is odd, X and (when present) Y have odd valuation or are zero. The two odd terms 1/q_j and X^2/q_j of alpha have distinct classes modulo four; A has even valuation. In the three-list version the two terms E_g^2 and Y in its square have distinct parities and cannot cancel. These facts hold also for negative odd v(q_j).

At a consumed prime v(q_j)=-e, the new reciprocal pole chart below implies v(alpha)>e/2. The parity separation then gives

    v(E_g)>e/4        (two lists),   v(E_g)>e/8 (three lists),
    v(q_j1)>-5e/8,    v(q_j2)>-3e/8 (when present).

Indeed X^2/q_j has valuation 4v(q_j1)+3e; in the three-list version A has valuation 2 min(2v(E_g),2v(q_j2)+e). The unique smallest contact valuation is consequently that of q_j, and C has valuation -e. The normalized weights have exactly one active residue 1, as in v147. All local growth, private comparison and global height arguments follow from sections 1 and 2. At any positive odd v(q_j), alpha has negative valuation by the first term and the same no-cancellation argument. This last assertion is used only for completeness at foreign primes.

## 4. Reciprocal native-pole rechart

Use the row (t-1)alpha'=q_j, so t=1+1/alpha. Store t^2, and use the five quadratic native rows for

    e0^2+7q_j p'^2=1,
    v'w'=e0(t^2-7q_j),
    v'^2-w'^2=7q_j z'^2

with p'^2,z'^2 stored. When t!=0 these are precisely the native equations of v104 for physical d=7q_j/t^2, with p=t p', v=v'/t, w=w'/t and z=z'. The t=0 branch is excluded **at every consumed prime**: the first equation and distinct valuation parity imply e0 is a unit; the second gives v_p(v')+v_p(w')=-e, so their valuations are unequal; the last equates a finite even valuation with an odd one (or infinity), impossible. This is the same elementary reciprocal-chart argument used in reciprocal_gate53. We need no assertion about t at lists with no consumed primes.

The physical pole obstruction now gives -e-2v(t)>=0; parity and integrality imply v(t)<-e/2. Thus v(alpha)=-v(t)>e/2, as used in section 3. Conversely, at a selected simple prime v(q_j)=-1 all the other q weights are integral and E_g positive. The formula gives v(alpha)=1, v(t)=-1 and the physical pole has valuation 1. At a foreign positive odd valuation of q_j, alpha has negative valuation and t is a unit, so the physical input has nonnegative valuation. The other foreign valuations are even. For the real and fixed-place asymptotics, q_j~lambda^(-10) and E_g~u/2; A grows as u^2 or u^4, dominates the reciprocal and other-weight terms, so t tends to 1. The native input is asymptotic to 7 lambda^(-10), giving the same real interval, dyadic squareclass and depth and seven-adic integrality. Apply the inherited BB realization to the actual physical inputs, then lift by the displayed substitutions. In the constructed witnesses t!=0 follows also at their own selected primes.

## 5. Count and verification

Starting from 519/552, remove four common private-threshold coordinates, two global field coordinates, the old E_g^4 coordinate, and one native-pole coordinate per comparison list. In the three-list case the three deleted squared-weight coordinates are offset by three new squared-sum coordinates. Thus 510/542 and 459/489, as compiled. The original growth ratio register count is unchanged; the normalization uses the same u^5. All individual group weights are still present. No seven-integer source claim is made.

The verifier checks ten exact fixture builds, quadratic support and degree, the v149 scalar polynomial identity, endpoint and dyadic facts, and the new finite valuation profiles. Those checks supplement rather than replace the quantified proof. No full repository CI or independent discharge of inherited arithmetic hypotheses is claimed.
