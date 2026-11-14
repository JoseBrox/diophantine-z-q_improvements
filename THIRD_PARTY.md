# Attribution and source material

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
