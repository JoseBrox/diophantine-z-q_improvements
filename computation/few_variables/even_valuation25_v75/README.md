# Even-valuation reciprocal tests in general25

This package constructs a complete **25-variable** integer polynomial family
under the arithmetic premises retained by the general source. The first ten
field tests are reciprocal abscissae. Their valuations are even outside the
retained exceptional set, so the revised factors use `C_i` in place of
`C_i^2`. The other six field tests, scalar factors, weights, two native pole
blocks and all guards are retained.

The four root points retain integer indices in `2E(K)`. The five auxiliary
points use the full guarded affine charts of `E(K)`. The new local extraction
is stronger; the original prepared `2E(K)` subfamily still proves completeness.
The proof is in
`papers/few_variables25/even_valuation25_20261117_v75.tex`.

## Bounds and scope

| Quantity | Bound or exact count |
| --- | ---: |
| Total rational coordinates, including input | 25 |
| Degree bound | 4,863,007,848,923,136 |
| Support bound | strictly below `2^1192` |
| Encoder degree bound | 1,048,576 |
| Integer content | 1 |
| Native arithmetic nodes | 6,039 |
| Recorded guards | 101 |
| Retained norm factors | 128 |

The degree bound improves the full-auxiliary v72 bound
4,924,857,429,000,192. It is a bound, not an assertion that the expanded
polynomial has exactly that degree.

The fixed coefficient exponent `L` is odd and at least three. Every sufficiently
large fixed `L` defines the integers under the retained premises; its sufficient
threshold remains ineffective. The stored **L = 3 member is an algebraic
fixture**, with coefficient L1 norm at most `2^34532878499971072`.
Its sufficiency for the defining assertion is not certified.

The same unsquared first-ten factors are valid in the normalized general
two-actual-trace source. This preserves its sound **21-variable** specification
and local preparation, but simultaneous global rational realization remains
unproved. The degree bound above applies to the compiled native-pole family,
not to that unproved smaller defining count.

## Reproduction

From the repository root:

```sh
python computation/few_variables/even_valuation25_v75/build_source.py --L 3
python computation/few_variables/even_valuation25_v75/check.py
```

The generator also accepts `--repo`, `--name general25`, `--parameter`, and
`--output`. The checker accepts `--repo`, `--specification`, and `--output`.
Pinned dependencies are read without modification. The constructor performs
exactly two checked edits of the pinned native build method: enumerate the
field-test loop and select the first power for its first ten numerators.

The source circuit, parent finite-algebra specification, final determinant
specification and all bounds are in `specification/`. Its independent
certificate checks the point algebra, guard supports, subalgebra norms,
weighted degrees, coefficient bounds and terminal root. Two deliberate
degree/guard corruptions are rejected. Independent chord-and-tangent
evaluation checks the detector at 72 finite characters, including
half-integral auxiliary indices. These checks do not exhaust all point-algebra
characters or establish any external arithmetic premise.

## Why the simplification is sound

For `y^2=x^3-Dx` with `v(D)=0`, a positive `v(x)` satisfies
`2v(y)=v(x)`, and a negative one satisfies `2v(y)=3v(x)`. Thus every
nonzero reciprocal abscissa has even valuation. At an odd weight valuation,
the numerator of a revised factor therefore still has parity opposite to
the denominator. No equal-valuation cancellation is introduced.

At a successful selected contact, reciprocal abscissae have valuation at
least two, so the revised factors remain one modulo the selected place.
On the original complete real characters the points and differences lie in
the identity component of the real elliptic curve, giving positive
reciprocal abscissae. The prepared whole-character norm guards survive.

Neither the scalar `rho` nor the comparison scale is independently free at
a fixed input. The ten contact branch points of the actual square cover
also remain, so this revision supplies no rational parametrization of that
cover and no complete 21-variable definition.
