# Checkpoint: native-pole replacement in the 163- and 179-variable quartics

> **Historical checkpoint, superseded on 24 November 2026.** This records the initial valid but less economical scaling (d=7b/17^2). The active, independently reconstructed systems use the smaller scaling (d=7b/9), after strengthening the integer-witness real preparation from (b<17) to (b<1); see [the complete proof](../papers/quartic/bb_native_quartics_20261124.tex), [current tables and checks](../computation/bb_native_quartic_20261124/README.md), and [current results](results_20261124_bb_native.md). An intervening proposal (d=3b/5) was **rejected**: the comparison inputs are (5)-adic units, and division by (5) creates a negative odd valuation. The active (7b/9) construction has no such obstruction. This checkpoint does **not** define the current polynomial.

**24 November 2026.** Working checkpoint; retain all historical v82 coefficient files.

## Arithmetic replacement

For every rational input \(b\) in the original native-pole completeness range, the v82 source provides
\[
0<b<17,\quad b\text{ has square reduced denominator},\quad
b\in\mathbb Q_2^{\times2},\quad v_2(b)\ge4,
\]
and additional local square/preparation conditions at \(3,17\).
The old native predicate has rational variables \(e,p,u,v,q\) satisfying
\[
3e^2-34e-289+17bp^2=0,\quad
e(17-b)=17uv,\quad
u^2+34uv-867v^2=17bq^2.
\]

Enlarge the **finite list of integer-witness preparation primes** by \(7\), and require \(v_7(b)\ge0\) there. This is an extra construction obligation, not a condition on arbitrary rational zeros. The old ordered completeness proof explicitly allows arbitrary finite preparation sets and exact positive depths; its scalar proof chooses \(v_p(\tau)\) sufficiently large at every prepared prime, while comparison-input preparation is preserved in the final synchronized neighborhoods. An independent review of this extra choice is still required before replacing the old published quartic theorem unconditionally.

Set
\[
d=\frac{7b}{17^2}.
\]
Then \(0<d<7/17<1\), \(d\in7\mathbb Q_2^{\times2}\), \(v_2(d)\ge4\), and \(d\) has square reduced denominator: at \(7\) its valuation is \(1+v_7(b)\ge1\), at \(17\) it differs from that of \(b\) by \(-2\), and elsewhere by zero. Bhargava--Burungale arXiv:2611.16130v2, Lemma 2.2 (as established via their Theorem 2.3) and the project's native-pole transfer in \`papers/pole_parameters/intrinsic_pole_20261117_v56.tex\` give the rational points needed for
\[
e^2+dp^2=1,\qquad uv=e(1-d),\qquad u^2-v^2=dq^2.
\]
At fixed \(d\), an elementary 2-adic/valuation argument shows that this native system forbids every negative odd denominator valuation of \(d\): the first equation forces \(e\) to be a unit, the last forces \(v_p(u)=v_p(v)\), but the middle has odd valuation. Therefore the new \(b\)-predicate is sound outside the prime \(7\); at primes other than \(7\) multiplication by \(7/17^2\) changes \(v_p(b)\) by an even integer (or zero). Any consumed-prime argument must exclude \(7\), which is already a fixed small prime and can be put in the source's exclusion set.

## Exact five-row replacement

The v82 physical systems contain two detector pole blocks in the 163-variable quartic, three in the 179-variable quartic, and one scalar block in each. Each has two square-register rows and three native conic rows. No other row consumes the five private pole witnesses or their two private square registers. Keep both square-register rows, and replace only the other three.

At the *unscaled physical level*, replace
\[
3e^2-34e-289+17bp^2=0,\quad e(17-b)-17uv=0,\quad
u^2+34uv-867v^2-17bq^2=0
\]
by the three quadrics
\[
289e^2-289+7bp^2=0,\quad
289uv-289e+7eb=0,\quad
289u^2-289v^2-7bq^2=0.
\]
(The second sign can be reversed without changing its zero set.) The source uses different Laurent weights for the detector blocks. The new equations must be transported with **the same nonzero Laurent monomial factors** as the three old rows, term by term; the scalar's corresponding homogeneous rows are immediate.

The rescaling uses \(d=7b/289\), not a hypothetical rational point on the original non-CM curves. Thus it removes the arithmetic dependence on Theorem 5.3/Route K *for the modified pole blocks* rather than proving Theorem 5.3. All other v82 elliptic, trace, geometry, recurrence, contact-height and prime-pattern premises remain unchanged.

## Reproduction obligations

- Rebuild the 163 and 179 quadratic row tables by this precise substitution, preserving the source coordinate maps; independently reconstruct and expand their sums of squares.
- Check the new integer content, exact polynomial degree, coordinate count, and coefficient height. The old exact heights and monomial counts **must not be copied** after the row replacement.
- Verify both directions of the physical Laurent equivalence and every zero branch.
- Prove the newly added \(7\)-adic integer-witness preparation is compatible with the ordered source's real neighborhoods and finite congruences, for the scalar and all detector inputs. Do not silently replace it by a bare assertion of local solubility.
- Keep the original v82 tables unchanged as reproducible history.

The already-complete v88 few-variable routes explicitly use Bhargava--Burungale. The general quartic replacement above is the remaining nontrivial current-family migration; it is a checkpoint until every bullet closes.
