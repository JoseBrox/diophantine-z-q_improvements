# Field extensions and anisotropic forms

The [systems and field-extensions paper](../../papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf) proves the equation-combination and field-transfer statements, with their precise field hypotheses. This directory contains the exact anisotropic-form computations; the complete quartic specialization is supplied with the quartic data.

## Anisotropic forms

`verify_anisotropic_examples.py` independently expands the displayed cubic norm determinant and verifies the quadratic and cubic coefficient tables. It enumerates the relevant residue-field vectors completely. The valuation argument in the paper proves the resulting anisotropy over the number field.

From the repository root:

```sh
python3 computation/field_extensions/verify_anisotropic_examples.py
```

The script uses only the Python standard library and writes `anisotropic-forms-verification.json`.

## An explicit failure of unchanged field transfer

For the published 392-variable quartic, set the input coordinate to $1/2$, coordinate 293 to $Y$, and every other coordinate to zero. Exact substitution gives

$$
Q_{392}=Y^2+D/16,
$$

where the positive integer $D$ is specified as a polynomial in the fixed integer $A=80989^{54929}$ in [the specialization certificate](../quartic/final392/field-specialization392.json). Over $\mathbb Q(\sqrt{-D})$, taking $Y=\sqrt{-D}/4$ gives a zero with input $1/2$. Since a rational algebraic integer is an integer, that input does not belong to the ring of integers of the field.

The checker obtains the identity in two ways: directly from every term of the quartic coefficient table, and independently by specializing all 364 quadratic equations and summing their squares. Run from the repository root:

```sh
python3 scripts/restore_data.py
python3 computation/quartic/check_field_specialization392.py
```

This proves that this particular polynomial does not define the ring of integers after unchanged transfer to every number field. The separate question of a field-dependent Diophantine definition is addressed with its stated hypotheses in the paper.
