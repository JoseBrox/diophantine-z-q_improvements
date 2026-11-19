# Hyperbolic parity certificate

The source shared-product packing is due to Gabe Conant with Astra 6.2.
The new result is a precise obstruction to replacing its final partial
hyperbolic reciprocal pair by a full pair in the retained integral diagonal
Laurent compilation.

The point row forces `w(U)=w(V)`. The factor row would then require
`1+2*w(U)=2+2*w(B3)`, which is impossible for integer weights. This is
independent of the number of stored unit powers. It also survives adding
an even integer to either indicated factor exponent.

Run from the repository root:

```sh
python -B computation/variable_reductions_v79/quartics/check_hyperbolic_parity.py
```

The standard-library checker reads the exact pinned source and factor
assignment, reconstructs the decisive monomials, checks the hyperbolic
identity, and verifies the four-equation contradiction modulo two. The
stored certificate is reproduced exactly. No solver is required.

The proof is in
[`hyperbolic_parity_20261119_v79.tex`](../../../papers/quartic/hyperbolic_parity_20261119_v79.tex).
This does not exclude different point charts, variable-dependent changes
of equations, nonlinear coordinate changes, other detector constructions,
or smaller quartics. No new general-quartic variable record is claimed.
