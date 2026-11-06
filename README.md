# Optimizing polynomial definitions of Z in Q

**Research checkpoint — 6 November 2026**

This project studies explicit polynomial presentations of the ordinary integers inside the rationals. The goal is to minimize (in that order) **total variables**, **polynomial degree**, and **coefficient height** in a statement of the form

\[
x\in\mathbb Z\quad\Longleftrightarrow\quad
\exists y_1,\ldots,y_r\in\mathbb Q:\ P(x,y_1,\ldots,y_r)=0.
\]

The input \(x\) counts as a variable; a polynomial with \(r\) existential witnesses has **\(r+1\) total variables**. Work here starts from the October 2026 [OpenAI preprint on Hilbert's tenth problem over the rationals](https://github.com/openai/math/tree/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026), and the released 12,504-variable quartic.

> **Status and qualification.** The polynomial constructions and their arithmetic interpretation are distinct claims. The supplied certificates verify exact algebraic transformations, finite computations, coefficient tables and selected equivalences, but **do not independently establish** the named arithmetic inputs from the pinned source or Sun's simultaneous prime-pattern theorem. In particular, the claims that the new polynomials define exactly \(\mathbb Z\) remain conditional on those inputs. No assertion of optimality or independent human refereeing is made.

## Best constructions

Each row includes the input variable. In the "size" column, **DAG nodes** measure a compact symbolic representation, whereas **monomials** count distinct terms in a completely expanded polynomial. Those are different metrics.

| Polynomial | Total variables | Witnesses | Degree | Size | Primitive coefficient height |
| --- | ---: | ---: | --- | ---: | --- |
| **41-variable indexed polynomial** | **41** | 40 | at most \(2^{9\,566\,673}\) | 6,018 DAG nodes | at most \(2^{2^{86\,098\,382}}\) |
| **43-variable semilocal polynomial** | 43 | 42 | at most \(2^{236}\) | 6,039 DAG nodes | at most \(2^{2^{240}}\) |
| **558-variable source-preserving polynomial** | 558 | 557 | at most \(2^{3122}\) | 101,637 DAG nodes | at most \(2^{2^{3127}}\) |
| **Smallest quartic in this release** | **1,315** | 1,314 | **4**, exact | **29,021 monomials** | exactly \(64\cdot3^{2^{28}}\) |
| **Small-coefficient quartic** | 1,335 | 1,334 | **4**, exact | 29,050 monomials | less than \(2^{1020}\) |
| Original released quartic | 12,504 | 12,503 | **4**, exact | 135,721 monomials | exactly 685783949153203534233601 |

The bounds for the three indexed rows are *upper bounds*, not expansion statistics. Those polynomials are specified by indexed determinants, finite products, and coefficient directed acyclic graphs; their gigantic expanded coefficient tables were **not** materialized. For the 1,315-variable quartic, the compact coefficient symbol \(S=3^{2^{27}}\) is one **fixed integer**, not an additional variable. All figures are recorded in the 6 November 2026 [standalone manuscript](paper/diophantine_optimization_20261106_v3.tex).

## What makes the constructions smaller?

A central improvement is to test the Lucas polynomial directly on approximate logarithmic ratios:

\[
F(U,V,W)=V^2-U(U-2)VW+(U-2)^2W^2-1.
\]

This eliminates two retained comparison proxies and one finite algebraic generator. Together with sharing elliptic comparison points and finite-algebra compilation, this produces the 41-variable indexed specification. A related semilocal alternative uses 43 coordinates but achieves a dramatically smaller degree bound. Separately, an affine transformation of private anchor witnesses reduces the height of the 1,315-variable quartic while preserving its variable count. Eliminating three more private coordinates yields the 1,335-variable ordinary-integer-coefficient quartic.

These transformations are accompanied by exact algebraic certificates; the numerical improvements are not a claim that the necessary external arithmetic facts have all been independently proved.

## Repository layout and evidence

| Folder | Purpose |
| --- | --- |
| [paper/](paper/) | Complete v3 research manuscript, with definitions, explicit constructions, proofs, comparisons, and bibliography |
| research/phase3/finite_fibre/ | Preferred 41-/43-variable indexed specifications and independent checks (in the complete archive) |
| research/phase3/quartic/ | Expanded 1,315-/1,335-variable quartic tables, producers, and transformation certificates (complete archive) |
| research/phase3/compression/ | Direct Lucas source programs, independent checks, fixed-algebra calculations (complete archive) |
| research/phase3/number_fields/ | Division-norm constructions and counterexamples to naive number-field base change (complete archive) |
| research/phase2/ | 558-variable source-preserving polynomial and previous reductions (complete archive) |
| research/optimization/ | Earlier optimization circuits, quartics, historical comparison artifacts, logs and proofs (complete archive) |
| quartics/quartic-12504/ | Original released quartic, expanded table, certificate, and verification tools (complete archive) |
| reference_upstream/ | Preserved reference manuscripts and source attribution (complete archive) |
| data/ | Machine-readable polynomial benchmark table |
| docs/ and scripts/ | Reproducibility, mathematical status, archive integrity and benchmark tools (complete archive) |

The historic artifact directories use their original names because producers, proofs and SHA-256 receipts refer to those paths. The research package contains **414 archived files**, of which **412** are covered by the archived SHA-256 manifest.

**Publication status:** The complete, checked 424-file repository package (original archive plus paper and new navigation/verification files) has been assembled separately. The GitHub connector has successfully published the paper and repository index; the large certificate/program archive is **not yet present in the remote repository**. Do not interpret links to the research archive directories as evidence that those directories have been committed. Use the complete ZIP provided alongside this publication session to import the remaining files. See [import instructions](docs/IMPORT_ARCHIVE.md). The file tree in that ZIP preserves the original internal paths.

## Reproducing the checks

Once the complete ZIP is unpacked into the repository root, run from the top level:

~~~sh
python3 scripts/check_archive_integrity.py
python3 scripts/report_benchmarks.py
python3 -E -B research/phase3/compression/check_direct_source.py
python3 -E -B research/phase3/number_fields/check_contact_exclusions_20261106_v1.py
python3 -E -B research/phase3/number_fields/check_quartic_base_change_20261106_v1.py
~~~

The new integrity script checks all 412 manifest entries, the standalone manuscript copy, and the six benchmark rows. The original independent checkers and their receipts have different scopes; the old all-in-one verification script also assumes a **pinned upstream checkout** at Git revision `28e87b1b62af0effd954605af7f70b2699dd5672` and should not be run indiscriminately against a reorganized repository. No finite certificate establishes the full arithmetic theorem.

## What is and is not known

The manuscript proves lower bounds excluding a two-variable Diophantine definition and certain quadratic systems under their stated hypotheses. It does **not** produce a polynomial in two through ten variables. The improvement to 41 variables is the best supplied here, not a proven global minimum. Literal quartics do not generally define rings of integers after base change: the manuscript includes exact counterexamples over \(\mathbb Q(i)\), specific input-contact obstructions and a totally real quartic-field obstruction to a finite elliptic-anchor inference. Field-dependent norm constructions combine systems into one equation but do not solve those arithmetic problems.

## Provenance

- **Research manuscript:** [Conditional polynomial constructions, lower bounds, and number-field obstructions for rational Diophantine integrality](paper/diophantine_optimization_20261106_v3.tex), working version 3, 6 November 2026.
- **Pinned base revision:** `28e87b1b62af0effd954605af7f70b2699dd5672`.
- **Upstream:** [OpenAI, *Hilbert's tenth problem over the rational numbers* (6 October 2026)](https://github.com/openai/math/tree/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026).
- **Other mathematical sources:** the LaTeX bibliography documents Sun, Koenigsmann, Daans and the other inputs and comparisons.
- **Authorship and licensing:** the research manuscript discloses ChatGPT-assisted preparation and computational review. Third-party attribution is preserved in the source archive; no blanket license or referee endorsement is implied.
