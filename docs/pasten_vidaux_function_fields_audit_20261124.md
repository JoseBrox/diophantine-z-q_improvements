# Audit and quantitative continuations of Pasten--Vidaux (function fields)

**Source:** Hector Pasten and Xavier Vidaux, *Diophantine sets over global function fields*, arXiv:2611.31218v1, 23 November 2026, https://arxiv.org/html/2611.31218v1. Arithmetic precursor: their arXiv:2611.24748v1. The present note separates the source proofs, new deductions, and obstacles to characteristic-zero transfer. All citations to numbered lemmas in Sections 1--4 below refer to the function-field preprint.

The main new number-field results are in [the torsion-supported selector](../papers/number_fields/torsion_parameter_rationality_20261124/README.md) and [selective rationality transfer](../papers/number_fields/selective_rationality_transfer_20261124/README.md). A new quantitative function-field bound is proved in Section 3.3 below. The source does not establish H10 results for additional number fields, nor does it supply a direct smaller polynomial defining Z over Q. It should not be used as a replacement for the characteristic-zero prime-pattern, rank-stability, height, or elliptic index inputs of the project.

## 1. Statements and architecture

For k=F_q with q=3 mod 4, F=k(t), and a finite separable K/F with full constant field k, Theorems 1.1--1.3 establish the definability of k[t] in F, F in K, and the DPRM property of K. The proof factors into five substantially different inputs:

1. A Pheidas predicate containing polynomials and excluding negative odd valuations away from a fixed finite set.
2. Definability of positive-characteristic Frobenius and local valuation rings.
3. The Riemann--Hurwitz truncated-height inequality and a uniform function-field Chebotarev estimate.
4. Interpretation of degree arithmetic using multiplication on natural numbers defined from addition and the p-power divisibility relation, followed by DPRM.
5. Simultaneous 2-isogeny descent, with isotriviality giving finiteness of the relevant Tate--Shafarevich groups.

Only the first input's local half holds over all number fields without arithmetic hypotheses. The characteristic-zero analogues of truncated-height and global approximation already occur in the project's v81 and BB-v88 proofs. The Frobenius and degree-arithmetic inputs are genuinely characteristic-p. The introduction also reports independent work of Arno Fehm removing the congruence restriction on q for the polynomial-ring theorem; this is a report in the preprint, not a theorem audited here.

## 2. The elementary and global halves of the pole predicate

### 2.1. Lemma 2.1, including all valuation and zero cases

Write the two conics as nu^2=b+(1-b)mu^2 and nu'^2=b+(1-b)mu'^2. The last equation is y^2=(1-b)mu mu' with y!=0. This forces b!=1 and mu mu'!=0. Suppose v(b)<0 is odd in any discrete valuation. If v(mu)>0 then b is the uniquely smaller term in the first conic, of odd valuation. If v(mu)<0 then (1-b)mu^2 is uniquely smaller, again of odd valuation. Both are impossible for a square. Hence v(mu)=0, and similarly v(mu')=0. The last equation has odd valuation, a contradiction. This proof does not need unramifiedness, odd residue characteristic, or the global nature of the field. The case b=0 has no negative valuation and is harmless. One can even omit y!=0 for the local implication: when v(b) is negative odd, b!=1 and either zero mu would force b to be a square. Keeping the guard is useful for the source's global geometric construction.

The polynomial-ring completeness follows from Proposition 2.2: for a nonconstant polynomial b, choose epsilon in {0,1} to make the leading degree of t^epsilon b even and at least two. Subtract a constant and adjust its linear coefficient to make the t-adic valuation exactly one. These choices leave the leading term. Constants, including zero, are included separately. The only possible new finite exceptional valuations in the local obstruction are those of the fixed rational functions/constants used in the transformation. In fact outside places above t and infinity the subtraction by the affine polynomial cannot mask a negative valuation and multiplication by t^epsilon is a unit.

For comparison the BB-v88 product-pole lemma already gives a stronger compact coefficient presentation for the arithmetic sources. Each of the two conics in Theta has the base point (mu,nu)=(1,1). With r=(nu-1)/(mu-1), the other intersection has

    mu=1-2(r+b-1)/(r^2+b-1),
    nu=1+r(mu-1).

For b!=0,1 the line gives a birational chart away from its denominator and the vertical line at the base point. The missing finite points are handled by separate branches. A second independent slope parametrizes the second conic; the remaining square equation is monic after clearing its denominator. Thus Theta uses two free parameters and one finite root, just like the current BB normalized product equation. The two slopes cannot simply be identified: identical conic points give (1-b)mu^2, requiring 1-b to be a square. The conic parametrization is therefore not by itself a route to a one-parameter universal pole. The paper's global-solubility step does not prove that an arbitrary prescribed section of this surface has rational points.

### 2.2. Proposition 2.2 and Lemma 5.1 over global fields

Let L be any global field of characteristic different from 2. Use E_D:y^2=x^3-Dx and its rational 2-isogenous curve E'_D:y^2=x^3+4Dx. For the squareclass descent quartics C_d(D): N^2=dU^4-(D/d)V^4, write S(D) for their locally soluble squareclasses, S'(D)=S(-4D).

Assume D and -D nonsquare, |S(D)|=4, |S'(D)|=2, and finite 2-primary Tate--Shafarevich groups for both curves. Then every class in S(D) and S'(D) is represented globally. Proof: the two rational torsion classes give dimension at least one in each image; the second image is all of S'. The descent exact sequences identify the two deficits with kernels of the two dual isogenies on Sha. One kernel is zero, the other has order at most two. If T,T' are the two finite 2-primary Sha groups, the first isogeny injects T into T', and maps T[2] into that kernel of size at most two. By nondegeneracy and alternation of the Cassels--Tate pairing for the finite 2-primary groups of elliptic curves, T[2] has square order. Thus T[2]=0, T=0; now T' is the second kernel and has square order at most two, hence T'=0. This proves the criterion. The alternation argument here uses the canonical principal polarization of an elliptic curve with rational identity; no odd-degree generalization to arbitrary principally polarized abelian varieties is asserted.

Alternatively, in any global field the usual two-isogeny rank formula is

    rank E_D(L) = dim_F2 I(D) + dim_F2 I'(D) - 2,

where I,I' are the two rational Kummer images. Under the same Selmer sizes and nonsquare assumptions, the rank is at most one. **Positive rank suffices** for both Selmer images to be saturated, even without an a priori Sha-finiteness theorem. Conversely saturation gives rank one. This is an exact criterion, not a proof that the rank is positive over a number field. The two torsion classes ensure the formula includes the rational 2-torsion contribution; D and -D nonsquare imply the stated minimal torsion images.

For c=1-b, the source simultaneously imposes the criterion on D=b(b-1)lambda^2 and Dc^2. The target class b is different from both torsion classes when b and c are independent modulo squares (which follows from v_t(b)=1 and c nonsquare in the source). Thus its two quartic points have U,V both nonzero. Normalize V=1 and do the same on the other quartic. The exact substitutions

    nu=N/U^2, mu=lambda/U^2,
    nu'=N'/U'^2, mu'=c lambda/U'^2,
    y=c lambda/(UU')

satisfy the conics and product, including the nonzero guard. If c is a nonzero square the trivial conic choice suffices. If b=1 the input is outside the source's Proposition 2.2 hypothesis.

Over a function field these j=1728 curves become constant over a separable extension of degree dividing four (adjoin a fourth root of D; this also works in characteristic three). Finiteness of Sha in the isotrivial case is the arithmetic input cited in Ulmer's survey, *Elliptic curves over function fields* (2011), and is not deduced merely from local solubility. Over number fields constant j does NOT give that finiteness. The global-field formulation shows precisely what additional input would be needed to reuse this argument, namely the Selmer-size construction plus rank positivity or the indicated 2-primary finiteness, separately for the two twists.

### 2.3. Complete local table at odd residue characteristic

Use squareclasses in an odd-residue-characteristic nonarchimedean local field, with valuation uniformizer pi, D=pi^e u. Replacing D by a fourth-power multiple preserves the images. Let H be the full two-dimensional squareclass space and U the line of unit classes. The full table is:

    e=0 mod 4                     W=U,       W'=U
    e odd                         W=<[-D]>,  W'=<[D]>
    e=2 mod 4, -1 nonsquare,
          u square                W=H,       W'={1}
          u nonsquare             W={1},     W'=H
    e=2 mod 4, -1 square,
          u square                W=<[sqrt(D)]>, W'=W
          u nonsquare             W=U,           W'=U

In the square-D row sqrt(D) is a local square root, and its squareclass does not depend on the sign since -1 is a square. The paper explicitly qualifies its last two displayed rows by the nonsquareness of -1 in the residue field. This qualification is essential; q=3 mod 4 alone does not guarantee it at even-degree places. Our two extra rows complete the table.

Proof: at good reduction the isogenies have degree prime to the residue characteristic; the images are unramified classes and each has order two (the residue-field cokernel has order two, by the rational kernel and equality of point counts for isogenous elliptic curves over a finite field). For odd e, the two terms of x^2-D cannot have equal valuation, so a nonzero point gives class 1 when x^2 dominates and class -D when D dominates. The torsion class supplies -D; apply the same argument to -4D. For e=2 and -1 nonsquare, u square gives both the nonsquare unit class from (0,0) and the odd class from (sqrt(D),0); the product of the two local image orders is 4 by local 2-isogeny duality, forcing the other image trivial. If u is nonsquare, -4u is a square and the same reasoning exchanges the curves. Finally if -1 is square, -4=(1+i)^4 with i^2=-1; scaling x by (1+i)^2 identifies the curves and their squareclass images. The order-product identity gives order two for each. In the u-square case the torsion point (sqrt(D),0) supplies the odd class; in the nonsquare case the class -D supplies the nonsquare unit. This gives all rows including zero coordinates under the standard torsion-class convention.

Example: in F_3(t) at the degree-two place t^2+1, D=(t^2+1)^2, the local field has -1 square. Both images have order two, not four and one. This is not a counterexample to the actual qualified table or to the theorem: Section 5.4 uses the extreme rows only at infinity and the newly chosen odd-degree primes. At every other prime of even degree the cases e odd or e=0 mod 4 suffice.

### 2.4. Check of simultaneous Selmer surgery (Section 5.4)

The squareclass of b(b-1) has monic squarefree representative gamma since its leading coefficient is a square; its degree is even. The prime t belongs to its support and has odd valuation. The subspaces Omega=<[b],[c]> and Omega'=<[gamma]> lie in the initial Selmer spaces after the prescribed infinity adjustment. At primes dividing b or c to odd order the other factor is a local square, because b+c=1 and odd residue characteristic. Away from their support the classes are unit classes even when b or c has even positive valuation; at infinity the selected rows allow Omega and require gamma square. The class [-1] is absent from S_0 by the condition at t and from S'_0 by the condition at infinity. This guarantees consistency of prescribing its nontrivial character simultaneously with the prescribed basis-character values.

For completeness the prime choices can be justified by Chebotarev in the multiquadratic extension generated by the square roots of the relevant independent classes, including -1. A character with value -1 on -1 and the required values on the given basis exists because -1 lies outside its span. Its restriction to the constant field selects a compatible degree congruence; in particular odd degrees occur. The function-field Chebotarev estimate supplies arbitrarily many primes of the allowed large degrees. Equivalently use the quadratic reciprocity and Dirichlet result cited by the authors. Exclude all finite old supports and choose the primes distinct.

At an ell_i the first image is trivial and the second full; at an m_j the second trivial and the first full. Multiplying by the square of t^(r+s) times all these primes preserves the old infinity row because the unsquared multiplier has even degree. The local rows at the old support of gamma are unchanged. To check that no new Selmer directions enter, pair a candidate eta in S'(D) with each old delta_i. At all old primes the old images are orthogonal. At the new m_j the candidate is a square, and at all ell_h the old delta_i is a unit with Legendre symbol nontrivial only for h=i. Hilbert reciprocity forces v_{ell_i}(eta) even. Consequently eta belongs to S'_0 and the m_j conditions kill its unwanted coordinates. The symmetric argument for S(D) uses each old epsilon_j and shows even valuations at m_j, then the ell_i conditions kill its unwanted coordinates. This proves exact Selmer sizes, not just upper estimates obtained by ignoring potentially new ramified classes.

For multiplication by c^2, if v(c) is odd then v(D) is odd and the row depends only on the squareclass of D. Otherwise the multiplier is a local fourth power times a square unit, which preserves the e mod 4 and unit-square tests of every row. Thus both D and Dc^2 have the same local images. The t-adic odd valuation ensures D,-D,Dc^2,-Dc^2 are nonsquares. All hypotheses of Lemma 5.1 hold in the function-field setting. This part of the source proof survives the completed local table.

Number-field obstacle: primes above 2, real/complex places, ideal classes and ray-class constraints all require separate treatment. Principal multipliers with prescribed odd valuations and appropriate dyadic and archimedean squareclasses cannot be assumed to exist just by prescribing Legendre symbols. If -1 is globally a square, the full-versus-trivial mechanism at new odd primes is absent. Even if both Selmer sizes can be arranged, the finite 2-primary Sha premise must not be silently imported. Over Q the existing BB theorem supplies actual prepared rational pole witnesses; no advantage in free parameters has been proved from replacing it with conditional Selmer surgery.

## 3. Rational-function descent (Section 3)

### 3.1. Explicit synchronization in Lemma 3.1

The unsynchronized relation P(x,y): y=x^(p^j) is the cited theorem of Pheidas/Shlapentokh. Fix a place over infinity with v(t)<0; its valuation ring is Diophantine by the cited Demeyer--Van Geel theorem. The interpreted nonnegative valuation magnitudes carry existential addition and p-power divisibility: equality of values is unit ratio, addition is multiplication of representatives, and P provides the p-power relation by its effect on nonzero valuations. For positive values, conversely, take a representative and its p-power to witness the relation, using value equality. The p-power divisibility relation defines multiplication by the cited Pheidas 1987 theorem; hence equality of products of these magnitudes is Diophantine. Constants and zero magnitudes have their separate elementary cases.

The pair of P conditions with t_0 and t_0+zeta selects T=t^(q^s) with s>=s_0: comparing the two positive pole orders forces equal p-exponents, and then comparison of constants fixes zeta. To synchronize x,w when x!=0 and v(x)!=0, require P(x,w) and equality

    |v(w)| |v(t)| = |v(x)| |v(T)|.

The absolute values here are implemented by a finite sign disjunction and inversion. This forces the same p-power. If v(x)=0, instead require P(xt,wT) and equality of the corresponding products of magnitudes; v(xt)=v(t)!=0 so the same argument applies, then divide by T. For x=0 take w=0. This supplies the omitted synchronization detail without assuming either of the two target definability theorems. The relevant multiplication theorem concerns the interpreted natural numbers, not multiplication of variable exponents in characteristic zero.

For the non-p-power guard, separability makes t a p-basis: [K:K^p]=p and t is not a p-th power. The coefficient decomposition relative to 1,t,...,t^(p-1) gives an existential certificate that some coefficient with index >0 is nonzero.

### 3.2. Height upper bound and Frobenius congruences

For x not a p-th power the map x from the smooth projective curve of K to the projective line is separable. Over an algebraic closure of k, consider the d distinct roots of G. Riemann--Hurwitz bounds the total excess multiplicity of all points in those d fibers by 2g-2+2 deg(x), since the different exponent is at least e_P-1, including wild ramification. Counting distinct fiber points therefore gives N^(1)(G(x)) >= (d-2)h(x)-(2g-2)/[K:F], as in Lemma 3.2. The fixed-divisor parity inequality then gives the stated (d-4)h(x)<=q^s+c1: an odd-order zero outside the exceptional set must occur over a zero of t^(q^s)-t, and that polynomial has degree q^s. No error term depending on the exponent j in M is needed. This is the same parity/radical mechanism as v81 and the current rational abc routes, except that Riemann--Hurwitz makes it unconditional here.

At each unramified degree-s base prime away from all exceptional places, v(t^(q^s)-t)=1. If x has a pole of order a>0 there, the first fraction in (3.1) has valuation -2q^s a-1, forbidden. Once x is integral, the same odd-valuation obstruction forces x^(q^s)-x to vanish modulo that prime. These observations apply also if the numerator is zero, and are the only properties of the first pole test needed for descent.

The source's Lemma 3.3 follows by counting degree-s primes with conjugacy class of tau: the asymptotic count is (f|Cl(tau)|/|Gamma|)q^s/s with error O(q^(s/2)/s), and the number of primes above each with *that particular* Frobenius tau is |C_Gamma(tau)|/ord(tau). Their degrees over the original constant field k are s ord(tau). Multiplication gives the stated f q^s plus error. If one uses degrees over k_L instead, divide the entire formula by f; the subsequent height comparison must use the same convention. Only fixed extensions occur in this estimate.

### 3.3. New improvement: degree 2[K:F]+5 instead of 2[L:Fk_L]+5

**Theorem.** In the source's Lemmas 3.4--3.6 and Theorem 1.2, the fixed squarefree polynomial G can be chosen of any degree d>=2n+5, where n=[K:F], with a sufficiently large s_0 depending on the fixed extension. In particular the required degree no longer grows with the degree of the Galois closure. This proof uses the same Pheidas predicate and no new arithmetic hypothesis.

Proof. Put L equal to the Galois closure and let Gamma=Gal(L/F), H=Gal(L/Fk_L). For an accepted x outside F let r=[F(x):F]>=2, and let x_1,...,x_r be its distinct conjugates in L. Define the nonzero discriminant expression

    Delta=product_{i<j}(x_i-x_j)^2 in F^*.

Using the height on F normalized by the original constant field, each conjugate has the original absolute function-field height h(x). The ultrametric pole inequality gives h(x_i-x_j)<=2h(x), and the product inequality gives h_F(Delta)<=2r(r-1)h(x). This applies to any x, not only to integral primitive generators.

Discard a fixed finite set of rational-function primes, containing the ramified primes of L/F and the primes below all exceptional places in the predicate. At every remaining degree-s prime p of F the congruences in Section 3.2, applied to all primes of K above p and then to their conjugates, show that all x_i are integral and x_i^q^s is congruent to x_i at every prime of L above p. Choose such a prime, with arithmetic Frobenius tau. Then x_i is congruent to x_{tau(i)}. If the cycle lengths of the permutation tau on the r conjugates are l_j, every pair in the same cycle contributes at least one to the valuation of its difference. As L/F is unramified at p, the normalized base valuation of Delta is at least sum_j l_j(l_j-1), which is at least the number r-fix(tau) of moved conjugates.

Because K has full constant field k and is separable over F, so does every subextension F(x)/F. This extension is linearly disjoint from constant extensions (regularity); hence H acts transitively on its r embeddings, equivalently on the r conjugates. For any fixed coset of H in Gamma the average number of fixed conjugates is exactly one: for each i, the fraction of coset elements fixing i is 1/r by transitivity. The degree-s primes have Frobenius in the single coset acting on k_L as q^s-power. Applying the effective Chebotarev estimate to the bounded class function r-fix, and summing the degrees of these primes, gives

    sum_{deg p=s, p good} deg(p) (r-fix(Frob_p))
        >= (r-1) q^s - C q^(s/2),

where C is uniform for all the possible intermediate fields F(x), because the fixed finite group has only finitely many subgroups and hence possible conjugate actions. The same constant can absorb the fixed exceptional set. The zeros of Delta therefore have degree at least this large. Combining the two bounds yields

    2r h(x) >= q^s - C' q^(s/2).

But Lemma 3.5 gives h(x)<=(q^s+c1)/(d-4). For d-4>2n>=2r, these inequalities contradict each other for sufficiently large s, uniformly in x. This proves the claim.

For example, a degree-three nonnormal extension with geometric Galois group S_3 requires d>=11 by this theorem rather than d>=17. This is a proved improvement of the contact degree, not a numerical variable census of a Frobenius predicate (the source does not give such a census). The remaining quotient argument in Theorem 1.2 is valid: any nonzero element is a quotient of two nonzero polynomials; among 1,t,t+1 at most one lies in each of the two forbidden F^p-lines, since their pairwise ratios are not p-th powers. Multiplying both polynomials by the remaining choice produces two permitted non-p-power polynomials. Zero is added separately.

Further optional optimization for a fixed extension: use the exact coset average of sum_j l_j(l_j-1) rather than r-1. If A is its minimum over the finitely many constant-field cosets, then the same argument permits d-4>2r(r-1)/A for that intermediate field. Taking the maximum of this ratio over nontrivial intermediate fields yields a finite, computable group-theoretic degree threshold. Since A>=r-1>0, it is never worse than the uniform 2n bound. This refinement needs no effective computation of the Chebotarev constant to establish existence of s_0.

## 4. Polynomial-ring sieve and DPRM (Section 4)

The interpretation in Lemma 4.1 is sound using the unsynchronized Frobenius relation (so no circular dependence on F-definability). Addition, equality, constants and p-power divisibility of nonnegative valuation magnitudes are existential; the cited Pheidas theorem adds multiplication, and DPRM supplies every recursively enumerable integer relation. The condition on q^s1 and q^s that s is divisible by all integers up to q^s1+c1 is decidable, so the existential interpretation is applicable. The fixed c1 can be replaced by an integer upper bound if necessary.

The first pole test then bounds the degree of every finite pole of x by q^s1+c1 (using d-4>=1). The degree of each such pole divides s. The polynomial t^(q^s)-t has a simple zero there. The second test, after multiplication by x^2, would have odd negative valuation there, impossible except at the finitely many exceptional primes where integrality has already been imposed. Thus x is polynomial. Completeness for non-p-power polynomials uses divisibility of G(x) into an appropriate power of t^(q^s1)-t; the second expression is a polynomial automatically. Every nonconstant polynomial is a finite p-power of a polynomial not in F^p by perfectness of k. Constants are added separately. This completes the source proof modulo the cited external theorems; the implication to the DPRM property uses Demeyer's published result rather than a new constructive bound on existential variables.

**Characteristic-zero obstruction:** the functions t^(q^s)-t and their zero sets uniformly enumerate primes by degree, while Frobenius itself is already Diophantine. There is no corresponding characteristic-zero operation known here that simultaneously covers rational primes by size, is Diophantine with low coordinate cost, and has a controlled height. Chebotarev alone does not supply it, particularly not uniformly in a modulus depending on the unknown input. Interpreting the recursively enumerable integer relation by assuming Z already definable in Q and then using it to define Z would also be circular as a foundational replacement. The paper's function-field polynomial sieve thus cannot directly replace the contact arithmetic of the rational constructions.

## 5. Integration with current project routes

The useful characteristic-zero transfers are the following, proved in the companion notes rather than asserted in the source.

* Ordered two-stage rational approximation can use a torsion-supported local parameter on the stable-rank curve. At every newly introduced odd-valuation prime the same cyclic subgroup has the required formal depth; the second approximation no longer needs its own denominator point. This reduces the joint rationality selector from 7k+3 to 7k+2 coordinates and, with one monic absorption, the general N-coordinate polynomial transfer from 7N+2 to 7N+1.
* The universal local pole obstruction implies that only rationality of the arithmetic prefix needs to be enforced; over K a terminal pole witness may be nonrational. A selected separating primitive value rationalizes the entire finite arithmetic prefix in a single extra test. The new count for v110 is 21k+45, or 21k+39 when K contains no quadratic subfield. This retains the stable-rank and height assumptions over K and all source premises. The old independent tests for all original polynomial witnesses are unnecessary.
* Odd degree implies that every rational prime has an odd-ramification-index prime above it. Thus the local pole exclusions in any rational source of the indicated kind remain valid even at the ramified rational primes. This preserves a fixed numerical source parameter, though not the effectiveness of the rationality correction.

No new Z-over-Q count is claimed: the general family remains 25, the explicit source 27, ordinary/weak abc 11; their quartic frontiers remain 163/178/54 (with the separately recorded weak-abc quartics). The 25/27 transfers to odd-degree number fields give 152/154 total ambient-field coordinates respectively, versus 176/190 by generic composition; the 11 transfer gives 66, or 60 in the no-quadratic-subfield case. For v110 and an integral basis, the ring-of-integers bounds are 21d+45, or 21d+39 in that case. In quadratic degree the new counts for Z and O_K are 66 and 87. These are not claims of quartic degree, explicit numerical cutoffs, or definability for every number field without the retained inputs.

The current quartic over Q native pole equations have a rational conic, a bilinear product and a difference of squares, with two square registers. The preprint's two-conic variant uses the same two free geometric parameters after parametrization and does not supply a smaller quadratic compiler. In particular, setting one conic parameter or one elliptic squareclass to a convenient constant requires additional rational realization; no such assertion follows from the isogeny Selmer criterion. This is the obstruction in the 163/178 and 54 routes as well as the general and weak-abc few-variable routes. The remaining rational-coordinate research should focus on the actual normalized detector inputs, not a different prepared input chosen after the fact.

No new undecidability-variable count follows directly over Q: the source's DPRM argument is over characteristic p, and the v110 transfer used here changes the ambient field and rationality constraints, not the rational mixed-integer universal source.

## 6. Review status and next steps

The preprint's elementary and height steps have been checked, its synchronization argument expanded, its local table completed in the square-minus-one case, and its degree threshold improved. The two companion proofs give the characteristic-zero reductions. The cited global-field Chebotarev, Pheidas/Shlapentokh, Demeyer--Van Geel, Ulmer and Demeyer theorems are external inputs; this audit does not reprove those published theorems or the project's inherited positive-rank, class-seven and simultaneous prime-pattern inputs. The algebraic checks in the companion script verify the identities and counts, not the infinite approximation or height assertions.

Priorities: (i) seek a single rationality pole forcing both contact parity propagation and uniform conjugate congruences, (ii) establish the stable-rank hypothesis in more extensions or replace it by a weaker source of rational witnesses, (iii) investigate exact sections of the normalized product pole at the actual rational detectors and their quadratic encodings, (iv) if attempting the function-field Selmer surgery over number fields, explicitly solve the dyadic, archimedean and principal-ideal constraints and separately prove the needed global rational-point criterion. None of these open steps is represented as an established count.
