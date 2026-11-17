# Upstream source and construction audit

## Identified source

The public source inspected is [Version 19](https://github.com/elliotglazer/diophantine-z-q/tree/498efba6fe75e9d28d6804f1391d7f70e4150afa), pinned to commit `498efba6fe75e9d28d6804f1391d7f70e4150afa`, tag `quartic-195-version-19`, dated 17 November 2026. Its manuscript is `manuscripts/quartic_v19.tex`, SHA-256:

```text
1f0e4db9e978115bb7f605f4bfcd84426a715b8cb6adaee3566107b33d61ad03
```

The requested **Version 59** was not located in the exposed main branch, manuscript paths, branches, tags, releases, or code searches. Pull request 59 is a different closed, unmerged Lean contribution. This audit does not identify Version 19 with Version 59. An exact additional source link would be needed to audit a different manuscript.

## Contributions and retained sources

Version 19 integrates José Brox's 195-variable quartic family and Gemini Carbon's explicit 250-variable construction. The 195-variable charts retain Gabriel Conant's inverse Vieta and affine-label contributions. The effective three-detector method builds on the project's earlier sum-height and additive constructions. The center $3/11$ also occurs in the upstream contact families; its existence is not claimed as a new discovery here.

The upstream 250-variable presentation starts from a 244-variable, 216-row quadratic family. Six coordinates and equations form a constant ladder that reduces the size of displayed coefficients. Since this repository gives variable count priority over coefficient size, the 244-variable family is the relevant intermediate comparison. It remains a source construction, not an additional current record competing with the complete 229-variable result.

The final 229-variable construction uses the already certified 195-variable source table from this repository. It adds a full 34-coordinate detector, recovers both height components without another coordinate, and proves an effective inequality on the full torsion and half-index domain. Its separate finite-prime argument supplies the numerical threshold $N=15$. Its full source provenance is in [PROVENANCE.json](../computation/quartic/explicit229_v62/PROVENANCE.json).

## Audit coverage

The pinned upstream finite verification workflow was run successfully, including the 195- and 250-variable expansions, printed coefficient rows and interface checks. The audit read the new effective sum-height argument, reflected height estimates, third-detector construction, scalar preparation, local extraction, complete witness argument, and their consumers in the 198/195 point charts.

The strengthened argument proves its local statements at the newly consumed small primes instead of extrapolating a theorem stated only above the former cutoff. It checks the three scalar valuation classes, the first integrality step before absolute formal precision, half-integral labels, the fourth odd label, zero numerator tests, the favorable denominator prime 409, and the endpoint $v^2\mid102$ for the input denominator. The complete witness proof uses the actual center-$3/11$ contacts, includes 2, 3 and 17 in preparation even when absent from scalar odd support, fixes every modulus before prime selection, and chooses pole certificates for the final reference point.

The resulting [independent algebra certificate](../computation/quartic/explicit229_v62/certificate.json) and [arithmetic certificate](../computation/quartic/explicit229_v62/arithmetic_certificate.json) distinguish exact finite verification from the mathematical existence arguments. The [literal polynomial certificate](../computation/quartic/explicit229_v62/literal_certificate.json) checks every specialized integer coefficient.

## Scope of the foundations

This audit does not claim an independent verification of every geometric, modular, prime-pattern and simultaneous-twist theorem in the cumulative upstream manuscript. The final paper retains its exact global arithmetic inputs, including H4.1 with its specified full-family radical, the prepared pole theorem, the elliptic group computation, and the fixed-data prime theorem. No additional abc hypothesis is introduced into the 229-variable result. The project's general 21/9 realization target remains unproved.
