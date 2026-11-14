# Correction of the printed reference-chart coefficient table

The v26 printed paper `compressed_reference_20261113_v26.pdf` omitted the term

`(171357/235298 + (2519877/7529536)*sqrt(2))*f*S`

from the polynomial L in `M*w+L=0`. Its displayed table instead listed zero coefficients of S*T and T². Without the omitted f*S term, the weight-recovery ideal identity is false. This is a genuine formula error in the printed presentation, not an optional hypothesis or a harmless alternate normalization.

## Repair and affected applications

The original six rational reference rows in the retained 212-coordinate table contain this term. The corrected v27 field equations are reconstructed against all six rows, including their half-imaginary-component conventions. The current coefficient table has seven terms in L, with the restored f*S term.

The corrected paper proves the full reference-chart equivalence. Its exact certificate contains five ideal-membership identities and two converse function-field identities, together with the exceptional quintic factorization, discriminant norm and residual. A separate standard-library checker reconstructs the targets and rejects deliberate deletion of the f*S term, corruption of an equation, and corruption of a certificate.

The current 79-variable construction has been regenerated from these corrected equations. It has 79 coordinates, 71 quadratic rows and 1,139 ordinary monomials. The previously announced count is unchanged, but the old v26 numerical ZIP was unavailable in this session: no byte comparison with that unavailable data is claimed. The current source, full coefficient table and proof are the operative version.

The new 260-variable and 224-variable applications use this same corrected chart and have separately checked complete row substitutions. The 204-variable construction retains the original six reference rows directly; none was replaced by the incomplete printed v26 table.

The new checks do not revise the historical v26 report into a claim of full external-source or non-author acceptance. The mathematical findings, corrected source, current consumers and finite verification scopes are kept distinct.
