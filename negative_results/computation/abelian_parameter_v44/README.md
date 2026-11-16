# Native pole obstruction on abelian parameter spaces

Run from the repository root:

```sh
python negative_results/computation/abelian_parameter_v44/check.py
```

Use `--output /path/to/certificate.json` to write the certificate to
another location. Missing parent directories are created. The resulting
JSON is deterministic and independent of the output path.

The script uses the Python standard library and writes `certificate.json`
in this directory. It checks the published native formula bindings,
the ten-contact and six-contact polynomials, the two independently
computed finite-field point counts used to prove simplicity of the
restriction of scalars, the fixed source point, the conditional weight
normalization, and finite audits of the odd-contact and pole valuations.

The accompanying proof is
`negative_results/papers/rational_fibers/abelian_parameter_obstruction_20261116_v44.tex`.
Its universal valuation arguments and geometric steps are explicit in
the paper; they are not inferred from a finite grid.

## Scope

The theorem fixes the input and early scalar and assumes the native
guards are generically nonzero. It excludes rational square-complement
sections and original normalized pole witnesses over an abelian
parameter function field when the detector argument is nonconstant.
Point maps, group translations, and pole square classes may vary.

The theorem does not exclude rational lifts after the root points and
slope have been fixed, individual rational tuples, or constructions
on ramified covers. The certificate makes no rational-realization or
variable-count claim.
