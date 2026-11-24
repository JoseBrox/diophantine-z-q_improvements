# Lucas-free general routes from arbitrarily small power growth of bounded odd denominator mass

This weakens the additional arithmetic hypothesis in the [19/21-coordinate Lucas-free amplifier](../simple_denominator_amplifier_20261124/README.md). The original no-additional-abc records are not replaced. The new result shows that proving the previously requested *linear* simple-denominator mass is considerably more than necessary.

## 1. Statement

Retain the original \(K=\mathbb Q(\sqrt2)\), \(E:y^2=x^3-(3-\sqrt2)^2x\), \(P\), cyclic point charts, modular contact-height and trace-height premises, simultaneous prime supplier and BB prepared pole theorem of the 19/21-coordinate construction. For a nonzero ordinary integer \(c\), at each good unramified odd rational prime \(p\) let
\[
 a_p(c)=\max_{\mathfrak p\mid p}\max(0,-v_{\mathfrak p}(x([c]P))/2)
\]
be the maximum formal depth; valuations are normalized by \(v_{\mathfrak p}(p)=1\). Outside a fixed set \(S\) containing the bad, ramified and scaling primes, define for any fixed integer \(d\ge1\)
\[
 \mathcal M_d(c)=
    \sum_{\substack{p\notin S\\1\le a_p(c)\le d\\a_p(c)\text{ odd}}}
        a_p(c)\log p .
\]
Assume only
\[
 \tag{OM}
 \mathcal M_d(c)\ge C_0 |c|^\eta\quad(|c|\ge c_0)
\]
for some fixed \(d\ge1,\eta>0,C_0>0\) and threshold \(c_0\). The constants may be ineffective. In particular it suffices that the logarithmic weight of bounded odd denominator depths has any fixed positive power growth, not necessarily linear growth and not necessarily exponent-one depths. The earlier hypothesis (SD) is the special case \(d=1,\eta=1,C_0=1\).

**Theorem.** Under (OM) and the corresponding original arithmetic premises, the Lucas-free constructions give **19 and 21 total rational coordinates**, respectively for the two-scale and three-scale routes. The coefficient threshold for the three-scale route is effective relative to valid effective data \(d,\eta,C_0,c_0\) for (OM) and the retained explicit height constants. No extra free coordinate is needed to increase the scalar precision.

We do not establish (OM) from the original modular and prime-pattern premises, nor assert it is logically independent of them. It remains an additional condition. Since \(d=1\) already follows from the previously proved weak-abc duplication mass at exponent below \(3/2\) over \(K\), the present theorem is a weaker **sufficient target**, not a new no-additional-abc theorem.

## 2. One weight for any fixed bounded odd depth

For \(Q=[c]P\ne O\) write \(y(Q)=y_0+y_1\sqrt2\). Set the fixed odd integer \(s=6d-1\), and choose a branch \(\epsilon\in\{1,2\}\) with
\[
 \ell=y_0^s+\epsilon y_1^{s+2}\ne0 .
\]
Such a branch exists, since vanishing for both choices would give \(y_1=0\) and then \(y_0=0\), impossible for the nontorsion \(Q\).

Suppose \(p\) occurs in \(\mathcal M_d(c)\), with \(a=a_p(c)\). The integral basis \(1,\sqrt2\) is unramified and has unit discriminant at such odd primes, so the minimum of the rational component valuations equals the minimum of the slot valuations:
\[
 \min(v_p(y_0),v_p(y_1))=-3a.
\]
This holds also for an inert prime (use the unramified quadratic integer basis). As usual zero components have infinite valuation. If \(v_p(y_1)=-3a\), the second term of \(\ell\) strictly dominates, giving \(v_p(\ell)=-3a(s+2)\). Otherwise \(v_p(y_0)=-3a\) and \(v_p(y_1)\ge-3a+1\). Then
\[
 (s+2)(-3a+1)-s(-3a)=s+2-6a\ge1
\]
because \(a\le d\). So the first term strictly dominates, giving \(v_p(\ell)=-3as\). Both valuations are negative odd since \(a,s,s+2\) are odd. This solves the cancellation issue for the full fixed menu of odd depths \(1,3,\ldots,d\); it does not try to implement a universal parity OR for arbitrary depths.

Use exactly the old amplifier with \(T=[j]P\ne O\),
\[
 Z=\ell^2/x(T)^{24},\quad \chi=(1+Z)^{-1},\quad
 F=z(T)/z(Q),\quad J=F^2/(\ell^{-1}+F^2),\quad
 C=2-\operatorname{Tr}(\chi(1-J)),\quad e=\frac{112}{841}(1+\ell C^2).
\]
Here \(z=-x/y\); guard all divisions and \(e\ne0\). Use the old BB pole with argument \(e\), two ordinary rational parameters and its finite ordinate. At every retained prime with negative odd valuation \(\nu=v_p(\ell)\), the parent's local Boolean-trace proof shows both (or the inert) slots have \(T\) formal and \(2v(F)>-\nu\). Specifically \(\chi,J\) have residues in \(\{0,1\}\) by distinct valuation parities, and the pole forces \(v_p(C)>-\nu/2\). Their trace sum is then two, so every slot has residue \(\chi(1-J)=1\). Take a slot of maximum depth \(a\) of \(Q\). The isometric logarithm for the two formal points gives \(v(F)=v_p(j/c)\). Therefore
\[
 v_p(j)> v_p(c)+\frac32 as\ge\frac32 as .
\]
Multiplication of all these integer divisibilities gives
\[
 \tag{1} \log|j|\ge\frac32s\,\mathcal M_d(c).
\]

Completeness is unchanged: once \(Q\) is fixed, so is \(\ell\). Choose \(T\) sufficiently deep at the finite negative-odd support of \(\ell\) and at \(2,7,29\), and close to the identity at both real embeddings. The amplifier tends to \(112/841\) at these places. At every other prime the old even-valuation or odd-positive-valuation calculation suffices. Thus the actual argument is prepared and its BB witnesses are chosen at this stage. This step does not involve the later comparison slope or reference.

## 3. Arbitrary scalar precision without more points or poles

Use the five point roles of the Lucas-free source:
\[
 A=[n]P,\ S_0=[a]P,\ T=[j]P,\ H=[h]P,\ U=[u_0]P,
 \qquad c=|a-1|>0,\ B=\max(1,|n|,|a|,|j|).
\]
In the amplifier one uses \(Q=S_0-P\); its denominator depth is unchanged by sign of the index \(a-1\). Retain the six comparison tests of order one, the v88 scalar \(\rho\) with four finite contacts in \(\beta=1632X^2+2477\), the target \(\tau=X^2+1\), the contact functions \(R_i,\delta_i,w_i=\rho R_i\), and the two or three scales determined by \(x(A)+x(S_0)+x(T)\). All these are exactly as in the earlier Lucas-free source.

The sole change to the comparison pole functions is to replace the six scalar orders \((1,1,1,1,3,3)\) by
\[
 (\kappa_1,\ldots,\kappa_6)=(1,1,1,1,k,k)
\]
for a fixed integer \(k\ge3\). The six scalar functions \(S_i\) remain the rational components of \(f(H),f(S_0-P),z(S_0-P)/z(H)\). As before put
\[
 G_{i,j}=R_i^{\kappa_j}\frac{R_iS_j}{1+R_iS_j},\qquad
 W_i=\prod_{j=1}^6(1+C_j^2/(\delta_i^2w_i))
              \prod_{j=1}^6(1+G_{i,j}^2/w_i^{2\kappa_j-1}).
\]
The \(C_j\) are the six original field comparison functions. Impose BB poles on \(4w_i/\operatorname{Tr}(W_i^{-1})^2\).

At any odd valuation \(\alpha=v_p(w_i)\) every nonzero second summand has odd valuation, so all factor valuations are nonpositive. The same trace-pole obstruction yields \(\alpha>0\), a slot with \(v(W_i)>-\alpha/2\), and hence
\[
 v_p(G_{i,j})>(\kappa_j-3/4)\alpha .
\]
At a retained prime of odd scalar valuation \(\mu=v_p(\rho)\), the unchanged scalar-unit argument supplies an \(R_i\) which is a unit (also at 67). Here \(\alpha=\mu>0\). The first four scalar orders force \(H,S_0-P\) formal at all slots, and the final two force the scalar ratio to have valuation \(>(k-3/4)\mu\) at all slots. The exact formal logarithm ratio is \((a-1)/h\); the local parameter ratio has its valuation. As \(h\) is an ordinary integer, this gives
\[
 \tag{2} v_p(c)>(k-3/4)\mu .
\]
In particular for any prime of the old scalar contact radical \(M_\beta\) the valuation of \(c\) is at least \(k\); at 67 with \(\mu=L\) it is at least \((k-1)L+1\). The fixed prime is disjoint from the scalar contact radical. Thus
\[
 \tag{3} 67^{(k-1)L+1}M_\beta^k\mid c .
\]
The old mixed-contact argument uses either a positive-odd scalar valuation or one of the six field-test slots, and still gives \(M_i\mid N c\) for every comparison radical, whenever \(N=\operatorname{num}(\tau-n)\ne0\). In particular no extra local comparison precision is demanded of a field test at a comparison prime.

Completeness with the larger \(k\) is identical in order to the old source. For the initial finite places choose \(S_0-P\) sufficiently close to the identity relative to the initially chosen \(H\), with tolerances now depending on the fixed \(k\). The prime-pattern and recurrence inputs already allow arbitrary fixed finite tolerances. Once the roots are chosen, the actual amplifier and its witness are fixed before comparison prime selection. At a fresh selected comparison prime the scalar component alternatives \(v_p(S_j)\ge0\) or \(v_p(S_j)\le-2\) imply \(\Phi_{R_i}(S_j)=R_iS_j/(1+R_iS_j)\) is integral when \(v_p(R_i)=1\). Thus \(v_p(G_{i,j})\ge\kappa_j\), and each new scalar factor is congruent to one at both slots, for every fixed \(k\). The six field comparison factors, the trace unit, the square-denominator argument at all other primes and the real/dyadic preparation are exactly as before. No new independence between a point and a later contact argument is asserted.

## 4. Height contradiction under (OM)

For the two-scale version the existing scalar modular height inequality and (3) give
\[
 h(\beta)\le H_1 M_\beta^{7/3}
          \le H_1 c^{7/(3k)} .
\]
For the three-scale effective version the old explicit inequality gives
\[
 h(\beta)< 2^{342}M_\beta^3 \le 2^{342} c^{3/k}.
\]
The scalar upper height estimate for \(\rho\) and the root aggregate inequalities are unchanged. The proof of the old Lucas-free source therefore still gives, when \(N\ne0\),
\[
 \log B\le\frac75(h(\beta)+\log c)+O(1)
\]
in the two-scale case for sufficiently large \(c\) (fixed \(k\)). Here the lower-order terms are absorbed exactly as in the parent: \(k\ge3\) implies all the old scalar bounds, and \(L\log67\le(\log c)/(k-1)\). In the three-scale case all the old effective absorption inequalities apply for \(L\ge143\), since (3) implies their weaker anchor bound; in particular
\[
 \log B<2(h(\beta)+\log c)+574 .
\]
Thus in either case
\[
 \tag{4}\log B=O(c^{3/k}+\log c+1)\quad\text{if }N\ne0.
\]
All constants are independent of the variable input and witnesses; \(k\) is fixed.

Choose \(k\ge3\) with \(3/k<\eta\). Combining (1), (OM) and \(B\ge|j|\) gives \(\log B\ge(3/2)sC_0c^\eta\) for large \(c\), in contradiction with (4). The strict exponent gap is decisive even if \(C_0\) is arbitrarily small. Increasing the fixed odd \(L\) in (3) ensures that every solution lies past the necessary threshold. Hence \(N=0\), \(\tau=n\in\mathbb Z\), and \(X\in\mathbb Z\) by the elementary denominator argument. Integer completeness was checked above and in the parent.

The effective three-scale choice can be made algorithmically when the constants in (OM) are provided effectively, using the explicit inequality of Section 4 and its positive exponent gap. With merely existential mass constants this is an existence theorem. We do not claim the old fixed \(L=143\) suffices without an explicit new threshold.

## 5. Count and limitations

All the new operations are rational functions of the same existing point charts and the same slope. Only fixed degrees are increased. Use the identical finite monic-algebra compiler of the earlier 19/21-coordinate theorem, with the new rational expressions and their selected-character nonzero guards; the two-element \(\epsilon\) menu is unchanged. The count remains
\[
 1+5\cdot2+1+2k_{\mathrm{scales}}+2+1=15+2k_{\mathrm{scales}}
\]
for \(k_{\mathrm{scales}}=2,3\). The symbol \(k\) used for the scalar precision is not the number of comparison poles. No new ordinary coordinate appears, and no claim of a particular numerical degree ceiling or quartic transfer is made.

This isolates a much weaker missing arithmetic statement: \(\liminf_{|c|\to\infty}\log(1+\mathcal M_d(c))/\log |c|>0\) for **some fixed** \(d\) suffices. A bound growing merely as a fixed power of \(\log|c|\), or just infinitude of non-Wieferich primes, would not give the exponent comparison in (4). The original retained modular height is polynomial in the *product* of odd contact primes and by itself supplies no such power lower bound on logarithmic denominator mass. Neither (OM) nor the quotient-size cap is proved under the original premises here.
## Reproduction

`python -B scripts/verify_sublinear_odd_mass_20261124.py` checks 39,360 component valuation profiles, 6,208 scalar precision inequalities, and rational examples of the strict exponent margins. The universally quantified inequalities are proved above. The checker does not establish (OM).
