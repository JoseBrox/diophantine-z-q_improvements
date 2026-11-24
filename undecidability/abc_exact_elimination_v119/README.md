# Five exact quadratic eliminations (368 variables)

**Theorem.** Under exactly the premises of [v118](../abc_primary_moments_v118/README.md), the twelve-input Jones transfer has the quartic `sum R_i^2` specified by **368 variables and 317 quadratic residuals** in `quadrics.json`. No defining parameter or arithmetic hypothesis is changed.

This is an exact bijective elimination, not a new arithmetic projection. In the field chart the two components of H0=K0 L0 and of sigsum=sum sig_i^2 occur only linearly elsewhere. Substitute their quadratic definitions and delete the four defining rows. For the contact circuit subtract 847974400 times row new.SS from row new.Fcoef6. The resulting affine equation is

```
n_Fcoef6 = 2529128704 n_contactP + 1018171392 n_SS.
```

Substitute it in every remaining row and delete the fifth definition. All terms have degree at most two. Conversely all five eliminated coordinates are uniquely reconstructed by these displayed definitions (the exact component formulas are in the certificate in the table). The row operation is invertible before elimination. No denominator or extra restriction occurs, including on exceptional chart fibers. The 52 Jones rows retain their named-monomial coefficients. Full support remains, and a nonzero quadratic residual ensures that the sum of squares has degree exactly four.

Run `node build.mjs` from this directory to compare the regenerated table exactly, or `node build.mjs --write` to regenerate it. The builder computes with BigInt coefficients and checks the affected rows and support. This algebraic step inherits the v118 arithmetic proof; it does not independently audit its arithmetic premises.
