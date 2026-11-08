# A quartic in 392 variables

This package specifies an integer polynomial in **392 total variables**, including its rational input. It has degree **4**, **6,204** nonzero coordinate monomials, content **1**, and coefficient height less than **$2^{1791357}$**. It is the sum of squares of 364 primitive integer quadratic polynomials.

The [quartic paper](../../papers/quartic/quartic392_20261108_v8.pdf), with [editable TeX source](../../papers/quartic/quartic392_20261108_v8.tex), proves that its rational input projection is $\mathbb Z$ under the stated arithmetic inputs. Its coefficient table, degree, variable count and finite numerical certificates are unconditional algebraic assertions.

## The scalar contact

Define

$$
\beta=51(2X+1)^2+2504,\qquad
r=\beta(\beta-1)(\beta-2401)(32\beta+343)(2\beta-1).
$$

Then $r>0$ for every rational input. The construction uses a quadratic equation for

$$
R=\frac{80989^{54929}r}{1+80989^2r}.
$$

Its valuation at 80989 is always either 54929 or 54927. The scalar condition forces a nonzero integer index to be divisible by $80989^{1283919}$. This gives the required size bound and excludes exceptional auxiliary elliptic points before the ratio equations are interpreted. The paper proves both soundness and simultaneous completeness with all relevant denominator conditions.

## Data and exact expressions

| File | Purpose |
|:--|:--|
| `build_quartic392.py` | Exact producer using the Python standard library. |
| `verify_quartic392.py` | Independent equation, coefficient and numerical checker. |
| `check_field_specialization392.py` | Exact imaginary-quadratic specialization checker. |
| `final392/quadratic-system392.json.gz` | All coordinates and 364 primitive quadratic equations. |
| `final392/polynomial392.json.gz` | Complete quartic coefficient table. |
| `final392/construction-report392.json` | Counts, exact maximum-coefficient formula and transformation data. |
| `final392/independent-verification392.json` | Independent verification receipt and hashes. |
| `final392/field-specialization392.json` | Exact field and witness for the field-transfer statement. |
| `upstream/candidate394-ir.json.gz` | Pinned source quadratic system, preserved byte for byte after decompression. |
| `upstream/polynomial394.json.gz` | Pinned source coefficient table, with line endings normalized. |
| `PROVENANCE.json` | Source locations, commit, hashes and verification scope. |

Coordinates have consecutive IDs starting at 1, with coordinate 1 as the input. Their source IDs make the exact transformation auditable.

A term with `parameterPower: e` represents its integer `coefficient` multiplied by $A^e$, where $A=80989^{54929}$ is a fixed integer. Equal coordinate monomials must be combined after specialization. There are 6,225 symbolic terms over $\mathbb Z[A]$ and 6,204 ordinary coordinate monomials. The independent checker verifies this distinction and the exact coefficient-height bound. Further conventions are documented in [Polynomial data formats](../../docs/data_format.md).

## Reproduction

Python 3.10 or newer with its standard library is sufficient. Run from the repository root:

```sh
python3 scripts/restore_data.py
python3 computation/quartic/build_quartic392.py
python3 computation/quartic/verify_quartic392.py
python3 computation/quartic/check_field_specialization392.py
```

Restoration checks the uncompressed byte lengths and hashes of all four gzip files before writing their JSON counterparts. For verification that preserves the published tree, run `python3 scripts/verify.py`; it restores and checks the data in a temporary copy.

The producer writes generated data under `final392`. The independent checker imports neither the producer nor an earlier checker. It reconstructs the complete source polynomial, verifies the changed and retained equations, derives the raw contact identity, expands all 364 squares, and compares every coefficient. It also certifies the fixed prime, the five nonresidue calculations, the integer-input congruences, the contact-height constant and the index-size margin.

The data keep the large fixed integer in exact power notation. The coefficient-height comparison evaluates that integer exactly; decimal expansion is unnecessary for the certificate.

## Field specialization

Setting the input to $1/2$, coordinate 293 to $Y$, and every other coordinate to zero gives $Y^2+D/16$, with $D>0$ specified in `final392/field-specialization392.json`. Thus the same polynomial accepts $1/2$ over $\mathbb Q(\sqrt{-D})$. The checker verifies this identity independently from both the full coefficient table and the quadratic equations.

This is an explicit obstruction to transferring the polynomial unchanged to every number field. The [systems and field-extensions paper](../../papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf) gives the full statement and distinguishes it from the existence of a field-dependent definition.

## Sources and arithmetic scope

The pinned source is Elliot Glazer's Version 13 repository at commit `5bbd74f6a479776a332cbe036809d5dddae63720`. Exact source paths and SHA-256 values appear in [PROVENANCE.json](PROVENANCE.json).

The paper identifies the elliptic group and index-height, contact-height, pole, and simultaneous prime-pattern inputs. It also states the quantitative prime-pattern premise used by the comparison construction. The elementary Lucas estimate and the forced-prime replacement are proved in the paper. The [arithmetic-input page](../../docs/arithmetic_inputs.md) records the precise scope of the global inputs and the finite computational checks.
