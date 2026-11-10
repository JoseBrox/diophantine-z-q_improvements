# Independent exact audit of the direct-input thirteen-variable sources

## Result and scope

Both source specifications in
`computation/few_variables/direct_input13_v22/` pass the independent exact
algebraic audit. This audit does not reprove the arithmetic height argument or
abc. It checks that the literal finite specifications express the intended
changed source, preserve its guarded rational projection through the existing
finite-algebra theorem, and have the stated degree and support upper bounds.

The audit imports neither the new source producer nor its new checkers. It uses
the existing independent source-conversion checker and active finite-algebra
checker, then adds an independent comparison of all source expression trees,
exact sparse polynomial identities for the changes, and a direct summation of
the separator-capped monomial count. No numerical sampling is used.

## Semantic change

Write

\[
\beta=2X^2+B,\qquad T=\operatorname{Tr}_{\mathbb Q(\sqrt2)/\mathbb Q}x(A),
\]

and retain the three point roles \(A,H,U\). The translations remain
\(V_0=H-P\) and \(V_1=U-A\), and

\[
L=\frac{z(U)}{z(H)},\qquad
L'=\sigma\!\left(\frac{z(V_1)}{z(V_0)}\right).
\]

The six local tests are exactly

\[
f(H),\quad f(U),\quad\sigma f(V_0),\quad\sigma f(V_1),\quad
L-L',\quad L-X.
\]

Thus the final test compares the elliptic index to \(X\), not to \(\beta\).
The positive quantity \(\beta\) appears in the second height scale
\(\beta^d+T^d\), with \(d=4\) or \(6\). In particular, the nonidentity
point \(A=[n]P\) has not been removed or repurposed: the same three point
quartics, translation formulas and guards occur in the literal source.

Every finite relation, guard and event of the predecessor weak-abc source
agrees identically with the new source after exactly these two replacements:

1. Replace the real numerator of \(L-\beta\) by the real numerator of
   \(L-X\), keeping its denominator and imaginary component.
2. Replace \(\beta^8+T^8\) by \(\beta^d+T^d\).

This is an equality of source formulas under the stated substitutions, not a
claim that the old and new arithmetic input projections are equal before their
respective soundness and completeness proofs. The replacements were also
checked directly as sparse polynomial identities with \(B\) an indeterminate.

## Finite algebra and the zero input

The source has twelve retained rational coordinates and five finite monic
relations of degrees \(4,4,4,2,2\). The point algebra has rank \(64\), the
full algebra rank \(256\), and one separating coordinate gives thirteen total
polynomial variables. The exact conversion checks all three point quartics,
their derivatives and automatic guards, both rational-square clearings, and
the complete materialized guard. The active-algebra checker verifies that the
guard is homogeneous of degree one in each pole generator and that each pole
radicand belongs to the point algebra.

If \(Q_B\) is the exact polynomial supplied by that elimination theorem, the
final specification is literally

\[
F_B(X,\mathbf y)=XQ_B(X,\mathbf y).
\]

Over \(\mathbb Q\), if \(X\ne0\), the equation \(F_B=0\) is equivalent to
\(Q_B=0\). If \(X=0\), every assignment of the remaining variables solves
\(F_B=0\). Therefore this operation adds precisely the zero input to the
guarded-source projection. It does not require the source to realize the
excluded identity point \(A=O\), introduce a new coordinate, or clear a
denominator. Multiplication by \(X\) shifts each monomial exponent injectively,
so it preserves the coefficient multiset and the number of nonzero monomials.

The separate arithmetic audit by the height agent covers completeness for
every nonzero integer index, including negative and even indices and
\(n=\pm1\). No individual comparison test is required to be nonzero.

## Verified numerical bounds

| Source | Extra abc exponent | Scale power | Degree upper bound for \(F_B\) | Support upper bound |
|---|---:|---:|---:|---:|
| `abc` | \(16/15\) | \(4\) | \(11212784195585<2^{44}\) | \(<2^{507}\) |
| `weak` | \(121/100\) | \(6\) | \(11774654098433<2^{44}\) | \(<2^{508}\) |

The degree bounds are obtained by independently summing all sixty-four
separation cases. The separator degree is bounded by

\[
E=63(2\cdot256)+256=32512.
\]

For the base degree bound \(D\), the support count was recomputed directly as

\[
\sum_{j=0}^{E}\binom{D-j+12}{12}
=\binom{D+13}{13}-\binom{D-E+12}{13}.
\]

This is an upper bound; the determinant polynomials have not been expanded
into their monomial tables, and these numbers are not asserted to be their
exact degrees or exact support sizes.

For the supplied coefficient fixture \(B=3\), the verified upper bounds on
\(\log_2\|F_B\|_1\) are \(27756172773305\) and
\(28598607557817\), respectively. Both are below \(2^{45}\). **The fixture
\(B=3\) is not certified to exceed the ineffective defining threshold.**
These coefficient bounds therefore describe the supplied algebraic fixtures,
not an effectively specified polynomial already certified to define
\(\mathbb Z\). The degree estimates are uniform in the fixed coefficient
\(B\), since it has degree weight zero throughout.

## Reproduction

From any working directory, run:

```sh
python3 /workspace/scratch/191d4e871efa/checkpoints/quartic_v22/direct_input13_audit.py
```

The machine-readable result is `direct_input13_audit.json` beside the checker.
It pins the source, integer, active and final specifications, the predecessor
source, the audit code, and all reused independent checker modules by SHA256.
It writes only its own checkpoint output and does not modify the producer's
source, specifications or reports.
