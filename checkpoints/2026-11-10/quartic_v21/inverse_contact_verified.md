# Verified quartics with 226 and 262 variables

The inverse-weight contact circuit in `contact_inverse_horner.md` has passed literal-source reconstruction, an independent standard-library checker, and a separate audit by the height-audit agent. There is no change to the rational projection of either complete source system.

| Family | Total variables | Quadratic rows | Ordinary monomials | Parameter-separated terms |
|---|---:|---:|---:|---:|
| family226_v21 | 226 | 200 | 2835 | 2836 |
| family262_v21 | 262 | 234 | 3494 | 3495 |

Both quartics have exact degree four and content one; every coordinate occurs. Their coefficient heights remain `max(C,A^2+1)`, with the same 1520-bit constant coefficient maximum and linear multiplier maximum 44402. For `A=149^(2N+1)`, the height is exactly `149^(4N+2)+1` for every `N>=53`.

The 226-variable defining threshold remains ineffective under the retained arithmetic premises. The fully specified 262-variable theorem holds for every `N>=9682`, inheriting the independently audited logarithmic contact-height threshold. At the specified value its coefficient height is `149^38730+1`, of binary length 279599. No additional abc assumption is used by either theorem.

## Files

- `computation/quartic/build_inverse_contact_v21.py`
- `computation/quartic/check_inverse_contact_v21.py`
- All four JSON files in `computation/quartic/family226_v21/`
- All four JSON files in `computation/quartic/family262_v21/`
- `papers/quartic_existence/quartic226_20261110_v21.tex`
- `papers/quartic/quartic262_20261110_v21.tex`

The papers are standalone versions of the full arithmetic arguments with the new contact circuit and all current counts. A byte comparison verified that their complete point, scalar, local-extraction, global-height and completeness sections match their respective current source papers exactly. The fixed arithmetic coefficient `-228` in `N_S` is preserved.

## SHA256

226 quadratic system:
`ccc845018e4d89b9d19f797bbfeca10c17ec637fbde5cb5bc08ad3bba9da105b`

226 quartic:
`245c69c180b01281ebc95480d9336793068a5c0dde76659015f2eb6d7bf92c31`

262 quadratic system:
`84c1130856dfda7d3a489f3077d7bc378cd8e594198dd8f3c03fe50463606a93`

262 quartic:
`727244236b25c1b1b54f6cc615433f6259440d28215b632de9d60bd4e50e2523`

## Independent scope

The checker derives the five polynomial coefficients by elementary symmetric sums, independently of the producer's convolution algorithm. It verifies the general projection identity, inspects every use of each omitted output, reconstructs four/six changed rows, compares 196/228 remaining rows exactly, and independently expands the complete quartic. All equations remain quadratic. The omitted polynomial values are nonzero on every solution. The `r=0` stratum is exactly the existing `q=s1=-1` stratum.

The separate audit is saved at `checkpoints/height_v21/inverse_contact_audit.py` and its JSON certificate. The root agent handles TeX compilation, PDF review, current-result metadata and repository publication.
