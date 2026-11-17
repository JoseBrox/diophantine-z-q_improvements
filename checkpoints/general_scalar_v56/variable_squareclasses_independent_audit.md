# Independent audit: variable native square classes

Audited manuscript: `../variable_classes_v57/variable_squareclasses.tex`.
The stated arithmetic realization remains unproved. This audit concerns
the support budget, soundness criterion, guards, count, and exact
parameter choices.

## Support and lost contact primes

For a fixed integral homogeneous form `G` of even degree `k`, write
the primitive common-denominator representation `(beta,T)=(a/c,b/c)`.
Then `G(beta,T)=G(a,b)/c^k`. The denominator contributes even valuations,
including after reduction. Hence every odd support prime divides the
integer `G(a,b)`, giving

`log r_S(G(beta,T)) <= k h(1:beta:T)+log ||G||_1`.

This includes negative odd valuations. Multiplication by a fixed
S-unit does not change support outside S. Finite menus of fixed forms
have a uniform constant and use the largest degree.

At a contact prime outside the odd support of `delta_j`, the allowed
class still gives even valuation of the native radicand. The native
obstruction and original elliptic comparison are therefore unchanged.
For nonzero numerator `N=num(X-n)`, the precise divisibility is

`M_j/gcd(M_j,r_S(delta_j)) | N`.

Both radicals are squarefree, so this implies
`M_j <= |N| r_S(delta_j)`. The elementary estimate
`|N| <= exp(h(X))(1+|n|)` and the exact reduced expression for
`beta=X^2+B` give `2h(X)<=h(beta)<=E_h`. Thus the lost-prime
term is exactly the stated `k_j E_h`, with no factor two missing.

## Height constants and B-uniformity

The retained binary-power inequality gives
`alpha_e E_h <= h(beta^e+T^e)+O(1)` for positive even e,
`alpha_e=e/kappa-3>0`. Since `a_1=t_1/t_0`, its height is at most
`h(t_0)+h(t_1)`. Combining with the contact-height bound gives

`(alpha_e gamma-1-k_0-k_1)E_h <= 2log(1+|n|)+O(1)`.

All forms, menus, exponents and weak-abc constants are fixed. The
appearance of B inside beta adds no constant depending on B. The
trace-height theorem bounds `n^2` by a constant times `E_h` plus a
constant. Strict absorption therefore bounds n and E_h uniformly,
contradicting `E_h>=h(beta)>=log B` for sufficiently large B.

The single-cover argument uses the previously proved mixed-power
bound with m=1 and gives the exact coefficient
`q=C_(kappa,d)/(alpha_e gamma)`. Its absorption requirement is
`q(k+1/2)<1`, as stated. The same B-uniformity argument applies.

## Guards and census

For `delta=beta^2+T^2`, positivity is automatic since beta is positive.
At a prepared real point-algebra character, the native radicand is
positive. Therefore multiplying it by a positive S-unit and delta
gives a nonzero quadratic radicand at every character. No additional
free coordinate is needed. Each branch uses the existing quadratic
encoder, and a finite product of branch polynomials uses the same
encoder variable. Ranks 256 and 128 and the nine-coordinate censuses
are correct.

The two-cover realization statement should explicitly require the
prepared real and whole-character guard locus (for example lambda>1,
which gives both arguments>1), or explicitly require all new
radicand norms to be nonzero. Merely finding an actual square at one
rational character is insufficient to invoke the automatic positivity
argument for every character. The single-cover argument is automatically
greater than one, so its new positivity is automatic. Root was notified
of this wording refinement.

## Improved ordinary-abc rows

The original rows all pass their exact checks. Ordinary abc also gives:

* Two covers: `kappa=36/35`, `e=6`, `alpha=17/6`, `gamma=16/9`,
  product `136/27`, absorption `135/136<1`.
* One cover: `kappa=251/250`, `e=14`, `d=8`,
  `q=20601327/51566684`, absorption `103006635/103133368<1`.
  Its height-argument degree is 224.
* The less tight choice `kappa=301/300`, `e=14`, `d=8` has the same
  degree 224 and absorption `330111215/332371512<1`.

For two varying quadratic classes, even e=6 is minimal in this
criterion: for kappa>1, `alpha_e gamma<2(e-3)`, which must exceed five.

For one varying quadratic class, degree 224 is minimal among the
stated m=1 even-power criteria, allowing any kappa>1. Indeed

`dC_(kappa,d)/d kappa = 2d(3d+2)/((2-kappa)d-4kappa)^2 > 0`,

while `alpha_e gamma` decreases with kappa on the positive domain.
The best possible limit is therefore kappa=1. In that limit
`d>=6`, `e>=4`, both even. A complete finite check of pairs with
`ed<112` gives no strict absorption; `(18,6)` at product 108 is an
equality. The pair `(14,8)` at product 112 is strict at kappa=1 and
at the displayed rational exponents greater than one.

This is an optimization of a height argument. It is not a lower bound
on the degree of defining polynomials and does not prove realization.

`check_variable_classes_independent.py` reproduces the exact
inequalities, the improved rows, and the finite optimization.
