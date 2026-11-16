# Scalar normalization for local square complements

The companion theorem is
[`square_complement_baseline_20261116_v43.tex`](../../../papers/pole_parameters/square_complement_baseline_20261116_v43.tex).
It proves a same-count variant of the general source, under its retained
arithmetic premises, with the early scalar

\[
\rho_* = \frac{102^2\,76249^L r}{(1+153\,76249^L r)^2}.
\]

Its complement `17*(17-rho_star)` is a nonzero rational square. The
actual detector complements can be made local squares at any prescribed
finite set of rational primes, while retaining preparation and all native
guards. The source still has 25 total coordinates. The theorem does not
give global rational square complements, a common rational pole fiber, a
smaller construction, or an effective new sufficient exponent.

Run from the repository root:

```sh
python computation/pole_parameters/square_complement_baseline_v43/check.py
```

The checker requires Python and SymPy and writes `verification.json`.
Use `--output PATH` for an independent reconstruction. It verifies:

- The exact square-complement identity and homogeneous height estimate.
- All 76,249 residues in the fixed-prime raw-contact certificate.
- Twenty-four prepared integer scalar examples.
- Fifteen nonintegral fixed-prime depth examples, including `L=21`,
  `X=1/76249`, where the scalar valuation is one. This confirms why the
  depth--height tradeoff is necessary.
- In-memory modifications of the native general25 and explicit27 builders,
  with unchanged coordinate roles and finite-block census. The explicit27
  check is structural and does not certify a new effective exponent.

The retained coefficient builder is not modified. The certificate records
hashes of that builder and of the exact source papers used in the proof.
The infinite soundness, completeness and finite-local assertions are
proved in the manuscript, under the stated inherited premises; finite
checks do not replace those arguments.
