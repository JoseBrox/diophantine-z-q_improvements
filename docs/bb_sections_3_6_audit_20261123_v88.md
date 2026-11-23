# Bhargava–Burungale v2: audit of Sections 3–6

Date: 23 November 2026. Source: M. Bhargava and A. Burungale, *A Diophantine definition of Z in Q*, arXiv:2611.16130v2, 19 November 2026, https://arxiv.org/html/2611.16130v2.

## Findings and scope

No counterexample or fatal gap was found in Sections 3–6 at the level of the imported theorems and the explicitly checked geometric interfaces. The rank-one carrier, density, local congruences, Green–Tao construction, and interval soundness have been independently reconstructed. The vKK height theorem, its exponent-24 sharpening, its exact Galois compatibility requirement, Buzzard’s fine-level results, the relevant Elkies Atkin–Lehner construction, Pazuki’s height comparison, Green–Tao Theorem 1.2, and von Buhren Theorem 1.1 have been checked against primary texts.

This is not a claim to have re-proved the full recursive foundations of those external theorems. Theorem 2.3 and its Tian–Yuan–Zhang descent mechanism are a separate audit. The target paper remains a contemporary preprint, and its use is explicitly identified; this report does not turn that status into an assertion of settled consensus.

Clean improvements and a direct quadratic interface are proved in `bb_two_tests_three_squares.tex`:

1. The BB squaring relation needs **two** copies of its local predicate C rather than five, using the project’s earlier positive aggregate-trace method transferred to the BB carrier. Gaussian auxiliary triples fall from 30 to 12, and their points from 90 to 36. A further power amplification removes the fixed large elliptic multiplication: use the two shifts 0 and T^k, with T the trace of the original two abscissas and k a fixed sufficiently large power of two.
2. For the **same** quadratic presentation of the original interval set T, the final wrapper needs **r+18** rational auxiliary variables instead of r+19. A fixed 2-adic coset allows three rational squares in the interval condition.
3. The local predicate generalizes to **every fixed integral quadratic relation**, with two aggregate-height tests. Direct multiplication uses six Gaussian quadruples per test, hence 48 auxiliary U-points. This compares with 108 U-points for three calls to the improved squaring relation, or 270 in the original BB implementation. These are point-block counts, not final rational-variable counts.

Neither result evaluates r or produces a new numerical variable record for the project’s existing 25/27, 163/179 or abc 11/56 routes. In particular, neither result supplies a physical lift on the actual one-parameter detector fiber needed for 21/9. The aggregate-trace method is credited to existing project work, not advertised as a new general height principle.

## 1. Proposition 3.1: the height estimate

### Split sextic and ramification

The exact identity used in (3.2) is correct. With Y=(x+1)/2, the branch points of the genus-two curve are −2,−1,0,1,2,3. The map

    t = 27Y² / (4(Y²−1)³)

has the required local orders. On the double cover, its ramification degrees over 0,1,∞ are respectively 4,2,6. Above 0, the point Y=0 is branched in the double cover, while infinity is unbranched; above 1, Y=±2 are branched and the roots of 2Y²+1 are unbranched. Above infinity, Y=±1 are branched. The additional branch point Y=3 lies over an ordinary value of t. That extra branch point does not spoil the étaleness of the normalized pullback of a cover already unramified over that value.

The companion exact checker verifies the map identity, derivative, coprimality of numerator and denominator, and the transformed sextic. The local ramification reasoning is mathematical; the script does not construct the Shimura cover.

### Moduli and Galois-linear isogenies

Elkies’s original paper, printed p.10, describes the Atkin–Lehner action by quotienting a principally polarized abelian surface by the kernel of a two-sided quaternionic ideal. The quotient inherits the quaternionic action, and the quotient isogeny is linear for that action. This supports the exact compatibility asserted in BB Lemma 3.2. Merely knowing that the conjugates are isogenous would have been insufficient: vKK (7.1) requires compatibility with the chosen degree-two subfield of endomorphisms.

Buzzard §1 supplies the canonical principal polarization for a fixed positive involution. Theorem 2.1, Lemma 2.2 and Corollary 2.3 supply smoothness, properness and fine representability at V₁(5). Here 5 is prime to the quaternion discriminant 6 and is at least 4, so the smallness hypothesis is met. The additional symmetric-line-bundle and theta choices are made on a finite étale cover in characteristic zero. Keeping all components, as BB does, avoids silently choosing a geometrically connected component not defined over Q.

The normalized fiber product is étale over the genus-two curve by the local form of covers in characteristic zero: their branch indices agree. More generally, divisibility of the upstairs index by the Shimura index would suffice; equality is not logically necessary.

### Varying fields and uniformity

A rational x defines a quadratic point on the genus-two curve through Dₓ=sqf(G(x)). Pulling back the fixed étale cover gives a field Lₓ of bounded degree, unramified over Q(√Dₓ) outside a fixed set. Neither Lₓ nor its discriminant is fixed. What is fixed is its degree bound and the finite exceptional support. This is enough for vKK Theorem 7.1, because that theorem depends on the degree and on rad(N_S D_K), not on a fixed field chosen once for all x.

The statement immediately following vKK Theorem 7.1 does explicitly replace 24g by max(24,5g). Thus g=2 gives 24. There is no missing factor of two in this invocation. Even the displayed unsharpened exponent 48 would retain a qualitative definition after increasing the formal-log precision and the fixed exceptional primes, as BB remarks. It would change complexity and must not be silently substituted in a fixed circuit.

### Theta and coordinate heights

The theta-null map becomes an honest morphism after fixing the indicated data. Its nonconstancy on each geometric component follows from the finite ambiguity in the polarized surface and the countability of possible quaternionic actions: a constant map on a complex curve would have an uncountable fiber. Hence its pulled-back hyperplane class is ample. Pazuki Corollary 1.3(2) supplies a uniform linear upper bound for theta height in terms of 1+max(0,h_F), after absorbing its logarithmic correction.

The map t(x) has degree 6; therefore h(t(x))=6h(x)+O(1). The monic sextic has v_p(G(x))=6v_p(x) whenever v_p(x)<0. Negative valuations consequently have even parity, and all primes greater than 25 in Dₓ occur in the positive odd radical M(x). The final radical comparison is valid.

### Limits of transfer

This is a bound for the displayed sextic and projectively transported configurations, not an automatic theorem for every sextic or every five-contact detector. The project’s existing contact set has different coordinates. A replacement must supply the exact coordinate map, coefficient/resultant exceptional primes, and consumed valuations. The paper does not lower the exponent below 24. Its CM-only height bound cannot be applied to all varying surfaces in the family.

## 2. Lemma 4.1: carrier rank and torsion

The elementary identities are d²−d−3=0 and N(d)=−3. The displayed Q=(d+1,d+2) lies on the curve. The class-number argument uses the Minkowski bound √13/2<2; the units −1 and d+1 give independent sign patterns and hence generate the unit group modulo squares. The isogeny-descent images have the stated orders 8 and 1: on the second curve, positivity and local squareness at (d) leave at most the global classes 1 and 2, and 2 is excluded modulo the residue field F₃. This gives rank one by the standard two-isogeny rank formula.

At (1−d), the reduced curve has four points, all from its rational two-torsion. The formal kernel over Q₃ is torsion-free, so no additional torsion survives. Thus 2E(F) is torsion-free cyclic. Its Diophantine presentation by a doubled F-point is legitimate when all projective/identity charts are included.

The paper fixes a generator P₀ but does not give its coordinates or a saturation computation proving that its displayed Q is a generator. This does not invalidate its existence theorem. It does matter for a fully explicit polynomial specification: one cannot silently identify P₀ with 2Q merely from rank one. The new three-square argument needs only 2Q∈Γ, so it avoids this issue.

## 3. Lemma 4.2: real density and finite-place preparation

The isomorphism to the conjugate curve over F(√3) is valid. Conjugation of √3 changes one of the two real-torus points to its negative and fixes the other. Therefore an integral relation modulo torsion would force both coefficients to vanish. Kronecker’s theorem then gives density of simultaneous multiples in the product of the two identity circles.

The y-coordinate is surjective onto R on each identity component away from O; an invertible linear transformation gives density of the rational coefficient pair (a,b). No equidistribution statement beyond this density is needed. The same argument works for any nonzero multiple of the generator and any translate by a point of Γ. This strengthening is what permits the new fixed-coset construction.

Finite-place preparation follows from compactness of the local elliptic groups: a sufficiently large multiple lies in any prescribed collection of open formal neighborhoods. The real upper bound 0<u<1/3 is uniform for every nonzero doubled point, so the local choice does not compromise it. If real and finite restrictions must hold for the same point, a finite-index coset argument supplies them; no independent unrestricted weak approximation assertion is needed.

## 4. Lemma 5.2: local comparison and Frobenius witnesses

The correct formal logarithm is

    f(Z)=Σ_{r=0}^5 (−1)^r binom(2r,r)d^{2r}Z^{4r+1}/(4r+1).

The companion script independently differentiates this and matches the invariant differential through the retained order. The next degree is 25. For p>25 and v(z)≥1, the coefficient denominators give relative error at least p²⁴; m−1−v_p(m)≥24 for all omitted degrees. This is relative precision, and the proof correctly multiplies by integral Gaussian indices before using it.

The decisive noncircular step is γ₀+δ₀=1. One obtains γ₀B_j≡γ_j and δ₀C_j≡δ_j, and then B_j≡C_j implies B_j≡n_j. Thus the ratios are proved integral before squaring them. The proof does not assume one of the ratios integral at the outset, nor require a coprimality statement about the two reduction orders.

For p≡17 (mod 312), p splits completely in F(i), while −3 is a nonsquare modulo p. Hence the conjugate reductions are quadratic twists with opposite Frobenius. Ordinary j=1728 reduction has Gaussian endomorphism ring, and rational two-torsion makes π≡1 (mod 2Z[i]). The multipliers (1±π)/2 are therefore Gaussian integers. As P_j are doubles of F-points, they give the required reductions to O. The exact logarithmic ratios are n_j. Nonzero multipliers ensure the reference denominators do not vanish.

The identity cases for numerator points are allowed with z(O)=ρ(O)=0. Reference denominators remain explicitly guarded. The subgroup Γ+[i]Γ is torsion-free, so a nonidentity point cannot have x=0 or y=0. These chart and guard conventions must survive compilation.

## 5. Definition 5.3 and Lemma 5.4: one local predicate

For w=v(R) odd in an unramified local field, the two terms in R+X² have different valuation. Thus v(H_R(X))=max(0,w−2v(X)). This exact identity works even when X is not initially integral. A failed local condition makes one factor divisible by p^w and hence makes W_k divisible by p^w. If all six triples failed at all places, the norm product would be 1 modulo p^w and w₀ would be divisible by p^w. The resulting c would have valuation −w, contradicting the square-denominator implication.

This reasoning extracts all tests from one successful triple at one place; it does not combine tests from different places. The six triples are independent across the six selected primes. Replacing them by one common triple would require a new simultaneous realization result. The Gaussian congruences at different reduction primes need not be compatible merely because the primes are different.

The norm is taken over the fixed degree-four field F(i), not a variable splitting field. Consequently the rational arithmetic encoding is finite and uniform. All rational-function denominators are guarded in the source.

The construction extends to a fixed polynomial F(n₁,…,n_s): use j=0,…,s, impose B_j=C_j for j=1,…,s, and use the last test F(B₁,…,B_s)=0 modulo p²⁴. The exact same integrality argument validates evaluation of any integral polynomial. Each local tuple has 3(s+1) inverse factors. For a quadratic F, |F(n)|≤C_F(1+Σn_j²), so the aggregate trace with the additional fixed point P₀ and a fixed power gives a two-test global definition. This provides a direct multiplication relation, rather than constructing multiplication through three separate squaring calls.

## 6. Lemmas 5.5–5.6: forcing equality and supplying witnesses

The five-test argument is valid. Passing to fixed large multiples amplifies canonical heights while leaving Δ in the local predicate unchanged. Bounds on both s and s+β bound each β. The implied constants can be chosen independently of the multiplier, because the coordinate-height comparison uses the fixed field basis. When Δ≠0, the integer quantity n₁²+n₂² is at least 1, so fixed additive errors can be absorbed legitimately.

Our transfer of the aggregate-trace theorem replaces the four scalar coordinate shifts by one rational aggregate trace T_m. It gives m²(n₁²+n₂²)≤A h(T_m)+J, with constants independent of m. Two tests at s and s+T_m then force equality. The proof checks independence of the two normalized conjugate generators, noncancellation on every abelian translate through the relevant finite-rank tuple, the projective graph boundary, the surjectivity hypothesis of von Buhren’s theorem, and the zero-index strata. It does not use an unproved assertion that a rational function globally controls heights on the entire ambient abelian variety.

There is a stronger implementation option. For the trace T of the original points, nonzero doubled-point strata give T>√13>3 and hence h(T)≥log3. Absorb J into A*=A+J/log3, obtaining n₁²+n₂²≤A* h(T). Two tests at s and s+T^k now imply k h(T)≤2H|Δ|+log2. Any fixed k>A*(2H+log2) forces equality. Thus the two large elliptic multiplication maps can be removed entirely. In an unrestricted-degree presentation T^k adds no retained parameter; for k=2^j a quadratic presentation uses j repeated squarings. Neither k nor j is numerically evaluated here.

The Green–Tao application is sound. Given all rational offsets β−θ, choose D clearing their denominators and choose integer positions r=m+D(β−θ)>2D. A sufficiently long progression in the positive-density congruence class supplies p=q₀+rv. Then T=Dv and T(s+β−θ)=p. Since p>D and p>v, p is coprime to T. This is the precise check preventing denominator cancellation. Distinct roots give distinct positions at a fixed shift; repetitions across different shifts cause no difficulty because their local witnesses are independent. A progression can be arbitrarily long even when the length depends on the chosen inputs; the existential formula never encodes primality or that length.

At each shift R=14∏p_i/T⁶ is positive and greater than 2. Its odd valuations occur only at 2,7 and the six selected primes. At 2 and 7, D divisible by 14 gives negative odd depth at most −5; the formula for c converts this into positive depth, with v₂(c)≥6. At the six chosen primes, the norm argument gives w₀≡1 and v_p(c)=1. All other valuations of c are even. The squareclass is 7 times a product of six primes congruent to 1 modulo 8. Thus all hypotheses of Lemma 2.2 are matched. The existence of one split prime of odd R-valuation also proves R+X²≠0 for every X in F(i).

## 7. Theorem A: the interval argument and its new saving

The set T is decidable on the nonzero indices: coordinates, numerator sizes, rational inequalities, and integer existence in a rational interval can be computed exactly. DPRM followed by the Diophantine arithmetic model therefore provides a definition. The use of DPRM occurs on represented integer indices; it does not assume that Z has already been defined as a subset of Q.

The rescaling to Lemma 2.2 is algebraically correct. A prime of positive odd valuation in g=G(16q+8) forces a positive odd valuation of c=u²/g and therefore divides Num(u). This gives the stated denominator bound for q. The strict interval-length inequality then excludes every distinct integer in that interval, including endpoint cases.

For integer q, 16q+8 has absolute value at least 8 and is divisible by 8, so g>0 and g≡7 modulo 8. Choosing u sufficiently small at the finite primes dividing g makes c have a square denominator and the required 2-adic properties. Real density supplies the interval after u is fixed.

The new improvement is entirely at the last step. Exact doubling gives

    y(2Q)=−205/108−(191/216)√13.

Its coefficient valuations are −2 and −3. They persist on a fixed finite-index coset in Γ, whose real image remains dense. On that coset, for **every integer q**, the interval product (q−a)(b−q) has valuation −5 at 2. Once positive, it is a sum of three rational squares by the three-square theorem. One chooses the interval point on this coset for completeness, but the coset is not imposed in the defining formula and no new witness is added. The old T is unchanged. Soundness is immediate because a sum of squares is nonnegative.

## 8. Variable accounting and implications

The original Remark 6.1 counts r+19 auxiliary variables besides the input. Our interval change saves one and gives r+18. The number r includes the actual quadratic presentation of T, and is not evaluated by the paper or this audit. A statement such as “an 18-variable definition” would be false.

Likewise, five→two is a count of local predicate blocks, not an asserted final total-coordinate count. Applying the finite-algebra compiler requires tracking the rational coordinates for Gaussian subgroup membership, point arithmetic, all denominators, and the DPRM relation. The two improvements can be used together, but their savings cannot simply be added to the existing project’s unrelated 163-variable quartic.

The choice of carrier in the BB proof differs from the project’s Q(√2) carrier. Its simpler Frobenius construction removes a reduction-order coprimality demand in that proof, but uses Gaussian auxiliary points in a degree-four field. The tradeoff requires a new circuit inventory; it is not automatically a smaller replacement.

The existence of a Diophantine model and DPRM yield the stated r.e.-set and quartic undecidability consequences. The elementary-extension argument in Corollary 1.2(4) uses the decidability of rational-root absence for fixed-degree monic rational polynomials, transfers the resulting first-order equivalence, and preserves its existential side under inclusions. This reasoning is valid. None of these consequences resolves the separate global realization condition for the project’s reduced pole family.

## 9. References checked

| Primary source | Location and check |
|---|---|
| Bhargava–Burungale v2 | https://arxiv.org/html/2611.16130v2, all of §§3–6 read. |
| von Känel–Kret | https://ar5iv.labs.arxiv.org/html/2307.06944, Theorem 7.1, its following sharpening, and definition (7.1). The original arXiv PDF and one institutional mirror were unavailable via the fetch route; the rendered full original text was available. |
| Elkies | https://arxiv.org/pdf/math/0005160, printed p.10 for the two-sided ideal quotient and §3.1 for signature (2,4,6) and the rational quotient. Author-listed corrections checked at https://people.math.harvard.edu/~elkies/papers/shimcorr1.html. |
| Buzzard | https://www.ma.imperial.ac.uk/~buzzard/maths/research/papers/shimura.pdf, §1 and Theorem 2.1, Lemma 2.2, Corollary 2.3. |
| Pazuki | https://www.numdam.org/item/10.24033/bsmf.2623.pdf, Corollary 1.3 and the theta-height discussion. |
| Green–Tao | https://annals.math.princeton.edu/wp-content/uploads/annals-v167-n2-p03.pdf, Theorem 1.2, printed p.482. |
| von Buhren | https://www.numdam.org/article/JTNB_2017__29_1_307_0.pdf, Theorem 1.1 and condition (1.1), printed p.308. |
| Three-square theorem | https://www.pollack-math.net/4squares-arxiv.pdf, Goldmakher–Pollack’s explicit statement of Legendre–Gauss; the rational consequence is proved here by clearing a square denominator. |
| Prior project method | `papers/trace_heights/weighted_trace_20261114_v27.tex` and `trace_on_all_points_20261113_v25.tex`, read directly from the current project checkout. |

## 10. Reproducibility and next work

Run `python research/height/check_bb_improvements.py`. The emitted `certificate.json` certifies only its finite exact identities: the seed point, duplicate, universal parity identity, rational map, formal series truncation, and fifteen sample primes in the specified class. The abstract height and density assertions are proved in the manuscript using their named external suppliers.

Next useful tasks are to compile the two-test arithmetic model, compare the exact new field and group interfaces with the existing 25/163 routes, and continue the actual-fiber rational-point/lift analysis for 21/9. No positive count should be changed before those interfaces and the compiled counts are established.
