# Checkpoint: a direct eight-multiplier replacement for Route K's pole input

Date: 24 November 2026. Status: **proved elementary reduction, conditional on the rational-solubility conclusion of Bhargava–Burungale, Lemma 2.2**, arXiv:2611.16130v2, https://arxiv.org/html/2611.16130v2. This is an additive research note, not a change to any existing polynomial or Lean kernel claim.

## Exact statement

Put
\[
\mathcal M=\{1,2,3,5,6,7,10,14\},\qquad
F(c;s,t,z)=(1-c)(s^4-c^2)(t^4-c^2)-z^2.
\]
For a rational \(B\ne0\), let \(\Psi(B)\) mean that **some** \(m\in\mathcal M\) and \(s,t,z\in\mathbb Q\) satisfy \(F(B/m;s,t,z)=0\).

**Proposition 1 (stronger soundness).** If \(\Psi(B)\), then for every prime \(p\notin\{2,3,5,7\}\), \(v_p(B)\) is not negative and odd.

**Proposition 2 (broader completeness).** If \(B\in\mathbb Q\) has square reduced denominator, \(0<B<1\), and \(v_2(B)\ge4\), then \(\Psi(B)\), provided the converse of Bhargava–Burungale Lemma 2.2 holds. No preparation at 3, 5, 7, or 13 is necessary for this direction.

## Proof

If \(v_p(c)=-r<0\) with \(r\) odd, then \(v_p(1-c)=-r\) is odd. For any rational \(s\), \(4v_p(s)\) is divisible by four (or infinite when \(s=0\)), whereas \(v_p(c^2)=-2r\equiv2\pmod4\). Consequently \(v_p(s^4-c^2)=\min\{4v_p(s),-2r\}\) is a **finite even** integer. The same holds for \(t\). The valuation of the left side of \(F=0\) is therefore odd and cannot equal \(v_p(z^2)\) (including \(z=0\)). If \(p\nmid m\), \(v_p(B/m)=v_p(B)\); all prime factors of all \(m\in\mathcal M\) lie in \(\{2,3,5,7\}\). This proves Proposition 1 unconditionally.

For Proposition 2, write \(B=bq^2\) with \(b>0\) squarefree and \(q\in\mathbb Q^\times\). Write \(b=2^f b_0\), where \(f\in\{0,1\}\) and \(b_0\) is odd. Choose the unique \(m_0\in\{1,3,5,7\}\) such that \(m_0b_0\equiv7\pmod8\), and set \(m=2^f m_0\in\mathcal M\). Since \(m_0^{-1}\equiv m_0\pmod8\) and \(2^f/m=1/m_0\),
\[
B/m=(b_0/m_0)q^2,
\qquad\operatorname{sqf}(B/m)\equiv b_0m_0\equiv7\pmod8.
\]
Furthermore \(v_2(B/m)=v_2(B)-f\ge3\), and \(0<B/m<1\). A square denominator is preserved by rational-square scaling, so Lemma 2.2 applies to \(c=B/m\). This proves Proposition 2 conditional only on the cited converse. The reduction is fully elementary; it does not assume Route K, CR3, Proposition N, or any general 2-converse.

**Polynomial form:** multiplying \(F(B/m;s,t,z)=0\) by \(m^5\) gives the integer-coefficient equation
\[
(m-B)(m^2s^4-B^2)(m^2t^4-B^2)-m^5z^2=0.
\]
For each fixed \(m\), it has total degree nine. The eight-way disjunction is algebraically expressible. This does **not** by itself give a quartic or a smaller global variable count; compilation and the consumer's exact scale need separate checks.

## Integration boundaries

1. The original Route K pole polynomial is **different**. This is a replacement for its *function* (soundness/completeness), not a proof of its identical zero set.
2. The original proof allows input \(B\) as prepared by the old callers. Those inputs satisfy the above broader completeness hypotheses; a compiler refactor must separately preserve every other denominator, guard, and degree.
3. This note is an independent strengthening of the multiplier menu, **not** an independent proof of Bhargava–Burungale Theorem 2.3. Their finite star construction and TYZ genus-point input are audited in the existing v88 manuscripts and should stay cited.
4. The result can be used as a new no-CR3 arithmetic interface in the project. Do not remove the original certified Route K implementation until a replacement Lean assembly builds and the final polynomial/variable count is independently checked.
