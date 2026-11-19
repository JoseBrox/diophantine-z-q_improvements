# One-helper ordinary-abc quartic: 58 coordinates

The v80 construction reduces the v79 ordinary-abc quartic from 59 to **58 total variables**, including the input. It has 50 quadratic residuals. Their sum of squares has degree exactly four, content one, 867 coordinate monomials, and 870 parameter-separated terms. For every positive integer `B`, its coefficient height is

\[
\max\{22838305425411,\ B^2+4091\}.
\]

For every sufficiently large odd `B`, it defines the integers under ordinary rational abc and the explicitly retained elliptic, formal-comparison, trace-index, and simultaneous prime-pattern premises. The threshold is ineffective. Pole completeness uses exactly Theorem B of Burungale, arXiv:2611.16130v1, in its published square classes; the stronger square-class extension retained in v79 is unnecessary here.

The new normalization is

\[
\alpha=u+u^2D^2,\qquad \tau=\frac{\alpha}{1+\alpha},
\qquad b=\frac7u\tau^2.
\]

With the retained physical scaling `D=c D_s`, `u=1/c`, and `b=c b_s`, its three quadratic rows are

\[
\alpha=c^{-1}+D_s^2,\qquad \tau(1+\alpha)=\alpha,
\qquad b_s=7\tau^2.
\]

Thus one coordinate replaces the two-helper ratio normalizer. The gate excludes `alpha=-1` identically; `alpha=0` would make `u` a negative square and is excluded by the derivative-height estimate for sufficiently large `B`. The valuation argument controls arbitrary actual auxiliary-point denominators, including negative odd poles of the derivative quotient.

The shared elliptic chart and Laurent packing derive from the supplied notes of **Gabe Conant with Astra 6.2**, audited in v78. The derivative transfer and compressed contact circuit are from v79; the one-helper normalization is v80 work.

## Reproduce

From the repository root:

```sh
python computation/variable_reductions_v80/abc/build58.py
python computation/variable_reductions_v80/abc/check58.py
```

The producer writes `quartic58/quadrics.json`, `polynomial.json`, `maps.json`, and `certificate.json`. The independent checker reconstructs the retained physical rows without importing the producer and independently expands the polynomial. Finite reconstruction does not establish the retained arithmetic premises.

The complete mathematical proof is in `papers/quartic_existence/one_helper58_20261119_v80.tex`. The independent proof review and final source hashes are in `proof_review58.md` and `manual_review58.json`; the compilation and page-layout receipt is `tex_review.json`.

The separate eleven-variable unbounded-degree construction is not reduced by this coordinate change. No rational one-parameter specialization of its intrinsic pole surface is asserted.
