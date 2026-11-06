# Third-party sources and dependencies

Project licensing applies only to original project material. It does not relicense the upstream software, papers, source excerpts, or theory files referenced or preserved by this project. Keep any notices supplied with those materials.

## Mathematical sources

- Sohail Farhangi with ChatGPT 6, [*A conditional Diophantine definition of Z in Q from four arithmetic inputs*](October%2011%20Manuscript/ZIsDiophantineInQBySohailsGPT-6.pdf), October 11, 2026. The manuscript is preserved without modification alongside its [provenance and comparison notes](October%2011%20Manuscript/README.md). Its provenance is separate from the current Version 2 collaboration credit.
- OpenAI, [*Hilbert's tenth problem over the rational numbers*](https://github.com/openai/math/blob/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026/main.pdf), October 6, 2026. This is a mathematical input cited by the manuscripts in this repository, not a proof produced by this repository.
- Jonas Bayer, Marco David, Benedikt Stock, Abhik Pal, Yuri Matiyasevich, and Dierk Schleicher, [*Diophantine Equations and the DPRM Theorem*](https://isa-afp.org/entries/DPRM_Theorem.html), Archive of Formal Proofs, June 6, 2022. The entry is distributed under the BSD license linked on its page. The alpha-sequence and exponentiation constructions are credited in the relevant project sources. The curated construction directory does not vendor the Isabelle development.
- Other mathematical sources for [Version 2](quartic_12504.pdf) are identified in its bibliography and [dependency evidence](docs/quartic-12504/README.md). The October 11 manuscript has its own bibliography. Historical review reports preserve their particular citations and scope.

## Build and proof dependencies

| Dependency | License/source of terms | How it is used |
| --- | --- | --- |
| Lean 4 | [Apache 2.0](https://github.com/leanprover/lean4/blob/v4.35.0/LICENSE) | Compiler and proof kernel; installed separately |
| Mathlib 4 and its dependencies | [Mathlib license](https://github.com/leanprover-community/mathlib4/blob/v4.35.0/LICENSE), plus each dependency's notices | Imported by Lean; exact repositories and revisions are in `lean/lake-manifest.json` |
| Tectonic | [Upstream licenses](https://github.com/tectonic-typesetting/tectonic/tree/tectonic%400.17.0) | Downloaded, hash-checked paper compiler; not committed here |
| TeX packages and fonts | Notices in the pinned Tectonic/TeX bundle and the respective package sources | Downloaded build inputs; not committed here |
| GitHub Actions | Each pinned action's upstream license | CI orchestration; referenced by commit hash |

The curated Lean files retain their original comments and attributions. A clean checkout fetches dependencies from their declared upstream repositories; it does not substitute a private dependency tree.

## Historical research archive

The research handoff is a provenance archive with a broader scope than the curated source tree. It includes third-party PDF references, Isabelle theory files, and source excerpts. Those files retain their own authorship and terms.

[Archive reference inventory](docs/archive-reference-inventory.json) groups the saved PDF references and Isabelle theory files by content hash and records their original paths. It is not a complete license audit of every excerpt in the archive. The corresponding historical manuscript's bibliography, archive source manifests, and original documents should be used to resolve attribution and redistribution terms.

The archive inventory does not establish permission to redistribute every source. Where redistribution is not permitted or remains unresolved, use a reference and source URL instead of a copy. The project's original-work license does not relicense the archive's third-party material.
