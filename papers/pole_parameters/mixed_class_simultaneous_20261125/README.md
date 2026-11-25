# Simultaneous mixed Kummer classes and a 24/26-coordinate transfer

## Statement and arithmetic inputs

The general unrestricted-degree routes of v88 (25 and 27 coordinates) can share one of their ordinary pole parameters after changing the contact positions and making a fixed integrality-reflecting substitution in the input. The two-scale route has 24 coordinates, with a sufficiently large fixed odd coefficient exponent in an explicit progression. The three-scale route has 26 coordinates with an effectively specified sufficient exponent in that progression.

All non-pole arithmetic premises of the respective [v88 general routes](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex) are retained. The new simultaneous realization uses the row-5a congruent-number analytic rank criterion (Smith's determinant formulation of the Tian--Yuan--Zhang genus-sum result), already recorded in the project's [Jaswal audit](../../../sources/hexagon/jaswal_row5a_audit_and_simultaneous_twists_20261113.tex). For the remaining independent pole in the three-scale route use the existing BB class-seven theorem. No abc hypothesis is added. This proof does not reprove the inherited modular height, elliptic index, or prime-pattern theorems. We give a finite coefficient prescription, not a new optimized degree or coefficient-height bound.

The key difference from [the preceding mixed-shift predicate](../mixed_shift_shared_pole_20261125/README.md) is to use the product of the two input classes as the common first Kummer coordinate, and to use opposite signs for the two private complementary levels.

## 1. A sound three-parameter pole predicate

For nonzero rational inputs \(d_1,d_2\), put
\[
 F_1=1-d_1,\quad F_2=1+d_2,\quad
 D=\frac{d_1d_2}{1+d_2 r^2},\quad D_i=DF_i.
\]
Retain three ordinary rational coordinates \(r,a,b\ne0\). Guard \(F_1F_2(1+d_2r^2)\ne0\). Adjoin the finite roots
\[
 s^2=d_1(2+d_2r^2),\quad
 Y_1^2=x_1(x_1-D_1)(x_1+D_1),\quad
 Y_2^2=x_2(x_2-D_2)(x_2+D_2)
\]
where \(x_1=D_1(d_1a^2-1)\), \(x_2=D_2(1+d_2b^2)\). Guard \(s\ne0\) (the private ordinates need not be guarded). The common point on \(E_D\) is
\[
 x_0=d_1d_2,\qquad y_0=Dd_2rs.
\]
Indeed \(x_0-D=Dd_2r^2,\ x_0+D=D(2+d_2r^2)\), and \(y_0^2=x_0(x_0-D)(x_0+D)\). Thus its two nonzero shifted abscissas have classes \(Dd_2,Dd_1\), respectively; the private points have the corresponding shifted classes \(D_1d_1,D_2d_2\).

At an odd prime with even \(v_p(C)\), every nonzero shifted abscissa \(x,x-C,x+C\) on \(E_C\) has even valuation: scale \(C\) to a unit by a rational local square, and either all three factors have the same negative valuation or at most one vanishes modulo \(p\). The assertion includes the nonzero shifted abscissas of torsion points. If \(v_p(d_i)<0\) is odd then \(v_p(F_i)=v_p(d_i)\), so one of \(D,D_i\) has even valuation. Its shifted abscissa of class \(Dd_i\) or \(D_id_i\) contradicts this elementary lemma. Hence the predicate excludes every negative odd valuation of either input outside 2, even for arbitrary rational base tuples.

## 2. Simultaneous rank-one theorem

Let \(J,A,B\) be pairwise coprime positive odd squarefree integers, \(J,A,B\equiv1\bmod8\), where \(A,B>1\) have all their prime factors \(1\bmod8\). Assume every prime of any one of these three supports is a quadratic residue at every prime of a different support. Assume \(J\) has a prime \(p_*\equiv3\bmod8\) (so \(J/p_*\equiv3\bmod8\)). Put \(j_1=JA,\ j_2=JB\).

Let \(k_1,k_2>0\) be odd squarefree integers congruent to 1 modulo 8, coprime to \(JAB\), and each having a prime absent from the other. They can have arbitrary common prime factors. Assume
\[
 (k_i/p)=1\quad(p\mid j_i),\qquad
 (j_1/q)=1\quad(q\mid k_1),\qquad
 (j_2/q)=(-1/q)\quad(q\mid k_2).
\]
Then there is a positive squarefree \(n\equiv5\bmod8\), divisible by \(JAB\) and coprime to \(k_1k_2\), such that the three curves \(E_n,E_{nk_1},E_{nk_2}\) have analytic and algebraic rank exactly one and admit non-torsion points with, respectively,
\[
\begin{array}{c|c}
 E_n & [x]=[AB],\quad [x-n]=[nj_2],\quad [x+n]=[nj_1]\\
 E_{nk_1} & [x+nk_1]=[nk_1j_1]\\
 E_{nk_2} & [x-nk_2]=[nk_2j_2].
\end{array}
\]
All auxiliary primes in \(n/(JAB)\) can avoid any prescribed finite set.

### 2.1. Descent convention and rank criterion

Use the normalized 2-descent equations from the [finite-support audit v88](../../arithmetic_dependencies/finite_support_twists_20261123_v88.tex), equivalently the sign-positive, second-coordinate-odd-valuation-zero slice of the Monsky--Redei equations in the row-5a audit. If \(A_*\) denotes the matrix of additive Legendre symbols \([q/p]\) off the diagonal and its diagonal makes the row sums zero, write \(y_p=[-1/p], z_p=[2/p]\), and use vectors \(u,v\) for the prime exponents of the first and second Kummer coordinates. The normalized space satisfies
\[
 A_*u=D_yv,\qquad A_*v=D_yv+D_zu.
\]
For level \(n\equiv5\bmod8\), the pure Selmer dimension is the nullity of this system; the two rational torsion classes supply the other two dimensions. The row-5a bordered determinant criterion says that if the normalized nullity is 1 and its nonzero vector gives positive divisor classes \(\beta\equiv1\bmod8,\ d\equiv5\bmod8\), then the first genus sum is odd and the analytic rank is one. This criterion does not require \(\gcd(\beta,d)=1\): in the audit's notation the kernel vector is \((u+v,u)\), and its pairing with the border vector is \(1\). Gross--Zagier--Kolyvagin and the exact Selmer sequence then give algebraic rank one and saturation of the 2-Selmer group by rational points. The nonzero normalized class is not a torsion class.

### 2.2. Eight-vertex core

The core groups, in order numbered 0 through 7, are
\[
 (\{p_*\},J/p_*,A,B,R,S,T,V),
 \quad\text{types modulo 8 }(3,3,1,1,1,1,3,7).
\]
Products of fixed supports designate their constituent prime sets. \(R,S,T,V\) initially consist of single new primes. Write \(b_*=[(J/p_*)/p_*]\) (additive symbol). The core matrix for \(b_*=0\) is
\[
 C=\begin{pmatrix}
0&0&0&0&1&0&0&1\\
1&1&0&0&0&0&0&0\\
0&0&0&0&1&0&0&1\\
0&0&0&0&1&0&1&0\\
1&0&1&1&0&1&0&0\\
0&0&0&0&1&1&1&1\\
1&1&0&1&0&1&0&0\\
0&1&1&0&0&1&1&0
\end{pmatrix}.
\]
For \(b_*=1\), flip the two off-diagonal symbols between groups 0,1 and recompute diagonal row sums. All entries meet reciprocity, including the asymmetric type-3 edges. At the base level the normalized kernel is the line with \(u=12,\ v=244\), writing a vector as its binary mask with least significant bit at group 0.

For the private level \(nk_1\), enlarge group \(R\) by the primes of \(k_1\); only the edge to group \(B\) is forced to change, by
\(g_1=[k_1/B]=\sum_{p\mid B}[k_1/p]\).
If \(g_1=1\), flip that edge and also the edge \(R,S\). If \(g_1=0\), leave the core unchanged. For \(nk_2\), use \(g_2=[k_2/A]\) and flip \(R,A\) and \(R,S\) if \(g_2=1\). Recompute diagonal row sums. In each of the two bit cases the 16-column normalized matrix has rank 15 in every case, with nonzero masks:
\[
\begin{array}{c|c|c}
 &u&v\\
\text{base or }g_i=0&12&244\\
i=1,\ g_i=1&32&216\\
i=2,\ g_i=1&32&244 .
\end{array}
\]
These are exact finite-field assertions, checked by Gaussian elimination in verify.py. In every case the first class is 1 modulo 8 and the second is 5 modulo 8. The private1 mask \(u+v=248\) is the indicator of the complement of \(J,A\); the private2 mask \(v=244\) is the indicator of the complement of \(J,B\). The \(R\)-labels in all cases are \((0,1)\).

### 2.3. Lifting the core simultaneously

For each of the three fixed groups \(J/p_*,A,B\) use a star with any fixed constituent prime as center. Subdivide every edge by a new type-1 prime with nonsquare symbols exactly to its two endpoints and square symbols to all other original and subdivision primes. The singleton group 0 needs no subdivision. Attach every prime in the union of the two optional complement supports to the permanent center \(R\) by another such subdivided edge. All subdivision primes are included in \(n\), even when their optional leaf is absent from a particular level. Prescribe all unspecified symbols from subdivision primes to the four new permanent centers to be zero, except the required edges to \(R\).

At a subdivision vertex with both endpoints present the two normalized equations force the two endpoint labels to agree for each coordinate; with a missing optional leaf they force the subdivision labels to equal the center labels. Each noncentral original leaf row determines its subdivision labels uniquely. Summing the original rows over a group cancels all internal subdivision contributions, giving exactly the core equations (the diagonal sign vectors add to the residue type of the group). The center equation is the remaining summed equation. This proves a bijection of full and core kernel spaces, not merely an injection.

Here is how to prescribe every needed new symbol. In each fixed group the sum of its prescribed outgoing core symbols to \(R,S,T,V\) is even. Choose the outgoing bits of each constituent prime to those four centers so that their column sums are the prescribed core bits and each row sum is the degree of that prime in its **unsubdivided** star, modulo two. Such row and column margins exist because both total sums are even (and the singleton has degree zero). For example fill every noncentral row in the first column, then complete the center row to satisfy the column sums. All fixed inter-group edges are already given and have the specified aggregates: zero between \(J,A,B\), with only the stated \(b_*\) edge internal to \(J\). Choose the permanent-center symbols among themselves as in \(C\). For the optional prime set, its symbols to fixed primes are already given. Their aggregate change is zero toward \(J,A\) in private1 and toward \(J,B\) in private2; toward the other group it is precisely \(g_i\). Prescribe symbols from the optional leaves toward \(S,T,V\) with sums \(g_i,0,0\) on the support of \(k_i\). Use the two exclusive marker leaves to set these sums independently, all other bits being zero. Reciprocity gives the corresponding reverse aggregate because each \(k_i\equiv1\bmod8\). The symbols from the optional leaves to \(R\) itself are internal to its enlarged group and can be arbitrary. All these prescriptions are achievable by successive CRT and Dirichlet selections of the new primes with the specified residue classes modulo 8; symbols between new primes are specified consistently by reciprocity. No constraints on the internal Legendre symbols of the original prime sets are imposed.

We check the desired Kummer classes on the entire, rather than the compressed, support. In the base kernel the first labels at all fixed-group subdivision vertices are zero. Indeed the first coordinate of the original leaf equation has only the outgoing-center contributions and the single subdivision contribution, with \(D_yv\) zero there (all \(A,B\) primes are type 1). The prescribed outgoing sum is one at a leaf, giving first label zero. For the second coordinate the same row calculation gives second label one: on a group with second label zero, the outgoing-center sum is one, while on a group with second label one it is zero. Optional subdivisions have both labels equal to \(R=(0,1)\) because their leaves are absent. Hence the base first class is \(AB\) and the second is \(n/(JB)\) in squareclasses.

In private1 the sum of the two normalized equations is \(A_*(u+v)=D_zu\). The labels \(u+v\) on \(J,A\) are zero and those on \(B\) and the four centers are one. At every original fixed-group leaf the right hand side is zero (first label zero on \(J\), and the primes of \(A,B\) are type 1). The optional leaves add zero to the sum of the outgoing symbols at primes of \(J,A\) by \((k_1/p)=1\), and add zero to the row expression at \(B\) because both endpoint labels are one. The same margin calculation gives label one on each fixed-group subdivision. At a present optional leaf \(q\), its label is one and its first coordinate zero. The outgoing contribution from \(J,A\) is zero by \((j_1/q)=1\); all other group labels are one. Thus its subdivision also has sum-label one. At an absent leaf this follows from the center equality. Therefore \([x+nk_1]=[nk_1/(JA)]=[nk_1 j_1]\) on the full support.

In private2 use \(A_*v=D_yv+D_zu\). Now \(v=0\) on \(J,B\) and one on \(A\) and the centers. At fixed-group leaves the right side is zero and the margin calculation is identical with \(k_2,j_2\). At a present optional leaf \(q\) the right side equals \(y_q\), and the contribution from \(J,B\) is \(y_q\) by \((j_2/q)=(-1/q)\). Again the subdivision label is one. This proves the private2 full Kummer class.

All subdivision primes have type 1. Every present optional complement support has its common labels \((0,1)\) and type product 1. Consequently the two full kernel classes have precisely the same residue types modulo 8 as their core masks, even though individual subdivision labels may differ between levels. The row-5a criterion in 2.1 applies to all three simultaneously. This completes the proof of the rank-one theorem.

### 2.4. Transfer to the three-parameter pole predicate

Suppose \(d_i>0\) are such that \(F_i>0\), their squarefree classes are \(j_i\), and those of \(F_i\) are \(k_i\) as in the theorem. Apply the theorem. Rescale the two private curves from level \(nk_i\) to \(nF_i\) using the rational square ratio \(F_i/k_i\). Independently take non-torsion points in the indicated Kummer classes. The base point has positive first coordinate of class \(j_1j_2=AB\); it therefore has \(x>n\). A further common square scaling sets \(x_0=d_1d_2\), yielding precisely \(D=d_1d_2/(1+d_2r^2)\) with \(r\ne0\) rational. The ordinate gives the finite \(s\ne0\) by the equation of Section 1. The two private points give \(a,b\ne0\) rational from the stated shifted classes. This supplies all three ordinary parameters and all finite roots at the same level. Unlike a common-class sharing argument, there is no requirement \(j_1=j_2\).

## 3. Actual detector preparation

We describe explicitly the changes to the general v78/v88 source. In this section write \(X_0\) for the new input and use its substituted value
\[
 X=\prod_{j=0}^{465}(X_0-j).
\]
This is integral for integral input, divisible by \(466!\) there, and reflects integrality: at a denominator prime of \(X_0\) all factors have its negative valuation. No root or point is added.

Use the source scalar \(\rho_*\) of v88 multiplied by \((7/9)^2\), denoted \(\rho\). This scalar multiplier is important: the tempting denominator 11 can turn a positive odd valuation at 11 into a negative odd valuation. The power of 3 instead changes the prepared valuation at 3 from 6 to 2, preserving the square-denominator property. The source target is still \(\tau=X^2+1\), with \(\beta=1632X^2+2477\). Use its original root and reference preparation. At primes over 7, the fixed generator \(P=((57-28\sqrt2)/8,(-660+417\sqrt2)/32)\) reduces to nonsingular points; the smooth group orders at the two places are 7 and 8, respectively. Thus \([56]P\) is in both formal subgroups. We may take \(a-1\) divisible by 56 and 6 in the source scalar-index preparation. Choose the Lucas index \(k>0\) divisible by \(a-2\) and congruent to 1 modulo 6 (since \(a\equiv1\bmod6\), these conditions are compatible). The source labels \(t=U_{k+1}(a), b=U_k(a)/(a-2)\) are positive odd integers, and, by the recurrence at \(a\equiv1\bmod56\), satisfy \(t\equiv1,b\equiv-1\bmod56\). Also \(\tau\equiv1\bmod56\). All four root abscissas are therefore integral at both places over 7. Their two rational components are 7-integral. Directly at \(X\equiv0\bmod7\), the four scalar factors and \(T_L\) are 7-units: \(67\equiv4\bmod7\) and no power of 4 is -1. Hence \(v_7(\rho)=3\). The source scales \(\alpha_j=1+\rho T_j^2\), with \(\alpha_0=1\), are all congruent to 1 modulo 49.

For the main reduction set
\[
 \sigma_0=0,\qquad \sigma_j=4j+67/7^{2j}\quad(j=1,2).
\]
Replace \(\Theta_j=(4j+2+\Theta)\cup(4j+4+\Theta)\) by \(\Theta_0+\sigma_j\), keeping the original poles \(\gamma_j=-j-1\). Use only the first two lists in the two-scale route. Each list is still positive with ten distinct contacts. For different lists the difference of scaled positions \((\theta+\sigma_j)/\alpha_j-(\theta'+\sigma_k)/\alpha_k\) has negative **even** 7-adic valuation (the two nonzero shift valuations are distinct). Thus all cross-list positions are distinct. The shifts are unchanged modulo 67, in the sense \(\sigma_j\equiv4j\); the first two contact/pole sets remain disjoint modulo 67. The scalar-unit argument and all local tests therefore remain valid at that forced prime.

Fix the positive integer input, its roots and scales before applying the existing prime-pattern supplier. Include in the avoidance modulus all fixed prime supports required by the source, all non-7 prime divisors of the fixed contact-position differences and their denominators, and the supports needed below. The supplier in the original arithmetic-dependencies theorem permits arbitrary fixed odd avoidance coprime to 7, with selected Gaussian primes congruent to \(9\bmod16,1+3i\bmod7,i\bmod M_1\). Thus the rational selected primes are \(1\bmod8,\ 3\bmod7,\ 1\bmod M_1\). If \(p,q\) correspond to two different fixed positions \(c_p,c_q\), the rational-contact representation gives
\[
 q-p=\pm(c_p-c_q)D_0^2 w^2 .
\]
All these selected primes are units at the denominator of this difference, and do not divide \(D_0w\) (otherwise all selected primes would be equal or divisible by the same prime). By reciprocity and the avoidance congruences,
\[
 (q/p)=(-1)^{v_7(c_p-c_q)}.
\]
In particular all cross-list symbols are +1 for the main shifts. Within a list the symbols are not controlled and are not required to be.

Let \(P_j\) be the product of the ten selected primes of list \(j\). The exact source factorization gives \([R_j]=[P_j]\), since its other factor is the tenth power of \(\alpha_j/(v\delta_j)\). The actual physical pole input \(e_j=4\rho R_j/\operatorname{Tr}(W_j^{-1})^2\) therefore has squarefree class \(7JP_j\), where \(J\) is the positive squarefree part of \(\rho/7\). It is odd, \(J\equiv1\bmod8\), excludes 7, and contains 67 since \(v_{67}\rho=L\). The \(P_j\) are pairwise disjoint and coprime to \(J\); each constituent prime is mutually a quadratic residue with every prime of \(J\) (include the latter in the finite avoidance, using reciprocity). The rank theorem's initial hypotheses hold with \(A=P_0,\ B=P_1,\ p_*=67\). The source preparation ensures square reduced denominators for the actual \(e_j\), \(0<e_j<1\), dyadic class 7 with depth at least 10, and \(v_7(e_j)=3\). At each fixed place \(R_j,W_j\) can be made as close to 1 as needed; in particular \(e_j\) can be made arbitrarily close to \(\rho\) at any fixed finite preparation prime. This uses the original scalar smallness and bounded comparison neighborhoods before prime selection; the new fixed contact translates do not affect these limits.

## 4. Two exclusive markers without adding coordinates

Take \(q_1=113,q_2=233\). Restrict the fixed odd \(L\) to
\[
 L\equiv3\pmod{171033184}.
\]
The period is twice the lcm of \(q_i(q_i-1)\), so all \(\rho/7\) residues modulo \(q_i^2\) agree with those at \(L=3,X=0\). Indeed \(466!\) is divisible by \(56,q_i^2\), and the corresponding rational scalar denominators at this specialization are units, checked exactly below. Write \(H=3^{30}=205891132094649\), \(M=67q_1^2q_2^2=46445488147\). Use two menus of 11 fixed integers
\[
 m_{1,l}=32764985881+lM,\qquad
 m_{2,l}=4885738625+lM,\qquad 0\le l\le10.
\]
All are positive, less than \(H\), and congruent to 1 modulo 67. Their square residues are pairwise distinct at every prime outside the fixed support of their nonzero pairwise squared differences. Avoid this support and that of the menus themselves and \(H\) at every selected contact prime.

For the actual scalar \(d_*= \rho(0;L=3)/7\) direct modular arithmetic gives for each \(l\)
\[
 v_{q_1}(1-d_*(m_{1,l}/H)^2)=1,\quad
 v_{q_2}(1+d_*(m_{2,l}/H)^2)=1,
\]
with the other factor a unit at the opposite marker (the numerator is divisible by that other marker squared). The verification uses exact rational arithmetic, not a distribution estimate. Enlarge the temporary preparation so \(e_0/7,e_1/7\) have the corresponding residues at both markers. They are units there, so neither marker divides \(J\).

Set \(d_1=e_0(m_{1,l}/H)^2/7,\ d_2=e_1(m_{2,l'}/H)^2/7\). For prepared inputs these remain positive less than 1, in dyadic class 1 with large positive even dyadic valuation, and have square reduced denominators. Division by 7 changes its positive valuation 3 to 2, and the only denominator of the multiplier is a power of 3 where the original scalar and physical inputs have even valuation. The squareclasses remain \(JA,JB\).

Choose \(l\) to avoid \(k_1=\operatorname{sf}(1-d_1)\) containing any of the ten primes of \(B\), and \(l'\) to avoid \(k_2=\operatorname{sf}(1+d_2)\) containing any of the ten primes of \(A\). At an opposite-list prime the valuation of the corresponding unscaled \(e_j/7\) is even. If nonzero, its complement has even valuation or is a unit; if zero, at most one menu member gives positive complement valuation because the square residues are distinct. Thus ten primes forbid at most ten choices in the menu of eleven. At a prime of \(j_i\), \(d_i\) has positive odd valuation, so \(1\mp d_i\) is a unit congruent to 1. The complementary classes are coprime to \(JAB\), congruent to 1 modulo 8, and have the exclusive markers \(q_1,q_2\) respectively. At an odd prime of \(k_i\) the input must be a unit (negative input valuations are even); its residue is 1 for \(i=1\) and -1 for \(i=2\). This proves exactly the mutual-square conditions of Section 2, including those at primes of \(j_i\) by taking square parts of the complements. The common-level theorem now supplies actual rational pole witnesses. In the three-scale route the third pole remains the independently prepared BB pole.

The selection of menu indices is a finite disjunction in the final polynomial. It is not a new quantified coordinate, and the marker primes are fixed before the coefficient exponent is chosen.

## 5. Soundness and fixed coefficients

At every relevant odd prime outside a fixed set of exceptional primes, \(d_i\) has the valuation of \(e_j\). Section 1 excludes negative odd valuations of the actual physical \(e_j\), which is exactly the sole pole implication used in v78/v88 local extraction. The third independent pole, where present, has the same implication. Preserve 67 separately: every multiplier is a unit there, and the first two contact/pole lists are the old lists modulo 67. All other exceptions arising from the finite menus, the fixed scalar multiplier and fixed contact translates can be added to the finite exceptional set. This includes prime divisors of fixed contact denominators and nonzero differences and contact-pole differences. We do **not** exclude the variable prime support of the root-dependent scales in soundness. Such variable avoidance was used only to choose canonical witnesses. The old scalar-unit argument at odd \(v_p(\rho)\), the formal comparisons, and the residual divisibilities hold as before.

Use the notation \(c=|a-1|,\ B_0=\max(1,|n|,|a|,|t|,|b|)\), the source integer Lucas residual \(\Delta\) and the reduced numerator \(N\) of \(\tau-n\). With the reduced radicals \(M_\beta,M_j\) omitting the extra fixed primes, the old local conclusions are
\[
 67^{2L+1} M_\beta^3\mid c,\qquad M_j^3\mid\Delta c\quad(\Delta\ne0),
 \qquad M_j\mid Nc\quad(N\ne0).
\]
Here \(67\) is omitted from the reduced radicals (the forced prime argument is unchanged). At a new contact the same source denominator is a unit outside the enlarged fixed set, and at an odd scalar prime one of the first two contact weights is a unit since their reduced contact/pole sets are disjoint. This is precisely the v19/v78 local calculation. In the two-scale route apply the original height estimates to the shifted arguments \(t_j-\sigma_j+4j\). Fixed translations and finitely many omitted radical primes affect only constants. In particular the original exponents \(7/9,7/18,7/6\) in the v28 and v78 soundness proof are unchanged. The estimate \(h(\rho)\le4h(\beta)+2L\log67+133\) holds uniformly. First \(|\Delta c|\le10B_0^5\) gives an upper power \(35/18<2\) in the bound for \(B_0^2\), so sufficiently large \(L\) forces \(\Delta=0\); then the original growth inequality \(\log B_0>c-4\) contradicts the logarithmic bound from nonzero \(N\), since \(h(\beta)=O(c^{7/9})\). Thus \(N=0\), \(\tau=X^2+1\in\mathbb Z\) and \(X_0\in\mathbb Z\).

For the three-scale route the threshold can be fixed by the following entirely effective recipe, rather than claiming that the old \(L=143\) suffices. Let \(Q\) be the product of the original explicit-route exceptional primes and all extra **fixed** exceptions just described (include 67 for the radical bounds). Define \(K_\beta=2^{342}Q^3\). From the original effective v78 bounds, applied to the translated arguments, one obtains
\[
 h(\beta)\le K_\beta M_\beta^3,\qquad
 h(t_j)\le K M_j(A_0+\log M_j)^2,
\]
where one can choose integers \(A_0=200+\operatorname{bitlength}(Q)\),
\(K=2^{552} Q(2+\max_j\{\operatorname{bitlength}(|\operatorname{num}(\sigma_j-4j)|+1)+\operatorname{bitlength}(\operatorname{den}(\sigma_j-4j))\})\).
Indeed each old radical is at most \(Q\) times the corresponding reduced new radical; use the triangle height inequality for the fixed translations. The original explicit abscissa-sum bound gives \(B_0^2\le2h(t_0)+h(t_1)+h(t_2)+2h(\rho)+84\). Hence for a nonzero residual \(Z\) of order \(j=3\) or 1,
\[
 B_0^2\le 4K|Zc|^{1/j}(A_0+\log|Zc|)^2
              +8h(\beta)+4L\log67+350 .
\]
All constants here are explicit. Increase \(L\) until \(67^{2L+1}\ge120K_\beta\). Then \(h(\beta)\le c/120\), and \(4L\log67\le2\log c\). For \(c\ge1000\), the last three terms of the preceding inequality are at most \(B_0^2/2\) since \(B_0\ge c-1\).

Choose the least integer \(m\ge10\) with
\[
 2^m>(24K)^3(A_0+3+5m)^6.
\]
This finite search terminates. For \(B_0\ge2^m\), monotonicity of \(B_0^{1/3}/(A_0+3+5\log B_0)^2\) excludes \(\Delta\ne0\), using \(|\Delta c|\le10B_0^5\). For nonzero input residual use \(|Nc|\le2\exp(h(\beta)) B_0 c\) and put \(s=\log B_0,\ t=h(\beta)+\log c\). The absorbed bound implies \(s\le\log(16K)+t+2\log(A_0+1+s+t)\). Applying \(\log(1+w)\le w\) gives \(s\le 2t+C_1\) with, for example, \(C_1=2(\operatorname{bitlength}(16K)+2(A_0+1))\). For \(c\ge\max(1000,4(C_1+4))\) this is \(s<c-4\), impossible once \(\Delta=0\). Specify \(L\) as the least integer in the progression of Section 4 with
\[
 67^{2L+1}\ge\max(120K_\beta,1000,2^m+1,4(C_1+4)).
\]
This uses only integer arithmetic and the fixed source data. It is a complete fixed-coefficient prescription, although the large integer has not been expanded here.

## 6. Single integer polynomial and coordinate ledger

Retain the nine point charts, all source rational tests and their selected-character nonzero guards. For the explicit route use the original three scales and independent third BB pole. Replace the old scalar and contact functions by Sections 3--4, and the first two terminal poles by Section 1. For each menu pair form the monic finite algebra using the original rank-four point blocks and the new three quadratic roots (and the independent third BB quadratic root if applicable). Clear denominators in each monic root equation by rescaling its root by the denominator; include these denominators in the selected-character guard. The [joint finite algebra encoder](../../../undecidability/papers/joint_finite_algebra_encoder.tex) supplies a single polynomial in the retained ordinary coordinates and one final encoder coordinate. It handles arbitrary zero radicands and denominator zeros on unselected characters; it does not require all-character invertibility of the new complements. Multiply the resulting finitely many menu-pair polynomials (121 factors), using the same ordinary variables and encoder variable in each. This is an explicit finite integer-polynomial recipe, with no additional existential choice of a marker, prime, residue, or curve level. The existence argument in Section 2 supplies them only in the proof, not as ordinary coordinates.

The counts, including input, are
\[
\begin{array}{c|rrrrrr|r}
 &\text{input}&\text{points}&\text{slope}&\text{shared poles}&
 \text{third pole}&\text{encoder}&\text{total}\\\hline
 \text{general}&1&18&1&3&0&1&24\\
 \text{specified}&1&18&1&3&2&1&26 .
\end{array}
\]
The monic finite-algebra ranks are \(4^9 2^3\) and \(4^9 2^4\). This is a variable-count improvement, not a degree improvement. The third pole and the existing point roles are unchanged. The sufficient general exponent is still ineffective; the specified-route exponent is the finite integer procedure above. The source arithmetic hypotheses remain exactly as stated, including the normalized modular realization.

## 7. Original mixed-shift conic (separate result)

The previous mixed-shift assignment \(x=e_0,\ x-D=2De_1r^2\) has common-conic norm criterion \((j'_0,-j'_1)=1\), where \(j'_j=\operatorname{sf}(e_j)\). Even without the main new common-level construction one can enforce this criterion for all integer inputs. Use the same 7-adic scalar/root preparation but instead take fixed translates \(\sigma_0=0,\sigma_1=2751,\sigma_2=2219\). They satisfy \(\sigma_j\equiv7j\bmod49,\ \sigma_j\equiv4j\bmod67\). The ten base contact residues modulo 49 in list order are
\(2,26,1,26,26,4,28,3,28,28\).
In any given residue class modulo 7 they agree modulo 49, and each such class has odd cardinality. Since the scales are 1 modulo 49, across any two lists each row and column contains an odd number of position differences of 7-adic valuation 1, and the others have valuation 0. Thus the product of the cross Legendre symbols at any selected prime is -1. In this preparation \(j'_j=7JP_j\). At an exclusive selected prime, \(7J\) has symbol -1 and the opposite product also has symbol -1, giving mutual symbol +1 between the two input classes. At a common prime the quotient of the two unit parts is a square residue: every selected prime is 1 modulo each prime of \(J\), and the products of ten selected primes are square residues modulo 7. At 2 the second Hilbert entry \(-j'_1\) is a square, and the real symbol is trivial. These are exactly the local Hilbert-symbol tests in the previous conic criterion. Thus that conic is everywhere locally and globally soluble on the new actual prepared pair, with infinitely many points. This separate observation alone does not prove its private-twist realization, which is why Sections 1--4 use a different assignment.
