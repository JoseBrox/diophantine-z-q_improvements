# Independent source-transfer audit

The two manuscripts audited are
`../general_scalar_v56/burungale_general_transfer_20261117_v56.tex`
and the simpler replacement
`../general_scalar_v56/burungale_scalar_transfer_20261117_v56.tex`.

## Scalar-only version

The change

`rho*=7 A_L r/(1+7 C_L r)^2`

preserves every consumed odd contact valuation outside the existing
exceptional set, which includes seven. At a positive odd valuation of
`r`, both denominators are units. At the consumed prime `ell=76249`,
negative input valuation makes both denominators have valuation `v(r)`;
integral inputs are covered by a complete finite residue certificate.
An independent certificate uses the polynomial gcd with `X^ell-X`
instead of the author's enumeration. Its checker is
`check_scalar_transfer_independent.py`.

For integer inputs one must check cancellation before asserting a square
reduced denominator. Write `D=1+7 C_L r`. Then `gcd(r,D)=1`. For the
aligned scalar, every prime of `A_L` other than `ell` divides `C_L`, so
is a unit in `D`; `ell` is covered by the residue certificate. For the
original scalar the coefficient primes are `2,3,17,ell`: `C_L` is even,
`r=0 mod3`, and `17` divides `C_L`, so the first three are units in `D`,
while `ell` is again certified. Also `D=1 mod7`. Thus the numerator and
denominator are coprime, and reduction leaves a square denominator.
The denominator is seven-adically a unit and the numerator is divisible
by seven. At two the squareclass is
multiplied by seven and the old valuation (four or twelve) is preserved.
The fixed coefficient change alters height constants by an absolute
amount, with no new dependence on the selectable exponent `L`.

On real inputs `C_L r>=1`, so the exact scalar ratio is at most `7/16`.
The original bound `rho<36/76249<1/56` therefore applies. On the
prepared selected character, `R_j<2`, both detector slots lie in
`[1,2)`, and the reciprocal trace exceeds one. Consequently
`0<b_j<8 rho*<1/7<1`. The input for the intrinsic theorem is `d=b_j`.

Ordered local preparation must include the support of `rho*` and
`1+rho*` before all auxiliary choices. This is a temporary avoidance
set, not an enlargement of the global height-exception set. The latest
manuscript explicitly uses this ordering. At those places the contact
functions tend to one and scalar comparisons can be made arbitrarily
small, so both inputs have square denominator and the required local
two-adic class. No seven-adic odd pole survives.

Every geometric point-algebra character is real and has positive
detector factors, so the inputs are nonzero at all characters. It is
unnecessary to bound the other character values by one: the intrinsic
radicand is nonzero as a polynomial at every nonzero input, including
input one. Its norm is a nonzero polynomial. The proved density of
actual witness pairs supplies simultaneous avoidance of this norm and
all retained finite guards. Thus the one-coordinate encoder is valid.

The scalar-only transfer passes this audit under the original explicitly
retained source premises and Burungale Theorem B. The coordinate count
remains 25. No 21-variable or complete degree bound is deduced.

## Coefficient-seven physical weight version

The alternative coherent weight `w=u/(1+7u)^2`, with `d=7b`, also
passes. It must replace the weight in every detector factor and every
scalar comparison. Odd valuations outside seven become their positive
absolute values exactly as before. At seven the limiting weight has
nonnegative valuation because the original scalar has square denominator.
The bound `w<=1/28` and selected reciprocal trace greater than one imply
`b<1/7`. The same temporary-set ordering is required, now including
the support of `1+7 rho`. The scalar-only version avoids this extra
change to the physical weights.
