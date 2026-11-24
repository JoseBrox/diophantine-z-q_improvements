# Shared Boolean comparison detector (v139)

**622 / 642 rational variables, 533 / 551 quadratic residuals** (general / specified), versus v137's 651 / 671. All twelve certified source inputs, all 52 Jones source rows, the single recursive scalar pole, and the two / three comparison poles are retained. This is a transfer under the arithmetic premises of v136/v137, including the full-domain five-contact height input H4.1; no new conjecture is used.

## 1. Booleanization over the two field slots

Use the notation and physical charts of [v137](../guarded_target_v137/README.md), [v133](../weighted_private_v133/README.md) and [v131](../shared_comparison_v131/README.md). The comparison gauge is \(c=\sum_jq_j\), \(u=c^{-1}\), \(K=\mathbb Q(\rho),\rho^2=2\). For a field element \(L\) and a positive odd exponent \(s\), use the failure fraction
\[
 B_s(L)=L/(u^s+L).
\]
Compile it by the two rational components of the single quadratic field equation \(B_s(L)(u^s+L)=L\), with \(u^s\) stored when necessary. There is no zero-denominator branch: a zero denominator would imply \(L=0\) and \(u^s=0\), impossible. At a good unramified prime with \(v(u)=\mu>0\) odd, and with \(v(L)\) even (or \(L=0\)), every such failure is integral at each slot, with residue zero if \(v(L)>s\mu\) and one otherwise. This follows from the strict inequality between the even valuation and the odd \(s\mu\). The formula includes a zero test value.

The list of failures is as follows.

* For the common reference pair and each of the 15 private or growth pairs: \(B_1(F),B_1(\bar G)\), using the literal stored reciprocal abscissas (scaled by the rational squares \(k_i^2\) for input pairs). Their valuations are even at good primes, by \(y^2=x^3-Dx\) and the good-prime unit \(D\). In each slot positive valuation of a scaled reciprocal will be interpreted together with the corresponding slope comparison, not assumed to imply formal membership alone.
* For the twelve input pairs with cleared errors \(C_i=S_i'-2S_H,\ E_i=\bar T_i'-2\bar T_H\): \(B_1(C_i^2),B_1(E_i^2)\).
* For the three growth pairs, with their old primary ratios \(L_jS_j=2S_H\) and alternate cleared errors \(E_j=L_j\bar T_j-2\bar T_H\): \(B_5(E_j^2)\).
* For the old growth residual \(\delta=L_t^2-(L_a^2-1)(L_a-1)^2(2L_m+1)^2-1\): \(B_7(\delta^2)\).

There are exactly 60 failure fractions. Set
\[
 W=u+\sum_\nu B_\nu,\qquad
 D_g\operatorname{Tr}W=\operatorname{Nm}W,\qquad
 u D'_g=D_g.
\]
The sum \(W\) is a linear expression, not a stored field product. Replace the old contact gate by
\[
 g_j=1+(D'_g)^2+(c-q_j)^2/q_j,\qquad
 \tau_j(1+q_j)=g_j,\qquad d_j=7q_j\tau_j^2 .
\]
The original seven-coordinate native pole equations for \(d_j\) remain. All equations are quadratic with the same scalar square and contact registers, plus the one extra scalar \(D'_g\).

## 2. Soundness at arbitrary consumed primes

Enlarge the fixed comparison exceptional set to contain all primes at most 60. The original reflected contact-height bound remains true with an enlarged fixed constant \(H\): multiplying its odd radical by the product of the finitely many deleted primes restores the old radical, including radical one. The specified constant is still effective. This enlargement does not change the scalar exceptional set or the recursive scalar proof.

Fix any comparison contact with \(v_p(q_j)=-\mu<0\), \(\mu\) odd, outside the enlarged set. At this point do not assume \(v(c)=-\mu\). The native pole obstruction implies \(v_p(g_j)>-\mu/2\), including \(g_j=0\) via infinite valuation, because \(1+q_j\) has valuation \(-\mu\) and \(v_p(d_j)=\mu+2v_p(g_j)\) whenever \(g_j\ne0\). In the gate the nonconstant terms have even and odd valuation respectively; a negative minimum cannot cancel. Hence \(v_p(D'_g)>-\mu/4\), \(v_p(c-q_j)>-3\mu/4\), and \(v_p(c)=-\mu\). Thus \(v_p(u)=\mu\) and
\[
 v_p(D_g)=v_p(uD'_g)>3\mu/4>0.
\]
This holds without assuming any of the failures integral beforehand.

Now all 60 failures are integral at both unramified slots, counting the inert slot twice. Their residues are 0 or 1. Since \(p>60\) and \(v(u)>0\), the field sum \(W\) has positive valuation at a slot precisely when every failure there is zero modulo that prime. At most one slot can pass: if both passed, the reference \(H\) and \(H-P_0\) would both lie in the formal group at the same place, contradicting the fixed good-prime nonidentity reduction of \(P_0\). The inert case cannot pass. In particular \(W\ne0\) at any consumed prime (it cannot have infinite valuation at both slots). If \(\operatorname{Tr}W=0\) the harmonic equation forces \(\operatorname{Nm}W=0\), impossible. For the finite nonzero slots,
\[
 v_p(D_g)=v_1(W)+v_2(W)-v_p(\operatorname{Tr}W)
 \le\max(v_1(W),v_2(W)).
\]
Consequently \(D_g\) of positive valuation forces the common passing slot. This argument is only used at consumed primes. If a comparison has radical one, the original height bound and divisibility implications hold vacuously, exactly as in v131; no global trace guard has been silently added.

At the passing slot the reference formal reciprocal conditions hold. For input \(i\) both scaled reciprocals have valuation \(>\mu\), and the two slope errors have valuation \(>\mu/2\). The argument in v133 (if the physical reciprocal is nonpositive then \(S^2=1/F-DF\) contradicts the negative valuation of the reference slope) recovers the actual two formal memberships even without prior integrality of \(k_i\). The cleared slope errors have positive valuation, so division by the formal slopes gives precision at least two. The order-four formal logarithm ratios and subtraction give \(k_i\equiv m_i\bmod p^2\), including integrality in that slot. The growth pairs pass both reciprocal tests and \(v(E_j)>5\mu/2\), hence their alternate ratio agrees to precision at least four after dividing by the formal slope. As before the primary ratios are then congruent to the integral labels \(a,t,m\) modulo \(p^4\). The final test gives \(v(\delta)>7\mu/2\), i.e. at least four. Therefore the same comparison radical divisibilities \(M_j^2\mid|\operatorname{num}(k_i-m_i)|\), \(M_j^4\mid\Delta\) hold for every nonzero indicated residual.

The recursive scalar normalization and weighted aggregate are literally unchanged. The v136/v137 height absorption and Pell growth proof now apply with the enlarged comparison height constant, after fixing a sufficiently large \(N\). This proves integrality of each source input, and the unchanged 52 Jones equations prove source soundness. The general threshold remains ineffective; the specified sufficient recipe is effective under the retained quantitative premises.

## 3. Simultaneous completeness and the new infinity limit

Choose the same canonical source witnesses, prepare the shared scalar and its positive growth index, fix all difference points and aggregate shifts, and choose the comparison primes and common reference in the order of v136/v137. Enlarge prime avoidance to include the new fixed exceptional primes and all prime divisors of the fixed nonzero linear targets. At every selected simple contact prime the gauge has \(v(u)=1\). The synchronized reference depth \(d\ge1\) yields scaled reciprocal depths at least \(2d\), primary and opposite raw errors of depth at least \(3d\), growth alternate errors of depth at least \(3d\), and residual depth at least \(4d\). All 60 failures at the intended slot therefore have residue zero. In the opposite slot at least one reference failure has residue one. Since \(p>60\), \(W\) has positive valuation in the intended slot and zero valuation in the opposite slot. The trace is a unit and \(D_g\) has positive valuation. Thus \(D'_g=D_g/u\) is integral at these primes. The complementary gate term has positive valuation because \(c-q_j\) is integral and \(q_j\) has valuation \(-1\). Hence \(v(g_j)\ge0\), not necessarily exactly zero; this suffices to give positive odd valuation \(v(d_j)=1+2v(g_j)\) whenever the gate is nonzero. No assumption that \(1+(D'_g)^2\) cannot vanish modulo a selected prime is required.

At any previously prepared finite place and real infinity, the fixed point/ratio neighborhoods keep the raw tests bounded. In the same large-slope limit of v131, \(q_j\sim\lambda^{-2}\), \(c\sim m\lambda^{-2}\), \(u\to\infty\) (here \(m\) is the number of comparison contacts). Every failure tends to zero, since its denominator is dominated by the positive power of \(u\). Therefore \(W\sim u\), \(\operatorname{Tr}W\sim2u\), \(D_g\sim u/2\), \(D'_g\to1/2\). These asymptotics hold in both embeddings and include the prime two; \(m,2\) are nonzero rational constants, and no unit condition is required on them. The new gate tends to \(5/4\), as does \(\tau_j\). This nonzero rational limit gives \(d_j\sim7(5/4)^2\lambda^{-2}\), so the same sufficiently large real slope and fixed-place divisibility impose \(0<d_j<1\), class seven and depth at least four at two, and nonnegative valuation at all prescribed odd-support primes. The dyadic class follows because the asymptotic ratio tends to one, a square neighborhood in \(\mathbb Q_2\). At foreign primes the contact weights have even valuation, and the square multiplier preserves that parity. The same all-prime preparation and BB realization apply, without new arithmetic hypotheses.

## 4. Compiler and census

The compiler preserves the scalar chain, weighted pair charts, growth polynomial, contact functions, and all outer source rows of v137. Delete all private tagged factors and the field-product chain. Each input uses two formal failure fields, two stored error-square fields, and two comparison failure fields. The reference uses two formal failure fields; each growth pair uses two formal failure fields, its old alternate error, its square, and its failure. The residual has its square and failure instead of its scaled square and product. Add the common scalar \(D'_g\). The exact build removes 29 variables and 29 rows per route.

The sparse tables and deterministic builder are included. Run node build.mjs (or --write). Exact build execution verified quadratic degree and full support, and the independent named monomial comparison checks all 52 Jones rows. The independent arithmetic fixture checks the parity, Boolean residue and harmonic selector cases, including zero tests and arbitrary odd depth, using integer valuation inequalities. Its finite checks supplement the proof and are not an independent proof of the inherited arithmetic premises. The quartic has exact degree four. No full repository CI run or source-certificate reduction is claimed in v139.
