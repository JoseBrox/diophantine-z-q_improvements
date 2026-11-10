# Twenty-five coordinates with two combined pole certificates

This directory specifies the twenty-five-variable family proved in
[`few_variables25_merged_20261110_v18.tex`](../../../papers/few_variables25/few_variables25_merged_20261110_v18.tex).
It retains the elliptic group, pole and prime-pattern inputs of the preceding
construction, the full modular realization used in the proved cubic
logarithmic contact-height estimate, and the proved aggregate trace-height
estimate. It does not add an abc conjecture.

All counts include the distinguished input. The fixed odd integer `L` is a
coefficient parameter, not a quantified variable. The theorem applies to every
sufficiently large odd `L`; its sufficient threshold is ineffective.
**The supplied fixture `L=3` is not certified to define the integers.**

## Construction and exact bounds

| Quantity | Value |
|:--|--:|
| Retained rational coordinates | 24 |
| Final finite-algebra coordinate | 1 |
| Total polynomial coordinates | **25** |
| Finite point quartics | 9 |
| Finite pole quadratics | 2 |
| Finite-algebra rank | 1,048,576 |
| Factors in the final polynomial specification | 262,144 |
| Total-degree upper bound | 104,263,275,909,198,787,271,196,672 |
| Simpler degree bound | strictly below $2^{87}$ |
| Coordinate-monomial upper bound | strictly below $2^{2035}$ |

The last two bounds are uniform in the fixed odd exponent. The polynomial has
not been expanded; the support bound is not an exact monomial count. No
coefficient-height bound for a certified defining member is inferred from the
fixture's coefficient certificate.

The 24 retained coordinates consist of the input, eighteen coordinates for
nine elliptic points over the quadratic field, one nonzero common slope, and
four parameters for two pole certificates. The scalar local conditions occur
inside both comparison products. They need no separate pole parameter pair.

The local normalization is the rational function

$$
\Psi_z(D)=\frac{zD^2}{1+zD^2}.
$$

At a prime where $z$ has odd valuation this function is integral, regardless
of the pole order of $D$. When $z$ is a unit, its positive valuation is
equivalent to positive valuation of $D$. The separate
[`local valuation paper`](../../../papers/local_tests/rationally_normalized_local_tests_20261110.tex)
also treats the even-valuation cases used in the global proof.

Only the first ten tests, the reciprocal elliptic abscissas, are squared. The
other six comparisons are unchanged. The formal parameter $-x/y$ provides
precision four for the integer residuals. Both the normalizing power and the
norm denominator power are seven. Exact integer rounding in the valuation
inequalities gives the fourth-power divisibilities required by the height
argument, while completeness requires only the first formal neighborhoods of
the opposite elliptic anchors.

The contact-height theorem gives an exponent $19/6$ for one five-contact
block. Two disjoint translates in each comparison function improve this to
$19/12$. Together with the fourth-power divisibilities, the global estimate
has exponent $95/48<2$, which is the strict inequality needed in the Lucas
comparison. This is where the full modular realization enters the proof.

## Files

- `build_merged_source.py` constructs the complete guarded rational source and
  converts it to integer coefficient operations.
- `certificate/source.json.gz` is the source coefficient graph for `L=3`.
- `certificate/source-polynomial-specification.json` is the exact integer
  finite-algebra specification.
- `active25/polynomial-specification.json` specifies the final polynomial by
  finite integer operations, determinants and products.
- `check_merged_source.py` independently checks the full affine conversion,
  all point quartics, square clearings and guards. It also reconstructs the
  new rational formulas in fifteen finite-field samples without importing
  their producer.
- `check_merged_bounds.py` independently sums all 262,144 degree cases and
  verifies a formal coefficient-symbol envelope for uniformity in `L`.
- `independent-source-verification.json` and
  `independent-bound-verification.json` give the successful verification
  receipts and their precise scopes.

The finite-field samples provide exact finite evidence for formula assembly.
They are not a proof of a universal identity or of the arithmetic projection.
The symbolic conversion and the point/pole equations are checked exactly;
the mathematical paper proves the global projection under its stated inputs.

## Reproduce

From the repository root, using Python's standard library:

```bash
python computation/few_variables/merged25/build_merged_source.py --anchor-exponent 3 --output computation/few_variables/merged25/certificate
python computation/few_variables/active_elimination/build_active_specification.py computation/few_variables/merged25/certificate/source-polynomial-specification.json computation/few_variables/merged25/active25
python computation/few_variables/merged25/check_merged_source.py computation/few_variables/merged25/certificate --output computation/few_variables/merged25/independent-source-verification.json
python computation/few_variables/merged25/check_merged_bounds.py --output computation/few_variables/merged25/independent-bound-verification.json
python computation/local_tests/check_rational_normalization.py --output computation/local_tests/rational-normalization-certificate.json
```

Successful reproduction verifies the supplied coefficient specification and
its bounds. It does not establish that the fixture exceeds the ineffective
sufficient threshold.
