# Independent audit of the conditional intrinsic-pole transfer

Audited source:
`../single_cover_realization_v56/conditional_burungale_transfer.tex`,
in its final form retaining the original physical weight
`w=F(t)/(4(t-1)^8)` and original fast product `W`, and using intrinsic
pole input `d=7b`, `b=4w/Tr(W^-1)^2`.

## Local soundness and original height argument

For primes outside the unchanged exceptional set, odd valuations of
`w` occur at odd positive contacts of `F`. At such a contact
`v_p(w)=v_p(F)=nu>0`. Each fast factor has the distinct-valuation
formula `min(0,2v(C_i)-nu)<=0`. The intrinsic all-prime obstruction
for `d=7b`, with seven exceptional, gives the same trace inequality
as the old pole predicate. It forces every test to have positive
valuation at a common local slot. The invertible transformation of
the final two comparisons recovers the original local index test.

The root point, both arguments and their height scales have not
changed. Hence both ordinary/weak-abc height arguments retain their
stated exponents and sufficient-shift contradiction. No auxiliary
index or new height term has entered the proof.

## Complete preparation

All scales are fixed after the integer root point and before prime
selection. Adding seven to the temporary preparation set is allowed
by the retained denominator-divisibility/avoidance theorem. Seven
is already globally exceptional, so this changes no height constants.

Uniformly on the fixed point-function neighborhoods,

`F(t) ~ t^6`, `w ~ 1/(4t^2)`, `W-1=O(t^-6)`, and `V -> 2`.

At two, sufficiently deep denominators make `w` a local square with
positive even valuation at least four, and `v_2(V)=1`. Therefore
`b` is a 2-adic square at the same depth and `d=7b` has class seven.
At seven, the same limit gives positive even valuation of `w` and
unit `V`, hence `b` is 7-integral. Multiplying `b` by seven does not
create an odd negative valuation there.

At the real embeddings the same limits give positive weights tending
to zero, both selected detector slots in `[1,2)`, and `V>1`. Thus
one can require `0<b<1/7` and consequently `0<d<1`.

Fresh selected contacts have the inherited test depths, a unit
reciprocal trace and positive odd valuation of `b`. The unchanged
prime-times-square factorization and fixed local preparation prove
square reduced denominators at every prime. Hence the actual `d_j`
satisfy all intrinsic Burungale preparation hypotheses simultaneously.

## Whole algebra, finite roots, and count

Every prepared point-algebra character is real, `F(t)>0`, and all
fast detector factors are at least one. The traces and inputs are
therefore units at all characters. No bound below one is needed at
the other characters, and the value `d=1` is allowed by the unguarded
intrinsic equation.

For each character `d=c!=0`, the radicand is a nonzero polynomial in
the two pole coordinates, with leading coefficient
`c(c+v^2)^2` in `s`. Its point-algebra norm is therefore nonzero.
The intrinsic density theorem permits simultaneous avoidance of
these radicand norms and all retained guards. Two terminal quadratic
extensions have rank factor four, so total finite rank is
`4^3*4=256`. The existing one-coordinate encoder applies.

The free-coordinate count is `1+6+1+4+1=13`; the final input factor
includes zero. This passes the independent proof audit under the
explicitly retained arithmetic premises and Burungale Theorem B.
It proves neither a nine-variable realization nor a numerical bound
for the full determinant degree.
