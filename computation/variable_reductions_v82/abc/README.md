# One-parameter pole criterion and shifted-menu obstruction (v82)

These deductions develop the source notes of **Gabe Conant with Astra 6.2**.

The manuscript proves the local soundness of

\[
Y^2=d\bigl(s^4-(V^2+d)^2\bigr),\qquad d=7u/(1+u)^2,
\]

and proves that every prepared scalar fibre is everywhere locally soluble. It gives a precise additional actual-input rational-point condition which would reduce the eleven-coordinate construction to ten. That condition remains unproved.

The certified counterexample has nonsquare `u`, the star square class `119=7*17`, and satisfies the displayed real, square-denominator and two-adic preparation. On `E_6305215`, algebraic descent gives rank exactly one, and the rational Kummer image excludes square class `119` from every nonzero shifted abscissa `x,x-N,x+N`. The exclusion survives all constant multipliers supported on `{2,3,5,7}`, and all powers of `N`. The parameter data are **not asserted to occur at the actual contact detector or W trace**.

## Reproduction

The exact checker uses SymPy and PARI/GP 2.17.4 through PassageMath 10.8.14. Install the pinned runtime and run from the repository root:

```sh
python -m pip install sympy==1.14.0 passagemath-pari==10.8.14
python -B computation/variable_reductions_v82/abc/check_genus_one.py
```

The default operation is read-only and compares the reconstructed result with `certificate.json`. The explicit `--write` option regenerates the certificate.

The algebraic rank calculation uses `ellrank`, whose first two outputs are unconditional lower and upper bounds. No floating-point analytic-rank calculation or BSD assumption is used. The second rank calculation is on a 2-isogenous curve and uses the same PARI implementation; it is not described as an independently implemented descent. The mathematical local and Kummer arguments are written in the manuscript.

## Files

- `papers/pole_parameters/genus_one_sound_criterion_20261120_v82.tex`: complete proof and open actual-input criterion.
- `check_genus_one.py`: exact read-only verifier.
- `certificate.json`: exact algebraic-descent and square-class data.
- `tex_review.json`: final TeX source hash and visual QA receipt.

There is no new defining-variable record in this package.
