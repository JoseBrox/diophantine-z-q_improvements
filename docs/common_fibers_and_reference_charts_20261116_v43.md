# Common rational fibers and quadratic reference coordinates

The defining-variable records remain **25**, **196 for quartics**, **13 under the stated additional height hypotheses**, and **78 for quartics under ordinary rational abc**. All counts include the input and retain the arithmetic premises listed in the [current construction table](../README.md). The results below supply arithmetic and algebraic reductions, with no smaller complete defining polynomial asserted.

## An early scalar with a rational square complement

The [scalar theorem](../papers/pole_parameters/square_complement_baseline_20261116_v43.tex) changes the early scalar in the general source, before the comparison primes and auxiliary points are chosen. Write

\[
\ell=76249,\quad \beta=216X^4+450459,\quad
r=\beta(\beta-1)(\beta-2401)(32\beta+343)(2\beta-1).
\]

For a sufficiently large fixed odd exponent \(L\), put

\[
\rho_* = \frac{102^2\ell^Lr}{(1+153\ell^Lr)^2}.
\]

With \(z=153\ell^Lr\), this gives the identity

\[
17(17-\rho_*)=
\left(\frac{17(1-z)}{1+z}\right)^2.
\]

The soundness proof includes rational inputs with a denominator divisible by \(\ell\). If \(m=-v_\ell(X)>0\), then

\[
v_\ell(\rho_*)=|L-20m|,
\]

which is positive and odd but need not be at least \(L\). The corrected height argument uses

\[
L\log\ell\le\tfrac12\log c+5h(\beta),\qquad
h(\rho_*)\le20h(\beta)+\log c+O(1).
\]

Together with the native scalar-height estimate, these inequalities preserve the source argument for every sufficiently large fixed odd \(L\), under the same arithmetic premises. The retained-coordinate and finite-algebra choice counts are unchanged. The theorem does not supply a numerical sufficient exponent or coefficient bounds for this modified family, so the current degree and coefficient record specifications remain the original ones.

For every integer input and any finite set of rational primes prescribed before preparation, the actual guarded detector inputs can be chosen so that each \(17(17-b_j)\) is a square in all those completions. This follows by choosing the detector multipliers sufficiently close to one and applying the [independent-index return theorem](../papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex). The complement of \(\rho_*\) is a nonzero rational square, so its local square neighborhoods are open, including at 2 and 17.

The remaining global condition is

\[
17(17-b_j)\in\mathbb Q^{\times2}
\quad\text{for every actual detector input }b_j.
\]

The finite-local conclusion does not establish it. If it holds, the explicit rational sections give a common nonzero rational conic parameter; the fixed-fiber theorem then supplies the remaining pole guards. A common rational fiber can also exist without rational square complements, so proving those complements is a sufficient route rather than a necessary condition for 24 variables.

The distinction between an early scalar and a final detector input is essential. The [normalization counterexample](../negative_results/papers/pole_parameters/square_complement_normalization_20261116_v43.tex) shows that replacing an actual input by \(1156b/(17+b)^2\) destroys the pole predicate despite preserving its square class and forcing a square complement. The [actual-neighborhood theorem](../negative_results/papers/pole_parameters/actual_square_complement_neighborhoods_20261116_v43.tex) proves that certain valid independent-index families in the original source have nonsquare complements throughout a fixed 23-adic neighborhood. The modified early scalar avoids that particular restriction without asserting global square complements.

## Quadratic reference and height equations

The [reference theorem](../papers/elliptic_charts/scaled_reference_height_20261116_v43.tex) starts from \(E:y^2=x^3-Dx\), \(P=(a,b)\), \(c=b/a\), and \(\delta=D/a\). Two quadrics

\[
J=\lambda^2,\qquad
\alpha(\alpha-\delta J-1)+c\lambda(1-\delta J)+2\delta J=0
\]

describe \(E\setminus\{(0,0),P+(0,0)\}\). Both reference reciprocal abscissas are linear:

\[
f_H=(1-\alpha-c\lambda)/a,\qquad
f_{H-P}=(\alpha-\delta J-c\lambda)/a.
\]

Retaining \(\kappa=J^2\) permits a weighted rescaling of all seven numerator-pair coordinates. Their point, difference, and complete ratio equations remain quadratic on \(\lambda\ne0\). The original height trace is recovered by one field equation

\[
J\left(T/2+\sqrt2 Z\right)=s_*^2+D(f_*+g_*),
\]

where \(T=\operatorname{Tr}x(U-V)\) and \(Z\) is one new rational coordinate. Thus the height still depends only on the original fixed difference, as required before prime selection.

Writing \(\kappa=\kappa_0+\sqrt2\kappa_1\), the quadratic row \(\kappa_0\zeta=1\), with one rational coordinate \(\zeta\), enforces \(\lambda\ne0\) exactly. Indeed

\[
\kappa_0=\lambda_0^4+12\lambda_0^2\lambda_1^2+4\lambda_1^4>0
\quad\text{when }\lambda\ne0.
\]

| Block | Original rational coordinates | Rescaled rational coordinates |
|:--|--:|--:|
| Reference | 10 | 8 |
| Numerator pair and slope | 14 | 14 |
| Ratios and comparison squares | 8 | 8 |
| Original trace recovery | 1 | 2 |
| Additional nonzero-scale guard | 0 | 1 |
| **Total for these blocks** | **33** | **33** |

The boundary \(\lambda=0\) admits additional degenerate scaled solutions. Its guard cannot be omitted from this comparison. A smaller complete quartic also needs quadratic conversion of every detector factor; those conversion costs are not included in the table.

The [reference-test obstruction theorem](../negative_results/papers/elliptic_charts/shared_reference_test_obstructions_20261116_v43.tex) gives exact local cancellations for the proposed squared reference factor and for its whole-factor odd-cube repairs. The latter fail even with positive comparison-slope valuation and a unit comparison error. These are local factor-level obstructions, not false solutions of a complete source. The separate [mixed-sign theorem](../negative_results/papers/elliptic_charts/mixed_reference_signs_20261116_v42.tex) still requires a revised detector to control both torsion branches.

## Global arithmetic structure

For distinct positive pole scales \(D_i\), fixing nonzero twist classes \(\alpha_i\) gives the propagation curve

\[
\alpha_i r_i^2=(\tau^2-D_i)/(\tau^2+3D_i),
\qquad g=1+2^r(r-1).
\]

For two poles its genus is five. The [synchronization theorem](../negative_results/papers/pole_parameters/fixed_class_synchronization_20261116_v43.tex) gives its elliptic and genus-two quotients, proves finiteness for each fixed class tuple, and computes Kodaira dimension one for the full common-parameter variety with at least two distinct pole scales. These statements restrict fixed-class propagation and direct Kummer-quotient methods. They do not exclude one common rational fiber or the union over infinitely many class tuples.

The [norm-map theorem](../papers/pole_parameters/doubled_source_congruent_twists_20261116_v43.tex) extracts a rational congruent-number point directly from a doubled point on the native elliptic curve. For \(d=3-\sqrt2\), write \(x=h^2\), \(j^2=x^2-d^2\), and put

\[
A=N(h),\quad B=N(j),\quad R=\operatorname{Tr}(x\bar d)/2,
\quad M=RB,\quad V=A^2+7+2R.
\]

Then

\[
(RV,2R^2V)\in\{Y^2=X^3-M^2X\},\qquad
B^2=(A^2+7)^2-4R^2,
\]

and the ordinate is nonzero. The abscissa class is \([R]\). Identifying that class with the required detector class, or using it to trivialize a prescribed complement torsor, remains open.

The [literature audit](../negative_results/docs/fixed_fiber_literature_20261116_v43.md) records the exact hypotheses preventing a direct application of existing Kummer and genus-one fibration theorems. Local solubility, positive rank, and finiteness of Tate--Shafarevich groups do not by themselves provide the prescribed simultaneous rational points.

## Next proof targets

1. Prove global square complements on a family of actual guarded detector tuples for the modified early scalar, allowing the auxiliary twist classes to vary; alternatively, trivialize the two prescribed isogeny-Selmer classes at a common rational parameter without imposing square complements.
2. Construct a quadratic reference test compatible with the rescaled chart, prove its implication on every torsion branch, and account for its detector conversion, fixed-index height, and nonzero constraints. A saving requires at least one fewer rational coordinate after all these costs.

Reconstruct the seven associated exact certificates with `python -B scripts/verify_v43.py`. The manuscripts prove the infinite statements; the checkers certify their listed finite identities, source bindings, and examples.
