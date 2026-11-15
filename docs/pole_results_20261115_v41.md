# Pole parameters: local solubility and compression obstructions

The construction records remain **25** total variables, **196** for a quartic, **13** under the stated weak-abc hypotheses, and **78** for a quartic under ordinary rational abc. The results below prove arithmetic statements about possible reductions; they do not specify a smaller defining polynomial.

## Every rational shared parameter is locally admissible

Let a prepared input satisfy

\[
0<b<17,\qquad b\in\mathbb Q_2^{\times2}\cap\mathbb Q_3^{\times2}
\cap\mathbb Q_{17}^{\times2},\qquad
v_2(b)\ge3,\quad v_3(b)\ge1,\quad v_{17}(b)\ge2,
\]

with square reduced denominator. Write \(b=dt^2\), set \(D=17d\), \(C=17(17-b)\), and put

\[
e_\tau=\frac{\tau^2-D}{\tau^2+3D}.
\]

For **every rational \(\tau\)**, the curve

\[
q^2=D(s^2-e_\tau C)(s^2+3e_\tau C)
\]

has points over every completion of \(\mathbb Q\). Each local curve has infinitely many affine points with nonzero ordinate, so finitely many nonzero polynomial guards in the abscissa parameter \(s\) can be avoided. The same parameter works locally for any finite family of prepared inputs. Conjugate denominator guards exclude at most a finite set of parameter values; zero is outside that set. The finite-algebra pole guards therefore admit \(\tau=0\), provided the preceding point-algebra guards have been met.

The [complete proof](../papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex) treats every valuation case, including primes dividing the conic denominator. The [checker](../computation/pole_parameters/shared_parameter_local_v41) verifies the identities, native source guards, 7,704 finite-field quartics, and 19,008 local valuation cases.

For the pole quartics, the equivalent rational-point condition is exact: for one common \(\tau\), each elliptic curve

\[
E_{N_i(\tau)}:\quad y^2=x(x-N_i(\tau))(x+3N_i(\tau)),
\qquad
N_i(\tau)=D_iC_i(\tau^2-D_i)(\tau^2+3D_i)
\]

must have a rational point with nonzero ordinate and abscissa in the prescribed class \(D_i\mathbb Q^{\times2}\). The complete source additionally requires the specified conjugate guards to be avoided. Local solubility does not establish this simultaneous rational occurrence. The published fixed-parameter counterexamples are global obstructions and are consistent with this theorem.

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

The [classification proof](../papers/pole_parameters/conic_chain_obstruction_20261115_v41.tex) uses three local lemmas, quadratic characters, CRT, and primitive Pythagorean triples. Its [exact certificate](../computation/pole_parameters/conic_chain_v41) requires no elliptic-rank computation or conjecture. This excludes the specified family on the full prepared locus, rather than all possible five-auxiliary pole predicates.

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

The [proof and explicit parametrizations](../papers/pole_parameters/automatic_conic_obstruction_20261115_v41.tex) and [exact checker](../computation/pole_parameters/automatic_conic_v41) use the necessary direction of Tunnell's theorem only. The examples do not assert that the current full detector system takes these values. A replacement restricted to a specially constructed detector locus would still need a separate completeness theorem.

## Reproduction and consequences

Run:

```sh
python -B scripts/verify_v41.py
```

The verifier reconstructs all three certificates in temporary files and compares their complete bytes. The universal assertions are proved in the TeX papers; finite samples do not replace those proofs. Primary references and the exact necessary direction of Tunnell's theorem are recorded in the [bibliography guide](literature_20261115.md).

For a reduction below 25 variables, the common-parameter route now has a fully resolved local stage and a specific simultaneous elliptic square-class problem over \(\mathbb Q\). For smaller quartics, a replacement must either preserve the full prepared locus or prove that the actual completeness inputs lie in a suitable restricted locus. The stated conic-chain and automatic-conic shortcuts do not supply that proof.
