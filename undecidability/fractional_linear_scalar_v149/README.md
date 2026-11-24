# v149: fractional-linear scalar recursion

**519 / 552 rational variables; 468 / 499 quadratic residuals.** This is the v147 transfer with eight source certificates, the same packed source (183 registers, 171 rows), and the same three or four native poles. All v136/v147 arithmetic premises remain. The scalar height input is the full-family H4.1 of v68, including the infinity contact. No additional abc premise is imposed.

## 1. Positive recursion and preservation of odd support

Let C=149^N, N>=1, P*=51948354689656, and r(Y)=Y(Y-1)(Y-2401)(32Y+343). For nonzero rational targets k_i, i=1,...,8, replace the scalar recursion in v136/v147 by

    S_0=5*2^20*149*C^2,
    W_i=S_(i-1)*k_i^2,
    Y_i=2504+W_i/(1+W_i),
    S_i=S_(i-1)*r(Y_i)/(P* (Y_i-2503)),
    R=2^64*149^2*C^2*S_8/(1+S_8)^2.

All quantities are defined and positive. In particular 2504<Y_i<2505, and monotonicity of the four factors of r gives

    1/2 < r(Y_i)/(P* (Y_i-2503)) < 2

because r(2504)=51948354689656 and r(2505)=52515494466240<2P*. Hence 2^(-8)S_0<S_8<2^8 S_0, S_8>1, and R>2^34*149/5>100.

Enlarge the fixed exceptional set of H4.1 by 149 and the prime divisors of r(2503), r(2504), r(2505) (and retain all previous fixed exclusions). Define M_i to be the H4.1 five-contact odd radical of Y_i outside this enlarged set.

At a prime p outside the set, suppose v(S_(i-1)) is odd. Then v(W_i) is odd and nonzero. If positive, Y_i=2504 mod p; if negative, Y_i=2505 mod p. In both cases r(Y_i)/(P*(Y_i-2503)) is a unit; the odd valuation is preserved exactly.

At a new finite contact prime of M_i, the factor r(Y_i) has positive odd valuation and Y_i-2503 is a unit by the exclusion of the prime divisors of r(2503). At an infinity contact v(Y_i)<0 is odd; the ratio has valuation 3v(Y_i), also odd. This latter case is essential: the fractional-linear normalization does not have square reduced denominator. In either case the previous S valuation cannot have been odd, by the endpoint argument, so the update captures the new prime. Subsequent updates preserve that odd valuation. The final map S/(1+S)^2 sends both positive and negative odd valuations to positive odd valuations.

At 149, r(2504)=75 and r(2505)=134 modulo 149; the extra denominator is 1 or 2 modulo 149 in the endpoint cases. Inductively v_149(S_i)=2N+1, so v_149(R)=4N+3 exactly. The scalar valuation proof of v136 applies unchanged to the physical R, reference and scalar difference. Thus with A=|a| and L=9N+7,

    149^L M_i^3 divides A,     A>=149^L.

The full-family H4.1 estimate (v68, as simplified in v136) gives h(Y_i)<=H_s M_i^3, with effective fixed H_s after accounting for the newly excluded primes. For instance multiply 2^238 by the cube of the product of all added primes. No new height theorem for a transformed contact set is invoked.

The inverse fractional-linear formula W_i=(Y_i-2504)/(2505-Y_i) gives h(W_i)<=h(Y_i)+log(2506) by evaluating the two integral linear forms on a reduced numerator/denominator pair. The rational map r(Y)/(P*(Y-2503)) has degree four, so its height is at most 4h(Y)+K_0, for a fixed effective K_0 (use homogeneous polynomials of degree four and their coefficient one-norms). Consequently

    2h(k_i)<=h(W_i)+h(S_(i-1))
             <=(1+4(i-1))*H_s*149^(-L)*A + O(N+1).

All implied constants are independent of the rational witness and effective relative to the inherited quantitative inputs. This gives h(k_i)<=delta_N A with delta_N->0 and effective delta_N. It supplies exactly the height absorption required in v147, whose comparison detector and growth circuit are otherwise unchanged.

## 2. Ordered completeness

For an integer source witness, all targets are nonzero; the recursion is fixed before the scalar elliptic points. At 2 the initial S_0 has valuation 20 and unit part 1 modulo 8 (the initial factor 5 cancels the unit class of 149). If this persists at S_(i-1), then W_i is divisible by 2^20 locally, and Y_i-2504 is too. Since v_2(P*)=3, r(Y_i)/P* is 1 modulo 2^17, and Y_i-2503 is 1 modulo 2^20. The update preserves depth 20 and the squareclass. The final R is a dyadic square of depth 84. The number 9792 is a dyadic square of depth 6, so R(R+9792) is a dyadic square. R(R+9792) has square reduced denominator for every rational R, by the argument in v136. The finite scalar preparation set is recomputed for the new fixed R. The existing scalar isometry, finite-place and real preparation, and BB native realization apply to this R>100, including 149. The ordered comparison completeness of v147 follows without any change.

## 3. Exact quadratic compilation

Replace the two old W_i and denominator registers by one inverse-square register v_i with k_i^2 v_i=1. Write

    (Y_i-2504)(v_i+S_(i-1))=S_(i-1),
    P_i=Y_i^2-76521 Y_i/64,
    (Y_i-2503) r_i=32 P_i^2-(5951086353/128) P_i
                              -(455376332353657/8192) Y_i,
    P* S_i=S_(i-1) r_i.

The polynomial identity in the third row is the one in v136. The inverse-square row forces k_i nonzero, and induction gives positive denominators, so no spurious zero-denominator branch is admitted. The final scalar normalizer, physical scalar and pole rows are unchanged.

This eliminates one scalar coordinate and row for each of eight targets. Five source parameter fixtures per comparison route were compiled exactly and checked for the announced counts, degrees and full support. See the arithmetic and compiler verifier in v150. The two/three-contact effectiveness distinction is unchanged. This is a conditional improvement, not an independently proved arithmetic theorem or a reduction of the number of certified source integers.
