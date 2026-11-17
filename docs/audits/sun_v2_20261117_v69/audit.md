# Sun v2: arithmetic audit and transferable consequences

Date: 17 November 2026. Repository comparison base: `7501669` (published v67).

## Outcome and scope

The latest inspected source is Zhi-Wei Sun, *Z is diophantine over Q with 26 unknowns*, arXiv:2611.14605v2, 13 November 2026, 39 pages. Its two counts are **27 total coordinates** without an additional abc hypothesis and **17 total coordinates** under ordinary rational abc. The input is excluded from Sun's 26 and 16 existential unknowns. These do not improve the project's established 25 and 11 total-coordinate constructions.

The complete v2 source was read, its substantive changes from v1 were compared, and the arithmetic implications below were independently reconstructed. No essential counterexample was found in those implications under their stated suppliers. This is **not** a complete independent acceptance of the imported prime-pattern, pole-realization, cyclic-generator, aggregate-trace or modular-height foundations. A source citation or an upstream review status is not substituted for such acceptance. The current work gives no 21- or 9-coordinate definition.

The transferable new project result is the power-shift theorem in the companion paper: finite false inputs can be removed without adding a witness coordinate. It sharpens the project's number-field criterion from `d(N+1)` to `dN` total coordinates, with degree at most `2dD`, and makes that degree independent of the number of exceptions. It does not construct an almost-integrality detector over an arbitrary number field. No global priority claim is made for the elementary finite-avoidance device.

## Version and provenance controls

| Source | Pinned version or hash | Role in this audit |
|---|---|---|
| Sun main paper v1 | arXiv:2611.14605v1; TeX SHA256 `db9fd3b3ab981c202ea2805c802098a54ab57f50ac826451dc3149eaf201640e` | Comparison source; 28 existential, 29 total coordinates. |
| Sun main paper v2 | arXiv:2611.14605v2; TeX SHA256 `46fc5724152dfb1756475a63c03d135f49b2ee849def41ae0bb263edfc29278a` | Complete main reduction inspected. |
| Sun pole/prime supplier | arXiv:2610.20691v3, *48 unknowns for Hilbert's tenth problem over the rationals*, 11 November 2026 | Proposition 2.3 and Theorem 4.1 statements matched to their consumers. Recursive analytic and descent foundations remain premises. |
| Burungale | arXiv:2611.16130v1, 12 November 2026 | Proposition 2.3 formal-log proof checked; carrier and five-contact applications matched. Full modular-height proof not accepted by this audit. |
| Kozachinskiy–Pasten–Vidaux | arXiv:2611.17124v1, 12 November 2026 | Comparison of the abc contact-height route; no new count transferred. |
| Granville | *ABC allows us to count squarefrees*, IMRN 1998, 991–1009, Theorem 5, printed p.994 | Author-hosted page image and statement checked. |
| Milne | *Algebraic Number Theory*, v3.08, Theorem 8.31 and Corollary 8.32 | Author-hosted PDF checked for the completely split primes used in the new theorem. |

The downloaded source files are working research copies, not publication deliverables. The included `audit.json` preserves the inspected versions, source hashes, and verified reference locations.

### Substantive changes from v1

1. The aggregate height object is now a half-trace of a **sum** of four abscissas. The source application is to the sum theorem in upstream Section A38. Two ordinary detector scales replace three, removing two free rational pole parameters.
2. Burungale supplies the normalized five-contact estimate and the local formal-log statement. The exact change of contact coordinates is checked below.
3. Theorem 1.2 and Section 11 add the ordinary-abc reduction with four freely represented cyclic points, two ordinary detector blocks and one scalar block.
4. A signed Lucas-growth argument is included directly. The finite separable-algebra compiler and the fixed-multiplier prescription remain existence specifications, without a numerical total degree or an expanded polynomial.
5. Burungale's alternative pole mechanism is discussed but **not substituted** for the two-parameter predicate actually used. Consequently this discussion alone does not remove the inherited pole premise from the construction.

There is a harmless retained phrase referring to three detectors in the CRT discussion after the change to two. The actual list and the completeness construction use two.

### Correct parity interpretation

The mixed-2-adic-valuation product-height example from the project's earlier audit is **not a counterexample to Sun v1**. V1 restricts the relevant root indices to the odd locus, where the product-height identity applies. The exact `log(41)` defect for `P,2P` lies outside that locus. V2's sum-height estimate is valid without parity, so its retained oddness certificates can instead be removed as a simplification of the newer source. These are different statements.

## Decisive checks of the main reduction

The following are audit conclusions and independently reconstructed calculations. They do not assert that every recursively cited paper has been audited.

| Passage | Decisive check | Disposition |
|---|---|---|
| Section 2, cyclic carrier | Exact arithmetic verifies `D=11−6sqrt(2)`, both displayed points on the curve, and `2R0=P`. The coordinate change to the earlier model is by powers of a fixed unit. | Algebra passes; generator and rank assertions remain retained arithmetic inputs. |
| Odd-index lemma | The squareclasses of `1+sqrt(2)`, `−1` and `3−sqrt(2)` are independent by rational norms and the two real signs. The half-point equations give a legitimate duplication before the squareclass implication is used. | Valid under the stated group decomposition. |
| Aggregate trace and two scales | Positivity follows because every nonzero cyclic point is a double. The height estimate is consumed for a sum of abscissas, and `t1/t0=T^2` gives `h(T)≤(h(t0)+h(t1))/2`. | No product-height substitution or parity requirement is introduced. |
| Formal logarithm | In `z=−x/y`, the invariant differential is `(1+4Dz^4)^(−1/2) dz`. Exact series computation checks the stated coefficients through the retained truncation. | Algebra passes. Burungale Proposition 2.3 supplies the relative valuation/precision implication. |
| Section 3, two anchors | At a consumed prime, the anchor difference is a unit. One integer denominator is therefore a unit; its exact ratio is integral first. The comparison test then makes the other ratio integral. Only then is relative logarithmic precision converted to absolute precision and subtracted. | No circular integrality inference found. Zero numerator points use their regular value; the two denominator points remain guarded. |
| Section 4, contact transport | The map `(49s−31213)/(s−13)` carries the five branch values to `{2401,infinity,−343/32,0,1}`. Pullback by `2+1/t` gives the stated five finite contacts; `t=3` is a distinct normalization point. | Exact rational checks pass. Coefficient, determinant and contact-difference primes must remain in the fixed set. |
| Ordinary detector extraction | The scale factor is a rational square. At an odd contact, factor valuations cannot cancel because their parity differs. The trace valuation supplies one common place satisfying the full test list. | All tests are extracted at the same place. No product of separate detector radicals is assumed coprime. |
| Section 5, scalar tree | The seven successive strict valuation coefficients are `1/16,9/16,5/16,13/16,3/8,7/16,15/16`, each below one. Their use is valid at every positive odd contact depth. | Gives the required scalar divisibility without supposing the comparison index is a unit. |
| Section 6, real and finite preparation | Real neighborhoods and bounds are chosen before later congruence moduli. Fixed-place preparation controls coefficients at ramified 2, with exact comparison-index valuations and a deeper scalar index. | The order of choices is consistent at the stated compactness/local-supplier level. |
| Joint CRT | Root labels and scales are fixed before the prime pattern. Repeated positions are merged but all incidences retained. The five contacts of the unit scale remain distinct. The stated plus/minus order gcd and exact 2-adic valuations are compatible with the anchor congruences. | No extra prime theorem inferred from local solvability. The prime-pattern theorem itself remains a supplier. |
| Completeness factorization | For each ordinary block the product is a square factor times the selected primes. At the successful split place inverse factors have residue one; at the other place the relevant product has residue zero or one. The trace is therefore nonzero. | The denominator and trace guards are established on the actual prepared tuple. |
| Fixed-prime completeness | If the normalization has depth `alpha` and the weight numerator depth `nu`, then `v(R)=nu−6alpha`; the transformed tests have the required positive bound `3nu+(10k−8)alpha`. | The same fixed-prime estimate applies before and after removing unused tests in Section 11. |
| Lucas and power-law contradictions | The exponents are `24/64=3/8`, `24/16=3/2`, and `24/48=1/2`. The signed Lucas estimate needs `abs(s)≥7` and `z≠0`; oddness is not needed for that implication. | The comparison grows strictly in the required direction. The source's large fixed multiplier forces the stated range. |
| Point and group-law charts | The generic ordinate quartic has discriminant `8 F1^2(F0^2−2F1^2)^2`, hence is separable for rational `F1≠0`. The zero and pure-component branches cover the remaining cases. Identity and tangent charts are retained. | No denominator division on a discarded zero stratum is used. |
| Finite compiler | Separation occurs before gcd selection. A rational separating value fixes the full tuple by Galois invariance. Dependent roots require a tower, and discriminant inversion is componentwise. | The specialization stratification is substantive and retained; a bare characteristic polynomial would not suffice. |
| Reciprocal guard | The final polynomial equals the reciprocal transform on the open set and equals one when a required guard or final reciprocal variable vanishes. | No spurious zero-guard solution is introduced. Finite disjunction reuses one witness because only one branch must vanish. |
| Multiplier and projection, Sections 9–10 | Classical division-polynomial charts give a finite prescription for each fixed multiplier. The multiplier is chosen only after uniform constants exist. | This is not a numerical defining member or a computed degree certificate. |
| Section 11 and Theorem 1.2 | The abc contradiction is reconstructed explicitly below. Completeness removes unused root/test conditions while retaining two ordinary pole blocks and the scalar block. | Valid at the retained-premise level; no 9-coordinate witness theorem follows. |
| Conjecture 1.3 | A proposed exact definition of `Z` over every number field is stronger than the ring-of-integers target. | It is a conjecture, not a supplied transfer theorem. |

### The abc calculation

Let `R=max(1,abs(n),abs(s))`, `c=abs(s−1)` and `J=abs(num(beta−n))≥1`. The two ordinary blocks imply

```math
R^2\le C_1+\frac{C_{ag}}8\log J.
```

The scalar block and five-contact estimate give

```math
h(\beta)\le C_2+\frac1{24}\log c.
```

Since `c≤R+1` and `J≤(R+1)exp(h(beta))`, substitution yields

```math
R^2\le C_3+\frac{25C_{ag}}{192}\log(R+1).
```

This bounds `R` independently of the eventual fixed multiplier; taking that multiplier large forces a contradiction. If `beta=n`, rational integrality of the input follows from its denominator equation. The count is `8+1+4+2+1=16` existential coordinates: eight for four point abscissas, one slope, four ordinary pole parameters, two scalar pole parameters and one final encoder. The freedom in the pole parameters remains essential to the supplied completeness proof.

## Scoped simplifications of Sun v2

### Removing the unused parity certificates

Retain every nonidentity and denominator guard, but delete the odd-index certificates on `N,T,Z`. Soundness still uses the all-index aggregate trace theorem and the signed Lucas implication. With the original multiplier divisible by six, `s` is automatically odd, but even this parity is not used in the growth contradiction. Completeness is preserved because the previous witnesses remain available.

Per finite branch, nine point-ordinate choices contribute rank at most `4^9`; the nine extra quadratic-field square roots in the parity certificates contribute another `4^9`; and six rational pole roots contribute `2^6`. Deleting the parity conditions therefore reduces this simple branch-rank envelope from `2^42` to `2^24`. The abc source already has no such certificates and has the corresponding envelope `4^4·2^6=2^14`. Finite labels are taken as separate branches in these figures. These are auxiliary-rank bounds, not new total-degree certificates or coordinate records.

### A fixed shift can replace the unspecified multiplication map

This observation concerns Sun's source and is included to explain the connection with the general power-shift theorem. Treat `beta` initially as the input, set `R_sc=Q` and `S=P+Q` (multiplier one), and remove the parity certificates. Keep the rest of the source, including `Q,S,N,T,Z` nonidentity. Write `R=max(1,abs(n),abs(s),abs(t),abs(z))` and `c=abs(s−1)`.

If `Delta≠0`, the ordinary estimate and `abs(Delta)≤10R^4` give

```math
R^2\le C(1+R^{3/2}),
```

so `R` and `c` are bounded. The scalar inequality `h(beta)≤C_sc sqrt(c)` bounds `h(beta)`.

If `Delta=0` but `beta≠n`, the numerator-height argument gives

```math
\log R\le C_2+3C_{sc}\sqrt c.
```

For `abs(s)≥7`, the signed Lucas estimate gives `log R>abs(s)−3≥c−4`, hence bounds `c`; for `abs(s)≤6`, already `c≤7`. Thus in every false-input case, `h(beta)` is bounded by a constant independent of the input. In the abc source the displayed logarithmic contradiction directly bounds `R` and then `h(beta)`.

Completeness for every sufficiently large positive integral `beta` uses the original ordered construction: choose the scalar index divisible by six and the necessary fixed local powers, then the Lucas labels when present, then the contact primes and comparison index. This does not require a large fixed multiplication map. Setting `beta=X^2+B` for an integer `B` above 2401 and above the false-input height threshold gives a definition of `Z`. Indeed, `h(beta)≥log B`, so false inputs are excluded, and rational `X` with integral `X^2+B` is integral. A finite compiler now has degree independent of `B`; no numerical value of that degree has been calculated here.

This retains 27 or 17 total coordinates and is dominated by the project's existing 25/11 families. It is not a new positive record. The same finite-error strategy extends to arbitrary number fields in the companion paper, which is the useful quantitative generalization.

## Contact-height sharpness and novelty crosswalk

Granville's Theorem 5 applied to the product `G` of `r` distinct primitive contact forms gives, under ordinary abc,

```math
H^{r-2-\epsilon}\ll\operatorname{rad}G(u,v).
```

Outside the fixed resultant primes, a prime divides at most one form. If `M` is the odd-contact radical, then

```math
\operatorname{rad}G(u,v)^2\ll |G(u,v)|M\ll H^rM.
```

Consequently, for `0<delta<r−4`,

```math
h(u:v)\le\frac1{r-4-\delta}\log M+O(1).
```

For five contacts this allows any coefficient strictly larger than one, improving the convenient coefficient two in Sun's Section 11. This consequence is **already in this repository**, in `mixed_power_height_20261116_v45.tex` and the derivative-detector source. It is therefore not promoted as new research here.

The requirement of at least five contacts cannot simply be dropped. On `E_5:y^2=x^3−25x`, the point `(25/4,75/8)` is nontorsion, and `a_n=x([n]P)/5` satisfies

```math
 a_n(a_n-1)(a_n+1)=5\bigl(y([n]P)/25\bigr)^2.
```

For a reduced fraction `a_n=u/v`, the product `uv(u−v)(u+v)` has squareclass five. Outside `{2,5}`, the four-contact odd radical for `{0,infinity,1,−1}` is one, whereas the heights are unbounded. The point is nontorsion by the integral-coordinate torsion criterion, and multiplication gives infinitely many abscissas; finiteness of bounded-height rational points then gives the unboundedness. The checker verifies the exact homogeneous identity on the first six multiples, not the infinitude theorem. This is a classical boundary example, consistent with Granville's and Burungale's discussion, not a disproof of the five-contact result.

| Candidate observation | Existing project result | Decision |
|---|---|---|
| Two scales from aggregate sum trace | Aggregate trace, all-point and weighted trace papers; the 25-coordinate source | Already incorporated. |
| Delete v2's odd-index certificates | Current sources already allow the relevant all-index trace bounds | Useful audit simplification only; no record change. |
| Replace a large multiplication map by a fixed input shift | Existing fixed-shift 25/13/11 sources and terminal-root compiler | A smaller degree mechanism for Sun's presentation, with no compiled bound competitive with project records. |
| Coefficient `1/(r−4−delta)` for odd-contact radicals | Mixed-power v45 and derivative-detector v63 | Already present. |
| Finite exceptional inputs via a power shift | v63 finite correction used an extra coordinate and exception-dependent degree | New quantitative project refinement: no extra coordinate; `dN` and `2dD`; eventual-positive variants included. |
| Remove the remaining pole parameters | Current 21/9 criteria require actual detector-trace square realization | Sun supplies no theorem resolving that requirement. |
| Transfer to arbitrary `O_K` | Existing rank-stability and height tools do not give complete integrality detectors | New finite-error criterion lowers the required output quality, but does not supply the detector itself. |

## Upstream work checked to avoid duplication

PR153, head `66d5263809d8a06784b3ee5d5d31125844b260c2`, proposes an explicit 247-coordinate quartic and retains the 195-coordinate result. Its correction inventory was read. The listed v19 issues concern exposition, a stronger unused divisibility citation, coordinate-map verification and formal-log explanation; the inventory itself explicitly does not claim independent acceptance. None of those entries establishes an invalidation of the retained 195-coordinate construction. No whole source-foundation acceptance is inferred from the PR.

PR139, head `ae55e9e393c0eeeaeedf1d28ddc17f628d601f9d`, is a draft consolidation of formalization work. Its status file still records source premises and unfinished glue in the height/rank chain. A mechanical merge and the existence of formal files do not discharge those premises. It supplies no new 21/9 witness theorem in the inspected material.

Both upstream repositories were read only. No comment, review, issue, pull request or external write was made.

## Deliverables and reproducibility

The clean companion manuscript is `power_shifts_and_finite_exceptions_20261117_v69.tex`. It proves the finite-avoidance lemma, the `dN` ring criterion, exact `O_K` and exact `Z` variants in the original `N` coordinates, and eventual-positive versions. For exact `Z`, any exponent `m` with `gcd(m,[K:Q])=1` and only rational mth roots of unity in `K` suffices. A square works exactly when `K` has no quadratic subfield, in particular for every odd-degree field; then both symmetric-error and eventual-positive versions have degree at most `2D`. Real quadratic fields admit a cube, giving `3D` and `6D`. For arbitrary `K`, an odd prime `p` with `p−1>[K:Q]` is a uniform fallback, with degrees `pD` and `2pD`. Coefficients may be ineffective when the exceptional set is only known to be finite.

Run:

```sh
python check.py --output check_certificate.json
```

The checker reconstructs the fixed curve and contact identities, the generic ordinate resultant and discriminant, and the formal-log expansion. It also constructs complete split-prime/CRT avoidance certificates for exponents 2, 3 and 5 in `Q(sqrt(2))`, preserving `B=5 mod 12`, and verifies six exact four-contact examples. These finite computations support the algebra and construction algorithm. They do not prove Chebotarev, the general finite-error theorem, an imported analytic supplier or a complete smaller defining polynomial.

The decisive remaining arithmetic target for 21/9 is still uniform rational realization at the actual coupled detector traces, or a new complete detector source avoiding that requirement. For the number-field problem, it is enough to construct a Diophantine set containing every sufficiently large positive rational integer with only finitely many nonintegral elements; the companion theorem then supplies `O_K` with the sharpened coordinate bound. That construction remains open here.

## Bibliography

- Z.-W. Sun, *Z is diophantine over Q with 26 unknowns*, arXiv:2611.14605v2, 13 November 2026. https://arxiv.org/html/2611.14605v2
- Z.-W. Sun, corresponding v1, 10 November 2026. https://arxiv.org/html/2611.14605v1
- Z.-W. Sun, *48 unknowns for Hilbert's tenth problem over the rationals*, arXiv:2610.20691v3, 11 November 2026. https://arxiv.org/abs/2610.20691v3
- A. Burungale, *A Diophantine definition of Z in Q*, arXiv:2611.16130v1, 12 November 2026. https://arxiv.org/abs/2611.16130v1
- A. Kozachinskiy, H. Pasten and X. Vidaux, *Why should Z be Diophantine in Q?*, arXiv:2611.17124v1, 12 November 2026. https://arxiv.org/abs/2611.17124v1
- A. Granville, *ABC allows us to count squarefrees*, International Mathematics Research Notices 1998, no. 19, 991–1009, Theorem 5. https://doi.org/10.1155/S1073792898000592 ; author copy: https://dms.umontreal.ca/~andrew/PDF/polysq3.pdf
- J. S. Milne, *Algebraic Number Theory*, version 3.08, 19 July 2020, Theorem 8.31 and Corollary 8.32. https://www.jmilne.org/math/CourseNotes/ANT.pdf
- M. Hindry and J. H. Silverman, *Diophantine Geometry: An Introduction*, GTM 201, Springer, 2000, Part B, Section 2. https://doi.org/10.1007/978-1-4612-1210-2
- J. H. Silverman, *The Arithmetic of Elliptic Curves*, second edition, GTM 106, Springer, 2009. https://doi.org/10.1007/978-0-387-09494-6
- Upstream PR153: https://github.com/elliotglazer/diophantine-z-q/pull/153
- Upstream PR139: https://github.com/elliotglazer/diophantine-z-q/pull/139
