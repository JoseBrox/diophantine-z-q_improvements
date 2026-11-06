#!/usr/bin/env python3
"""Assemble one standalone TeX document; no external inputs or BibTeX needed."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
PARTS = HERE / 'paper_parts'
PHASE2 = HERE.parent / 'phase2'


def read(name):
    return (PARTS / name).read_text()


def section_between(text, start, end=None):
    at = text.index(start)
    return text[at:] if end is None else text[at:text.index(end, at)]


def assemble():
    front = (HERE/'paper_front.tex').read_text()
    front = front.replace(r'A model,\+an', 'A model, an')
    front = front.replace(r'\DeclareMathOperator{\Frac}{Frac}',
                          r'\DeclareMathOperator{\Frac}{Frac}'+'\n'+r'\DeclareMathOperator{\Sha}{Sha}')
    lit = read('literature_optimization.tex')
    anchor = section_between(lit, r'\section{Published methods', r'\subsection{Precision thresholds')
    anchor = anchor.replace('Published methods and exact improvements to the algebraic presentation',
                            'An economical semilocal condition')
    anchor = anchor.replace('The results below should therefore be applied to the repository only after\nmatching their hypotheses to its actual residual system.',
                            'The next section matches these statements to the actual residual system.')
    anchor = anchor.replace('This count\nconcerns the specified module; an implementation should report the exact\nfinal global count after removing any unused lifting definitions.',
                            'The exact global counts and independent incidence checks are given in the next section.')
    anchor = anchor.replace(r'\cite[Chapter 14]{Voight2021}', r'\cite[Proposition 14.6.7]{Voight2021}')
    combine = section_between(lit, r'\subsection{Combining square conditions', r'\subsection{How MRDP')
    combine = '\\section{Rational relation combining and finite algebraic choices}\n'+combine
    fiber = read('finite_fibre_one_variable.tex')
    fiber = fiber[fiber.index(r'\section{'):]
    begin = fiber.index(r'\begin{theorem}')
    fiber = ('\\section{One witness for a constructible finite-fiber projection}\n'
             '\\label{sec:one-finite-variable}\n'
             'A constructible set is a finite union of locally closed algebraic sets.\n'
             'A projection has finite geometric fibers if every fiber over every\n'
             'point with coordinates in an algebraic closure is a finite set.\n'
             'Finite rational fibers alone are not the hypothesis used here.\n\n'
             +fiber[begin:])
    fiber = fiber.replace('thm:one-finite-variable', 'thm:finite-fibre-one-variable')
    fiber = fiber.replace('$d+1$ total variables, with $d$ existential witnesses. In particular\n$d=557$ gives $558$ total variables; $d=565$ gives $566$ total variables.\nThese numerical applications require their respective finite-geometric-\nfiber certificates and inherit the arithmetic hypotheses of the source.',
                         '$d+1$ total variables, with $d$ existential witnesses. In particular\n$d=557$ gives $558$ total variables. This numerical application requires\nthe finite-geometric-fiber proof supplied below and inherits the arithmetic\nhypotheses of the source.')
    if 'The exact quotations' in fiber:
        fiber = fiber[:fiber.index('The exact quotations')]
    square = read('square_root_compression.tex')
    square = square[square.index(r'\section{'):square.index(r'\subsection{Variable count')]
    application = read('finite_fibre_application.tex')
    application = application[application.index(r'\section{'):]
    audit = read('source-audit.tex')
    audit = audit[audit.index(r'\section{'):]
    audit = audit.replace('(arXiv:2205.11334v2, pp. 2--6)', r'\cite[Theorem 1.1 and Section 2.1]{Yuan2024}')
    audit = audit.replace('(arXiv:1901.07166v2, p. 5)', r'\cite[Theorem 1.0.4]{Pan2022}')
    # Long identifiers are reference labels from the original manuscript,
    # not cross-references into this document.
    audit = re.sub(r'\\texttt\{([^}]{28,})\}', r'\\nolinkurl{\1}', audit)
    precision = section_between(lit, r'\subsection{Precision thresholds', r'\subsection{Combining square')
    precision = precision.replace(r'\subsection{Precision thresholds and a smaller scalar order}',
                                  r'\section{Permissible precision reductions}')
    precision = ('\\appendix\n'+precision+
                 '\nThe source-preserving released-count packages retain the original precisions.\n'
                 'The $(52,13)$ experiment on the original source did not improve its\n'
                 'coordinate count, because its power chains were less economical.\n'
                 'The new shared-point quartics of Section~\\ref{sec:new-quartic}\n'
                 'use precision $52$ and scalar order $32$, together with stronger\n'
                 'size conditions and a different evaluation scheme. Their certified\n'
                 'counts are $1367$ and $1391$, as proved there.\n')
    fields = (PARTS/'finite_fibre_fields.tex').read_text() if (PARTS/'finite_fibre_fields.tex').exists() else ''
    def phase(name):
        return (PHASE2/name).read_text()
    quotient = phase('quartic/field_quotient_domains.tex')
    quotient = (r'\subsection{The domains of the division equations}'+'\n'
                +r'\label{subsec:direct-field-quotients}'+'\n'
                +r'Put $k=\mathbb Q(\sqrt2)$, $d=3-\sqrt2$, and $D=d^2$.'+'\n'
                +section_between(quotient, r'\begin{lemma}', r'\subsection{Square scales'))
    new_quartic = phase('quartic/compilation.tex')
    at = new_quartic.index(r'\subsection{The exact arithmetic conventions}')
    new_quartic = (new_quartic[:at]+phase('new_polynomials/precision52.tex')+'\n'
                   +phase('quartic/scalar32.tex')+'\n'+quotient+'\n'+new_quartic[at:])
    stronger_lower = phase('lower_bounds/results.tex')
    stronger_lower = stronger_lower.replace('first report', 'preceding lower-bound section')
    stronger_lower = stronger_lower.replace('all the expanded quartic variants in the preceding lower-bound section',
                                            'all the expanded quartic variants constructed above')
    conics = phase('lower_bounds/conic_obstruction.tex')
    parts = [front, anchor, combine, square, fiber,
             (HERE/'paper_intersection.tex').read_text(), fields,
             phase('finite_fibre/finite_algebra_polynomial.tex'),
             phase('finite_fibre/coefficient_bounds.tex'), application,
             phase('finite_fibre/source_558.tex'), phase('finite_anchor.tex'),
             phase('finite_fibre/fixed_anchor_height.tex'),
             phase('new_polynomials/shared_source.tex'),
             phase('new_polynomials/scalar_preparation_zero.tex'),
             phase('new_polynomials/degree_refinements.tex'),
             phase('finite_fibre/source_shared.tex'), new_quartic,
             (HERE/'paper_quartics.tex').read_text(),
             (HERE/'paper_circuit.tex').read_text(),
             (HERE/'paper_circuit_853.tex').read_text(),
             read('lower_bounds.tex'), stronger_lower, conics,
             (HERE/'paper_mrdp_quantitative.tex').read_text(),
             read('number_fields.tex'), (HERE/'paper_strategy.tex').read_text(),
             precision, audit]
    appendix = HERE/'paper_reproducibility.tex'
    if appendix.exists():
        parts.append(appendix.read_text())
    if (PHASE2/'reproducibility.tex').exists():
        parts.append(phase('reproducibility.tex'))
    parts.append((HERE/'paper_bibliography.tex').read_text())
    text = '\n\n'.join(parts)
    (HERE/'diophantine_optimization.tex').write_text(text)
    return text


def check(text):
    # Static consistency checks, not a replacement for TeX rendering.
    clean = re.sub(r'(?<!\\)%[^\n]*', '', text)
    stack = []
    for token in re.finditer(r'\\(begin|end)\{([^}]+)\}', clean):
        which, env = token.groups()
        if which == 'begin':
            stack.append(env)
        else:
            assert stack and stack.pop() == env, ('environment mismatch', token.group())
    assert not stack
    braces = []
    for match in re.finditer(r'(?<!\\)[{}]', clean):
        if match.group() == '{': braces.append(match.start())
        else:
            assert braces, ('unmatched closing brace', match.start())
            braces.pop()
    assert not braces
    labels = re.findall(r'\\label\{([^}]+)\}', clean)
    assert len(labels) == len(set(labels)), 'duplicate labels'
    refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', clean)
    assert not (set(refs)-set(labels)), ('undefined references', set(refs)-set(labels))
    bib = re.findall(r'\\bibitem\{([^}]+)\}', clean)
    cites = [k.strip() for c in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', clean) for k in c.split(',')]
    assert not (set(cites)-set(bib)), ('undefined citations', set(cites)-set(bib))
    assert clean.count(r'\begin{document}') == clean.count(r'\end{document}') == 1
    assert r'\input{' not in clean and r'\bibliography{' not in clean
    print({'bytes': len(text.encode()), 'lines': text.count('\n'),
           'labels': len(labels), 'references': len(refs), 'bibliography_items': len(bib),
           'status': 'static TeX consistency checks PASS; no rendering claim'})


if __name__ == '__main__':
    check(assemble())
