# Proposed title

Add conditional shared-point constructions, exact polynomial compilers, and lower bounds

## Why this change

The released quartic uses 12,504 total variables. The new work separates
coordinates that carry arithmetic information from finite algebraic choices
and arithmetic evaluation coordinates. It gives substantially smaller
polynomial presentations, while keeping a precise distinction between finite
algebraic verification and the external arithmetic inputs.

## What this adds

The proposed additions are **research/optimization/** and **research/phase2/**.
The released polynomial and arithmetic manuscript are unchanged.

- A standalone LaTeX paper with definitions, full proofs of the new statements,
  primary references, explicit hypotheses and a partial source audit.
- Exact indexed polynomials in 43 and 45 total variables, using a new
  shared-point construction under the source lemmas and Sun's Theorem 4.1.
  Their degree bounds are respectively 2^9566680 and 2^243. All finite cases,
  coefficient operations, determinant dimensions and bounds are specified.
- An implemented 558-variable polynomial preserving the original source
  projection, with degree at most 2^3122 and height at most 2^(2^3127).
- A 1367-variable quartic with a complete 29,419-term table over one fixed
  integer coefficient, and a 1391-variable ordinary integer quartic with
  29,489 terms and coefficient height below 2^1020.
- Unconditional lower bounds and a simultaneous conic-specialization theorem
  excluding two jointly quadratic witnesses at every input degree.
- The earlier source-preserving quartics and circuits as reviewable comparisons,
  plus integer-to-rational reductions, quantitative MRDP consequences and
  number-field transfer results.

All counts include the distinguished input. The large indexed matrices and
outer products are not expanded; their exact finite definitions are supplied.
Only the quartics have complete expanded coefficient tables.

## Validation

From the pinned repository root:

    python3 -E -B research/phase2/verify_phase2.py
    python3 -E -B research/optimization/verify_all.py
    python3 -E -B research/optimization/assemble_paper.py

Receipts and detailed logs are included. The new preferred verification suite
runs eleven checks, including exact coefficient conversion, denominator guard
coverage, all quadratic zero cases, monicity, source counts, degree and height
bounds, and both complete quartic coefficient tables. The general finite-algebra
construction is also fully executed on eight small exceptional examples.

The independent quartic checker replays every gate, nine row additions and
sixty eliminations, then independently computes the entire sum-of-squares table.
It does not import the producer. Separate proofs justify the domains of the
direct quotient equations. The older 855 circuit's six modular samples retain
their explicitly limited status.

The TeX assembly passes static consistency checks. A working LaTeX format was
not available, so successful typesetting still requires a normal installation.

## Scope and mathematical review

The identification of the source projections with Z is conditional on the
specified arithmetic inputs. The source restricted pole converse, full explicit
five-contact height theorem, and every ingredient of Sun's prime-pattern
theorem have not all received independent reproofs here. The exact algebraic
receipts do not certify those theorems.

Review should first address those arithmetic dependencies, then the shared-point
construction, scalar normalization, exceptional finite-algebra cases and quotient
domains. No global variable minimum or unconditional new solution of Hilbert's
tenth problem over Q is claimed.

The released equation's failure over Q(i) concerns that equation. The general
existence of field-dependent definitions of all rings of integers remains
unsettled here.

Prepared with ChatGPT and parallel mathematical/computational reviews. This is
a draft for human review, with no historical priority claim. No commit, push,
or pull request has been created.
