# Independent audit: a pole-cancelling quotient height

Date: 17 November 2026.

Audited manuscript:
`checkpoints/general_scalar_v56/pole_cancelling_quotient_height_v59.tex`.

**Result: PASS, with its explicit global-completeness gap retained.**

The source uses `U=[n]H`, `beta=X^2+B`, and
`Y=X^2 x(U)-x(H)`. The sum/product height inequality gives

`h(Y)+2h(X) >= 2(n^2-1) hhat(H)-2 C_E-log 2`.

Since `h(1:beta:Y)` dominates both `h(Y)` and `h(beta)>=2h(X)`,
the claimed lower bound with half these constants follows. All constants
are uniform in the positive integer coefficient shift B. The assumption
X nonzero is needed when dividing by X^2 and is stated. The cases n=+-1
cause no defect: the index-height lower bound becomes zero, and the final
absorption still bounds h(beta) independently of B for false inputs.

I recomputed the formal expansion independently. In parameter t=-x/y,

`x=t^-2+d^2 t^2+O(t^6)` and
`log_E(t)=t-(2d^2/5)t^5+O(t^9)`.

Thus `[n]t=n t+(2d^2/5)(n^5-n)t^5+O(t^9)`, and substitution gives

`n^2 x([n]H)-x(H)=d^2(n^4-1)t^2/5+O(t^6)`.

The local integrality claim is correctly restricted to primes not dividing
10dn. There n is a unit, so the inverse Laurent series is integral after
its leading term; the cancellation removes the pole. Negative n has the
same expansion. The identity is identically zero for n=+-1.

For the second derivative pole, the binary-power and signed-height
inequalities give alpha=997/1001 and Q=1002/995. With gamma=997/200
and C=401/100, the exact margin is

`gamma-Q*(C+1/(2alpha))=87545567/198403000>0`.

The local one-slot balanced detector supplies divisibility of the reduced
numerator of X-n at each positive odd valuation outside a fixed finite set.
The resulting inequality bounds `h(1:beta:Y)` by a constant multiple of
`log(1+|n|)+1`; the canonical-height lower bound then bounds n, and hence
beta, uniformly in B. The large-B contradiction is valid.

This is a soundness theorem for a candidate source. The manuscript does not
claim that local preparation at the limiting value beta^e controls the new
positive odd primes of the actual value M(H). That global simultaneous
realization is still missing, so this does not establish nine variables.
