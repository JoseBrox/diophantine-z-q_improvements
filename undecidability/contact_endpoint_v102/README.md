# Two retained endpoint powers replace two contact helpers

The complete general and specified systems now have **968 variables / 823 quadratic rows** and **1143 variables / 994 rows**, respectively. This is an exact guarded rational rechart and two affine eliminations. It changes no source or integer-interface hypothesis and needs no additional prime-supplier argument. The ordinary-`abc` result remains 695/590.

The previous aggregate-spacing theorem makes the root block's second contact the sixteenth point of the common progression. Its square and fourth power are already stored, but in a different gauge. Rechart its four private square/fourth/combination/inverse-weight registers to the first-contact gauge: each old value equals `epsilon` times the new one in the general chart, or `epsilon^2` times the new one in the specified chart. The existing nonzero gauge makes this reversible; every affected row remains quadratic.

The endpoint values `u2,f2` then replace two common interpolation helpers:

```text
v  = (u2 - u - 256*w) / 32
a1 = (f2 - f - 256*a2 - 4096*a3 - 65536*a4) / 16
```

The endpoint square and fourth-power rows are exact combinations of the retained root and interpolation rows, so they can be deleted. This saves two coordinates and two rows on each interface. Every reconstructed coordinate is unique; the equivalence applies to the rational zero sets, not merely the instance projection.

## Files and reproduction

- `contact_endpoint_reuse.tex` / `.pdf`: complete guarded chart, reconstruction identities, counts and audit proof.
- `endpoint_general_quadrics.json` / `_certificate.json`: full 968/823 system, from frozen v101.
- `endpoint_specified_quadrics.json` / `_certificate.json`: full 1143/994 system, from frozen v100.
- `build_contact_endpoint.py`: deterministic compiler.
- `verify_contact_endpoint.py`: independent exact checker with no compiler import.

From the repository root:

```sh
python undecidability/contact_endpoint_v102/build_contact_endpoint.py
python undecidability/contact_endpoint_v102/verify_contact_endpoint.py
```

The compiler uses the first-contact polynomial templates. The checker independently derives every recharted row by Laurent substitution using the retained gauge guards, then verifies both affine eliminations and omitted-row identities. It checks all 32/28 changed rows, 791/966 unchanged rows, every recharted-coordinate occurrence, both gauge guards, coefficient rings, support, degrees, metadata and hashes.
