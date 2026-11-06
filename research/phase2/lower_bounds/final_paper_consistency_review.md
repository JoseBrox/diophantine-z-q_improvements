# Final assembled-paper consistency review

Reviewed `research/optimization/diophantine_optimization.tex` after the
43/45-variable specifications and the 1367/1391-variable quartics were
assembled. This review checks theorem scope, numerical agreement, and
preservation of the lower-bound proofs. It adds no new arithmetic result.

## Mathematical and numerical conclusions

No further mathematical inconsistency was found in the reviewed statements.
The final counts agree exactly with the construction reports and separate
passing verification receipts:

| Presentation | Total coordinates | Witnesses | Degree bound | Coefficient-height bound |
|---|---:|---:|---:|---:|
| Preferred indexed exclusion | 43 | 42 | 2^9566680 | 2^(2^86098389) |
| Preferred semilocal source | 45 | 44 | 2^243 | 2^(2^246) |
| Fixed-symbol quartic | 1367 | 1366 | 4 | Complete table over the specified fixed integer kappa |
| Ordinary integer quartic | 1391 | 1390 | 4 | Strictly less than 2^1020 |

The 43/45-variable algebra ranks 2^29/2^30, formal-generator counts
20/21, quadratic-stratum counts 11/12, and coefficient-DAG sizes
6224/6245 agree with the emitted specifications. The retained-coordinate
inventories have 42/44 coordinates before the final finite-choice witness.
The first-conic parameters replace retained coordinates and finite roots
as stated; none is omitted from the count.

The quartic has nine point occurrences and ten pole blocks. Its scalar
pole intentionally retains its preparation parameter. Its comparison and
scalar orders are 52 and 32, with fixed kappa=3^(2^28). The reported
1322/1346 residual counts, 29419/29489 coefficient-table term counts,
sixty eliminations, and 1020-bit coefficient bound agree with the exact
receipts. The smaller-variable scalar normalization and conic
parametrization are correctly distinguished from the quartic source.

The shared-point upper bounds explicitly assume the named arithmetic
inputs and the additional simultaneous prime-pattern theorem. The
source-preserving 558-variable construction and earlier quartics/circuits
are correctly separated from that arithmetic modification. No global
optimality statement is made. The unrestricted gap is three to 43 total
coordinates under the stated upper-bound hypotheses; the sum-of-squares
quartic gap is five to 1367.

## Lower-bound integration

Compared the integrated text against all three finalized sources:

- `research/optimization/paper_parts/lower_bounds.tex`;
- `research/phase2/lower_bounds/results.tex`;
- `research/phase2/lower_bounds/conic_obstruction.tex`.

All proofs are complete in the assembly. The original unrestricted
lower-bound text is unchanged apart from surrounding comments. The new
geometric section differs only in three editorial substitutions of
cross-reference wording. The conic section is identical, including its
degenerate cases and integral-superset corollary. The verified references
supporting each section are present. A static scan found no duplicate
labels, unresolved references, or unresolved citation keys.

The two-witness unrestricted quartic case remains explicitly unresolved.
The degree-eight result retains the nonnegativity hypothesis; the
five-coordinate result retains its quadratic-system/sum-of-squares
hypothesis. The weak Bombieri–Lang surface obstruction is explicitly
conditional in its proposition.

## Concrete editorial corrections reported to the main author

1. In the abstract, qualify the nonnegative-polynomial degree-eight
   sentence by saying it defines the integers. Without that qualifier
   the isolated sentence would be false.
2. Replace the reference to expanded quartics "in the preceding
   lower-bound section" by "constructed above".
3. Replace the appendix's stale statement that no quartic saving from
   scalar order 32 is reported. The final shared-point quartics already
   use that order; the earlier original-source experiments should be
   identified as such.
4. Qualify the blanket phrase "The lower bounds above are unconditional"
   before the Mazur section, since the earlier general-type obstruction
   assumes weak Bombieri–Lang. The numerical bounds and conic theorem
   themselves are unconditional.
5. The quantitative MRDP theorem may now be instantiated with N=42,
   giving 463 witnesses for computably enumerable subsets of Q and
   undecidability of rational polynomial solvability with at most 380
   variables. The N=557 example remains a valid weaker comparison with
   fewer additional arithmetic dependencies.

The main author acknowledged these corrections and is rerunning the
assembly. No further mathematical or count discrepancy remained at the
end of this review. The forthcoming reproducibility/manifest updates are
the main author's separate responsibility.
