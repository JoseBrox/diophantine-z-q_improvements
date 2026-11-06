# Z is Diophantine in Q

## Version 2

This repository contains the manuscript *Z is Diophantine in Q*, Version 2, and its explicit quartic polynomial in 12,504 variables. The complete polynomial, its source system, and the certificate checks accompany the manuscript.

Version 2 is a collaboration using the collective agentic notes from Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jenn Park, Caroline Terry.

| To | Open |
| --- | --- |
| Read Version 2 | [Manuscript PDF](quartic_12504.pdf) |
| Inspect or edit the manuscript | [TeX source](quartic_12504.tex) |
| Read the complete polynomial and check its certificate | [Quartic package](quartics/quartic-12504/README.md) |
| Inspect the proof dependencies and review evidence | [Version 2 evidence](docs/quartic-12504/README.md) |
| Build the manuscript or run the checks | [Build instructions](docs/building.md) |
| Download the Version 2 research handoffs | [Full handoff](https://github.com/elliotglazer/diophantine-z-q/releases/download/quartic-12504-version-2/z-in-q-version2-full-handoff.zip), [current-only handoff](https://github.com/elliotglazer/diophantine-z-q/releases/download/quartic-12504-version-2/z-in-q-version2-current-handoff.zip), [contents and verification](handoff/README.md) |
| Read the October 11 manuscript | [October 11 manuscript and provenance](October%2011%20Manuscript/README.md) |
| Find earlier constructions and research history | [Research guide](docs/research-guide.md) |
| Inspect the partial formalization | [Accepted Lean helpers](lean/README.md) |
| Cite the manuscript or report an issue | [BibTeX](CITATION.bib), [contribution guide](CONTRIBUTING.md) |

The full handoff combines the current public snapshot and selected research notes with the unchanged November 4 archive. The current-only handoff omits that embedded archive. The handoff guide specifies the included collections and verification procedure.

## The polynomial

The manuscript presents a fixed polynomial with integer coefficients such that, for every rational number $q$,

$$
q\in\mathbb Z
\quad\Longleftrightarrow\quad
\exists\,\mathbf w\in\mathbb Q^{12\,503},\quad P(q,\mathbf w)=0.
$$

The input and every auxiliary variable range over the rationals. The released polynomial has the following exact statistics.

| Quantity | Value |
| --- | --- |
| Total variables, including the input | 12,504 |
| Rational witness variables | 12,503 |
| Total degree | 4 |
| Nonzero monomials | 135,721 |
| Maximum absolute coefficient | 685,783,949,153,203,534,233,601, strictly less than $2^{80}$ |
| Quadratic residuals whose squares are summed | 11,939, all with weight 1 |

The [full monomial table](quartics/quartic-12504/polynomial.expanded.txt) specifies the polynomial explicitly. Its SHA-256 is `7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca`. The [verification receipt](quartics/quartic-12504/verification.json) records the certificate and source identities. These are statistics of this construction, not a claim of minimality.

## Verification status

The certificate checks establish exact projection-preserving algebraic equivalence to the pinned source system and verify the full integer expansion. They check both directions of the algebraic transformations. They do not prove the source system's arithmetic characterization of the integers.

The manuscript supplies that arithmetic argument. The [Version 2 evidence](docs/quartic-12504/README.md) identifies its dependencies, source changes and review scopes. The [earlier theorem-application inventory](docs/theorem-application-audit/README.md) contains 82 scoped decisions for its own frozen manuscript. Its recorded internal premises and version boundaries remain in force. It is not a blanket audit of every later statement.

The Lean formalization is incomplete. The accepted snapshot contains 48 helper modules; the main bounded-polynomial declaration still contains `sorry`. AI review and successful finite checks do not constitute independent human peer review or a completed formal proof.

## Earlier work and provenance

The October 11, 2026 manuscript, *A conditional Diophantine definition of Z in Q from four arithmetic inputs*, was produced by Sohail Farhangi with ChatGPT 6. Its PDF is preserved separately and without modification. Its provenance and conditional scope are distinct from Version 2.

The earlier November 5 manuscript was produced by Elliot Glazer with Astra 6, Sol 6.1, and Opus 5.5, with auditing from Fable 5.1. Earlier manuscript revisions remain in Git history. The [November 4 research handoff](https://github.com/elliotglazer/diophantine-z-q/releases/tag/research-handoff-2026-11-04-r2) and its checksum identify a historical archive; that archive is not an updated copy of Version 2 or its quartic package. The [original large construction](construction/README.md) and its checks remain available for comparison.

The project builds on OpenAI's October 6, 2026 preprint, [*Hilbert's tenth problem over the rational numbers*](https://github.com/openai/math/blob/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026/main.pdf). The manuscript's bibliography and dependency records identify the other mathematical inputs.

The manuscript author field is blank, and [CITATION.bib](CITATION.bib) intentionally omits author fields. See [archival notes](docs/archiving.md) for citation and DOI status, and [third-party notices](THIRD_PARTY_NOTICES.md) for source attribution and redistribution scope.
