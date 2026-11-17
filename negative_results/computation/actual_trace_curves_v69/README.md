# Curves and abelian families in actual-trace loci

The [complete proof](../../papers/pole_parameters/curves_and_abelian_families_20261117_v69.tex) treats the guarded derivative and general two-trace sources at fixed input. It proves finiteness on each fixed algebraic curve and the precisely stated restrictions on abelian families. It does not prove failure of rational realization, or a new defining-variable count.

From the repository root:

```sh
python -B negative_results/computation/actual_trace_curves_v69/check.py --manuscript negative_results/papers/pole_parameters/curves_and_abelian_families_20261117_v69.tex --output /tmp/actual-trace-curves-v69.json
```

The SymPy checker verifies the conjugate-twist identity, independent point-count formulas at 17, eighteen derivative contacts, the infinity expansion, ten general contacts and the exact fifth-order scalar contribution. The 200 Laurent boundary cases are finite regression checks; the general divisorial and geometric arguments are in the manuscript. The independent review and independent arithmetic certificate are included, with exact hashes and primary-source locations in `provenance.json`.
