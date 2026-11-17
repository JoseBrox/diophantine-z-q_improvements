# Actual halfpoint weight cover

For the full-auxiliary tuple `X=1, B=3, A=P, H=U=P/2`, with
`P/2=(1+sqrt(2),2sqrt(2))`, the actual tests are
`(c,c,bar(c),bar(c),0,0)`, where `c=sqrt(2)-1`.
Write

- `D=u^2(u^2+6u+1)^2`;
- `R=D+2u^3+12u^2+34u+1`;
- `Pi=4D^4(1+u)^2+2uR^2(R^2-D^2)`.

Then `W=(R/D)^2`, `V=2D^2/R^2`, and the exact actual weight cover is
`Y0^2=Pi`. It has **genus 12**. The seven-contact physical lift has degree
seven in `z^2`. Its squared-slope quotient has genus 90, its companion has
genus 91, and its slope cover has genus 181.

The selected-character weight guards exclude only `u=0,-1` among rational
weights. The physical degree-seven equation, rational-square squared slope,
original guards, and all preparation conditions still have to be checked.
**No admissible rational point or complete nine-variable construction is
claimed.** `B=3` is an algebraic fixture, not a certified defining shift.

Reproduce from the repository root:

```sh
python computation/pole_parameters/halfpoint_trace_v74/check.py
python computation/pole_parameters/halfpoint_trace_v74/check_independent.py
```

The second checker imports no producer routine and rebuilds all five integer
polynomials. Modulo-53 Bezout identities certify the two squarefreeness
claims; these identities are not the lost physical-lift obstruction mentioned
in the interrupted conversation.

The proof is
[`seven_contact_detector_20261117_v74.tex`](../../../papers/conditional_few_variables/seven_contact_detector_20261117_v74.tex).
