# A smaller quartic specification at 78 variables

The two components of the reciprocal-pair curve equation are consequences of
the other source equations. Their removal preserves every solution at every
fixed value of `B`. The count remains 78, while the number of quadratic squares
decreases from 70 to 68 and the quartic support decreases from 1,143 to 1,113.
Degree, primitive content, exact height and arithmetic hypotheses are unchanged.

The proof is in
`papers/elliptic_charts/paired_ratio_redundancy_20261115_v40.tex`.

Run from the repository root:

```sh
python -B computation/quartic/abc78_reduced_v40/build.py
python -B computation/quartic/abc78_reduced_v40/check.py
```

The producer uses the Python standard library. The independent checker uses
SymPy, imports no producer code, checks three universal polynomial identities,
preserves all retained rows literally, and independently expands every square.
The coefficient parameter remains a sufficiently large fixed odd integer. No
numerical defining threshold, lower global variable count, or independent audit
of the external arithmetic premises is asserted.
