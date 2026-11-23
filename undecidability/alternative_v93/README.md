# Lower-degree guarded finite-algebra encoding

The [proof](../papers/paired_spectral_encoder.tex) and
[PDF](../papers/paired_spectral_encoder.pdf) give a new complete coefficient
recipe for a rational character of a finite algebra with a nonzero guard.
All ordinary coordinates, source equations, integer predicates, and
arithmetic qualifications are retained.

The existing **82 / 100 / 52** undecidability transfers now have degree
ceilings **2^532 / 2^578 / 2^425**, respectively, instead of
2^650 / 2^714 / 2^500. The **83 / 101 / 53** tradeoffs have ceilings
**2^302 / 2^349 / 2^212**. Every ceiling is strict. The last route in each
triple retains ordinary rational abc. These are changes of degree;
the rational variable counts do not change.

## Exact construction

Use the complete finite algebra and guard of each pinned source in the
certificate. Given its multiplication matrices for
`g, g*theta_1, ..., g*theta_m`, `paired_spectral.py` specifies the new
single-coordinate polynomial. For a rank `n` algebra put
`ell=m+1` and `J=ell*n*(n+1)/2`. Remove the universally present diagonal
zero factors in each tensor-difference characteristic polynomial and
replace its even powers by one variable. The resulting monic polynomial
has degree `J` and contains every squared spectral difference.

The spectral-size envelope uses only the original matrix entries. Separate
coefficient factors bound nonzero differences and give a separator on each
coefficient stratum. The final polynomial is the finite product of the
sum-of-squares factors in the manuscript. The uniform total-degree bound is

```
2*n*(J+1)*(1+d*(1+(4+6*ell)*J))
```

where `d` bounds the multiplication-matrix entry degrees. Nilpotents, zero
terminal roots, and guards vanishing on excluded characters are allowed.
The large matrices and resulting polynomials are specified, not expanded.

## Reproduction

From the repository root, run:

```sh
python -B undecidability/alternative_v93/check_paired_spectral.py
```

The checker verifies small exact spectra and every coefficient stratum,
replays degree bounds from the full stored source DAGs, independently
replays the finite-wrapper rescaling and the degree formula, and computes
the nine numerical application bounds. Its report is
[`certificate.json`](certificate.json).

The current 25-, 27-, and three 11-variable defining polynomials keep their
smaller specialized v88 degree bounds. This generic encoder does not
improve those five bounds. The checked universal source pair remains
`(58,4)`; no unverified alternative source pair is used. For the
53-variable transfer the universal source, not the new encoder, determines
the final degree ceiling.
