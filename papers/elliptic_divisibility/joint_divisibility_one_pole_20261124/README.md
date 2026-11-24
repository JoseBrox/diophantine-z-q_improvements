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
