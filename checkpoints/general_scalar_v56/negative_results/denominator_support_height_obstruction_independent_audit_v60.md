# Independent audit: denominator support and fixed rational carriers

Reviewed canonical manuscript:
`../../independent_route_v56/negative_results/denominator_support_height_obstruction_v60.tex`.

## Verdict

PASS for the full merged proof: the direct radical-budget obstruction,
its exact derivative-source application, the fixed rational carrier
height bound, and the degeneration argument using Siegel's theorem.
The result excludes the stated architecture. It is not a general
impossibility theorem for nine variables or for all two-point sources.

## Direct obstruction and exact constants

At a good prime, forcing H to be formal is equivalent to forcing the
prime into B_H. Thus the entire positive odd radical is bounded by
log B_H≤hhat(H)+O_E(1). Combining a positive lower bound
delta·h(M) and a carrier lower bound a(n²−1)hhat(H) gives exactly

`[a*delta*(n²−1)−1] hhat(H) <= O(1)`.

Since hhat(H)=h²hhat(P)≥hhat(P)>0, this bounds the internal quotient
n uniformly. If3a*delta>1, it also bounds h on |n|≥2.

For the specific derivative source, independent exact arithmetic gives

- delta=gamma/Q−C=188411/200400;
- alpha*delta=187845767/200600400;
-3alpha*delta−1=120978967/66866800>0.

The local extraction remains valid with any added balanced test:
at odd positive weight valuation every W-factor has nonpositive
valuation, so a bad1/x(H) factor cannot be compensated by another
factor. The intrinsic pole condition therefore forces the claimed
denominator support. No enlargement of the global exceptional set
depending on H, X or B is allowed or used. The temporary finite
completeness sets do not change this soundness set.

When the source constants are independent of B, the bounds on h
also bound h(M), whereas h(M)≥alpha E_h−O(1) and E_h≥log B.
Therefore all intended inputs |n|≥2 are excluded for sufficiently
large B. This statement does not need X≠n and directly defeats
completeness of the particular proposed quotient-height source.

## Coefficient-height lemma

For R=(A+By_U)/(C+Dy_U), pad coefficient vectors p,q in the
independent basis x_U^i,x_U^i y_U. At rational parameters, nonzero
minor-square sum is exactly nonproportionality, hence nonconstancy
of the specialized function of U. If r=R, the norm polynomial

`(A−rC)²−(Z³−d²Z)(B−rD)²`

vanishes at x(U) and is nonzero: otherwise the nonsquare cubic
would be a square in Q(Z), unless both linear expressions vanish,
which is precisely the excluded constant specialization.

After primitive integer scaling of p,q and of r, polynomial
convolution bounds its projective coefficient height by
2h(p:q)+2h(r)+O(1). The rational-root theorem bounds h(x(U)) by
that coefficient height; no resultant lower bound is needed.
Fixed polynomial coefficient degrees give
K_X=d_X and K_H=2d_x+3d_y, using h(x(H))=2hhat(H)+O(1) and
h(y(H))≤3hhat(H)+O(1). Hence the claimed canonical-height
inequality is uniform in the input and both elliptic points.

A separate independent proof in `fixed_rational_carrier_height_v60.tex`
makes the coefficient constant explicit as4(N+1)(d²+2), using
the slightly larger affine coefficient height. The accompanying
standard-library checker verifies1,404 nonconstant fixtures,
16 constant specializations and12 denominator-guard cases, including
common polynomial factors, zero function values, and96 parameter
height fixtures. These finite checks audit the algebra and constants;
the uniform lemma follows from the proof.

## Degeneration and intended integer inputs

Defining the degeneration locus by all coefficient-minor zeros is
correct and avoids any issue over complex points with a single sum
of squares. Generic nonconstancy makes this locus proper of dimension
at most one in A1×E. Its zero-dimensional parts, singular points and
non-Q-defined geometric components contribute only finitely many
rational images, after taking intersections with Galois conjugates.

On a geometrically integral curve component, pass to its smooth
projective normalization. If X is constant, there is at most one
rational input. If H is constant, the radical budget and E_R≥2h(X)
bound the rational input height. If both maps are nonconstant, the
map to E forces genus at least one. Siegel's theorem applied to the
nonconstant rational function X gives finitely many rational points
with X integral. A nonsingular rational point lifts uniquely to the
normalization; the finitely many singular exceptions were already
separated. This proves finiteness of the intended X=n integer inputs
without imposing a minor guard.

The primary statement was independently reopened: Aaron Levin,
“Siegel's theorem and the Shafarevich conjecture,” JTNB24(2012),
705–727, Theorem1.1, at
https://www.numdam.org/article/JTNB_2012__24_3_705_0.pdf.
It states the needed finiteness directly for a nonconstant rational
function taking S-integer values on a positive-genus curve.

The result does not assert finiteness of the full rational X-projection
before input equality is known. It requires a fixed rational carrier,
retained coefficient/evaluation denominator guards, fixed positive
height constants, and positive odd contact support contained in B_H.

## Audited source hash

SHA256: `fa3dabda27b49ec62cc7d5fdfa94d15f4546e5af1f60bb5b146b984e974f05d9`.
