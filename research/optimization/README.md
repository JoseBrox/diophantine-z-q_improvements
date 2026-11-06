# Polynomial optimization research for review

This directory and **../phase2/** contain a standalone mathematical paper,
exact polynomial specifications, producers, independent checkers, and saved
verification receipts. The pinned source revision is
**28e87b1b62af0effd954605af7f70b2699dd5672**.

All additions are prepared in the local fork checkout on branch
**research/polynomial-optimization**. The released manuscript and polynomial
are unchanged. No commit, push, or pull request has been made.

## Main results

Counts include the input variable. Subtract one for existential witnesses.
The degree and height bounds on indexed polynomials are certified upper bounds,
not exact expansion statistics.

| Total variables | Degree | Form supplied | Coefficient bound |
| ---: | ---: | --- | --- |
| **43** | at most 2^9566680 | Exact indexed finite-algebra polynomial and fixed elliptic exclusion product | at most 2^(2^86098389) |
| **45** | at most 2^243 | Exact indexed finite-algebra polynomial; coefficient DAG materialized | at most 2^(2^246) |
| **558** | at most 2^3122 | Implemented original-source finite-algebra polynomial | at most 2^(2^3127) |
| **1367** | **4** | Complete 29,419-term table over fixed K=3^(2^28) | Exact coefficients supplied over the fixed integer K |
| **1391** | **4** | Complete 29,489-term ordinary integer table | **less than 2^1020** |
| 853 | at most 894,090,701,148,160 | Complete source-preserving integer polynomial circuit | at most 2^29154205340326912 |
| 12,449 | 4 | Earlier source-preserving table over a fixed integer power | Exact height in its receipt |
| 12,465 | 4 | Earlier fully expanded source-preserving integer table | less than 2^3247 |
| 12,493 | 4 | Earlier fully expanded source-preserving integer table | less than 2^80 |
| 12,504 | 4 | Unchanged upstream release | less than 2^80 |

The 43-variable construction reaches the requested range of 10--50 variables
under the stated arithmetic inputs. Its price is an enormous degree. The
45-variable alternative has a substantially smaller degree bound. No global
minimum is claimed.

The indexed formulas specify every finite range, coefficient operation,
determinant, guard and exceptional case. Their huge matrices and outer products
are not materialized. Formal algebra generators used in these formulas are
not quantified coordinates. The new quartics have complete coefficient tables
and full exact expansion checks.

## Arithmetic scope

The 558-variable implementation and the older source-preserving constructions
have the same rational input projection as the pinned original source.
Identifying that set with the ordinary integers requires the source arithmetic
assertion.

The 43/45-variable polynomials and new quartics use a different, shared-point
arithmetic construction. They require the explicitly stated source lemmas and
Sun's simultaneous prime-pattern theorem, arXiv:2610.20691v2, Theorem 4.1.
The paper proves the new construction from those inputs. It does not infer
a definition of the integers merely from an undecidability theorem.

The original restricted pole converse and complete explicit five-contact height
bound, and every ingredient of the cited prime-pattern theorem, have not all
received independent full reproofs here. Exact polynomial checks do not certify
those arithmetic inputs. The paper and receipts state these boundaries.
No unconditional solution of Hilbert's tenth problem over the rationals is
claimed by this review package.

## Other proved results

- An effective reduction from integer polynomial solvability to rational
  polynomial solvability whenever a polynomial defines the integers.
- Quantitative MRDP consequences: with N rational witnesses for the integers,
  every computably enumerable subset of Q uses at most 11N+1 witnesses, and
  rational solvability with at most 9N+2 unknowns is undecidable. At N=42,
  these give 463 and 380, conditionally. These are not record claims.
- A general explicit finite-algebra construction using one additional
  coordinate, with repeated-root cases, separating parameters, guards and
  trace equations fully specified.
- Unconditional lower bounds: degree at least four and at least two
  existential witnesses over every number field; at least five total
  variables for a sum-of-squares quartic; and degree at least eight for a
  globally nonnegative three-variable definition over Q.
- A simultaneous conic obstruction: two jointly quadratic witnesses cannot
  define the ring of integers at any input degree, even by finite disjunction.
- An exact section showing that the released equation accepts every input
  over Q(i). This refutes unchanged extension of that equation; it does not
  refute the existence of another definition of Z[i].
- Conditional number-field transfer equivalences and a bounded-extension
  obstruction to one fixed polynomial working over all number fields.
  The general field-dependent existence question remains unsettled here.

## Read and rebuild the paper

**diophantine_optimization.tex** is a complete standalone LaTeX source with
definitions, proofs, primary references, source-audit boundaries and
reproducibility details. It requires no external inputs or BibTeX database.
Its editable sources are the paper files in this directory and the proof
supplements in **../phase2/**.

From the repository root:

    python3 -E -B research/optimization/assemble_paper.py

The assembly checks braces, environments, unique labels, references and
bibliography keys. A working LaTeX format was not available in the preparation
environment; no successful typesetting or rendered-layout check is claimed.
Compile the standalone source twice with pdflatex in a normal installation.

## Verify the finite computations

The preferred new construction checks are:

    python3 -E -B research/phase2/verify_phase2.py

The aggregate receipt is **../phase2/verification/all-checks.json**.
It runs eleven exact checks and retains all logs. The source, finite-algebra
and quartic package README files contain their producer commands.
The large indexed operations are justified by the proved theorem; the complete
interpreter executes 177 factors over eight deliberately exceptional small
algebras and emits a degree-16 expanded example.

The original-source comparison checks remain available separately:

    python3 -E -B research/optimization/verify_all.py

Their aggregate receipt is **verification/all-checks.json**. They verify the
three earlier quartics, square-root identities, coordinate inventory, exact
number-field section, and 855/854/853 circuits. The parent 855 audit includes
six sampled finite-field formula comparisons, explicitly identified as such;
its source correspondence is separately proved. The later 854/853 substitutions
use exact identities and induction through the circuits.

No checker proves the external arithmetic theorems or global minimality.
Independent programs check the new quartic producers without importing them.

## File guide

| File or directory | Purpose |
| --- | --- |
| diophantine_optimization.tex | Complete paper |
| PR_DRAFT.md | Unsubmitted proposed pull-request description |
| manifest.json | SHA-256 manifest for all bundled research and reference files |
| ../phase2/README.md | Preferred new construction and lower-bound index |
| ../phase2/finite_fibre/ | 43/45/558 indexed polynomials, theorem, bounds and checks |
| ../phase2/new_polynomials/ | New arithmetic systems and source proofs |
| ../phase2/quartic/ | 1367/1391 quartics, exact compiler and coefficient checker |
| ../phase2/lower_bounds/ | Stronger lower bounds, primary source notes and final audit |
| quartic-anchor-packed/, quartic-anchor-packed-large/, quartic-12449/ | Earlier source-preserving quartic comparisons |
| polynomial-853/, polynomial-854/, polynomial-855/ | Earlier complete circuit comparisons |
| paper_parts/source-audit.tex | Partial arithmetic audit and outstanding dependencies |
| ../phase2/continuation_state.json | Current results, hypotheses and next review tasks |

The older exploratory scripts and source variants are retained for comparison.
The preferred frozen artifacts are listed in the phase2 README. Their receipts
and hashes identify the final versions unambiguously.

## Next review priorities

1. Independently review the original restricted pole converse, explicit height
   theorem and the exact simultaneous prime-pattern input.
2. Review the shared-point soundness/completeness proof, scalar normalization
   and all exceptional cases in the finite-algebra theorem.
3. Seek further savings in the nine shared elliptic points and ten pole blocks.
   A more economical size anchor would sharply reduce the 43-variable degree.
   For quartics, focus on shared evaluation and quadratic-preserving elimination.
4. Typeset and review the paper before deciding what to submit upstream.

Prepared with ChatGPT and parallel mathematical/computational reviews.
No independent human review or historical priority claim is implied.
