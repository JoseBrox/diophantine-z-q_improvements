# Simultaneous elliptic index divisibility through a single prepared pole

## Theorem and status

Retain ordinary rational abc, the rank-one rational point chart and the eventual exponent-one primitive denominator divisor theorem proved in [v82](../prepared_eds_divisibility_20261120_v82.tex), and the published class-seven Bhargava--Burungale pole realization (the normalized product equation in [v88](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex)). Put
\[
 E/\mathbb Q:y^2=x^3-2x,\qquad P=(9/4,-21/8).
\]
For each fixed \(k\ge1\), there is a guarded single-polynomial presentation in **\(k+4\) rational coordinates** of a subrelation on \(k+1\) nonzero points \(H=[h]P,U_i=[j_i]P\), with the following properties:

1. Every accepted tuple satisfies \(h\mid j_i\) for all \(i\).
2. Every prescribed tuple \((m_1,\ldots,m_k)\) of nonzero integers occurs as \(j_i/h=m_i\), with arbitrarily large positive reference indices \(h\).
3. All tests share a **single** pair of free pole parameters. Relative to independently imposing the preceding five-coordinate EDS predicate with a common reference and a common finite encoder, this saves \(2(k-1)\) variables.

This is an actual simultaneous divisibility subrelation, not a definition of the integers by an input-coordinate projection. In particular the previous 25/27/11 and 163/178/54 defining-variable records do not change on the basis of this result.

## Construction

The square-abscissa chart of v82 uses \(x=g^2,\ y=g\eta,\ \eta^2=g^4-2\) for each nonzero point. Retain the standard nonzero chart guards. Define, using the actual affine ordinates and abscissas,
\[
 L=y(H),\qquad
 Z_i=\frac{L^2}{x(U_i)^4},\qquad
 \chi_i=\frac{1}{1+Z_i},\qquad
 C=1-\prod_{i=1}^k\chi_i,\qquad b=1+LC^2.
\]
Every displayed denominator is nonzero on the rational point charts: the abscissas are nonzero and \(Z_i\) is positive over the reals (the ordinate of a nonzero multiple of \(P\) is nonzero). Put
\[
 e=\frac{112}{841} b=7(4/29)^2 b
\]
and require the prepared product pole
\[
 Y^2=(1-e)(v^4-e^2)(s^4-e^2),
\]
with guard \(e\ne0\). Its elementary valuation obstruction says that \(v_p(e)\) cannot be negative odd, even allowing a zero ordinate or zero pole parameters. Exclude the fixed primes \(S=\{2,7,29\}\) and any additional primes in the primitive-divisor theorem.

The local argument is independent of \(k\), and is not a universal parity-OR operation on arbitrary scalar inputs. The coupled normalization uses the reference point's ordinate to distinguish formal depth one from the nonformal case.

## Local soundness at a primitive prime

Suppose \(p\) is an odd good prime, \(H\) is formal at \(p\) and has depth \(v_p(-x(H)/y(H))=1\). Then \(v_p(L)=-3\).

If \(U_i\) is formal, \(v_p(x(U_i))=-2e_i\) with \(e_i\ge1\); consequently \(v_p(Z_i)=-6+8e_i\ge2\) and \(\chi_i\equiv1\bmod p\). If \(U_i\) is not formal, its affine abscissa is integral, so \(v_p(Z_i)=-6-4v_p(x(U_i))\le-6\) and \(v_p(\chi_i)\ge6\). Thus all \(\chi_i\) are integral. If even one \(U_i\) is nonformal, their product is divisible by \(p\), so \(C\equiv1\bmod p\) and
\[
 v_p(b)=-3.
\]
Outside \(S\) this contradicts the product pole. Hence every \(U_i\) is formal at that prime.

Use the finite reference guard from v82 excluding \(0<|h|\le h_0\), where \(h_0\) is a sufficient threshold for an exponent-one primitive denominator prime outside \(S\). Such a prime for \(H=[h]P\) has reduction order \(|h|\) for \(P\). Its formal condition on \(U_i=[j_i]P\) gives \(h\mid j_i\) simultaneously. The finite exceptional-index guard can be expressed directly on the retained square abscissa \(x(H)=g_H^2\); no additional coordinate is needed.

## True multiples: all-prime denominator control

Suppose \(U_i=[m_i]H\) for nonzero integers \(m_i\). At any rational prime where \(H\) is formal of depth \(a\ge1\), formal multiplication preserves the integral formal disk and gives \(e_i\ge a\) for every \(U_i\). This remains true for primes of bad reduction of the given integral model. Therefore
\[
 v_p(Z_i)\ge -6a+8a=2a,\qquad
 v_p(1-\chi_i)\ge2a,\qquad v_p(C)\ge2a.
\]
The last estimate follows from the product of quantities congruent to one modulo \(p^{2a}\). Hence \(v_p(b-1)\ge -3a+4a=a\), so \(b\) is a unit.

At any prime where \(H\) is not formal, \(L\) is integral. If every \(\chi_i\) is integral, then \(b\) is integral. Otherwise a pole of some \(\chi_i\) means \(v_p(1+Z_i)>0\), so \(v_p(Z_i)=0\). It follows exactly that
\[
 2v_p(L)-4v_p(x(U_i))=0,\qquad v_p(L)=2v_p(x(U_i))\in2\mathbb Z.
\]
Consequently the valuation of \(LC^2\), if finite, is even; adding 1 either leaves its negative even valuation unchanged or gives an integral result. This also handles cancellation among the various factors of \(C\). These arguments use no assumption on the valuations of the unselected \(U_i\) beyond the true-multiple relation in the formal case, and cover the primes 2 and 7 as well.

Thus \(b\) has square reduced denominator for true multiples.

## Ordered preparation

Fix any nonzero integer tuple \(m_i\). First prescribe \(H\) to be formal at \(2,7,29\), with depth at 2 at least three, and at any additional fixed primes if necessary. This imposes only a fixed divisibility condition on \(h\) and is independent of the \(m_i\). Then choose arbitrarily large positive \(h\) in that progression in a compact real arc about \(-P\) inside the identity component on which \(0<L<3\). The real recurrence used in v82 supplies such \(h\). Set \(U_i=[m_i]H\). On this arc every \(Z_i>0\), so \(0<C<1\) and \(1<b<4\). Consequently
\[
 0<e<448/841<1,\qquad e\in7\mathbb Q_2^{\times2},\qquad v_2(e)=4 .
\]
At 7, \(b\) is a unit and \(v_7(e)=1\); at 29 the possible new denominator has even valuation \(-2\). Elsewhere square-denominator soundness of \(b\) proved above gives that of \(e\). The two-adic class follows from \(b\equiv1\bmod 8\). All preparation conditions are thus on the **actual** scalar \(e\); no simultaneous exact-square assertion is imposed on any independently chosen input.

The BB theorem supplies rational \(v,s,Y\) on the actual product pole. This proves simultaneous completeness. Every \(U_i\) is a nonzero multiple of \(P\), and \(h\) can be taken beyond the finite index exclusions.

## Finite coefficient prescription and count

Use the \(k+1\) retained rational square-abscissa coordinates \(g_H,g_{U_i}\) and adjoin their monic quadratic roots \(\eta_Q\). Evaluate the displayed rational functions in the resulting finite algebra as numerator-denominator pairs, using all selected-character denominator guards. Form the pole radicand \(R=N/D\) in the same way, adjoin \(Y_*^2=ND\) and recover \(Y=Y_*/D\) when \(D\ne0\). The finite algebra is free of rank \(2^{k+2}\), with the \(k+2\) ordinate and pole generators. Use the [guarded determinant encoder](../../../undecidability/papers/joint_finite_algebra_encoder.tex), which allows guards to vanish at other characters and zero terminal roots; clear fixed rational denominators. This yields a literal finite integer-polynomial recipe. There is one additional encoder coordinate, so the total is
\[
 (k+1)+2+1=k+4.
\]
No explicit uniform degree number or effective \(h_0\) is claimed. All guards apply to selected characters. The old chart and primitive-divisor hypotheses remain in force.

## Remaining obstruction for an integer projection

Writing \(m_i=j_i/h\) now gives genuine integers, but the rational formal parameter ratio only approximates \(m_i\) locally. The primitive-prime mass of \(H\) is of order \(h^2\), not a function of the height of an independently chosen external rational input. There is also no bound on \(\log |m_i|\) from a divisibility assertion alone. A further comparison must control these quantities without fixing \(H\) and its multiples before a prime selection requiring new formal primes.

The same issue is not solved simply by adding \(h-1\mid j-n\) or any fixed finite set of shifted index divisibilities: these give congruences on the quotient modulo fixed functions of \(h\), not equality. Existential addition and divisibility on ordinary integer indices alone is decidable (Lipshitz/Bel'tyukov); one must introduce a genuinely additional arithmetic relation, not assume that general index multiplication is available. This is not a lower bound on Diophantine definitions using additional relations.

The result is a new shared arithmetic subroutine. It does not assume a one-parameter pole theorem or claim that the target 9-variable integer definition has been obtained.


## Extension: shifted references without additional point or pole parameters

The common-reference theorem extends to a finite list of **fixed integer shifts** \(a_1,\ldots,a_k\) (repetitions allowed). With the same \(k+4\) coordinates there is a guarded predicate on \(H=[h]P,U_i=[j_i]P\) implying
\[
 (h+a_i)\mid j_i\qquad (1\le i\le k).
\]
Every prescribed tuple of nonzero integer quotients \(m_i=j_i/(h+a_i)\) occurs with arbitrarily large positive \(h\). More generally one may substitute any fixed integer-linear point expressions for numerator roles in the local soundness assertion; completeness then requires that the resulting point expressions actually satisfy the intended divisible relations. This is not a multiplication predicate.

After translating the common reference by a fixed multiple of \(P\), assume one shift is zero. Let \(A\) be the set of distinct shifts and put
\[
 H_a=H+[a]P,\qquad L_a=y(H_a),\qquad L=\sum_{a\in A}L_a.
\]
The shifts and their points are fixed coefficients. Exclude the finitely many base indices where a shifted reference is the identity, the ordinary rational addition chart has a zero denominator, or a shifted reference index lies in the finite exceptional range for the primitive-divisor theorem. Require \(L\ne0\). Use
\[
 Z_i=\frac{L^2}{x(U_i)^4},\quad
 \chi_i=\frac1{1+Z_i},\quad
 C=\frac{\sum_i L_{a_i}^2(1-\chi_i)}{1+L^2},\quad
 b=1+LC^2,\quad e=7(4/q)^2 b .
\]
Here \(q\) is a fixed positive odd integer prime to seven, chosen sufficiently large below. The same product pole on \(e\) is imposed.

### Soundness

Enlarge the fixed set \(S\) to include bad primes, primes at most \(k\), primes dividing \(7q\), and primes where one of the finitely many nonzero differences \([a-a']P\) reduces to the identity. The latter are contained in the prime supports of their abscissa denominators. For each shift \(a\), choose an exponent-one primitive good prime of \(H_a\) outside \(S\) using the retained eventual primitive-divisor theorem. At that prime \(L_a\) has valuation \(-3\); all other \(L_{a'}\) are integral since their references reduce to \([a'-a]P\ne O\). Thus \(v_p(L)=-3\).

The previous local calculation with this \(L\) makes every \(\chi_i\) integral, congruent to 1 for formal \(U_i\) and to 0 otherwise. The weight \(L_a^2/(1+L^2)\) is congruent to 1, whereas the other shift weights vanish modulo \(p\). Consequently \(C\) reduces to the number of nonformal numerator points belonging to the active shift. If any such failure occurs, this count lies between 1 and \(k<p\); hence \(v_p(b)=-3\), a forbidden valuation for \(e\). Every numerator of the active shift is therefore formal. Primitivity gives the asserted divisibilities for that shift, and repeating over the finite shift list proves their conjunction.

### Completeness at all primes outside \(S\)

For prescribed nonzero \(m_i\), set \(U_i=[m_i]H_{a_i}\). At a prime outside \(S\) at most one shifted reference is formal. If all are nonformal, all \(L_a\), hence \(L\), are integral. If \(v_p(L)\) is even, the square factor in \(LC^2\) directly excludes negative odd valuations of \(b\). If \(v_p(L)\) is odd, the valuation of each \(Z_i\) is nonzero, because \(2v_p(L)-4v_p(x(U_i))\) is 2 modulo 4. All \(\chi_i\) and \(1-\chi_i\) are integral, and \(1+L^2\) is a unit (here \(v_p(L)>0\)); therefore \(C,b\) are integral.

If precisely \(H_a\) is formal of depth \(d\ge1\), then \(v_p(L)=-3d\). The even valuation case again needs no further condition. In the odd valuation case all \(\chi_i\) are integral by the same parity calculation. For every test of the active shift, formal multiplication gives depth at least \(d\), so \(v_p(Z_i)\ge2d\) and \(v_p(1-\chi_i)\ge2d\). Its shift weight is a unit. Every inactive shift weight has valuation at least \(6d\). It follows that \(v_p(C)\ge2d\), giving \(v_p(b-1)\ge d\). Thus at every prime outside \(S\) the valuation obstruction is satisfied.

### Fixed-place and real preparation

At the finitely many fixed primes choose \(H\) sufficiently deep in the formal group. The zero-shift reference has ordinate valuation \(-3d\) for depth \(d\) and dominates the bounded ordinates of the other references, which tend to the nonzero fixed points \([a]P\). For the nonzero shifts the numerator points tend to the finite nonzero points \([m_i a_i]P\); their abscissa valuations stay bounded, so \(Z_i\) has strictly negative valuation for sufficiently deep \(H\), irrespective of parity. For the zero shift its numerator depths are at least \(d\). The zero-shift weights are units and the other shift weights have valuation at least \(2d\) once the prescribed depth is sufficiently large. As above \(v_p(C)\ge2d\) and \(v_p(b-1)\ge d\). Choose \(d\ge3\) at two. These requirements impose only divisibility of \(h\) by a sufficiently large fixed integer (allowed to depend on the target quotients).

Choose a compact real arc sufficiently close to the identity on the branch where \(y(H)>0\) tends to \(+\infty\); all the other shifted references tend to finite points, so \(L>0\) throughout a suitable arc avoiding their poles. On this arc \(0\le1-\chi_i\le1\) at every real rational point under consideration. Thus \(b\ge1\) and
\[
 b\le 1+L\left(\frac{\sum_i L_{a_i}^2}{1+L^2}\right)^2
\]
is bounded above by a constant depending only on the fixed arc and shift list, not on the quotients. Choose \(q\) once, odd and prime to seven, sufficiently large that this upper bound multiplied by \(112/q^2\) is less than 1. The real recurrence in v82 gives arbitrarily large positive \(h\) in the prescribed progression visiting the arc and avoiding all finitely many excluded indices. Now \(0<e<1\), \(v_2(e)=4\), \(e\) has dyadic squareclass seven, and \(b\) is a unit at seven. Its denominator is a square at every prime by the preceding argument. Thus \(e\) is prepared, so the BB pole provides the actual rational witnesses.

### Coefficient count and verification

All shifted points are rational functions of the single retained reference point with fixed coefficients. The same rank-\(2^{k+2}\) monic algebra and selected-character guard determinant, with the new rational functions and guards substituted, give \(k+4\) coordinates. No reference variable is introduced for a shift. The finite regression checks in this directory were run with exact Python rational arithmetic: 32 ordinary true-multiple fixtures, 10 ordinary rejection fixtures, 24 shifted true-multiple fixtures tested on the complete prime-to-exclusion denominator, and 24 shifted primitive-prime rejection fixtures all passed. These finite tests do not prove the infinite primitive-divisor theorem, and the sufficient reference threshold remains ineffective. The proof of completeness above, not the finite tests, justifies the fixed-place preparation.

The resulting joint predicate can test shifted congruence conditions such as \(h\mid j\) and \(h-1\mid j-n\) on elliptic point expressions using one pole. It still needs a new mechanism bounding the quotient error or identifying an external rational input. No lower variable count for a defining polynomial of \(\mathbb Z\) is claimed.
