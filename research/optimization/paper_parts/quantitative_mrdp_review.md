# Independent mathematical review of the quantitative MRDP application

Reviewed in parallel by the literature/optimization agent and the primary
agent. These are mathematical checks, not an emitted polynomial audit.

## Accepted bounds

If the ordinary integers have a rational one-polynomial definition with N
existential witnesses, the construction in `paper_mrdp_quantitative.tex`
gives:

- at most `11N + 1` existential witnesses for any computably enumerable
  subset of Q (one more variable when the rational input is counted);
- undecidability for rational polynomial solvability in at most `9N + 2`
  variables, after specializing the natural-number input of a fixed
  nonrecursive set.

For N = 557 the numbers are 6128 and 5015. No polynomial at these counts is
emitted, and no literature-record or global-minimum claim is made.

## Checked points

1. Sun, *Further results on Hilbert's Tenth Problem*, Sci. China Math.
   64 (2021), 281–306, Theorem 1.1(i), uses nine integer witnesses with
   the last one nonnegative. The publisher and arXiv:1704.03504v7 are the
   primary sources. Plain-text PDF extraction can misrender the inequality.
2. For integer t, the equation `t = u²+v²+w²+w` with rational witnesses
   is equivalent to nonnegativity. Forward: the integer three-square
   theorem applied to 4t+1. Reverse: t >= -1/4 and t integral. The integer
   test must be kept.
3. Coding Q inputs by an injective polynomial on integer numerator/denominator
   pairs requires eleven integrality tests: y0, x*y0, y1,...,y9, together with
   y0 != 0. The polynomial 2t²−t is injective and nonnegative on Z; twice
   Cantor pairing is an injective integer polynomial on two nonnegative inputs.
4. Normalize g as a polynomial in y9. When all coefficients vanish, set
   y9=0, choose fresh private integrality witnesses, and set the positivity
   witnesses to zero. This preserves only the required input projection;
   the larger projection to already chosen private coordinates need not be
   preserved and is not claimed to be.
5. Normalize the final witness of every integrality predicate on its
   coefficient-zero stratum. Retain y0,...,y8, N−1 private coordinates from
   each of eleven predicates, and two positivity coordinates. This is
   `9 + 11(N−1) + 2 = 11N` existential retained coordinates.
6. Over every geometric retained tuple, y9 is finite, the remaining private
   integrality witnesses are finite, the third positivity witness satisfies
   a monic quadratic, and the denominator inverse is unique. The finite-fiber
   theorem adds exactly one witness to the bound.
7. For a supplied natural input, omit numerator/denominator coding. The
   analogous retained count is `8 + 9(N−1) + 2 = 9N+1`, followed by one
   witness. This is not a definition on arbitrary rational inputs unless
   the input domain is also enforced.

References: https://arxiv.org/pdf/1704.03504v7;
https://doi.org/10.1007/s11425-020-1813-5;
https://arxiv.org/pdf/2102.06941v5, Corollary 4.21 and Remark 8.23.
