# Fixed 22-variable polynomial via the quantitative Busy Beaver record bound

## Scope

The third comparison scale in [the selective construction](selective.md)
is needed for the **ordinary numerical** effective specialization, not
for integer completeness of the two-scale system. Here we specify a
single two-scale 22-variable defining polynomial relative to Busy
Beaver, using the quantitative record and compiler results already
retained in the project's [v86](../../quartic/bb163_fixed_20261120_v86.tex)
and [v87](../../quartic/bb163_compact_record_20261120_v87.tex) notes.

In addition to the original 22-variable arithmetic premises, retain
the explicit full-domain modular height estimates of the ordinary
numerically specified three-scale route, and the weighted-height
geometry, quantitative record count and register-to-binary compiler
lemmas of v86/v87 (from the pinned Version 22 manuscript of Elliot
Glazer's project). No abc or odd denominator mass hypothesis is
added. The arithmetic and compiler premises are not independently
reproved here. This is a fixed coefficient prescription **relative to
Busy Beaver**, not an evaluated ordinary integer coefficient table,
and does not replace the ordinary effective 24-variable record.

## 1. Actual bound on the trace-height constants

Use the halting-time Busy Beaver convention of v86: two symbols,
blank tape, two-way infinite tape, one tape, uncounted halting state,
counted halting transition, unused working states permitted. Define
\[
 \psi_*=\prod_{j=2}^{90}(3j+1),\qquad
 \kappa_*=27160+16032\psi_*,\qquad U=2^{\kappa_*},
\]
\[
 t_*=2^{20}(16\kappa_*+2^{186}+1)(2^{186}+3),\qquad
 H_*=\operatorname{BB}(t_*).
\]
These are exactly the v87 record parameters. The result used is not
merely eventual absence of bad witnesses. It is the actual last-record
bound from v86/v87:
\[
 H_*>U^3(R_f+3),\qquad
 S\le2U(h(r)+h(T))+U(R_f+2).
\]
Here the running record starts at U; S is the sum of squared
integer indices of four finite points relative to R0, allowing
the specified torsion strata, r>0 is the weighted graph parameter,
and \(T=7+\frac14\operatorname{Tr}(x(Q_1)+r x(Q_2)+x(Q_3)+x(Q_4))\).
The proof of this bound uses the finite ordinal of the last record
and its clocked program, whose state count is bounded explicitly
by t_* in v87. This avoids the invalid general inference from an
arbitrary finite computably enumerable set to a numerical BB index
discussed in v85.

For our four square-abscissa roots \(A=[n]P,S_0=[a]P,
T_0=[t]P,Z=[b]P\), take r=1. Since \(P=2R_0\), the corresponding
record index norm is \(S=4(n^2+a^2+t^2+b^2)\). Write
\[
 B=\max(1,|n|,|a|,|t|,|b|),\qquad
 T_{\rm raw}=\operatorname{Tr}(x(A)+x(S_0)+x(T_0)+x(Z)).
\]
The affine height inequality gives
\(h(7+T_{\rm raw}/4)\le h(T_{\rm raw})+\log32<
h(T_{\rm raw})+4\).
Consequently, using \(R_f\ge U>16\),
\[
 B^2\le 2U h(T_{\rm raw})+U(R_f+10)
       \le H_*(h(T_{\rm raw})+1).
\]
In particular H_* dominates the needed trace-height constants.
It also exceeds \(1024\), \(2^{342+3q}\), \(2^{q+600}\) and \(q+201\)
for \(q=4000000\): the record clock bound gives \(H_*>U^4\)
and \(\kappa_*>342+3q\), the latter a direct integer comparison.

## 2. Fixed coefficient prescription

Keep the **two-scale** 22-variable selective system, with no third
contact, third pole, or new quantified coordinate. The input map,
scalar function, two sets of twenty contacts, four root labels,
four auxiliary points, marker menus and finite-algebra compiler
are all exactly as in selective.md.

Set the fixed coefficient exponent to
\[
 \boxed{L=3+171033184(H_*+1)^2}.
\]
It is positive, odd, and in the required progression
\(L\equiv3\bmod171033184\). The preceding inequality for H_*
is a proved input to the following threshold argument, not an
assumed rate of BB growth.

## 3. Soundness with the new fixed coefficient

For the two selective families the same divisibility conclusions hold:
\[
 67^{2L+1}M_\beta^3\mid c,\qquad c=|a-1|>0,
 \qquad M_{i,G}^3\mid\Delta c,\quad M_{i,I}\mid Nc
\]
for nonzero residuals, where \(N=\operatorname{num}(\tau-n)\)
and \(\Delta=t^2-a(a-2)tb+(a-2)^2b^2-1\).
The fixed exception product bound of selective.md applies also
with the third scale absent. In particular for either family
\[
 h(\beta)\le K_\beta M_\beta^3,\quad
 h(t_i)\le K M_{i,g}(A_0+\log M_{i,g})^2,
\]
where \(K_\beta=2^{342+3q}\), \(K=2^{q+600}\), \(A_0=q+201\).
The notation t_i here refers to contact arguments, not the Lucas label t.
Set \(H=H_*\). Each of these three constants is at most H.

The coefficient exponent forces
\[
 c\ge 67^{2L+1}>2^{H^2},\qquad
 h(\beta)\le Hc/67^{2L+1}<c/120,\qquad B\ge c-1.
\]
For example \(67^{2L+1}>2^{6(2L+1)}\) and the displayed
formula for L gives \(6(2L+1)>H^2\); for H>=1024 this
also dominates 120H and 40H. The original scalar estimate is
\[
 h(\rho)\le4h(\beta)+2L\log67+133
           \le4h(\beta)+\log c+133 .
\]

The second scale satisfies \(\alpha_1=t_1/t_0=1+\rho T_{\rm raw}^2\)
on the guarded locus, where in this equality t_0,t_1 are contact
arguments. Therefore \(2h(T_{\rm raw})\le
h(t_0)+h(t_1)+h(\rho)+\log2\), by the elementary product,
translation and power inequalities. The height constant from
Section 1 gives the coarser but convenient bound
\[
 B^2\le H\{h(t_0)+h(t_1)+h(\rho)+2\}.
\]
If \(Z\) is the nonzero residual \(\Delta\) or \(N\), use its
corresponding family in both contact height estimates, writing
\(j=3\) or \(1\), respectively. Since \(M_{i,g}^j\mid Zc\), this
implies
\[
 B^2\le 2H^2|Zc|^{1/j}(H+\log |Zc|)^2
        +H(c/30+\log c+135).
\]
Here the height estimate does not identify the trace with a
single field component or need the third comparison scale.
For c>=1000, \(\log c\le c/10\), \(135\le c/5\); and
\(c\ge40H\), \(B\ge c-1\ge c/2\). Thus the last term is
strictly less than \(B^2/2\). In either nonzero-residual case,
\[
 B^2<4H^2|Zc|^{1/j}(H+\log |Zc|)^2. \tag{1}
\]

If \(\Delta\ne0\), the original integer estimate
\(|\Delta c|\le10 B^5\) gives from (1)
\[
 B^{1/3}<12H^2(H+3+5\log B)^2 .
\]
The function \(e^{s/3}/(H+3+5s)^2\) is strictly increasing for
\(s\ge0,\ H\ge1024\). We have \(B\ge2^H\). At \(B=2^H\)
the proposed inequality already fails, because
\(H+3+5H\log2\le7H\) and
\(2^{H/3}>588 H^4\). The latter follows for all integer
\(H\ge1024\) from \(2^{1024}>588^3 1024^{12}\) and
\(2(1024/1025)^{12}>1\). Thus \(\Delta=0\).

If \(N\ne0\), write \(s=\log B\), \(u=h(\beta)+\log c\).
The elementary numerator bound \(|Nc|\le2Bc e^{h(\beta)}\)
and (1) give
\[
 s<\log(8H^2)+u+2\log(H+1+s+u).
\]
By \(\log(1+x)\le x\) for x>=0, the right side is at most
\(\log(8H^2)+u+2\log(H+1)+2(s+u)/(H+1)\).
Rearranging, for H>=1024,
\[
 s<2u+10H\le c/60+c/5+c/4<c/2 .
\]
For the middle inequality use \(h(\beta)<c/120\),
\(\log c\le c/10\), \(c\ge40H\). For the constant in the
first inequality, the coefficient of u after rearrangement
is \((H+3)/(H-1)<2\) and the remaining constant is
at most \(2(\log(8H^2)+2\log(H+1))<10H\).
But the original integral Lucas growth conclusion, now
applicable because \(\Delta=0\), is \(\log B>c-4\),
contradicting \(s<c/2\) for c>=1000.

Consequently \(N=0\), so \(X^2+1=n\in\mathbb Z\) and X is
integral. The input substitution reflects integrality of X0.

## 4. Completeness, count and limitations

Integer completeness of the selective two-scale construction
holds throughout the coefficient progression; in particular
it holds at this L. Nothing in the arithmetic witness preparation
or finite menu choices depends on effectiveness of the exponent
bound. The identical determinant prescription has 22 total
rational coordinates: input, 16 point components, one slope,
three shared pole coordinates, one finite-algebra encoder.

Under the stated inherited premises the result is therefore a
single 22-variable polynomial with a coefficient prescription
relative to the fixed Busy Beaver index \(t_*<2^{826}\). The
state-count lemma used here is inherited from v86/v87, including
its specific weighted-graph record argument; we have not computed
the value of BB(t_*), or a new numerical bound on degree or
coefficient height. In particular this is not a computable
ordinary numerical specialization. The ordinary numerical
24-variable construction at L=171033187 remains a separate
achievement. This result avoids its third pole by avoiding its
third scale, not by solving simultaneous sharing of three actual
pole inputs.
