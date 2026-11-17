# Simple primitive elliptic denominator primes

The [manuscript](../../../papers/elliptic_divisibility/simple_primitive_denominators_20261117_v60.tex) proves a simple-prime support bound by duplication and weak rational abc. Weak exponent (4/3) gives a primitive prime of valuation one for every sufficiently large index. Every fixed exponent (1<\kappa<2) suffices on indices coprime to a suitable fixed primorial.

Run from the repository root:

```sh
python -B computation/elliptic_divisibility/primitive_denominators_v60/check.py --output /tmp/primitive-v60.json
```

The exact checker verifies the quartic and duplication identities on rational points, cancellation outside the fixed bad primes, 1,992 finite-field reduction/order cases, and the rational constants for the coprime-index argument. It reproduces `certificate.json`. The asymptotic primitive-prime statement is proved in the manuscript under its stated weak-abc hypothesis; the finite examples do not establish that hypothesis or an integer-defining variable bound.
