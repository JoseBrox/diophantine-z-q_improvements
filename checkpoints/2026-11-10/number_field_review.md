# Number-field review and exact obstruction

## Conclusions

No counterexample was found to the assertion that the ring of integers of a **finite number field** is Diophantine in that field. None of the primary references reviewed below supplies one. There is also no proof here of the assertion for every number field. The new proved contribution is an obstruction to transferring the project's particular elliptic rank and trace-height inputs unchanged after adjoining `i`.

The existing three number-field papers were read first. The equivalences and finite-correspondence obstructions listed below are retained results, not new claims of this checkpoint. The new result is isolated in:

- `papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.tex`
- `computation/number_fields/check_trace_cancellation.py`
- `computation/number_fields/trace-cancellation-certificate.json`

The standard-library checker passes. The root agent has been notified that these files are frozen and ready for compilation and durable checkpointing.

## Primary-source findings

1. **Alpoge--Bhargava--Ho--Shnidman.** The published paper, *Rank stability in quadratic extensions and Hilbert's tenth problem for the ring of integers of a number field*, Inventiones Mathematicae 243 (2026), 1129--1139 (online 1 December 2025), DOI `10.1007/s00222-025-01392-3`, explicitly states in Corollary 1.2 that the actual subset Z is Diophantine in every ring of integers. This is stronger than the formulation using a Diophantine model in an early arXiv version. The published statement, not the early wording, supports the project's equivalence between defining Z and defining O_K in K. Theorem 1.1 supplies positive-rank abelian varieties with rank stability in arbitrary quadratic extensions.

   Primary PDF: https://link.springer.com/content/pdf/10.1007/s00222-025-01392-3.pdf

2. **Poonen.** The author-hosted manuscript *Rank stability makes rings of integers diophantine*, version dated 3 July 2026, is useful for locating the exact integrality dependence. Theorem 4.2(d) deduces that O_K is O_L-Diophantine from positive-rank stability. It does **not** deduce that O_K is L-Diophantine. Part 4.2(c) starts with an integral element alpha in O_L, and its ideal-divisibility witnesses are also integral. The vertical argument uses the fact that a nonzero norm of an algebraic integer has absolute value at least one. Allowing arbitrary field witnesses removes this bound. Theorem 5.1 gives Shlapentokh's reduction via quadratic descent and totally real fields.

   Primary PDF: https://math.mit.edu/~poonen/papers/h10_over_OK.pdf

3. **Zywina.** *Rank one elliptic curves and rank stability*, arXiv:2505.16960, Theorem 1.1 gives infinitely many rank-one elliptic curves over every number field; Theorem 1.2 gives such curves whose rank remains one in every prescribed quadratic extension. Thus a general absence of rank-one or rank-stable curves cannot be used as a counterexample strategy. This theorem does not preserve the project's specific j=1728 curve or supply its opposite-place prime-order construction and pole predicate. Theorem 1.5 works with the explicit family

   `y^2 = x^3 + 4T(T+1)x^2 + 2T(T+1)^2(T-1)x`

   and point `(-2T(T+1), 2T(T+1)^2)`, together with simultaneous prime patterns and local conditions. This is a concrete alternative curve family if a new field-level construction is attempted.

   Primary PDF: https://davidzywina.github.io/papers/Rank1WithStability.pdf

4. **Eisenträger--Miller--Springer--Westrick.** *A topological approach to undefinability in algebraic extensions of Q*, Bulletin of Symbolic Logic 29 (2023), 626--655, DOI `10.1017/bsl.2023.37`, proves that fields in Qbar whose rings of integers are existentially or universally definable form a meager set (Theorems 1.3 and 5.7). The constructive results, including Theorem 5.12, concern **infinite algebraic extensions**. They provide no finite-number-field counterexample. The number fields themselves form a countable, hence meager, subset of this space, so the category argument cannot force a bad finite field.

   Primary publication: https://www.cambridge.org/core/journals/bulletin-of-symbolic-logic/article/topological-approach-to-undefinability-in-algebraic-extensions-of-mathbb-q/65268ECD074C358FA8E50C6C72B777AE

5. **Silverman.** *The Arithmetic of Elliptic Curves*, second edition, Springer, 2009, DOI `10.1007/978-0-387-09494-6`, supports the standard isogeny, good-reduction torsion injection, and number-field canonical-height facts used in the new elementary obstruction. Relevant chapters are III, VII, and VIII. The publisher information was checked against the author's official book page.

   Author page: https://www.math.brown.edu/johsilve/AECHome.html

## Existing logical reductions and their consequences

The retained papers already prove the following, assuming the project's rational definition of Z and the published ABHS theorem.

- O_K is Diophantine in K if and only if Z is Diophantine in K, and if and only if Q is Diophantine in K.
- If O_L is Diophantine in a finite extension L/K, then O_K is Diophantine in K: expand the ambient L-equations in a K-basis and restrict the input to K. Consequently, a hypothetical bad number field remains bad in every finite extension. A counterexample search may therefore pass to a totally imaginary Galois extension, for example by taking a normal closure and adjoining i. This does not imply that it can be taken to be a CM field.
- For a quadratic extension, a Diophantine graph of the nonidentity automorphism is equivalent to definability of the fixed field. Similarly, the relevant norm and trace graphs require definability of the base field. Introducing conjugation as if it were already an ambient polynomial operation would assume the missing conclusion.
- Rank-stable elliptic constructions can give infinite rationality filters without giving the whole rational subfield. Finite rational-function outputs from abelian varieties, and the retained bounded-denominator finite-correspondence variants, miss almost all members of suitable affine geometric progressions. The exceptional positive-dimensional fibers must be checked separately.
- A finite collection of unchanged defining formulas cannot cover all finite extensions: algebraic witnesses to a false input can be placed in an extension of bounded degree. This is an obstruction to uniform base change, not to allowing a different formula for each field.

A useful field-level analogue of Shlapentokh's organizational reduction would require two inputs still missing here: defining Z in every totally real **field**, and defining the fixed field of each complex conjugation in a totally imaginary Galois field. The intersection of those fixed fields is the maximal totally real subfield. The known integral-domain theorem supplies neither field-level input automatically.

## New exact obstruction

Let K be a number field not containing i, D in K nonzero, and E_D: y^2=x^3-Dx. Put L=K(i), with conjugation sigma, and let iota(x,y)=(-x,iy).

For every Q in E_D(L),

`A=Q+sigma(Q)`, `B=-iota(Q-sigma(Q))`

both belong to E_D(K), and `2Q=A+iota(B)`. The intersection of E_D(K) and iota(E_D(K)) is killed by two. Therefore

`rank E_D(K(i)) = 2 rank E_D(K)`.

For a non-torsion P in E_D(K), set C=(1+iota)P. Then sigma(C)=-iota(C), so every nonzero multiple has

`Tr_{L/K} x([n]C)=0`,

while `h(x([n]C))=4n^2 hhat(P)+O_E(1)`. The absolute trace is also zero. Restricting to even multiples leaves an infinite family of doubled points. Thus no bound by any function of trace height finite at zero can hold on this cyclic subgroup.

The four points `[2n]P`, `iota[2n]P`, `[4n]P`, `iota[4n]P` are pairwise distinct doubled non-torsion points, have pairwise distinct abscissas, and have abscissa sum zero; all four heights tend to infinity. Distinctness follows because `(a-b iota)P=O` would give `(a^2+b^2)P=O` after multiplication by `a+b iota`.

For the project curve over Q(sqrt(2)), D=11-6sqrt(2) and P=2(1+sqrt(2),2sqrt(2)), non-torsion is certified unconditionally. At the prime sqrt(2)=6 mod17, the group has order20 and P order5. At sqrt(2)=5 mod23, the group has order24. A hypothetical torsion P would yield K-rational5-torsion, contradicting its injection into the second reduction. The exact checker verifies both group counts by independent methods, the coordinates, and universal CM identities over the appropriate Laurent polynomial quotient ring.

This is not a counterexample to definability of O_L in L. It identifies why the existing real sum-height argument and fixed rank-one CM curve do not transfer unchanged. The aggregate trace theorem's independence hypotheses are explicitly violated by sigma(C)=-iota(C), so there is no contradiction with that theorem.

## Which parts of the arithmetic architecture could transfer?

The modular-factor multiplicity argument itself uses stable Faltings heights, an exact-sequence inequality, and a dimension-two isogeny bound. These are available over arbitrary number fields and do not require real places. The rationality of the restricted traces in its representation-theoretic input is a separate hypothesis, not an ordering condition. A contact-height theorem for algebraic parameters would still need the corresponding modular realization and level/control hypotheses; the rational theorem does not establish them by base change. Hilbert or Shimura constructions may be relevant in appropriate totally real settings, but no such general replacement is proved here.

Real positivity is used separately in three places. First, aggregation by a sum of squares fails over a field containing i, since 1+i^2=0. Finite systems can instead be combined by an anisotropic norm form, at a possible degree cost, so this alone is not an obstruction to existential definability. Second, positive abscissas prevent the exact cancellation displayed above. Third, the pole predicate's completeness uses a specifically prepared real region; discarding the ordering does not preserve its converse.

The obvious Hermitian repair, replacing a trace or sum by a norm involving complex conjugation, risks circularity: existentially defining the graph of that conjugation already defines its fixed field. A successful new construction must either avoid this graph or provide it independently.

The strongest concrete positive direction from the reviewed literature is to use Zywina's rank-stable rank-one curves as fresh arithmetic input, then rebuild the field-level denominator control and local prime-pattern mechanism. The existence of these curves removes one structural obstruction but not the definability problem. The Q(i) and Q(sqrt(2),i) cases are useful first test cases precisely because the project's original CM architecture fails there in explicit, certified ways.

## Unproved exploratory direction

One possible replacement for an ordered integer-index argument is a Lucas/Pell descent over the Gaussian integers. For `a,t,c` in Z[i], the equation `t^2-a*t*c+c^2=1` admits Vieta transformations. If |a| is large and |t|>=|c|, the transformed coordinate has absolute value `|c^2-1|/|t|`, suggesting a descent in squared Gaussian norm. A complete argument would need all unit terminal cases and a classification of the resulting orbits. It would then still need compatibility with divisibility by a-2, growth estimates, and entirely new contact-height/pole inputs over Q(i). No lemma, count improvement, or definability result is asserted from this observation.
