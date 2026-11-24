# Gaussian-module stability in place of ordinary rank stability

## Theorem

Let F=Q(sqrt(2)), E/F:y^2=x^3-(3-sqrt(2))^2 x be the original carrier, and let K contain i=sqrt(-1) and be linearly disjoint from F. Suppose

    rank_Z E(KF)=2.

Retain the original non-pole elliptic formal-comparison and compatible rational prime-pattern/recurrence premises of v110, and the published BB prepared-pole theorem. Assume ordinary abc over K. For each k>=1 there is a single polynomial over K in **3k+8 total K-coordinates**, including k inputs, with input projection S_k satisfying

    Z^k subset S_k subset Z[i]^k.

The construction is unrestricted-degree; the sufficient fixed coefficient is ineffective. It is NOT asserted that every Gaussian-integer tuple is accepted.

Consequently the ring of integers of K has a polynomial definition over O_K in **3[K:Q]+8** total K-coordinates. For **K=Q(i)** the rank hypothesis is an unconditional fact by the [exact rank certificate](../carrier_twist_parity_20261124/README.md), so **14 variables** suffice for O_K under ordinary abc over K and the other retained arithmetic premises. This supersedes the 69-variable transfer for this particular quadratic field without assuming the impossible ordinary rank-stability hypothesis.

If in addition some elliptic curve over Q has stable positive rank over K, then the torsion-supported rationality selector gives **9k+9** coordinates for Z^k in K^k, in particular **18** for Z in K. For K=Q(i) the some-curve-over-Q hypothesis is supplied by the cited Zywina quadratic-field theorem already used in v81. The count 18 does not require Gaussian-integer completeness of S_k.

## 1. The Gaussian module and rational generator

The explicit endomorphism [i](x,y)=(-x,iy) is defined over KF and its action on the local parameter zeta=-x/y is multiplication by i. The finitely generated free part of E(KF) is a module over Z[i]. Because Z[i] is a PID and the Z-rank is 2, killing torsion by a fixed integer M>0 makes G=M E(KF) a free Z[i]-module of rank one. Let R generate it. Take the fixed original nontorsion point P in E(F), and set P_*=[M]P. This is a nonzero element of G, so P_*=[a]R for some fixed a in Z[i] minus zero. The image of the algebraic map [a] composed with [M] on E(KF) is exactly Z[i]P_*. In particular the generator P_* is a rational-over-F point, not an uncontrolled Gaussian multiple of the old generator.

Use k+2 arbitrary affine preimages under that fixed map for A_i,H,U. Every image has a unique Gaussian index, say m_i,h,j. Exclude identity images and the same forbidden differences/denominators as the original source. All such images have preimages, and a nonzero image has an affine preimage. The fixed endomorphism [a] is expressed via ordinary addition, integer multiplication and [i]; these are rational maps on the curve with finite guarded charts. One can use the division-polynomial charts for [M], followed by a fixed finite chart cover of the morphism [a], with no quantified coordinates for their intermediate values. All formulas are taken in a finite disjunction over their rational charts.

For K=Q(i), the rank sum over F(i)/F identifies the minus eigenspace with the twist by -1, which has exactly the same Weierstrass equation. The rank of E(F) is one by the companion exact descent, hence the rank of E(F(i)) is two. This is unconditional, independent of the parity obstruction for general rational twists. The original group saturation statement is not needed for this module argument, only the explicit non-torsion P and the retained supplier/comparison properties of its integer multiples.

## 2. Ambient source and height anchor

Use the same ordinary coordinates and selective gates as in the [ambient detector](../ambient_selective_detector_20261124/README.md). The only changes are the fixed image map above, Gaussian indices rather than integer indices, and the height leaves. Work in KF=K[J]/(J^2-2), with sigma fixing K and sending J to -J. In particular sigma fixes i; this is essential.

For input X_i allow the fixed shifts c_i in {0,1}, put Y_i=X_i+c_i, beta_i=Y_i^2+B. Write the image abscissa x(A_i)=a_i+J b_i, a_i,b_i in K; these are computed rational expressions in the finite point algebra, not extra coordinates. Instead of the single rational trace T_i use both components in the eighth-power height tree: take as leaves the k triples beta_i,a_i,b_i, pair successive nodes by L^8+R^8 and carry any unpaired node, and set M_height=M_0^8+B^8 where M_0 is the resulting root. Guard every actual sum node nonzero. If some leaf is zero it can be omitted by a finite disjunction over zero-leaf patterns, imposing the corresponding zero residuals and nonzero guards on other leaves; the final sum with B is retained, and an empty tree means M_height=B^8. This finite branching avoids a pair of zero leaves creating an artificial obstruction. For the rational completeness data all nonzero leaves are rational and their eighth powers positive. There is no ordering hypothesis on arbitrary K-valued witnesses.

Set midpoint a0=M_height^4, use exactly the v110 shift lists, derivative u and selective factors, with the original six raw tests

    f(H), f(U), sigma(f(H-P_*)), sigma(f(U-A_i)),
    r-sigma(r_i'), r-Y_i,

where r=zeta(U)/zeta(H) and r_i'=zeta(U-A_i)/zeta(H-P_*). Here sigma is the K-linear involution just defined, not complex conjugation. Use the product pole and all guards of the ambient theorem, including the guards on the pair-sum collision polynomials. No rationality constraint on the input, slope or elliptic point coordinates is made.

The canonical height bounds the squared complex modulus of the Gaussian index:

    hat h([m_i]P_*)=|m_i|^2 hat h(P_*).

This follows from the canonical quadratic height and the degree |m_i|^2 of the nonzero CM endomorphism (or use that [i] preserves the height and reverses the sign of its cross term with P_*). The fixed P_* has positive canonical height. The standard bound |h(x(Q))-2 hat h(Q)|<=C_E for the fixed curve then gives

    |m_i|^2 <= C (h(a_i)+h(b_i)+1)

since h(a_i+J b_i)<=h(a_i)+h(b_i)+h(J)+log 2. This avoids assuming a trace lower bound for nonrational Gaussian multiples. For zero components use height zero. The eighth-power lemma of the ambient theorem, for ordinary abc over K, gives h(beta_i),h(a_i),h(b_i),h(B)<=h(M_height)/2+O(1), uniformly in all tuples and the positive fixed integer B. Consequently |m_i|^2<=C'(h(M_height)+1) and h(Y_i)<=h(M_height)/2+O(1). These are exactly the height controls needed below. No new variables are used.

## 3. Soundness: recover Gaussian indices

At a good rational prime unramified in K and F, the rank-two algebra over K_v has two slots, or is an unramified quadratic local field. The v110 selective valuation lemma applies literally to these slots. The product pole supplies the universal obstruction to negative odd valuations of its input. At every active contact of index i and v(u)=1, there is a slot at which all six raw tests have positive valuation.

The first four tests give the formal groups for H,U at the first slot and H-P_*,U-A_i at the other. Extend the formal logarithm to a nonzero scalar on P_* by multiplying into the injective formal subgroup and dividing by the integer. Its value is nonzero because P_* is nontorsion. The logarithm commutes with [i]; on the formal groups its relative precision is the same as in v22, since the curve is unchanged. Thus the exact logarithmic ratios are

    j/h and (j-m_i)/(h-1)

in Q(i). Since sigma fixes i, the conjugated ratio in the fifth test approximates the *same* second Gaussian ratio at the successful slot. Every Gaussian integer is integral at that slot, and at least one of h,h-1 is a unit. The corresponding exact ratio is integral; the fifth test and the relative formal precision then make the other integral too. Their residue classes agree. Multiplying by h and h-1 and subtracting gives r congruent to m_i at the successful slot. The sixth test implies Y_i congruent to m_i. Because both are in K, this gives v_P(Y_i-m_i)>0 at the underlying prime of K. No hypothesis of rational Gaussian index or equality of complex conjugates has been used.

The ambient simple-contact proof with ordinary abc over K gives, for each i, normalized consumed-prime weight R_i >= 393/100 h(M_height)-O(1), with all exceptional primes fixed. If Y_i!=m_i then

    R_i <= h(Y_i-m_i)
        <= h(Y_i)+h(m_i)+log 2
        <= h(M_height)/2+log(1+|m_i|)+O(1).

The last inequality uses the absolute height of a Gaussian integer: h(m_i)=log max(1,|m_i|). The positive margin and the Gaussian-index height control of Section 2 bound |m_i| and h(M_height) uniformly in B. This contradicts the fixed anchor height h(B)<=h(M_height)/2+O(1) for B sufficiently large. Hence all Y_i=m_i, and X_i belongs to Z[i].

## 4. Integer completeness and coefficient count

For every rational integer tuple choose shifts so n_i=X_i+c_i!=0, and use A_i=[n_i]P_* (in E(F)). Their coordinates a_i,b_i, the height leaves and M_height are rational and fixed before the prime-pattern step. The nonzero eighth-power leaves make the scale positive, with a0 a rational fourth power. The old compatible prime supplier for P and the two-index CRT refinements for integer indices work also for P_*=[M]P: an old required formal multiple becomes a formal multiple after multiplication by M. One can enlarge the fixed prime exclusions by the prime divisors of M, and choose the same bounded neighborhoods and real recurrence with the nontorsion cyclic generator P_*. Choose H,U with rational integer indices in Z P_*, not arbitrary Gaussian indices, with the prescribed CRT residues for each n_i. All raw tests are then in F, and their two-slot trace produces the actual rational pole input e. The selective lemma, nonselected-prime parity, fixed-place dyadic class-seven preparation and real interval 0<e<1 are exactly those in v110/ambient completeness. In particular this step applies the BB theorem only to rational e, never to an arbitrary e in K. Supply its two rational free parameters and finite terminal root. The fixed image map admits preimages of the chosen points by Section 1; those preimages may be nonrational over F. This proves Z^k subset S_k.

Retain two K-components of the abscissa of each of the k+2 preimages. Adjoin the two ordinate components by the original rank-four point algebra for x^3-Dx (not the square-abscissa chart). Compute the fixed image maps, then the raw tests, tree, contacts and gates by rational expression DAGs and guarded field norm inverses. The rank-two algebra is a field since K and F are disjoint. Adjoin the cleared pole square root in a finite monic stage. Use the selected-character encoder of the absorbed rationality theorem over K, together with norm conjunctions for the finite chart and zero-leaf strata. The one encoder coordinate suffices; the count is

    k+2(k+2)+1 slope+2 pole parameters+1 encoder=3k+8.

The polynomial has coefficients in K, and clearing fixed denominators makes them integral in O_K. The integer and Gaussian rings are preserved by the relevant coefficient conjugation when K=Q(i); one may take the product with the coefficient-conjugate polynomial for an integer-coefficient definition, if desired.

## 5. Extract the required ring or subfield

For K containing i, choose an integral Z-basis 1,omega_2,...,omega_d of O_K. Use k=d and substitute X_1=T-sum_{i=2}^d omega_i X_i, with the other X_i existential. Since Z^d subset S_d, every integral element has witnesses from its integer basis coefficients. Since S_d subset Z[i]^d and Z[i] is contained in O_K, every accepted T is integral. This is why full Gaussian-tuple completeness is unnecessary. The count is 3d+8. For K=Q(i) use the basis 1,i, giving 14. This polynomial has coefficients in O_K (and may be symmetrized as above).

For Z^k, intersect S_k with Q^k, using the joint torsion-supported rationality selector with k targets. Combine the two monic algebras with one common selected-character encoder rather than two. It adds 2k+1 point abscissas and 4k pole parameters, so the count is 3k+8+6k+1=9k+9. The rationality hypothesis is exactly the stable positive rank of some elliptic curve over Q plus the six-point height bound (ordinary abc suffices). The projection is Z^k since Z[i] intersect Q = Z. For K=Q(i) this gives 18 for the rational integers inside K.

The restriction i in K is crucial: if K=Q(sqrt(-2)) then KF contains i but sigma negates it, and the fifth-test subtraction would compare conjugate Gaussian indices. That case does not follow. Nor does the proof establish rank two for arbitrary K containing i, or rank stability of the original carrier in other extensions. No claim about quartic degree or numerical B is made. The separate one-parameter pole problem remains open.

Attribution: v110 and v22 point/CRT comparisons, the prior ambient-field and torsion-supported height/rationality arguments, and BB rational pole realization. The Gaussian-module replacement, two-component canonical-height anchor and sandwich projection are the present deductions.
