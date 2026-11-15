# Obstructions to pole compression

The results below concern specified replacement predicates on the full prepared locus. Their hypotheses and counterfamilies do not give lower bounds for arbitrary defining polynomials. The positive shared-parameter local theorem is presented [separately](../../docs/pole_results_20261115_v41.md).

## No fixed rational coefficient repairs the conic-chain family

For a fixed \(c\in\mathbb Q\), consider five auxiliary rational coordinates satisfying

\[
P=p^2,\qquad e^2+bP=1,\qquad
D=1+(cb-1)P,\qquad z^2=bD.
\]

**For every fixed rational \(c\)**, this system fails locally on arbitrarily small positive inputs having square reduced denominator, which are squares in \(\mathbb Q_2\) and have \(2\)-adic valuation four. These are valid prepared inputs for the congruent-twist pole theorem.

Examples include

| Coefficient | Prepared counterfamily | Obstruction |
|:--|:--|:--|
| \(c=0\), which reduces to four auxiliaries | \(272/29^{2n}\), \(n\ge1\) | No \(\mathbb Q_{29}\)-point |
| \(c=1\) | \(528/31^{2n}\), \(n\ge1\) | No \(\mathbb Q_5\)-point |
| \(c=-9/25\) | \(272/441\) | No \(\mathbb Q_3\)-point |

The [classification proof](../papers/pole_parameters/conic_chain_obstruction_20261115_v41.tex) uses three local lemmas, quadratic characters, CRT, and primitive Pythagorean triples. Its [exact certificate](../../computation/pole_parameters/conic_chain_v41) requires no elliptic-rank computation or conjecture. This excludes the specified family on the full prepared locus, rather than all possible five-auxiliary pole predicates.

## An automatic first conic does not realize the second pole

The fully split rational contact formula

\[
e(\delta)=\frac{49\delta^2-1}{120\delta^3},\qquad
R(\delta)=1-e(\delta)^2
=\frac{\prod_{a\in\{3,5,8\}}(\delta^2-a^{-2})}{\delta^6}
\]

makes \(e^2+bp^2=1\) automatic when \(b=Rr^2\) and \(p=1/r\). This algebraic identity does not ensure the other two pole equations

\[
uv=e(1-b),\qquad u^2-v^2=bq^2.
\]

At \(\delta=7\), so \(e=20/343\), a rational conic gives a **dense family of prepared inputs in \((0,1)\)** for which the first equation holds and the remaining equations have no rational solution. Their existence would make

\[
15\,499\,155=3\cdot5\cdot7\cdot17\cdot19\cdot457
\]

a congruent number. Tunnell's unconditional necessary criterion excludes this: the coefficient of his original modular-form product is \(-256\). Independent ternary counts are \(5,120\) and \(10,752\), with \(2\cdot5,120\ne10,752\). A smaller counterfamily at \(e=9/41\) uses the noncongruent number \(17\).

The [proof and explicit parametrizations](../papers/pole_parameters/automatic_conic_obstruction_20261115_v41.tex) and [exact checker](../../computation/pole_parameters/automatic_conic_v41) use the necessary direction of Tunnell's theorem only. The examples do not assert that the current full detector system takes these values. A replacement restricted to a specially constructed detector locus would still need a separate completeness theorem.

## Verification

Run `python -B scripts/verify_v41.py` from the repository root. The conic-chain and automatic-conic certificates are rebuilt exactly, with no rank computation or conditional converse to Tunnell’s theorem. See the [primary bibliography](../../docs/literature_20261115.md).
