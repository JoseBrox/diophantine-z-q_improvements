# Shared squared input comparisons: reconstructed 948/1127, improved 943/1124

Two common field coefficients replace the private input-comparison fields in every ordinary integrality block. This independently reconstructs the previously reported **948/1127** quartic counts from the pinned v102 tables and composes with the new contact compression and BB-native poles to give preferred complete systems in **943/1124 variables**.

| Complete stage | General variables / rows | Specified variables / rows |
|---|---:|---:|
| Reconstructed from v102 | 948 / 803 | 1127 / 978 |
| Preferred, including contact compression and BB-native poles | 943 / 798 | 1124 / 975 |

The earlier original files and commits for the reported 948/1127 counts were not recovered. These are newly compiled, independently audited reconstructions of those counts, not a claim that the missing historical files were found. The preferred tables improve those counts by another five and three variables.

## Exact saving and the reciprocal chart

Let `epsilon*rho=1` be the retained common gauge. Existing ordinary-input coordinates `Y_i,P_i` satisfy

```text
(51*rho*Y_i + 2501)^2 = 4*rho*P_i.
```

Their private field `I_i=S-(2504+51*rho*Y_i)*s` occurs only in its own definition and through `I_i^2`. Introduce two common fields

```text
epsilon*B = (S-3*s)*s
epsilon*C = s^2
```

Then substitute the exact quadratic expression

```text
I_i^2 = S^2 - 5008*S*s + 15015*s^2 - 102*B*Y_i + 4*C*P_i.
```

The constant quadratic expression needs no additional coordinate. Delete the two rational components of `I_i` in all 12 general ordinary blocks or 10 specified ordinary blocks, and add only the four rational components of `B,C`: the savings are 20 and 16 coordinates and rows. The reciprocal block uses a different gauge, `i_inverse`, so its comparison coordinates and all its rows are retained literally. All 13/11 integer predicates remain.

The change is a bijection on the complete rational zero sets of each pinned predecessor. The only division is by the existing nonzero common gauge; no input, comparison, point coordinate, or scalar-pair register is required to be nonzero. The new operation adds no arithmetic premise. The preferred systems retain the BB-native premise set and the other existing arithmetic interfaces; no unconditional undecidability claim is introduced.

## Artifacts and reproduction

- `input_comparison_sharing.tex` / `.pdf`: exact identities, complete inverse, reciprocal-chart treatment, counts, and scope.
- `reconstructed_general_quadrics.json` / `_certificate.json`: 948/803 from the frozen v102 general table.
- `reconstructed_specified_quadrics.json` / `_certificate.json`: 1127/978 from the frozen v102 specified table.
- `preferred_general_quadrics.json` / `_certificate.json`: 943/798 including contact compression and BB-native poles.
- `preferred_specified_quadrics.json` / `_certificate.json`: 1124/975 including contact compression and BB-native poles.
- `build_input_comparison.py`: deterministic compiler.
- `verify_input_comparison.py`: independent symbolic, occurrence, row, guard, metadata, and hash audit; no compiler import.
- `independent_verification.json`: recorded finite audit results and scope.

From the repository root:

```sh
python undecidability/input_comparison_v105/build_input_comparison.py
python undecidability/input_comparison_v105/verify_input_comparison.py
```

The verifier independently expands the polynomial reconstruction identity, derives field components modulo `z^2-2`, checks both common gauge guards, every scalar-pair relation and comparison-coordinate occurrence, and compares all unchanged rows by named monomials. It also verifies all retained metadata, integer coefficient rings, complete variable support, degree, and file hashes. The finite audit does not prove the inherited arithmetic theorems.
