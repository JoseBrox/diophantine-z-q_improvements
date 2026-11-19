# Paired-contact ordinary-abc quartic: 56 variables

The v81 construction reduces the reviewed v80 quartic from 58 to **56 total variables**, including the input. Its 46 quadratic residuals give a sum of squares with degree exactly four, content one, 809 coordinate monomials, and 812 parameter-separated terms. For every positive integer `B`, the exact coefficient height is

\[
H(F_B)=B^2+377888002299.
\]

For every sufficiently large odd `B`, the polynomial defines the integers under ordinary rational abc and the stated elliptic, formal-comparison, trace-index, and simultaneous prime-pattern premises. The threshold is ineffective. The v80 native pole and its application of Burungale's Theorem B in the exact published square classes are unchanged.

## The nonlinear contact rechart

Set

\[
M=B+2(X^8+T_{\mathrm{sc}}^2),\qquad a=M^4+16,
\qquad T=a^2-z^2,\quad S=a^2+z^2,\quad P=T^2.
\]

The eight original shifts are `8,9,12,15,17,20,23,24`. Pairing them about 16 gives

\[
F(a,z)=\Phi(P,S),\qquad
\Phi(P,S)=\prod_{r\in\{1,4,7,8\}}(P-2r^2S+r^4).
\]

The radius pairs `(1,8)` and `(4,7)` both have sum of squares 65. Store their two quadratic pair-products `A1,A2`, the normalized value `Fbar=F/a`, and one combined derivative `H=2T(A1)_P+(A1)_S`. The other combined derivative differs by the linear form `720(-4T+8S-130)`. Thus

\[
a\overline F=A_1A_2,\qquad
H(A_1+A_2)+720(-4T+8S-130)A_1+8c\overline F=0.
\]

The chain rule gives `F_a=2a(2T Phi_P+Phi_S)`, so the last equation recovers exactly the original quotient `u=-16F/F_a`, with `c=1/u`.

Every residual is quadratic. The nine contact coordinates are
`a,z,T,S,P,A1,A2,Fbar,H`; the old contact block needed eleven. The denominator `a` is positive for every rational input, and no coordinate is removed by assuming a contact value is nonzero.

The proof establishes `n^2 Tr x([n]R0) in Z_2` for every nonzero integer `n`, and checks the zero-input fibre separately. The factor-two padding therefore makes `M` a two-adic unit for every integer witness, so `a=M^4+16` is a two-adic square. This preserves completeness for the actual pole input. The residue/valuation proof handles any negative odd contact valuation caused by an odd valuation of `a` at another prime.

The shared elliptic chart and Laurent packing derive from the supplied notes of **Gabe Conant with Astra 6.2**, audited in v78. The derivative transfer is from v79, the one-helper normalizer is from v80, and this nonlinear contact rechart is v81 work.

## Reproduce and review

From the repository root:

```sh
python computation/variable_reductions_v81/abc/build56.py
python computation/variable_reductions_v81/abc/check56.py
```

The producer writes `quartic56/quadrics.json`, `polynomial.json`, `maps.json`, and `certificate.json`. The independent checker reconstructs the retained physical chart without importing the producer, derives the contact identities independently, and independently expands the complete sum of squares. Its finite computations do not certify the retained arithmetic premises.

The full proof is `papers/quartic_existence/paired_contact56_20261119_v81.tex`. The proof-review and immutable source-pin artifacts are provided separately from the exact coefficient checker. `tex_review.json` records compilation and page-layout review.

This construction is independent of the earlier incomplete proposal that scaled the normalizer by `1-tau`; the remaining cubic in that proposal is not used. No reduction of the eleven-variable unbounded-degree construction or global minimality assertion is made.
