# Selective rationality: do not rationalize terminal pole witnesses

## Theorem (same arithmetic hypotheses as the sources)

Let K be a number field with a positive-rank E/Q whose rank is stable over K, and assume the six-point divisor height hypothesis of v81. Retain the prepared class-seven pole theorem and all the arithmetic hypotheses of the integer source. The [torsion-supported joint selector](../torsion_parameter_rationality_20261124/README.md) and [selected-character encoder](../absorbed_joint_rationality_20261124/README.md) give the following transfer.

Suppose a rational defining source has n ordinary arithmetic coordinates (including its distinguished input coordinates), a finite monic arithmetic-prefix algebra over them, and t ordinary terminal pole parameters. Its soundness proof after recovering a rational arithmetic character must use the terminal equations only through the absence of negative odd valuations of rational detector values, at rational primes outside a specified finite set. Its integer completeness must give rational witnesses. Suppose, in addition, that its arithmetic proof tolerates enlarging that finite set by the ramified primes of K (this is automatic for the v110 and v88 abc sources, by absorbing a fixed sum of logarithms into their ineffective height constant). Then the same integer relation has a single polynomial definition over K in at most

    7n+t+8

total K-coordinates, including the distinguished inputs. If K has no quadratic subfield and the splitting fields of all specialized guarded arithmetic-prefix algebras over Q have 2-power degree, the bound is

    7n+t+2.

If [K:Q] is odd, no extra exceptional primes are needed, and hence the transfer applies even to a fixed numerical parameter of a source with the stated soundness property. No effectiveness of the rationality correction over K is claimed.

### Applications

* For the [v110 joint integer selector](../../../undecidability/abc_selective_pole_v110/README.md) with k integer inputs, n=3k+5, t=2. The bound is **21k+45**; with no quadratic subfield it is **21k+39**. In particular Z in K takes **66** coordinates, or **60** in the no-quadratic-subfield case. For O_K in degree d use k=d and the integral-basis substitution, giving **21d+45**, or **21d+39** in the latter case. For quadratic K the bounds are **66** and **87** respectively.
* The ordinary and both fixed weak-abc eleven-coordinate sources of [v88](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex) have n=8,t=2. The same general bound is 66. The height hypothesis over K implies ordinary rational abc when it is supplied by abc over K; when only the stated fixed-divisor inequality over K is assumed, keep the separate rational abc or weak-abc assumptions. We make no claim that the weak-abc hypothesis alone supplies stable-rank rationality.
* For the general 25- and 27-coordinate v88 sources the corresponding arithmetic-prefix census is n=20, t=4 or 6. In odd degree, under their retained premises and the stable-rank and height assumptions over K, the general bounds are **152** and **154**, preserving the numerical L=143 in the latter source. For arbitrary K we do not assert that the effective fixed cutoff survives extra ramified-prime exceptions; the unconditional-in-the-exception-set generic composition remains available (176 and 190 coordinates, respectively, using 7N+1). These are not smaller definitions over Q or quartic bounds over K.

All of these are finite-polynomial specifications. Coefficients of the ring-of-integers definition are over O_K after the integral-basis substitution. No new positive-rank curve or effective exceptional-set correction is proved.

## 1. Universal local obstruction and odd ramification

The normalized product-pole equation of v88 is

    Y^2=(1-e)(v^4-d^2)(s^4-d^2),     e=d k_0^2, d k_0!=0.

This is sound over every discretely valued field of characteristic zero, not merely over Q. If v(e)<0 is odd, v(d) is odd; each quartic factor is nonzero with even valuation because 4v(v) and 2v(d) are distinct modulo four (allow the coordinate zero with infinite valuation), while 1-e has negative odd valuation. Therefore the product is not a square. The native conic pole in v81 or the three-equation native BB quartic has its own identical valuation obstruction, valid over every such field; this argument does not invoke positivity of a square over K.

For a nonzero rational e and a prime P of K over p, v_P(e)=e(P/p)v_p(e), with both valuations normalized to value group Z. If some e(P/p) is odd, a negative odd v_p(e) is impossible. For unramified p this always holds. If [K:Q] is odd, at least one e(P/p) is odd at every p since sum e(P/p)f(P/p)=[K:Q]. Thus rationality of the terminal pole witnesses is redundant: over K they have exactly the implication consumed by the rational arithmetic proof at all unramified p, or at every p in odd degree. The input detector e and the squareclass normalization d,k_0 remain rational.

In v110 the contact count outside any fixed finite set is bounded below by 393/100 h(M)-O(1) with epsilon=1/100. Discarding all extra ramified primes removes at most their fixed logarithmic weight. The subsequent local comparisons use the rational prefix, so nothing changes in those comparisons. The strict height gap (1001/997)^5/2<393/100 at k=9 and its k-dependent analogue are unchanged. Increase the ineffective B if necessary. The same reasoning applies to the ordinary and weak-abc sources of v88, whose height margins are strict and whose constants are ineffective. The general sources of v88 use only the obstruction in this lemma from their terminal block (see their arithmetic-transfer section); in odd degree their original prime ledger is unaltered.

## 2. Rationalize a selected character with one extra rationality test

Write A for the finite monic arithmetic-prefix algebra over the ring of the n ordinary arithmetic coordinates. Its finite ordered generators are theta_1,...,theta_l. Denote its rank by r. The arithmetic expressions are rational functions of these generators with explicit denominator guards. Keep the guard only on the selected character as in the selected-character encoder; if the source needs a guard on every geometric character, retain its original norm guard as a polynomial in the ordinary base.

Fix an integer h in the menu 1,...,(l-1)binom(r,2)+1 (for l=1 use h=1), and put alpha_h=sum_j h^(j-1)theta_j. At a specialization the distinct geometric characters are separated by some such h: for each unequal character pair, equality of their alpha values rules out at most l-1 integers. For every h let M_h be the multiplication matrix of alpha_h, and form the r-by-r Hankel matrix

    H_h=(Tr(M_h^(i+j)))_(0<=i,j<r).

Over an algebraic closure in characteristic zero, if the distinct eigenvalues are a_1,...,a_u of multiplicities m_1,...,m_u, then H_h=V diag(m_i) V^T, with V a full-column-rank Vandermonde matrix. Its rank is u. Thus the maximum of these finitely many ranks equals the number of geometric characters, including in nonreduced fibers. A maximizing h separates them.

Specify the maximum-rank stratum by a finite disjunction: choose s and an s-by-s minor Delta of H_h with Delta!=0, and impose vanishing of every (s+1)-by-(s+1) minor of every H_h' (vacuous if s=r). These are ordinary polynomial equations and a selected guard. There is no new coordinate.

Apply the joint rationality construction to the n ordinary arithmetic coordinates and to the algebra element alpha_h of the selected character. It needs 2(n+1)+1 point abscissas and 4(n+1) ordinary pole parameters, with all ordinates hidden in finite monic algebras. There is no ordinary coordinate for alpha_h, since it is already an element of A. If the selector holds, the ordinary coordinates and the selected value of alpha_h lie in Q. The chosen h separates all geometric characters. Since A is then defined over Q, Galois invariance of this value implies Galois invariance of its unique character. Hence every theta_j of that character is rational. This recovers the original rational point charts including all finite arithmetic coordinates. No rationality conclusion is needed for the terminal pole parameters or their roots.

For completeness start with an original rational witness, take a separating h and nonzero minor, and use rational witnesses to the joint rationality theorem for these n+1 rational values. The original terminal witnesses may also be taken rational. This produces a selected character of the combined algebra.

## 3. No-quadratic-subfield case for v110

For the v110 charts over L_0=Q(sqrt(2)), h=h0+h1 sqrt(2) has ordinary rational components and j^2=h^4-(11-6sqrt(2)). The two components of j are recovered by adjoining the square roots of the radicand and its conjugate, using sqrt(2) to take the sum and difference. The normal splitting field of the rank-four component algebra lies in the field obtained by adjoining sqrt(2) and these two square roots. For finitely many charts the compositum is still a finite Galois 2-extension of Q. This holds for zero radicands too, and the selected chart guards can only restrict the characters.

A nontrivial subfield of a finite Galois 2-extension contains a quadratic subfield: its subgroup is proper and lies in a maximal subgroup of index 2. Thus if K has no quadratic subfield, every K-valued character of this rational-base prefix is rational. The extra alpha_h test is unnecessary; the n ordinary-coordinate tests suffice. In particular this applies to odd degree, but is not restricted to odd degree. The same claim for other chart systems requires checking their entire arithmetic-prefix splitting fields, not merely the last square root.

## 4. Literal coefficient construction

Use the arithmetic-prefix multiplication tables of the chosen source, then the point ordinates of the torsion-supported selector, its terminal pole roots, and the source terminal roots, in that order (independent terminal roots may be interchanged). Rational expressions use numerator-denominator pairs; to adjoin a root of a radicand A/B, adjoin a root of Z^2-AB and recover Z/B at a guarded character. Include every actual source guard and every joint rationality guard, including H applied to alpha_h. The norm guards of sources that use all-character recovery are retained as literal base polynomials. The maximum-rank equations, where needed, are also retained. Apply the selected-character finite determinant of the absorbed joint-rationality theorem, including all these conditions by the guard product, Eisenstein norm conjunction and finite disjunction. This yields a polynomial over Q, hence over Z after clearing rational coefficient denominators. Primitive normalization is permitted. All monic towers are finite free; a finite degree bound is obtained by expanding this specified finite sequence of matrix operations, products and norms in the fixed data. The ineffective finite correction from the rationality theorem prevents a numerical coefficient or degree claim here.

The count is n+t ordinary source coordinates, 2(n+1)+1 ordinary point coordinates, 4(n+1) ordinary rationality-pole parameters, and one common encoder =7n+t+8. Without alpha it is 7n+t+2. There are no extra ordinary coordinates for the rank strata, norm forms, ordinates, source terminal roots, or separator values. The selected-character argument works over nonreal K (one must not replace the norm conjunction by a sum of squares there).

For O_K, choose an integral basis 1,omega_2,...,omega_d, and substitute the first of the d integer inputs by X-sum_{j=2}^d omega_j x_j. This is the usual integral-basis transfer and preserves the count; the polynomial's coefficients then lie in O_K. It does not require the ambient input X itself to be rational.

## Scope and attribution

The local obstruction is the elementary half of the Pheidas predicates in Pasten--Vidaux and Bhargava--Burungale. The actual rational completeness used here is the published class-seven BB theorem already used by the project. The proof uses the existing joint arithmetic selector v110 (including all its stated external premises), the new torsion-supported rationality argument, and the older finite-algebra encoder. It is an unrestricted-degree transfer, not a reduction of the Z-over-Q polynomial, not an independent verification of the elliptic rank or prime-pattern inputs, and not an unconditional result for every number field.
