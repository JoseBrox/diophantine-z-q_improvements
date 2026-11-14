# Correction of the unpublished 200-variable table

The v32 package treated the stored second ratio as the physical ratio. The
stored value is R times that ratio. Substitution `(L2-2)/2` therefore did
not produce the integer physical label `2a+2` used in the proof.

The corrected substitution is `(L2-2R)/2` in the second-root equations only,
and identically for the alternate ratio. In parent coordinate numbering,
the real shifts are `x35 -> x35/2-x118` and `x37 -> x37/2-x118`; the imaginary
components are divided by two. R is nonzero on every rational solution.
The downstream cross-square and Lucas product equations already divide by
R^2 and R respectively and are kept unchanged. No extra variable is needed.

The v32 reconstruction checker repeated the producer's same semantic error.
This release includes a separate physical-normalization test deriving the
labels from the retained product equations and rejecting the old shift.
The original unpublished tables are superseded; no equivalence is claimed.

Corrected counts: 200 total coordinates, 186 quadratic equations, degree
exactly four, content one, 3221 monomials at every positive fixed parameter.
The mathematical proof remains conditional on the named inherited inputs.
