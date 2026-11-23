# Exact boundaries for further compression

This checkpoint proves three narrowly scoped statements. It does not change any variable census.

1. **The 139-coordinate power circuit is optimal in a larger model than previously proved.** Starting from 1, b, b², each triangular quadratic binomial step enlarges the interval of Laurent exponents by at most a factor of two. Negative exponents, rational exponents, repeated factors, and constant monomials are included. Since 2¹³⁹<5⁶⁰<2¹⁴⁰, at least 139 new coordinates are needed. The existing ceiling circuit attains 139. A separate elementary common-denominator degree proof gives the same 139 lower bound for arbitrary rational-function intermediate values, including a quadratic row selecting a rational-function branch. The bound still does not concern simultaneously implicit systems, arbitrary algebraic-function branches, or arguments using the other source equations.
2. **One quadratic integer test cannot certify an unrestricted tuple.** For r≥2, every rational polynomial f of degree at most two with f(Zʳ) contained in Z also takes an integer value at a nonintegral rational tuple. A rational parametrization of a quadratic level set proves this, including degenerate cases. Higher-degree tests, several tests, quantified witnesses, and source subvarieties are outside the statement.
3. **A common sum does not retain the scalar height contraction.** For every k≥3, an explicit elementary Pell family has all Xᵢ>0, unbounded h(X₁), and Σ(Xᵢ⁸+Tᵢ²)=k exactly. Therefore the proposed common M=B+2Σ(Xᵢ⁸+Tᵢ²) cannot bound input heights on unrestricted rational tuples. The family is not claimed to consist of allowed elliptic traces, so this is an obstruction to transferring the old proof, not a counterexample to a complete proposed integer predicate.

The proofs and exact scope are in `compression_barriers.tex` and its rendered PDF. Reproduce the finite certificate with:

```sh
python -B undecidability/joint_research_v94/verify_compression_barriers.py
```

The checker verifies the exact power chain and integer inequalities, the rational-function degree recursion, signed rational interval edge cases, the quadratic level-set identity, the Pell norm and three-square identities, and twelve exact height counterexamples. The universal claims are proved in the paper rather than inferred from those finite examples. All dependencies are existing project proofs or elementary algebra; no new arithmetic premise is introduced.
