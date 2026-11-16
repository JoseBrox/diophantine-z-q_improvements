# Parity-sensitive mixed-power height bounds

This package certifies the exact arithmetic in
[`mixed_power_height_20261116_v45.tex`](../../../papers/elliptic_heights/mixed_power_height_20261116_v45.tex).

For `s=x^(2n)+y^2`, `n>=3`, and a weak rational abc inequality with exponent
`1<=kappa<2n/(n+2)`, put `D=2n-kappa(n+2)`. The proved coefficient of
`h(s)` in the bound for `h(x)` is

```text
[n+kappa(n-2)]/[n D],
```

with additive constant `log(K)/D`. The companion bound for `h(y)` multiplies
both quantities by `n`. No parity restriction on `n` is needed.

At `n=8`, `kappa=101/100`, the coefficient is `703/2360`. Combining the
proved estimate with the ordinary-abc eight-contact bound and a residual
divisor satisfying `log N<=4h(X)+log(1+|m|)+O(1)` gives the strict absorption
coefficient `1406/2065`.

## Verification

Python 3 and SymPy are required. From the repository root:

```sh
python computation/elliptic_heights/mixed_power_v45/check.py --check
```

The checker reconstructs 27 exact symbolic and arithmetic checks, compares
the full report with `certificate.json`, and writes no files. The six
valuation cases are certified by nonnegative polynomial identities in
unbounded nonnegative parameters; this is not a finite valuation search.
The check also binds the manuscript by SHA-256 and verifies the quadratic
height circuit and its one-coordinate cost relative to the eighth-power
scale.

Without arguments the checker prints the full reconstructed certificate to
standard output. An explicit output path can be supplied when regenerating
an owned certificate:

```sh
python computation/elliptic_heights/mixed_power_v45/check.py --output /tmp/mixed_power_certificate.json
```

The theorem's proof is in the manuscript. The exact checks support its
algebra and case arithmetic. The fixed-exponent height lemma uses only its
stated weak-abc hypothesis; the marked-contact application retains
ordinary rational abc. The package supplies no new detector completeness
theorem and does not change a published polynomial variable count.
