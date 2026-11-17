# Pole cancellation and quotient heights

For `U=[n]H`, the rational coordinate `Y=X^2 x(U)-x(H)` controls the input and the integer quotient through the height inequalities in the [manuscript](../../../papers/elliptic_heights/pole_cancelling_quotient_height_20261117_v60.tex). On `X=n`, its pole at the elliptic identity cancels, and its leading formal coefficient is `d^2(n^4-1)/5`.

Run from the repository root:

```sh
python -B computation/elliptic_heights/quotient_height_v60/check.py --output /tmp/quotient-height-v60.json
```

The checker derives the generic multiplication formulas directly by the tangent/chord law and checks 32 leading coefficients. It also verifies 252 exact rational height cases. Canonical-height comparisons are mathematical inputs to the proof, not conclusions of finite sampling. No defining-variable bound follows from this coordinate alone. Its proposed derivative-detector application is excluded by the separate [denominator-support theorem](../../../negative_results/papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex).
