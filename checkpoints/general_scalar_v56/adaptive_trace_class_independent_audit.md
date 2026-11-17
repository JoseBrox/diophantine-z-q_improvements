# Independent audit: classes from retained source functions

**PASS.** Audited `../adaptive_trace_class_v57.tex` and the family

\[
q=2+wc^2,\qquad
\delta_c(V)=(q^2-2q-1)^2+4q(q^2-1)V.
\]

The rationality requirement on the selected value of `c` is essential.
It may be an already retained rational coordinate, a guarded rational
function, or a generator of the original point algebra whose selected
character is rational. It is not an additional free rational parameter,
a raw K-valued function, or a newly introduced root with no rational
character audit.

At a hypothetical bad pole outside the exceptional set, let
`nu=v_p(w)>0` be odd and `m=v_p(V)>0`. For nonzero rational `c`,
`v_p(wc^2)` is odd and hence cannot be zero. If it is positive,
`q≡2` and `delta_c≡1`. If it is negative, write `e=v_p(q)<0`.
The two terms have exact valuations `4e` and `3e+m`. Their difference
is `m−e>0`, so the square first term dominates, and the quotient by
that square lies in `1+p Z_p`. This proves even valuation, in fact
local squareness, without a height bound on `c`.

At a selected contact, `v_p(V)=0`. The same argument handles negative
`e`; the other case has residues 25 or 49 when `V≡1` or 2. The stated
condition `p>7` excludes the only exceptional residue primes. If `c=0`,
the family is exactly `1+24V` and the same assertions hold.

At every prepared real character, `q>=2`, `V>0`, so the second term
is strictly positive. This also covers zeros of the first square.
No guard on `q`, `q^2−1` or `q^2−2q−1` is required. All denominators
come from the already retained functions `w,V,c`. Thus the numerator
norm is automatically nonzero at the prepared characters, and the
terminal quadratic extensions retain the same rank and coordinate count.

## The explicit slope choice

For `c=lambda` in the conditional source,

\[
w\lambda^2\longrightarrow 1/(4a^2),\quad
q\longrightarrow 2+1/(4a^2),\quad V\longrightarrow2.
\]

The scales `a` are fixed, nonzero rational values before slope selection.
The limiting radicand is `(q^2+2q−1)^2`; its root is a nonzero rational
number because the polynomial has roots `−1±sqrt(2)`. The neighborhood
of this nonzero square is open in every `Q_p`, including two and any
prime dividing the square root. The source permits the required fixed
precision before its final index refinement.

For the general source, `w` tends to a fixed nonzero value and
`v_p(lambda)` tends to minus infinity. Therefore `v_p(q)` tends to
minus infinity, and the relative correction to `(q^2−2q−1)^2` has
valuation tending to plus infinity. It is enough that `V` remains in
its fixed prepared neighborhood; exact convergence `V→2` is not
needed. This includes two, where the correction can be made divisible
by eight. The same choice can retain the already prescribed local
trace-conic square neighborhood.

No soundness contact is lost, so the original unconditional Lucas
height exponents and conditional height constants remain unchanged.
The result supplies an admissible family of variable square classes;
it does not prove actual rational realization.

`check_adaptive_trace_class_independent.py` verifies the three square
identities and exact local valuation fixtures. Its certificate is
`adaptive_trace_class_independent_certificate.json`.
