# Attribution and source material

## Rationality descent and rank stability (v81)

The number-field descent architecture is due to **Hector Pasten and
Xavier Vidaux, *On Hilbert's tenth problem for number fields*,
arXiv:2611.24748v1 (18 November 2026)**:
[primary source](https://arxiv.org/html/2611.24748v1), Theorem 1.1 and
Sections 2–6. The repository's amplified descent, all-rational and real
approximation, cubic rational map, prepared-pole replacement and
coordinate encodings are subsequent extensions, explicitly separated
from that source in their proofs.

The quadratic-field application uses **David Zywina, *Rank one elliptic
curves and rank stability*, arXiv:2505.16960v1, Theorem 1.2**:
[primary source](https://arxiv.org/html/2505.16960v1). The prepared pole
and rational witness density use Burungale's published Theorem B in
its beta-seven, eta-one classes, as specified below. These external
papers are cited, not redistributed. Composition with the rational
integer constructions retains their original attribution to **notes
of Gabe Conant with Astra 6.2** and all their stated arithmetic inputs.

## Busy Beaver effectivity: Elliot Glazer's agentic notes (v86–v87)

The **explicit numerical Busy Beaver parameter** for the 163-variable quartic was derived using the agentic research notes and [Version 22 manuscript](https://github.com/elliotglazer/private-diophantine/blob/4b43ba288b9b8639cc5cc85f8c1507d64c698659/manuscripts/quartic_v22.tex) of **Elliot Glazer's research project** (pinned commit `4b43ba288b9b8639cc5cc85f8c1507d64c698659`; access to the private repository may require permission). Version 22 specifically attributes its new Busy Beaver estimate and receiving-source checks to an **OpenAI Codex agent**; it acknowledges Elliot Glazer's direction of the broader agentic research. The v86/v87 papers use that quantitative Vojta record method and its geometric/compiler arguments, then sharpen the record scale and coefficient bounds. Separately, the underlying 163-variable scalar-point construction and tables are **Jose Brox's**, based on **Gabe Conant's** shared-product constructions with Astra 6.2. Each contribution is separately identified; the published finite regression checks are not independent proofs of all source mathematics.

## Earlier source map

The explicit arithmetic constructions build on the mathematical sources in [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q). The source pins distinguish the coefficient expressions from the arithmetic proofs supporting their interpretation.

| Material used | Pinned source |
|:--|:--|
| Arithmetic and coefficient source for the 29-variable construction | Version 9, commit `14e8f601fe0d9173d4a5f084aedc3e07066a7688`. |
| Kato index-set and retained-class correction incorporated in the arithmetic dependencies | Version 11, commit `650b298a2a18fa956f8859f3ca80e9d7c8cedd82`. |
| Starting quadratic system and coefficient table for the quartic construction | Version 13, commit `5bbd74f6a479776a332cbe036809d5dddae63720`. |
| Simultaneous prime-pattern theorem | Z.-W. Sun, arXiv:2610.20691v2, Theorem 4.1. |
| Uniform family height theorem used in the 27-variable and 317-variable existence results | J. Von Buhren, *Borne de hauteur semi-effective pour le problème de Mordell–Lang dans une variété abélienne*, J. Théor. Nombres Bordeaux **29** (2017), 307–320, Theorem 1.1, [doi:10.5802/jtnb.981](https://doi.org/10.5802/jtnb.981). |

The [arithmetic-dependency paper](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) identifies the exact theorem and lemma statements used. The construction papers retain the attribution of the underlying mathematical arguments and cite the relevant OpenAI, Sun and other primary sources. Each topic paper gives the references needed for its results. The [aggregate trace-height paper](papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) proves the geometric hypotheses needed to apply the uniform height theorem and states its ineffectivity explicitly.

Exact third-party coefficient objects retained for reproducibility are identified by source path and SHA-256 hash in the computational provenance files. The quartic package records the normalization of line endings in one source file; its polynomial data are unchanged. Adapted source expressions and implementations should be attributed to their indicated sources. These source bindings establish provenance, while the papers state the mathematical hypotheses and proofs separately.

The repository's CC BY 4.0 license applies to original contributions by the project contributors to the extent they have the right to license them. Third-party material retains its original rights and notices. The repository license does not relicense that material, imply endorsement by cited authors, or supersede an existing source notice. External research papers are cited rather than redistributed.


## Sources integrated in v27

The upstream 214-coordinate numerical source is pinned to `elliotglazer/diophantine-z-q` commit `1f7e1f1fb0438feda3c9f3da9cc16982126aeeed`, with exact source identities in `computation/quartic/balanced214_v24/PROVENANCE.json`. The original construction and arithmetic arguments retain the credit recorded by that source. The successive contributions here are coefficient balancing, additive contact arguments, recovered reciprocal differences and the weighted-height application. No upstream repository was changed by this publication.

The new abc pole realization uses **Manvir Jaswal, A proof that Z is Diophantine in Q through congruent-number twists, Hexagon 2611.00331v2 (12 November 2026), Theorem 1.2**, available at https://hexagonmath.org/pdf/2611.00331v2. The exact squareclass application and coordinate transformations are proved in `papers/pole_parameters/congruent_twist_poles_20261114_v27.tex`. This attribution does not claim a completed independent audit of the entire source paper or use its separate height and prime-pattern assertions.

The positive weighted trace theorem applies the final published **Jérôme von Buhren, JTNB 29 (2017), 307–320, Theorem 1.1, p. 308**, with the actual fixed finite-rank group, projective embedding, graph family and exceptional translates checked in `papers/trace_heights/weighted_trace_20261114_v27.tex`. External papers are cited, not redistributed.

## Source supplied for the v30 common-twist application

The user-supplied project audit *A row-5a audit and a simultaneous-twist
strengthening: On Manvir Jaswal's congruent-number route to Diophantine
definability*, dated 13 November 2026, is preserved unchanged in
`sources/hexagon/jaswal_row5a_audit_and_simultaneous_twists_20261113.tex`.
SHA-256: `6764fcb1f3fd5d21494b9d18818f20abcb1f47d8d543829df69344223bf92bdb`.
This is supplied project source material, not a redistribution of the external
Hexagon paper. Its finite-family theorem (label `thm:sim`) is distinguished from
Jaswal's original two-twist Theorem 1.2. The new application retains that theorem
as an explicit input and does not claim to complete its independent arithmetic
audit. The subalgebra-norm degree improvements use no new twist input.


## Uploaded 198-variable research archive (v38 integration)

`sources/h10_quartic198/` preserves the supplied `H10-quartic198.zip` members
unchanged. Its README attributes new analysis and code to ChatGPT in
collaboration with Gabriel Conant's research request. It includes selected
original sources and licenses from Jose Brox's repository and a pinned
upstream arithmetic note. Those notices are retained. Our 196-variable
construction is an exact subsequent coordinate transformation, not a claim
to authorship of the supplied 198-variable reduction. The archive identity
is bound in `ARCHIVE_ORIGIN.json`; all source bytes appear in the main manifest.

## Prepared pole input from Burungale

The intrinsic degree-nine pole block uses **Ashay Burungale, A Diophantine definition of Z in Q, arXiv:2611.16130v1 (12 November 2026), Theorem B**: [primary source](https://arxiv.org/html/2611.16130v1). The [intrinsic pole manuscript](papers/pole_parameters/intrinsic_pole_20261117_v56.tex) checks the squarefree, congruence and reciprocal local-square hypotheses and proves the coordinate transformations, density and all-character guards. It does not claim an independent reproof of Theorem B or import the paper's separate height and prime-pattern theorems. Existing construction records retain their stated arithmetic premises. The external paper is cited, not redistributed.

## Intrinsic source transfers and prepared descent obstructions

The complete intrinsic source transfers use A. Burungale, *A Diophantine definition of Z in Q*, arXiv:2611.16130v1, Theorem B, in the exact prepared-input form stated in the repository intrinsic-pole paper. The other source arithmetic premises remain explicit. The new source variants have no separately certified numerical full determinant bound.

The prepared covering obstruction uses the full 2-descent, Monsky-matrix and Cassels-pairing conventions in Z. Wang, *Congruent Elliptic Curves with Non-trivial Shafarevich-Tate Groups*, arXiv:1511.03810v2, Sections 2.1–2.2 ([primary paper](https://arxiv.org/pdf/1511.03810)), and S. Zhang, *On non-congruent numbers as multiples of non-congruent numbers*, 28 August 2025, Sections 2.1–2.2 ([author manuscript](https://zhangshenxing.github.io/publications/Zhang2025.pdf)). Its specific conics, tangent identities, all-prime local factors and Mordell–Weil point are proved and exactly checked in this repository. The proof does not infer rank from a numerical L-value or assume finiteness of the Tate–Shafarevich group.

The cubic trace rank theorems, including the four-term trace cubic, use **B. Mazur, Modular curves and the Eisenstein ideal, Publications Mathématiques de l’IHÉS 47 (1977), 33–186, Theorem 8 and III, Theorem 5.1**, for the classification of rational elliptic torsion. The division-polynomial recurrence and vanishing criterion are as stated in **J. H. Silverman, The Arithmetic of Elliptic Curves, second edition, Chapter III, Exercise 3.7**. The coefficient, projective-residue and direct group-law certificates are supplied in this repository. The external sources are cited, not redistributed.

## Geometric reference for actual multiplication surfaces

The obstruction in [the actual multiplication-surface paper](negative_results/papers/rational_fibers/actual_multiplication_surface_20261117_v58.tex) uses the characteristic-zero Riemann–Hurwitz formula in the Stacks Project, [Section 53.12, tag 0C1B](https://stacks.math.columbia.edu/tag/0C1B). It concerns uniform rational identities on the specified full surface, not individual rational witnesses. The small trace-class preparation uses the already cited Sun Theorem 4.1 with its existing odd avoidance modulus containing three.

## Derivative detector and fixed-slope incidence

The eleven-variable height argument uses Z. Rudnick, P. Sarnak and A. Zaharescu, *The distribution of spacings between the fractional parts of n²α*, Inventiones Mathematicae **145** (2001), 37–57, Appendix A.2, equation (A.2): [author PDF](https://www.math.tau.ac.il/~rudnick/papers/rsz.pdf). That precise homogeneous squarefree-form consequence requires ordinary rational abc. Its prime realization uses the explicitly arbitrary fixed finite number of positions in **Sun, arXiv:2610.20691v3, Theorem 4.1**: [primary text](https://arxiv.org/html/2610.20691v3). The inherited elliptic and intrinsic-pole premises remain as stated in the construction paper.

The fixed-slope incidence proof uses J. S. Milne, *Abelian varieties*, Proposition 12.1 ([author notes](https://www.jmilne.org/math/xnotes/AVs.pdf)), and Z. Gao, T. Ge and L. Kühne, *The Uniform Mordell–Lang Conjecture*, Publications Mathématiques de l’IHÉS **143** (2026), 189–235, Theorem 1.1 and equation (1.1) ([author manuscript](https://ziyangjeremygao.github.io/articles/UML.pdf)). The repository proves the required rational endomorphism calculation and nonconstancy hypotheses. These external works are cited, not redistributed.

## Primitive denominators, elliptic indices and quotient-height obstructions

The primitive-prime argument builds on the duplication and canonical-height method in **G. Cornelissen and K. Zahidi, Elliptic divisibility sequences and undecidable problems about rational points, arXiv:math/0412473v3, Proposition 3.10** ([primary manuscript](https://arxiv.org/pdf/math/0412473v3)), and **J. H. Silverman, Wieferich's criterion and the abc-conjecture, Journal of Number Theory 30 (1988), 226–237, Lemma 13**, [doi:10.1016/0022-314X(88)90019-4](https://doi.org/10.1016/0022-314X(88)90019-4). The repository proves its stated coefficient, coprime-index refinement and exact local application. Canonical-height comparisons and multiplication-map division polynomials use **Silverman, The Arithmetic of Elliptic Curves, second edition, Chapters III and VIII**.

The fixed rational carrier obstruction uses Siegel's theorem in rational-function form as stated in **A. Levin, Siegel's theorem and the Shafarevich conjecture, Journal de Théorie des Nombres de Bordeaux 24 (2012), 705–727, Theorem 1.1**, [doi:10.5802/jtnb.818](https://doi.org/10.5802/jtnb.818), [published PDF](https://www.numdam.org/article/JTNB_2012__24_3_705_0.pdf). The proof checks positive genus and nonconstant input on each relevant degeneration component. It concerns intended integer witnesses of the specified support architecture. These external sources are cited, not redistributed.

## Local fibers and varying rational levels

The varying-level pole theorem retains Burungale's exact simultaneous-twist input above. Its local proof uses **W. Aitken and F. Lemmermeyer, Counterexamples to the Hasse principle, Theorem 6 and Appendix C**, [author manuscript](https://public.csusm.edu/aitken_html/CounterHasse.pdf), for a nontrivial point on a nonsingular binary quartic over an odd residue field. The exact rational maps, infinite selected levels, character guards and explicit examples are proved in the repository. The external paper is cited, not redistributed.

## Canonical explicit-polynomial measurement

The compact 229-variable package includes unchanged copies of the explicit-record notation and measuring program from [elliotglazer/diophantine-z-q, commit 970ec6bf338dc47fad151132a4122fd5c899e348](https://github.com/elliotglazer/diophantine-z-q/tree/970ec6bf338dc47fad151132a4122fd5c899e348/docs/explicit-record). Their original paths are `docs/explicit-record/README.md` and `docs/explicit-record/measure_plain_text.py`. Their SHA-256 digests, source URLs and Git blob identities are retained in `computation/quartic/explicit229_compact_v68/transformation.json`. These files specify and measure the upstream notation; the new coefficient normalization and independent algebra checker are separate project work. Meeting the notation's size requirement does not assert upstream review or acceptance.


## Gabe Conant’s notes with Astra 6.2 (v78 integration)

The supplied `H10-quartic-constructions.zip` and
`H10-eleven-variable-constructions.zip` are **notes of Gabe Conant with
Astra 6.2**. They supply the shared-product reductions 193→165 and
229→180, the conditional quartic reduction 68→62, the weak-abc reduction
13→11, and their associated finite-algebra and realization notes. The
[attribution record](computation/coauthor_audit_v78/ATTRIBUTION.md)
distinguishes these source contributions from the subsequent independent
audit and extensions. Original source files and archive checksum lists
remain unchanged; historical technical identifiers retain their spelling.

The six integration papers, current proof guide, package documentation and
main README use this named attribution. The earlier 198-variable archive
is separately attributed above and is not relabeled as part of these new
notes.


## Elliptic divisibility and algebraic descent (v82)

The prepared divisibility detector cites **G. Cornelissen and K. Zahidi, Elliptic divisibility sequences and undecidable problems about rational points**, Journal für die reine und angewandte Mathematik 613 (2007), 1–33, [arXiv:math/0412473v3](https://arxiv.org/pdf/math/0412473), Proposition 3.10(iii), and **J. H. Silverman, Wieferich's criterion and the abc-conjecture**, Journal of Number Theory 30 (1988), 226–237, [doi:10.1016/0022-314X(88)90019-4](https://doi.org/10.1016/0022-314X(88)90019-4), Lemma 13. The v82 manuscript also supplies its own direct ordinary-abc argument for the specified curve. These papers are cited, not redistributed.

The curve and recorded Mordell–Weil generators are sourced to **The LMFDB Collaboration**, [elliptic curve 256.b1](https://www.lmfdb.org/EllipticCurve/Q/256/b/1), consulted 20 November 2026. The exact rank, torsion and conductor checks are distinguished from that generator assertion.

The new genus-one obstruction uses **PARI/GP 2.17.4**, through **PassageMath PARI 10.8.14**, for unconditional algebraic lower and upper rank bounds; see the [ellrank documentation](https://pari.math.u-bordeaux.fr/dochtml/html/Elliptic_curves.html#ellrank). The code, exact Kummer calculation and certificates are project work. No analytic-rank or BSD inference is made, and a second descent on an isogenous curve is not represented as an independently implemented algorithm.
