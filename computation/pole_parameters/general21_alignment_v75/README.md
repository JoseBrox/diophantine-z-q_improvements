# Aligned contact numerators and physical detector scales

The physical relation `lambda=4/(rho*T^2)` gives `a*lambda=lambda+4`.
The two contact numerators coincide, and the original and normalized
weights have the same rational square class. This also makes the actual
pole inputs have the same square class whenever both traces are nonzero.

On the stated positive domain, the physical contact normalizers still
make the two order-one detector coefficients strictly different. The
normalized equality threshold is greater than `2/3`, whereas the actual
weight `u0` is less than `rho<2/3`. The complete proof and precise scope are
in [contact_alignment_20261117_v76.tex](../../../papers/pole_parameters/contact_alignment_20261117_v76.tex).

This excludes coefficientwise identification with the unchanged field
tests. It does not exclude accidental full-product equality, rational
points on either square cover, or a different correspondence between
pole surfaces. Fixing this slope also requires a new completeness
argument: the original order of prime preparation does not supply it.

Run from the repository root:

```sh
python3 computation/pole_parameters/general21_alignment_v75/check.py
python3 computation/pole_parameters/general21_alignment_v75/check_independent.py
```

The first checker uses exact symbolic identities. The second imports no
producer code or symbolic library; integer convolution independently
verifies the decisive positive factorization, with exact rational scalar
fixtures as supplementary checks. These fixtures are not actual elliptic
witnesses, and neither checker claims twenty-one-variable completeness.
