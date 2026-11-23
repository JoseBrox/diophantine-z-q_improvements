# Exact conditions and remaining gaps in quotient merging

This checkpoint records proved algebra and the specific missing hypotheses in several possible reductions. It adds no variable-count claim. In particular, a condition that holds after the old integer reconstruction must not be used circularly to justify deleting an integrality predicate that that reconstruction needs.

## 1. Coprime denominator lemma

Let A, B, m, n be integers with mn nonzero and gcd(|m|,|n|)=1. Put α=A/m and β=B/n. If α+β is an integer, then α and β are integers.

Indeed, if α+β=T∈Z, then An+Bm=Tmn. Reduction modulo m and coprimality give m|A; reduction modulo n gives n|B. Negative denominators cause no change. The converse is immediate.

Thus, when two independently established rational quotients have coprime integer denominators, one integer predicate on their sum can replace the two predicates. Both numerator-integrality assertions and the coprimality assertion must already be available in the reduced system. The lemma alone does not establish them.

## 2. The two Jones quotient denominators

In the corrected binomial source write

- M=n², U=wM, and L=rsM;
- a=(U+1)L and p=2UL²;
- d₁=p−1=2UL²−1 and d₂=4a−5=4(U+1)L−5.

The small-Pell quotient is h=(k−r−1)/d₁. The linear Pell quotient is γ=(d−bw−(a−2)c)/d₂. When the relevant numerator coordinates have independently been shown integral, these are quotients of integers.

Define R(U)=8U²−9U+8. The exact polynomial identity

> R(U)=U d₂(d₂+10)−8(U+1)²d₁

shows that gcd(d₁,d₂) divides R(U), including its full prime-power multiplicity. There is no division by2 or5 and no exception hidden in this divisibility.

Both denominators are odd, so2 never divides their gcd. Also5 never divides their gcd: if5|d₂, then either5|L or U≡−1 mod5. The first case gives d₁≡−1 mod5. In the second case d₁≡3L²−1 mod5, and its vanishing would require L²≡2 mod5, impossible. A common factor7 can occur: U=1,L=5 gives d₁=49,d₂=35 and gcd=7=R(1). This is an example for the displayed algebraic parametrization; it is not claimed to satisfy the entire universal source or the additional condition that U be a particular large power of two.

If L were a multiple of R(U), then d₁ and d₂ would be coprime. To see this, a common prime would divide R(U), hence L, while d₁≡−1 at that prime. This is a sufficient condition, not an established condition on the actual source witnesses.

### Two separate gaps prevent a count reduction

First, s is not a freely chosen padding variable in the binomial certificate. The complete sufficiency proof in `undecidability/papers/binomial_pell_certificate.tex`, “Proof of Theorem1: sufficiency,” sets

> w=2^(2r+1)/b, U=wM,
> T=Σ_{j=0}^r binom(2r,j) U^(r−j), and s=T/M.

The necessity proof forces the same Y=T and hence the same s. One cannot simply require s, and therefore L=rsM, to be divisible by R(U) while citing the old completeness proof. The corresponding divisibility or a new padding theorem would have to be proved.

Second, if the integer predicate on h is removed, integrality of k is no longer available merely from k=r+1+h(p−1). The rational Pell conic for k and τ does not by itself prove that k is integral. Therefore even a separate proof of gcd(d₁,d₂)=1 would not alone license applying the coprime denominator lemma to h and γ. An independent reconstruction of the needed numerator integrality is also required. This circularity is distinct from the gcd obstruction.

## 3. The third-Pell quotient

The v95 construction replaces two integer quotients by one integer J through

> H=c+F²(B−c)+cFJ, with B=2r+1.

It enforces H≡B modc and H≡c modF. Its complete proof and coefficient tables are in `undecidability/pell_crt_v95/one_quotient_pell.tex` and the neighboring files. The positive completeness construction can vary a later Pell index in an arithmetic progression. This freedom does not prove that the resulting J equals a prescribed h or γ, or that a proposed linear combination of quotients has a sound inverse reconstruction. Merging γ with J by the coprime denominator lemma would, at minimum, require independent integrality of both numerators and control of gcd(4a−5,cF). No such uniform coprimality statement is proved here.

## 4. An alternative abc guard saving, already covered by v96

In the v95 ordinary-abc table, the input i is an ordinary integer-predicate coordinate, c² is already stored as `int_c_29`, and `i_inverse` occurs exactly in the two rows

> i·i_inverse=1 and i_inverse·E=c².

There is also the separate guard s·s_inverse=1, and the existing coordinate AE satisfies AE=aE. Against this v95 predecessor one may replace the three displayed inverse/source rows by

> E=i c² and AE·AE_inverse=1.

This removes two inverse coordinates and adds one, saving one coordinate and one quadratic row. For soundness, the new unit gives AE≠0, so a≠0 and E≠0. The first relation then gives i≠0. Since a=(U+1)rsM, nonvanishing of a implies s≠0. Thus the old inverse coordinates can be recovered. Conversely, the old signed-binomial reconstruction gives a>0,c>0 and i≠0, so AE≠0 and the new inverse exists.

This is an outer-instance equivalence under the retained arithmetic and signed-binomial reconstruction, not a claim that the predecessor equations alone establish a≠0 without those results.

The general and specified routes use genuine reciprocal charts for the i integrality predicate: `i_inverse` has additional occurrences inside those blocks, and c² is represented by a product of two stored coordinates. The preceding literal deletion therefore applies only to the ordinary-abc chart.

The v96 half-trace branch already removes s_inverse and its guard. After that reduction, replacing i_inverse by AE_inverse has zero net coordinate saving. Consequently this alternative abc chart must not be added to the v96 saving or advertised as a further numerical record.

## 5. Verification and status

The gcd identity and the small-prime assertions are elementary polynomial and modular calculations. The accompanying `verify_quotient_merging.py` verifies the identity symbolically, checks all residue classes needed for the2 and5 assertions, and checks a finite set of gcd-divisibility examples by exact integer arithmetic. The universal conclusions are the arguments above, not an extrapolation from that finite sample.

No new simultaneous-completeness assertion, arithmetic premise, or undisplayed integrality condition is introduced. The unresolved items are numerator integrality after predicate removal, uniform gcd control, and preservation of the actual binomial witness construction.
