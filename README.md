# Polynomial presentations of the integers over the rationals

**Research materials · 6 November 2026**

This repository studies how economically one can write a polynomial equation over the rational numbers whose rational solutions project onto the ordinary integers. The goal is to reduce the **number of variables**, the **degree**, and the **coefficient height**, while retaining precise mathematical hypotheses and independently reproducible computations.

A polynomial $P\in\mathbb Z[X,Y_1,\ldots,Y_r]$ would define $\mathbb Z$ in $\mathbb Q$ if

$$
x\in\mathbb Z
\quad\Longleftrightarrow\quad
\exists\,(y_1,\ldots,y_r)\in\mathbb Q^r:
P(x,y_1,\ldots,y_r)=0.
$$

Here $X$ is the **input variable** and $Y_1,\ldots,Y_r$ are **existential witnesses**. Thus the total variable count is $r+1$—**including** $X$. All counts below use this convention.

> **Scope of the claims.** The algebraic transformations, coefficient tables, and verification certificates are supplied here. Identifying the rational input projections of the new constructions with $\mathbb Z$ requires the explicitly named arithmetic inputs of the [upstream construction](https://github.com/elliotglazer/diophantine-z-q) and, for the shared-point constructions, Sun's simultaneous prime-pattern result. The checkers do **not** independently prove those arithmetic theorems. The results should therefore be read as **conditional polynomial presentations**, not as a new independent proof that $\mathbb Z$ is Diophantine in $\mathbb Q$. See [Mathematical status](docs/RESEARCH_STATUS.md).

## Best polynomial constructions

The following are the best representatives *among the constructions archived in this repository*, not globally optimality claims. Smaller numbers of variables are prioritized, but quartics and smaller-coefficient alternatives are shown separately.

| Construction | Total variables | Witnesses | Degree | Polynomial size | Coefficient height |
|:--|--:|--:|:--|:--|:--|
| [Indexed, minimum variables](research/phase3/finite_fibre/polynomial-41/) | **41** | 40 | $\le 2^{9\,566\,673}$ | 6,018 coefficient-DAG nodes | $\le 2^{2^{86\,098\,382}}$ |
| [Indexed, semilocal](research/phase3/finite_fibre/polynomial-43-semilocal/) | **43** | 42 | $\le 2^{236}$ | 6,039 coefficient-DAG nodes | $\le 2^{2^{240}}$ |
| [Source-preserving indexed](research/phase2/finite_fibre/polynomial-558/) | **558** | 557 | $\le 2^{3122}$ | 101,637 coefficient-DAG nodes | $\le 2^{2^{3127}}$ |
| [Smallest quartic](research/phase3/quartic/quartic-direct-translated/) | **1,315** | 1,314 | **4** | 29,021 nonzero coordinate monomials | $64\cdot3^{2^{28}}$ (exact) |
| [Small-coefficient quartic](research/phase3/quartic/quartic-direct-small-coefficients-1335/) | **1,335** | 1,334 | **4** | 29,050 nonzero coordinate monomials | $<2^{1020}$ |
| [Released reference quartic](quartics/quartic-12504/) | **12,504** | 12,503 | **4** | 135,721 nonzero coordinate monomials | $685783949153203534233601$ (exact) |

**What “size” means.** For the three quartics, the size is the number of *distinct nonzero monomials* in the expanded polynomial. For the three indexed constructions, the enormous determinant/product expression is given by an explicitly specified *coefficient directed acyclic graph (DAG)*. A DAG-node count measures the representation, **not** the number of monomials after expansion. The two types of size are not directly comparable. Degrees and heights for the indexed constructions are certified upper bounds, not exact measurements of an expansion. Height is the largest absolute primitive integer coefficient after fixed constants are substituted. For byte sizes and machine-readable metadata, see [CSV](data/polynomial_benchmarks.csv) and [JSON](data/polynomial_benchmarks.json).

The 41-variable presentation is smallest by variable count in this collection, at the cost of an extremely large degree bound. The 43-variable presentation trades two more coordinates for a much smaller degree bound. Among the quartics, 1,315 variables is the best count here; the 1,335-variable alternative has substantially smaller coefficients.

## Main mathematical idea

The constructions optimize several layers of the rational witness system: the description of points over a quadratic extension, the sharing of elliptic comparison points, finite-choice encodings, denominator guards, and the compilation of finite systems into a single polynomial.

One key step replaces a proxy-variable encoding of an integer relation with the explicit **Lucas-type quartic**

$$
F(U,V,W)=V^2-U(U-2)VW+(U-2)^2W^2-1.
$$

The rational expressions substituted for $U$, $V$, and $W$ allow some intermediate variables and an algebraic generator to be removed. In the direct quartic construction an affine change of private anchor coordinates reduces coefficient height while preserving the projection and the variable count. The fixed integer $3^{2^{27}}$ that appears in that construction is a **coefficient**, not an extra variable.

These statements concern explicit algebraic manipulations. Soundness and completeness as a *definition of the integers* also require the arithmetic hypotheses described in the [paper](paper/diophantine_optimization_20261106_v3.tex) and its [source audit](docs/RESEARCH_STATUS.md).

## Repository guide

| Path | What to find |
|:--|:--|
| [`paper/`](paper/) | [Polished, standalone LaTeX manuscript](paper/diophantine_optimization_20261106_v3.tex) and compiled PDF |
| [`research/phase3/`](research/phase3/) | Preferred 41/43-variable specifications; direct-Lucas and 1,315/1,335-variable quartics; programs, certificates, counterexamples, and independent verification receipts |
| [`research/phase2/`](research/phase2/) | 558-variable indexed construction and preceding compressed polynomial families |
| [`research/optimization/`](research/optimization/) | Earlier circuits, coefficient-height improvements, experimental variants, negative checks, and their scripts |
| [`quartics/quartic-12504/`](quartics/quartic-12504/) | Released reference quartic, complete coefficient table, residual system, certificate, and source reproducibility data |
| [`reference_upstream/`](reference_upstream/) | Archived upstream manuscript and attribution material |
| [`data/`](data/) | [CSV](data/polynomial_benchmarks.csv) and [JSON](data/polynomial_benchmarks.json) benchmark tables |
| [`scripts/`](scripts/) | Independent file-integrity and benchmark reporters |
| [`docs/`](docs/) | [Research status](docs/RESEARCH_STATUS.md), [reproduction instructions](docs/REPRODUCIBILITY.md), and [import/provenance](docs/IMPORT_ARCHIVE.md) |
| [`MANIFEST.json`](MANIFEST.json) | Original research archive: paths, sizes, and SHA-256 hashes for **412 source files** |

**One large-file exception.** The 6.3 MB historical `research/optimization/polynomial-855/polynomial-circuit.json` is stored on GitHub as the **lossless** `polynomial-circuit.json.gz` because the GitHub transfer interface could not accept the uncompressed file in one request. Run `python3 scripts/restore_large_sources.py` to restore the original bytes; both the restored file and the gzip payload are checked against the frozen source manifest. No mathematical data are omitted.

**Provenance rule.** The files in the original research bundle keep their original paths and bytes: older scripts and certificates rely on these exact objects. The paper in `paper/` is an **editorially revised publication copy**, and its original, byte-identical source remains at [`research/phase3/diophantine_optimization_20261106_v3.tex`](research/phase3/diophantine_optimization_20261106_v3.tex). The polished manuscript is intentionally **not** identical to the frozen source; do not use the historical manifest to assert that it is.

## Reproduce the checks

Start from the repository root with Python 3.10 or newer. The top-level metadata checks use the Python standard library:

```bash
python3 scripts/restore_large_sources.py  # one large historical circuit
python3 scripts/check_archive_integrity.py
python3 scripts/report_benchmarks.py
```

The integrity checker compares the 412 frozen files with their recorded SHA-256 hashes and checks the six benchmark entries against the original construction reports. It does not prove the arithmetic inputs, nor does a successful LaTeX compilation.

For deeper verification, follow [the reproducibility guide](docs/REPRODUCIBILITY.md). It identifies the original producer and **separate checker** for each major construction, distinguishes exact identities from sampled tests, and records when a command needs the pinned upstream checkout. For example:

```bash
python3 research/phase3/compression/check_direct_source.py
python3 research/phase2/verify_phase2.py
```

Some historical runners assume the original source-repository layout or perform expensive calculations; read their package READMEs before executing them. The archived `verification.json` files describe the scope of checks performed when the research bundle was produced.

To compile the manuscript:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error diophantine_optimization_20261106_v3.tex
pdflatex -interaction=nonstopmode -halt-on-error diophantine_optimization_20261106_v3.tex
```

## Mathematical limitations and further questions

The paper establishes unconditional lower-bound results **within their stated hypotheses**: two total variables are impossible for the target Diophantine definition, a single defining polynomial must have degree at least four, and a system of quadrics presenting an infinite subset of a number field's ring of integers requires at least three independent quadratic equations (hence at least five total coordinates for a quadratic system defining the full ring). None of this establishes that 41 variables is optimal or produces a definition in **3–10 total variables**.

The same polynomials do not automatically define rings of integers in number fields. The research package includes explicit obstructions over $\mathbb Q(i)$ and a totally real quartic extension, as well as a field-dependent division-norm method for combining finite systems without new variables. See the [technical manuscript](paper/diophantine_optimization_20261106_v3.tex) for hypotheses and proofs.

## Sources and attribution

- OpenAI, *Hilbert's tenth problem over the rational numbers*, preprint, 6 October 2026: [preprint source](https://github.com/openai/math/tree/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026).
- Original polynomial construction: [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), pinned source commit `28e87b1b62af0effd954605af7f70b2699dd5672`.
- Further references (Daans, Koenigsmann, Sun, and others) are cited in the [manuscript bibliography](paper/diophantine_optimization_20261106_v3.tex).

The research includes computer-assisted manuscript preparation and verification. Mathematical dependencies and independent verification scope are documented explicitly. Third-party files retain their own notices; this repository does not assert a blanket license over those materials.
