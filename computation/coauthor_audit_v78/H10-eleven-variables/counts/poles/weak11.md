# One native pole for the two weak-abc rows

The sharper degree bounds and eight-contact extension are in [simple-eight.md](simple-eight.md). The following six-contact construction gives a second proof with balancing denominators positive at every rational character.

The base source is JoseBrox/diophantine-z-q_improvements at commit d3a8c223716a0fc0dbf5af4eb7998d640c21048d. All counts below include the input. The theorem is conditional, with the same fixed-exponent rational abc, elliptic group, simultaneous prime theorem and native restricted-converse/descent inputs as the v22 direct-input 13-coordinate theorem. The one-point trace-height theorem supplies its original ineffective constant. No numerical sufficient input shift is known. The compact polynomial is specified by an integral determinant, without expanding its monomials.

| Exponent κ | Even exponent e | Band K | Total variables | Total degree at most | Support strictly less than |
|---|---:|---:|---:|---:|---:|
| 121/100 | 10 | 15 | 11 | 136,332,673 | 2^256 |
| 16/15 | 6 | 6 | 11 | 41,307,521 | 2^239 |

Fix an odd integer B at least three. For each row, the resulting family defines precisely the rational integers for every sufficiently large fixed B. The ten retained coordinates consist of X, three pairs for the points A,H,U, a slope z and the two native parameters τ,s for one pole. A single further rational coordinate Y encodes a character of a rank-128 finite algebra. The two comparison coordinates removed from v22 are the second pole's τ,s. No root or inequality witness is hidden in the new rational contact functions.

## Scalar and radical estimate

Use the v22 point charts over F=Q(√2) on E with 2E(F)=Z P₀ and T=Tr x(A). On a rational point chart A=[n]P₀ for n a nonzero integer and T>6. Put β=X²+B, a=β^e+T^e, x=a−z and y=a+z. All heights h are absolute logarithmic projective heights. Define

    Θ = {0, −1, −1/2, −1/3, −1/4, −2/5}
    G(t) = product of (t−θ) over Θ
    P = G(x),  Q = G(y),  J = (x−1)(y−1)
    D = (P³+Q⁵)(P+Q^K)(P^K+Q)
    u = J^(6K)(PQ)³ / D,   w = u/(1+u)².

Guard nonzero u and all denominators. For soundness fix S independent of n,B,z to contain the v22 exceptional set, the small primes dividing the denominators of Θ, their pairwise differences and 1−θ. Write r⁺(u) for the squarefree product of p outside S at which v_p(u) is positive odd.

For t=A₁/B₁ in reduced terms, away from the contacts, form the product N(t) of the six primitive integral linear forms associated to Θ at (A₁,B₁). The six-point proof in v22, Lemma 2 (label lem:contact), applies the quartic Belyi map t(t+2)³/(2t+1)³ after a fixed unimodular change of coordinates. Before removing high multiplicity primes it proves log rad N(t) ≥ (4/κ)h(t)−O(1), with omission of fixed primes costing O(1). Also log|N(t)| ≤ 6h(t)+O(1). Since 2−v_p(N)≤0 for all multiplicities at least two, the log product of simple primes of N(t) outside S is at least

    γ h(t) − O(1),     γ = 8/κ − 6.

These simple primes have v_p(G(t))=1. Choose the slot t with larger height among x,y. From its simple primes discard those at which the other slot is integral and the other G has valuation at least K. The lost log product is bounded by (6/K)h(other)+O(1), using its own primitive contact numerator product, with no dependence of the constants on a or B.

Every remaining simple prime is detected. First take both slots integral and let m=v(P), n'=v(Q). If the other valuation is zero all denominator factors are units and v(u)=3+6K v(J)>0 is odd. Otherwise m,n'≥1, one equals one and the other is less than K. Thus the three valuations of the denominator factors are min(3m,5n'), m and n'. The minima are strict, including that of 3m and 5n'. Substitution gives

    v(u) = 6K v(J) + 2(m+n') − min(3m,5n').

The last two terms sum to a positive odd integer. For m=1 the sum is 2n'−1. For n'=1 and m≥2 it is 2m−3. If instead v(P)=1 and s=v(y)<0, then v(Q)=6s and v(J)=s. The denominator valuation is 6(K+6)s, so v(u)=3−18s. When v(Q)=1 and s=v(x)<0, the denominator valuation is 6(K+4)s and v(u)=3−6s. Both are positive odd. No prime of the denominator of the moving scale a was excluded in this argument.

Consequently log r⁺(u)≥(γ−6/K)max(h(x),h(y))−O(1). Since 2a=x+y, h(a)≤2max(h(x),h(y))+O(1). Write E_h=h(1:β:T). The binary power lemma in v22 (label lem:powers) applies for every even e and gives h(a)≥(e/κ−3)E_h−O(1). Together these give

    log r⁺(u) ≥ λ E_h − O(1),    λ = (8/κ−6−6/K)(e/κ−3)/2.

The two values are 40768/73205 and 21/32. Their excess over 1/2 is 8331/146410 and 5/32 respectively. More generally every fixed 1<κ<4/3 admits K≥6 and an even e with λ>1/2 by choosing K first and e second. The numerical receipts concern the two tabulated choices.

## One pole and its soundness

Keep the six order-one v22 field tests. For f=1/x_E, ζ=−x_E/y_E, the conjugation σ of F and L=ζ(U)/ζ(H), they are

    f(H), f(U), σ f(H−P₀), σ f(U−A),
    L−σ[ζ(U−A)/ζ(H−P₀)], L−X.

For each test C set t=C⁴/(1+u²C⁴). Set W=∏(1+t²/u²) in F, V=Tr(1/W) and b=4w/V². This is exactly w Norm(W)²/W₀² for W=W₀+W₁√2. At every rational point-algebra character with original test denominators protected, each balancing denominator is strictly positive in both real slots, W≥1 in both slots and its norm and rational part W₀ are nonzero. Apply the native v28 pole at b, allowing zero final ordinate by v40's negative-odd obstruction.

At p outside S with ν=v_p(u) odd, use unramified valuations normalized by v(p)=1. The formula

    v(t) = 2 max(2v(C), −ν)

holds at every place over p, including C=0 with infinite valuation. For nonzero C, the two terms in the denominator have unequal valuations because ν is odd. Thus v(t/u) cannot be zero. The valuation of each factor of W is 2min(0,v(t)−ν)≤0. If ν>0, put q=max_{p'|p}v_{p'}(W)≤0. Then v_p(V)≥−q, v_p(w)=ν, and the obstruction to negative odd v_p(b) gives

    0 < v_p(b) = ν − 2v_p(V) ≤ ν + 2q.

At a place attaining q, each factor valuation is at least q>−ν/2. Therefore v(t)>3ν/4>0 and v(C)>0 for every original test at this same place. The formal-group calculation of v22 (proof of lem:local, starting with the first four tests) then gives X≡n mod p, including p-integrality. Briefly the two logarithmic quotients are u₀/h and (u₀−n)/(h−1) for H=[h]P₀, U=[u₀]P₀. At least one denominator is a unit. The tests and the uniform formal logarithm congruence identify both quotients modulo p with integral L, hence L≡n≡X.

If X≠n, r⁺(u) divides the nonzero reduced numerator of X−n. This gives log r⁺(u)≤h(X)+log(1+|n|) ≤ E_h/2+log(1+|n|), by the v22 positive input shift lemma. The fixed trace-height bound n²≤A₀ h(T)+J₀ and λ>1/2 now uniformly bound E_h, independently of B. Indeed (λ−1/2)E_h ≤ O(1)+log(1+√(A₀ E_h+J₀)). But E_h≥h(β)≥log B. For large enough fixed B this rules out every X≠n on a rational character.

## Completeness and every other prime

Fix a nonzero integer n=X and take A=[n]P₀. The numbers a>2 and Θ are fixed before applying the prime theorem. The twelve slope contacts ±(a−θ) are distinct. With H=[h]P₀ and U=[hn]P₀, choose compact real and fixed local neighborhoods on the multiplication curve avoiding all chart poles, using the sign-branch preparation in v22/v28 and v63. Non-identically-zero tests can also be bounded away from zero there. At n=±1, any identically zero tests are kept identically zero. These restrictions exclude only proper closed subsets on the multiplication curve; the fixed index progression and non-torsion approximation are the same as in v22/v28.

The temporary set for this n includes S, denominators of a and the contacts, primes of pairwise contact differences, and all primes of the nonzero rational numbers P,Q,D at both specializations (x,y)=(1,2a−1),(2a−1,1). Both P and Q, and all three summands defining the factors of D, are positive at those specializations. In particular a fresh contact cannot coincide with x=1 or y=1 outside this set. Take a denominator-clearing integer d>0, with d²(a−θ) integral for every θ and its primes in the temporary set.

As |z| tends to infinity with a fixed, the monic even-degree G gives P,Q∼z⁶ and J∼−z². The dominant terms in D have degrees 30,6K,6K, all with leading coefficient 1. Consequently u/z⁶→1 and w z⁶→1. For any nonzero C in the selected neighborhoods, t∼u⁻², and for identically zero tests t=0. Uniformly, W→1 and V→2, so b z⁶→1. At every temporary finite prime prescribe sufficiently large p-adic absolute value of z, giving a local square b of arbitrarily large positive even valuation. This includes the native conditions v₂(b)≥3, v₃(b)≥1, v₁₇(b)≥2 and local square classes there. At the real place require z sufficiently large and positive that 0<b<17. These requirements and all compact-neighborhood bounds can be chosen before selection of the fresh primes.

Apply the same finite rational coefficient version of the prime-pattern theorem used by v22/v63 to obtain z=N/(d²l²) for which the twelve N±d²l²(a−θ) are distinct large positive primes, with prescribed divisibility of l, avoidance, real lower bounds, and the conjugate reduction orders. Coprimality with the slope denominator is ensured by the prime-pattern construction. The v22 compatible CRT on h places H,U in the formal group at one of the two places over every fresh prime and H−P₀,U−A in it at the other, while preserving the fixed local/real neighborhoods. At the successful place every C has valuation at least one. At a fresh prime exactly one of P,Q has valuation one and the other is a unit, and J is a unit. Thus ν=3. At the successful place each t has valuation at least four, W≡1. At the other place each factor reciprocal is 1 or 0 mod p by strict parity. Hence V≡1 or 2 mod p and v_p(b)=3.

For clarity the remaining finite primes outside the temporary set divide into the following cases.

* If z is nonintegral, a and the fixed coefficients are integral. All leading terms at infinity dominate, giving v(u)=6v(z), even.
* If z is integral and p is not fresh, all twelve contact factors are units by the prime-pattern numerators. If J is a unit, v(u)=−v(D)≤0. If p divides J, then x≡1 or y≡1, where the two specialized values of D are units by construction of the temporary set. Hence v(u)=6K v(J) is even.
* At negative odd ν the identity for v(t) gives v(t)≥−2ν, so t/u has positive valuation at all places, W≡1, V≡2 and v(b)=−ν>0. At even ν, v(b) is even since b=u times a rational square. This includes ν=0 even when 1+u gains valuation.

Thus b has square reduced denominator, is in the native local square classes with the required valuations, and is in (0,17). Native restricted converse and its nonzero-witness/density result supply the pair τ,s. The entire point-algebra chart specialization from these multiples has real geometric characters as in v28. On each, a is the same scalar, the six original chart functions have protected denominators by the upstream preparation, and all additional balancing/product/trace denominators are positive. Each corresponding pole input is nonzero. The v28 norm-guard preparation at its finitely many conjugate parameters consequently applies to our single dense witness set as well. X=0 is included by multiplying the final polynomial by X.

## Integral determinant and guards

Use v28's three rank-four direct point algebras and the v30 square-extracted pole equation q²=R over their tensor product. The old polynomial and the new one use the same rational unscaling Z=S q for the pole ordinate. In soundness allow Z=0, so the square-multiplier S need not be a unit to reconstruct Z. For completeness the nonzero witness and the same v28 avoidance permit division on the prepared tuple. The v40 pole obstruction applies also at zero ordinate. Preserve the point chart guards, which guarantee nonzero values of every quadratic point-tower generator on all characters. Let G₀ be the product of the v30 scalar subalgebra norms of the atoms listed in compact.json as retained_norm_atoms.

Here is the exact removal rule. Start with all nonconstant multiplicative atoms of native inversion/guard numerators except for the isolated pole ordinate. Treat nonzero integer factors as units. In the first stage protect every denominator for u, C, 1+u²C⁴ and its field norm, together with the numerator of u. Remove any other guarded numerator atoms of the six field norms Norm(1+u²C⁴). In the second stage additionally protect all denominators of t, t²/u², both coordinates of W and its field norm, and remove any other guarded numerator atoms of W₀ and Norm(W). The checker verifies these inclusions and the two removed lists. On a recovered rational character positivity first recovers the first-stage atoms, then the second-stage atoms, with no circular use of unprotected denominators. The retained scalar guard imposes those atoms globally. On the prepared tuples the corresponding factors are units at every character.

For the seven quadratic tower generators take the positive envelopes M_i in polynomial.json (quadratic_tower). The first six t_i are point generators. The last generator is q. Set φ₇=q/(4M₇), φ_i=t_i(1+φ_{i+1})/(4M_i) for i descending from 6 to 1 and Ω=(∏4M_i)φ₁, a polynomial element in the integral free algebra. Each normalized value has magnitude ≤1/3. At the first distinct point sign the two disks centered at ±t_i/(4M_i) of relative radius 1/3 are disjoint. All common earlier maps are injective because t_i≠0. If only the pole sign differs it is already separated. Every φ₁ is nonzero. Thus Ω separates even with repeated or zero pole roots and every conjugate of a rational Ω-value is obtained at the same geometric character. The defining polynomial is

    X det(I − Y G₀ Mult(Ω)).

The scalar multiplier cannot specialize to zero on a zero of the determinant. The eigenvalues of multiplication on a finite algebra over an algebraic closure are precisely its character values, counted with multiplicities, including when a fiber is nonreduced. Rationality of Ω then implies rationality of the character by Galois invariance. Conversely a prepared rational character provides reciprocal Y. This supplies a single honest integral polynomial in eleven variables.

For algebra rank N and bounds g,w' on the degrees of G₀ and Mult(Ω), total degree is at most 1+N(1+g+w'). The support bound is the binomial difference for total degree d=N(1+g+w') before the factor X and Y-degree ≤N, namely binom(d+11,11)−binom(d−N+10,11). Here N=128. The two pairs (g,w') are (13366,1051732), (4278,318436). All degree/support bounds are uniform in B. The numerical log₂ coefficient one-norm bounds 503353600 and 158951296 refer only to the fixture B=3. At a different fixed B rerun with --shift B. No bound for an explicitly certified defining member follows while its sufficient shift is ineffective.

## Reproduction

Use Python 3.10+ with SymPy and the pinned repository. From this directory run the following commands. Each accepts an explicit --repo path when needed.

    python -B build_weak11.py
    python -B build_weak11.py --strong
    python -B check_weak11.py

The directories specification and strong contain the native rational graphs, upstream intermediate operator data in polynomial.json, and the defining compact determinant receipts. The intermediate v30 all-guard separator bounds are superseded by compact.json and the displayed determinant. This algebraic audit does not prove the external arithmetic inputs.
