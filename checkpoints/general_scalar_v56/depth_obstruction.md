# Obstruction to simultaneous deeper formal preparation

This negative checkpoint concerns the proposed reciprocal-order-three
preparation, not the corrected `ell_8` source.

Let `p=76289`, let `K=Q(sqrt(2))`, and retain

\[
E:y^2=x^3-(11-6\sqrt2)x,
\qquad
P=((57-28\sqrt2)/8,(-660+417\sqrt2)/32).
\]

At the two primes above `p`, the reductions of `P` have orders
`18989` and `9578`. Each order is coprime to `p`, and the orders are
coprime to one another. At each place the corresponding minimal formal
return has parameter `z=-x/y` of valuation exactly one. The exact
certificate records its nonzero coefficient modulo `p^2`.

If `m` is the reduction order at one place, membership of `[h]P` in
the first formal group requires `m | h`. Write `h=mk`. Formal
multiplication at this good odd prime gives

\[
v_p(z([h]P))=1+v_p(k)=1+v_p(h).
\]

Consequently depth at least two forces `p | h`. Requiring depth at
least two for `[h-1]P` at the conjugate place similarly forces
`p | h-1`. These demands are incompatible. The original depth-one
congruences are compatible because the two reduction orders are
coprime; orienting the even order on the primary side is also
compatible with the usual fixed even divisibility of `h`.

The checker `check_precision_transfer.py` verifies the two finite-field
point orders, Hensel lifts, and projective multiplication modulo `p^2`.
It confirms that both first-return parameters are nonzero modulo
`p^2`. This excludes an unconditional upgrade by deeper local CRT at
all allowed comparison primes. It does not exclude selecting a
different, specially constrained family of primes.
