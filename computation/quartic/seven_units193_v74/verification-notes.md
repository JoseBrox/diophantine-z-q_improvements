# Verification of the reconstructed 193-coordinate family

## Proven transfer

The exact physical source is the published v73 system. `check_transfer.py`, written separately from the new producer, verifies equality of all 162 physical rational component rows for each reference basis, unchanged detector assignments, retained input and a bijection of the unit chart with the two-dimensional torus. Removing the stored inverse of `u` therefore changes neither soundness nor completeness. The sufficient defining parameter and all imported arithmetic premises are exactly those of v73.

The coefficient producer is a modification of the published Laurent compiler. Its independent verifier does not import it: it reconstructs the 81 new physical component equations from their formulas, reads the 81 retained equations from the pinned source, checks the primitive row normalizations and exact Laurent pullbacks, and independently re-expands the sum of squares using triangular sparse multiplication. A separate standard-library support verifier checks all 804 terms and the five unit equations.

The parameter-rescaling verifier does not import either producer or a computer algebra system. It checks every row under the inverse diagonal map, validates all primitive coefficient gcds, expands all 167 squares independently, and proves the exact support and height claims. Its short height proof applies to every real `C >= 149`; an additional finite-and-tail certificate independently proves the stated `149^N` crossovers.

## Exact results

- 193 total coordinates, including the input.
- 167 quadratic squares; degree exactly four and integer content one.
- 2,770 monomials in the primitive reference basis, or 2,626 in the alternative basis.
- Compact heights `max(K,149^(2N+2))` and `max(L,149^(2N+2))`, with the constants stated in the README.
- The coefficient crossovers are 6 and 13. They are not defining thresholds.
- Every coordinate occurs. The input fourth-power coefficient is one.
- Every quadratic row is primitive at every `C=149^N`, `N>=1`.
- All unit boundaries are excluded by the five explicit equations before inversion.

## Recovered versus newly reconstructed

The interruption's working files and exact 193-coordinate certificate were unavailable. This package is a complete reconstruction from published v73, with newly regenerated coefficients and verification receipts. It establishes the requested 193-coordinate result and the improved parameter dependence independently of a claim that these files match the lost checkpoint.

## Limits

The finite checks prove algebraic identities, all coefficient tables, rational coordinate equivalence, degree, support and heights. The full manuscript includes the inherited arithmetic proof with its precise premises. These checks do not complete a separate audit of the imported elliptic, height, prime-pattern or pole-realization foundations, give a numerical sufficient defining `N`, or prove the separate 21/9 global rational-realization criteria.
