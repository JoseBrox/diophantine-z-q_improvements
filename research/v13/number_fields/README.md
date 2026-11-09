# Locally dense rational subsets and integrality criteria

The main document is `elliptic_ratios_and_integrality_20261109_v13.tex` (compiled PDF alongside it).

## Proved results

- The integer polynomial
  `t*((u^2*w-9*w^3-1)^2-2*(v^2*t*w-9*t^3*w^3-1)^2)`
  defines a proper subset `D` of `Q` inside `Q(i)`. It has four total coordinates, degree 13, height 162 and 11 monomials. The set contains 0 and 1, excludes -1, and is dense simultaneously in every finite collection of completions of Q.
- Every input is locally represented in every completion of Q(i). Thus this example supplies a rigorous obstruction to inferring global completeness from local solubility or density. It is not a definition of Q, Z, or Z[i].
- The two required rank-zero calculations are unconditional and reproducible; their data agree with Cremona's tables. The elliptic points over Q(i) are proved to be exactly the rational points using the trivial rational group of the quadratic twist.
- The identical polynomial defines the identical set in each quadratic field Q(sqrt(d)) for d in {-15, -13, -11, -10, -1, 3, 5, 7}; all eight twist calculations are included in the certificate. This includes both real and imaginary quadratic fields.
- A general stable positive-rank elliptic curve supplies a similarly locally dense rational subset with six total coordinates, with no assertion of global surjectivity.
- A Diophantine set containing Z with uniformly bounded denominators in O_K suffices to define O_K. The integral-basis and finite-union constructions have explicit coordinate and degree counts.

## Reproduction

Install `cypari2>=2.2.4`, then run:

```sh
python3 check_elliptic_ratio_obstruction.py --output elliptic-ratio-certificate.json
```

The script invokes the unconditional `ellrank` and `ell2cover` routines, checks torsion and finite-field counts, verifies the explicit doubling formula, and expands the four-coordinate polynomial exactly. No analytic-rank or BSD assumption is used. The saved certificate reports PARI 2.17.2 and PASS.

## Files for integration

- `elliptic_ratios_and_integrality_20261109_v13.tex`
- `elliptic_ratios_and_integrality_20261109_v13.pdf`
- `check_elliptic_ratio_obstruction.py`
- `elliptic-ratio-certificate.json`
- `checkpoint.md`

The `python/` and `dependencies/` directories contain disposable local execution dependencies and are not deliverables to commit.
