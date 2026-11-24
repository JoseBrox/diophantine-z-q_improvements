# Checkpoint: a direct eight-multiplier replacement for Route K's pole input

Date: 24 November 2026. Status: **proved elementary reduction, conditional on the rational-solubility conclusion of Bhargava–Burungale, Lemma 2.2**, arXiv:2611.16130v2, https://arxiv.org/html/2611.16130v2. This is an additive research note, not a change to any existing polynomial or Lean kernel claim.

## Exact statement

Put
\[
\mathcal M=\{1,2,3,5,6,10,15,30\},\qquad
F(c;s,t,z)=(1-c)(s^4-c^2)(t^4-c^2)-z^2.
\]
For a rational \(B\ne0\), let \(\Psi(B)\) mean that **some** \(m\in\mathcal M\) and \(s,t,z\in\mathbb Q\) satisfy \(F(B/m;s,t,z)=0\).

**Proposition 1 (stronger soundness).** If \(\Psi(B)\), then for every prime \(p\notin\{2,3,5\}\), \(v_p(B)\) is not negative and odd.

**Proposition 2 (broader completeness).** If \(B\in\mathbb Q\) has square reduced denominator, \(0<B<1\), and \(v_2(B)\ge4\), and \(v_p(B)\ge1\) at \(p=3,5\), then \(\Psi(B)\), provided the converse of Bhargava–Burungale Lemma 2.2 holds. The additional local conditions \(v_p(B)\ge1\) for \(p=3,5\) are required to ensure that division by \(m\) preserves square denominators. No conditions at 7 or 13 are needed.

## Proof

If \(v_p(c)=-r<0\) with \(r\) odd, then \(v_p(1-c)=-r\) is odd. For any rational \(s\), \(4v_p(s)\) is divisible by four (or infinite when \(s=0\)), whereas \(v_p(c^2)=-2r\equiv2\pmod4\). Consequently \(v_p(s^4-c^2)=\min\{4v_p(s),-2r\}\) is a **finite even** integer. The same holds for \(t\). The valuation of the left side of \(F=0\) is therefore odd and cannot equal \(v_p(z^2)\) (including \(z=0\)). If \(p\nmid m\), \(v_p(B/m)=v_p(B)\); all prime factors of all \(m\in\mathcal M\) lie in \(\{2,3,5\}\). This proves Proposition 1 unconditionally.

For Proposition 2, write \(B=bq^2\) with \(b>0\) squarefree and \(q\in\mathbb Q^\times\). Write \(b=2^f b_0\), where \(f\in\{0,1\}\) and \(b_0\) is odd. Choose the unique \(m_0\in\{1,3,5,15\}\) such that \(m_0b_0\equiv7\pmod8\), and set \(m=2^f m_0\in\mathcal M\). Since \(m_0^{-1}\equiv m_0\pmod8\) and \(2^f/m=1/m_0\),
\[
B/m=(b_0/m_0)q^2,
\qquad\operatorname{sqf}(B/m)\equiv b_0m_0\equiv7\pmod8.
\]
Furthermore \(v_2(B/m)=v_2(B)-f\ge3\), and \(0<B/m<1\). At each odd \(p\mid m\), the assumption \(v_p(B)\ge1\) gives \(v_p(B/m)\ge0\). At \(2\), the valuation is at least 3. At every other prime, \(v_p(B/m)=v_p(B)\), whose negative valuations are even by hypothesis. Hence \(c=B/m\) really has square reduced denominator, and Lemma 2.2 applies. This proves Proposition 2 conditional only on the cited converse. The reduction is fully elementary; it does not assume Route K, CR3, Proposition N, or any general 2-converse.

**Polynomial form:** multiplying \(F(B/m;s,t,z)=0\) by \(m^5\) gives the integer-coefficient equation
\[
(m-B)(m^2s^4-B^2)(m^2t^4-B^2)-m^5z^2=0.
\]
For each fixed \(m\), it has total degree nine. The eight-way disjunction is algebraically expressible. The **degree-seven** birational form in the next section is preferable. This does **not** by itself give a quartic or a smaller global variable count; compilation and the consumer's exact scale need separate checks.

## A smaller four-variable, degree-56 polynomial

The project's already-reviewed v88 paper `papers/arithmetic_dependencies/finite_support_twists_20261123_v88.tex`, Proposition on the degree-seven pole equation, gives
\[
(s^2+c)(t^2-c)=(1-c)r^2(s^2-c)(t^2+c).
\]
For every nonzero rational \(c\), this implies square denominator. Conversely every \(c\) satisfying the preparation in Proposition 2 has a solution. The second implication is obtained from Bhargava–Burungale Lemma 2.2 by the explicitly proved rational substitution in the v88 paper, with all denominators nonzero because \(\operatorname{sqf}(c)\equiv7\pmod8\).

For each **fixed integer** \(m\in\mathcal M\), clear denominators after setting \(c=B/m\):
\[
H_m(B,s,t,r)=m(ms^2+B)(mt^2-B)
-(m-B)r^2(ms^2-B)(mt^2+B).
\]
Define the single, explicit integer polynomial
\[
\boxed{\mathscr P(B,s,t,r)=\prod_{m\in\{1,2,3,5,6,10,15,30\}}H_m(B,s,t,r).}
\]
It has **four total variables** (one rational input and **three** rational witnesses), and **total degree exactly 56**, since each factor has degree seven and its degree-seven highest homogeneous component is nonzero. Over \(\mathbb Q\), \(\mathscr P=0\) if and only if one of the eight factors vanishes. Proposition 1's soundness proof applies to each such factor, by the independent valuation proof in v88; Proposition 2's multiplier selection supplies a factor having a rational zero. Consequently this *single* polynomial has precisely the two one-sided properties required of a pole detector:
\[
\begin{aligned}
&B\neq0,\ \mathscr P(B,s,t,r)=0
\ \Longrightarrow\ 
 v_p(B)\notin\{-1,-3,-5,\dots\}\quad(p\notin\{2,3,5\}),\\
&0<B<1,\ \text{square denominator},\ v_2(B)\ge4,\ 
 v_3(B),v_5(B)\ge1
\ \Longrightarrow\ \exists s,t,r\in\mathbb Q:\ \mathscr P(B,s,t,r)=0.
\end{aligned}
\]

**Scope:** This gives an improved *existential pole predicate*, not a quartic construction in four variables. Its degree-56 polynomial is a direct factored specification, with no additional existential multiplier or Boolean variables. Changing a source template to use it requires the complete global compiler/guard and caller proof. The v88 project paper's degree-seven identity, not a fresh theorem of Bhargava–Burungale, supplies this extra degree reduction.

## Integration boundaries

1. The eight multipliers are minimal among fixed squareclass corrections covering all eight classes of \(\mathbb Q_2^\times/\mathbb Q_2^{\times2}\): one multiplier can correct only one input class. The choice \(\{1,3,5,15\}\) generates the four odd classes using only primes 3 and 5. This optimality is only for the multiplier menu, not a lower bound for Diophantine variables.\n\n2. The original Route K pole polynomial is **different**. This is a replacement for its *function* (soundness/completeness), not a proof of its identical zero set.
3. The local integrality assumptions at 3 and 5 cannot simply be dropped: for example, if a selected multiplier is divisible by 3 and \(v_3(B)=-2\), then \(v_3(B/m)=-3\). The original proof allows input \(B\) as prepared by the old callers. Those inputs satisfy the above broader completeness hypotheses; a compiler refactor must separately preserve every other denominator, guard, and degree.
4. This note is an independent strengthening of the multiplier menu, **not** an independent proof of Bhargava–Burungale Theorem 2.3. Their finite star construction and TYZ genus-point input are audited in the existing v88 manuscripts and should stay cited.
5. The result can be used as a new no-CR3 arithmetic interface in the project. Do not remove the original certified Route K implementation until a replacement Lean assembly builds and the final polynomial/variable count is independently checked.
