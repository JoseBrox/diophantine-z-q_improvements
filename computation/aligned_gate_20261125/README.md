# Aligned contact gates: 161 and 175 variables

## Result and assumptions

The two depressed-scalar constructions in [the preceding directory](../depressed_scalar_20261125/README.md)
admit exact coordinate reductions from 162 to 161 and from 177 to 175,
respectively, with the same arithmetic premises, including all inherited
elliptic, modular, height and prime-pattern inputs. The first remains an
existence family with ineffective sufficiently large N; the second is a
fixed polynomial at C=331^26. Counts include the input coordinate.

No new Diophantine or number-theoretic assertion is needed: this is an
isomorphism of the rational solution sets of the guarded quadratic systems,
preserving the input and parameter.

| system | variables | quadratic residuals | symbolic terms in sum of squares | monomials at N=26 | coefficient height at N=26 (bits) |
|---|---:|---:|---:|---:|---:|
| general | 161 | 135 | 2877 | 2860 | 1923 |
| explicit | 175 | 147 | 3221 | 3204 | 1923 |

The expanded explicit polynomial is [expanded175.txt](expanded175.txt)
(77,928 bytes). Both sums of squares are primitive of exact degree four,
as witnessed by the coefficient 1 of x1^4. The N=26 instance of the first
family is a size illustration only, not a certified defining instance.

## Transformation

In this discussion use the **parent indices**, before deleting and
renumbering coordinates. Write c for the contact gauge, u=c^(-1), and
v=u^2. Both unit residuals are retained literally. In each certificate
`chg[j]=e` means that old coordinate j is replaced by u^e times the new
coordinate j. The listed `exps[row]=f` means divide the transformed
residual by u^f. All omitted exponents are zero. Negative exponents are
legitimate only because cu=1; powers are represented by the existing
c,u,v registers. After these changes all rows are still quadratic.

### 162 -> 161

Here (c,u,v)=(x158,x159,x160). Multiply the old coordinates 69,70,71,157
by u relative to the new ones, divide the three detector-1 contact
power/combination/relation rows by u^2, and divide shared.inverse1 by u.
The two gate equations become

    v(2x63-x152-x156+2u-v) - x155^2 = 0,
    v(2x72+x152-x157+u-v) - x155^2 = 0.

Subtract and divide by v (nonzero): this gives

    x72 = x63 - x152 + (x157-x156+u)/2.

Delete shared.gate1 and replace x72 by this affine expression in all
remaining rows. Inserting that expression recovers the deleted row
identically on the retained gate equation. Renumber consecutively.

### 177 -> 175

Here (c,u,v)=(x160,x161,x162). The complete gauge and row multipliers
are recorded in certificate175.json. In particular the first contact
chart is shifted by u^(-1), the other two by u; their gate and pole
charts are rescaled compatibly. The three gates become

    2x63-x152-x156^2-x157+2u-v = 0,
    2x72-x153-x156^2-x158+2u-v = 0,
    2x171+x152+x153-x156^2-x159+u-v = 0.

The two affine substitutions are

    x72  = x63 + (x153+x158-x152-x157)/2,
    x171 = x63 + (-2x152-x153+x159+u-x157)/2.

Delete shared.gate1 and shared.gate2 and their two variables. The
remaining gate implies both deleted gates after substitution. Clear
constant denominators, normalize integral rows and renumber consecutively.
The complete table is in quartic175.json. C remains fixed at 331^26.

## Verification and general principle

The certificates pin the exact parent blobs and specify all substitutions.
The independent verifier embeds both parent and child into the Laurent
polynomial ring in u (using c=u^(-1), v=u^2), with coefficients in Q[C]
and the other witness coordinates. It checks proportionality by a
nonzero rational constant of each transformed parent residual with its
child counterpart, including the equality of the deleted gates with the
retained gate after insertion. It checks the two unit equations separately
as literal quadratics; they must not be replaced by their identically zero
Laurent images. It also checks degree, full variable coverage, term
counts, specialization and the explicit expansion. This verifies both
directions of the rational solution-set correspondence, not just
soundness on generic coordinates. The checks do not independently
validate the inherited arithmetic premises.

More generally, if a common monomial gauge converts m gates to
G_j=H+L_j, where H is shared and each difference L_j-L_0 is affine in
the ordinary coordinates, independent affine pivots allow elimination
of up to m-1 variables. The proof requires the gauge monomial to be
nonzero on every solution and affine substitutions to keep all remaining
rows quadratic. Simply subtracting gates with unaligned weights need
not yield a valid elimination.

## Reproduction

Run from the repository root:

    python3 computation/aligned_gate_20261125/verify.py

An independent BigInt Laurent-ring replay during the construction
verified all 136 and 149 parent equations (including the two literal
unit guards), the three redundant gate identities, and the exact
sum-of-squares coefficient counts and specialization heights. A draft
generator had simplified the unit equations to zero when reducing
Laurent powers; the final tables restore both unit equations and the
verifier checks them separately.
