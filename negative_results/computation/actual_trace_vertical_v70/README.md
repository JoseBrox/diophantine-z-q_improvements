# Vertical valuations and affine derivative slopes

The [complete proof](../../papers/pole_parameters/vertical_and_fixed_slope_20261117_v70.tex) proves two restrictions on rational maps from abelian varieties into the actual-trace loci.

At a split good prime with positive odd weight valuation, the fixed-slope locus admits only constant abelian maps. Together with the preceding constant-slope theorem, this excludes nonconstant abelian families through prepared points. The derivative statement fixes the input and root; the general two-trace statement fixes the input and permits every point role to vary.

For the derivative locus, a separate proposition allows the root to vary and assumes a fixed rational affine relation between slope and scale. The root, trace, scale and slope must then be constant. This proposition needs no chosen-prime hypothesis.

Neither theorem excludes individual rational witnesses or establishes a defining-polynomial count.

From the repository root:

```sh
python -B negative_results/computation/actual_trace_vertical_v70/check.py --manuscript negative_results/papers/pole_parameters/vertical_and_fixed_slope_20261117_v70.tex --output /tmp/actual-trace-vertical-v70.json
```

The checker verifies all 35 collision slopes for fixed-slope contacts and the four symbolic affine contact cases, including parallel contact lines and repeated roots. The geometric and vertical-valuation arguments are proved in the paper and reviewed independently. The exact manuscript, checker, dependency and reference locations are recorded in `provenance.json` and `independent_review.json`.
