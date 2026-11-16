# Square-complement normalization obstruction

The companion proof is
[`square_complement_normalization_20261116_v43.tex`](../../papers/pole_parameters/square_complement_normalization_20261116_v43.tex).
The substitution

\[
\Phi(b)=\frac{1156b}{(17+b)^2}
\]

preserves square class and makes the pole complement a square, but it
does not preserve the pole predicate. For `b_n=204^2/409^(2n-1)`, `n>=2`,
the original curve has no `Q_409` point for any local conic parameter,
including zero and both projective boundaries. Its transformed input is
fully prepared and has explicit nonzero rational witnesses at every
finite nonzero rational conic parameter.

This is an isolated pole-subsystem obstruction. The family has not been
realized as actual values in a complete detector source.

Run from the repository root:

```sh
python negative_results/computation/square_complement_normalization_v43/check.py
```

The checker uses only the Python standard library and writes
`verification.json`. Use `--output PATH` to reconstruct a separate
certificate. Exact sparse polynomial arithmetic verifies the substitution
and conic identities. It also verifies primality, the fixed congruences
and coprimality constants, eight family instances, forty rational
nondegenerate witnesses, 1,098 integer valuation cases, and 288 exact
rational local checks including zero parameters.

The universal local obstruction and boundary cases are proved in the
manuscript. The finite valuation grid is a regression check. The
certificate binds the proof, verifier, and exact source papers by SHA-256.
