# Eleven coordinates under fixed weak rational abc

The coefficient specification in this directory gives a single polynomial in 11 rational coordinates, including its input. For every sufficiently large fixed odd integer coefficient shift, its rational input projection is the integers. The threshold is ineffective. This uses weak rational abc at exponent 121/100 and the same elliptic, trace, simultaneous prime and intrinsic pole inputs as Brox's v63. A smaller-degree second specialization uses weak abc at 16/15. Upstream previously used 13 coordinates for both fixed-exponent rows. The result trades degree for two coordinates.

| Weak exponent κ | d | m | cutoff K | degree upper bound | support upper bound |
|---|---:|---:|---:|---:|---:|
| 121/100 | 6 | 8 | 21 | 25,230,309,249 | <2³³¹ |
| 16/15 | 4 | 5 | 8 | 5,638,364,545 | <2³¹⁰ |

Both bounds are for the 11-variable determinant circuit. The supplied B=3 coefficient fixtures are for algebra verification. The prior 13-coordinate families have smaller defining-degree upper bounds.

## Construction

Use the three square-abscissa point charts of the pinned derivative11_v63 source, its six physical tests C_i and every point and difference guard. In particular A=[n]P with n a nonzero integer and T=Tr x(A). For B odd, B≥3, take β=X²+B, M=βᵈ+Tᵈ, a=Mᵐ, x=a−z, y=a+z. Put

    G(t) = t(t+15)(t+20)(t+24)(t+30)(t+60),
    g = G(x),  h = G(y),  L = g+h,  F = gh,
    N = L³ + g²h²,  D = L² + g²h,
    Q = ND(gᴷ+h)(g+hᴷ),  u = F⁵(1+QF)²/Q.

Guard M,F,Q,u,1+u. Use w=u/(1+u)² and the v63 equations

    D_i = C_i²/(1+u C_i²), W = ∏(1+D_i²/u), V = Tr(W⁻¹),
    b = 4w/V², η = 7b,
    Y² = η(η+v²)²s⁴ − η(η−v²)²(1−η)².

Retain each v63 division and norm guard, permitting zero terminal ordinate Y. The coordinates are X, six point coordinates, z, v, s and the single finite-algebra encoder. The three point blocks and terminal ordinate give rank 128.

## Collision valuation

At any prime, suppose one of g,h has valuation one and the other has valuation j with 0≤j<K. Then u has positive odd valuation, provided u is defined and nonzero. If j=0, Q is a unit and v(u)=5. If 2≤j<K, the valuation of L is one. N and D have valuations 3 and 2. The last two factors in Q have valuations 1 and j in either order. Thus v(u)=4j−1. If j=1, the last two factors both have valuation one. For v(L)=1 the pair of valuations (v(N),v(D)) equals (3,2). For v(L)≥2, including L=0, it equals (4,3). These pairs yield v(u)=3 and 1 respectively. In all these cases 1+QF is a unit. The strict inequalities of monomial valuations in N,D also prove the assertion at the prime two.

## Fixed-exponent height estimate

Write h for absolute logarithmic rational height. Enlarge the project's fixed exceptional set by the primes dividing the shift differences or 60. All of these already lie below its cutoff. Under weak abc, for any rational t at which G(t)≠0, let S₁(t) be the product outside that fixed set of primes with v_p(G(t))=1. Then

    log S₁(t) ≥ γ h(t)−O(1),         γ=8/κ−6.

Indeed the six roots are 60 times the six v22 rational Belyi contacts. At a primitive numerator/denominator pair of t, the cleared sextic numerator J has |J|≤O(exp(6h(t))). The explicit Belyi triple from v22 section 2 gives log rad(J)≥(4/κ)h(t)−O(1). The change t↦t/60 affects height by at most log 60 and its bad primes lie in the fixed set. For integral J the product of primes dividing J exactly once is ≥rad(J)²/|J|. This gives the asserted simple, rather than merely odd, support. G is monic, so its cleared numerator is coprime to the slope denominator.

Write H=max(h(x),h(y)), and start with the simple support for whichever argument attains H. Discard primes dividing the denominator of M at total logarithmic cost ≤h(M). The first argument is integral at each remaining prime from this support. The identity x+y=2a makes the second integral too. Discard primes where the second G value has valuation at least K. Their product has logarithm ≤6H/K+O(1) by the same cleared-numerator size bound. The collision lemma applies to everything retained. Consequently the product R(u) of primes outside the fixed set with positive odd valuation on u satisfies

    log R(u) ≥ (γ−6/K)H−h(M)−O(1).
    H ≥ (m/2)h(M)−O(1),

where the second inequality follows from x+y=2Mᵐ and h(x+y)≤h(x)+h(y)+log 2. All constants are independent of B. Set λ=(m/2)(γ−6/K)−1 and α=d/κ−3. Then log R(u)≥λ h(M)−O(1). The v22 binary-power height lemma gives α E≤h(M)+O(1) for E=h(1:β:T). The two exact comparisons are

| κ | γ | α | λ | λ−1/(2α) |
|---|---:|---:|---:|---:|
| 121/100 | 74/121 | 237/121 | 257/847 | 19331/401478 |
| 16/15 | 3/2 | 3/4 | 7/8 | 5/24 |

More generally, every fixed weak abc exponent 1≤κ<4/3 suffices for this 11-coordinate construction. Choose any even d>3κ, any integer K>max(2,6/γ), then m sufficiently large that λ>1/(2α). These choices retain the same source and proof. The displayed degree bounds concern the two specific rows.

## Soundness

The v63 extraction lemma depends only on the valuation of u and the displayed balanced elliptic tests. It gives R(u) dividing |num(X−n)| whenever X differs from the root index n. In detail, at positive odd ν=v_p(u), write q≤0 for the largest valuation of W across the places above p. Negative odd valuations of b are excluded by the intrinsic pole. As v_p(b)≤ν+2q is odd, ν+2q≥1. At a place attaining q, every factor in W has valuation greater than −ν/2. This forces each D_i to have strictly positive valuation, hence each original C_i as well. The v63 formal comparison gives X≡n modulo p with X integral at p.

For X≠n, the numerator bound gives log R(u)≤h(X)+log(1+|n|)≤E/2+log(1+|n|). Therefore

    (λ−1/(2α))h(M) ≤ log(1+|n|)+O(1).

The inherited trace bound n²≤A₀h(T)+J₀≤A₀E+J₀ and E≤h(M)/α+O(1) bound h(M), uniformly in B. But E≥h(β)≥log B. This contradicts any sufficiently large shift. Thus all rational solutions with X≠0 have integer input.

## Completeness

For each nonzero integer n, set X=n,A=[n]P and U=[n]H as in v63. The height scale is now a fixed positive rational. The twelve coefficients ±(a+c), c∈{0,15,20,24,30,60}, are all distinct. At every real point-algebra character the scale is positive, as β>0 and d is even. For sufficiently large real z, both g and h are positive because G is monic of even degree. Consequently N,D,Q,u,1+u and every new denominator are positive. At every fixed place, as z tends to infinity,

    g,h ∼ z⁶, F ∼ z¹², N ∼ z²⁴, D ∼ z¹⁸, Q ∼ z^(42+12K),
    u ∼ F⁷ Q ∼ z^(126+12K),        w ∼ z^(−126−12K).

The leading coefficient is one. Prepare the fixed neighborhoods of H exactly as in v63, avoiding the zeros of the nonidentically zero tests. Make z sufficiently large there. Each nonzero test gives D_i∼1/u, and identically zero tests give D_i=0. Thus W→1 and V→2. At the real place we obtain 0<7b<1. At two, w is a local square of arbitrarily large even positive valuation, so b is a local square and v₂(b)≥4. At seven ensure v₇(b)≥0. At the other finitely many temporary exceptional places make v_p(b) nonnegative by the same limiting argument. Include all primes dividing the numerator or denominator of the fixed scale.

By the identical v63 simultaneous-prime argument applied to twelve distinct rational positions, choose L₀,N₀ and a common positive integer R with R²(a+c) integral such that

    z=N₀/(R²L₀²),      p_c^±=N₀±R²(a+c)L₀²,

are the prescribed twelve distinct admissible primes, as large as required with all fixed-place and real constraints. In particular at each p_c^± just one linear factor of F has valuation one, all others are units. Therefore v(u)=5 at each such prime. The synchronized v63 elliptic refinement makes the first four tests have valuation ≥2 and the last two ≥4 at the successful embedding. Hence there W≡1. At the other embedding all factors of W have valuation either zero with residue one or strictly negative, by oddness of 5 and the even valuation of D_i². The other inverse W is therefore 0 or 1 modulo p. As a result V is a unit and v_p(b)=5.

For any unselected p outside the temporary preparations at which z is integral, g and h are integral and the twelve-prime factorization makes F a unit. If v_p(Q)>0, then 1+QF is a unit and v_p(u)=−v_p(Q)<0. If Q is a unit, then v_p(u) is even. At an unselected prime with v_p(z)<0, the scale and all coefficients are integral, and the leading terms just displayed have coefficient one, so v_p(u)=(126+12K)v_p(z) is even. For every negative odd valuation of u, the v63 balanced tests give W≡1 in every slot, V≡2, and v_p(b)=−v_p(u)>0. Every even valuation of u gives even valuation of b since 4, the normalizer denominator and V² are squares. All cases thus make the reduced denominator of b a square. The preparation at seven also makes the reduced denominator of η=7b a square.

The inherited intrinsic-pole theorem now applies with 0<η<1, η∈7Q₂² and v₂(η)≥4. It supplies rational v,s,Y on the given pole surface, with dense choices for avoiding any retained whole-character square-extraction conditions. At each point character η≠0 by real positivity, so the cleared terminal radicand is a nonzero polynomial in v,s. The v63 terminal-root encoder allows zero terminal ordinate and retains every preceding guard. The usual factor X includes the integer zero. This completes both directions.

## Lower degree by normalizing at poles of the scale

The `weak-compact` and `strong-compact` specifications use the same coordinates, tests and shifts. For these two replace u throughout by

    u* = u/(1+M^e F)²,         e=3m(K+11),

and guard the new denominator. The old positive integral collision calculation stays exact whenever v_p(M)≥0, because F then has positive valuation at every target contact from that lemma. If a simple target contact occurs with v_p(M)=−t<0 outside the fixed set, the opposite argument has valuation −mt. Thus the two values g,h have valuations 1 and −b₀ with b₀=6mt, in either order. In this situation v(L)=−b₀, v(N)=−3b₀ and v(D)=−2b₀; in the last comparison the other term has valuation either 2−b₀ or 1−2b₀. The remaining two factors of Q have valuations −Kb₀ and −b₀. Hence v(Q)=−(K+6)b₀, v(F)=1−b₀ and v(1+QF)=v(QF)<0. The raw valuation is 7−(K+13)b₀, while v(1+M^e F)=1−b₀−et. This gives v(u*)=5 exactly. Therefore no primes dividing the denominator of M need to be discarded. When bounding the opposite G numerator's K-fold factors it is enough to work among the other primes, where both arguments are integral.

The height lower coefficient is now λ=(m/2)(γ−6/K), and the remainder of soundness is unchanged. For completeness add the scale primes to the temporary fixed set as before. At the selected primes M is a unit and F has valuation one, so 1+M^e F is a unit. At every unselected integral place outside the temporary set, the new denominator is integral. Division by its square preserves even valuation, and can only make a negative odd valuation more negative. At fixed and real infinity the new asymptotic is

    u* ∼ M^(−2e) z^(102+12K).

The leading coefficient is a positive rational square. At unselected nonintegral slopes outside the temporary set M is a unit, so the valuation stays even. At the prepared real characters M and F are positive for all sufficiently large z, which also guards 1+M^e F. Thus all extraction, intrinsic-pole and terminal-encoder arguments still apply.

| κ | d | m | K | λ−1/(2α) | degree upper bound | support upper bound |
|---|---:|---:|---:|---:|---:|---:|
| 121/100 | 8 | 1 | 18 | 107/158631 | 3,762,160,001 | <2³⁰⁴ |
| 16/15 | 6 | 1 | 6 | 5/84 | 1,472,544,129 | <2²⁹⁰ |

## Coefficient specification and reproduction

Run `python build.py --repo /path/to/diophantine-z-q_improvements --flavor weak` and similarly for `strong`, `weak-compact` and `strong-compact`. Run `python verify.py --repo /path/to/diophantine-z-q_improvements` for independent guard, coefficient and circuit checks on all four fixtures. The pinned source commit is d3a8c223716a0fc0dbf5af4eb7998d640c21048d. The generator uses the unmodified v63 point arithmetic, v30 subalgebra norms and v40 terminal-root compiler and replaces only the scalar contact circuit and its guards. `polynomial.json` is the finite determinant specification, indexed to `source.json`. In each flavor the fixed integer B can be changed with `--shift`.

Upstream mathematical references in the pinned repository are `papers/conditional_few_variables/direct_input13_20261110_v22.tex` (weak Belyi and binary powers) and `papers/conditional_few_variables/derivative_detector11_20261117_v63.tex` (elliptic and intrinsic machinery, finite encoder and prime preparation). Finite algebra and valuation checks do not certify an effective shift.
