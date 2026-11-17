# Odd halfpoint coset and raw abscissas

This exact local counterexample concerns the proposed replacement of the first four balanced factors by `1+C_i^2/u`, while retaining the two balanced comparison factors. Restricting the source input to an odd integer and the auxiliary point to an odd multiple of `R0=P/2` does not automatically prepare newly arising negative-odd-weight primes.

The tuple is `X=1`, `B=3`, `A=P`, `H=U=2665 R0`. At `p=85817`, both reductions of `H` are the two-torsion point `(0,0)`, even though `2665` is odd. The physical nine-contact map with `a=(10621537/256)^4` has `v_p(u)=-1` for every integer slope `z=39827 mod p^2`. The actual raw trace has valuation six and the pole input `b` has valuation `-11`. The actual-trace square radicand has valuation one, so it is not a rational square.

Every sufficiently large positive slope in this progression satisfies all pre-pole whole-character guards and the real preparation. Neither the selected prime factorization nor all fixed finite-place preparation is asserted. The computation does not exclude other auxiliary points, a new compatible CRT argument, or a complete construction using a different family. The shift `B=3` is a fixture, not a certified defining shift.

Run `python check.py` and `python check_independent.py`. Both use only the Python standard library. The first computes points by an affine addition chain modulo `p^3`, checking every denominator as a unit. The second reconstructs the decisive coordinates from division polynomials and evaluates the physical logarithmic derivative independently.

The complete proposition and guard proof are in `negative_results/papers/pole_parameters/odd_coset_raw_20261117_v76.tex`.
