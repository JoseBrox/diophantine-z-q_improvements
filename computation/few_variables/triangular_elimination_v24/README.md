# Smaller degrees from a triangular combination of quadratic roots

The [complete proof](../../../papers/finite_algebra/triangular_separation_20261113_v24.pdf) replaces the previous finite-algebra separating element and truncates each characteristic polynomial to the dimension of its nonzero part. The arithmetic sources and all their hypotheses are unchanged. Every count includes the input.

| Construction | Variables | Degree upper bound | Support upper bound |
|---|---:|---:|---:|
| `general25` |25|185517288563368898320200, less than 2^78|less than 2^1815|
| `explicit27` |27|679086760181946108087584, less than 2^80|less than 2^2009|
| `weak13` |13|207969001841, less than 2^38|less than 2^437|
| `abc13` |13|199368913265, less than 2^38|less than 2^436|

These are bounds for unexpanded polynomials, not exact degrees or monomial counts. Both 13-coordinate constructions are multiplied by the input to include zero. `weak13` assumes the retained weak abc inequality at exponent 121/100; `abc13` uses exponent 16/15. Neither removes the source elliptic, pole-realization, height or prime-pattern hypotheses.

The explicit27 member retains L=20483 and has coefficient height less than 2^(2^92), under the same premises. The remaining coefficient estimates are only for the stored L=3 or B=3 fixtures. Those fixtures are not certified defining members. The defining thresholds of the general25 and 13-variable families remain ineffective.

## Exact specifications

`inputs.json` pins the source commit, existing specification hash, certificate Git blob and numerical bounds. Each construction directory contains a complete indexed finite-operation specification and its bounds. The new specification uses the old native coefficient algebra, not its old final determinant expression. Monic relation signs, generator order, the nonzero condition, every product range and every principal-minor range are explicit.

For a different permitted coefficient parameter, run the identified source builder at the pinned commit with that parameter, and apply the same construction to its native algebra. Parameter values are coefficients, never quantified coordinates. Source uniform-degree certificates continue to apply. The numerical coefficient norms for the three small fixtures are not asserted uniform in the parameter.

## Reproduction

From the repository root:

```sh
python computation/few_variables/triangular_elimination_v24/build.py --source-checkout .
python computation/few_variables/triangular_elimination_v24/check_bounds.py
python computation/few_variables/triangular_elimination_v24/check_examples.py
```

The first two programs require only the standard library. The third requires SymPy and performs 13 exact small-algebra tests, including two point generators, radicands depending on both, nonreal roots, repeated characteristic values, vanishing radicands, excluded nilpotents, an empty nonzero locus and a tiny nonzero radicand. The bound checker imports no producer and uses closed sums with a binary-searched correction interval rather than the producer's direct case summation. Deliberately corrupted bounds and omission of the nonzero-part projector are rejected.

The distributed `bounds.json` records that the full-checkout authentication was **not** run in the authoring environment. The pinned source certificates were read through GitHub and their numerical inputs were checked; complete native source files remain dependencies in the existing repository. Running the first command in a complete checkout performs the additional byte authentication. Neither those checks nor the small examples certify the source arithmetic foundations or constitute non-author review.
