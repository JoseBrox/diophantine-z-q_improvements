# Fixed pole fibers and independent detector indices

The [complete proof](../papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex) establishes two reductions of the common-parameter problem. Neither supplies a new defining variable count. The construction records remain [25 and 13 total variables, and quartics in 196 and 78](../README.md#current-constructions--15-november-2026), under their stated arithmetic premises and additional height hypotheses.

## Rational witnesses at a fixed parameter

For a prepared input \(b=dt^2\), put

\[
D=17d,\qquad C=17(17-b),\qquad e=\frac{\tau^2-D}{\tau^2+3D}.
\]

At every rational \(\tau\), the twist \(n=DeC\) has odd valuation at 17. Consequently the rational torsion of

\[
E_n:\quad y^2=x(x-n)(x+3n)
\]

consists only of its two-torsion. A rational solution with \(q\ne0\) of

\[
q^2=D(s^2-eC)(s^2+3eC)
\]

gives an infinite-order point \((Ds^2,Dsq)\). Its positive odd multiples preserve the abscissa square class \(D\mathbb Q^{\times2}\) and produce infinitely many admissible values of \(s\) at the **same** \(\tau\). These witnesses avoid every finite collection of nonzero specialized polynomial guards.

For all four native source circuits, the syntactically extracted \(d_i\) depend only on the input, root abscissas, comparison slope and fixed parameters. They are independent of every auxiliary point and every finite-algebra character. At an actual prepared tuple, each \(d_i\) is a positive rational scalar. Thus \(\tau^2+51d_i\) is nonzero at every character for every rational \(\tau\). The remaining pole radicands have unit leading coefficients in their respective \(s_i\), so their norms remain nonzero polynomials after fixing \(\tau\).

It follows that, once all earlier point-stage guards hold, **one common rational parameter with nonzero second-pole ordinates suffices for every native pole-stage guard**. This includes the stricter nonzero guards used before the terminal-root relaxation. The argument permits \(\tau=0\); it asserts no rational solubility at that value.

## Independent actual detector families

Fix an integer input, root points, comparison data and one actual guarded prepared tuple. Under the retained source premise \(2E(\mathbb Q(\sqrt2))=\mathbb ZP\), the auxiliary indices can vary independently in infinite return sets

\[
R_\ell=[m_{\ell,0}+2Mk_\ell]P,
\qquad (k_1,\ldots,k_r)\in\mathcal S^r.
\]

Here \(r=5\) for the general and explicit sources, and \(r=2\) for either conditional source. Every tuple preserves preparation, all point-stage character guards, the root and comparison data, and each scalar \(d_i\). The differences are recomputed from the new points. Half-point charts prove the existence of rational retained square-abscissa coordinates without adding source variables.

This result uses finite-place continuity and returns in the compact real cyclic closure. It does not require density in the full product of real elliptic curves. It gives independent choices of **indices**; it does not assert that detector values vary independently or cover any prescribed rational set. Rational pole solubility is not one of the open conditions proved to persist.

## The remaining theorem for 24 variables

For each integer input, choose actual guarded prepared detector data such that both second-pole equations have rational solutions with nonzero ordinates at one common \(\tau\). The first theorem then supplies all remaining pole guards. Identifying the two conic coordinates would leave \(\tau,s_0,s_1\), reducing the general construction to 24 total variables. The analogous statement for a conditional source would give 12.

These counts are consequences of an **unproved global realization assertion**. The [local theorem](pole_results_20261115_v41.md) establishes local solubility everywhere for every rational parameter, so local congruence searches do not resolve this assertion.

## A concrete sufficient locus

The separate [section classification](../negative_results/papers/pole_parameters/rational_sections_20261116_v42.tex) gives an explicit sufficient locus for the global assertion. If every \(C_i=17(17-b_i)\) is a rational square, write \(C_i=c_i^2\) and use

\[
s_i=c_i,\qquad q_i=-\frac{4C_iD_i\tau}{\tau^2+3D_i}.
\]

These are simultaneous witnesses for every nonzero rational \(\tau\), and the fixed-fiber theorem supplies all remaining pole guards. Whether the actual detector tuples can always be chosen on this locus is unproved. The classification proves that this locus is necessary for rational-function sections of the fixed-input family; it does not make it necessary for isolated rational fibers or a common rational specialization.

## Reproduction and scope

```sh
python -B scripts/verify_v42.py
```

The [exact checker](../computation/pole_parameters/fixed_fiber_guards_v42/check.py) independently audits the square extraction and dependency sets in all four native circuits. It verifies the elliptic and half-point identities, the torsion diagnostic, and exact pole witnesses recovered from odd multiples in six prepared examples. The four circuit fixtures use their stated default fixed parameters; the manuscript proves the parameter-uniform assertion by multiplicative parity. These checks do not prove the inherited arithmetic premises or simultaneous rational realization.
