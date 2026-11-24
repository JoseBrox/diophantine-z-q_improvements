# Guarded linear targets and shared squares (v137)

**651 / 671 variables, 562 / 580 quadratic residuals.** This is a twelve-coordinate reduction of both v136 tables. It retains one scalar pole for the whole tuple and respectively two or three comparison poles. All 52 named Jones source residuals are unchanged. The hypotheses, including the full-domain five-contact height input H4.1, are those of [v136](../recursive_scalar_v136/README.md).

## Nonzero linear targets

Write \(X_i\) for the twelve source inputs. Put \(k_i=X_i\) for \(b,g\), and \(k_i=X_i+1\) for the others. In the recursive scalar chain of v136 replace \(X_i\) by \(k_i\). Store \(K_i=k_i^2\), using the existing square of \(g\), and use
\[
W_i=S_{i-1}K_i,\qquad K_iD_i=(1+W_i)^2,\qquad (Y_i-2504)D_i=S_{i-1}.
\]
These are quadratic equations. The first two exclude \(K_i=0\) (which would imply \(W_i=0\) and \(0=1\)). Inductively \(S_{i-1}>0\), so \(D_i\ne0\), and they yield precisely \(Y_i=2504+W_i/(1+W_i)^2\). Thus the recursive odd-support proof, forced 149 valuation, and all height estimates of v136 apply to the tuple \(k_i\), without any sign condition on a rational solution. The denominator guard costs no extra row or coordinate.

## Weighted comparison and height

In the private weighted chart of v133/v136 use scale \(k_i\) rather than the previous positive quadratic target. Nonzero scale is all that its algebraic chart requires. The weight \(K_i>0\) is the very square already stored by the scalar chain. The valuation argument of the weighted comparison (the two formal conditions with target \(k_i\)) is unchanged, and yields divisibility of the numerator of \(k_i-m_i\) by the square of each comparison radical, where \(m_i\) is the integral index difference. The aggregate still has positive weights \(K_i\); their heights are \(2h(k_i)\). The bound in v136 for the height of the old quadratic target was obtained from the bound on the input height; it therefore also bounds \(h(k_i)\) when the scalar chain is applied to the \(k_i\). The estimate on the nonzero numerator of \(k_i-m_i\) is at most \(2B\exp(h(k_i))\) for \(B\ge |m_i|,1\). The same weighted height absorption, growth-label comparison, and final Pell amplification of v136 imply \(k_i=m_i\). This proves \(X_i\in\mathbb Z\). There is no requirement that a solution of the rational system have positive \(k_i\).

For completeness choose the positive canonical source witnesses used in the preceding corrected Jones construction, including the positive short-power quotients. In particular \(b,g>0\) and all shifted targets are nonzero integers. The v136 preparation for any such tuple applies with the \(k_i\) in place of the original inputs, and the exact same weighted comparison charts give witnesses. The borrowed squares for the outer source remain \(g^2,b^4\). The parameters of v136 can be retained.

## Compilation and checks

The old comparison weight was the square of an affine expression in the input square, so it required an extra register. Here the shared square \(K_i\) is already present; the private chart is written using \(K_i^2\) as before. Delete twelve extra registers and their defining rows. No new scalar or comparison pole is introduced.

Run \`node build.mjs\` to check byte-for-byte replay of the two sparse tables, or \`node build.mjs --write\` to regenerate. The builder pins v128, verifies quadratic degrees and full variable support. Both tables were additionally replayed and every one of their 52 named Jones residuals compared term-for-term by variable name against v128. The sum of squared residuals is an integer-coefficient quartic after specializing the integer parameters.

This is an improvement conditional on the retained arithmetic inputs, not a proof of those inputs, an independent source-certificate reduction, or a full CI run.
