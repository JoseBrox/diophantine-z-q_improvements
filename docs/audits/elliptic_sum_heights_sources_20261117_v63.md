# Source and proof audit — 17 November 2026

## Result recovered and strengthened

The checkpoint finite-place argument is valid and extends to **every integral short Weierstrass equation**, not only `y^2=x^3-Dx`. The complete proof and consequences are in `elliptic_sum_heights_over_number_fields_20261117_v63.tex`.

For a number field K, an infinite-order P, and finite Q_i=[n_i]P+T_i with K-rational torsion T_i, the paper proves

`h(sum_i x(Q_i)+c) >= max_i h(x(Q_i)) - a_r log M - b_r - R_K - C(E,K,P) log(M+2) - h_fin(c)`.

Here M=max(1,|n_i|), a_r=(r-1)2^(r-1), b_r=sum binomial(r-1,j-1) log j, and R_K is the explicit ramification sum from the recovered proof. This gives an effective logarithmic loss over every number field, with no log-log factor. All n_i=0 cases and all rational torsion translates are included. The statement holds for arbitrary c in K, and its c-dependent loss vanishes for integral c.

The finite-place proof is elementary. Its universal-series extension follows from X=z^2 x satisfying X^3-X^2+A z^4 X+B z^6=0, then the invariant differential 1-zX'/(2X). In particular the formal logarithm has only odd powers starting at degree 5, with integral numerators and denominator m for degree m. This yields exactly the original deep-place threshold and ramification constant.

## David–Hirata-Kohno checked directly

Primary bibliographic source:

- S. David and N. Hirata-Kohno, *Linear forms in elliptic logarithms*, Journal für die reine und angewandte Mathematik 628 (2009), 37–89. DOI: https://doi.org/10.1515/CRELLE.2009.018 . Publisher page https://www.degruyterbrill.com/document/doi/10.1515/CRELLE.2009.018/html . Published paper, not a conjectural input.
- Full original-paper text inspected at https://www.academia.edu/109964712/Linear_forms_in_elliptic_logarithms . This is a mirror of the published paper. Data 1.4 is on pp. 41–42; Theorem 1.6 on p. 43. Theorem 1.3 on p. 39 explicitly establishes the fixed-data Lang statement described earlier as Conjecture 1.2.

The source's `log B` is the coefficient height. In Theorem 1.6 it occurs **only linearly**, in a factor `log B + h(model) + log log^+ V + log(D E)`. The `log log^+` is applied to the height parameter V of the fixed logarithms' algebraic points, **not to B**. Choose auxiliary E=e and sufficiently large fixed V_i. All other factors are fixed. This is the 2009 improvement beyond older elliptic-logarithm estimates with weaker coefficient dependence.

The uniformization uses three fixed logarithms: u_P, omega_1 and omega_2, with algebraic images P,O,O on three copies of E. The source defines exponential maps projectively, so logarithms of O (periods) are allowed. It does not require linear independence of the three logarithms. Its s=t=1 hypothesis is automatic when the evaluated linear form is nonzero: a tangent space inside the kernel cannot contain a vector outside the kernel.

For a fixed torsion exponent t, reduction to a centered parallelogram gives

`t u_Q = t n u_P + (a-t m_1) omega_1 + (b-t m_2) omega_2`

with all integer coefficients O(t(|n|+3)). The form is nonzero exactly because the chosen finite Q has u_Q != 0. This remains valid at n=0 for nonzero torsion. The Weierstrass function's double pole then gives h_infinity(x(Q))=O(log(2+|n|)), effectively.

## Further consequences and limitations

1. Effective finiteness of S-integral abscissa sums on the fixed cyclic group modulo torsion. At a fixed finite place, the same formal logarithm identity bounds the local contribution by O(log M); no p-adic linear-forms theorem is needed.
2. Zywina, *Rank one elliptic curves and rank stability*, arXiv:2505.16960v1 (2025), Theorem 1.1, supplies infinitely many rank-one elliptic curves over every number field. The author-hosted primary manuscript https://davidzywina.github.io/papers/Rank1WithStability.pdf was inspected, especially first-page Theorems 1.1 and 1.2. The arXiv record currently labels it a preprint and lists only v1, so the manuscript bibliography keeps that status explicit.
3. Thus every number field has curves for which the sum-height estimate holds on the **whole finite K-point domain**, after choosing a generator modulo torsion. Constants are effective once curve and generator are supplied. No uniform effective choice of generators for all number fields is claimed.
4. Existing CM examples exclude extending the estimate to arbitrary points on arbitrary higher-rank curves, or replacing the sum by a field trace. They do not contradict the fixed cyclic-group theorem.
5. Nothing here proves or disproves that O_K is Diophantine in K. No counterexample to that definability assertion was found. Rank-one existence and the sum-height bound remove two potential obstacles, but local detector completeness and its Diophantine encoding remain separate.

## Exact finite verification

`python computation/effective_sums/cyclic_number_fields_v63/check.py` passes under SymPy 1.14.0. It independently recovers the universal series to degree 17, checks coefficient integrality for that finite truncation, checks agreement with the j=1728 logarithm, and verifies the positive-subset combinatorics for r=1,...,10. Output: `computation/effective_sums/cyclic_number_fields_v63/certificate.json`. These are finite identity checks; the infinite formal and transcendence assertions are supported by the proof, not by this script.

## Rendering status

The publication build and all-page visual review are recorded separately in `data/audits/tex_build_20261117_v63.json`.
