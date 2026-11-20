# Busy Beaver coefficients for the 163-variable quartic, and expanded file sizes

## Scope and inherited theorem

This is an exact coefficient specialization of the [163-variable
quartic](../papers/quartic/scalar_point163_179_20261120_v82.tex) under its
explicitly retained arithmetic premises. It is **not** a new proof of an
effective family threshold, nor a claim that the Busy Beaver index
`2^1000` is already certified sufficient.

Define \(\mathrm{BB}(t)\) as the maximal halting time among deterministic
two-symbol, blank-tape Turing machines with at most \(t\) states, under a
fixed standard machine convention. The only property needed for the
defining-family result is \(\mathrm{BB}(t)\to\infty\).

The published coefficient table has 2,789 distinct monomials and exactly
three \(C\)-dependent coefficients when \(C=149^N\):
\[
\begin{array}{c|c}
\text{monomial}&\text{integer coefficient}\\\hline
x_{78}^{2}x_{90}&-6615898 C^2\\
x_{78}x_{90}&-298 C^2\\
x_{78}^2&22201 C^4.
\end{array}
\]
All remaining 2,786 coefficients are fixed integers. They are printed
in the [published table](../computation/variable_reductions_v82/general/quartic163/polynomial.json)
and in the [60,905-byte \(N=1\) fixture](../computation/expanded_text_v84/quartic163-N1.txt).

For \(M=\mathrm{BB}(t)\), the entire specialized polynomial is therefore
specified by
\[
\boxed{
\begin{aligned}
F^{\rm BB}_t=F_1
&-6615898(149^{2M}-149^2)x_{78}^{2}x_{90}\\
&-298(149^{2M}-149^2)x_{78}x_{90}\\
&+22201(149^{4M}-149^4)x_{78}^2.
\end{aligned}}
\]
The [single-line symbolic file](../computation/expanded_text_v84/quartic163-BB_t-symbolic.txt)
lists **every monomial** but leaves the three Busy Beaver coefficients
symbolic. It is not a decimal-coefficient expansion.

**Defining statement (eventual, not fixed-index).** The v82 theorem
asserts that there is an integer \(N_0\) such that \(F_N\) defines
\(\mathbb Z\) in \(\mathbb Q\) for every fixed \(N\ge N_0\), under the
retained arithmetic premises. Since \(\mathrm{BB}(t)\) is unbounded and
nondecreasing, there is a \(t_0\) such that \(F_t^{\rm BB}\) defines
\(\mathbb Z\) for every fixed \(t\ge t_0\). The coefficients are
completely specified in terms of \(\mathrm{BB}(t)\); the total degree is
exactly four, the content is one, and the variable count is 163,
including the input \(X\).

**Unresolved effectivity.** The constant \(N_0\) is not effectively
bounded by the current proof: the uniform weighted elliptic-trace
estimate invokes an ineffective additive constant. Hence **no
specific numeral \(t\)**, including \(t=2^{1000}\), is certified by the
argument. The eventual family is a theorem, but no single fixed-index
163-variable Busy Beaver polynomial has been certified here. The
179-variable quartic remains the record with fully specified,
certified defining coefficients. No claim to an explicit *numerical*
163-variable defining polynomial follows just from the growth of
Busy Beaver.

## Fully expanded decimal text sizes

Here a kilobyte is **1,000 bytes**, not 1,024 bytes. A compact
expanded TXT is one ASCII line, with no spaces or final newline,
using `X` for coordinate one, `x2`, ..., `xN` for the remaining
coordinates, `*` for products, `^` for exponents, and **decimal**
integer coefficients. Like monomials are collected. These are
measurements of the complete polynomial, not of the JSON table.

| Polynomial | Parameters | Monomials | Exact decimal TXT size |
|---|---|---:|---:|
| [163-variable family fixture](../computation/expanded_text_v84/quartic163-N1.txt) | \(N=1\), **not certified defining** | 2789 | **60,905 bytes = 60.905 kB** |
| [179-variable fixed polynomial](../computation/expanded_text_v84/quartic179.txt) | Fixed defining coefficients | 3036 | **66,903 bytes = 66.903 kB** |
| [56-variable ordinary-abc fixture](../computation/expanded_text_v84/quartic56-B3.txt) | \(B=3\), **not certified defining** | 809 | **11,562 bytes = 11.562 kB** |

The symbolic 163-variable Busy Beaver file has exactly 60,929 ASCII
bytes (60.929 kB) but does **not** count as a decimal-coefficient file.

Define \(d(m)=\lfloor\log_{10}(m)\rfloor+1\) for positive integers \(m\).
For **any \(N\ge1\)**, the exact number of bytes in the 163-variable
fully decimal-expanded TXT under the convention above is
\[
\boxed{\ S_{163}(N)=60872+
 d(6615898\cdot149^{2N})+
 d(298\cdot149^{2N})+
 d(22201\cdot149^{4N}).\ }
\]
The 60,872-byte term includes all other coefficients, signs, and
monomials. In particular, substituting \(N=\mathrm{BB}(t)\) gives an
**exact numerical-file-size formula in terms of Busy Beaver**:
\[
S_{163}^{\rm BB}(t)
=17.385490147298192\,\mathrm{BB}(t)+O(1)
\quad\text{bytes},
\]
or about \(0.01738549\,\mathrm{BB}(t)\) kB, plus the fixed
60.872 kB notation cost. No astronomically long decimal file was
claimed to have been generated.

For the large finite-determinant constructions, no decimal expansion
is feasible from the currently published circuits. The table in
[README](../README.md) instead supplies deliberately loose
**fixture-only upper bounds**, based on the recorded support bounds
and coefficient one-norm majorants:

| Route | Stored fixture | Strict upper bound, kB | Defining fixture? |
|---|---|---:|---|
| 25 variables | \(L=143\) | \(<2^{848}\) | No |
| 27 variables | \(L=143\) | \(<2^{965}\) | Yes |
| 11 variables | \(B=3\) | \(<2^{227}\) | No |

These bounds are not measured sizes or estimates of what a first
defining member would occupy. They only bound the particular indicated
circuit member. If \(s\) is the strict power-of-two support exponent
and \(E\) the published upper bound for \(\log_2\ell^1\)-coefficient
norm, then every coefficient has at most
\(\lfloor 31E/100\rfloor+2\) decimal digits because
\(\log_{10}(2)<31/100\). Bounding the length of the variable
monomial and multiplication signs gives the stated powers of two.

## Reproduction and checks

The complete source-independent published JSON coefficient tables
are unchanged. Run:

```sh
python -B computation/expanded_text_v84/build.py
python -B computation/expanded_text_v84/build.py --output /tmp/expanded-v84
python -B scripts/verify_v84.py
```

The first command prints sizes without writing; the second
regenerates the four files. The verifier **independently parses**
each decimal TXT back to its integer coefficient map, compares it
with the original table after parameter substitution and coalescing,
checks the Busy Beaver specialization at \(N=1\), authenticates the
ASCII files and proves the fixture-only size bounds from the stored
majorants. [Machine-readable sizes and SHA-1 Git blob identifiers](../computation/expanded_text_v84/size_report.json)
allow byte-for-byte reproduction. The checks verify coefficients and
file lengths, not the inherited arithmetic existence theorems.
