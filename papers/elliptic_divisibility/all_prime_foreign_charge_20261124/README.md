# All-prime foreign denominator charging and its exact height budget

## Statement

Continue the [height-anchored quotient](../height_anchored_quotient_20261124/README.md) and [duplication-mass continuation](../duplication_mass_and_bounded_quotients_20261124/README.md), on the rational carrier
\[
 E:y^2=x^3-2x,\qquad P=(9/4,-21/8),\qquad q=\widehat h(P)>0.
\]
Retain their cyclic square-abscissa charts, ordinary rational abc when invoking their quantitative mass and input-height results, and the published class-seven BB pole realization. Write \(H=[h]P,\ U=[j]P\), with nonzero integer labels. A foreign prime means a prime at which \(U\) is formal but \(H\) is not formal. The following results hold.

1. There is a **nine-coordinate relation**, obtained by adding one rational charging variable and one coupled BB pole to the six-coordinate source, which forces **every foreign prime of odd positive depth** outside the fixed scaling primes to divide the numerator of the charging variable with a specified multiplicity. This includes every foreign simple denominator prime, without any splitting restriction. No assertion of detecting every even-depth prime is made.
2. All integer inputs of the six-coordinate source still have complete witnesses, with arbitrarily large references. In fact the new relation projects onto the entire guarded old source: any old witness extends. Thus the extra condition alone is not a definition of the integers and does not establish a quotient-size cap.
3. For every fixed nonzero integer \(m\), on true witnesses \(U=[m]H\), the optimal asymptotic logarithmic height of the charge is
\[
 \tag{1}
 (3(m^2-1)+o(1))q h^2
\]
along suitable arbitrarily large reference indices, and this is an asymptotic lower bound on all such witnesses. This last statement uses ordinary abc; no new selective prime-distribution input is needed.
4. A uniform upper bound on the logarithmic height of this one charge of the form
\[
 \tag{2}
 h(s)\le C\exp(Aq h^2)
\]
with fixed positive \(C,A\), compatible with complete integer witnesses, would give a quotient cap with coefficient \(A/2\) and thus finish a sufficiently high-precision version of the six-coordinate method. **No such Diophantine upper bound is proved here.** A linear logarithmic-height bound in \(h(X),h(x(H))\) cannot preserve completeness. In particular a tempting upper bound via the original five-contact modular radical premise is impossible if its odd contacts are restricted to a bounded-height anchor: ordinary abc makes that bound much stronger and contradicts (1).

The construction is a positive transfer of all odd foreign contacts to one free witness, not a new numerical defining-variable record. It neither assumes nor derives a bound for that witness by merely imposing a real inequality.

## 1. Coupled cover and local soundness

Use \(L=y(U)\ne0\) and a new ordinary rational coordinate \(s\ne0\). Define
\[
 Z=\frac{L^2}{x(H)^4},\qquad
 \chi=\frac1{1+Z},\qquad
 T=\frac{s^2}{L^{-1}+s^2}=\frac{Ls^2}{1+Ls^2},\qquad
 C=(1-\chi)T ,
\]
\[
 b=1+LC^2,\qquad e=\frac{112}{841}b .
\]
Guard all displayed denominators and \(e\ne0\). Retain two ordinary parameters \(v,w\), and one finite root, with
\[
 Y^2=(1-e)(v^4-e^2)(w^4-e^2).
\]
This is the BB product pole, imposed on the *actual* coupled scalar \(e(H,U,s)\). All the original six-coordinate equations and guards remain in force. The new finite ordinate can be adjoined to their common monic algebra, with numerator-denominator clearing and the same selected-character encoder. Thus the count is \(6+1+2=9\). The original comparison precision is not altered.

Suppose \(p\notin\{2,7,29\}\) is a good foreign prime at which \(U\) is formal of depth \(a=v_p(-x(U)/y(U))>0\), with \(a\) odd. Then
\[
 v_p(L)=-3a,\qquad v_p(x(H))\ge0 .
\]
Consequently \(v_p(Z)=-6a-4v_p(x(H))<0\) and \(\chi\equiv0\bmod p\). Thus \(v_p(1-\chi)=0\). The two summands of \(L^{-1}+s^2\) have distinct valuation parity; hence \(T\) is integral, with
\[
 v_p(T)=2v_p(s)-\min(3a,2v_p(s)).
\]
If the BB pole holds then \(e\) has no negative odd valuation. Since \(v_p(LC^2)\) is odd, the only possibility is
\[
 -3a+2v_p(C)>0 .
\]
Indeed, if this valuation were negative, adding 1 would preserve it; zero is impossible by parity. Since \(v_p(C)=v_p(T)\), this inequality is equivalent to
\[
 \tag{3} v_p(s)>\frac94 a.
\]
At a foreign simple prime \(a=1\) this means \(v_p(s)\ge3\). Conversely (3) suffices for \(b\) to be a unit at this prime. This is an exact local equivalence for the negative-odd denominator obstruction, not an assertion that every locally admissible scalar has a rational pole witness.

For any odd valuation \(\nu=v_p(L)\) (positive or negative), the valuations of \(Z\) and of \(L^{-1},s^2\) cannot tie in the relevant sums: \(v_p(Z)=2\nu-4v_p(x(H))\equiv2\bmod4\). Both \(1-\chi\) and \(T\) are therefore integral. In particular when \(\nu>0\) is odd, \(b\) is integral. When \(\nu\) is even, a negative valuation of \(1+LC^2\) is necessarily even. These facts hold irrespective of foreign denominator primes of \(s\). The only extra denominator conditions to be prepared are at negative odd valuations of \(L\) and the fixed scaling primes.

## 2. Complete actual witnesses, not just local solubility

Fix any guarded old witness \(X,H,U\), including one of its actual old BB realizations. The points and \(L\) are fixed rational numbers. At each prime where \(v_p(L)<0\) is odd, and at \(2,7,29\), prescribe \(s\) sufficiently deep so that \(T\) and hence \(LC^2\) are arbitrarily small locally. The value \(1-\chi\) is fixed and finite because \(1+Z>0\) over the rationals. At the real place \(s\to0\) gives \(T\to0\) and \(b\to1\). These are finite local open conditions. Ordinary rational weak approximation, or elementary CRT with a denominator prime outside the fixed set, supplies a nonzero rational \(s\) satisfying all of them and avoiding all guards. In particular \(1+Ls^2\ne0\).

At every other prime the integral/positive-odd or even-valuation calculation of Section 1 applies. At 2 we ensure \(b\equiv1\bmod8\), at 7 and 29 we ensure \(b\) is a unit, and really \(0<112b/841<1\). Thus \(e\) has square reduced denominator, dyadic class seven and dyadic valuation four. The actual BB theorem supplies \(v,w,Y\) after the charge is chosen. This proves complete extension of *every* old witness. In particular any noninteger false input of the previous six-coordinate theorem still has complete witnesses.

This use of weak approximation is legitimate because the charge is not required to have small height in this extension theorem. It is not a proof of any bound such as (2).

## 3. Lower bound at all foreign primes and the conditional quotient cap

For a rational point \([n]P\), write \(B_n\) for its square-root denominator, so \(x([n]P)=A_n/B_n^2\) in lowest terms. Under ordinary abc the doubled-point mass estimate in the [duplication continuation](../duplication_mass_and_bounded_quotients_20261124/README.md) gives
\[
 \log\prod_{v_p(B_n)=1}p=q n^2+o(n^2),
 \qquad \log B_n\le q n^2+O(1).
\]
Fixed finite exclusions cost only a constant for simple support. Define \(F_1(H,U)\) to be the product of all retained foreign simple denominator primes. Subtracting the whole denominator support of \(H\) gives the uniform lower bound
\[
 \tag{4} \log F_1(H,U)\ge q j^2-q h^2-o(j^2)-O(1).
\]
Here the little-oh depends only on the fixed elliptic sequence and tends to zero relative to \(j^2\), not on any additional witness. By (3), \(F_1(H,U)^3\) divides the nonzero reduced numerator of \(s\). Thus
\[
 \tag{5}
 h(s)\ge 3q j^2-3q h^2-o(j^2)-O(1).
\]
In particular, for all sufficiently large \(|j|\),
\(h(s)\ge (3/2)qj^2-3qh^2-O(1)\).
If (2) held for some new complete coupled constraint with no additional ordinary variables, this would imply
\[
 j^2\ll \exp(Aq h^2)+h^2+1,\qquad
 \log(1+|j/h|)\le (A/2)q h^2+O(1).
\]
The old six-coordinate source already bounds the height of \(X\) and forces \(h\mid j\) for sufficiently large reference indices. The sharpened discrepancy bound in the duplication continuation makes the coefficient of \(qh^2\) for a false quotient arbitrarily large by increasing the fixed logarithm precision. Hence (2) with a coefficient independent of that precision would suffice, after a finite reference exclusion. This argument also works if the upper-bound coefficient is bounded by a specified function of the precision strictly smaller than its discrepancy coefficient. The extra constraint and its completeness are the missing theorem.

Notice that (5) is much stronger than charging only the primes inert in a fixed norm field. For \(|m|\ge2\) fixed, \(j=mh\), it implies
\[
 h(s)\ge (3(m^2-1)-o(1))q h^2.
\]
This quantitative budget is intrinsic to a charge which enforces (3) at every foreign simple prime.

## 4. Sharp attainable height for true multiplication

Fix a nonzero integer \(m\). We show that (1) is sharp for the all-prime charge, including actual pole preparation. The ordinary-abc input implies the full denominator weight at exponent at least two is \(o(n^2)\): the radical surplus is \(o(n^2)\) and \(a\le2(a-1)\) for \(a\ge2\). At a fixed finite set of primes the denominator exponents of \([n]P\) grow by \(O(1+\log |n|)\), by formal entry and the isometric logarithm in a sufficiently deep disk.

Choose the original reference \(H=[h]P\) as in the six-coordinate true-multiple construction for \(X=m\), but deepen it further at every fixed preparation prime and at all primes dividing \(m\). In particular, at two require
\[
 a_2(H)\ge15v_2(m)+3
\]
and sufficiently deep formal logarithm. We can still choose arbitrarily large positive \(h\) with the same real preparation. Shrink the compact real arc, for this fixed \(m\), to avoid the finitely many zeros, poles, and identity or torsion fibers of the functions of \(H,[m]H\) used in the new charge. Such an arc exists: every excluded rational function is nonzero as a rational function on the multiplication graph, and the original arc has nonempty interior in the real identity component. In particular \(L\) is uniformly bounded on this arc, independently of \(h\). All old local and real conditions continue to hold. Put \(U=[m]H\).

At any odd good prime outside the fixed primes and the primes of \(m\), if \(H\) is formal of depth \(a\), then \(U\) is formal of the **same** depth \(a\) by the formal logarithm. When this depth is odd,
\[
 v_p(Z)=2a,\qquad v_p(1-\chi)=2a,\qquad v_p(T)\ge0,
\]
so \(v_p(b-1)\ge a>0\) without any condition on \(s\). At a foreign odd-depth prime of \(U\), prescribe the minimum positive valuation
\[
 e_p=\lfloor9a_p(U)/4\rfloor+1 .
\]
At the finitely many fixed odd primes and primes of \(m\), choose nonnegative integer \(e_p\) sufficiently large that \(T\) and \(LC^2\) have the requisite positive local depths. These latter \(e_p\) may be taken \(O_m(1+\log h)\): the valuations of \(L\) and \(x(H)\) at these primes are linear in the corresponding deep formal depths, and the explicit displayed formulas then give such a sufficient linear bound. There are no conditions at foreign even-depth primes, since their negative valuations of \(L\) are even.

Let \(A\) be the positive odd integer whose prime powers are precisely these prescribed odd-prime powers (zero exponents are omitted). Set
\[
 s=A/2^t
\]
with \(t\) a sufficiently large positive integer, taking the smallest \(t\) beyond a fixed lower bound for which \(s\) is in a fixed sufficiently small positive real interval \((0,\epsilon_m)\). The real bound on \(L\) makes \(b\) uniformly close to 1 there, so all real guards and preparations hold. At every odd prime the preceding valuation conditions hold exactly. At 2, write \(a=a_2(H)\) and \(k=v_2(m)\); then \(a_2(U)=a+k\), \(v_2(L)=-3(a+k)\), and
\[
 v_2(Z)=2a-6k>0,\qquad v_2(1-\chi)=2a-6k .
\]
Since \(v_2(s)=-t<0\), \(v_2(Ls^2)<0\) and \(T\) is a unit. Consequently
\[
 v_2(b-1)=-3(a+k)+2(2a-6k)=a-15k\ge3 .
\]
This gives the exact dyadic preparation even though the charge has a dyadic pole. Thus \(e\) is actually BB-prepared and its pole witnesses follow. The dyadic denominator introduces no new odd foreign prime. The height satisfies \(h(s)=\log A+O_m(1)\), because \(A\) is odd and \(t\log2=\log A+O_m(1)\) when \(A\) is large (the fixed lower bound affects only a bounded error).

For \(p\) outside the fixed set and the primes dividing \(m\), if \(p\mid B_h\) then its depths in \(B_h\) and \(B_{mh}\) agree. Their common simple support therefore has logarithmic mass \(qh^2+o(h^2)\). The complete simple mass of \(B_{mh}\) is \(qm^2h^2+o(h^2)\) for this fixed \(m\). Hence
\[
 \log F_1(H,[m]H)=q(m^2-1)h^2+o(h^2).
\]
Each foreign simple prime contributes exactly three times its logarithm to \(\log A\). Foreign odd primes of depth at least three have total full weight \(o(h^2)\), and their prescribed exponent is at most three times the depth, so they contribute \(o(h^2)\). The finitely many other preparation primes contribute \(O_m(1+\log h)\). Thus
\[
 h(s)=3q(m^2-1)h^2+o(h^2),
\]
which matches (5). This proves the stated optimal asymptotic on arbitrarily large true witnesses. For \(m=\pm1\) the same argument gives height \(o(h^2)\); for integer zero the old defining-factor convention can be used, or one can keep the nonzero-input scope of the six-coordinate relation.

## 5. Why the modular-radical upper-bound shortcut cannot work

A tempting cap on the new charge is to use the original five-contact modular estimate
\[
 h(t)\le C_2 M_5(t)^2(1+\log M_5(t))^2 .
\]
For instance, if \(t\) is a fixed fractional linear transform of \(s\), and all its odd contact primes are required to lie in the denominator support of \(H\) and the support of a fixed rational function of \(X,H\), then \(\log M_5(t)\ll h(X)+qh^2+1\). The modular estimate indeed yields an exponential upper bound on \(h(s)\) of the form (2) after the old input-height bound. But this soundness argument **cannot preserve completeness for every integer input with arbitrarily large references under ordinary abc**.

Here is the precise obstruction. For the five distinct marked contacts, including infinity, ordinary rational abc in its standard binary-form consequence gives for each fixed small \(\varepsilon>0\)
\[
 N^{(1)}_5(t)\ge(3-\varepsilon)h(t)-O(1).
\]
The full contact multiplicity sum is at most \(5h(t)+O(1)\). This follows by multiplying the five fixed primitive homogeneous linear forms in a reduced numerator-denominator pair, outside their fixed coefficient and collision primes. For each positive multiplicity \(a\), \(2\le a+(a\bmod2)\). Therefore the logarithmic positive-odd contact product satisfies
\[
 \tag{6}\log M_5(t)\ge (1-2\varepsilon)h(t)-O(1).
\]
Fixed omitted primes change only a constant. This is the same polynomial-form abc consequence already retained in the project's ordinary-abc contact estimates; no number-field abc is used.

More generally, let \(t\) be any fixed nonconstant rational function of \(s\) whose coefficients are rational functions of \(X,H\) of bounded degrees. For fixed integer \(X=m\), after excluding finitely many coefficient-degeneration reference points, its degree \(d\ge1\) is constant and
\[
 h(t)\ge d\,h(s)-C_0 h(x(H))-C_m .
\]
This is the usual height estimate for a rational map of the line: clear coefficient denominators, use the homogeneous resultant identities and the upper height inequality, absorbing the coefficient heights into \(C_0 h(x(H))+C_m\); the ordinate has height at most \(3h(x(H))/2+O(1)\). The fixed degrees give \(C_0\) independent of sufficiently large \(m\). Specializations at finitely many exceptional \(m\) can be omitted. It follows from (6) that **any** proposed bound
\[
 \log M_5(t)\le C_1 qh^2+C_2' h(X)+C_3'\log(1+|j|)+O(1)
\]
with constants independent of the witnesses forces \(h(s)\le C_4 q h^2+C_m'+O(\log(1+|j|))\), with \(C_4\) independent of \(m\). On \(j=mh\) with arbitrarily large references this contradicts (1) for every sufficiently large fixed integer \(m\).

The same proof works for a fixed finite list of such contact constraints whenever one nonconstant rational function of the charge is bounded in this manner. It also works if the radical upper bound is obtained by divisibilities in integers with logarithmic sizes \(O(h(X)+h^2+\log|j|)\), rather than literal denominator-support inclusion.

Thus exploiting the *weakness* of the modular upper bound on a five-contact radical cannot by itself close this ordinary-abc source. The necessary all-prime charge has a genuinely nonlinear logarithmic-height budget: for fixed \(m\) the coefficient of \(qh^2\) must grow at least quadratically in \(m\). A sufficient exponential cap like (2) is compatible with the sharp budget; a fixed-coefficient linear cap is not. This is a restriction on a concrete proposed mechanism, not a logical independence statement for all possible uses of the modular realization.

## 6. Scope

The new charge does not remove the old comparison pole, nor is it claimed to exclude nonintegral inputs. It uses one extra scalar and one two-parameter pole, and covers all odd formal depths at foreign primes, including all simple primes of every Frobenius type. Its exact height asymptotic explains what a successful extra coupled constraint must control. The main remaining issue is to impose a nonlinear upper height bound without another free variable and without imposing the impossible fixed-degree radical budget in Section 5. An alternative is to use a different completeness mechanism with only finitely many reference indices at each fixed integer input.

The [standard-library checker](../../../scripts/verify_foreign_charge_20261124.py) tests valuation thresholds, sharp local profiles, exact rational elliptic fixtures, and the dyadic denominator preparation; these are finite arithmetic checks. The asymptotic mass and height results are proved using the explicitly retained ordinary-abc premises, not inferred from those fixtures. No new defining-polynomial or quartic bound is asserted.


**Continuation.** The [one-conic transfer](../one_conic_foreign_charge_20261124/README.md) removes the extra BB pole entirely, obtaining seven-coordinate extensions, including an all-depth charge into two rational conic coordinates. The executed exact checker passed 81,600 BB valuation profiles, 815 exact rational local BB scalar fixtures, and eight complete prepared-scalar fixtures (their rational pole witnesses follow from the retained BB theorem; they were not computed). It also verifies the new conic identities and torsion-degree census. The sharper optimal coefficient 3 in (1) refers to the particular BB charge of this note, not the later conic.
