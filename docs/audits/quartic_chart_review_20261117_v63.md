# Independent quartic chart pass — 17 November 2026

**No complete reduction below 195 or 71 variables was obtained.** The current counts must remain unchanged. This pass inspected the complete 71-coordinate point, helper, contact and terminal-pole equations and the 195-coordinate specification; it did not repeat the already recorded Laurent-weight searches. The latter searches were reported by the independent arithmetic auditor as infeasible in their stated search class, not as a general lower bound.

## A four-coordinate algebraic saving that does not inherit completeness

The tempting replacement of the varying-difference chart consists of two independent scaled point charts

\[
 a_U\delta_U=D\beta^4,\quad a_U-s^2-\delta_U=0,
 \qquad
 a_V\delta_V=D\beta^4,\quad a_V-t^2-\delta_V=0.
\]

For \(\beta\ne0\), these cover exactly all finite nonzero-abscissa points \(U,V\) on \(y^2=x^3-Dx\), including every allowed zero ordinate. Their meanings are

\[
 a_U=\beta^2x(U),\quad s=\beta y(U)/x(U),\quad
 \delta_U=D\beta^2/x(U),
\]

and similarly for \(V\). The reciprocal helpers are now affine:
\(F=\delta_U/D\), \(G=\delta_V/D\). Therefore the product rows can be written directly as

\[
 Dv_HJ=u_H\delta_U,\qquad Dv_HK=w_H\delta_V.
\]

This removes the four rational coordinates for \(F,G\) while retaining quadratic rows, using the already retained fourth-power coordinate for the displayed $\beta^4$. The positive weighted trace theorem would provide height soundness for the affine carrier

\[
 T_+=\operatorname{Tr}(a_U+a_V)
     =\beta^2\operatorname{Tr}(x(U)+x(V)).
\]

But the current prime preparation cannot be transferred: its gap must be fixed before the reference index is selected. More strongly, its intended multiplication witnesses are bounded in the integer input under this replacement.

### Precise obstruction to the inherited witness family

Retain the existing contact and pole inputs, ordinary abc, and the positive weighted trace theorem. Consider intended witnesses

\[
 \beta=n\ne0,\quad H=[h]R_0,\quad
 U=[nh]R_0,\quad V=[n(h-1)]R_0,\qquad h\notin\{0,1\},
\]

with new gap \(g=B+n^8+T_+^2\). Then \(|n|\) is bounded for every fixed choice of the construction data.

Indeed, let \(M_j\) be the radical of consumed contact primes in block \(j\). At every such good prime not dividing \(n\), the inverse-parameter extraction places \(H\) in the formal group at at least one place of \(K=\mathbb Q(\sqrt2)\) above that prime. At a good place its negative abscissa valuation is at most \(-2\). By the definition of normalized absolute finite height,

\[
 \log M_j\le h_{\mathrm{fin}}(x(H))+\log|n|+O(1)
             \le 2h^2\widehat h(R_0)+\log|n|+O(1).
\]

The \(\log|n|\) term covers the omitted primes dividing the input; all other omitted primes are fixed. The unchanged eight-contact estimate gives

\[
 h(g)\le\frac27(\log M_0+\log M_1)+O(1)
       \le C_1h^2+C_2\log|n|+C_3.
\]

The existing mixed-power estimate bounds \(h(T_+)\) by a fixed multiple of \(h(g)+1\). The positive weighted trace theorem, with both weights \(n^2\), gives

\[
 n^2\max\{h^2,(h-1)^2\}
       \le C_4\bigl(h(T_+)+\log|n|\bigr)+C_5.
\]

Since \(h^2\ge1\), division yields
\(n^2\le C_6+C_7\log|n|\), which bounds \(|n|\).

Thus the algebraic saving is **not a complete quartic improvement**. This argument excludes the inherited multiplication-witness family. It does not exclude every possible witness of the altered equations, and it does not prove that a different prime preparation could never complete that candidate.

## Terminal rows and next target

The current 71-variable native pole subsystem already permits all zero boundary values of its auxiliary coordinates:

\[
 e^2+bp_2=1,\quad p_2=p^2,\quad
 uv=e(1-b),\quad u^2-v^2=bq_2,\quad q_2=q^2.
\]

There is no separate terminal nonzero guard to delete. Direct substitution of \(p^2\) or \(q^2\) makes a residual cubic and its sum-of-squares contribution sextic; a variable reduction therefore needs another quadratic presentation, rather than simply omitting the square helper. Imposing a special conic parameter would require a new completeness theorem and is not licensed by the retained simultaneous-twist input. The known fixed-parameter obstructions remain relevant.

**Best next algebraic target:** reduce the current eight-field-coordinate pair-plus-reciprocal chart to seven field coordinates while keeping the scaled difference abscissa \(\beta^2x(U-V)\) affine, both inverse-parameter outputs available linearly, and both reciprocal products available by quadrics. The difference carrier is fixed on intended witnesses before prime selection, which is exactly what the rejected positive-sum replacement loses. Any proposed chart must cover the allowed tangencies and nonzero-abscissa two-torsion differences, and its unit conditions must follow from its equations for nonzero input. No existence or lower-bound claim is made for this seven-coordinate target.

## Reproduction and sources

- `computation/elliptic_charts/scaled_single_point_audit_v63/check.py` verifies the two universal polynomial identities used for the independent single-point charts and the exact unchanged absorption constant. It is an algebraic check, not a completeness certificate.
- Current complete source: `papers/quartic_existence/quartic_abc71_20261116_v49.tex`, Sections 2–5 and 7, with the exact table in `computation/quartic/abc71_v49`.
- Positive weighted trace: `papers/trace_heights/weighted_trace_20261114_v27.tex`, Theorem 1.1.
- Prior support obstruction: `negative_results/papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex`; the proof above gives the corresponding quadratic-field, two-contact version for this particular proposed edit.
- Native pole scope: `papers/pole_parameters/congruent_twist_poles_20261114_v27.tex`.
- The 195-coordinate table and its input-preserving guards remain as specified in `computation/quartic/affine_laurent195_v45`.
