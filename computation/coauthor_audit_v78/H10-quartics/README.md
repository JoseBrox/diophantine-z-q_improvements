# Quartic and finite-algebra improvements

These constructions improve the table in José Brox's **Polynomial presentations of the integers over the rationals**, commit `d3a8c223716a0fc0dbf5af4eb7998d640c21048d`. Every count includes the input. The defining assertions use the arithmetic premises of the corresponding upstream construction. The finite checks establish polynomial identities, arithmetic ledger entries, degree, support and reported heights.

| Construction | Variables | Quadratic equations | Degree | Monomials |
|---|---:|---:|---:|---:|
| Two contacts at a sufficiently large fixed parameter | 165 | 139 | 4 | 2,608 |
| Fully explicit three contacts | 180 | 152 | 4 | 2,648 |
| Ordinary rational abc | 62 | 50 | 4 | 830 |
| Sparse ordinary-abc alternative | 68 | 56 | 4 | 693 |

## Quartics

`quartics/general/polynomial.json` is the balanced general polynomial. Set C=149^N at any sufficiently large fixed integer N. The exact height for N≥1 is max(126616122944180358034867798936,149^(2N+2)). Each term represents its signed coefficient times C to the indicated parameter power times the product of the indexed variables. Indices are one-based and repeats denote powers. Index 1 is the input. The defining threshold N remains ineffective.

`quartics/explicit/quartic180.txt` is the fully specified expanded polynomial in Brox's canonical notation, including its leading sign conventions and variable indices. Its SHA-256 is `e6fd2cab3564dd0eb84c388aa252db1b6057f1135fbedfdf248416cd6585fd73`. It has 54,695 ASCII bytes. Its maximum absolute coefficient is 2584403986888404839167627077886434458396171597584 (161 bits). The underlying three-contact quartic with the original scalar at N=15 is also fully specified by `quartics/explicit-physical/polynomial.json` evaluated at C=149^15. The displayed literal uses the smaller, fully numerical squarefree scalar described in `quartics/explicit/ANCHOR.md`.

`quartics/check_physical.py` reverses the stored Laurent scalings, checks the point equations, signed detector factors, fresh gate, true product and complete expansion against the pinned physical source. `quartics/check_scalar.py` checks the common two/three-contact scalar and both trace-shift formulas. `quartics/effective-transfer.md` and `quartics/three-contact-audit.md` give the effective argument for the hybrid. `quartics/local-transfer.md` records the shared-product lemmas and successive choices of factors. The final factors and gates for this package are specified in the PDF and `assignment.json` in each physical folder. `quartics/check_balancing.py` checks the final general parameter scaling. `quartics/explicit/verify.py` checks the numeric anchor, transformations, full expansion and canonical text.

`abc62/` contains the ordinary-abc quartic with fixed odd shift B, and its fourth-power subfamily. For every odd n≥3, with B=n^4, the latter has exact height B+4091 and 830 monomials. A second presentation in the same 62 variables has 757 monomials and exact height B+758541. Its defining threshold remains ineffective. `abc68/` contains the 693-monomial alternative. Its height is 2B for odd n≥31 in the same cofinal subfamily.

## Few-variable determinants

| Route | Variables | Degree upper bound |
|---|---:|---:|
| General | 25 | 238,739,783,680 |
| Explicit at L=20483 | 27 | 1,941,079,851,008 |
| Weak abc at 121/100 | 13 | 2,525,697 |
| Weak abc at 16/15 | 13 | 2,206,209 |
| Ordinary abc | 11 | 36,482,433 |
| Ordinary abc, seven-contact variant | 11 | 56,391,041 |

Read `fewvars/POSITIVE.md` for the detector and guards, `fewvars/PROOF.md` for sign separation and determinant descent, `fewvars/PROJECTIVE.md` for the stronger two-pole 25- and 13-variable specifications, and `fewvars/BALANCED.md` for the stronger 11-variable specifications. The JSON circuits and receipts fully specify the determinants without expansion. The 27-variable coefficient height bound is below 2^(2^54).

## Reproduction

With Python 3.11 or later and SymPy installed, run the following from the directory containing this README. All verification inputs are included.

```sh
python -B verify.py
```

The checkers for the two general quartics and their coefficient transformations use standard Python. The independent symbolic verification of the 62-variable chart and the few-variable checks use SymPy. `source/` contains selected upstream files at the pinned commit. Upstream licensing and attribution are in `UPSTREAM.txt` and `source/LICENSE`. The LaTeX source of the research note is in `note/`. To compile it on an ordinary TeX installation run `pdflatex research.tex` there twice.

Source repository: https://github.com/JoseBrox/diophantine-z-q_improvements/tree/d3a8c223716a0fc0dbf5af4eb7998d640c21048d
