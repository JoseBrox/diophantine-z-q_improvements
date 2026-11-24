# Two limited obstructions for the defining-polynomial frontier

These results are **not variable lower bounds** for any Diophantine definition of the integers.

## 1. No affine equation from constant row combinations

For each of the pinned BB-native 163- and 179-coordinate quadratic tables and the new 54-coordinate abc table, form the coefficient matrix of the homogeneous degree-two parts of its residuals. The rank over Q equals the number of residuals:

| coordinates | rows | rank |
|---:|---:|---:|
| 163 | 137 | 137 |
| 179 | 151 | 151 |
| 54 | 44 | 44 |

This is certified by explicitly specified nonzero maximal minors modulo the prime 1000003. In all three tables the degree-two coefficient matrix is independent of the fixed coefficient parameter; the result therefore holds for every specialization. The exact certificate records the table blob, ordered columns and determinant modulo the prime. The independent Python verifier recomputes the minor with elementary finite-field elimination and checks the blob hashes.

Consequently no nonzero constant Q-linear combination of the rows is affine-linear. This only rules out finding a coordinate-eliminating affine equation by such a combination; it does not rule out nonlinear row combinations, affine changes of coordinates followed by other elimination procedures, or new physical charts.

## 2. A single universal rational valuation gate cannot implement parity OR

Let k>=2. There is no nonzero rational function F in Q(T_1,...,T_k) with the following property at every rational tuple on which it is defined and nonzero: for every sufficiently large prime p, whenever all v_p(T_i)<0 and at least one v_p(T_i) is odd, v_p(F(T)) is negative and odd. In fact no such F works even at a single prime outside the finite set of numerator and denominator coefficient primes.

Proof. Write F=N/D in nonzero polynomials. Fix such a prime p. In the open negative orthant of R^k choose a nonempty rational open cone avoiding the finitely many hyperplanes on which two distinct exponent vectors of N or of D have equal scalar products. On a smaller such cone the minimizing exponent vectors a and b of N and D are fixed and unique. For every integral valuation vector v in this cone, evaluate T_i=p^{v_i}. Both polynomial values are nonzero and their valuations are exactly a.v and b.v, by uniqueness of their least-valuation terms. Thus the valuation of F is (a-b).v. The open cone contains integral vectors in every residue class modulo 2: take a sufficiently large even multiple of an integral interior vector, then add any vector with coordinates 0 or 1. Since k>=2, the linear functional a-b modulo 2 has a nonzero kernel vector. Choose that nonzero residue class. At least one input valuation is negative odd, but the output valuation is even. This contradicts the required property.

The same proof permits any fixed finite list of additional nonvanishing polynomial guards: avoid their exponent-tie hyperplanes as well. It does not cover equality-constrained inputs, auxiliary algebraic witnesses, multiple output functions, or specialized relations between actual elliptic detector values. In particular this result does not rule out combining poles on the true detector locus. It rules out a proposed *universal single rational-function replacement* based solely on the valuations of independently varying scalar inputs.

The proof explains why multiplying independent detector inputs (parity cancellation) or substituting a more elaborate universal rational expression cannot automatically combine their square-denominator tests. Any successful general reduction must exploit extra structure of the actual inputs or a new arithmetic predicate.
