# Independent audit of the eleven-coordinate derivative construction

## Verdict and scope

**PASS.** The complete manuscript
`../single_cover_realization_v56/derivative_detector_11_v59.tex`, with
sixteen shifts, `M=(X²+B)^4+T^4`, `a=M³`, and
`u=-32aF/F_a=-16 G/G_A`, proves its eleven-coordinate statement under
ordinary rational abc and the arithmetic theorems explicitly retained
there. The argument gives no unconditional reduction, no nine-coordinate
construction, and no full determinant-degree bound. The coefficient
shift must be sufficiently large; its threshold is not numerically
specified.

This audit independently read the full source, the local comparison in
`papers/conditional_few_variables/direct_input13_20261110_v22.tex`, the
exact Sun-order compatibility in
`papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex`,
the all-character and encoder proofs in
`papers/finite_algebra/unit_norm_20261114_v28.tex`, and the intrinsic
transfer in
`papers/pole_parameters/conditional_intrinsic_transfer_20261117_v57.tex`.
The primary homogeneous-form abc consequence was independently checked
in Rudnick–Sarnak–Zaharescu, Inventiones 145 (2001), Appendix A.2,
equation (A.2), at https://www.math.tau.ac.il/~rudnick/papers/rsz.pdf.

## 1. The radical estimate and its uniform constants

For a fixed product `G0(X)=prod(X+c_i)` of distinct integer linear
factors and `x=A/B` reduced, the numerator is
`N=prod(A+c_i B)`, coprime to `B`. The homogeneous-form consequence
of ordinary abc yields
`log rad(N)>=(k-2-epsilon)h(x)-O(1)`. The elementary numerator bound
is `log|N|<=k h(x)+O(1)`. Consequently the support of multiplicity
at least two costs at most `(2+epsilon)h(x)+O(1)`, and the support
of multiplicity exactly one has logarithm at least
`(k-4-2epsilon)h(x)-O(1)`. All forms and shifts are fixed. These
constants have no dependence on the later coefficient shift `B`.

Write `x=a-z`, `y=a+z`, and interchange them so `h(x)>=h(y)`.
After omitting the numerator and denominator support of `M`, at cost
at most `2h(M)`, the scalar `2ka` is a local unit. A simple
`G0(x)` contact forces both `x` and `y` integral. If `G0(y)` is a
unit, `F_a` is a unit and `v(u)=1`. If `v(G0(y))>=2`, the preceding
multiple-support bound applies. At a double simple collision,
`F=LRK` with `K` a unit and
`F_a=(L+R)K+LRK_a`. Unless `p²` divides `2M^m+c_i+c_j`, this has
valuation one and again `v(u)=1`. The derivative is taken with
`z` fixed, not with `t=a²-z²` fixed.

The nonzero collision sums are fixed. For each reduced
`s_j=p_j/q_j`, the form
`AB prod(2q_j A^m+p_j B^m)` is squarefree, of degree `rm+2`.
The same ordinary-abc consequence bounds its repeated-prime support,
after removing `AB`, by `(2+epsilon)h(M)+O(1)`. Cancellations at
denominator primes affect only fixed coefficient primes. The zero
collision sums cannot occur at a prime where `a` is a unit.
The manuscript explicitly excludes vanishing nonzero-sum factors;
in the source `a>8` makes them nonzero automatically.

Combining the losses gives exactly

`log r_odd^+(u) >= ((k-6-3epsilon)/2) h(a²-z²) -(4+epsilon)h(M)-O(1)`.

The final use of `h(xy)<=h(x)+h(y)<=2 max(h(x),h(y))` is in the
correct direction. No extra `h(M)` loss is needed locally below.

## 2. The transformed detector and soundness

For odd `nu=v_p(u)`, distinct parity of the denominator terms gives
`v(D_i)=max(2v(C_i),-nu)` for `D_i=C_i²/(1+u C_i²)`.
This includes zero tests, whose valuation is infinite. If `nu>0`,
positive valuation of `D_i` is equivalent to positive valuation of
the original test. If `nu<0`, every term `D_i²/u` has valuation at
least `-3nu>0`, even when the original test has a pole.

At every positive odd valuation outside the fixed exceptional set,
the physical weight has valuation `nu`. The intrinsic pole excludes
a negative odd valuation of `7b`. With `q` the largest local
valuation of `W`, the inequalities
`1<=v(b)<=nu+2q` force each transformed test at the successful
place to have valuation greater than `nu/4`. The six original tests
therefore satisfy precisely the retained local formal-comparison
theorem. The draft uses its original target `C6=r-X`, which is
valid; the symmetric replacement from later papers is unnecessary.
It follows that every such prime divides the reduced numerator of
`X-n`, including primes in the support of `M`. The support of `M`
was discarded only in the *lower* radical estimate, not in the
local implication.

For `X=p/q` reduced and integer `B>=3`,
`beta=(p²+Bq²)/q²` is already reduced, since
`gcd(p²+Bq²,q²)=1`. Its positive numerator dominates both `p²`
and `q²`; hence `2h(X)<=h(beta)` exactly, with no cancellation
or `B`-dependent additive term. Also `h(beta)>=log B`.

With `kappa=1001/1000` and `epsilon=1/100`, the exact constants are
`alpha=997/1001`, `Q=1002/995`, `gamma=997/200`, and `C=401/100`.
The absorbed term is
`Q(C+1/(2alpha))=225373347/49600750`, with positive gap
`87545567/198403000` below `gamma`. The signed-height denominator
is `6-5kappa=199/200>0`. Thus the radical upper bound from the
input numerator yields `h(t)<=O(log(1+|n|))+O(1)`; the binary-power
and trace-height inequalities then bound `n`, `h(t)`, and the
joint root/input height independently of `B`. The sufficiently
large fixed shift contradiction is valid.

## 3. Ordered completeness and the new denominator primes

For a fixed nonzero integer input, `A=[n]P`, `M`, and `a` are
fixed before Sun's theorem is applied. Temporary finite preparation
includes their numerator/denominator support. This set is used only
for completeness and does not enlarge the fixed exceptional set of
the soundness estimates.

Choose a nonexceptional auxiliary return in `64 Z P`, avoid the
finitely many point/difference guards and zeros of nonidentically
zero tests, and choose small finite-place neighborhoods. If a test
is identically zero, it causes no restriction. The fixed congruence
modulus preserves these neighborhoods and is chosen before primes.
For every real ordinate-sign branch, the abscissas, hence `M,a,u`,
are unchanged. For `z>a+8`, every factor of `F` is negative and
every summand of `F_a/F` is negative, so `u>0`.

Symmetry gives `F~z^32`, `F_a~-32az^30`, and `u~z²` at every
fixed place. The leading square, including at two, gives arbitrarily
deep square preparation. The transformed tests tend to zero and
`W` tends to one uniformly on the fixed neighborhoods. At two,
`b` is a local square with valuation at least four; at seven it is
integral. At real places `b` tends to zero and can be made less
than `1/7`.

For an integer `D` clearing the fixed contacts, the thirty-two
distinct coefficients `+/-D²(a+c_i)` meet the retained form of
Sun's theorem. Its Gaussian-order conditions give exactly the
compatible `h=0` / `h=1` conjugate congruences and avoid the odd
part of the earlier neighborhood modulus. The two-adic compatibility
is supplied by the original `64` divisibility. Refinement preserves
the real neighborhood and all earlier finite conditions. At a fresh
selected prime, one linear numerator factor has valuation one,
`F_a` is a unit, and `v(u)=1`. The successful tests give `W=1`
modulo the prime; the other reciprocal product is zero or one.
Thus the trace is a unit and `v(b)=1`.

Away from the temporary set, every nonselected integral-slope prime
has `F` a unit and `F_a` integral, so `v(u)<=0`. Every slope
denominator prime has `v(u)=2v(z)`, even. The fixed-set preparation
gives the same even valuation at primes of `a` and `2k`. Most
importantly, a new negative odd denominator valuation requires no
auxiliary-index congruence: the new detector makes both products
equal to one modulo that prime, so the trace equals two and
`v(b)=-v(u)>0`. If `v(u)` is even, `v(w)` is even, including the
case `v(u)=0` with extra zeros of `1+u`. Division by the trace
square preserves parity. This proves the square reduced denominator
of `b`; preparation at seven ensures that of `7b` as well.

Consequently the actual input `eta=7b` has all the required
intrinsic hypotheses, including `0<eta<1`, the square denominator,
`eta in 7 Q_2²`, and dyadic depth at least four. There is no
post-prime choice whose denominator primes need to be inserted
back into the earlier Sun modulus.

## 4. Whole-character guards and the coordinate count

Each point block has four real characters at a prepared tuple;
these independently change ordinate signs and leave abscissas
fixed. The existing signed-index guard proof applies for `h>2`
and every nonzero integer `n`, including `n=1,-1`. The new factors
`1+u C_i²` are strictly positive at every character, every factor
of `W` is at least one, and the trace and pole input are positive.
Thus every new denominator and every product/input norm is a unit.

At a character with `eta=c!=0`, the intrinsic radicand polynomial
is nonzero because its leading coefficient in `s` is
`c(c+v²)²`. The actual witness-pair density therefore avoids the
nonzero product over all characters. It is unnecessary to impose
`c<1` or `c!=1` on other characters. The final quadratic block is
etale, though its nonselected characters can be nonreal; the
retained separator theorem explicitly permits this.

The point algebra has rank `4³=64`; one pole root gives rank
`128`. There are the input, six point coordinates, the one slope,
two free intrinsic parameters, and one encoder coordinate, totaling
**eleven**. No finite root, guard, height quantity, detector function,
or trace requires a further unrestricted coordinate. The final
input factor includes zero. Only local expression degrees are
claimed in the manuscript; no unverified full determinant estimate
is introduced.

## 5. Exact verification

`check_derivative_source_independent_v59.py` uses exact rational
arithmetic and a logarithmic-derivative evaluation independent of
the author's symbolic differentiation. Its certificate checks the
normalized quotient, local leading square, both signs of odd
valuation, both-slot trace behavior including arbitrary poles,
zero-test edge cases, valuation-zero denominator cancellation,
the uniform input-height calculation, the strict contraction, and
the rank/count. The external arithmetic existence statements and
the universal arguments above are proved or cited separately,
not inferred from finite fixtures.
