# Prepared elliptic divisibility audit

The manuscript proves a prepared subrelation of elliptic index divisibility,
conditional on ordinary rational `abc` and the published class-seven
intrinsic-pole theorem. Every accepted pair has integral index quotient;
every nonzero integer quotient occurs for some prepared reference point.
The fixed construction need not accept every divisible pair.

The surrounding constructions are based on notes of **Gabe Conant with Astra 6.2**;
this detector and its normalization are subsequent project work.

This package does **not** prove a smaller definition of the ordinary integers.
Identifying an external rational input with the elliptic index quotient
remains unresolved.

## Read-only exact audit

From this directory, run:

```sh
python -B check_eds_detector.py
```

Only the Python standard library is required. The command recomputes the
clearing, coefficient table, rational fixtures, and finite selector count;
when the stored receipt exists, it checks equality with that receipt.
It does not write files.

To write an explicitly requested new receipt:

```sh
python -B check_eds_detector.py --report new_receipt.json
```

The `288` true-multiple fixtures and six prepared inputs are exact rational
computations. They supplement the proof; they do not establish the infinite
odd-primitive or intrinsic-pole realization theorems.

## Optional PARI audit

Install the same wheel distribution used for the arithmetic receipt:

```sh
python -m pip install passagemath-pari==10.8.14
python -B check_eds_detector.py --pari
```

This additionally calls PARI/GP through `cypari2`. The recorded exact output is:

```json
{
  "version": "(2, 17, 4)",
  "rank_bounds": [1, 1],
  "torsion_order": 2,
  "rank_point_output": "[[-1, 1]]",
  "conductor": 256
}
```

The alternative rank point differs from `(2,2)` by the rational point of
order two. The assertion that `(2,2)` generates the free part is separately
bound to the LMFDB primary record cited in the manuscript. The optional
PARI computation does not claim to prove a saturation result from rank
bounds alone.

## Files

- `papers/elliptic_divisibility/prepared_eds_divisibility_20261120_v82.tex`: complete proof and precise scope in the repository.
- `check_eds_detector.py`: independent exact checker.
- `eds_detector_certificate.json`: standard-library receipt.
- `eds_detector_pari_certificate.json`: receipt including the optional PARI data.

The finite algebra has rank eight over four free rational coordinates.
A single encoder variable and a menu of 57 separating elements suffice.
The terminal radicand has degree 48 and 162 monomials.
