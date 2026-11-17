# Independent review of native pole ramification

Reviewer: `/root/twentyone_realization`

Date: 2026-11-17

Status: **PASS**

This review covers the new norm identity, physical counterexample, valued-field
parity lemmas, finite-cover ramification theorem, and extension of the existing
abelian-family argument. It is not a fresh audit of the inherited Diophantine
definition or of its external arithmetic premises.

## Independent arithmetic and source verification

`check_independent.py` imports neither the producer nor any project module. It
reconstructs the two norm orders using four-coordinate quadratic-algebra
multiplication; independently doubles and triples the point
`R=(1+sqrt(2),2*sqrt(2))`; reconstructs the exact physical scale, slope,
contact product, derivative, and weight; and multiplies the actual six
balanced tests in `Q(sqrt(2))`. The resulting product and all displayed
valuations agree with the producer certificate, including `v_100003(b)=-7`.

The checker recursively evaluates the actual source DAG at the different
split prime `1000000009`, using square root `291087696` of 2. All 30 native
pre-pole guards are nonzero at all 64 point characters, for 1,920 independent
guard evaluations. On the selected character it additionally checks the
physical scale, squared slope, weight, detector product, trace and pole input
against their independently reconstructed rational values. Since `u>0`, the
balanced denominators are positive in every real character once the actual
tests are defined. This proves the claimed nonvanishing without importing
the producer's finite evaluation routine.

## Mathematical review

1. **Norm composition.** Both orders of quadratic norm give the displayed
   identity. A norm representation alone does not imply either native pole
   equation. The actual tuple makes this failure concrete, without asserting
   fixed-place or selected-prime preparation.
2. **Intrinsic parity.** For negative odd `nu=v(eta)`, the valuations of
   `eta+v^2` and `eta-v^2` equal the same finite minimum. The two quartic
   summands have unequal odd valuations; `s=0` leaves one nonzero odd-valued
   summand. Zero auxiliary parameters and zero terminal ordinate are handled.
3. **General-17 parity.** The first equation forces `v(e)=0`. The remaining
   coefficient has odd valuation `3*nu`, so the second equation equates an
   even, finite valuation with an odd valuation or zero. The stated unit
   hypotheses on 2, 3 and 17 are sufficient. Guarded invertible rescaling
   preserves the exclusion.
4. **Finite covers.** Pullback multiplies each negative odd pole order by
   its ramification index; the parity lemmas force every such index even.
   For `r>=1` the degree is even, and each contact fiber contributes at least
   `d/2` to the ramification divisor. Riemann--Hurwitz gives exactly
   `g>=1+d*(r-4)/4`. The explicit `r>=1` hypothesis was added during review.
5. **Actual contact applications.** Fixed guarded rational point characters,
   and the derivative condition `a>max|c|`, ensure distinct contact positions
   and defined nonzero reciprocal tests. Zero comparison tests contribute
   one, and trace cancellation only raises the trace order. Thus the
   displayed contact counts and genus bounds follow for both balancing
   versions.
6. **Abelian families.** The inherited simplicity and point-map facts are
   explicitly retained. The paired reference zero locus has codimension two
   after a surjective abelian point map, so it contains no divisor. Even
   divisors of reciprocal abscissae justify the revised balancing formula.
   Every odd contact component would give a negative odd pole input, which
   contradicts the native equations. The resulting even contact divisors
   yield an etale double cover; its abelian structure precludes a nonconstant
   map to the indicated higher-genus hyperelliptic curve. Constant slopes
   and nonabelian higher-dimensional families remain open.

The cited primary sources were checked directly: Milne, *Abelian Varieties*
(2008), Chapter I, Theorem 3.2, Corollary 3.7 and Remark 12.3, and the Stacks
Project, Tag 0C1B (Riemann--Hurwitz). They support the precise geometric steps
used here. The paper also gives the complex-torus explanation of the etale
cover step.

## Limits

This is a proof of restrictions on specific rational constructions and
native-pole covers. It neither disproves prepared realization for integer
inputs nor supplies a 21-variable or 9-variable definition. It does not
establish a lower bound on variables of arbitrary defining polynomials.
There are no remaining material issues in the reviewed claims.

The accompanying JSON binds this review to the final producer, independent
checker, certificates and manuscript hashes.
