# Research directions and proved constraints

The priority is total coordinates, then degree, then coefficient height. Every count includes the input. The leading results and their precise conditional scope are in the [main table](../README.md#main-results).

## Fewer variables

The weighted finite-algebra compiler already eliminates the finite algebraic choices with one rational coordinate. Its bounds are controlled by the algebra rank, the weighted degree of the guarded multiplication element, and the number of separating selectors. Reducing those quantities can improve degree and height, but reducing the total coordinate count requires removing a retained scalar or point parameter, or a different arithmetic presentation.

The most direct target is the retained pole-witness presentation. A reduction must preserve both soundness at negative odd valuations and simultaneous realization at every prescribed finite and real place. A proposed rational parameterization must be checked at zero and exceptional strata before any denominator is cancelled. The existing one-parameter elliptic-chart obstruction applies to finite presentations of the specified infinite point set; it does not prove a general coordinate lower bound for defining the integers.

An effective one-scalar height comparison on the actual elliptic index tuples would make the 27-variable family explicit and could make the 297-variable quartic explicit. The general trace-height theorem supplies an ineffective additive constant. The effective two-component bound is sufficient for the explicit 29-variable and 342-variable constructions. A generic low-degree scalar height function on all rational pairs cannot fill this gap: the scalar-height paper proves an obstruction through degree three. A theorem restricted to the actual index tuples remains possible.

The coprime-index sum estimate has stronger effective constants, but coprimality must be proved before invoking it. Deducing it only after the Lucas equation would make a completeness or soundness argument circular if used earlier.

## Quartic systems

Shared powers now provide the weights for orders 1, 10, and 40 with quadratic equations. Further savings should target simultaneous reuse of formal-logarithm powers, redundant linear coordinates, and the pole equations, while retaining a proof for all rational solutions. The complete coefficient tables make affine elimination and circuit comparisons exact. A finite search among chosen groupings or arithmetic circuits gives a conclusion only for that specified search class.

The input-map obstruction rules out integer quadratic maps satisfying all three of these requirements: rational integrality reflection, odd values on all integers, and the uncorrected five-contact square condition at 2. Routes with a scalar correction, unrestricted parity, or a different contact construction remain open. The present quartics use a corrected scalar normalization.

The exact coefficient height is the coefficient $A_N^2+1$ of the normalized contact coordinate squared. Further height improvement with the same variable count and degree can come from reducing the effective required exponent, changing the fixed prime, or reducing the way the coefficient enters the quadratic normalizer. Any such change must repeat the global height comparison and local squareclass checks.

## Rings of integers in their fraction fields

The reduction to defining the rational subfield is exact under a separate definition of the integers over the rationals. Relative norm-image and trace-graph definitions are equivalent targets, with explicit coordinate bounds. Writing a norm form with unrestricted extension-field coordinates does not achieve such a definition: its intended base-field coordinates still need restriction.

A useful independent sufficient condition is a Diophantine subset $S\subseteq\mathcal O_K$ containing $\mathbb Z$. For an integral basis $\omega_1,\ldots,\omega_n$, one has $\mathcal O_K=\sum_i\omega_iS$. Constructing such a set with unrestricted field witnesses would solve the field's problem without first defining the exact rational subfield.

Rank-stable elliptic curves produce infinite Diophantine subsets of the rational subfield. The concrete valuation example in the number-field paper shows why ratios and multiplicative combinations of arbitrary abscissa sets need not cover it. Additive constructions or additional arithmetic restrictions must be proved, not inferred from infinitude.

For a counterexample, failure of any one formula, or of a fixed finite list, is insufficient. A genuine counterexample must exclude every existential formula for that field. Descent shows that such failure persists under finite extensions and would yield a totally imaginary Galois counterexample. No such field is exhibited by the current results.
