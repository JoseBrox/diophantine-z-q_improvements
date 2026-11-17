# The explicit-polynomial record

The project keeps two records for quartic Diophantine definitions of the integers in the rationals. One allows coefficients given by a formula (for example in terms of a Busy Beaver value). The other is the **explicit** record: a polynomial that can simply be written down. This page says what counts as explicit, so that the record is decided by a measurement and not by judgement.

## The rule

A pull request may claim the explicit record only if both of the following hold.

1. **It is a new record, justified by the project's usual standards.** The polynomial has fewer variables than the current explicit record, it is a quartic with integer coefficients whose rational zero projection is exactly the integers, and the claim comes with a complete proof and reproducible computations under the [release policy](../release-policy.md) and the [review guide](../research-review/README.md).
2. **Written out in plain algebraic notation, it is under 100,000 bytes.** The notation is defined below and the size is whatever `measure_plain_text.py` reports. The limit is strict: 100,000 bytes or more does not qualify.

The number of variables is the number of variables that occur, including the input.

The limit is a convention of this repository. It is not a mathematical statement and does not belong in the manuscript; a manuscript may state a polynomial's size in this notation.

A polynomial that meets the first condition but not the second is still a result worth recording. It is recorded as such, not as the explicit record.

## Plain algebraic notation

The polynomial is written fully expanded, as one line of ASCII text.

- Variables are `x1`, `x2`, …, `xn`, in the coordinate order of the table the polynomial comes from. The input is `x1`.
- Like terms are combined and zero terms are dropped.
- Within a term, variables appear in increasing index order. A repeated variable is written with `^2`, `^3` or `^4`; exponent one is not written.
- `*` is multiplication, between the coefficient and the variables and between variables.
- Coefficients are integers in base ten, with no leading zeros, separators, exponents or abbreviations of any kind. A coefficient of magnitude one is omitted on a term that has variables.
- Terms are ordered by their lists of variable indices, each written out with repetition and sorted (so `x1^2*x47` is `1, 1, 47`), compared as lists of integers. The constant term, whose list is empty, comes first.
- A negative term begins with `-`. A positive term begins with `+`, except the first term of the polynomial.
- There are no spaces, line breaks, parentheses, names, declarations or trailing newline.

Example: `17+x1^4-2*x1^2*x47+x2*x250`.

Nothing may be factored, compressed, or expressed through a parameter, a circuit or a sum of squares. The text is the polynomial.

## Measuring

```sh
python -B docs/explicit-record/measure_plain_text.py polynomial.json --output polynomial.txt
```

The input is a JSON file with an integer `variables` and a list `terms`; each term has `monomial`, a list of one-based variable indices with repetition, and `coefficient`, a decimal integer string. The program prints the number of variables that occur, the number of monomials, the degree, the size in bytes, the SHA-256 of the text, and whether it is under the limit. It exits with status 1 if the polynomial is over the limit. `--verify-text FILE` additionally checks that an existing text file equals the canonical text byte for byte.

The program is the reference implementation of the notation above. It uses only the Python standard library; `test_measure_plain_text.py` holds its tests.

A claim should include the JSON, the text, and the program's printed report.
