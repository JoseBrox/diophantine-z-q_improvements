# Denominator-support obstruction

`check.py` verifies the exact height constants and 1,326 valuation cases
that force the positive odd support into the reference denominator.
`check_carrier.py` checks nonconstant and constant rational specializations,
denominator guards, the nonzero norm polynomial, rational-root height
bounds and fixed parameter coefficient bounds. Both use exact arithmetic.

```sh
python -B negative_results/computation/denominator_support_v60/check.py
python -B negative_results/computation/denominator_support_v60/check_carrier.py
```

The [manuscript](../../papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex)
proves the infinite statements. Its Siegel argument is a theorem application,
not a conclusion from the finite fixtures. The obstruction concerns the stated
support and fixed rational carrier architecture; it is not a lower bound for
every possible defining polynomial. The guard-free finiteness statement
concerns intended witnesses `X=n`, `U=[n]H`.
