# Fixed-argument native square-complement ramification

Run from the repository root:

    python negative_results/computation/fixed_argument_complement_v44/check.py

The standard-library checker writes certificate.json in this directory.
Use --output /path/to/certificate.json to write elsewhere; missing parent
directories are created, and the certificate is independent of that path.

The exact audits bind the native test lists and orders, verify the
two-torsion translation and conditional weight normalization, check
the orders of the elliptic functions and the leading coefficients of
the three-factor boundary product, and enumerate the possible signed
pole weights. Source hashes are recorded in the certificate.

The accompanying paper is
negative_results/papers/rational_fibers/fixed_argument_complement_ramification_20261116_v44.tex.
Its geometric proof establishes ramification of each native complement
double cover on the full independent auxiliary-point variety, for
fixed allowed root and slope data with positive scalar coefficient.
It also excludes sections after dominant abelian pullbacks, including
the actual half-point doubling map.

The result does not exclude rational lifts at individual tuples,
sections on proper coupled subvarieties, or direct common-pole
constructions that do not use square complements. The finite checks
do not certify a global realization theorem or a variable reduction.
