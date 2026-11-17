# Seven-contact ordinary-abc source

This complete eleven-variable family replaces the nine contact shifts by
`[-7,-6,-4,1,3,5,8]` and changes the scale to `a=M^8`.
It reduces the physical weight equation from degree nine to degree seven in
`z^2`. It retains all point, denominator, character, and terminal-root guards.

The degree bound **357,309,057** is larger than the v71 bound. This variant
is for actual-weight arithmetic and is not a new defining-variable or degree
record. The sufficient odd shift is ineffective; the stored `B=3` is only an
algebraic fixture. Nine- and twenty-one-variable realization remain open.

Reproduce from the repository root:

```sh
python computation/few_variables/seven_contact11_v74/build_source.py
python computation/few_variables/seven_contact11_v74/check.py
```

The source has 11 total coordinates, rank 128, 1,940 nodes and 32 native guards.
The checker independently traverses degree/coefficient bounds and verifies
384 finite-field point-character evaluations. Its proof is
[`seven_contact_detector_20261117_v74.tex`](../../../papers/conditional_few_variables/seven_contact_detector_20261117_v74.tex).
The related exact halfpoint fixture is in `computation/pole_parameters/halfpoint_trace_v74`.
