# Fixed fibers of the native square test

The [theorem](../../papers/pole_parameters/fixed_flat_fibers_20261116_v53.tex) concerns the actual point tuples $A=[X]P$, $H=3P$, $U=[3X]P$ for $X=1,2$, with the fixture $B=3$ and exponent $4$. It treats both original and symmetric final comparisons in the faster quadratic detector. This value of $B$ is not asserted to be a sufficient defining parameter.

The single square covers have genera **59** and **83**. At the actual coupled source scales, their geometrically integral simultaneous covers have genera **236** and **332**. Each has four rational points above infinity. Those boundary points are outside the guarded source domain.

The certificate supplies exact rational source data, modular polynomial coefficient vectors, and explicit Bézout identities proving squarefreeness and the branch-set intersection. The independent checker uses only the Python standard library:

```bash
python -B negative_results/computation/fixed_flat_fibers_v53/check.py
```

To reconstruct the certificate with SymPy 1.14.0:

```bash
python -B negative_results/computation/fixed_flat_fibers_v53/generate.py
```

Both default commands leave the distributed files unchanged. Generation accepts `--output PATH`; checking accepts `--certificate PATH`. The result proves neither absence of finite rational points nor an obstruction to varying the auxiliary indices. It gives no lower bound for the number of defining variables.
