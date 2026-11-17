# Independent review of the new 193-coordinate steps

Date: 17 November 2026.

## Scope

This review concerns the changes from the published v73 194-coordinate
presentation to the v74 193-coordinate presentation: the deletion of one unit
coordinate, the resulting invertible rational maps and their boundary behavior,
the coordinate and equation counts, and the compact parameter normalization and
its exact coefficient height. It does not independently reprove the elliptic
group description, contact-height assertion, pole-realization interface,
simultaneous-prime supplier, or the rest of the inherited arithmetic proof.
The defining assertion therefore retains exactly those premises and the
ineffective sufficient parameter threshold of v73.

## Unit deletion and all zero strata

In the source numbering the seven retained unit coordinates satisfy

\[
x_{77}x_{903}=x_{91},\quad x_{90}x_{91}=1,\quad
x_{77}x_{92}=x_{91}^{2},\quad x_{90}x_{901}=x_{91}^{2},\quad
x_{902}=x_{77}x_{91}.
\]

The second equation forces both factors to be nonzero. The first then forces
both of its factors to be nonzero. Set \(u=x_{77}\) and \(v=x_{90}\). The
remaining coordinates are uniquely

\[
x_{91}=v^{-1},\quad x_{903}=(uv)^{-1},\quad
x_{92}=(uv^2)^{-1},\quad x_{901}=v^{-3},\quad x_{902}=u/v.
\]

Conversely these expressions satisfy every unit equation for every
\((u,v)\in(\mathbb Q^*)^2\). Thus the full rational unit variety, not merely
an open subset of it, is a two-dimensional torus. There is no additional
component with a unit coordinate zero. The deleted coordinate is recovered
uniquely as \(x_{78}=u^{-1}=x_{90}x_{903}\).

Every nonunit coordinate change multiplies by a Laurent monomial in these
nonzero units; its inverse negates the exponents. Hence zero values of
nonunit coordinates remain permitted, and this new step introduces no
division by an ordinate, point difference, or other nonunit coordinate.
The input has weight \((0,0)\), so it is fixed. This argument treats all
potential zero strata introduced by this unit deletion; it does not replace
the separate point-chart boundary analysis already in v73.

For clarity, if a physical coordinate has the two presentations
\(z=u^{a_{\rm old}}v^{b_{\rm old}}X_{\rm old}
=u^{a_{\rm new}}v^{b_{\rm new}}X_{\rm new}\), then

\[
X_{\rm old}=u^{a_{\rm new}-a_{\rm old}}
v^{b_{\rm new}-b_{\rm old}}X_{\rm new}.
\]

The updated transfer certificate uses this sign. The previous reporting
field used its opposite; that reporting correction did not change the
physical rows, construction, or polynomial coefficient tables.

The updated `check_transfer.py` was read and executed to an independent
output path. It passed, comparing all 162 physical rows with v73 in both
reference bases, all factor assignments, the seven retained unit exponents,
the five actual guard rows, the coordinate numbering, and the fixed input.

## Exact census and rational equivalence

The coordinate model has 186 distinct nonunit indices and seven disjoint
unit indices. Renumbering gives exactly the indices 1 through 193, with the
input first. All 193 coordinates occur in the expanded compact quartics.
There are 162 physical rational rows and five unit rows, giving 167
quadratic residuals. Thus the total of 193 includes the input and consists
of 192 existential coordinates. The fixed integer \(C=149^N\) is a
coefficient parameter, not an additional quantified coordinate.

All coordinate and row multipliers are nonzero on the proved unit torus.
Over \(\mathbb Q\), a finite sum of squares vanishes if and only if every
square vanishes. The recovered coordinate and inverse diagonal maps
therefore give an input-preserving bijection of the rational solution sets.
No new arithmetic existence statement is needed for this step.

## Compact parameter normalization

The compact transformation is

\[
X_i=C^{-1}Z_i\quad
(i\in\{44,45,46,47,52,53,54,55,56,57,99,100\}),
\qquad X_i=Z_i\quad\text{otherwise}.
\]

It is invertible for every nonzero rational \(C\) and fixes the input.
For each row, multiplication by \(C\) to the negative of its least
parameter exponent after substitution produces the stored compact row.
The row multipliers have exponents 0, 1 or 2, and the resulting term
exponents are all 0 or 1. Each transformed row was compared exactly with
this pullback, using independently written standard-library arithmetic.
This comparison covered all 167 rows in each basis.

The rational zero sets before and after this step are related by the
displayed diagonal bijection. They need not be identical subsets when
their differently scaled coordinates are assigned the same numerical
values. Their rational input projections agree for every nonzero \(C\).

Each compact row has distinct coordinate monomials. Its coefficient gcd
at \(C=149\) is one. For any prime other than 149, changing a coefficient
from \(c149^e\) to \(c149^{Ne}\) does not change its divisibility by that
prime. Divisibility of every coefficient by 149 depends only on its
zero-exponent terms and is also unchanged. This proves row primitivity
for every \(N\ge1\), rather than only at a sampled parameter value.

## Independent coefficient reconstruction and exact height

For each compact basis, an independent sparse integer expansion formed
every ordered pair of terms in each of the 167 row squares and collected
by coordinate monomial and parameter exponent. It imported neither a
producer nor a checker. Every resulting coefficient agreed with the
stored polynomial table. The resulting counts are:

| Basis | Coordinates | Quadratic rows | Coordinate monomials | Parameter-separated terms |
| --- | ---: | ---: | ---: | ---: |
| `compact` | 193 | 167 | 2770 | 2775 |
| `compact_fewer_monomials` | 193 | 167 | 2626 | 2631 |

Both polynomials have coefficient exactly one on the input fourth power.
Consequently their degree is exactly four and their integer content is
one for every \(N\ge1\).

Put

\[
K=126616122944180358034867798936,
\]

\[
L=484991541504995159662206970923766531374664106904986910720,
\qquad \alpha=22201.
\]

For \(J=K\) in the first basis and \(J=L\) in the second, a pure
constant coefficient of absolute value \(J\) and a pure coefficient
\(\alpha C^2\) both occur. Every other pure constant or quadratic
coefficient is bounded by the corresponding one. The maximum absolute
pure linear coefficient is \(M=384444691473074\). Exact integer arithmetic
gives \(M^2\le\alpha J\), so

\[
MC\le\sqrt{\alpha J}\,C\le\max\{J,\alpha C^2\}.
\]

There are exactly five mixed coefficient polynomials in each basis. One
is \(289C^2-578\), which is positive for \(C\ge149\) and bounded by
\(\alpha C^2\). The other four are \(A+C^2\). The values of \(A\) are:

| Basis | First value | Other three values |
| --- | --- | --- |
| `compact` | 17086754668551163707 | 204934086831195733699, 1, 1 |
| `compact_fewer_monomials` | 1747145497790223592810060466409331738555986526175401275 | 204934086831195733699, 1, 1 |

Every one satisfies the checked integer inequality
\(\alpha A\le(\alpha-1)J\). Hence

\[
A+C^2\le \frac{\alpha-1}{\alpha}J+
\frac1\alpha(\alpha C^2)\le\max\{J,\alpha C^2\}.
\]

These inequalities bound every coefficient for every real \(C\ge149\),
and the occurring pure coefficients attain the bound. They establish
the exact heights

\[
\max\{K,149^{2N+2}\}\quad\text{and}\quad
\max\{L,149^{2N+2}\},
\qquad N\ge1.
\]

No coefficient vanishes in this range: pure terms are nonzero, the four
positive mixed terms are positive, and the sole mixed-sign term was
checked above. Thus the support counts hold for the entire parameter
range. Exact integer comparison gives height crossovers 6 and 13.
These are coefficient crossovers only and give no effective sufficient
defining parameter.

The first review identified that the compact-height proof's displayed
list of four \(A\) values described only the first basis while its
surrounding sentence referred to both bases. The table above records
the necessary distinction. This is a statement correction, not a failure
of either height inequality or coefficient table. The machine-readable
review records whether that paper correction is present in the reviewed
source.

## Conclusion and limits

The new unit deletion, input-preserving maps, compact parameter scaling,
counts, degree, content, support and exact coefficient heights pass this
review. No remaining mathematical gap was found in these new algebraic
steps. The defining claim is a transfer from v73 under its retained
premises; this review does not certify those premises as unconditional
theorems and does not supply an effective sufficient value of \(N\).

The 21-variable and 9-variable completeness targets are separate from
this quartic compilation and are not claimed by this review.
