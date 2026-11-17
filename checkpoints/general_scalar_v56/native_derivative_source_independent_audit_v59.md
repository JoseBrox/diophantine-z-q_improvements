# Independent native-source audit

**PASS.** The explicit source in
`research-repo/computation/few_variables/derivative11_v59/build_source.py`
matches the audited eleven-coordinate proof. The stored member has
`B=3`; this is a coefficient fixture, not a numerically certified
defining shift.

The source retains exactly the input, six point-chart coordinates,
one slope, and two intrinsic parameters. Its three rank-four point
blocks and one quadratic pole block have rank 128. The inherited
one-coordinate encoder therefore gives eleven external coordinates.
No test value, trace, height scale, square root, or reciprocal is
retained as an additional unrestricted coordinate.

The six original tests use the original direct-input target `r-X`,
as in the proof. The moving quotient is
`u=-2G/(G_A/8)=-16G/G_A`; the eight factors implement exactly the
sixteen shifts. The field divisions form
`D_i=C_i²/(1+u C_i²)` and
`W=prod(1+D_i²/u)`. With components `W0,W1`, the source computes
`V=2W0/(W0²-2W1²)` and
`b=w(W0²-2W1²)²/W0²=4w/V²`, so no factor of four is missing.
Its terminal radicand is precisely
`eta(eta+v²)² s⁴-eta(eta-v²)²(1-eta)²`, with `eta=7b`.
The square clearing and original-root recovery use the inherited
monic quadratic rule.

All original point/difference/quotient denominator guards remain.
The extra source guards `s!=0`, `eta+v²!=0`, and `eta-v²!=0` are
permitted by the already used intrinsic witness-pair density: their
product over the finitely many point characters is a nonzero
polynomial in the free parameters. The manuscript's whole-character
positivity handles the detector guards, and the nonzero radicand
norm handles the quadratic root. Thus these guards require no
extra variable and create no completeness gap.

## Independent exact evaluations

The checker `check_native_derivative_source_v59.py` imports no
producer code. It constructs the curve and generator over
`Q(sqrt(2))`, obtains actual points by the ordinary tangent/chord
law, and takes exact square-abscissa charts. The three tuples have
indices

| Input | Root A | Auxiliary H | Product U |
|---:|---:|---:|---:|
| 1 | P | 2P | 2P |
| -1 | -P | 2P | -2P |
| 2 | 2P | 3P | 6P |

For each tuple it sets the real slope to `M³+9`, fixes the intrinsic
parameters to `v=2,s=3`, and reduces the exact rational coordinates
at the split primes 1000000007 and 1000000009. At each pair it
enumerates all 64 independent ordinate-sign characters of the
three point blocks. The total is **384 exact evaluations**, with
all 38 guarded numerators accounted for.

The reference computations use ordinary chord formulas for point
differences and a sum of logarithmic derivatives for the scalar
quotient. They check the point-block relations, point coordinates,
all six original tests, all transformed tests, the product in both
slots, its norm and reciprocal trace, the pole input, the intrinsic
radicand, and its monic clearing identity. Every guarded numerator
is nonzero at these fixtures. For the finite quadratic generator,
the checker verifies its nonzero cleared radicand rather than
pretending an arbitrary value is a root; the actual roots may be
in a quadratic extension of the residue field.

The certificate is `native_derivative_source_v59_certificate.json`
and includes the source and checker hashes. These finite checks
verify the implementation on the stated fixtures. The infinite
arithmetic existence and whole-character avoidance statements are
the mathematical results in
`derivative_source_independent_audit_v59.md`, not consequences of
the finite evaluations. The determinant degree and coefficient
majorants are covered by the parent's separate inherited-compiler
structural audit.
