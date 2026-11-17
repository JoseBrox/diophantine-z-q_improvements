# Independent review of the vertical and affine-slope follow-up

Date: 17 November 2026. Reviewer: `height_and_fields`.

**Status: PASS**, for the mathematical statements in
`vertical_and_fixed_slope_20261117_v70.tex`, SHA256
`967de7f992e4212b1878460d5729a574b9d447da7361d9ac273e85a7c9e056a6`.
This is separate from the frozen v69 review. It is an audit of the written argument, not a formal proof certificate or a claim of a smaller defining polynomial.

## Connected-kernel quotient and good reduction

The point-data map extends to a morphism from the abelian variety and becomes a homomorphism after subtracting its value at zero. Quotienting by the identity component of its kernel gives an abelian variety `J1` isogenous to the point-image `S`. Its generic fibers are geometrically integral: after algebraic closure they are translates of the connected abelian kernel. Hence `Q(J1)` is relatively algebraically closed in `Q(J)`. Every putative actual square root, including zero, therefore descends to `Q(J1)`. This does not require the square root to be invariant under the original finite kernel.

For an auxiliary prime ell different from p, `V_ell(S)` is a subrepresentation of the unramified representation `V_ell(R^r)`. The Néron good-reduction criterion gives good reduction of `S`, and its isogeny invariance gives good reduction of `J1`. This step is valid even when the isogeny degree is divisible by p; no prime-to-p degree hypothesis is missing.

A nonconstant coordinate map to the rationally simple surface is surjective up to translation. Poincaré reducibility gives a reverse map whose composite is multiplication by a nonzero integer m. Both maps extend over the good models, and multiplication by m remains surjective in residue characteristic dividing m. Thus the reduced coordinate map is surjective. At the generic point of the smooth special fiber its reciprocal abscissa has valuation zero in both split slots. The argument uses this ordinary vertical divisor with `v(p)=1`, not an exceptional divisor above it.

## Vertical parity argument

In the fixed-root, fixed-slope derivative source, at least one of `H,U` is nonconstant whenever the whole point map is nonconstant. Its reciprocal supplies a unit test in each slot. At positive odd `v_p(u)=nu`, every balanced factor has nonpositive valuation and that selected factor has valuation exactly `−nu`. Therefore `v(V)≥nu` and the actual radicand has exact odd valuation nu, contradicting the descended square.

For the general source, a nonconstant one of the nine point roles forces a nonconstant map among `H,U_i,U_i−Q_i`; otherwise all nine are constant. These are precisely reciprocal tests of field order one. The explicit hypothesis `v_p(lambda+1)=0` is necessary for the displayed argument and is correctly retained. It supplies the same selected factor valuation `−nu`. Without that unit hypothesis, a negative normalizer valuation could invalidate this step. Scalar factors still have nonpositive order by parity even when their own tests have poles. The three retained small-class factors are units at the resulting trace valuation.

The selected good primes of the respective prepared sources meet the hypotheses. Combining with the v69 constant-slope theorems therefore excludes nonconstant abelian families whose images contain such prepared points. It does not exclude those points themselves. Finite point-chart covers cannot create a positive-dimensional family over a constant base point.

## Affine slope with a varying root

Fix rational m,b and impose z=m*a+b. The derivative F_a in u=−18F/F_a is the partial derivative before restriction to this line. Its logarithmic derivative is the sum of the reciprocals of a+c−z and a+c+z. For m different from ±1, the two contact sets each have nine distinct rational roots, and their union has at least nine. A single contact gives a simple pole of F_a/F with residue 1/(1−m) or 1/(1+m). At a collision the residue is their sum 2/(1−m²), which cannot vanish. Therefore u has a simple zero at every distinct contact, with derivative respectively −18(1−m), −18(1+m), or −9(1−m²).

When m=1, a zero constant factor occurs exactly when b belongs to the shift set; when m=−1, it occurs exactly when −b belongs to that set. Such a line makes F identically zero and is excluded by the guards. Every remaining parallel line has nine distinct moving contacts, each with derivative −36. This exhausts the rational affine cases, including fixed slopes as m=0.

The geometric reference-pair argument from v69 excludes every positive odd order along those simple contact fibers. The pole divisor of a=M⁴ is divisible by four, so the product over distinct contacts has even divisor even when their number is odd. Its square root defines a finite étale cover, which after algebraic closure is abelian. A nonconstant a would produce a nonconstant map from that cover to a hyperelliptic curve of genus at least four, a contradiction. Thus a and then T are constant. Rational simplicity and nonconstancy of the trace-abscissa function on R force the root map A to be constant, and z=m*a+b is constant too. The small-class multipliers remain units at the geometric odd-valuation contradiction.

This proves constancy under a fixed rational affine relation, not under unrestricted simultaneous variation of A and z. The fixed-weight vertical theorems and their required hypotheses are unchanged.

## Primary statements independently verified

In Milne, *Abelian Varieties*, v2.0 (2008), author PDF https://www.jmilne.org/math/CourseNotes/AV.pdf:

- Chapter IV, Theorem 3.5, printed p.141: good reduction is equivalent to an unramified rational ell-adic Tate module.
- Chapter IV, Corollary 3.6, printed p.142: good reduction is invariant under isogeny.
- Chapter I, Proposition 10.1, printed p.42: the Poincaré complement construction.
- Chapter I, Remark 17.2, printed p.70: the Néron mapping property used to extend morphisms.

The descent of the square root also follows directly from geometric integrality of the generic fiber, as explained above. No unresolved quotient, good-reduction or valuation gap was found in the stated scope.

## Final source and exact contact replay

The final source includes the precise Milne Chapter I citations identified in this review and the independently checked affine-slope strengthening. The author's exact contact checker was independently rerun: all 35 fixed-slope collision cases passed, with distinct-root counts 9, 14, 15, 16 or 17 and minimum hyperelliptic genus four. Every fixed-slope reduced derivative is exactly −18/multiplicity. Four symbolic local calculations also verify the affine derivatives above, retaining their explicit m≠±1 or guarded parallel-line hypotheses. The noncollision fixed-slope case has eighteen distinct roots and genus eight. This computation verifies contact algebra only, not the quotient, good-reduction or global-witness assertions. The replay is retained as independent_run_certificate.json and is byte-identical to the author's certificate.
