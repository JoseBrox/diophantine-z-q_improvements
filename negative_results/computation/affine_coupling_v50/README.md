# Affine scalar coupling obstruction

The manuscript in `negative_results/papers/integer_labels/affine_scalar_coupling_obstruction_20261116_v50.tex` proves that every fixed finite set of identifications `S=[m]A+[k]P` loses an infinite arithmetic progression of integer inputs for the specified general source in its sufficiently large coefficient range.

The checker certifies the exact example `X=11`, `p=80287`, including primality by trial division, all five contact residues and the valuation contradiction. The infinite-family statement follows from the manuscript's elementary prime-divisor and Chinese remainder arguments, not from the finite calculation.

```bash
python -B negative_results/computation/affine_coupling_v50/check.py --output /tmp/affine-coupling.json
```

Compare the output with `affine_coupling_certificate.json`. This is a source-specific obstruction, not a minimum-variable theorem.
