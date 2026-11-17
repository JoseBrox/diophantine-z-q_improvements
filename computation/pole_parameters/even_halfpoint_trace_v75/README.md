# Actual halfpoint cover with even-valuation balancing

For `X=1, B=3, A=P, H=U=P/2`, the first four tests are
`c,c,bar(c),bar(c)` with `c=sqrt(2)-1`. After unsquared balancing, set

- `D0=u^2(1-2u-u^2)^2`;
- `R0=D0+2u^3+4u^2+6u+1`;
- `Pi0=4D0^4(1+u)^2+2uR0^2(R0^2-D0^2)`.

Then the **actual** detector has `W=(R0/D0)^2`, `V=2D0^2/R0^2`,
and weight cover `Y0^2=Pi0` of **genus 12**. Its seven-contact physical
slope cover has genus 181; the nine-contact physical slope cover has
genus 233. The corresponding squared-slope genera are 90 and 116.

The exact physical lifting equation, rational-square squared slope,
original guards, and all preparation conditions remain necessary.
**No admissible rational point or complete nine-variable construction
is claimed.** The fixed shift 3 is an algebraic fixture only.

Reproduce from the repository root:

```sh
python computation/pole_parameters/even_halfpoint_trace_v75/check.py
python computation/pole_parameters/even_halfpoint_trace_v75/check_independent.py
python computation/pole_parameters/even_halfpoint_trace_v75/check.py --contacts 9
python computation/pole_parameters/even_halfpoint_trace_v75/check_independent.py --contacts 9
```

Each independent run reconstructs all five integer polynomials without
importing the producer and checks the recorded finite-field Bezout identities.
The proof is
[`even_valuation_detector_20261117_v75.tex`](../../../papers/conditional_few_variables/even_valuation_detector_20261117_v75.tex).
