# One half-trace square replaces the c-integer predicate

The complete preferred quartic systems now have **887 variables / 750 quadratic rows** in the general route and **1052 variables / 913 rows** in the specified route. These improve the 943/798 and 1124/975 predecessors by **56 and 72 variables**, respectively.

The proved arithmetic theorem in `undecidability/pell_integrality_replacement_v106/` supplies integrality of the source coordinate `c` from its first Pell norm, integral shifted trace, and one rational half-trace square. The retained source prefix already gives `3 | a`, before `c` is known integral. The general system restores the historical half-trace coordinate and row; the specified system already contains them. Their complete c-integer interfaces can therefore be removed.

| Complete system | Variables | Quadratic rows | Integer predicates | Contact weights | BB-native poles |
|---|---:|---:|---:|---:|---:|
| General | 887 | 750 | 12 | 24 | 36 |
| Specified | 1052 | 913 | 10 | 30 | 40 |

The equivalence concerns the **coded-instance projection under the retained arithmetic interfaces**. Completeness chooses the smaller tuple of elliptic witnesses anew. No bijection between the full old and new auxiliary zero sets is claimed. The ordinary non-pole interfaces, BB-native pole theorem, external Jones coding theorem, and existing general parameter threshold remain in force. No unconditional undecidability claim is introduced.

## Arithmetic and source equations

The source gives

```text
n=q^16, M=q^32,
r=S*(M-n)+T*(M-1),
a=(w*M+1)*r*s*M.
```

Its integral prefix implies `3 | M*r`, hence `3 | a`, without using the final power recovery or integrality of `c`. With `ac=a*c`, the restored or retained row is

```text
pell_d_positive_square^2 - 2*a*d - 2*a*ac + 2*c - 2 = 0.
```

Together with `d^2-(a^2-1)*c^2=1` and the integral shifted trace `d-(a-2)*c=b*w+(4*a-5)*gamma`, the separate proved Pell theorem gives `c,d` integral, including `a=0`. Canonical positive coding witnesses have `c=Y_(2r+1)(a)`, `d=X_(2r+1)(a)`, and the required square root `2*X_(r+1)(a)`.

One extra coordinate is saved by eliminating the source square helper borrowed from the removed c-chart. After its private rows are deleted, `int_c_37` occurs only through `rho*int_c_37=c^2` in two outer equations. Replace those occurrences by `c^2`:

```text
d^2 - ac^2 + c^2 - 1 = 0
E*i_inverse - c^2 = 0.
```

The old helper reconstructs uniquely as `epsilon*c^2`, using the existing `rho*epsilon=1` guard. This step preserves zero values of `c` and introduces no division by a source input.

## The shared contact sum is updated explicitly

The c-block contributes two stored contact weights in the general route or three in the specified route. These are removed from the actual shared sum. The final reciprocal-block weight was already eliminated as `epsilon` minus all the other weights; its expression must therefore change in **all three** retained occurrences: the final pole-input row, inverse row, and gate row.

The independent checker derives all three old and new rows from the eliminated-weight formulas and their original quadratic templates. The retained contact indices are unchanged except for omission of index seven. The root b-block, aggregate spacing, sixteenth endpoint, and common contact coefficients remain. The same finite-family prime, common-point, and BB preparation arguments apply to the reduced tuple; no omitted physical contact is asserted to vanish.

## Complete artifacts

- `c_predicate_deletion.tex` / `.pdf`: arithmetic order, source-square elimination, complete shared-gauge repair, source-instance proof, counts, and scope.
- `c_deleted_general_quadrics.json` / `_certificate.json`: complete 887/750 general system.
- `c_deleted_specified_quadrics.json` / `_certificate.json`: complete 1052/913 specified system.
- `build_c_deletion.py`: deterministic compiler from the frozen v105 preferred tables.
- `verify_c_deletion.py`: independent audit with no compiler import.
- `independent_verification.json`: recorded finite verification results.

From the repository root:

```sh
python undecidability/c_integrality_reduction_v106/build_c_deletion.py
python undecidability/c_integrality_reduction_v106/verify_c_deletion.py
```

The checker pins both predecessor hashes, all occurrences of the 57/72 removed coordinates, both source-square identities, the existing gauge guards, the linear and product source rows, and the half-trace polynomial. It verifies the five changed retained rows, compares the other 744/908 rows literally by named monomials, and checks complete support, coefficient rings, degree, current metadata, and output hashes. The quantified arithmetic theorem is proved and audited separately in `pell_integrality_replacement_v106`; the finite table audit does not establish the retained arithmetic premises.
