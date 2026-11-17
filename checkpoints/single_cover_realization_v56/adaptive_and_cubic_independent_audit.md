# Independent audit: adaptive trace classes and the cubic reference family

Date: 17 November 2026. Status: proved algebraic and arithmetic statements;
the prescribed detector-trace realization is not proved.

## Adaptive class

Audited source: `checkpoints/adaptive_trace_class_v57.tex`.
Write

\[
C=V^2+w(2-V),\quad q=2+wc^2,\quad
\delta_c=(q^2-2q-1)^2+4q(q^2-1)V.
\]

Here `c` must be an already guarded scalar function with rational value at
the selected character. Its values at other prepared characters are real.
The proposition is correct with the stated rational-scalar restriction.

At a hypothetical forbidden pole, let `nu=v_p(w)>0` be odd and
`m=v_p(V)>0`, with `p` odd. If `c=0` or `v_p(wc^2)>0`, then `q=2 mod p`
and `delta_c=1 mod p`. Otherwise `e=v_p(q)=v_p(wc^2)<0`. The two
summands have valuations `4e` and `3e+m`. Their difference is `m-e>0`,
so the first summand dominates and `delta_c` is a nonzero local square.
Its valuation need not be zero, but is even; that is exactly sufficient
for the pole implication. No height or denominator bound on `c` is used.

At a selected contact with `V=1` or `2 mod p`, the negative-valuation
case still has strict dominance. In the other case the residues are
25 and 49, nonzero squares for `p>7`. At every prepared real character,
`q>=2` and `V>0`; hence the second summand is strictly positive. There
is no claim that `q^2-2q-1` itself is positive.

The exact reference identities are

\[
\delta_c(0)=(q^2-2q-1)^2,\quad
\delta_c(1)=(q^2+1)^2,\quad
\delta_c(2)=(q^2+2q-1)^2.
\]

For the retained conditional slope `c=lambda`, the asserted limit is
`q -> 2+1/(4a^2)` when `t=a lambda`. It is rational, and
`q^2+2q-1` has no rational zero. Thus square-class openness gives the
claimed fixed-place preparation, including the two-adic place. In the
general source the nonzero limiting weight makes `v_p(q)` tend to
minus infinity. The quotient of `delta_c` by its first square summand
tends to one. This gives the same preparation, in the original order
of choices. These arguments do not give a global rational square.

## Cubic reference family

Audited certificate:
`checkpoints/general_scalar_v56/cubic_trace_rank_certificate.json`.
The curve and its section are

\[
E_w:\ y^2=x^3-(2+24w)x^2+(1+1176w)x,
\qquad P=(49,336).
\]

The substitution `x=1+24V`, `y=24Y` identifies it with
`Y^2=(1+24V)C`. Its discriminant is

\[
9216w(w-8)(1+1176w)^2.
\]

The author's standard-library verifier was read and executed. Its
division-polynomial normalizations are correct for
`a1=a3=a6=0`, and its even recurrence divides by the nonzero constant
`psi2(P)=672`. The exact factor products for `psi8`, `psi10`, and
`psi12` pass. Every nonlinear factor has a no-root certificate over
a finite projective line: no affine residue is a root, and the leading
coefficient is nonzero modulo the certificate prime. The latter check
is essential and correctly covers rational roots with a denominator
divisible by that prime.

I also independently constructed `[8]P`, `[10]P`, and `[12]P` by
affine tangent/chord addition over `Q(w)`. Their reduced abscissa
denominators have degrees 30, 48, and 70 and are nonzero rational
constant multiples of the certified `psi8^2`, `psi10^2`, and
`psi12^2`, respectively. This is a different computation from the
division-polynomial recurrence and checks its normalization and its
use in the certificate.

The complete surviving rational torsion weights are

| Weight | Exact order of P |
| --- | --- |
| `296/49` | 3 |
| `-96/49` | 3 |
| `100/49` | 4 |

The exact orders are checked by rational group addition. No other
rational specialization of a smooth fiber makes P torsion. Indeed,
the curve has the rational point `(0,0)` of order two. Mazur's torsion
classification leaves cyclic groups of even order 2, 4, 6, 8, 10, 12,
or groups `Z/2 x Z/(2n)` for `1<=n<=4`; in every case the order of a
point divides 8, 10, or 12. Thus the three checked division polynomials
cover every possible torsion order, including odd orders 3 and 5.
All three exceptional weights lie outside `0<w<=1/4`, so P has
infinite order throughout the prepared general-weight interval.

Bibliographic input: B. Mazur, *Modular curves and the Eisenstein ideal*,
Publications mathematiques de l'IHES 47 (1977), 33--186, Theorem 8,
DOI `10.1007/BF02684339`; original article at
https://www.numdam.org/articles/10.1007/BF02684339/.

## Scope and remaining gap

The rank statement gives infinitely many rational points on each
reference cubic and therefore infinitely many rational candidate
trace values. It does not show that the abscissa
`1+24 Tr(W^{-1})` of an actual detector tuple lies on that curve.
Neither this audit nor the adaptive-class proposition proves a
21-variable or 9-variable definition.

Reproducible independent checker:
`check_adaptive_and_cubic_audit.py`; output:
`adaptive_and_cubic_audit_certificate.json`.
