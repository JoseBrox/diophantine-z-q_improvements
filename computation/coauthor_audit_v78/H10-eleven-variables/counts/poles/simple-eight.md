# Sharper one-pole construction and eight rational contacts

Use the elliptic charts, imports, separation determinant and fixed arithmetic assumptions of weak11.md. The new integral polynomials have 11 total coordinates. Let d be the number of finite contact positions, either six (the original Θ) or eight (below). Fix e even and K≥2. For each sufficiently large fixed odd B put a=(X²+B)^e+T^e and x=a−z, y=a+z. Define G,P,Q,J,D as in weak11.md with the chosen d contacts. The modified weight and the exact detector are

    F = P² + Q³
    u = J^[d(K−1)] P Q F² / D,    w = u/(1+u)²
    t_i = C_i/(1+u C_i)                 for the first four reciprocal abscissas
    t_i = C_i²/(1+u C_i²)               for the last two comparison tests
    W = ∏ (1 + (t_i/u)²), V = Tr(1/W), b = 4 w / V².

These formulas specify the degree-certified variant. For the first four tests the compiler writes C_i=R/L and forms t_i=R/(L+uR). For H,U take L=x_E and R=1. For the two differences take L to be the conjugated homogeneous difference-abscissa numerator and R the conjugated square of the difference of the two original abscissas. All four C_i are squares in the real quadratic field on an original rational chart: each point involved is a nonzero member of 2E(F), and doubling on y²=x³−Dx gives x(2Q)=(x(Q)²+D)²/(4y(Q)²). Thus their valuations are even at every good prime, including the difference points. Original chart guards supply the required nonzero L. More precisely the checker compares all original point coordinates and six tests with v28 up to renaming of nodal variables. It then directly reconstructs both difference numerators from the two point coordinates and constant generator.

## Primitive degree-six three-fiber map

Put

    B₆(u)=(u+4)(u+20)³(u−5)²,   C₆(u)=(u−4)(u−20)³(u+5)².
    B₆(u)−C₆(u)=108u⁵.

The eight rational positions before the change of coordinate are 0, ∞, ±4, ±5, ±20. Their images under t=1/(u−21) are

    Θ={0,−1/21,−1/17,−1/25,−1/16,−1/26,−1,−1/41}.

On a primitive pair s,t₀ the homogenized difference is 108s⁵t₀. The two degree-six forms have no common projective root; their gcd on primitive pairs divides a fixed integer by the resultant identities. The largest absolute value of the two forms is at least c max(|s|,|t₀|)^6, by continuity and homogeneity on the real unit square boundary, for some fixed c>0. The fixed weak-abc bound, applied after dividing by the bounded gcd and allowing signed triples, therefore gives

    log rad(N) ≥ (6/κ) h − O(1),

where N is the product of the eight primitive linear forms at the contact positions, including the factor for infinity. The coordinate change is unimodular over the integers, preserving primitivity and changing logarithmic height by O(1). It identifies the homogeneous contact forms up to sign, with the new infinity contact now finite. As log |N|≤8h+O(1), the complete product over primes with valuation exactly one has log ≥(12/κ−8)h−O(1), using 2rad-log minus log|N| as in weak11.md. The finite set S can be chosen once and for all. In general for d=6,8 the slope coefficient is γ=2(d−2)/κ−d.

## Simple-prime valuation of the new scalar

Among simple contact primes for the larger-height slot discard as before only other integral valuations at least K; the loss is at most (d/K) times the smaller height plus O(1). Outside S all retained simple primes give positive odd v(u). If the other slot is integral and its contact value is a unit, both F and all denominator factors are units, so v(u)=1+d(K−1)v(J). When both contact values have positive valuations m,n<K and one is one, the three denominator valuations remain min(3m,5n), m and n. The numerator F has valuation min(2m,3n), with no tie (if n=1 the equation 2m=3 is impossible, and m=1 gives 2=3n). Also J is a unit at these simultaneous contacts since 1 is separated from every θ. Thus

    v(u) = 2min(2m,3n) − min(3m,5n) = 1.

For m=1 these minima are 2 and 3. For n=1 and m≥2 they are 3 and 5. In the mixed case m=1, s=v(y)<0, one has n=d s and v(J)=s. Then v(F)=3d s and v(D)=(K+6)d s, giving v(u)=1 exactly. In the reversed mixed case v(P)=d s and n=1, the corresponding values are 2d s and (K+4)d s, also giving v(u)=1. The logarithmic radical bound and the proof of uniform soundness now hold with

    λ=(2(d−2)/κ−d−d/K)(e/κ−3)/2.

In particular r⁺(u)>1 for all rational well-defined scalar/point chart specializations with sufficiently large fixed B. This conclusion precedes all field balancing, the pole witness and the formal-group comparison. With eight contacts any fixed 1<κ<3/2 allows K then e to be chosen so that λ>1/2.

At odd ν=v_p(u), each t_i has valuation max(v(C_i),−ν) for the first four, and max(2v(C_i),−ν) for the last two. The first argument in each maximum is even (or infinite); hence the denominator valuations are strict and v(t_i)≠ν. If ν>0, the bound 0<v_p(b)≤ν+2 max v(W) forces v(t_i)>3ν/4 and then v(C_i)>0, as before. If ν<0 then v(t_i)≥−ν>0 and W≡1, so outside S we have v(b)=−ν>0. This covers all negative odd valuations, including new primes of the denominator D.

## Resultants and completeness

Repeat the fixed-n preparation in weak11.md, using 2d distinct rational coefficients ±(a−θ). Add the primes dividing the resultants in the variable z of F=P²+Q³ with each of D's three factors; take primitive integer multiples after a has been fixed, also including primes introduced by denominators and leading coefficients. All three resultants are nonzero. Indeed a simultaneous complex zero has either P=Q=0 or nonzero P,Q. In the latter case |P|²=|Q|³ and the additional relation is |P|³=|Q|⁵, |P|=|Q|^K, or |P|^K=|Q|. Each forces |P|=|Q|=1, since K is an integer ≥2. All θ have absolute value ≤1, so |G(t)|≤1 implies |t|≤2. This also holds at roots of G. Thus |x|,|y|≤2 in either case, inconsistent with x+y=2a>4. These exceptional primes depend on the fixed input n only in completeness. The set S in the height inequality remains independent of B,n.

At infinity both P,Q∼z^d and J∼−z². Since d is even, the numerator's leading coefficient is 1. Its degree is 2d(K−1)+2d+6d, compared to (5+2K)d for the denominator. Therefore u∼z^d at every fixed place and b z^d→1 uniformly on the prepared neighborhoods. The same local square, valuation and real requirements follow since d is even. At a fresh prime J is a unit and the nonvanishing contact slot is a unit; now ν=1. At the v22 successful conjugate the first four C_i have even valuation at least 2 and the last two C_i² have valuation at least 2. Thus every t_i/u vanishes modulo that place and v_p(b)=1.

For any remaining non-temporary p with nonintegral z, v(u)=d v(z) is even. With integral z and p not fresh, P,Q are units. If p divides D, neither J nor F can vanish there, by the specializations at J=0 and the three resultants. Then v(u)=−v(D)≤0. If D is a unit, the only possible positive contributions are the even exponents d(K−1)v(J)+2v(F). This proves square reduced denominator everywhere. The point/CRT/prime ordering, local square classes at 2,3,17 and native zero-pole density are those in weak11.md, with sixteen prescribed prime forms for d=8. Positivity of u on prepared specializations is ensured by z large and the leading-term computation.

## Guards, numerical bounds and verification

At an arbitrary rational character the sign of u can be negative. The six balancing norms in the compact certificate are nonzero for a different reason. The retained scalar guards protect u, x,y, the original elliptic charts and their six original tests before any balancing denominator needs to be inverted. For sufficiently large B the scalar lower bound above gives an unramified prime p with v_p(u)>0 odd. Consequently −u is not a square in F=Q(√2). For any square S∈F, including zero, 1+uS is therefore nonzero. This applies to all six denominators, since C_i is itself a square in the first four slots and the last two use C_i². It also shows L+uR≠0 in the homogeneous form, since L≠0. These arguments concern the rational character obtained after the algebraic separator argument. They use neither the pole obstruction nor integrality of X. Once the six denominators have been recovered, the real values of every factor 1+(t_i/u)² are ≥1, proving positivity of W₀ and Norm(W) as in weak11.md. For applications where shift-independent denominator guards are preferable, conservative.json instead keeps all six balancing norms as genuine scalar guards. Both versions coincide on the prepared integer fibers. The original scheme in weak11.md always used strictly positive 1+u²C⁴ and requires no nonsquare argument.

| d | κ | e | K | λ | Compact degree | Compact support | Conservative degree |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 121/100 | 10 | 15 | 40768/73205 | 82,954,625 | <2^249 | 143,305,089 |
| 6 | 16/15 | 6 | 6 | 21/32 | 25,069,953 | <2^232 | 43,616,641 |
| 8 | 121/100 | 6 | 6 | 8374/14641 | 33,344,385 | <2^236 | 57,863,041 |
| 8 | 16/15 | 4 | 5 | 99/160 | 19,861,377 | <2^228 | 34,647,937 |

The two eight-contact conservative support bounds are <2^244 and <2^236 respectively. All these degree/support bounds hold for any B. Coefficient bounds in the JSON files refer to the displayed fixture B=3, which is not certified to define the integers.

Run the following from the poles directory with Python 3.10+ and SymPy. All commands accept --repo for the pinned checkout.

    python -B build_weak11.py --simple
    python -B build_weak11.py --simple --strong
    python -B build_weak11.py --eight
    python -B build_weak11.py --eight --strong
    python -B check_weak11.py

The checker runs the upstream v30 degree/finite-algebra verifier, reconciles all original point coordinates and six comparisons, reconstructs both rational field slots of every denominator/t_i/product/pole on its integer DAG, verifies the guard partitions and the determinant bounds separately for compact and conservative versions. The determinant stays unexpanded.
