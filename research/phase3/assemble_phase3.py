#!/usr/bin/env python3
"""Create a fresh standalone paper, preserving the preceding complete paper."""
from pathlib import Path
import importlib.util
import json
import re
import hashlib
import os

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "optimization" / "diophantine_optimization.tex"
OUTPUT = HERE / "diophantine_optimization_20261106_v3.tex"


def read(name):
    return (HERE / name).read_text()


def replace_once(text, old, new):
    assert text.count(old) == 1, (old[:90], text.count(old))
    return text.replace(old, new, 1)


def insert_before(text, marker, addition):
    return replace_once(text, marker, addition + "\n\n" + marker)


def assemble():
    text = OLD.read_text()
    text = replace_once(text,
        r"\title{Variable bounds and exact transformations for a proposed\newline" + "\n" +
        "Diophantine definition of the integers in the rationals}",
        r"\title{Conditional polynomial constructions, lower bounds, and\newline" + "\n" +
        "number-field obstructions for rational Diophantine integrality}")
    text = replace_once(text,
        r"\date{6 November 2026\quad---\quad working version for review}",
        r"\date{6 November 2026\quad---\quad revised working version 3}")
    start, end = text.index(r"\begin{abstract}"), text.index(r"\end{abstract}")
    abstract = r"""\begin{abstract}
We study explicit polynomial presentations of the ordinary integers in
the rationals, starting from a pinned revision of the repository
\emph{diophantine-z-q}. Under its named arithmetic inputs and Sun's
simultaneous prime-pattern theorem, we construct an indexed polynomial
in 41 total variables, including the input, with degree at most
$2^{9566673}$. A 43-variable alternative has degree at most $2^{236}$.
The direct substitution of the Lucas polynomial into approximate
logarithmic ratios removes two retained coordinates and one finite
algebraic coordinate. It also gives quartics with 1315 variables.
An affine change reduces their coefficient height to $64\cdot3^{2^{28}}$;
an alternative with 1335 variables has coefficient height less than $2^{1020}$.
Their complete sparse coefficient tables are independently checked.
The previously implemented 558-variable construction and its
source-preserving alternatives remain available for comparison.

No construction in two through ten total variables is established.
Unconditional lower bounds exclude two total variables at every
degree. We prove that two quadratic equations, in any number of
coordinates, cannot have an infinite input image contained in a
number field's ring of integers. A quadratic system defining that
ring consequently needs at least five total coordinates and at
least three independent quadratic equations. Further results explain
precise limits of finite algebraic encoding and fixed denominator
tests without mistaking them for universal variable lower bounds.

Over every specified number field, a finite system can be combined
into one equation without adding variables. An explicit division-norm
construction gives degree at most $D\lceil\sqrt{s}\rceil$ for $s$
equations of degree at most $D$; the preferred quadratic systems yield
degree 72. These are faithful encodings, not general integrality
theorems. Exact counterexamples show that the literal newer quartics
accept all inputs over $\mathbb Q(i)$, the unshifted indexed equations
reject certain algebraic integers, and the fixed cyclic elliptic
argument fails in an explicit totally real quartic extension.
A translated square repairs the finite input contacts but not that
arithmetic obstruction. All hypotheses, proofs, computational scopes,
and unresolved dependencies are stated separately.
"""
    text = text[:start] + abstract + text[end:]
    table_start = text.index(r"\begin{center}" + "\n" + r"\small" + "\n" + r"\begin{tabular}{r l l p{43mm}}")
    table_end = text.index(r"\section{From integer equations to rational equations}", table_start)
    overview = r"""\begin{center}
\small
\begin{tabular}{r l l p{43mm}}
\toprule
Total variables & Degree & Coefficients & Output supplied\\
\midrule
41 & $\le2^{9566673}$ & $\le2^{2^{86098382}}$ & Indexed polynomial with fixed elliptic exclusion product\\
43 & $\le2^{236}$ & $\le2^{2^{240}}$ & Indexed semilocal alternative with coefficient DAG\\
558 & $\le2^{3122}$ & $\le2^{2^{3127}}$ & Implemented source-preserving indexed polynomial\\
1315 & $4$ & $64\kappa<2^{429496736}$ & Complete table over $\mathbb Z[s]$, with $s^2=\kappa$\\
1335 & $4$ & $<2^{1020}$ & Complete integer coefficient table\\
12,504 & $4$ & $<2^{80}$ & Unchanged released package\\
\bottomrule
\end{tabular}
\end{center}

All counts include the input. The first two and the two smaller quartic
rows use the shared-point arithmetic argument and the direct Lucas
test. The 558-variable row is a source-preserving algebraic
construction. Large displayed degree and height inequalities are proved
upper bounds, not exact expansion statistics. Here
$\kappa=3^{2^{28}}$ and $s=3^{2^{27}}$ are fixed integers;
neither counts as a coordinate. The indexed polynomials specify every
matrix and finite product but do not expand their enormous tables.
Both 41- and 43-variable specifications also have separately checked
versions with $\beta=X^2+2402$, with the same displayed bounds.

The preceding 43- and 45-variable indexed formulas, the untransformed
1315-variable table, the 1338-, 1339-, 1367- and 1391-variable quartics,
source-preserving 853-variable circuit, and
12,449--12,493-variable quartics are retained as reviewable comparison
constructions. Their proofs supply several ingredients used below.
None of these counts is claimed to be globally minimal. Under the
stated arithmetic inputs, the unrestricted gap is between three and
41 total variables. For a sum of squares of quadratic residuals, the
proved gap is between five and 1315. Degree four is the least possible
degree for one defining equation if the conditional construction is
valid. A definition using at most ten total variables remains unproved.

Allowing several equations helps with degree and presentation but
does not change the minimum number of variables when degree is
unrestricted. Over $\mathbb Q$, their sum of squares combines any
finite system without a new variable. Over any specified number field,
the division-norm construction gives the same conclusion with a
controlled degree. The general and field-specific assertions are
proved separately in this report.

"""
    text = text[:table_start] + overview + text[table_end:]
    systems = read("systems/systems_combination.tex")
    systems = systems.replace("were proved in\nSection", "are proved in\nSection")
    systems = systems.replace("proved earlier.", "proved below.")
    text = insert_before(text, r"\section{The arithmetic structure retained from the source}", systems)
    compiled = read("compiled_constructions.tex")
    split = compiled.index(r"\section{Quartics obtained from the direct Lucas test}")
    text = insert_before(text, r"\section{A new quartic with 1367 variables}",
        read("compression/direct_polynomial.tex") + "\n\n" + read("beta_shift.tex") + "\n\n" + compiled[:split])
    text = insert_before(text, r"\section{Exact quartics and their computational verification}",
        compiled[split:] + "\n\n" + read("quartic/affine_anchor_refinement.tex"))
    mrdp_marker = r"\subsection{A quantitative consequence for rational Diophantine problems}"
    text = insert_before(text, mrdp_marker,
        "\n\n".join(read(p) for p in [
            "systems/low_degree_systems.tex", "systems/projection_limits.tex",
            "compression/geometric_compression.tex", "compression/denominator_obstructions.tex",
            "compression/packing_literature.tex"]))
    text = replace_once(text, mrdp_marker,
        r"\section{Quantitative consequences for rational Diophantine problems}")
    text = replace_once(text,
        "With $N=42$, the conditional 43-variable construction therefore gives\n"
        "$463$ existential witnesses for each computably enumerable subset of\n"
        "$\\Q$, and undecidability of rational polynomial solvability in at most\n"
        "$380$ variables.",
        "With $N=40$, the conditional 41-variable construction therefore gives\n"
        "$441$ existential witnesses for each computably enumerable subset of\n"
        "$\\Q$, and undecidability of rational polynomial solvability in at most\n"
        "$362$ variables.")
    strategy_start = text.index(r"\section{What remains open and which reductions are promising}")
    strategy_end = text.index(r"\section{A conditional geometric obstruction}", strategy_start)
    field_supplements = "\n\n".join(read(p) for p in [
        "number_fields/base_change_20261106_v1.tex",
        "number_fields/division_norm_compiler_20261106_v1.tex",
        "number_fields/final_quartic_fields_20261106_v2.tex"])
    text = text[:strategy_start] + field_supplements + "\n\n" + read("strategy.tex") + "\n\n" + text[strategy_end:]
    text = replace_once(text, r"\section{A new quartic with 1367 variables}",
        r"\section{The quadratic compilation with Lucas proxy coordinates}")
    text = replace_once(text, r"\section{The compiled shared-point polynomials}",
        r"\section{The compiled shared-point polynomials with Lucas proxies}")
    text = replace_once(text, r"\section{Reproducing the new polynomial constructions}",
        r"\section{Reproducing the constructions with Lucas proxies}")
    text = insert_before(text, r"\begin{thebibliography}{99}",
        read("reproducibility.tex") + "\n\n" + read("compression/source_review.tex"))
    additions = "\n\n".join(read(p) for p in [
        "systems/bibliography.tex", "bibliography_compression.tex",
        "number_fields/bibliography_20261106_v1.tex"])
    text = replace_once(text, r"\end{thebibliography}", additions + "\n\n" + r"\end{thebibliography}")
    # One bibliographic entry per primary source; retain the prior DDF key.
    text = text.replace("P3DDF2025", "DDF2025")
    text = replace_once(text,
        r"to 29,419 nonzero terms over $\mathbb Z[\kappa]$.  The independent checker",
        r"to 29,419 nonzero encoded entries over $\mathbb Z[\kappa]$, giving" + "\n" +
        r"29,415 distinct coordinate monomials after collecting the fixed" + "\n" +
        r"constant's powers. The independent checker")
    # Keep paths and labels stable, but do not organize the mathematical prose
    # by the chronology of internal working directories.
    text = text.replace("preferred phase-three systems", "untransformed direct-Lucas systems")
    text = text.replace("The preferred degree-36 form and the two new quadratic systems",
                        "The degree-36 form and the untransformed direct systems")
    text = text.replace("The last two refinements are exact transformations",
                        "The following refinements are exact transformations")
    text = text.replace("phase-three finite anchor", "direct finite anchor")
    text = text.replace("phase-three semilocal", "direct semilocal")
    text = text.replace("phase-two finite anchor", "proxy finite anchor")
    text = text.replace("phase-two semilocal", "proxy semilocal")
    text = text.replace("from phases three and two", "from the direct and proxy constructions")
    text = text.replace("frozen phase-two producer and the phase-three\nproducer", "frozen producer with proxies and the direct-Lucas\nproducer")
    text = text.replace("proved earlier.", "proved in this report.")
    # Long filenames are breakable; no external TeX input is required.
    text = re.sub(r"\\texttt\{([^{}\n]{35,})\}", lambda m: r"\nolinkurl{" + m.group(1).replace(r"\_", "_") + "}", text)
    temporary = OUTPUT.with_suffix(".tex.building")
    temporary.write_text(text)
    with temporary.open("rb") as stream:
        os.fsync(stream.fileno())
    os.replace(temporary, OUTPUT)
    return text


def main():
    original_hash = hashlib.sha256(OLD.read_bytes()).hexdigest()
    text = assemble()
    spec = importlib.util.spec_from_file_location("prior_static_checker", OLD.parent / "assemble_paper.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.check(text)
    assert hashlib.sha256(OLD.read_bytes()).hexdigest() == original_hash
    bib = re.findall(r"\\bibitem\{([^}]+)\}", text)
    assert len(bib) == len(set(bib)), "duplicate bibliography entries"
    receipt = {
        "status": "PASS", "scope": "Static TeX consistency, standalone inclusion, and preservation of preceding paper; not TeX rendering",
        "paper": OUTPUT.name, "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "bytes": len(text.encode()), "lines": text.count("\n"),
        "labels": len(re.findall(r"\\label\{([^}]+)\}", text)),
        "bibliography_items": len(bib), "preceding_paper_sha256": original_hash,
        "rendered": False
    }
    (HERE / "paper-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
