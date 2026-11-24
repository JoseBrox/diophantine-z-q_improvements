# Duplication mass, bounded divisibility defects, and sharp quotient precision

This note continues the [simple-denominator amplifier](../simple_denominator_amplifier_20261124/README.md) and the [height-anchored quotient](../height_anchored_quotient_20261124/README.md). We found a substantially stronger mass estimate by revisiting the project's earlier [v60 duplication argument](../simple_primitive_denominators_20261117_v60.tex). The improvement is a transfer to the original quadratic carrier, followed by a new gcd argument that eliminates the need for primitive primes. We also determine the sharp exponential size of false CRT quotients in the six-coordinate source.

**No derivation of (SD) from the no-additional-abc general premises is obtained here. Nor is a Diophantine upper cap on the quotient established.** The results below strengthen the sufficient mass hypotheses and remove several unnecessary parts of the remaining target.

## 1. Duplication concentrates all four Belyi contacts in one denominator

Let \(K\) be a fixed number field of degree \(k\), \(E/K:y^2=x^3-Dx\), \(D\ne0\), with an integral fixed equation, and \(P=[2]R\) for \(R\in E(K)\) nontorsion. This does not require the abscissa of \(R\) to be a square, and \(D\) need not be a square in \(K\). Put \(q=\widehat h(P)>0\), in the normalization \(h(x([n]P))=2qn^2+O(1)\). Let \(\mathfrak B_n\) be the square root of the denominator ideal of \(x([n]P)\), so its exponent is the formal depth. Use normalized logarithmic ideal norms
\[
 \mathcal N(\mathfrak a)=k^{-1}\log N_{K/\mathbb Q}(\mathfrak a).
\]
Let \(S\) be any fixed finite set of rational primes containing the bad primes, 2, and ramified primes of \(K\).

Assume fixed weak abc over \(K\) with exponent \(\kappa>1\) and additive constant \(C_\kappa\), in the normalized truncated-height form used in the [torsion-Belyi mass theorem](../torsion_belyi_mass_20261124/README.md). Then
\[
\begin{aligned}
 \mathcal N(\operatorname{rad}\mathfrak B_n)&\ge \kappa^{-1}qn^2-O(1),\\
 \mathcal N(\mathfrak B_n)-\mathcal N(\operatorname{rad}\mathfrak B_n)
     &\le (1-\kappa^{-1})qn^2+O(1),\\
 \tag{1}
 \mathcal N\left(\prod_{\substack{\mathfrak p\nmid S\\
 v_{\mathfrak p}(\mathfrak B_n)=1}}\mathfrak p\right)
     &\ge (2/\kappa-1)qn^2-O(1).
\end{aligned}
\]
Here and below fixed exclusions from a truncated or simple support cost only a fixed additive constant.

**Proof.** Apply weak abc to
\[
 t_n=x([n]R)^2/D.
\]
The degree-four Belyi map \(x^2/D\) has contact set \(E[2]\). By the standard canonical-height comparison and \(P=2R\),
\[
 h(t_n)=2h(x([n]R))+O_D(1)=4\widehat h(R)n^2+O(1)=qn^2+O(1).
\]
At every good prime outside \(S\) and the primes dividing \(D\), a contact with \(0,1,\infty\) is equivalent to reduction of \([n]R\) into the geometric two-torsion: \(x=0\), \(x^2=D\), or reduction to \(O\). This is in turn exactly the condition that \([n]P\) reduce to \(O\). This equivalence holds without rational two-torsion, since the geometric kernel of [2] is the two-torsion and the residue characteristic is odd. Thus the truncated contact count is the truncated denominator count of the **doubled** point, up to a fixed finite-prime contribution. Applying weak abc gives the first inequality. The full normalized denominator norm is at most \(h(x([n]P))/2=qn^2+O(1)\), proving the surplus bound. At a prime of exponent \(a\ge2\), the full multiplicity \(a\) is at most \(2(a-1)\). Equivalently the simple-support norm is at least twice the radical norm minus the full norm. This proves (1). No archimedean denominator asymptotic is needed for these three inequalities.

In ordinary abc the simple mass is \(qn^2+o(n^2)\), by letting the fixed exponent tend to one after taking liminf, and using the full-height upper bound. In contrast, without duplication the earlier Belyi argument lost a factor of four in the surplus bound. The rational case with \(R\) itself in the doubled subgroup is already in v60; the Belyi formulation above extends it to every doubled point over \(K\), including the original project carrier and the rational carrier \(y^2=x^3-2x\) where \(P=2(2,2)\).

## 2. Consequences for the original quadratic carrier and the 19/21 alternatives

Use \(K=\mathbb Q(\sqrt2)\), \(R=(1+\sqrt2,2\sqrt2)\), \(P=[2]R\). Let \(R_{\max}(n)\) denote the product of rational good primes outside \(S\) where the maximum of the local formal depths over \(p\) is exactly one, as in (SD). If a rational prime has some local exponent at least two, its full multiplicity weight is at most three times its local surplus weight: at inert primes or when both split exponents are at least two, factor two suffices; for split profile \((b,1)\), \(b\ge2\), use \(b+1\le3(b-1)\).

For the full norm \(D_n=\mathcal N(\mathfrak B_n)\) and surplus \(S_n\), this gives
\[
 \log R_{\max}(n)\ge D_n-3S_n-O(1)
   =3\mathcal N(\operatorname{rad}\mathfrak B_n)-2D_n-O(1)
   \ge (3/\kappa-2)qn^2-O(1).
\]
The inequality follows because the normalized full multiplicity at a retained rational prime is at most \(\log p\), including split profiles \((1,0)\) and \((1,1)\). Hence **weak abc over the original quadratic carrier field at any exponent \(\kappa<3/2\) implies (SD)**, strengthening the previous \(12/11\) threshold. The old conditional 19/21-coordinate constructions work with this sufficient hypothesis, with no changes to their equations. The additive constant and the sufficient threshold are effective relative to an effective weak-abc constant and fixed canonical-height comparison bounds. No numerical threshold is asserted without them.

### Two poles detect a simple slot even if the other slot has greater depth

Let \(R_{\rm any}(n)\) denote the rational-prime product for which **some** slot has depth one, not necessarily maximum one. By (1),
\[
 \log R_{\rm any}(n)\ge (2/\kappa-1)qn^2-O(1).
\]
This requires only \(\kappa<2\) for positive quadratic mass. We can use this weaker mass directly by adding one pole pair to the preceding Lucas-free amplifier.

Retain the first weight \(\ell_1=y_0^5+\epsilon y_1^7\) from the [simple-denominator amplifier](../simple_denominator_amplifier_20261124/README.md), where \(y([c]P)=y_0+y_1\sqrt2\) and \(\epsilon\in\{1,2\}\) is its finite menu. If \(y_0\ne0\), use a second weight
\[
 \ell_2=\operatorname{Nm}(y([c]P))/\operatorname{Tr}(y([c]P)).
\]
It is a nonzero rational number. If \(y_0=0\), omit this second pole in a finite equality stratum, since then the two local ordinate valuations coincide at every odd unramified split prime. Pad the unused variables when forming the final disjunction. At an inert prime there is only one slot.

For each weight \(\ell\), independently impose the same amplifier pole, with the same common \(T=[j]P\), namely
\[
 Z=\ell^2/x(T)^{24},\quad \chi=(1+Z)^{-1},\quad
 F=z(T)/z([c]P),\quad J=F^2/(\ell^{-1}+F^2),\quad
 C=2-\operatorname{Tr}(\chi(1-J)),\quad e=112(1+\ell C^2)/841 .
\]
Impose \(Y^2=(1-e)(v^4-e^2)(s^4-e^2)\) with the usual actual selected-character guards. At a prime of maximum depth one the first pole gives \(p^8\mid j\) by the previous theorem. At any other prime of \(R_{\rm any}(c)\) the two depths are \(1,b\) with \(b\ge2\), at a split prime. The ordinate valuations are \(-3,-3b\), so the trace has valuation \(-3b\) and the norm has valuation \(-3-3b\). Therefore \(v_p(\ell_2)=-3\). The same Boolean-trace argument gives formality of \(T\) in both slots and \(2v(z(T)/z([c]P))>3\). At the simple slot the logarithm ratio gives \(v_p(j/c)\ge2\), hence \(p^2\mid j\). We have proved
\[
 R_{\rm any}(c)^2\mid j .
\]
Completeness for the two poles is simultaneous: after fixing the reference \([c]P\), choose \(T\) arbitrarily deep at the finite union of the negative-odd supports of the two actual weights and at 2,7,29, and close to the identity at both real embeddings. Both pole inputs then have the requisite limiting value \(112/841\). At other primes the same even-valuation or odd-positive-valuation argument applies to each weight separately. Apply BB independently after choosing the one common \(T\). No extra elliptic point is required.

It follows that the Lucas-free construction gives **21/23 total coordinates** under the original respective general premises **plus** weak abc over \(K\) at any fixed exponent \(\kappa<2\). The soundness contradiction uses \(\log|j|\ge2\log R_{\rm any}(c)\ge2|c|\) eventually, which is more than the linear bound needed in the existing proof. The explicit three-scale coefficient requires an effective sufficient mass threshold as before. The same finite-algebra recipe applies, with one further terminal square root and two more ordinary pole parameters. This is an alternative sufficient hypothesis, not the desired result under the original no-additional-abc premises alone.

## 3. All simple primes suffice for a bounded divisibility defect

Now take \(K=\mathbb Q\) and \(P=2R\) on the rational carrier. Let \(L_h\) be the product of all simple denominator primes of \(H=[h]P\) outside a fixed set, and assume a predicate has forced \(U=[j]P\) to be formal at every prime of a subset of these simple primes, of product \(M_h\). No primitive hypothesis is needed. At every such prime the reduction order of \(P\) divides both \(h\) and \(j\), and hence divides \(g=\gcd(|h|,|j|)\). Consequently
\[
 \tag{2} M_h\mid B_g,\qquad \log M_h\le qg^2+O(1).
\]
If \(\log M_h\ge\alpha qh^2-O(1)\) for some fixed \(\alpha>0\), then for sufficiently large \(|h|\),
\[
 |h|/g\le \sqrt{2/\alpha}.
\]
In particular the reduced denominator of \(j/h\) is bounded by a fixed integer. If \(\alpha>1/4\), then in fact \(h\mid j\) for sufficiently large \(|h|\): a proper positive divisor \(g\) of \(|h|\) has \(g\le|h|/2\), contradicting (2) with the strict coefficient gap.

Thus the simple-support detector of v60 forces exact divisibility, for every sufficiently large index, under any fixed weak rational abc exponent \(\kappa<8/5\), by (1). Under every \(\kappa<2\) it forces bounded denominator of the quotient. This is stronger for divisibility than proving existence of one simple **primitive** prime, since several nonprimitive primes may jointly generate the full reduction-order lcm. No coprime-index progression is needed. A fixed finite-index exclusion is sufficient.

For comparison the [full primitive-part asymptotic](../torsion_belyi_mass_20261124/README.md), combined with the new surplus bound, gives the primitive exponent-one mass estimate
\[
 qh^2\left(\prod_{p\mid h}(1-p^{-2})-2(1-1/\kappa)\right)-o(h^2).
\]
It is positive uniformly in \(h\) if \(\kappa<2/(2-1/\zeta(2))\). For example \(\kappa=7/5\) gives an eventual lower bound \(qh^2/30\), since \(147/242-4/7=61/1694>1/30\). The gcd argument above has a wider range for exact divisibility and does not require the primitive asymptotic.

## 4. Six-coordinate quotient under every weak rational abc exponent below two

Fix \(1<\kappa<2\). On \(E:y^2=x^3-2x\) retain the v82 cyclic point chart and BB realization. Choose an integer \(d\) so large that
\[
 \gamma=d(2/\kappa-1)-2>0,\qquad \sigma=2/\kappa-1>0.
\]
Use \(t=X^2+100\), \(u=t(t^d-1)>1\). In contrast to the previous split-polynomial input weights, no splitting of the cyclotomic roots is required. Apply weak abc to \(t^d\). The homogeneous contact form for \(t, t^d-1,\infty\) has degree \(d+2\) and distinct geometric roots. Its positive multiplicity sum is at most \((d+2)h(t)+O(1)\); its truncated sum is at least \(d h(t)/\kappa-O(1)\). The identity \(2\le a+(a\bmod2)\) for every positive integer \(a\) bounds the logarithmic odd contact product below by \(\gamma h(t)-O(1)\). Outside fixed coefficient primes the denominator contact has even valuation, since \(t=X^2+100\), and the finite contacts are disjoint modulo \(p\) because the roots of \(t^d-1\) are simple at \(p\nmid d\) and do not meet 0. Thus the product of the positive odd primes of \(u\) has exactly this lower bound.

Choose a sufficiently large fixed integer \(K_0\) so that
\[
 \delta:=\sigma-\frac{2(d+1)}{K_0\gamma}>0 .
\]
If \(\sigma>1/4\), choose \(K_0\) even larger to make \(\delta>1/4\). Use the height-anchored source with \(L=y(H)+u^{-(4K_0+1)}\) and the same \(\chi_H,\chi_U\). In its comparison test \(F\) replace the target \(X\), if desired, by a fixed polynomial \(\tau(X)=X^r+1\) with \(r\) even. The remainder of the pole is unchanged. The valuation argument gives depth at least \(K_0\) at every positive odd input contact. It follows that
\[
 h(t)\le qh^2/(K_0\gamma)+O(1),\qquad h(X)\le qh^2/(2K_0\gamma)+O(1),
 \quad 2h(u)\le2(d+1)qh^2/(K_0\gamma)+O(1).
\]
By (1) the remaining product \(M_h\) of simple denominator primes of \(H\) outside fixed exceptions and the finite support of \(u\) satisfies \(\log M_h\ge\delta qh^2-O(1)\). The pole forces \(U\) formal at all these primes, so (2) gives the bounded denominator \(D_0=\lceil\sqrt{2/\delta}\rceil\) of \(m=j/h\); if \(\delta>1/4\), its denominator is one. This reasoning is valid for arbitrary rational solutions, not just true multiples.

At these simple primes \(L\) has valuation \(-3\) and the pole gives \(v(C)\ge2\). The Boolean product yields \(T\equiv0\), hence \(v(F)\ge2\), enough to make the truncated log ratio and its exact ratio \(m\) integral provided the target is integral. More directly, \(m\) has nonnegative valuation here because both points are formal and the reference has depth one. Once \(U\) is formal its depth is at least one, so both \(\chi\) factors have error of order at least two. In fact the refined argument of Section 5 yields \(v(F)\ge3\) and
\[
 v_p(\tau(X)-m)\ge N+3 .
\]
The logarithm truncation relative error is of order at least \(N+4\); the exact ratio \(m\) is \(p\)-integral at these primes even if its rational denominator at other primes is not one.

Write \(m=a/b\) reduced, \(1\le b\le D_0\). If \(\tau(X)\ne m\), its nonzero reduced numerator is divisible by \(M_h^{N+3}\); its absolute value is bounded by \(2\max(|a|,b)\exp(h(\tau(X)))\). Thus
\[
 \tag{3}
 \log(1+|m|)\ge
 \left((N+3)\delta-\frac{r}{2K_0\gamma}\right)qh^2-O(1)
\]
for the target \(X^r+1\). Use \(r=1\) and \(h(\tau)=h(X)\) if the target is \(X\) itself. The fixed denominator bound contributes only to the additive constant. For an even \(r\) with \(2^r>D_0\), equality \(\tau(X)=m\) implies \(X\in\mathbb Z\), because the reduced denominator of \(X^r+1\) is the \(r\)-th power of the reduced denominator of \(X\).

Completeness for integers uses \(U=[\tau(X)]H\), a true integral multiple, and exactly the old ordered reference preparation, with the new fixed scalar and its support. For nonzero target \(X\) itself use the original nonzero-input convention. The real compact arc and fixed-place preparations do not depend on the size of the actual multiplier. The finite six-coordinate monic-algebra encoding is unchanged. If an independent cap \(\log(1+|j/h|)\le C qh^2+O(1)\) were established, \(N\) could be chosen so that the coefficient in (3) exceeds \(C\), and the finite reference cutoff enlarged; this would force integrality without a separate primitive-divisor theorem. **The cap is still an additional condition, not obtained by (2).** Bounded denominator does not bound the numerator.

## 5. Sharp local precision and sharp size of false quotients

For the ordinary-abc [six-coordinate source](../height_anchored_quotient_20261124/README.md), fix a prime outside the fixed scaling exceptions with \(u\) a unit and \(H\) formal of odd depth \(a\). Assume \(h\mid j\), so \(U=[m]H\) with \(m\in\mathbb Z\). Then \(v(L)=-3a\), and \(v(Z_H),v(Z_U)\ge2a\). Write \(\chi=\chi_H\chi_U\); it is a unit with \(v(1-\chi)\ge2a\). The exact local pole obstruction is
\[
 v(C)>3a/2,\qquad C=(1-\chi)+\chi T .
\]
As \(2a>3a/2\), this is equivalent to \(v(T)>3a/2\). In
\[
 T=F^2/(L^{-1}+F^2)
\]
the two denominator valuations \(3a,2v(F)\) cannot coincide. Hence the inequality is equivalent to \(2v(F)-3a>3a/2\), or \(v(F)>9a/4\). The zero numerator case satisfies all these inequalities. The logarithm ratio has absolute truncation error at least \((N+4)a\), so this is exactly
\[
 \tag{4}v_p(m-X)>(N+9/4)a .
\]
Here the converse means sufficiency for the local denominator obstruction (indeed \(b\) is a unit), not for a local or global point on an arbitrary pole fiber. At a simple prime the necessary and sufficient precision for this obstruction is **\(N+3\)**, not just \(N+2\). The same calculation works when \(m\) is merely \(p\)-integral and \(H,U\) have equal-or-greater formal depths.

Under ordinary abc the full simple support has \(\log L_h=qh^2+o(h^2)\) by (1). For the original ten-contact source with \(K_0=100\), removing the input support loses at most \(2h(u)\le(10/299)qh^2+O(1)\). The gcd argument gives \(h\mid j\) and (4) yields the stronger uniform discrepancy bound
\[
 \log(1+|m|)\ \ge\
 \left((N+3)(1-10/299)-1/1196-o(1)\right)qh^2-O(1)
 \quad(X\ne m).
\]
The \(o(1)\) is uniform in \(X\), as it comes from the fixed elliptic denominator sequence. Increasing the reference-depth forcing coefficient makes the input-support loss arbitrarily small.

More sharply, fix **one noninteger rational input \(X\)** integral at 2,7,29. For all sufficiently large reference indices of accepted tuples, the input support is now fixed, so (4) and the full simple mass yield
\[
 \tag{5}\liminf\frac{\log(1+|m|)}{qh^2}\ge N+3.
\]
Conversely there are accepted tuples for this same \(X\) with arbitrarily large positive \(h\) and
\[
 \tag{6}\lim\frac{\log(1+|m|)}{qh^2}=N+3 .
\]
To prove this, use the exact same initial choice of \(H\) as in the false-positive theorem: deep at the fixed input support, all fixed bad and preparation primes, and at the denominator primes of \(X\) with even depth at the latter. Make \(y(H)\) dominate \(u^{-(4K_0+1)}\) at formal primes, which is automatic away from the fixed input support. Choose its real value in the old compact arc. Now fix \(H\). At each odd-depth formal prime outside the fixed set require the integer \(m\) to approximate \(X\) modulo
\[
 p^{\lfloor (N+9/4)a\rfloor+1}.
\]
There is no nonintegral target at any of these primes. For the finitely many fixed preparation or coefficient primes at which a unit condition on \(b\) is needed or the truncation requires deeper precision, impose the stronger congruence modulo \(p^{(N+4)a}\) where \(X\) is integral; elsewhere use the original parity argument. Their additional contribution to the log modulus is \(O(1+\log h)\), by the fixed-place formal depth bound. At any odd-depth formal prime of the fixed input support with \(X\) integral the same exact valuation argument applies after the initial domination of the input term. At a denominator prime of \(X\) the chosen even depth makes the pole parity automatic.

The total CRT modulus \(M\) has
\[
 \log M\le (N+3)\log B_h+O(1+\log h),
\]
since \(\lfloor(N+9/4)a\rfloor+1\le(N+3)a\) for every positive integer \(a\). Choose the positive representative \(1\le m\le M\) of its residue class, taking \(M\) for residue zero. Set \(U=[m]H\). The complete denominator and fixed-place argument of the previous false-positive theorem now works with the sharpened precision, using (4) for the odd-depth primes and the even-valuation identity elsewhere. All real bounds are independent of \(m\), and the actual scalar is prepared, so BB supplies the rational pole witnesses. The upper bound \(\log B_h\le qh^2+O(1)\) suffices for the limsup in (6), while (5) gives the matching liminf. This establishes the exact exponential scale of these counterexamples.

Consequently no cap with coefficient strictly less than \(N+3\) follows from the six-coordinate source itself. One must add a genuinely different arithmetic constraint. The stronger discrepancy estimates make the required target more precise, but do not replace the cap.

## Scope and status

The original modular height premise gives a polynomial bound in the *product* of odd contact primes, not in the logarithm of that product. It neither supplies the surplus estimate used in Section 1 nor controls exponent-one primes by itself. Ordinary primitive divisors are insufficient as their depth can be even. For background, Silverman, *Wieferich's criterion and the abc-conjecture*, J. Number Theory 30 (1988), 226–237, proves conditional infinitude of elliptic non-Wieferich primes on these CM types; [DOI](https://doi.org/10.1016/0022-314X(88)90019-4). The sought eventual linear mass (SD) would imply infinitely many such primes for the fixed original carrier, in a much stronger quantitative form. This is not a proof that (SD) is logically independent of the original premises, only the precise unresolved implication.

Attribution: v60 for duplication in the rational doubled subgroup, the previous project's torsion-Belyi and height-anchored quotient notes, Streng for the full primitive-part asymptotic, and BB for the prepared pole realization. The general doubled-point mass transfer, two-slot second pole, gcd defect estimate, \(t^d\) weak-abc input contact, and matching quotient-size asymptotic are the present deductions. The ordinary-abc and weak-abc arithmetic assumptions and other inherited rank and pole premises are expressly retained. No new no-additional-abc, 9-variable, or quartic defining-polynomial record is claimed.
