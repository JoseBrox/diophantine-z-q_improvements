# Paired denominator height and a smaller contact exponent (v126)

**302 rational coordinates, 251 quadratic residuals.** Under precisely the retained premises of v125 (including ordinary rational abc), the same source-instance projection is obtained with contact center \(a=M^{12}+784\) rather than \(M^{32}+784\). All twelve certified integers, the single BB-native pole, the exact mean, the interpolation theorem and the full outer coding equations are retained. No unconditional arithmetic claim is made.

The v115 height tree pairs the twelve input leaves consecutively, leaving the trace leaf unpaired in the first layer. Its first six nodes are \(P_i=X_{2i-1}^4+X_{2i}^4\), \(1\le i\le6\). By the **projective** positive-power lemma in [v58](../../papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex), at \(\kappa=1001/1000\),
\[
 h(1:X_{2i-1}:X_{2i})\le(1001/997)h(P_i)+O(1).
\]
Apply it to absolute values. A zero input is covered by \(h(X^4)=4h(X)\), including the all-zero pair. Iterating the same lemma along the remaining path (depth at most three), with the old uniform positive-root-shift estimate \(h((M-B_{\rm abc})/2)\le h(M)+\log 2\), gives
\[
 h(1:X_{2i-1}:X_{2i})\le C h(M)+O(1),
 \quad C=(1001/997)^4.
\]
For a rational pair the logarithm of the least common multiple of its reduced denominators is at most this projective height. Consequently the logarithmic cost of discarding the union of denominator primes of all twelve inputs is at most \(6C h(M)+O(1)\), replacing the old \(12C h(M)+O(1)\). This bound is uniform in the fixed positive integer shift \(B_{\rm abc}\).

The v115/v118 contact argument applies verbatim for any fixed positive even exponent \(m\) in \(a=M^m+784\): set \(x=M^m-z,\ y=M^m+z\), use the same eight shifts per group, and discard the fixed exceptions, denominator primes of \(M\), the multiple-prime support on the other slot, and the multiple-prime support of the nonzero distinct pair sums evaluated at \(2M^m\). The [v63 power-multiple lemma](../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex) explicitly allows every fixed integer \(m\ge1\), with cost independent of \(m\) in its leading coefficient. The pair sums are positive and distinct after repetitions are merged, hence their values cannot vanish for positive \(M\). The derivative formulas differentiate in \(a\), not \(M\), so they do not depend on \(m\). With \(\epsilon=1/100\), the logarithm of the retained radical per group before excluding the twelve input denominators is at least
\[
 \left((8-6-3\epsilon)m/2-(3+\epsilon)\right)h(M)-O(1).
\]
Here \(h(x)+h(y)+\log 2\ge h(2M^m)\ge m h(M)-\log 2\); the separate cost \(h(M)\) for denominator primes of \(M\) has been retained. For \(m=12\) the coefficient is \(881/100\). After the pairwise exclusion and the v123 nonzero-label-prime exclusion, all v125 local implications still hold: at each retained prime \(X_i\equiv\pm m_i\bmod p\). If \(X_i\ne\pm m_i\), its signed numerator product then gives
\[
 (881/100-8C)h(M)
 \le \sum_j\log(1+|m_j|)+2\log(1+|m_i|)+O(1).
\]
The left coefficient is strictly positive (checked by exact integer arithmetic). The old positive-weight trace bound \(m_j^2\ll h(M)+1\) therefore bounds \(h(M)\) uniformly in \(B_{\rm abc}\). Since \(M\ge B_{\rm abc}\), sufficiently large fixed shifts give the same integrality conclusion.

For completeness, the center remains positive, exceeds every radius, and is a nonzero square in \(\mathbb Q_2\). If \(v_2(M)=0\), \(M^{12}+784\equiv1\bmod8\); if \(v_2(M)\ne0\), the two even valuations differ by at least eight, so the lower term is a square times a 2-adic unit congruent to 1 modulo 8. Thus all v115/v125 contact positions, fixed-place preparations and slope asymptotics remain valid with the new center, and the same simultaneous prime supplier, interpolated mean and native pole theorem construct the witnesses. The sufficient shift can increase and remains ineffective.

Keep \(M^2,M^4,M^8\); replace the two rows defining \(M^{16}\) and the center by \(a=M^8M^4+784\). All 250 other rows remain exactly the same by coordinate reindexing. This deletes one variable and one quadratic row; the checked table has full support. Run `node build.mjs` in this directory (or `--write` to regenerate). The checker verifies the exact coefficient table and positive rational margin; the above proof supplies the quantified height argument.
