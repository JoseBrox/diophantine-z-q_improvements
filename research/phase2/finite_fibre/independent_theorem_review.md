# Independent review of the explicit finite-algebra theorem and bounds

Reviewed `finite_algebra_polynomial.tex` SHA-256:
`ff856054afcf07ee596fe99f1cb97761feb1fee76d4c4d378621cd4630389358`.
Reviewed `coefficient_bounds.tex` SHA-256:
`82da66e427dca20949699c5e377072c1439960698c11a885ee6bc234aabc2caf`.

The reciprocal residual identity is exact. At its rational zero, the
leading coefficient, resultant, and reciprocal coordinate are nonzero;
the resulting root of det(I-VM) is simple. A simple root forces a
one-dimensional rational kernel. Every commuting generator multiplication
matrix preserves that kernel, hence acts on it by a rational scalar.
Those scalars satisfy all monic relations. No reducedness assumption on
the rest of the fiber is needed for this reverse implication.

For the adjugate selector, the matrix identity gives
`M adj(I-VM)=V^-1 adj(I-VM)` at the root. The determinant derivative
therefore gives `Tr(adj(I-VM))=-V H'(V)!=0`. Every column lies in
the common eigenline, so `Tr(M_E adj(I-VM))` is exactly E evaluated
at the selected rational point times this nonzero scalar. This proves
the closed-condition selection.

For the forward implication, local components where G vanishes contribute
1 to det(I-VM), including nonreduced components. All other components
have length one by hypothesis. The fixed family of linear forms in the
generators excludes at most `m*n*(n+1)/2` parameter values, counting
zero values and pairwise collisions. One of the stipulated integers thus
separates every retained point and gives a squarefree nonconstant H.
The degree-drop cases in the finite product correctly cover its actual
degree. No unresolved generic-specialization step remains in this theorem.

The coefficient-bound proof is valid at the level reviewed. Monic
reduction never increases the assigned weighted degree. The maximum
column-sum coefficient norm is submultiplicative; the block companion
description gives the stated recursive bounds and is unchanged by free
monic extensions. Determinant norms are bounded by the product of column
sums, without a further factorial. Differentiating in a matrix direction
gives exactly the trace residual and its n-column bound.

One useful explicit justification for the reciprocal-residual bound is
that its j-th coefficient equals
`a_(d-j) * a_d^(3j-1) * Res^j`. Its logarithmic norm is at most
`j*(3*B_H+B_Res)=j*B_L`, and the degree calculation is identical.
This avoids treating division by a_d as norm division. The stated
reversal and sum-of-squares estimates then follow.

Finally the exact finite-factor total is the binomial expansion of
the sum over the 86 masks of
`n_k*(1+297*n_k*(n_k+1)/2)` with `n_k=4^211*2^k`, times 54272.
It yields the displayed powers 3^86, 5^86, and 9^86. This review has
not independently recomputed the numerical coefficient-DAG weight table
or the emitted 558-variable specification. Those are separate checks.

## Fixed elliptic exclusion coefficients

The separate file `fixed_anchor_height.tex` gives a full elementary proof
of the coefficient-height estimates for the indexed finite exclusion.
It uses primitive common-denominator triples in Q(sqrt(2)), handles the
identity and exceptional additions explicitly, and gives
`h_0(x(nP))<=17*n^8`. The multiplication-matrix norm of the product
through n=M is at most `2^((2*b+38)*M^9)` when the three input numerator
and denominator matrices have norm at most `2^b`.

The independent standard-library script `check_fixed_anchor_height.py`
checks the fixed curve data and compares binary multiplication with
repeated addition for n=1,...,24, exactly over Q(sqrt(2)). Its receipt is
`fixed-anchor-height-verification.json`. This finite computation checks
the stated scope only; the uniform bounds follow from the written proof.
Neither the proof nor this check expands the enormous indexed product.
