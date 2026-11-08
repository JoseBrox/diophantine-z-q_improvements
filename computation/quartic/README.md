# Quartics defining the integers over the rationals

This package contains a fully specified **389-variable quartic** and an exact **317-variable quartic family**. Every count includes the input coordinate. Their integer-projection theorems retain the arithmetic premises stated in the accompanying papers, including the quantitative weighted prime-selection premise. The equations, coefficient tables and finite verification results are exact algebraic data.

| Construction | Total variables | Degree | Quadratic equations | Nonzero coordinate monomials | Coefficient statement |
|:--|--:|--:|--:|--:|:--|
| Fully specified polynomial | 389 | 4 | 361 | 6,198 | All coefficients fixed; height below $2^{1791357}$ |
| Aggregate trace family $P_N$ | 317 | 4 | 291 | 5,032 for $N\ge27464$ | Height below $2^{1520}80989^{4N+2}$ |

Both polynomials have integer content one. For the family, degree four and content one hold for every integer $N\ge1$.

## The fully specified quartic

The [389-variable paper](../../papers/quartic/quartic389_20261108_v9.pdf), with [editable TeX source](../../papers/quartic/quartic389_20261108_v9.tex), proves that the polynomial's rational input projection is $\mathbb Z$ under the retained arithmetic inputs.

The construction removes three trace inverse coordinates from the pinned 392-variable baseline. At every contact prime needed by a height detector, the remaining equations already force the relevant denominator to be nonzero. When the contact radical is empty, the required divisibility consequence is automatic. The proof includes the degenerate detector value and retains the original completeness construction.

The coefficient table uses the fixed integer

$$
A=80989^{54929}.
$$

It contains 6,219 terms when powers of $A$ are listed separately, and 6,198 nonzero coordinate monomials after collection. The largest coefficient has exactly 1,791,357 binary digits and is three smaller than the largest coefficient of the baseline polynomial.

The independent normalization checker verifies the actual affine coordinate dictionary of all three detectors. Stored gate names alone do not specify their mathematical values: the retained substitutions recover exactly the scales $1,C_0^2,(1+C_1^2)^2$, the detector weights, and the pole inputs.

## The 317-variable family

The [317-variable paper](../../papers/quartic_existence/quartic317_family_20261108_v9.pdf), with [editable TeX source](../../papers/quartic_existence/quartic317_family_20261108_v9.tex), proves

$$
\exists N_0\ge27464\ \forall N\ge N_0:\quad
x\in\mathbb Z\ \Longleftrightarrow
\exists\boldsymbol y\in\mathbb Q^{316},\ P_N(x,\boldsymbol y)=0.
$$

Its fixed coefficient parameter is $A_N=80989^{2N+1}$. Neither $A_N$ nor $N$ is a quantified variable. The sufficient threshold $N_0$ is ineffective: the proof does not identify a numerical member that defines the integers. The bound $N\ge27464$ in the monomial count is an algebraic support bound, not a sufficient threshold for the integer-projection theorem.

The [aggregate-trace height theorem](../../papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) allows the two scales $1,F^2$, where

$$
F=\frac12\operatorname{Tr}_{\mathbb Q(\sqrt2)/\mathbb Q}
\bigl(x(Q_1)+x(Q_2)+x(Q_3)+x(Q_4)\bigr).
$$

Replacing the field product by this sum and deleting one height detector saves 60 coordinates. The theorem requires no parity condition, so the four odd-index certificates can also be removed, saving 12 more coordinates. The basic square-abscissa charts still force nonzero integer elliptic indices.

The family uses $\beta=51X^2+2504$ and scalar shift $9792$. Integrality of $\beta$ implies integrality of $X$, and the new shift preserves the necessary local squareclasses at $2,3,17$. These changes are verified through an invertible affine input substitution and the complete retained equations.

There are 5,047 terms over $\mathbb Z[A_N]$ and 5,032 ordinary monomials for $N\ge27464$. Every coefficient is a polynomial of degree at most two in $A_N$.

## Files and dependencies

| File or directory | Role |
|:--|:--|
| `build_quartic389.py` | Constructs the fully specified quartic from the pinned baseline. |
| `check_quartic389.py` | Independently checks every retained equation and every coefficient in two ways. |
| `verify_detector_normalizations.py` | Checks the complete affine detector identities over the rationals. |
| `final389/` | Complete quadratic system, full quartic table, construction report and verification certificates. |
| `build_quartic317.py`, `check_quartic317.py` | Construct and independently verify the final aggregate trace family. |
| `family317/` | Complete quadratic family, full quartic family table, construction report and verification certificate. |
| `build_quartic329.py`, `check_quartic329.py`, `family329/` | Internal algebraic construction stage used to reproduce the 317-variable family. |
| `baseline392/*.json.gz` | Two pinned baseline archives, decompressed and checked directly by the new builders. |
| `build_quartic392.py`, `verify_quartic392.py`, `final392/`, `upstream/` | Reproduction of the baseline from the pinned upstream 394-variable source. |
| `check_field_specialization392.py` | Verifies the baseline's separate number-field specialization certificate. |
| `PROVENANCE.json` | Dependency chain, exact source locations, formats, hashes and proof references. |

The 392-variable baseline and the 329-variable stage are replication dependencies. The final results presented here are the specified 389-variable polynomial and the 317-variable existence family.

Coordinates have consecutive IDs starting at 1, with coordinate 1 as the input. Source IDs identify the retained equations and coordinates across transformations. Coefficients are decimal strings, and powers of the fixed integer parameter are stored separately. [Polynomial data formats](../../docs/data_format.md) gives the complete conventions.

## Reproduction

Python 3.10 or newer and its standard library suffice. From the repository root, the complete verifier checks the publication manifest and reproduces all constructions in a temporary copy:

```sh
python3 scripts/verify.py
```

For the quartic constructions alone, run from this directory:

```sh
python3 build_quartic389.py
python3 check_quartic389.py
python3 verify_detector_normalizations.py
python3 build_quartic329.py
python3 check_quartic329.py
python3 build_quartic317.py
python3 check_quartic317.py
```

These commands read the pinned `baseline392` archives directly and regenerate `final389`, `family329` and `family317`. The 329-variable stage must precede the 317-variable producer. No external computer algebra package or manual expansion of the large fixed integer is required.

The 389-variable checker reconstructs the baseline sum of squares, verifies the three deleted coordinates have no other uses, checks every retained row, and compares the complete new table both by direct squaring and by subtraction of the deleted squares. The 317-variable checker applies the inverse affine input map to every retained row, checks removal of the twelve private odd-chart coordinates, reconstructs the full coefficient table, and independently verifies the new input label and local congruences.

To reproduce the baseline from its upstream source, run these commands from the repository root:

```sh
python3 scripts/restore_data.py
python3 computation/quartic/build_quartic392.py
python3 computation/quartic/verify_quartic392.py
python3 computation/quartic/check_field_specialization392.py
```

The restoration step checks the uncompressed hashes and byte lengths of the four baseline/upstream archives. The top-level verifier includes these checks automatically. The baseline's field-specialization certificate concerns that particular 392-variable polynomial and supports the separate [systems and field-extensions paper](../../papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf).

## Sources and arithmetic scope

The direct baseline is the specified 392-variable construction at commit `de7aa60dd1794d7ea62a8a83cdc4bfd22380c74f` of this project. Its upstream arithmetic source is Elliot Glazer's Version 13 repository at commit `5bbd74f6a479776a332cbe036809d5dddae63720`. Exact paths and hashes appear in [PROVENANCE.json](PROVENANCE.json).

The [arithmetic-input page](../../docs/arithmetic_inputs.md) states the elliptic group, contact-height, pole, and simultaneous prime-pattern premises and the additional quantitative premise retained for quartics. The aggregate trace theorem is proved separately; its ineffective additive constant accounts for the unknown family threshold. Finite computation verifies the algebra and stated numerical certificates, not the global arithmetic premises or an effective value of that threshold.
