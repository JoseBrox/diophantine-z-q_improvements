# Executable finite-wrapper coefficient recipe

`../code/build_finite_wrapper.py` accepts a sparse integer polynomial
`P(a,z1,...,z_nu)` and produces a complete polynomial coefficient DAG for
the finite algebra in `../papers/finite_wrapper_transfer.tex`. The
external instance parameter `a` is not a quantified unknown. The output
has 82, 100, or 52 ordinary rational coordinates after the single final
finite-algebra encoder, according to the selected source route. The
52-coordinate route retains ordinary rational `abc`; each route retains
the arithmetic premises and parameter qualifications of its source.

## Input and reproduction

Run from the repository root:

```sh
python undecidability/code/build_finite_wrapper.py \
  --input undecidability/fixtures/natural_square_sparse.json \
  --route explicit27 \
  --output undecidability/finite_wrapper_sources/natural_square/explicit27

python undecidability/verify_finite_wrapper_compiler.py \
  --report undecidability/certificates/finite_wrapper_compiler.json
```

An input contains `unknowns: nu` and a list of terms, each with an integer
`coefficient` and a nonnegative exponent list of length `nu+1`, in the
order `(a,z1,...,z_nu)`. Duplicate terms are combined exactly. The zero
polynomial and the case `nu=0` are supported. The optional `--instance a`
specializes the external parameter to a specified nonnegative integer.

The stored example is `P(a,z1)=z1^2-a`. It is **not universal** and is
**not an undecidability witness**. It demonstrates the coefficient
compiler on a small, independently checkable input. The same compiler
accepts an explicitly supplied universal polynomial. No unspecified
universal coefficients are inserted or fabricated.

## Construction recorded in the output

The compiler follows Bayer–David–Haßler–Matiyasevich–Schleicher,
arXiv:2506.20909v3, Definitions 2.1, 4.1 and 5.3. It first computes the
sparse coefficients of `P^2+(z_(nu+1)-1)^2`. The potentially enormous
geometric sums are polynomial circuits built by binary doubling.
Constants such as `beta^((delta+1)^v)` remain power nodes; their decimal
expansions are not materialized. The degree-eight monic norm polynomial
is computed using arrays of at most nine coefficient nodes.

The output is the complete inherited common-numerator source after
these changes:

- The ninth ordinary input `n` is removed; the two ordinary parameters
  `s,t` are added.
- A monic degree-eight generator `m` and a monic quadratic generator
  `xi` are adjoined. Their equations are `P_m(m)=0` and
  `xi^2+S*xi+S^2*(s^2+t^2)-m=0`.
- Every old coefficient and guard receives the exact substitution
  `n=m/S^2`. Powers of `S` clear its denominator. For an old terminal
  pole `q^2+c(n)=0`, the new generator is `S^d*q`, where `d` is an upper
  bound for the degree of `c` in `n`.
- The selected-character guard includes `S`. The nine integer
  predicates are all retained.

The JSON schema is `finite-wrapper-source/v1`. `coefficient_dag` uses
integer, parameter, variable, addition, negation, multiplication and
nonnegative integral-power nodes. A `monic_extension` block lists its
coefficients in ascending order, **omitting the leading coefficient
one**. Its multiplication table is the usual companion table over
the preceding algebra. The point-block multiplication tables and
terminal quadratic blocks are recorded as well. Each old coefficient
has an explicit map `(new_node,e)` certifying that the new node equals
`S^e` times the old expression after substitution. The original root
fractions are also retained with their exact transformed numerators
and denominators.

`separating_generator_nodes` omits `m`, because `xi` generates it, and
omits each point's `W`, because `W=U^2/2-A`. The nodes still exist in the
finite algebra. Apply `../papers/joint_finite_algebra_encoder.tex` to
these generators and the product guard to obtain the final single
polynomial. The enormous final determinants are specified exactly;
they are not expanded by this compiler.

## Verification scope

The verifier exactly replays every denominator-clearing instruction,
checks the sparse input transformation and coding constants, verifies
the absence of cyclic finite-stage dependencies, checks guards, and
recomputes ranks and variable counts. It additionally compares every
old and new DAG node at three deterministic finite-field assignments.
Independent modular evaluations check the primary bridge recipe and
the eight-sign norm in a multiquadratic quotient algebra. Those modular
checks are supplementary diagnostics, not polynomial identity proofs.

The stress fixture has 58 input unknowns and degree four. Its largest
coding position is `9^60`; its bridge uses fewer than 2,000 DAG nodes.
It too is a nonuniversal demonstration. The general algebraic identities
and both directions of the transfer are proved in the manuscript.
