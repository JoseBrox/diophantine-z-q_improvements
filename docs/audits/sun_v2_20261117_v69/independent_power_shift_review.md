# Independent audit of the power-shift theorem

**PASS**, reviewed 17 November 2026 against `power_shifts_and_finite_exceptions_20261117_v69.tex`.

- The split-prime construction supplies a degree-one residue field with `m | (ell-1)`. Choosing a non-mth-power unit residue and reducing an alleged `x^m=alpha-B` gives the required contradiction. The primes can be distinct, avoid every fixed denominator and progression modulus, and be combined by CRT. This proves uniform avoidance for every shift in the resulting subprogression.
- The square substitution covers every rational integer and forces integrality by normalized valuations (equivalently integral closedness). An integral basis gives `O_K=sum omega_i S_B`; eliminating its last coordinate gives exactly `dN` total coordinates. A degree-d field norm combines the d equations without new variables and gives degree at most `2dD`.
- For the stronger rational-integer conclusion, `c^p=a^e`, `rp+se=1` gives `a=(a^r c^s)^p`. The primitive-pth-root alternative is excluded by `p-1>d`; rational x with integral power is integral. This includes signs because p is odd.
- The eventual-positive square-shift variant is valid once B exceeds the threshold. For the odd-power variant, `K^p=-K^p`, so the same avoidance shift handles both signs. At least one of `B+x^p,B-x^p` is at least B for integer x. Sharing the witness tuple in the product is legitimate because only one factor needs to vanish. The degree bound is `2pD`, and the coordinate count remains N.
- The elementary bounded-height argument via the primitive minimal polynomial and its Mahler measure proves the required finiteness. No effective exceptional set or shift is claimed when only finiteness is given.

The proof does not construct an all-number-field detector or imply that every ring of integers is Diophantine without its stated source hypotheses. This audit verifies the mathematical use of Chebotarev and the explicit algebraic arguments; the author independently checked the cited primary theorem location.

## Addendum: smaller rationality-reflecting powers

The strengthened final lemma also passes. With `gcd(m,d)=1`, the norm identity `c^m=a^d` and integers `rm+sd=1` give `a=(a^r c^s)^m`. The remaining root of unity belongs to `mu_m(K)` and is rational under the stated hypothesis. Separately, an irrational element with rational square generates exactly a quadratic subfield, proving the necessary-and-sufficient square criterion. Thus odd-degree fields admit the degree-2 substitution; real quadratic fields admit m=3. Theorem 3 and its eventual-positive variant correctly use the same avoidance lemma with this general exponent. For even m one equation suffices because `n^m+B>=B`; for odd m the shared-witness two-factor product is necessary for both signs and has degree at most `2mD`. No incorrect irreducibility criterion for a composite binomial is used.

Reviewed final SHA256: `6fa2602dd667c1fc772e1b477afae75b19c1809ce116707ed0cd2593e238546d`.
