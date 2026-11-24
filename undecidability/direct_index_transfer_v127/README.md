# Short direct-index logarithms and a whole-guard tagged determinant (v127)

**48 / 50 rational unknowns, unchanged; a strictly smaller rank-dependent degree majorant.** This integrates the shorter logarithm and two-layer character separator of the [supplied Sun audit](../../docs/audits/sun_september_20261124/sun_2609_transfer_supplied.tex), sections 4, 6 and 7, into the complete finite recipe of [v111](../direct_index_transfer_v111/README.md). We then improve the guard handling using an additional observation about the actual real preparation. All v111 arithmetic inputs are retained, including the full-family quantitative modular-height input for the specified route. The coefficient instance remains fixed, not an unknown. The ten-variable coding theorem is Sun, [arXiv:2609.01594v2](https://arxiv.org/abs/2609.01594v2), Theorem 1.1.

## 1. Replace the precision and its height ledger

Keep the eleven shift branches \(\Psi_s\), point roles \(A_i,U_i,H\), coefficient point \(A_0\), contact lists, and guarded ratios of v111. Let \(D,C\ge1\) be the maximum degree and integer coefficient one-norm of the eleven shifted source polynomials (including the variable \(M_0\)), as in that construction. Use
\[
 L=\lfloor D/2\rfloor+1,\quad C'=\lceil C^{1/L}\rceil,\quad
 r_0=\min\{r\ge1:4r-\lfloor\log_{p_0}(4r+1)\rfloor\ge L\},
 \quad
 \ell^{[L]}(z)=\sum_{r=0}^{r_0-1}
 \frac{(-1)^r\binom{2r}{r}D_E^r}{4r+1}z^{4r+1}.
\]
Take \(p_0=3\), or a larger lower bound for the retained primes. The integer test defining \(r_0\) uses integer powers only. Keep the same fixed exceptional set, including all needed denominator primes of the shorter polynomial, and let \(R_S\) be a computable upper bound on its prime product. The omitted relative terms have valuation at least \(L\) at every retained formal point: the bound \(4r-v_p(4r+1)\) is at least \(4r-\lfloor\log_{p_0}(4r+1)\rfloor\), nondecreasing in \(r\), and at least \(3r\). Thus \(r_0\le\lceil L/3\rceil\); if \(p_0>4\lceil L/4\rceil+1\), the exact cutoff is \(\lceil L/4\rceil\). No deeper reference points are assumed.

In every ratio of v111 use this shorter polynomial; use \(u^{L-1}\) in the comparison and target tests. Its local proof applies literally: the two relative-logarithm congruences are first multiplied by integer indices, and only then their difference forces the ratios congruent to the actual labels. For each nonzero residual \(N=\Psi_s(m)\) and every contact argument,
\[
 M_S(t)^L\mid N,\qquad
 M_S(t)\le C' B^{D/L},
 \quad B=\max(1,|m_0|,\ldots,|m_{10}|).
\]
Write \(b(n)\) for positive integer bit length. The retained modular estimate of v111, \(h(t)\le 2^{551} M(t)(199+\tfrac12\log M(t))^2\), gives
\[
 h(t)\le H B^2,\qquad
 H=2^{551} R_S C'(199+b(R_S)+b(C')+2L)^2.
\]
Indeed \(M(t)\le R_S M_S(t)\), \(2-D/L\ge 1/L\), and for \(x=\log B\ge0\), \(e^{-(2-D/L)x/2}(199+b(R_S)+b(C')+x)\le199+b(R_S)+b(C')+2L\). All constants are fixed before the instance. Use the two-contact exponent \(J>A_*(2H+1)\) with the same absorbed trace constant \(A_*\) of v111 (ineffective), or the three-contact effective \(J=2K_r(4H+3)\) of v111, \(r=11\). Subtraction of arguments gives the identical contradiction when \(N\ne0\). The old completeness proof works for the shorter ratios: at selected primes the exact logarithm ratios are the given labels, and the prescribed relative precision suffices. Include any new reference-function zeros in the finite avoidance before the slope and reference are chosen. These are finite since the truncated logarithm is a nonzero rational function and the relevant point maps are nonconstant.

The same construction handles a finite list of source equations, with individual \(D_j,C_j,L_j,H_j\), maximum logarithm precision and common \(H=\max_j H_j\) as in the supplied note. This changes no unknown count.

## 2. Finite point/pole tower and tagged separator

For each ordinary parameter pair \(h_i\in\mathbb Q(\sqrt2)\), adjoin the rank-four square-root algebra of v111, using the actual radicands \(A_i\pm B_i\sqrt2=h_i^4-D_E\) and its conjugate. Here the 21 pairs parametrize the ten label points, ten numerator points and reference point (do not confuse their radicand coefficients with the point roles of section 1). The point-prefix rank is \(N_0=4^{21}\). Make every field division by scalar denominator using the quadratic-field norm, and represent each rational radicand of the terminal pole by \(N_j/D_j\). Adjoin the independent monic root \(q_j^2=N_jD_j\), with recovery \(q_j/D_j\), as in v111. Let \(g\) be the product of every scalar denominator and explicit nonzero guard (including the \(D_j\)); all these are in the point prefix. Zero test and terminal root values remain allowed. Let \(c=2,3\) denote the number of poles, \(N=N_0 2^c\).

Use the two-layer separator \(\beta\) of section 7 of the supplied note **literally**, with \(p=7,\ \pi=3+\sqrt2,\ n=42,\ m=43,\ l=3\) for \(c=2\) and \(l=5\) for \(c=3\). The first-layer norms \(A_i^2-2B_i^2\) are nonzero at every rational specialization: a zero would imply \(h_i^2=\pm(3-\sqrt2)\) and \(\operatorname{Nm}(h_i)^2=7\). All terms of the rational scale in the supplied formula therefore have nonzero denominators. The proof by valuation tags separates the first-layer sign differences modulo \(m/2\) and the terminal sign differences modulo \(l/4\); the rational scaling makes the latter perturbations strictly smaller in 7-adic absolute value than any nonzero first-layer difference. The constant tag ensures nonzero separator values. This proves separation and nonvanishing on *all* geometric characters at rational specializations, even if terminal radicands are zero or some guards fail. The nilpotent diagonal argument in the note applies unchanged. We do not use a generic spectral-difference separator.

## 3. New: whole-prefix guards suffice for direct-index completeness

The supplied note gives a guarded extraction working with arbitrary excluded-character subsets. For the specific direct-index architecture we can avoid its coefficient-stratum product entirely. Replace that extraction by
\[
 G_*=\det M^{(0)}_g,\qquad
 F_s(Y)=\det(I_N-YG_* M_\beta)
\]
where \(M^{(0)}_g\) is multiplication by \(g\) on the point prefix. All matrices are polynomial over \(\mathbb Q\); clear fixed rational coefficient denominators. The new equation is more restrictive than the generic guarded extractor, so its completeness must be justified.

Soundness is immediate without any preparation assumption: if \(G_*=0\), the polynomial specializes to 1. Otherwise \(g\) is nonzero at every geometric character, since multiplication by \(g\) is invertible. A rational zero of \(F_s\) gives a rational nonzero separator value \(1/(YG_*)\) at some character by the diagonal formula. All Galois conjugates have that same value; separation forces the character to be rational. It recovers an actual guarded solution of section 1 and v111.

For completeness start from the integer witness of v111, with nonzero labels and \(A_i=[m_i]P,\ U_i=[hm_i]P\). At each real embedding all square-abscissa chart radicands at the actual tuple admit real nonzero roots. The geometric point-prefix characters are precisely the independent ordinate-sign choices at these two embeddings. Opposite or equal signs of the fixed \(A_i\) and \(U_i\) give affine differences \([\pm hm_i\pm m_i]P\); sign choices for \(H-P\) give \([\pm h-1]P\). More generally an ordinate-sign change negates the corresponding point without changing its abscissa. For fixed nonzero \(m_i\), all these maps of the preliminary reference point are nonconstant translations of nonzero multiplication maps. All denominators in the point formulas (including the secant denominator \(x(U_i)-x(A_i)\) or \(x(H)-x(P)\)), the nonzero abscissa and ordinate guards, and the nonzero reference logarithms can thus be secured at both embeddings and simultaneously for every sign choice by excluding finitely many reference fibers. The reference polynomial is nonzero since its linear term is \(z\). The zero/nonzero conditions on the fixed points hold because the labels are nonzero and \(P\) is nontorsion. At the selected initial real neighborhoods all these finitely many quantities are bounded, and the guarded ones are bounded away from zero. The same choice of initial multiple of \(64P\), finite-place neighborhoods and modulus \(M\) as in v111 may be used; the real restrictions are open and require no new prime supplier.

At real slope infinity every contact argument tends to infinity, \(u\to1\), and the common factor \((t+1)^{-2}\) in each raw test tends to zero. The boundedness just proved gives \(C_j\to0,\ D_{C_j}\to0,\ W\to1,\ V\to2\) for every sign choice, not just the actual one. All these finitely many denominator factors and required nonzero numerators are therefore nonzero for sufficiently large real slope; \(e\to112/10201\ne0\) and \(d=7u\to7\). The numerator of a raw comparison is **not** guarded nonzero. The terminal roots are also not guarded and do not occur in \(g\). The literal denominator-clearing rules multiply nonzero denominator factors, so their guards are nonzero on these same characters. The point-prefix character statement follows at the *actual* final rational specialization, because sign changes do not change the already fixed base coordinates. Consequently \(G_*\ne0\). The unchanged finite-place and selected-prime preparations of v111 apply to the chosen actual character and provide the BB pole roots; they do not need to hold at the other characters. This gives a rational character of the full algebra, hence a rational \(Y=1/(G_*\beta)\). Thus this more restrictive guard treatment still realizes every integer solution. It does not assert that every auxiliary zero of the generic extractor lifts.

## 4. Degree accounting and exact coefficient recipe

Use the precise computable majorant \(\delta\ge1\) from section 7 of the supplied note: maximum degrees of first-layer radicand components, terminal polynomial basis coefficients after monic denominator clearing, entries of the multiplication matrices of \(j_i,j_i'\), \(q_j\), and \(g\). Include the point-prefix entries for \(g\) as well (they are repeated in the full matrix). Take the maximum across all eleven shift branches. With the literal scale of the note, its separator matrix degree is at most
\[
 B_*\delta,\qquad B_*=[m+l(n+2)](8b+2cN_0)+\max(m,l),\quad b=21.
\]
The new guard norm has degree at most \(N_0\delta\); thus the single determinant has total degree at most
\[
 N[1+(N_0+B_*)\delta]\le N(1+N_0+B_*)\delta.
\]
In the two-pole case this is strictly below \(2^{96}\delta\), and in the three-pole case strictly below \(2^{98}\delta\), by the exact integer ledger. The eleven-branch product is strictly below \(11\cdot2^{96}\delta\) or \(11\cdot2^{98}\delta\). For the same coefficient/operator majorant the supplied general guarded extractor gave \(11\cdot2^{140}\delta\) and \(11\cdot2^{143}\delta\). No numerical evaluation of \(\delta\) for Sun's entire universal source is claimed here; these are explicit parametric degree bounds, not numeric degrees of expanded polynomials. The ranks are \(2^{44},2^{45}\). The coordinate count is still 42 point parameters + one slope + four or six pole parameters + one encoder = 48 or 50.

This is a complete finite prescription relative to the accepted integer polynomial \(Q\): for each branch compute the source shifts and coefficient point, form the shorter logarithm and the v111 rational expressions in the stated point basis, clear denominators by the v111 pair rules (guarding every introduced divisor), adjoin the terminal roots, form the supplied literal tagged separator and the whole-prefix guard determinant above, and multiply the eleven determinants after clearing fixed coefficient denominators. As in v111, the degree in the ordinary variables is uniform in the instance. The first route retains its ineffective sufficient \(J\); the three-contact route has the explicit algorithm for \(J\) in section 1. No new rational coordinate, arithmetic premise, or integer coding source is used.

Run the accompanying exact ledger verifier. It checks the rank and integer degree comparisons, not a full universal-source expansion, the retained infinite arithmetic inputs, or a new numerical value of \(\delta\).
