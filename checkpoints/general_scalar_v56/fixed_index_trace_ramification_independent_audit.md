# Independent audit: fixed-index trace ramification

Audited manuscript:
`../independent_route_v56/negative_results/fixed_index_trace_ramification_v58.tex`.

**Result: PASS, with the stated scope.** Both propositions concern a
rational-function square identity. They do not exclude individual
rational witnesses or a proper correspondence between the elliptic
coordinates and the slope.

## Independent slope

At a simple contact divisor, the weight has valuation one: the six
zeros of the conditional contact polynomial are distinct, and none is
the normalizing pole at one. With nonzero fixed index n, each of the
four reciprocal-point tests is a nonzero rational function of the
generic elliptic point. They therefore give four factors of valuation
minus one in each geometric slot. Identically zero comparison tests
at n=1 or n=-1 contribute factors equal to one and cause no problem.
Thus both reciprocal products have valuation at least four. Their sum
has at least this valuation (even if it vanished identically), so the
trace-conic radicand has valuation one. Each displayed fixed class has
nonzero constant term at trace zero.

For the adaptive class, the valuation of wc^2 is odd whenever c is
nonzero. If positive, q=2+wc^2 reduces to two and the class is a unit.
If negative e, its two summands have valuations 4e and 3e+v(V), with
the first strictly smaller. The resulting even class valuation cannot
remove the odd radicand valuation. The case c=0 is the unit branch.

## Rational slope graph on the whole multiplication surface

Over the algebraic closure of the generic second-coordinate field, a
nonconstant slope is a map from a genus-one curve to the projective
line. At a contact with odd multiplicity nu, the first slot contains a
nonzero constant reciprocal-point test from the second elliptic
coordinate; the second slot contains the conjugate such test. Each
forces a detector factor of valuation minus nu. Every remaining factor
has nonpositive valuation because its second summand has an odd
valuation and cannot cancel the constant one. Hence v(V)>=nu, and
the trace radicand has valuation nu. This argument works whether the
other tests are zeros, poles, or regular functions at the chosen point.

A square identity would force even multiplicity at every point in
each of six distinct contact fibers. A degree d fiber with only even
multiplicities contributes at least d/2 to ramification; six such
fibers contribute at least 3d. Riemann--Hurwitz for a genus-one map to
P1 gives total ramification 2d, a contradiction. All rational maps of
smooth projective curves extend to morphisms, so poles of the slope
and points at infinity are included. If the slope depends only on the
second elliptic coordinate, the roles are interchanged.

The adaptive-class calculation remains valid in the corresponding
discrete valuation, independently of the poles or size of c. The
argument excludes a rational graph on the entire two-dimensional
multiplication surface. It places no restriction on a proper
correspondence or on a nontrivial algebraic cover of that surface.
