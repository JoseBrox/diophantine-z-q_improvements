# Local solubility of shared pole parameters

The construction records remain **25** total variables, **196** for a quartic, **13** under the stated weak-abc hypotheses, and **78** for a quartic under ordinary rational abc. The local theorem below does not specify a smaller defining polynomial.

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

## Reproduction and the remaining rational-point problem

Run `python -B scripts/verify_v41.py` from the repository root. The local checker reconstructs its complete certificate, including the native guard audit. The proof in the TeX manuscript establishes the assertions for every prepared input and parameter; finite tests supplement that proof.

A reduction to 24 variables requires one common rational parameter with rational points in all the stated abscissa classes, together with the required guards. The separate [negative-results directory](../negative_results/README.md) records the proved limitations of other pole replacements.
