# Exact field-extension and anisotropic-form checks

The full proofs are in the [systems and field-extensions paper](../../papers/systems_and_fields/systems_and_field_extensions_20261107_v7.pdf).

`verify_anisotropic_examples.py` independently expands the displayed cubic norm determinant and checks the quadratic and cubic coefficient tables. It completely enumerates the relevant residue-field vectors. The valuation argument in the paper proves anisotropy over the number field.

`check_field_extension.py` specializes both the complete quartic coefficient table and all 426 quadratic residuals. These independent evaluations prove

$$
Q_{456}(\tfrac12\mathbf e_0+Y\mathbf e_{79})
=Y^2+16081968676531905/16.
$$

The resulting quadratic field admits a rational-polynomial zero with input $1/2$, which is not an algebraic integer. The result concerns this unchanged equation over the stated extension. It does not rule out a field-dependent definition of the ring of integers.

Run the checks from the repository root:

```bash
python3 computation/field_extensions/verify_anisotropic_examples.py
python3 computation/field_extensions/check_field_extension.py computation/quartic/polynomial-456
```

The second command reads either the raw JSON tables or their distributed gzip encodings. Both scripts use only the Python standard library.
