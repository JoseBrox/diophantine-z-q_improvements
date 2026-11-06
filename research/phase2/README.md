# New constructions and stronger lower bounds

The complete paper is in **../optimization/diophantine_optimization.tex**.
This directory supplies new arithmetic constructions, their exact polynomial
implementations, independent algebraic checks, and the stronger lower-bound
proofs. It is prepared for human review; no commit, push, or pull request
has been made.

## Main results

All counts include the input variable. Subtract one for existential witnesses.
All displayed degree and height bounds for the indexed polynomials are upper
bounds, not expansion statistics.

| Package | Total variables | Degree | Coefficient height |
| --- | ---: | ---: | --- |
| finite_fibre/polynomial-43-conic | **43** | at most 2^9566680 | at most 2^(2^86098389) |
| finite_fibre/polynomial-45-conic-semilocal | **45** | at most 2^243 | at most 2^(2^246) |
| finite_fibre/polynomial-558 | **558** | at most 2^3122 | at most 2^(2^3127) |
| quartic/quartic-best | **1367** | **4** | complete table over the fixed integer K=3^(2^28) |
| quartic/quartic-small-coefficients | **1391** | **4** | **less than 2^1020** |

The first three are exact indexed determinant and finite-product formulas.
Their finite index ranges, algebra relations, guards, closed equations, and
polynomial recipes are supplied. Their enormous matrices and outer products
are not expanded. Formal generators of a finite algebra are eliminated by
the formula and are not quantified coordinates.

The two quartics have complete sparse coefficient tables: respectively
29,419 and 29,489 terms. The former uses one specified fixed integer
coefficient; the latter has ordinary expanded integer coefficients.
Their 1322 and 1346 primitive quadratic residuals are also supplied.

## Arithmetic hypotheses and verification

The 558-variable construction preserves the pinned original source projection.
Identifying that projection with the integers requires its arithmetic theorem.
The 43/45-variable constructions and the new quartics use a different,
shared-point source. They additionally use Theorem 4.1 of Zhi-Wei Sun,
*86 unknowns for Hilbert's tenth problem over the rationals*,
arXiv:2610.20691v2. They do not infer a definition of the integers from an
undecidability theorem.

The paper proves the new constructions from the explicitly listed arithmetic
inputs. The source's restricted pole converse and full explicit five-contact
height theorem, and the cited prime-pattern theorem, have not all received
complete independent reproofs here. The algebraic receipts do not certify
these external arithmetic inputs. No unconditional breakthrough or global
minimality claim is made.

Run all eleven preferred checks from the repository root:

    python3 -E -B research/phase2/verify_phase2.py

The aggregate receipt is **verification/all-checks.json**. Each checker states
its own scope. The complete small-algebra interpreter includes 177 factors
over eight examples, and emits a degree-16 expanded example. The large
instances rely on the proved general finite-algebra theorem, not on numerical
sampling.

## Lower bounds

The lower-bound proofs in **lower_bounds/** are independent of the arithmetic
construction:

- Over any number field, a polynomial defining its ring of integers needs
  degree at least four and at least two existential witnesses.
- A quartic given as a sum of squares of quadratic residuals needs at least
  five total variables.
- A globally nonnegative three-variable polynomial defining the integers
  in the rationals needs degree at least eight.
- Two witnesses occurring jointly quadratically cannot define the ring of
  integers, regardless of the input degree. A finite disjunction cannot
  circumvent this obstruction. The proof uses quaternion residues,
  Chebotarev and integral Hilbert irreducibility.

The weak Bombieri–Lang obstruction is separately labeled conditional.
No argument here rules out an unrestricted three-variable quartic, or
establishes a numerical lower bound near the new upper bounds.

## File guide and continuation

**new_polynomials/** contains the arithmetic construction, exact source DAGs,
the scalar normalization, the rational conic parametrizations, and the
precision proofs. **finite_fibre/** contains the general one-witness compiler,
source conversions, bounds, indexed specifications and checks.
**quartic/** contains the exact quadratic compiler, its independent table
checker and the two preferred tables. **lower_bounds/** contains the
unconditional restrictions and their source notes.

The preferred next mathematical work is independent review of the remaining
arithmetic dependencies, then reductions in the nine shared elliptic-point
coordinates and ten pole blocks. For the 43-variable construction, a smaller
size certificate would substantially lower degree. For quartics, further
quadratic-preserving eliminations and shared polynomial evaluation offer
concrete targets. The full paper discusses these possibilities and the
remaining general number-field question.
