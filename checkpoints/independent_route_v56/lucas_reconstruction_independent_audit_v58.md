# Independent audit: finite Lucas point reconstruction

Date: 17 November 2026.

Manuscript audited in full:
`checkpoints/general_scalar_v56/negative_results/finite_lucas_point_reconstruction_v58.tex`.

## Conclusion

PASS, with the scope exactly stated in the manuscript. The density theorems and the finite-correspondence corollary are valid. They do not give a lower bound on the number of existential variables and do not rule out selecting a smaller arithmetic family, or adjoining numerical rather than elliptic-point data.

## Decisive checks

1. The integer Lucas estimate used is the proved lemma in `papers/few_variables/few_variables_20261108_v8.tex`. For `a=s^2` and `|s|>=3`, its hypotheses hold. The integrality and nonvanishing of `b` are essential; the displayed rational-cofactor counterexample correctly shows their role.

2. Eliminating `t` from `u s+v t+w b=r` when `v!=0` gives the stated coefficient
   `A(a)=v(w+v)a^2-2v(w+2v)a+(w^2+4v^2)`.
   The only way its quadratic coefficient vanishes is `w=-v`, giving `A(a)=v^2(5-2a)`, still nonzero. Thus only finitely many integer `s` have `A(s^2)=0`; outside these, integer coefficients and Cauchy's root bound force polynomial growth of `b,t`. The exponential Lucas lower bound excludes unbounded `|s|`. The `v=0` cases are correct.

3. I re-read Section 2 of `papers/trace_heights/weighted_trace_20261114_v27.tex`. The square classes `3-sqrt(2)` and `3+sqrt(2)` are independent in `Q(sqrt(2),i)^*/Q(sqrt(2),i)^{*2}`. The sign-changing automorphism gives the claimed endomorphism independence of the two conjugate generators modulo torsion. The conclusion that the cyclic group is dense in the restriction-of-scalars surface follows.

4. The primary author manuscript of Gao--Ge--Kuehne was opened independently at `https://ziyangjeremygao.github.io/articles/UML.pdf`. Theorem 1.1 and equation (1.1), pages 1--2, give the required finite union of cosets contained in a closed subvariety (after treating finitely many irreducible components). Intersecting a coset with the finitely generated subgroup yields either nothing or a coset of a subgroup. A full-rank subgroup of `Z^m` contains `N Z^m` and is dense in `A^m`; hence a proper closed subset can contain only the lower-rank cosets. Each such coset satisfies an integer affine equation.

5. For the seven-index theorem, a finite list of equations `L0(s,t,b)+h L1(s,t,b)=0` covering infinitely many `h` for each fixed triple must have one equation with both coefficients zero at that triple. Since each equation is nontrivial as a polynomial in the seven independent indices, its two coefficient polynomials are not both identically zero. The affine-label lemma then bounds `|s|` on the finite union. This correctly handles the fact that the covering equation can vary with the triple.

6. A fixed algebraic correspondence with finite fibers over only the retained point coordinates has dimension at most the retained base. Its image closure is therefore proper in `A^3` or `A^7`. The density results exclude containment of the full preparation family. This remains correct on affine charts and after adjoining a fixed input point and its fixed-index multiplication graph. It does not apply to additional independent parameter coordinates, to a correspondence varying with the scalar label, or to a new arithmetic subfamily outside the theorem's quantifiers.

No mathematical corrections requested.
