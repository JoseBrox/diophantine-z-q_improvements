# Exact checks for power shifts and the Sun audit

The complete theorem is in [the manuscript](../../../papers/number_fields/power_shifts_and_finite_exceptions_20261117_v69.tex). Its proof establishes finite avoidance over every number field, the `dN` coordinate count and the degree bounds. The finite computations here verify fixed identities used in the accompanying Sun audit and explicit avoidance examples; they do not replace those general proofs.

From the repository root:

```sh
python -B computation/number_fields/power_shifts_v69/check.py --manuscript papers/number_fields/power_shifts_and_finite_exceptions_20261117_v69.tex --output /tmp/power-shifts-v69.json
```

The program uses exact Python fractions and SymPy. It checks the elliptic carrier and duplication, ordinate resultant and discriminant, formal-logarithm coefficients, contact transformations, three split-prime/CRT examples and six four-contact boundary examples. The certificate labels its finite and arithmetic scope. The [audit](../../../docs/audits/sun_v2_20261117_v69/audit.md) preserves source versions, qualifications and bibliography.
