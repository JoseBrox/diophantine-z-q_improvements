# Attribution and source material

The explicit arithmetic constructions build on the mathematical sources in [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q). The source pins distinguish the coefficient expressions from the arithmetic proofs supporting their interpretation.

| Material used | Pinned source |
|:--|:--|
| Arithmetic and coefficient source for the 29-variable construction | Version 9, commit `14e8f601fe0d9173d4a5f084aedc3e07066a7688`. |
| Kato index-set and retained-class correction incorporated in the arithmetic dependencies | Version 11, commit `650b298a2a18fa956f8859f3ca80e9d7c8cedd82`. |
| Starting quadratic system and coefficient table for the quartic construction | Version 13, commit `5bbd74f6a479776a332cbe036809d5dddae63720`. |
| Simultaneous prime-pattern theorem | Z.-W. Sun, arXiv:2610.20691v2, Theorem 4.1. |

The [arithmetic-dependency paper](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) identifies the exact theorem and lemma statements used. The construction papers retain the attribution of the underlying mathematical arguments and cite the relevant OpenAI, Sun and other primary sources. The nine topic papers each give the references needed for their results.

Exact third-party coefficient objects retained for reproducibility are identified by source path and SHA-256 hash in the computational provenance files. The quartic package records the normalization of line endings in one source file; its polynomial data are unchanged. Adapted source expressions and implementations should be attributed to their indicated sources. These source bindings establish provenance, while the papers state the mathematical hypotheses and proofs separately.

The repository's CC BY 4.0 license applies to original contributions by the project contributors to the extent they have the right to license them. Third-party material retains its original rights and notices. The repository license does not relicense that material, imply endorsement by cited authors, or supersede an existing source notice. External research papers are cited rather than redistributed.
