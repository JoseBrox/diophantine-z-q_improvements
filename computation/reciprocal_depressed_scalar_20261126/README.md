# Reciprocal depressed-cubic chart and a smaller specified quartic

This is an exact coefficient/size improvement of the
[161/175-coordinate constructions](../aligned_gate_20261125/README.md).
It does not change their coordinate counts or add an arithmetic hypothesis.
The explicit 175-coordinate member has **74,465 bytes**, below 100 decimal
kB, with maximum coefficient bit length 936 (formerly 1923).
The general 161-coordinate family's sufficient coefficient exponent
remains ineffective. Its size at N=25 is an algebraic fixture only.

## Exact quadratic rechart

Use the parent indices, x37=X^2 and x88=R, and keep the two
literal contact-unit guards and the R-square guard. Retain
\[
 s=2^{20}X^2,\quad w=s+34981/36000,\quad
 W=36000w,\quad K=18536C^2,\quad C=331^N.
\]
In the [depressed scalar proof](../depressed_scalar_20261125/README.md),
\[
 r=(2401+2400s)(343+375s)(1+s)
   =e+900000w^3-(1053721/480)w,
 \qquad e=-1081567619/25920000.
\]
The old two scalar rows recover R=Kr/(r-e) and their old x76
is w^2(R-K). Replace just those two rows and reinterpret x76=T:
\[
 WT=1,\qquad
 (W-3161163T)(R-K)+2163135238\,K T^2=0.
\]
Both are ordinary quadrics (C is a fixed coefficient parameter).
Since W>0 for every rational input, T=1/W. Multiplying the
second equation by W^2 gives
\[
 (W^3-3161163W)(R-K)=-2163135238K.
\]
The exact identity
\[
 r-e=\frac{900000}{36000^3}(W^3-3161163W),
 \qquad
 e=-2163135238\frac{900000}{36000^3}
\]
recovers precisely the old positive scalar, R=Kr/(r-e).
In particular r-e>0 on the entire rational input domain.
Conversely the old scalar gives T=1/W and satisfies both new rows.
All other rows are literally unchanged: x76 had no occurrences
outside the two replaced rows. Thus both directions of the
rational input projection, and all arithmetic preparation, are
preserved for every N>=1. In the new rows the parameter degree
is at most two instead of four.

## Smaller certified exponent

The specified-route proof in
[depressed_scalar_20261125](../depressed_scalar_20261125/README.md)
uses the uniform anchor
\[
 L_N=\lfloor9(2N+1)/4\rfloor+1,\quad A=|a|\ge331^{L_N},
 \quad h(u)<2^{301}331^{-L_N}A .
\]
At N=25 one has L_N=115 and the exact integer inequality
\[
 331^{115}>2^{960}.
\]
This is the same lower bound used at the N=26 endpoint.
Consequently h(u)<2^(-659) A. The unchanged estimates
h(beta)<=h(u)+30 and h(R)<=3h(u)+log K+50
(with log K<400 since 331<512, log 2<0.7)
give h(beta)<A/2 and h(R)<A. The effective weighted
abscissa-sum bound and the strict endpoint comparisons of
[the 178-coordinate proof](../weighted_explicit178_20261124/README.md)
require only these inequalities and A>=2^960. Its two
residual contradictions therefore apply verbatim.
The uniform 331-adic computation, parity of the contact factors
and 2-adic class of R used in the depressed scalar proof do
not depend on changing N from 26 to 25. Hence the new N=25
member is a defining polynomial under exactly the preceding
specified-route arithmetic premises, not merely a fixture.

## Exact coefficient census

| Coordinates | Quadratic residuals | Symbolic parameter terms | Monomials at N=25 | Max coefficient bits | Expanded bytes |
|---|---:|---:|---:|---:|---:|
| 161 | 135 | 2864 | 2858 | 936 | 66222 (fixture) |
| 175 | 147 | 3208 | 3202 | 936 | 74465 (defining member) |

All rows are integral quadrics in the ordinary coordinates.
The sum of their squares has exact degree four and content one,
as follows from the coefficient of x1^4, which is 1.
The complete 175-member expansion is [expanded175.txt](expanded175.txt).
The decimal byte limit is applied to this actual expanded ASCII
file, not the JSON circuit or a compressed representation.

The two literal JSON tables, pinned predecessor blobs and exact
census are in this directory. The separate verifier reconstructs
the two quadratic expressions from the factored identities,
checks all unchanged rows and the nonoccurrence of x76 there,
and independently expands and parses the final polynomial.
No independent proof of the inherited modular, point group,
prime-pattern, trace or BB realization theorems is claimed.
No new variable-count record is claimed.

An executed independent BigInt replay reconstructed both specialized sums
of squares from their rows, checked the two changed rows and the unchanged
rows against the parents, and parsed the full 175-variable TXT expansion
back into the same coefficient dictionary. The results were degree four,
content one, 2,858/3,202 monomials, and maximum coefficient bit length 936.
The separate Python verifier is supplied for reproducibility; it was not
executed in that replay.
