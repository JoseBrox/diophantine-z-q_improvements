# Genus of the derivative trace fibers

For the nine-contact derivative weight and its actual trace, fixing any guarded auxiliary elliptic point gives a geometrically integral double cover of the slope line with genus at least eight. All eighteen rational contacts are simple branch points. At the contact `z=epsilon*(a+c)`, the exact derivatives are `u'=18*epsilon` and `C'=36*epsilon`.

The proof requires `a>10` and four finite nonzero tests in each slot. The original four reciprocal tests supply those hypotheses; either or both comparison tests may vanish. The source excludes the eighteen known rational branch points because it guards `u!=0`.

Projecting the guarded multiplication locus to the abelian surface `Res(E)` shows that it contains no geometric rational curve. This excludes rational parametrization, and says neither that individual rational witnesses are absent nor that the actual-trace criterion fails.

Files:

- [Complete proof and precise scope](../../papers/pole_parameters/derivative_trace_genus_20261117_v65.tex).
- `check.py`: exact symbolic contact identities, reciprocal-factor identity, and trace first-order expansion.
- `certificate.json`: reproducible PASS certificate, including all eighteen derivatives and source hashes.

Run:

```sh
python -B check.py
```

The checker also accepts `--source PATH` and `--output PATH`. In the repository computation directory it finds the matching manuscript under `negative_results/papers/pole_parameters/`. The geometric conclusions use the proofs in the manuscript; they are not inferred from sampling.
