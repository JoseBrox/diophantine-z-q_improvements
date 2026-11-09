# Independent audit of the quadratic input obstruction

Audited 9 November 2026 against `work/few_variables/quadratic_input_obstruction_20261109_v12.tex` and its standard-library checker. The proof passes. The finite checker was rerun, writing `quadratic-input-independent-audit.json` in this directory; all checks passed.

## Integrality reflection

For an integer quadratic `q(X)=AX^2+BX+C` with `A != 0`, rational integrality reflection is equivalent to `|A|` squarefree and `A | B`. Necessity follows first from `q(-B/A)=C`, then from the nonintegral input `1/p` if `p^2 | A`. For sufficiency, writing `B=Ak` and a reduced input `u/v`, integrality implies `v^2 | A u(u+kv)`; both factors after `A` are prime to `v`, so `v^2 | A`, whence `v=1`. Signs of `A` cause no issue. Constants and linear polynomials are handled correctly in the paper.

## Local cases

The stated nonsquare residues for the contact polynomial `r(T)=T(T-1)(T-2401)(32T+343)(2T-1)` are correct: `t=5 mod8` gives valuation 4 and odd part 3 mod8; `t=7 mod8` gives valuation 2 and odd part 5; `t=9 mod16` gives valuation 6 and odd part 3. No contact factor vanishes in these classes.

Odd-valued reflection quadratics reduce correctly to the final normalized case `Ay^2+c`, with `A=6 mod8`, `c=3 mod8`, `A+c=1 mod16`. Here `(1-c)/A` is an odd two-adic square. For an odd root `y0` of `Ay0^2+c=1`, choosing an integer `y-y0=16 mod32` gives valuations `v2(y-y0)=4`, `v2(y+y0)=1` and `v2(q(y)-1)=6`. Since `v2(2400)=5`, the other even contact has valuation 5; all remaining contact factors are odd. Thus `v2(r(q(y)))=11`, which is impossible for a square. The approximation by an ordinary integer follows from reduction of `y0` modulo 32.

The finite checker covers all relevant classes modulo 512, more than the 2-adic precision required for the odd parts, and all 128 surviving coefficient pairs modulo 128. Its witnesses modulo 32 certify `Ay^2+c-1=64 mod128`, which forces the asserted valuations for every lift.

## Scope

The theorem is unconditional and concerns integer-coefficient input maps, the odd-value condition, and this particular contact polynomial. It does not constrain arbitrary Diophantine defining polynomials, unrestricted parity, rational-coefficient input maps, or additional scalar corrections.

## A sharp corollary when positivity is included

Suppose in addition that `q(x)>0` for every integer `x`. A nonconstant integer polynomial with this property has positive leading coefficient and even degree. The obstruction to degree at most two therefore gives degree at least four in this specified class.

The existing map `q(X)=216X^4+450459` attains degree four. It is positive and is 3 modulo 8 at every integer. For a reduced rational `u/v`, integrality of its value gives `v^4 | 216`; because `216=2^3 3^3`, this forces `v=1`. If `t=3 mod8`, both even contact factors have valuation one. Their odd parts differ by `1200=0 mod8`, so their product is 1 modulo 8. The three odd contact factors have product `3*7*5=1 mod8`. Consequently `r(t)` has valuation two and odd part one modulo eight, and is a square in `Q_2`. Thus degree four is exact only for these combined scalar-map requirements.
