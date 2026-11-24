# Bhargava--Burungale native poles: quartics in 163 and 179 variables

**Current preferred general quartic implementations, 24 November 2026.**
The defining assertions are conditional on the same non-pole arithmetic,
height, comparison and prime-pattern suppliers as the v82 construction,
with pole completeness now supplied by Bhargava--Burungale
[arXiv:2611.16130v2, Lemma 2.2 and Theorem 2.3](https://arxiv.org/html/2611.16130v2).
There is no reliance on the original non-CM Theorem 5.3, Route K, CR3
or the repository's Proposition N in these new systems.

The full written proof of the substitution and of the required local
preparation is [here](../../papers/quartic/bb_native_quartics_20261124.tex).
The original v82 tables remain unmodified and available for exact comparison.

## Exact results

| Source | Total variables | Quadratic rows | Changed rows | Monomials | Degree | Content |
|---|---:|---:|---:|---:|---:|---:|
| `quartic163` | 163 | 137 | 9 | 2771 | 4 | 1 |
| `quartic179` | 179 | 151 | 12 | 3012 | 4 | 1 |

The three replaced rows in **each** pole block come from
\[
  9e^2-9+7bp^2=0,\quad
  9uv-9e+7eb=0,\quad
  9u^2-9v^2-7bq^2=0,
\]
equivalently \(e^2+dp^2=1,\ uv=e(1-d),\ u^2-v^2=dq^2\)
for \(d=7b/9\). All private square-register rows and all
non-pole rows are unchanged. The original 163 system has two
comparison poles and one scalar pole; the 179 system has three
comparison poles and one scalar pole. The original Laurent weights
are preserved, including the distinct ones in the comparison blocks.

**Prepared integer inputs.** The v82 proof supplies positive \(b\)
with square denominator, \(b\in\mathbb Q_2^{\times2}\), \(v_2(b)\ge4\),
and \(v_3(b)\ge2\). The original real intervals can be restricted to
\(0<b<1\), since the scalar input is already \(<0.245\) and
each comparison input approaches \((204/409)^2<1\).
At the additional fixed prime 7 the scalar input can be made integral
by the same arbitrary-depth formal recurrence; each comparison
input can be taken a 7-adic unit, as its limiting value is a unit.
Then \(d=7b/9\) has square denominator and lies in the 2-adic squareclass \(7\mathbb Q_2^{\times2}\),
with 2-adic valuation at least four, so BB gives rational
pole witnesses. The changed equations exclude negative odd
denominator valuations at **every** prime other than 7 for arbitrary
rational zeros, stronger than the previous fixed exceptional-prime
scope. The prime 7 already belongs to the fixed height-theorem
exceptional set, so no numerical height constant changes.

**Scope.** The independent finite checks certify algebraic identities,
quartic expansions and coefficient bounds; they do not prove BB's
analytic arithmetic or the other inherited elliptic/geometric/sieve
theorems. The resulting conditional integer-definition theorem is
proved in the accompanying TeX under exactly these retained inputs.

## Coefficients

The variable-163 family retains the parameter \(C=149^N\), \(N\ge1\).
Its exact height is
\[
 \max\{126616122944180358034867798936,\;149^{4N+2}\}.
\]
Only three expanded monomials depend on \(C\); their nonconstant
coefficients are unchanged from v82.
The fixed 179-variable member still has 748-bit height
\( (A_0 B_a^4)^2 \), where
\(A_0=645904574641049503754777843805872291231896003979\)
and \(B_a=14904184670611231\).

## Reproduction

No extra Python packages are needed. At the repository root run:

~~~sh
python -B computation/bb_native_quartic_20261124/build.py --verify
python -B computation/bb_native_quartic_20261124/check.py
~~~

To reproduce outside the tracked files:

~~~sh
python -B computation/bb_native_quartic_20261124/build.py --output /tmp/bb-native-quartics
~~~

\`build.py\` reads only the pinned old v82 ordinary quadratic tables,
changes the stated private-pole coefficients, and computes the whole
sum of squares. **Independently**, \`check.py\` reads the physical
Laurent rows and source weight maps, reconstructs the old and new
quadratics, checks all unchanged rows, and expands every ordered pair
of quadratic monomials; it does not import the producer. It also
checks an exact prepared rational witness and the coefficient formula.

A separate exact algebra reconstruction using the GitHub source data
was completed when the tables were committed. Both sizes passed:
137/151 quadratic rows, 9/12 changed rows, content one and degree
exactly four, full 2771/3012-term agreement, and unchanged heights.

The earlier 7/289 proposal is preserved in Git history and the
dated [migration checkpoint](../../docs/bb_quartic_native_migration_20261124.md).
The rejected 3/5 proposal was found to fail at the comparison
5-adic local condition; it is **not** a defining-polynomial input.
