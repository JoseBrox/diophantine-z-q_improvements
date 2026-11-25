# v155: exact affine elimination and the recovered denominator-prime weight

**Conditional quartic bounds: 508 / 540 / 286 rational unknowns, with 457 / 487 / 235 quadratic residuals**, in general / specified / ordinary rational abc order. The respective numbers of independently certified integers remain 8 / 8 / 12. The arithmetic assumptions are exactly those of v150 and v152; no new global point-realization assumption is introduced.

## Exact algebraic reduction

If a row has the form \(v-E=0\), where \(E\) is affine in the other rational unknowns over the fixed coefficient ring, substitute \(E\) for \(v\) in every remaining row and delete the defining row. Degrees in the unknowns do not increase. Projection and the inverse map inserting \(v=E\) are inverse bijections on rational solutions, including all zero strata. In particular the sum of the squares of the new rows has the same existential projection; no inference from approximate numerical solutions is used.

In each v150 general compiler eliminate the seed using
\[
 G_{\rm scalar\_seed}=781189120\,C_{\rm parameter}^2.
\]
Then use the global gauge row to eliminate one actual contact weight:
\[
 G_{\rm contact0\_group0}=8G_c-\sum_{(j,i)\ne(0,0)}G_{\rm contact j\_group i}.
\]
The number of contacts is precisely the number in the parent compiler, two or three. This removes two unknowns and two rows: 510/459 becomes 508/457, and 542/489 becomes 540/487.

In v152 the normalized derivative sum is \(\sum_{i=0}^{11}r_i=12c\). Eliminate \(r_{11}=12c-\sum_{i=0}^{10}r_i\), i.e. n_r11, in every row, including its own derivative equation. This removes one unknown and one row from 287/236, giving 286/235. The 52 Jones rows are untouched. The substitutions can densify some quadrics; the objective here is number of unknowns, not coefficient sparsity.

## Recovering the denominator primes of M under abc

The argument of v152 section 2 may retain the simple contact primes dividing the denominator of the height root \(M\), as in the original v63 derivative construction. Use \(x=M^4\pm z\), \(y=2M^4-x\), and write the shifted contact factors on either side as \(x+d\), \(y+d'\) for fixed rational shifts. At a simple contact of group \(i\) on the larger-height side \(x\), outside the same fixed exceptional set, \(x\) is integral. If (v_p\(M\)<0), then (v_p(y)=4v_p\(M\)<0) (we exclude 2), so *every* factor on the other side has that valuation. In the logarithmic derivative, every other-side reciprocal has positive valuation. On the \(x\) side exactly one factor has valuation 1; all other factors are units. Thus the logarithmic derivative of \(F_i\) has valuation -1, as does the total logarithmic derivative. The other groups have integral logarithmic derivatives. Because \(r_i=-F_i'/24F_i\), \(c=\sum r_i/12\), and \(u=1/c\), we obtain \(v_p(u)=1\), and \(\omega_i=r_i/c\equiv12\pmod p\) with all other weights zero modulo \(p\). These are exactly the local requirements of v148 used in v152. The exclusion of primes dividing input denominators and nonzero labels is still made as before.

At integral primes of \(M\) retain the old opposite-multiple-root and contact-sum exclusions. Consequently no term (h\(M\)) for denominator primes of \(M\) is needed. The v63/v126 estimates give per group
\[
 (12-6-3\epsilon)\max(h(x),h(y))-(2+\epsilon)h(M)-O(1)
 \ge \frac{993}{100}h(M)-O(1),
\]
for \(\epsilon=1/100\), using \(x+y=2M^4\) and the usual height inequality. The strict height margin improves from \(893/100-8C\) to \(993/100-8C\), \(C=(1001/997)^4\). All other arguments, in particular canonical completeness, remain literally those of v152. This strengthening needs no new assumption and does not add coordinates.

## Reproducibility and scope

The exact substitutions are implemented in `eliminate.mjs`. Its general and abc functions accept the respective full parent tables. The general CLI `build_general.mjs` compiles the v150 source and applies the substitutions; the exported inner build routine alone still produces the parent table. The parameterized `build_abc.mjs` checks the v152 parent blob and reproduces the committed `abc_quadrics.json`. Every elimination requires a unit affine pivot, rejects eliminating certified input variables, and checks support, degrees and dimensions. The separate verifier compares residuals at arbitrary reconstructed assignments rather than merely comparing the numbers of rows.

All conclusions retain the parent qualifications: general coefficient choice is ineffective under the retained hypotheses, and the specified construction uses its existing recipe. The ordinary abc bound uses a sufficiently large positive odd coefficient. The candidate one-integer Pell mergers of v151–v154 are not used in these compilers. No unconditional assertion of undecidability, seven-integer source bound, or new unrestricted-degree variable bound follows.

Executed verification: ten general/specified fixture builds (five parameter sets each), 14,220 exact parent/child row comparisons on reconstructed assignments, 2,360 abc row comparisons, and an exact replay of the committed abc table. See `verification.json`. These are algebraic checks, not an independent verification of the retained arithmetic premises. Full repository CI was not run.
